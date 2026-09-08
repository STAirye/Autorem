#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Sonnet 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.8.4
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. Distributed WITHOUT ANY WARRANTY. See the GNU
# General Public License for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
REM Salud Mental — Rescate de inasistentes (auditoría, no tributa al REM).

Segundo consumidor de la tabla «Ferrada» (`programas.poblacion`), en el mismo
patrón que `rem_sm_trabajo_perdido` respecto de `rem_sm_actividades`: reporte
OPERATIVO, no casilla del REM. Ver `docs/SP_P6_poblacion_plan.md` §8.

Cinco hojas, todas SECTORIZADAS (columna `Sector`) y SIN datos de contacto
(§8.4 del plan — solo RUN, nunca nombre/dirección/teléfono/mail):

  - `Rescate_6m` / `Rescate_13m` — dejó de asistir hace 6 / 13 meses (§8.1: las
    dos usan la MISMA lista de 7 actividades validada de `poblacion.ACTIVIDADES_SM_7`,
    no el `contains "salud mental"` laxo del DAX original).
  - `Fallecidos_mes` — para NO llamarlos, y para el egreso del A05 (fase 4).
  - `Posibles_Traslados` — de las cohortes de rescate, quienes se pasivaron por
    traslado/cambio de domicilio: NO se excluyen (§8.5), se flagean para
    confirmar en vez de perseguir un abandono.
  - `Brecha_Medico` (§8.6) — corre `programas.poblacion.construir_poblacion()`
    dos veces (con/sin el filtro INSTRUMENTO contiene MEDIC) y reporta a quién le
    falta control médico del diagnóstico (lo tiene solo por otro estamento).
    GUARDARRAÍL: esa segunda pasada (`exigir_medico=False`) es EXCLUSIVA de
    esta hoja — `rem_sp_p6_poblacion.construir_p6()` la rechaza si se le pasa
    por error.

