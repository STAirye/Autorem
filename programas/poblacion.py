#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 2.0.10
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. Distributed WITHOUT ANY WARRANTY. See the GNU
# General Public License for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
poblacion.py — port del DAX de la tabla «Ferrada» del PowerBI (Fase 1, SP·P6 A.1).

Construye, desde 3 exports crudos, la tabla intermedia POR-PACIENTE que hoy se
obtiene abriendo el PowerBI y exportando a mano el visual «Población PSM». Es
INFRAESTRUCTURA TRANSVERSAL (la tabla Ferrada la usan 8 páginas del PowerBI, no
solo Salud Mental) — vive en `programas/`, no en `modulos/`. Ver
`docs/SP_P6_poblacion_plan.md` (plan) y `docs/SP_P6_config_por_dx.md` (config,
tablas A/B/C, decisiones D1-D5).

Alcance SLIM (§3.2 del plan): de las ~150 columnas de Ferrada se portan ~55 —
solo las columnas `(form)` (28 diagnósticos/factores de riesgo), la actividad
(¿Ingresado?/¿Activo 12m?/rescate 6m-13m/¿Embarazada?), demografía básica y los
campos de traza del Inscritos (Estado/Situación/Motivo y Fecha Pasivación/Sector).
Fuera: fármacos, columnas `(fecha)`/`(mixto)`/`(dg)`, y todo dato de CONTACTO
(nombre, dirección, teléfono, mail — §8 CLAUDE.md, no solo economía de columnas).

Los NOMBRES de columna de salida son los del export PowerBI (para poder diffear
celda a celda contra un mes ya conocido). El corte reemplaza a TODAY() (§4.1):
todo se calcula hacia atrás desde el último día del MES REPORTADO, nunca desde
"hoy", para poder recalcular un mes pasado.

Divergencias esperadas contra el PowerBI (documentadas, NO son bugs del port):
  - D1 (fila 56/TGD no especificado): usa la pregunta 91 con fallback a la 63.
  - D2 (factores de riesgo): Violencia y Suicidio NO filtran por instrumento
    médico (el DAX sí filtraba — eso era el bug; el correcto es Abuso Sexual,
    que nunca filtró).
  - D5: si el diagnóstico está Activo pero su subtipo viene vacío, no tributa.
  - §4.3: egreso por DIAGNÓSTICO (el DAX original egresaba TODOS los dx del RUN
    con cualquier egreso del mes). Columna de auditoría + aviso en el log.
  - §4.7: gestante = control prenatal/formulario con matrona en ventana de 3
    meses (vs. los 2 meses off-by-one del DAX).

