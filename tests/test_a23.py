#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# SPDX-License-Identifier: GPL-3.0-or-later
# ==========================================================================
"""Pruebas del motor REM A23 (respiratorio). Datos SINTÉTICOS. Correr:
    python tests/test_a23.py"""

import sys
import tempfile
from datetime import date
from pathlib import Path

import openpyxl

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
import _aislar_cache   # noqa: E402,F401  (PRIMERO: nunca tocar el ~/.autorem real)

import modulos.rem_a23_respiratorio as a23   # noqa: E402

_TMP = Path(tempfile.mkdtemp(prefix="autorem_a23_"))

_HDR = ["NUMERO TIPO IDENTIFICACION", "FECHA ATENCION", "ACTIVIDADES", "DIAGNOSTICOS",
        "INSTRUMENTO", "TIPO ATENCION", "SEXO", "SECTOR", "NACIONALIDAD",
        "PUEBLO ORIGINARIO", "FECHA DE NACIMIENTO", "NOMBRES", "APELLIDO PATERNO",
        "APELLIDO MATERNO", "AÑOS"]


def _mk(rows):
    """rows = lista de dicts parciales (claves = subset de _HDR)."""
    p = _TMP / "aten.xlsx"
    wb = openpyxl.Workbook(); ws = wb.active
    ws.append(_HDR)
    for r in rows:
        ws.append([r.get(h, "") for h in _HDR])
    wb.save(p)
    return p


def _quiet(*_a, **_k): pass


def _fer():
    rows = [
        # RUN A: bronquitis (J20) por médico + autocuidado/control sala por kine
        {"NUMERO TIPO IDENTIFICACION": "A", "FECHA ATENCION": date(2026, 7, 10),
         "DIAGNOSTICOS": "J20.9 Bronquitis aguda", "ACTIVIDADES": "Consulta Sala (IRA/ERA)",
         "INSTRUMENTO": "Médico", "FECHA DE NACIMIENTO": date(2000, 7, 15), "SEXO": "Hombre",
         "NACIONALIDAD": "Chilena", "PUEBLO ORIGINARIO": "Ninguno", "SECTOR": "Rojo"},
        {"NUMERO TIPO IDENTIFICACION": "A", "FECHA ATENCION": date(2026, 7, 12),
         "ACTIVIDADES": "Control Sala (IRA/ERA) - Autocuidado", "INSTRUMENTO": "Kinesiólogo(a)"},
        # RUN B: IRA alta (J0) + consulta de morbilidad por médico -> Morbi
        {"NUMERO TIPO IDENTIFICACION": "B", "FECHA ATENCION": date(2026, 7, 5),
         "DIAGNOSTICOS": "J06.9 IRA alta", "INSTRUMENTO": "Médico",
         "TIPO ATENCION": "Consulta de morbilidad", "NACIONALIDAD": "Venezolana"},
        # RUN C: junio (fuera de la ventana de julio)
        {"NUMERO TIPO IDENTIFICACION": "C", "FECHA ATENCION": date(2026, 6, 20),
         "DIAGNOSTICOS": "J06 IRA", "INSTRUMENTO": "Médico", "TIPO ATENCION": "morbilidad"},
        # RUN D: espirometría por enfermería
        {"NUMERO TIPO IDENTIFICACION": "D", "FECHA ATENCION": date(2026, 7, 8),
         "ACTIVIDADES": "Espirometría basal", "INSTRUMENTO": "Enfermero(a)"},
    ]
    fer = a23.procesar(_mk(rows), mes=(2026, 7), log=_quiet)
    return fer.set_index("RUN")


def test_indicadores_mes():
    f = _fer()
    assert set(f.index) == {"A", "B", "C", "D"}
    assert f.loc["A", "REMA23 Bronquitis Aguda"] == "SI"
    assert f.loc["A", "REMA23 Autocuidado"] == "SI"
    assert f.loc["A", "REMA23 Control SALA Kine (act)"] == "SI"
    assert f.loc["A", "REMA23 Ira Alta"] == "NO"          # J20 no contiene J0
    assert f.loc["B", "REMA23 Ira Alta"] == "SI"
    assert f.loc["B", "REMA23 Morbi respiratoria"] == "SI"   # médico+morbilidad+base resp
    assert f.loc["D", "REMA23 Espirometría (act)"] == "SI"


def test_ventana_de_mes():
    f = _fer()
    # C solo tiene atención en junio -> no atendido en julio, todo NO
    assert f.loc["C", "¿Atendido 1 mes?"] == "NO"
    assert f.loc["C", "REMA23 Ira Alta"] == "NO"
    assert f.loc["A", "¿Atendido 1 mes?"] == "SI"


def test_demografia():
    f = _fer()
    assert int(f.loc["A", "Edad"]) == 26                  # DOB 2000-07 al 2026-07
    assert f.loc["A", "¿Originario o Migrante?"] == "NO"   # chilena, pueblo Ninguno
    assert f.loc["B", "¿Originario o Migrante?"] == "Migrante"  # Venezolana


