#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.4
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
autorem.py — dispatcher (GUI + CLI) del proyecto autoREM.

Arma la ventana, muestra el selector de TAREAS agrupadas por reporte de entrada,
y orquesta la corrida. Cada tarea vive en su propio módulo HEADLESS (sin GUI) y
se registra aquí a través de su descriptor TAREA.

Tareas que leen el MISMO reporte se pueden marcar juntas. Reportes distintos
(IRIS, PowerBI, atenciones, ...) son grupos separados en el selector.

Para sumar una tarea nueva:  impórtala abajo y agrega su .TAREA a TAREAS
(y su .REPORTE a REPORTES si es un reporte de entrada nuevo).

USO:
  - Doble-clic al .exe / .py                 -> ventana (GUI).
  - Arrastra el .xlsx ENCIMA del .exe / .py  -> ventana con la ruta cargada.
  - Terminal:  python autorem.py --cli entrada.xlsx [salida.xlsx] [--tarea ID]
"""

import sys
from pathlib import Path
from collections import OrderedDict

from rem_utils import OPENPYXL_OK, ArchivoInvalido, abrir_carpeta

# ── Registro de módulos de tarea ──────────────────────────────────────
import rem_a05_egresos

TAREAS = [
    rem_a05_egresos.TAREA,
]
REPORTES = {
    rem_a05_egresos.REPORTE["id"]: rem_a05_egresos.REPORTE,
}


def tareas_por_reporte(tareas):
    """Agrupa las tareas por su reporte de entrada, conservando el orden."""
    grupos = OrderedDict()
    for t in tareas:
        grupos.setdefault(t["reporte"], []).append(t)
    return grupos


def nombre_reporte(rep_id):
    rep = REPORTES.get(rep_id)
    return rep["nombre"] if rep else rep_id


def buscar_tarea(tarea_id):
    for t in TAREAS:
        if t["id"] == tarea_id:
            return t
    return None


# ╔═══════════════════════════════════════════════════════════════════╗
# ║  INTERFAZ GRÁFICA (Tkinter)                                        ║
# ╚═══════════════════════════════════════════════════════════════════╝
def lanzar_gui(ruta_inicial=""):
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext

    root = tk.Tk()
    root.title("autoREM — Tabulador del REM (Salud Mental)")
    root.geometry("800x640")
    root.minsize(700, 580)

    cont = ttk.Frame(root, padding=14)
    cont.pack(fill="both", expand=True)

    # — Título —
    ttk.Label(cont, text="autoREM — Tabulador del REM (Salud Mental)",
              font=("Segoe UI", 13, "bold")).pack(anchor="w")

    # — Instrucciones —
    instr = (
        "1.  Descarga el Excel desde IRIS → Formularios RAYEN → «Control de Salud Mental».\n"
        "2.  Elige ese archivo abajo (botón «Examinar…» o pega la ruta).\n"
        "3.  Marca la(s) tarea(s) y presiona «Procesar». Se crea una copia\n"
        "     «…_procesado.xlsx» con una hoja por tarea. Tu archivo original NO se modifica.\n"
        "⚠  No sirve el reporte «administrativo»: tiene otro formato.\n"
        "⚠  No discrimina fecha"
    )
    caja_instr = ttk.LabelFrame(cont, text="Instrucciones", padding=8)
    caja_instr.pack(fill="x", pady=(10, 8))
    ttk.Label(caja_instr, text=instr, justify="left").pack(anchor="w")

    # — Selector de archivo —
    fila_arch = ttk.Frame(cont)
    fila_arch.pack(fill="x", pady=(2, 6))
    ttk.Label(fila_arch, text="Archivo Excel:").pack(side="left")
    var_ruta = tk.StringVar(value=ruta_inicial)
    entry = ttk.Entry(fila_arch, textvariable=var_ruta)
    entry.pack(side="left", fill="x", expand=True, padx=6)

    def examinar():
        f = filedialog.askopenfilename(
            title="Elige el export de IRIS (Control de Salud Mental)",
            filetypes=[("Excel", "*.xlsx"), ("Todos", "*.*")],
        )
        if f:
            var_ruta.set(f)

    ttk.Button(fila_arch, text="Examinar…", command=examinar).pack(side="left")

    # — Selector de tareas (agrupadas por reporte de entrada) —
    caja_tareas = ttk.LabelFrame(cont, text="Tareas a ejecutar", padding=8)
    caja_tareas.pack(fill="x", pady=(2, 6))
    checks = OrderedDict()   # tarea_id -> (tarea, BooleanVar)
    solo_una = len(TAREAS) == 1
    for rep_id, tareas_grp in tareas_por_reporte(TAREAS).items():
        ttk.Label(caja_tareas, text=nombre_reporte(rep_id),
                  font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(4, 0))
        for t in tareas_grp:
            var = tk.BooleanVar(value=solo_una)   # si hay una sola tarea, va marcada
            ttk.Checkbutton(caja_tareas, text=t["nombre"], variable=var).pack(
                anchor="w", padx=(16, 0))
            checks[t["id"]] = (t, var)

    # — Log —
    caja_log = ttk.LabelFrame(cont, text="Registro", padding=6)
    caja_log.pack(fill="both", expand=True, pady=(6, 8))
    txt = scrolledtext.ScrolledText(caja_log, height=11, wrap="word",
                                    font=("Consolas", 9), state="disabled")
    txt.pack(fill="both", expand=True)

    def log(msg=""):
        txt.configure(state="normal")
        txt.insert("end", str(msg) + "\n")
        txt.see("end")
        txt.configure(state="disabled")
        root.update_idletasks()

    def limpiar_log():
        txt.configure(state="normal")
        txt.delete("1.0", "end")
        txt.configure(state="disabled")

    # — Acción principal —
    def on_procesar():
        limpiar_log()
        ruta = var_ruta.get().strip().strip('"').strip("'")
        if not ruta:
            messagebox.showwarning("Falta el archivo",
                                   "Primero elige el Excel descargado desde IRIS.")
            return
        entrada = Path(ruta)
        if not entrada.exists():
            messagebox.showerror("No encontrado", f"No encuentro el archivo:\n{entrada}")
            return
        seleccionadas = [t for (t, var) in checks.values() if var.get()]
        if not seleccionadas:
            messagebox.showwarning("Sin tareas", "Marca al menos una tarea a ejecutar.")
            return
        if entrada.suffix.lower() not in (".xlsx", ".xlsm"):
            if not messagebox.askyesno(
                "¿Seguro?",
                f"El archivo no termina en .xlsx ({entrada.suffix}).\n"
                "¿Intento procesarlo igual?"):
                return

        btn_proc.configure(state="disabled")
        try:
            resultados = _correr_tareas(seleccionadas, entrada, log)
        except ArchivoInvalido as e:
            titulo = ("Archivo equivocado (reporte administrativo)"
                      if e.categoria == "administrativo" else "Formato no reconocido")
            log(f"[ARCHIVO EQUIVOCADO] {e.categoria}")
            messagebox.showerror(titulo, str(e))
            return
        except PermissionError:
            msg = ("No pude escribir el resultado.\n\n"
                   "Suele ser porque el archivo está ABIERTO en Excel "
                   "(o bloqueado por OneDrive).\n\n"
                   "Ciérralo en Excel y vuelve a intentar.")
            log("[PERMISO DENEGADO] archivo abierto en Excel / OneDrive")
            messagebox.showerror("Permiso denegado", msg)
            return
        except ImportError as e:
            log(f"[DEPENDENCIA] {e}")
            messagebox.showerror("Falta una librería", str(e))
            return
        except Exception as e:
            import traceback
            log("[ERROR INESPERADO]")
            log(traceback.format_exc())
            messagebox.showerror(
                "Error inesperado",
                f"Ocurrió un error no previsto:\n\n{e}\n\n"
                "Copia el texto del registro y pásaselo a Simón.")
            return
        finally:
            btn_proc.configure(state="normal")

        # éxito
        resumen, carpeta = _resumen_texto(resultados)
        log("")
        log("✔ " + resumen.replace("\n", " | "))
        if messagebox.askyesno("Listo", resumen + "\n\n¿Abrir la carpeta del resultado?"):
            if carpeta:
                abrir_carpeta(carpeta)

    # — Botonera —
    fila_btn = ttk.Frame(cont)
    fila_btn.pack(fill="x")
    btn_proc = ttk.Button(fila_btn, text="Procesar", command=on_procesar)
    btn_proc.pack(side="left")
    ttk.Button(fila_btn, text="Salir", command=root.destroy).pack(side="right")

    if not OPENPYXL_OK:
        log("⚠ Falta 'openpyxl'. Instálalo con: pip install openpyxl")

    root.mainloop()


# ── Orquestación (compartida GUI/CLI) ─────────────────────────────────
def _correr_tareas(tareas, entrada, log=print):
    """Ejecuta las tareas seleccionadas sobre `entrada`. Hoy cada tarea hace su
    propia carga+guardado; para una sola tarea el resultado es «…_procesado.xlsx».

    TODO (llega con el 2º módulo, ver CLAUDE.md §12): cuando haya >1 tarea del
    MISMO reporte, cargar el workbook una vez, dejar que cada tarea agregue su
    hoja y guardar UN solo archivo con todas las hojas.
    """
    salida = entrada.with_name(entrada.stem + "_procesado.xlsx")
    resultados = []
    for tarea in tareas:
        log(f"▶ {tarea['nombre']}  —  {entrada.name}")
        res = tarea["correr"](entrada, salida, log=log)
        resultados.append((tarea, res))
    return resultados


def _resumen_texto(resultados):
    """Arma el texto de confirmación y devuelve (texto, carpeta_salida | None)."""
    partes = []
    carpeta = None
    for tarea, res in resultados:
        sal = res.get("salida")
        if sal:
            carpeta = Path(sal).parent
        det = ""
        if "por_tipo" in res:
            det = " · ".join(f"{t}: {c}" for t, c in res["por_tipo"].items())
        linea = f"{tarea['nombre']}: {res.get('total', '?')} filas"
        if det:
            linea += f"  ({det})"
        partes.append(linea)
    texto = "Listo.\n" + "\n".join(partes)
    if carpeta:
        texto += f"\n\nGuardado en:\n{carpeta}"
    return texto, carpeta


# ╔═══════════════════════════════════════════════════════════════════╗
# ║  MODO CONSOLA (experto) y ARRANQUE                                 ║
# ╚═══════════════════════════════════════════════════════════════════╝
def main_cli(args):
    # args: entrada [salida] [--tarea ID]
    tarea_id = None
    if "--tarea" in args:
        i = args.index("--tarea")
        if i + 1 >= len(args):
            print("ERROR: --tarea requiere un ID.")
            return 2
        tarea_id = args[i + 1]
        args = args[:i] + args[i + 2:]

    if not args:
        ids = ", ".join(t["id"] for t in TAREAS)
        print("USO: python autorem.py --cli entrada.xlsx [salida.xlsx] [--tarea ID]")
        print(f"Tareas disponibles: {ids}")
        return 2

    tarea = buscar_tarea(tarea_id) if tarea_id else TAREAS[0]
    if tarea is None:
        print(f"ERROR: no existe la tarea '{tarea_id}'. "
              f"Disponibles: {', '.join(t['id'] for t in TAREAS)}")
        return 2

    entrada = Path(args[0].strip().strip('"').strip("'"))
    salida = (Path(args[1]) if len(args) > 1
              else entrada.with_name(entrada.stem + "_procesado.xlsx"))
    if not entrada.exists():
        print(f"ERROR: no encuentro el archivo:\n  {entrada}")
        return 1
    try:
        tarea["correr"](entrada, salida)
    except ArchivoInvalido as e:
        print(f"\n[ARCHIVO EQUIVOCADO — {e.categoria}]\n{e}")
        return 1
    except PermissionError:
        print("\n[PERMISO DENEGADO] ¿está abierto en Excel? Ciérralo y reintenta.")
        return 1
    return 0


def main():
    argv = sys.argv[1:]

    # Modo consola explícito para usuarios avanzados: --cli entrada [salida]
    if argv and argv[0] in ("--cli", "-c"):
        sys.exit(main_cli(argv[1:]))

    # Si arrastraron un archivo encima del .exe/.py, Windows lo pasa como argv[1].
    ruta_inicial = ""
    if argv:
        cand = argv[0].strip().strip('"').strip("'")
        if cand and not cand.startswith("-"):
            ruta_inicial = cand

    try:
        lanzar_gui(ruta_inicial)
    except Exception as e:
        # Si Tkinter no está disponible (raro), caemos a un modo texto mínimo.
        print(f"No pude abrir la ventana ({e}).")
        print("Modo texto: pega la ruta del .xlsx (Enter para salir).")
        try:
            ruta = input("> ").strip().strip('"').strip("'")
        except EOFError:
            return
        if ruta:
            sys.exit(main_cli([ruta]))


if __name__ == "__main__":
    main()
