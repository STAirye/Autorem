#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# SPDX-License-Identifier: GPL-3.0-or-later
# ==========================================================================
"""Pruebas del módulo REM SM Actividades. Datos SINTÉTICOS. Correr:
    python tests/test_sm_actividades.py"""

import sys
import tempfile
from datetime import date
from pathlib import Path

import openpyxl

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
import _aislar_cache   # noqa: E402,F401  (PRIMERO: nunca tocar el ~/.autorem real)

import modulos.rem_sm_actividades as sm   # noqa: E402
from programas.rem_utils import ArchivoInvalido   # noqa: E402

_TMP = Path(tempfile.mkdtemp(prefix="autorem_sm_"))

_ADA_HDR = ["NUMERO TIPO IDENTIFICACION", "ATEN ID", "FECHA ATENCION", "ACTIVIDADES",
            "DIAGNOSTICOS", "INSTRUMENTO", "TIPO ATENCION", "SEXO", "AÑOS ATENCION",
            "ALERTAS ADMINISTRATIVAS", "ES IMIGRANTE", "PUEBLO ORIGINARIO", "FORMULARIOS CLINICOS"]
_GRP_HDR = ["NUMERO TIPO IDENTIFICACION", "FECHA ATENCION", "ACTIVIDADES",
            "ASISTE (SI/NO)", "SEXO", "EDAD", "INSTRUMENTO", "FUNCIONARIO PRESTADOR"]

# alias cortos -> nombre real de columna
_ADA_K = {"run": 0, "id": 1, "fecha": 2, "act": 3, "dg": 4, "instr": 5, "tipo": 6, "sexo": 7, "edad": 8,
          "alertas": 9, "emig": 10, "pueblo": 11, "formclin": 12}
_GRP_K = {"run": 0, "fecha": 1, "act": 2, "asiste": 3, "sexo": 4, "edad": 5, "instr": 6, "prest": 7}


def _mk(hdr, keymap, rows, nombre):
    p = _TMP / nombre
    wb = openpyxl.Workbook(); ws = wb.active
    ws.append(hdr)
    for r in rows:
        line = [""] * len(hdr)
        for k, v in r.items():
            line[keymap[k]] = v
        ws.append(line)
    wb.save(p)
    return p


def _mk_ada(rows):
    return _mk(_ADA_HDR, _ADA_K, rows, "ada.xlsx")


def _mk_grupal(rows):
    return _mk(_GRP_HDR, _GRP_K, rows, "grupal.xlsx")


_INS_HDR = ["NUMERO TIPO IDENTIFICACION", "SEXO", "GENERO", "ESTADO", "SITUACION",
            "ALERTAS ADMINISTRATIVAS", "PUEBLO INDIG"]
_INS_DEFAULT = {"ESTADO": "Activo", "SITUACION": "Inscrito"}


def _mk_inscritos(rows):
    p = _TMP / "inscritos.xlsx"
    wb = openpyxl.Workbook(); ws = wb.active; ws.append(_INS_HDR)
    for r in rows:
        r = {**_INS_DEFAULT, **r}
        ws.append([r.get(h, "") for h in _INS_HDR])
    wb.save(p)
    return p


def _mk_multi(rows):
    """Monitoreo Multiprofesional sintético: [ATEN ID, Multiprofesional-1]."""
    p = _TMP / "multi.xlsx"
    wb = openpyxl.Workbook(); ws = wb.active; ws.append(["ATEN ID", "Multiprofesional-1"])
    for r in rows:
        ws.append([r.get("aten", ""), r.get("m1", "")])
    wb.save(p)
    return p


def _quiet(*_a, **_k): pass


# Tabla de dotación VACÍA explícita en cada llamada a procesar(): sin esto,
# procesar() cae al caché real del usuario (~/.autorem/dotacion.json) y estos
# tests dejarían de ser deterministas apenas alguien use el diálogo de verdad.
_SIN_DOTACION = {"funcionarios": {}, "omitidos": {}}


# El guardarraíl de mes (rem_utils.filtrar_mes) exige que el ADA CUBRA el mes pedido.
# Los tests que solo miran el grupal necesitan una fila de relleno en el ADA: del mes,
# pero de una actividad que no tributa a ninguna casilla SM (no mueve ningún conteo).
_RELLENO_ADA = [{"run": "Z", "id": "Z1", "fecha": date(2026, 7, 15), "act": "Curacion simple",
                 "instr": "Enfermero(a)", "sexo": "Hombre", "edad": 50}]


def _run(ada_rows, grupal_rows=None, mes=(2026, 7)):
    ada = _mk_ada(ada_rows)
    grupal = _mk_grupal(grupal_rows) if grupal_rows is not None else None
    E = sm.procesar(ada, grupal=grupal, mes=mes, log=_quiet, dotacion_tabla=_SIN_DOTACION)
    return E, E.attrs["tablas"]


def _n(E, casilla, sub=None):
    m = E["casilla"] == casilla
    if sub is not None:
        m = m & (E["sub"] == sub)
    return int(m.sum())


def _cell(tabla, col_key, col_val, dato):
    """Valor de `dato` en la fila donde tabla[col_key]==col_val."""
    fila = tabla[tabla[col_key] == col_val].iloc[0]
    return fila[dato]


def _a06_tot(tabla, col):
    """Suma `col` en las filas de estamento de A06 (ya no hay fila TOTAL; el grupal
    'Intervención Psicosocial Grupal' se excluye)."""
    ests = tabla[tabla["Profesional"] != "Intervención Psicosocial Grupal"]
    return int(ests[col].sum())


# -- A04: consultas médicas SM (solo médico) --
def test_a04_solo_medico():
    E, t = _run([
        {"run": "A", "id": "1", "fecha": date(2026, 7, 3), "act": "Consulta De Salud Mental  ;",
         "instr": "Médico", "sexo": "Mujer", "edad": 30},
        {"run": "B", "id": "2", "fecha": date(2026, 7, 4), "act": "Consulta De Salud Mental  ;",
         "instr": "Psicólogo(a)", "sexo": "Hombre", "edad": 20},   # NO médico -> fuera de A04
    ])
    assert _n(E, "A04") == 1
    assert _cell(t["A04_Consultas_Medicas"], "Consulta", "Salud Mental", "Ambos") == 1
    assert _cell(t["A04_Consultas_Medicas"], "Consulta", "Salud Mental", "Mujeres") == 1


# -- A06: controles por estamento + SENAME excluido --
def test_a06_controles_estamento_y_sename():
    E, t = _run([
        {"run": "A", "id": "1", "fecha": date(2026, 7, 3), "act": "Controles Salud Mental  ;",
         "instr": "Médico", "sexo": "Hombre", "edad": 40},
        {"run": "B", "id": "2", "fecha": date(2026, 7, 4), "act": "Controles Salud Mental  ;",
         "instr": "Psicólogo(a)", "sexo": "Mujer", "edad": 8},
        {"run": "C", "id": "3", "fecha": date(2026, 7, 5), "act": "Control Salud Mental a Paciente SENAME  ;",
         "instr": "Psicólogo(a)", "sexo": "Hombre", "edad": 12},   # SENAME -> string aparte, excluido
    ])
    assert _n(E, "A06") == 2
    a06 = t["A06_Controles"]
    assert _cell(a06, "Profesional", "Médico/a", "Ambos") == 1
    assert _cell(a06, "Profesional", "Psicólogo/a", "Ambos") == 1
    assert _a06_tot(a06, "Ambos") == 2
    assert _cell(a06, "Profesional", "Psicólogo/a", "5-9 M") == 1   # edad 8, mujer