_OHDR = ["NUMERO TIPO IDENTIFICACION", "FECHA ATENCION", "INSTRUMENTO", "SEXO", "FECHA DE NACIMIENTO",
         "1.- ¿PADECE DE SÍNDROME BRONQUIAL OBSTRUCTIVO?", "2.- ¿ES RECURRENTE?", "3.- ESTADO", "4.- GRAVEDAD SBOR",
         "9.- ¿PADECE DE ASMA BRONQUIAL?", "10.- ESTADO", "11.- GRAVEDAD ASMA BRONQUIAL", "13.- ESTADO DE CONTROL ASMA",
         "12.- FECHA DEL PRÓXIMO CONTROL",
         "14.- ¿PADECE ENFERMEDAD PULMONAR CRONICA?", "16.- TIPO EPOC", "17.- ESTADO", "19.- ESTADO DE CONTROL EPOC",
         "99.- RESULTADO ENCUESTA CALIDAD DE VIDA"]
_OKEY = {"RUN": 0, "FECHA": 1, "INSTR": 2, "SEXO": 3, "FNAC": 4,
         "SBOR_p": 5, "SBOR_rec": 6, "SBOR_est": 7, "SBOR_grav": 8,
         "ASMA_p": 9, "ASMA_est": 10, "ASMA_grav": 11, "ASMA_ctrl": 12, "ASMA_prox": 13,
         "EPOC_p": 14, "EPOC_tipo": 15, "EPOC_est": 16, "EPOC_ctrl": 17, "CDV": 18}


def _mk_otros(rows):
    p = _TMP / "otros.xlsx"
    wb = openpyxl.Workbook(); ws = wb.active; ws.append(_OHDR)
    for r in rows:
        line = [""] * len(_OHDR)
        for k, v in r.items():
            line[_OKEY[k]] = v
        ws.append(line)
    wb.save(p)
    return p


# Un mes de atenciones sin NADA respiratorio es ArchivoInvalido (ronda 9): los fixtures
# que miran SALA / Seccion G llevan esta fila de relleno (otro RUN, IRA alta).
_RESP = {"NUMERO TIPO IDENTIFICACION": "Z", "FECHA ATENCION": date(2026, 7, 5),
         "DIAGNOSTICOS": "J06.9 IRA alta", "INSTRUMENTO": "Médico"}


def test_sala_bajo_control():
    aten = _mk([
        {"NUMERO TIPO IDENTIFICACION": "A", "FECHA ATENCION": date(2026, 7, 10), "INSTRUMENTO": "Médico", "FECHA DE NACIMIENTO": date(1990, 1, 1)},
        {"NUMERO TIPO IDENTIFICACION": "S", "FECHA ATENCION": date(2026, 7, 11), "INSTRUMENTO": "Médico", "FECHA DE NACIMIENTO": date(2023, 1, 1)},
        {"NUMERO TIPO IDENTIFICACION": "E", "FECHA ATENCION": date(2026, 7, 12), "INSTRUMENTO": "Médico", "FECHA DE NACIMIENTO": date(1970, 1, 1)},
        _RESP,
    ])
    otros = _mk_otros([
        {"RUN": "A", "FECHA": date(2026, 5, 1), "INSTR": "Médico", "ASMA_p": "Si", "ASMA_grav": "Moderado", "ASMA_ctrl": "Controlado", "ASMA_est": "Ingreso"},
        {"RUN": "S", "FECHA": date(2026, 5, 1), "INSTR": "Médico", "SBOR_p": "Si", "SBOR_rec": "Si", "SBOR_grav": "Leve", "SBOR_est": "Seguimiento"},
        {"RUN": "E", "FECHA": date(2026, 5, 1), "INSTR": "Médico", "EPOC_p": "Si", "EPOC_tipo": "Tipo A", "EPOC_ctrl": "Controlado", "EPOC_est": "Ingreso"},
    ])
    f = a23.procesar(aten, otros=otros, mes=(2026, 7), log=lambda *a: None).set_index("RUN")
    assert f.loc["A", "SALA ASMA"] == "SI" and f.loc["A", "SALA Ingresado"] == "SI"
    assert f.loc["A", "SALA ASMA Gravedad"] == "Moderado"
    assert f.loc["A", "SALA SBOR"] == "NO"                       # no <5
    assert f.loc["S", "SALA SBOR"] == "SI" and f.loc["S", "SALA SBOR Gravedad"] == "Leve"
    assert f.loc["E", "SALA EPOC"] == "SI" and f.loc["E", "SALA EPOC Tipo"] == "Tipo A"


