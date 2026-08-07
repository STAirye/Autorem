#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.7.1
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

La GUI tiene una PESTAÑA por módulo/reporte (cada una autocontenida: su archivo,
sus opciones, sus instrucciones y su log). Al sumar un módulo se agrega su pestaña.
Hoy:
  - «REM A05 · Egresos / Ingresos»  (formulario Control de Salud Mental; perfil
    IRIS/Administrativo + tareas egresos/ingresos → un .xlsx con una hoja por tarea).
  - «REM A03 D.3 · Screening»       (instrumentos PSC/PSC-Y/GHQ-12; autodetecta
    formato e instrumento por contenido).

USO:
  - Doble-clic al .exe / .py                 -> ventana (GUI, pestaña A05 por defecto).
  - Arrastra el .xlsx ENCIMA del .exe / .py  -> GUI con la ruta cargada en A05.
  - Terminal (solo A05):  python autorem.py --cli entrada.xlsx
                    [--formato iris|administrativo] [--tarea ID[,ID2,...]]
"""

import sys
from pathlib import Path

from programas.rem_utils import VERSION
import programas.rem_saludmental as sm

# ── Registro de módulos de tarea ──────────────────────────────────────
from modulos import rem_a05_o_egresos
from modulos import rem_a05_n_ingresos
import modulos.rem_a03_d3_instrumentos as screening   # reporte aparte (su propia pestaña)

MODULOS = [rem_a05_o_egresos, rem_a05_n_ingresos]

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
# ║  INTERFAZ GRÁFICA (Tkinter) — una pestaña por módulo/reporte       ║
# ╚═══════════════════════════════════════════════════════════════════╝
_MSG_PERMISO = ("No pude escribir el resultado.\n\nSuele ser porque el archivo está "
                "ABIERTO en Excel (o bloqueado por OneDrive).\n\nCiérralo y reintenta.")

_AVISO_SIN_MODIFICAR = ("⚠  Carga los archivos TAL COMO los descargas de RAYEN/IRIS: "
                        "sin abrirlos, editarlos ni re-guardarlos.\n"
                        "     Un export modificado (cambio de formato, columnas, hojas) "
                        "puede fallar en silencio o dar cifras erróneas.")


def _aviso_sin_modificar(parent):
    """Recordatorio (todas las pestañas) de cargar los exports SIN modificar."""
    from tkinter import ttk
    ttk.Label(parent, text=_AVISO_SIN_MODIFICAR, justify="left",
              foreground="#a05a00").pack(anchor="w", pady=(0, 6))


def _tab_scroll(nb, texto):
    """Pestaña con SCROLL vertical, para contenido más alto que la ventana (p.ej. al
    desplegar los cuestionarios en Actividades). Reemplaza a `ttk.Frame(nb, padding=12)
    + nb.add(...)`: devuelve el frame INTERNO donde se arma el contenido.

    KNOWN ISSUE (no se arregla, a propósito): al DESPLEGAR crece y aparece el scroll OK,
    pero al OCULTAR (destickear cuestionarios) el scrollregion NO se encoge de vuelta
    (queda scroll sobrante). Es el clásico baile Canvas+scrollregion de tkinter; se
    resuelve gratis en la GUI 2.0 con customtkinter (CTkScrollableFrame). No vale la
    pena pelearlo acá."""
    import tkinter as tk
    from tkinter import ttk
    outer = ttk.Frame(nb)
    nb.add(outer, text=texto)
    canvas = tk.Canvas(outer, highlightthickness=0)
    vsb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    inner = ttk.Frame(canvas, padding=12)
    win = canvas.create_window((0, 0), window=inner, anchor="nw")
    inner.bind("<Configure>", lambda _e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfigure(win, width=e.width))

    def _wheel(e):
        canvas.yview_scroll(int(-(e.delta or 0) / 120), "units")
    canvas.bind("<Enter>", lambda _e: canvas.bind_all("<MouseWheel>", _wheel))
    canvas.bind("<Leave>", lambda _e: canvas.unbind_all("<MouseWheel>"))
    return inner


def lanzar_gui(ruta_inicial=""):
    import tkinter as tk
    from tkinter import ttk

    root = tk.Tk()
    root.title(f"autoREM {VERSION} — Tabulador del REM")
    root.geometry("880x780")
    root.minsize(760, 680)

    ttk.Label(root, text=f"autoREM {VERSION}", font=("Segoe UI", 12, "bold")).pack(
        anchor="w", padx=12, pady=(10, 0))
    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True, padx=8, pady=8)

    _tab_a05(nb, root, ruta_inicial)
    _tab_a03(nb, root)
    _tab_a23(nb, root)
    _tab_sm(nb, root)

    root.mainloop()


# ── Helpers reutilizables por las pestañas ────────────────────────────
def _crear_log(parent, root, height=10):
    """Caja de log. Devuelve (log, limpiar)."""
    from tkinter import ttk, scrolledtext
    caja = ttk.LabelFrame(parent, text="Registro", padding=6)
    caja.pack(fill="both", expand=True, pady=(6, 8))
    txt = scrolledtext.ScrolledText(caja, height=height, wrap="word",
                                    font=("Consolas", 9), state="disabled")
    txt.pack(fill="both", expand=True)

    def log(msg=""):
        txt.configure(state="normal")
        txt.insert("end", str(msg) + "\n")
        txt.see("end")
        txt.configure(state="disabled")
        root.update_idletasks()

    def limpiar():
        txt.configure(state="normal")
        txt.delete("1.0", "end")
        txt.configure(state="disabled")

    return log, limpiar


def _fila_archivo(parent, var_ruta, titulo):
    """Fila 'Archivo Excel: [___] [Examinar…]'."""
    from tkinter import ttk, filedialog
    fila = ttk.Frame(parent)
    fila.pack(fill="x", pady=(6, 6))
    ttk.Label(fila, text="Archivo Excel:").pack(side="left")
    ttk.Entry(fila, textvariable=var_ruta).pack(side="left", fill="x", expand=True, padx=6)

    def examinar():
        f = filedialog.askopenfilename(
            title=titulo, filetypes=[("Excel", "*.xlsx"), ("Todos", "*.*")])
        if f:
            var_ruta.set(f)

    ttk.Button(fila, text="Examinar…", command=examinar).pack(side="left")


def _fila_archivos(parent, etiqueta, titulo):
    """Fila con selección de VARIOS archivos (histórico multi-año). Devuelve get()->list[str]."""
    from tkinter import ttk, filedialog
    fila = ttk.Frame(parent)
    fila.pack(fill="x", pady=(3, 3))
    ttk.Label(fila, text=etiqueta, width=30, anchor="w").pack(side="left")
    lbl = ttk.Label(fila, text="(ninguno)", foreground="#666")
    sel = []

    def examinar():
        fs = filedialog.askopenfilenames(title=titulo, filetypes=[("Excel", "*.xlsx"), ("Todos", "*.*")])
        if fs:
            sel[:] = list(fs)
            nombres = ", ".join(Path(f).name for f in sel)
            lbl.configure(text=f"{len(sel)}: " + (nombres[:70] + "…" if len(nombres) > 70 else nombres))

    ttk.Button(fila, text="Examinar…", command=examinar).pack(side="left")
    lbl.pack(side="left", padx=8)
    return lambda: list(sel)


def _separador_opcionales(parent, texto="Opcionales"):
    """Barra horizontal que separa visualmente los inputs OBLIGATORIOS (arriba) de
    los OPCIONALES (abajo). Se llama entre unos y otros al armar la pestaña."""
    from tkinter import ttk
    ttk.Separator(parent, orient="horizontal").pack(fill="x", pady=(8, 3))
    ttk.Label(parent, text=f"—  {texto}  —", foreground="#888").pack(anchor="w", pady=(0, 2))


def _dir_salida_default():
    """Carpeta de salida por defecto: donde está el .exe (empaquetado) o el cwd."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path.cwd()


