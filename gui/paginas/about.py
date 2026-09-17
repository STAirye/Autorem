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
gui/paginas/about.py - Acerca de (paso 10 del plan, SS7 + SS7.1).

NO expone `PANTALLA` (mismo motivo que inicio.py): no procesa nada, no vive
en `gui.registro`, `gui.app` la registra a mano fuera del agrupado por
programa. Expone `construir(frame, app)`.

Contenido SS7: version + autor + licencia (boton que MUESTRA el texto
completo en un Toplevel -- no depende de que Windows tenga un programa
asociado a un archivo sin extension) + la frase "100% local" (redactada para
argumentar la whitelist de un .exe sin firmar ante TI, ya vive en CLAUDE.md
SS11 y ahi no la ve nadie) + credito de asistencia de IA + contacto SOLO la
URL del repo, sin correo (decidido con el autor, sep-2026 -- NO agregar un
correo aunque parezca que falta) + ediciones de catalogos DEIS (SS7.1a,
leidas de catalogos/FUENTES.json).

Modo avanzado (SS7.1b -- "version completa", decidido con el autor sep-2026,
con un ajuste tambien decidido con el autor): cargar a mano un .xlsx que
reemplace un catalogo, con el MISMO escaneo de PII que usa
`tools/scan_catalogo.py` antes de aceptarlo (rechazo duro si hay hallazgos,
igual que `catalogos_deis.py --slim`).