def test_seccion_g_inasistentes():
    """Inasistente a control de crónico = padece+estado válido y última Fecha
    Próximo Control vencida > umbral(edad) al corte (último día del mes reportado)."""
    import pandas as pd
    otros = _mk_otros([
        # adulta asma, próximo control vencido hace ~2 años -> inasistente (umbral 11m29d)
        {"RUN": "AD", "FECHA": date(2024, 1, 1), "INSTR": "Médico", "SEXO": "Mujer", "FNAC": date(1980, 1, 1),
         "ASMA_p": "Si", "ASMA_est": "Seguimiento", "ASMA_grav": "Leve", "ASMA_ctrl": "Controlado", "ASMA_prox": date(2024, 6, 1)},
        # adulto asma al día (próximo control futuro) -> NO
        {"RUN": "OK", "FECHA": date(2026, 6, 1), "INSTR": "Médico", "SEXO": "Hombre", "FNAC": date(1990, 1, 1),
         "ASMA_p": "Si", "ASMA_est": "Ingreso", "ASMA_grav": "Leve", "ASMA_ctrl": "Controlado", "ASMA_prox": date(2026, 9, 1)},
    ])
    od, _ = a23.cargar_otros(otros)
    counts, flags = a23._seccion_g(od, pd.Timestamp(2026, 7, 31))
    assert counts["Asma"]["Total"] == 1                       # solo AD (vencida)
    assert counts["Asma"]["Mujer"] == 1 and counts["Asma"]["Hombre"] == 0
    assert "AD" in flags["ASMA"] and "OK" not in flags["ASMA"]


def test_carga_multiarchivo():
    """cargar_otros acepta una LISTA (histórico multi-año) y concatena."""
    a = _mk_otros([{"RUN": "X", "FECHA": date(2025, 1, 1), "INSTR": "Médico", "ASMA_p": "Si"}])
    import shutil
    b = _TMP / "otros_b.xlsx"; shutil.copy(a, b)
    od, _ = a23.cargar_otros([a, b])
    assert len(od) == 2


_NSP_HDR = ["INSTRUMENTO", "TIPO DE ATENCION", "FECHA HORA CITA",
            "NUMERO TIPO IDENTIFICACION", "AÑOS"]
_NKEY = {"instr": 0, "tipo": 1, "fecha": 2, "run": 3, "anos": 4}


def _mk_nsp(rows):
    p = _TMP / "nsp.xlsx"
    wb = openpyxl.Workbook(); ws = wb.active; ws.append(_NSP_HDR)
    for r in rows:
        line = [""] * len(_NSP_HDR)
        for k, v in r.items():
            line[_NKEY[k]] = v
        ws.append(line)
    wb.save(p)
    return p


def _mk_estrat(hdr, rows):
    p = _TMP / "estrat.xlsx"
    wb = openpyxl.Workbook(); ws = wb.active; ws.append(hdr)
    for r in rows:
        ws.append(r)
    wb.save(p)
    return p


def test_cargar_estrat_arma_run_y_falla_en_la_fuente():
    """Estratificación: RUN = RUT-DV. Las dos guardas son sobre la FUENTE (CLAUDE.md
    regla 2): sin columna RUT reventaba con TypeError en f[None], y con solo el
    encabezado dejaba la gravedad de TODOS en "" vía _gate -> SALA en 0 callado."""
    from programas.rem_utils import ArchivoInvalido
    hdr = ["RUT", "DV", "DETALLE DIAGNOSTICOS"]
    s = a23.cargar_estrat(_mk_estrat(hdr, [[11111111, "1", "Asma Moderada"]]))
    assert s.loc["11111111-1"] == "ASMA MODERADA"

    for etq, h, rows in (("sin columna RUT", ["FOO", "BAR", "BAZ", "QUX"], [[1, 2, 3, 4]]),
                         ("solo encabezado", hdr, [])):
        try:
            a23.cargar_estrat(_mk_estrat(h, rows))
            assert False, f"Estratificación {etq}: debió levantar ArchivoInvalido"
        except ArchivoInvalido as e:
            assert e.categoria in ("sin_columnas", "sin_datos"), (etq, e.categoria)


def test_seccion_h():
    """Sección H: citas Control/Ingreso IRA/ERA no asistidas, por estamento × tramo
    (<20 / >=20), del mes por FECHA HORA CITA. Excluye KTR y otros meses/tipos."""
    import pandas as pd
    nsp = _mk_nsp([
        {"instr": "Médico", "tipo": "Control IRA", "fecha": "10-07-2026 09:00:00", "run": "A", "anos": 40},
        {"instr": "Médico", "tipo": "Ingreso ERA", "fecha": "12-07-2026 09:00:00", "run": "B", "anos": 15},
        {"instr": "Kinesiólogo(a)", "tipo": "Control ERA", "fecha": "13-07-2026 09:00:00", "run": "C", "anos": 60},
        {"instr": "Kinesiólogo(a)", "tipo": "kinesioterapia respiratoria IRA", "fecha": "14-07-2026 09:00:00", "run": "D", "anos": 30},  # KTR -> fuera
        {"instr": "Médico", "tipo": "Control IRA", "fecha": "10-06-2026 09:00:00", "run": "E", "anos": 40},  # junio -> fuera
        {"instr": "Médico", "tipo": "Consulta SAC", "fecha": "11-07-2026 09:00:00", "run": "F", "anos": 40},  # no IRA/ERA -> fuera
    ])
    d = a23.cargar_inasistentes(nsp)
    h = a23._seccion_h(d, pd.Timestamp(2026, 7, 1), pd.Timestamp(2026, 7, 31)).set_index("Profesional")
    assert h.loc["Médico/a", "Total"] == 2 and h.loc["Médico/a", "Menor de 20"] == 1 and h.loc["Médico/a", "20 y más"] == 1
    assert h.loc["Kinesiólogo/a", "Total"] == 1        # Control ERA; KTR excluido
    assert h.loc["TOTAL", "Total"] == 3                # junio y Consulta SAC fuera