# -- ADA cuenta por ATEN ID (distinct), no por fila --
def test_ada_conteo_por_atenid():
    E, _ = _run([
        {"run": "A", "id": "1", "fecha": date(2026, 7, 3), "act": "Controles Salud Mental  ;", "instr": "Médico", "edad": 30},
        {"run": "A", "id": "1", "fecha": date(2026, 7, 3), "act": "Controles Salud Mental  ;", "instr": "Médico", "edad": 30},  # MISMO ATEN ID
        {"run": "A", "id": "2", "fecha": date(2026, 7, 9), "act": "Controles Salud Mental  ;", "instr": "Médico", "edad": 30},  # otra atención
    ])
    assert _n(E, "A06") == 2   # dos ATEN ID distintos (la fila repetida NO suma)


# -- Grupal cuenta por ASISTENCIA (sin dedup) + filtro Asiste=SI --
def test_grupal_por_asistencia():
    E, t = _run(_RELLENO_ADA, grupal_rows=[
        # EDAD en TEXTO ('30 años…') como viene del export crudo del grupal
        {"run": "P", "fecha": date(2026, 7, 5), "act": "Intervencion psicosocial grupal.", "asiste": "SI", "sexo": "Mujer", "edad": "30 años 2 meses 1 día"},
        {"run": "P", "fecha": date(2026, 7, 5), "act": "Intervencion psicosocial grupal.", "asiste": "SI", "sexo": "Mujer", "edad": "31 años"},  # mismo día, 2º taller -> cuenta 2
        {"run": "Q", "fecha": date(2026, 7, 6), "act": "Intervencion psicosocial grupal.", "asiste": "NO", "sexo": "Hombre", "edad": "40 años"},  # no asiste -> fuera
    ])
    assert _n(E, "A06PG") == 2
    pg = _cell_row(t["A06_Controles"], "Profesional", "Intervención Psicosocial Grupal")
    assert pg["Ambos"] == 2 and pg["Mujeres"] == 2
    assert pg["30-34 M"] == 2      # ambas mujeres 30/31 caen en la banda 30-34 (EDAD texto parseada)


# -- Ventana de mes (por FECHA ATENCIÓN) --
def test_ventana_de_mes():
    E, _ = _run(
        [{"run": "A", "id": "1", "fecha": date(2026, 6, 30), "act": "Controles Salud Mental  ;", "instr": "Médico", "edad": 30},
         {"run": "B", "id": "2", "fecha": date(2026, 7, 1), "act": "Controles Salud Mental  ;", "instr": "Médico", "edad": 30}],
        # el grupal SÍ cubre julio (si no, el guardarraíl de mes lo rechazaría), pero
        # esa fila no asistió; la que asiste es de agosto -> ninguna de las dos cuenta
        grupal_rows=[{"run": "P", "fecha": date(2026, 7, 20), "act": "Intervencion psicosocial grupal.", "asiste": "NO", "edad": 30},
                     {"run": "Q", "fecha": date(2026, 8, 1), "act": "Intervencion psicosocial grupal.", "asiste": "SI", "edad": 30}],
    )
    assert _n(E, "A06") == 1        # solo la de julio
    assert _n(E, "A06PG") == 0      # una es de agosto, la otra no asistió


# -- A19a: ADA (individual) + grupal, y el guion evita comerse las VDI de A26 --
def test_a19a_ada_mas_grupal_sin_vdi():
    E, t = _run(
        [{"run": "A", "id": "1", "fecha": date(2026, 7, 3), "instr": "Psicólogo(a)",
          "act": "Consejerías familiares - Temas Prioridad - Con integrante con problema de salud mental (Ind)  ;", "edad": 40},
         {"run": "B", "id": "2", "fecha": date(2026, 7, 4), "instr": "Médico",
          "act": "Visita domiciliaria integral familia con integrante con problema de salud mental - Primera visita  ;", "edad": 50}],
        grupal_rows=[{"run": "C", "fecha": date(2026, 7, 5), "asiste": "SI", "edad": 35,
                      "act": "Consejerías familiares - Temas Prioridad - Con integrante con problema de salud mental (Grp)"}],
    )
    assert _n(E, "A19a", "97") == 2          # 1 ADA + 1 grupal (la VDI NO cuenta acá)
    assert _n(E, "A26") == 1                 # la VDI va a A26
    a19 = t["A19a_Consejerias_Fam"]
    fila = a19[a19["Tema prioridad (familiar)"] == "Con integrante con problema de salud mental"].iloc[0]
    assert fila["Total Actividades"] == 2 and fila["  · desde ADA (individual)"] == 1 and fila["  · desde Grupal"] == 1


# -- A26: split etario 5-9 (A.31) excluye de A.30, + secuencia de visita --
def test_a26_split_5a9_y_visita():
    E, t = _run([
        {"run": "K", "id": "1", "fecha": date(2026, 7, 3), "instr": "Médico", "edad": 7,
         "act": "Visita domiciliaria integral familia con integrante con problema de salud mental - Primera visita  ;"},
        {"run": "L", "id": "2", "fecha": date(2026, 7, 4), "instr": "Médico", "edad": 45,
         "act": "Visita domiciliaria integral familia con integrante con problema de salud mental - Tercera o más visitas de seguimiento  ;"},
    ])
    a26 = t["A26_VDI_SM"]
    r30 = a26[a26["Concepto"].str.startswith("A.30")].iloc[0]
    r31 = a26[a26["Concepto"].str.startswith("A.31")].iloc[0]
    assert r30["Total"] == 1 and r30["Tercera o Más"] == 1     # adulto 45
    assert r31["Total"] == 1 and r31["Primera Visita"] == 1     # niño 7
    assert r30["Un Profesional"] == 1                          # default mono-profesional


def test_a26_multiprofesional():
    """Con el Monitoreo Multiprofesional, las VDI cuya ATEN ID está en el reporte
    (Multiprofesional-1 no vacío) pasan a 'Dos o Más Prof.'; el resto queda mono."""
    ada = _mk_ada([
        {"run": "K", "id": "1", "fecha": date(2026, 7, 3), "instr": "Médico", "edad": 45,
         "act": "Visita domiciliaria integral familia con integrante con problema de salud mental - Primera visita  ;"},
        {"run": "L", "id": "2", "fecha": date(2026, 7, 4), "instr": "Médico", "edad": 50,
         "act": "Visita domiciliaria integral familia con integrante con problema de salud mental - Primera visita  ;"},
    ])
    mp = _mk_multi([{"aten": "1", "m1": "Enfermero(a)"}, {"aten": "2", "m1": ""}])  # solo la 1 es multi
    E = sm.procesar(ada, multiprofesional=str(mp), mes=(2026, 7), log=_quiet, dotacion_tabla=_SIN_DOTACION)
    r30 = _cell_row(E.attrs["tablas"]["A26_VDI_SM"], "Concepto",
                    "A.30 Familia con integrante con problema de salud mental")
    assert r30["Total"] == 2 and r30["Dos o Más Prof."] == 1 and r30["Un Profesional"] == 1


