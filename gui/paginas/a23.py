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
    "RAYEN ADMINISTRATIVO: sirven el formulario Otros Crónicos, el «Monitoreo de Inasistentes» (Sección H)\n"
    "   y el «Monitoreo de Actividades», con MENOS info que IRIS: el Otros Crónicos no trae el estamento\n"
    "   (se saca del nombre del funcionario en el export de atenciones; si no lo encuentra, te avisa), y el\n"
    "   Monitoreo trae los diagnósticos sin código (Ira Alta, Bronquitis y EPOC exacerbado salen en 0).\n"
    "Un archivo OPCIONAL que no sirve no corta la corrida: te pregunta si seguir sin él.\n"
    "Los cálculos van hacia atrás desde el ÚLTIMO DÍA del mes reportado (no desde hoy)."
)


def correr(ctx, log):
    import modulos.rem_a23_respiratorio as a23
    from programas.rem_utils import rutas_libres, escribir_atomico
    from gui.runner import avisos_descartados
    y, m = ctx["mes"]
    estrat = ctx["estratificacion"]   # UN archivo (snapshot), no una lista
    nsp = ctx["nsp"] or None   # Sección H acepta VARIOS años -> la lista entera, no solo el primero
    fer = a23.procesar(ctx["atenciones"], otros=ctx["otros_cronicos"], estrat=estrat,
                       inasistentes=nsp, mes=(y, m), log=log)
    fer.attrs.setdefault("avisos", []).extend(avisos_descartados(ctx))   # opcionales que se omitieron
    salida, = rutas_libres(ctx["carpeta"] / f"REM_A23_{y}_{m:02d}_procesado.xlsx")   # nunca pisa
    escribir_atomico(salida, lambda p: a23.escribir(fer, p))   # temporal + rename
    return {"fer": fer, "salida": salida, "mes": (y, m)}


def resumen(res):
    fer, salida, (y, m) = res["fer"], res["salida"], res["mes"]
    g = fer.attrs.get("seccion_g", {})
    gtxt = " · ".join(f"{lbl.split()[0]}:{d['Total']}" for lbl, d in g.items() if d["Total"])
    return (f"Listo. REM A23 {y}-{m:02d}.\n{len(fer)} pacientes en el detalle.\n"
            f"Sección G (inasistentes crónicos): {gtxt or 'ninguno'}"
            f"{widgets.texto_avisos(fer.attrs.get('avisos'))}\n\nGuardado en:\n{salida}")


def al_completar(res, pagina):
    widgets.pintar_banner_fuente(pagina, res["fer"])


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
         "motivo_obligatorio": "De ahí salen SALA bajo control y la Sección G "
                               "(inasistentes crónicos). Ideal varios años.",
         "titulo_dialogo": "Formulario Otros Crónicos — selecciona VARIOS años (año del reporte + anterior, ideal 5)"},
        # `entrada` = el parametro de a23.procesar: con eso la app sabe que archivo
        # omitir si el modulo dice que este opcional no sirve (runner.sin_opcional).
        # `multi: False` porque la Estratificacion es UN snapshot: declarada multiple
        # (como la heredo de la 1.x) el usuario podia elegir dos con ctrl-click -- la
        # fila decia "2: a.xlsx, b.xlsx" -- y `correr` usaba solo la primera, callado
        # (ronda 12).
        {"key": "estratificacion", "etiqueta": "Estratificación (opcional):", "multi": False,
         "obligatorio": False, "entrada": "estrat", "titulo_dialogo": "Estratificación de Riesgo — opcional"},
        {"key": "nsp", "etiqueta": "Inasistentes NSP (opc):", "multi": True, "obligatorio": False,
         "entrada": "inasistentes",
         "titulo_dialogo": "Reporte de pacientes inasistentes (NSP) — Sección H "
                           "(puedes cargar VARIOS años; se filtra al mes por FECHA CITA)"},
    ],
    "mes": True,
    "carpeta_salida": True,
    "extras": [
        {"despues_de": "atenciones", "construir": widgets.bloque_banner_fuente},
    ],
    "correr": correr,
    "resumen": resumen,
    "al_completar": al_completar,
}