# -- Guardarraíl de mes vacío (CLAUDE.md §3: fail loud, como el A05) --
def test_mes_sin_atenciones_falla_duro():
    """Sin atenciones del mes los 27 indicadores salen 'NO' y el detalle se lee como
    un mes de cero actividad. Es archivo/mes equivocado -> ArchivoInvalido."""
    from programas.rem_utils import ArchivoInvalido
    rows = [{"NUMERO TIPO IDENTIFICACION": "A", "FECHA ATENCION": date(2025, 7, 10),
             "DIAGNOSTICOS": "J20.9 Bronquitis aguda", "INSTRUMENTO": "Médico"}]
    try:
        a23.procesar(_mk(rows), mes=(2026, 7), log=_quiet)
    except ArchivoInvalido as e:
        assert e.categoria == "mes_vacio" and "07/2026" in str(e)
        return
    raise AssertionError("un export que no cubre el mes debió levantar ArchivoInvalido")


def test_export_sin_filas_falla_claro():
    """Export header-only: antes el log del span reventaba con 'NaTType does not
    support strftime'. Hoy lo corta `cargar_canonico` con ArchivoInvalido('sin_datos')
    NOMBRANDO el archivo, antes incluso de llegar al filtro de mes."""
    from programas.rem_utils import ArchivoInvalido
    try:
        a23.procesar(_mk([]), mes=(2026, 7), log=_quiet)
    except ArchivoInvalido as e:
        assert e.categoria == "sin_datos" and "ninguna fila" in str(e)
        return
    raise AssertionError("un export sin filas debió levantar ArchivoInvalido")


def test_indicador_en_cero_con_el_mes_cubierto_no_falla():
    """La guarda es sobre la FUENTE: con el mes cubierto, un indicador en 0 (acá
    Bronquitis, que nadie tuvo) es legítimo y la corrida sigue."""
    rows = [{"NUMERO TIPO IDENTIFICACION": "A", "FECHA ATENCION": date(2026, 7, 10),
             "DIAGNOSTICOS": "J06.9 IRA alta", "INSTRUMENTO": "Médico"}]
    f = a23.procesar(_mk(rows), mes=(2026, 7), log=_quiet).set_index("RUN")
    assert f.loc["A", "REMA23 Ira Alta"] == "SI"
    assert f.loc["A", "REMA23 Bronquitis Aguda"] == "NO"     # 0 legítimo, sin excepción


def test_seccion_h_nsp_de_otro_mes_falla_duro():
    """El NSP es opcional, pero si se carga tiene que cubrir el mes: si no, la
    Sección H sale en cero y parece que nadie faltó a su cita."""
    import pandas as pd
    from programas.rem_utils import ArchivoInvalido
    nsp = _mk_nsp([{"instr": "Médico", "tipo": "Control IRA", "fecha": "10-06-2026 09:00:00",
                    "run": "A", "anos": 40}])
    d = a23.cargar_inasistentes(nsp)
    try:
        a23._seccion_h(d, pd.Timestamp(2026, 7, 1), pd.Timestamp(2026, 7, 31))
    except ArchivoInvalido as e:
        assert e.categoria == "mes_vacio" and "NSP" in str(e)
        return
    raise AssertionError("un NSP que no cubre el mes debió levantar ArchivoInvalido")


def test_seccion_h_sin_ira_era_en_el_mes_no_falla():
    """…pero el filtro Control/Ingreso IRA/ERA va DESPUÉS: un mes con inasistencias
    que no son respiratorias da Sección H = 0, y eso es legítimo."""
    import pandas as pd
    nsp = _mk_nsp([{"instr": "Médico", "tipo": "Consulta SAC", "fecha": "11-07-2026 09:00:00",
                    "run": "F", "anos": 40}])
    d = a23.cargar_inasistentes(nsp)
    h = a23._seccion_h(d, pd.Timestamp(2026, 7, 1), pd.Timestamp(2026, 7, 31)).set_index("Profesional")
    assert h.loc["TOTAL", "Total"] == 0


def test_fecha_col_avisa_ilegibles():
    """fecha_col cuenta y AVISA solo los valores no-vacíos ilegibles; los vacíos
    legítimos (blanco / None) quedan callados. Serie limpia -> sin aviso (CORR-1)."""
    import pandas as pd
    from programas.rem_utils import fecha_col
    msgs = []
    s = pd.Series(["01/03/2026", "no-es-fecha", "", None, "15/13/2026"])
    out = fecha_col(s, log=msgs.append, etiqueta="X")
    assert int(out.isna().sum()) == 4                 # 2 ilegibles + 2 vacíos (1 válido)
    assert len(msgs) == 1 and "2 valor" in msgs[0]    # avisa exactamente 2 ilegibles
    msgs2 = []
    fecha_col(pd.Series(["01/03/2026", "", None]), log=msgs2.append)
    assert msgs2 == []                                # serie limpia: silencio


