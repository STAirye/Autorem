#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 5 (Anthropic).
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
hook_pre_commit_rut.py - bloquea RUTs reales antes de que entren a un commit.

Nace de un incidente real (sep-2026): un RUT de una persona real vivio como
"ejemplo" en CLAUDE.md y en legacy/ desde el commit inicial, y llego a GitHub
publico. Hubo que reescribir el historial y recrear el repositorio.

QUE BLOQUEA
  Cualquier cadena con forma de RUT (NNNNNNNN-D) cuyo DIGITO VERIFICADOR CUADRE
  (modulo 11), en el contenido de los archivos staged Y en el mensaje de commit.
  Validar el DV es lo que distingue un RUT plausible de un placeholder cualquiera.

QUE DEJA PASAR (placeholders obvios, para tests y documentacion)
  - digitos todos iguales:            11111111-1, 22222222-2 ...
  - cuerpo que empieza en 1000:       10000001-K ... (relleno de fixtures)
  - todos ceros:                      00000000-0

INSTALACION
    python tools/hook_pre_commit_rut.py --instalar

Copia este archivo a .git/hooks/pre-commit (y a commit-msg). Los hooks NO se
versionan, asi que hay que instalarlo en cada clon.

SALTARSE EL HOOK (solo si estas SEGURO de que es sintetico)
    git commit --no-verify
"""

import re
import subprocess
import sys
from pathlib import Path

RUT = re.compile(r"\b(\d{7,9})-([\dkK])\b")

BIN = (".xlsx", ".xlsm", ".xls", ".gz", ".png", ".jpg", ".jpeg", ".pdf",
       ".exe", ".pyc", ".zip")


def dv(cuerpo):
    """Digito verificador chileno (modulo 11)."""
    suma, mult = 0, 2
    for ch in reversed(str(cuerpo)):
        suma += int(ch) * mult
        mult = 2 if mult == 7 else mult + 1
    r = 11 - (suma % 11)
    return "0" if r == 11 else "K" if r == 10 else str(r)


def es_placeholder(cuerpo):
    return len(set(cuerpo)) == 1 or cuerpo.startswith("1000") or set(cuerpo) == {"0"}


def sospechosos(texto):
    """RUTs con DV valido que NO son placeholders obvios."""
    out = set()
    for cuerpo, d in RUT.findall(texto or ""):
        if not es_placeholder(cuerpo) and d.upper() == dv(cuerpo):
            out.add(f"{cuerpo}-{d}")
    return out


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True,
                          errors="ignore").stdout


def revisar_staged():
    hallazgos = {}
    for f in git("diff", "--cached", "--name-only", "--diff-filter=ACM").split("\n"):
        f = f.strip()
        if not f or f.lower().endswith(BIN):
            continue
        # el CONTENIDO QUE SE VA A COMMITEAR (el del index, no el del disco)
        for r in sospechosos(git("show", f":{f}")):
            hallazgos.setdefault(r, set()).add(f)
    return hallazgos


def revisar_mensaje(ruta):
    try:
        return sospechosos(Path(ruta).read_text(encoding="utf-8", errors="ignore"))
    except OSError:
        return set()


def instalar():
    hooks = Path(git("rev-parse", "--git-path", "hooks").strip())
    hooks.mkdir(parents=True, exist_ok=True)
    yo = Path(__file__).resolve()
    for nombre in ("pre-commit", "commit-msg"):
        destino = hooks / nombre
        destino.write_text(
            "#!/bin/sh\n"
            f'exec "{sys.executable}" "{yo}" --hook {nombre} "$@"\n',
            encoding="utf-8")
        destino.chmod(0o755)
        print(f"instalado: {destino}")
    print("\nListo. Para saltarlo puntualmente: git commit --no-verify")


def main():
    if "--instalar" in sys.argv:
        instalar()
        return 0

    modo = sys.argv[sys.argv.index("--hook") + 1] if "--hook" in sys.argv else "pre-commit"

    if modo == "commit-msg":
        ruta = sys.argv[-1]
        malos = revisar_mensaje(ruta)
        donde = {r: {"(mensaje de commit)"} for r in malos}
    else:
        donde = revisar_staged()

    if not donde:
        return 0

    print("=" * 70, file=sys.stderr)
    print("COMMIT BLOQUEADO: hay RUT(s) con digito verificador VALIDO", file=sys.stderr)
    print("=" * 70, file=sys.stderr)
    for r, archivos in sorted(donde.items()):
        print(f"  {r}", file=sys.stderr)
        for a in sorted(archivos):
            print(f"      {a}", file=sys.stderr)
    print("\nUn RUT con DV valido es, muy probablemente, de una persona REAL.", file=sys.stderr)
    print("Reemplazalo por un placeholder (11111111-1) antes de commitear.", file=sys.stderr)
    print("Si estas SEGURO de que es sintetico:  git commit --no-verify", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
