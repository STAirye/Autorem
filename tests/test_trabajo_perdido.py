#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# SPDX-License-Identifier: GPL-3.0-or-later
# ==========================================================================
"""Pruebas del módulo REM SM Trabajo Perdido + guarda multi-hoja. Datos SINTÉTICOS.
    python tests/test_trabajo_perdido.py"""

import sys
import tempfile
from pathlib import Path

import openpyxl

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

import modulos.rem_sm_trabajo_perdido as tp     # noqa: E402
from programas.rem_utils import ArchivoInvalido, verificar_hoja_unica   # noqa: E402

_TMP = Path(tempfile.mkdtemp(prefix="autorem_tp_"))

_ADA_HDR = ["NUMERO TIPO IDENTIFICACION", "ATEN ID", "FECHA ATENCION", "ACTIVIDADES",
            "DIAGNOSTICOS", "INSTRUMENTO", "PROFESIONAL ATENCION", "TIPO ATENCION",
            "SEXO", "AÑOS ATENCION", "FORMULARIOS CLINICOS"]
_ADA_K = {"run": 0, "id": 1, "fecha": 2, "act": 3, "dg": 4, "instr": 5,
          "prof": 6, "tipo": 7, "sexo": 8, "edad": 9, "form": 10}

_MAESTRO_HDR = ["ACTIVIDAD", "INSTRUMENTO ASOCIADO", "NUM REM", "NUM SECCION", "REM"]


def _mk_ada(rows, nombre="ada.xlsx"):
    p = _TMP / nombre
    wb = openpyxl.Workbook(); ws = wb.active
    ws.append(_ADA_HDR)
    for r in rows:
        line = [""] * len(_ADA_HDR)
        for k, v in r.items():
            if _ADA_K[k] < len(_ADA_HDR):     # header recortado = columna ausente
                line[_ADA_K[k]] = v
        ws.append(line)
    wb.save(p)
    return p


def _mk_maestro(pares, nombre="maestro.xlsx"):
    """pares = [(actividad, num_rem), ...]. Banner en fila 1 (como el real)."""
    p = _TMP / nombre
    wb = openpyxl.Workbook(); ws = wb.active
    ws.append(["Maestro de Actividades"])          # banner
    ws.append(_MAESTRO_HDR)
    for act, numrem in pares:
        ws.append([act, "Psicólogo(a)", numrem, "", "desc"])
    wb.save(p)
    return p


def _a(act, prof, run="1-1", instr="Psicólogo(a)", fecha="10/07/2026", id=None, form=""):
    return dict(act=act, prof=prof, run=run, instr=instr, fecha=fecha,
                id=id or f"AT{run}{act[:3]}", form=form,
                dg="x", tipo="Espontánea", sexo="Femenino", edad="30 años")


def _quiet(*_a, **_k): pass


# VDI del PADDS: trae 'demencia' (como descriptor, y aquí NEGADO) -> la red SM-ish la
# capta, pero no es Salud Mental. Debe salir del universo (EXCLUIR_SMISH).
_PADDS = ("Visita domiciliaria integral a personas con PADDS - Familia con integrante "
          "con dependencia severa sin diagnóstico de demencia y/o que no se encuentra "
          "en etapa terminal - Elaboración plan de cuidados a cuidador")
# VDI de Salud Mental (A26 sección A): parecida en forma, pero SÍ tributa. Guarda
# contra excluir de más.
_VDI_SM = ("Visita domiciliaria integral familia con integrante con problema de salud "
           "mental - Primera visita")

_MAESTRO = [
    ("Consulta De Salud Mental", "REM-A04"),
    ("Controles Salud Mental", "REM-A06"),
    ("AG_Alta programa salud mental", "REM-Gestion"),
    ("AG_Atencion de salud mental adolescente", "REM-Gestion"),
    ("Confirmacion diagnostica salud mental", "REM-A03"),      # otro REM real
    ("Curacion simple", "REM-A28"),                            # no SM
    (_PADDS, "REM-A26"),                                       # A26 pero sección A1
    (_VDI_SM, "REM-A26"),                                      # A26 sección A -> SM
]


def _run(ada_rows, con_maestro=True, mes=(2026, 7)):
    ada = _mk_ada(ada_rows)
    maestro = _mk_maestro(_MAESTRO) if con_maestro else None
    E = tp.procesar(ada, maestro=maestro, mes=mes, log=_quiet)
    return E


# -- Tests --------------------------------------------------------------

def test_gestion_es_perdida():
    E = _run([_a("Consulta De Salud Mental", "ANA"),          # A04 -> tributa
              _a("AG_Alta programa salud mental", "JUAN"),    # Gestion -> PERDIDA
              _a("Controles Salud Mental", "ANA")])           # A06 -> tributa
    assert len(E) == 1, f"esperaba 1 perdida, hubo {len(E)}"
    assert E.iloc[0]["num_rem"].upper() == "REM-GESTION", E.iloc[0]["num_rem"]
    assert E.iloc[0]["profesional"] == "JUAN"