Filtro duro (§8.3): CUALQUIER paciente con `Motivo Pasivación = Fallecido`
(cualquier fecha, no solo el mes reportado) sale de Rescate_6m/13m — llamar a
la familia de alguien fallecido es exactamente lo que este reporte existe para
evitar. `Fallecidos_mes` es la cohorte DEL MES (para el A05); el filtro del
rescate mira el histórico completo.
"""

from pathlib import Path

import pandas as pd

from programas.rem_utils import norm, contiene_alguno, fecha_col, _rango_mes, ArchivoInvalido
from programas.poblacion import (
    cargar_inscritos, cargar_formulario_sm, construir_poblacion,
    ACTIVIDADES_SM_7, TABLA_DX, TODAS_LAS_SPECS, _estado_dx,
)
from programas.rem_utils import cargar_atenciones

_COLS_DX = [s["col"] for s in TODAS_LAS_SPECS]

# §8.5: heurístico sobre 'Motivo Pasivación' — a refinar contra los valores REALES
# del export (mismo espíritu que EXCLUIR_SMISH en rem_sm_trabajo_perdido: mejor
# ruido visible en el reporte que un descarte silencioso).
_TRASLADO_KW = ["TRASLADO", "CAMBIO DE DOMICILIO", "CAMBIO DOMICILIO"]
# §5.5.1/§8.3: si más de esto de la cohorte de rescate resulta fallecida, avisa
# fuerte (no es un error automático, pero es una señal de que algo puede estar mal).
_TECHO_FALLECIDOS_RESCATE = 0.02


def _dx_activos_txt(row):
    return "; ".join(c.replace(" (form)", "") for c in _COLS_DX if row.get(c) == "Activo")


def _ultima_atencion_sm(d_ada, corte):
    """Fecha real (no el formulario SM) de la última ATENCIÓN de alguna de las 7
    actividades SM validadas (§8.1), por RUN — lo que hace accionable la lista."""
    w = d_ada[(d_ada["FECHA"] <= corte) & contiene_alguno(d_ada["ACT_n"], ACTIVIDADES_SM_7)]
    return w.groupby("RUN")["FECHA"].max()


def _tabla(sub, ultima=None, extra=(), orden_extra=None):
    """Arma una hoja de rescate: RUN/Sector/Edad/Sexo/Diagnósticos activos +
    columnas `extra` [(nombre_salida, columna_origen)], ordenada por Sector y
    luego por `ultima` (si se da) o `orden_extra`."""
    cols = ["RUN", "Sector", "Edad", "Sexo", "Diagnósticos activos"]
    if ultima is not None:
        cols.append("Fecha última atención SM")
    cols += [nombre for nombre, _ in extra]
    if not len(sub):
        return pd.DataFrame(columns=cols)

    d = {"RUN": sub["Número"].values, "Sector": sub["Sector"].values,
        "Edad": sub["Edad"].values, "Sexo": sub["Sexo"].values,
        "Diagnósticos activos": sub.apply(_dx_activos_txt, axis=1).values}
    if ultima is not None:
        d["Fecha última atención SM"] = sub["Número"].map(ultima).values
    for nombre, col in extra:
        d[nombre] = sub[col].values

    orden = ["Sector"]
    if ultima is not None:
        orden.append("Fecha última atención SM")
    elif orden_extra:
        orden.append(orden_extra)
    return pd.DataFrame(d)[cols].sort_values(orden, na_position="last").reset_index(drop=True)


def construir_rescate(P, d_ada, mes=None, log=print):
    """Cohortes de rescate (§8): Rescate_6m, Rescate_13m, Fallecidos_mes,
    Posibles_Traslados. `P` = `programas.poblacion.construir_poblacion()` (la
    corrida NORMAL, `exigir_medico=True`). `d_ada` = ADA ya cargado (para la
    fecha real de última atención, que `P` no trae). Devuelve {hoja: DataFrame}."""
    mes_ini, mes_fin = _rango_mes(mes)
    corte = mes_fin
    ultima = _ultima_atencion_sm(d_ada, corte)

    es_fallecido_hist = P["Motivo Pasivación"].map(norm).str.contains("FALLECI", na=False)
    n_fall_padron = int(es_fallecido_hist.sum())
    if n_fall_padron:
        log(f"[rescate] {n_fall_padron} persona(s) con Motivo Pasivación=Fallecido en el "
            "padrón completo -> excluidas de TODAS las listas de rescate (filtro duro, §8.3).")

    pool6 = P[P["¿Última atención hace 6m?"] == "Si"]
    pool13 = P[P["¿Última atención hace 13m?"] == "Si"]
    n_pool = len(pool6) + len(pool13)
    n_excl = int(es_fallecido_hist.loc[pool6.index].sum()) + int(es_fallecido_hist.loc[pool13.index].sum())
    if n_pool and n_excl / n_pool > _TECHO_FALLECIDOS_RESCATE:
        log(f"[rescate] AVISO: {n_excl} de {n_pool} ({n_excl / n_pool:.0%}) de la cohorte de "
            f"rescate son fallecidos -> por encima del {_TECHO_FALLECIDOS_RESCATE:.0%} esperado "
            "(§5.5.1/§8.3). Revisa que 'Motivo Pasivación' venga bien en el Informe Inscritos.")

    rescate6 = pool6.loc[~es_fallecido_hist.loc[pool6.index]]
    rescate13 = pool13.loc[~es_fallecido_hist.loc[pool13.index]]

    patron_traslado = "|".join(norm(k) for k in _TRASLADO_KW)
    es_traslado6 = rescate6["Motivo Pasivación"].map(norm).str.contains(patron_traslado, regex=True, na=False)
    es_traslado13 = rescate13["Motivo Pasivación"].map(norm).str.contains(patron_traslado, regex=True, na=False)
    # .attrs.clear(): pandas intenta comparar .attrs al concatenar (contiene un
    # DataFrame -> "truth value ambiguous"), mismo fix que rem_sp_p6_poblacion._base_valida.
    t6, t13 = rescate6[es_traslado6].copy(), rescate13[es_traslado13].copy()
    t6.attrs.clear(); t13.attrs.clear()
    traslados = pd.concat([t6, t13]).drop_duplicates(subset="Número")

    cumple_sm = P["¿Pertenece? (28 real)"] == "SI"
    ya_no_activo_ingresado = ~((P["Estado"].map(norm) == "ACTIVO") & (P["¿Ingresado?"] == "SI"))
    fpasiv = fecha_col(P["Fecha Pasivación"], log, "Fecha Pasivación")
    fallecido_mes = es_fallecido_hist & fpasiv.between(mes_ini, mes_fin)
    fallecidos = P[cumple_sm & ya_no_activo_ingresado & fallecido_mes]

    log(f"[rescate] mes {mes_ini:%Y-%m}: Rescate_6m={len(rescate6)} · Rescate_13m={len(rescate13)} "
        f"· Fallecidos_mes={len(fallecidos)} · Posibles_Traslados={len(traslados)}")

    return {
        "Rescate_6m": _tabla(rescate6, ultima),
        "Rescate_13m": _tabla(rescate13, ultima),
        "Fallecidos_mes": _tabla(fallecidos, extra=[("Fecha Pasivación", "Fecha Pasivación")],
                                 orden_extra="Fecha Pasivación"),
        "Posibles_Traslados": _tabla(traslados, ultima,
                                     extra=[("Motivo Pasivación", "Motivo Pasivación"),
                                           ("Fecha Pasivación", "Fecha Pasivación")]),
    }


def calcular_brecha_medico(insc, form, d_ada, P_med, mes=None, log=print):
    """§8.6: corre `construir_poblacion` una SEGUNDA vez con `exigir_medico=False` y
    compara contra `P_med` (la pasada normal) para encontrar a quién le falta
    control médico del diagnóstico (lo tiene solo por otro estamento). El toggle
    NUNCA sale de esta función — nunca alimenta un P6."""
    def _base(P):
        return (P["Estado"].map(norm) == "ACTIVO") & (P["¿Activo 12m?"] == "SI") & (P["¿Ingresado?"] == "SI")

    P_todos = construir_poblacion(insc, form, d_ada, mes=mes, log=lambda *a, **k: None, exigir_medico=False)
    runs_med = set(P_med.loc[_base(P_med), "Número"])
    runs_todos = set(P_todos.loc[_base(P_todos), "Número"])
    brecha_runs = runs_todos - runs_med
    log(f"[rescate] Brecha_Medico: {len(brecha_runs)} persona(s) quedan Ingresado=SI SOLO sin "
        "el filtro de estamento médico (§8.6) -> al debe de control médico del diagnóstico.")

    cols = ["RUN", "Sector", "Edad", "Sexo", "Estamento que lo registró",
           "Fecha último formulario", "Dx que entran solo por no-médico"]
    if not brecha_runs:
        return pd.DataFrame(columns=cols)

    mes_ini, mes_fin = _rango_mes(mes)
    corte = mes_fin
    detalle = {}
    for spec in TABLA_DX:
        if not spec["instrumento"]:
            continue   # ya no filtra por estamento (D2/D3): no puede causar brecha
        est_med = _estado_dx(form, spec["dx"], spec["estado"], corte, mes_ini, mes_fin, instrumento=True)
        est_todos = _estado_dx(form, spec["dx"], spec["estado"], corte, mes_ini, mes_fin, instrumento=False)
        activo_med = set(est_med.index[est_med["estado"] == "Activo"])
        dx_label = spec["col"].replace(" (form)", "")
        for run in brecha_runs:
            if run in est_todos.index and est_todos.loc[run, "estado"] == "Activo" and run not in activo_med:
                d = detalle.setdefault(run, {"dx": [], "fecha": pd.NaT, "instr": ""})
                d["dx"].append(dx_label)
                f = est_todos.loc[run, "fecha"]
                if pd.notna(f) and (pd.isna(d["fecha"]) or f > d["fecha"]):
                    d["fecha"], d["instr"] = f, est_todos.loc[run, "instr"]

    sin_detalle = brecha_runs - set(detalle)
    if sin_detalle:   # fail loud: las dos pasadas deberían explicar el 100% de la brecha
        log(f"[rescate] AVISO: {len(sin_detalle)} de Brecha_Medico sin ningún diagnóstico "
            "identificado como 'solo por no-médico' (inconsistencia entre las dos pasadas; "
            "revisar) -> RUN: " + ", ".join(sorted(sin_detalle)[:10]))

    Pref = P_med.set_index("Número")
    filas = []
    for run in sorted(brecha_runs):
        row = Pref.loc[run] if run in Pref.index else None
        d = detalle.get(run, {"dx": [], "fecha": pd.NaT, "instr": ""})
        filas.append({
            "RUN": run,
            "Sector": row["Sector"] if row is not None else "",
            "Edad": row["Edad"] if row is not None else "",
            "Sexo": row["Sexo"] if row is not None else "",
            "Estamento que lo registró": d["instr"],
            "Fecha último formulario": d["fecha"],
            "Dx que entran solo por no-médico": "; ".join(d["dx"]),
        })
    return pd.DataFrame(filas)[cols].sort_values(["Sector", "RUN"]).reset_index(drop=True)


def _nombres(x):
    if isinstance(x, pd.DataFrame):
        return []
    return [Path(str(p)).name for p in (x if isinstance(x, (list, tuple)) else [x])]


def procesar(inscritos, formulario_sm, ada, mes=None, log=print, P=None):
    """Standalone: carga los 3 inputs del SP·P6 (o los reusa si ya vienen
    cargados/construidos — la GUI ya arma `P` para el P6 y se lo pasa acá para
    no reconstruirlo) y arma las 5 hojas de rescate (§8). `P` debe venir de una
    pasada NORMAL (`exigir_medico=True`, el default)."""
    insc = inscritos if isinstance(inscritos, pd.DataFrame) else cargar_inscritos(inscritos, log=log)
    form = formulario_sm if isinstance(formulario_sm, pd.DataFrame) else cargar_formulario_sm(formulario_sm, log=log)
    d_ada = ada if isinstance(ada, pd.DataFrame) else cargar_atenciones(ada, log=log)

    if P is None:
        P = construir_poblacion(insc, form, d_ada, mes=mes, log=log)
    elif P.attrs.get("exigir_medico") is False:
        raise ArchivoInvalido(
            "exigir_medico_apagado",
            "rem_sm_rescate_inasistentes.procesar() recibió un `P` construido con "
            "exigir_medico=False (§8.6) — las cohortes de rescate necesitan la población "
            "NORMAL (con el filtro médico puesto).")

    tablas = construir_rescate(P, d_ada, mes=mes, log=log)
    tablas["Brecha_Medico"] = calcular_brecha_medico(insc, form, d_ada, P, mes=mes, log=log)

    E = pd.DataFrame({"Hoja": list(tablas.keys()), "Filas": [len(t) for t in tablas.values()]})
    E.attrs["tablas"] = tablas
    E.attrs["mes"] = P.attrs.get("mes")
    E.attrs["avisos"] = []
    E.attrs["fuentes"] = _nombres(inscritos) + _nombres(formulario_sm) + _nombres(ada)
    return E


def escribir(E, salida):
    """Escribe el reporte de rescate: Rescate_6m/13m, Fallecidos_mes,
    Posibles_Traslados, Brecha_Medico. No tributa a ninguna casilla del REM."""
    from programas import cobertura
    tablas = E.attrs.get("tablas", {})
    contexto = {"mes": E.attrs.get("mes"), "archivos": E.attrs.get("fuentes")}
    with pd.ExcelWriter(salida) as xw:
        cobertura.escribir_hoja(xw.book, "sm_rescate_inasistentes", contexto,
                                avisos=E.attrs.get("avisos", ()))
        for nombre, df in tablas.items():
            df.to_excel(xw, index=False, sheet_name=nombre[:31])
    return str(salida)


# -- Descriptor (mismo patrón que rem_sm_trabajo_perdido.TAREA) --
TAREA = {
    "id": "sm_rescate_inasistentes",
    "nombre": "SM · Rescate de inasistentes",
    "correr": procesar,
    "escribir": escribir,
}
