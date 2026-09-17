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
gui/paginas/a05.py - REM A05 Egresos/Ingresos: paso 8 del plan.

Portada de autorem.py._tab_a05 sin tocar la logica (docs/GUI_2.0_plan.md SS8),
con DOS cambios de fondo pedidos explicitamente por el plan:

1. Se saca el selector IRIS/Administrativo (SS5, CLAUDE.md SS12): el selector
   no le puede ganar a la deteccion (`sm.abrir_validado` bloquea igual si no
   calza), asi que solo aportaba una forma de equivocarse. Ahora se detecta
   el formato SOLO al elegir el archivo (deteccion barata: mira el
   encabezado) y se estrena `widgets.BannerFuente` (SS5.1) para mostrarlo.
2. `inputs`/`mes`/`carpeta_salida` quedan vacios/False a proposito: TODO en
   esta pagina (archivo+formato, Periodo, Tareas, Carpeta) vive en `extras`
   'despues_de': None, en el orden en que deben pintarse -- ninguno es un
   input generico (Periodo NO es el SelectorMes, SS3.1 del plan) y ninguno
   necesita interleave con otro input. La validacion completa (existe el
   archivo, formato reconocido, acuse si es Administrativo, mes valido,
   >=1 tarea, carpeta valida) vive en `preparar` porque usa `messagebox` y
   tiene que correr en el hilo GUI, antes del worker (SS3.3).