def _fila_carpeta_salida(parent):
    """Fila 'Carpeta de salida: [___] [Examinar…]'. Devuelve get()->str (ruta)."""
    import tkinter as tk
    from tkinter import ttk, filedialog
    fila = ttk.Frame(parent)
    fila.pack(fill="x", pady=(3, 3))
    ttk.Label(fila, text="Carpeta de salida:", width=30, anchor="w").pack(side="left")
    var = tk.StringVar(value=str(_dir_salida_default()))
    ttk.Entry(fila, textvariable=var).pack(side="left", fill="x", expand=True, padx=6)

    def elegir():
        d = filedialog.askdirectory(title="Elige dónde guardar el resultado")
        if d:
            var.set(d)

    ttk.Button(fila, text="Examinar…", command=elegir).pack(side="left")
    return lambda: (var.get() or "").strip().strip('"').strip("'")


def _valida_ruta(ruta, messagebox):
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


def _valida_carpeta(ruta, messagebox):
    """Valida (o cae al default) la carpeta de salida. Devuelve Path o None."""
    ruta = (ruta or "").strip().strip('"').strip("'")
    p = Path(ruta) if ruta else _dir_salida_default()
    if not p.exists() or not p.is_dir():
        messagebox.showerror("Carpeta inválida", f"No existe la carpeta de salida:\n{p}")
        return None
    return p


def _error_inesperado(e, log, messagebox):
    import traceback
    log("[ERROR INESPERADO]")
    log(traceback.format_exc())
    messagebox.showerror(
        "Error inesperado",
        f"Ocurrió un error no previsto:\n\n{e}\n\n"
        "Copia el texto del registro y pásaselo a Simón.")


