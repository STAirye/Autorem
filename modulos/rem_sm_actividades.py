#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.5.5
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

Fuentes (mensuales; el export puede venir del AÑO COMPLETO → se filtra el mes):
  - ADA  = 'Atenciones/Diagnósticos/Actividades' (IRIS). Todo salvo lo grupal.
           Se lee con rem_utils.cargar_atenciones. Conteo por ATEN ID (distinct).
  - Grupal = 'Atenciones Grupales'. Solo A06 psicosocial, A19a grupal y A27.
           Conteo por ASISTENCIA (cada fila Asiste=SI), SIN deduplicar.

Reglas: mes = FECHA ATENCIÓN (hacia atrás desde el último día del mes). SENAME se
excluye solo (es un string aparte: 'Control Salud Mental a Paciente SENAME' — ellos
hacen su propio REM). A05 y las Consultorías A06·A.2 quedan fuera (módulo/manual).
"""

import calendar
from datetime import date

import pandas as pd

from programas.rem_utils import (norm, cargar_atenciones, cargar_canonico,
                                 resolver_columnas, contiene_todos as _all,
                                 marcar_demografia, gestante_runs, trans_map)

# Flags demográficos por evento (fuente ADA IRIS; grupal no los trae -> False).
# Ver rem_utils.marcar_demografia. dem_gestante (RUN) y dem_trans_* (RUN, requiere
# el 'Informe Inscritos') se calculan en procesar().
DEM_COLS = ["dem_originario", "dem_migrante", "dem_sename", "dem_mejorninez",
            "dem_demencia", "dem_cuidador", "dem_campana", "dem_gestante",
            "dem_trans_m", "dem_trans_f"]

# Bloque de columnas demográficas por sección (label template -> flag).
#   '_total' = todos (Beneficiarios Fonasa) · '_zero' = no derivable (reservado).
#   TRANS sale del 'Informe Inscritos' (split M/F, opcional). 'Espacios Amigables' y
#   'Familias en Riesgo' se OMITEN (no se usan en el centro).
DEM_A04 = [("Pueblos Originarios", "dem_originario"), ("Migrantes", "dem_migrante"),
           ("SENAME", "dem_sename"), ("Prot. Especializada", "dem_mejorninez"),
           ("Campaña de Invierno", "dem_campana")]
DEM_A06 = [("Beneficiarios", "_total"), ("SENAME", "dem_sename"),
           ("Prot. Especializada", "dem_mejorninez"), ("Pueblos Originarios", "dem_originario"),
           ("Migrantes", "dem_migrante"), ("Demencia", "dem_demencia"),
           ("TRANS Masculino", "dem_trans_m"), ("TRANS Femenina", "dem_trans_f"),
           ("Cuidadores demencia", "dem_cuidador")]
DEM_A26 = [("Pueblos Originarios", "dem_originario"), ("Migrantes", "dem_migrante"),
           ("SENAME", "dem_sename"), ("Prot. Especializada", "dem_mejorninez")]
DEM_A32 = [("SENAME", "dem_sename"), ("Prot. Especializada", "dem_mejorninez"),
           ("Pueblos Originarios", "dem_originario"), ("Migrantes", "dem_migrante"),
           ("Demencia", "dem_demencia")]


# ── Bandas etarias (inclusive). El último tramo (80,200) = '80 y más'. ──
BANDAS_A04 = [(0, 0), (1, 4), (5, 9), (10, 14), (15, 19), (20, 24), (25, 29),
              (30, 34), (35, 39), (40, 44), (45, 49), (50, 54), (55, 59),
              (60, 64), (65, 69), (70, 74), (75, 79), (80, 200)]
LBL_A04 = ["<1", "1-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34",
           "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69",
           "70-74", "75-79", "80+"]
BANDAS_A06 = [(0, 4)] + BANDAS_A04[2:]     # A06/A32 agrupan 0-4 (A04 separa <1 y 1-4)
LBL_A06 = ["0-4"] + LBL_A04[2:]

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

_EV_COLS = ["casilla", "sub", "run", "id", "estamento", "edad", "sexo",
            "fecha", "actividad", "fuente"]


def cargar_grupal(entrada):
    """Export(s) de 'Atenciones Grupales' -> DataFrame canónico. Ruta o lista
    (el export puede venir por período). La fecha viene en TEXTO DD/MM/YYYY."""
    d, col = cargar_canonico(entrada, ["ACTIVIDADES", "FECHA ATENCION"],
                             lambda h: resolver_columnas(h, MAPA_GRUPAL))
    if not col.get("ASISTE"):
        raise ValueError("El reporte de Atenciones Grupales no trae la columna "
                         "'ASISTE (SI/NO)'. Descárgalo sin modificar desde RAYEN.")
    d["FECHA"] = pd.to_datetime(d["FECHA"], errors="coerce", dayfirst=True)
    d["ACT_n"] = d["ACT"].map(norm)
    d["ASISTE_n"] = d["ASISTE"].map(norm)
    return d


def _rango_mes(mes):
    """(inicio, fin) del mes de reporte. mes=(año,mes) o None -> mes anterior."""
    if mes is None:
        hoy = date.today()
        y, m = (hoy.year, hoy.month - 1) if hoy.month > 1 else (hoy.year - 1, 12)
    else:
        y, m = mes
    return pd.Timestamp(y, m, 1), pd.Timestamp(y, m, calendar.monthrange(y, m)[1])


def _mujer(s):
    n = norm(s); return ("FEMENIN" in n) or ("MUJER" in n)


def _hombre(s):
    n = norm(s); return ("MASCULIN" in n) or ("HOMBRE" in n)


def _band_idx(edad, bandas):
    if pd.isna(edad):
        return None
    e = int(edad)
    return next((i for i, (lo, hi) in enumerate(bandas) if lo <= e <= hi), None)


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


def _isum(s):
    """Suma robusta a Series vacías (evita el '' de object-Series vacía)."""
    return int(s.sum()) if len(s) else 0


def _grid(sub, bandas, lbls, con_sexo=True):
    """Fila de conteos en el ORDEN del template: Ambos·Hombres·Mujeres y luego
    cada banda × sexo (o solo total por banda si con_sexo=False)."""
    hom = sub["sexo"].map(_hombre)
    muj = sub["sexo"].map(_mujer)
    bi = sub["edad"].map(lambda x: _band_idx(x, bandas))
    if con_sexo:
        out = {"Ambos": len(sub), "Hombres": _isum(hom), "Mujeres": _isum(muj)}
        for i, l in enumerate(lbls):
            m = bi.eq(i)
            out[f"{l} H"] = _isum(m & hom)
            out[f"{l} M"] = _isum(m & muj)
    else:
        out = {"Total": len(sub)}
        for i, l in enumerate(lbls):
            out[l] = _isum(bi.eq(i))
    return out


def _empty_ev():
    return pd.DataFrame({c: pd.Series(dtype="object") for c in _EV_COLS + DEM_COLS})


def _ev(df, mask, casilla, sub, id_col, edad_col, est_col, fuente):
    s = df.loc[mask]
    if s.empty:
        return None
    ids = (s["RUN"].astype(str) + "|" + s["FECHA"].dt.strftime("%Y%m%d") + "|" + s.index.astype(str)
           if id_col is None else s[id_col].astype(str))
    base = {
        "casilla": casilla, "sub": sub, "run": s["RUN"].astype(str), "id": ids,
        "estamento": s[est_col].astype(str),
        "edad": pd.to_numeric(s[edad_col], errors="coerce"),
        "sexo": s["SEXO"].astype(str), "fecha": s["FECHA"],
        "actividad": s["ACT"].astype(str), "fuente": fuente}
    for c in DEM_COLS:   # flags demográficos (ADA los trae; grupal -> False)
        base[c] = s[c].values if c in s.columns else False
    return pd.DataFrame(base)


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


def _ada_eventos(dm):
    """Eventos del ADA (mes filtrado). Conteo por ATEN ID: dedup (casilla,sub,id)."""
    if dm.empty:
        return _empty_ev()
    A, I = dm["ACT_n"], dm["INSTR_n"]
    remotas = _all(A, "acciones remotas de salud mental")
    ctrl_rem = _all(A, "controles salud mental por")
    llam = _all(A, "llamada") & ~_all(A, "videollamada")
    specs = [
        ("A04", "", (I == "MEDICO") & _all(A, "consulta de salud mental")),
        ("A06", "", _all(A, "controles salud mental")),
        ("A19a", "97", _all(A, "prioridad - con integrante con problema de salud mental")),
        ("A19a", "99", _all(A, "prioridad - con integrante con demencia")),
        ("A26", "", _all(A, "visita domiciliaria integral familia con integrante con problema de salud mental")),
        ("A32F1", "Llamadas Telefónicas", remotas & llam),
        ("A32F1", "Videollamadas", remotas & _all(A, "videollamada")),
        ("A32F1", "Mensajería de Texto", remotas & _all(A, "mensaj")),
        ("A32F2", "Llamadas Telefónicas", ctrl_rem & llam),
        ("A32F2", "Videollamadas", ctrl_rem & _all(A, "videollamada")),
    ]
    partes = [_ev(dm, m, c, s, "ATENID", "ANOS_AT", "INSTR", "ADA") for c, s, m in specs]
    partes = [p for p in partes if p is not None]
    E = pd.concat(partes, ignore_index=True) if partes else _empty_ev()
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
    partes = [_ev(gm, m, c, s, None, "EDAD", "PREST", "Grupal") for c, s, m in specs]
    partes = [p for p in partes if p is not None]
    return pd.concat(partes, ignore_index=True) if partes else _empty_ev()


# ── Tablas de salida (una por sección REM; forma = template SA_26) ──

def _tabla_a04(E):
    sub = E[E["casilla"] == "A04"]
    return pd.DataFrame([{"Consulta": "Salud Mental",
                          **_grid(sub, BANDAS_A04, LBL_A04), **_demcols(sub, DEM_A04)}])


def _tabla_a06(E):
    filas = []
    for est in A06_ORDEN:
        s = E[(E["casilla"] == "A06") & (E["estamento_rem"] == est)]
        filas.append({"Profesional": est, **_grid(s, BANDAS_A06, LBL_A06), **_demcols(s, DEM_A06)})
    tot = E[E["casilla"] == "A06"]
    filas.append({"Profesional": "TOTAL", **_grid(tot, BANDAS_A06, LBL_A06), **_demcols(tot, DEM_A06)})
    pg = E[E["casilla"] == "A06PG"]
    filas.append({"Profesional": "Intervención Psicosocial Grupal",
                  **_grid(pg, BANDAS_A06, LBL_A06), **_demcols(pg, DEM_A06)})
    return pd.DataFrame(filas)


def _tabla_a19a(E):
    filas = []
    for cell, lbl in [("97", "Con integrante con problema de salud mental"),
                      ("99", "Con integrante con demencia")]:
        s = E[(E["casilla"] == "A19a") & (E["sub"] == cell)]
        filas.append({"Tema prioridad (familiar)": lbl, "Total Actividades": len(s),
                      "  · desde ADA (individual)": int((s["fuente"] == "ADA").sum()),
                      "  · desde Grupal": int((s["fuente"] == "Grupal").sum())})
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


def _tabla_a26(E):
    s = E[E["casilla"] == "A26"].copy()
    s["visita"] = s["actividad"].map(_visita)
    s["r59"] = s["edad"].between(5, 9)
    filas = []
    for lbl, msk in [("A.30 Familia con integrante con problema de salud mental", ~s["r59"]),
                     ("A.31 Familia con niños/as 5-9 años con problemas SM", s["r59"])]:
        ss = s[msk]
        filas.append({"Concepto": lbl, "Total": len(ss),
                      "Primera Visita": int((ss["visita"] == "Primera").sum()),
                      "Segunda Visita": int((ss["visita"] == "Segunda").sum()),
                      "Tercera o más": int((ss["visita"] == "Tercera o más").sum()),
                      **_demcols(ss, DEM_A26)})
    return pd.DataFrame(filas)


def _tabla_a27(E):
    filas = []
    for cell, lbl in [("suicidio", "Prevención suicidio"),
                      ("trastorno", "Prevención trastorno mental")]:
        s = E[(E["casilla"] == "A27") & (E["sub"] == cell)]
        ses = s.drop_duplicates(subset=["fecha", "estamento", "actividad"])
        filas.append({"Área temática": lbl, "A · Asistentes (usuarios)": len(s),
                      "B · Sesiones (actividades)": len(ses)})
    return pd.DataFrame(filas)


def _tabla_a32f1(E):
    filas = []
    for via in ["Llamadas Telefónicas", "Videollamadas", "Mensajería de Texto"]:
        s = E[(E["casilla"] == "A32F1") & (E["sub"] == via)]
        filas.append({"Vía": via, **_grid(s, BANDAS_A06, LBL_A06, con_sexo=False), **_demcols(s, DEM_A32)})
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


def _tabla_resumen(E, ini):
    def n(cas, sub=None):
        s = E[E["casilla"] == cas]
        if sub is not None:
            s = s[s["sub"] == sub]
        return len(s)
    filas = [
        ("A04 · A24", "Consultas médicas SM (médico)", n("A04")),
        ("A06 · A.1", "Controles Salud Mental (todos los estamentos)", n("A06")),
        ("A06 · A.1", "Intervención Psicosocial Grupal", n("A06PG")),
        ("A19a · 97", "Consejería familiar — problema SM (ADA+Grupal)", n("A19a", "97")),
        ("A19a · 99", "Consejería familiar — demencia (ADA+Grupal)", n("A19a", "99")),
        ("A26 · A.30/31", "VDI familia con problema SM", n("A26")),
        ("A27 · 34", "Educación grupal — prevención suicidio", n("A27", "suicidio")),
        ("A27 · 35", "Educación grupal — prevención trastorno mental", n("A27", "trastorno")),
        ("A32 · F1", "Acciones remotas SM (llamada+video+mensaje)", n("A32F1")),
        ("A32 · F2", "Controles SM remotos", n("A32F2")),
    ]
    df = pd.DataFrame(filas, columns=["Casilla", "Qué se registra", "Total mes"])
    df.attrs["mes"] = f"{ini:%Y-%m}"
    return df


def procesar(ada, grupal=None, inscritos=None, mes=None, log=print):
    """Devuelve el DataFrame de EVENTOS (detalle largo, auditable) con
    `.attrs['tablas']` = {nombre_hoja: DataFrame} listas para el template SA_26.
    `ada` = export de atenciones (ruta o lista). `grupal` = export de Atenciones
    Grupales (opcional; sin él, A06 grupal / A19a grupal / A27 salen 0). `inscritos`
    = 'Informe Inscritos y Adscritos' (opcional; sin él, TRANS sale 0)."""
    d = cargar_atenciones(ada)
    d = marcar_demografia(d)
    ini, fin = _rango_mes(mes)
    # Gestante (patrón PowerBI): ventana de 3 meses terminando en el mes reportado.
    ini3 = ini - pd.DateOffset(months=2)
    gset = gestante_runs(d, ini3, fin)
    d["dem_gestante"] = d["RUN"].isin(gset)
    # TRANS: requiere el padrón de Inscritos (GÉNERO con selección explícita).
    if inscritos is not None:
        try:
            tmap = trans_map(inscritos)
        except ValueError as e:                       # archivo modificado / reporte equivocado
            tmap = {}
            log(f"[sm] ⚠⚠ TRANS NO calculado: {e}  → TRANS queda en 0.")
        d["dem_trans_m"] = d["RUN"].map(lambda r: tmap.get(r) == "M")
        d["dem_trans_f"] = d["RUN"].map(lambda r: tmap.get(r) == "F")
        if not tmap:
            # 0 TRANS en el padrón COMPLETO es sospechoso -> avisar en vez de callar
            log("[sm] ⚠⚠ El 'Informe Inscritos' arrojó 0 personas TRANS. En el padrón "
                "COMPLETO del CESFAM eso casi seguro significa que el archivo está "
                "MODIFICADO/filtrado o es otro reporte → descárgalo de nuevo SIN tocar. "
                "(TRANS queda en 0.)")
        else:
            log(f"[sm] Inscritos: {len(tmap)} personas TRANS en el padrón del CESFAM")
    else:
        d["dem_trans_m"] = False
        d["dem_trans_f"] = False
    dm = d[(d["FECHA"] >= ini) & (d["FECHA"] <= fin)]
    span = (f"{d['FECHA'].min():%Y-%m-%d}..{d['FECHA'].max():%Y-%m-%d}"
            if d["FECHA"].notna().any() else "sin fechas")
    log(f"[sm] ADA: {len(d)} atenciones ({span}) | mes reporte {ini:%Y-%m} -> {len(dm)} atenciones")
    if d["FECHA"].notna().any() and d["FECHA"].min() > ini3:
        log(f"[sm] ⚠ GESTANTES usa ventana de 3 meses (desde {ini3:%Y-%m}), pero el ADA "
            f"arranca en {d['FECHA'].min():%Y-%m} → puede SUBCONTAR. Carga el ADA de los últimos 3 meses.")
    Ea = _ada_eventos(dm)

    if grupal is not None:
        g = cargar_grupal(grupal)
        gm = g[(g["FECHA"] >= ini) & (g["FECHA"] <= fin) & (g["ASISTE_n"] == "SI")]
        log(f"[sm] Grupal: {len(g)} filas | mes {ini:%Y-%m} + Asiste=SI -> {len(gm)} asistencias")
        Eg = _grupal_eventos(gm)
    else:
        log("[sm] sin reporte grupal -> A06 psicosocial / A19a grupal / A27 = 0")
        Eg = _empty_ev()

    E = pd.concat([Ea, Eg], ignore_index=True)
    E["estamento_rem"] = E["estamento"].map(_estamento_rem)

    E.attrs["tablas"] = {
        "SM_Resumen": _tabla_resumen(E, ini),
        "A04_Consultas_Medicas": _tabla_a04(E),
        "A06_Controles": _tabla_a06(E),
        "A19a_Consejerias_Fam": _tabla_a19a(E),
        "A26_VDI_SM": _tabla_a26(E),
        "A27_Educacion_Prev": _tabla_a27(E),
        "A32_F1_Acciones_Remotas": _tabla_a32f1(E),
        "A32_F2_Controles_Remotos": _tabla_a32f2(E),
    }
    E.attrs["mes"] = (ini.year, ini.month)
    log("[sm] resumen: " + " · ".join(
        f"{r['Casilla']}={r['Total mes']}" for _, r in E.attrs["tablas"]["SM_Resumen"].iterrows()))
    return E


def escribir(E, salida):
    """Escribe el detalle auditable (SM_Detalle) + una hoja por sección REM
    (tablas copy-paste al template SA_26) en un solo .xlsx."""
    tablas = E.attrs.get("tablas", {})
    with pd.ExcelWriter(salida) as xw:
        for nombre, df in tablas.items():
            df.to_excel(xw, index=False, sheet_name=nombre[:31])
        cols = _EV_COLS + [c for c in DEM_COLS if c in E.columns]
        det = E[cols].sort_values(["casilla", "sub", "fecha"])
        det.to_excel(xw, index=False, sheet_name="SM_Detalle")
    return str(salida)
