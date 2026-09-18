#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 and Claude Opus 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.9.17
#
# Distributed WITHOUT ANY WARRANTY. GPL-3.0-or-later:
# <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
limpiar_refs.py — deja los EXPORTS de ejemplo de `refs_tablas/` en BANNER + ENCABEZADO.

Privacidad-by-design (CLAUDE.md §8): cualquier export de RAYEN/IRIS que se agregue a
la carpeta de referencia puede traer PII de paciente en sus filas. Este tool ubica el
encabezado y se queda con TODO lo que hay arriba de él (el banner) y con el bloque de
encabezado (una fila, o dos si RAYEN lo parte con celdas combinadas). Lo de abajo, los
datos, no llega al archivo nuevo.

EL BANNER SE CONSERVA (sep-2026). A los usuarios se les pide cargar el export tal cual
sale, sin borrarle el banner, y la herramienta lo salta sola; una referencia sin banner
no es la forma real del export, y los contratos (tests/contratos_fuentes.py) no
probarían el salto. Hasta 1.9.17 varias referencias IRIS llegaron sin banner porque se
las recortó a mano en Excel, y eso escondió que la herramienta asumía «IRIS no trae
banner».

SE ARMA UN LIBRO NUEVO, no se edita el original (sep-2026). Editar el original con
openpyxl y guardarlo conserva lo que no son celdas: la CACHÉ de una tabla dinámica (con
todas las filas de datos), comentarios, propiedades del documento (autor). Y un export
con una imagen rota adentro (pasa con los de RAYEN) ni siquiera abre en modo normal. El
libro nuevo lleva solo los valores del banner y el encabezado, las celdas combinadas de
ese bloque y las hojas con sus nombres (las 2 vacías incluidas: la herramienta revisa
que venga UNA hoja con datos). Lo demás no se copia porque no se lee.

GUARDAS:
  - El resultado se ESCANEA (`scan_catalogo.escanear`: RUT con DV válido, email,
    teléfono). Si queda algo, el archivo NO se escribe. El banner puede traer el
    «GENERADO PARA:» de quien lo bajó: eso es de un funcionario, no lo caza el escáner,
    y se revisa a mano al vetar (skill limpiar-refs).
  - Una hoja con filas pero sin encabezado reconocible NO se toca y se avisa.
  - No imprime valores de celda. Reporta filas antes/después y conteos de hallazgos.

NO toca (denylist): templates/planillas con fórmulas y specs, que SÍ necesitan sus
filas — `.xlsm/.xltx` (SA_26, SP_26), y por nombre: minimanual, REM comentado,
calculador, manual, arsenal, maestro. Todo lo demás (.xlsx export plano) se recorta.

USO:
    python tools/limpiar_refs.py            # DRY-RUN: reporta qué recortaría
    python tools/limpiar_refs.py --aplicar  # aplica el recorte
    python tools/limpiar_refs.py --aplicar archivo1.xlsx archivo2.xlsx  # solo esos