def _manejar_error(e, log, messagebox):
    """Despacha una excepción de procesamiento a un messagebox claro (hilo GUI).
    Incluye ArchivoInvalido (p.ej. la guarda multi-hoja) sin volcar traceback feo."""
    if isinstance(e, ImportError):
        messagebox.showerror("Falta una librería", f"Este módulo necesita pandas:\n{e}")
    elif isinstance(e, PermissionError):
        log("[PERMISO DENEGADO] archivo abierto en Excel / OneDrive")
        messagebox.showerror("Permiso denegado", _MSG_PERMISO)
    elif isinstance(e, sm.ArchivoInvalido):
        log(f"[archivo inválido] {e}")
        messagebox.showerror("Archivo inválido", str(e))
    else:
        _error_inesperado(e, log, messagebox)


def _slim_por_defecto():
    """Ruta del Maestro SLIM que shippea el repo/exe (`maestro_slim.csv.gz`), o None.
    Busca en el bundle de PyInstaller (si está congelado) y junto al código."""
    cands = []
    if getattr(sys, "frozen", False):
        base = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
        cands += [base / "refs tablas" / "maestro_slim.csv.gz",
                  Path(sys.executable).parent / "maestro_slim.csv.gz"]
    cands.append(Path(__file__).resolve().parent / "refs tablas" / "maestro_slim.csv.gz")
    return next((str(c) for c in cands if c.exists()), None)


_FIN = object()   # centinela de fin de trabajo en la cola del runner


class _Reloj:
    """Reloj de arena dibujado que GIRA: indicador indeterminado ('trabajando', sin
    porcentajes que mienten). Se anima en el hilo de la GUI (`root.after`), por eso
    sigue girando mientras el worker hace el trabajo pesado en OTRO hilo."""
    def __init__(self, parent, root, size=26):
        import tkinter as tk
        self.root = root
        self.size = size
        self.cv = tk.Canvas(parent, width=size, height=size, highlightthickness=0)
        self.ang = 0
        self._job = None

    def _dibujar(self):
        import math
        s, a = self.size, math.radians(self.ang)
        c, r = s / 2, s * 0.34
        self.cv.delete("all")

        def pt(dx, dy):
            return (c + dx * math.cos(a) - dy * math.sin(a),
                    c + dx * math.sin(a) + dy * math.cos(a))
        # Dos triángulos que se tocan en el centro = reloj de arena; al rotar, "gira".
        for tri in ([pt(-r, -r), pt(r, -r), pt(0, 0)],
                    [pt(-r, r), pt(r, r), pt(0, 0)]):
            self.cv.create_polygon([v for p in tri for v in p], fill="#c8801a", outline="#5a3200")

    def _tick(self):
        self._dibujar()
        self.ang = (self.ang + 15) % 360
        self._job = self.root.after(70, self._tick)

    def start(self, **pack):
        self.cv.pack(**pack)
        self._tick()
        return self

    def stop(self):
        if self._job:
            self.root.after_cancel(self._job)
            self._job = None
        self.cv.destroy()


def _correr_con_reloj(root, barra, btn, log, trabajo, al_terminar):
    """Corre `trabajo(log)` en un HILO aparte para que la ventana NO se congele.
    Muestra el reloj de arena girando + 'Procesando…' y vuelca el log en vivo. Al
    terminar llama `al_terminar(resultado, error)` en el hilo de la GUI (uno es None).
    `trabajo` debe usar SOLO el `log` que recibe (thread-safe); no tocar widgets."""
    import threading
    import queue
    from tkinter import ttk
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
    reloj = _Reloj(barra, root).start(side="left", padx=(10, 4))
    lbl = ttk.Label(barra, text="Procesando…  (puede tardar ~1 min)")
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


# ── Estamentos (REUTILIZABLE por cualquier flujo en formato Administrativo) ──
def _bloque_estamentos(parent):
    """Cuadro para cargar la tabla de estamentos ('Utilización de Cupos'), con el
    porqué y las instrucciones. Reutilizable por cualquier módulo que procese
    Administrativo. Devuelve get_ruta() -> str (ruta elegida, '' si nada)."""
    import tkinter as tk
    from tkinter import ttk
    caja = ttk.LabelFrame(parent, text="Estamentos (para formato Administrativo)", padding=8)
    caja.pack(fill="x", pady=(2, 6))
    ttk.Label(caja, justify="left", foreground="#a05a00", text=(
        "¿Por qué? El reporte Administrativo NO indica el estamento de quien atendió, "
        "solo el nombre.\nPara poder reportar por estamento hay que cargar, una vez, "
        "la tabla del equipo.")).pack(anchor="w")
    ttk.Label(caja, justify="left", text=(
        "En RAYEN Administrativo, descarga un reporte desde  Herramientas → Reportes "
        "Estadísticos → Otros → Utilización de Cupos,\ncon fecha de un día en que hubo "
        "atenciones de TODO tu equipo. Copia el reporte completo, pásalo a Excel y "
        "cárgalo aquí.")).pack(anchor="w", pady=(4, 4))
    var = tk.StringVar()
    _fila_archivo(caja, var, "Elige el reporte 'Utilización de Cupos'")
    return lambda: (var.get() or "").strip().strip('"').strip("'")


