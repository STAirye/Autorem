#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# Copyright (C) 2026 Simon Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.9.0
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. Distributed WITHOUT ANY WARRANTY. See the GNU
# General Public License for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
scan_catalogo.py - escanea un catalogo ANTES de versionarlo.

POR QUE EXISTE
  El pre-commit anti-RUT (tools/hook_pre_commit_rut.py) SALTA los binarios:
  .xlsx, .xlsm, .gz, .pdf... (su lista BIN). O sea que un `catalogos/*.csv.gz`
  vendorizado NO lo revisa nadie. Este script es ese filtro: se corre a mano
  sobre el archivo fuente y sobre el slim generado, antes del `git add -f`.

QUE BUSCA (y por que)
  - RUT con DV valido       -> reusa hook_pre_commit_rut.sospechosos (fuente
                               unica del modulo 11; si cambia la regla, cambia
                               en un solo lugar).
  - Email                   -> nadie deberia aparecer en un catalogo de codigos.
  - Telefono chileno        -> +569NNNNNNNN / 9NNNNNNNN sueltos.
  Ninguno de estos deberia dar un solo hit en un catalogo publico DEIS. Un hit
  no prueba que haya PII (un "+56 2 2574 xxxx" de mesa central es inocuo), pero
  obliga a mirar antes de convertir el archivo en un .gz opaco.

QUE NO HACE
  Detectar nombres de persona. Es ruido puro en un catalogo lleno de
  epinimos ("Enfermedad de Creutzfeldt-Jakob", "Lista de Becker"). Para eso
  esta el volcado de estructura: headers + muestra de valores por columna,
  para mirarlo con los ojos una vez.

USO
    python tools/scan_catalogo.py refs_tablas/DEIS_CIE10_lista_tabular_2026-08.xlsx
    python tools/scan_catalogo.py catalogos/*.csv.gz --muestra 5

Codigo de salida: 0 limpio, 1 con hallazgos (sirve para encadenarlo).
"""

import gzip
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from tools.hook_pre_commit_rut import sospechosos          # noqa: E402

EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]{2,}\b")
FONO = re.compile(r"(?:\+?56[\s-]?)?9[\s-]?\d{4}[\s-]?\d{4}\b")

MUESTRA_DEFECTO = 3
MAX_LARGO = 70


def _celdas_xlsx(ruta):
    """[(hoja, fila, col, texto)] de todas las celdas no vacias de un .xlsx/.xlsm."""
    import openpyxl
    wb = openpyxl.load_workbook(ruta, read_only=True, data_only=True)
    try:
        for ws in wb.worksheets:
            for i, fila in enumerate(ws.iter_rows(values_only=True), start=1):
                for j, v in enumerate(fila, start=1):
                    if v is not None and str(v).strip():
                        yield ws.title, i, j, str(v)
    finally:
        wb.close()


def _celdas_texto(ruta):
    """Idem para .csv / .csv.gz (una 'hoja' unica, split crudo por coma)."""
    op = gzip.open if str(ruta).lower().endswith(".gz") else open
    with op(ruta, "rt", encoding="utf-8", errors="replace") as fh:
        for i, linea in enumerate(fh, start=1):
            for j, v in enumerate(linea.rstrip("\n").split(","), start=1):
                if v.strip():
                    yield "(csv)", i, j, v


def celdas(ruta):
    lower = str(ruta).lower()
    return _celdas_xlsx(ruta) if lower.endswith((".xlsx", ".xlsm")) else _celdas_texto(ruta)


def escanear(ruta, muestra=MUESTRA_DEFECTO):
    """Devuelve (hallazgos, estructura). hallazgos = [(tipo, hoja, fila, col, dato)]."""
    hallazgos = []
    # estructura: {hoja: {col: [primeros valores distintos]}}
    estructura, vistos, filas = {}, {}, {}
    for hoja, i, j, txt in celdas(ruta):
        filas[hoja] = i
        for rut in sospechosos(txt):
            hallazgos.append(("RUT", hoja, i, j, rut))
        for m in EMAIL.findall(txt):
            hallazgos.append(("EMAIL", hoja, i, j, m))
        for m in FONO.findall(txt):
            hallazgos.append(("FONO", hoja, i, j, m.strip()))
        col = estructura.setdefault(hoja, {}).setdefault(j, [])
        clave = (hoja, j)
        if len(col) < muestra and txt not in vistos.setdefault(clave, set()):
            vistos[clave].add(txt)
            col.append(txt)
    return hallazgos, estructura, filas


def informe(ruta, muestra=MUESTRA_DEFECTO):
    hallazgos, estructura, filas = escanear(ruta, muestra)
    print("=" * 72)
    kb = Path(ruta).stat().st_size / 1024
    print(f"{Path(ruta).name}   ({kb:,.1f} KB)")
    print("=" * 72)
    for hoja, cols in estructura.items():
        print(f"\n  hoja {hoja!r}  -  {filas.get(hoja, 0)} filas, {len(cols)} columnas con datos")
        for j in sorted(cols):
            vals = " | ".join(v[:MAX_LARGO] for v in cols[j])
            print(f"    col {j:>3}: {vals}")
    if hallazgos:
        print(f"\n  !! {len(hallazgos)} HALLAZGO(S) - revisar antes de versionar:")
        for tipo, hoja, i, j, dato in hallazgos[:40]:
            print(f"    [{tipo}] {hoja} fila {i} col {j}: {dato}")
        if len(hallazgos) > 40:
            print(f"    ... y {len(hallazgos) - 40} mas")
    else:
        print("\n  OK sin RUT validos, ni emails, ni telefonos.")
    return len(hallazgos)


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    muestra = MUESTRA_DEFECTO
    if "--muestra" in argv:
        k = argv.index("--muestra")
        muestra = int(argv[k + 1])
        argv = argv[:k] + argv[k + 2:]
    if not argv:
        print(__doc__)
        return 2
    total = 0
    for ruta in argv:
        p = Path(ruta)
        if not p.exists():
            print(f"X no existe: {p}")
            total += 1
            continue
        total += informe(p, muestra)
    print()
    print("LIMPIO: se puede versionar." if total == 0
          else f"{total} hallazgo(s): NO versionar hasta revisarlos.")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