# -- A32 F1: desagregado llamada / videollamada / mensaje (video != llamada) --
def test_a32f1_desagregado():
    E, t = _run([
        {"run": "A", "id": "1", "fecha": date(2026, 7, 3), "instr": "Psicólogo(a)", "edad": 30,
         "act": "Acciones remotas de salud mental - Llamadas telefónicas  ;"},
        {"run": "B", "id": "2", "fecha": date(2026, 7, 4), "instr": "Psicólogo(a)", "edad": 20,
         "act": "Acciones remotas de salud mental - Videollamadas  ;"},
        {"run": "C", "id": "3", "fecha": date(2026, 7, 5), "instr": "Psicólogo(a)", "edad": 40,
         "act": "Acciones remotas de salud mental - Mensajería de texto  ;"},
    ])
    f1 = t["A32_F1_Acciones_Remotas"]
    assert _cell(f1, "Vía", "Llamadas Telefónicas", "Total") == 1
    assert _cell(f1, "Vía", "Videollamadas", "Total") == 1
    assert _cell(f1, "Vía", "Mensajería de Texto", "Total") == 1
    assert _n(E, "A32F1") == 3


# -- A27: A = asistentes (usuarios), B = sesiones (por prestador/fecha/actividad) --
def test_a27_asistentes_y_sesiones():
    E, t = _run(_RELLENO_ADA, grupal_rows=[
        {"run": "X", "fecha": date(2026, 7, 10), "asiste": "SI", "edad": 30, "prest": "Dra A",
         "act": "Educación en grupo - Prevención de salud mental - Prevención trastorno mental"},
        {"run": "Y", "fecha": date(2026, 7, 10), "asiste": "SI", "edad": 40, "prest": "Dra A",
         "act": "Educación en grupo - Prevención de salud mental - Prevención trastorno mental"},  # misma sesión
    ])
    a27 = t["A27_Educacion_Prev"]
    fila = a27[a27["Área temática"] == "Prevención trastorno mental"].iloc[0]
    assert fila["Total"] == 2
    ses = t["A27_B_Sesiones"]
    assert ses[ses["Área temática"] == "Prevención trastorno mental"].iloc[0]["B · Sesiones (actividades)"] == 1


# -- Demografía: SENAME / Mejor Niñez / migrante / pueblo / demencia (Beneficiarios=todos) --
def test_demografia_flags():
    E, t = _run([
        {"run": "A", "id": "1", "fecha": date(2026, 7, 3), "act": "Controles Salud Mental  ;",
         "instr": "Médico", "edad": 40, "emig": "SI", "pueblo": "Mapuche"},
        {"run": "B", "id": "2", "fecha": date(2026, 7, 4), "act": "Controles Salud Mental  ;",
         "instr": "Psicólogo(a)", "edad": 30, "alertas": "Programa SENAME - Ambulatorio",
         "dg": "F03.X-Demencia, No Especificada"},
        {"run": "C", "id": "3", "fecha": date(2026, 7, 5), "act": "Controles Salud Mental  ;",
         "instr": "Médico", "edad": 10, "alertas": "SPE ex Mejor Niñez- Ambulatorio", "pueblo": "Ninguno"},
    ])
    a06 = t["A06_Controles"]
    assert _a06_tot(a06, "Beneficiarios") == 3        # todos (Fonasa)
    assert _a06_tot(a06, "Migrantes") == 1            # A
    assert _a06_tot(a06, "Pueblos Originarios") == 1  # A (Mapuche); C=Ninguno no cuenta
    assert _a06_tot(a06, "SENAME") == 1               # B
    assert _a06_tot(a06, "Prot. Especializada") == 1  # C
    assert _a06_tot(a06, "Demencia") == 1             # B (norm: 'demencia' vs DIAG en MAYÚSCULA)
    assert _a06_tot(a06, "TRANS Masculino") == 0 and _a06_tot(a06, "TRANS Femenina") == 0   # sin inscritos


# -- Gestante: matrona + control prenatal en la ventana -> flag en el evento SM --
def test_gestante_flag():
    E, _ = _run([
        {"run": "G", "id": "1", "fecha": date(2026, 7, 2), "act": "Control Prenatal  ;",
         "instr": "Matron(a)", "edad": 25},
        {"run": "G", "id": "2", "fecha": date(2026, 7, 10), "act": "Controles Salud Mental  ;",
         "instr": "Psicólogo(a)", "edad": 25},
        {"run": "H", "id": "3", "fecha": date(2026, 7, 11), "act": "Controles Salud Mental  ;",
         "instr": "Médico", "edad": 40},
    ])
    a06 = E[E["casilla"] == "A06"]
    assert bool(a06.loc[a06["run"] == "G", "dem_gestante"].iloc[0]) is True
    assert bool(a06.loc[a06["run"] == "H", "dem_gestante"].iloc[0]) is False


def test_trans_inscritos_modificado():
    """Inscritos SIN columna GÉNERO (archivo modificado/otro reporte): trans_map levanta
    ArchivoInvalido (ronda 12: era un ValueError pelado, y `opcional()` tenia que atrapar
    ValueError para convertirlo -- o sea que cualquier bug de codigo dentro del bloque se
    presentaba como «tu archivo opcional no sirve»). Ronda 11 (decision del autor):
    procesar ya NO sigue callado con TRANS en 0 (quedaba solo en el log): levanta
    OpcionalInvalido('inscritos') y la GUI pregunta si seguir sin el. Sin el archivo,
    corre normal con TRANS en 0."""
    from programas.rem_utils import ArchivoInvalido, OpcionalInvalido, opcional
    p = _TMP / "inscritos_malo.xlsx"
    wb = openpyxl.Workbook(); ws = wb.active
    ws.append(["NUMERO TIPO IDENTIFICACION", "SEXO", "ESTADO", "SITUACION"])
    ws.append(["T", "Mujer", "Activo", "Inscrito"])  # sin GÉNERO
    wb.save(p)
    try:
        sm._cargar(_mk_ada([{"run": "T", "id": "1", "fecha": date(2026, 7, 3),
                             "act": "Controles Salud Mental  ;", "instr": "Médico", "edad": 30}]),
                   inscritos=str(p), log=_quiet, dotacion_tabla=_SIN_DOTACION)
        cat = None
    except OpcionalInvalido as e:
        cat = e.categoria
    assert cat == "sin_columnas", cat
    # Y `opcional` NO disfraza un bug de codigo de archivo invalido.
    try:
        with opcional("inscritos"):
            raise ValueError("bug de codigo, no del archivo")
        assert False, "el ValueError no llego"
    except OpcionalInvalido:
        assert False, "opcional() convirtio un ValueError de codigo en «archivo invalido»"
    except ValueError:
        pass
    ada = _mk_ada([{"run": "T", "id": "1", "fecha": date(2026, 7, 3),
                    "act": "Controles Salud Mental  ;", "instr": "Médico", "edad": 30}])
    try:
        sm.procesar(ada, inscritos=str(p), mes=(2026, 7), log=_quiet, dotacion_tabla=_SIN_DOTACION)
        assert False, "debio levantar OpcionalInvalido"
    except OpcionalInvalido as e:
        assert e.entrada == "inscritos", e.entrada
    E = sm.procesar(ada, inscritos=None, mes=(2026, 7), log=_quiet, dotacion_tabla=_SIN_DOTACION)
    a06 = E.attrs["tablas"]["A06_Controles"]
    assert _a06_tot(a06, "TRANS Masculino") == 0 and _a06_tot(a06, "TRANS Femenina") == 0


