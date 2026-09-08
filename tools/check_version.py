#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# Copyright (C) 2026 Simon Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.9.4
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. Distributed WITHOUT ANY WARRANTY. See the GNU
# General Public License for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
check_version.py - coherencia de versionado y contadores, en un solo lugar.

POR QUE EXISTE. Cada version del proyecto obliga a tocar los mismos cinco sitios a
mano: rem_utils.VERSION, el header de los .py que cambiaron, la version en CLAUDE.md
(dos lugares), el conteo de tests (cuatro lugares) y la entrada del CHANGELOG. En una
sola sesion de sep-2026 eso se hizo cuatro veces, y cada vez quedo algo desincronizado
-- CLAUDE.md llego a declarar 94 tests cuando habia 124, y 1.8.2 cuando iba 1.9.1.
Nada de eso rompe el codigo: rompe la CONFIANZA en la documentacion, que es lo unico
que tiene una sesion fria para orientarse.

QUE REVISA
  1. MANIFIESTO, en las DOS direcciones:
       - codigo distribuible SIN '# Version:'  -> falta
       - archivo fuera de esas rutas CON version -> se esta colando
     El manifiesto se DERIVA DE LA RUTA, no es una lista a mano: una lista seria otra
     cosa que se pudre (ya paso con el .spec ignorado y con el catalogo de cobertura).
  2. La VERSION de rem_utils aparece en CLAUDE.md y tiene entrada en el CHANGELOG.
  3. Los .py de codigo que vas a commitear declaran la VERSION ACTUAL en su header.
     Convencion del proyecto: cada archivo lleva la version de SU ULTIMO CAMBIO
     (no todos sincronizados) -> el header dice CUANDO cambio ese archivo.
  4. El conteo de tests declarado en CLAUDE.md calza con los `def test_` reales.
     Se cuenta ESTATICAMENTE (no corre pytest): son 143 por ambos metodos, y un hook
     que tarda 30 segundos por commit no lo usa nadie.

LEGACY. legacy/ esta CONGELADO a proposito en sus versiones historicas (1.1, 1.2):
son el registro de como era el monolito, no codigo vivo. Queda exento de todo.

USO
    python tools/check_version.py                 # revisa (lo que corre el hook)
    python tools/check_version.py --arreglar      # sincroniza lo que sea automatico
    python tools/check_version.py --bump 1.9.4    # sube de version de un viaje
    python tools/check_version.py --instalar      # encadena al hook pre-commit

