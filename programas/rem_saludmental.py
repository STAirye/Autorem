#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.9.17
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
rem_saludmental.py — capa compartida del formulario 'Control de Salud Mental'.

Conoce la ESTRUCTURA del formulario (no una sección concreta del REM): dónde está
el encabezado, cómo se ubican RUT/edad/sexo, la caminata al diagnóstico, subtipos,
demografía y el motor de marcado de eventos por token de ESTADO.

El mismo formulario se puede descargar en DOS formatos de export distintos:
  - PERFIL_IRIS   ('Control de Salud Mental' de IRIS)   -> el que la herramienta
                  fue hecha para procesar; trae todas las columnas.
  - PERFIL_ADMIN  ('Reporte Administrativo' de RAYEN)   -> mismo formulario, otro
                  layout de encabezado y SIN varias columnas demográficas.

Un 'perfil' encapsula esas diferencias de formato; las tareas (egresos/ingresos)
son agnósticas al formato. Lo consumen rem_a05_o_egresos.py y rem_a05_n_ingresos.py.
La GUI/CLI (autorem.py) deja elegir el perfil al inicio.

+======================================================================+
|  Aquí vive la CONFIGURACIÓN CLÍNICA del formulario.                    |
+======================================================================+
"""

import re

from programas.rem_utils import (
    OPENPYXL_OK, OPENPYXL_ERR, openpyxl,
    ArchivoInvalido,
    norm, buscar_col, num_pregunta,
    encontrar_fila_encabezado, edad_anios, mes_de_celda,
    PUEBLO_VACIO, verificar_hoja_unica, _mujer, trans_de, exigir_filas_ws,
)
from programas import formatos

# -- Diagnósticos con subtipo (clave = N.- diagnóstico, valor = N.- subtipo) --
# La numeración de preguntas es IDÉNTICA en IRIS y en el Administrativo.
DIAGNOSTICOS_CON_SUBTIPO = {
    4:  6,    # Violencia   -> 6.- TIPO DE VIOLENCIA
    11: 12,   # Suicidio    -> 12.- TIPO DE SUICIDIO
    18: 20,   # Depresión   -> 20.- TIPO DE DEPRESIÓN
    41: 43,   # Ansiedad    -> 43.- TIPO DE TRASTORNO DE ANSIEDAD
    44: 45,   # Alzheimer   -> 45.- ETAPA
}
SUBTIPO_NUMS = set(DIAGNOSTICOS_CON_SUBTIPO.values())

# Remapeo de bloques deprecated -> (patología, subtipo) forzados.
REMAP_DIAGNOSTICO = {
    9: ("Violencia", "Sexual"),   # Abuso Sexual (deprecated) -> Violencia > Víctima > Sexual
}

# Diagnósticos que NO van al A05 Salud Mental (se saltan del output):
#   epilepsia -> REM adulto; programas de rehabilitación/acompañamiento -> no son
#   egresos/ingresos de diagnóstico SM.
EXCLUIR_PATOLOGIA = {75, 77, 79, 81}

# Nombre de patología: True = limpiar_patologia() + OVERRIDE (nombres canónicos,
# tomados de SP·P6 y revisados jul-2026). False = header crudo.
LIMPIAR_NOMBRE_PATOLOGIA = True
OVERRIDE_PATOLOGIA = {
    4:  "Violencia",
    11: "Suicidio",
    18: "Depresión",
    21: "Depresión post parto",
    23: "Trastorno bipolar",                 # RAYEN trae typo 'Transtorno'
    25: "Depresión refractaria",
    27: "Depresión grave con psicosis",
    29: "Depresión con alto riesgo suicida",
    31: "Consumo perjudicial de alcohol",
    33: "Consumo dependiente de alcohol",
    35: "Consumo perjudicial de drogas",
    37: "Consumo dependiente de drogas",
    39: "Consumo de drogas y alcohol",
    41: "Trastorno de ansiedad",
    44: "Demencia (incluye Alzheimer)",
    47: "Psicosis",
    49: "Trastorno adaptativo",
    51: "Esquizofrenia",
    53: "Primer episodio de esquizofrenia",
    55: "Trastorno de la conducta alimentaria",
    57: "TDAH (trastorno hipercinético)",
    59: "Retraso mental",
    61: "Trastorno de personalidad",
    63: "Trastorno generalizado del desarrollo",
    65: "Otros trastornos (no incluidos)",
    67: "Trastornos conductuales asociados a demencia",
    69: "Trastorno disocial desafiante y oposicionista",
    71: "Trastorno de ansiedad de separación en la infancia",
    73: "Otros trastornos del comportamiento y las emociones (infancia)",
    83: "Autismo",
    85: "Asperger",
    87: "Síndrome de Rett",
    89: "Trastorno desintegrativo de la infancia",
    91: "Trastorno generalizado del desarrollo no especificado",
    # 9 (Abuso Sexual) NO va aquí: lo maneja REMAP_DIAGNOSTICO -> Violencia/Sexual.
    # 75/77/79/81 excluidos (ver EXCLUIR_PATOLOGIA).
}

# Override de nombre de SUBTIPO, por Nº de pregunta del subtipo. Cada regla es
# (keywords, nombre): si el valor crudo normalizado contiene CUALQUIER keyword,
# sale ese nombre. Sirve para juntar variantes (el REM tiene 'Pánico' a secas ->
# los dos pánicos de RAYEN caen en uno) y acortar. Los subtipos SIN entrada acá
# (Depresión, Violencia, Suicidio, Alzheimer) salen por el recorte del header,
# que ya los deja limpios (Moderada / Física / Intento / Moderado).
OVERRIDE_SUBTIPO = {
    43: [  # 43.- TIPO DE TRASTORNO DE ANSIEDAD  (¡PANICO antes que FOBIA! 'AgoroFOBIA')
        (["PANICO"],                       "Pánico"),        # junta 'Pánico' y 'Pánico sin agorafobia'
        (["FOBIA"],                        "Fobia social"),
        (["GENERALIZ"],                    "Generalizada"),
        (["TEPT", "ESTRES", "TRAUMATICO"], "TEPT"),
        (["OTROS"],                        "Otros"),
    ],
}

# -- Firma de CONTENIDO del formulario (CLAUDE.md regla 5) ----------------
# Todo lo de arriba (y la tabla del P6 en poblacion.py) ubica las preguntas por su
# NUMERO. Eso solo vale si el archivo ES el formulario 'Control de Salud Mental': un
# cuestionario RAYEN (Goldberg, PSC) trae las mismas firmas IRIS/Admin, su '1.- ESTADO'
# dice Ingreso/Egreso, y hasta la ronda 11 pasaba entero -- «4.- 3. ¿Ha sentido que está
# jugando un papel útil…» se leia como Violencia y el A05 contaba ingresos con
# patologia «Estado». Y si RAYEN RENUMERA el formulario, cada numero apunta a otra
# pregunta sin que nada falle. Por eso cada numero que el codigo usa se contrasta con
# lo que su encabezado DICE. Verificada contra los dos formatos reales
# (refs_tablas/Formularios_RAYEN_csm_IRis.xlsx y Formulario_csm_reporte_Administrativo.xlsx;
# lo vigila tests/test_autorem.py).
FIRMA_FORMULARIO_SM = {
    4: ["VIOLENCIA"], 6: ["TIPO", "VIOLENCIA"], 7: ["VIOLENCIA"], 9: ["ABUSO SEXUAL"],
    11: ["SUICIDIO"], 12: ["TIPO", "SUICIDIO"], 18: ["DEPRESION"], 20: ["TIPO", "DEPRESION"],
    21: ["DEPRESION", "PARTO"], 23: ["BIPOLAR"], 25: ["REFRACTARIA"], 27: ["PSICOSIS"],
    29: ["RIESGO SUICIDA"], 31: ["PERJUDICIAL", "ALCOHOL"], 33: ["DEPENDIENTE", "ALCOHOL"],
    35: ["PERJUDICIAL", "DROGAS"], 37: ["DEPENDIENTE", "DROGAS"], 39: ["DROGAS", "ALCOHOL"],
    41: ["ANSIEDAD"], 43: ["TIPO", "ANSIEDAD"], 44: ["DEMENCIAS"], 45: ["ETAPA"],
    47: ["PSICOSIS"], 49: ["ADAPTATIVO"], 51: ["ESQUIZOFRENIA"], 53: ["ESQUIZOFRENIA"],
    55: ["ALIMENTARIA"], 57: ["HIPERCINETICOS"], 59: ["RETRASO MENTAL"], 61: ["PERSONALIDAD"],
    63: ["GENERALIZADO", "DESARROLLO"], 65: ["NO INCLUIDOS"], 67: ["DEMENCIA"],
    69: ["DISOCIAL"], 71: ["SEPARACION"], 73: ["COMPORTAMIENTO"], 75: ["EPILEPSIA"],
    77: ["REHABILITACION"], 79: ["REHABILITACION"], 81: ["ACOMPANAMIENTO"], 83: ["AUTISMO"],
    85: ["ASPERGER"], 87: ["RETT"], 89: ["DESINTEGRATIVO"], 91: ["GENERALIZADO", "DESARROLLO"],
}
# Y el ESTADO de cada diagnostico va pegado a su pregunta (encontrar_diagnostico y el
# P6 leen el numero siguiente): esos tienen que decir ESTADO.
ESTADOS_FORMULARIO_SM = (5, 10, 13, 19, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 46,
                         48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78,
                         80, 82, 84, 86, 88, 90, 92)


def verificar_formulario_sm(headers, archivo=None):
    """ArchivoInvalido si `headers` no es el encabezado del formulario 'Control de Salud
    Mental' (numero de pregunta -> lo que dice). Una pregunta AUSENTE no falla (un
    historico viejo puede no traer las nuevas); una que esta y dice OTRA cosa, si."""
    n2h = {num_pregunta(h): norm(h) for h in headers if num_pregunta(h) is not None}
    esperado = {n: [norm(t) for t in toks] for n, toks in FIRMA_FORMULARIO_SM.items()}
    esperado.update({n: ["ESTADO"] for n in ESTADOS_FORMULARIO_SM})
    presentes = [n for n in esperado if n in n2h]
    malas = [n for n in presentes if not all(t in n2h[n] for t in esperado[n])]
    donde = f"Archivo «{archivo}»:\n\n" if archivo else ""
    # «No es este formulario» si calza MENOS DE LA MITAD de las preguntas de diagnostico
    # presentes: otro formulario RAYEN coincide por casualidad en alguna (Otros Cronicos
    # tambien trae '75.- ¿Padece de Epilepsia?') y en sus 'N.- ESTADO'.
    dx = [n for n in presentes if n in FIRMA_FORMULARIO_SM]
    if 2 * sum(n not in malas for n in dx) < len(dx) or not dx:
        raise ArchivoInvalido(
            "no_formulario_sm",
            f"{donde}Este archivo no es el formulario 'Control de Salud Mental': sus "
            "preguntas numeradas no son las de ese formulario (¿es un cuestionario, como "
            "Goldberg o PSC, que van en el A03 · D.3? ¿u otro formulario de RAYEN?).\n\n"
            "Descarga el formulario 'Control de Salud Mental' desde RAYEN/IRIS. Si es ese "
            "y lo bajaste tal cual, RAYEN le cambió la numeración: avisa al desarrollador.")
    if malas:
        muestra = "; ".join(f"{n}.- esperaba {' '.join(esperado[n])}" for n in malas[:4])
        raise ArchivoInvalido(
            "formulario_cambiado",
            f"{donde}El formulario 'Control de Salud Mental' no tiene sus preguntas donde "
            f"la herramienta las espera ({len(malas)} de {len(presentes)} no calzan: "
            f"{muestra}{' ...' if len(malas) > 4 else ''}).\n\n"
            "O RAYEN cambió la numeración del formulario, o el archivo fue editado. Si lo "
            "bajaste tal cual, avisa al desarrollador: los diagnósticos se leerían cruzados.")


# -- Detección de columnas de identificación (RUT/edad/sexo, ambos formatos) --
# El eje IRIS/Admin y la resolución de identidad viven en `programas.formatos`
# (compartidos con A03/estamentos). El QUIRK de 'AÑO APLICACIÓN FORMULARIO' (que
# trae la EDAD, no el año) está documentado allá.

# Caracterización demográfica (devuelve "SI"/"" salvo Trans). Validado jul-2026
# contra valores reales de 'ALERTAS ADMINISTRATIVAS' (IRIS). En el Administrativo
# las fuentes ALERTAS/PUEBLO ORIGINARIO/GÉNERO NO existen -> esos flags salen vacíos.
DEMOGRAFIA = {
    "Madre_menor5":        (["USTED", "MADRE"],       ["SI"]),                                   # pregunta 1 (ambos formatos)
    "Pueblos_Originarios": (["PUEBLO", "ORIGINARIO"], "_no_vacio"),                              # solo IRIS
    "SENAME":              (["ALERTAS"],              ["SENAME", "REINSERCION"]),                # solo IRIS
    "Proteccion_Ninez":    (["ALERTAS"],              ["MEJOR NINEZ", "PROTECCION ESPECIAL"]),   # solo IRIS
    "Migrante":            (["ALERTAS"],              ["MIGRANTE"]),                             # solo IRIS
}
# Flags que el REM define SOLO sobre mujeres -> se anulan si el sexo REGISTRAL no es
# femenino. La pregunta 1 ('¿usted es madre de hijo menor de 5 años?') a veces se
# marca en hombres y esos, por definición, no cuentan. El filtro va por SEXO y no por
# GÉNERO: sexo femenino con género transmasculino SÍ cuenta (puede ser madre).
DEMOGRAFIA_SOLO_FEMENINO = {"Madre_menor5"}

COL_GENERO_TOKENS = ["GENERO"]   # Trans: regla rem_utils.trans_de (explícita + implícita; solo IRIS)
# (los "vacío de pueblo" se comparten con pandas: rem_utils.PUEBLO_VACIO, ver flag_demo)

# -- Config técnica compartida --
HOJA = None
# (Hasta 1.9.17 habia un ANIO_COL_FALLBACK = 11: si no se encontraba la columna de edad
# por nombre, se tomaba la columna 11 POR POSICION. Es la posicion del layout IRIS, y
# ahi nunca hacia falta -- el encabezado de edad ES el ancla de la deteccion --; en el
# Administrativo la columna 11 es 'Convenio'. Se armo antes de tener refs_tablas/, a
# ciegas. Ver _preparar: ahora la edad se busca solo por NOMBRE, o falla.)
MAX_FILAS_BUSQUEDA_HEADER = formatos.MAX_FILAS_HEADER

# -- Layout de salida (compartido por egresos/ingresos) --
ANCHOS_BASE = [14, 8, 8, 13, 44, 26, 13]   # RUT, Edad, Sexo, Tipo, Patologia, Subtipo, Falta
ANCHO_DEMO = 11
ANCHOS_COLA = [16, 11]                      # Trans, Fila_Origen


# -- Helpers de estructura del formulario ------------------------------
def es_estado(h):
    return norm(h).endswith("ESTADO")


def limpiar_patologia(header):
    """'18.- ¿ TIENE  DEPRESIÓN ?' -> 'Depresión'. Solo si LIMPIAR_NOMBRE_PATOLOGIA."""
    n = num_pregunta(header)
    if n in OVERRIDE_PATOLOGIA:
        return OVERRIDE_PATOLOGIA[n]
    s = re.sub(r"^\s*\d+\s*\.\-\s*", "", str(header))
    s = s.replace("¿", "").replace("?", "")
    s = re.sub(r"^\s*(TIENE|ES|SUFRE DE|PRESENTA|PADECE)\s+", "", s, flags=re.I)
    s = re.sub(r"^\s*PACIENTE\s+PRESENTA\s+", "", s, flags=re.I)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:1].upper() + s[1:].lower() if s else s


def limpiar_subtipo(valor, subtipo_header):
    """Nombre de subtipo limpio. 1) aplica OVERRIDE_SUBTIPO (mapa por Nº de
    pregunta del subtipo; ej. Ansiedad Q43 junta los dos 'Pánico'). 2) si no hay
    regla, recorta el sustantivo del header ('Depresión Moderada' con
    '20.- TIPO DE DEPRESIÓN' -> 'Moderada'; sin 'TIPO DE' deja el valor)."""
    if valor in (None, ""): return ""
    s = str(valor).strip()
    reglas = OVERRIDE_SUBTIPO.get(num_pregunta(subtipo_header))
    if reglas:
        vn = norm(s)
        for keys, nombre in reglas:
            if any(norm(k) in vn for k in keys):
                return nombre
    m = re.search(r"TIPO DE\s+(.+)$", norm(subtipo_header))
    if m:
        noun = m.group(1).strip()
        if norm(s).startswith(noun):
            rec = s[len(noun):].strip(" -,:")
            if rec: s = rec
    return s


def flag_demo(cell, regla):
    n = norm(cell)
    if regla == "_no_vacio":   # hoy solo Pueblos_Originarios; lista compartida con pandas
        return "SI" if n not in PUEBLO_VACIO else ""
    if isinstance(regla, (list, tuple)):
        return "SI" if any(norm(k) in n for k in regla) else ""
    return ""


def encontrar_diagnostico(headers, c0):
    """Camina a la izquierda del ESTADO saltando subtipos/estados hasta dar
    con la pregunta del diagnóstico. Devuelve índice 0-based o c0 si no hay."""
    d = c0 - 1
    while d >= 0:
        h = headers[d]
        n = num_pregunta(h)
        if es_estado(h) or (n in SUBTIPO_NUMS) or (n is None):
            d -= 1
            continue
        return d
    return c0


# -- DETECCIÓN Y VALIDACIÓN DE FORMATO ---------------------------------
# La detección del eje IRIS/Admin vive en `formatos.detectar_eje` (compartida con
# A03/estamentos, con las firmas RAYEN estándar). Acá solo los validadores con los
# mensajes específicos del formulario 'Control de Salud Mental'.
def detectar_formato(ws):
    """'iris' | 'administrativo' | 'desconocido' (firmas RAYEN estándar)."""
    return formatos.detectar_eje(ws)


def detectar_formato_filas(filas):
    """Igual que `detectar_formato` pero sobre las primeras filas YA LEÍDAS (ver
    `formatos.detectar_eje_filas`): para quien solo quiere saber el formato y no
    necesita el archivo entero, como la detección al elegir el archivo en la GUI."""
    return formatos.detectar_eje_filas(filas)


_MSG_DESCONOCIDO = (
    "No reconozco este archivo como un export de 'Control de Salud Mental'.\n\n"
    "No encontré las firmas ni del formato IRIS ni del Administrativo.\n\n"
    "Asegúrate de descargarlo desde IRIS o desde el Reporte Administrativo de "
    "RAYEN, y de no haberlo modificado (no borres filas ni columnas del export)."
)


def validar_iris(ws):
    """Acepta el export IRIS. Si es el Administrativo, avisa que cambie el
    selector de formato. Si no es ninguno, 'desconocido'."""
    fmt = detectar_formato(ws)
    if fmt == "iris":
        return
    if fmt == "administrativo":
        raise ArchivoInvalido(
            "administrativo",
            "Elegiste el formato IRIS, pero este archivo parece el REPORTE "
            "ADMINISTRATIVO de RAYEN.\n\n"
            "Cambia el selector de formato a «Administrativo», o descarga el "
            "export de IRIS (Formularios RAYEN -> 'Control de Salud Mental').")
    raise ArchivoInvalido("desconocido", _MSG_DESCONOCIDO)


def validar_admin(ws):
    """Acepta el Reporte Administrativo. Si es el IRIS, avisa que cambie el
    selector. Si no es ninguno, 'desconocido'."""
    fmt = detectar_formato(ws)
    if fmt == "administrativo":
        return
    if fmt == "iris":
        raise ArchivoInvalido(
            "iris",
            "Elegiste el formato Administrativo, pero este archivo parece el "
            "export de IRIS.\n\n"
            "Cambia el selector de formato a «IRIS» (es el recomendado: trae "
            "todas las columnas).")
    raise ArchivoInvalido("desconocido", _MSG_DESCONOCIDO)


# -- PERFILES DE FORMATO -----------------------------------------------
_DISCLAIMER_ADMIN = (
    "Formato ADMINISTRATIVO: esta herramienta fue hecha para IRIS.\n"
    "Funciona, pero OJO:\n"
    "  • Las columnas Pueblos Originarios, SENAME, Proteccion Niñez, Migrante y\n"
    "    Trans NO son calculables desde este export -> saldrán VACÍAS.\n"
    "  • La edad se toma de 'Edad de registro formulario' (formato en años).\n"
    "    y no de la edad real del Usuario que se informa por fecha de nacimiento.\n"
    "Revisa los resultados antes de tabular."
)

PERFIL_IRIS = {
    "id": "iris",
    "nombre": "IRIS · Formularios Clinicos Control de Salud Mental  (recomendado)",
    "ancla": formatos.ANCLA_IRIS,
    "validar": validar_iris,
    "disclaimer": "",
}
PERFIL_ADMIN = {
    "id": "administrativo",
    "nombre": "RAYEN · Reporte Administrativo",
    "ancla": formatos.ANCLA_ADMIN,
    "validar": validar_admin,
    "disclaimer": _DISCLAIMER_ADMIN,
}
PERFILES = [PERFIL_IRIS, PERFIL_ADMIN]


def perfil_por_id(perfil_id):
    for p in PERFILES:
        if p["id"] == perfil_id:
            return p
    return None


# -- Apertura + preparación de columnas --------------------------------
def abrir_validado(entrada, perfil):
    """Carga el workbook, toma la hoja de trabajo y valida contra el `perfil`.
    Devuelve (wb, ws). Levanta ImportError si falta openpyxl, ArchivoInvalido si
    el formato no corresponde al perfil elegido."""
    if not OPENPYXL_OK:
        raise ImportError(
            "Falta la librería 'openpyxl'. Si corres el .py suelto, instálala con:\n"
            "    pip install openpyxl\n"
            f"(detalle: {OPENPYXL_ERR})"
        )
    verificar_hoja_unica(entrada)   # rechaza exports modificados (datos en >1 hoja)
    wb = openpyxl.load_workbook(entrada)
    ws = wb[HOJA] if HOJA else wb.active
    perfil["validar"](ws)   # portón: rechaza archivos que no son el formato elegido
    return wb, ws


def _preparar(ws, perfil, log):
    """Ubica encabezado (según el perfil) y detecta las columnas compartidas
    (RUT/edad/sexo/género + demografía). Devuelve un dict de contexto."""
    header_idx = encontrar_fila_encabezado(ws, perfil["ancla"], MAX_FILAS_BUSQUEDA_HEADER)
    log(f"[corte] perfil={perfil['id']} | encabezado en fila {header_idx} "
        f"(la hoja original NO se modifica)")
    # Fail loud sobre la FUENTE (CLAUDE.md regla 2): un export con solo el encabezado
    # daria 0 eventos con cara de resultado legitimo (un mes sin ingresos SI existe,
    # un archivo sin filas no). La guarda del mes vacio de mas abajo no cubre este
    # caso cuando se procesa el 'Archivo completo' (mes=None).
    exigir_filas_ws(ws, header_idx, "el formulario 'Control de Salud Mental'")

    ncols = ws.max_column
    headers = [ws.cell(row=header_idx, column=c).value for c in range(1, ncols + 1)]
    headers_norm = [norm(h) for h in headers]
    verificar_formulario_sm(headers)   # por CONTENIDO: un cuestionario no pasa (regla 5)
    num2col = {num_pregunta(h): i for i, h in enumerate(headers) if num_pregunta(h) is not None}

    # RUT/edad/sexo: se aceptan los nombres de AMBOS formatos (robusto ante mala elección)
    rut_col, edad_col, sexo_col = formatos.resolver_identidad(headers_norm)
    if edad_col is None:
        # Fail loud (CLAUDE.md regla 2), nunca una columna por POSICION: el fallback
        # viejo a la columna 11 leia 'Convenio' en el Administrativo. Sin edad, las
        # bandas etarias del A05 saldrian vacias (o con numeros de otra columna).
        raise ArchivoInvalido(
            "sin_columnas",
            "No encuentro la columna de EDAD del formulario ('AÑO APLICACIÓN FORMULARIO' "
            "en IRIS, 'Edad de registro formulario' en el Administrativo).\n\n"
            "Carga el export tal como sale de RAYEN/IRIS, sin renombrar ni borrar columnas.")
    log(f"[cols] RUT=col{rut_col} | Edad=col{edad_col} | Sexo=col{sexo_col}")

    demo_cols = {flag: (buscar_col(headers_norm, tokens=[norm(t) for t in src]), regla)
                 for flag, (src, regla) in DEMOGRAFIA.items()}
    genero_col = buscar_col(headers_norm, tokens=[norm(t) for t in COL_GENERO_TOKENS])
    fecha_col = buscar_col(headers_norm, tokens=["FECHA", "FORMULARIO"])   # mes: FECHA FORMULARIO (IRIS y Admin)
    faltantes = [f for f, (c, _) in demo_cols.items() if not c]
    log("[demo] " + " ".join(f"{f}=col{c}" for f, (c, _) in demo_cols.items()) +
        f" Trans(Genero)=col{genero_col}")
    if faltantes:
        log(f"[demo] columnas AUSENTES en este formato (saldrán vacías): {', '.join(faltantes)}")

    return {
        "header_idx": header_idx, "ncols": ncols, "headers": headers,
        "headers_norm": headers_norm, "num2col": num2col,
        "rut_col": rut_col, "edad_col": edad_col, "sexo_col": sexo_col,
        "genero_col": genero_col, "demo_cols": demo_cols, "fecha_col": fecha_col,
    }


# -- MOTOR DE MARCADO (compartido egresos/ingresos, agnóstico al formato) --
def marcar_eventos(wb, ws, perfil, *, busquedas, tipo_label, orden_tipos, hoja_salida,
                   tipo_col_header, avisar_sin_subtipo=frozenset(), etiqueta="evento",
                   mes=None, log=print):
    """Recorre las filas, detecta eventos por token de ESTADO (`busquedas`), les
    agrega patología + subtipo + demografía y escribe la hoja `hoja_salida`
    (formato largo: 1 fila por evento). NO guarda el workbook.

    `perfil` fija la ubicación de encabezado/columnas (formato IRIS o admin).
    `mes` = (año, mes) filtra los formularios por FECHA FORMULARIO a ese mes; None
    procesa el archivo completo. Si se pide un mes sin ningún formulario en el
    archivo, levanta ArchivoInvalido (fail loud, no cuenta silenciosa en 0).
    Devuelve {'total','por_tipo','falta_subtipo','hoja'}.
    """
    ctx = _preparar(ws, perfil, log)
    headers = ctx["headers"]; ncols = ctx["ncols"]; num2col = ctx["num2col"]
    header_idx = ctx["header_idx"]
    rut_col = ctx["rut_col"]; edad_col = ctx["edad_col"]; sexo_col = ctx["sexo_col"]
    genero_col = ctx["genero_col"]; demo_cols = ctx["demo_cols"]; fecha_col = ctx["fecha_col"]

    mes_activo = mes is not None
    if mes_activo and not fecha_col:
        raise ArchivoInvalido(
            "sin_fecha",
            "Pediste filtrar por un mes, pero no encuentro la columna «FECHA "
            "FORMULARIO» en este export.\n\nCarga el archivo tal como lo descargas "
            "de RAYEN/IRIS (sin borrar columnas), o procesa el archivo completo.")
    if mes_activo:
        log(f"[mes] filtrando por FECHA FORMULARIO = {mes[1]:02d}/{mes[0]}")

    busq = {k: [norm(t) for t in v] for k, v in busquedas.items()}
    estado_idx = [c0 for c0 in range(ncols) if es_estado(headers[c0])]   # fijo: precomputado
    eventos = []
    filas_en_mes = 0        # formularios que caen en el mes pedido
    filas_con_rut = 0       # formularios con RUT (los que se miran por fecha)
    filas_fecha_mala = 0    # formularios con RUT pero fecha ilegible (se excluyen)
    solo_fem_anulados = {}  # flag -> nº de formularios donde se marcó en un no-femenino

    for r in range(header_idx + 1, ws.max_row + 1):
        fila = [ws.cell(row=r, column=c).value for c in range(1, ncols + 1)]
        fila_n = [norm(v) for v in fila]
        rut  = fila[rut_col - 1]  if rut_col  else ""
        if mes_activo:
            if not str(rut or "").strip():
                continue   # fila vacía de relleno: no cuenta
            filas_con_rut += 1
            ym = mes_de_celda(fila[fecha_col - 1])
            if ym is None:
                filas_fecha_mala += 1
                continue
            if ym != mes:
                continue
            filas_en_mes += 1
        edad = edad_anios(fila[edad_col - 1]) if edad_col else None
        sexo = fila[sexo_col - 1] if sexo_col else ""
        demo = {flag: (flag_demo(fila[c - 1], regla) if c else "")
                for flag, (c, regla) in demo_cols.items()}
        if not _mujer(sexo):   # flags solo-mujeres: anular y contar (ver DEMOGRAFIA_SOLO_FEMENINO)
            for flag in DEMOGRAFIA_SOLO_FEMENINO:
                if demo.get(flag):
                    demo[flag] = ""
                    solo_fem_anulados[flag] = solo_fem_anulados.get(flag, 0) + 1
        trans = ""
        if genero_col:
            g = fila[genero_col - 1]
            if trans_de(sexo, g):   # implícita: se deja el sexo a la vista para auditar
                trans = str(g) if "TRANS" in norm(g) else f"{g} (sexo {sexo})"

        for k, toks in busq.items():
            for c0 in estado_idx:
                if not all(t in fila_n[c0] for t in toks):
                    continue
                d = encontrar_diagnostico(headers, c0)
                diag_num = num_pregunta(headers[d])
                if diag_num in EXCLUIR_PATOLOGIA:
                    continue   # epilepsia / programas -> no van al A05 SM
                if diag_num in REMAP_DIAGNOSTICO:
                    pat, sub = REMAP_DIAGNOSTICO[diag_num]
                else:
                    pat = (limpiar_patologia(headers[d]) if LIMPIAR_NOMBRE_PATOLOGIA
                           else str(headers[d]))
                    sub_num = DIAGNOSTICOS_CON_SUBTIPO.get(diag_num)
                    sub_col0 = num2col.get(sub_num) if sub_num else None
                    sub_val = fila[sub_col0] if sub_col0 is not None else ""
                    sub = limpiar_subtipo(sub_val, headers[sub_col0] if sub_col0 is not None else "")
                falta_sub = ""
                if (k in avisar_sin_subtipo and diag_num in DIAGNOSTICOS_CON_SUBTIPO
                        and not str(sub).strip()):
                    falta_sub = "SI"
                ev = {"rut": rut, "edad": edad, "sexo": sexo, "tipo": k,
                      "pat": pat, "sub": sub, "falta_sub": falta_sub,
                      "trans": trans, "fila": r}
                ev.update(demo)
                eventos.append(ev)

    for flag, n in sorted(solo_fem_anulados.items()):
        log(f"[demo] AVISO: «{flag}» venía marcado en {n} formulario(s) de sexo NO "
            f"femenino -> se ANULA (por definición no cuenta). Corregir la ficha en "
            f"RAYEN. Ojo: el filtro es por SEXO, no por género (transmasculino sí cuenta).")

    if mes_activo:
        if filas_fecha_mala:
            log(f"[mes] AVISO: {filas_fecha_mala} formulario(s) con fecha ilegible "
                f"quedaron FUERA del filtro (revisa la columna FECHA FORMULARIO).")
        if filas_con_rut and filas_fecha_mala == filas_con_rut:
            # Ninguna fecha legible: NO es "mes equivocado", y el consejo de abajo
            # ("elige Archivo completo") procesaria el año entero como si fuera el mes.
            # Mismo criterio que rem_utils.filtrar_mes.
            raise ArchivoInvalido(
                "sin_fecha",
                f"Ninguno de los {filas_con_rut} formulario(s) tiene una FECHA FORMULARIO "
                f"legible, así que no se puede saber cuáles son de {mes[1]:02d}/{mes[0]}.\n\n"
                "Revisa que sea el export correcto y que esté SIN modificar (una columna de "
                "fecha reformateada a mano rompe la lectura). NO lo proceses como «Archivo "
                "completo»: contaría todos los formularios del archivo como si fueran del mes.")
        if filas_en_mes == 0:
            raise ArchivoInvalido(
                "mes_vacio",
                f"No hay formularios de {mes[1]:02d}/{mes[0]} en este archivo.\n\n"
                "Revisa el mes/año elegido, o que el export cubra ese período. "
                "Si querías todo, elige «Archivo completo».")
        log(f"[mes] {filas_en_mes} formulario(s) en {mes[1]:02d}/{mes[0]}")

    # -- hoja nueva (la original intacta) --
    if hoja_salida in wb.sheetnames:
        del wb[hoja_salida]
    ws2 = wb.create_sheet(hoja_salida)
    demo_keys = list(DEMOGRAFIA.keys())
    cols = (["RUT", "Edad_Formulario", "Sexo", tipo_col_header, "Patologia", "Subtipo",
             "Falta_Subtipo"] + demo_keys + ["Trans", "Fila_Origen"])
    ws2.append(cols)
    eventos.sort(key=lambda e: (orden_tipos.get(e["tipo"], 9), str(e["pat"]), str(e["sub"])))
    for e in eventos:
        fila_out = [e["rut"], e["edad"], e["sexo"], tipo_label.get(e["tipo"], e["tipo"]),
                    e["pat"], e["sub"], e["falta_sub"]]
        fila_out += [e.get(fk, "") for fk in demo_keys]
        fila_out += [e["trans"], e["fila"]]
        ws2.append(fila_out)

    # presentación amigable
    from openpyxl.styles import Font
    for cell in ws2[1]:
        cell.font = Font(bold=True)
    ws2.freeze_panes = "A2"
    if ws2.max_row >= 1:
        ws2.auto_filter.ref = ws2.dimensions
    from openpyxl.utils import get_column_letter
    anchos = ANCHOS_BASE + [ANCHO_DEMO] * len(demo_keys) + ANCHOS_COLA
    for i, w in enumerate(anchos, 1):
        ws2.column_dimensions[get_column_letter(i)].width = w

    log(f"[ok] hoja '{hoja_salida}' escrita")

    n = {}
    for e in eventos:
        n[e["tipo"]] = n.get(e["tipo"], 0) + 1
    n_falta = sum(1 for e in eventos if e["falta_sub"] == "SI")
    log(f"[resumen] {etiqueta}s: {len(eventos)}")
    if avisar_sin_subtipo:
        log(f"          sin subtipo (debiendo tenerlo): {n_falta}")
    for k in busquedas:
        log(f"          {tipo_label.get(k, k)}: {n.get(k, 0)}")

    return {
        "total": len(eventos),
        "por_tipo": {tipo_label.get(k, k): n.get(k, 0) for k in busquedas},
        "falta_subtipo": n_falta,
        "hoja": hoja_salida,
    }
