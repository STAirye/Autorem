#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 2.0.27
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. Distributed WITHOUT ANY WARRANTY. See the GNU
# General Public License for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
REM Salud Mental — ACTIVIDADES (estadística, sin juicio clínico).

Tabula las casillas de actividades de Salud Mental que hoy se llenan a mano con
tablas dinámicas: A04·A24, A06·A.1 (controles + psicosocial grupal), A19a·A.3
(consejerías familiares SM/demencia), A26 (VDI SM), A27 (educación prev. SM) y
A32·F (acciones/controles remotos SM). Salida = tablas listas para copiar-pegar
al template SA_26. Filtros VALIDADOS casilla por casilla contra el REM manual de
julio 2026 (ver docs / CLAUDE.md).

Fuentes (mensuales; el export puede venir del AÑO COMPLETO -> se filtra el mes):
  - ADA  = 'Atenciones/Diagnósticos/Actividades' (IRIS). Todo salvo lo grupal.
           Se lee con rem_utils.cargar_atenciones. Conteo por ATEN ID (distinct).
  - Grupal = 'Atenciones Grupales'. Solo A06 psicosocial, A19a grupal y A27.
           Conteo por ASISTENCIA (cada fila Asiste=SI), SIN deduplicar.

Reglas: mes = FECHA ATENCIÓN (hacia atrás desde el último día del mes). SENAME se
excluye solo (es un string aparte: 'Control Salud Mental a Paciente SENAME' — ellos
hacen su propio REM). A05 queda fuera (otro módulo). Las Consultorías A06·A.2 entran
desde 2.0.20, con el N° de consultorías INFERIDO de las fechas (aviso REVISAR).