"""

from __future__ import annotations   # `int | None` en las firmas: el Python del proyecto es 3.9

import re
import sys
import zipfile
from pathlib import Path

import openpyxl
from openpyxl.utils.cell import range_boundaries

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

# Windows: consola cp1252 revienta con OK·-> (UnicodeEncodeError en ValueError). Ver §4.5.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

# Carpeta de referencia (relativa a la raíz del repo = padre de tools/).
CARPETA = REPO / "refs_tablas"

# Se conservan intactos (tienen fórmulas/estructura que depende de sus filas).
DENY_EXT = {".xlsm", ".xltx", ".xltm", ".dotx", ".potx"}
# 'maestro' = Maestro de Actividades (catálogo completo RAYEN act<->profesional, 217k
# filas, sin PII de paciente). Es REFERENCIA de por vida -> se mantiene INTACTO.
# 'comparativo' = tabla PSC/PSC-Y/GHQ-12 armada a mano (documento, no export).
DENY_NOMBRE = ("minimanual", "comentado", "calculador", "manual", "arsenal", "maestro",
               "comparativo")

# Fila de header = primera fila con al menos esta cantidad de celdas no vacías.
MIN_CELDAS_HEADER = 5
# Solo se busca el header en las primeras filas (banner/filtros de RAYEN arriba).
MAX_FILAS_SCAN = 50

# Partes del .xlsx que NO son celdas y pueden llevar datos. Un archivo ya recortado
# no debe traer ninguna (el libro nuevo no las genera).
PARTES_SOSPECHOSAS = re.compile(r"pivotCache|pivotTable|/tables/|comments|threadedComments|"
                                r"externalLink|/media/|/drawings/")


def _es_referencia_export(p: Path) -> bool:
    """True si el archivo es un export de datos plano (candidato a recorte)."""
    if p.suffix.lower() not in (".xlsx",):
        return False
    n = p.name.lower()
    return not any(k in n for k in DENY_NOMBRE)


def _fila_header(filas) -> int | None:
    """Primera fila (1-indexada) con >= MIN_CELDAS_HEADER celdas no vacías, entre las
    primeras MAX_FILAS_SCAN. Solo cuenta no-vacíos."""
    for i, fila in enumerate(filas[:MAX_FILAS_SCAN], start=1):
        if sum(1 for v in fila if v not in (None, "")) >= MIN_CELDAS_HEADER:
            return i
    return None


def _combinadas(archivo: Path, ruta_hoja: str) -> list[str]:
    """Rangos combinados de una hoja, leídos del XML (el modo read_only de openpyxl no
    los expone, y el modo normal no abre exports con una imagen rota)."""
    with zipfile.ZipFile(archivo) as z:
        xml = z.read(ruta_hoja.lstrip("/")).decode("utf-8", errors="replace")
    return re.findall(r'<mergeCell ref="([A-Z]+[0-9]+:[A-Z]+[0-9]+)"', xml)


def _fin_bloque(h: int, combinadas: list[str]) -> int:
    """Última fila del bloque de encabezado: la `h`, o más abajo si una celda combinada
    que EMPIEZA en `h` baja (encabezado de dos pisos, p.ej. Utilización de Cupos)."""
    fin = h
    for rng in combinadas:
        _c0, r0, _c1, r1 = range_boundaries(rng)
        if r0 == h:
            fin = max(fin, r1)
    return fin


def _leer(p: Path):
    """[(titulo, filas_de_valores, combinadas)] por hoja. read_only: no abre imágenes
    ni gráficos (un export con una imagen rota adentro no rompe la lectura)."""
    wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
    try:
        hojas = []
        for ws in wb.worksheets:
            ws.reset_dimensions()          # la <dimension> puede venir rota (abrir_xlsx_ro)
            filas = [tuple(f) for f in ws.iter_rows(values_only=True)]
            while filas and not any(v not in (None, "") for v in filas[-1]):
                filas.pop()
            hojas.append((ws.title, filas, _combinadas(p, ws._worksheet_path)))
        return hojas
    finally:
        wb.close()


def _partes_sospechosas(p: Path) -> list[str]:
    with zipfile.ZipFile(p) as z:
        return [n for n in z.namelist() if PARTES_SOSPECHOSAS.search(n)]


def _escribir(destino: Path, hojas) -> None:
    """Libro NUEVO con (titulo, filas, combinadas) por hoja. Via temporal + rename."""
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for titulo, filas, combinadas in hojas:
        ws = wb.create_sheet(titulo)
        for f in filas:
            ws.append(list(f))
        for rng in combinadas:
            ws.merge_cells(rng)
    tmp = destino.with_name(destino.stem + ".limpiando.xlsx")
    wb.save(tmp)
    tmp.replace(destino)


def _hallazgos(p: Path) -> dict[str, int]:
    """Conteo por tipo (RUT/EMAIL/FONO) de lo que el escáner encuentra. Sin valores."""
    from tools.scan_catalogo import escanear
    conteo: dict[str, int] = {}
    for tipo, *_ in escanear(p)[0]:
        conteo[tipo] = conteo.get(tipo, 0) + 1
    return conteo


def recortar(p: Path, aplicar: bool) -> tuple[str, int, int, list[str]]:
    """Deja un .xlsx en banner + encabezado (todas las hojas). Devuelve (estado,
    filas_antes, filas_despues, avisos), SUMADAS sobre las hojas. Sin imprimir valores.
    Estados: 'ya limpio' · 'recortaría' · 'recortado' · 'NO ESCRITO' (hallazgos)."""
    antes = despues = 0
    cambio = False
    avisos: list[str] = []
    nuevas = []
    for titulo, filas, combinadas in _leer(p):
        antes += len(filas)
        h = _fila_header(filas)
        if h is None:                      # hoja sin header reconocible -> no tocar
            # Fail loud: una hoja angosta (menos de MIN_CELDAS_HEADER columnas, p.ej. una
            # lista de RUT en una sola columna) NO se recorta. Callarlo daria un
            # "ya limpio" falso sobre un archivo que sigue con filas de datos.
            if len(filas) > 1:
                avisos.append(
                    f"hoja '{titulo}': {len(filas)} filas SIN recortar "
                    f"(header no reconocible, <{MIN_CELDAS_HEADER} columnas). REVISAR A MANO.")
            nuevas.append((titulo, filas, combinadas))
            despues += len(filas)
            continue
        fin = _fin_bloque(h, combinadas)
        if len(filas) > fin:
            cambio = True
        nuevas.append((titulo, filas[:fin],
                       [r for r in combinadas if range_boundaries(r)[3] <= fin]))
        despues += fin
    extra = _partes_sospechosas(p)
    if extra:
        cambio = True
        avisos.append(f"{len(extra)} parte(s) que no son celdas (tablas, caché de tabla "
                      "dinámica, comentarios, imágenes): no pasan al archivo limpio")
    if any(a.endswith("REVISAR A MANO.") for a in avisos):
        return "NO ESCRITO", antes, despues, avisos
    if not cambio:
        return "ya limpio", antes, despues, avisos
    if not aplicar:
        return "recortaría", antes, despues, avisos
    tmp = p.with_name(p.stem + ".revisando.xlsx")
    _escribir(tmp, nuevas)
    try:
        hall = _hallazgos(tmp)
        if hall:
            avisos.append("el banner/encabezado trae " +
                          ", ".join(f"{n} {t}" for t, n in hall.items()) +
                          " -> NO se escribe. Revísalo a mano (sin copiar el dato a ningún lado).")
            return "NO ESCRITO", antes, despues, avisos
        tmp.replace(p)
    finally:
        tmp.unlink(missing_ok=True)
    return "recortado", antes, despues, avisos


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
        marca = {"ya limpio": "·", "NO ESCRITO": "!!"}.get(estado, "OK")
        print(f"  {marca} {estado}: {p.name}  ({antes} -> {despues} filas)")
        for a in avisos:
            print(f"      AVISO: {a}")
        if estado == "NO ESCRITO":
            revisar += 1
        if estado in ("recortado", "recortaría"):
            tocados += 1
    if revisar:
        print(f"\n!! {revisar} archivo(s) NO se escribieron (ver AVISO arriba).")
    if not aplicar and tocados:
        print(f"\n{tocados} archivo(s) con filas de datos. Corre con --aplicar para recortarlos.")
    return 1 if revisar else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
