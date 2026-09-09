#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Sonnet 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.9.8
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. Distributed WITHOUT ANY WARRANTY. See the GNU
# General Public License for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
dotacion.py — separar atenciones de funcionarios EXTERNOS (no son de la
dotación del CESFAM, p.ej. la sala AIDIA) de las de la dotación propia.

Módulo TRANSVERSAL, gemelo estructural de `programas/estamentos.py` (misma
persistencia/merge/failsafe — ver ese archivo antes de tocar este). No sabe
nada de Salud Mental: hoy lo consume `modulos/rem_sm_actividades.py`, pero
cualquier módulo con el mismo problema (A23, otros programas) lo reusa igual.

PROBLEMA: no existe ninguna fuente autoritativa que distinga funcionarios
internos de externos (verificado contra exports reales, ver
docs/dotacion_externos_plan.md §0.1). La tabla se construye desde las
decisiones del propio usuario.

DISEÑO (ver el plan, NO deshacer sin motivo):
  - El eje es el FUNCIONARIO (persona), no la actividad/agenda (§1.1).
  - Tri-estado `interno` / `externo` / `desconocido`, nunca whitelist/blacklist
    puras: ambas fallan calladas en direcciones opuestas (§1.2).
  - `en_rem = (clase != "externo")`: un `desconocido` CUENTA al REM (el default
    no sangra producción propia), pero se reporta siempre (§1.3).
  - Persistencia en `~/.autorem/dotacion.json`, DOS claves independientes:
    `funcionarios` (clasificación, global — es un hecho de la persona) y
    `omitidos` (estamentos que un módulo dejó de preguntar, indexado POR
    módulo — un estamento irrelevante en SM puede ser central en A23) (§2.1).
  - Un funcionario de un estamento OMITIDO NO se marca `interno`: queda
    `desconocido` (nadie lo miró) y solo deja de preguntarse por él en ESE
    módulo.

USO:
    from programas import dotacion
    tabla = dotacion.cargar()
    ev = dotacion.evidencia(ada_tributa, tabla, modulo="sm")   # ada YA filtrado
    nuevos = dotacion.nuevos(ev, tabla, "sm")                  # -> abrir diálogo si no está vacío
    dotacion.marcar(tabla, {"Juan Perez": True, "Ana Soto": False})
    clase = dotacion.clasificar(serie_de_nombres, tabla)       # vectorizado