def _resolver_estamentos(root, faltantes, opciones):
    """Failsafe modal: por cada funcionario SIN estamento en la tabla, elegir uno
    o IGNORAR (externo que presta servicios transitorios). Devuelve
    {nombre: estamento | None} (None = ignorar). {} si se cancela."""
    import tkinter as tk
    from tkinter import ttk
    IGN = "— Ignorar (externo / transitorio) —"
    top = tk.Toplevel(root)
    top.title("Estamentos sin identificar")
    top.transient(root); top.grab_set()
    ttk.Label(top, padding=12, justify="left", text=(
        f"{len(faltantes)} profesional(es) no están en la tabla «Utilización de Cupos».\n"
        "Asigna su estamento, o Ignóralos si son externos que prestan servicios "
        "transitorios.")).pack(anchor="w")
    cont = ttk.Frame(top, padding=(12, 0)); cont.pack(fill="both", expand=True)
    ops = [IGN] + list(opciones)
    vars_ = {}
    for i, nombre in enumerate(faltantes):
        ttk.Label(cont, text=nombre).grid(row=i, column=0, sticky="w", padx=(0, 10), pady=2)
        v = tk.StringVar(value=ops[0])
        ttk.OptionMenu(cont, v, ops[0], *ops).grid(row=i, column=1, sticky="w", pady=2)
        vars_[nombre] = v
    res = {}

    def aplicar():
        for nombre, v in vars_.items():
            val = v.get()
            res[nombre] = None if val == IGN else val
        top.destroy()

    barra = ttk.Frame(top, padding=12); barra.pack(fill="x")
    ttk.Button(barra, text="Aplicar", command=aplicar).pack(side="right")
    ttk.Button(barra, text="Cancelar", command=top.destroy).pack(side="right", padx=6)
    top.wait_window()
    return res


# ── Pestaña A05: Egresos / Ingresos ───────────────────────────────────
def _tab_a05(nb, root, ruta_inicial=""):
    import tkinter as tk
    from tkinter import ttk, messagebox
    tab = ttk.Frame(nb, padding=12)
    nb.add(tab, text="REM A05 · Egresos / Ingresos")

    instr = (
        "1.  Descarga el Excel del formulario «Control de Salud Mental»:\n"
        "     A) IRIS: Formularios RAYEN → Control de Salud Mental → todos los metacampos, Situación TODOS, Estado AMBOS.\n"
        "     B) RAYEN: Herramientas → Informe Estadístico → Impresión Formularios Clínicos → Reporte Administrativo.\n"
        "2.  Elige el FORMATO que descargaste y el archivo.\n"
        "3.  Marca la(s) TAREA(s) y «Procesar» → «…_procesado.xlsx» con una hoja por tarea.\n"
        "     Tu archivo original NO se modifica.\n"
        "⚠  No discrimina fecha: debe seleccionarse bien al bajar el reporte."
    )
    caja_instr = ttk.LabelFrame(tab, text="Instrucciones", padding=8)
    caja_instr.pack(fill="x", pady=(0, 8))
    ttk.Label(caja_instr, text=instr, justify="left").pack(anchor="w")
    _aviso_sin_modificar(tab)

    caja_fmt = ttk.LabelFrame(tab, text="Formato del reporte", padding=8)
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

    var_ruta = tk.StringVar(value=ruta_inicial)
    _fila_archivo(tab, var_ruta, "Elige el export de Control de Salud Mental")

    caja_tareas = ttk.LabelFrame(tab, text="Tareas a ejecutar", padding=8)
    caja_tareas.pack(fill="x", pady=(2, 6))
    checks = {}
    for t in TAREAS:
        var = tk.BooleanVar(value=True)
        ttk.Checkbutton(caja_tareas, text=t["nombre"], variable=var).pack(anchor="w")
        checks[t["id"]] = (t, var)

    log, limpiar = _crear_log(tab, root)

    def on_procesar():
        limpiar()
        entrada = _valida_ruta(var_ruta.get(), messagebox)
        if entrada is None:
            return
        seleccionadas = [t for (t, var) in checks.values() if var.get()]
        if not seleccionadas:
            messagebox.showwarning("Sin tareas", "Marca al menos una tarea.")
            return
        perfil = sm.perfil_por_id(var_perfil.get())
        if perfil["disclaimer"]:
            log(perfil["disclaimer"]); log("")
        btn.configure(state="disabled")
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
            log("[PERMISO DENEGADO] archivo abierto en Excel / OneDrive")
            messagebox.showerror("Permiso denegado", _MSG_PERMISO)
            return
        except Exception as e:
            _error_inesperado(e, log, messagebox)
            return
        finally:
            btn.configure(state="normal")
        resumen = _resumen_texto(resultados, salida)
        log(""); log("✔ " + resumen.replace("\n", " | "))
        if messagebox.askyesno("Listo", resumen + "\n\n¿Abrir la carpeta del resultado?"):
            if salida:
                _abrir_carpeta(Path(salida).parent)

    barra = ttk.Frame(tab)
    barra.pack(fill="x")
    btn = ttk.Button(barra, text="Procesar", command=on_procesar)
    btn.pack(side="left")

    on_perfil_change()
    if not sm.OPENPYXL_OK:
        log("⚠ Falta 'openpyxl'. Instálalo con: pip install openpyxl")


