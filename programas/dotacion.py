#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Sonnet 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.9.17
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

from pathlib import Path

import pandas as pd

from programas.rem_utils import norm, leer_cache_json, guardar_cache_json, apartar_cache

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


# Textos de los avisos de caché (rem_utils.leer_cache_json / guardar_cache_json): QUE
# se pierde, dicho en lo que le importa al usuario -- no "no pude escribir el JSON".
_QUE = "la tabla de dotación (quién es externo)"
_SI_SE_PIERDE = ("te voy a preguntar por TODOS los funcionarios como si fuera la primera "
                 "vez. OJO: sin tick cuenta como interno, así que vuelve a marcar a los "
                 "externos que ya tenías marcados.")
_SI_NO_SE_GUARDA = ("el próximo mes te va a volver a preguntar por estos funcionarios (y "
                    "sin tick cuentan como internos).")


def _cargar_con_estado(log=print):
    datos, estado = leer_cache_json(RUTA_CACHE, _QUE, _SI_SE_PIERDE, log=log)
    if estado != "ok":
        return _tabla_vacia(), estado
    func = datos.get("funcionarios", {})
    omit = datos.get("omitidos", {})
    if not (isinstance(func, dict) and isinstance(omit, dict)):
        apartar_cache(RUTA_CACHE, _QUE, "no tiene la forma esperada", _SI_SE_PIERDE, log=log)
        return _tabla_vacia(), "corrupto"
    return {"funcionarios": dict(func), "omitidos": dict(omit)}, "ok"


def cargar(log=print):
    """Tabla cacheada del disco: {'funcionarios': {nombre_norm: 'interno'|
    'externo'}, 'omitidos': {modulo: [estamento_norm, ...]}}. Vacía si no existe;
    si esta dañada o no se puede leer, tambien vacia pero con aviso RUIDOSO
    (rem_utils.leer_cache_json): una tabla vacia vuelve a contar a todos los
    externos, asi que eso nunca puede pasar callado. Nunca revienta la corrida."""
    return _cargar_con_estado(log=log)[0]


def guardar(tabla, log=print):
    """Escribe la tabla ENTERA al caché. True si quedo guardada; si no, aviso ruidoso
    (rem_utils.guardar_cache_json). Las decisiones del dialogo NO pasan por aca sino
    por `_persistir`, que no pisa lo que otra ventana haya guardado mientras tanto."""
    return guardar_cache_json(RUTA_CACHE, tabla, _QUE, _SI_NO_SE_GUARDA, log=log)


def _persistir(cambiar, log=print):
    """Relee el disco, le aplica `cambiar(tabla_del_disco)` y guarda: solo ESTOS
    cambios, sobre lo que hay AHORA. Guardar la copia en memoria entera pisaria lo
    que otra ventana de autoREM guardo despues de que esta cargara (la ultima en
    guardar ganaba y revertia el resto). Si el disco no se pudo LEER no se guarda
    nada: el archivo puede estar sano, y escribir encima lo perderia entero."""
    disco, estado = _cargar_con_estado(log=log)
    if estado == "ilegible":
        from programas.rem_utils import _avisar_cache, _SIGUE
        _avisar_cache(log, f"No guardé los cambios en {_QUE}: {_SI_NO_SE_GUARDA} {_SIGUE}")
        return False
    cambiar(disco)
    return guardar(disco, log=log)


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


def marcar(tabla, decisiones, log=print):
    """Aplica decisiones del diálogo: {nombre: True(externo)/False(interno)}.
    Muta `tabla['funcionarios']` (lo que usa ESTA corrida) y persiste solo estas
    decisiones (`_persistir`). Devuelve `tabla`."""
    cambios = {norm(n): (EXTERNO if ext else INTERNO)
               for n, ext in (decisiones or {}).items() if n}
    tabla.setdefault("funcionarios", {}).update(cambios)
    _persistir(lambda t: t.setdefault("funcionarios", {}).update(cambios), log=log)
    return tabla


def omitir(tabla, modulo, estamentos, log=print):
    """Agrega estamentos a `omitidos[modulo]` (normalizados, dedup). Un
    funcionario de un estamento omitido NO se marca interno: sigue
    `desconocido`, solo deja de preguntarse por él en ESE módulo (§2.1).
    Muta y persiste (solo este cambio, `_persistir`). Devuelve `tabla`."""
    nuevos_est = [k for k in (norm(e) for e in (estamentos or [])) if k]

    def agregar(t):
        omit = t.setdefault("omitidos", {})
        lista = list(dict.fromkeys(omit.get(modulo, [])))
        lista += [k for k in nuevos_est if k not in lista]
        omit[modulo] = lista
    agregar(tabla)
    _persistir(agregar, log=log)
    return tabla


def quitar_omision(tabla, modulo, estamento, log=print):
    """Deshace `omitir` para UN estamento (el dialogo 'Revisar dotacion'). Muta y
    persiste solo este cambio (`_persistir`). Devuelve `tabla`."""
    k = norm(estamento)

    def quitar(t):
        omit = t.setdefault("omitidos", {})
        omit[modulo] = [x for x in omit.get(modulo, []) if x != k]
    quitar(tabla)
    _persistir(quitar, log=log)
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