`construir_poblacion(..., exigir_medico=True)` (§8.6 del plan, para
rem_sm_rescate_inasistentes.Brecha_Medico): con False, los diagnósticos que
normalmente exigen INSTRUMENTO contiene MEDIC dejan de filtrar por estamento. NUNCA
usar False para tabular el P6 — GUARDARRAÍL: rem_sp_p6_poblacion.construir_p6()
rechaza un `P` construido con el toggle apagado.
"""

import weakref
from pathlib import Path

import numpy as np
import pandas as pd

from programas.rem_utils import (
    norm, fecha_col, cargar_atenciones, cargar_canonico, MAPA_INSCRITOS,
    resolver_columnas, contiene_alguno, gestante_runs, PUEBLO_VACIO,
    OPENPYXL_OK, OPENPYXL_ERR, openpyxl, ArchivoInvalido, verificar_hoja_unica,
    buscar_col, num_pregunta, encontrar_fila_encabezado, _rango_mes, TOKEN_MEDICO,
)
from programas import formatos
from programas.rem_saludmental import DIAGNOSTICOS_CON_SUBTIPO, verificar_formulario_sm

# ======================================================================
# Tabla A/B — config por diagnóstico (docs/SP_P6_config_por_dx.md, APROBADA)
# ======================================================================
# El DAX es UNIFORME: TODAS las 28 fórmulas (form) siguen el mismo patrón
# (§4.2 del plan) -> UNA función parametrizada (_estado_dx) + esta tabla de
# datos, no 28 casos especiales. `subtipo` se REUSA de rem_saludmental
# (fuente única con el A05) en vez de repetir los números acá.

def _spec(col, dx, estado, *, instrumento=True, subtipo_col=None,
          subtipo2=None, subtipo2_col=None):
    return dict(col=col, dx=dx, estado=estado, instrumento=instrumento,
                subtipo=DIAGNOSTICOS_CON_SUBTIPO.get(dx), subtipo_col=subtipo_col,
                subtipo2=subtipo2, subtipo2_col=subtipo2_col)


# Diagnósticos (filas 25-58 del P6): TODOS filtran INSTRUMENTO contiene MEDIC (D3).
TABLA_DX = [
    _spec("Depresión (form)", 18, 19, subtipo_col="Depresión gravedad (form)"),
    _spec("Depresión Postparto (form)", 21, 22),
    _spec("Bipolaridad (form)", 23, 24),
    _spec("OH Perjudicial (form)", 31, 32),
    _spec("OH Dependiente (form)", 33, 34),
    _spec("Drogas Perjudicial (form)", 35, 36),
    _spec("Drogas Dependiente (form)", 37, 38),
    _spec("OH y Drogas (form)", 39, 40),
    _spec("TDAH (form)", 57, 58),
    _spec("Oposicionista desafiante (form)", 69, 70),
    _spec("Ansiedad separación (form)", 71, 72),
    _spec("Otras Infancia/Adolescencia (form)", 73, 74),
    _spec("Ansiedad (form)", 41, 42, subtipo_col="Ansiedad (tipo)"),
    _spec("Demencia (form)", 44, 46, subtipo_col="Demencia gravedad (form)"),
    _spec("Esquizofrenia (form)", 51, 52),
    _spec("Adaptativo (form)", 49, 50),
    _spec("Conducta Alimentaria (form)", 55, 56),
    _spec("Retraso Mental (form)", 59, 60),
    _spec("Personalidad (form)", 61, 62),
    _spec("Autismo (form)", 83, 84),
    _spec("Asperger (form)", 85, 86),
    _spec("Rett (form)", 87, 88),
    _spec("Desintegrativo niñez (form)", 89, 90),
    _spec("TGD (form)", 91, 92),   # D1: fallback a la 63/64, ver _aplicar_fallback_tgd
    _spec("Otros (form)", 65, 66),
]

# Factores de riesgo (filas 15-23): NINGUNO filtra por instrumento (D2) —
# contraintuitivo: un factor de riesgo lo puede registrar cualquier
# estamento, no solo médico. Abuso Sexual ya estaba bien en el DAX (única
# excepción correcta); Violencia y Suicidio SÍ filtraban y eso era el bug.
TABLA_FR = [
    _spec("Violencia (form)", 4, 5, instrumento=False,
          subtipo_col="Violencia Tipo (form)",
          subtipo2=7, subtipo2_col="Violencia Victima o Agresor (form)"),
    _spec("Abuso Sexual (form)", 9, 10, instrumento=False),
    _spec("Suicidio (form)", 11, 13, instrumento=False, subtipo_col="Suicidio Tipo (form)"),
]

TODAS_LAS_SPECS = TABLA_FR + TABLA_DX

# Las 28 columnas de diagnóstico/factor, en el orden de las specs. UNA sola lista,
# porque la leen dos consumidores que TIENEN que estar de acuerdo: `_col_dx()` (el
# orden de columnas de la planilla) y `_ingresado()` / `¿Pertenece?` (los números).
# Con dos derivaciones, filtrar una spec en un lado dejaba una columna llena en la
# hoja y un `¿Ingresado?`=NO al lado, callado.
_COLS_DX = [s["col"] for s in TODAS_LAS_SPECS]

# El DAX de 'Pertenece a PSM' lista 24 columnas, pero el de 'Ingresado' usa 28:
# faltan las 4 de OH/drogas granulares (Pertenece solo tiene el agregado "OH y
# Drogas"). Como el reporte 'Poblacion SM' del PowerBI trae Pertenece de PREFILTRO
# de pagina, quien queda Ingresado SOLO por una de esas 4 cae FUERA del export del
# PowerBI pero DENTRO de autoREM -> el supuesto "Ingresado => Pertenece" NO se
# cumple. Se emiten las dos versiones para poder comparar de dónde sale la brecha.
#
# Base FORMULARIO: el DAX mezcla columnas con y sin (form) y las sin-(form) miran
# ademas los CIE-10 del ADA historico; replicar eso seria lentisimo y el objetivo
# aca es COMPARAR, no reproducir el numero exacto. Cuenta Activo Y Egresado
# (el DAX usa <> "NO"), que es lo que se necesita en el reporte.
_PERTENECE_FALTANTES_EN_DAX = ["OH Perjudicial (form)", "OH Dependiente (form)",
                               "Drogas Perjudicial (form)", "Drogas Dependiente (form)"]

# D1 — TGD no especificado: la 91 no tiene columna en el PowerBI (nunca se
# llenó); se recupera vía la pregunta "padre" 63, pero SOLO si ninguna de las
# TGD específicas (83/85/87/89/91) está activa (evita doble conteo).
_TGD_ESPECIFICAS = ["Autismo (form)", "Asperger (form)", "Rett (form)",
                    "Desintegrativo niñez (form)"]
_Q_TGD_FALLBACK, _E_TGD_FALLBACK = 63, 64
# La UNICA columna que `_aplicar_fallback_tgd` sobreescribe, o sea la unica cuyo valor
# en la tabla final NO es el resultado de su propia spec. Quien compare la tabla contra
# una pasada de `_estado_dx` tiene que saltearla (ver Brecha_Medico).
COL_TGD_FALLBACK = "TGD (form)"

# Preguntas que se leen del formulario histórico (unión de todo lo de arriba
# + la 1, "madre de hijo <5", que NO tiene subtipo/estado propio).
QUESTIONS = sorted({1, _Q_TGD_FALLBACK, _E_TGD_FALLBACK} | {
    n for spec in TODAS_LAS_SPECS
    for n in (spec["dx"], spec["estado"], spec["subtipo"], spec["subtipo2"]) if n
})
ESTADOS_TODOS = sorted({spec["estado"] for spec in TODAS_LAS_SPECS} | {_E_TGD_FALLBACK})

# Las 7 actividades SM validadas (rem_sm_actividades.ADA_TRIBUTAN habla de
# CASILLAS del REM; esta lista es la del DAX "SM Activo 12m", ver §8.1 del
# plan: rescate 6m/13m usan la MISMA lista, no el 'contains "salud mental"'
# laxo del DAX original). Fuente única para Activo12m / rescate 6m / rescate 13m.
#
# Ronda 11 (sep-2026): 3 de las 7 venian del DAX con nombres que NO EXISTEN en el
# Maestro de Actividades (catalogos/maestro_slim.csv.gz) -> no calzaban con nada, y
# quien solo tenia esas visitas salia NO Activo 12m (y al rescate como inasistente).
# Mismo bug que el A32-F2. Se cambiaron por los nombres reales del Maestro; un test
# (tests/test_refs_tablas.py) exige que cada una calce con alguna actividad del Maestro.
ACTIVIDADES_SM_7 = [
    "control salud mental",
    "controles salud mental",
    "consulta de salud mental",
    # DAX: "...con integrante con PATOLOGIA de salud mental". El Maestro dice PROBLEMA.
    "visita domiciliaria integral familia con integrante con problema de salud mental",
    # DAX: "visita domiciliaria integral a familia con adulto mayor con demencia". En el
    # Maestro calza con las actividades de gestion (AG_VIDOPCDS / AG_VISITA DOMICILIARA
    # INTEGRALES ... ADULTO MAYOR CON DEMENCIA) y la VDI A26 de hoy es la del PADDS.
    "adulto mayor con demencia",
    # La VDI del PADDS con demencia SI cuenta para 'Activo 12m' (decision del autor,
    # sep-2026): es contacto del programa con la persona. Que el Trabajo Perdido la saque
    # del universo SM (EXCLUIR_SMISH) es otra cosa: dice a que REM TRIBUTA (al del PADDS,
    # A26·A1), no si la persona esta activa.
    "dependencia severa con diagnostico de demencia",
    "visita domiciliaria integral a familia con niños/as de 5 a 9 años con problemas y/o trastorno",
    # DAX: "visita integral de salud mental a domicilio". El Maestro: "OTRAS VISITAS
    # INTEGRALES - VISITA INTEGRAL DE SALUD MENTAL - A DOMICILIO (NIVEL SECUNDARIO)".
    "visita integral de salud mental - a domicilio",
]

# -- Columnas de salida (nombres = export PowerBI; §3.2 slim) --
COL_IDENTIDAD = ["Número", "Tipo de identificación", "Sexo", "Género", "Edad", "Sector",
                 "Situación", "Estado", "Motivo Pasivación", "Fecha Pasivación",
                 "¿Originario o Migrante?", "Pueblo Originario", "PROTECCION NIÑEZ"]
COL_ACTIVIDAD = ["¿Ingresado?", "¿Pertenece? (24 DAX)", "¿Pertenece? (28 real)",
                 "¿Activo 12m?", "¿Última atención hace 6m?",
                 "¿Última atención hace 13m?", "¿Embarazada?", "Madre <5 años"]


def _col_dx():
    cols = list(_COLS_DX)
    for s in TODAS_LAS_SPECS:
        if s["subtipo_col"]:
            cols.append(s["subtipo_col"])
        if s["subtipo2_col"]:
            cols.append(s["subtipo2_col"])
    return cols


COLUMNAS_SALIDA = COL_IDENTIDAD + COL_ACTIVIDAD + _col_dx()


# ======================================================================
# Input 1 — Informe Inscritos y Adscritos (snapshot, IRIS)
# ======================================================================
# `MAPA_INSCRITOS` vive en rem_utils desde la ronda 12: el mismo export lo lee
# `rem_utils.trans_map` (flag TRANS del SM), que resolvía las mismas columnas por su
# cuenta -- dos mapas para una planilla es una guarda que hay que escribir dos veces.


def cargar_inscritos(entrada, log=print):
    """'Informe Inscritos y Adscritos' (IRIS, snapshot) -> DataFrame, 1 fila por
    RUN. Es la base de la tabla Ferrada: TODA la población, sin filtrar (el filtro
    Activo/Ingresado lo aplica quien consuma la tabla)."""
    d, col = cargar_canonico(entrada, lambda h: resolver_columnas(h, MAPA_INSCRITOS),
                             requeridas=("RUN", "SEXO", "ESTADO", "SITUACION"),
                             no_vacias=("RUN",))
    n_filas = len(d)
    d["RUN"] = d["RUN"].astype(str).str.strip()
    # Las DOS mitades hacen falta, una por cada pandas mayor -- no es redundancia:
    #   pandas 2: `astype(str)` vuelve el faltante el TEXTO "nan" (o "None"), que no es
    #             nulo para `isna()` y solo lo caza el `isin`.
    #   pandas 3: `astype(str)` PRESERVA el faltante, asi que el `isin` no ve nada y solo
    #             lo caza el `isna()`.
    # Con solo el `isin` (como estaba hasta la 2.0.8) bajo pandas 3 la fila sin RUN
    # sobrevivia: el snapshot Ferrada quedaba con una persona fantasma de `Numero` NaN.
    # No rompia el P6 -- `_base_valida` la descarta con `rut_valido` --, pero ensuciaba la
    # hoja PSM_Poblacion, que es la que se archiva para auditar, e inflaba el conteo del
    # log. Mismo patron que `rem_utils.fecha_col`, que ya lo hacia bien.
    sin_run = d["RUN"].isna() | d["RUN"].isin(("", "None", "nan"))
    n_sin_run = int(sin_run.sum())
    d = d[~sin_run]

    # «RUN Responsable» (§5.5.2 del plan sp-p6): un recién nacido de <1 mes sin RUT
    # propio se inscribe con el RUN de un tercero (típicamente la madre) -> ESE RUN
    # queda repetido en el Inscritos, una fila por la madre y otra por el RN. Es una
    # COLISIÓN de clave, no una fila más: si no se saca ANTES de deduplicar, el
    # `drop_duplicates` de abajo puede quedarse con la fila del RN y perder la de la
    # madre (el caso de riesgo real: madre con Depresión Postparto activa).
    n_resp = 0
    if "TIPOID" in d.columns:
        es_responsable = d["TIPOID"].map(norm) == "RUN RESPONSABLE"
        n_resp = int(es_responsable.sum())
        if n_resp:
            log(f"[poblacion] {n_resp} fila(s) 'RUN Responsable' descartadas antes de "
                "deduplicar (recién nacido <1 mes con el RUN de un tercero; no se "
                "pierde a la persona real, solo la fila colisionada).")
        d = d[~es_responsable]

    d = d.drop_duplicates(subset="RUN", keep="last").reset_index(drop=True)
    if len(d) == 0:
        # Fail loud sobre la FUENTE (CLAUDE.md regla 2), no sobre una casilla mas
        # abajo: con 0 filas, las columnas de mas adelante (ALERTAS, etc.) quedan
        # con dtype float64 en vez de object y revientan con un AttributeError
        # criptico en .str.contains(). El export SOLO-encabezado lo corta cargar_canonico
        # (ronda 1) y el que trae el RUN vacio en TODAS las filas tambien, por archivo
        # (`no_vacias`, ronda 12); aca queda el caso propio de este loader: filas con RUN
        # pero todas 'RUN Responsable' (o una mezcla que no deja a nadie).
        raise ArchivoInvalido(
            "sin_datos",
            f"El 'Informe Inscritos y Adscritos' trae {n_filas} fila(s), pero ninguna con "
            f"un RUN usable: {n_sin_run} sin RUN en 'NUMERO TIPO IDENTIFICACION' y "
            f"{n_resp} 'RUN Responsable' (recién nacidos con el RUN de un tercero).\n\n"
            "Revisa que sea el export completo del centro, sin modificar.")
    # Columnas opcionales que NO vinieron (quedan en None para todos). Las usa quien
    # depende de ellas para decir que no puede, en vez de dar un resultado vacio
    # callado: p.ej. el rescate sin MOTIVO/FECHA PASIVACION no flagea fallecidos.
    d.attrs["columnas_ausentes"] = [k for k, c in col.items() if not c]
    log(f"[poblacion] Inscritos: {len(d)} personas (snapshot)")
    return d


# ======================================================================
# Input 2 — Formulario 'Control de Salud Mental' histórico (IRIS, multi-archivo)
# ======================================================================
def _leer_formulario_1(entrada, log):
    """Un archivo del histórico -> DataFrame (RUN, FECHA cruda, INSTR, q<N> por
    cada pregunta de QUESTIONS). Reusa la detección de encabezado/identidad de
    `formatos`/`rem_saludmental` (perfil IRIS): mismo export que el A05."""
    if not OPENPYXL_OK:
        raise ImportError(f"Falta 'openpyxl' (pip install openpyxl). Detalle: {OPENPYXL_ERR}")
    nombre = Path(str(entrada)).name
    verificar_hoja_unica(entrada)
    # NO read_only: detectar_eje/encontrar_fila_encabezado usan ws[r] / ws.cell(),
    # que el modo read-only de openpyxl no soporta (mismo patrón que
    # rem_saludmental.abrir_validado). El costo de memoria es aceptable: es el
    # mismo tipo de archivo que ya procesa el A05, un mes/año a la vez.
    wb = openpyxl.load_workbook(entrada, data_only=True)
    ws = wb.active
    if formatos.detectar_eje(ws) != "iris":
        wb.close()
        raise ArchivoInvalido(
            "no_iris",
            f"Archivo «{nombre}»:\n\nEl histórico de 'Control de Salud Mental' debe "
            "venir en formato IRIS (no el Reporte Administrativo): trae columnas que "
            "el Administrativo no tiene y que este módulo necesita.")
    header_idx = encontrar_fila_encabezado(ws, formatos.ANCLA_IRIS, formatos.MAX_FILAS_HEADER)
    filas = list(ws.iter_rows(values_only=True))
    wb.close()
    headers = list(filas[header_idx - 1])
    headers_n = [norm(h) for h in headers]
    verificar_formulario_sm(headers, nombre)   # por CONTENIDO (regla 5), mismo que el A05
    rut_col, _edad_col, _sexo_col = formatos.resolver_identidad(headers_n)
    fecha_col_i = buscar_col(headers_n, tokens=["FECHA", "FORMULARIO"])
    instr_col_i = buscar_col(headers_n, exacto="INSTRUMENTO")
    # INSTRUMENTO es requerido (gemelo del A23, ronda 9): sin el, `INSTR_n` queda "" y
    # TODOS los diagnosticos que exigen medico salen no-Activos -> el P6 subcuenta
    # callado (los factores de riesgo, que no lo exigen, mantienen la base viva).
    faltan_id = [n for n, c in (("RUT", rut_col), ("FECHA FORMULARIO", fecha_col_i),
                                ("INSTRUMENTO", instr_col_i)) if not c]
    if faltan_id:
        raise ArchivoInvalido(
            "sin_columnas",
            f"Archivo «{nombre}»:\n\nNo encuentro la(s) columna(s) {', '.join(faltan_id)}. "
            "¿Es el export IRIS de 'Control de Salud Mental', sin modificar?")
    num2col = {num_pregunta(h): i for i, h in enumerate(headers) if num_pregunta(h) is not None}
    # Las preguntas se ubican por su NUMERO ("18.- ..."). Una que falta quedaba como
    # columna en None, callada: sin NINGUNA (RAYEN renombro los encabezados) el P6
    # salia con 0 ingresados y avisos=[]. Todas -> fail loud; algunas -> se devuelven
    # para el aviso (un historico de años viejos puede no tener las preguntas nuevas).
    faltan = [n for n in QUESTIONS if n not in num2col]
    if len(faltan) == len(QUESTIONS):
        raise ArchivoInvalido(
            "sin_columnas",
            f"Archivo «{nombre}»:\n\nNo encuentro NINGUNA de las preguntas del "
            "formulario (encabezados «18.- ¿TIENE DEPRESIÓN?», «19.- ESTADO», ...), así "
            "que no se puede saber ningún diagnóstico.\n\n"
            "¿Es el export IRIS de 'Control de Salud Mental', sin modificar?")
    if faltan:
        log(f"[poblacion] «{nombre}» no trae {len(faltan)} pregunta(s) que usa la tabla "
            f"({', '.join(map(str, faltan[:12]))}{'...' if len(faltan) > 12 else ''}): "
            "esos diagnósticos salen de los OTROS archivos, o en 0.")

    out = {"RUN": [], "FECHA": [], "INSTR": []}
    for n in QUESTIONS:
        out[f"q{n}"] = []
    for row in filas[header_idx:]:
        rut = row[rut_col - 1] if rut_col - 1 < len(row) else None
        if not str(rut or "").strip():
            continue
        out["RUN"].append(str(rut).strip())
        out["FECHA"].append(row[fecha_col_i - 1] if fecha_col_i - 1 < len(row) else None)
        out["INSTR"].append(row[instr_col_i - 1] if instr_col_i - 1 < len(row) else "")
        for n in QUESTIONS:
            c = num2col.get(n)
            out[f"q{n}"].append(row[c] if c is not None and c < len(row) else None)
    if not out["RUN"]:
        # Fail loud POR ARCHIVO (CLAUDE.md regla 2), igual que cargar_canonico: en un
        # historico de varios años, un año que bajo cortado (solo encabezado) se perdia
        # callado en el concat -- los RUN cuyo unico formulario valido era de ese año
        # quedaban sin diagnostico, y la cobertura por fecha min/max no lo ve.
        raise ArchivoInvalido(
            "sin_datos",
            f"Archivo «{nombre}»:\n\nNo trae ninguna fila de datos con RUT "
            f"({len(filas) - header_idx} fila(s) bajo el encabezado).\n\n"
            "Revisa que sea el export completo de IRIS (no solo el encabezado) y que "
            "este sin modificar.")
    d = pd.DataFrame(out)
    d.attrs["preguntas_faltantes"] = {nombre: faltan} if faltan else {}
    return d


def cargar_formulario_sm(entrada, log=print):
    """Histórico COMPLETO del formulario 'Control de Salud Mental' (IRIS) -> uno
    o varios archivos (acepta LISTA, como el ADA del A23). Devuelve DataFrame
    largo: 1 fila por formulario aplicado, con q<N>/q<N>_n por cada pregunta que
    consume la config de arriba."""
    archivos = entrada if isinstance(entrada, (list, tuple)) else [entrada]
    partes = []
    for e in archivos:
        try:
            partes.append(_leer_formulario_1(e, log))
        except ArchivoInvalido:
            raise
        except Exception as ex:
            raise ArchivoInvalido(
                "no_legible",
                f"No pude leer «{Path(str(e)).name}»:\n\n{ex}\n\n"
                "¿Es un .xlsx válido del export IRIS, sin modificar?") from ex
    faltantes = {k: v for p in partes for k, v in p.attrs.get("preguntas_faltantes", {}).items()}
    d = pd.concat(partes, ignore_index=True) if len(partes) > 1 else partes[0]
    d.attrs["preguntas_faltantes"] = faltantes   # concat no conserva attrs
    # (0 filas ya no llega aca: _leer_formulario_1 falla POR ARCHIVO, nombrandolo.)
    d["FECHA"] = fecha_col(d["FECHA"], log, "FECHA FORMULARIO (histórico SM)")
    d["INSTR_n"] = d["INSTR"].map(norm)
    for n in QUESTIONS:
        d[f"q{n}_n"] = d[f"q{n}"].map(norm)
    span = (f"{d['FECHA'].min():%Y-%m}..{d['FECHA'].max():%Y-%m}"
            if d["FECHA"].notna().any() else "sin fechas")
    log(f"[poblacion] Formulario SM histórico: {len(d)} formularios, "
        f"{d['RUN'].nunique()} RUN distintos ({span})")
    return d


# ======================================================================
# Motor: último formulario por RUN×diagnóstico (parametrizado, D2/D3/D5/§4.3)
# ======================================================================
def _mes_offset(corte, n_meses):
    """(inicio, fin) del mes calendario que está `n_meses` ANTES del mes de
    `corte` (Timestamp = último día del mes reportado)."""
    import calendar
    y, m = corte.year, corte.month - n_meses
    while m <= 0:
        m += 12
        y -= 1
    return pd.Timestamp(y, m, 1), pd.Timestamp(y, m, calendar.monthrange(y, m)[1])


# Mascaras "la columna <col> contiene <token>" del ultimo `df` que las pidio: el
# INSTRUMENTO medico y los tokens de las columnas ESTADO pasan TODOS por aca. Hubo un
# rato en que el INSTRUMENTO tenia su propia memo, identica salvo por tener la columna y
# el token clavados: dos globales y dos caminos de invalidacion para la misma regla, y
# la primera invariante nueva (el `.copy()` de mas abajo) ya nacio en una y hubo que
# copiarla a mano a la otra. Una sola.
#
# QUE se repetia:
#   - el INSTRUMENTO medico es lo unico de `_estado_dx` que NO depende del dx ni del
#     estado, y se recalculaba en las 28 specs de cada pasada (mas las de
#     Brecha_Medico): 0.138 s de los 0.425 s que cuestan las mascaras, sobre 30k filas.
#   - los tokens de ESTADO no saltan a la vista, porque dentro de una pasada de
#     `construir_poblacion` cada columna ESTADO pertenece a UNA sola spec -- pero
#     `_egreso_powerbi_bug` recorre ESTADOS_TODOS y calcula el EGRES de las 29 columnas,
#     que son EXACTAMENTE las que `_estado_dx` vuelve a calcular una por spec. Entre eso
#     y Brecha_Medico, cada mascara se calculaba hasta 4 veces sobre el mismo formulario.
#     Medido sobre 60.000 formularios x 29 columnas: calcular las 29 EGRES dos veces
#     cuesta 0,629 s contra 0,289 s memoizadas (2,2x), mismo resultado.
#
# Memo de UNA sola ranura y por WEAKREF, no un parametro. Las dos cosas a proposito:
#   - un parametro `instr_ok=` dejaria pasar una mascara calculada sobre OTRO DataFrame,
#     que alinearia por indice y daria un resultado plausible y errado (regla 2). Aca la
#     mascara se deriva siempre del `df` que se recibe: no hay como equivocarse.
#     (Y no vale guardarse comparando `serie.index is df.index`: pandas NO comparte el
#     objeto indice, lo comprobamos -- da False.)
#   - el weakref evita retener el formulario historico (cientos de MB) despues de la
#     corrida. `ref()` devuelve None cuando el df murio, nunca un objeto distinto, asi
#     que una ranura vieja jamas se confunde con el df de ahora.
# Una ranura basta: dentro de una corrida siempre es el MISMO `form` (construir_poblacion,
# el fallback TGD y las dos pasadas de Brecha_Medico).
#
# OJO, y por eso se devuelve una COPIA: `serie &= otra` en pandas SI muta la Serie en su
# lugar (comprobado, no es como los `int`), asi que entregar el objeto cacheado dejaria
# que un llamador lo pise y la siguiente spec leyera una mascara ya intersectada -- un
# resultado plausible y errado, que es lo que la regla 2 persigue. Copiar una mascara de
# 60k cuesta 0,007 ms contra los 10 ms del `str.contains`: es gratis al lado de lo que
# ahorra, y hace que la memo no tenga forma de morder.
_TOKENS_MEMO = (None, None)   # (weakref al df, {(columna, token): mascara})


def _tok(df, col, token):
    """Mascara booleana '`df[col]` contiene `token`', cacheada por DataFrame (ver arriba).
    `regex=False` como `rem_utils.es_medico`: todos los tokens son literales."""
    global _TOKENS_MEMO
    ref, cache = _TOKENS_MEMO
    if cache is None or ref() is not df:
        cache = {}
        _TOKENS_MEMO = (weakref.ref(df), cache)
    clave = (col, token)
    if clave not in cache:
        cache[clave] = df[col].str.contains(token, regex=False, na=False)
    return cache[clave].copy()


def _instr_medico(df):
    """Mascara booleana 'el formulario lo aplico un MEDICO' de `df`, memoizada.

    El criterio (que token, con que semantica) NO vive aca: es `rem_utils.TOKEN_MEDICO`,
    el mismo que usa el A23 via `es_medico`. Este modulo solo le agrega la memo, porque
    lo pide 28 veces por pasada."""
    return _tok(df, "INSTR_n", TOKEN_MEDICO)


def _estado_dx(df, dx, estado, corte, mes_ini, mes_fin, *, instrumento=True,
              subtipo=None, subtipo2=None):
    """Motor ÚNICO (parametrizado por dx/estado/instrumento) que reemplaza las
    28 fórmulas (form) del DAX (§4.2 del plan): busca, por RUN, el último
    formulario con `dx`contieneSI & `estado`contieneingreso|seguimiento (filtrando INSTRUMENTO
    contiene MEDIC solo si `instrumento`=True — D2/D3) hasta `corte`; separa el egreso
    POR DIAGNÓSTICO (§4.3, no el bug del PowerBI): Egresado si ESE mismo bloque
    ESTADO trae 'egreso' dentro del mes reportado [mes_ini, mes_fin].

    Devuelve DataFrame indexado por RUN: 'activo_base' (bool, antes del egreso —
    para la auditoría §4.3), 'estado' ('Activo'/'Egresado'/''), 'subtipo'/
    'subtipo2' (valor CRUDO del último formulario activo; D5: no se filtra acá
    si viene vacío — eso lo decide quien consume la tabla), y 'instr'/'fecha'
    (INSTRUMENTO y FECHA del formulario que ganó — los usa Brecha_Medico, §8.6,
    para decir QUIÉN registró el dx y HACE CUÁNTO)."""
    qd, qe = f"q{dx}_n", f"q{estado}_n"
    cond_si = df[qd] == "SI"
    cond_ing = cond_si & (_tok(df, qe, "INGRES") | _tok(df, qe, "SEGUIMIEN"))
    cond_egr = cond_si & _tok(df, qe, "EGRES")
    if instrumento:
        instr_ok = _instr_medico(df)
        cond_ing &= instr_ok
        cond_egr &= instr_ok

    # Solo las columnas que se LEEN del resultado. `df` trae ~130 columnas (q<N> y
    # q<N>_n de cada una de las ~65 preguntas) y esta funcion corre 29 veces por pasada
    # de `construir_poblacion` -- y Brecha_Medico (§8.6) agrega una pasada entera mas,
    # con otras 44 llamadas sueltas: copiar y ordenar esas 130 columnas para leer 5 era
    # el costo dominante de toda la familia poblacion.
    # Es EXACTAMENTE el mismo resultado, no una aproximacion: `sort_values` ordena por
    # la clave FECHA sola (el orden de filas no depende de cuantas columnas cuelguen) y
    # `groupby().last()` trabaja columna por columna. Medido sobre 30k x 130: 0.22 s ->
    # 0.008 s por llamada, con los dos resultados comparados fila a fila.
    # OJO si algun dia se lee otra columna de `activos`: hay que agregarla ACA.
    cols = [c for c in ("RUN", "FECHA", "INSTR",
                        f"q{subtipo}" if subtipo else None,
                        f"q{subtipo2}" if subtipo2 else None)
            if c and c in df.columns]
    activos = (df.loc[cond_ing & (df["FECHA"] <= corte), cols]
              .sort_values("FECHA").groupby("RUN").last())
    egresados_mes = set(df.loc[cond_egr & df["FECHA"].between(mes_ini, mes_fin), "RUN"])

    out = pd.DataFrame(index=sorted(set(activos.index) | egresados_mes))
    out["activo_base"] = out.index.isin(activos.index)
    out["estado"] = np.where(out.index.isin(egresados_mes), "Egresado",
                             np.where(out["activo_base"], "Activo", ""))
    if subtipo:
        col = f"q{subtipo}"
        out["subtipo"] = activos[col].reindex(out.index) if col in activos.columns else ""
    if subtipo2:
        col2 = f"q{subtipo2}"
        out["subtipo2"] = activos[col2].reindex(out.index) if col2 in activos.columns else ""
    out["instr"] = activos["INSTR"].reindex(out.index) if "INSTR" in activos.columns else ""
    out["fecha"] = activos["FECHA"].reindex(out.index) if "FECHA" in activos.columns else pd.NaT
    return out


def _aplicar_fallback_tgd(P, form, corte, mes_ini, mes_fin, log):
    """D1: la fila 56 (TGD no especificado) usa la pregunta 91 — que nunca tiene
    dato en el PowerBI (0 referencias en el spec) — con fallback a la pregunta
    "padre" 63, SOLO para quien no tenga ninguna TGD específica activa."""
    est63 = _estado_dx(form, _Q_TGD_FALLBACK, _E_TGD_FALLBACK, corte, mes_ini, mes_fin)
    ya_tiene_tgd = P[_TGD_ESPECIFICAS].apply(lambda c: c.isin(["Activo", "Egresado"])).any(axis=1)
    fallback_estado = P["Número"].map(est63["estado"]).fillna("")
    usa_fallback = (P[COL_TGD_FALLBACK] == "") & ~ya_tiene_tgd & (fallback_estado != "")
    n = int(usa_fallback.sum())
    if n:
        log(f"[poblacion] D1: {n} persona(s) recuperada(s) para «TGD (form)» vía la "
            f"pregunta 63 (fallback; la 91 no tiene columna en el PowerBI actual).")
    P.loc[usa_fallback, COL_TGD_FALLBACK] = fallback_estado[usa_fallback]
    return P


def _egreso_powerbi_bug(form, mes_ini, mes_fin):
    """RUN con CUALQUIER columna ESTADO (de las 28) marcando 'egreso' en el mes
    reportado — replica el bug histórico del PowerBI (§4.3): un egreso de UN
    diagnóstico egresaba TODOS los dx activos del RUN, sin mirar el bloque."""
    m = pd.Series(False, index=form.index)
    for n in ESTADOS_TODOS:
        col = f"q{n}_n"
        if col in form.columns:
            m |= _tok(form, col, "EGRES")   # las mismas 29 que recalcula `_estado_dx`
    m &= form["FECHA"].between(mes_ini, mes_fin)
    return set(form.loc[m, "RUN"])


# ======================================================================
# Actividad SM (Ingresado / Activo 12m / rescate 6m-13m / Gestante)
# ======================================================================
def _runs_actividad_sm(d_ada, ini, fin):
    w = d_ada[(d_ada["FECHA"] >= ini) & (d_ada["FECHA"] <= fin) &
             contiene_alguno(d_ada["ACT_n"], ACTIVIDADES_SM_7)]
    return set(w["RUN"])


def _flags_actividad(d_ada, corte):
    """(activos_12m, rescate_6m, rescate_13m): sets de RUN. Ver §8.1 del plan —
    las 3 usan la MISMA lista de actividades validada (ACTIVIDADES_SM_7)."""
    ini12, _ = _mes_offset(corte, 11)
    activos12 = _runs_actividad_sm(d_ada, ini12, corte)

    ini6, fin6 = _mes_offset(corte, 6)
    activos6 = _runs_actividad_sm(d_ada, ini6, fin6)
    posteriores6 = set(d_ada.loc[(d_ada["FECHA"] > fin6) & (d_ada["FECHA"] <= corte) &
                                 contiene_alguno(d_ada["ACT_n"], ACTIVIDADES_SM_7), "RUN"])
    rescate6 = activos6 - posteriores6

    ini13, fin13 = _mes_offset(corte, 13)
    activos13mes = _runs_actividad_sm(d_ada, ini13, fin13)
    rescate13 = activos13mes - activos12

    return activos12, rescate6, rescate13


def _verificar_cobertura_fechas(form, d_ada, corte, log):
    """Fail loud (§CLAUDE.md) sobre DESCALCES de fecha entre inputs — hoy el único
    chequeo que existía era el de la ventana de gestante (3 meses); esto generaliza
    a TODO lo que corte/ADA/formulario necesitan cubrir. Un histórico INCOMPLETO no
    bloquea (algunos workflows arrancan sin histórico completo a propósito), pero
    nunca en silencio.

    Lo que SÍ bloquea (ArchivoInvalido) es una fuente que queda VACÍA tras el corte:
    ninguna fecha legible, o todas posteriores al mes reportado. Ahí no hay nada que
    avisar a medias: el P6 saldría entero en 0 (¿Ingresado?=NO o ¿Activo 12m?=NO
    para todos) con cara de resultado legítimo -- el mismo caso que `filtrar_mes`
    corta en los módulos de actividades.

    Acá el mes es un CORTE sobre el snapshot de inscritos, no un filtro de filas:
    no existe el "0 filas del mes" que sí guarda `rem_utils.filtrar_mes` en los
    módulos de actividades. Por eso avisa en vez de bloquear — y el aviso se
    DEVUELVE, para que además del log quede escrito en la hoja LEEME del .xlsx
    (si no, un desfase se lee en la consola y se olvida al mirar la planilla).

    Devuelve la lista de avisos (casilla, estado, motivo, que_hacer) de cobertura."""
    avisos = []
    ada_min = d_ada["FECHA"].min() if d_ada["FECHA"].notna().any() else None
    ada_max = d_ada["FECHA"].max() if d_ada["FECHA"].notna().any() else None
    form_min = form["FECHA"].min() if form["FECHA"].notna().any() else None
    form_max = form["FECHA"].max() if form["FECHA"].notna().any() else None

    def _mes(v):
        return f"{v:%Y-%m}" if v is not None else "?"

    def _ym(v):   # (año, mes) para comparar a nivel de MES, no de timestamp exacto
        return (v.year, v.month)

    log(f"[poblacion] cobertura de fechas -> corte: {corte:%Y-%m} | formulario SM: "
        f"{_mes(form_min)}..{_mes(form_max)} | ADA: {_mes(ada_min)}..{_mes(ada_max)}")

    # Fuente vacia TRAS el corte -> fail loud (CLAUDE.md regla 2), no un aviso: todo
    # lo que se calcula de ella sale en 0 para TODOS, sin nada que lo distinga de un
    # mes real. `len == 0` ya lo cortan los loaders; esto es el "tiene filas, pero
    # ninguna sirve para este corte".
    for nombre, fmin, que in (
            ("el formulario 'Control de Salud Mental'", form_min, "¿Ingresado? y los diagnósticos"),
            ("el ADA (Atenciones / Diagnosticos / Actividades)", ada_min,
             "¿Activo 12m?, el rescate y gestante")):
        if fmin is None:
            raise ArchivoInvalido(
                "sin_fecha",
                f"En {nombre} ninguna fila tiene una fecha legible, así que no se puede "
                f"calcular {que} al corte {corte:%m/%Y}.\n\n"
                "Revisa que sea el export correcto y que esté SIN modificar "
                "(una columna de fecha reformateada a mano rompe la lectura).")
        if _ym(fmin) > _ym(corte):
            raise ArchivoInvalido(
                "mes_vacio",
                f"Todas las filas de {nombre} son POSTERIORES al mes reportado "
                f"({corte:%m/%Y}): la primera es de {fmin:%m/%Y}. Con ese corte, "
                f"{que} saldrían en 0 para todos.\n\n"
                "Revisa el mes/año elegido, o carga el histórico que cubra ese período.")

    # El ADA debe llegar HASTA el mes reportado -> si no, Activo12m/rescate/gestante
    # de ESTE mes quedan incompletos (falta la atención más reciente). Comparación por
    # MES: nada garantiza una atención el último día calendario exacto del mes.
    if ada_max is not None and _ym(ada_max) < _ym(corte):
        log(f"[poblacion] El ADA NO llega hasta el mes reportado ({corte:%Y-%m}): "
            f"la atención más reciente cargada es de {ada_max:%Y-%m}. ¿Falta el export "
            "más nuevo, o se eligió mal el mes? Activo12m/rescate/gestante van a salir "
            "incompletos para este mes.")
        avisos.append((
            "Poblacion en control (corte del mes)", "INCOMPLETO",
            f"se pidio el mes {corte:%Y-%m} pero el ADA llega solo hasta "
            f"{ada_max:%Y-%m}: las atenciones del mes reportado NO estan en el "
            "archivo, asi que Activo 12m / rescate / gestante subcuentan",
            f"Cargar el ADA hasta {corte:%Y-%m}, o reportar el mes que cubre el archivo"))

    # El ADA necesita llegar hasta 13 meses atrás (Activo 12m exige un mínimo de 12;
    # rescate 13m mira específicamente el mes exacto -13; gestante solo 3 meses ->
    # queda cubierto si esto se cumple). Idem: por MES, no por día exacto.
    ini13, _ = _mes_offset(corte, 13)
    if ada_min is not None and _ym(ada_min) > _ym(ini13):
        log(f"[poblacion] El ADA arranca en {ada_min:%Y-%m}, pero Activo12m/rescate "
            f"13m/gestante necesitan desde {ini13:%Y-%m} (13 meses cerrados) -> pueden "
            "SUBCONTAR. Carga el histórico de 13 meses del ADA (§3 del plan).")
        avisos.append((
            "Activo 12m / rescate 13m / gestante", "SUBCONTADO",
            f"el ADA arranca en {ada_min:%Y-%m} y se necesita desde {ini13:%Y-%m} "
            "(13 meses cerrados hacia atras)",
            "Cargar el historico de 13 meses del ADA"))

    # El histórico del formulario debe llegar hasta el mes reportado -> si no, un
    # ingreso/egreso de ESTE mes no está en los datos y el snapshot queda desfasado.
    if form_max is not None and _ym(form_max) < _ym(corte):
        log(f"[poblacion] El histórico del formulario SM NO llega hasta el mes "
            f"reportado ({corte:%Y-%m}): el formulario más reciente cargado es de "
            f"{form_max:%Y-%m}. Ingresos/egresos de este mes NO se van a reflejar -> "
            "revisa que el histórico esté actualizado.")
        avisos.append((
            "Diagnosticos / ingresos y egresos del mes", "DESFASADO",
            f"se pidio el mes {corte:%Y-%m} pero el historico del formulario SM "
            f"llega solo hasta {form_max:%Y-%m}: los ingresos y egresos del mes "
            "reportado no estan en el archivo",
            f"Descargar el historico del formulario SM hasta {corte:%Y-%m}"))
    return avisos


def _ultima_respuesta(form, pregunta, corte):
    """Última respuesta NO vacía a `pregunta`, por RUN, hasta `corte` (para
    'Madre <5 años': se reporta con el dato más reciente que exista, sin
    exigir ingreso/seguimiento — así lo trae el DAX)."""
    q = f"q{pregunta}_n"
    # Recorte de columnas por el MISMO motivo y con el MISMO argumento que `_estado_dx`
    # (ver alla): de las ~134 columnas del formulario historico aca se lee UNA, y
    # ordenar y agrupar las otras 131 era todo el costo. `sort_values` ordena por la
    # clave FECHA sola y `groupby().last()` trabaja columna por columna, asi que el
    # resultado es identico. Medido sobre 60.000 x 132: 0,514 s -> 0,019 s (28x),
    # comparado tambien con fechas llenas de empates a proposito (25 fechas distintas
    # sobre 60.000 filas), que es donde el orden podria moverse.
    cols = [c for c in ("RUN", "FECHA", q) if c in form.columns]
    w = (form.loc[(form[q] != "") & (form["FECHA"] <= corte), cols]
         .sort_values("FECHA").groupby("RUN").last())
    return w[q] if q in w.columns else pd.Series(dtype=object)


# ======================================================================
# Las 28 columnas de diagnóstico — motor compartido por las DOS pasadas
# ======================================================================
# (`_COLS_DX` se define junto a TODAS_LAS_SPECS, arriba: lo comparte con `_col_dx()`.)
def _ingresado(P):
    """Máscara booleana `¿Ingresado?`: CUALQUIER dx/factor quedó 'Activo'. Regla en UN
    solo lugar, porque la usan las dos pasadas y su DIFERENCIA es la Brecha_Medico."""
    return (P[_COLS_DX] == "Activo").any(axis=1)


def _poner_diagnosticos(P, form, corte, mes_ini, mes_fin, exigir_medico, log,
                        con_subtipos=True, divergencias=None, por_spec=None):
    """Escribe en `P` las columnas de los 28 diagnósticos/factores ('Activo' /
    'Egresado' / '') y aplica el fallback TGD (D1). Devuelve `P`.

    Es el ÚNICO lugar donde se decide qué diagnóstico queda Activo, y eso es a
    propósito: lo llaman `construir_poblacion` y `runs_ingresados_sin_filtro_medico`
    (§8.6), y el número que sale de COMPARAR las dos ES la Brecha_Medico. Con una copia
    del bucle en cada lado, una puede derivar de la otra y la brecha pasaría a medir la
    diferencia entre dos implementaciones en vez de la del filtro de estamento — un
    número plausible y errado, callado (CLAUDE.md regla 2).

    `con_subtipos=False` para quien solo va a leer `¿Ingresado?`: el 'estado' sale del
    índice de `activos` y del set de egresados, NUNCA de los subtipos, así que es el
    mismo valor y `_estado_dx` se ahorra arrastrar dos columnas más por spec.

    `divergencias` = lista donde acumular la auditoría §4.3 (None = no auditar; la
    Brecha no la necesita y así se salta también `_egreso_powerbi_bug`).

    `por_spec` = dict donde dejar `{columna: tabla de _estado_dx}` de ESTA pasada. Para
    quien además del veredicto necesita el POR QUÉ (Brecha_Medico usa 'instr' y 'fecha'):
    sin esto volvía a llamar a `_estado_dx` spec por spec sobre el mismo formulario, con
    los mismos argumentos, para reconstruir las tablas que esta función acababa de tirar.

    OJO con el fallback TGD: llama a `_estado_dx` SIN pasarle `instrumento`, o sea que
    la pregunta 63 sigue exigiendo médico aunque `exigir_medico` esté en False. Es el
    comportamiento que había antes de partir esta función en dos y se conserva TAL CUAL
    — si algún día se decide que el toggle también debe alcanzarlo, se cambia acá y
    cambia en las dos pasadas a la vez, que es justamente la gracia."""
    en_bug = None
    if divergencias is not None:
        # `_egreso_powerbi_bug` no depende de la spec: se calcula UNA vez, no 28.
        en_bug = P["Número"].isin(_egreso_powerbi_bug(form, mes_ini, mes_fin))
    for spec in TODAS_LAS_SPECS:
        est = _estado_dx(form, spec["dx"], spec["estado"], corte, mes_ini, mes_fin,
                         instrumento=spec["instrumento"] and exigir_medico,
                         subtipo=spec["subtipo"] if con_subtipos else None,
                         subtipo2=spec["subtipo2"] if con_subtipos else None)
        if por_spec is not None:
            por_spec[spec["col"]] = est
        P[spec["col"]] = P["Número"].map(est["estado"]).fillna("")
        if con_subtipos and spec["subtipo_col"]:
            P[spec["subtipo_col"]] = P["Número"].map(est.get("subtipo", pd.Series(dtype=object))).fillna("")
        if con_subtipos and spec["subtipo2_col"]:
            P[spec["subtipo2_col"]] = P["Número"].map(est.get("subtipo2", pd.Series(dtype=object))).fillna("")
        if divergencias is None:
            continue
        # Auditoría §4.3: valor que habría dado el PowerBI (bug cross-dx de egreso).
        # Se guarda el RUN (no solo el conteo) para que Egreso_Divergencias sea auditable.
        base = P["Número"].map(est["activo_base"]).fillna(False)
        pbi = np.where(base & en_bug, "Egresado", np.where(base, "Activo", ""))
        diverge = ((P[spec["col"]] != pbi) & base).to_numpy()
        if diverge.any():
            for run, nuestro, pbi_v in zip(P.loc[diverge, "Número"], P.loc[diverge, spec["col"]],
                                           pbi[diverge]):
                divergencias.append({"Diagnostico": spec["col"], "RUN": run,
                                     "Valor_port": nuestro, "Valor_PowerBI": pbi_v})
    return _aplicar_fallback_tgd(P, form, corte, mes_ini, mes_fin, log)


def runs_ingresados_sin_filtro_medico(P, form, mes=None, log=print, con_detalle=False):
    """Los RUN que quedarían `¿Ingresado?`=SI con el filtro de estamento médico
    APAGADO. USO EXCLUSIVO de Brecha_Medico (§8.6 del plan) — nunca del P6.

    POR QUÉ existe: `calcular_brecha_medico` corría `construir_poblacion` COMPLETA una
    segunda vez (1,66 s de los 4,06 s de la familia población, el 41% del total) y de
    esa tabla entera consumía UNA columna. El toggle solo toca los ~25 diagnósticos que
    filtran por estamento: la demografía, la edad al corte, Pueblo/Migrante, PROTECCION
    NIÑEZ, los flags de actividad, gestante, Madre<5 y la cobertura de fechas salen
    IDÉNTICOS en las dos pasadas. Y `Estado` y `¿Activo 12m?` también — que es lo otro
    que mira la base de la brecha —, así que se leen del `P` que ya existe en vez de
    recalcularse: `Estado` viene del Inscritos y `¿Activo 12m?` de `_flags_actividad`,
    y ninguno de los dos sabe del toggle.

    Devuelve un SET de RUN, y NO una columna, a propósito: una Serie alineada a `P` se
    puede escribir de vuelta en la tabla, y ahí el guardarraíl del P6 —que mira
    `attrs['exigir_medico']`— ya no la vería. Quedaría un `¿Ingresado?` sin filtro de
    estamento dentro de un `P` que se declara filtrado, que es exactamente el número
    plausible y errado que ese guardarraíl existe para impedir. Un set no se pega por
    descuido.

    `con_detalle=True` devuelve `(runs, {columna: tabla de _estado_dx})` con las tablas
    de ESTA misma pasada. Es para Brecha_Medico, que después necesita el 'instr' y la
    'fecha' del formulario que ganó: sin esto las volvía a calcular spec por spec, sobre
    el mismo formulario y con los mismos argumentos, justo después de que esta función
    las tirara — ~25 `_estado_dx` de regalo, en la función que existe para no repetir
    una pasada."""
    ini, fin = _rango_mes(mes)
    Q = pd.DataFrame({"Número": P["Número"].to_numpy()})
    por_spec = {} if con_detalle else None
    Q = _poner_diagnosticos(Q, form, fin, ini, fin, False, log, con_subtipos=False,
                            por_spec=por_spec)
    runs = set(Q.loc[_ingresado(Q), "Número"])
    return (runs, por_spec) if con_detalle else runs


# ======================================================================
# Ensamblado: construir_poblacion()
# ======================================================================
def construir_poblacion(inscritos, formulario_sm, ada, mes=None, log=print,
                        exigir_medico=True):
    """Arma la tabla «Ferrada» SLIM (§3.2): TODOS los inscritos (snapshot), 1
    fila por RUN, sin filtrar por Activo/Ingresado (eso lo aplica quien consuma
    la tabla — el P6 filtra, el rescate filtra distinto). `mes`=(año,mes) fija
    el corte (None = mes anterior, como el resto de los módulos pandas).
    `inscritos`/`formulario_sm`/`ada` aceptan DataFrame ya cargado (para no
    releer el archivo si el caller ya lo tiene, p.ej. para correr dos pasadas
    con `exigir_medico` distinto) o ruta(s) del export correspondiente.

    `exigir_medico=False` (§8.6 del plan, SOLO para Brecha_Medico): apaga el
    filtro INSTRUMENTO contiene MEDIC en los diagnósticos que normalmente lo exigen.
    NUNCA usar False para el P6 — ver guardarraíl en rem_sp_p6_poblacion."""
    ini, fin = _rango_mes(mes)
    corte = fin
    mes_ini, mes_fin = ini, fin

    insc = inscritos if isinstance(inscritos, pd.DataFrame) else cargar_inscritos(inscritos, log=log)
    form = formulario_sm if isinstance(formulario_sm, pd.DataFrame) else cargar_formulario_sm(formulario_sm, log=log)
    d_ada = ada if isinstance(ada, pd.DataFrame) else cargar_atenciones(ada, log=log)
    if len(d_ada) == 0:
        # Fail loud sobre la FUENTE (CLAUDE.md regla 2): la familia poblacion no pasa
        # por filtrar_mes, y un ADA vacio revienta abajo en .str.contains().
        raise ArchivoInvalido(
            "sin_datos",
            "El ADA (Atenciones / Diagnosticos / Actividades) no trae ninguna fila de "
            "datos.\n\nRevisa que sea el export completo de IRIS (no solo el encabezado) "
            "y que este sin modificar.")
    avisos_cobertura = _verificar_cobertura_fechas(form, d_ada, corte, log)
    for nombre, faltan in (form.attrs.get("preguntas_faltantes") or {}).items():
        avisos_cobertura.append((
            "Diagnosticos del formulario SM", "SUBCONTADO",
            f"«{nombre}» no trae {len(faltan)} pregunta(s) que usa la tabla "
            f"({', '.join(map(str, faltan[:12]))}{'...' if len(faltan) > 12 else ''}): "
            "esos diagnosticos no se leen de ese archivo",
            "Revisar que el export sea el formulario IRIS completo, sin modificar"))

    # El ADA trae filas en la ventana de 13 meses pero NINGUNA de las 7 actividades SM
    # -> ¿Activo 12m? y el rescate = NO para TODOS, con cara de legitimo (el gemelo del
    # SM sin nada que tribute). Un ADA fuera de la ventana ya lo avisa la cobertura.
    ini13, _ = _mes_offset(corte, 13)
    en_ventana = d_ada[(d_ada["FECHA"] >= ini13) & (d_ada["FECHA"] <= corte)]
    if len(en_ventana) and not _runs_actividad_sm(d_ada, ini13, corte):
        raise ArchivoInvalido(
            "sin_datos",
            f"El ADA trae {len(en_ventana)} atención(es) entre {ini13:%m/%Y} y "
            f"{corte:%m/%Y}, pero NINGUNA es una actividad de Salud Mental (control, "
            "consulta, ingreso...).\n\n¿Activo 12m? y el rescate saldrían en NO para "
            "todos. Revisa que el ADA sea el export COMPLETO del centro (no filtrado por "
            "otro programa) y que esté SIN modificar.")

    P = insc.rename(columns={"RUN": "Número", "TIPOID": "Tipo de identificación",
                             "SITUACION": "Situación", "ESTADO": "Estado",
                             "FPASIV": "Fecha Pasivación", "MPASIV": "Motivo Pasivación",
                             "SECTOR": "Sector"}).copy()

    # -- Sexo/Género (Sexo vacío -> 'No informado', igual que el DAX) --
    P["Sexo"] = P["SEXO"].where(P["SEXO"].notna() & (P["SEXO"].astype(str).str.strip() != ""),
                                "No informado")
    P["Género"] = P["GENERO"]

    # -- Edad al CORTE (no a hoy): fecha nacimiento; fallback EDAD AÑOS del snapshot --
    fnac = fecha_col(P["FNAC"], log, "Fecha Nacimiento (Inscritos)")
    edad_calc = ((corte - fnac).dt.days / 365.25).apply(lambda x: int(x) if pd.notna(x) else np.nan)
    edad_fallback = pd.to_numeric(P["EDADANOS"], errors="coerce")
    P["Edad"] = edad_calc.where(edad_calc.notna(), edad_fallback)

    # -- Pueblo Originario / Migrante (norm-based; más robusto que el literal del DAX) --
    P["Pueblo Originario"] = P["PUEBLO"]
    nac_n = P["NACIONALIDAD"].map(norm)
    pueblo_n = P["PUEBLO"].map(norm)
    es_migrante = ~nac_n.isin({"", "CHILENA", "DESCONOCIDO", "DESCONOCIDA"})
    es_originario = (nac_n == "CHILENA") & (~pueblo_n.isin(PUEBLO_VACIO))
    P["¿Originario o Migrante?"] = np.select([es_migrante, es_originario],
                                             ["Migrante", "Originario"], default="NO")

    # -- PROTECCION NIÑEZ (SENAME / Mejor Niñez, desde ALERTAS ADMINISTRATIVAS) --
    alertas_n = P["ALERTAS"].map(norm)
    es_sename = alertas_n.str.contains("SENAME", na=False)
    es_mejorninez = alertas_n.str.contains("SPE", na=False) | alertas_n.str.contains("MEJOR NINEZ", na=False)
    P["PROTECCION NIÑEZ"] = np.select([es_sename, es_mejorninez], ["SENAME", "Mejor Niñez"], default="NO")

    # -- Actividad SM (§8.1: misma lista de 7 para las 3 definiciones) --
    activos12, rescate6, rescate13 = _flags_actividad(d_ada, corte)
    P["¿Activo 12m?"] = np.where(P["Número"].isin(activos12), "SI", "NO")
    P["¿Última atención hace 6m?"] = np.where(P["Número"].isin(rescate6), "Si", "No")
    P["¿Última atención hace 13m?"] = np.where(P["Número"].isin(rescate13), "Si", "No")

    # -- Gestante (§4.7: 3 meses cerrados, matrona; NO el DAX de 2 meses). Cubierta
    #     por el chequeo general de cobertura de arriba (13 meses > 3 meses). --
    ini3 = ini - pd.DateOffset(months=2)
    gset = gestante_runs(d_ada, ini3, corte)
    P["¿Embarazada?"] = np.where(P["Número"].isin(gset), "SI", "NO")

    # -- Madre <5 años (pregunta 1, última respuesta con dato; SIN filtro de
    #     sexo acá -- eso es una regla del P6, no de Ferrada, §5.4.1 del plan) --
    m5 = _ultima_respuesta(form, 1, corte)
    P["Madre <5 años"] = P["Número"].map(m5).fillna("")

    # -- Los 28 diagnósticos/factores de riesgo (motor único, ver _estado_dx) --
    divergencias_detalle = []   # 1 fila por (Diagnóstico, RUN) que diverge — auditoría §4.3
    P = _poner_diagnosticos(P, form, corte, mes_ini, mes_fin, exigir_medico, log,
                            divergencias=divergencias_detalle)

    # -- ¿Ingresado? (SI si CUALQUIER dx/FR quedó 'Activo') --
    P["¿Ingresado?"] = np.where(_ingresado(P), "SI", "NO")

    # -- ¿Pertenece? en sus DOS versiones (ver _PERTENECE_FALTANTES_EN_DAX) --
    cols_dx = _COLS_DX
    cols_24 = [c for c in cols_dx if c not in _PERTENECE_FALTANTES_EN_DAX]
    P["¿Pertenece? (24 DAX)"] = np.where((P[cols_24] != "").any(axis=1), "SI", "NO")
    P["¿Pertenece? (28 real)"] = np.where((P[cols_dx] != "").any(axis=1), "SI", "NO")

    div_df = pd.DataFrame(divergencias_detalle,
                          columns=["Diagnostico", "RUN", "Valor_port", "Valor_PowerBI"])
    if len(div_df):
        div_df = div_df.sort_values(["Diagnostico", "RUN"]).reset_index(drop=True)
        resumen = div_df.groupby("Diagnostico", sort=False).size()
        log(f"[poblacion] §4.3 egreso por diagnóstico: {len(div_df)} persona(s)×diagnóstico "
            f"difieren del PowerBI (que egresaba TODOS los dx con cualquier egreso del RUN en "
            f"el mes). Detalle (con RUT) en la hoja 'Egreso_Divergencias'. Esperado, no es bug. "
            + " · ".join(f"{d}={n}" for d, n in resumen.items()))
    else:
        log("[poblacion] §4.3: sin divergencias de egreso este mes.")

    if not exigir_medico:
        log("[poblacion] §8.6: exigir_medico=False — diagnosticos que exigen estamento "
            "medico NO estan filtrando por instrumento en esta pasada. Uso exclusivo: "
            "Brecha_Medico (rem_sm_rescate_inasistentes). NUNCA para el P6.")
    P.attrs["mes"] = (ini.year, ini.month)
    P.attrs["egreso_divergencias"] = div_df
    P.attrs["avisos"] = avisos_cobertura
    n_ingresados = int((P["¿Ingresado?"] == "SI").sum())
    log(f"[poblacion] Ferrada: {len(P)} personas en el snapshot | {n_ingresados} con "
        f"¿Ingresado?=SI (mes {ini:%Y-%m})")
    if not (1300 <= n_ingresados <= 1500):
        log(f"[poblacion] {n_ingresados} ingresados está fuera del rango histórico "
            "~1300-1500 esperado para este centro (sanity check, no error automático).")

    # .attrs de pandas NO se propaga de forma confiable al recortar columnas
    # (es "experimental" en pandas) -> se reasigna explícito sobre la salida.
    P_out = P[COLUMNAS_SALIDA].copy()
    P_out.attrs["mes"] = P.attrs["mes"]
    P_out.attrs["egreso_divergencias"] = P.attrs["egreso_divergencias"]
    P_out.attrs["exigir_medico"] = exigir_medico
    P_out.attrs["avisos"] = P.attrs["avisos"]
    return P_out


def escribir_divergencias(wb, div, sheet_name="Egreso_Divergencias"):
    """Escribe `div` (columnas Diagnostico/RUN/Valor_port/Valor_PowerBI, YA ordenado
    por Diagnostico) como bloques COLAPSABLES por diagnóstico (agrupación de filas de
    Excel, +/- en el margen izquierdo, §4.3 del plan): 1 fila de cabecera con el
    diagnóstico y el total, y debajo el detalle por RUN. `wb` = Workbook openpyxl.
    Nada que escribir -> no crea la hoja."""
    if div is None or not len(div):
        return None
    from openpyxl.styles import Font
    from openpyxl.utils import get_column_letter
    ws = wb.create_sheet(sheet_name)
    ws.sheet_properties.outlinePr.summaryBelow = False   # cabecera ARRIBA de su detalle -> el
                                                          # +/- de colapsar queda junto a ella
    ws.append(["Diagnóstico", "N personas", "RUN", "Valor_port", "Valor_PowerBI (con el bug §4.3)"])
    for c in ws[1]:
        c.font = Font(bold=True)
    r = 2
    for diag, sub in div.groupby("Diagnostico", sort=False):
        ws.cell(row=r, column=1, value=diag).font = Font(bold=True)
        ws.cell(row=r, column=2, value=len(sub))
        r += 1
        for _, fila in sub.iterrows():
            ws.cell(row=r, column=3, value=fila["RUN"])
            ws.cell(row=r, column=4, value=fila["Valor_port"])
            ws.cell(row=r, column=5, value=fila["Valor_PowerBI"])
            ws.row_dimensions[r].outline_level = 1   # colapsable bajo la cabecera del diagnóstico
            r += 1
    ws.freeze_panes = "A2"
    for i, w in enumerate([38, 11, 14, 16, 26], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    return ws


def escribir(P, salida):
    """Escribe `PSM_Poblacion` (la tabla intermedia, snapshot mensual archivable)
    + `Egreso_Divergencias` (auditoría §4.3, con RUT y colapsable por diagnóstico —
    ver `escribir_divergencias`) en un solo .xlsx."""
    with pd.ExcelWriter(salida, engine="openpyxl") as xw:
        P.to_excel(xw, index=False, sheet_name="PSM_Poblacion")
        escribir_divergencias(xw.book, P.attrs.get("egreso_divergencias"))
    return str(salida)
