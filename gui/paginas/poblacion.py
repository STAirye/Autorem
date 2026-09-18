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
gui/paginas/poblacion.py - SP.P6 A.1 + Rescate de Inasistentes: paso 9 del plan.

Portada de autorem.py._tab_beta sin tocar la logica (docs/GUI_2.0_plan.md SS4,
CLAUDE.md SS12): la pestaña "BETA" desaparece como programa -- BETA es un
ESTADO de una pantalla (badge en el sidebar, `estado: "beta"`), no un programa
de salud, y esta pantalla pasa a vivir en su propio grupo del sidebar
("Salud Mental -- Poblacion", CLAUDE.md SS9 matriz de programas) hasta que la
familia poblacion salga de validacion (modulos/CLAUDE.md SS2.1).

Los 3 inputs + mes + carpeta caben en el contrato ESTANDAR (a diferencia de
A05): "mes" siempre es un CORTE puntual (nunca "archivo completo", a
diferencia del Periodo de A05) y ninguno de los 3 archivos necesita un
widget a medida, asi que van en `inputs` normal en vez de `extras`.

`correr` hace DOS pasadas sobre la misma `P` (construir_poblacion corre una
sola vez): el P6 (que SI se copia al SP) y el Rescate (auditoria de gestion,
NO tributa al REM) -- el rescate va en su propio try/except para que un
fallo ahi (todavia en validacion, en particular Brecha_Medico) no tumbe el
P6 si este ya salio bien, igual que en autorem.py."""

instrucciones = (
    "EN PRUEBAS — Fase 1+2 de SP·P6, todavía SIN validar contra un P6 llenado a\n"
    "mano. Úsala para ir comparando, no para tabular en producción todavía.\n"
    "Arma la tabla intermedia PSM_Poblacion (port del PowerBI 'Ferrada') y la grilla\n"
    "P6·A.1 lista para copiar-pegar al SP_26.xlsm — respeta la máscara de celdas\n"
    "protegidas de la plantilla real, pliega las edades fuera de rango (no las\n"
    "descarta) y deja en P6_Revisar todo lo que requiere decisión humana antes de\n"
    "pegar. También genera, aparte, el reporte de RESCATE DE INASISTENTES (§8: quién\n"
    "dejó de asistir hace 6/13 meses, fallecidos del mes, posibles traslados y brecha\n"
    "de control médico) — no tributa al REM, es para gestión.\n"
    "Ver docs/SP_P6_poblacion_plan.md.\n"
    "1.  Formulario 'Control de Salud Mental' (IRIS)  ->  HISTÓRICO COMPLETO: carga\n"
    "     TODOS los archivos que tengas (uno por año/descarga, ctrl-click).\n"
    "2.  Atenciones/Diagnósticos/Actividades (ADA)  ->  13 meses (Activo 12m,\n"
    "     Gestante, rescate a 13 meses); acepta varios archivos.\n"
    "3.  Informe Inscritos y Adscritos (IRIS)  ->  snapshot actual, un archivo.\n"
    "Los cálculos van hacia atrás desde el ÚLTIMO DÍA del mes reportado (no desde hoy)."
)


def correr(ctx, log):
    import programas.poblacion as pob
    import modulos.rem_sp_p6_poblacion as p6
    import modulos.rem_sm_rescate_inasistentes as resc

    from programas.rem_utils import cargar_atenciones, rutas_libres, escribir_atomico
    y, m = ctx["mes"]
    # Se carga UNA vez (Inscritos es enorme) y se pasa el DataFrame al P6 y al rescate;
    # los nombres de archivo viajan aparte para la hoja LEEME del rescate.
    fuentes = [p.name for p in [ctx["inscritos"], *ctx["formularios"], *ctx["ada"]]]
    insc = pob.cargar_inscritos(ctx["inscritos"], log=log)
    form = pob.cargar_formulario_sm(ctx["formularios"], log=log)
    ada = cargar_atenciones(ctx["ada"], log=log)
    P = pob.construir_poblacion(insc, form, ada, mes=(y, m), log=log)
    resultado = p6.construir_p6(P, log=log)
    # Los dos nombres juntos, con el mismo `(n)` si alguno ya existe (rem_utils.rutas_libres).
    salida, salida_rescate = rutas_libres(ctx["carpeta"] / f"REM_SP_P6_{y}_{m:02d}_BETA.xlsx",
                                          ctx["carpeta"] / f"REM_SM_Rescate_{y}_{m:02d}_BETA.xlsx")
    # Temporal + rename (rem_utils.escribir_atomico): un corte no deja un .xlsx roto.
    escribir_atomico(salida, lambda p: p6.escribir(P, resultado, p))

    n_rescate = None
    fallo_rescate = None
    # Rescate de inasistentes (SS8): reutiliza el MISMO P (exigir_medico=True) que
    # el P6, no lo reconstruye. Try propio para que un fallo aca (p.ej. Brecha_Medico,
    # todavia en validacion) no tumbe el P6, que es lo que si se copia al SP.
    try:
        Er = resc.procesar(insc, form, ada, mes=(y, m), log=log, P=P, fuentes=fuentes)
        escribir_atomico(salida_rescate, lambda p: resc.escribir(Er, p))
        n_rescate = {h: len(t) for h, t in Er.attrs["tablas"].items()}
        log(f"OK Rescate de inasistentes -> {salida_rescate.name}")
    except Exception as e:   # noqa: BLE001
        fallo_rescate = str(e)   # el resumen lo dice: no basta con el log
        log(f"[rescate] no se generó el reporte de rescate: {e}")

    return {"P": P, "resultado": resultado, "n_rescate": n_rescate, "salida": salida,
            "mes": (y, m), "fallo_rescate": fallo_rescate}


def resumen(res):
    P, resultado, n_rescate = res["P"], res["resultado"], res["n_rescate"]
    y, m = res["mes"]
    n_ingresados = int((P["¿Ingresado?"] == "SI").sum())
    n_admin = len(resultado["revisar_administrativo"])
    n_clin = len(resultado["revisar_clinico"])
    rtxt = ("\nRescate: " + " · ".join(f"{h}={n}" for h, n in n_rescate.items())
           if n_rescate is not None else "")
    if res.get("fallo_rescate"):
        rtxt = f"\nRescate: NO se generó ({res['fallo_rescate']})."
    # Los avisos de cobertura (ADA/formulario que no llegan al mes) NO bloquean a
    # proposito (programas/poblacion._verificar_cobertura_fechas), y justamente por eso
    # tienen que verse ACA: solo en el log y en la LEEME, el "Listo" de abajo se leia
    # igual que el de una corrida completa, con Activo 12m subcontado para todos.
    avisos = P.attrs.get("avisos") or []
    atxt = "".join(f"\n  - {casilla}: {estado} ({motivo})"
                   for casilla, estado, motivo, _ in avisos)
    atxt = (f"\n\nOJO, {len(avisos)} aviso(s) de cobertura -- estas cifras pueden "
            f"estar SUBCONTADAS:{atxt}" if avisos else "")
    return (f"Listo (BETA, sin validar todavía). SP·P6 {y}-{m:02d}.\n"
            f"{len(P)} personas en el snapshot, {n_ingresados} con ¿Ingresado?=SI.\n"
            f"Revisar_Administrativo: {n_admin} fila(s) · Revisar_Clinico: {n_clin} fila(s) "
            f"— revísalas antes de pegar al SP.{rtxt}{atxt}\n\n"
            f"Guardado en:\n{res['salida']}")


PANTALLA = {
    "id": "sp_p6_poblacion",
    "programa": "Salud Mental — Población",
    "titulo": "Población en control",
    "estado": "beta",
    "instrucciones": instrucciones,
    "inputs": [
        {"key": "formularios", "etiqueta": "1. Formulario SM (histórico):", "multi": True,
         "obligatorio": True,
         "motivo_obligatorio": "Es la base de la tabla por RUN: sin el histórico "
                               "completo, «Ingresado» subcuenta.",
         "titulo_dialogo": "Formulario 'Control de Salud Mental' (IRIS) — carga TODO el histórico disponible"},
        {"key": "ada", "etiqueta": "2. Atenciones/Diag/Activ (ADA):", "multi": True,
         "obligatorio": True,
         "titulo_dialogo": "Atenciones / Diagnósticos / Actividades — 13 meses"},
        {"key": "inscritos", "etiqueta": "3. Inscritos y Adscritos:", "multi": False,
         "obligatorio": True,
         # La salida va junto al INSCRITOS, como en `_tab_beta` (`defecto=entrada.parent`):
         # es el snapshot DEL MES que se esta reportando. Los otros dos son historico
         # multi-anio, que suele vivir archivado aparte -- sin esta marca el P6 y el
         # Rescate del mes se guardaban alla (ver `_resolver_ctx` en gui/app.py).
         "ancla_salida": True,
         "titulo_dialogo": "Elige el 'Informe Inscritos y Adscritos'"},
    ],
    "mes": True,
    "carpeta_salida": True,
    "correr": correr,
    "resumen": resumen,
}