def _cell_row(tabla, col_key, col_val):
    return tabla[tabla[col_key] == col_val].iloc[0]


# -- TRANS: selección explícita en GÉNERO del padrón de Inscritos, split M/F --
def test_trans_flag():
    ins = _mk_inscritos([
        {"NUMERO TIPO IDENTIFICACION": "T", "SEXO": "Mujer", "GENERO": "Transgénero Masculino"},
        {"NUMERO TIPO IDENTIFICACION": "U", "SEXO": "Hombre", "GENERO": "Masculino"},       # cis
        {"NUMERO TIPO IDENTIFICACION": "V", "SEXO": "Hombre", "GENERO": "Femenino Trans"},
        {"NUMERO TIPO IDENTIFICACION": "W", "SEXO": "Mujer", "GENERO": "Masculino"},        # implícita
        {"NUMERO TIPO IDENTIFICACION": "X", "SEXO": "Hombre", "GENERO": "No binarie"},      # no cuenta
    ])
    ada = _mk_ada([
        {"run": "T", "id": "1", "fecha": date(2026, 7, 3), "act": "Controles Salud Mental  ;", "instr": "Médico", "edad": 30},
        {"run": "U", "id": "2", "fecha": date(2026, 7, 4), "act": "Controles Salud Mental  ;", "instr": "Médico", "edad": 30},
        {"run": "V", "id": "3", "fecha": date(2026, 7, 5), "act": "Controles Salud Mental  ;", "instr": "Psicólogo(a)", "edad": 30},
        {"run": "W", "id": "4", "fecha": date(2026, 7, 6), "act": "Controles Salud Mental  ;", "instr": "Médico", "edad": 30},
        {"run": "X", "id": "5", "fecha": date(2026, 7, 7), "act": "Controles Salud Mental  ;", "instr": "Médico", "edad": 30},
    ])
    E = sm.procesar(ada, inscritos=ins, mes=(2026, 7), log=_quiet, dotacion_tabla=_SIN_DOTACION)
    a06 = E.attrs["tablas"]["A06_Controles"]
    assert _a06_tot(a06, "TRANS Masculino") == 2   # T (explícita) + W (Mujer + Masculino)
    assert _a06_tot(a06, "TRANS Femenina") == 1    # V (Femenino Trans)
    assert not bool(E.loc[E["run"] == "X", "dem_trans_m"].iloc[0])   # X no binarie
    assert not bool(E.loc[E["run"] == "X", "dem_trans_f"].iloc[0])
    assert not bool(E.loc[E["run"] == "U", "dem_trans_m"].iloc[0])   # U cis
    assert not bool(E.loc[E["run"] == "U", "dem_trans_f"].iloc[0])


# ======================================================================
# Guardarraíl de mes vacío (CLAUDE.md §3: fail loud, como el A05)
# ======================================================================
def test_mes_sin_datos_falla_duro():
    """El ADA del año pasado (o el mes mal elegido en el spinbox) NO puede producir
    un .xlsx con todas las tablas en cero: eso se copia al SA_26 como si fuera real."""
    try:
        _run([{"run": "A", "id": "1", "fecha": date(2025, 7, 3), "act": "Controles Salud Mental  ;",
               "instr": "Médico", "sexo": "Mujer", "edad": 30}], mes=(2026, 7))
    except ArchivoInvalido as e:
        assert e.categoria == "mes_vacio"
        assert "07/2026" in str(e) and "07/2025" in str(e)   # mes pedido y span real
        return
    raise AssertionError("un ADA que no cubre el mes debió levantar ArchivoInvalido")


def test_fechas_ilegibles_falla_distinto():
    """Todas las fechas ilegibles no es lo mismo que 'otro mes': mensaje aparte,
    porque lo que hay que revisar es el archivo, no el spinbox."""
    try:
        _run([{"run": "A", "id": "1", "fecha": "no-es-fecha", "act": "Controles Salud Mental  ;",
               "instr": "Médico", "sexo": "Mujer", "edad": 30}], mes=(2026, 7))
    except ArchivoInvalido as e:
        assert e.categoria == "mes_vacio" and "legible" in str(e)
        return
    raise AssertionError("un ADA sin fechas legibles debió levantar ArchivoInvalido")


def test_casilla_en_cero_con_el_mes_cubierto_no_falla():
    """El corazón del guardarraíl: la guarda es sobre la FUENTE, no sobre la casilla.
    Con el mes cubierto, A27/A32 en 0 son legítimos (CLAUDE.md los da por esperables)
    y la corrida tiene que llegar hasta las tablas."""
    E, t = _run([{"run": "A", "id": "1", "fecha": date(2026, 7, 3), "act": "Controles Salud Mental  ;",
                  "instr": "Médico", "sexo": "Mujer", "edad": 30}])
    assert _n(E, "A06") == 1
    a27 = t["A27_Educacion_Prev"]
    assert int(a27["Total"].sum()) == 0        # 0 legítimo, sin excepción
    assert int(t["A32_F1_Acciones_Remotas"]["Total"].sum()) == 0


def test_grupal_de_otro_mes_falla_duro():
    """El grupal es opcional, pero si se CARGA tiene que cubrir el mes: si no,
    A06 psicosocial / A19a grupal / A27 salen en cero sin que nadie lo note."""
    try:
        _run([{"run": "A", "id": "1", "fecha": date(2026, 7, 3), "act": "Controles Salud Mental  ;",
               "instr": "Médico", "sexo": "Mujer", "edad": 30}],
             grupal_rows=[{"run": "P", "fecha": date(2026, 3, 5), "asiste": "SI", "edad": 30,
                           "act": "Intervencion psicosocial grupal."}])
    except ArchivoInvalido as e:
        assert e.categoria == "mes_vacio" and "Grupales" in str(e)
        return
    raise AssertionError("un grupal que no cubre el mes debió levantar ArchivoInvalido")


def test_grupal_del_mes_sin_asistencias_no_falla():
    """…pero el filtro Asiste=SI va DESPUÉS del guardarraíl: un mes con talleres
    a los que nadie asistió es un 0 legítimo, no un archivo equivocado."""
    E, t = _run([{"run": "A", "id": "1", "fecha": date(2026, 7, 3), "act": "Controles Salud Mental  ;",
                  "instr": "Médico", "sexo": "Mujer", "edad": 30}],
                grupal_rows=[{"run": "P", "fecha": date(2026, 7, 5), "asiste": "NO", "edad": 30,
                              "act": "Intervencion psicosocial grupal."}])
    assert _n(E, "A06PG") == 0
    assert _cell_row(t["A06_Controles"], "Profesional", "Intervención Psicosocial Grupal")["Ambos"] == 0


