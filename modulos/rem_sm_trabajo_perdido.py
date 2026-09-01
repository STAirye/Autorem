#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.7.9
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. Distributed WITHOUT ANY WARRANTY. See the GNU
# General Public License for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
REM Salud Mental — TRABAJO PERDIDO ("saco vacío").

Reporte de auditoría (no tributa a ninguna casilla del REM). Detecta atenciones del
ADA cuya ACTIVIDAD parece de Salud Mental (contiene 'mental' o 'demencia', heurístico
—RAYEN agrega actividades nuevas seguido, no hay lista fija—) pero que NO tributan a
las casillas SM que el exe reporta (A04·A06·19A·A26·A27·A32). Objetivo: disminuir el
trabajo a "saco vacío" mostrando QUÉ actividades mal elegidas se registran y QUÉ
FUNCIONARIOS (nombre y apellido, columna 'PROFESIONAL ATENCION') las registran, para
corregirlos.

CLASIFICACIÓN (autoridad = Maestro de Actividades; ver rem_utils.cargar_maestro):
  - Actividad SM-ish EN el Maestro → tributa sii su NUM REM ∈ {A04,A06,19A,A26,A27,A32}.
    Si su NUM REM es otro (REM-Gestion, A03 screening, A28, B17…) → PERDIDA (se muestra
    el NUM REM para que el referente vea por qué y refine).
  - Actividad SM-ish que NO está en el Maestro (RAYEN la agregó después) → heurística
    de respaldo: tributa sii matchea los patrones de rem_sm_actividades.mask_tributa_ada.
  - Sin Maestro cargado → todo por heurística (menos preciso).

Recicla el módulo de actividades (mismo ADA): `cargar_atenciones`, `_rango_mes` y la
heurística `mask_tributa_ada`. No es un fork: reporte aparte que comparte código.

