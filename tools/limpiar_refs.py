#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.8.4
#
# Distributed WITHOUT ANY WARRANTY. GPL-3.0-or-later:
# <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
limpiar_refs.py — recorta los EXPORTS de ejemplo de `refs tablas/` a SOLO EL HEADER.

Privacidad-by-design (CLAUDE.md §8): cualquier export de RAYEN/IRIS que se agregue a
la carpeta de referencia puede traer PII de paciente en sus filas. Este tool ubica la
fila de encabezado y **borra todo lo que hay debajo**, dejando solo la estructura
(columnas). Así el repo nunca ve valores de paciente aunque uno olvide anonimizar.

GARANTÍA: NO lee ni imprime valores de celda. Solo cuenta celdas no vacías para
localizar el header y reporta nº de filas antes/después. Nadie (ni humano ni modelo)
ve el dato.

Al recortar también se eliminan los ListObject (tablas de Excel) de la hoja: su `ref`
abarca el rango de datos completo y, si queda apuntando a filas que ya no existen,
Excel abre el archivo con "contenido ilegible" y lo repara. Los encabezados viven en
las celdas, no en el ListObject, así que no se pierde nada de la estructura.

NO toca (denylist): templates/planillas con fórmulas y specs, que SÍ necesitan sus
filas — `.xlsm/.xltx` (SA_26, SP_26), y por nombre: minimanual, REM comentado,
calculador, manual, arsenal. Todo lo demás (.xlsx export plano) se recorta.

USO:
    python tools/limpiar_refs.py            # DRY-RUN: reporta qué recortaría
    python tools/limpiar_refs.py --aplicar  # aplica el recorte
    python tools/limpiar_refs.py --aplicar archivo1.xlsx archivo2.xlsx  # solo esos
