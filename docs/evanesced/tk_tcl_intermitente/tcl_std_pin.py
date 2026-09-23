# -*- coding: utf-8 -*-
# This code was generated with the assistance of Claude Opus 5.5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# SPDX-License-Identifier: GPL-3.0-or-later
"""
PROTOTIPO del arreglo (docs/tk_tcl_intermitente.md SS7). Se carga como plugin de
pytest (`-p tcl_std_pin`) o se importa antes del primer Tk.

Tcl envuelve una sola vez por hilo los HANDLE de stdin/stdout/stderr y guarda sus
valores (win/tclWinChan.c). pytest --capture=fd los cierra con dup2 en cada fase, Windows
reusa los valores, y Tcl confunde un .tcl recien abierto con su viejo stdout. El
arreglo: que los handles que Tcl fija sean TRES NUL privados que nadie cierra nunca.
"""
import sys

if sys.platform == "win32":
    import ctypes
    import tkinter
    from ctypes import wintypes

    _k32 = ctypes.windll.kernel32
    _k32.GetStdHandle.restype = wintypes.HANDLE
    _k32.GetStdHandle.argtypes = [wintypes.DWORD]
    _k32.SetStdHandle.argtypes = [wintypes.DWORD, wintypes.HANDLE]
    _k32.CreateFileW.restype = wintypes.HANDLE
    _k32.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                                 ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD,
                                 wintypes.HANDLE]
    _STD = [ctypes.c_uint32(n).value for n in (-10, -11, -12)]   # IN, OUT, ERR
    _RW, _SHARE, _OPEN_EXISTING = 0xC0000000, 0x3, 3

    _reales = [_k32.GetStdHandle(s) for s in _STD]
    # UNO por canal: tres canales sobre el mismo handle chocan en la misma lista.
    _nul = [_k32.CreateFileW("NUL", _RW, _SHARE, None, _OPEN_EXISTING, 0, None)
            for _ in _STD]
    for s, h in zip(_STD, _nul):
        _k32.SetStdHandle(s, h)
    try:
        _TCL = tkinter.Tcl()          # vive todo el proceso: fija los canales
        for canal in ("stdin", "stdout", "stderr"):
            _TCL.eval("fconfigure %s" % canal)
    finally:
        for s, h in zip(_STD, _reales):
            _k32.SetStdHandle(s, h)