Escape puntual: git commit --no-verify
"""

import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FUENTE_VERSION = RAIZ / "programas" / "rem_utils.py"
CLAUDE = RAIZ / "CLAUDE.md"
CHANGELOG = RAIZ / "CHANGELOG.md"
TESTS = RAIZ / "tests"

# Codigo DISTRIBUIBLE = lo que viaja dentro del .exe. Eso lleva version.
DIRS_VERSIONADOS = ("programas", "modulos", "tools")
RAIZ_VERSIONADOS = ("autorem.py",)
# Exentos: __init__.py (vacios), tests/ (no se distribuyen) y legacy/ (congelado).
EXENTOS_NOMBRE = ("__init__.py",)
EXENTOS_DIR = ("legacy",)

RE_HEADER = re.compile(r"^# Version: *([\d.]+) *$", re.M)
RE_VERSION_PY = re.compile(r'^VERSION = "([\d.]+)"', re.M)

# Los sitios de CLAUDE.md donde se repite el conteo de tests. Cada patron tiene UN
# grupo: el numero. Si agregas otra frase con el conteo, agregala aca o se desincroniza.
PATRONES_TESTS = [
    re.compile(r"\*\*(\d+) tests\.\*\*"),
    re.compile(r"pruebas automáticas \((\d+)\)"),
    re.compile(r"suite: (\d+) tests"),
    re.compile(r"\*\*(\d+) tests\*\* \(§2\.1"),
]


def _git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True,
                          errors="ignore", cwd=RAIZ).stdout


def version_actual():
    m = RE_VERSION_PY.search(FUENTE_VERSION.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def _rel(p):
    return p.relative_to(RAIZ).as_posix()


def _tupla(v):
    return tuple(int(x) for x in v.split("."))


def versiones_changelog():
    """Todas las versiones con entrada '## [X.Y.Z]', de mayor a menor."""
    vs = re.findall(r"^## \[(\d+\.\d+\.\d+)\]", CHANGELOG.read_text(encoding="utf-8"), re.M)
    return sorted(set(vs), key=_tupla, reverse=True)


def revisar_colision(ver):
    """DOS SESIONES EN PARALELO subiendo de version al mismo tiempo.

    Paso de verdad (sep-2026): un workflow queria 1.8.4 y otro 1.9.0 sobre el mismo
    repo. Los dos numeros eran defendibles por separado, asi que nada los frenaba
    hasta que chocaban. El CHANGELOG es el arbitro: si ya tiene una version MAYOR
    que la que declara rem_utils.VERSION, alguien mas avanzo y esta copia quedo
    atras -- seguir bumpeando desde aca pisa su trabajo."""
    top = versiones_changelog()
    if top and _tupla(top[0]) > _tupla(ver):
        return (f"COLISION DE VERSIONES: el CHANGELOG ya tiene {top[0]}, pero "
                f"rem_utils.VERSION dice {ver}. Otro workflow subio la version "
                f"mientras trabajabas. Sincroniza (git pull / revisa el CHANGELOG) "
                f"y re-bumpea DESDE {top[0]}, no desde {ver}.")
    return None


def exento(rel):
    """Ni obligado ni prohibido: no se opina. Hoy solo legacy/, que esta CONGELADO
    en sus versiones historicas (1.1, 1.2) a proposito -- son el registro de como era
    el monolito. Ojo con la distincion: 'exento' NO es lo mismo que 'no debe llevar'."""
    return Path(rel).parts[0] in EXENTOS_DIR


def debe_llevar_version(rel):
    """La regla del manifiesto, derivada de la RUTA."""
    p = Path(rel)
    if exento(rel) or p.name in EXENTOS_NOMBRE:
        return False
    return p.parts[0] in DIRS_VERSIONADOS or rel in RAIZ_VERSIONADOS


def py_del_repo():
    return [l for l in _git("ls-files", "*.py").split("\n") if l.strip()]


def contar_tests():
    return sum(len(re.findall(r"^def test_", f.read_text(encoding="utf-8"), re.M))
               for f in sorted(TESTS.glob("test_*.py")))


def header_de(rel):
    try:
        m = RE_HEADER.search((RAIZ / rel).read_text(encoding="utf-8"))
    except OSError:
        return None
    return m.group(1) if m else None


def staged_py():
    """.py de CODIGO que entran en este commit (los que deben declarar la version)."""
    salida = _git("diff", "--cached", "--name-only", "--diff-filter=ACM")
    return [f for f in (l.strip() for l in salida.split("\n"))
            if f.endswith(".py") and debe_llevar_version(f)]


# -- Los chequeos -------------------------------------------------------------
def revisar(solo_staged=True):
    """Lista de (grave, mensaje). `grave` hoy no cambia el exit code (todo bloquea);
    esta para poder aflojar el hook sin reescribir los chequeos."""
    problemas = []
    ver = version_actual()
    if not ver:
        return [(True, "No pude leer VERSION de programas/rem_utils.py")]

    # 1. Manifiesto, las dos direcciones.
    for rel in py_del_repo():
        if exento(rel):
            continue
        tiene = header_de(rel)
        if debe_llevar_version(rel) and tiene is None:
            problemas.append((True, f"{rel}: es codigo distribuible y NO lleva "
                                    f"'# Version:'"))
        elif not debe_llevar_version(rel) and tiene is not None:
            problemas.append((True, f"{rel}: lleva '# Version: {tiene}' pero NO es "
                                    f"codigo distribuible -> se esta colando en el "
                                    f"esquema (sacalo, o mueve el archivo)"))

    # 2. La version esta declarada donde corresponde.
    # Los DOS sitios concretos, no "que aparezca en algun lado": la version se cita
    # tambien en prosa ("(v1.9.3)") y eso hacia pasar el chequeo con §2 desfasado.
    claude = CLAUDE.read_text(encoding="utf-8")
    for etiqueta, esperado in ((u"§2 'Versión **X**'", f"Versión **{ver}**"),
                               (u"§9 'Estado actual: **X**'", f"Estado actual: **{ver}**")):
        if esperado not in claude:
            declara = re.search(re.escape(esperado.split("**")[0]) + r"\*\*([\d.]+)\*\*",
                                claude)
            visto = f" (dice {declara.group(1)})" if declara else ""
            problemas.append((True, f"CLAUDE.md {etiqueta} no declara {ver}{visto}"))
    if f"## [{ver}]" not in CHANGELOG.read_text(encoding="utf-8"):
        problemas.append((True, f"CHANGELOG.md no tiene entrada '## [{ver}]'"))
    colision = revisar_colision(ver)
    if colision:
        problemas.append((True, colision))

    # 3. Lo que se commitea declara la version actual.
    if solo_staged:
        for rel in staged_py():
            h = header_de(rel)
            if h is not None and h != ver:
                problemas.append((True, f"{rel}: header dice {h} pero la version "
                                        f"actual es {ver} (lo estas commiteando)"))

    # 4. Contadores de tests.
    n = contar_tests()
    for pat in PATRONES_TESTS:
        for declarado in pat.findall(claude):
            if int(declarado) != n:
                problemas.append((False, f"CLAUDE.md declara {declarado} tests, "
                                         f"pero hay {n}"))
    return problemas


# -- Arreglo automatico -------------------------------------------------------
def arreglar():
    ver, n, tocados = version_actual(), contar_tests(), []

    claude = CLAUDE.read_text(encoding="utf-8")
    nuevo = claude
    for pat in PATRONES_TESTS:
        nuevo = pat.sub(lambda m: m.group(0).replace(m.group(1), str(n)), nuevo)
    if nuevo != claude:
        CLAUDE.write_text(nuevo, encoding="utf-8")
        tocados.append(f"CLAUDE.md: contador de tests -> {n}")

    for rel in staged_py():
        h = header_de(rel)
        if h is not None and h != ver:
            p = RAIZ / rel
            p.write_text(RE_HEADER.sub(f"# Version: {ver}", p.read_text(encoding="utf-8"),
                                       count=1), encoding="utf-8")
            tocados.append(f"{rel}: header {h} -> {ver}")

    for t in tocados:
        print("  arreglado:", t)
    if not tocados:
        print("  nada que arreglar automaticamente.")
    print("\nLo que NO se arregla solo (requiere criterio):")
    print("  - la entrada del CHANGELOG: el texto lo escribis vos")
    print("  - la version en CLAUDE.md: usa --bump")
    return 0


def bump(nueva):
    """Sube la version: fuente de verdad + headers de lo modificado + CLAUDE.md."""
    if not re.fullmatch(r"\d+\.\d+\.\d+", nueva):
        print(f"version invalida: {nueva} (formato X.Y.Z)", file=sys.stderr)
        return 2
    vieja = version_actual()
    # Guardarrail anti-colision (ver revisar_colision): rechazar un numero que NO
    # avanza respecto de lo ya publicado. Sin esto, dos sesiones en paralelo eligen
    # numeros distintos y las dos "funcionan" hasta que chocan.
    publicadas = versiones_changelog()
    tope = max([vieja] + publicadas, key=_tupla) if (vieja or publicadas) else None
    if tope and _tupla(nueva) <= _tupla(tope):
        print(f"RECHAZADO: {nueva} no avanza respecto de {tope}.", file=sys.stderr)
        if publicadas and _tupla(publicadas[0]) > _tupla(vieja or "0.0.0"):
            print(f"El CHANGELOG ya tiene {publicadas[0]}: otro workflow subio la "
                  f"version mientras trabajabas.", file=sys.stderr)
        print(f"Elegi un numero mayor que {tope} (o revisa si otra sesion ya "
              f"bumpeo).", file=sys.stderr)
        return 2
    print(f"bump {vieja} -> {nueva}")

    t = FUENTE_VERSION.read_text(encoding="utf-8")
    FUENTE_VERSION.write_text(
        RE_VERSION_PY.sub(f'VERSION = "{nueva}"', t, count=1), encoding="utf-8")
    print(f"  rem_utils.VERSION -> {nueva}")

    # Headers de lo modificado en el arbol (staged o no): son los que cambiaron.
    mod = {l[3:].strip() for l in _git("status", "--porcelain").split("\n")
           if l[3:].strip().endswith(".py")}
    for rel in sorted(f for f in mod if debe_llevar_version(f)):
        p = RAIZ / rel
        if p.exists() and header_de(rel) not in (None, nueva):
            p.write_text(RE_HEADER.sub(f"# Version: {nueva}",
                                       p.read_text(encoding="utf-8"), count=1),
                         encoding="utf-8")
            print(f"  {rel} -> {nueva}")

    claude = CLAUDE.read_text(encoding="utf-8")
    if vieja:
        claude = claude.replace(f"Versión **{vieja}**", f"Versión **{nueva}**")
        claude = claude.replace(f"Estado actual: **{vieja}**.",
                                f"Estado actual: **{nueva}**.")
        CLAUDE.write_text(claude, encoding="utf-8")
        print("  CLAUDE.md: version actualizada")

    print(f"\nFALTA A MANO: escribir la entrada '## [{nueva}]' en CHANGELOG.md.")
    print("(a proposito: el QUE cambio y por que no lo puede inventar un script)")
    return 0


def instalar_hook():
    """Encadena este check al pre-commit, respetando lo que ya haya."""
    hooks = Path(_git("rev-parse", "--git-path", "hooks").strip())
    hooks.mkdir(parents=True, exist_ok=True)
    destino = hooks / "pre-commit"
    yo = Path(__file__).resolve()
    invocacion = f'"{sys.executable}" "{yo}"'

    if destino.exists() and str(yo) in destino.read_text(encoding="utf-8"):
        print(f"ya instalado: {destino}")
        return
    lineas = (destino.read_text(encoding="utf-8").rstrip("\n").split("\n")
              if destino.exists() else ["#!/bin/sh"])
    # 'exec' reemplaza el proceso -> nada corre despues. Si el hook existente lo usa,
    # se convierte en invocacion normal para poder encadenar este check.
    lineas = [f"{l[len('exec '):]} || exit 1" if l.startswith("exec ") else l
              for l in lineas]
    if "exit 0" in lineas:
        lineas.remove("exit 0")
    lineas.append(f"{invocacion} || exit 1")
    lineas.append("exit 0")
    destino.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    destino.chmod(0o755)
    print(f"instalado: {destino}")


def main():
    argv = sys.argv[1:]
    if "--instalar" in argv:
        instalar_hook()
        return 0
    if "--arreglar" in argv:
        return arreglar()
    if "--bump" in argv:
        i = argv.index("--bump")
        if i + 1 >= len(argv):
            print("uso: --bump X.Y.Z", file=sys.stderr)
            return 2
        return bump(argv[i + 1])

    problemas = revisar()
    if not problemas:
        print(f"[version] OK - {version_actual()} coherente, {contar_tests()} tests")
        return 0
    print("=" * 70, file=sys.stderr)
    print("COMMIT BLOQUEADO: versionado/contadores desincronizados", file=sys.stderr)
    print("=" * 70, file=sys.stderr)
    for _grave, m in problemas:
        print(f"  {m}", file=sys.stderr)
    print("\nArreglo automatico:  python tools/check_version.py --arreglar",
          file=sys.stderr)
    print("Subir de version:    python tools/check_version.py --bump X.Y.Z",
          file=sys.stderr)
    print("Saltar el hook:      git commit --no-verify", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