`_correr_tareas`/`_resumen_texto`/`TAREAS`/`buscar_tarea` se quedan en
autorem.py (SS2 del plan: no son GUI, y tests/test_autorem.py los usa) --
esta pagina los importa en vez de duplicarlos.
"""

import threading

import customtkinter as ctk

import programas.rem_saludmental as sm
from programas.rem_utils import mes_anterior
from gui import widgets, runner

instrucciones = (
    "1.  Descarga el Excel del formulario «Control de Salud Mental»:\n"
    "     A) IRIS: Formularios RAYEN -> Control de Salud Mental -> todos los metacampos, Situación TODOS, Estado AMBOS.\n"
    "     B) RAYEN: Herramientas -> Informe Estadístico -> Impresión Formularios Clínicos -> Reporte Administrativo.\n"
    "2.  Elige el archivo: el formato (IRIS / Administrativo) se detecta solo.\n"
    "3.  Elige el PERÍODO: archivo completo, o un mes puntual (por FECHA FORMULARIO).\n"
    "4.  Marca la(s) TAREA(s) y «Procesar» -> «…_procesado.xlsx» con una hoja por tarea.\n"
    "     Tu archivo original NO se modifica."
)


def bloque_archivo_formato(frame, pagina):
    """Archivo + deteccion automatica de formato (SS5 del plan). Al elegir el
    archivo se abre en un HILO (puede ser lento en un export grande) y se
    pinta un BannerFuente con el resultado -- la ventana no se congela, el
    banner dice 'Detectando...' mientras tanto."""
    var_ruta = ctk.StringVar()
    banner = widgets.BannerFuente(frame)
    var_acuse = ctk.BooleanVar(value=False)
    chk_acuse = ctk.CTkCheckBox(
        frame, variable=var_acuse,
        text="Entiendo que las columnas demográficas saldrán vacías")
    estado = {"categoria": None}

    def _aplicar(categoria):
        estado["categoria"] = categoria
        chk_acuse.pack_forget()
        if categoria == "iris":
            banner.mostrar("plena", "Formato detectado: IRIS")
            var_acuse.set(False)
        elif categoria == "administrativo":
            banner.mostrar("parcial", "Formato detectado: Administrativo.\n" + sm._DISCLAIMER_ADMIN)
            chk_acuse.pack(anchor="w", pady=(2, 6))
        elif categoria == "error_lectura":
            banner.mostrar("no_reconocido", "No pude abrir el archivo para detectar el formato "
                           "(¿esta abierto en Excel, o no es un .xlsx real?).")
        else:
            banner.mostrar("no_reconocido", sm._MSG_DESCONOCIDO)

    def _detectar(ruta):
        banner.mostrar("detectando", "Detectando formato...")

        def trabajo():
            try:
                import openpyxl
                wb = openpyxl.load_workbook(ruta, read_only=True, data_only=True)
                categoria = sm.detectar_formato(wb.active)
                wb.close()
            except Exception:   # noqa: BLE001  (cualquier falla al abrir -> banner rojo, no traceback)
                categoria = "error_lectura"
            frame.after(0, lambda: _aplicar(categoria))

        threading.Thread(target=trabajo, daemon=True).start()

    widgets.fila_archivo(frame, var_ruta, "Elige el export de Control de Salud Mental",
                         on_elegido=_detectar)

    def get():
        return {"ruta": var_ruta.get(), "categoria": estado["categoria"],
               "acuse": var_acuse.get()}
    return get


def bloque_periodo(frame, pagina):
    """Caja 'Periodo' propia de A05: archivo completo vs. un mes puntual (por
    FECHA FORMULARIO). NO es el SelectorMes generico (SS3.1 del plan)."""
    from tkinter import ttk
    y0, m0 = mes_anterior()
    caja = widgets.caja_titulada(frame, "Período")
    caja.pack(fill="x", pady=(2, 6))
    var_periodo = ctk.StringVar(value="todo")
    ctk.CTkRadioButton(caja, text="Archivo completo", value="todo",
                       variable=var_periodo).pack(anchor="w", padx=8, pady=(6, 2))
    fila_mes = ctk.CTkFrame(caja, fg_color="transparent")
    fila_mes.pack(anchor="w", fill="x", padx=8, pady=(0, 6))
    ctk.CTkRadioButton(fila_mes, text="Un mes (año / mes):", value="mes",
                       variable=var_periodo).pack(side="left")
    var_anio = ctk.StringVar(value=str(y0))
    var_mes = ctk.StringVar(value=str(m0))
    spin_anio = ttk.Spinbox(fila_mes, from_=2020, to=2100, width=6, textvariable=var_anio)
    spin_anio.pack(side="left", padx=(6, 2))
    spin_mes = ttk.Spinbox(fila_mes, from_=1, to=12, width=4, textvariable=var_mes)
    spin_mes.pack(side="left")

    def _on_periodo(*_):
        activo = "normal" if var_periodo.get() == "mes" else "disabled"
        spin_anio.configure(state=activo)
        spin_mes.configure(state=activo)
    var_periodo.trace_add("write", _on_periodo)
    _on_periodo()

    def get():
        if var_periodo.get() != "mes":
            return {"modo": "todo"}
        return {"modo": "mes", "anio": var_anio.get(), "mes_str": var_mes.get()}
    return get


def bloque_tareas(frame, pagina):
    from autorem import TAREAS
    caja = widgets.caja_titulada(frame, "Tareas a ejecutar")
    caja.pack(fill="x", pady=(2, 6))
    checks = {}
    for t in TAREAS:
        var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(caja, text=t["nombre"], variable=var).pack(anchor="w", padx=8, pady=2)
        checks[t["id"]] = var

    def get():
        return [tid for tid, var in checks.items() if var.get()]
    return get


def bloque_carpeta(frame, pagina):
    return widgets.fila_carpeta_salida(frame)


def preparar(ctx, pagina):
    import tkinter.messagebox as messagebox
    from autorem import buscar_tarea

    archivo = ctx["archivo"]
    entrada = runner.valida_ruta(archivo["ruta"], messagebox)
    if entrada is None:
        return None

    categoria = archivo["categoria"]
    if categoria not in ("iris", "administrativo"):
        messagebox.showerror("Formato no reconocido", sm._MSG_DESCONOCIDO)
        return None
    if categoria == "administrativo" and not archivo["acuse"]:
        messagebox.showwarning(
            "Falta el acuse", "Marca la casilla que confirma que entiendes que las "
            "columnas demográficas saldrán vacías (formato Administrativo).")
        return None

    periodo = ctx["periodo"]
    mes = None
    if periodo["modo"] == "mes":
        try:
            mes = (int(periodo["anio"]), int(periodo["mes_str"]))
        except ValueError:
            messagebox.showwarning("Mes inválido", "Año y mes deben ser números.")
            return None
        if not (1 <= mes[1] <= 12):
            messagebox.showwarning("Mes inválido", "El mes debe estar entre 1 y 12.")
            return None

    tareas_ids = ctx["tareas"]
    if not tareas_ids:
        messagebox.showwarning("Sin tareas", "Marca al menos una tarea.")
        return None
    seleccionadas = [buscar_tarea(tid) for tid in tareas_ids]

    carpeta = runner.valida_carpeta(ctx["carpeta"], messagebox, defecto=entrada.parent)
    if carpeta is None:
        return None

    perfil = sm.perfil_por_id(categoria)
    return {"entrada": entrada, "perfil": perfil, "tareas": seleccionadas,
           "mes": mes, "carpeta": carpeta}


def correr(ctx, log):
    from autorem import _correr_tareas
    perfil = ctx["perfil"]
    if perfil.get("disclaimer"):
        log(perfil["disclaimer"]); log("")
    resultados, salida = _correr_tareas(ctx["tareas"], ctx["entrada"], perfil, log,
                                        mes=ctx["mes"], carpeta=ctx["carpeta"])
    return {"resultados": resultados, "salida": salida}


def resumen(res):
    from autorem import _resumen_texto
    return _resumen_texto(res["resultados"], res["salida"])


PANTALLA = {
    "id": "a05",
    "programa": "Salud Mental",
    "titulo": "A05 · Egresos / Ingresos",
    "estado": "estable",
    "instrucciones": instrucciones,
    "inputs": [],
    "mes": False,
    "carpeta_salida": False,
    "extras": [
        {"despues_de": None, "construir": bloque_archivo_formato, "key": "archivo"},
        {"despues_de": None, "construir": bloque_periodo, "key": "periodo"},
        {"despues_de": None, "construir": bloque_tareas, "key": "tareas"},
        {"despues_de": None, "construir": bloque_carpeta, "key": "carpeta"},
    ],
    "preparar": preparar,
    "correr": correr,
    "resumen": resumen,
}
