#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 5 (Anthropic).
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
check_fuentes.py - pre-commit: los lectores de planillas externas tienen CONTRATO.

POR QUE (revision gui-2.0, sep-2026): el bug recurrente de c38a8cc -- un export que
pasa el loader con 0 filas, o que queda vacio TRAS un filtro, o una columna leida por
POSICION -- aparecio en 10 rondas de revision, siempre DESPUES de escrito. Este hook
lo corre al commitear, sobre lo que el commit toca:

  1. Funciones tocadas = las que el diff STAGED cambia (por rango de lineas).
  2. Un LECTOR (llama directo a leer_xlsx / cargar_canonico / load_workbook /
     abrir_xlsx_ro / read_excel / read_csv / primeras_filas / filas_hoja) tocado y
     SIN contrato en tests/contratos_fuentes.py -> BLOQUEA. Se arregla con la skill
     `tests-fuentes`: escribir su contrato (o exentarlo aca, con motivo).
  3. Corre SOLO los contratos cuyas funciones (`cubre`) toco el commit, o cuya
     referencia de refs_tablas/ cambio. Tocar una primitiva compartida (TRANSVERSALES)
     o el propio registro corre todos.

No revisa todo en cada commit a proposito: lo que no se toca ya paso cuando se toco.
El barrido completo es a pedido: `--todo` (y la suite, tests/test_contratos_fuentes.py).
Corre contra el ARBOL de trabajo (como check_version), no contra el index.

USO
    python tools/check_fuentes.py            # modo pre-commit (lo staged)
    python tools/check_fuentes.py --todo     # todos los contratos + lectores sin contrato
    python tools/check_fuentes.py --instalar # encadena al pre-commit (tools/hooks_git.py)
