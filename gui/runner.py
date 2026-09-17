#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Sonnet 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# Copyright (C) 2026 Simon Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.9.15
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. Distributed WITHOUT ANY WARRANTY. See the GNU
# General Public License for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
gui/runner.py - correr un worker en hilo aparte + validar/despachar errores.

Portado de autorem.py sin tocar la logica (docs/GUI_2.0_plan.md, paso 3):
`correr_con_reloj` (hilo + queue + poll) y los helpers que vivian junto a el
("Helpers reutilizables por las pestanias" en el Tk actual) -- validacion de
rutas/carpeta y el despacho de excepciones a un messagebox legible, INCLUIDA
la rama 'cruzados' de 1.9.10. `app.py` (paso 4) los usa para construir `ctx`
antes de lanzar el worker y para interpretar su resultado (SS3.2 del plan:
nada de Tk vars dentro del worker).
"""

import sys
import threading
import queue
from pathlib import Path

import customtkinter as ctk

import programas.rem_saludmental as sm
from gui.widgets import Reloj

_MSG_PERMISO = ("No pude escribir el resultado.\n\nSuele ser porque el archivo está "
                "ABIERTO en Excel (o bloqueado por OneDrive).\n\nCiérralo y reintenta.")

# RAYEN/IRIS exportan en .xls, .csv, .html y .xlsx; la herramienta lee SOLO .xlsx.
_MSG_NO_XLSX = (
    "El archivo no es un Excel .xlsx válido.\n\n"
    "RAYEN/IRIS entregan varios formatos (.xls antiguo, .csv, .html) y esta "
    "herramienta lee SOLO .xlsx.\n\n"
    "Ábrelo en Excel y usa «Guardar como» -> «Libro de Excel (.xlsx)», y carga ese.\n"
    "(Si un .xlsx te da este error, suele ser un .html/.xls disfrazado: mismo arreglo.)")

_FIN = object()   # centinela de fin de trabajo en la cola del runner


def dir_salida_default():
    """Carpeta de salida por defecto: donde esta el .exe (empaquetado) o el cwd."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path.cwd()


def slim_por_defecto():
    """Ruta del Maestro SLIM que shippea el repo/exe (`maestro_slim.csv.gz`), o
    None. Busca en el bundle de PyInstaller (si esta congelado) y junto al
    codigo. Vive en `catalogos/` (feedback del autor, sep-2026: es un
    catalogo actividad<->estamento<->REM igual que cie10/eno/ges, no un
    ejemplo anonimizado como el resto de `refs_tablas/`) -- ver autoREM.spec
    y tools/slim_maestro.py, que tienen que apuntar al mismo lugar."""
    cands = []
    if getattr(sys, "frozen", False):
        base = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
        cands += [base / "catalogos" / "maestro_slim.csv.gz",
                  Path(sys.executable).parent / "maestro_slim.csv.gz"]
    cands.append(Path(__file__).resolve().parent.parent / "catalogos" / "maestro_slim.csv.gz")
    return next((str(c) for c in cands if c.exists()), None)


def abrir_carpeta(carpeta):
    from programas.rem_utils import abrir_carpeta as _abrir
    _abrir(carpeta)


def valida_ruta(ruta, messagebox):
    """Valida que la ruta exista. Devuelve Path o None (avisa con messagebox)."""
    ruta = (ruta or "").strip().strip('"').strip("'")
    if not ruta:
        messagebox.showwarning("Falta el archivo", "Primero elige el Excel.")
        return None
    p = Path(ruta)
    if not p.exists():
        messagebox.showerror("No encontrado", f"No encuentro el archivo:\n{p}")
        return None
    return p


def valida_carpeta(ruta, messagebox, defecto=None):
    """Valida la carpeta de salida. Si `ruta` esta vacia, cae a `defecto` (la
    carpeta del archivo de entrada) y, si tampoco hay, a `dir_salida_default()`.
    Devuelve Path o None."""
    ruta = (ruta or "").strip().strip('"').strip("'")
    p = Path(ruta) if ruta else (Path(defecto) if defecto else dir_salida_default())
    if not p.exists() or not p.is_dir():
        messagebox.showerror("Carpeta inválida", f"No existe la carpeta de salida:\n{p}")
        return None
    return p


