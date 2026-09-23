#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This code was generated with the assistance of Claude Opus 5.5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tcl cierra el HANDLE Win32 de stdout/stderr al borrar un interprete, cuando esos
std handles son ARCHIVOS (como los deja la captura por fd de pytest)?

Hace lo mismo que pytest: dup2 de un temporal sobre el fd 1 y el 2. Crea y destruye
un Tk, suelta el objeto (Tcl_DeleteInterp), y mira si el handle que Windows tiene
como STD_OUTPUT/STD_ERROR sigue vivo. Los resultados van a un archivo aparte,
porque stdout/stderr son justo lo que se esta rompiendo.
"""
import ctypes
import gc
import os
import sys
import tempfile
from ctypes import wintypes

k32 = ctypes.windll.kernel32
k32.GetStdHandle.restype = wintypes.HANDLE
k32.GetHandleInformation.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
k32.GetFileType.argtypes = [wintypes.HANDLE]
STD = {"out": -11, "err": -12}
salida = open(sys.argv[1], "w")


def estado(etiqueta):
    partes = []
    for nombre, n in STD.items():
        h = k32.GetStdHandle(n)
        flags = wintypes.DWORD()
        vivo = bool(k32.GetHandleInformation(h, ctypes.byref(flags)))
        partes.append("%s h=%s vivo=%s tipo=%s" % (nombre, h, vivo, k32.GetFileType(h)))
    salida.write("%-28s %s\n" % (etiqueta, " | ".join(partes)))
    salida.flush()


modo = sys.argv[2] if len(sys.argv) > 2 else "archivo"
if modo == "archivo":        # como pytest --capture=fd
    for fd in (1, 2):
        tmp = tempfile.TemporaryFile(buffering=0)
        os.dup2(tmp.fileno(), fd)
estado("antes (%s)" % modo)

import tkinter  # noqa: E402
for i in range(3):
    r = tkinter.Tk(); r.update(); r.destroy()
    estado("Tk %d destroy()" % i)
    del r; gc.collect()
    estado("Tk %d borrado (DeleteInterp)" % i)
try:
    os.write(1, b"x"); salida.write("os.write(1) ok\n")
except OSError as e:
    salida.write("os.write(1) FALLA: %s\n" % e)
salida.close()
