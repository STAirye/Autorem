#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Sonnet 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# Copyright (C) 2026 Simon Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.9.17
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

`ttk.Spinbox` no tiene equivalente en customtkinter 6.0.0 (no existe
CTkSpinbox): se embebe el widget ttk tal cual dentro del CTkFrame, practica
soportada por CTk.

MODO OSCURO (plan SS4/SS5.2, agregado tras habilitar el toggle en gui/app.py):
`COLOR_AVISO`/`COLOR_ATENUADO` eran un string UNICO (el color de aviso del Tk
actual, pensado solo para fondo blanco) -- pasan a tupla (claro, oscuro),
medida en contraste WCAG igual que `_PALETA_FUENTE` (SS5.2 del plan), y
reusan sus mismos tonos oscuros para que el lenguaje visual de "aviso" sea
uno solo. El reloj de arena (`Reloj`, mas abajo) es la excepcion: dibuja
sobre un `tkinter.Canvas` CRUDO (no CTk), asi que sus colores no se resuelven
solos con una tupla -- se resuelven a mano con `root._apply_appearance_mode()`
en cada tick (ver la clase).
"""

from pathlib import Path

import customtkinter as ctk

# Mismo tono oscuro que "parcial"/"cambiada" de _PALETA_FUENTE (mas abajo):
# un solo lenguaje visual de "aviso" en toda la GUI, no dos paletas de avisos
# midiendo contraste por separado.
COLOR_AVISO = ("#a05a00", "#F0C070")      # 3.83:1 / 8.41:1 contra el fondo de pagina
COLOR_ATENUADO = ("#888888", "#aaaaaa")   # texto secundario ("(vacio = ...)", "Opcionales")
# 'top_fg_color' del tema de CTk: un paso mas oscuro/claro que el fondo por
# defecto de un CTkFrame/CTkScrollableFrame, asi una caja titulada se nota
# sin inventar un color nuevo (feedback visual del autor, sep-2026: las cajas
# se perdian contra el fondo de la pagina).
COLOR_CAJA = ("gray81", "gray20")
# El tema de CTk (ThemeManager.theme["CTkButton"]["text_color"]) es
# ['#DCE4EE', '#DCE4EE'] EN LOS DOS MODOS -- pensado para leerse sobre el
# fg_color AZUL por defecto del boton, no sobre "transparent". Un boton
# transparente (el sidebar) queda casi ilegible (texto casi blanco sobre
# gris claro) si no se pisa a mano. Mismo texto_color que trae CTkLabel por
# defecto (SI calza con "transparent"), para que un boton transparente lea
# igual que una etiqueta (feedback visual del autor, sep-2026: sidebar
# ilegible en modo claro).
COLOR_TEXTO_TRANSPARENTE = ("gray10", "#DCE4EE")

# Rango de años aceptado por el selector de mes. UNA fuente: los `from_`/`to` del
# Spinbox Y la guarda de `runner.valida_mes` salen de aca -- el Spinbox acota solo
# sus flechas, asi que la guarda es la que de verdad rechaza un año tecleado, y las
# dos tienen que decir lo mismo o el mensaje de error miente.
ANIO_MIN, ANIO_MAX = 2020, 2100

_AVISO_SIN_MODIFICAR = ((" Carga los archivos TAL COMO los descargas de RAYEN/IRIS: sin abrirlos, editarlos ni re-guardarlos, excepto los que se solicitan explicitamente.\n"
                         "     Un export modificado (cambio de formato, columnas, hojas) puede dar cifras erróneas sin aviso."))


def etiqueta_envolvente(parent, text, **kwargs):
    """CTkLabel que AJUSTA su wraplength al ancho de `parent` en cada resize,
    en vez de desbordar horizontalmente (feedback del autor, sep-2026: prefiere
    esto a un scrollbar horizontal). `parent` debe ser un contenedor que se
    estire con la ventana (pack fill='x' o similar) -- su ancho real es el
    que manda.

    OJO CON EL DPI: `e.width` ya viene en pixeles REALES (escalados), y
    `CTkLabel.configure(wraplength=)` lo vuelve a escalar (`_apply_widget_scaling`).
    Sin des-escalarlo, con Windows al 150% el texto pedia 1.5x el ancho de su caja
    y se cortaba por la derecha -- incluido el mensaje del BannerFuente, o sea un
    color sin su leyenda completa (SS5.1 del plan, regla 1). Al 100% no se nota."""
    lbl = ctk.CTkLabel(parent, text=text, justify="left", anchor="w", **kwargs)
    parent.bind("<Configure>", lambda e: lbl.configure(
        wraplength=lbl._reverse_widget_scaling(max(e.width - 20, 50))), add="+")
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


def fila_archivos(parent, etiqueta, titulo, on_elegido=None):
    """Fila con seleccion de VARIOS archivos (historico multi-anio). Devuelve
    get() -> list[str]. `on_elegido(lista)` (opcional) corre justo despues de
    elegir -- lo usa SM para el preview de cruce ADA<->Grupal (SS5.1 del plan).

    El boton 'Quitar' NO es cosmetico: hasta 1.9.17 esta fila solo se podia
    SOBREESCRIBIR (el dialogo cancelado deja la seleccion anterior), y un input
    multiple no se podia dejar vacio de vuelta. Eso dejaba sin salida la corrida
    solo-cuestionarios de SM Actividades, que exige 'ni ADA ni Grupal'
    (`sm._es_solo_a03`): un click accidental en Examinar sobre el ADA la volvia
    inalcanzable hasta reiniciar autoREM, porque las paginas no se destruyen al
    cambiar de pantalla (ver App.mostrar). Avisa con `on_elegido([])` para que los
    previews que dependen del archivo (banner de cruce) se apaguen solos."""
    from tkinter import filedialog
    fila = ctk.CTkFrame(parent, fg_color="transparent")
    fila.pack(fill="x", pady=(3, 3))
    ctk.CTkLabel(fila, text=etiqueta, width=220, anchor="w").pack(side="left")
    lbl = ctk.CTkLabel(fila, text="(ninguno)", text_color=COLOR_ATENUADO)
    sel = []

    def _pintar():
        if not sel:
            lbl.configure(text="(ninguno)")
            return
        nombres = ", ".join(Path(f).name for f in sel)
        lbl.configure(text=f"{len(sel)}: " + (nombres[:70] + "…" if len(nombres) > 70 else nombres))

    def examinar():
        fs = filedialog.askopenfilenames(title=titulo, filetypes=[("Excel", "*.xlsx"), ("Todos", "*.*")])
        if fs:
            sel[:] = list(fs)
            _pintar()
            if on_elegido:
                on_elegido(list(sel))

    def quitar():
        if not sel:
            return
        sel.clear()
        _pintar()
        if on_elegido:
            on_elegido([])

    ctk.CTkButton(fila, text="Examinar…", width=100, command=examinar).pack(side="left")
    ctk.CTkButton(fila, text="Quitar", width=70, fg_color="transparent", border_width=1,
                  text_color=COLOR_TEXTO_TRANSPARENTE, command=quitar).pack(side="left", padx=(4, 0))
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

    def get():
        from gui.runner import limpiar_ruta   # perezoso: runner importa este modulo
        return limpiar_ruta(var.get())
    return get


def selector_mes(parent, mes_defecto, etiqueta="Mes a reportar (año / mes):"):
    """Fila '<etiqueta> [año] [mes]', consolidada de la copia que autorem.py
    repetia tal cual en A23/SM/BETA (docs/GUI_2.0_plan.md SS2). `mes_defecto`
    = (año, mes) inicial -- normalmente `rem_utils.mes_anterior()`, decidido
    por quien llama (no importado aca para no atar el widget a esa regla).

    Devuelve get() -> (año, mes) o None si lo tecleado no son numeros. El RANGO
    no se valida aca sino en `runner.valida_mes`, que es quien tiene el
    messagebox: el Spinbox acota solo sus FLECHAS, no lo que se teclea.
    La caja de A05 (que alterna 'archivo completo' vs 'un mes') usa ESTE mismo
    selector sin etiqueta (`etiqueta=None`) dentro de su propia fila, y activa o
    apaga sus Spinbox via `get.spinboxes`: hasta 1.9.17 tenia una copia a mano de
    los dos Spinbox y del parseo, fuera del test que amarra los años."""
    import tkinter as tk
    from tkinter import ttk
    y0, m0 = mes_defecto
    fila = ctk.CTkFrame(parent, fg_color="transparent")
    fila.pack(fill="x", pady=(4, 4) if etiqueta else 0)
    if etiqueta:
        ctk.CTkLabel(fila, text=etiqueta).pack(side="left")
    var_anio = tk.StringVar(value=str(y0))
    var_mes = tk.StringVar(value=str(m0))
    spin_anio = ttk.Spinbox(fila, from_=ANIO_MIN, to=ANIO_MAX, width=6, textvariable=var_anio)
    spin_anio.pack(side="left", padx=(6, 2))
    spin_mes = ttk.Spinbox(fila, from_=1, to=12, width=4, textvariable=var_mes)
    spin_mes.pack(side="left")

    def get():
        try:
            return int(var_anio.get()), int(var_mes.get())
        except ValueError:
            return None
    get.spinboxes = (spin_anio, spin_mes)
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
    "detectando":    {"fondo": ("gray86", "gray17"), "texto": COLOR_ATENUADO},
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
        # Ancla = el ultimo widget ya empacado al crearla. Un pack() tardio sin
        # `after=` la manda al FINAL de la pagina (debajo de Procesar y del log).
        slaves = parent.pack_slaves()
        self._ancla = slaves[-1] if slaves else None
        self._visible = False

    def mostrar(self, estado, mensaje):
        colores = _PALETA_FUENTE[estado]
        self.configure(fg_color=colores["fondo"])
        self._label.configure(text=mensaje, text_color=colores["texto"])
        if not self._visible:
            if self._ancla is not None and self._ancla.winfo_exists():
                self.pack(fill="x", pady=(0, 6), after=self._ancla)
            else:
                self.pack(fill="x", pady=(0, 6))
            self._visible = True

    def ocultar(self):
        self.pack_forget()
        self._visible = False


def bloque_banner_fuente(frame, pagina):
    """Extra de A23/SM: BannerFuente oculto hasta `pintar_banner_fuente` (post-corrida)."""
    pagina.datos["banner_fuente"] = BannerFuente(frame)
    return None


def pintar_banner_fuente(pagina, df):
    """`al_completar` compartido: pinta el banner con los avisos de fuente de `df`.

    Sin `df` (p.ej. la corrida solo-cuestionarios de SM, que no carga ADA) el banner
    se APAGA en vez de dejarse como estaba: el color es una AFIRMACION sobre la fuente
    (SS5.1 del plan, regla 1), asi que un banner verde heredado de la corrida anterior
    estaria jurando 'A/D/A de IRIS completo' sobre un archivo que esta corrida ni
    abrio."""
    banner = pagina.datos.get("banner_fuente")
    if banner is None:
        return
    if df is None:
        banner.ocultar()
        return
    estado_mensaje = estado_fuente_de_avisos(df.attrs.get("avisos"))
    if estado_mensaje is None:
        banner.mostrar("plena", "Fuente: A/D/A de IRIS completo.")
    else:
        banner.mostrar(*estado_mensaje)


def texto_avisos(avisos, titulo="OJO, {n} aviso(s) -- revísalos (y la hoja LEEME) antes de copiar:"):
    """Bloque de texto con los avisos de una corrida (tuplas `(casilla, estado, motivo,
    que_hacer)`) para el RESUMEN de la página, o '' si no hay. Los avisos no bloquean a
    proposito, y justamente por eso tienen que verse en el «Listo»: solo en el log y la
    LEEME, se leía igual que una corrida sin nada que advertir. `titulo` con `{n}`."""
    avisos = list(avisos or [])
    if not avisos:
        return ""
    lineas = "".join(f"\n  - {casilla}: {estado} ({motivo})"
                     for casilla, estado, motivo, _ in avisos)
    return f"\n\n{titulo.format(n=len(avisos))}{lineas}"


def estado_fuente_de_avisos(avisos):
    """(estado_banner, mensaje) para BannerFuente.mostrar(), extraido de un
    `.attrs['avisos']` de A23/SM (formatos.aviso_fuente, ver programas/CLAUDE.md
    SS_formatos). None si la fuente es plena (nada que avisar) o si no hay
    ningun aviso de fuente en la lista.

    Los avisos de fuente son identificables por su 2do elemento -- literales
    estables que devuelve `aviso_fuente()` ('FUENTE PARCIAL' | 'EXPORT
    CAMBIADO') -- y se buscan entre CUALQUIER otro aviso que la corrida haya
    acumulado (ej. exclusiones de trabajo perdido): no se puede asumir que el
    de fuente sea el primero ni el unico."""
    for aviso in avisos or []:
        _casilla, estado_txt, motivo, _que_hacer = aviso
        if estado_txt in ("FUENTE PARCIAL", "EXPORT CAMBIADO"):
            estado_banner = "parcial" if estado_txt == "FUENTE PARCIAL" else "cambiada"
            return estado_banner, f"{estado_txt}: {motivo}"
    return None


class Reloj:
    """Reloj de arena dibujado que GIRA: indicador indeterminado ('trabajando',
    sin porcentajes que mienten). Portado tal cual de autorem.py._Reloj (el
    dibujo usa un tkinter.Canvas crudo, que se embebe sin problema dentro de
    un CTkFrame). Se anima en el hilo de la GUI (`root.after`), por eso sigue
    girando mientras el worker hace el trabajo pesado en OTRO hilo.

    MODO OSCURO: un `tkinter.Canvas` crudo no resuelve tuplas (claro, oscuro)
    solo (eso es un truco de CTk) -- el fondo y los colores del dibujo se
    resuelven a mano en cada tick con `root._apply_appearance_mode()` (el
    mismo metodo que usa CTk puertas adentro), asi el reloj sigue el mismo
    modo aunque alguien toque el toggle MIENTRAS esta girando."""

    _BG = ("gray86", "gray17")             # mismo fondo que el resto de la pagina
    _FILL = ("#c8801a", "#c8801a")         # ambar: contraste OK en los dos modos
    _OUTLINE = ("#5a3200", "#f0b060")      # marron oscuro se pierde en fondo oscuro

    def __init__(self, parent, root, size=26):
        import tkinter as tk
        self.root = root
        self.size = size
        self.cv = tk.Canvas(parent, width=size, height=size, highlightthickness=0,
                            bg=root._apply_appearance_mode(self._BG))
        self.ang = 0
        self._job = None

    def _dibujar(self):
        import math
        s, a = self.size, math.radians(self.ang)
        c, r = s / 2, s * 0.34
        self.cv.configure(bg=self.root._apply_appearance_mode(self._BG))
        self.cv.delete("all")
        fill = self.root._apply_appearance_mode(self._FILL)
        outline = self.root._apply_appearance_mode(self._OUTLINE)

        def pt(dx, dy):
            return (c + dx * math.cos(a) - dy * math.sin(a),
                    c + dx * math.sin(a) + dy * math.cos(a))
        # Dos triangulos que se tocan en el centro = reloj de arena; al rotar, "gira".
        for tri in ([pt(-r, -r), pt(r, -r), pt(0, 0)],
                    [pt(-r, r), pt(r, r), pt(0, 0)]):
            self.cv.create_polygon([v for p in tri for v in p], fill=fill, outline=outline)

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
