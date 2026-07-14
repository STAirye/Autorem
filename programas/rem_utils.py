#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.3.1
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
rem_utils.py — utilidades comunes para los módulos del REM (RAYEN/IRIS).

Base compartida por todas las herramientas del proyecto autoREM. NO contiene
lógica de ninguna sección específica del REM; cada módulo de tarea
(modulos/rem_<pestaña>_<casilla>_<descriptor>.py) importa de aquí.

Contenido:
  - Guarda de dependencia (openpyxl) y excepción común (ArchivoInvalido).
  - Normalización y parsing de celdas: norm, to_year, solo_entero.
  - Búsqueda de columnas y numeración de preguntas RAYEN: buscar_col, num_pregunta.
  - Localización de la fila de encabezado (salta banner + filtros): encontrar_fila_encabezado.
  - Utilidad de SO: abrir_carpeta.
"""

import re
import sys
from pathlib import Path   # reexport de conveniencia para los módulos

# ── Versión del proyecto (fuente única de verdad) ──
# Convención X.Y.Z (ver CLAUDE.md §9):
#   X = programa · Y = módulos de programa acumulados · Z = corrección del módulo actual.
# Todos los .py comparten esta versión en su header; bumpear aquí al cambiarla.
VERSION = "1.3.1"

# openpyxl es la única dependencia externa real. En el .exe va empaquetado;
# corriendo como .py suelto puede faltar -> los módulos avisan con instrucciones.
try:
    import openpyxl
    OPENPYXL_OK = True
    OPENPYXL_ERR = ""
except ImportError as _e:
    openpyxl = None
    OPENPYXL_OK = False
    OPENPYXL_ERR = str(_e)


class ArchivoInvalido(Exception):
    """El archivo no es el export que el módulo esperaba.

    `categoria` la define cada módulo según sus propios formatos (por ejemplo,
    el A05 usa 'administrativo' | 'desconocido'). El mensaje es para el usuario.
    """
    def __init__(self, categoria, mensaje):
        self.categoria = categoria
        super().__init__(mensaje)


# ── Normalización y parsing de celdas ─────────────────────────────────
def norm(v):
    """Texto en MAYÚSCULA, sin tildes/ñ, con espacios colapsados. '' si es None."""
    if v is None: return ""
    s = str(v).upper().strip()
    for a, b in zip("ÁÉÍÓÚÜÑ", "AEIOUUN"): s = s.replace(a, b)
    return re.sub(r"\s+", " ", s)


def to_year(v):
    """Primeros 4 dígitos de la celda como int (año). None si no hay dígitos."""
    if v is None: return None
    d = re.sub(r"\D", "", str(v))
    return int(d[:4]) if d else None


def solo_entero(v):
    """Primer entero que aparezca en la celda. None si no hay ninguno."""
    if v is None: return None
    m = re.search(r"\d+", str(v))
    return int(m.group()) if m else None


def edad_anios(v):
    """Edad en AÑOS (int) desde la celda. RAYEN a veces la trae pelada (IRIS:
    'AÑO APLICACIÓN FORMULARIO' = número) y a veces como texto (Administrativo:
    '99 años 12 meses 31 días'). Menor de 1 año (solo meses/días) -> 0. None si
    no hay dato. Genérica: sirve a cualquier export RAYEN."""
    if v is None:
        return None
    n = norm(v)                       # '99 ANOS 12 MESES 31 DIAS'
    m = re.search(r"(\d+)\s*ANOS?", n)
    if m:
        return int(m.group(1))
    if "MES" in n or "DIA" in n:      # menor de 1 año expresado en meses/días
        return 0
    return solo_entero(v)


# ── Búsqueda de columnas / numeración de preguntas RAYEN ──────────────
def buscar_col(headers_norm, tokens=None, exacto=None):
    """Índice 1-based de la 1ª columna cuyo header (ya normalizado) contiene
    TODOS los `tokens`, o coincide exactamente con `exacto`. None si no hay."""
    for i, h in enumerate(headers_norm, 1):
        if exacto is not None and h == norm(exacto): return i
        if tokens and all(t in h for t in tokens): return i
    return None


def num_pregunta(header):
    """Número 'N.-' con que RAYEN antepone cada pregunta ('18.- ¿...?' -> 18)."""
    m = re.match(r"\s*(\d+)\s*\.\-", str(header))
    return int(m.group(1)) if m else None


# ── Localización de la fila de encabezado (banner + filtros arriba) ────
def encontrar_fila_encabezado(ws, ancla, usar_blanco_en_a=True,
                              n_hardcode=16, max_filas=60):
    """Ubica la fila del encabezado real saltando el banner y los filtros que
    RAYEN pone arriba. Cascada de detección:
      1. Fila que contiene TODOS los tokens de `ancla` (match por substring).
      2. Si `usar_blanco_en_a`: la fila siguiente a la 1ª con la columna A vacía.
      3. Fallback: `n_hardcode` (+1).
    Devuelve (fila_encabezado_1based, modo)."""
    tope = min(ws.max_row, max_filas)
    ancla_n = [norm(t) for t in ancla]
    for r in range(1, tope + 1):
        vals = [norm(c.value) for c in ws[r]]
        if all(any(tok in v for v in vals) for tok in ancla_n):
            return r, "ancla"
    if usar_blanco_en_a:
        for r in range(1, tope + 1):
            if norm(ws.cell(row=r, column=1).value) == "":
                return r + 1, "blanco_en_A"
    return n_hardcode + 1, "hardcode"


# ── Utilidad de SO ────────────────────────────────────────────────────
def abrir_carpeta(carpeta: Path):
    """Abre el explorador de archivos en `carpeta` (Windows / macOS / Linux)."""
    import subprocess
    try:
        if sys.platform.startswith("win"):
            import os
            os.startfile(str(carpeta))   # noqa
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(carpeta)])
        else:
            subprocess.Popen(["xdg-open", str(carpeta)])
    except Exception:
        pass
