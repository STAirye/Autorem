#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Sonnet 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# Copyright (C) 2026 Simon Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.8.2
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. Distributed WITHOUT ANY WARRANTY. See the GNU
# General Public License for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
check_cp1252.py - verifica que el codigo .py del repo sea seguro para cp1252.

POR QUE
  La consola de Windows sin el wrapper UTF-8 (ver CLAUDE.md #4.5/#13) usa
  cp1252. Un simbolo decorativo (flecha, caja, check, emoji) en un log o un
  comentario revienta el modulo con UnicodeEncodeError en la primera linea
  que lo imprime -- y ese error hereda de ValueError, asi que se disfraza de
  otra cosa. Ya paso una vez (sep-2026: 19 caracteres distintos en 20 .py).

  El texto en espanol con tildes/enie SI es seguro (esta en cp1252). Lo que
  se busca son los simbolos de fuera de esa tabla: flechas Unicode, cajas de
  comentario (box-drawing), checks/emoji, simbolos matematicos.

USO
    python tools/check_cp1252.py                  # repo completo, dry-run
    python tools/check_cp1252.py modulos/x.py      # un archivo/carpeta puntual
    python tools/check_cp1252.py --fix             # corrige los simbolos CONOCIDOS
                                                    # (ver REEMPLAZOS) y reporta el resto

Exit code 0 = limpio, 1 = quedan caracteres por revisar (util en pre-commit/CI).
"""

import sys
import unicodedata
from pathlib import Path

# Este script IMPRIME los simbolos problematicos que encuentra (para
# diagnosticarlos), asi que su propia salida necesita el wrapper UTF-8 -- si
# no, revienta con el mismo UnicodeEncodeError que esta buscando. Ver #4.5.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

RAIZ = Path(__file__).resolve().parent.parent

EXCLUIR_DIRS = {".git", "__pycache__", ".pytest_cache", "build", "dist",
                "venv", ".venv", ".mypy_cache"}

# Simbolo problematico -> reemplazo ASCII (mismo criterio que la lista
# "Usar ASCII" de la memoria 'solo-ascii-en-el-codigo'). Solo se auto-corrigen
# los que tienen un reemplazo inequivoco; el resto (emoji, simbolos raros)
# se reporta para arreglar a mano.
#
# Escritos como \uXXXX (no como el glifo literal): asi este mismo archivo
# se mantiene cp1252-limpio y no se auto-reporta al correr el checker sobre
# el repo completo.
REEMPLAZOS = {
    "\u2192": "->",   # flecha derecha
    "\u2190": "<-",   # flecha izquierda
    "\u2194": "<->",  # flecha doble
    "\u21D2": "->",   # flecha doble (implica)
    "\u2265": ">=",
    "\u2264": "<=",
    "\u2260": "!=",
    "\u2714": "OK",   # check pesado
    "\u2713": "OK",   # check
    "\u2718": "X",    # cruz pesada
    "\u2717": "X",    # cruz
    "\u25B6": ">",    # triangulo/play
    "\u26A0": "!",    # warning
    "\u2550": "=", "\u2500": "-", "\u2502": "|", "\u2551": "|",
    "\u2554": "+", "\u2557": "+", "\u255A": "+", "\u255D": "+",
    "\u2560": "+", "\u2563": "+", "\u2566": "+", "\u2569": "+", "\u256C": "+",
    "\u250C": "+", "\u2510": "+", "\u2514": "+", "\u2518": "+",
    "\u256D": "+", "\u256E": "+", "\u2570": "+", "\u256F": "+",
}


def nombre_char(ch):
    try:
        return unicodedata.name(ch)
    except ValueError:
        return f"U+{ord(ch):04X}"


def problemas_en(texto):
    """[(linea, col, char)] para cada caracter que no se puede codificar en cp1252."""
    hallazgos = []
    linea, col = 1, 1
    for ch in texto:
        try:
            ch.encode("cp1252")
        except UnicodeEncodeError:
            hallazgos.append((linea, col, ch))
        if ch == "\n":
            linea += 1
            col = 1
        else:
            col += 1
    return hallazgos


def archivos_py(objetivo):
    if objetivo.is_file():
        return [objetivo]
    return sorted(
        p for p in objetivo.rglob("*.py")
        if not EXCLUIR_DIRS & set(p.relative_to(RAIZ).parts)
    )


def arreglar(ruta):
    """Aplica REEMPLAZOS conocidos. Devuelve True si modifico el archivo."""
    texto = ruta.read_text(encoding="utf-8")
    nuevo = texto
    for malo, bueno in REEMPLAZOS.items():
        nuevo = nuevo.replace(malo, bueno)
    if nuevo != texto:
        ruta.write_text(nuevo, encoding="utf-8")
        return True
    return False


def main():
    argv = sys.argv[1:]
    fix = "--fix" in argv
    rutas = [a for a in argv if not a.startswith("--")]

    objetivo = Path(rutas[0]) if rutas else RAIZ
    if not objetivo.is_absolute():
        objetivo = RAIZ / objetivo
    if not objetivo.exists():
        print(f"No existe: {objetivo}", file=sys.stderr)
        return 2

    archivos = archivos_py(objetivo)

    if fix:
        arreglados = [f for f in archivos if arreglar(f)]
        if arreglados:
            print(f"[fix] corregidos automaticamente ({len(arreglados)}):")
            for f in arreglados:
                print(f"    {f.relative_to(RAIZ)}")
            print()

    con_problemas = {}
    for f in archivos:
        texto = f.read_text(encoding="utf-8", errors="replace")
        hallazgos = problemas_en(texto)
        if hallazgos:
            con_problemas[f] = hallazgos

    if not con_problemas:
        print(f"[cp1252] OK - {len(archivos)} archivo(s) .py revisados, sin problemas")
        return 0

    print("=" * 70)
    print("Caracteres que NO son seguros en cp1252 (consola Windows sin wrapper UTF-8)")
    print("=" * 70)
    for f, hallazgos in con_problemas.items():
        print(f"\n  {f.relative_to(RAIZ)}  ({len(hallazgos)} caracter(es))")
        for linea, col, ch in hallazgos[:20]:
            print(f"      linea {linea}, col {col}: {ch!r} ({nombre_char(ch)})")
        if len(hallazgos) > 20:
            print(f"      ... y {len(hallazgos) - 20} mas")

    print(f"\nTotal: {len(con_problemas)} archivo(s) con problemas.")
    print("Correr con --fix corrige flechas/cajas/checks conocidos; lo que quede")
    print("(emoji, simbolos raros) se corrige a mano. Ver CLAUDE.md #13.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