"""

import ast
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CARPETAS = ("programas", "modulos", "gui")
LECTORES = {"cargar_canonico", "leer_xlsx", "load_workbook", "abrir_xlsx_ro", "read_excel",
            "read_csv", "primeras_filas", "filas_hoja", "filas_xlsx"}
# Primitivas compartidas por TODOS los lectores: tocar una corre todos los contratos.
TRANSVERSALES = {f"programas/rem_utils.py::{f}" for f in (
    "abrir_xlsx_ro", "filas_hoja", "filas_xlsx", "leer_xlsx", "primeras_filas",
    "verificar_hoja_unica", "indice_encabezado", "encabezado_por_columnas",
    "cargar_canonico", "_una_fila_por_atencion", "exigir_filas", "exigir_filas_ws",
    "resolver_columnas", "fecha_col", "filtrar_mes")}
# Lectores que NO leen un export del usuario, con su motivo (no llevan contrato).
EXENTOS = {
    "programas/catalogos.py::_hojas": "catalogos DEIS versionados en el repo (test_catalogos)",
    "programas/catalogos.py::cargar": "catalogos DEIS versionados en el repo (test_catalogos)",
    "gui/paginas/a05.py::bloque_archivo_formato": "solo detecta el formato para el acuse",
    "gui/paginas/a05.py::_leer_categoria": "solo detecta el formato para el acuse",
    "gui/paginas/sm.py::_header_rapido": "preview del cruce ADA/grupal, solo encabezado",
}


def _git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, cwd=RAIZ,
                          encoding="utf-8", errors="ignore").stdout


def _funciones(src):
    """[(nombre, ini, fin, es_lector)] de un fuente (incluye metodos y anidadas)."""
    out = []
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            llamadas = {getattr(c.func, "attr", getattr(c.func, "id", None))
                        for c in ast.walk(n) if isinstance(c, ast.Call)}
            out.append((n.name, n.lineno, n.end_lineno, bool(llamadas & LECTORES)))
    return out


def _lineas_nuevas(rel):
    """Lineas (del lado staged) que el diff agrega o cambia; None = archivo nuevo."""
    diff = _git("diff", "--cached", "-U0", "--", rel)
    if re.search(r"^new file mode", diff, re.M):
        return None
    lineas = set()
    for m in re.finditer(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", diff, re.M):
        ini, n = int(m.group(1)), int(m.group(2) or 1)
        lineas.update(range(ini, ini + max(n, 1)))   # n=0 (solo borra): marca el punto
    return lineas


def staged():
    return [p for p in _git("diff", "--cached", "--name-only",
                            "--diff-filter=ACMR").splitlines() if p]


def tocadas(rutas):
    """({'ruta::funcion' tocadas}, {las que son LECTORES})."""
    todas, lectores = set(), set()
    for rel in rutas:
        if not (rel.endswith(".py") and rel.split("/")[0] in CARPETAS):
            continue
        src = _git("show", f":{rel}")
        try:
            funcs = _funciones(src)
        except SyntaxError:
            continue   # que lo diga el que corresponda; aca no hay nada que medir
        nuevas = _lineas_nuevas(rel)
        for nombre, ini, fin, lector in funcs:
            if nuevas is None or any(ini <= l <= fin for l in nuevas):
                clave = f"{rel}::{nombre}"
                todas.add(clave)
                if lector:
                    lectores.add(clave)
    return todas, lectores


def inventario():
    """{'ruta::funcion'} de TODOS los lectores del arbol (para --todo y la suite)."""
    out = set()
    for carpeta in CARPETAS:
        for p in sorted((RAIZ / carpeta).rglob("*.py")):
            rel = p.relative_to(RAIZ).as_posix()
            out |= {f"{rel}::{n}" for n, _i, _f, lector in _funciones(p.read_text(encoding="utf-8"))
                    if lector}
    return out


def _registro():
    sys.path.insert(0, str(RAIZ))
    sys.path.insert(0, str(RAIZ / "tests"))
    import warnings
    warnings.filterwarnings("ignore")   # FutureWarning de pandas: ruido en el hook
    import contratos_fuentes
    return contratos_fuentes


def sin_contrato(lectores, cf):
    cubiertas = {f for c in cf.CONTRATOS for f in c.cubre}
    return sorted(f for f in lectores
                  if f not in cubiertas and f not in EXENTOS and f not in TRANSVERSALES)


def _bloquear(huerfanos):
    print("=" * 70, file=sys.stderr)
    print("COMMIT BLOQUEADO: lector(es) de planillas SIN contrato", file=sys.stderr)
    print("=" * 70, file=sys.stderr)
    for f in huerfanos:
        print(f"  {f}", file=sys.stderr)
    print("\nCada funcion que lee un export del usuario necesita su contrato en\n"
          "tests/contratos_fuentes.py (0 filas, columna renombrada, clave vacia, fechas\n"
          "ilegibles, indice fijo). En Claude Code: skill `tests-fuentes`.\n"
          "Si NO lee un export del usuario: agregarla a EXENTOS en tools/check_fuentes.py,\n"
          "con el motivo.\nSaltar el hook: git commit --no-verify", file=sys.stderr)


def pre_commit():
    rutas = staged()
    relevantes = [r for r in rutas if r.split("/")[0] in CARPETAS and r.endswith(".py")]
    refs = {Path(r).name for r in rutas if r.startswith("refs_tablas/")}
    registro = any(r in ("tests/contratos_fuentes.py", "tools/check_fuentes.py") for r in rutas)
    if not (relevantes or refs or registro):
        return 0
    todas, lectores = tocadas(relevantes)
    cf = _registro()
    huerfanos = sin_contrato(lectores, cf)
    if registro or todas & TRANSVERSALES:
        ids = None
        motivo = "cambio el registro o una primitiva compartida -> todos"
    else:
        ids = {c.id for c in cf.CONTRATOS if set(c.cubre) & todas or (c.ref and c.ref in refs)}
        motivo = ", ".join(sorted(ids)) if ids else ""
    fallas = 0
    if ids is None or ids:
        print(f"[fuentes] contratos: {motivo}")
        fallas = cf.correr(ids)
    if huerfanos:
        _bloquear(huerfanos)
        return 1
    if fallas:
        print(f"\nCOMMIT BLOQUEADO: {fallas} falla(s) de contrato (ver arriba). "
              "Arreglar la guarda sobre la FUENTE (CLAUDE.md regla 2), o -- si es un\n"
              "pendiente conocido -- anotarlo en `conocidos` del contrato, con motivo.",
              file=sys.stderr)
        return 1
    print("[fuentes] OK" + ("" if ids is None or ids else " - ningun lector tocado"))
    return 0


def todo():
    cf = _registro()
    fallas = cf.correr()
    faltan = sin_contrato(inventario(), cf)
    if faltan:
        print(f"\n[fuentes] {len(faltan)} lector(es) todavia SIN contrato (no bloquea hasta "
              "que un commit los toque):")
        for f in faltan:
            print(f"    {f}")
    sin_ref = [c.id for c in cf.CONTRATOS if not c.ref]
    if sin_ref:
        print(f"\n[fuentes] {len(sin_ref)} contrato(s) con encabezado SINTETICO: pedir el "
              "export real, solo encabezado (skill limpiar-refs): " + ", ".join(sin_ref))
    print(f"\n[fuentes] {'OK' if not fallas else f'{fallas} FALLA(S)'}")
    return 1 if fallas else 0


def instalar_hook():
    """Encadena este check al pre-commit (logica comun en tools/hooks_git.py)."""
    sys.path.insert(0, str(RAIZ))
    from tools.hooks_git import encadenar
    encadenar("tools/check_fuentes.py")


def main():
    argv = sys.argv[1:]
    if "--instalar" in argv:
        instalar_hook()
        return 0
    if "--todo" in argv:
        return todo()
    return pre_commit()


if __name__ == "__main__":
    sys.exit(main())
