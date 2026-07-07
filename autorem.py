#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.2.0
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

Arma la ventana, deja elegir el FORMATO del reporte de entrada (IRIS o
Administrativo) y las TAREAS a ejecutar (egresos/ingresos), y orquesta la
corrida. Cada tarea vive en su propio módulo HEADLESS y se registra vía su
descriptor TAREA. El formato es un 'perfil' de rem_saludmental.

Se carga el workbook UNA vez y cada tarea agrega su hoja -> un solo
«…_procesado.xlsx» con una hoja por tarea.

Para sumar una tarea nueva: impórtala y agrégala a MODULOS.

USO:
  - Doble-clic al .exe / .py                 -> ventana (GUI).
  - Arrastra el .xlsx ENCIMA del .exe / .py  -> ventana con la ruta cargada.
  - Terminal:  python autorem.py --cli entrada.xlsx
                    [--formato iris|administrativo] [--tarea ID[,ID2,...]]
"""

import sys
from pathlib import Path

from programas.rem_utils import VERSION
import programas.rem_saludmental as sm

# ── Registro de módulos de tarea ──────────────────────────────────────
from modulos import rem_a05_egresos
from modulos import rem_a05_ingresos

MODULOS = [rem_a05_egresos, rem_a05_ingresos]

TAREAS = [m.TAREA for m in MODULOS]
PERFILES = sm.PERFILES


def buscar_tarea(tarea_id):
    for t in TAREAS:
        if t["id"] == tarea_id:
            return t
    return None


def _forzar_utf8_stdout():
    """En consola Windows (cp1252) los símbolos ▶ · → «» ✔ revientan con
    UnicodeEncodeError. Forzar UTF-8 en stdout/stderr lo evita (no afecta a la GUI)."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


# ── Orquestación (compartida GUI/CLI) ─────────────────────────────────
def _correr_tareas(tareas, entrada, perfil, log=print):
    """Carga el workbook UNA vez (validando contra `perfil`), cada tarea agrega
    su hoja, y guarda UN solo «…_procesado.xlsx». Devuelve (resultados, salida)."""
    wb, ws = sm.abrir_validado(entrada, perfil)
    resultados = []
    for tarea in tareas:
        log(f"▶ {tarea['nombre']}   ({perfil['nombre']})")
        res = tarea["agregar"](wb, ws, perfil, log=log)
        resultados.append((tarea, res))

    salida = entrada.with_name(entrada.stem + "_procesado.xlsx")
    wb.save(salida)
    log(f"[ok] guardado: {salida}")
    return resultados, str(salida)


def _resumen_texto(resultados, salida):
    """Arma el texto de confirmación a partir de (resultados, salida)."""
    partes = []
    for tarea, res in resultados:
        det = ""
        if "por_tipo" in res:
            det = " · ".join(f"{t}: {c}" for t, c in res["por_tipo"].items())
        linea = f"{tarea['nombre']}  →  hoja «{res.get('hoja', '?')}»: {res.get('total', '?')} filas"
        if det:
            linea += f"  ({det})"
        partes.append(linea)
    texto = "Listo.\n" + "\n".join(partes)
    if salida:
        texto += f"\n\nGuardado en:\n{salida}"
    return texto


