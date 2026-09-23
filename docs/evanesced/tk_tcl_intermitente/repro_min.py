#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This code was generated with the assistance of Claude Opus 5.5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Repro MINIMO del `tk.tcl` intermitente, SIN pytest (docs/tk_tcl_intermitente.md).

Mecanismo propuesto: Tcl (win/tclWinChan.c, OpenFileChannel) guarda por hilo una
lista de los HANDLE Win32 que ya envolvio -- entre ellos stdin/stdout/stderr, que el
1er interprete toma como canales estandar y no suelta nunca. Si despues alguien cierra
esos handles por debajo (pytest --capture=fd hace dup2 sobre los fd 0/1/2 en cada
fase de cada test), Windows REUSA esos valores; cuando Tcl abre un .tcl y le toca un
valor que tiene en la lista, devuelve NULL (permisos distintos) sin tocar errno ->
"couldn't read file ...: No error" / ENOENT viejo.

Modos:
  dup2     lo que hace pytest: 1er Tk, y antes de cada Tk nuevo, dup2 de temporales
           frescos sobre 0/1/2 (cierra los handles viejos).
  control  lo mismo sin dup2.
Uso: python repro_min.py <modo> <N> <archivo_resultado>
"""
import os
import sys
import tempfile
import tkinter

modo, n, destino = sys.argv[1], int(sys.argv[2]), sys.argv[3]
out = open(destino, "w")          # stdout/stderr son justo lo que se rompe


def redirigir():
    """Como FDCapture de pytest: un temporal nuevo sobre 1 y 2, devnull sobre 0.
    dup2 cierra el handle que tenia el fd -- ese es el que Tcl sigue creyendo suyo."""
    for fd in (1, 2):
        tmp = tempfile.TemporaryFile(buffering=0)
        os.dup2(tmp.fileno(), fd)
        tmp.close()
    nul = os.open(os.devnull, os.O_RDONLY)
    os.dup2(nul, 0)
    os.close(nul)


r = tkinter.Tk(); r.destroy(); del r      # el 1er interprete fija los canales estandar
fallas = []
for i in range(1, n + 1):
    if modo == "dup2":
        redirigir()
    try:
        r = tkinter.Tk(); r.update(); r.destroy(); del r
    except tkinter.TclError as e:
        fallas.append(i)
        linea = [l for l in str(e).splitlines() if "couldn't read" in l or "invalid" in l]
        out.write("i=%d  %s\n" % (i, (linea[0] if linea else str(e).splitlines()[0])[:170]))
out.write("modo=%s  N=%d  fallas=%d\n" % (modo, n, len(fallas)))
out.close()