def test_ada_del_mes_sin_nada_que_tribute_falla_en_la_fuente():
    """Ronda 9: el ADA cubre el mes (filtrar_mes pasa) pero NINGUNA fila tributa a SM
    -> antes salía el REM SM ENTERO en 0 con "Listo" y sin aviso. Una casilla en 0 es
    legítima; TODAS en 0 (E vacío) es el gemelo por programa del mes_vacio."""
    try:
        _run(_RELLENO_ADA)
        assert False, "debió levantar ArchivoInvalido"
    except ArchivoInvalido as e:
        assert e.categoria == "sin_datos", e.categoria
    # el grupal solo (con asistencias) SÍ basta: no es un REM vacío
    E, _ = _run(_RELLENO_ADA, grupal_rows=[{"run": "P", "fecha": date(2026, 7, 5), "asiste": "SI",
                                           "act": "Intervencion psicosocial grupal.", "edad": 30}])
    assert _n(E, "A06PG") == 1


def test_asiste_sin_si_ni_no_no_es_nadie_asistio():
    """Ronda 9: una ASISTE en blanco (o 'S') se filtraba como si fuera NO, y A27 / A06
    grupal / A19a grupal salían en 0 callados. Toda la columna sin SI/NO ->
    ArchivoInvalido; algunas filas -> aviso SUBCONTADO (las SI siguen contando)."""
    ada = [{"run": "A", "id": "1", "fecha": date(2026, 7, 3), "act": "Controles Salud Mental  ;",
            "instr": "Médico", "edad": 30}]
    taller = {"run": "P", "fecha": date(2026, 7, 5), "act": "Intervencion psicosocial grupal.", "edad": 30}
    for raro in ("", "S"):
        try:
            _run(ada, grupal_rows=[dict(taller, asiste=raro)])
            assert False, f"ASISTE={raro!r} en todas: debió levantar ArchivoInvalido"
        except ArchivoInvalido as e:
            assert e.categoria == "sin_datos", e.categoria
    E, _ = _run(ada, grupal_rows=[dict(taller, asiste="SI"), dict(taller, asiste="")])
    assert _n(E, "A06PG") == 1
    assert any(a[1] == "SUBCONTADO" and "ASISTE" in a[2] for a in E.attrs["avisos"]), E.attrs["avisos"]
    # un NO explícito sigue siendo legítimo: 0 sin aviso
    E, _ = _run(ada, grupal_rows=[dict(taller, asiste="NO")])
    assert _n(E, "A06PG") == 0
    assert not any("ASISTE" in a[2] for a in E.attrs["avisos"])


def test_sexo_o_edad_fuera_del_grid_se_avisa():
    """Ronda 9, 2a pasada: `grid` cuenta en Ambos una fila sin sexo Hombre/Mujer o sin
    edad, pero en ninguna columna H/M ni tramo -> las columnas que se pegan suman menos
    que el total, callado. Ahora aviso REVISAR con el conteo."""
    E, _ = _run([{"run": "A", "id": "1", "fecha": date(2026, 7, 3), "act": "Consulta De Salud Mental  ;",
                  "instr": "Médico", "sexo": "Intersexual", "edad": 30},
                 {"run": "B", "id": "2", "fecha": date(2026, 7, 3), "act": "Consulta De Salud Mental  ;",
                  "instr": "Médico", "sexo": "Mujer", "edad": ""}])
    av = [a for a in E.attrs["avisos"] if a[1] == "REVISAR" and "Ambos" in a[2]]
    assert av and "1 sin sexo" in av[0][2] and "1 sin edad" in av[0][2], E.attrs["avisos"]
    E, _ = _run([{"run": "A", "id": "1", "fecha": date(2026, 7, 3), "act": "Consulta De Salud Mental  ;",
                  "instr": "Médico", "sexo": "Mujer", "edad": 30}])
    assert not any("Ambos" in a[2] for a in E.attrs["avisos"])


def test_los_opcionales_ilegibles_son_opcional_invalido_y_se_validan_primero():
    """Ronda 12. Los tres opcionales del SM (Inscritos, Multiprofesional, Maestro) leian
    con `leer_xlsx` a mano, asi que el clasico .html/.xls disfrazado de .xlsx (CLAUDE.md
    SS13) salia como `BadZipFile`: `opcional()` no lo reconoce y la corrida ENTERA se
    caia, en vez de ofrecer seguir sin el. Y se validan ANTES del trabajo pesado: la GUI
    re-corre si el usuario dice que si."""
    from programas.rem_utils import (OpcionalInvalido, atenid_multiprofesional,
                                     cargar_maestro, opcional)
    falso = _TMP / "opcional_disfrazado.xlsx"
    falso.write_text("<html><body><table><tr><td>x</td></tr></table></body></html>", encoding="utf-8")
    for entrada, fn in (("inscritos", sm.cargar_inscritos), ("multiprofesional", atenid_multiprofesional),
                        ("maestro", cargar_maestro)):
        try:
            with opcional(entrada):
                fn(falso)
            assert False, f"{entrada}: debio levantar OpcionalInvalido"
        except OpcionalInvalido as e:
            assert e.entrada == entrada and e.categoria == "no_legible", (e.entrada, e.categoria)

    # Y `procesar` los valida antes de leer el ADA (que es el archivo grande).
    leidos = []
    previo = sm.cargar_atenciones     # el nombre que USA el modulo, no el de rem_utils
    sm.cargar_atenciones = lambda *a, **k: leidos.append(1) or previo(*a, **k)
    try:
        sm.procesar(_mk_ada([{"run": "T", "id": "1", "fecha": date(2026, 7, 3),
                              "act": "Controles Salud Mental  ;", "instr": "Médico", "edad": 30}]),
                    inscritos=str(falso), mes=(2026, 7), log=_quiet,
                    dotacion_tabla=_SIN_DOTACION)
        assert False, "debio levantar OpcionalInvalido"
    except OpcionalInvalido:
        assert not leidos, "el ADA se leyo ANTES de validar el opcional"
    finally:
        sm.cargar_atenciones = previo


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


# -- A32·F2: los nombres REALES de RAYEN llevan un "de" en medio --------
# Regresion de un bug silencioso (sep-2026): el patron era la subcadena contigua
# "controles salud mental por", que no matchea "Controles DE Salud Mental por
# llamadas telefonicas" -> F2 daba 0 SIEMPRE y el 0 se leia como "no hubo casos".
# Se descubrio porque esas atenciones aparecian en el reporte de Trabajo Perdido.
_F2_REALES = ["Controles de Salud Mental por llamadas telefónicas",
              "Controles de salud mental por videollamadas"]


