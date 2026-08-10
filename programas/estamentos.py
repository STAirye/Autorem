#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.7.2
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
cada CESFAM. La TABLA (nombres de funcionarios) queda LOCAL — NO va al repo.

FAILSAFE: si un funcionario del reporte no está en la tabla (p.ej. externo que
presta servicios transitorios), `faltantes()` lo detecta y el flujo lo resuelve a
mano (elegir estamento) o lo IGNORA (`aplicar_resoluciones`, None = ignorar).

USO:
    from programas.estamentos import cargar_estamentos, buscar_estamento
    tabla, meta = cargar_estamentos("Utilizacion de Cupos.xlsx")
    est = buscar_estamento("Catalina Andrea Mayorga Pino", tabla)  # -> 'Psicólogo(a)'
"""

from programas.rem_utils import (
    OPENPYXL_OK, OPENPYXL_ERR, openpyxl,
    ArchivoInvalido, norm, buscar_col,
)
from programas import formatos

# ── Firmas del reporte 'Utilización de Cupos' (RAYEN Administrativo) ──
# Header en fila 9 (banner Comuna/Establecimiento/Mes/Año/'Utilización de Cupos'
# arriba). Solo nos importan 2 columnas: Profesional (nombre) e Instrumento (=estamento).
# Es un export Administrativo → comparte los params de encabezado con A05/A03
# (`formatos.HEADER_ADMIN`), pero con su PROPIA ancla (Profesional/Instrumento).
ANCLA = ["PROFESIONAL", "INSTRUMENTO"]
MAX_FILAS_HEADER = 40


def _fila_encabezado(ws):
    return formatos.fila_encabezado_admin(ws, ancla=ANCLA, max_filas=MAX_FILAS_HEADER)


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
    hidx, _ = _fila_encabezado(ws)
    hn = [norm(ws.cell(row=hidx, column=c).value) for c in range(1, ws.max_column + 1)]
    prof_c = buscar_col(hn, exacto="PROFESIONAL") or buscar_col(hn, tokens=["PROFESIONAL"])
    inst_c = buscar_col(hn, exacto="INSTRUMENTO") or buscar_col(hn, tokens=["INSTRUMENTO"])
    if not (prof_c and inst_c):
        raise ArchivoInvalido(
            "no_estamentos",
            "Ubiqué el encabezado pero no las columnas Profesional / Instrumento.")

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


# ── Failsafe: resolución manual de funcionarios sin match ─────────────
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