def test_cargar_inasistentes_avisa_fecha_ilegible():
    """El loader NSP usa fecha_col y REENVÍA el log: una FECHA HORA CITA ilegible
    se avisa (no cae callada fuera del filtro de mes). Verifica la propagación."""
    nsp = _mk_nsp([
        {"instr": "Médico", "tipo": "Control IRA", "fecha": "10-07-2026 09:00:00", "run": "A", "anos": 40},
        {"instr": "Médico", "tipo": "Control IRA", "fecha": "fecha-mala",           "run": "B", "anos": 40},
    ])
    msgs = []
    a23.cargar_inasistentes(nsp, log=msgs.append)
    avisos = [m for m in msgs if "[fecha]" in m and "ilegible" in m]
    assert avisos, "debió avisar la fecha ilegible"
    assert "1 valor" in avisos[0]                     # exactamente 1 ilegible (la otra es válida)


_G_ATEN = [{"NUMERO TIPO IDENTIFICACION": "A", "FECHA ATENCION": date(2026, 7, 10),
            "INSTRUMENTO": "Médico", "FECHA DE NACIMIENTO": date(1990, 1, 1)}, _RESP]
# Asma en seguimiento, próximo control 2025-06-01: al corte 2026-07-31 lleva 14 meses
# vencido -> inasistente con cualquier umbral (el mayor es 11m29d).
_G_OT = {"RUN": "A", "FECHA": date(2025, 5, 1), "INSTR": "Médico", "SEXO": "Mujer",
         "ASMA_p": "Si", "ASMA_grav": "Leve", "ASMA_ctrl": "Controlado", "ASMA_est": "Seguimiento",
         "ASMA_prox": date(2025, 6, 1)}


def test_seccion_g_no_descarta_callado_al_que_no_tiene_fecha_de_nacimiento():
    """Ronda 9: sin FECHA DE NACIMIENTO legible en 'Otros Cronicos' el paciente se
    DESCARTABA de la Sección G (`continue`), y sin la columna la G entera daba 0 sin
    ningún aviso. Ahora: edad del ADA como respaldo; si tampoco está, umbral >=2 años
    + aviso REVISAR."""
    def g(otros_rows, aten=_G_ATEN):
        fer = a23.procesar(_mk(aten), otros=_mk_otros(otros_rows), mes=(2026, 7), log=_quiet)
        return fer.attrs["seccion_g"]["Asma"]["Total"], [a[1] for a in fer.attrs["avisos"]
                                                          if a[0].startswith("Seccion G")]
    assert g([dict(_G_OT, FNAC=date(1980, 1, 1))]) == (1, [])        # control
    assert g([_G_OT]) == (1, [])                                     # edad del ADA (1990)
    sin_fnac_ada = [{k: v for k, v in _G_ATEN[0].items() if k != "FECHA DE NACIMIENTO"}, _RESP]
    assert g([_G_OT], aten=sin_fnac_ada) == (1, ["REVISAR"])         # ni ahí -> umbral + aviso


def test_otros_cronicos_sin_fechas_legibles_falla_en_la_fuente():
    """Ronda 9: FECHA ATENCION ilegible en TODO el formulario -> NaT callado (to_datetime
    pelado), el chequeo de historial de la G se saltaba y la encuesta del mes quedaba
    vacía. Ahora cuenta las ilegibles en el log y, si no queda ninguna, ArchivoInvalido."""
    from programas.rem_utils import ArchivoInvalido
    msgs = []
    a23.cargar_otros(_mk_otros([_G_OT, dict(_G_OT, RUN="B", FECHA="xx")]), log=msgs.append)
    assert any("[fecha]" in m and "1 valor" in m for m in msgs), msgs
    try:
        a23.procesar(_mk(_G_ATEN), otros=_mk_otros([dict(_G_OT, FECHA="xx")]),
                     mes=(2026, 7), log=_quiet)
        assert False, "debió levantar ArchivoInvalido"
    except ArchivoInvalido as e:
        assert e.categoria == "sin_fecha", e.categoria


def test_mes_sin_nada_respiratorio_y_otros_sin_medico_no_dan_0_callado():
    """Ronda 9, 2a pasada: (a) atenciones del mes sin NADA respiratorio -> los 27
    indicadores en NO con "Listo" -> ahora sin_datos. (b) 'Otros Cronicos' sin columna
    INSTRUMENTO -> _med False para todos y SALA/G en 0 -> sin_columnas; con la columna
    pero sin ningun medico -> aviso EN 0."""
    from programas.rem_utils import ArchivoInvalido
    nada = [{"NUMERO TIPO IDENTIFICACION": "A", "FECHA ATENCION": date(2026, 7, 10),
             "INSTRUMENTO": "Enfermero(a)", "ACTIVIDADES": "Curacion simple"}]
    try:
        a23.procesar(_mk(nada), mes=(2026, 7), log=_quiet)
        assert False, "debio levantar ArchivoInvalido"
    except ArchivoInvalido as e:
        assert e.categoria == "sin_datos", e.categoria

    o = _mk_otros([dict(_G_OT, FNAC=date(1980, 1, 1))])
    wb = openpyxl.load_workbook(o); ws = wb.active; ws.delete_cols(3); wb.save(o)   # sin INSTRUMENTO
    try:
        a23.procesar(_mk(_G_ATEN), otros=o, mes=(2026, 7), log=_quiet)
        assert False, "debio levantar ArchivoInvalido"
    except ArchivoInvalido as e:
        assert e.categoria == "sin_columnas", e.categoria

    # Sin ningun medico en el formulario pero con SALA no vacia (asma por el dx J45 del
    # ADA): aviso EN 0. Con SALA vacia del todo, ver el test de la ronda 10 de abajo.
    j45 = dict(_G_ATEN[0], DIAGNOSTICOS="J45.9 Asma")
    fer = a23.procesar(_mk([j45, _RESP]), otros=_mk_otros([dict(_G_OT, INSTR="Kinesiologo(a)")]),
                       mes=(2026, 7), log=_quiet)
    assert any(a[0].startswith("SALA") and a[1] == "EN 0" for a in fer.attrs["avisos"]), fer.attrs["avisos"]