def test_otro_rem_real_tambien_es_perdida():
    # Definición elegida (referente): todo lo no-SM-estadístico es perdido, incluso A03.
    E = _run([_a("Confirmacion diagnostica salud mental", "MARIA")])
    assert len(E) == 1
    assert E.iloc[0]["num_rem"].upper() == "REM-A03"


def test_no_sm_se_ignora():
    E = _run([_a("Curacion simple", "PEDRO")])       # sin mental/demencia -> ni se mira
    assert len(E) == 0


def test_actividad_nueva_no_en_maestro():
    # 'Taller mental raro' no está en el Maestro y no matchea heurística -> PERDIDA.
    # 'Controles Salud Mental por chat' no está en el Maestro pero SÍ matchea heur -> tributa.
    E = _run([_a("Taller mental raro inventado", "LUCIA"),
              _a("Controles Salud Mental por chat", "LUCIA")])
    assert len(E) == 1, f"esperaba 1, hubo {len(E)}"
    assert "NO EN MAESTRO" in E.iloc[0]["num_rem"].upper()


def test_padds_fuera_del_universo_con_maestro():
    # Con Maestro el PADDS ya quedaba fuera del reporte, pero por la razón EQUIVOCADA:
    # caía en TRIBUTA_SM_REM por su NUM REM (REM-A26, sin sección), o sea se daba por
    # trabajo de SM bien tabulado. La salida (E) no cambia; lo que cambia es que ahora
    # se declara como exclusión. Por eso el assert va sobre el LOG, no sobre E: es la
    # única diferencia observable en esta ruta, y es la que hace que el día que
    # TRIBUTA_SM_REM gane granularidad de sección el PADDS no se vuelva 'perdida'.
    lineas = []
    ada = _mk_ada([_a(_PADDS, "SOFIA"), _a("AG_Alta programa salud mental", "JUAN")])
    E = tp.procesar(ada, maestro=_mk_maestro(_MAESTRO), mes=(2026, 7), log=lineas.append)
    assert len(E) == 1, f"esperaba 1 perdida (solo JUAN), hubo {len(E)}"
    assert E.iloc[0]["profesional"] == "JUAN"
    txt = "\n".join(lineas)
    assert "FUERA del universo SM" in txt, txt
    assert "padds" in txt.lower(), txt


def test_padds_fuera_del_universo_sin_maestro():
    # Sin Maestro la heurística NO matchea el PADDS -> antes salía como PERDIDA (falso
    # positivo). La exclusión vive al nivel SM-ish justamente para cubrir esta ruta.
    E = _run([_a(_PADDS, "SOFIA")], con_maestro=False)
    assert len(E) == 0, f"el PADDS no es trabajo perdido de SM, hubo {len(E)}"


def test_vdi_sm_no_se_excluye_de_mas():
    # Guarda simétrica: la VDI de SM (A26 sección A) sigue tributando, con y sin Maestro.
    assert len(_run([_a(_VDI_SM, "ANA")])) == 0
    assert len(_run([_a(_VDI_SM, "ANA")], con_maestro=False)) == 0


def test_por_funcionario_rankea():
    E = _run([_a("AG_Alta programa salud mental", "JUAN"),
              _a("AG_Atencion de salud mental adolescente", "JUAN"),
              _a("AG_Alta programa salud mental", "ANA")])
    pf = E.attrs["tablas"]["Por_Funcionario"]
    assert pf.iloc[0]["Funcionario"] == "JUAN"
    assert int(pf.iloc[0]["N a saco roto"]) == 2


def test_sin_maestro_usa_heuristica():
    # Sin Maestro: 'AG_Alta programa salud mental' es SM-ish y no matchea heurística -> PERDIDA.
    E = _run([_a("AG_Alta programa salud mental", "JUAN"),
              _a("Consulta De Salud Mental", "ANA")], con_maestro=False)
    assert len(E) == 1
    assert E.iloc[0]["num_rem"] == "(sin maestro)"


def test_solo_del_mes():
    E = _run([_a("AG_Alta programa salud mental", "JUAN", fecha="10/07/2026"),
              _a("AG_Alta programa salud mental", "JUAN", fecha="10/06/2026")])
    assert len(E) == 1, "solo la atención de julio cuenta"


# -- Auditorías por ATEN ID: control sin formulario / SM sin consejería --
_FORM_OK = "COLUMBIA-ESCALA DE SEVERIDAD SUICIDA (C-SSRS) 8  ;  Control de Salud Mental"
_CONS = "Prioridad - con integrante con problema de salud mental"


