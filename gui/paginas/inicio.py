#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Sonnet 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# Copyright (C) 2026 Simon Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 2.0.4
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
     "La informacion sensible de paciente (PII) se procesa en memoria: el programa no guarda copia de ella.\n"
     "Como no hay conexion con internet, no hay actualizacion automatica: se revisa a mano en el link de Acerca de.")
)

_TITULO_VENTAJAS = "¿Qué ventajas tiene sobre el REM automático de RAYEN?"

# Las cinco afirmaciones son VERIFICABLES y hay que mantenerlas asi (regla 2:
# nada plausible pero falso). La de trazabilidad se apoya en que los siete
# modulos dejan el RUT/RUN en la salida: el A05 marca el export completo (la
# columna RUT abre su hoja, ver rem_saludmental.ANCHOS_BASE) y el resto escribe
# su hoja `*_Detalle`. Si algun modulo nuevo NO deja detalle por paciente, esta
# frase deja de ser cierta y hay que corregirla aca y en el README.
_VENTAJAS = (
    ("100% offline: no requiere conexión a internet y ningún dato sale de este computador. "
     "Los exports se leen y las salidas se escriben en tu propio equipo.\n"
     "Trazabilidad: a diferencia de RAYEN, cada reporte deja la lista de los RUT que lo componen, "
     "así que cualquier cifra se puede abrir y revisar caso a caso.\n"
     "Transparencia: programa de código abierto, 100% auditable y revisable por cualquiera.\n"
     "Apoyo a la gestión: genera automáticamente reportes de auditoría para mejorar los flujos de "
     "atención y automatizar tareas recurrentes.\n"
     "Criterios explícitos: los criterios de conteo están revisados y escritos en la documentación, "
     "y la hoja LEEME de cada salida dice qué casillas NO cubre ese módulo.")
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

    # Debajo de los accesos directos A PROPOSITO: esto se lee una vez, y los
    # botones son lo que se usa mes a mes.
    ventajas = widgets.caja_titulada(frame, _TITULO_VENTAJAS)
    ventajas.pack(fill="x", pady=(12, 8))
    widgets.etiqueta_envolvente(ventajas, _VENTAJAS).pack(fill="x", padx=8, pady=(4, 8))
