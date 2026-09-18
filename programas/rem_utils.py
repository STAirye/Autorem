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
rem_utils.py — utilidades comunes para los módulos del REM (RAYEN/IRIS).

Base compartida por todas las herramientas del proyecto autoREM. NO contiene
lógica de ninguna sección específica del REM; cada módulo de tarea
(modulos/rem_<pestaña>_<casilla>_<descriptor>.py) importa de aquí.

Contenido:
  - Guarda de dependencia (openpyxl) y excepción común (ArchivoInvalido).
  - Normalización y parsing de celdas: norm, to_year, solo_entero.
  - Búsqueda de columnas y numeración de preguntas RAYEN: buscar_col, num_pregunta.
  - Localización de la fila de encabezado (salta banner + filtros): encontrar_fila_encabezado.
  - Utilidad de SO: abrir_carpeta.
"""

import re
import sys
from pathlib import Path   # reexport de conveniencia para los módulos

# -- Versión del proyecto (fuente única de verdad) --
# Convención X.Y.Z (ver CLAUDE.md §9):
#   X = arquitectura grande o plantillas REM de un año nuevo · Y = módulo/reporte nuevo
#   · Z = corrección. Cada .py lleva en su header la versión de SU último cambio.
VERSION = "1.9.17"

# openpyxl es la única dependencia externa real. En el .exe va empaquetado;
# corriendo como .py suelto puede faltar -> los módulos avisan con instrucciones.
try:
    import openpyxl
    OPENPYXL_OK = True
    OPENPYXL_ERR = ""
except ImportError as _e:
    openpyxl = None
    OPENPYXL_OK = False
    OPENPYXL_ERR = str(_e)


class ArchivoInvalido(Exception):
    """El archivo no es el export que el módulo esperaba.

    `categoria` la define cada módulo según sus propios formatos (por ejemplo,
    el A05 usa 'administrativo' | 'desconocido'). El mensaje es para el usuario.
    """
    def __init__(self, categoria, mensaje):
        self.categoria = categoria
        super().__init__(mensaje)


# -- Normalización y parsing de celdas ---------------------------------
def norm(v):
    """Texto en MAYÚSCULA, sin tildes/ñ, con espacios colapsados. '' si es None/NaN."""
    if v is None or v != v: return ""   # v != v capta NaN (float) -> '' (celda vacía)
    s = str(v).upper().strip()
    for a, b in zip("ÁÉÍÓÚÜÑ", "AEIOUUN"): s = s.replace(a, b)
    return re.sub(r"\s+", " ", s)


def to_year(v):
    """Primeros 4 dígitos de la celda como int (año). None si no hay dígitos."""
    if v is None: return None
    d = re.sub(r"\D", "", str(v))
    return int(d[:4]) if d else None


def solo_entero(v):
    """Primer entero que aparezca en la celda. None si no hay ninguno."""
    if v is None: return None
    m = re.search(r"\d+", str(v))
    return int(m.group()) if m else None


def edad_anios(v):
    """Edad en AÑOS (int) desde la celda. RAYEN a veces la trae pelada (IRIS:
    'AÑO APLICACIÓN FORMULARIO' = número) y a veces como texto (Administrativo:
    '99 años 12 meses 31 días'). Menor de 1 año (solo meses/días) -> 0. None si
    no hay dato. Genérica: sirve a cualquier export RAYEN."""
    if v is None:
        return None
    n = norm(v)                       # '99 ANOS 12 MESES 31 DIAS'
    m = re.search(r"(\d+)\s*ANOS?", n)
    if m:
        return int(m.group(1))
    if "MES" in n or "DIA" in n:      # menor de 1 año expresado en meses/días
        return 0
    return solo_entero(v)


# -- Búsqueda de columnas / numeración de preguntas RAYEN --------------
def buscar_col(headers_norm, tokens=None, exacto=None):
    """Índice 1-based de la 1ª columna cuyo header (ya normalizado) contiene
    TODOS los `tokens`, o coincide exactamente con `exacto`. None si no hay."""
    for i, h in enumerate(headers_norm, 1):
        if exacto is not None and h == norm(exacto): return i
        if tokens and all(t in h for t in tokens): return i
    return None


def num_pregunta(header):
    """Número 'N.-' con que RAYEN antepone cada pregunta ('18.- ¿...?' -> 18)."""
    m = re.match(r"\s*(\d+)\s*\.\-", str(header))
    return int(m.group(1)) if m else None


# -- Localización de la fila de encabezado (banner + filtros arriba) ----
def encontrar_fila_encabezado(ws, ancla, usar_blanco_en_a=True,
                              n_hardcode=16, max_filas=60):
    """Ubica la fila del encabezado real saltando el banner y los filtros que
    RAYEN pone arriba. Cascada de detección:
      1. Fila que contiene TODOS los tokens de `ancla` (match por substring).
      2. Si `usar_blanco_en_a`: la fila siguiente a la 1ª con la columna A vacía.
      3. Fallback: `n_hardcode` (+1).
    Devuelve (fila_encabezado_1based, modo)."""
    tope = min(ws.max_row, max_filas)
    ancla_n = [norm(t) for t in ancla]
    for r in range(1, tope + 1):
        vals = [norm(c.value) for c in ws[r]]
        if all(any(tok in v for v in vals) for tok in ancla_n):
            return r, "ancla"
    if usar_blanco_en_a:
        for r in range(1, tope + 1):
            if norm(ws.cell(row=r, column=1).value) == "":
                return r + 1, "blanco_en_A"
    return n_hardcode + 1, "hardcode"


# -- Lectura + clasificación de reportes (compartido; usado por módulos pandas) --
def abrir_xlsx_ro(entrada):
    """`load_workbook(read_only=True, data_only=True)` con la <dimension> de CADA
    hoja descartada. TODA lectura read_only del proyecto pasa por aca.

    POR QUE (sep-2026): en modo read_only openpyxl ACOTA `iter_rows` a la
    <dimension> que declara el propio .xlsx (`max_row`/`max_column` salen de ahi;
    ver `ReadOnlyWorksheet._cells_by_row`). Si esa etiqueta viene rota -- p.ej.
    `A1:D5` en una hoja de 10 filas, tipico de exports copy-paste / de BD --, las
    filas y columnas de fuera se pierden SIN ningun error: un ADA truncado cuenta de
    menos con cara de resultado legitimo. `reset_dimensions()` hace que se lea lo que
    el archivo trae de verdad (es lo mismo que hace pandas.read_excel por dentro).
    Quien cierra el workbook es el llamador (`wb.close()`)."""
    wb = openpyxl.load_workbook(entrada, data_only=True, read_only=True)
    for ws in wb.worksheets:
        ws.reset_dimensions()
    return wb


def filas_hoja(ws, max_filas=None):
    """Filas (tuplas de VALORES) de una hoja abierta con `abrir_xlsx_ro`, todas del
    MISMO ancho. Sin <dimension> openpyxl entrega cada fila hasta su ultima celda
    escrita (filas desparejas); se rellenan con None para que un indice de columna
    valga en todas, como antes. `max_filas` corta temprano (encabezado, deteccion)."""
    from itertools import islice
    filas = list(islice(ws.iter_rows(values_only=True), max_filas))
    ancho = max((len(f) for f in filas), default=0)
    return [tuple(f) + (None,) * (ancho - len(f)) for f in filas]


def leer_xlsx(entrada, ancla=None, max_scan=40):
    """Lee un .xlsx con openpyxl y devuelve (headers, filas_de_datos). ROBUSTO a
    la 'dimension' rota o ausente de los exports copy-paste / de BD: lee con
    `abrir_xlsx_ro`, que la descarta (hasta 1.9.17 NO lo era: la respetaba y
    truncaba en silencio -- ver ahi). `ancla` = nombres de columna que deben
    estar TODOS en la fila de encabezado; si es None, toma la 1ª fila con >3
    celdas llenas."""
    wb = abrir_xlsx_ro(entrada)
    try:
        filas = filas_hoja(wb.active)
    finally:
        wb.close()
    if not filas:   # hoja SIN ninguna fila (ni encabezado): filas[hi] seria IndexError
        raise ArchivoInvalido(
            "sin_datos",
            "La hoja del archivo esta completamente vacia (ni siquiera trae el "
            "encabezado).\n\nVuelve a descargar el export desde RAYEN/IRIS.")
    if ancla:
        want = {norm(a) for a in ancla}
        hi = next((i for i, r in enumerate(filas[:max_scan]) if want <= {norm(v) for v in r}), 0)
    else:
        hi = next((i for i, r in enumerate(filas[:max_scan]) if sum(v not in (None, "") for v in r) > 3), 0)
    return list(filas[hi]), filas[hi + 1:]


def exigir_filas(filas, fuente):
    """Fail loud sobre la FUENTE (CLAUDE.md regla 2): un export con solo el
    encabezado (0 filas de datos) levanta ArchivoInvalido('sin_datos') aca, en vez de
    dar un 0 plausible o reventar mas abajo con un error criptico."""
    if not any(any(v not in (None, "") for v in f) for f in filas):
        raise ArchivoInvalido(
            "sin_datos",
            f"{fuente[:1].upper()}{fuente[1:]} no trae ninguna fila de datos.\n\n"
            "Revisa que sea el export completo (no solo el encabezado) y que este sin modificar.")


def exigir_filas_ws(ws, header_idx, fuente):
    """Gemelo de `exigir_filas` para el mundo openpyxl-worksheet (A05, A03,
    estamentos): 0 filas de datos bajo el encabezado -> ArchivoInvalido('sin_datos').
    `header_idx` es 1-based (la fila del encabezado)."""
    if not any(any(v not in (None, "") for v in fila)
               for fila in ws.iter_rows(min_row=header_idx + 1, values_only=True)):
        raise ArchivoInvalido(
            "sin_datos",
            f"{fuente[:1].upper()}{fuente[1:]} no trae ninguna fila de datos bajo el "
            "encabezado.\n\nRevisa que sea el export completo (no solo el encabezado) "
            "y que este sin modificar.")


def verificar_hoja_unica(entrada):
    """Guarda de integridad de los exports RAYEN/IRIS: SIEMPRE bajan UNA hoja con
    datos + 2 vacías. Si hay datos en más de una hoja, el archivo fue MODIFICADO
    (típicamente se le agregó una tabla dinámica) y sus resultados no son confiables
    -> levanta ArchivoInvalido. Robusta a la 'dimension' rota igual que leer_xlsx
    (`abrir_xlsx_ro`): con la <dimension> respetada, una hoja extra con datos FUERA
    de lo que declara la etiqueta pasaba por vacia."""
    wb = abrir_xlsx_ro(entrada)
    try:   # read_only deja el .xlsx ABIERTO hasta close(): sin finally, un export a
        # medio sincronizar que revienta a mitad de la lectura quedaba bloqueado
        # (OneDrive no lo termina de bajar, el usuario no lo puede reemplazar).
        con_datos = [ws.title for ws in wb.worksheets
                     if any(any(v not in (None, "") for v in row)
                            for row in ws.iter_rows(values_only=True))]
    finally:
        wb.close()
    if len(con_datos) > 1:
        raise ArchivoInvalido(
            "modificado",
            f"El archivo trae datos en {len(con_datos)} hojas ({', '.join(con_datos)}). "
            "RAYEN/IRIS siempre baja UNA hoja con datos + 2 vacías, así que esto significa "
            "que el export fue MODIFICADO (¿le agregaste una tabla dinámica?). Vuelve a "
            "descargarlo SIN tocar desde RAYEN/IRIS y cárgalo tal cual.")


def resolver_columnas(headers, mapa):
    """Mapea nombres canónicos -> columnas reales por nombre SEMÁNTICO. `mapa` =
    {canonico: opcion | [opcion, ...]} con opcion = ('exact','NOMBRE') |
    ('subs',['TOK1','TOK2']). Una LISTA de opciones se prueba EN ORDEN (para
    formatos alternativos, p.ej. IRIS vs Admin). Match normalizado (tildes,
    mayúsculas, renumeración 'N.- '). Devuelve {canonico: nombre_columna | None}."""
    hn = [(c, norm(c)) for c in headers]

    def _match(modo, obj):
        if modo == "exact":
            t = norm(obj)
            return next((c for c, n in hn if n == t), None)
        toks = [norm(t) for t in obj]
        return next((c for c, n in hn if all(t in n for t in toks)), None)

    out = {}
    for canon, spec in mapa.items():
        opciones = spec if isinstance(spec, list) else [spec]
        out[canon] = next((c for modo, obj in opciones if (c := _match(modo, obj)) is not None), None)
    return out


# Mapa de columnas del reporte de ATENCIONES, compartido por los módulos que lo
# consumen (respiratorio A23, y a futuro cualquier otro programa). Alternativas
# IRIS | Admin ('Monitoreo de Actividades').
# El Monitoreo admin queda INCOMPLETO (IRIS es la fuente plena):
#   (a) DEMOGRAFÍA: no trae nacionalidad/pueblo/fecha nac/nombres -> origen-migrante
#       y nombre completo salen vacíos; edad desde 'AÑOS'.
#   (b) DIAGNÓSTICO EN TEXTO, sin código ICD -> los indicadores que matchean por
#       código (Ira Alta 'j0', Bronquitis 'J20', EPOC Exacerbado 'J44.1') salen 0.
#       Los de texto (Neumonía/Influenza/Coqueluche) y los de ACTIVIDAD (KTR,
#       espirometría, controles…) sí cuadran (verificado vs IRIS, jul-2026).
#   (c) Estructura PADRE-HIJO -> forward-fill de cabecera en cargar_atenciones.
# Nombre EXACTO de la columna correlativa del Monitoreo. Vive fuera del mapa porque
# `cargar_canonico` necesita reconocerla para namespacearla (ver alla).
ATENID_CORRELATIVO = "N°"

MAPA_ATENCIONES = {
    "RUN":     [("subs", ["NUMERO", "IDENTIFICACION"]), ("exact", "RUN")],
    # IRIS: 'ATEN ID', global y unico. Monitoreo: 'N°', un correlativo 1..N que
    # agrupa las filas de una misma atencion (verificado: 2625 atenciones en 6590
    # filas, 0 con cabecera inconsistente). SIRVE para contar, pero REINICIA EN 1 en
    # cada export -> cargar_canonico lo namespacea por archivo (ver alla). Sin eso,
    # concatenar dos Monitoreos fusiona atenciones distintas y subcuenta EN SILENCIO.
    "ATENID":  [("subs", ["ATEN", "ID"]), ("subs", ["ATENCION", "ID"]), ("exact", "N°")],
    "FECHA":   [("exact", "FECHA ATENCION"), ("exact", "FECHA CONSULTA")],
    "ACT":     [("exact", "ACTIVIDADES"), ("subs", ["ACTIVIDAD", "PROCEDIMIENTO"])],
    "DIAG":    [("exact", "DIAGNOSTICOS"), ("exact", "DIAGNOSTICO")],
    "INSTR":   ("exact", "INSTRUMENTO"),
    # NOMBRE del funcionario que atendió. IRIS lo llama 'PROFESIONAL ATENCION' y el
    # Monitoreo 'FUNCIONARIO': el mismo dato con otro nombre.
    "PROF":    [("subs", ["PROFESIONAL", "ATENCION"]), ("exact", "FUNCIONARIO")],
    "TIPO":    ("subs", ["TIPO", "ATENCION"]),          # 'TIPO ATENCION' | 'TIPO DE ATENCION'
    "SEXO":    ("exact", "SEXO"),
    "SECTOR":  ("exact", "SECTOR"),
    "NACION":  ("exact", "NACIONALIDAD"),               # solo IRIS
    "EMIG":    [("subs", ["ES", "IMIGRANTE"]), ("subs", ["ES", "INMIGRANTE"])],  # flag migrante, IRIS
    "ALERTAS": ("subs", ["ALERTAS", "ADMINISTRATIVAS"]),  # SENAME/Mejor Niñez/Cuidador…, IRIS
    "FORMCLIN": ("subs", ["FORMULARIOS", "CLINICOS"]),  # para detectar gestante, IRIS
    "PUEBLO":  ("subs", ["PUEBLO", "ORIGINARIO"]),      # solo IRIS
    "FNAC":    ("subs", ["FECHA", "NACIMIENTO"]),       # solo IRIS
    "NOMBRES": ("exact", "NOMBRES"),                    # solo IRIS
    "APAT":    ("subs", ["APELLIDO", "PATERNO"]),       # solo IRIS
    "AMAT":    ("subs", ["APELLIDO", "MATERNO"]),       # solo IRIS
    "ANOS":    ("exact", "AÑOS"),                        # edad a la DESCARGA
    # Edad a la ATENCIÓN — la que pide el REM para las bandas etarias.
    # TRAMPA: el MISMO nombre de columna significa cosas DISTINTAS según el reporte.
    #   IRIS      -> 'AÑOS' es edad a la DESCARGA; la buena es 'AÑOS ATENCION'.
    #   Monitoreo -> NO tiene 'AÑOS ATENCION', y su 'AÑOS' YA es a la atención
    #                (confirmado por el autor contra enero-2026; viene como triple
    #                numérico AÑOS/MESES/DÍAS en la fila-padre de cada atención).
    # Por eso el orden IMPORTA: 'AÑOS ATENCION' primero, y sólo si no está se cae al
    # 'AÑOS' pelado. En IRIS la 1ª opción siempre gana, así que nunca se toma la
    # edad-a-la-descarga por error. Si RAYEN renombrara 'AÑOS ATENCION' en IRIS, ese
    # fallback pasaría a dar edad a la descarga EN SILENCIO -> lo cubre un test que
    # exige que en IRIS esta clave resuelva a una columna que diga ATENCION.
    "ANOS_AT": [("subs", ["AÑOS", "ATENCION"]), ("subs", ["ANOS", "ATENCION"]),
                ("exact", "AÑOS")],
}


def cargar_canonico(entrada, ancla, resolver, requeridas=None, solo_iris=None,
                    log=print, espera=None):
    """Lee UNO o VARIOS .xlsx (los reportes acumulativos necesitan varios años) y
    arma el DataFrame canónico concatenado. `resolver(headers) -> {canon: columna}`.
    `requeridas` = claves canónicas que DEBEN resolverse en CADA archivo; si a alguno
    le faltan, levanta ArchivoInvalido NOMBRANDO ese archivo (los módulos multi-archivo
    así saben CUÁL falló). Devuelve (df, col_del_primero).

    `solo_iris` = claves que SOLO trae el export IRIS pleno (ej.
    `formatos.SOLO_IRIS_ATENCIONES`). Si se pasan, clasifica la FUENTE y deja el
    resultado en `df.attrs['fuente'] = (estado, ausentes)`. Con VARIOS archivos se clasifica CADA UNO y gana el PEOR (plena <
    cambiada < parcial); si se mezclan plenos con no-plenos, los no-plenos quedan en
    `df.attrs['fuente_mezcla']` = [nombre, ...] para que el aviso diga cuales (None si
    no hay mezcla). Hasta 1.9.17 se clasificaba solo el PRIMERO: [IRIS, Monitoreo]
    daba 'plena' y banner verde sobre filas sin demografia, [Monitoreo, IRIS] daba
    'parcial' -- el veredicto dependia del orden en que se eligieron, no del contenido.
    Loguea cuando NO es plena. Este es el único cuello de botella de carga del grupo pandas — ADA,
    grupal, NSP y 'Otros y Respi' pasan todos por acá —, así que la fase 2 del eje
    de formatos se engancha en UN solo punto. Ver `formatos.clasificar_fuente`.

    `espera` = 'ada' | 'grupal': si al archivo le faltan columnas Y parece el OTRO
    reporte del par, se levanta un error que dice CUÁL cruce, en vez del genérico
    'no reconozco el archivo'. Ver `formatos.verificar_cruce`."""
    import pandas as pd
    partes, col0, cols_por_archivo = [], None, []
    for e in (entrada if isinstance(entrada, (list, tuple)) else [entrada]):
        nombre = Path(str(e)).name
        try:
            verificar_hoja_unica(e)      # rechaza exports modificados (datos en >1 hoja)
            hdr, filas = leer_xlsx(e, ancla=ancla)
        except ArchivoInvalido as ai:    # p.ej. 'modificado' -> agrega el nombre del archivo
            raise ArchivoInvalido(ai.categoria, f"Archivo «{nombre}»:\n\n{ai}") from ai
        except Exception as ex:          # openpyxl/zip/etc. -> no es un .xlsx legible
            raise ArchivoInvalido(
                "no_legible",
                f"No pude leer el archivo:\n«{nombre}»\n\n{ex}\n\n"
                "¿Es un .xlsx válido (no .xls/.csv/.html) y sin modificar?") from ex
        # Fail loud sobre la FUENTE (CLAUDE.md regla 2) y POR ARCHIVO: con 0 filas
        # las columnas quedan float64 y .str.contains() revienta abajo con un error
        # criptico (o el conteo sale 0 en silencio). Unico cuello de botella del grupo
        # pandas -> cubre ADA, grupal, Inscritos, NSP y 'Otros y Respi'.
        exigir_filas(filas, f"el archivo «{nombre}»")
        col = resolver(hdr)
        if requeridas:
            faltan = [k for k in requeridas if not col.get(k)]
            if faltan:
                # Antes del mensaje generico: si el archivo es claramente el OTRO
                # reporte del par ADA/grupal, decirlo. Solo se consulta cuando ya
                # falla -> cero riesgo de falso positivo sobre un archivo valido.
                if espera:
                    from programas import formatos
                    formatos.verificar_cruce(hdr, espera, nombre)
                raise ArchivoInvalido(
                    "sin_columnas",
                    f"No reconozco el archivo:\n«{nombre}»\n\n"
                    f"No encuentro las columnas: {', '.join(faltan)}.\n\n"
                    "¿Está SIN la fila de encabezado (nombres de columna) o modificado? "
                    "Cárgalo tal como sale de RAYEN/IRIS, sin editar.")
        col0 = col0 or col
        cols_por_archivo.append((nombre, col))
        idx = {c: i for i, c in enumerate(hdr)}
        parte = pd.DataFrame(
            {k: [f[idx[c]] if c is not None and idx[c] < len(f) else None for f in filas]
             for k, c in col.items()})
        # ATENID por CORRELATIVO ('N°' del Monitoreo) reinicia en 1 en cada export:
        # concatenar dos archivos fusionaria atenciones distintas bajo el mismo id y
        # el conteo por-atencion SUBCONTARIA en silencio. Se namespacea con el nombre
        # del archivo. NO se toca el 'ATEN ID' de IRIS, que es global y unico: si el
        # mismo ATEN ID aparece en dos exports que se solapan, tiene que deduplicar.
        if col.get("ATENID") == ATENID_CORRELATIVO and "ATENID" in parte:
            parte["ATENID"] = nombre + "|" + parte["ATENID"].astype(str)
        partes.append(parte)
    d = pd.concat(partes, ignore_index=True) if len(partes) > 1 else partes[0]
    if solo_iris:
        from programas import formatos
        gravedad = {formatos.FUENTE_PLENA: 0, formatos.FUENTE_CAMBIADA: 1,
                    formatos.FUENTE_PARCIAL: 2}
        por_archivo = [(n, *formatos.clasificar_fuente(c, solo_iris))
                       for n, c in cols_por_archivo]
        estado = max((e for _, e, _ in por_archivo), key=gravedad.__getitem__)
        ausentes = list(dict.fromkeys(a for _, _, aus in por_archivo for a in aus))
        no_plenos = [n for n, e, _ in por_archivo if e != formatos.FUENTE_PLENA]
        d.attrs["fuente"] = (estado, ausentes)
        d.attrs["fuente_mezcla"] = (no_plenos if no_plenos and len(no_plenos) < len(por_archivo)
                                    else None)
        if d.attrs["fuente_mezcla"]:
            log(f"[fuente] MEZCLA: {', '.join(no_plenos)} NO es/son el A/D/A de IRIS "
                f"completo, el resto si. Lo de esos archivos cuenta de MENOS en lo que "
                f"dependa de: {', '.join(ausentes)}.")
        if estado == formatos.FUENTE_PARCIAL:
            log(f"[fuente] PARCIAL: el archivo no es el export A/D/A de IRIS (no trae "
                f"ninguna de: {', '.join(ausentes)}). Los indicadores que dependen "
                f"de esas columnas van a salir en 0 o incompletos.")
        elif estado == formatos.FUENTE_CAMBIADA:
            log(f"[fuente] EXPORT CAMBIADO: parece el A/D/A de IRIS pero le faltan columnas "
                f"que antes traia: {', '.join(ausentes)}. O RAYEN cambio el export, "
                f"o el archivo fue editado -> revisar MAPA_ATENCIONES.")
    return d, col0


def fecha_col(serie, log=print, etiqueta="fecha"):
    """to_datetime robusto que AVISA las fechas ilegibles en vez de callarlas.
    Un texto no vacío que no se puede parsear queda NaT y saldría del filtro por
    mes en SILENCIO (subconteo con número plausible); acá se cuenta y se loguea
    (regla fail-loud del proyecto). Devuelve la serie parseada (datetime)."""
    import pandas as pd
    # format="mixed": la columna mezcla datetime YA parseados por openpyxl (celdas con
    # formato fecha) con texto "DD/MM/YYYY" (celdas como texto) -> sin esto pandas
    # avisa "Could not infer format" y cae a dateutil elemento-por-elemento igual,
    # pero con warning. Explícito = mismo resultado, sin el ruido (pandas>=2.0).
    parsed = pd.to_datetime(serie, errors="coerce", dayfirst=True, format="mixed")
    # vacío legítimo = nulo real, o texto en blanco / centinela -> NO es "ilegible".
    vacio = serie.isna() | serie.astype(str).str.strip().isin(
        ("", "nan", "NaN", "NaT", "None", "<NA>"))
    ilegible = parsed.isna() & ~vacio
    n = int(ilegible.sum())
    if n:
        log(f"[fecha] {n} valor(es) de «{etiqueta}» ilegibles -> NaT: quedan "
            f"FUERA del filtro por fecha (revisar el export).")
    return parsed


def cargar_atenciones(entrada, log=print):
    """Export(s) de ATENCIONES (IRIS ó Monitoreo admin) -> DataFrame canónico +
    textos normalizados (act/diag/instr/tipo) + FECHA parseada. Ruta o lista."""
    import pandas as pd
    from programas.formatos import SOLO_IRIS_ATENCIONES
    d, col = cargar_canonico(entrada, None, lambda h: resolver_columnas(h, MAPA_ATENCIONES),
                             requeridas=("RUN", "FECHA", "ACT", "DIAG", "INSTR", "TIPO"),
                             solo_iris=SOLO_IRIS_ATENCIONES, log=log, espera="ada")
    # Monitoreo admin: estructura PADRE-HIJO — una atención se abre en varias filas
    # de actividad, con RUN y datos de cabecera SOLO en la 1ª. Se rellena la cabecera
    # a las filas HIJAS (RUN vacío) para atribuir cada actividad/diagnóstico a su
    # paciente. En IRIS (sin filas hijas) NO se toca nada (evita contaminar campos
    # vacíos legítimos entre pacientes distintos).
    cab = ["RUN", "ATENID", "FECHA", "INSTR", "PROF", "TIPO", "SEXO", "SECTOR", "NACION",
           "EMIG", "ALERTAS", "FORMCLIN", "PUEBLO", "FNAC", "NOMBRES", "APAT",
           "AMAT", "ANOS", "ANOS_AT"]
    child = d["RUN"].replace("", pd.NA).isna()
    if child.any():
        dd = d[cab].replace("", pd.NA)
        d[cab] = dd.where(~child, dd.ffill())
    d["FECHA"] = fecha_col(d["FECHA"], log, "FECHA atención")
    for k in ("ACT", "DIAG", "INSTR", "TIPO"):
        d[k + "_n"] = d[k].map(norm)
    exigir_estamento(d)
    return d


def exigir_estamento(d):
    """Fail loud sobre la FUENTE (CLAUDE.md regla 2): toda atencion con funcionario
    (PROF) trae su estamento (INSTR). RAYEN no puede registrar una atencion sin el
    estamento de quien atendio, asi que una fila asi es un export MODIFICADO (o
    armado a mano), no un dato legitimo.

    POR QUE aca y no en el dialogo de dotacion (sep-2026): el dialogo la mostraba
    como el grupo '(sin estamento)', cuyo 'Omitir estamento' no guardaba nada
    (`dotacion.omitir` descarta la clave vacia) aunque el grupo desaparecia de la
    ventana -- y esa misma fila, aguas abajo, no cae en NINGUNA casilla por
    estamento. Emparcharlo en el dialogo era darle un lugar a algo que no deberia
    existir. `d` = DataFrame canonico con INSTR_n ya calculado."""
    if "PROF" not in d.columns:
        return      # fuente sin funcionario (p.ej. Monitoreo sin esa columna): nada que exigir
    prof = d["PROF"].map(norm)
    sin = d[(prof != "") & (d["INSTR_n"] == "")]
    if len(sin):
        nombres = sorted(set(sin["PROF"].astype(str).str.strip()))
        muestra = ", ".join(nombres[:5]) + (f" y {len(nombres) - 5} mas" if len(nombres) > 5 else "")
        raise ArchivoInvalido(
            "sin_estamento",
            f"{len(sin)} atencion(es) de {len(nombres)} funcionario(s) vienen SIN "
            f"estamento (columna INSTRUMENTO vacia): {muestra}.\n\n"
            "RAYEN siempre registra el estamento de quien atiende, asi que el export "
            "fue MODIFICADO o no es el reporte de Atenciones. Vuelve a descargarlo desde "
            "RAYEN/IRIS y cargalo tal cual.")


# -- Maestro de Actividades (catálogo RAYEN: actividad <-> estamento <-> casilla REM) --
# Referencia transversal (no solo SM): mapea cada actividad a su NUM REM oficial. Una
# fila por (actividad × instrumento). Banner en fila 1 -> ancla en la fila de headers.
# Se actualiza ~semestralmente. Usos: clasificar (¿tributa y a qué casilla?), validar
# la clasificación RAYEN vs la nuestra (el referente técnico arbitra), y chequear que
# cada estamento tenga las actividades que el exe reporta.
MAPA_MAESTRO = {
    "ACT":     ("exact", "ACTIVIDAD"),
    "INSTR":   [("subs", ["INSTRUMENTO", "ASOCIADO"]), ("exact", "INSTRUMENTO")],
    "NUMREM":  ("subs", ["NUM", "REM"]),
    "SECCION": ("subs", ["NUM", "SECCION"]),
    "REM":     ("exact", "REM"),
}


def cargar_maestro(entrada):
    """Lee el 'Maestro de Actividades' -> DataFrame (ACT/INSTR/NUMREM/SECCION/REM) +
    ACT_n y NUMREM_n normalizados. Una fila por (actividad × instrumento). Acepta el
    Maestro COMPLETO (.xlsx, con banner) o el SLIM comprimido (.csv.gz que shippea el
    repo, generado por tools/slim_maestro.py)."""
    import pandas as pd
    ent = str(entrada).lower()
    if ent.endswith((".csv", ".gz", ".csv.gz")):
        raw = pd.read_csv(entrada, dtype=str, keep_default_na=False)   # compresión inferida
        hdr = list(raw.columns)
        col = resolver_columnas(hdr, MAPA_MAESTRO)
        _guard_maestro(col)
        d = pd.DataFrame({k: (raw[c] if c is not None else "") for k, c in col.items()})
    else:
        hdr, filas = leer_xlsx(entrada, ancla=["ACTIVIDAD", "INSTRUMENTO ASOCIADO", "NUM REM"])
        col = resolver_columnas(hdr, MAPA_MAESTRO)
        _guard_maestro(col)
        idx = {c: i for i, c in enumerate(hdr)}
        d = pd.DataFrame({k: [f[idx[c]] if c is not None and idx[c] < len(f) else None
                              for f in filas] for k, c in col.items()})
    d = d[d["ACT"].map(lambda x: x not in (None, ""))].copy()
    if len(d) == 0:
        raise ArchivoInvalido("sin_datos", "El Maestro de Actividades no trae ninguna fila "
                              "de datos. Revisa que sea el archivo completo, sin modificar.")
    d["ACT_n"] = d["ACT"].map(norm)
    d["NUMREM_n"] = d["NUMREM"].map(norm)
    return d


def _guard_maestro(col):
    if not col["ACT"] or not col["NUMREM"]:
        raise ValueError("No reconozco el Maestro de Actividades (faltan 'ACTIVIDAD' "
                         "y/o 'NUM REM'). ¿Es el archivo correcto?")


# -- Grilla de agregación edad×sexo (tablas REM copy-paste; SM · A23 · A03) --
# Forma del template MINSAL: Ambos·Hombres·Mujeres + cada banda etaria × (H/M).
# Bandas inclusive; el último tramo (80,200) = '80 y más'. A04 separa <1 y 1-4;
# A06/A32/A03·D.3 agrupan 0-4. Compartido para no re-implementar en cada módulo.
BANDAS_A04 = [(0, 0), (1, 4), (5, 9), (10, 14), (15, 19), (20, 24), (25, 29),
              (30, 34), (35, 39), (40, 44), (45, 49), (50, 54), (55, 59),
              (60, 64), (65, 69), (70, 74), (75, 79), (80, 200)]
LBL_A04 = ["<1", "1-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34",
           "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69",
           "70-74", "75-79", "80+"]
BANDAS_A06 = [(0, 4)] + BANDAS_A04[2:]
LBL_A06 = ["0-4"] + LBL_A04[2:]


def dv_rut(cuerpo):
    """Digito verificador de un RUT chileno (modulo 11). `cuerpo` = los digitos sin
    DV. Devuelve '0'-'9' o 'K'."""
    suma, mult = 0, 2
    for ch in reversed(str(cuerpo)):
        suma += int(ch) * mult
        mult = 2 if mult == 7 else mult + 1
    resto = 11 - (suma % 11)
    return "0" if resto == 11 else "K" if resto == 10 else str(resto)


def rut_valido(v):
    """True si `v` es un RUT chileno BIEN FORMADO: forma correcta Y digito
    verificador que cuadra (modulo 11). Mas fuerte que validar solo la forma -- un
    numero de pasaporte con pinta de RUT pasa el regex pero casi nunca el DV.

    OJO: valida la ARITMETICA, no la existencia. '11111111-1' cuadra el modulo 11
    pero no es un RUT asignado a nadie. Sirve para descartar identificadores que NO
    son RUT (pasaportes, FONASA), no para verificar la identidad de una persona."""
    n = norm(v).replace(".", "").replace(" ", "")
    cuerpo, sep, dv = n.rpartition("-")
    if not sep or not cuerpo.isdigit() or not (6 <= len(cuerpo) <= 9):
        return False
    return dv == dv_rut(cuerpo)


def _mujer(s):
    """Sexo REGISTRAL femenino. Es el criterio de los flags que el REM define solo
    sobre mujeres (Madre de hijo <5, Gestante): va por SEXO, nunca por GÉNERO, así
    que una persona de sexo femenino y género transmasculino SÍ cuenta."""
    n = norm(s); return ("FEMENIN" in n) or ("MUJER" in n)


def _hombre(s):
    n = norm(s); return ("MASCULIN" in n) or ("HOMBRE" in n)


def _band_idx(edad, bandas):
    import pandas as pd
    if pd.isna(edad):
        return None
    e = int(edad)
    return next((i for i, (lo, hi) in enumerate(bandas) if lo <= e <= hi), None)


def _isum(s):
    """Suma robusta a Series vacías (evita el '' de una object-Series vacía)."""
    return int(s.sum()) if len(s) else 0


def grid(sub, bandas, lbls, con_sexo=True):
    """Fila de conteos en el ORDEN del template: Ambos·Hombres·Mujeres y luego cada
    banda × sexo (o solo total por banda si con_sexo=False). `sub` = DataFrame con
    columnas 'sexo' y 'edad'."""
    hom = sub["sexo"].map(_hombre)
    muj = sub["sexo"].map(_mujer)
    bi = sub["edad"].map(lambda x: _band_idx(x, bandas))
    if con_sexo:
        out = {"Ambos": len(sub), "Hombres": _isum(hom), "Mujeres": _isum(muj)}
        for i, l in enumerate(lbls):
            m = bi.eq(i)
            out[f"{l} H"] = _isum(m & hom)
            out[f"{l} M"] = _isum(m & muj)
    else:
        out = {"Total": len(sub)}
        for i, l in enumerate(lbls):
            out[l] = _isum(bi.eq(i))
    return out


def indice_col(headers_norm, *subs):
    """Índice 0-based de la 1ª columna cuyo header YA normalizado contiene TODAS
    las subcadenas `subs` (se normalizan). None si no hay. Para el mundo leer_xlsx
    (acceso por índice de tupla); resolver_columnas es el equivalente por-nombre."""
    return next((i for i, n in enumerate(headers_norm)
                 if all(norm(s) in n for s in subs)), None)


def mes_anterior(hoy=None):
    """(año, mes) del mes calendario anterior a `hoy` (date; default = hoy real).
    Fuente única del 'mes por defecto' que comparten la GUI y los módulos pandas."""
    from datetime import date
    hoy = hoy or date.today()
    return (hoy.year, hoy.month - 1) if hoy.month > 1 else (hoy.year - 1, 12)


def _rango_mes(mes):
    """(inicio, fin) Timestamp del mes de reporte. mes=(año,mes) o None -> mes
    anterior. Compartido por los módulos pandas (A23, SM Actividades, Trabajo
    Perdido); los cálculos van hacia atrás desde el mes reportado, NO TODAY()."""
    import calendar
    import pandas as pd
    y, m = mes if mes is not None else mes_anterior()
    return pd.Timestamp(y, m, 1), pd.Timestamp(y, m, calendar.monthrange(y, m)[1])


def filtrar_mes(d, ini, fin, fuente, col="FECHA"):
    """Filtra `d` al mes [ini, fin] por `col` y FALLA RUIDOSO si el export no
    cubre ese mes. Punto ÚNICO donde los módulos pandas cumplen la regla del A05
    (CLAUDE.md §3): un mes sin datos es un error del USUARIO — archivo del año
    pasado, o mes mal elegido en el spinbox —, no un .xlsx lleno de ceros con
    pinta de legítimo que alguien copia al SA_26.

    El guardarraíl va sobre la FUENTE, nunca sobre la casilla: que una casilla
    concreta dé 0 con el mes cubierto es LEGÍTIMO (A27 y A32·F2 lo hacen de
    verdad) y no debe fallar. Por eso los filtros que vienen DESPUÉS del mes
    (Asiste=SI del grupal, tipo de atención de la Sección H) se aplican aparte,
    sobre lo que esta función devuelve.

    `fuente` = nombre del reporte para el mensaje ('el ADA', 'el reporte NSP'...).
    """
    dm = d[(d[col] >= ini) & (d[col] <= fin)]
    if len(dm):
        return dm
    if len(d) == 0:
        raise ArchivoInvalido(
            "mes_vacio",
            f"{fuente[:1].upper()}{fuente[1:]} no trae ninguna fila de datos.\n\n"
            "Revisa que sea el export correcto, descargado completo y SIN modificar.")
    if not d[col].notna().any():
        raise ArchivoInvalido(
            "mes_vacio",
            f"En {fuente} ninguna fila tiene una fecha legible, así que no se "
            f"puede saber si cubre {ini:%m/%Y}.\n\n"
            "Revisa que sea el export correcto y que esté SIN modificar "
            "(una columna de fecha reformateada a mano rompe la lectura).")
    raise ArchivoInvalido(
        "mes_vacio",
        f"No hay filas de {ini:%m/%Y} en {fuente}.\n\n"
        f"El archivo cargado cubre {d[col].min():%m/%Y} a {d[col].max():%m/%Y}.\n\n"
        "Revisa el mes/año elegido, o carga el export que cubra ese período.")


def mes_de_celda(v):
    """(año, mes) desde una celda de fecha RAYEN, o None si no se puede parsear.
    Acepta datetime/date (lo que openpyxl entrega en celdas con formato fecha) y
    texto en las DOS formas que usa RAYEN: 'YYYY/MM/DD' (Admin/monitoreo) y
    'DD/MM/YYYY' (formularios clínicos), con '-', '/' o '.' y hora opcional.

    Distingue las dos formas por ESTRUCTURA (año de 4 dígitos adelante = ISO),
    NO por dayfirst a ciegas: 'YYYY/MM/DD' con dayyfirst se lee como el mes
    equivocado en silencio (justo lo que no queremos). Cualquier otra cosa -> None
    (se excluye y se avisa; nunca se adivina un mes plausible pero errado)."""
    if v is None:
        return None
    from datetime import datetime as _dt, date as _date
    if isinstance(v, (_dt, _date)):
        return (v.year, v.month)
    s = str(v).strip()
    if not s:
        return None
    m = re.match(r"^(\d{4})[-/.](\d{1,2})[-/.]\d{1,2}", s)      # YYYY/MM/DD
    if m:
        y, mo = int(m.group(1)), int(m.group(2))
    else:
        m = re.match(r"^\d{1,2}[-/.](\d{1,2})[-/.](\d{4})", s)  # DD/MM/YYYY
        if not m:
            return None
        mo, y = int(m.group(1)), int(m.group(2))
    return (y, mo) if 1 <= mo <= 12 else None


def maestro_rem_map(dfm):
    """{ACT_n -> NUM REM normalizado} desde el Maestro (dedup por actividad; una
    actividad tiene el mismo NUM REM en todas sus filas de instrumento)."""
    return dict(zip(dfm["ACT_n"], dfm["NUMREM_n"]))


# -- Demografía por atención (columnas del REM: SENAME, migrante, pueblos…) --
# Fuente = ADA IRIS (ALERTAS ADMINISTRATIVAS / ES IMIGRANTE / PUEBLO / DIAG / ACT).
# El grupal y el Monitoreo admin NO traen estos campos -> todos los flags quedan
# en False (limitación conocida). Reutilizable por cualquier módulo (A23, SM…).
# Valores de PUEBLO ORIGINARIO que NO cuentan como pertenencia (formato norm()).
# Fuente ÚNICA compartida: la usa marcar_demografia (pandas) Y flag_demo del A05
# (openpyxl, vía rem_saludmental). Antes divergían: el A05 no listaba "NO SABE"/
# "NO CONTESTA"/"NO INFORMADO" -> sobrecontaba originarios en silencio (CORR-2).
PUEBLO_VACIO = {"", "NO", "NINGUNO", "NINGUNA", "NO APLICA", "SIN INFORMACION",
                "N/A", "NO SABE", "NO CONTESTA", "NO INFORMADO"}
_PUEBLO_VACIO = PUEBLO_VACIO   # alias retrocompat (uso interno histórico)


def marcar_demografia(d):
    """Agrega columnas booleanas `dem_*` por atención. Devuelve el mismo df.
    dem_migrante · dem_originario · dem_sename · dem_mejorninez · dem_cuidador ·
    dem_demencia · dem_campana. (Gestante es a nivel RUN -> `gestante_runs`.)"""
    cols = ("dem_migrante", "dem_originario", "dem_sename", "dem_mejorninez",
            "dem_cuidador", "dem_campana", "dem_demencia")
    if len(d) == 0:                       # df vacío: columnas booleanas vacías
        for c in cols:
            d[c] = False
        return d

    def alerta(*subs):   # ALERTAS ADMIN contiene ALGUNA subcadena
        s = d["ALERTAS"].map(norm) if "ALERTAS" in d else None
        if s is None:
            return d.get("RUN", d.index).map(lambda _: False)
        m = None
        for x in subs:
            c = s.str.contains(norm(x), regex=False, na=False)
            m = c if m is None else (m | c)
        return m.fillna(False)

    emig = d["EMIG"].map(norm) if "EMIG" in d else None
    pueblo = d["PUEBLO"].map(norm) if "PUEBLO" in d else None
    d["dem_migrante"] = ((emig == "SI") if emig is not None else False) | alerta("MIGRANTE")
    d["dem_originario"] = (~pueblo.isin(_PUEBLO_VACIO)) if pueblo is not None else False
    d["dem_sename"] = alerta("SENAME")
    d["dem_mejorninez"] = alerta("MEJOR NINEZ", "SPE EX MEJOR")
    d["dem_cuidador"] = alerta("CUIDADOR")
    d["dem_campana"] = d["ACT_n"].str.contains(norm("campaña de invierno"), regex=False, na=False)
    d["dem_demencia"] = d["DIAG_n"].str.contains(norm("demencia"), regex=False, na=False)
    return d


def trans_de(sexo, genero):
    """Regla TRANS unica (A05 y SM) -> 'M' | 'F' | 'X' | None. M/F = el GENERO.
      - explicita: GENERO trae 'TRANS' ('Transgenero Masculino', 'Femenino Trans').
      - implicita: sexo registral binario y genero binario OPUESTO
                   (Hombre + Femenina -> F, Mujer + Masculino -> M).
    Todo lo demas no cuenta: 'No binarie', 'Otra', 'No Revelado', vacio, y los sexos
    Intersexual/Desconocido/No Informado. No es juicio clinico: RAYEN registra no
    binario pero el REM solo tiene binario + Trans, no hay casilla donde ponerlo.
    La implicita es ESTRECHA a proposito (solo los dos cruces binarios): la vieja
    heuristica genero!=sexo era ruidosa porque cruzaba contra cualquier valor."""
    g, s = norm(genero), norm(sexo)
    if "TRANS" in g:
        return "M" if "MASCULIN" in g else "F" if "FEMENIN" in g else "X"
    if s == "HOMBRE" and g in ("FEMENINA", "FEMENINO"):
        return "F"
    if s == "MUJER" and g in ("MASCULINO", "MASCULINA"):
        return "M"
    return None


def trans_map(entrada):
    """Lee el 'Informe Inscritos y Adscritos' -> dict RUN -> 'M' | 'F' | 'X' para
    personas TRANS segun `trans_de` (explicita por GENERO + implicita sexo/genero).
    La direccion (M/F) alimenta el split TRANS Masculino/Femenina del template.
    Archivo ENORME (toda la poblacion del CESFAM) -> se carga solo si el usuario lo
    aporta. SEXO es obligatorio igual que GENERO: sin el, la via implicita se
    perderia en silencio."""
    hdr, filas = leer_xlsx(entrada)
    hn = [norm(h) for h in hdr]
    i_run = indice_col(hn, "NUMERO", "IDENTIFICACION")
    if i_run is None:
        i_run = indice_col(hn, "RUN")
    i_gen = indice_col(hn, "GENERO")
    i_sex = indice_col(hn, "SEXO")
    faltan = [c for c, i in [("RUN", i_run), ("GÉNERO", i_gen), ("SEXO", i_sex)] if i is None]
    if faltan:   # archivo modificado o reporte equivocado
        raise ValueError(f"el 'Informe Inscritos' no trae la(s) columna(s) {' y '.join(faltan)}. "
                         "¿Está modificado o es otro reporte? Descárgalo de nuevo SIN tocar.")
    exigir_filas(filas, "el 'Informe Inscritos y Adscritos'")
    out = {}
    for f in filas:
        t = trans_de(f[i_sex] if i_sex < len(f) else "", f[i_gen] if i_gen < len(f) else "")
        if t:
            out[str(f[i_run]).strip()] = t
    return out


def atenid_multiprofesional(entrada):
    """Set de ATEN ID MULTIPROFESIONALES (2+ profesionales), del reporte 'Monitoreo
    Multiprofesional': la columna 'Multiprofesional-1' no vacía = tuvo >=1 profesional
    adicional. Sirve para marcar composición (Un Profesional vs Dos o Más). Opcional:
    sin este reporte, todo se asume mono-profesional."""
    hdr, filas = leer_xlsx(entrada)
    hn = [norm(h) for h in hdr]
    i_aten, i_m1 = indice_col(hn, "ATEN", "ID"), indice_col(hn, "MULTIPROFESIONAL", "1")
    if i_aten is None or i_m1 is None:
        raise ValueError("el 'Monitoreo Multiprofesional' no trae ATEN ID / "
                         "Multiprofesional-1. ¿Modificado o reporte equivocado?")
    exigir_filas(filas, "el 'Monitoreo Multiprofesional'")
    return {str(f[i_aten]).strip() for f in filas if i_m1 < len(f) and norm(f[i_m1])}


def gestante_runs(d, ini, fin):
    """Set de RUNs GESTANTES (patrón PowerBI): atención de MATRONA con 'control
    prenatal' (o formulario clínico 'gestante') en la ventana [ini, fin] (3 meses
    terminando en el mes reportado). Requiere columnas del ADA IRIS."""
    w = d[(d["FECHA"] >= ini) & (d["FECHA"] <= fin)]
    if w.empty:
        return set()
    mat = w["INSTR_n"].str.contains(norm("matron"), regex=False, na=False)
    prenatal = w["ACT_n"].str.contains(norm("control prenatal"), regex=False, na=False)
    form = (w["FORMCLIN"].map(norm).str.contains(norm("gestante"), regex=False, na=False)
            if "FORMCLIN" in w else prenatal & False)
    return set(w.loc[mat & (prenatal | form), "RUN"])


def contiene_todos(serie, *subs):
    """Máscara booleana pandas: la Serie (ya normalizada) contiene TODAS las
    subcadenas (case/acento-insensible vía norm). Para clasificar reportes."""
    m = None
    for x in subs:
        c = serie.str.contains(norm(x), regex=False, na=False)
        m = c if m is None else (m & c)
    return m


def contiene_alguno(serie, subs):
    """Máscara booleana pandas: la Serie contiene ALGUNA de las subcadenas."""
    m = None
    for x in subs:
        c = serie.str.contains(norm(x), regex=False, na=False)
        m = c if m is None else (m | c)
    return m


# -- Salidas -----------------------------------------------------------
def rutas_libres(*rutas):
    """Las rutas de salida de UNA corrida, sin pisar nada que ya exista: si alguna
    esta tomada, TODAS pasan a `nombre (1).xlsx`, `nombre (2).xlsx`... con el MISMO
    numero, el menor que deja libres a todas (como Windows al copiar).

    POR QUE no se sobreescribe (decision del autor, sep-2026): una corrida que falla a
    medias (un paso opcional que revienta, la ventana cerrada mientras escribe) dejaba
    junto a la salida nueva un archivo VIEJO del mismo mes, de otra corrida con otros
    archivos -- un A03·D.3 de agosto que nadie regenero, con cara de ser de esta
    corrida y listo para copiarse al REM. Y un archivo abierto en Excel ya no hace
    fallar la corrida entera al guardar.

    POR QUE el mismo numero para todas: el sufijo es lo que dice que archivos salieron
    JUNTOS. `actividades (1)` al lado de un `trabajo_perdido` sin numero delata que
    ese no es de esta corrida."""
    rutas = [Path(r) for r in rutas]
    n = 0
    while True:
        cands = [r if n == 0 else r.with_name(f"{r.stem} ({n}){r.suffix}") for r in rutas]
        if not any(c.exists() for c in cands):
            return cands
        n += 1


def escribir_atomico(salida, escribir):
    """`escribir(ruta)` sobre un TEMPORAL junto a `salida` y, solo si termina, lo
    renombra a `salida` (`os.replace`). Devuelve `salida`.

    POR QUE: si la corrida se corta a mitad de la escritura (el usuario cierra la
    ventana y el hilo del worker muere con el proceso, o revienta el disco), lo que
    queda es un `… .escribiendo.xlsx` que dice lo que es -- nunca un `.xlsx` roto con
    nombre de resultado, listo para abrirse y copiarse al REM. Si `escribir` levanta,
    el temporal se borra y la excepcion sigue su camino."""
    import os
    salida = Path(salida)
    tmp = salida.with_name(f"{salida.stem}.escribiendo{salida.suffix}")
    try:
        escribir(tmp)
        os.replace(tmp, salida)
    except BaseException:
        try:
            tmp.unlink()
        except OSError:
            pass
        raise
    return salida


# -- Caches del usuario (~/.autorem): leer/guardar con fallas RUIDOSAS ---
# dotacion.json (quien es externo) y estamentos.json cambian CIFRAS del REM: un veto de
# dotacion que no llego al disco hace que el mes siguiente se pregunte todo de nuevo con
# 'interno' por defecto (doble conteo si se aprieta Aplicar de pasada), y un caché dañado
# que se lee como vacio vuelve a contar a todos los externos. Por eso aca nada falla
# callado: cada problema queda en `_AVISOS_CACHE`, que la GUI vacia y MUESTRA
# (`gui.runner.avisar_cache`), ademas de ir al log. Lo que NO se hace, a proposito: caer
# a otra carpeta cuando esta falla -- partiria la tabla en dos (este mes se guarda en B,
# el proximo se lee de A) y el veto volveria en silencio a lo de antes.
_AVISOS_CACHE = []
_SIGUE = ("Más detalle y qué hacer: «Acerca de», sección «Preferencias guardadas».")


def _avisar_cache(log, msg):
    log(f"[caché] {msg}")
    _AVISOS_CACHE.append(msg)


def tomar_avisos_cache():
    """Los avisos de caché pendientes, vaciando la cola (los muestra la GUI)."""
    avisos = _AVISOS_CACHE[:]
    del _AVISOS_CACHE[:len(avisos)]
    return avisos


def apartar_cache(ruta, que, motivo, si_se_pierde, log=print):
    """Un caché DAÑADO no se sobreescribe ni se lee como vacio en silencio: se renombra
    a `<nombre>.corrupto-<fecha>.json` (queda la evidencia, y el proximo guardado no lo
    pisa) y se avisa."""
    import os
    import time
    ruta = Path(ruta)
    apartado = ruta.with_name(f"{ruta.stem}.corrupto-{time.strftime('%Y%m%d-%H%M%S')}{ruta.suffix}")
    try:
        os.replace(ruta, apartado)
        donde = f"Lo aparté como «{apartado.name}» (puedes borrarlo)."
    except OSError as e:
        donde = f"Tampoco pude apartarlo ({e})."
    _avisar_cache(log, f"{que} estaba dañado ({motivo}). {donde} Empiezo sin él: "
                       f"{si_se_pierde} {_SIGUE}")


def leer_cache_json(ruta, que, si_se_pierde, log=print, intentos=4):
    """(datos, estado) del caché JSON `ruta`. estado:
      'ok'        -> datos = lo leido (un dict; la FORMA la valida quien llama).
      'falta'     -> nunca se guardo (primera vez): datos None, sin aviso.
      'corrupto'  -> se aparto (`apartar_cache`) y se aviso: datos None.
      'ilegible'  -> existe pero no se pudo leer (permisos, bloqueo que no se solto):
                     datos None y aviso. Quien llama NO debe guardar encima: el archivo
                     puede estar sano y se perderia entero.
    Un `PermissionError` se reintenta: en Windows el antivirus o el indexador toman el
    archivo unos milisegundos y lo sueltan solos."""
    import json
    import time
    ruta = Path(ruta)
    if not ruta.exists():
        return None, "falta"
    error = None
    for i in range(intentos):
        try:
            texto = ruta.read_text(encoding="utf-8")
            break
        except PermissionError as e:
            error = e
            time.sleep(0.1 * (i + 1))
        except OSError as e:
            error = e
            break
    else:
        texto = None
    if texto is None:
        _avisar_cache(log, f"No pude leer {que} en {ruta} ({error}). Esta corrida sigue sin "
                           f"él y NO lo sobreescribo: {si_se_pierde} {_SIGUE}")
        return None, "ilegible"
    try:
        datos = json.loads(texto)
    except ValueError as e:
        apartar_cache(ruta, que, e, si_se_pierde, log=log)
        return None, "corrupto"
    if not isinstance(datos, dict):
        apartar_cache(ruta, que, "no tiene la forma esperada", si_se_pierde, log=log)
        return None, "corrupto"
    return datos, "ok"


def guardar_cache_json(ruta, datos, que, si_no_se_guarda, log=print, intentos=4):
    """Guarda `datos` en `ruta` via `escribir_atomico` (un corte no deja un JSON a
    medias), reintentando un `PermissionError` pasajero. True si quedo guardado; si no,
    aviso RUIDOSO (no excepcion: lo que esta en memoria sigue sirviendo para ESTA
    corrida, solo que no se recuerda)."""
    import json
    import time
    ruta = Path(ruta)
    texto = json.dumps(datos, ensure_ascii=False, sort_keys=True, indent=0)
    error = None
    for i in range(intentos):
        try:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            escribir_atomico(ruta, lambda p: p.write_text(texto, encoding="utf-8"))
            return True
        except PermissionError as e:
            error = e
            time.sleep(0.15 * (i + 1))
        except OSError as e:
            error = e
            break
    _avisar_cache(log, f"No pude guardar {que} en {ruta} ({error}). Esta corrida la usa "
                       f"igual, pero no queda recordada: {si_no_se_guarda} {_SIGUE}")
    return False


def estado_cache(ruta):
    """Diagnostico SIN efectos (para «Acerca de»): nunca aparta ni avisa.
    {'existe', 'modificado' (datetime|None), 'datos' (dict|None), 'problema' (str|None)}."""
    import json
    from datetime import datetime
    ruta = Path(ruta)
    info = {"existe": ruta.exists(), "modificado": None, "datos": None, "problema": None}
    if not info["existe"]:
        return info
    try:
        info["modificado"] = datetime.fromtimestamp(ruta.stat().st_mtime)
        datos = json.loads(ruta.read_text(encoding="utf-8"))
        if isinstance(datos, dict):
            info["datos"] = datos
        else:
            info["problema"] = "dañado (no tiene la forma esperada)"
    except ValueError:
        info["problema"] = "dañado (no es JSON válido)"
    except OSError as e:
        info["problema"] = f"no se puede leer ({e})"
    return info


def carpeta_escribible(carpeta):
    """True si se puede crear un archivo en `carpeta` (o, si todavia no existe, en la
    primera carpeta existente hacia arriba). Prueba de verdad: crea y borra."""
    import tempfile
    c = Path(carpeta)
    while not c.exists() and c.parent != c:
        c = c.parent
    try:
        with tempfile.NamedTemporaryFile(dir=c, prefix=".autorem-prueba-"):
            pass
        return True
    except OSError:
        return False


# -- Utilidad de SO ----------------------------------------------------
def abrir_carpeta(carpeta: Path):
    """Abre el explorador de archivos en `carpeta` (Windows / macOS / Linux)."""
    import subprocess
    try:
        if sys.platform.startswith("win"):
            import os
            os.startfile(str(carpeta))   # noqa
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(carpeta)])
        else:
            subprocess.Popen(["xdg-open", str(carpeta)])
    except Exception:
        pass
