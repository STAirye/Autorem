#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.3.3
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
Marcado de EGRESOS de Salud Mental (export IRIS) para el REM A05.

Módulo de tarea HEADLESS y fino: solo aporta la config del egreso (qué token de
ESTADO flaggear, cómo se llama su hoja/columna). Todo el análisis —validación,
patología, subtipo, demografía, motor de marcado— vive en rem_saludmental.py,
que comparte con rem_a05_n_ingresos.py. La GUI/CLI está en autorem.py.

Un egreso puede ser Alta, Traslado u Otras Causas:
  - Alta y Traslado van a estadística.
  - Otras Causas se flaggea para revisión MANUAL (abandono vs clínica, caso a
    caso); solo se marca, no se clasifica automático.

USO como librería:
    from modulos.rem_a05_o_egresos import procesar
    procesar(entrada_xlsx, salida_xlsx, log=print)
"""

import programas.rem_saludmental as sm

# ── Config específica del EGRESO (lo único propio de este módulo) ──────
NOMBRE_HOJA_SALIDA = "A05_Egresos"
BUSQUEDAS = {
    "Alta":        ["EGRESO", "ALTA"],
    "Traslado":    ["EGRESO", "TRASLADO"],
    "OtrasCausas": ["EGRESO", "OTRAS", "CAUSAS"],
}
TIPO_LABEL = {"Alta": "Alta", "Traslado": "Traslado", "OtrasCausas": "Otras Causas"}
ORDEN_TIPOS = {"Alta": 0, "Traslado": 1, "OtrasCausas": 2}
# Avisar egreso por Alta sin subtipo (solo en diagnósticos que SÍ tienen subtipo).
AVISAR_SIN_SUBTIPO = {"Alta"}

_CFG = dict(
    busquedas=BUSQUEDAS,
    tipo_label=TIPO_LABEL,
    orden_tipos=ORDEN_TIPOS,
    hoja_salida=NOMBRE_HOJA_SALIDA,
    tipo_col_header="Tipo_Egreso",
    avisar_sin_subtipo=AVISAR_SIN_SUBTIPO,
    etiqueta="egreso",
)


def agregar_hoja(wb, ws, perfil, log=print):
    """Agrega la hoja de egresos al workbook ya abierto (NO guarda)."""
    return sm.marcar_eventos(wb, ws, perfil, log=log, **_CFG)


def procesar(entrada, salida, perfil=sm.PERFIL_IRIS, log=print):
    """Conveniencia standalone: abre + valida + marca + guarda. `perfil` fija el
    formato de entrada (IRIS por defecto). Devuelve el resumen con la ruta."""
    wb, ws = sm.abrir_validado(entrada, perfil)
    res = agregar_hoja(wb, ws, perfil, log=log)
    wb.save(salida)
    log(f"[ok] guardado: {salida}  (hoja '{NOMBRE_HOJA_SALIDA}')")
    res = dict(res)
    res["salida"] = str(salida)
    return res


# ── Descriptor para el registro de tareas (lo consume autorem.py) ──
# La tarea es agnóstica al formato; el perfil (IRIS/admin) lo elige el usuario y
# lo pasa el dispatcher. Egresos e ingresos leen el mismo formulario.
TAREA = {
    "id": "a05_o_egresos",
    "nombre": "A05 · Egresos",
    "agregar": agregar_hoja,             # (wb, ws, perfil, log) -> resumen ; NO guarda
    "correr": procesar,                  # (entrada, salida, perfil, log) -> resumen
    "hoja": NOMBRE_HOJA_SALIDA,
}