def test_sala_vacia_preguntas_renombradas_y_nsp_incompleto_no_dan_0_callado():
    """Ronda 10 (R2 estática): (a) nadie 'Pertenece a SALA' -> TODAS las hojas del A23
    en 0 (se calculan solo sobre SALA) -> sin_datos. (b) una pregunta de condición
    renombrada ('TIENE' por 'PADECE DE') dejaba esa condición en 0 callada -> aviso
    SUBCONTADO; ninguna -> sin_columnas. (c) NSP sin TIPO/INSTRUMENTO/AÑOS daba la H
    en 0 o todo en '20 y más' -> sin_columnas; AÑOS ilegible -> aviso REVISAR."""
    import pandas as pd
    from programas.rem_utils import ArchivoInvalido

    def _cat(fn):
        try:
            fn()
        except ArchivoInvalido as e:
            return e.categoria
        return None

    # (a) formulario sin ningun medico y sin dx J45 en el ADA -> SALA vacia
    assert _cat(lambda: a23.procesar(_mk(_G_ATEN), otros=_mk_otros([dict(_G_OT, INSTR="Kine")]),
                                     mes=(2026, 7), log=_quiet)) == "sin_datos"

    # (b) asma renombrada: A deja de estar en SALA por el formulario -> aviso
    o = _mk_otros([dict(_G_OT, FNAC=date(1980, 1, 1))])
    wb = openpyxl.load_workbook(o); ws = wb.active
    ws.cell(row=1, column=10, value="9.- ¿TIENE ASMA BRONQUIAL?"); wb.save(o)
    j45 = dict(_G_ATEN[0], DIAGNOSTICOS="J45.9 Asma")          # SALA no vacia via el ADA
    fer = a23.procesar(_mk([j45, _RESP]), otros=o, mes=(2026, 7), log=_quiet)
    av = [a for a in fer.attrs["avisos"] if a[0].startswith("SALA / Seccion G")]
    assert av and "Asma" in av[0][2] and av[0][1] == "SUBCONTADO", fer.attrs["avisos"]
    ws.cell(row=1, column=6, value="1.- ¿TIENE SBO?")          # + SBOR y EPOC: ya no queda
    ws.cell(row=1, column=15, value="14.- ¿TIENE EPOC?"); wb.save(o)   # ninguna '¿PADECE...?'
    assert _cat(lambda: a23.cargar_otros(o, log=_quiet)) == "sin_columnas"

    # (c) NSP
    fila = {"instr": "Médico", "tipo": "Control IRA", "fecha": "10-07-2026 09:00:00", "run": "A", "anos": 5}
    for i, nombre in ((1, "PRESTACION"), (0, "PROFESIONAL"), (4, "EDAD AL DESCARGAR")):   # "EDAD" pelado = Admin
        viejo = _NSP_HDR[i]; _NSP_HDR[i] = nombre
        try:
            assert _cat(lambda: a23.cargar_inasistentes(_mk_nsp([fila]), log=_quiet)) == "sin_columnas", nombre
        finally:
            _NSP_HDR[i] = viejo
    h = a23._seccion_h(a23.cargar_inasistentes(_mk_nsp([dict(fila, anos="")]), log=_quiet),
                       pd.Timestamp(2026, 7, 1), pd.Timestamp(2026, 7, 31))
    assert h.attrs["sin_edad"] == 1


def test_estratificacion_sin_columna_de_diagnosticos_falla():
    """Ronda 10, 2a pasada: sin la columna de diagnosticos el reporte cargaba y no
    aportaba NADA a SALA, callado -> sin_columnas. Ronda 11, contra el export real: el
    fallback "CONDICIONES CRONICAS" calzaba con 'Cantidad de Condiciones Crónicas' (un
    CONTEO), asi que sin 'Detalle...' tiene que fallar igual aunque esa este."""
    from programas.rem_utils import ArchivoInvalido
    for hdr, fila in ((["RUT", "DV", "COMUNA"], [11111111, "1", "Maipu"]),
                      (["RUT", "DV", "Cantidad de Condiciones Crónicas"], [11111111, "1", 2])):
        try:
            a23.cargar_estrat(_mk_estrat(hdr, [fila]))
            assert False, f"debio levantar ArchivoInvalido con {hdr}"
        except ArchivoInvalido as e:
            assert e.categoria == "sin_columnas", e.categoria
    s = a23.cargar_estrat(_mk_estrat(["DETALLE DIAGNOSTICOS", "RUT", "DV"],
                                     [["Asma Moderada", 11111111, "1"]]))
    assert s.loc["11111111-1"] == "ASMA MODERADA"                  # col 0 SI cuenta


