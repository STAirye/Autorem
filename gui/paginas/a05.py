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
    var_acuse = ctk.BooleanVar(value=False)
    chk_acuse = ctk.CTkCheckBox(
        frame, variable=var_acuse,
        text="Entiendo que las columnas demográficas saldrán vacías")
    # La categoria se guarda JUNTO A LA RUTA para la que se calculo. Dos motivos:
    #   1. CARRERA: elegir dos archivos rapido lanza dos hilos, y si el primero
    #      termina DESPUES del segundo, pintaba la categoria del archivo viejo sobre
    #      el nuevo -> podia colar un Administrativo como IRIS (o bloquear un valido).
    #   2. RUTA TECLEADA/PEGADA (o precargada al arrastrar el archivo al exe): no pasa
    #      por "Examinar", asi que `on_elegido` nunca corre. Antes eso daba "Formato no
    #      reconocido", culpando a un archivo que puede estar perfecto.
    # Con la ruta como clave, `get()` sabe cuando lo que tiene NO corresponde y
    # `detectar_ahora()` (lo llama `preparar`) resuelve en el hilo GUI.
    estado = {"ruta": None, "categoria": None, "error": None}

    def _ruta_caja():
        # Una sola lectura de la caja para detectar, comparar y validar: con comillas
        # (Copiar como ruta de Windows) la deteccion abria OTRA ruta que la validada.
        return runner.limpiar_ruta(var_ruta.get())

    def _aplicar(categoria, ruta, error=None):
        if ruta != _ruta_caja():
            return          # resultado de una eleccion ya reemplazada: se descarta
        estado["ruta"] = ruta
        estado["categoria"] = categoria
        estado["error"] = error
        chk_acuse.pack_forget()
        if error is not None:
            # El motivo sale del MISMO arbol que `runner.manejar_error`, que es quien
            # da el dialogo con el arreglo concreto al apretar Procesar. El banner
            # resume; los dos no se pueden contradecir porque comparten la funcion.
            banner.mostrar("no_reconocido", runner.motivo_fuente(error))
        elif categoria == "iris":
            banner.mostrar("plena", "Formato detectado: IRIS")
            var_acuse.set(False)
        elif categoria == "administrativo":
            banner.mostrar("parcial", "Formato detectado: Administrativo.\n" + sm._DISCLAIMER_ADMIN)
            chk_acuse.pack(anchor="w", pady=(2, 6), after=banner)
        else:
            banner.mostrar("no_reconocido", sm._MSG_DESCONOCIDO)

    def _leer_categoria(ruta):
        """Formato del export leyendo SOLO el encabezado. Levanta lo que levante
        openpyxl: quien llama se lo pasa a `runner.manejar_error`, que distingue
        'no es un .xlsx' de 'esta abierto en Excel' de 'falta openpyxl' -- tres
        arreglos DISTINTOS que un `except Exception` generico aplastaba en uno solo
        ("Formato no reconocido"), culpando al contenido del export.

        Lee solo las primeras MAX_FILAS_HEADER filas: el click cuesta ~60 filas en
        vez de parsear el export completo (lo que hacia que la corrida leyera el
        archivo entero DOS veces: aca y despues en `sm.abrir_validado`). Con
        `abrir_xlsx_ro` y no un `read_only=True` pelado: ese modo acota la lectura a
        la <dimension> del .xlsx, y con la etiqueta rota el encabezado llegaba con
        UNA columna -> un IRIS valido salia 'Formato no reconocido'."""
        from programas.formatos import MAX_FILAS_HEADER
        from programas.rem_utils import primeras_filas
        return sm.detectar_formato_filas(primeras_filas(ruta, MAX_FILAS_HEADER))

    def _detectar(ruta):
        ruta = runner.limpiar_ruta(ruta)
        banner.mostrar("detectando", "Detectando formato...")

        # runner.en_hilo y NO frame.after(0,...) desde el hilo: Tk.after no es
        # thread-safe (ver la nota en runner.en_hilo).
        runner.en_hilo(frame, lambda: _leer_categoria(ruta),
                       lambda cat, err: _aplicar(cat, ruta, err))

    def detectar_ahora():
        """Detecta AQUI MISMO (hilo GUI, bloqueando) la ruta que este en la caja, si
        todavia no hay categoria para ELLA. La llama `preparar` justo antes de
        procesar: cubre la ruta tecleada/pegada/precargada, que no dispara
        `on_elegido`. Devuelve (categoria, error) -- ver `get()`."""
        ruta = _ruta_caja()
        if ruta and estado["ruta"] != ruta:
            try:
                _aplicar(_leer_categoria(ruta), ruta)
            except Exception as e:   # noqa: BLE001  (se despacha en `preparar`)
                _aplicar(None, ruta, e)
        return estado["categoria"], estado["error"]

    widgets.fila_archivo(frame, var_ruta, "Elige el export de Control de Salud Mental",
                         on_elegido=_detectar)
    banner = widgets.BannerFuente(frame)   # despues de la fila: se pinta debajo de ella

    # Ruta PRECARGADA (arrastrar el .xlsx sobre el exe, `pagina.datos['ruta_inicial']`):
    # se pinta y se detecta como si la hubiera elegido el usuario.
    inicial = runner.limpiar_ruta(pagina.datos.get("ruta_inicial"))
    if inicial:
        var_ruta.set(inicial)
        _detectar(inicial)

    def get():
        # `categoria`/`error` solo valen si son los de la ruta que HOY esta en la caja.
        ruta = _ruta_caja()
        vigente = estado["ruta"] == ruta
        return {"ruta": ruta,
                "categoria": estado["categoria"] if vigente else None,
                "error": estado["error"] if vigente else None,
                "acuse": var_acuse.get(),
                "detectar_ahora": detectar_ahora}
    return get