Salida `escribir()`: TP_Resumen + Por_Actividad (qué strings son basura, con su NUM
REM) + Por_Funcionario (a quién avisar) + TP_Detalle (auditable).
"""

import pandas as pd

from programas.rem_utils import (norm, cargar_atenciones, cargar_maestro, maestro_rem_map,
                                 _rango_mes)
from modulos.rem_sm_actividades import mask_tributa_ada

# Heurística SM-ish sobre la ACTIVIDAD (no exhaustiva, por diseño). Ampliable.
_SMISH = ("mental", "demencia")
# NUM REM (normalizados) que SÍ tributan a las casillas SM del exe. Lo demás = perdido.
TRIBUTA_SM_REM = {norm(x) for x in
                  ("REM-A04", "REM-A06", "REM-19A", "REM-A26", "REM-A27", "REM-A32")}
_SIN_MAESTRO = "(sin maestro)"
_NO_EN_MAESTRO = "(nueva / no en maestro)"

_DET_COLS = ["fecha", "profesional", "estamento", "actividad", "num_rem", "run"]


def _mask_any(A, terminos):
    m = pd.Series(False, index=A.index)
    for t in terminos:
        m |= A.str.contains(norm(t), regex=False, na=False)
    return m


def analizar(d, ini, fin, rem_map=None, log=print):
    """`d` = ADA ya cargado (trae ACT_n, FECHA, PROF...). `rem_map` = {ACT_n -> NUM
    REM} del Maestro (opcional). Devuelve DataFrame de eventos PERDIDOS con
    `.attrs['tablas']` = {hoja: DataFrame}."""
    dm = d[(d["FECHA"] >= ini) & (d["FECHA"] <= fin)].copy()
    A = dm["ACT_n"]
    smish = _mask_any(A, _SMISH)
    heur = mask_tributa_ada(A)
    if rem_map:
        numrem = A.map(lambda x: rem_map.get(x))          # None si no está en el Maestro
        en_maestro = numrem.notna()
        tributa = (en_maestro & numrem.isin(TRIBUTA_SM_REM)) | (~en_maestro & heur)
        etiqueta = numrem.where(en_maestro, _NO_EN_MAESTRO)
    else:
        tributa = heur
        etiqueta = pd.Series(_SIN_MAESTRO, index=A.index)

    perd_mask = smish & ~tributa
    rep = dm[perd_mask]
    prof = rep["PROF"].map(lambda x: norm(x) or "(SIN PROFESIONAL)") if "PROF" in rep.columns \
        else pd.Series("(SIN PROFESIONAL)", index=rep.index)
    E = pd.DataFrame({
        "fecha": rep["FECHA"].values,
        "profesional": prof.values,
        "estamento": rep["INSTR"].astype(str).values if "INSTR" in rep.columns else "",
        "actividad": rep["ACT"].astype(str).values,
        "num_rem": etiqueta[perd_mask].astype(str).values,
        "run": rep["RUN"].astype(str).values,
    })

    E.attrs["tablas"] = {
        "TP_Resumen": _tabla_resumen(E, ini, rem_map is not None),
        "Por_Actividad": _por_actividad(E),
        "Por_Funcionario": _por_funcionario(E),
    }
    E.attrs["mes"] = (ini.year, ini.month)
    log(f"[tp] mes {ini:%Y-%m}: {len(E)} atenciones SM a SACO VACÍO (no tributan a "
        f"A04/A06/19A/A26/A27/A32)")
    if len(E):
        ta, na = _top(E, "actividad")
        tf, nf = _top(E, "profesional")
        log(f"[tp]   actividad top: «{ta}» ×{na}")
        log(f"[tp]   funcionario top: {tf} ×{nf}  (ver Por_Funcionario para corregir)")
    return E


def _top(sub, col):
    if not len(sub):
        return ("—", 0)
    vc = sub[col].value_counts()
    return (str(vc.index[0]), int(vc.iloc[0]))


def _tabla_resumen(E, ini, con_maestro):
    filas = [
        ("Atenciones SM a saco vacío (no tributan)", len(E)),
        ("  · funcionarios involucrados", E["profesional"].nunique() if len(E) else 0),
        ("  · actividades distintas mal usadas", E["actividad"].nunique() if len(E) else 0),
        ("  · pacientes afectados (RUN distintos)", E["run"].nunique() if len(E) else 0),
    ]
    if con_maestro and len(E):     # desglose por a-dónde-sí-iba (NUM REM del Maestro)
        for rem, n in E["num_rem"].value_counts().items():
            filas.append((f"  · a {rem}", int(n)))
    df = pd.DataFrame(filas, columns=["Indicador", "Valor"])
    df.attrs["mes"] = f"{ini:%Y-%m}"
    return df


def _por_actividad(E):
    """Una fila por (ACTIVIDAD, NUM REM): cuántas veces, cuántos funcionarios, cuántos
    pacientes. Ordena por frecuencia (lo más rentable de corregir arriba)."""
    cols = ["Actividad registrada", "NUM REM", "N atenciones", "N funcionarios", "N pacientes"]
    if not len(E):
        return pd.DataFrame(columns=cols)
    g = (E.groupby(["actividad", "num_rem"])
          .agg(**{"N atenciones": ("run", "size"),
                  "N funcionarios": ("profesional", "nunique"),
                  "N pacientes": ("run", "nunique")})
          .reset_index()
          .rename(columns={"actividad": "Actividad registrada", "num_rem": "NUM REM"})
          .sort_values("N atenciones", ascending=False, ignore_index=True))
    return g[cols]


def _por_funcionario(E):
    """Una fila por FUNCIONARIO: cuántas atenciones a saco vacío y qué actividad más
    repite. Ordena por N (a quién conviene avisar primero)."""
    cols = ["Funcionario", "Estamento", "N a saco vacío", "Actividad más repetida", "N pacientes"]
    if not len(E):
        return pd.DataFrame(columns=cols)
    filas = []
    for prof, s in E.groupby("profesional"):
        est = s["estamento"].mode()
        top = s["actividad"].value_counts()
        filas.append({
            "Funcionario": prof,
            "Estamento": (str(est.iloc[0]) if len(est) else ""),
            "N a saco vacío": len(s),
            "Actividad más repetida": str(top.index[0]),
            "N pacientes": s["run"].nunique(),
        })
    return pd.DataFrame(filas).sort_values("N a saco vacío", ascending=False, ignore_index=True)


def procesar(ada, maestro=None, mes=None, log=print, d=None):
    """Standalone: carga el ADA (+ Maestro opcional) y analiza. `ada` = ruta o lista.
    `maestro` = 'Maestro de Actividades' (opcional; sin él, todo por heurística).
    `mes` = (año, mes) o None (mes anterior). `d` = ADA ya cargado (para leer el ADA
    UNA sola vez cuando lo comparte con el módulo de actividades)."""
    d = cargar_atenciones(ada) if d is None else d
    rem_map = None
    if maestro is not None:
        dfm = cargar_maestro(maestro)
        rem_map = maestro_rem_map(dfm)
        log(f"[tp] Maestro: {len(rem_map)} actividades clasificadas por RAYEN")
    ini, fin = _rango_mes(mes)
    span = (f"{d['FECHA'].min():%Y-%m-%d}..{d['FECHA'].max():%Y-%m-%d}"
            if d["FECHA"].notna().any() else "sin fechas")
    log(f"[tp] ADA: {len(d)} atenciones ({span})")
    return analizar(d, ini, fin, rem_map=rem_map, log=log)


def escribir(E, salida):
    """Escribe el reporte de trabajo perdido (resumen + vistas + detalle auditable)."""
    tablas = E.attrs.get("tablas", {})
    with pd.ExcelWriter(salida) as xw:
        for nombre, df in tablas.items():
            df.to_excel(xw, index=False, sheet_name=nombre[:31])
        det = E[[c for c in _DET_COLS if c in E.columns]].sort_values(
            ["num_rem", "profesional", "fecha"])
        det.to_excel(xw, index=False, sheet_name="TP_Detalle")
    return str(salida)


# ── Descriptor para el registro (lo consume autorem.py) ──
TAREA = {
    "id": "sm_trabajo_perdido",
    "nombre": "SM · Trabajo perdido",
    "correr": procesar,       # (ada, maestro, mes, log) -> E
    "escribir": escribir,
}
