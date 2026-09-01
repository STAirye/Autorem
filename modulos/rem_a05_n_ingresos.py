#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.7.12
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
Marcado de INGRESOS de Salud Mental (export IRIS) para el REM A05.

Gemelo de rem_a05_o_egresos.py: mismo export IRIS 'Control de Salud Mental', mismo
análisis (patología, subtipo, demografía). La única diferencia es el token de
ESTADO: aquí se flaggea 'INGRESO' (un solo tipo de evento). Todo el motor vive en
rem_saludmental.py. La GUI/CLI está en autorem.py.

USO como librería:
    from modulos.rem_a05_n_ingresos import procesar
    procesar(entrada_xlsx, salida_xlsx, log=print)
"""

import programas.rem_saludmental as sm

# ── Config específica del INGRESO ─────────────────────────────────────
NOMBRE_HOJA_SALIDA = "A05_Ingresos"
BUSQUEDAS = {"Ingreso": ["INGRESO"]}     # la columna '...ESTADO' muestra 'Ingreso'
TIPO_LABEL = {"Ingreso": "Ingreso"}
ORDEN_TIPOS = {"Ingreso": 0}
# Ingreso con diagnóstico que DEBERÍA tener subtipo y no lo trae -> Falta_Subtipo.
AVISAR_SIN_SUBTIPO = {"Ingreso"}

_CFG = dict(
    busquedas=BUSQUEDAS,
    tipo_label=TIPO_LABEL,
    orden_tipos=ORDEN_TIPOS,
    hoja_salida=NOMBRE_HOJA_SALIDA,
    tipo_col_header="Tipo_Ingreso",
    avisar_sin_subtipo=AVISAR_SIN_SUBTIPO,
    etiqueta="ingreso",
)


def agregar_hoja(wb, ws, perfil, log=print, mes=None):
    """Agrega la hoja de ingresos al workbook ya abierto (NO guarda). `mes`=(año,mes)
    filtra por FECHA FORMULARIO; None = archivo completo."""
    return sm.marcar_eventos(wb, ws, perfil, log=log, mes=mes, **_CFG)


def procesar(entrada, salida, perfil=sm.PERFIL_IRIS, log=print, mes=None):
    """Conveniencia standalone: abre + valida + marca + guarda. `mes`=(año,mes) o
    None (todo el archivo)."""
    wb, ws = sm.abrir_validado(entrada, perfil)
    res = agregar_hoja(wb, ws, perfil, log=log, mes=mes)
    wb.save(salida)
    log(f"[ok] guardado: {salida}  (hoja '{NOMBRE_HOJA_SALIDA}')")
    res = dict(res)
    res["salida"] = str(salida)
    return res


# ── Descriptor para el registro de tareas (lo consume autorem.py) ──
TAREA = {
    "id": "a05_n_ingresos",
    "nombre": "A05 · Ingresos",
    "agregar": agregar_hoja,             # (wb, ws, perfil, log) -> resumen ; NO guarda
    "correr": procesar,                  # (entrada, salida, perfil, log) -> resumen
    "hoja": NOMBRE_HOJA_SALIDA,
}