def test_a32f2_nombres_reales_de_rayen():
    E, t = _run([
        {"run": "A", "id": "1", "fecha": date(2026, 7, 3), "instr": "Terapeuta Ocupacional",
         "edad": 30, "act": _F2_REALES[0] + "  ;"},
        {"run": "B", "id": "2", "fecha": date(2026, 7, 4), "instr": "Psicólogo(a)",
         "edad": 20, "act": _F2_REALES[1] + "  ;"},
    ])
    assert _n(E, "A32F2") == 2, "el patron viejo daba 0: F2 nunca matcheaba"
    f2ev = E[E["casilla"] == "A32F2"]
    assert set(f2ev["sub"]) == {"Llamadas Telefónicas", "Videollamadas"}
    # y llegan a la tabla, en la fila del estamento que las hizo
    import pandas as pd
    f2 = t["A32_F2_Controles_Remotos"]
    bandas = [c for c in f2.columns if c not in ("Control remoto por", "Profesional")]
    tot = f2[bandas].apply(pd.to_numeric, errors="coerce").sum().sum()
    assert tot > 0


def test_a32_no_se_arma_con_tokens_de_actividades_distintas():
    """Merge de la GUI 2.0 (1.9.17). Las mascaras del A32 son VARIOS tokens del nombre
    de UNA actividad ("Controles DE Salud Mental POR llamadas telefonicas"), y desde la
    ronda 12 la celda ACT trae TODAS las actividades de la atencion unidas: el AND los
    tomaba de actividades DISTINTAS. Las dos direcciones mueven una casilla del REM, y
    por eso las mascaras van `por_actividad` (ver rem_utils).

      atencion 1 - falso POSITIVO: "controles" de una actividad y "salud mental por" de
        otra armaban un A32F2 sin que exista ningun control remoto de SM.
      atencion 2 - falso NEGATIVO: el A32F2-Llamadas real se apagaba porque el
        ~videollamada de la mascara leia la palabra en la actividad HERMANA.
    """
    E, _ = _run([
        {"run": "A", "id": "1", "fecha": date(2026, 7, 3), "instr": "Psicólogo(a)", "edad": 30,
         "act": "Controles de pie diabético  ;  Consulta de salud mental por psicólogo  ;  "
                "Consulta de morbilidad por llamada telefónica  ;"},
        {"run": "B", "id": "2", "fecha": date(2026, 7, 4), "instr": "Psicólogo(a)", "edad": 20,
         "act": "Controles de Salud Mental por llamadas telefónicas  ;  "
                "Acciones remotas de salud mental - Videollamadas  ;"},
    ])
    a32 = E[E["casilla"].isin(("A32F1", "A32F2"))]
    assert set(a32["run"]) == {"B"}, "la atencion A no tiene ninguna actividad A32"
    assert set(zip(a32["casilla"], a32["sub"])) == {
        ("A32F2", "Llamadas Telefónicas"), ("A32F1", "Videollamadas")},         sorted(set(zip(a32["casilla"], a32["sub"])))


# ======================================================================
# Rango de meses (docs/rango_meses_plan.md §4.2, §6)
# ======================================================================
def test_rango_es_suma_de_mensuales_y_gestante_no_se_filtra_de_una():
    """El test principal del plan (§6.1): el rango == la suma de cada mes por
    separado, y la trampa de GESTANTE (§3 del plan) no se cuela -- si alguien
    volviera a filtrar el ADA por el rango ENTERO en vez del bucle mensual, G
    quedaría marcada gestante también en enero (el control prenatal es de marzo),
    y este test lo detectaría."""
    meses = [(2026, 1), (2026, 2), (2026, 3)]
    ada = _mk_ada([
        {"run": "G", "id": "G1", "fecha": date(2026, 1, 10), "act": "Controles Salud Mental  ;",
         "instr": "Psicólogo(a)", "sexo": "Mujer", "edad": 25},
        {"run": "A", "id": "A1", "fecha": date(2026, 1, 15), "act": "Controles Salud Mental  ;",
         "instr": "Médico", "sexo": "Hombre", "edad": 30},
        {"run": "B", "id": "B1", "fecha": date(2026, 2, 5), "act": "Controles Salud Mental  ;",
         "instr": "Médico", "sexo": "Mujer", "edad": 40},
        {"run": "G", "id": "G2", "fecha": date(2026, 3, 1), "act": "Control Prenatal  ;",
         "instr": "Matron(a)", "sexo": "Mujer", "edad": 25},
        {"run": "C", "id": "C1", "fecha": date(2026, 3, 10), "act": "Controles Salud Mental  ;",
         "instr": "Psicólogo(a)", "sexo": "Hombre", "edad": 20},
    ])
    E = sm.procesar_rango(ada, meses=meses, log=_quiet, dotacion_tabla=_SIN_DOTACION)
    assert _n(E, "A06") == 4   # G(ene) + A(ene) + B(feb) + C(mar)

    total = sum(_n(sm.procesar(ada, mes=m, log=_quiet, dotacion_tabla=_SIN_DOTACION), "A06")
               for m in meses)
    assert total == _n(E, "A06") == 4

    # la trampa: en enero, G NO lleva la marca (su ventana es nov-2025..ene-2026,
    # el control prenatal de marzo queda FUERA)
    ev_g_ene = E[(E["run"] == "G") & (E["mes"] == "2026-01")]
    assert len(ev_g_ene) == 1
    assert bool(ev_g_ene["dem_gestante"].iloc[0]) is False

    pm = E.attrs["tablas"]["Por_Mes"]
    assert pm["Total"].tolist() == E.attrs["tablas"]["SM_Resumen"]["Total mes"].tolist()
    assert set(pm.columns) >= {"Casilla", "Qué se registra", "2026-01", "2026-02", "2026-03", "Total"}


def test_rango_un_solo_mes_igual_a_procesar():
    """§6.4 del plan: con un solo mes, `procesar_rango` da las mismas tablas que
    `procesar` y sin hoja Por_Mes."""
    ada = _mk_ada([{"run": "A", "id": "1", "fecha": date(2026, 7, 3), "act": "Controles Salud Mental  ;",
                    "instr": "Médico", "sexo": "Mujer", "edad": 30}])
    E1 = sm.procesar(ada, mes=(2026, 7), log=_quiet, dotacion_tabla=_SIN_DOTACION)
    E2 = sm.procesar_rango(ada, meses=[(2026, 7)], log=_quiet, dotacion_tabla=_SIN_DOTACION)
    assert len(E1) == len(E2)
    assert E1.attrs["mes"] == E2.attrs["mes"] == (2026, 7)
    assert "Por_Mes" not in E2.attrs["tablas"]
    t1, t2 = E1.attrs["tablas"]["SM_Resumen"], E2.attrs["tablas"]["SM_Resumen"]
    assert t1["Total mes"].tolist() == t2["Total mes"].tolist()


def test_rango_mes_vacio_en_medio_falla_nombrandolo():
    """§6.3 del plan: un mes vacío en el medio del rango falla nombrándolo, aunque
    el resto del rango tenga datos."""
    ada = _mk_ada([
        {"run": "A", "id": "1", "fecha": date(2026, 1, 15), "act": "Controles Salud Mental  ;",
         "instr": "Médico", "sexo": "Hombre", "edad": 30},
        {"run": "C", "id": "2", "fecha": date(2026, 3, 10), "act": "Controles Salud Mental  ;",
         "instr": "Psicólogo(a)", "sexo": "Hombre", "edad": 20},
    ])
    try:
        sm.procesar_rango(ada, meses=[(2026, 1), (2026, 2), (2026, 3)], log=_quiet,
                          dotacion_tabla=_SIN_DOTACION)
        assert False, "debió levantar ArchivoInvalido"
    except ArchivoInvalido as e:
        assert "02/2026" in str(e), str(e)


