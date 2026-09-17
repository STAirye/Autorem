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
gui/dialogos.py - modales compartidos: Estamentos + Dotacion (GUI 2.0).

Portados de autorem.py sin tocar la logica (docs/GUI_2.0_plan.md, paso 6):
mismo comportamiento e INVARIANTES, otro toolkit (CTkToplevel/CTkScrollableFrame/
CTkTabview en vez de Toplevel + Canvas-a-mano + ttk.Notebook). Van aca (no a
una pagina especifica) porque son modales reutilizables por mas de una
pantalla: Estamentos lo usan A03 y cualquier flujo Administrativo; Dotacion
hoy la usa SM Actividades y cualquier modulo futuro con el mismo problema.

INVARIANTES DE DOTACION que el port NO puede perder (cada una costo un bug o
una decision explicita, ver docs/dotacion_externos_plan.md):
  - El tick arranca en la clase YA GUARDADA, no en False (`valores_iniciales`,
    extraida como funcion PURA para poder testearla sin ventana -- SS11 del
    plan: "es de las pocas logicas de GUI que ya fallo una vez", bug de 1.9.9).
  - 'Omitir estamento' es INMEDIATO (persiste al click) y saca a esos nombres
    de `checks`: si quedaran, 'Aplicar' los marcaria 'interno' -- un omitido
    debe seguir 'desconocido'.
  - 'Cancelar' no clasifica a nadie.
  - El dialogo recibe `modulo` porque las omisiones se indexan por modulo.