def bloque_periodo(frame, pagina):
    """Caja 'Periodo' propia de A05: archivo completo vs. un mes puntual (por
    FECHA FORMULARIO). NO es el SelectorMes generico de la pagina (SS3.1 del
    plan), pero el año/mes SI es `widgets.selector_mes`: mismos Spinbox, mismo
    parseo, bajo el mismo test que amarra los años a `valida_mes`."""
    caja = widgets.caja_titulada(frame, "Período")
    caja.pack(fill="x", pady=(2, 6))
    var_periodo = ctk.StringVar(value="todo")
    ctk.CTkRadioButton(caja, text="Archivo completo", value="todo",
                       variable=var_periodo).pack(anchor="w", padx=8, pady=(6, 2))
    fila_mes = ctk.CTkFrame(caja, fg_color="transparent")
    fila_mes.pack(anchor="w", fill="x", padx=8, pady=(0, 6))
    ctk.CTkRadioButton(fila_mes, text="Un mes (año / mes):", value="mes",
                       variable=var_periodo).pack(side="left")
    get_mes = widgets.selector_mes(fila_mes, mes_anterior(), etiqueta=None)

    def _on_periodo(*_):
        activo = "normal" if var_periodo.get() == "mes" else "disabled"
        for spin in get_mes.spinboxes:
            spin.configure(state=activo)
    var_periodo.trace_add("write", _on_periodo)
    _on_periodo()

    def get():
        if var_periodo.get() != "mes":
            return {"modo": "todo"}
        return {"modo": "mes", "mes": get_mes()}   # (año, mes) o None si no son numeros
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

    # Ruta tecleada/pegada/precargada: no paso por "Examinar", asi que no hay
    # categoria todavia. Se detecta aca (hilo GUI) en vez de decirle al usuario
    # "formato no reconocido" sobre un archivo que puede estar perfecto.
    categoria, error = archivo["categoria"], archivo["error"]
    if categoria is None and error is None:
        categoria, error = archivo["detectar_ahora"]()
    if error is not None:
        # NO "Formato no reconocido": el archivo puede estar impecable y ser un .xls
        # disfrazado de .xlsx (el clasico de RAYEN, CLAUDE.md SS13), o estar abierto en
        # Excel, o faltar openpyxl. `manejar_error` los distingue y da el arreglo de
        # CADA uno -- decirle "no reconozco las firmas del export" a las tres manda a
        # re-descargar un archivo que no tiene nada de malo.
        runner.manejar_error(error, pagina.log, messagebox)
        return None
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
        mes = runner.valida_mes(periodo["mes"], messagebox)   # None (no son numeros) incluido
        if mes is None:
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