_A2_REALES = ["Consultorías de salud mental adulto (Individual).",
              "Consultorías de salud mental infanto adolescente (Individual).",
              "Teleconsultorías de salud mental adulto (Individual).",
              "Teleconsultorías de salud mental infanto adolescente (Individual).",
              "Casos revisados consultoria salud mental (Individual)",
              "Casos revisados teleconsultoria salud mental (Individual)"]


def test_a06a2_consultorias_casos_y_numero_inferido():
    """2.0.20 (decisiones del autor): la consultoria es UNA reunion pero la ficha va por
    PACIENTE; Infanto/Adulto sale del NOMBRE de la actividad (15-19 cabe en las dos); el
    N° de consultorias = fechas distintas, INFERIDO, con aviso REVISAR obligatorio; un
    paciente con «Consultoria» + «Casos revisados» el mismo dia es UN caso."""
    ad, inf, tad, _, caso, _ = _A2_REALES
    E, t = _run([
        {"run": "A", "id": "1", "fecha": date(2026, 7, 3), "act": ad, "sexo": "Mujer", "edad": 17},
        {"run": "B", "id": "2", "fecha": date(2026, 7, 3), "act": ad, "sexo": "Hombre", "edad": 40},
        {"run": "A", "id": "3", "fecha": date(2026, 7, 3), "act": caso, "sexo": "Mujer", "edad": 17},
        {"run": "C", "id": "4", "fecha": date(2026, 7, 10), "act": inf, "sexo": "Hombre", "edad": 17},
        {"run": "D", "id": "5", "fecha": date(2026, 7, 12), "act": tad, "sexo": "Mujer", "edad": 30},
    ])
    a2 = t["A06_A2_Consultorias"]
    pres = a2[a2["Actividad"] == "Consultorías de Salud Mental"].iloc[0]
    tele = a2[a2["Actividad"] == "Teleconsultorías de Salud Mental"].iloc[0]
    assert pres["N° consultorías Adulto (INFERIDO)"] == 1, "A y B el mismo dia = UNA reunion"
    assert pres["N° consultorías Infanto Adolescente (INFERIDO)"] == 1
    assert pres["Ambos"] == 3, "A (consultoria + caso el mismo dia) cuenta UNA vez"
    assert pres["15-19 M"] == 1 and pres["15-19 H"] == 1, "15-19 en adulto Y en infanto"
    assert tele["N° consultorías Adulto (INFERIDO)"] == 1 and tele["Ambos"] == 1
    assert _n(E, "A06") == 0, "una consultoria no es un control de SM"
    assert any(a[0].startswith("A06-A.2") and a[1] == "REVISAR" for a in E.attrs["avisos"])


def test_a06a2_sale_aunque_sea_cero_y_sin_revisar():
    """El autor: la seccion se reporta aunque de 0. Sin registros no hay nada que
    inferir, asi que tampoco hay REVISAR."""
    E, t = _run([{"run": "A", "id": "1", "fecha": date(2026, 7, 3),
                  "act": "Controles Salud Mental  ;", "instr": "Médico", "sexo": "Hombre",
                  "edad": 40}])   # algo que tribute: un ADA sin nada de SM falla en la fuente
    a2 = t["A06_A2_Consultorias"]
    assert len(a2) == 2 and int(a2.select_dtypes("number").to_numpy().sum()) == 0
    assert not any(a[0].startswith("A06-A.2") for a in E.attrs["avisos"])


def test_a06a2_tributa_no_es_trabajo_perdido():
    """Las 6 actividades del Maestro para A06·A.2 traen «mental»: si no tributan, el
    Trabajo Perdido las acusa como saco roto."""
    import pandas as pd
    from programas.rem_utils import norm
    assert sm.mask_tributa_ada(pd.Series([norm(a) for a in _A2_REALES])).all()


def test_a32f2_tributa_no_es_trabajo_perdido():
    """`mask_tributa_ada` es la fuente unica de 'que tributa': si no las reconoce,
    las F2 vuelven a caer como trabajo perdido aunque la casilla ya las cuente."""
    import pandas as pd
    from programas.rem_utils import norm
    A = pd.Series([norm(a) for a in _F2_REALES])
    assert sm.mask_tributa_ada(A).all()


# ======================================================================
# Demografia del grupal por RUN + A27 con tramos y demografia
# (docs/demografia_grupal_plan.md)
# ======================================================================
_PG = "Intervencion psicosocial grupal."
_A27_TRAST = "Educación en grupo - Prevención de salud mental - Prevención trastorno mental"
_A27_SUIC = "Educación en grupo - Prevención de salud mental - Prevención del suicidio"


def _rut(n):
    from programas.rem_utils import dv_rut
    return f"{n}-{dv_rut(n)}"


def _rg(run, asiste="SI", edad=30, act=_PG, sexo="Mujer", dia=10):
    return {"run": run, "fecha": date(2026, 7, dia), "asiste": asiste, "edad": edad,
            "act": act, "sexo": sexo, "prest": "Dra A"}


def _run_g(grupal, inscritos=None, ada=None):
    """Corrida con grupal + (opcional) Inscritos + ADA de relleno. -> (E, tablas)."""
    ins = _mk_inscritos(inscritos) if inscritos is not None else None
    E = sm.procesar(_mk_ada(_RELLENO_ADA + (ada or [])), grupal=_mk_grupal(grupal),
                    inscritos=ins, mes=(2026, 7), log=_quiet, dotacion_tabla=_SIN_DOTACION)
    return E, E.attrs["tablas"]


def _pg(t):
    return _cell_row(t["A06_Controles"], "Profesional", "Intervención Psicosocial Grupal")


def _aviso(E, empieza):
    return next((a for a in E.attrs["avisos"] if a[0].startswith(empieza)), None)


def test_grupal_demografia_desde_el_inscritos():
    r = _rut(11111111)
    E, t = _run_g([_rg(r)], inscritos=[{"NUMERO TIPO IDENTIFICACION": r, "SEXO": "Mujer",
                                        "ALERTAS ADMINISTRATIVAS": "Programa SENAME - Ambulatorio",
                                        "PUEBLO INDIG": "Mapuche"}])
    assert _pg(t)["SENAME"] == 1 and _pg(t)["Pueblos Originarios"] == 1
    assert _pg(t)["Beneficiarios"] == 1
    assert list(E.loc[E["casilla"] == "A06PG", "dem_fuente"]) == ["inscritos"]


def test_grupal_demografia_cae_al_ada_y_sin_inscritos():
    r = _rut(11111112)
    ada = [{"run": r, "id": "P1", "fecha": date(2026, 6, 20), "act": "Curacion simple",
            "instr": "Enfermero(a)", "sexo": "Mujer", "edad": 30, "pueblo": "Mapuche"}]
    E, t = _run_g([_rg(r)], ada=ada)                  # sin Inscritos: solo la via ADA
    assert _pg(t)["Pueblos Originarios"] == 1
    assert list(E.loc[E["casilla"] == "A06PG", "dem_fuente"]) == ["ada"]
    assert _aviso(E, "A06 Psicosocial Grupal (demografia)") is not None