"""

import tkinter as tk

import customtkinter as ctk

from programas import dotacion


# -- Estamentos (reutilizable por cualquier flujo en formato Administrativo) --
def bloque_estamentos(parent):
    """Cuadro para cargar la tabla de estamentos ('Utilizacion de Cupos'), con
    el porque y las instrucciones. Devuelve get_ruta() -> str (ruta elegida,
    '' si nada)."""
    from gui.widgets import fila_archivo, caja_titulada, etiqueta_envolvente, COLOR_AVISO
    caja = caja_titulada(parent, "Estamentos (para formato Administrativo)")
    caja.pack(fill="x", pady=(2, 6))
    etiqueta_envolvente(caja, text_color=COLOR_AVISO, text=(
        "¿Por qué? El reporte Administrativo NO indica el estamento de quien atendió, "
        "solo el nombre.\nLa tabla del equipo QUEDA GUARDADA (caché en ~/.autorem): "
        "cárgala una vez y los meses siguientes se autocompleta sola.\nVuelve a cargar "
        "'Utilización de Cupos' solo cuando cambie el equipo (se fusiona con lo guardado).")
        ).pack(fill="x", padx=8, pady=(4, 0))
    etiqueta_envolvente(caja, text=(
        "En RAYEN Administrativo, descarga un reporte desde  Herramientas -> Reportes "
        "Estadísticos -> Otros -> Utilización de Cupos,\ncon fecha de un día en que hubo "
        "atenciones de TODO tu equipo. Copia el reporte completo, pásalo a Excel y "
        "cárgalo aquí.  (Opcional si ya lo cargaste antes.)")).pack(fill="x", padx=8, pady=(4, 4))
    var = tk.StringVar()
    fila_archivo(caja, var, "Elige el reporte 'Utilización de Cupos'")
    return lambda: (var.get() or "").strip().strip('"').strip("'")


def resolver_estamentos(root, faltantes, opciones):
    """Failsafe modal: por cada funcionario SIN estamento en la tabla, elegir
    uno o IGNORAR (externo que presta servicios transitorios). Devuelve
    {nombre: estamento | None} (None = ignorar). {} si se cancela."""
    IGN = "— Ignorar (externo / transitorio) —"
    top = ctk.CTkToplevel(root)
    top.title("Estamentos sin identificar")
    top.transient(root); top.grab_set()
    ctk.CTkLabel(top, justify="left", text=(
        f"{len(faltantes)} profesional(es) no están en la tabla «Utilización de Cupos».\n"
        "Asigna su estamento, o Ignóralos si son externos que prestan servicios "
        "transitorios.")).pack(anchor="w", padx=12, pady=12)
    cont = ctk.CTkFrame(top, fg_color="transparent")
    cont.pack(fill="both", expand=True, padx=12)
    ops = [IGN] + list(opciones)
    vars_ = {}
    for nombre in faltantes:
        fila = ctk.CTkFrame(cont, fg_color="transparent")
        fila.pack(fill="x", pady=2)
        ctk.CTkLabel(fila, text=nombre, anchor="w", width=220).pack(side="left", padx=(0, 10))
        v = tk.StringVar(value=ops[0])
        ctk.CTkOptionMenu(fila, variable=v, values=ops).pack(side="left")
        vars_[nombre] = v
    res = {}

    def aplicar():
        for nombre, v in vars_.items():
            val = v.get()
            res[nombre] = None if val == IGN else val
        top.destroy()

    barra = ctk.CTkFrame(top, fg_color="transparent")
    barra.pack(fill="x", padx=12, pady=12)
    ctk.CTkButton(barra, text="Aplicar", command=aplicar).pack(side="right")
    ctk.CTkButton(barra, text="Cancelar", command=top.destroy, fg_color="transparent"
                 ).pack(side="right", padx=6)
    top.wait_window()
    return res


# -- Dotacion: separar funcionarios EXTERNOS (docs/dotacion_externos_plan.md) --
def valores_iniciales(nombres, tabla):
    """nombre -> tick inicial (True = externo) para el dialogo de dotacion.

    Arranca en la clase YA GUARDADA en `tabla`, NUNCA en False: con un default
    fijo, un 'Aplicar' sobre gente ya clasificada le borraria la marca de
    externo EN SILENCIO (bug de 1.9.9). Para un nombre nuevo `dotacion.clase`
    da 'desconocido' -> False = interno (el default del plan de dotacion, SS1.3).

    Funcion PURA (sin widgets): testeable sin ventana (SS11 del plan)."""
    return {nombre: (dotacion.clase(nombre, tabla) == dotacion.EXTERNO) for nombre in nombres}


def dotacion_ada(root, modulo, ada, mes, log, messagebox, mask=None, todos=False):
    """Carga el ADA, lo filtra al `mes` y abre el dialogo de dotacion.

    `mask(serie_act_norm)` -> booleana con las filas que TRIBUTAN al REM de
    ese modulo; sin ella se preguntaria por gente cuyo trabajo no entra a
    este REM. `todos=True` muestra TODOS los funcionarios del ADA (boton
    'Precargar dotacion': sirve para el veto inicial y para corregir a
    alguien ya clasificado); por defecto solo los que faltan clasificar.

    Devuelve (d, tabla) -- `d` es el ADA YA cargado, para que quien procese
    despues no lo relea. (None, None) si el archivo no se pudo leer."""
    from programas.rem_utils import cargar_atenciones, filtrar_mes, _rango_mes
    # Esto BLOQUEA la GUI y no hay como evitarlo: el dialogo que viene despues
    # es Tk y tiene que correr en este hilo (mandarlo a un worker revienta). Lo
    # que si se puede es que no PAREZCA colgada -- cursor de espera + repintar
    # el log antes de arrancar.
    log("[dotacion] cargando el ADA (la ventana queda quieta unos segundos)...")
    try:
        root.configure(cursor="watch")
        root.update()
    except Exception:            # noqa: BLE001  (sin GUI / root ya destruido)
        pass
    try:
        d = cargar_atenciones(ada, log=log)
        ini, fin = _rango_mes(mes)
        dm = filtrar_mes(d, ini, fin, "el ADA (Atenciones Diarias Ambulatorias)")
    except Exception as e:   # noqa: BLE001
        from gui.runner import manejar_error
        manejar_error(e, log, messagebox)
        return None, None
    finally:
        try:
            root.configure(cursor="")
        except Exception:    # noqa: BLE001
            pass
    tabla = dotacion.cargar(log=log)
    trib = dm[mask(dm["ACT_n"])] if mask else dm
    ev = dotacion.evidencia(trib, tabla, modulo=modulo)
    log(f"[dotacion] {len(ev)} funcionario(s) en {len(trib)} atenciones que tributan.")
    filas = ev if todos else dotacion.nuevos(ev, tabla, modulo)
    if len(filas):
        dialogo_dotacion(root, tabla, modulo, filas)
    elif todos:
        messagebox.showinfo(
            "Dotación", "El ADA no trae funcionarios con atenciones que tributen a "
            "este REM en el mes elegido. Revisa el archivo y el mes.")
    else:
        log("[dotacion] sin funcionarios nuevos que clasificar.")
    return d, tabla


def bloque_dotacion(parent, modulo, get_ada, get_mes, log, mask=None):
    """Cuadro informativo + 'Precargar dotación…' y 'Revisar dotación…'.
    Reutilizable por cualquier modulo con el mismo problema (hoy solo SM).

    VA DEBAJO de los selectores de archivo: necesita el ADA cargado y el mes
    elegido para tener algo que mostrar. `get_ada`/`get_mes` son los getters
    de la pagina; `mask` filtra a lo que tributa a ese REM."""
    import tkinter.messagebox as messagebox
    from gui.widgets import caja_titulada, etiqueta_envolvente, COLOR_AVISO
    caja = caja_titulada(parent, "Dotación (separar funcionarios externos)")
    caja.pack(fill="x", pady=(2, 6))
    etiqueta_envolvente(caja, text_color=COLOR_AVISO, text=(
        "¿Por qué? El ADA trae atenciones a nuestros usuarios hechas por funcionarios que "
        "NO son de tu dotación (p.ej. la sala AIDIA); no deben tributar a este REM (doble "
        "conteo).\nLa PRIMERA vez hay que vetar el equipo completo: carga el ADA y el mes "
        "aquí arriba y aprieta «Precargar dotación…». Después, al Procesar se pregunta solo "
        "por los nombres nuevos.\nLa tabla queda GUARDADA (caché en ~/.autorem/dotacion.json).")
        ).pack(fill="x", padx=8, pady=(4, 4))

    def _precargar():
        ada = get_ada()
        if not ada:
            messagebox.showwarning(
                "Falta el ADA", "Primero carga el archivo de Atenciones / Diagnósticos / "
                "Actividades y elige el mes; recién ahí puedo mostrarte los funcionarios.")
            return
        mes = get_mes()
        if mes is None:
            messagebox.showwarning("Mes inválido", "Año y mes deben ser números.")
            return
        dotacion_ada(parent.winfo_toplevel(), modulo, ada, mes, log, messagebox,
                     mask=mask, todos=True)

    barra = ctk.CTkFrame(caja, fg_color="transparent")
    barra.pack(anchor="w", padx=8, pady=(0, 6))
    ctk.CTkButton(barra, text="Precargar dotación…", command=_precargar).pack(side="left")
    ctk.CTkButton(barra, text="Revisar dotación…", fg_color="transparent",
                 command=lambda: revisar_dotacion(parent.winfo_toplevel(), modulo)
                 ).pack(side="left", padx=6)


def _grupo_dotacion(inner, estamento, filas, checks, tabla, modulo, con_evidencia):
    """UN grupo (estamento) del dialogo: cabecera con costo de omitir +
    colapsar/expandir + 'Omitir estamento', y un CTkCheckBox por funcionario
    (tick = externo). `filas` = sub-DataFrame de ese estamento. Puebla
    `checks` {nombre: BooleanVar} in-place; no devuelve nada."""
    n_func = len(filas)
    n_at = int(filas["n_atenciones"].sum()) if con_evidencia and "n_atenciones" in filas else None
    cab = ctk.CTkFrame(inner, fg_color="transparent")
    cab.pack(fill="x", pady=(6, 0))
    costo = f"{n_func} funcionario(s)" + (f" · {n_at} atenciones" if n_at is not None else "")
    var_abierto = tk.BooleanVar(value=True)
    cuerpo = ctk.CTkFrame(inner, fg_color="transparent")

    def _toggle():
        if var_abierto.get():
            cuerpo.pack(fill="x", padx=(18, 0))
        else:
            cuerpo.pack_forget()

    ctk.CTkCheckBox(cab, text=f"{estamento or '(sin estamento)'}   {costo}",
                    variable=var_abierto, command=_toggle).pack(side="left")

    nombres_grupo = list(filas["funcionario"])

    def _omitir():
        # Inmediato: persiste la omision YA y saca a estos funcionarios de
        # `checks` -- si quedaran, un 'Aplicar' posterior los marcaria
        # 'interno' (tick sin marcar = interno), violando la regla de que un
        # omitido sigue 'desconocido' hasta que alguien lo revise a mano.
        dotacion.omitir(tabla, modulo, [estamento])
        for n in nombres_grupo:
            checks.pop(n, None)
        cab.destroy(); cuerpo.destroy()

    ctk.CTkButton(cab, text="Omitir estamento", width=120, command=_omitir).pack(side="right")
    cuerpo.pack(fill="x", padx=(18, 0))

    iniciales = valores_iniciales(nombres_grupo, tabla)
    for _, fila in filas.iterrows():
        nombre = fila["funcionario"]
        v = tk.BooleanVar(value=iniciales[nombre])
        checks[nombre] = v
        detalle = ""
        if con_evidencia:
            detalle = f"   ({int(fila.get('n_atenciones', 0))} at.)"
            act = str(fila.get("actividades", "") or "")
            if act:
                detalle += f" — {act}"
        ctk.CTkCheckBox(cuerpo, text=f"{nombre}{detalle}", variable=v).pack(anchor="w", pady=1)


def dialogo_dotacion(root, tabla, modulo, filas, con_evidencia=True,
                     titulo="Dotación: clasificar funcionarios"):
    """Dialogo modal: ticks agrupados por estamento. Tick = externo, sin tick
    = interno (default). 'Omitir estamento' es INMEDIATO (se persiste al
    click, no espera 'Aplicar') y deja a esos funcionarios `desconocido` --
    nunca `interno`. 'Aplicar' clasifica los ticks restantes via
    `dotacion.marcar()` (persiste). 'Cancelar' no clasifica a nadie: los
    nombres quedan `desconocido` y la corrida sigue igual."""
    if filas is None or filas.empty:
        return
    top = ctk.CTkToplevel(root)
    top.title(titulo)
    top.transient(root); top.grab_set()
    top.geometry("720x560")
    ctk.CTkLabel(top, justify="left", text=(
        f"{len(filas)} funcionario(s). Marca el tick de quienes NO son de tu dotación "
        "(externos). Sin tick = interno.")).pack(anchor="w", padx=12, pady=12)

    inner = ctk.CTkScrollableFrame(top)
    inner.pack(fill="both", expand=True, padx=12)

    checks = {}
    por_est = filas.attrs.get("por_estamento") if hasattr(filas, "attrs") else None
    if por_est is not None and len(por_est):
        orden = [e for e in por_est["estamento"] if e in set(filas["estamento"])]
    else:
        orden = sorted(filas["estamento"].unique())
    for est in orden:
        sub = filas[filas["estamento"] == est]
        if sub.empty:
            continue
        _grupo_dotacion(inner, est, sub, checks, tabla, modulo, con_evidencia)

    def aplicar():
        dotacion.marcar(tabla, {n: v.get() for n, v in checks.items()})
        top.destroy()

    barra = ctk.CTkFrame(top, fg_color="transparent")
    barra.pack(fill="x", padx=12, pady=12)
    ctk.CTkButton(barra, text="Aplicar", command=aplicar).pack(side="right")
    ctk.CTkButton(barra, text="Cancelar", command=top.destroy, fg_color="transparent"
                 ).pack(side="right", padx=6)
    top.wait_window()


def revisar_dotacion(root, modulo="sm"):
    """Reabre la clasificacion GUARDADA (todos los funcionarios ya vistos +
    estamentos omitidos), sin necesitar un ADA cargado -- por eso NO hay
    evidencia (n_atenciones/actividades): solo el nombre y su clase actual.
    Permite revertir una clasificacion o una omision equivocada."""
    import tkinter.messagebox as messagebox
    tabla = dotacion.cargar()
    func = tabla.get("funcionarios", {})
    if not func and not tabla.get("omitidos"):
        messagebox.showinfo(
            "Dotación", "Todavía no hay ningún funcionario clasificado.\n\n"
            "Esta ventana solo muestra lo YA guardado. Para poblarla: carga el ADA, "
            "elige el mes y aprieta «Precargar dotación…» (o procesa y se preguntará "
            "por los nombres nuevos).")
        return
    top = ctk.CTkToplevel(root)
    top.title("Revisar dotación")
    top.transient(root); top.grab_set()
    top.geometry("560x560")

    tabview = ctk.CTkTabview(top)
    tabview.pack(fill="both", expand=True, padx=12, pady=12)
    tabview.add("Funcionarios")
    tabview.add("Estamentos omitidos")

    # -- Funcionarios clasificados (lista plana: sin ADA no hay estamento) --
    tab1 = tabview.tab("Funcionarios")
    ctk.CTkLabel(tab1, justify="left", text=(
        "Tick = externo, sin tick = interno. 'Aplicar' guarda los cambios.")
        ).pack(anchor="w", pady=(0, 6))
    cont1 = ctk.CTkScrollableFrame(tab1)
    cont1.pack(fill="both", expand=True)
    checks = {}
    iniciales = valores_iniciales(func.keys(), tabla)
    for nombre_norm in sorted(func):
        v = tk.BooleanVar(value=iniciales[nombre_norm])
        checks[nombre_norm] = v
        ctk.CTkCheckBox(cont1, text=nombre_norm, variable=v).pack(anchor="w", pady=1)

    # -- Estamentos omitidos (por modulo) --
    tab2 = tabview.tab("Estamentos omitidos")
    cont2 = ctk.CTkFrame(tab2, fg_color="transparent")
    cont2.pack(fill="both", expand=True)

    def _pintar_omitidos():
        for w in cont2.winfo_children():
            w.destroy()
        ests = dotacion.omitidos(tabla, modulo)
        if not ests:
            ctk.CTkLabel(cont2, text=f"Ningún estamento omitido en '{modulo}'.").pack(anchor="w")
            return
        for est in ests:
            fila = ctk.CTkFrame(cont2, fg_color="transparent")
            fila.pack(fill="x", pady=1)
            ctk.CTkLabel(fila, text=est).pack(side="left")

            def _quitar(e=est):
                tabla["omitidos"][modulo] = [x for x in tabla["omitidos"].get(modulo, []) if x != e]
                dotacion.guardar(tabla)
                _pintar_omitidos()
            ctk.CTkButton(fila, text="Quitar omisión", width=120, command=_quitar).pack(side="right")

    _pintar_omitidos()

    def aplicar():
        dotacion.marcar(tabla, {n: v.get() for n, v in checks.items()})
        top.destroy()

    barra = ctk.CTkFrame(top, fg_color="transparent")
    barra.pack(fill="x", padx=12, pady=(0, 12))
    ctk.CTkButton(barra, text="Aplicar", command=aplicar).pack(side="right")
    ctk.CTkButton(barra, text="Cerrar", command=top.destroy, fg_color="transparent"
                 ).pack(side="right", padx=6)
    top.wait_window()
