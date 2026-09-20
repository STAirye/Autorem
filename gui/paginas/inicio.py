#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Sonnet 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# Copyright (C) 2026 Simon Tobar
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
gui/paginas/inicio.py - Pantalla de inicio (paso 10 del plan, SS4).

NO expone `PANTALLA`: no es una pagina de procesamiento (sin `correr`,
sin Procesar, sin log) y por eso NO vive en `gui.registro` (que descubre
paginas por ese contrato) ni se agrupa por programa en el sidebar -- `gui.app`
la registra a mano junto a `about.py`, aparte, debajo del separador (mismo
tratamiento que la maqueta de SS4 del plan).

En vez del contrato `PANTALLA`, expone `construir(frame, app)`: mismo molde
que `extras[].construir(frame, pagina)`, pero con la `App` completa (no una
`Pagina` de una pantalla puntual) porque necesita `app.registro` y
`app.mostrar()` para los accesos directos.

A PROPOSITO no lleva el aviso de "carga los archivos sin modificar": esa
salvaguarda fail-loud (CLAUDE.md regla 2) vive en cada pagina que RECIBE un
export (`widgets.aviso_sin_modificar`), no en una pantalla que se ve una vez
y no toca ningun archivo (SS4 del plan lo dice explicito)."""

import customtkinter as ctk

from programas.rem_utils import VERSION
from gui import widgets

_DESCRIPCION = (
    ("autoREM tabula el REM (Registro Estadístico Mensual) a partir de los exports directamente descargados de RAYEN Administrativo e IRIS: cargas las planillas de Excel, eliges el mes, y obtienes una planilla lista para copiar al formulario oficial.\n"
     "Nació por iniciativa de referente de Salud Mental del CESFAM Dr. Luis Ferrada Urzúa y apunta a ser universal — cualquier programa de salud, cualquier centro.\n"
     "100% local: ningún archivo ni dato sale de este computador. Toda informacion sensible de paciente (PII) es procesada por el programa, pero no se guarda memoria de ello ni sale del equipo.\n"
     "Por diseño, el programa no realiza conexion con internet, por lo que cualquier actualizacion debe ser revisada a mano en el link en Acerca De.")
)

# Accesos directos a lo mas usado (ids de PANTALLA, ver gui/paginas/*.py). A05
# primero: es el UNICO modulo validado en produccion hoy (modulos/CLAUDE.md
# SS3, "el REM de agosto 2026 se hizo completo con la herramienta"), asi que
# es el que mas se usa mes a mes. Un id que ya no exista simplemente no
# aparece (fail soft: esto es un atajo, no el unico camino a la pagina).
_ACCESOS = ("a05", "sm_actividades", "a23_respiratorio")


def construir(frame, app):
    ctk.CTkLabel(frame, text=f"autoREM {VERSION}",
                font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", pady=(4, 8))
    widgets.etiqueta_envolvente(frame, _DESCRIPCION).pack(fill="x", pady=(0, 16))

    caja = widgets.caja_titulada(frame, "Accesos directos")
    caja.pack(fill="x", pady=(0, 8))
    disponibles = {p["id"]: p for p in app.registro}
    for pid in _ACCESOS:
        pantalla = disponibles.get(pid)
        if pantalla is None:
            continue
        ctk.CTkButton(caja, text=pantalla["titulo"], anchor="w",
                     command=lambda pid=pid: app.mostrar(pid)
                    ).pack(fill="x", padx=8, pady=(4, 4))
