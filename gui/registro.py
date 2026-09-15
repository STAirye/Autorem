#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Sonnet 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# Copyright (C) 2026 Simon Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.9.10
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. Distributed WITHOUT ANY WARRANTY. See the GNU
# General Public License for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
gui/registro.py - REGISTRO de pantallas (declarativo) + orden de programas.

Mismo espiritu que TAREA (modulos/), COBERTURA (programas/cobertura.py) y
CATALOGOS (programas/catalogos.py): un registro DECLARATIVO en vez de una
lista a mano que se pudre. Aca el registro se DESCUBRE POR INTROSPECCION de
gui/paginas/*.py -- agregar un modulo con un dict PANTALLA alcanza para que
aparezca en el sidebar, sin tocar este archivo (docs/GUI_2.0_plan.md SS1: el
costo de sumar un modulo a mano es justo lo que esta capa elimina).

Cada PANTALLA (ver gui/app.py para el contrato completo) declara `programa`
(agrupa en el sidebar) e `id` (unico, usado por el router). `ORDEN_PROGRAMAS`
fija el orden de los grupos; un programa nuevo que no esta en la lista NO
revienta -- se agrega al final (fail soft: el sidebar sigue armandose aunque
alguien haya olvidado declarar el orden, la omision se seguiria notando a
simple vista igual).
"""

import importlib
import pkgutil

# Orden de la matriz de programas de salud (CLAUDE.md SS9). Los que todavia no
# tienen ninguna pagina migrada no molestan: un programa sin pantallas
# registradas simplemente no aparece.
ORDEN_PROGRAMAS = (
    "Salud Mental",
    "Salud Mental — Población",
    "Respiratorio",
    "Dependencia / Domiciliaria",
    "Cardiovascular",
)


def _paginas_encontradas():
    """Importa cada modulo de gui/paginas/*.py (menos los que empiezan con
    '_', p.ej. un spike descartable) y devuelve los PANTALLA que expone cada
    uno, en el orden de archivo (alfabetico, via pkgutil)."""
    from gui import paginas
    encontradas = []
    for info in pkgutil.iter_modules(paginas.__path__):
        if info.name.startswith("_"):
            continue
        mod = importlib.import_module(f"gui.paginas.{info.name}")
        pantalla = getattr(mod, "PANTALLA", None)
        if pantalla is not None:
            encontradas.append(pantalla)
    return encontradas


def _orden_programa(programa):
    try:
        return ORDEN_PROGRAMAS.index(programa)
    except ValueError:
        return len(ORDEN_PROGRAMAS)   # desconocido: al final, no revienta


def cargar_registro():
    """[PANTALLA, ...] ordenadas por programa (ORDEN_PROGRAMAS) y, dentro de
    cada programa, por el orden en que pkgutil encontro el archivo."""
    pantallas = _paginas_encontradas()
    orden_archivo = {id(p): i for i, p in enumerate(pantallas)}
    return sorted(pantallas, key=lambda p: (_orden_programa(p["programa"]), orden_archivo[id(p)]))


def programas_en_orden(registro):
    """Programas presentes en `registro`, en el orden en que van en el sidebar."""
    vistos = []
    for pantalla in registro:
        if pantalla["programa"] not in vistos:
            vistos.append(pantalla["programa"])
    return sorted(vistos, key=_orden_programa)
