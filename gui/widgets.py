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
gui/widgets.py - primitivas CTk reutilizables por las paginas (GUI 2.0).

Portadas de autorem.py (Tk/ttk) sin tocar la logica -- mismo comportamiento,
otro toolkit (docs/GUI_2.0_plan.md, paso 3). `SelectorMes` es la unica pieza
NUEVA de esta migracion: consolida un bloque que estaba duplicado tal cual en
A23/SM/BETA (autorem.py) en una sola funcion.

PENDIENTE A PROPOSITO (no en este paso): paleta clara/oscura centralizada
(plan SS4/SS5.2) -- el color de aviso sigue hardcodeado (`COLOR_AVISO`) como
en el Tk actual. Se centraliza cuando se aborde el modo oscuro.

`ttk.Spinbox` no tiene equivalente en customtkinter 6.0.0 (no existe
CTkSpinbox): se embebe el widget ttk tal cual dentro del CTkFrame, practica
soportada por CTk. Puede necesitar un repaso visual cuando se trabaje el modo
oscuro (SS4 del plan).
"""

from pathlib import Path

import customtkinter as ctk

COLOR_AVISO = "#a05a00"      # mismo color de aviso del proyecto (Tk actual)
COLOR_ATENUADO = "#888888"   # texto secundario ("(vacio = ...)", "Opcionales")
# 'top_fg_color' del tema de CTk: un paso mas oscuro/claro que el fondo por
# defecto de un CTkFrame/CTkScrollableFrame, asi una caja titulada se nota
# sin inventar un color nuevo (feedback visual del autor, sep-2026: las cajas
# se perdian contra el fondo de la pagina).
COLOR_CAJA = ("gray81", "gray20")

_AVISO_SIN_MODIFICAR = (" Carga los archivos TAL COMO los descargas de RAYEN/IRIS: "
                        "sin abrirlos, editarlos ni re-guardarlos.\n"
                        "     Un export modificado (cambio de formato, columnas, hojas) "
                        "puede fallar en silencio o dar cifras erróneas.")


def etiqueta_envolvente(parent, text, **kwargs):
    """CTkLabel que AJUSTA su wraplength al ancho de `parent` en cada resize,
    en vez de desbordar horizontalmente (feedback del autor, sep-2026: prefiere
    esto a un scrollbar horizontal). `parent` debe ser un contenedor que se
    estire con la ventana (pack fill='x' o similar) -- su ancho real es el
    que manda."""
    lbl = ctk.CTkLabel(parent, text=text, justify="left", anchor="w", **kwargs)
    parent.bind("<Configure>", lambda e: lbl.configure(wraplength=max(e.width - 20, 50)), add="+")
    return lbl


def caja_titulada(parent, titulo):
    """Caja con encabezado en negrita y fondo (COLOR_CAJA) sutilmente distinto
    del resto de la pagina. Reemplaza el patron repetido de
    ttk.LabelFrame(text=...) del Tk viejo (Instrucciones, Estamentos,
    Dotacion, Cuestionarios). NO se empaca sola -- el llamador decide el
    `pack`/`pack_forget` (algunas cajas arrancan ocultas, p.ej. el bloque de
    cuestionarios de SM Actividades) y empaca su contenido adentro, debajo
    del encabezado."""
    caja = ctk.CTkFrame(parent, fg_color=COLOR_CAJA)
    ctk.CTkLabel(caja, text=titulo, anchor="w", font=ctk.CTkFont(weight="bold")
                ).pack(fill="x", padx=8, pady=(6, 0))
    return caja


def aviso_sin_modificar(parent):
    """Recordatorio (todas las paginas) de cargar los exports SIN modificar."""
    etiqueta_envolvente(parent, _AVISO_SIN_MODIFICAR, text_color=COLOR_AVISO
                        ).pack(fill="x", pady=(0, 6))


def separador_opcionales(parent, texto="Opcionales"):
    """Barra horizontal que separa los inputs OBLIGATORIOS (arriba) de los
    OPCIONALES (abajo). CTk no trae un separador nativo (no hay CTkSeparator
    en 6.0.0): se simula con un CTkFrame delgado, equivalente visual del
    ttk.Separator que usaba autorem.py."""
    ctk.CTkFrame(parent, height=1, fg_color=COLOR_ATENUADO).pack(fill="x", pady=(8, 3))
    ctk.CTkLabel(parent, text=f"—  {texto}  —", text_color=COLOR_ATENUADO
                 ).pack(anchor="w", pady=(0, 2))


def fila_archivo(parent, var_ruta, titulo, etiqueta="Archivo Excel:", on_elegido=None):
    """Fila '<etiqueta> [___] [Examinar...]', UN solo archivo. `etiqueta` por
    defecto sirve para paginas con un solo input; en paginas con varios,
    pasar una etiqueta especifica para no confundir cual es cual.
    `on_elegido(ruta)` (opcional) corre justo despues de elegir el archivo --
    lo usa A05 para disparar la deteccion de formato (SS5 del plan)."""
    from tkinter import filedialog
    fila = ctk.CTkFrame(parent, fg_color="transparent")
    fila.pack(fill="x", pady=(6, 6))
    ctk.CTkLabel(fila, text=etiqueta).pack(side="left")
    ctk.CTkEntry(fila, textvariable=var_ruta).pack(side="left", fill="x", expand=True, padx=6)

    def examinar():
        f = filedialog.askopenfilename(
            title=titulo, filetypes=[("Excel", "*.xlsx"), ("Todos", "*.*")])
        if f:
            var_ruta.set(f)
            if on_elegido:
                on_elegido(f)

    ctk.CTkButton(fila, text="Examinar…", width=100, command=examinar).pack(side="left")


def fila_archivos(parent, etiqueta, titulo):
    """Fila con seleccion de VARIOS archivos (historico multi-anio). Devuelve
    get() -> list[str]."""
    from tkinter import filedialog
    fila = ctk.CTkFrame(parent, fg_color="transparent")
    fila.pack(fill="x", pady=(3, 3))
    ctk.CTkLabel(fila, text=etiqueta, width=220, anchor="w").pack(side="left")
    lbl = ctk.CTkLabel(fila, text="(ninguno)", text_color=COLOR_ATENUADO)
    sel = []

    def examinar():
        fs = filedialog.askopenfilenames(title=titulo, filetypes=[("Excel", "*.xlsx"), ("Todos", "*.*")])
        if fs:
            sel[:] = list(fs)
            nombres = ", ".join(Path(f).name for f in sel)
            lbl.configure(text=f"{len(sel)}: " + (nombres[:70] + "…" if len(nombres) > 70 else nombres))

    ctk.CTkButton(fila, text="Examinar…", width=100, command=examinar).pack(side="left")
    lbl.pack(side="left", padx=8)
    return lambda: list(sel)


def fila_carpeta_salida(parent):
    """Fila 'Carpeta de salida: [___] [Examinar…]'. Devuelve get() -> str.
    Vacio por defecto = guardar JUNTO al archivo de entrada (ver
    `runner.valida_carpeta`); asi no se ensucia el cwd/carpeta del .exe."""
    import tkinter as tk
    from tkinter import filedialog
    fila = ctk.CTkFrame(parent, fg_color="transparent")
    fila.pack(fill="x", pady=(3, 3))
    ctk.CTkLabel(fila, text="Carpeta de salida:", width=220, anchor="w").pack(side="left")
    var = tk.StringVar(value="")   # vacio -> junto al archivo de entrada
    ctk.CTkEntry(fila, textvariable=var).pack(side="left", fill="x", expand=True, padx=6)

    def elegir():
        d = filedialog.askdirectory(title="Elige dónde guardar el resultado")
        if d:
            var.set(d)

    ctk.CTkButton(fila, text="Examinar…", width=100, command=elegir).pack(side="left")
    ctk.CTkLabel(parent, text="     (vacío = junto al archivo cargado)",
                 text_color=COLOR_ATENUADO).pack(anchor="w")
    return lambda: (var.get() or "").strip().strip('"').strip("'")


def selector_mes(parent, mes_defecto, etiqueta="Mes a reportar (año / mes):"):
    """Fila '<etiqueta> [año] [mes]', consolidada de la copia que autorem.py
    repetia tal cual en A23/SM/BETA (docs/GUI_2.0_plan.md SS2). `mes_defecto`
    = (año, mes) inicial -- normalmente `rem_utils.mes_anterior()`, decidido
    por quien llama (no importado aca para no atar el widget a esa regla).

    Devuelve get() -> (año, mes) o None si lo tecleado no son numeros.
    NO es la caja de A05 (esa alterna 'archivo completo' vs 'un mes'; sigue
    siendo un `extra` propio de esa pagina, ver SS3.1 del plan)."""
    import tkinter as tk
    from tkinter import ttk
    y0, m0 = mes_defecto
    fila = ctk.CTkFrame(parent, fg_color="transparent")
    fila.pack(fill="x", pady=(4, 4))
    ctk.CTkLabel(fila, text=etiqueta).pack(side="left")
    var_anio = tk.StringVar(value=str(y0))
    var_mes = tk.StringVar(value=str(m0))
    ttk.Spinbox(fila, from_=2020, to=2100, width=6, textvariable=var_anio).pack(side="left", padx=(6, 2))
    ttk.Spinbox(fila, from_=1, to=12, width=4, textvariable=var_mes).pack(side="left")

    def get():
        try:
            return int(var_anio.get()), int(var_mes.get())
        except ValueError:
            return None
    return get


def crear_log(parent, root, height=10):
    """Caja de log (CTkTextbox: scroll incluido, sin el Canvas+Scrollbar a
    mano de `_tab_scroll`). Devuelve (log, limpiar)."""
    caja = ctk.CTkFrame(parent)
    ctk.CTkLabel(caja, text="Registro", anchor="w").pack(fill="x", padx=6, pady=(4, 0))
    caja.pack(fill="both", expand=True, pady=(6, 8))
    txt = ctk.CTkTextbox(caja, height=height * 20, wrap="word",
                         font=ctk.CTkFont(family="Consolas", size=12), state="disabled")
    txt.pack(fill="both", expand=True, padx=6, pady=6)

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


# -- BannerFuente: el color como estado de la fuente (GUI_2.0_plan.md SS5.1) --
# Paleta medida en contraste WCAG (SS5.2 del plan; no aclarar el texto ni
# oscurecer el fondo de 'parcial' sin recalcular -- 4.70:1 en claro es el
# unico par ajustado, los demas tienen holgura de sobra). 'cambiada' (estado
# dev-facing de formatos.clasificar_fuente) reusa el par ambar de 'parcial':
# no necesita color propio. 'no_reconocido' cubre tanto un A05 sin match como
# un archivo cruzado en los modulos pandas -- mismo rojo, mismo mensaje "cuidado".
_PALETA_FUENTE = {
    "plena":         {"fondo": ("#E4F2EF", "#12312C"), "texto": ("#0F4F45", "#8FD8C9")},
    "parcial":       {"fondo": ("#FCF0DA", "#33280F"), "texto": ("#A05A00", "#F0C070")},
    "cambiada":      {"fondo": ("#FCF0DA", "#33280F"), "texto": ("#A05A00", "#F0C070")},
    "no_reconocido": {"fondo": ("#FBE6E4", "#3A1A18"), "texto": ("#8C1D18", "#F2B8B4")},
    # Transitorio (no es un estado de la fuente, es "todavia no se sabe"):
    # gris neutro, sin significado propio -- se reemplaza en <1s por uno real.
    "detectando":    {"fondo": ("gray86", "gray17"), "texto": (COLOR_ATENUADO, COLOR_ATENUADO)},
}


class BannerFuente(ctk.CTkFrame):
    """Franja de estado de la fuente: color + mensaje, NUNCA el color solo
    (regla 1 de SS5.1 del plan -- el texto siempre dice lo mismo que el
    color, para daltonismo y porque un color sin leyenda no se aprende solo).
    Arranca oculta (nada que mostrar hasta que se detecte algo); `mostrar()`
    la puebla y la despliega, `ocultar()` la esconde de nuevo (p.ej. si el
    usuario borra la ruta elegida)."""

    def __init__(self, parent):
        super().__init__(parent, corner_radius=6)
        self._label = etiqueta_envolvente(self, "")
        self._label.pack(fill="x", padx=10, pady=6)
        self.pack_forget()

    def mostrar(self, estado, mensaje):
        colores = _PALETA_FUENTE[estado]
        self.configure(fg_color=colores["fondo"])
        self._label.configure(text=mensaje, text_color=colores["texto"])
        if not self.winfo_ismapped():
            self.pack(fill="x", pady=(0, 6))

    def ocultar(self):
        self.pack_forget()


class Reloj:
    """Reloj de arena dibujado que GIRA: indicador indeterminado ('trabajando',
    sin porcentajes que mienten). Portado tal cual de autorem.py._Reloj (el
    dibujo usa un tkinter.Canvas crudo, que se embebe sin problema dentro de
    un CTkFrame). Se anima en el hilo de la GUI (`root.after`), por eso sigue
    girando mientras el worker hace el trabajo pesado en OTRO hilo."""

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
        # Dos triangulos que se tocan en el centro = reloj de arena; al rotar, "gira".
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