# ╔═══════════════════════════════════════════════════════════════════╗
# ║  INTERFAZ GRÁFICA (Tkinter)                                        ║
# ╚═══════════════════════════════════════════════════════════════════╝
def lanzar_gui(ruta_inicial=""):
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext

    root = tk.Tk()
    root.title(f"autoREM {VERSION} — Tabulador del REM (Salud Mental)")
    root.geometry("820x720")
    root.minsize(720, 640)

    cont = ttk.Frame(root, padding=14)
    cont.pack(fill="both", expand=True)

    ttk.Label(cont, text=f"autoREM {VERSION} — Tabulador del REM (Salud Mental)",
              font=("Segoe UI", 13, "bold")).pack(anchor="w")

    instr = (
        "1.  Descarga el Excel del formulario «Control de Salud Mental» (IRIS o Administrativo).\n"
        "A) IRIS: Formularios RAYEN -> Control de Salud Mental. -> Todos los metacampos, Situacion TODOS, estado AMBOS.\n"
        "B) RAYEN: Herramientas -> Informe Estadistico -> Impresion Formularios Clinicos. Reporte Administrativo.\n"
        "2.  Elige abajo el FORMATO que descargaste y el archivo.\n"
        "3.  Marca la(s) TAREA(s) y presiona «Procesar». Se crea una copia\n"
        "     «…_procesado.xlsx» con una hoja por tarea. Tu archivo original NO se modifica.\n"
        "⚠  No discrimina fecha, debe seleccionarse correctamente al bajar el reporte.\n"
        "Programa de código abierto, con licencia GPL-3.0 y posterior (ver LICENSE)."
    )
    caja_instr = ttk.LabelFrame(cont, text="Instrucciones", padding=8)
    caja_instr.pack(fill="x", pady=(10, 8))
    ttk.Label(caja_instr, text=instr, justify="left").pack(anchor="w")

    # — Selector de FORMATO (perfil) —
    caja_fmt = ttk.LabelFrame(cont, text="Formato del reporte de entrada", padding=8)
    caja_fmt.pack(fill="x", pady=(2, 6))
    var_perfil = tk.StringVar(value=PERFILES[0]["id"])
    lbl_disc = ttk.Label(caja_fmt, text="", justify="left", foreground="#a05a00")

    def on_perfil_change():
        p = sm.perfil_por_id(var_perfil.get())
        lbl_disc.configure(text=(p["disclaimer"] if p else ""))

    for p in PERFILES:
        ttk.Radiobutton(caja_fmt, text=p["nombre"], value=p["id"],
                        variable=var_perfil, command=on_perfil_change).pack(anchor="w")
    lbl_disc.pack(anchor="w", pady=(4, 0))

    # — Selector de archivo —
    fila_arch = ttk.Frame(cont)
    fila_arch.pack(fill="x", pady=(6, 6))
    ttk.Label(fila_arch, text="Archivo Excel:").pack(side="left")
    var_ruta = tk.StringVar(value=ruta_inicial)
    entry = ttk.Entry(fila_arch, textvariable=var_ruta)
    entry.pack(side="left", fill="x", expand=True, padx=6)

    def examinar():
        f = filedialog.askopenfilename(
            title="Elige el export del formulario Control de Salud Mental",
            filetypes=[("Excel", "*.xlsx"), ("Todos", "*.*")],
        )
        if f:
            var_ruta.set(f)

    ttk.Button(fila_arch, text="Examinar…", command=examinar).pack(side="left")

    # — Selector de TAREAS —
    caja_tareas = ttk.LabelFrame(cont, text="Tareas a ejecutar", padding=8)
    caja_tareas.pack(fill="x", pady=(2, 6))
    checks = {}   # tarea_id -> (tarea, BooleanVar)
    for t in TAREAS:
        var = tk.BooleanVar(value=True)   # por defecto todas marcadas
        ttk.Checkbutton(caja_tareas, text=t["nombre"], variable=var).pack(anchor="w")
        checks[t["id"]] = (t, var)

    # — Log —
    caja_log = ttk.LabelFrame(cont, text="Registro", padding=6)
    caja_log.pack(fill="both", expand=True, pady=(6, 8))
    txt = scrolledtext.ScrolledText(caja_log, height=10, wrap="word",
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
                                   "Primero elige el Excel del formulario.")
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

        perfil = sm.perfil_por_id(var_perfil.get())
        if perfil is None:
            messagebox.showerror("Formato", "Elige un formato de reporte.")
            return
        if perfil["disclaimer"]:
            log(perfil["disclaimer"])
            log("")

        btn_proc.configure(state="disabled")
        try:
            resultados, salida = _correr_tareas(seleccionadas, entrada, perfil, log)
        except sm.ArchivoInvalido as e:
            titulo = {"administrativo": "Parece Administrativo, no IRIS",
                      "iris": "Parece IRIS, no Administrativo"}.get(
                          e.categoria, "Formato no reconocido")
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
        resumen = _resumen_texto(resultados, salida)
        log("")
        log("✔ " + resumen.replace("\n", " | "))
        if messagebox.askyesno("Listo", resumen + "\n\n¿Abrir la carpeta del resultado?"):
            if salida:
                _abrir_carpeta(Path(salida).parent)

    # — Botonera —
    fila_btn = ttk.Frame(cont)
    fila_btn.pack(fill="x")
    btn_proc = ttk.Button(fila_btn, text="Procesar", command=on_procesar)
    btn_proc.pack(side="left")
    ttk.Button(fila_btn, text="Salir", command=root.destroy).pack(side="right")

    on_perfil_change()   # pinta el disclaimer inicial (vacío para IRIS)
    if not sm.OPENPYXL_OK:
        log("⚠ Falta 'openpyxl'. Instálalo con: pip install openpyxl")

    root.mainloop()