"""

import sys
from pathlib import Path

import openpyxl

# Windows: consola cp1252 revienta con OK·-> (UnicodeEncodeError en ValueError). Ver §4.5.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

# Carpeta de referencia (relativa a la raíz del repo = padre de tools/).
CARPETA = Path(__file__).resolve().parent.parent / "refs tablas"

# Se conservan intactos (tienen fórmulas/estructura que depende de sus filas).
DENY_EXT = {".xlsm", ".xltx", ".xltm", ".dotx", ".potx"}
# 'maestro' = Maestro de Actividades (catálogo completo RAYEN act<->profesional, 217k
# filas, sin PII de paciente). Es REFERENCIA de por vida -> se mantiene INTACTO.
DENY_NOMBRE = ("minimanual", "comentado", "calculador", "manual", "arsenal", "maestro")

# Fila de header = primera fila con al menos esta cantidad de celdas no vacías.
MIN_CELDAS_HEADER = 5
# Solo se busca el header en las primeras filas (banner/filtros de RAYEN arriba).
MAX_FILAS_SCAN = 50

# Sobre esta cantidad de filas a borrar, delete_rows() sale carísimo: mueve celda por
# celda (55k filas x 92 columnas = ~5M movimientos, minutos). Arriba del umbral se
# truncan las celdas de una, que es lo unico que hace falta (no queda nada debajo que
# haya que desplazar hacia arriba).
UMBRAL_TRUNCADO = 500


def _es_referencia_export(p: Path) -> bool:
    """True si el archivo es un export de datos plano (candidato a recorte)."""
    if p.suffix.lower() not in (".xlsx",):
        return False
    n = p.name.lower()
    if p.suffix.lower() in DENY_EXT:
        return False
    return not any(k in n for k in DENY_NOMBRE)


def _fila_header(ws) -> int | None:
    """Primera fila (1-indexada) con >= MIN_CELDAS_HEADER celdas no vacías. NO
    devuelve ni mira los valores: solo cuenta no-vacíos.

    Recorre `_cells` en vez de iter_rows() a proposito: iter_rows(max_row=50)
    MATERIALIZA el rectangulo que escanea, o sea inflaba a 50 filas cada hoja vacia
    del libro (y las dejaba asi al guardar). Escanear no debe escribir."""
    celdas = getattr(ws, "_cells", None)
    if celdas is None:                     # openpyxl distinto -> acotado a lo que existe
        tope = min(MAX_FILAS_SCAN, ws.max_row)
        for i, row in enumerate(ws.iter_rows(min_row=1, max_row=tope), start=1):
            if sum(1 for c in row if c.value not in (None, "")) >= MIN_CELDAS_HEADER:
                return i
        return None
    conteo: dict[int, int] = {}
    for (fila, _), c in celdas.items():
        if fila <= MAX_FILAS_SCAN and c.value not in (None, ""):
            conteo[fila] = conteo.get(fila, 0) + 1
    for fila in sorted(conteo):
        if conteo[fila] >= MIN_CELDAS_HEADER:
            return fila
    return None


def _truncar(ws, h: int) -> None:
    """Borra toda celda por debajo de la fila `h`, sin el costo de delete_rows(). Sirve
    solo para truncar la cola de la hoja (no desplaza nada). Toca la API privada
    `_cells`; si openpyxl la cambia, cae al delete_rows() publico."""
    celdas = getattr(ws, "_cells", None)
    if celdas is None:                     # openpyxl distinto -> camino lento pero publico
        ws.delete_rows(h + 1, ws.max_row - h)
        return
    for coord in [c for c in celdas if c[0] > h]:
        del celdas[coord]
    for fila in [f for f in ws.row_dimensions if f > h]:
        del ws.row_dimensions[fila]
    ws._current_row = h


def _limpiar_estructuras(ws, h: int) -> None:
    """Saca lo que queda apuntando al rango de datos ya borrado. Un ListObject con
    ref='A1:CN55002' sobre una hoja de 1 fila hace que Excel 'repare' el archivo."""
    for nombre in list(ws.tables):
        del ws.tables[nombre]
    if ws.auto_filter is not None and ws.auto_filter.ref:
        ws.auto_filter.ref = None


def recortar(p: Path, aplicar: bool) -> tuple[str, int, int, list[str]]:
    """Recorta un .xlsx a header-only (todas las hojas). Devuelve (estado, filas_antes,
    filas_despues, avisos) SUMADAS sobre las hojas. Sin leer valores."""
    wb = openpyxl.load_workbook(p)
    antes = despues = 0
    cambio = False
    avisos: list[str] = []
    for ws in wb.worksheets:
        h = _fila_header(ws)
        antes += ws.max_row
        if h is None:                      # hoja sin header reconocible -> no tocar
            # Fail loud: una hoja angosta (menos de MIN_CELDAS_HEADER columnas, p.ej. una
            # lista de RUT en una sola columna) NO se recorta. Callarlo daria un
            # "ya limpio" falso sobre un archivo que sigue con filas de datos.
            if ws.max_row > 1:
                avisos.append(
                    f"hoja '{ws.title}': {ws.max_row} filas SIN recortar "
                    f"(header no reconocible, <{MIN_CELDAS_HEADER} columnas). REVISAR A MANO."
                )
            despues += ws.max_row
            continue
        if ws.max_row > h:
            if aplicar:
                if ws.max_row - h > UMBRAL_TRUNCADO:
                    _truncar(ws, h)
                else:
                    ws.delete_rows(h + 1, ws.max_row - h)
                _limpiar_estructuras(ws, h)
            cambio = True
        despues += h
    if aplicar and cambio:
        wb.save(p)
    wb.close()
    estado = "recortado" if (cambio and aplicar) else ("recortaría" if cambio else "ya limpio")
    return estado, antes, despues, avisos


def main(argv):
    aplicar = "--aplicar" in argv
    nombrados = [a for a in argv if not a.startswith("--")]
    if nombrados:
        objetivos = [Path(a) if Path(a).is_absolute() else CARPETA / a for a in nombrados]
    else:
        objetivos = sorted(CARPETA.glob("*.xlsx"))

    print(f"{'APLICANDO' if aplicar else 'DRY-RUN'} · carpeta: {CARPETA}")
    tocados = revisar = 0
    for p in objetivos:
        if not p.exists():
            print(f"  X no existe: {p.name}")
            continue
        if not _es_referencia_export(p):
            print(f"  — omitido (denylist/no-export): {p.name}")
            continue
        estado, antes, despues, avisos = recortar(p, aplicar)
        marca = "·" if estado == "ya limpio" else "OK"
        print(f"  {marca} {estado}: {p.name}  ({antes} -> {despues} filas)")
        for a in avisos:
            print(f"      AVISO: {a}")
        revisar += len(avisos)
        if estado in ("recortado", "recortaría"):
            tocados += 1
    if revisar:
        print(f"\n!! {revisar} hoja(s) quedaron SIN recortar (ver AVISO arriba).")
    if not aplicar and tocados:
        print(f"\n{tocados} archivo(s) con filas de datos. Corré con --aplicar para recortarlos.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