def es_error_formato(e):
    """True si la excepcion viene de intentar abrir algo que NO es un .xlsx
    real (extension no soportada por openpyxl, o zip corrupto = html/xls
    disfrazado)."""
    import zipfile
    try:
        from openpyxl.utils.exceptions import InvalidFileException
    except Exception:   # noqa: BLE001
        InvalidFileException = ()
    return isinstance(e, (zipfile.BadZipFile,) + ((InvalidFileException,) if InvalidFileException else ()))


def error_inesperado(e, log, messagebox):
    import traceback
    log(f"[ERROR INESPERADO] {type(e).__name__}: {e}")   # legible aunque no haya traceback vivo
    tb = traceback.format_exc()
    if tb and not tb.startswith("NoneType"):   # en hilo worker format_exc() da 'NoneType: None'
        log(tb)
    messagebox.showerror(
        "Error inesperado",
        f"Ocurrió un error no previsto:\n\n{type(e).__name__}: {e}\n\n"
        "Copia el texto del registro y pásaselo a Simón.")


def manejar_error(e, log, messagebox):
    """Despacha una excepcion de procesamiento a un messagebox claro (hilo
    GUI). Incluye ArchivoInvalido (p.ej. la guarda multi-hoja, o 'cruzados'
    desde 1.9.10) sin volcar traceback feo."""
    if isinstance(e, ImportError):
        messagebox.showerror("Falta una librería", f"Este módulo necesita pandas:\n{e}")
    elif isinstance(e, PermissionError):
        log("[PERMISO DENEGADO] archivo abierto en Excel / OneDrive")
        messagebox.showerror("Permiso denegado", _MSG_PERMISO)
    elif isinstance(e, sm.ArchivoInvalido):
        cruce = getattr(e, "categoria", "") == "cruzados"
        log(f"[{'archivos cruzados' if cruce else 'archivo inválido'}] {e}")
        messagebox.showerror("Archivos cruzados" if cruce else "Archivo inválido", str(e))
    elif es_error_formato(e):
        log(f"[formato no soportado] {e}")
        messagebox.showerror("No es un .xlsx", _MSG_NO_XLSX)
    else:
        error_inesperado(e, log, messagebox)


def correr_con_reloj(root, barra, btn, log, trabajo, al_terminar):
    """Corre `trabajo(log)` en un HILO aparte para que la ventana NO se
    congele. Muestra el reloj de arena girando + 'Procesando...' y vuelca el
    log en vivo. Al terminar llama `al_terminar(resultado, error)` en el hilo
    de la GUI (uno es None). `trabajo` debe usar SOLO el `log` que recibe
    (thread-safe); no tocar widgets (SS3.2 del plan)."""
    q = queue.Queue()
    estado = {}

    def log_seguro(msg=""):
        q.put(str(msg))          # el worker solo encola; la GUI escribe el widget

    def worker():
        try:
            estado["res"] = trabajo(log_seguro)
        except Exception as e:   # noqa: BLE001  (se re-despacha en el hilo GUI)
            estado["err"] = e
        finally:
            q.put(_FIN)

    btn.configure(state="disabled")
    reloj = Reloj(barra, root).start(side="left", padx=(10, 4))
    lbl = ctk.CTkLabel(barra, text="Procesando…  (puede tardar ~1 min)")
    lbl.pack(side="left")
    threading.Thread(target=worker, daemon=True).start()

    def poll():
        try:
            while True:
                item = q.get_nowait()
                if item is _FIN:
                    reloj.stop(); lbl.destroy(); btn.configure(state="normal")
                    al_terminar(estado.get("res"), estado.get("err"))
                    return
                log(item)
        except queue.Empty:
            pass
        root.after(80, poll)
    root.after(80, poll)