"""

import json
from pathlib import Path

import pandas as pd

from programas.rem_utils import norm

# -- Persistencia entre corridas (caché local, HOME del usuario) -------
# Nombres de funcionario NO son PII de paciente -> cachearlos es aceptable
# (mismo criterio ya documentado en estamentos.py). Nunca en el repo ni junto
# al .exe.
RUTA_CACHE = Path.home() / ".autorem" / "dotacion.json"

INTERNO = "interno"
EXTERNO = "externo"
DESCONOCIDO = "desconocido"


def _tabla_vacia():
    return {"funcionarios": {}, "omitidos": {}}


def cargar(log=print):
    """Tabla cacheada del disco: {'funcionarios': {nombre_norm: 'interno'|
    'externo'}, 'omitidos': {modulo: [estamento_norm, ...]}}. Vacía si no
    existe o el caché está corrupto (robusto: nunca revienta la corrida)."""
    try:
        if RUTA_CACHE.exists():
            with open(RUTA_CACHE, encoding="utf-8") as f:
                d = json.load(f)
            if isinstance(d, dict):
                func = d.get("funcionarios", {})
                omit = d.get("omitidos", {})
                if isinstance(func, dict) and isinstance(omit, dict):
                    return {"funcionarios": dict(func), "omitidos": dict(omit)}
    except Exception as e:   # noqa: BLE001
        log(f"[dotacion] no pude leer el caché ({e}); sigo sin él")
    return _tabla_vacia()


def guardar(tabla, log=print):
    """Escribe la tabla al caché (crea ~/.autorem si falta). Falla silenciosa
    con aviso: no arruina la corrida si el disco/permisos fallan."""
    try:
        RUTA_CACHE.parent.mkdir(parents=True, exist_ok=True)
        with open(RUTA_CACHE, "w", encoding="utf-8") as f:
            json.dump(tabla, f, ensure_ascii=False, sort_keys=True, indent=0)
    except Exception as e:   # noqa: BLE001
        log(f"[dotacion] no pude guardar el caché ({e})")


def clase(nombre, tabla):
    """'interno' | 'externo' | 'desconocido' (default) para un nombre."""
    if not nombre:
        return DESCONOCIDO
    return (tabla or {}).get("funcionarios", {}).get(norm(nombre), DESCONOCIDO)


def clasificar(serie_nombres, tabla):
    """Vectorizado: Series de nombres -> Series de clase ('interno'/'externo'/
    'desconocido')."""
    func = (tabla or {}).get("funcionarios", {})
    return serie_nombres.map(lambda n: func.get(norm(n), DESCONOCIDO) if n else DESCONOCIDO)


def en_rem(serie_clase):
    """bool: True salvo 'externo' (§1.3) — el desconocido CUENTA al REM."""
    return serie_clase != EXTERNO


def marcar(tabla, decisiones):
    """Aplica decisiones del diálogo: {nombre: True(externo)/False(interno)}.
    Muta `tabla['funcionarios']` y persiste. Devuelve `tabla`."""
    func = tabla.setdefault("funcionarios", {})
    for nombre, es_externo in (decisiones or {}).items():
        if not nombre:
            continue
        func[norm(nombre)] = EXTERNO if es_externo else INTERNO
    guardar(tabla)
    return tabla


def omitir(tabla, modulo, estamentos):
    """Agrega estamentos a `omitidos[modulo]` (normalizados, dedup). Un
    funcionario de un estamento omitido NO se marca interno: sigue
    `desconocido`, solo deja de preguntarse por él en ESE módulo (§2.1).
    Muta y persiste. Devuelve `tabla`."""
    omit = tabla.setdefault("omitidos", {})
    lista = list(dict.fromkeys(omit.get(modulo, [])))
    for e in (estamentos or []):
        k = norm(e)
        if k and k not in lista:
            lista.append(k)
    omit[modulo] = lista
    guardar(tabla)
    return tabla


def omitidos(tabla, modulo):
    """Estamentos omitidos (sin preguntar) para ese módulo."""
    return list((tabla or {}).get("omitidos", {}).get(modulo, []))


def evidencia(ada, tabla=None, modulo=None):
    """`ada` = DataFrame canónico de atenciones (columnas PROF/INSTR/ACT, y
    SECTOR si está) YA RESTRINGIDO a las filas que tributan al REM del módulo
    llamante (p.ej. `dm[mask_tributa_ada(dm['ACT_n'])]`) — dotacion.py no sabe
    qué tributa, por eso el filtro lo aplica el módulo antes de llamar acá.

    Devuelve 1 fila por funcionario: `funcionario` (nombre original), `estamento`
    (INSTR más frecuente), `n_atenciones`, `actividades` (top-3 ACT por
    frecuencia, unidas con ' · '), `sector` (más frecuente). Orden: por
    `n_atenciones` descendente.

    El agregado por estamento (lo que ordena el diálogo, §2.3) queda en
    `.attrs['por_estamento']`: `estamento`, `n_funcionarios`, `n_atenciones`,
    también ordenado por `n_atenciones` descendente."""
    cols_ev = ["funcionario", "estamento", "n_atenciones", "actividades", "sector"]
    cols_est = ["estamento", "n_funcionarios", "n_atenciones"]
    if ada is None or len(ada) == 0:
        ev = pd.DataFrame(columns=cols_ev)
        ev.attrs["por_estamento"] = pd.DataFrame(columns=cols_est)
        return ev

    d = ada.copy()
    d["_prof"] = d["PROF"].fillna("").astype(str).str.strip() if "PROF" in d.columns else ""
    d = d[d["_prof"] != ""]
    if d.empty:
        ev = pd.DataFrame(columns=cols_ev)
        ev.attrs["por_estamento"] = pd.DataFrame(columns=cols_est)
        return ev

    filas = []
    for prof, g in d.groupby("_prof", sort=False):
        inst = g["INSTR"].astype(str) if "INSTR" in g.columns else pd.Series([""] * len(g))
        moda_inst = inst.mode()
        act = g["ACT"].astype(str) if "ACT" in g.columns else pd.Series([""] * len(g))
        top_act = " · ".join(act.value_counts().head(3).index.tolist())
        sect = g["SECTOR"].astype(str) if "SECTOR" in g.columns else pd.Series(dtype=str)
        moda_sect = sect.mode() if len(sect) else pd.Series(dtype=str)
        filas.append({
            "funcionario": prof,
            "estamento": moda_inst.iat[0] if not moda_inst.empty else "",
            "n_atenciones": len(g),
            "actividades": top_act,
            "sector": moda_sect.iat[0] if not moda_sect.empty else "",
        })
    ev = pd.DataFrame(filas, columns=cols_ev).sort_values(
        "n_atenciones", ascending=False).reset_index(drop=True)

    por_est = (ev.groupby("estamento", as_index=False)
                 .agg(n_funcionarios=("funcionario", "nunique"),
                      n_atenciones=("n_atenciones", "sum"))
                 .sort_values("n_atenciones", ascending=False)
                 .reset_index(drop=True))
    ev.attrs["por_estamento"] = por_est[cols_est]
    return ev


def nuevos(ev, tabla, modulo):
    """De la evidencia (`evidencia()`), los funcionarios SIN clasificar y de
    estamento NO omitido para `modulo` (§2.3). Vacío -> no abrir el diálogo.
    Primera corrida (tabla vacía) -> devuelve TODOS (comportamiento first-run,
    §3.1)."""
    if ev is None or ev.empty:
        return ev if ev is not None else pd.DataFrame(
            columns=["funcionario", "estamento", "n_atenciones", "actividades", "sector"])
    func = (tabla or {}).get("funcionarios", {})
    omit_est = {norm(e) for e in omitidos(tabla, modulo)}
    ya_clasificado = ev["funcionario"].map(lambda n: norm(n) in func)
    estamento_omitido = ev["estamento"].map(lambda e: norm(e) in omit_est)
    return ev[~ya_clasificado & ~estamento_omitido].reset_index(drop=True)
