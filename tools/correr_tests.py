#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# Copyright (C) 2026 Simon Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. Distributed WITHOUT ANY WARRANTY. See the GNU
# General Public License for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
Corre la suite en varios PROCESOS, un archivo de tests por proceso.

POR QUE ASI Y NO CON pytest-xdist (medido en 2.0.2, sep-2026, 12 CPUs):

    secuencial (`pytest`)         194 s
    2 procesos POR ARCHIVO        106 s
    3 procesos POR ARCHIVO        103 s   <- esto (1.9x)
    4 procesos POR ARCHIVO        110 s
    6 procesos POR TEST suelto    ~94 s en 2.0.1 -- y peor que por archivo

La culpa de todo es Tk. `test_gui_construccion.py` abre la ventana de verdad y
se lleva 90 s de los 191 s de la suite; encima NO se paraleliza, porque dos
procesos Tk en Windows se frenan entre si. Medido, el mismo archivo:

    solo, sin nadie al lado                74 s
    con 1 proceso  (no-Tk) compitiendo    ~96 s
    con 2 procesos (no-Tk) compitiendo   ~102 s
    con 3 procesos (no-Tk) compitiendo   ~109 s

O sea el wall de la suite es `max(gui_penalizada(N), resto / (N-1))`, y esa
formula predice las tres corridas de arriba. Dos consecuencias:

  - MAS procesos no es mejor: pasado N=3 la GUI se degrada mas rapido de lo
    que se acelera el resto. De ahi el default 3 y no `os.cpu_count()`.
  - El reparto es por ARCHIVO, para que TODO Tk caiga en UN proceso. Repartir
    por test suelto -- que es lo que hace `xdist -n auto` -- esparce los tests
    de Tk entre todos los workers, que es justo el caso malo. Si algun dia se
    instala xdist, el equivalente honesto es `--dist loadfile`, nunca `-n auto`.

El piso duro son esos 74 s de la GUI corriendo sola: no hay reparto que lo
baje. Para ganar mas hay que hacer la GUI mas barata, no sumar procesos.

NO reemplaza a `pytest`: para depurar un test suelto se sigue usando pytest
directo, que da el traceback ordenado. Esto es para la pasada completa.

USO
    python tools/correr_tests.py              # 3 procesos
    python tools/correr_tests.py -n 6         # otro reparto
    python tools/correr_tests.py -n 1         # secuencial (comparar tiempos)
"""

import heapq
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TESTS = RAIZ / "tests"

# Version: 2.0.3

# Costo relativo de cada archivo (segundos de la corrida secuencial de 2.0.2).
# Solo ORDENA el reparto: un archivo que no este aca entra con PESO_NUEVO y el
# reparto sigue funcionando -- no hay que mantener esto al dia para que corra,
# solo para que reparta bien. Reveer si un archivo crece mucho.
PESOS = {
    "test_gui_construccion.py": 90.0,
    "test_sp_p6.py": 38.5,
    "test_rescate_inasistentes.py": 12.5,
    "test_contratos_fuentes.py": 10.0,
    "test_gui_registro.py": 10.0,
    "test_sm_actividades.py": 7.0,
    "test_refs_tablas.py": 5.0,
    "test_a23.py": 4.5,
    "test_dotacion.py": 3.0,
    "test_trabajo_perdido.py": 3.0,
    "test_formatos_fuente.py": 2.0,
    "test_screening.py": 1.5,
    "test_autorem.py": 1.5,
    "test_estamentos.py": 1.5,
    "test_cobertura.py": 0.5,
    "test_catalogos.py": 0.5,
}
PESO_NUEVO = 5.0


def repartir(archivos, n):
    """LPT: el archivo mas caro primero, siempre al proceso mas vacio. Da el
    reparto optimo o casi, y en un caso tan desbalanceado como este el optimo
    es 'el archivo grande solo y todo lo demas junto'."""
    montones = [(0.0, i, []) for i in range(n)]
    heapq.heapify(montones)
    for a in sorted(archivos, key=lambda p: -PESOS.get(p.name, PESO_NUEVO)):
        carga, i, lista = heapq.heappop(montones)
        lista.append(a)
        heapq.heappush(montones, (carga + PESOS.get(a.name, PESO_NUEVO), i, lista))
    return [(c, l) for c, _, l in sorted(montones) if l]


def main(argv):
    n = 3
    if "-n" in argv:
        n = int(argv[argv.index("-n") + 1])

    archivos = sorted(TESTS.glob("test_*.py"))
    if not archivos:
        print("No encontre tests/test_*.py")
        return 1
    nuevos = [a.name for a in archivos if a.name not in PESOS]
    if nuevos:
        print("Sin peso conocido (reparto a ciegas): " + ", ".join(nuevos))

    planes = repartir(archivos, n)
    print("%d archivos en %d procesos, carga estimada %s"
          % (len(archivos), len(planes), [round(c) for c, _ in planes]))

    t0 = time.time()
    procs = [(lista, subprocess.Popen(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         *[str(a) for a in lista]],
        cwd=str(RAIZ), stdout=subprocess.PIPE, stderr=subprocess.STDOUT))
        for _, lista in planes]

    malos = []
    for lista, p in procs:
        salida = p.communicate()[0].decode("utf-8", "replace")
        resumen = [L for L in salida.splitlines()
                   if " passed" in L or " failed" in L or " error" in L]
        print("  [%s] %s" % ("ok " if p.returncode == 0 else "FALLA",
                             resumen[-1] if resumen else "(sin resumen)"))
        if p.returncode != 0:
            malos.append((lista, salida))

    # El detalle de los que fallaron va AL FINAL y completo: si se imprime
    # mezclado, seis procesos escupiendo tracebacks a la vez no se lee.
    for lista, salida in malos:
        print("\n" + "=" * 70)
        print("FALLO: " + ", ".join(a.name for a in lista))
        print("=" * 70)
        print(salida)

    print("\n%.1fs en total (%d procesos)%s"
          % (time.time() - t0, len(planes),
             "" if not malos else "  -- HAY FALLAS, mira arriba"))
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
