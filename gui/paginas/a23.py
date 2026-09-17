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
gui/paginas/a23.py - REM A23 (Respiratorio), primera pagina real de la 2.0.

Portada de autorem.py._tab_a23 sin tocar la logica (docs/GUI_2.0_plan.md,
paso 5): la mas simple del set (un input multiple obligatorio, dos opcionales,
un mes, una salida) y sin estamentos/A03/selector de perfil/dotacion -- si el
contrato PANTALLA (gui/app.py) no le calzaba a esta pagina, mejor descubrirlo
aca que con cinco paginas ya migradas.

`correr` debe devolver todo lo que `resumen` necesita para el texto de
cierre (mes y ruta de salida incluidos) porque `resumen(resultado)` NO recibe
`ctx` (SS3 del plan: el worker/resumen no tocan Tk vars ni el `ctx` de la
GUI directamente, solo lo que `correr` decide devolver).

`bloque_banner_fuente` + `al_completar` (SS5.1 del plan, agregado tras migrar
A05): `formatos.clasificar_fuente` para A23 corre DENTRO de `cargar_atenciones`,
en el worker -- a diferencia de A05 (deteccion barata al elegir el archivo),
aca no hay banner posible ANTES de apretar Procesar, solo despues. El extra
arma el BannerFuente y lo deja en `pagina.datos`; `al_completar` (hilo GUI,
justo despues del worker) lo actualiza con lo que `procesar()` ya calculo y
dejo en `fer.attrs['avisos']` (misma fuente que alimenta la hoja LEEME)."""

from gui import widgets

instrucciones = (
    "Tabula el REM A23 (Respiratorio) por paciente. Todos los inputs tienen PII -> quedan LOCALES.\n"
    "1.  Atenciones / Diagnósticos / Actividades  ->  indicadores del MES (IRA, neumonía, KTR,\n"
    "     espirometría, controles de sala por profesión, rehab…). Carga el/los archivo(s);\n"
    "     puede venir del AÑO COMPLETO -> se filtra al mes elegido por FECHA ATENCIÓN.\n"
    "2.  Formulario «Otros Crónicos»  ->  SALA bajo control + inasistentes crónicos (Sección G).\n"
    "     Se baja POR AÑO calendario -> SELECCIONA VARIOS a la vez (ctrl-click): como MÍNIMO\n"
    "        el año del reporte Y el ANTERIOR (ideal 5). El inasistente tiene su último control\n"
    "        hace >1 año, así que sin el año previo la Sección G subcuenta (te avisa si falta).\n"
    "3.  Estratificación de Riesgo (opcional)  ->  mejora la detección de asma/EPOC/FQ/SBOR.\n"
    "4.  Inasistentes NSP (opcional)  ->  Sección H: citas Control/Ingreso IRA/ERA no asistidas.\n"
    "     También acepta VARIOS años (ctrl-click); se filtra al mes por FECHA CITA.\n"
    "\n"
    "OJO CON RAYEN ADMINISTRATIVO: desde ahí SOLO obtienes el formulario Otros Crónicos y un\n"
    "   «monitoreo de actividades» mensual — con MUCHO menos info que el export IRIS (y horrible de\n"
    "   parsear). Para los indicadores del mes conviene el export completo de atenciones (IRIS / BD PowerBI).\n"
    "Los cálculos van hacia atrás desde el ÚLTIMO DÍA del mes reportado (no desde hoy)."
)


def correr(ctx, log):
    import modulos.rem_a23_respiratorio as a23
    y, m = ctx["mes"]
    estrat = ctx["estratificacion"][0] if ctx["estratificacion"] else None
    nsp = ctx["nsp"] or None   # Sección H acepta VARIOS años -> la lista entera, no solo el primero
    fer = a23.procesar(ctx["atenciones"], otros=ctx["otros_cronicos"], estrat=estrat,
                       inasistentes=nsp, mes=(y, m), log=log)
    salida = ctx["carpeta"] / f"REM_A23_{y}_{m:02d}_procesado.xlsx"
    a23.escribir(fer, salida)
    return {"fer": fer, "salida": salida, "mes": (y, m)}


def resumen(res):
    fer, salida, (y, m) = res["fer"], res["salida"], res["mes"]
    g = fer.attrs.get("seccion_g", {})
    gtxt = " · ".join(f"{lbl.split()[0]}:{d['Total']}" for lbl, d in g.items() if d["Total"])
    return (f"Listo. REM A23 {y}-{m:02d}.\n{len(fer)} pacientes en el detalle.\n"
            f"Sección G (inasistentes crónicos): {gtxt or 'ninguno'}\n\nGuardado en:\n{salida}")


def bloque_banner_fuente(frame, pagina):
    """Arranca oculto: no hay nada que mostrar hasta que `al_completar` corra
    despues de la primera corrida exitosa."""
    banner = widgets.BannerFuente(frame)
    pagina.datos["banner_fuente"] = banner
    return None


def al_completar(res, pagina):
    banner = pagina.datos.get("banner_fuente")
    if banner is None:   # no deberia pasar (el extra siempre lo arma primero), pero no reventar
        return
    estado_mensaje = widgets.estado_fuente_de_avisos(res["fer"].attrs.get("avisos"))
    if estado_mensaje is None:
        banner.mostrar("plena", "Fuente: A/D/A de IRIS completo.")
    else:
        banner.mostrar(*estado_mensaje)


PANTALLA = {
    "id": "a23_respiratorio",
    "programa": "Respiratorio",
    "titulo": "A23 · Respiratorio",
    "estado": "estable",
    "instrucciones": instrucciones,
    "inputs": [
        {"key": "atenciones", "etiqueta": "Atenciones (mes o año):", "multi": True,
         "obligatorio": True,
         "titulo_dialogo": "Atenciones / Diagnósticos / Actividades (se filtra al mes elegido por FECHA ATENCIÓN)"},
        {"key": "otros_cronicos", "etiqueta": "Otros Crónicos (2+ años):", "multi": True,
         "obligatorio": True,
         "titulo_dialogo": "Formulario Otros Crónicos — selecciona VARIOS años (año del reporte + anterior, ideal 5)"},
        {"key": "estratificacion", "etiqueta": "Estratificación (opcional):", "multi": True,
         "obligatorio": False, "titulo_dialogo": "Estratificación de Riesgo — opcional"},
        {"key": "nsp", "etiqueta": "Inasistentes NSP (opc):", "multi": True, "obligatorio": False,
         "titulo_dialogo": "Reporte de pacientes inasistentes (NSP) — Sección H "
                           "(puedes cargar VARIOS años; se filtra al mes por FECHA CITA)"},
    ],
    "mes": True,
    "carpeta_salida": True,
    "extras": [
        {"despues_de": "atenciones", "construir": bloque_banner_fuente},
    ],
    "correr": correr,
    "resumen": resumen,
    "al_completar": al_completar,
}