def test_atencion_multifila_y_run_heredado_solo_dentro_de_la_atencion():
    """Ronda 11, contra los encabezados REALES (refs_tablas): (a) en el Monitoreo una
    atencion son VARIAS filas con el mismo 'N°', y los indicadores con AND entre
    actividades («autocuidado» Y «control sala») comparaban fila por fila -> NO callado;
    (b) el RUN se rellenaba con un ffill global: en IRIS una fila sin RUN heredaba el
    paciente de la fila de ARRIBA, de otra atencion."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from contratos_fuentes import Contrato, escribir, plantilla
    from programas.rem_utils import cargar_atenciones, dv_rut

    def _fx(ref, filas):
        b, h, p = plantilla(Contrato(id=ref, cubre=(), llamar=None, fila={}, ref=ref))
        return escribir(_TMP / f"multi_{ref}", b, h, filas, p)
    otro = "10000013-" + dv_rut("10000013")
    mon = cargar_atenciones(_fx("Monitoreo_de_Actividades_anonimizado.xlsx", [
        {"N°": 1, "RUN": "11111111-1", "FECHA CONSULTA": "05/08/2026", "AÑOS": 40,
         "ACTIVIDAD Y/O PROCEDIMIENTO": "CONTROL SALA (IRA, ERA O MIXTA)", "DIAGNÓSTICO": "ASMA",
         "INSTRUMENTO": "MEDICO", "TIPO DE ATENCIÓN": "CONTROL", "FUNCIONARIO": "DR X"},
        {"N°": 1, "ACTIVIDAD Y/O PROCEDIMIENTO":
            "EDUCACION INDIVIDUAL EN SALA - AUTOCUIDADO SEGUN PATOLOGIA"},
        {"N°": 2, "RUN": otro, "FECHA CONSULTA": "06/08/2026", "AÑOS": 7,
         "ACTIVIDAD Y/O PROCEDIMIENTO": "EDUCACION INDIVIDUAL EN SALA - AUTOCUIDADO SEGUN PATOLOGIA",
         "DIAGNÓSTICO": "ASMA", "INSTRUMENTO": "KINESIOLOGO(A)", "TIPO DE ATENCIÓN": "CONTROL",
         "FUNCIONARIO": "KINE Z"},
    ]), log=_quiet)
    assert list(mon["RUN"]) == ["11111111-1", "11111111-1", otro], list(mon["RUN"])
    auto = a23._masks_simples(mon)["REMA23 Autocuidado"]
    assert set(mon.loc[auto, "RUN"]) == {"11111111-1"}, set(mon.loc[auto, "RUN"])  # la 2 no

    iris = cargar_atenciones(_fx("ATENCIONESDIAGNOSTICOSACTIVIDADES_iris.xlsx", [
        {"NUMERO TIPO IDENTIFICACION": "11111111-1", "ATEN ID": "901", "FECHA ATENCION": "05/08/2026",
         "ACTIVIDADES": "CONTROL SALA (IRA, ERA O MIXTA); EDUCACION INDIVIDUAL EN SALA - "
                        "AUTOCUIDADO SEGUN PATOLOGIA", "DIAGNOSTICOS": "J45",
         "INSTRUMENTO": "MEDICO", "TIPO ATENCION": "CONTROL", "PROFESIONAL ATENCION": "DR X"},
        {"ATEN ID": "902", "FECHA ATENCION": "06/08/2026", "ACTIVIDADES": "CONSULTA SALA (IRA, ERA O MIXTA)",
         "DIAGNOSTICOS": "J45", "INSTRUMENTO": "MEDICO", "TIPO ATENCION": "CONSULTA",
         "PROFESIONAL ATENCION": "DR Y"},
    ]), log=_quiet)
    assert iris["RUN"].iloc[1] != "11111111-1", "la 902 heredo el RUN de la 901 (otra atencion)"
    assert bool(a23._masks_simples(iris)["REMA23 Autocuidado"].iloc[0])


def test_otros_cronicos_administrativo_saca_el_estamento_del_funcionario():
    """Ronda 11 (decision del autor: se soporta). El 'Otros Cronicos' Administrativo trae
    RUT / Fecha Formulario / Funcionario y NO trae INSTRUMENTO: el estamento sale del
    nombre del funcionario en el propio export de atenciones. Encabezados REALES."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from contratos_fuentes import Contrato, escribir, plantilla

    def _fx(ref, filas):
        b, h, p = plantilla(Contrato(id=ref, cubre=(), llamar=None, fila={}, ref=ref))
        return escribir(_TMP / f"adm_{ref}", b, h, filas, p)
    ada = _fx("ATENCIONESDIAGNOSTICOSACTIVIDADES_iris.xlsx", [
        {"NUMERO TIPO IDENTIFICACION": "11111111-1", "ATEN ID": "901", "FECHA ATENCION": "10/07/2026",
         "ACTIVIDADES": "CONTROL SALA (IRA, ERA O MIXTA)", "DIAGNOSTICOS": "J45 ASMA",
         "INSTRUMENTO": "Médico", "TIPO ATENCION": "CONTROL", "PROFESIONAL ATENCION": "ANA PEREZ",
         "FECHA DE NACIMIENTO": "01/01/1990"}])
    asma = {"9.- ¿Padece de Asma Bronquial?": "Si", "10.- Estado": "Ingreso",
            "11.- Gravedad Asma Bronquial": "Moderado", "13.- Estado de Control Asma": "Controlado"}
    otros = _fx("Otros_cronicos_admin.xlsx", [
        dict(asma, **{"RUT": "11111111-1", "Fecha Formulario": "2026/05/01", "Funcionario": "ANA PEREZ"}),
        dict(asma, **{"RUT": "11111111-1", "Fecha Formulario": "2026/04/01", "Funcionario": "NN DESCONOCIDO"}),
    ])
    f = a23.procesar(ada, otros=otros, mes=(2026, 7), log=_quiet)
    fila = f.set_index("RUN").loc["11111111-1"]
    assert fila["SALA ASMA"] == "SI" and fila["SALA ASMA Gravedad"] == "Moderado", dict(fila)
    assert any(a[1] == "SUBCONTADO" and "NN DESCONOCIDO" in a[2] for a in f.attrs["avisos"]), \
        f.attrs["avisos"]


