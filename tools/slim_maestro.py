#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.8.2
#
# Distributed WITHOUT ANY WARRANTY. GPL-3.0-or-later:
# <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
slim_maestro.py — genera el Maestro de Actividades SLIM (versionado) desde el completo.

El 'Maestro de Actividades' completo (.xlsx, ~7.7 MB, 218k filas × 11 col) es catálogo
de por vida pero pesa demasiado para el repo. Este script lo recorta a lo que usa la
herramienta —ACTIVIDAD · INSTRUMENTO ASOCIADO · NUM REM · NUM SECCION · REM (sin las 6
flags booleanas)— y lo guarda comprimido en `refs tablas/maestro_slim.csv.gz` (~1.2 MB,
whitelisteado en .gitignore). NO contiene PII de paciente (solo actividades, estamentos
y su clasificación REM).

Flujo: el Maestro completo vive LOCAL (gitignored). Cuando MINSAL/RAYEN lo actualice
(~semestral), reemplázalo y re-corre este script para regenerar el slim versionado.

USO:
    python tools/slim_maestro.py                       # usa el .xlsx completo de refs/
    python tools/slim_maestro.py "ruta/al/Maestro.xlsx"
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from programas.rem_utils import cargar_maestro   # noqa: E402

CARPETA = REPO / "refs tablas"
FULL_DEFAULT = CARPETA / "Maestro_de_Actividades.xlsx"
SLIM = CARPETA / "maestro_slim.csv.gz"

# Columnas canónicas -> nombre de salida (mismos headers que el completo, para que
# cargar_maestro los resuelva igual).
_SALIDA = [("ACT", "ACTIVIDAD"), ("INSTR", "INSTRUMENTO ASOCIADO"),
           ("NUMREM", "NUM REM"), ("SECCION", "NUM SECCION"), ("REM", "REM")]


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    full = Path(argv[0]) if argv else FULL_DEFAULT
    if not full.exists():
        print(f"✗ No encuentro el Maestro completo: {full}")
        print("  Deja 'Maestro_de_Actividades.xlsx' en 'refs tablas/' o pásalo como argumento.")
        return 1
    print(f"Leyendo Maestro completo: {full.name}")
    dfm = cargar_maestro(full)
    slim = dfm[[c for c, _ in _SALIDA]].drop_duplicates().copy()
    slim.columns = [nombre for _, nombre in _SALIDA]
    slim.to_csv(SLIM, index=False, compression="gzip")
    mb = SLIM.stat().st_size / 1e6
    print(f"✔ Slim escrito: {SLIM.relative_to(REPO)}  ({len(slim)} filas, {mb:.2f} MB)")
    print("  Versionar:  git add -f \"refs tablas/maestro_slim.csv.gz\"")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