# ── Pestaña A03 D.3: Screening (PSC / PSC-Y / GHQ-12) ──────────────────
def _bloque_a03(parent):
    """Los 3 slots de instrumentos A03·D.3 (carga los que existan, ≥1). El slot fija
    el instrumento (sin autodetección). Devuelve get() -> dict {instrumento: ruta}."""
    g = {
        "PSC":    _fila_archivos(parent, "PSC (padres, 5-9):", "Cuestionario para Padres PSC"),
        "PSC-Y":  _fila_archivos(parent, "PSC-Y (10-14):", "Cuestionario para Adolescentes (PSC-Y)"),
        "GHQ-12": _fila_archivos(parent, "GHQ-12 (Goldberg, 15+):", "Cuestionario de Salud de Goldberg"),
    }

    def get():
        out = {}
        for inst, getf in g.items():
            fs = getf()
            if fs:
                out[inst] = fs[0]
        return out
    return get


def _correr_a03(root, barra, btn, log, por_inst, salida, est_ruta, messagebox):
    """Corre el reporte A03·D.3 unificado en hilo (con reloj) y avisa al terminar.
    Reutilizado por la pestaña A03 y por el checkbox 'cuestionarios' de Actividades."""
    def trabajo(log):
        # resolver_estamento=None: el diálogo Tk no puede abrirse desde el hilo worker;
        # el estamento solo alimenta el DETALLE (no la tabla D.3), así que va best-effort
        # (los funcionarios sin match quedan sin estamento en el detalle).
        estamentos = str(est_ruta) if est_ruta else None
        return screening.procesar_unificado(
            por_inst, salida, estamentos=estamentos, resolver_estamento=None, log=log)

    def al_terminar(res, err):
        if err is not None:
            _manejar_error(err, log, messagebox)
            return
        pit = " · ".join(f"{k}: {v}" for k, v in res["por_instrumento"].items())
        txt = (f"Listo. A03·D.3 unificado.\n{res['total']} aplicaciones ({pit}).\n\n"
               f"Guardado en:\n{res['salida']}")
        log(""); log("✔ A03·D.3 " + txt.replace("\n", " | "))
        if messagebox.askyesno("Listo", txt + "\n\n¿Abrir la carpeta del resultado?"):
            _abrir_carpeta(Path(res["salida"]).parent)

    _correr_con_reloj(root, barra, btn, log, trabajo, al_terminar)


def _tab_a03(nb, root):
    from tkinter import ttk, messagebox
    tab = ttk.Frame(nb, padding=12)
    nb.add(tab, text="REM A03 D.3 · Screening")

    instr = (
        "Monitoreo del PSM (PSC / PSC-Y / GHQ-12), aplicado al INGRESO y EGRESO del programa.\n"
        "Carga UN archivo por instrumento (los que existan; el slot ya dice cuál es, sin\n"
        "auto-detección). Salida UNIFICADA: la tabla A03·D.3 lista para copiar-pegar al SA_26\n"
        "(Evaluación ingreso/egreso × Bajo/Medio/Alto × rango etario × sexo) + una hoja de\n"
        "DETALLE auditable (una fila por aplicación: puntaje, DISAM vs RAYEN, discrepancia…).\n"
        "Solo cuenta personas INGRESADAS al PSM; los 'Sin riesgo' (bajo el corte) van al\n"
        "detalle pero NO a la tabla D.3 (no son categoría del REM). Tamizaje = A03·H (aparte)."
    )
    caja_instr = ttk.LabelFrame(tab, text="Instrucciones", padding=8)
    caja_instr.pack(fill="x", pady=(0, 8))
    ttk.Label(caja_instr, text=instr, justify="left").pack(anchor="w")
    _aviso_sin_modificar(tab)

    get_a03 = _bloque_a03(tab)
    _separador_opcionales(tab)
    get_est = _bloque_estamentos(tab)     # opcional: solo rellena el Estamento del detalle (admin)
    get_salida = _fila_carpeta_salida(tab)

    log, limpiar = _crear_log(tab, root)

    def on_procesar():
        limpiar()
        por_inst = get_a03()
        if not por_inst:
            messagebox.showwarning("Sin archivos", "Carga al menos un instrumento "
                                   "(PSC / PSC-Y / GHQ-12).")
            return
        carpeta = _valida_carpeta(get_salida(), messagebox)
        if carpeta is None:
            return
        salida = carpeta / "REM_A03_D3.xlsx"
        _correr_a03(root, barra, btn, log, por_inst, salida, get_est(), messagebox)

    barra = ttk.Frame(tab)
    barra.pack(fill="x")
    btn = ttk.Button(barra, text="Procesar", command=on_procesar)
    btn.pack(side="left")


