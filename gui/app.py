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
gui/app.py - shell: ventana, sidebar, router, construccion desde PANTALLA.

docs/GUI_2.0_plan.md, paso 4 (SS3, SS3.1, SS3.2, SS3.3, SS4). Arranca con
`python -m gui.app` -- autorem.py no se toca hasta el paso 11 del plan.

EL CONTRATO PANTALLA (lo que expone cada modulo de gui/paginas/*.py):

    PANTALLA = {
        "id": "sm_actividades",        # unico, usado por el router
        "programa": "Salud Mental",    # agrupa en el sidebar (registro.ORDEN_PROGRAMAS)
        "titulo": "Actividades",
        "estado": "estable",           # "estable" | "beta" -> badge en el sidebar
        "instrucciones": "...",        # opcional
        "inputs": [
            {"key": "ada", "etiqueta": "...", "multi": True, "obligatorio": True,
             "titulo_dialogo": "..."},
            ...
        ],
        # `obligatorio` puede ser un bool, o callable(getters) -> bool cuando
        # depende de OTRO input (SM Actividades, docs/GUI_2.0_plan.md SS6: ADA
        # y Grupal dejan de serlo SOLO en una corrida solo-cuestionarios).
        "mes": True,                   # muestra SelectorMes
        "carpeta_salida": True,        # muestra CarpetaSalida
        "extras": [                    # opcional, ver SS3.1 del plan
            {"despues_de": "ada", "construir": fn, "key": "tabla_dot"},
        ],
        "preparar": None,              # opcional, hilo GUI, ver SS3.3
        "correr": correr,              # callable(ctx, log) -> resultado, EN EL WORKER
        "resumen": resumen,            # callable(resultado) -> str para el messagebox
    }

INVARIANTE DURA (SS3.2): nada de Tk vars en el worker. `_resolver_ctx` resuelve
TODOS los getters a un dict plano `ctx` (Path/tuplas/listas, nunca StringVar)
ANTES de lanzar el hilo; `pantalla["correr"]` no debe tocar widgets.

Los `inputs` obligatorios se pintan arriba, los opcionales bajo el separador
(mismo orden visual que autorem.py). Un `extras[].despues_de` = key de un
input posiciona el bloque justo debajo de ese input (p.ej. Dotacion debajo
del ADA); `despues_de: None` lo pinta al final (antes del boton Procesar).
"""

from pathlib import Path

import tkinter.messagebox as messagebox
import customtkinter as ctk

from programas.rem_utils import VERSION, mes_anterior
from gui import widgets, runner
from gui.registro import cargar_registro, programas_en_orden

ANCHO_SIDEBAR = 210


class Pagina:
    """Lo que un `extras[].construir(frame, pagina)` puede necesitar de su
    propia pagina (SS3.1 del plan): leer OTRO input ya elegido, el mes, y
    escribir al mismo log / abrir dialogos sobre la misma ventana."""

    def __init__(self, app, getters, get_mes_celda, log):
        self.root = app
        self._getters = getters
        self._get_mes_celda = get_mes_celda   # celda mutable: ver nota en _construir_pagina
        self.log = log

    def get(self, key):
        """Valor CRUDO (string o list[str]) del getter de ese input -- el
        mismo que ve `_resolver_ctx`, sin validar todavia (la pagina puede
        llamar a esto ANTES de apretar Procesar, p.ej. 'Precargar dotacion')."""
        return self._getters[key]()

    def mes(self):
        """(anio, mes) del SelectorMes de la pagina, o None si no tiene uno
        (pantalla["mes"] es False) o si lo tecleado no son numeros.

        Resuelto PEREZOSAMENTE (celda mutable, no el getter ya resuelto): un
        extra puede recibir su `Pagina` ANTES de que el SelectorMes exista
        todavia (se pinta despues de los inputs, un extra puede ir pegado a
        uno temprano) -- lo que importa es que funcione cuando la pagina
        LLAME a esto de verdad, dentro de un boton, tras un click real, y
        para entonces la pagina ya esta completa."""
        getter = self._get_mes_celda[0]
        return getter() if getter else None


def _resolver_ctx(pantalla, getters, get_mes, get_carpeta):
    """Valida los inputs/mes/carpeta y arma el `ctx` PLANO que ve el worker
    (SS3.2). Funcion libre (sin `self`) para poder testearla con getters
    falsos, sin ventana real (mismo criterio que SS11 del plan para
    `valores_iniciales` de dotacion). Devuelve None si algo no valida (ya
    avisado con messagebox)."""
    ctx = {}
    inputs = pantalla.get("inputs", [])
    for inp in inputs:
        valor = getters[inp["key"]]()
        obligatorio = inp.get("obligatorio", True)
        if callable(obligatorio):
            # SM Actividades lo necesita (docs/GUI_2.0_plan.md SS6): ADA/Grupal
            # dejan de ser obligatorios SOLO si es una corrida solo-cuestionarios
            # (checkbox 'Incluir cuestionarios' marcado, con archivos, y ni ADA
            # ni Grupal elegidos) -- una condicion que depende de OTRO input, no
            # de esta pantalla en abstracto.
            obligatorio = obligatorio(getters)
        if inp.get("multi"):
            if obligatorio and not valor:
                messagebox.showwarning(
                    "Falta un archivo", f"Carga al menos un archivo: {inp['etiqueta']}")
                return None
            ctx[inp["key"]] = [Path(v) for v in valor]
        else:
            if obligatorio:
                p = runner.valida_ruta(valor, messagebox)
                if p is None:
                    return None
                ctx[inp["key"]] = p
            else:
                ctx[inp["key"]] = Path(valor) if (valor or "").strip() else None

    if get_mes:
        mes = get_mes()
        if mes is None:
            messagebox.showwarning("Mes invalido", "Ano y mes deben ser numeros.")
            return None
        ctx["mes"] = mes

    if get_carpeta:
        defecto = None
        primer_obligatorio = next((i for i in inputs if i.get("obligatorio", True)), None)
        if primer_obligatorio:
            v = ctx.get(primer_obligatorio["key"])
            if isinstance(v, list):
                defecto = v[0].parent if v else None
            elif v is not None:
                defecto = v.parent
        carpeta = runner.valida_carpeta(get_carpeta(), messagebox, defecto=defecto)
        if carpeta is None:
            return None
        ctx["carpeta"] = carpeta

    for extra in pantalla.get("extras", []):
        key = extra.get("key")
        if key and key in getters:
            ctx[key] = getters[key]()

    return ctx


class App(ctk.CTk):
    """Ventana principal: sidebar agrupado por programa + area de contenido
    que intercambia frames por `tkraise` (SS4 del plan: construccion PEREZOSA,
    una pagina se arma recien la primera vez que se visita).

    `registro=None` -> se descubre via `gui.registro.cargar_registro()`
    (comportamiento real). Pasar una lista propia sirve para probar el shell
    con una PANTALLA de mentira sin tener que dejarla en gui/paginas/."""

    def __init__(self, registro=None):
        super().__init__()
        self.title(f"autoREM {VERSION}")
        # Ancho por defecto (feedback del autor, sep-2026: 1000 quedaba
        # estrecho contra las instrucciones/etiquetas largas de las paginas).
        self.geometry("1180x820")
        self.minsize(980, 680)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.registro = registro if registro is not None else cargar_registro()
        self._frames = {}         # id -> CTkFrame ya construido (perezoso)
        self._logs = {}           # id -> log(msg) (existe recien tras construir la pagina)
        self._on_procesar = {}    # id -> callable, expuesto para poder testear sin click real
        self._getters = {}        # id -> {key: getter}, idem (inyectar valores sin clickear dialogos)
        self._botones_sidebar = {}

        self._construir_sidebar()

        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.grid(row=0, column=1, sticky="nsew", padx=(4, 0))
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)

        if self.registro:
            self.mostrar(self.registro[0]["id"])

    # -- Sidebar / router ------------------------------------------------
    def _construir_sidebar(self):
        barra = ctk.CTkScrollableFrame(self, width=ANCHO_SIDEBAR,
                                       label_text=f"autoREM {VERSION}")
        barra.grid(row=0, column=0, sticky="nsw")
        for programa in programas_en_orden(self.registro):
            ctk.CTkLabel(barra, text=programa.upper(), text_color=widgets.COLOR_ATENUADO,
                        anchor="w", font=ctk.CTkFont(size=11, weight="bold")
                        ).pack(fill="x", padx=6, pady=(10, 2))
            for pantalla in self.registro:
                if pantalla["programa"] != programa:
                    continue
                texto = pantalla["titulo"]
                if pantalla.get("estado") == "beta":
                    texto += "  [BETA]"
                btn = ctk.CTkButton(barra, text=texto, anchor="w", fg_color="transparent",
                                    command=lambda pid=pantalla["id"]: self.mostrar(pid))
                btn.pack(fill="x", padx=6, pady=1)
                self._botones_sidebar[pantalla["id"]] = btn

    def mostrar(self, pantalla_id):
        """Router: construye la pagina la PRIMERA vez (perezoso) y la trae al
        frente. Volver a una pagina ya visitada conserva sus rutas elegidas y
        el log de la corrida anterior (no se destruye nada)."""
        if pantalla_id not in self._frames:
            pantalla = next(p for p in self.registro if p["id"] == pantalla_id)
            self._frames[pantalla_id] = self._construir_pagina(pantalla)
        self._frames[pantalla_id].tkraise()
        for pid, btn in self._botones_sidebar.items():
            btn.configure(fg_color=("gray75", "gray25") if pid == pantalla_id else "transparent")

    # -- Construccion de una pagina desde su PANTALLA --------------------
    def _construir_pagina(self, pantalla):
        frame = ctk.CTkScrollableFrame(self.contenedor)
        frame.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(frame, text=pantalla["titulo"],
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(0, 6))
        if pantalla.get("instrucciones"):
            caja = widgets.caja_titulada(frame, "Instrucciones")
            caja.pack(fill="x", pady=(0, 8))
            widgets.etiqueta_envolvente(caja, pantalla["instrucciones"]
                                       ).pack(fill="x", padx=8, pady=(2, 8))
        widgets.aviso_sin_modificar(frame)

        getters = {}
        get_mes = [None]   # celda mutable: un extra "despues_de" un input puede
                           # necesitar pagina.mes() antes de que el SelectorMes
                           # exista (se pinta despues de los inputs, SS4 del plan)

        def pagina_ctx():
            return Pagina(self, getters, get_mes, self._log_de(pantalla["id"]))

        def pintar_extras(despues_de):
            for extra in pantalla.get("extras", []):
                if extra.get("despues_de") != despues_de:
                    continue
                valor = extra["construir"](frame, pagina_ctx())
                if valor is not None:
                    if "key" not in extra:
                        # Fail loud (CLAUDE.md SS_fail-loud): un extra que devuelve
                        # datos y no dice donde van en ctx es un bug de config de
                        # la pagina, no un caso de usuario -- mejor reventar ahora
                        # que perder el valor en silencio.
                        raise ValueError(
                            f"extras de '{pantalla['id']}' (despues_de={despues_de!r}): "
                            f"construir() devolvio un valor pero el extra no declara 'key'")
                    getters[extra["key"]] = valor

        inputs = pantalla.get("inputs", [])
        obligatorios = [i for i in inputs if i.get("obligatorio", True)]
        opcionales = [i for i in inputs if not i.get("obligatorio", True)]

        def pintar_input(inp):
            if inp.get("multi"):
                getters[inp["key"]] = widgets.fila_archivos(
                    frame, inp["etiqueta"], inp.get("titulo_dialogo", inp["etiqueta"]))
            else:
                var = ctk.StringVar()
                widgets.fila_archivo(frame, var, inp.get("titulo_dialogo", inp["etiqueta"]),
                                     etiqueta=inp["etiqueta"])
                getters[inp["key"]] = var.get

        for inp in obligatorios:
            pintar_input(inp)
            pintar_extras(inp["key"])

        if opcionales:
            widgets.separador_opcionales(frame)
            for inp in opcionales:
                pintar_input(inp)
                pintar_extras(inp["key"])

        # Carpeta ANTES que mes: mismo orden visual que traian A23/SM/BETA en
        # autorem.py (orden puramente cosmetico, sin efecto funcional).
        get_carpeta = widgets.fila_carpeta_salida(frame) if pantalla.get("carpeta_salida") else None

        if pantalla.get("mes"):
            get_mes[0] = widgets.selector_mes(frame, mes_anterior())

        pintar_extras(None)   # los que van "al final", antes del boton Procesar

        log, limpiar = widgets.crear_log(frame, self)
        self._logs[pantalla["id"]] = log

        barra_botones = ctk.CTkFrame(frame, fg_color="transparent")
        barra_botones.pack(fill="x")
        btn = ctk.CTkButton(barra_botones, text="Procesar")
        btn.pack(side="left")

        def on_procesar():
            limpiar()
            ctx = _resolver_ctx(pantalla, getters, get_mes[0], get_carpeta)
            if ctx is None:
                return
            if pantalla.get("preparar"):
                ctx = pantalla["preparar"](ctx, pagina_ctx())
                if ctx is None:   # preparar aborto (p.ej. ADA ilegible, mes vacio)
                    return

            def trabajo(log_hilo):
                return pantalla["correr"](ctx, log_hilo)

            def al_terminar(res, err):
                if err is not None:
                    runner.manejar_error(err, log, messagebox)
                    return
                texto = pantalla["resumen"](res) if pantalla.get("resumen") else "Listo."
                log(""); log("OK " + texto.replace("\n", " | "))
                carpeta = ctx.get("carpeta")
                if carpeta and messagebox.askyesno(
                        "Listo", texto + "\n\n¿Abrir la carpeta del resultado?"):
                    runner.abrir_carpeta(carpeta)

            runner.correr_con_reloj(self, barra_botones, btn, log, trabajo, al_terminar)

        btn.configure(command=on_procesar)
        self._on_procesar[pantalla["id"]] = on_procesar   # testeable sin click real
        self._getters[pantalla["id"]] = getters           # idem: inyectar valores sin dialogo
        return frame

    def _log_de(self, pantalla_id):
        """Log de una pagina, resuelto PEREZOSAMENTE: un extra puede recibir
        `pagina.log` antes de que `widgets.crear_log` exista todavia (se pinta
        al final de `_construir_pagina`); para cuando alguien lo LLAME de
        verdad (dentro de un boton, tras un click real) la pagina ya esta
        completa."""
        return lambda msg="": self._logs[pantalla_id](msg)


def lanzar():
    ctk.set_appearance_mode("light")
    App().mainloop()


if __name__ == "__main__":
    lanzar()