def test_seccion_h_con_el_monitoreo_de_inasistentes_administrativo():
    """Ronda 11: el NSP Administrativo ('Monitoreo de Inasistentes') trae RUN, FECHA CITA
    y EDAD (en texto) en vez de NUMERO... / FECHA HORA CITA / AÑOS. Encabezado REAL."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from contratos_fuentes import Contrato, escribir, plantilla
    import pandas as pd
    b, h, p = plantilla(Contrato(id="nsp", cubre=(), llamar=None, fila={},
                                 ref="Monitoreo_de_Inasistentes_admin.xlsx"))
    base = {"INSTRUMENTO": "Kinesiólogo(a)", "TIPO ATENCION": "Control ERA", "FECHA CITA": "10-08-2026",
            "RUN": "11111111-1", "SEXO": "Mujer"}
    ruta = escribir(_TMP / "nsp_admin.xlsx", b, h, [dict(base, EDAD="8 años 2 meses"),
                                                     dict(base, EDAD="45 años")], p)
    hh = a23._seccion_h(a23.cargar_inasistentes(ruta, log=_quiet),
                        pd.Timestamp(2026, 8, 1), pd.Timestamp(2026, 8, 31, 23, 59))
    kine = hh[hh["Profesional"] == "Kinesiólogo/a"].iloc[0]
    assert (kine["Menor de 20"], kine["20 y más"]) == (1, 1), dict(kine)


def test_estratificacion_o_nsp_invalidos_son_opcional_invalido():
    """Ronda 11: un opcional que no sirve levanta OpcionalInvalido con el NOMBRE del
    parametro, para que la GUI ofrezca seguir sin el (gui/runner.sin_opcional)."""
    from programas.rem_utils import OpcionalInvalido
    aten = _mk([{"NUMERO TIPO IDENTIFICACION": "A", "FECHA ATENCION": date(2026, 7, 10),
                 "INSTRUMENTO": "Médico", "FECHA DE NACIMIENTO": date(1990, 1, 1)}, _RESP])
    otros = _mk_otros([{"RUN": "A", "FECHA": date(2026, 5, 1), "INSTR": "Médico", "ASMA_p": "Si",
                        "ASMA_grav": "Moderado", "ASMA_ctrl": "Controlado", "ASMA_est": "Ingreso"}])
    malo = _mk_estrat(["RUT", "DV", "COMUNA"], [[11111111, "1", "Maipu"]])   # sin diagnosticos
    for kw, entrada in ((dict(estrat=malo), "estrat"), (dict(inasistentes=[malo]), "inasistentes")):
        try:
            a23.procesar(aten, otros=otros, mes=(2026, 7), log=_quiet, **kw)
            assert False, f"{entrada}: debio levantar OpcionalInvalido"
        except OpcionalInvalido as e:
            assert e.entrada == entrada, (entrada, e.entrada)


def _main():
    pruebas = [v for k, v in sorted(globals().items())
               if k.startswith("test_") and callable(v)]
    fallos = 0
    for fn in pruebas:
        try:
            fn(); print(f"PASS  {fn.__name__}")
        except AssertionError as e:
            fallos += 1; print(f"FAIL  {fn.__name__} -> {e or 'assert'}")
        except Exception as e:  # noqa: BLE001
            fallos += 1; print(f"ERROR {fn.__name__} -> {type(e).__name__}: {e}")
    print("-" * 50)
    print(f"{len(pruebas) - fallos}/{len(pruebas)} OK" + (f" ({fallos} problemas)" if fallos else ""))
    return 1 if fallos else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(_main())