# ── Pestaña A23 D · Respiratorio ──────────────────────────────────────
def _tab_a23(nb, root):
    import tkinter as tk
    from tkinter import ttk, messagebox
    from datetime import date
    tab = ttk.Frame(nb, padding=12)
    nb.add(tab, text="REM A23 · Respiratorio")

    instr = (
        "Tabula el REM A23 (Respiratorio) por paciente. Todos los inputs tienen PII → quedan LOCALES.\n"
        "1.  Atenciones / Diagnósticos / Actividades  →  indicadores del MES (IRA, neumonía, KTR,\n"
        "     espirometría, controles de sala por profesión, rehab…). Carga el/los archivo(s).\n"
        "2.  Formulario «Otros Crónicos»  →  SALA bajo control + inasistentes crónicos (Sección G).\n"
        "     ⚠ Se bajan POR AÑO → carga VARIOS archivos (al menos el año actual + el anterior, ideal 5):\n"
        "        el inasistente tiene su último control hace >1 año, así que con pocos meses G subcuenta.\n"
        "3.  Estratificación de Riesgo (opcional)  →  mejora la detección de asma/EPOC/FQ/SBOR.\n"
        "4.  Inasistentes NSP (opcional)  →  Sección H: citas Control/Ingreso IRA/ERA no asistidas.\n"
        "\n"
        "⚠ OJO CON RAYEN ADMINISTRATIVO: desde ahí SOLO obtienes el formulario Otros Crónicos y un\n"
        "   «monitoreo de actividades» mensual — con MUCHO menos info que el export IRIS (y horrible de\n"
        "   parsear). Para los indicadores del mes conviene el export completo de atenciones (IRIS / BD PowerBI).\n"
        "Los cálculos van hacia atrás desde el ÚLTIMO DÍA del mes reportado (no desde hoy)."
    )
    caja = ttk.LabelFrame(tab, text="Instrucciones", padding=8)
    caja.pack(fill="x", pady=(0, 8))
    ttk.Label(caja, text=instr, justify="left").pack(anchor="w")
    _aviso_sin_modificar(tab)

    get_aten = _fila_archivos(tab, "Atenciones (del mes):", "Atenciones / Diagnósticos / Actividades")
    get_otros = _fila_archivos(tab, "Otros Crónicos (histórico):", "Formulario Otros Crónicos — varios años")
    _separador_opcionales(tab)
    get_estrat = _fila_archivos(tab, "Estratificación (opcional):", "Estratificación de Riesgo — opcional")
    get_nsp = _fila_archivos(tab, "Inasistentes NSP (opc):", "Reporte de pacientes inasistentes (NSP) — Sección H")
    get_salida = _fila_carpeta_salida(tab)

    hoy = date.today()
    y0, m0 = (hoy.year, hoy.month - 1) if hoy.month > 1 else (hoy.year - 1, 12)
    barra_mes = ttk.Frame(tab)
    barra_mes.pack(fill="x", pady=(4, 4))
    ttk.Label(barra_mes, text="Mes a reportar (año / mes):").pack(side="left")
    var_anio = tk.StringVar(value=str(y0))
    var_mes = tk.StringVar(value=str(m0))
    ttk.Spinbox(barra_mes, from_=2020, to=2100, width=6, textvariable=var_anio).pack(side="left", padx=(6, 2))
    ttk.Spinbox(barra_mes, from_=1, to=12, width=4, textvariable=var_mes).pack(side="left")

    log, limpiar = _crear_log(tab, root)

    def on_procesar():
        limpiar()
        atens = get_aten()
        if not atens:
            messagebox.showwarning("Falta atenciones", "Carga al menos un archivo de atenciones.")
            return
        otros = get_otros()
        if not otros:
            messagebox.showwarning("Falta Otros Crónicos",
                                   "El formulario Otros Crónicos es OBLIGATORIO (SALA bajo control "
                                   "+ Sección G). Cárgalo — ideal varios años para los inasistentes.")
            return
        est_sel = get_estrat()
        est = est_sel[0] if est_sel else None
        nsp_sel = get_nsp()
        nsp = nsp_sel[0] if nsp_sel else None
        try:
            y, m = int(var_anio.get()), int(var_mes.get())
        except ValueError:
            messagebox.showwarning("Mes inválido", "Año y mes deben ser números.")
            return
        carpeta = _valida_carpeta(get_salida(), messagebox)
        if carpeta is None:
            return
        salida = carpeta / f"REM_A23_{y}_{m:02d}_procesado.xlsx"

        def trabajo(log):
            import modulos.rem_a23_respiratorio as a23
            fer = a23.procesar(atens, otros=(otros or None), estrat=est,
                               inasistentes=nsp, mes=(y, m), log=log)
            a23.escribir(fer, salida)
            return fer

        def al_terminar(fer, err):
            if err is not None:
                _manejar_error(err, log, messagebox)
                return
            g = fer.attrs.get("seccion_g", {})
            gtxt = " · ".join(f"{lbl.split()[0]}:{d['Total']}" for lbl, d in g.items() if d["Total"])
            txt = (f"Listo. REM A23 {y}-{m:02d}.\n{len(fer)} pacientes en el detalle.\n"
                   f"Sección G (inasistentes crónicos): {gtxt or 'ninguno'}\n\nGuardado en:\n{salida}")
            log(""); log("✔ " + txt.replace("\n", " | "))
            if messagebox.askyesno("Listo", txt + "\n\n¿Abrir la carpeta del resultado?"):
                _abrir_carpeta(salida.parent)

        _correr_con_reloj(root, barra, btn, log, trabajo, al_terminar)

    barra = ttk.Frame(tab)
    barra.pack(fill="x")
    btn = ttk.Button(barra, text="Procesar", command=on_procesar)
    btn.pack(side="left")