LIMITE A PROPOSITO -- por que NO persiste entre sesiones: una cascada
persistente (`~/.autorem/catalogos/`, la que describe SS7.1b del plan)
requiere extender la logica de `programas/catalogos.py` (su cascada
`cargar()`), y el plan es explicito: **ese cambio se hace en `main`, no en
esta rama** (SS7.1, aislamiento de ramas SS9.1) -- esta pagina es un
CONSUMIDOR de `catalogos.py`, no el lugar para tocar su logica. Por eso el
modo avanzado usa el parametro `entrada=` que `catalogos.cargar()` YA acepta
hoy: el reemplazo vale solo mientras el proceso sigue abierto (cache en
memoria de `catalogos._CACHE`), y se pierde al reiniciar. Ademas, hoy NINGUN
modulo de `modulos/` consulta `catalogos.cargar()` todavia (CLAUDE.md SS12:
"enchufar `en_rango` en el A23" sigue pendiente) -- se lo dice al usuario en
el mensaje de confirmacion para no prometer un efecto que hoy no existe."""

from pathlib import Path

import customtkinter as ctk

from programas.rem_utils import VERSION
from gui import widgets

REPO_URL = "https://github.com/STAirye/Autorem"

_LOCAL_TXT = (
    "Procesa todo localmente. No envía ningún dato a internet.\n"
    "Argumento para pedir la whitelist de un .exe sin firmar ante TI del servicio de "
    "salud: no hay nube que auditar (Ley 20.584 y 21.719)."
)

# nombre -> override de esta SESION (Path del .xlsx cargado a mano, o ausente
# si usa el catalogo incluido). Vive a nivel de modulo -- sobrevive a que el
# usuario salga y vuelva a "Acerca de", pero NO al reinicio del proceso
# (ver docstring: es a proposito, la persistencia real es tarea de main).
_OVERRIDES = {}


def _ruta_licencia():
    import sys
    if getattr(sys, "frozen", False):
        cand = Path(sys.executable).parent / "LICENSE"
        if cand.exists():
            return cand
    return Path(__file__).resolve().parent.parent.parent / "LICENSE"


def _ver_licencia(root):
    ruta = _ruta_licencia()
    try:
        contenido = ruta.read_text(encoding="utf-8")
    except OSError as e:
        contenido = f"No pude leer {ruta}:\n\n{e}"
    top = ctk.CTkToplevel(root)
    top.title("Licencia - GPL-3.0-or-later")
    top.geometry("700x600")
    txt = ctk.CTkTextbox(top, wrap="word", font=ctk.CTkFont(family="Consolas", size=12))
    txt.pack(fill="both", expand=True, padx=10, pady=10)
    txt.insert("1.0", contenido)
    txt.configure(state="disabled")


def _cargar_manual(nombre, root, refrescar):
    from tkinter import filedialog, messagebox
    ruta = filedialog.askopenfilename(
        title=f"Elige el .xlsx del catálogo '{nombre}' (DEIS)",
        filetypes=[("Excel", "*.xlsx"), ("Todos", "*.*")])
    if not ruta:
        return

    from tools.scan_catalogo import escanear
    try:
        hallazgos, _estructura, _filas = escanear(ruta)
    except Exception as e:   # noqa: BLE001  (archivo no legible como Excel, etc.)
        messagebox.showerror("No pude escanear el archivo", str(e))
        return
    if hallazgos:
        detalle = "\n".join(f"  [{t}] hoja {h} fila {i} col {j}: {d}"
                            for t, h, i, j, d in hallazgos[:15])
        if len(hallazgos) > 15:
            detalle += f"\n  ... y {len(hallazgos) - 15} más"
        messagebox.showerror(
            "Hallazgos de privacidad — rechazado",
            f"«{Path(ruta).name}» tiene {len(hallazgos)} hallazgo(s) con forma de RUT, "
            f"email o teléfono, y NO se puede cargar (CLAUDE.md regla 1):\n\n{detalle}\n\n"
            "Un catálogo DEIS real no debería tener ninguno — revisa el archivo.")
        return

    import programas.catalogos as cat
    try:
        d = cat.cargar(nombre, entrada=ruta, recargar=True)
    except Exception as e:   # noqa: BLE001
        messagebox.showerror("No pude leer el catálogo", str(e))
        return
    _OVERRIDES[nombre] = Path(ruta)
    messagebox.showinfo(
        "Cargado",
        f"'{nombre}': {len(d)} fila(s) leídas de {Path(ruta).name}.\n\n"
        "Vale SOLO para esta sesión — se pierde al cerrar autoREM (persistirlo entre "
        "sesiones es trabajo de main, no de esta rama, ver CLAUDE.md §12).\n\n"
        "Ojo: ningún módulo REM consulta todavía los catálogos DEIS (pendiente en "
        "CLAUDE.md §12), así que por ahora esto no cambia ningún resultado.")
    refrescar()


def _volver_a_embebido(nombre, refrescar):
    import programas.catalogos as cat
    cat.cargar(nombre, entrada=None, recargar=True)
    _OVERRIDES.pop(nombre, None)
    refrescar()


def _bloque_catalogos(frame, root):
    import programas.catalogos as cat
    caja = widgets.caja_titulada(frame, "Catálogos DEIS")
    caja.pack(fill="x", pady=(0, 8))
    contenido = ctk.CTkFrame(caja, fg_color="transparent")
    contenido.pack(fill="x", padx=8, pady=(2, 4))
    var_avanzado = ctk.BooleanVar(value=False)

    def refrescar():
        for w in contenido.winfo_children():
            w.destroy()
        try:
            fuentes = cat.fuentes()
        except Exception as e:   # noqa: BLE001
            widgets.etiqueta_envolvente(
                contenido, f"No pude leer catalogos/FUENTES.json: {e}").pack(fill="x")
            return
        if not fuentes:
            widgets.etiqueta_envolvente(
                contenido, "No encuentro catalogos/FUENTES.json — revisa que el "
                "empaquetado incluya la carpeta catalogos/ (CLAUDE.md §11)."
            ).pack(fill="x")
            return
        for nombre, meta in fuentes.items():
            fila = ctk.CTkFrame(contenido, fg_color="transparent")
            fila.pack(fill="x", pady=(2, 2))
            override = _OVERRIDES.get(nombre)
            estado = (f"cargado a mano: {override.name} (solo esta sesión)" if override
                     else "catálogo incluido en autoREM")
            texto = (f"{meta.get('titulo', nombre)}\n"
                    f"edición {meta.get('edicion', '?')} ({meta.get('generado', '?')}) · "
                    f"{meta.get('filas', '?')} filas · {estado}")
            widgets.etiqueta_envolvente(fila, texto).pack(side="left", fill="x", expand=True)
            if var_avanzado.get():
                botones = ctk.CTkFrame(fila, fg_color="transparent")
                botones.pack(side="right")
                ctk.CTkButton(botones, text="Cargar archivo…", width=130,
                             command=lambda n=nombre: _cargar_manual(n, root, refrescar)
                            ).pack(side="left", padx=(4, 0))
                if override:
                    ctk.CTkButton(botones, text="Volver al embebido", width=130,
                                 fg_color="transparent", border_width=1,
                                 command=lambda n=nombre: _volver_a_embebido(n, refrescar)
                                ).pack(side="left", padx=(4, 0))

    def on_avanzado():
        if var_avanzado.get():
            from tkinter import messagebox
            ok = messagebox.askyesno(
                "Modo avanzado",
                "Esto te deja cargar un .xlsx distinto para un catálogo DEIS (cie10 / "
                "eno / ges).\n\nHazlo SOLO si sabes exactamente qué edición estás "
                "cargando: hoy ningún módulo REM consulta estos catálogos todavía, "
                "pero cuando eso se conecte (CLAUDE.md §12), el catálogo cargado es el "
                "que se usa.\n\n¿Continuar?")
            if not ok:
                var_avanzado.set(False)
                return
        refrescar()

    ctk.CTkCheckBox(caja, text="Modo avanzado: actualizar catálogos a mano",
                    variable=var_avanzado, command=on_avanzado
                   ).pack(anchor="w", padx=8, pady=(0, 6))
    refrescar()


def construir(frame, app):
    ctk.CTkLabel(frame, text=f"autoREM {VERSION}",
                font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=(0, 8))

    caja_lic = widgets.caja_titulada(frame, "Licencia y privacidad")
    caja_lic.pack(fill="x", pady=(0, 8))
    widgets.etiqueta_envolvente(
        caja_lic, "Licencia: GPL-3.0-or-later.\n" + _LOCAL_TXT
    ).pack(fill="x", padx=8, pady=(2, 4))
    ctk.CTkButton(caja_lic, text="Ver licencia completa", width=180,
                 command=lambda: _ver_licencia(app)).pack(anchor="w", padx=8, pady=(0, 8))

    _bloque_catalogos(frame, app)

    caja_creditos = widgets.caja_titulada(frame, "Autor y créditos")
    caja_creditos.pack(fill="x", pady=(0, 8))
    widgets.etiqueta_envolvente(
        caja_creditos,
        "Simón Tobar — médico APS, CESFAM Dr. Luis Ferrada Urzúa (SSMC).\n"
        "El código de esta herramienta se escribió con asistencia de modelos de IA "
        "(Claude, Anthropic); el autor revisó, modificó e integró cada archivo "
        "(detalle en el encabezado de cada uno).\n"
        f"Contacto / reportar un problema: {REPO_URL}"
    ).pack(fill="x", padx=8, pady=(2, 8))