def test_grupal_demografia_sin_dato_se_avisa():
    r = _rut(11111113)
    E, t = _run_g([_rg(r)], inscritos=[{"NUMERO TIPO IDENTIFICACION": _rut(11111114), "SEXO": "Mujer"}])
    assert _pg(t)["SENAME"] == 0
    assert list(E.loc[E["casilla"] == "A06PG", "dem_fuente"]) == ["sin_dato"]
    av = _aviso(E, "A06 Psicosocial Grupal (demografia)")
    assert av[1] == "SUBCONTADO" and "1 sin dato" in av[2]


def test_grupal_trans_desde_el_inscritos():
    r = _rut(11111115)
    E, t = _run_g([_rg(r)], inscritos=[{"NUMERO TIPO IDENTIFICACION": r, "SEXO": "Mujer",
                                        "GENERO": "Transgénero Masculino"}])
    assert _pg(t)["TRANS Masculino"] == 1 and _pg(t)["TRANS Femenina"] == 0


def test_grupal_run_con_dv_en_minuscula_calza():
    r = _rut(10000013)
    assert r.endswith("K")
    E, t = _run_g([_rg(r.lower())], inscritos=[{"NUMERO TIPO IDENTIFICACION": r, "SEXO": "Mujer",
                                                "ALERTAS ADMINISTRATIVAS": "SENAME"}])
    assert _pg(t)["SENAME"] == 1


def test_grupal_inscritos_sin_ningun_cruce_es_revisar():
    E, t = _run_g([_rg(_rut(11111116))],
                  inscritos=[{"NUMERO TIPO IDENTIFICACION": _rut(11111117), "SEXO": "Mujer"}])
    av = _aviso(E, "Demografia del grupal (cruce con el Inscritos)")
    assert av is not None and av[1] == "REVISAR"


def test_grupal_nsp_no_suma_a_nada():
    a, b = _rut(11111118), _rut(11111119)
    ins = [{"NUMERO TIPO IDENTIFICACION": a, "SEXO": "Mujer", "ALERTAS ADMINISTRATIVAS": "SENAME"},
           {"NUMERO TIPO IDENTIFICACION": b, "SEXO": "Mujer"}]
    E, t = _run_g([_rg(a, asiste="NO"), _rg(b)], inscritos=ins)
    assert _pg(t)["Ambos"] == 1 and _pg(t)["SENAME"] == 0
    assert _pg(t)["Beneficiarios"] == 1


def test_a27_tramos_sin_sexo_y_total():
    rs = [_rut(20000000 + i) for i in range(3)]
    E, t = _run_g([_rg(rs[0], edad=12, act=_A27_TRAST), _rg(rs[1], edad=37, act=_A27_TRAST),
                   _rg(rs[2], edad=85, act=_A27_TRAST)])
    f = _cell_row(t["A27_Educacion_Prev"], "Área temática", "Prevención trastorno mental")
    assert f["10-14"] == 1 and f["35-39"] == 1 and f["80+"] == 1
    assert f["Total"] == 3 == sum(f[l] for l in sm.LBL_A27)
    assert f["Cuidador de <1 año"] == 0


def test_a27_menor_de_10_no_cuenta_y_se_avisa():
    E, t = _run_g([_rg(_rut(20000010), edad=7, act=_A27_SUIC), _rg(_rut(20000011), edad=20, act=_A27_SUIC)])
    f = _cell_row(t["A27_Educacion_Prev"], "Área temática", "Prevención suicidio")
    assert f["Total"] == 1 and sum(f[l] for l in sm.LBL_A27) == 1
    av = _aviso(E, "A27 menores de 10")
    assert av is not None and "1 asistente" in av[2]
    # ...pero la sesion existio: la seccion B no depende de la edad.
    ses = _cell_row(t["A27_B_Sesiones"], "Área temática", "Prevención suicidio")
    assert ses["B · Sesiones (actividades)"] == 1


def test_a27_gestante_y_demografia_por_la_cascada():
    g, s, p = _rut(20000020), _rut(20000021), _rut(20000022)
    ada = [{"run": g, "id": "G1", "fecha": date(2026, 7, 2), "act": "Control Prenatal  ;",
            "instr": "Matron(a)", "sexo": "Mujer", "edad": 25}]
    ins = [{"NUMERO TIPO IDENTIFICACION": s, "SEXO": "Mujer", "ALERTAS ADMINISTRATIVAS": "SENAME"},
           {"NUMERO TIPO IDENTIFICACION": p, "SEXO": "Mujer", "PUEBLO INDIG": "Aymara"}]
    E, t = _run_g([_rg(r, edad=25, act=_A27_TRAST) for r in (g, s, p)], inscritos=ins, ada=ada)
    f = _cell_row(t["A27_Educacion_Prev"], "Área temática", "Prevención trastorno mental")
    assert f["Gestantes APS"] == 1 and f["SENAME"] == 1 and f["Pueblos Originarios"] == 1
    assert f["Gestantes Nivel Secundario"] == 0 and f["Familias en Riesgo"] == 0


def test_a27_columnas_en_el_orden_de_la_plantilla():
    """D..AI de la hoja A27 del SA_26: si MINSAL mueve columnas (SA_27), esto falla."""
    from programas.rem_utils import norm
    ws = openpyxl.load_workbook(REPO / "refs_tablas" / "SA_26_V1.2.xlsm", read_only=True)["A27"]
    r9, r10 = (list(next(ws.iter_rows(min_row=n, max_row=n, min_col=4, max_col=35,
                                      values_only=True))) for n in (9, 10))
    plantilla = [norm(b or a).replace(" ", "") for a, b in zip(r9, r10)]
    # (token en MI columna, token en la plantilla), una por columna D..AI
    esperado = [("TOTAL", "TOTAL"), ("<1", "MENOSDE1"), ("12-23", "12-23"), ("2-5", "2-5"),
                ("6-9", "6-9"), ("10-14", "10-14")]
    esperado += [(l, "80YMAS" if l == "80+" else l) for l in sm.LBL_A27]
    esperado += [("APS", "APS"), ("SECUNDARIO", "SECUNDARIO"), ("TERCIARIO", "TERCIARIO"),
                 ("FAMILIAS", "FAMILIAS"), ("PUEBLOS", "PUEBLOS"), ("MIGRANTES", "MIGRANTES"),
                 ("ESPACIOS", "ESPACIOS"), ("MASCULINO", "MASCULINO"), ("FEMENINO", "FEMENINO"),
                 ("SENAME", "SENAME"), ("PROT", "PROTECCION")]
    _, t = _run_g([_rg(_rut(20000030), edad=30, act=_A27_TRAST)])
    cols = [norm(c).replace(" ", "") for c in t["A27_Educacion_Prev"].columns[1:]]
    assert len(cols) == len(esperado) == len(plantilla), (len(cols), len(esperado), len(plantilla))
    for i, (mio, tmpl) in enumerate(esperado):
        assert mio in cols[i] and tmpl in plantilla[i], (i, cols[i], plantilla[i])