def test_control_sin_formulario():
    E = _run([_a("Controles Salud Mental", "ANA", id="A1", form=_FORM_OK),         # ok
              _a("Controles Salud Mental", "JUAN", run="2-7", id="A2",
                 form="MINIMENTAL ABREVIADO ; Otro formulario"),                   # minimental NO
              _a("Controles de Salud Mental por videollamadas", "LUCIA", id="A3"),  # remoto cuenta
              _a("Acciones remotas de salud mental por llamada", "PEDRO", id="A4"),  # no cuenta
              _a("Consulta De Salud Mental", "ANA", id="A5")])                     # no es control
    t = E.attrs["tablas"]["Ctrl_sin_Formulario"]
    assert sorted(t["aten_id"]) == ["A2", "A3"], list(t["aten_id"])
    assert set(t.columns) >= {"run", "profesional", "estamento"}


def test_sin_formulario_clinico_no_calcula_y_avisa():
    # El test base sin la columna FORMULARIOS CLINICOS = Monitoreo admin: no un 0 callado.
    global _ADA_HDR
    viejo = _ADA_HDR
    _ADA_HDR = viejo[:-1]
    try:
        E = _run([_a("Controles Salud Mental", "ANA")])
    finally:
        _ADA_HDR = viejo
    assert "Ctrl_sin_Formulario" not in E.attrs["tablas"]
    assert any(a[1] == "NO CALCULADO" for a in E.attrs["avisos"]), E.attrs["avisos"]


def test_sm_sin_consejeria_por_atencion():
    _vdi = "Visita domiciliaria integral familia con integrante con problema de salud mental"
    E = _run([_a("Controles Salud Mental", "ANA", id="B1", form=_FORM_OK),
              _a(_CONS, "ANA", id="B1", form=_FORM_OK),                   # misma atencion -> ok
              _a("Consulta De Salud Mental", "JUAN", id="B2"),              # sin consejeria
              _a(_vdi, "SOFIA", id="B3"),                                   # sin consejeria
              _a(_CONS, "SOFIA", id="B4"),                                  # consejeria en OTRA atencion
              _a("Curacion simple", "PEDRO", id="B5")])                     # no SM
    t = E.attrs["tablas"]["Sin_Consejeria"]
    assert sorted(t["aten_id"]) == ["B2", "B3"], list(t["aten_id"])


def test_aten_id_numerico_como_iris():
    # IRIS trae el ATEN ID como número (683.016.530,00 en Excel), float en una fila.
    E = _run([_a("Controles Salud Mental", "ANA", id=683016530.0, form=_FORM_OK),
              _a(_CONS, "ANA", id=683016530),                              # misma atencion
              _a("Consulta De Salud Mental", "JUAN", id=689438471.0)])
    t = E.attrs["tablas"]["Sin_Consejeria"]
    assert list(t["aten_id"]) == ["689438471"], list(t["aten_id"])


# -- Guardarraíl de mes vacío (CLAUDE.md §3: fail loud, como el A05) --
def test_mes_sin_datos_falla_duro():
    """Un ADA que no cubre el mes daría 0 perdidas, y eso se lee como la buena
    noticia que no es. Es archivo/mes equivocado -> ArchivoInvalido."""
    try:
        _run([_a("AG_Alta programa salud mental", "JUAN", fecha="10/07/2025")], mes=(2026, 7))
    except ArchivoInvalido as e:
        assert e.categoria == "mes_vacio" and "07/2026" in str(e)
        return
    raise AssertionError("un ADA que no cubre el mes debió levantar ArchivoInvalido")


def test_cero_perdidas_con_el_mes_cubierto_no_falla():
    """La guarda es sobre la FUENTE: con el mes cubierto, 0 perdidas es un
    resultado legítimo (y el ideal), no un error."""
    E = _run([_a("Consulta De Salud Mental", "ANA", fecha="10/07/2026")])   # tributa -> nada perdido
    assert len(E) == 0


def test_guarda_multihoja_rechaza():
    # ADA con datos en 2 hojas = modificado -> el loader debe rechazar.
    p = _TMP / "modificado.xlsx"
    wb = openpyxl.Workbook(); ws = wb.active
    ws.append(_ADA_HDR); ws.append(["1-1", "AT1", "10/07/2026", "Consulta De Salud Mental",
                                    "x", "Médico(a)", "ANA", "Esp", "F", "30 años"])
    wb.create_sheet("TablaDinamica").append(["pivote", "aqui"])
    wb.save(p)
    try:
        tp.procesar(p, mes=(2026, 7), log=_quiet)
        assert False, "debió rechazar el archivo modificado"
    except ArchivoInvalido as e:
        assert e.categoria == "modificado"


def test_guarda_una_hoja_pasa():
    p = _mk_ada([_a("Consulta De Salud Mental", "ANA")])   # 1 hoja con datos -> pasa
    verificar_hoja_unica(p)   # no debe levantar


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
            import traceback
            fallos += 1; print(f"ERROR {fn.__name__} -> {type(e).__name__}: {e}")
            traceback.print_exc()
    print("-" * 50)
    print(f"{len(pruebas) - fallos}/{len(pruebas)} OK" + (f" ({fallos} problemas)" if fallos else ""))
    return 1 if fallos else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(_main())
