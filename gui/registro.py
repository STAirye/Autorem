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
gui/registro.py - REGISTRO de pantallas (declarativo) + orden de programas.

Mismo espiritu que TAREA (modulos/), COBERTURA (programas/cobertura.py) y
CATALOGOS (programas/catalogos.py): un registro DECLARATIVO en vez de una
lista a mano que se pudre. Aca el registro se DESCUBRE POR INTROSPECCION de
gui/paginas/*.py -- agregar un modulo con un dict PANTALLA alcanza para que
aparezca en el sidebar, sin tocar este archivo (docs/GUI_2.0_plan.md SS1: el
costo de sumar un modulo a mano es justo lo que esta capa elimina).

Cada PANTALLA (ver gui/app.py para el contrato completo) declara `programa`
(agrupa en el sidebar) e `id` (unico, usado por el router). `ORDEN_PROGRAMAS`
fija el orden de los grupos y `ORDEN_PAGINAS` el de las paginas DENTRO de cada
grupo; lo que no este en esas listas NO revienta -- se agrega al final (fail
soft: el sidebar sigue armandose aunque alguien haya olvidado declarar el
orden, la omision se seguiria notando a simple vista igual). El fail LOUD que
les falta son los tests de tests/test_gui_registro.py.
"""

import importlib
import pkgutil

# Orden de la matriz de programas de salud (CLAUDE.md SS9). Los que todavia no
# tienen ninguna pagina migrada no molestan: un programa sin pantallas
# registradas simplemente no aparece.
ORDEN_PROGRAMAS = (
    "Salud Mental",
    "Respiratorio",
    "Dependencia / Domiciliaria",
    "Cardiovascular",
)

# Orden de las paginas DENTRO de su grupo, por `id` de PANTALLA. Es el orden en que
# las montaba `autorem.lanzar_gui` (A05 -> Actividades -> A23 -> BETA).
#
# POR QUE existe y no alcanza el orden de `pkgutil` (sep-2026): `iter_modules` los
# devuelve por NOMBRE DE ARCHIVO, asi que la posicion en el sidebar quedaba colgando
# de como se llama el .py. Hoy A05 va antes de Actividades solo porque "a05" < "sm";
# renombrar sm.py a actividades.py (el titulo de la pagina ES "Actividades", o sea el
# rename natural) las daba vuelta en silencio, y una pagina nueva de Salud Mental
# entra donde le toque alfabeticamente. Misma clase de bug que la posicion de
# Inicio/Acerca de en el sidebar: la posicion es un DATO, no un efecto del orden en
# que corrio algo.
ORDEN_PAGINAS = (
    "a05",
    "sm_actividades",
    "sp_p6_poblacion",
    "a23_respiratorio",
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
    if not encontradas:
        # Fail loud (CLAUDE.md regla 2): una ventana con el sidebar VACIO parece una
        # herramienta funcionando y sin nada que hacer. El modo de falla real es el
        # .exe: nadie importa gui.paginas.* por nombre, asi que sin el
        # collect_submodules('gui.paginas') de autoREM.spec PyInstaller no las
        # empaqueta y iter_modules() no devuelve NADA.
        raise RuntimeError(
            "gui/paginas/ no expuso ninguna PANTALLA. Corriendo el .py suelto suele ser "
            "un import roto en una pagina; en el .exe, que falte "
            "collect_submodules('gui.paginas') en autoREM.spec.")
    return encontradas


def _orden_programa(programa):
    try:
        return ORDEN_PROGRAMAS.index(programa)
    except ValueError:
        return len(ORDEN_PROGRAMAS)   # desconocido: al final, no revienta


def _orden_pagina(pantalla_id):
    try:
        return ORDEN_PAGINAS.index(pantalla_id)
    except ValueError:
        return len(ORDEN_PAGINAS)     # desconocida: al final de su grupo, no revienta


def cargar_registro():
    """[PANTALLA, ...] ordenadas por programa (ORDEN_PROGRAMAS) y, dentro de
    cada programa, por ORDEN_PAGINAS. Una pagina que no este declarada en
    ORDEN_PAGINAS cae al final de su grupo, y ahi desempata el orden de
    archivo de pkgutil (alfabetico) para que el resultado sea determinista."""
    pantallas = _paginas_encontradas()
    orden_archivo = {id(p): i for i, p in enumerate(pantallas)}
    return sorted(pantallas, key=lambda p: (_orden_programa(p["programa"]),
                                            _orden_pagina(p["id"]),
                                            orden_archivo[id(p)]))


def programas_en_orden(registro):
    """Programas presentes en `registro`, en el orden en que van en el sidebar."""
    vistos = []
    for pantalla in registro:
        if pantalla["programa"] not in vistos:
            vistos.append(pantalla["programa"])
    return sorted(vistos, key=_orden_programa)