def _abrir_carpeta(carpeta):
    from programas.rem_utils import abrir_carpeta
    abrir_carpeta(carpeta)


# ╔═══════════════════════════════════════════════════════════════════╗
# ║  MODO CONSOLA (experto) y ARRANQUE                                 ║
# ╚═══════════════════════════════════════════════════════════════════╝
def main_cli(args):
    # args: entrada.xlsx [--formato iris|administrativo] [--tarea ID[,ID2,...]]
    _forzar_utf8_stdout()

    perfil = PERFILES[0]
    if "--formato" in args:
        i = args.index("--formato")
        if i + 1 >= len(args):
            print("ERROR: --formato requiere un ID (iris | administrativo).")
            return 2
        perfil = sm.perfil_por_id(args[i + 1])
        if perfil is None:
            print(f"ERROR: formato inválido. Disponibles: "
                  f"{', '.join(p['id'] for p in PERFILES)}")
            return 2
        args = args[:i] + args[i + 2:]

    tarea_ids = None
    if "--tarea" in args:
        i = args.index("--tarea")
        if i + 1 >= len(args):
            print("ERROR: --tarea requiere uno o más IDs (separados por coma).")
            return 2
        tarea_ids = [s for s in args[i + 1].split(",") if s]
        args = args[:i] + args[i + 2:]

    if not args:
        ids = ", ".join(t["id"] for t in TAREAS)
        fmts = ", ".join(p["id"] for p in PERFILES)
        print("USO: python autorem.py --cli entrada.xlsx "
              "[--formato iris|administrativo] [--tarea ID[,ID2,...]]")
        print(f"Formatos: {fmts}  (por defecto: {PERFILES[0]['id']})")
        print(f"Tareas:   {ids}  (por defecto: la primera)")
        return 2

    if tarea_ids:
        seleccionadas = []
        for tid in tarea_ids:
            t = buscar_tarea(tid)
            if t is None:
                print(f"ERROR: no existe la tarea '{tid}'. "
                      f"Disponibles: {', '.join(x['id'] for x in TAREAS)}")
                return 2
            seleccionadas.append(t)
    else:
        seleccionadas = [TAREAS[0]]

    entrada = Path(args[0].strip().strip('"').strip("'"))
    if not entrada.exists():
        print(f"ERROR: no encuentro el archivo:\n  {entrada}")
        return 1

    if perfil["disclaimer"]:
        print(perfil["disclaimer"] + "\n")
    try:
        resultados, salida = _correr_tareas(seleccionadas, entrada, perfil)
    except sm.ArchivoInvalido as e:
        print(f"\n[ARCHIVO EQUIVOCADO — {e.categoria}]\n{e}")
        return 1
    except PermissionError:
        print("\n[PERMISO DENEGADO] ¿está abierto en Excel? Ciérralo y reintenta.")
        return 1
    print(_resumen_texto(resultados, salida))
    return 0


def main():
    _forzar_utf8_stdout()
    argv = sys.argv[1:]

    # Modo consola explícito para usuarios avanzados.
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
