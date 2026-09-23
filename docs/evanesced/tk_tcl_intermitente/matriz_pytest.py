#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This code was generated with the assistance of Claude Opus 5.5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Segunda ronda del repro (docs/tk_tcl_intermitente.md SS6): la primera mostro que el
`tk.tcl` NO sale fuera de pytest (9000 lecturas de .tcl limpias) y SI dentro (3/5),
ya en el 2o interprete. Esto corre el archivo real con distintas opciones de pytest
para aislar que parte de pytest lo dispara.

Uso (desde la raiz del repo):  python matriz_pytest.py [K] [variante,variante,...]
"""
import re
import subprocess
import sys
import time

ARCHIVO = "tests/test_gui_construccion.py"
VARIANTES = {
    "base":         [],
    "sin_captura":  ["-s"],                      # sin captura: fd 0/1/2 intactos
    "captura_sys":  ["--capture=sys"],           # captura solo sys.stdout, sin dup2
    "sin_faulth":   ["-p", "no:faulthandler"],
    "pin":          ["-p", "tcl_std_pin"],       # el arreglo (PYTHONPATH=scratchpad)
}
RE_TCL = re.compile(r'couldn\'t read file "[^"]*/([^/"]+)": ([^\n]+)')


def correr(extra):
    t0 = time.perf_counter()
    r = subprocess.run([sys.executable, "-m", "pytest", ARCHIVO, "-q",
                        "-p", "no:cacheprovider"] + extra, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    out = r.stdout + r.stderr
    fallas = re.findall(r"^FAILED \S+::(\S+)", out, re.M)
    tcl = sorted(set("%s (%s)" % m for m in RE_TCL.findall(out)))
    return time.perf_counter() - t0, fallas, tcl


def main():
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    nombres = sys.argv[2].split(",") if len(sys.argv) > 2 else list(VARIANTES)
    total = dict.fromkeys(nombres, 0)
    for run in range(k):              # intercaladas: mismas condiciones de maquina
        for nombre in nombres:
            dt, fallas, tcl = correr(VARIANTES[nombre])
            total[nombre] += bool(fallas)
            print("%-12s run %d  %5.1fs  %s  %s" % (nombre, run, dt,
                  ("FALLA " + ",".join(fallas)) if fallas else "ok", "; ".join(tcl)))
            sys.stdout.flush()
    print("\n==== RESUMEN (corridas con falla / %d)" % k)
    for nombre in nombres:
        print("  %-12s %d/%d" % (nombre, total[nombre], k))


if __name__ == "__main__":
    main()
