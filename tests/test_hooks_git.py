#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 5.5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# SPDX-License-Identifier: GPL-3.0-or-later
# ==========================================================================
"""
Pruebas de `tools/hooks_git.encadenar`, el instalador comun de los 4 checks.

Por que existen: hasta la 2.0.11, reinstalar los hooks con OTRO Python agregaba las
lineas nuevas al lado de las viejas en vez de reemplazarlas (solo reconocia como
vieja la invocacion de ruta absoluta pre-1.9.6). Cada check corria dos veces, y al
desinstalar el Python viejo su linea fallaba y bloqueaba TODO commit. Paso al pasar
el PC del trabajo de 3.14.3 (Tcl 8.6) a 3.14.7 (Tcl 9), ver
docs/tk_tcl_intermitente.md.

Corre contra un repo git TEMPORAL: nunca toca los hooks reales.
Correr: python tests/test_hooks_git.py
"""

import os
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
import _aislar_cache   # noqa: E402,F401  (PRIMERO: nunca tocar el ~/.autorem real)

from tools import hooks_git   # noqa: E402

PY_VIEJO = r"C:\Python\viejo\python.exe"
PY_NUEVO = r"C:\Python\nuevo\python.exe"
SCRIPTS = ("tools/check_cp1252.py", "tools/check_version.py")


@contextmanager
def _repo_temporal(interprete):
    """cwd en un `git init` fresco y `sys.executable` fingido: `encadenar` escribe
    ahi, con ese interprete, y el .git real ni se entera."""
    previo_cwd, previo_exe = os.getcwd(), sys.executable
    with tempfile.TemporaryDirectory(prefix="autorem_hooks_") as d:
        subprocess.run(["git", "init", "-q", d], check=True)
        os.chdir(d)
        sys.executable = interprete
        try:
            yield Path(d) / ".git" / "hooks" / "pre-commit"
        finally:
            sys.executable = previo_exe
            os.chdir(previo_cwd)


def _instalar(interprete=None):
    if interprete:
        sys.executable = interprete
    for s in SCRIPTS:
        hooks_git.encadenar(s)


def test_cambiar_de_python_reemplaza_no_duplica():
    """El caso real: reinstalar con otro Python deja UNA linea por check, la nueva."""
    with _repo_temporal(PY_VIEJO) as hook:
        _instalar()
        _instalar(PY_NUEVO)
        texto = hook.read_text(encoding="utf-8")
        for s in SCRIPTS:
            assert texto.count(Path(s).name) == 1, f"{s} quedo {texto.count(Path(s).name)} veces"
        assert PY_VIEJO not in texto, "sobrevivio una linea del Python viejo"
        assert texto.count(PY_NUEVO) == len(SCRIPTS)


def test_un_hook_que_ya_quedo_duplicado_se_limpia():
    """El estado que dejo la 2.0.11 en el PC del trabajo: la linea nueva YA escrita al
    lado de la vieja. Reinstalar tiene que limpiarla, no decir «ya instalado» y salir."""
    with _repo_temporal(PY_VIEJO) as hook:
        _instalar()
        sucio = hook.read_text(encoding="utf-8").replace(
            "exit 0\n", "".join(f'"{PY_NUEVO}" "$REPO/{s}" || exit 1\n' for s in SCRIPTS)
            + "exit 0\n")
        hook.write_text(sucio, encoding="utf-8")
        _instalar(PY_NUEVO)
        texto = hook.read_text(encoding="utf-8")
        assert PY_VIEJO not in texto, "el hook duplicado no se limpio"
        for s in SCRIPTS:
            assert texto.count(Path(s).name) == 1


def test_reinstalar_igual_no_cambia_nada():
    with _repo_temporal(PY_NUEVO) as hook:
        _instalar()
        antes = hook.read_text(encoding="utf-8")
        _instalar()
        assert hook.read_text(encoding="utf-8") == antes


def test_la_invocacion_de_ruta_absoluta_pre_196_se_sigue_reemplazando():
    """Lo que ya hacia antes de 2.0.12 no se pierde al ensanchar el criterio."""
    with _repo_temporal(PY_NUEVO) as hook:
        hook.parent.mkdir(parents=True, exist_ok=True)
        hook.write_text('#!/bin/sh\n"C:/py/python.exe" "C:/clon/tools/check_version.py" '
                        "|| exit 1\nexit 0\n", encoding="utf-8")
        _instalar()
        texto = hook.read_text(encoding="utf-8")
        assert "C:/clon/" not in texto
        assert texto.count("check_version.py") == 1


def test_exit_0_queda_al_final_y_una_sola_vez():
    """Si el `exit 0` quedara antes de una linea, esa linea no correria nunca (1.9.5)."""
    with _repo_temporal(PY_VIEJO) as hook:
        _instalar()
        _instalar(PY_NUEVO)
        lineas = hook.read_text(encoding="utf-8").strip().split("\n")
        assert lineas[-1] == "exit 0" and lineas.count("exit 0") == 1


if __name__ == "__main__":
    fallos = 0
    for nombre, fn in sorted(globals().items()):
        if nombre.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"  ok  {nombre}")
            except AssertionError as e:
                fallos += 1
                print(f"  FALLA  {nombre}: {e}")
    print(f"\n{'FALLARON ' + str(fallos) if fallos else 'TODO OK'}")
    sys.exit(1 if fallos else 0)
