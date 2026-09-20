#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
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
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
estamentos.py — lookup Funcionario -> Estamento (desde 'Utilización de Cupos').

Módulo TRANSVERSAL: aplica a CUALQUIER carga en formato **Administrativo** (hoy el
screening A03 D.3; a futuro cualquier módulo que reporte por estamento). El
Administrativo NO trae el estamento de quien atendió, solo el NOMBRE del
funcionario. El reporte de RAYEN 'Utilización de Cupos' sí parea `Profesional` ->
`Instrumento`, donde 'Instrumento' es —otra vez— el ESTAMENTO mal rotulado
(Médico / Psicólogo(a) / Terapeuta Ocupacional / Trabajador(a) Social / etc.).

Como los profesionales cambian por centro, el lookup se arma DESDE el export de
cada CESFAM. La TABLA (nombres de funcionarios) queda LOCAL — NO va al repo — y
PERSISTE entre corridas en `~/.autorem/estamentos.json` (ver `tabla_efectiva`):
se carga una vez y los meses siguientes se autocompleta; cargar un reporte nuevo
fusiona (el fresco gana, lo solo-en-caché se conserva).

FAILSAFE: si un funcionario del reporte no está en la tabla (p.ej. externo que
presta servicios transitorios), `faltantes()` lo detecta y el flujo lo resuelve a
mano (elegir estamento) o lo IGNORA (`aplicar_resoluciones`, None = ignorar).

USO:
    from programas.estamentos import cargar_estamentos, buscar_estamento
    tabla, meta = cargar_estamentos("Utilizacion de Cupos.xlsx")
    est = buscar_estamento("Catalina Andrea Mayorga Pino", tabla)  # -> 'Psicólogo(a)'
