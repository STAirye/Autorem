#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# Copyright (C) 2026 Simon Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.9.6
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. Distributed WITHOUT ANY WARRANTY. See the GNU
# General Public License for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
hooks_git.py - instalador COMUN de los hooks del repo (lado desarrollo).

Fuente unica de `--instalar`: la usan hook_pre_commit_rut.py (#8.2),
check_cp1252.py y check_version.py (#9). Los tres encadenan al MISMO
.git/hooks/pre-commit, y hasta 1.9.5 cada uno traia su propia copia de la
logica de encadenado -- copias que ya habian divergido (la de check_cp1252 no
sacaba el 'exit 0' final, asi que instalarlo despues de check_version dejaba su
linea DESPUES del exit: instalado y sin correr nunca, callado).

RUTAS RELATIVAS AL WORKTREE (la razon de este archivo, sep-2026)
  La invocacion se escribe contra $REPO = `git rev-parse --show-toplevel`, NO
  contra la ruta absoluta del clon donde corriste --instalar.

  Los hooks viven en el .git COMPARTIDO, asi que el mismo archivo corre desde el
  checkout principal Y desde cada worktree (#10.1). Con rutas absolutas, un
  commit hecho en un worktree ejecutaba los checks del OTRO arbol: paso con
  check_version, que bloqueo el commit reportando headers viejos de main
  mientras el worktree ya iba en 1.9.5 -- describiendo con precision un arbol
  que no se estaba commiteando. Con $REPO, cada commit se revisa a si mismo.

  Efecto colateral bueno: el hook deja de depender de DONDE esta clonado el
  repo, asi que sobrevive a mover la carpeta.

Si el script no existe en ese arbol (rama vieja, anterior a la herramienta), la
invocacion falla y BLOQUEA el commit: es raro, se ve en el acto y se destraba con
--no-verify. Preferible a saltarse en silencio un check de privacidad.

USO (desde los otros tools, no directo)
    from tools.hooks_git import encadenar
    encadenar("tools/check_version.py")
"""

import subprocess
import sys
from pathlib import Path

_SHEBANG = "#!/bin/sh"
_REPO = 'REPO="$(git rev-parse --show-toplevel)"'


def _git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True,
                          errors="ignore").stdout


def encadenar(script, hook="pre-commit", args=""):
    """Encadena `script` (ruta RELATIVA a la raiz del repo) al hook `hook`.

    Respeta lo que ya haya en el hook e idempotente: reinstalar no duplica. Si
    encuentra una invocacion VIEJA del mismo script (ruta absoluta, pre-1.9.6),
    la REEMPLAZA -- si no, quedarian las dos y la vieja seguiria mirando el
    arbol equivocado. Devuelve la ruta del hook escrito.
    """
    hooks = Path(_git("rev-parse", "--git-path", "hooks").strip())   # el .git COMPARTIDO
    hooks.mkdir(parents=True, exist_ok=True)
    destino = hooks / hook
    invocacion = f'"{sys.executable}" "$REPO/{script}"' + (f" {args}" if args else "")
    texto = destino.read_text(encoding="utf-8") if destino.exists() else ""

    if invocacion in texto:
        print(f"ya instalado: {destino}")
        return destino

    lineas = texto.rstrip("\n").split("\n") if texto.strip() else [_SHEBANG]
    # 'exec' reemplaza el proceso -> nada corre despues; se degrada a invocacion
    # normal para poder encadenar detras.
    lineas = [f"{l[len('exec '):]} || exit 1" if l.startswith("exec ") else l
              for l in lineas]
    viejas = [l for l in lineas if Path(script).name in l and "$REPO" not in l]
    if viejas:
        print(f"reemplazo la invocacion vieja (ruta absoluta) de {script}")
        lineas = [l for l in lineas if l not in viejas]
    # el 'exit 0' final se saca y se vuelve a poner al final: si no, la linea
    # nueva queda DESPUES del exit (instalada y sin correr nunca).
    lineas = [l for l in lineas if l.strip() != "exit 0"]
    if _REPO not in lineas:
        lineas.insert(1 if lineas[0].startswith("#!") else 0, _REPO)
    lineas += [f"{invocacion} || exit 1", "exit 0"]

    destino.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    destino.chmod(0o755)
    print(f"instalado: {destino}")
    return destino