Separación interno/externo (docs/dotacion_externos_plan.md): el ADA trae atenciones
de funcionarios que NO son de la dotación (p.ej. la sala AIDIA), que no deben
tributar a este REM. `programas/dotacion.py` clasifica por funcionario (tri-estado
interno/externo/desconocido, vía `~/.autorem/dotacion.json`); acá se reduce a nivel
de EVENTO (`clasificar_evento`, caso mixto) y las tablas de sección se calculan
sobre `E[en_rem]` — el detalle `SM_Detalle` conserva TODAS las filas (marcar, no
borrar) y la hoja `Externos_Delta` muestra el desglose Total/Externos/REM.
"""

import pandas as pd

from programas.rem_utils import (norm, edad_anios, cargar_atenciones, cargar_canonico,
                                 resolver_columnas, contiene_todos as _all,
                                 contiene_alguno as _any,
                                 marcar_demografia, gestante_runs, trans_de, clave_run,
                                 demografia_por_run,
                                 atenid_multiprofesional, _rango_mes, filtrar_mes, opcional,
                                 grid as _grid, _mujer, _hombre, _band_idx, _isum,
                                 BANDAS_A04, LBL_A04, BANDAS_A06, LBL_A06, BANDAS_A27, LBL_A27,
                                 fecha_col,
                                 ArchivoInvalido, aviso_fuera_de_grid, por_actividad,
                                 meses_del_rango, etiqueta_periodo)
from programas.poblacion import cargar_inscritos
from programas import formatos          # clasificación de fuente plena/parcial (fase 2)
from programas import dotacion          # separación interno/externo (docs/dotacion_externos_plan.md)
from programas import cobertura         # categorías de aviso (PENDIENTE/OMITIDO) para la hoja LEEME

# Flags demográficos por evento (fuente ADA IRIS; el grupal los toma por RUN de la
# cascada Inscritos -> ADA, `rem_utils.demografia_por_run`). Ver marcar_demografia.
# dem_gestante (RUN) y dem_trans_* (RUN, requiere el 'Informe Inscritos') se calculan
# en _cargar / _eventos_mes.
DEM_COLS = ["dem_originario", "dem_migrante", "dem_sename", "dem_mejorninez",
            "dem_demencia", "dem_cuidador", "dem_campana", "dem_gestante",
            "dem_trans_m", "dem_trans_f"]

# Bloque de columnas demográficas por sección (label template -> flag).
#   '_total' = todos (Beneficiarios Fonasa) · '_zero' = no derivable (reservado).
#   TRANS sale del 'Informe Inscritos' (split M/F, opcional). 'Espacios Amigables' y
#   'Familias en Riesgo' se OMITEN (no se usan en el centro).
DEM_A04 = [("Pueblos Originarios", "dem_originario"), ("Migrantes", "dem_migrante"),
           ("SENAME", "dem_sename"), ("Prot. Especializada", "dem_mejorninez")]
# (Campaña de Invierno: write-protected en la hoja de Salud Mental -> se omite.)
DEM_A06 = [("Beneficiarios", "_total"), ("SENAME", "dem_sename"),
           ("Prot. Especializada", "dem_mejorninez"), ("Pueblos Originarios", "dem_originario"),
           ("Migrantes", "dem_migrante"), ("Demencia", "dem_demencia"),
           ("TRANS Masculino", "dem_trans_m"), ("TRANS Femenina", "dem_trans_f"),
           ("Cuidadores demencia", "dem_cuidador")]
DEM_A26 = [("Pueblos Originarios", "dem_originario"), ("Migrantes", "dem_migrante"),
           ("SENAME", "dem_sename"), ("Prot. Especializada", "dem_mejorninez")]
# A06·A.2 (cols. AP-AS). Las de demencia (AT sospecha / AU diagnostico) NO: la columna
# DIAGNOSTICO de RAYEN no distingue CONFIRMADO de SOSPECHA -> MANUAL (cobertura.py).
DEM_A06A2 = [("Pueblos Originarios", "dem_originario"), ("Migrantes", "dem_migrante"),
             ("SENAME", "dem_sename"), ("Prot. Especializada", "dem_mejorninez")]
DEM_A32 = [("SENAME", "dem_sename"), ("Prot. Especializada", "dem_mejorninez"),
           ("Pueblos Originarios", "dem_originario"), ("Migrantes", "dem_migrante"),
           ("Demencia", "dem_demencia")]
# A27 (cols. Y..AI del SA_26, en el ORDEN de la plantilla). Las `_zero` no se derivan
# (docs/demografia_grupal_plan.md §2): gestantes de nivel secundario/terciario, Familias
# en Riesgo y Espacios Amigables (estos dos OMITIDOS, igual que en el resto del SM).
DEM_A27 = [("Gestantes APS", "dem_gestante"), ("Gestantes Nivel Secundario", "_zero"),
           ("Gestantes Nivel Terciario", "_zero"), ("Familias en Riesgo", "_zero"),
           ("Pueblos Originarios", "dem_originario"), ("Migrantes", "dem_migrante"),
           ("Espacios Amigables", "_zero"), ("TRANS Masculino", "dem_trans_m"),
           ("TRANS Femenino", "dem_trans_f"), ("SENAME", "dem_sename"),
           ("Prot. Especializada", "dem_mejorninez")]
# A27 E..I «Madre, Padre o Cuidador de»: el grupal no dice en que calidad asistio -> 0.
A27_CUIDADOR = ["Cuidador de <1 año", "Cuidador de 12-23 meses", "Cuidador de 2-5 años",
                "Cuidador de 6-9 años", "Cuidador de 10-14 años"]


# Bandas etarias + grilla edad×sexo (`_grid`) viven en rem_utils (compartidas SM/A23/A03).

# Orden de filas de estamento en A06·A.1 (template SA_26).
A06_ORDEN = ["Médico/a", "Psicólogo/a", "Enfermera/o", "Matrona/ón",
             "Trabajador/a Social", "Otros Profesionales Capacitados (Salud Mental)",
             "Terapeuta Ocupacional", "Técnico en Enfermería en Salud Mental",
             "Gestor Comunitario", "Técnico Rehabilitación Alcohol y Drogas"]

# Mapa de columnas del reporte 'Atenciones Grupales'.
MAPA_GRUPAL = {
    "RUN":       [("subs", ["NUMERO", "IDENTIFICACION"])],
    "FECHA":     ("exact", "FECHA ATENCION"),
    "ACT":       ("exact", "ACTIVIDADES"),
    "ASISTE":    ("subs", ["ASISTE"]),
    "SEXO":      ("exact", "SEXO"),
    "EDAD":      ("exact", "EDAD"),
    "INSTR":     ("exact", "INSTRUMENTO"),
    "PREST":     [("subs", ["FUNCIONARIO", "PRESTADOR"]), ("subs", ["NOMBRE", "PROFESIONAL"])],
    "MULTIPROF": ("subs", ["MULTIPROFESIONAL"]),
}

_EV_COLS = ["casilla", "sub", "run", "id", "estamento", "funcionario", "edad", "sexo",
            "fecha", "actividad", "fuente", "externo", "tabula_en", "mes", "dem_fuente"]


def cargar_grupal(entrada, log=print):
    """Export(s) de 'Atenciones Grupales' -> DataFrame canónico. Ruta o lista
    (el export puede venir por período). La fecha viene en TEXTO DD/MM/YYYY."""
    d, col = cargar_canonico(entrada, lambda h: resolver_columnas(h, MAPA_GRUPAL),
                             requeridas=("ACT", "FECHA", "ASISTE"), espera="grupal", log=log)
    d["FECHA"] = fecha_col(d["FECHA"], log, "FECHA atención (grupal)")
    d["ACT_n"] = d["ACT"].map(norm)
    d["ASISTE_n"] = d["ASISTE"].map(norm)
    # EDAD del grupal viene en TEXTO ('55 años 3 meses 1 día') -> años (nº). Sin esto,
    # la desagregación por banda etaria queda en 0 (pd.to_numeric del texto = NaN).
    d["EDAD"] = d["EDAD"].map(edad_anios)
    return d


def _estamento_rem(instr):
    """INSTRUMENTO del reporte -> fila de estamento del template A06."""
    n = norm(instr)
    if n == "MEDICO" or n.startswith("MEDICO "):
        return "Médico/a"
    if "PSICOLOG" in n:
        return "Psicólogo/a"
    if "ENFERMER" in n and "TECNICO" not in n:
        return "Enfermera/o"
    if "MATRON" in n:
        return "Matrona/ón"
    if "TRABAJADOR" in n and "SOCIAL" in n:
        return "Trabajador/a Social"
    if "TERAPEUTA OCUPACIONAL" in n:
        return "Terapeuta Ocupacional"
    if "GESTOR" in n:
        return "Gestor Comunitario"
    return "Otros Profesionales Capacitados (Salud Mental)"


def _empty_ev():
    return pd.DataFrame({c: pd.Series(dtype="object") for c in _EV_COLS + DEM_COLS})


def _ev(df, mask, casilla, sub, id_col, edad_col, est_col, fuente, prof_col):
    s = df.loc[mask]
    if s.empty:
        return None
    ids = (s["RUN"].astype(str) + "|" + s["FECHA"].dt.strftime("%Y%m%d") + "|" + s.index.astype(str)
           if id_col is None else s[id_col].astype(str))
    base = {
        "casilla": casilla, "sub": sub, "run": s["RUN"].astype(str), "id": ids,
        "estamento": s[est_col].astype(str),
        "funcionario": s[prof_col].fillna("").astype(str) if prof_col in s.columns else "",
        "edad": pd.to_numeric(s[edad_col].map(edad_anios), errors="coerce"),  # ANOS_AT num o texto verboso
        "sexo": s["SEXO"].astype(str), "fecha": s["FECHA"],
        "actividad": s["ACT"].astype(str), "fuente": fuente}
    for c in DEM_COLS:   # flags demográficos (ADA los trae; el grupal por la cascada)
        base[c] = s[c].values if c in s.columns else False
    base["dem_fuente"] = s["dem_fuente"].values if "dem_fuente" in s.columns else ""
    return pd.DataFrame(base)


def _concat_funcionario(E):
    """El dedup por (casilla,sub,id) puede colapsar varias filas de UNA misma
    atención (p.ej. 2 diagnósticos de la misma visita) que traigan distinto
    `funcionario` (visita con más de un profesional). Antes de deduplicar, junta
    los nombres ÚNICOS de cada grupo en el ORDEN en que aparecen (no alfabético,
    para que calce con el orden en que se listan las atenciones)."""
    if E.empty:
        return E
    def _join(s):
        return " · ".join(dict.fromkeys(v for v in s if v))
    E["funcionario"] = E.groupby(["casilla", "sub", "id"])["funcionario"].transform(_join)
    return E


def _nombres_funcionario(campo):
    """'NOMBRE A · NOMBRE B' -> ['NOMBRE A', 'NOMBRE B'] (ver `_concat_funcionario`).
    Ignora nombres vacíos."""
    return [n for n in str(campo or "").split(" · ") if n]


def clasificar_evento(funcionario, tabla):
    """Clase dotación (`dotacion.INTERNO`/`EXTERNO`/`DESCONOCIDO`) de UN EVENTO,
    cuyo campo `funcionario` puede traer VARIOS nombres unidos con ' · ' (visita
    con más de un profesional). Regla (docs/dotacion_externos_plan.md §4.2):
    interno si hay al menos uno interno (hubo gente nuestra, es producción
    nuestra); si no, externo si hay al menos uno externo; si no, desconocido."""
    clases = {dotacion.clase(n, tabla) for n in _nombres_funcionario(funcionario)}
    if dotacion.INTERNO in clases:
        return dotacion.INTERNO
    if dotacion.EXTERNO in clases:
        return dotacion.EXTERNO
    return dotacion.DESCONOCIDO


def _demcols(sub, spec):
    """Conteos demográficos en el orden del template. `_total`=todos, `_zero`=0."""
    out = {}
    for label, flag in spec:
        if flag == "_total":
            out[label] = len(sub)
        elif flag == "_zero":
            out[label] = 0
        else:
            out[label] = int(sub[flag].sum()) if (flag in sub.columns and len(sub)) else 0
    return out


# Substrings de ACTIVIDADES (normalizados) que SÍ tributan a algún REM SM desde el
# ADA. Fuente única: la usan _ada_eventos (indirecto) y el detector de trabajo
# perdido (rem_sm_trabajo_perdido): lo que trae 'mental'/'demencia' y NO cae acá es
# candidato a saco roto. 'controles salud mental' cubre también los remotos A32F2
# ('… por llamada/videollamada'). SENAME se trata aparte (tributa a su propio REM).
ADA_TRIBUTAN = [
    "consulta de salud mental",                                            # A04
    "controles salud mental",                                              # A06 + A32F2
    "prioridad - con integrante con problema de salud mental",             # A19a·97
    "prioridad - con integrante con demencia",                             # A19a·99
    "visita domiciliaria integral familia con integrante con problema de salud mental",  # A26
    "acciones remotas de salud mental",                                    # A32F1
    # A32F2. Van APARTE de "controles salud mental" (A06): el nombre real lleva un
    # "de" en medio ("Controles DE Salud Mental por llamadas telefonicas"), asi que
    # el patron del A06 NO los captura. Sin estas dos entradas caian como TRABAJO
    # PERDIDO (fue asi como se descubrio el bug de `ctrl_rem`, mas abajo).
    "salud mental por llamadas",                                           # A32F2
    "salud mental por videollamada",                                       # A32F2
    # A06·A.2 (2.0.20). «consultorias de salud mental» cubre tambien las TELEconsultorias.
    "consultorias de salud mental",                                        # A06A2
    "casos revisados consultoria salud mental",                            # A06A2
    "casos revisados teleconsultoria salud mental",                        # A06A2
]


def mask_tributa_ada(A):
    """A = Serie ACT_n (ya normalizada). True si la actividad tributa a algún REM SM.

    Por `contiene_alguno` (2.0.11) y no un OR a mano: es la MISMA reducción, y es el
    idioma que ya usan poblacion.py, el rescate y el A23 (regla 4). Escrita acá aparte,
    una corrección en el helper compartido (el `na=`, o la Serie vacía) no alcanzaba a
    la máscara que decide qué tributa a SM -- la que alimentan el Trabajo Perdido y el
    diálogo de dotación de la GUI."""
    return _any(A, ADA_TRIBUTAN)


# -- Máscaras del A32, POR ACTIVIDAD -------------------------------------------
# Sus tokens parten el nombre de UNA actividad («Controles DE Salud Mental POR llamadas
# telefónicas»), así que van dentro de `por_actividad`: sobre la celda canónica, que trae
# todas las actividades de la atención, el AND se satisface con un token de cada una.
# Ver el comentario en `_ada_eventos` y el docstring de rem_utils.por_actividad.
def _remotas(s):        # A32F1
    return _all(s, "acciones remotas de salud mental")


def _llamada(s):        # «por llamada telefónica», nunca la videollamada
    return _all(s, "llamada") & ~_all(s, "videollamada")


def _ctrl_remoto(s):
    """A32F2. OJO con el «de»: las actividades reales de RAYEN son «Controles DE Salud
    Mental por llamadas telefónicas» y «... por videollamadas». El patrón viejo era la
    subcadena CONTIGUA «controles salud mental por», que no matchea ninguna de las 4 del
    Maestro -> A32-F2 daba 0 SIEMPRE, y el 0 se leía como «ese mes no hubo». Son dos
    subcadenas en AND, que capturan las 4 y nada más."""
    return _all(s, "controles", "salud mental por")


def _a2(A, tele, patron):
    """A06·A.2, POR ACTIVIDAD: «consultorias de salud mental adulto» es subcadena de la
    TELEconsultoria, asi que presencial = el patron SIN «teleconsultoria» en la misma
    actividad. Infanto/Adulto sale del NOMBRE de la actividad, nunca de la edad: 15-19
    puede ir en cualquiera de las dos (decision del autor, 2.0.20)."""
    return por_actividad(A, lambda s: _all(s, patron) & (_all(s, "teleconsultoria") if tele
                                                         else ~_all(s, "teleconsultoria")))


def _ada_eventos(dm):
    """Eventos del ADA (mes filtrado). Conteo por ATEN ID: dedup (casilla,sub,id)."""
    if dm.empty:
        return _empty_ev()
    A, I = dm["ACT_n"], dm["INSTR_n"]
    # A06·A.2: sub = «<presencial|tele>|<Adulto|Infanto|Caso>». La consultoria es UNA
    # reunion, pero la ficha se registra por PACIENTE (una actividad por caso revisado).
    a2 = [("A06A2", f"{mod}|{g}", _a2(A, mod == "tele", pat))
          for mod in ("presencial", "tele")
          for g, pat in (("Adulto", "consultorias de salud mental adulto"),
                         ("Infanto", "consultorias de salud mental infanto"),
                         ("Caso", "casos revisados teleconsultoria salud mental" if mod == "tele"
                          else "casos revisados consultoria salud mental"))]
    # Las cinco del A32 van `por_actividad` (ver arriba): sus tokens parten el nombre de
    # UNA actividad, y sobre la celda canónica el AND los tomaba de actividades DISTINTAS.
    # Las dos direcciones, medidas (2.0.0):
    #   falso POSITIVO: «Controles de pie diabético; Consulta de salud mental por
    #     psicólogo; Consulta de morbilidad por llamada telefónica» -> A32F2 = True, sin
    #     que exista ningún control remoto de SM.
    #   falso NEGATIVO: «Controles de Salud Mental por llamadas telefónicas; Acciones
    #     remotas de salud mental por videollamada» -> A32F2-Llamadas = False, porque el
    #     ~videollamada de `_llamada` lee la palabra en la actividad HERMANA.
    specs = [
        ("A04", "", (I == "MEDICO") & _all(A, "consulta de salud mental")),
        ("A06", "", _all(A, "controles salud mental")),
        ("A19a", "97", _all(A, "prioridad - con integrante con problema de salud mental")),
        ("A19a", "99", _all(A, "prioridad - con integrante con demencia")),
        ("A26", "", _all(A, "visita domiciliaria integral familia con integrante con problema de salud mental")),
        ("A32F1", "Llamadas Telefónicas", por_actividad(A, lambda s: _remotas(s) & _llamada(s))),
        ("A32F1", "Videollamadas", por_actividad(A, lambda s: _remotas(s) & _all(s, "videollamada"))),
        ("A32F1", "Mensajería de Texto", por_actividad(A, lambda s: _remotas(s) & _all(s, "mensaj"))),
        ("A32F2", "Llamadas Telefónicas", por_actividad(A, lambda s: _ctrl_remoto(s) & _llamada(s))),
        ("A32F2", "Videollamadas", por_actividad(A, lambda s: _ctrl_remoto(s) & _all(s, "videollamada"))),
    ] + a2
    partes = [_ev(dm, m, c, s, "ATENID", "ANOS_AT", "INSTR", "ADA", "PROF") for c, s, m in specs]
    partes = [p for p in partes if p is not None]
    E = pd.concat(partes, ignore_index=True) if partes else _empty_ev()
    E = _concat_funcionario(E)
    return E.drop_duplicates(subset=["casilla", "sub", "id"])


def _grupal_eventos(gm):
    """Eventos del grupal (mes + Asiste=SI). Conteo por ASISTENCIA (sin dedup)."""
    if gm.empty:
        return _empty_ev()
    A = gm["ACT_n"]
    specs = [
        ("A06PG", "", _all(A, "intervencion psicosocial grupal")),
        ("A19a", "97", _all(A, "consejerias familiares") & _all(A, "problema de salud mental")),
        ("A19a", "99", _all(A, "consejerias familiares") & _all(A, "demencia")),
        ("A27", "suicidio", _all(A, "prevencion") & _all(A, "suicid")),
        ("A27", "trastorno", _all(A, "prevencion trastorno mental")),
    ]
    partes = [_ev(gm, m, c, s, None, "EDAD", "PREST", "Grupal", "PREST") for c, s, m in specs]
    partes = [p for p in partes if p is not None]
    return pd.concat(partes, ignore_index=True) if partes else _empty_ev()


# -- Tablas de salida (una por sección REM; forma = template SA_26) --

def _tabla_a04(E):
    sub = E[E["casilla"] == "A04"]
    return pd.DataFrame([{"Consulta": "Salud Mental",
                          **_grid(sub, BANDAS_A04, LBL_A04), **_demcols(sub, DEM_A04)}])


def _tabla_a06(E):
    filas = []
    for est in A06_ORDEN:
        s = E[(E["casilla"] == "A06") & (E["estamento_rem"] == est)]
        filas.append({"Profesional": est, **_grid(s, BANDAS_A06, LBL_A06), **_demcols(s, DEM_A06)})
    # (TOTAL: write-protected en el template — se calcula solo -> se omite.)
    pg = E[E["casilla"] == "A06PG"]
    filas.append({"Profesional": "Intervención Psicosocial Grupal",
                  **_grid(pg, BANDAS_A06, LBL_A06), **_demcols(pg, DEM_A06)})
    return pd.DataFrame(filas)


def _casos_a2(s):
    """CASOS REVISADOS de A06·A.2: un caso = (RUN, dia, modalidad) distinto. Si a un
    paciente se le registro la «Consultoria ... adulto» Y el «Casos revisados ...»,
    es UN caso, no dos."""
    if s.empty:
        return s
    return s.assign(_dia=_dia(s), _mod=s["sub"].astype(str).str.split("|").str[0]
                    ).drop_duplicates(["run", "_dia", "_mod"])


def _dia(s):
    """Fecha sin hora. `pd.to_datetime` porque un E vacio trae `fecha` como object."""
    return pd.to_datetime(s["fecha"]).dt.normalize()


def _consultorias_a2(s, grupo):
    """N° de consultorias de un grupo (Adulto/Infanto) = FECHAS DISTINTAS de registro.
    INFERIDO, nunca afirmado (decision del autor): la reunion es una sola pero la ficha
    se escribe por paciente, a veces otro dia -> tiende a SOBREestimar. Por eso
    `_tablas` deja SIEMPRE un aviso REVISAR cuando hay alguna."""
    return int(_dia(s[s["sub"].astype(str).str.endswith("|" + grupo)]).nunique())


def _tabla_a06a2(E):
    """A06·A.2 (consultorias RECIBIDAS en APS), forma del SA_26: fila 30 presencial,
    fila 31 tele. C/D = N° de consultorias (INFERIDO, ver `_consultorias_a2`); E..AO =
    casos revisados por banda x sexo; AP..AS = demografia. AT/AU (demencia) = MANUAL."""
    filas = []
    for mod, etiqueta in (("presencial", "Consultorías de Salud Mental"),
                          ("tele", "Teleconsultorías de Salud Mental")):
        s = E[(E["casilla"] == "A06A2") & E["sub"].astype(str).str.startswith(mod + "|")]
        casos = _casos_a2(s)
        filas.append({"Actividad": etiqueta,
                      "N° consultorías Infanto Adolescente (INFERIDO)": _consultorias_a2(s, "Infanto"),
                      "N° consultorías Adulto (INFERIDO)": _consultorias_a2(s, "Adulto"),
                      **_grid(casos, BANDAS_A06, LBL_A06), **_demcols(casos, DEM_A06A2)})
    return pd.DataFrame(filas)


def _tabla_a19a(E):
    filas = []
    especs = [("97", "Con integrante con problema de salud mental"),
              ("99", "Con integrante con demencia")]
    for i, (cell, lbl) in enumerate(especs):
        s = E[(E["casilla"] == "A19a") & (E["sub"] == cell)]
        filas.append({"Tema prioridad (familiar)": lbl, "Total Actividades": len(s),
                      "  · desde ADA (individual)": int((s["fuente"] == "ADA").sum()),
                      "  · desde Grupal": int((s["fuente"] == "Grupal").sum())})
        if i == 0:    # fila EN BLANCO entre 97 y 99 (en el template hay otra fila al medio)
            filas.append({"Tema prioridad (familiar)": ""})
    return pd.DataFrame(filas)


def _visita(a):
    n = norm(a)
    if "PRIMERA" in n:
        return "Primera"
    if "SEGUNDA" in n:
        return "Segunda"
    if "TERCERA" in n or "MAS VISITAS" in n:
        return "Tercera o más"
    return "s/i"


def _tabla_a26(E, multi=None):
    """`multi` = set de ATEN ID multiprofesionales (del reporte 'Monitoreo
    Multiprofesional'). Sin él, todo se asume mono-profesional (Un Profesional)."""
    multi = multi or set()
    s = E[E["casilla"] == "A26"].copy()
    s["visita"] = s["actividad"].map(_visita)
    s["r59"] = s["edad"].between(5, 9)
    s["es_multi"] = s["id"].isin(multi)
    filas = []
    for lbl, msk in [("A.30 Familia con integrante con problema de salud mental", ~s["r59"]),
                     ("A.31 Familia con niños/as 5-9 años con problemas SM", s["r59"])]:
        ss = s[msk]
        n, n_dos = len(ss), int(ss["es_multi"].sum())
        # Composición: 'Dos o Más' si la atención está en el Monitoreo Multiprofesional;
        # el resto 'Un Profesional'. Sin ese reporte, n_dos=0 -> todo mono (default).
        filas.append({"Concepto": lbl, "Total": n,
                      "Un Profesional": n - n_dos, "Dos o Más Prof.": n_dos,
                      "Un Prof + Técnico": 0, "Técnico": 0, "Facilitador": 0, "Agente Comunitario": 0,
                      "Primera Visita": int((ss["visita"] == "Primera").sum()),
                      "Segunda Visita": int((ss["visita"] == "Segunda").sum()),
                      "Tercera o Más": int((ss["visita"] == "Tercera o más").sum()),
                      **_demcols(ss, DEM_A26)})
    return pd.DataFrame(filas)


_A27_AREAS = [("suicidio", "Prevención suicidio"), ("trastorno", "Prevención trastorno mental")]


def _a27_menores(s):
    """Máscara: asistentes de A27 menores de 10 años (no hay tramo: el mínimo es 10-14)."""
    return pd.to_numeric(s["edad"], errors="coerce") < 10


def _tabla_a27(E):
    """A27·A (filas 34/35), forma del SA_26: D Total, E..I cuidador (0), J..X rango etario
    SIN sexo, Y..AI gestantes y demografía (`DEM_A27`). Los menores de 10 años no entran
    (`_tablas` deja el aviso con su conteo). La sección B va en `_tabla_a27_sesiones`."""
    filas = []
    for cell, lbl in _A27_AREAS:
        s = E[(E["casilla"] == "A27") & (E["sub"] == cell)]
        s = s[~_a27_menores(s)]
        g = _grid(s, BANDAS_A27, LBL_A27, con_sexo=False)
        filas.append({"Área temática": lbl, "Total": g.pop("Total"),
                      **{c: 0 for c in A27_CUIDADOR}, **g, **_demcols(s, DEM_A27)})
    return pd.DataFrame(filas)


def _tabla_a27_sesiones(E):
    """A27·B: sesiones = (fecha, prestador, actividad) distintas, sobre las asistencias YA
    filtradas por Asiste=SI (un taller donde todos fueron NSP no cuenta como sesión) y
    sin los menores de 10 (un taller solo de menores tampoco cuenta)."""
    filas = []
    for cell, lbl in _A27_AREAS:
        s = E[(E["casilla"] == "A27") & (E["sub"] == cell)]
        s = s[~_a27_menores(s)]
        filas.append({"Área temática": lbl, "B · Sesiones (actividades)":
                      len(s.drop_duplicates(subset=["fecha", "estamento", "actividad"]))})
    return pd.DataFrame(filas)


def _tabla_a32f1(E):
    filas = []
    for via in ["Llamadas Telefónicas", "Videollamadas", "Mensajería de Texto"]:
        s = E[(E["casilla"] == "A32F1") & (E["sub"] == via)]
        g = _grid(s, BANDAS_A06, LBL_A06, con_sexo=False)   # Total + bandas etarias (sin sexo)
        g["Hombres"] = _isum(s["sexo"].map(_hombre))         # el template agrupa por sexo al final
        g["Mujeres"] = _isum(s["sexo"].map(_mujer))
        filas.append({"Vía": via, **g, **_demcols(s, DEM_A32)})
    return pd.DataFrame(filas)


def _tabla_a32f2(E):
    filas = []
    for via in ["Llamadas Telefónicas", "Videollamadas"]:
        base = E[(E["casilla"] == "A32F2") & (E["sub"] == via)]
        for est in A06_ORDEN:
            s = base[base["estamento_rem"] == est]
            filas.append({"Control remoto por": via, "Profesional": est,
                          **_grid(s, BANDAS_A06, LBL_A06), **_demcols(s, DEM_A32)})
    return pd.DataFrame(filas)


def _tabla_resumen(E, etiqueta):
    def n(cas, sub=None):
        s = E[E["casilla"] == cas]
        if sub is not None:
            s = s[s["sub"] == sub]
        return len(s)
    filas = [
        ("A04 · A24", "Consultas médicas SM (médico)", n("A04")),
        ("A06 · A.1", "Controles Salud Mental (todos los estamentos)", n("A06")),
        ("A06 · A.1", "Intervención Psicosocial Grupal", n("A06PG")),
        ("A06 · A.2", "Casos revisados en consultorías SM (presencial + tele)",
         len(_casos_a2(E[E["casilla"] == "A06A2"]))),
        ("A19a · 97", "Consejería familiar — problema SM (ADA+Grupal)", n("A19a", "97")),
        ("A19a · 99", "Consejería familiar — demencia (ADA+Grupal)", n("A19a", "99")),
        ("A26 · A.30/31", "VDI familia con problema SM", n("A26")),
        ("A27 · 34", "Educación grupal — prevención suicidio", n("A27", "suicidio")),
        ("A27 · 35", "Educación grupal — prevención trastorno mental", n("A27", "trastorno")),
        ("A32 · F1", "Acciones remotas SM (llamada+video+mensaje)", n("A32F1")),
        ("A32 · F2", "Controles SM remotos", n("A32F2")),
    ]
    df = pd.DataFrame(filas, columns=["Casilla", "Qué se registra", "Total mes"])
    df.attrs["mes"] = etiqueta
    return df


def _tabla_externos_delta(E, etiqueta):
    """1 fila por casilla: Total (todo E) · Externos · REM (E[en_rem]). Reusa
    `_tabla_resumen` sobre los dos subconjuntos (docs/dotacion_externos_plan.md
    §4.4, fase 1) — ambas llamadas emiten SIEMPRE las mismas filas/orden, así
    que se alinean por posición sin necesidad de merge."""
    total = _tabla_resumen(E, etiqueta)
    rem = _tabla_resumen(E[E["en_rem"]], etiqueta)
    out = total[["Casilla", "Total mes"]].rename(columns={"Total mes": "Total"})
    out["REM"] = rem["Total mes"].values
    out["Externos"] = out["Total"] - out["REM"]
    return out[["Casilla", "Total", "Externos", "REM"]]


def _tabla_por_mes(E, resumen):
    """Hoja `Por_Mes` (docs/rango_meses_plan.md §4.2.5): filas = las de SM_Resumen
    (mismo orden, fijo), una columna por mes + `Total`. `Total` tiene que calzar con
    la columna de SM_Resumen (lo amarra el test): SM cuenta por ATENCIÓN, y una
    atención cae en un solo mes, así que los conteos SUMAN (§3 del plan). `E` ya
    trae las columnas `mes` y `en_rem` (las pone `_eventos_mes` / `_tablas`)."""
    meses = sorted(E["mes"].unique())
    df = resumen[["Casilla", "Qué se registra"]].copy()
    for m in meses:
        sub = E[(E["mes"] == m) & E["en_rem"]]
        df[m] = _tabla_resumen(sub, m)["Total mes"].values
    df["Total"] = resumen["Total mes"].values
    return df


def _cargar(ada, grupal=None, inscritos=None, multiprofesional=None, log=print, d=None,
           dotacion_tabla=None):
    """CARGA compartida por todos los meses de una corrida (docs/rango_meses_plan.md
    §4.2.1): ADA + demografía por atención + TRANS (Inscritos) + grupal + tabla de
    dotación — nada de esto depende del mes. Devuelve un dict que `_eventos_mes` y
    `_tablas` consumen. Los OPCIONALES van PRIMERO (ronda 12): si uno no sirve, la GUI
    pregunta «¿seguir sin él?» ANTES del trabajo pesado (el ADA y el grupal)."""
    from pathlib import Path
    tmap = insc = None
    if inscritos is not None:
        # Invalido -> OpcionalInvalido: la GUI pregunta si seguir sin el (ronda 11; antes
        # quedaba en una linea del log y TRANS en 0, sin llegar a la LEEME). Se lee UNA
        # vez (~55k filas): de este DataFrame salen el `tmap` TRANS del ADA y la
        # demografia del grupal (docs/demografia_grupal_plan.md §3.5).
        with opcional("inscritos"):
            insc = cargar_inscritos(inscritos, log=log)
            if "GENERO" in insc.attrs["columnas_ausentes"]:   # TRANS no se puede sin el
                raise ArchivoInvalido(
                    "sin_columnas",
                    "No reconozco el 'Informe Inscritos y Adscritos': no encuentro la columna "
                    "GENERO.\n\n¿Está modificado o es otro reporte? Cárgalo tal como sale de "
                    "RAYEN/IRIS, sin editar.")
            tmap = {r: t for r, s, g in zip(insc["RUN"], insc["SEXO"], insc["GENERO"])
                    if (t := trans_de(s, g))}
    multi = set()
    if multiprofesional is not None:
        with opcional("multiprofesional"):   # invalido: la GUI pregunta si seguir sin el
            multi = atenid_multiprofesional(multiprofesional)

    tabla_dot = dotacion.cargar(log=log) if dotacion_tabla is None else dotacion_tabla
    d = cargar_atenciones(ada, log=log) if d is None else d
    d = marcar_demografia(d)
    avisos = []   # degradaciones de ESTA corrida -> hoja LEEME (programas/cobertura.py)
    # Fuente PARCIAL (fase 2). Desde v1.9.3 el Monitoreo YA NO rompe el conteo: se
    # le encontró equivalente al ATEN ID ('N°') y a la edad-a-la-atención ('AÑOS').
    # Lo que sigue sin tener equivalente es la DEMOGRAFÍA — y no por descuido: son
    # datos que ese reporte simplemente no trae. Ver formatos.SOLO_IRIS_ATENCIONES.
    _av = formatos.aviso_fuente(
        *d.attrs.get("fuente", (formatos.FUENTE_PLENA, [])),
        "Los CONTEOS de A04/A06/A19a/A26/A32 son validos, pero TODA la demografia "
        "sale en 0 (pueblos originarios, migrante, SENAME, Mejor Ninez, cuidador, "
        "demencia, gestante): esas columnas no existen en la fuente. Copiar los "
        "totales, NO las columnas demograficas (AN-AV del SA_26).",
        casilla="ADA (fuente de las casillas SM)", archivos=d.attrs.get("fuente_mezcla"))
    if _av:
        avisos.append(_av)
    fuentes = [Path(p).name for p in (ada if isinstance(ada, (list, tuple)) else [ada])]
    if grupal is not None:
        fuentes += [Path(p).name for p in (grupal if isinstance(grupal, (list, tuple)) else [grupal])]

    # TRANS: requiere el padrón de Inscritos (GÉNERO con selección explícita). NO
    # depende del mes -> se marca UNA vez sobre `d` completo (a diferencia de
    # dem_gestante, que SÍ depende del mes y se calcula por mes en `_eventos_mes`,
    # sin pisar `d`).
    if tmap is not None:
        gen = d["RUN"].map(tmap)                       # M/F/X por RUN (NaN si no TRANS)
        d["dem_trans_m"] = gen.eq("M")
        d["dem_trans_f"] = gen.eq("F")
        if not tmap:
            # 0 TRANS en el padrón COMPLETO es sospechoso -> avisar en vez de callar
            log("[sm] El 'Informe Inscritos' arrojó 0 personas TRANS. En el padrón "
                "COMPLETO del CESFAM eso casi seguro significa que el archivo está "
                "MODIFICADO/filtrado o es otro reporte -> descárgalo de nuevo SIN tocar. "
                "(TRANS queda en 0.)")
            avisos.append(("Columnas TRANS (A06/A32)", "EN 0",
                            "el 'Informe Inscritos' dio 0 personas TRANS (sospechoso: "
                            "revisar si el archivo esta modificado/filtrado)",
                            "Descargar el 'Informe Inscritos y Adscritos' de nuevo, sin tocar"))
        else:
            log(f"[sm] Inscritos: {len(tmap)} personas TRANS en el padrón del CESFAM")
    else:
        d["dem_trans_m"] = False
        d["dem_trans_f"] = False
        avisos.append(("Columnas TRANS (A06/A32)", "EN 0",
                        "no se cargo el 'Informe Inscritos y Adscritos' (opcional)",
                        "Cargar el 'Informe Inscritos y Adscritos' si se necesita el flag TRANS"))

    span = (f"{d['FECHA'].min():%Y-%m-%d}..{d['FECHA'].max():%Y-%m-%d}"
            if d["FECHA"].notna().any() else "sin fechas")

    g = None
    if grupal is not None:
        g = cargar_grupal(grupal, log=log)
        # Demografia del grupal por RUN (Inscritos -> ultima atencion del ADA -> sin dato).
        # No depende del mes: UNA vez, sobre `g` completo; los conteos se filtran despues.
        dem = demografia_por_run(g["RUN"], insc, d)
        for c in dem.columns:
            g[c] = dem[c].values
        por_run = dem["dem_fuente"][~g["RUN"].map(clave_run).duplicated()].value_counts()
        log("[sm] Grupal, demografia por RUN: " + ", ".join(f"{n} {f}" for f, n in por_run.items()))
        if insc is not None:
            ausentes = [c for c in ("ALERTAS", "PUEBLO") if c in insc.attrs["columnas_ausentes"]]
            if ausentes:
                avisos.append(("A06 Psicosocial Grupal / A27 (demografia)", "SUBCONTADO",
                               f"el 'Informe Inscritos' no trae la(s) columna(s) {', '.join(ausentes)}: "
                               "esas columnas demograficas salen en 0 aunque el RUN calce",
                               "Descargar el 'Informe Inscritos y Adscritos' completo, sin tocar"))
    else:
        log("[sm] sin reporte grupal -> A06 psicosocial / A19a grupal / A27 = 0")
        avisos.append(("A06 psicosocial / A19a grupal / A27", "EN 0",
                        "no se cargo el reporte 'Atenciones Grupales'",
                        "Cargar 'Atenciones Grupales'"))

    if not tabla_dot.get("funcionarios"):
        log("[dotacion] AVISO: la tabla de dotacion esta VACIA (nunca se clasifico a nadie, o "
            "se cancelo el dialogo) -> NINGUNA atencion se separo; el total INCLUYE posibles "
            "externos sin revisar.")
        avisos.append(("Separacion interno/externo (dotacion)", cobertura.PENDIENTE,
                        "la tabla de dotacion esta vacia: nunca se clasifico a nadie (o se "
                        "cancelo el dialogo) -> ninguna atencion se separo del REM",
                        "Abrir 'Revisar dotacion...' y clasificar al equipo"))

    return {"d": d, "g": g, "insc": insc, "span": span, "multi": multi, "tabla_dot": tabla_dot,
            "multiprofesional_cargado": multiprofesional is not None,
            "fuentes": fuentes, "avisos": avisos}


def _eventos_mes(carga, mes, log=print):
    """Eventos del ADA + grupal para UN mes: TODAS las reglas ancladas al mes
    (GESTANTE con su ventana de 3 meses, `filtrar_mes`, Asiste=SI del grupal) corren
    EXACTAMENTE igual que en un `procesar()` de un solo mes (docs/rango_meses_plan.md
    §2). `carga` = el dict de `_cargar`, compartido entre TODOS los meses de la corrida:
    nunca se pisa `carga['d']` con la marca de gestante de este mes -- se calcula sobre
    una COPIA (`dm`), o el mes 2 heredaría la marca del mes 1. Devuelve (E_mes, avisos_mes)."""
    d, g = carga["d"], carga["g"]
    avisos = []
    ini, fin = _rango_mes(mes)
    # Gestante (patrón PowerBI): ventana de 3 meses terminando en el mes reportado.
    ini3 = ini - pd.DateOffset(months=2)
    gset = gestante_runs(d, ini3, fin)
    log(f"[sm] ADA: {len(d)} atenciones ({carga['span']}) | mes reporte {ini:%Y-%m}")
    # Fail loud (§3): el ADA sin NINGUNA atención del mes es archivo/mes equivocado,
    # no un mes de cero actividad. Va sobre la FUENTE; que una casilla dé 0 es legítimo.
    dm = filtrar_mes(d, ini, fin, "el ADA (Atenciones Diarias Ambulatorias)").copy()
    dm["dem_gestante"] = dm["RUN"].isin(gset)
    log(f"[sm] atenciones en el mes: {len(dm)}")
    if d["FECHA"].notna().any() and d["FECHA"].min() > ini3:
        log(f"[sm] GESTANTES usa ventana de 3 meses (desde {ini3:%Y-%m}), pero el ADA "
            f"arranca en {d['FECHA'].min():%Y-%m} -> puede SUBCONTAR. Carga el ADA de los últimos 3 meses.")
        avisos.append(("Gestantes (demografia)", "SUBCONTADO",
                        f"el ADA arranca en {d['FECHA'].min():%Y-%m}, la ventana de "
                        f"GESTANTE necesita 3 meses (desde {ini3:%Y-%m})",
                        "Cargar el ADA de los ultimos 3 meses"))
    Ea = _ada_eventos(dm)

    if g is not None:
        # El mes se guarda (archivo de otro período = error); Asiste=SI se aplica
        # DESPUÉS y sí puede dejar 0 (mes con talleres pero nadie asistió: legítimo).
        gm = filtrar_mes(g, ini, fin, "el reporte 'Atenciones Grupales'")
        # "Nadie asistio" es legitimo SOLO si la columna lo DICE (NO). Una ASISTE en
        # blanco o con otro valor ("S", "Asistio"...) no es un NO: sin esto, el filtro de
        # abajo la tomaba como tal y A27 / A06 grupal / A19a grupal salian en 0 callados.
        reconocido = gm["ASISTE_n"].isin(("SI", "NO"))
        if not reconocido.any():
            vistos = sorted(set(gm["ASISTE_n"]))[:5]
            raise ArchivoInvalido(
                "sin_datos",
                f"En el reporte 'Atenciones Grupales' ninguna de las {len(gm)} fila(s) de "
                f"{ini:%m/%Y} dice SI o NO en la columna ASISTE (valores: "
                f"{', '.join(repr(v) for v in vistos)}).\n\n"
                "Sin eso no se puede saber quién asistió: A27, A06 grupal y A19a grupal "
                "saldrían en 0. Revisa que sea el export correcto, SIN modificar.")
        n_raro = int((~reconocido).sum())
        if n_raro:
            log(f"[sm] Grupal: {n_raro} fila(s) del mes sin SI/NO en ASISTE -> NO se "
                "cuentan (pueden SUBCONTAR A27 / A06 grupal / A19a grupal).")
            avisos.append(("A06 psicosocial / A19a grupal / A27", "SUBCONTADO",
                           f"{n_raro} fila(s) del reporte grupal del mes no dicen SI ni NO "
                           "en ASISTE: no se cuentan",
                           "Revisar esas filas en RAYEN (asistencia sin registrar)"))
        gm = gm[gm["ASISTE_n"] == "SI"]
        # Gestante del grupal (solo la usa A27): misma ventana de 3 meses que el ADA.
        gkeys = {clave_run(r) for r in gset}
        gm = gm.assign(dem_gestante=gm["RUN"].map(clave_run).isin(gkeys))
        log(f"[sm] Grupal: {len(g)} filas | mes {ini:%Y-%m} + Asiste=SI -> {len(gm)} asistencias")
        Eg = _grupal_eventos(gm)
    else:
        Eg = _empty_ev()

    E = pd.concat([Ea, Eg], ignore_index=True)
    if len(E) == 0:
        # Fail loud (§3): el mes esta cubierto (filtrar_mes paso), pero NINGUNA fila
        # tributa a NINGUNA casilla SM. Una casilla en 0 es legitima; TODAS en 0 es el
        # gemelo por programa del `mes_vacio`: un ADA bajado filtrado por otro
        # programa, o un export cuyas actividades ya no calzan con ADA_TRIBUTAN.
        raise ArchivoInvalido(
            "sin_datos",
            f"El ADA trae {len(dm)} atención(es) de {ini:%m/%Y}, pero NINGUNA tributa a "
            "una casilla de Salud Mental (A04, A06, A19a, A26, A27, A32)"
            + (", y el reporte grupal tampoco aporta asistencias" if g is not None else "")
            + ".\n\nTodo el REM SM saldría en 0. Revisa que el ADA sea el export COMPLETO "
            "del centro (no filtrado por otro programa) y que esté SIN modificar.")
    E["estamento_rem"] = E["estamento"].map(_estamento_rem)
    E["mes"] = f"{ini:%Y-%m}"   # arma `Por_Mes` y queda en SM_Detalle para auditar
    return E, avisos


def _avisos_grupal(Erem, tiene_insc, log=print):
    """Avisos LEEME de la demografia del grupal (docs/demografia_grupal_plan.md §4.3-4.5):
    el conteo por fuente de la cascada (por casilla), la guarda de «0 cruces» y los
    menores de 10 años que el A27 no cuenta. Todo sobre los eventos YA filtrados
    (Asiste=SI), nunca sobre las filas NSP."""
    avisos = []
    G = Erem[Erem["fuente"] == "Grupal"]
    if G.empty:
        return avisos
    n = G["dem_fuente"].value_counts()
    if tiene_insc and not n.get("inscritos", 0):
        avisos.append(("Demografia del grupal (cruce con el Inscritos)", "REVISAR",
                       f"el 'Informe Inscritos' esta cargado pero NINGUNA de las {len(G)} "
                       "asistencias grupales calza con el por RUN: RUN en otro formato o archivo "
                       "equivocado. No es que nadie sea SENAME/migrante/etc.",
                       "Revisar que el Inscritos sea el del mismo centro y sin modificar"))
    elif not tiene_insc and not n.get("ada", 0):
        avisos.append(("Demografia del grupal (cruce con el ADA)", "REVISAR",
                       f"ninguno de los RUN de las {len(G)} asistencias grupales aparece en el ADA "
                       "ni se cargo el Inscritos: la demografia sale toda en 0",
                       "Cargar el 'Informe Inscritos y Adscritos', o revisar el RUN del grupal"))
    origen = "" if tiene_insc else " (no se cargo el Informe Inscritos: solo la via ADA)"
    for cas, nombre, nota in (
            ("A06PG", "A06 Psicosocial Grupal", "Demencia queda en 0 (no se deriva de otra atencion)"),
            ("A27", "A27 Educacion prev.", "Gestantes APS por el ADA (ventana de 3 meses); "
                                          "TRANS solo desde el Inscritos")):
        s = G[G["casilla"] == cas]
        if s.empty:
            continue
        ni, na, ns = (int((s["dem_fuente"] == f).sum()) for f in ("inscritos", "ada", "sin_dato"))
        avisos.append((f"{nombre} (demografia)", "SUBCONTADO" if ns else "REVISAR",
                       f"{len(s)} asistencias: {ni} desde el Inscritos, {na} desde la ultima "
                       f"atencion del ADA, {ns} sin dato (cuentan como NO). Es la foto al dia de "
                       f"la descarga, no la del taller. {nota}{origen}",
                       "Cargar el 'Informe Inscritos y Adscritos' para completar"))
    men = int(_a27_menores(G[G["casilla"] == "A27"]).sum())
    if men:
        log(f"[sm] A27: {men} asistente(s) menores de 10 años no se cuentan.")
        avisos.append(("A27 menores de 10 años", "REVISAR",
                       f"{men} asistente(s) menores de 10 años no se cuentan en el A27 (no hay "
                       "tramo etario; el minimo es 10-14): el total baja en ese numero",
                       "Si hace falta, registrarlos a mano en el REM"))
    return avisos


def _tablas(E, carga, avisos, etiqueta, log=print, modulo="sm"):
    """Marca dotación (interno/externo) sobre el E CONCATENADO (todos los meses de la
    corrida) y arma las tablas de salida + los avisos que dependen del PERÍODO completo
    (composición profesional A26, dotación, fuera-de-grid). `avisos` se muta con lo
    nuevo. `etiqueta` = período para `attrs['mes']` de cada tabla (`_tabla_resumen`)."""
    tabla_dot, multi = carga["tabla_dot"], carga["multi"]

    # Separación interno/externo (docs/dotacion_externos_plan.md): marcar, no
    # borrar (§1.4) — el detalle conserva TODAS las filas; solo las tablas de
    # sección se calculan sobre E[en_rem] más abajo. `desconocido` cuenta al REM
    # (§1.3): el default nunca sangra producción propia en silencio.
    E["externo"] = E["funcionario"].map(lambda f: clasificar_evento(f, tabla_dot))
    E["en_rem"] = dotacion.en_rem(E["externo"])
    E["tabula_en"] = E["en_rem"].map({True: "AMBAS", False: "SOLO_TOTAL"})

    # Composición profesional de A26 (opcional): Monitoreo Multiprofesional.
    # OJO: el reporte NO se filtra por mes; se cruza por ATEN ID con las VDI del
    # período. Debe CUBRIR el período reportado (bajarlo del año completo sirve). Si no
    # coincide con ninguna VDI, probablemente es de otro período -> aviso RUIDOSO.
    if carga["multiprofesional_cargado"]:
        log(f"[sm] Multiprofesional: {len(multi)} atenciones con 2+ profesionales en el padrón")
        a26_ids = set(E.loc[E["casilla"] == "A26", "id"])
        if a26_ids and not (a26_ids & multi):
            log("[sm] el Monitoreo Multiprofesional NO coincide con NINGUNA de las "
                f"{len(a26_ids)} VDI de A26 del período -> parece de OTRO período. A26 saldría "
                "TODO 'Un Profesional' (subcuenta). Revisa que el reporte cubra el período.")
            avisos.append(("A26 (composicion profesional)", "SUBCONTADO",
                            "el 'Monitoreo Multiprofesional' no coincide con ninguna VDI "
                            "del período (parece de otro periodo)",
                            "Revisar que el reporte cubra el período reportado"))
    else:
        avisos.append(("A26 (composicion profesional)", "SIN DESGLOSAR",
                        "no se cargo 'Monitoreo Multiprofesional' (opcional)",
                        "Cargar el reporte, o dejar todo como 'Un Profesional'"))

    # Avisos de dotación -> hoja LEEME (docs/dotacion_externos_plan.md §4.5).
    ext_rows = E[E["externo"] == dotacion.EXTERNO]
    desc_rows = E[E["externo"] == dotacion.DESCONOCIDO]
    if len(ext_rows):
        nombres_ext = {n for f in ext_rows["funcionario"] for n in _nombres_funcionario(f)
                       if dotacion.clase(n, tabla_dot) == dotacion.EXTERNO}
        log(f"[dotacion] {len(ext_rows)} atencion(es) de {len(nombres_ext)} funcionario(s) "
            "EXTERNO(s) separadas del REM (ver hoja Externos_Delta y columna 'externo' en SM_Detalle).")
        # Este aviso es el MAS importante de los tres: los otros dos hablan de lo que
        # falta hacer, este de lo que la herramienta YA HIZO -- sacar atenciones de las
        # tablas a proposito. Para eso existe la hoja LEEME (decir que NO esta en los
        # numeros); si el unico rastro fuera el log de la corrida, el mes que alguien
        # cuadre estas tablas contra RAYEN veria una diferencia sin explicacion.
        avisos.append((
            "Atenciones EXCLUIDAS a proposito (funcionarios externos)", cobertura.OMITIDO,
            f"{len(ext_rows)} atencion(es) de {len(nombres_ext)} funcionario(s) marcados "
            "EXTERNOS (no son de la dotacion de este centro: las reporta su propio "
            "dispositivo, contarlas aca seria doble conteo). NO estan en las tablas de "
            "seccion; SI estan en SM_Detalle (columna 'externo') y en Externos_Delta",
            "Si algun nombre no corresponde, corregirlo en 'Revisar dotacion...' y "
            "volver a procesar"))
    if len(desc_rows):
        nombres_desc = sorted({n for f in desc_rows["funcionario"] for n in _nombres_funcionario(f)
                               if dotacion.clase(n, tabla_dot) == dotacion.DESCONOCIDO})
        muestra = ", ".join(nombres_desc[:10]) + (", ..." if len(nombres_desc) > 10 else "")
        log(f"[dotacion] {len(desc_rows)} atencion(es) de {len(nombres_desc)} funcionario(s) SIN "
            f"clasificar (cuentan al REM por defecto, §1.3): {muestra}")
        avisos.append(("Funcionarios sin clasificar (dotacion)", cobertura.PENDIENTE,
                        f"{len(desc_rows)} atenciones de {len(nombres_desc)} funcionario(s) sin "
                        f"clasificar interno/externo: {muestra}",
                        "Clasificarlos en 'Revisar dotacion...' de la pagina"))
    ests_omit = dotacion.omitidos(tabla_dot, modulo)
    if ests_omit:
        om_norm = set(ests_omit)
        om_rows = E[E["estamento"].map(norm).isin(om_norm)]
        if len(om_rows):
            log(f"[dotacion] Estamentos omitidos para '{modulo}': {', '.join(ests_omit)} -> "
                f"{len(om_rows)} atencion(es) cuentan al REM sin revision individual.")
            avisos.append((f"Estamentos omitidos ({modulo})", cobertura.OMITIDO,
                            f"{', '.join(ests_omit)} - {len(om_rows)} atenciones cuentan al REM "
                            "sin revision individual (funcionarios quedan 'desconocido')",
                            "Revisar 'Revisar dotacion...' si se quiere clasificar a mano"))

    Erem = E[E["en_rem"]]
    # A06·A.2: el N° de consultorias (C/D) es INFERIDO de las fechas -> REVISAR SIEMPRE
    # que haya alguna (decision del autor: nunca un numero asumido, callado).
    a2 = Erem[Erem["casilla"] == "A06A2"]
    if len(a2):
        sub = a2["sub"].astype(str)
        n_c = sum(_consultorias_a2(a2[sub.str.startswith(m + "|")], g)
                  for m in ("presencial", "tele") for g in ("Infanto", "Adulto"))
        solo_caso = len(set(_casos_a2(a2)["_dia"]) - set(_dia(a2[~sub.str.endswith("|Caso")])))
        log(f"[sm] A06-A.2: {len(_casos_a2(a2))} caso(s) revisado(s), {n_c} consultoria(s) "
            "INFERIDAS de las fechas de registro (revisar antes de copiar C/D)")
        avisos.append((
            "A06-A.2 N° de consultorias (columnas C/D)", "REVISAR",
            f"{n_c} consultoria(s) INFERIDAS de las fechas distintas de registro, no "
            "registradas como tales: la consultoria es una reunion pero la ficha se escribe "
            "por paciente, y una escrita otro dia suma una consultoria que no existio "
            "(tiende a SOBREESTIMAR). Dos el mismo dia cuentan como una"
            + (f". {solo_caso} dia(s) con solo 'Casos revisados' (sin adulto/infanto) no "
               "entran a C/D" if solo_caso else ""),
            "Confirmar contra el registro de las consultorias antes de copiar C/D; los "
            "casos revisados (E en adelante) si son un conteo directo"))
    # BANDAS_A04 y BANDAS_A06 cubren el mismo rango (0-200): una sola pasada basta.
    _av = aviso_fuera_de_grid(Erem, BANDAS_A04, "Columnas por sexo / edad (todas las secciones)",
                              log=log)
    if _av:
        avisos.append(_av)
    avisos.extend(_avisos_grupal(Erem, carga["insc"] is not None, log))
    return {
        "SM_Resumen": _tabla_resumen(Erem, etiqueta),
        "Externos_Delta": _tabla_externos_delta(E, etiqueta),
        "A04_Consultas_Medicas": _tabla_a04(Erem),
        "A06_Controles": _tabla_a06(Erem),
        "A06_A2_Consultorias": _tabla_a06a2(Erem),
        "A19a_Consejerias_Fam": _tabla_a19a(Erem),
        "A26_VDI_SM": _tabla_a26(Erem, multi),
        "A27_Educacion_Prev": _tabla_a27(Erem),
        "A27_B_Sesiones": _tabla_a27_sesiones(Erem),
        "A32_F1_Acciones_Remotas": _tabla_a32f1(Erem),
        "A32_F2_Controles_Remotos": _tabla_a32f2(Erem),
    }


def procesar(ada, grupal=None, inscritos=None, multiprofesional=None, mes=None, log=print, d=None,
            dotacion_tabla=None, modulo="sm"):
    """Devuelve el DataFrame de EVENTOS (detalle largo, auditable) con
    `.attrs['tablas']` = {nombre_hoja: DataFrame} listas para el template SA_26.
    `ada` = export de atenciones (ruta o lista). `grupal` = export de Atenciones
    Grupales (opcional; sin él, A06 grupal / A19a grupal / A27 salen 0). `inscritos`
    = 'Informe Inscritos y Adscritos' (opcional; sin él, TRANS sale 0).
    `multiprofesional` = 'Monitoreo Multiprofesional' (opcional; sin él, las VDI de
    A26 se asumen mono-profesional). `d` = ADA ya cargado (para leer el archivo UNA
    sola vez cuando el mismo ADA lo comparten varios reportes; si es None, se carga).
    `dotacion_tabla` = tabla interno/externo YA resuelta (dict de `dotacion.cargar()`,
    normalmente actualizada por el diálogo de la GUI ANTES de llamar acá); si es
    None, se carga del caché (`~/.autorem/dotacion.json`) tal cual está — este
    módulo NO abre ningún diálogo (eso es responsabilidad de la GUI, que corre en
    el hilo de Tk, no en este worker). Ver docs/dotacion_externos_plan.md.

    Caso particular de UN solo mes de `procesar_rango` (docs/rango_meses_plan.md):
    `_cargar` + `_eventos_mes` + `_tablas`, sin la hoja `Por_Mes`."""
    ini, _fin = _rango_mes(mes)
    carga = _cargar(ada, grupal=grupal, inscritos=inscritos, multiprofesional=multiprofesional,
                    log=log, d=d, dotacion_tabla=dotacion_tabla)
    E, avisos_mes = _eventos_mes(carga, (ini.year, ini.month), log)
    avisos = list(carga["avisos"]) + avisos_mes
    tablas = _tablas(E, carga, avisos, f"{ini:%Y-%m}", log=log, modulo=modulo)
    E.attrs["avisos"] = avisos
    E.attrs["fuentes"] = carga["fuentes"]
    E.attrs["tablas"] = tablas
    E.attrs["mes"] = (ini.year, ini.month)
    log("[sm] resumen: " + " · ".join(
        f"{r['Casilla']}={r['Total mes']}" for _, r in tablas["SM_Resumen"].iterrows()))
    return E


def procesar_rango(ada, grupal=None, inscritos=None, multiprofesional=None, meses=None, log=print,
                   d=None, dotacion_tabla=None, modulo="sm"):
    """Como `procesar`, pero para un RANGO de meses (docs/rango_meses_plan.md).
    `meses` = lista de `(año, mes)` INCLUSIVE (`rem_utils.meses_del_rango`). Corre el
    motor MENSUAL (`_eventos_mes`) una vez por mes y agrega UNA vez al final -- nunca
    filtra el ADA por el rango entero (rompe GESTANTE, ver el plan §3). Con un solo mes,
    el resultado es IDÉNTICO al de `procesar(mes=meses[0])`: mismo archivo, mismos
    números, sin la hoja `Por_Mes`. Si un mes del rango falla (`ArchivoInvalido`), se
    re-levanta nombrándolo («en 03/2026: <mensaje original>») y no sigue con los demás."""
    carga = _cargar(ada, grupal=grupal, inscritos=inscritos, multiprofesional=multiprofesional,
                    log=log, d=d, dotacion_tabla=dotacion_tabla)
    partes, avisos = [], list(carga["avisos"])
    for mes in meses:
        try:
            E_mes, avisos_mes = _eventos_mes(carga, mes, log)
        except ArchivoInvalido as e:
            y, m = mes
            raise ArchivoInvalido(e.categoria, f"En {m:02d}/{y}: {e}") from e
        partes.append(E_mes)
        avisos.extend(avisos_mes)
    E = pd.concat(partes, ignore_index=True)
    etiqueta = etiqueta_periodo(meses)
    tablas = _tablas(E, carga, avisos, etiqueta, log=log, modulo=modulo)
    if len(meses) > 1:
        tablas["Por_Mes"] = _tabla_por_mes(E, tablas["SM_Resumen"])
    E.attrs["avisos"] = avisos
    E.attrs["fuentes"] = carga["fuentes"]
    E.attrs["tablas"] = tablas
    E.attrs["mes"] = etiqueta if len(meses) > 1 else meses[0]
    log("[sm] resumen: " + " · ".join(
        f"{r['Casilla']}={r['Total mes']}" for _, r in tablas["SM_Resumen"].iterrows()))
    return E


def escribir(E, salida):
    """Escribe el detalle auditable (SM_Detalle) + una hoja por sección REM
    (tablas copy-paste al template SA_26) en un solo .xlsx."""
    from programas import cobertura
    tablas = E.attrs.get("tablas", {})
    contexto = {"mes": E.attrs.get("mes"), "archivos": E.attrs.get("fuentes")}
    with pd.ExcelWriter(salida) as xw:
        cobertura.escribir_hoja(xw.book, "sm_actividades", contexto,
                                avisos=E.attrs.get("avisos", ()))
        for nombre, df in tablas.items():
            df.to_excel(xw, index=False, sheet_name=nombre[:31])
        cols = _EV_COLS + [c for c in DEM_COLS if c in E.columns]
        det = E[cols].sort_values(["casilla", "sub", "fecha"])
        det.to_excel(xw, index=False, sheet_name="SM_Detalle")
    return str(salida)