# ── Pestaña SM Actividades: A04 / A06 / A19a / A26 / A27 / A32 ─────────
def _tab_sm(nb, root):
    import tkinter as tk
    from tkinter import ttk, messagebox
    from datetime import date
    tab = _tab_scroll(nb, "REM SM · Actividades")   # scroll: al desplegar cuestionarios crece

    instr = (
        "Tabula las ACTIVIDADES de Salud Mental (estadística, sin juicio clínico) → tablas\n"
        "listas para copiar-pegar al template SA_26. Cubre A04·A24, A06·A.1 (controles +\n"
        "psicosocial grupal), A19a·A.3 (consejerías familiares SM/demencia), A26 (VDI SM),\n"
        "A27 (educación prev. SM) y A32·F (acciones/controles remotos SM).\n"
        "1.  Atenciones / Diagnósticos / Actividades (ADA, IRIS)  →  casi todas las casillas.\n"
        "2.  Atenciones Grupales  →  A06 psicosocial grupal, A19a grupal y A27 (educación).\n"
        "3.  Inscritos y Adscritos (opcional, ENORME)  →  solo para el flag TRANS (género).\n"
        "4.  Maestro de Actividades (opcional)  →  clasifica el reporte extra de TRABAJO PERDIDO:\n"
        "     actividades con 'mental'/'demencia' que NO tributan al REM + qué funcionario las registra.\n"
        "El export puede venir del AÑO COMPLETO: se filtra el mes que elijas (por FECHA ATENCIÓN,\n"
        "hacia atrás desde el último día del mes). ADA cuenta por atención; grupal por asistencia.\n"
        "⚠ Para el flag GESTANTE se usa una ventana de 3 MESES → carga el ADA de los últimos 3 meses."
    )
    caja = ttk.LabelFrame(tab, text="Instrucciones", padding=8)
    caja.pack(fill="x", pady=(0, 8))
    ttk.Label(caja, text=instr, justify="left").pack(anchor="w")
    _aviso_sin_modificar(tab)

    get_ada = _fila_archivos(tab, "Atenciones/Diag/Activ (ADA):", "Atenciones / Diagnósticos / Actividades")
    get_grupal = _fila_archivos(tab, "Atenciones Grupales:", "Reporte de Atenciones Grupales")
    _separador_opcionales(tab)
    get_inscritos = _fila_archivos(tab, "Inscritos (opcional, TRANS):", "Informe Inscritos y Adscritos — para el flag TRANS")
    get_multi = _fila_archivos(tab, "Multiprofesional (opc, A26):", "Monitoreo Multiprofesional — composición de VDI en A26")
    get_maestro = _fila_archivos(tab, "Maestro (opc, saco vacío):", "Maestro de Actividades — catálogo RAYEN para clasificar el trabajo perdido")
    get_salida = _fila_carpeta_salida(tab)

    hoy = date.today()
    y0, m0 = (hoy.year, hoy.month - 1) if hoy.month > 1 else (hoy.year - 1, 12)
    barra_mes = ttk.Frame(tab)
    barra_mes.pack(fill="x", pady=(4, 4))
    ttk.Label(barra_mes, text="Mes a reportar (año / mes):").pack(side="left")
    var_anio = tk.StringVar(value=str(y0))
    var_mes = tk.StringVar(value=str(m0))
    ttk.Spinbox(barra_mes, from_=2020, to=2100, width=6, textvariable=var_anio).pack(side="left", padx=(6, 2))
    ttk.Spinbox(barra_mes, from_=1, to=12, width=4, textvariable=var_mes).pack(side="left")

    # Checkbox opcional: incluir los cuestionarios A03·D.3 (se despliegan al marcarlo).
    var_a03 = tk.BooleanVar(value=False)
    ttk.Checkbutton(tab, text="¿Incluir cuestionarios?  (genera además la tabla A03·D.3)",
                    variable=var_a03, command=lambda: _toggle_a03()).pack(anchor="w", pady=(6, 0))
    holder_a03 = ttk.Frame(tab)
    holder_a03.pack(fill="x")
    frame_a03 = ttk.LabelFrame(holder_a03, text="Cuestionarios A03·D.3 (PSC / PSC-Y / GHQ-12)", padding=8)
    get_a03_sm = _bloque_a03(frame_a03)

    def _toggle_a03():
        frame_a03.pack(fill="x", pady=(2, 4)) if var_a03.get() else frame_a03.pack_forget()

    log, limpiar = _crear_log(tab, root)

    def on_procesar():
        limpiar()
        ada = get_ada()
        if not ada:
            messagebox.showwarning("Falta el ADA", "Carga al menos un archivo de "
                                   "Atenciones / Diagnósticos / Actividades.")
            return
        grupal = get_grupal() or None
        if grupal is None:
            messagebox.showwarning("Falta Atenciones Grupales",
                                   "El reporte de Atenciones Grupales es OBLIGATORIO: de ahí "
                                   "salen A06 psicosocial grupal, A19a grupal y A27.")
            return
        ins = get_inscritos()
        inscritos = ins[0] if ins else None
        mp = get_multi()
        multiprofesional = mp[0] if mp else None
        try:
            y, m = int(var_anio.get()), int(var_mes.get())
        except ValueError:
            messagebox.showwarning("Mes inválido", "Año y mes deben ser números.")
            return
        carpeta = _valida_carpeta(get_salida(), messagebox)
        if carpeta is None:
            return
        salida = carpeta / f"REM_SM_actividades_{y}_{m:02d}.xlsx"
        salida_tp = carpeta / f"REM_SM_trabajo_perdido_{y}_{m:02d}.xlsx"
        mtr = get_maestro()
        maestro = mtr[0] if mtr else _slim_por_defecto()    # sin selección → Maestro slim del repo/exe
        # Cuestionarios A03·D.3 (opcional): resolver en el hilo GUI (Tk vars no son
        # thread-safe) y pasar los valores capturados al worker.
        incluir_a03 = var_a03.get()
        por_inst_a03 = get_a03_sm() if incluir_a03 else {}
        salida_a03 = carpeta / f"REM_A03_D3_{y}_{m:02d}.xlsx"

        def trabajo(log):
            from programas.rem_utils import cargar_atenciones
            import modulos.rem_sm_actividades as smact
            d = cargar_atenciones(ada)          # el ADA se lee UNA sola vez y se comparte
            E = smact.procesar(ada, grupal=grupal, inscritos=inscritos,
                               multiprofesional=multiprofesional, mes=(y, m), log=log, d=d)
            smact.escribir(E, salida)
            n_tp = None
            # Trabajo perdido (saco vacío): mismo ADA ya cargado. Try propio para que un
            # fallo acá (p.ej. Monitoreo admin sin 'PROFESIONAL ATENCION') no tumbe el SM.
            try:
                import modulos.rem_sm_trabajo_perdido as tpmod
                Etp = tpmod.procesar(ada, maestro=maestro, mes=(y, m), log=log, d=d)
                tpmod.escribir(Etp, salida_tp)
                n_tp = len(Etp)
                log(f"✔ Trabajo perdido: {n_tp} atenciones a saco vacío → {salida_tp.name}")
            except Exception as e:   # noqa: BLE001
                log(f"[tp] ⚠ no se generó el reporte de trabajo perdido: {e}")
            n_a03 = None
            if incluir_a03:
                if por_inst_a03:
                    try:
                        r03 = screening.procesar_unificado(por_inst_a03, salida_a03,
                                                           estamentos=None, resolver_estamento=None, log=log)
                        n_a03 = r03["total"]
                        log(f"✔ A03·D.3: {n_a03} aplicaciones → {salida_a03.name}")
                    except Exception as e:   # noqa: BLE001
                        log(f"[a03] ⚠ no se generó la tabla A03·D.3: {e}")
                else:
                    log("[a03] ⚠ 'Incluir cuestionarios' marcado pero sin archivos → se omite.")
            return E, n_tp, n_a03

        def al_terminar(res, err):
            if err is not None:
                _manejar_error(err, log, messagebox)
                return
            E, n_tp, n_a03 = res
            resu = E.attrs["tablas"]["SM_Resumen"]
            rtxt = "\n".join(f"  {r['Casilla']}: {r['Total mes']}" for _, r in resu.iterrows())
            tptxt = f"\nTrabajo perdido: {n_tp} atenciones a saco vacío." if n_tp is not None else ""
            a03txt = f"\nA03·D.3: {n_a03} aplicaciones." if n_a03 is not None else ""
            txt = (f"Listo. REM SM Actividades {y}-{m:02d}.\n{len(E)} eventos en el detalle.{tptxt}{a03txt}\n\n"
                   f"{rtxt}\n\nGuardado en:\n{salida}")
            log(""); log("✔ REM SM " + f"{y}-{m:02d} guardado: {salida.name}")
            if messagebox.askyesno("Listo", txt + "\n\n¿Abrir la carpeta del resultado?"):
                _abrir_carpeta(salida.parent)

        _correr_con_reloj(root, barra, btn, log, trabajo, al_terminar)

    barra = ttk.Frame(tab)
    barra.pack(fill="x")
    btn = ttk.Button(barra, text="Procesar", command=on_procesar)
    btn.pack(side="left")


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
        print("(El screening A03 por ahora solo desde la GUI, pestaña 'Screening'.)")
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