"""

from pathlib import Path

from programas.rem_utils import (
    OPENPYXL_OK, OPENPYXL_ERR, openpyxl,
    ArchivoInvalido, norm, buscar_col, exigir_filas_ws, encontrar_fila_encabezado,
    leer_cache_json, guardar_cache_json,
)
from programas import formatos

# -- Firmas del reporte 'Utilización de Cupos' (RAYEN Administrativo) --
# Header en fila 9, de DOS pisos (celdas combinadas; banner Comuna/Establecimiento/Mes/
# Año/'Utilización de Cupos' arriba; ver refs_tablas/Utilizacion_cupos_admin.xlsx).
# Solo nos importan 2 columnas: Profesional (nombre) e Instrumento (=estamento). El
# encabezado se ubica con `rem_utils.encontrar_fila_encabezado` y su PROPIA ancla.
ANCLA = ["PROFESIONAL", "INSTRUMENTO"]
MAX_FILAS_HEADER = 40


def detectar(ws):
    """True si la hoja parece el reporte de Utilización de Cupos (fila con
    'Profesional' e 'Instrumento' en el encabezado)."""
    tope = min(ws.max_row, MAX_FILAS_HEADER)
    anc = [norm(t) for t in ANCLA]
    for r in range(1, tope + 1):
        vals = [norm(c.value) for c in ws[r]]
        if all(any(t in v for v in vals) for t in anc):
            return True
    return False


def cargar_estamentos(entrada, log=print):
    """Lee el reporte y devuelve (tabla, meta):
      tabla = {nombre_normalizado: estamento_original}   (para buscar_estamento)
      meta  = {'funcionarios', 'conflictos', 'header'}
    Dedup por nombre; ante un nombre con >1 estamento conserva el 1º y avisa."""
    if not OPENPYXL_OK:
        raise ImportError(
            "Falta 'openpyxl'. Instálala con:  pip install openpyxl\n"
            f"(detalle: {OPENPYXL_ERR})")
    wb = openpyxl.load_workbook(entrada)
    ws = wb.active
    if not detectar(ws):
        raise ArchivoInvalido(
            "no_estamentos",
            "Este archivo no parece el reporte de 'Utilización de Cupos': no "
            "encontré las columnas 'Profesional' e 'Instrumento'.\n"
            "Bájalo del Administrativo (Utilización de Cupos), copia la tabla a "
            "un Excel y guárdalo como .xlsx.")
    hidx = encontrar_fila_encabezado(ws, ANCLA, MAX_FILAS_HEADER)
    hn = [norm(ws.cell(row=hidx, column=c).value) for c in range(1, ws.max_column + 1)]
    prof_c = buscar_col(hn, exacto="PROFESIONAL") or buscar_col(hn, tokens=["PROFESIONAL"])
    inst_c = buscar_col(hn, exacto="INSTRUMENTO") or buscar_col(hn, tokens=["INSTRUMENTO"])
    if not (prof_c and inst_c):
        raise ArchivoInvalido(
            "no_estamentos",
            "Ubiqué el encabezado pero no las columnas Profesional / Instrumento.")
    # Fail loud sobre la FUENTE (CLAUDE.md regla 2): una tabla vacia no falla, deja a
    # TODOS los funcionarios sin estamento (y pisaria el cache con un dict vacio).
    exigir_filas_ws(ws, hidx, "el reporte de 'Utilización de Cupos'")

    tabla = {}
    conflictos = {}
    n_filas = 0
    for r in range(hidx + 1, ws.max_row + 1):
        nombre = ws.cell(row=r, column=prof_c).value
        estam = ws.cell(row=r, column=inst_c).value
        if nombre in (None, "") or estam in (None, ""):
            continue
        k = norm(nombre)
        e = str(estam).strip()
        n_filas += 1
        if k in tabla:
            if tabla[k] != e:
                conflictos.setdefault(str(nombre).strip(), set()).update({tabla[k], e})
            continue                      # conserva el primero visto
        tabla[k] = e

    if not tabla:
        # exigir_filas_ws de arriba mira que HAYA filas; esto, que alguna sirva. Sin
        # ninguna fila con Profesional E Instrumento, la tabla sale vacia y la corrida
        # sigue con el cache solo, sin decirlo.
        raise ArchivoInvalido(
            "sin_datos",
            "El reporte de 'Utilización de Cupos' trae filas, pero ninguna con Profesional "
            "e Instrumento a la vez: no hay ningún estamento que leer.\n\n"
            "Revisa que sea el reporte completo, sin modificar.")
    log(f"[estamentos] {len(tabla)} funcionarios (de {n_filas} filas de agenda) "
        f"| encabezado fila {hidx}")
    if conflictos:
        muestra = "; ".join(f"{n}: {sorted(v)}" for n, v in list(conflictos.items())[:5])
        log(f"[estamentos] AVISO: {len(conflictos)} funcionario(s) con >1 estamento "
            f"(se usó el 1º): {muestra}")
    return tabla, {"funcionarios": len(tabla), "conflictos": len(conflictos), "header": hidx}


def buscar_estamento(nombre, tabla):
    """Estamento del funcionario por nombre (match normalizado). '' si no está
    o si no hay tabla."""
    if not nombre or not tabla:
        return ""
    return tabla.get(norm(nombre), "")


# -- Failsafe: resolución manual de funcionarios sin match -------------
# Estamentos estándar del CESFAM (opciones del selector manual cuando un
# profesional no aparece en 'Utilización de Cupos'). Superset de lo visto en el
# reporte real; los 4 primeros son los que aplican screening.
ESTAMENTOS = [
    "Médico", "Psicólogo(a)", "Terapeuta Ocupacional", "Trabajador(a) Social",
    "Enfermero(a)", "Matron(a)", "Nutricionista", "Kinesiólogo(a)",
    "Odontólogo(a)", "Técnico Paramédico", "Fonoaudiólogo(a)",
    "Educador(a) de Párvulos", "Otro",
]


def estamentos_conocidos(tabla=None):
    """Opciones para el selector manual: los estamentos vistos en la tabla + el
    estándar (sin duplicar, en ese orden)."""
    vistos = list(dict.fromkeys(tabla.values())) if tabla else []
    for e in ESTAMENTOS:
        if e and e not in vistos:
            vistos.append(e)
    return vistos


def faltantes(nombres, tabla):
    """De una lista de nombres de funcionario, los que NO tienen match en `tabla`
    (normalizado, sin duplicados, en orden de aparición). Ignora vacíos."""
    out, seen = [], set()
    for n in nombres:
        if not n:
            continue
        k = norm(n)
        if k in seen:
            continue
        seen.add(k)
        if k not in tabla:
            out.append(str(n).strip())
    return out


def aplicar_resoluciones(tabla, resoluciones):
    """Mete las resoluciones manuales en `tabla` (la muta y la devuelve).
    resoluciones = {nombre: estamento | None}; None = IGNORAR -> queda '' (ya no
    se vuelve a preguntar; p.ej. externo que presta servicios transitorios)."""
    for nombre, est in (resoluciones or {}).items():
        tabla[norm(nombre)] = est or ""
    return tabla


# -- Persistencia entre corridas (caché local) -------------------------
# La tabla funcionario->estamento se guarda en el HOME del usuario (no en el repo,
# no junto al .exe) para que persista entre meses/carpetas: cargar 'Utilización de
# Cupos' una vez y que el mes siguiente se autocomplete sin volver a cargarlo.
# Nombres de funcionario NO son PII de paciente -> cachearlos es aceptable.
RUTA_CACHE = Path.home() / ".autorem" / "estamentos.json"


# Textos de los avisos de caché (rem_utils.leer_cache_json / guardar_cache_json).
_QUE = "la tabla de estamentos (del reporte «Utilización de Cupos»)"
_SI_SE_PIERDE = ("los meses que no cargues «Utilización de Cupos», las atenciones del "
                 "formato Administrativo quedan sin estamento. Vuelve a cargarlo.")
_SI_NO_SE_GUARDA = ("el próximo mes vas a tener que volver a cargar «Utilización de "
                    "Cupos».")


def _cargar_cache_con_estado(log=print):
    datos, estado = leer_cache_json(RUTA_CACHE, _QUE, _SI_SE_PIERDE, log=log)
    if estado != "ok":
        return {}, estado
    return {str(k): ("" if v is None else str(v)) for k, v in datos.items()}, "ok"


def cargar_cache(log=print):
    """Tabla cacheada del disco. {} si no existe; si esta dañada o no se puede leer,
    tambien {} pero con aviso RUIDOSO (rem_utils.leer_cache_json). Nunca revienta."""
    return _cargar_cache_con_estado(log=log)[0]


def guardar_cache(tabla, log=print):
    """Escribe la tabla al caché. True si quedo guardada; si no, aviso ruidoso
    (rem_utils.guardar_cache_json): la corrida sigue con la tabla en memoria."""
    return guardar_cache_json(RUTA_CACHE, tabla, _QUE, _SI_NO_SE_GUARDA, log=log)


def tabla_efectiva(entrada=None, log=print):
    """Tabla funcionario->estamento combinando el CACHÉ persistente con el reporte
    'Utilización de Cupos' recién cargado (si se pasa `entrada`, ruta al .xlsx).

    - El reporte fresco GANA sobre el caché (los profesionales cambian).
    - Los nombres que solo están en el caché se CONSERVAN (funcionarios de meses
      previos + resoluciones manuales) -> un mes sin cargar el reporte igual rellena.
    - Persiste el merge de vuelta al caché.
    Devuelve la tabla (dict); {} si no hay ni caché ni archivo."""
    cache, estado = _cargar_cache_con_estado(log=log)
    if entrada:
        nueva, _meta = cargar_estamentos(entrada, log=log)
        tabla = {**cache, **nueva}                  # reporte fresco pisa al caché
        if estado == "ilegible":
            # El caché existe pero no se pudo leer: guardar encima lo perderia ENTERO
            # (los funcionarios de meses anteriores). Ya se aviso en la lectura.
            log("[estamentos] no actualizo el caché: no lo pude leer (ver el aviso)")
        elif guardar_cache(tabla, log=log):
            solo_cache = len(tabla) - len(nueva)
            log(f"[estamentos] caché actualizado: {len(tabla)} funcionarios "
                f"({len(nueva)} del reporte + {solo_cache} sólo en caché) -> {RUTA_CACHE}")
    else:
        tabla = cache
        if tabla:
            log(f"[estamentos] usando SOLO el caché ({len(tabla)} funcionarios, {RUTA_CACHE}): "
                "no cargaste 'Utilización de Cupos' esta vez")
    return tabla
