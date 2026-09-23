#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 2.0.11
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

import contextlib
import re
import sys
from pathlib import Path   # reexport de conveniencia para los módulos

# -- Versión del proyecto (fuente única de verdad) --
# Convención X.Y.Z (ver CLAUDE.md §9):
#   X = arquitectura grande o plantillas REM de un año nuevo · Y = módulo/reporte nuevo
#   · Z = corrección. Cada .py lleva en su header la versión de SU último cambio.
VERSION = "2.0.11"

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


class OpcionalInvalido(ArchivoInvalido):
    """Un archivo OPCIONAL que el usuario cargó y no sirve. `entrada` = cuál (el nombre
    del parámetro del módulo; la página lo traduce a su input).

    Decisión del autor (ronda 11, sep-2026): ni seguir callado sin él (TRANS y el
    Multiprofesional quedaban en un log) ni tumbar la corrida sin salida: la GUI
    pregunta «¿quieres continuar sin él?», y si sí, re-corre sin ese archivo y lo deja
    en la LEEME. Fuera de la GUI se comporta como cualquier ArchivoInvalido."""
    def __init__(self, entrada, error):
        super().__init__(getattr(error, "categoria", "opcional_invalido"), str(error))
        self.entrada = entrada


@contextlib.contextmanager
def opcional(entrada):
    """`with opcional("inscritos"): tmap = trans_map(ruta)` -> un ArchivoInvalido del
    bloque sale como OpcionalInvalido(entrada).

    SOLO ArchivoInvalido (ronda 12). Hasta 1.9.17 tambien atrapaba ValueError, porque
    `trans_map`, `atenid_multiprofesional` y `_guard_maestro` señalaban "este archivo no
    sirve" con un ValueError pelado. Ahora esos tres pasan por `cargar_canonico` y
    levantan ArchivoInvalido como todos los demas, asi que seguir atrapando ValueError
    solo servia para disfrazar un BUG de codigo (un ValueError de pandas dentro del
    bloque, que en el A23 abarca tambien el procesamiento de la Seccion H) como "tu
    archivo opcional no sirve, ¿seguimos sin el?": el usuario contestaba que si y
    perdia una desagregacion por un bug nuestro, con la LEEME culpando a su archivo."""
    try:
        yield
    except OpcionalInvalido:
        raise
    except ArchivoInvalido as e:
        raise OpcionalInvalido(entrada, e) from e


# -- Normalización y parsing de celdas ---------------------------------
# `norm` es la función MÁS llamada del proyecto: una vez por CELDA en
# `encontrar_fila_encabezado`, `detectar_eje_filas`, `marcar_eventos` y en cada
# `.map(norm)` de los loaders pandas -- millones de llamadas por corrida. Por eso la
# tabla de tildes y el patrón de espacios viven ACÁ ARRIBA y no dentro de la función:
#   - `str.translate` hace UNA pasada con la tabla ya construida, contra las 7
#     `str.replace` encadenadas (7 pasadas) más el `zip()` que se rearmaba por llamada.
#   - el patrón compilado se salta el lookup en la caché de `re` y el parseo de args.
# Medido (300k llamadas, valores típicos de un export): 0.42 s -> 0.19 s, 2.2x, con el
# MISMO resultado -- verificado contra tildes, ñ, \xa0 (el espacio duro que traen los
# exports copy-paste), \r\v\f y los caracteres cuya MAYÚSCULA cambia de largo o de
# forma (la ligadura fi -> 'FI', la i sin punto del turco -> 'I').
_TRAD_NORM = str.maketrans("ÁÉÍÓÚÜÑ", "AEIOUUN")
_RE_ESPACIOS = re.compile(r"\s+")


def norm(v):
    """Texto en MAYÚSCULA, sin tildes/ñ, con espacios colapsados. '' si es None/NaN."""
    if v is None or v != v: return ""   # v != v capta NaN (float) -> '' (celda vacía)
    return _RE_ESPACIOS.sub(" ", str(v).upper().strip().translate(_TRAD_NORM))


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
def encontrar_fila_encabezado(ws, ancla, max_filas=60):
    """Ubica la fila del encabezado real saltando el banner y los filtros que RAYEN pone
    arriba: la 1ª fila que contiene TODOS los tokens de `ancla` (match por substring).
    Sin ancla -> ArchivoInvalido('sin_encabezado'). Devuelve la fila (1-based).

    Hasta la ronda 11 (sep-2026) habia dos fallbacks POSICIONALES detras del ancla: «la
    fila siguiente a la 1ª con la columna A vacia» y un numero fijo de fila (16 en IRIS,
    8 en el Administrativo), para el export al que le borraron el encabezado. Los dos
    devolvian una fila de DATOS como encabezado y seguian: se armaron antes de tener
    refs_tablas/ y, con la deteccion por contenido, ya no tenian caso. (Devolvia tambien
    un `modo` que decia CUAL de los tres habia acertado; sin fallbacks era la constante
    'ancla', y se saco en la ronda 12 junto con los envoltorios `fila_encabezado_admin`
    y los `_fila_encabezado` del A03 y de estamentos: la unica diferencia entre formatos
    es QUE ancla se pasa, y eso ya lo dice `formatos.ANCLA`.)"""
    tope = min(ws.max_row, max_filas)
    ancla_n = [norm(t) for t in ancla]
    for r in range(1, tope + 1):
        vals = [norm(c.value) for c in ws[r]]
        if all(any(tok in v for v in vals) for tok in ancla_n):
            return r
    raise ArchivoInvalido(
        "sin_encabezado",
        f"No encuentro la fila de encabezado del export (busqué una fila con: "
        f"{', '.join(ancla)}) en las primeras {tope} filas.\n\n"
        "¿Le borraste o editaste el encabezado? Carga el archivo tal como sale de "
        "RAYEN/IRIS, con su banner y su fila de nombres de columna.")


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


def primeras_filas(entrada, n):
    """Las primeras `n` filas (ver `filas_hoja`) de la hoja activa: abrir con
    `abrir_xlsx_ro`, leer y cerrar. Para las detecciones BARATAS (formato del A05,
    cruce ADA<->Grupal), que no necesitan el archivo entero."""
    wb = abrir_xlsx_ro(entrada)
    try:
        return filas_hoja(wb.active, n)
    finally:
        wb.close()


def indice_encabezado(filas, ancla=None, max_scan=40):
    """Indice de la fila de encabezado dentro de `filas`, o None si ninguna calza.
    `ancla` = nombres de columna que deben estar TODOS en esa fila; sin ancla, la 1ª
    fila con >3 celdas llenas. La usan `leer_xlsx` y el preview de cruce del SM, que
    antes lo copiaba a mano.

    OJO, no es el unico criterio del proyecto (lo decia este docstring hasta la ronda
    13, y era falso): el grupo pandas ubica el encabezado por las columnas REQUERIDAS
    (`encabezado_por_columnas`, ronda 12) porque contar celdas rechazaba exports validos,
    y `tools/limpiar_refs.py` tiene su propio umbral (`MIN_CELDAS_HEADER = 5`) para
    recortar las referencias. Si hay que mover un umbral, son TRES lugares.

    Devolvia 0 (la 1ª fila, o sea el banner) cuando ninguna calzaba -- un fallback
    POSICIONAL callado, de la misma familia que los que la ronda 11 saco de
    `encontrar_fila_encabezado`. Ahora devuelve None y decide quien llama (ronda 12)."""
    if ancla:
        want = {norm(a) for a in ancla}
        return next((i for i, r in enumerate(filas[:max_scan]) if want <= {norm(v) for v in r}), None)
    return next((i for i, r in enumerate(filas[:max_scan])
                 if sum(v not in (None, "") for v in r) > 3), None)


def filas_xlsx(entrada):
    """TODAS las filas (tuplas de valores) de la hoja activa de un .xlsx. ROBUSTO a la
    'dimension' rota o ausente de los exports copy-paste / de BD: lee con
    `abrir_xlsx_ro`, que la descarta (hasta 1.9.17 NO lo era: la respetaba y truncaba en
    silencio -- ver alla). Hoja sin NINGUNA fila -> ArchivoInvalido."""
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
    return filas


def leer_xlsx(entrada, ancla=None, max_scan=40):
    """Lee un .xlsx y devuelve (headers, filas_de_datos). `ancla` = nombres de columna
    que deben estar TODOS en la fila de encabezado; si es None, toma la 1ª fila con >3
    celdas llenas. Sin fila de encabezado -> ArchivoInvalido('sin_encabezado').

    Los lectores del grupo pandas NO pasan por aca: `cargar_canonico` ubica el
    encabezado por las columnas que el propio loader declara REQUERIDAS
    (`encabezado_por_columnas`), que es un ancla de verdad y no un conteo de celdas."""
    filas = filas_xlsx(entrada)
    hi = indice_encabezado(filas, ancla, max_scan)
    if hi is None:
        raise ArchivoInvalido(
            "sin_encabezado",
            "No encuentro la fila de encabezado (nombres de columna) en las primeras "
            f"{max_scan} filas del archivo"
            + (f", buscando: {', '.join(ancla)}" if ancla else "") + ".\n\n"
            "¿Le borraste o editaste el encabezado? Carga el archivo tal como sale de "
            "RAYEN/IRIS, con su banner y su fila de nombres de columna.")
    return list(filas[hi]), filas[hi + 1:]


def encabezado_por_columnas(filas, resolver, requeridas, max_scan=40):
    """Ubica el encabezado por las columnas que el loader NECESITA: la 1ª fila en que
    `resolver(fila)` resuelve TODAS las claves `requeridas`. Devuelve
    (indice, {canon: columna}, faltan): con `indice` None no hubo ninguna, y `faltan`
    son las claves que le faltaban a la fila que MAS resolvio (la candidata a ser el
    encabezado con una columna renombrada), para poder decirlo en el error.

    POR QUE (ronda 12): el criterio viejo era «la 1ª fila con >3 celdas llenas», o sea
    un conteo, y los banners de RAYEN ya traen filas de 3 celdas -- una sola columna mas
    en el banner del Monitoreo y el encabezado pasaba a ser una fila de filtros. El ancla
    real es lo que el loader declara en `requeridas`, y no hace falta declararla dos
    veces. Solo se le pasa el resolver a las filas con al menos tantas celdas llenas como
    claves requeridas (el encabezado las tiene por definicion): asi el costo sigue siendo
    una llamada o dos por archivo, no 40."""
    minimo = max(2, len(requeridas))
    mejor = (None, None, list(requeridas))
    for i, r in enumerate(filas[:max_scan]):
        if sum(v not in (None, "") for v in r) < minimo:
            continue
        col = resolver(list(r))
        faltan = [k for k in requeridas if not col.get(k)]
        if not faltan:
            return i, col, []
        if len(faltan) < len(mejor[2]):
            mejor = (i, col, faltan)
    return None, mejor[1], mejor[2]


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


def cargar_canonico(entrada, resolver, requeridas, no_vacias=(), solo_iris=None,
                    log=print, espera=None):
    """Lee UNO o VARIOS .xlsx (los reportes acumulativos necesitan varios años) y
    arma el DataFrame canónico concatenado. `resolver(headers) -> {canon: columna}`.
    `requeridas` = claves canónicas que DEBEN resolverse en CADA archivo; ubican el
    ENCABEZADO (`encabezado_por_columnas`) y, si a algún archivo le faltan, levanta
    ArchivoInvalido NOMBRANDO ese archivo (los módulos multi-archivo así saben CUÁL
    falló). Devuelve (df, col_del_primero); `df.attrs['columnas_por_archivo']` trae
    [(nombre, {canon: columna}), ...] para quien necesite la resolución POR ARCHIVO
    (el 'Otros Crónicos' la usa para sus avisos; antes se la llevaba con un efecto
    secundario dentro del propio `resolver`, que ahora se llama varias veces).

    `no_vacias` = claves que, además de resolverse, tienen que traer ALGÚN valor en
    CADA archivo. Una columna clave presente pero VACÍA en todas las filas es el mismo
    bug que la columna ausente y da el mismo 0 callado (ronda 11, §1.L.7): la guarda
    estaba escrita a mano en seis loaders, y en dos de ellos sobre el DataFrame ya
    CONCATENADO -- así que un archivo con el RUN entero en blanco, cargado junto a uno
    bueno, pasaba sin decir nada y sus filas se perdían (o se juntaban bajo un paciente
    fantasma). Acá es POR ARCHIVO, como `exigir_filas` (ronda 12).

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
            todas = filas_xlsx(e)
        except ArchivoInvalido as ai:    # p.ej. 'modificado' -> agrega el nombre del archivo
            raise ArchivoInvalido(ai.categoria, f"Archivo «{nombre}»:\n\n{ai}") from ai
        except Exception as ex:          # openpyxl/zip/etc. -> no es un .xlsx legible
            raise ArchivoInvalido(
                "no_legible",
                f"No pude leer el archivo:\n«{nombre}»\n\n{ex}\n\n"
                "¿Es un .xlsx válido (no .xls/.csv/.html) y sin modificar?") from ex
        # El encabezado se ubica por las columnas REQUERIDAS, no por un conteo de celdas
        # llenas (ver `encabezado_por_columnas`): el mismo chequeo resuelve donde empieza
        # la tabla y si el archivo trae lo que el loader necesita.
        hi, col, faltan = encabezado_por_columnas(todas, resolver, requeridas)
        hdr = list(todas[hi if hi is not None else 0])
        if hi is None:
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
        filas = todas[hi + 1:]
        # Fail loud sobre la FUENTE (CLAUDE.md regla 2) y POR ARCHIVO: con 0 filas
        # las columnas quedan float64 y .str.contains() revienta abajo con un error
        # criptico (o el conteo sale 0 en silencio). Unico cuello de botella del grupo
        # pandas -> cubre ADA, grupal, Inscritos, NSP y 'Otros y Respi'.
        exigir_filas(filas, f"el archivo «{nombre}»")
        col0 = col0 or col
        cols_por_archivo.append((nombre, col))
        idx = {c: i for i, c in enumerate(hdr)}
        parte = pd.DataFrame(
            {k: [f[idx[c]] if c is not None and idx[c] < len(f) else None for f in filas]
             for k, c in col.items()})
        # Columna clave PRESENTE pero vacia en todas las filas = el mismo 0 callado que
        # la columna ausente, y POR ARCHIVO (ver el docstring).
        # Corto circuito, no barrido: la pregunta es «¿hay ALGÚN valor con dato?», y en
        # un export sano la contesta la 1ª fila. `.map(norm).ne("").any()` normalizaba
        # la columna ENTERA antes de reducir -- 0,091 s por (clave x archivo) sobre
        # 30.000 filas, o sea ~0,55 s en un ADA de 3 años (2 claves x 3 archivos), y se
        # pagaban COMPLETOS justo cuando el archivo está bien. El `norm` sigue siendo
        # quien define «vacío» (regla 4), no un `.strip()` a mano: mismo booleano.
        vacias = [k for k in no_vacias if not any(norm(v) != "" for v in parte[k])]
        if vacias:
            raise ArchivoInvalido(
                "sin_datos",
                f"Archivo «{nombre}»:\n\nTrae {len(filas)} fila(s), pero la(s) "
                f"columna(s) {', '.join(f'«{col.get(k) or k}»' for k in vacias)} vienen VACÍAS en "
                "todas ellas, así que no se puede atribuir ninguna fila.\n\n"
                "Revisa que sea el export completo, sin modificar.")
        # ATENID por CORRELATIVO ('N°' del Monitoreo) reinicia en 1 en cada export:
        # concatenar dos archivos fusionaria atenciones distintas bajo el mismo id y
        # el conteo por-atencion SUBCONTARIA en silencio. Se namespacea con el nombre
        # del archivo. NO se toca el 'ATEN ID' de IRIS, que es global y unico: si el
        # mismo ATEN ID aparece en dos exports que se solapan, tiene que deduplicar.
        if col.get("ATENID") == ATENID_CORRELATIVO and "ATENID" in parte:
            parte["ATENID"] = nombre + "|" + parte["ATENID"].astype(str)
        partes.append(parte)
    d = pd.concat(partes, ignore_index=True) if len(partes) > 1 else partes[0]
    d.attrs["columnas_por_archivo"] = cols_por_archivo
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


# Separador con que el A/D/A de IRIS junta en UNA celda las actividades de una misma
# atención. Al colapsar el Monitoreo se usa el mismo, para que la celda ACTIVIDADES
# tenga la misma forma en los dos formatos.
SEP_ACTIVIDADES = "; "

# Columnas de CABECERA de la atención (las que el Monitoreo trae solo en su fila padre).
# Lo que NO está acá es por-actividad: ACT y DIAG (se unen) y ATENID (es la clave).
CAB_ATENCION = ["RUN", "FECHA", "INSTR", "PROF", "TIPO", "SEXO", "SECTOR", "NACION",
                "EMIG", "ALERTAS", "FORMCLIN", "PUEBLO", "FNAC", "NOMBRES", "APAT",
                "AMAT", "ANOS", "ANOS_AT"]


def clave_atencion(v):
    """ATEN ID / N° -> clave de TEXTO estable, y la etiqueta que se le muestra al
    usuario. El ATEN ID de IRIS es NUMÉRICO (Excel lo muestra '683.016.530,00') y
    openpyxl lo entrega como int o como float según la celda: sin esto, `norm` daría
    '683016530' y '683016530.0' y la MISMA atención se partiría en dos. Vacío -> ''."""
    if isinstance(v, float) and v == v and v.is_integer():
        v = int(v)
    return norm(v)


def _una_fila_por_atencion(d, log=print):
    """Forma CANÓNICA de las atenciones: UNA fila por atención, con todas sus
    actividades (y diagnósticos) en una celda, como las entrega el A/D/A de IRIS.

    El Monitoreo admin usa estructura PADRE-HIJO: una atención abierta en varias filas,
    una actividad cada una, con la cabecera solo en la 1ª y el 'N°' repetido en las hijas
    (§5.1 de programas/CLAUDE.md). Eso no es una diferencia de CONTENIDO sino de FORMA, y
    es de la FUENTE: normalizarla acá es lo que hace que los dos formatos den el MISMO
    número, en todos los consumidores y en los que vengan.

    Hasta 1.9.17 estaba resuelta a medias (ronda 12): la cabecera se rellenaba acá con un
    ffill dentro del ATENID, y el resto quedaba a cargo de UN consumidor
    (`a23._act_de_la_atencion`, para los indicadores con AND entre actividades). Los demás
    seguían viendo una fila por actividad: el Trabajo Perdido marcaba «saco roto» una
    actividad cuya hermana de la misma atención SÍ tributaba (0 desde IRIS, 1 desde el
    Monitoreo, con los mismos datos) y contaba actividades donde su tabla dice
    «atenciones»; y la evidencia del diálogo de dotación inflaba `n_atenciones`."""
    import pandas as pd
    aten = d["ATENID"].map(clave_atencion)
    dup = aten.ne("") & aten.duplicated(keep=False)
    if not dup.any():
        return d      # IRIS, o un Monitoreo sin atenciones de 2+ actividades: ya está
    # Las filas sin ATENID (o con uno único) NO se pueden agrupar: cada una es su grupo.
    # La clave es NUMÉRICA a propósito. Con un centinela de TEXTO hay que inventar un
    # string que no pueda chocar con un ATEN ID real, y el que se usó ('\x00fila{i}')
    # traía un byte NUL: el groupby de pandas hashea el str HASTA el NUL, así que las
    # filas sueltas caían TODAS en el mismo grupo y se fusionaban en una sola atención
    # -- callado, y solo en un export MIXTO (alguna atención de 2+ actividades y el
    # resto de una), que es justo la forma del Monitoreo admin real. Medido en pandas
    # 2.3.3: groupby(['\x00a','\x00b','\x00c']) -> UN grupo. Con enteros no hay
    # centinela que inventar: `factorize` da -1 a lo que no agrupa, y ahí va un id
    # negativo distinto por fila.
    grupo = pd.Series(pd.factorize(aten.where(dup))[0], index=d.index)
    solas = pd.Series(range(-1, -len(d) - 1, -1), index=d.index)
    clave = grupo.where(grupo >= 0, solas)
    # Antes de juntar nada: el ATENID tiene que identificar UNA atención, o sea UN
    # paciente. Si el mismo id aparece con RUN distintos no es un id de atención, y
    # juntar esas filas mezclaría a dos personas en una -- callado. Fail loud (regla 2).
    run = d["RUN"].map(norm)
    con_run = run.ne("")
    por_grupo = run[con_run].groupby(clave[con_run]).nunique()
    mezclados = por_grupo[por_grupo > 1]
    if len(mezclados):
        raise ArchivoInvalido(
            "modificado",
            f"El export de atenciones trae {len(mezclados)} identificador(es) de atención "
            "(ATEN ID / N°) repetidos entre pacientes DISTINTOS, así que ese número no "
            "identifica una atención y no se puede contar por atención.\n\n"
            "¿El archivo fue modificado, o no es el reporte de Atenciones? Vuelve a "
            "descargarlo desde RAYEN/IRIS y cárgalo tal cual.")

    def _juntar(s):      # ACT / DIAG: todas las de la atención, sin repetir
        vals = [str(v).strip() for v in s if norm(v) != ""]
        return SEP_ACTIVIDADES.join(dict.fromkeys(vals)) if vals else None

    # La CABECERA no se agrega con una función Python, se ELIGE POR POSICIÓN. Un
    # `groupby().agg({col: fn})` manda a pandas por su camino pure-python: rebana una
    # Serie por cada par (grupo x columna) y llama a la función ahí. Con las 18 columnas
    # de CAB_ATENCION eso son decenas de miles de rebanadas -- medido sobre un Monitoreo
    # de 20.000 filas / 9.525 atenciones: 2,15 s, de los cuales cProfile pone 3,9 s (con
    # el perfilador encima) en `_aggregate_series_pure_python`, 140.007 llamadas a
    # `_chop`.
    # Lo que la vieja `_primero` calculaba era, en realidad, UNA POSICIÓN: la del 1er
    # valor no vacío del grupo, y si el grupo entero venía vacío, la de su 1ª fila. Eso
    # es un `min()` por grupo sobre enteros -- que pandas sí hace en C --, y después un
    # indexado numpy sobre los valores ORIGINALES. Tres detalles que NO son de adorno:
    #   - el centinela `len(d)` ("este grupo no tiene ningún valor lleno") es mayor que
    #     cualquier posición real, así que el `min()` lo descarta solo. Sin él, la
    #     atención con la columna vacía en TODAS sus filas se lleva el valor de OTRA
    #     atención: el SECTOR (o el estamento) de otro paciente, con cara de dato propio.
    #   - el respaldo es la 1ª fila POSICIONAL, no un `groupby().first()` de pandas, que
    #     salta los nulos: un grupo vacío que empieza en None y sigue en '' devolvería el
    #     '' de la 2ª fila en vez del None de la 1ª. Distinto valor, mismo "vacío".
    #   - `col.to_numpy()[posicion]` devuelve el valor TAL CUAL, así que el ATEN ID
    #     numérico de IRIS sigue saliendo entero y no hay dtype que se mueva. (Un
    #     `col.where(...)` habría sido más corto, pero introduce nulos y con ellos la
    #     promoción a float64; acá no hay por dónde.)
    # ACT/DIAG siguen con `_juntar`: juntar y deduplicar no es elegir una fila. Son 2
    # columnas de 21, o sea ~1/10 del costo de antes.
    # Medido: 2,15 s -> 0,39 s (5,5x). Equivalencia verificada valor a valor y por
    # `repr` (no por texto: un int que se vuelve float tiene que saltar) contra una copia
    # textual de la versión 2.0.8, sobre los bordes -- grupo con la cabecera vacía en
    # TODAS sus filas, NaN antes que '' y al revés, ACT/DIAG vacíos en todo el grupo,
    # fila padre que no es la primera, ATEN ID numérico, filas sueltas entre medio -- y
    # sobre 6 frames grandes al azar. Arnés en docs/evanesced/.
    import numpy as np
    pos = np.arange(len(d))
    gpos = pd.Series(pos, index=d.index).groupby(clave, sort=False)
    primera = gpos.min()                 # 1ª fila de cada grupo, en orden de aparición
    orden = primera.index                # las claves, en ESE mismo orden
    primera = primera.to_numpy()

    out = {}
    for c in d.columns:
        col = d[c]
        if c in ("ACT", "DIAG"):
            out[c] = col.groupby(clave, sort=False).agg(_juntar).to_numpy()
            continue
        # RUN ya viene normalizada de la guarda de arriba (`run`): normalizarla de
        # nuevo seria una segunda pasada completa sobre la columna mas grande del
        # frame, y ademas dos definiciones de "vacio" para la misma columna.
        lleno = (run if c == "RUN" else col.map(norm)).ne("").to_numpy()
        llena = (pd.Series(np.where(lleno, pos, len(d)), index=d.index)
                 .groupby(clave, sort=False).min().to_numpy())
        out[c] = col.to_numpy()[np.where(llena < len(d), llena, primera)]
    attrs = dict(d.attrs)   # groupby().agg() no conserva attrs (fuente, columnas_por_archivo)
    out = pd.DataFrame(out, index=orden).reset_index(drop=True)
    out.attrs.update(attrs)
    log(f"[atenciones] {len(d)} filas -> {len(out)} atenciones (el Monitoreo abre cada "
        "atencion en una fila por actividad; se juntan para contar igual que IRIS)")
    return out


def cargar_atenciones(entrada, log=print):
    """Export(s) de ATENCIONES (IRIS ó Monitoreo admin) -> DataFrame canónico, UNA FILA
    POR ATENCIÓN en los dos formatos (`_una_fila_por_atencion`), + textos normalizados
    (act/diag/instr/tipo) + FECHA parseada. Ruta o lista."""
    from programas.formatos import SOLO_IRIS_ATENCIONES
    # ATENID es requerida: es la unidad de conteo del ADA (el SM dedup por ella, el TP
    # cuenta atenciones, y el Monitoreo se colapsa por ella). Sin la columna, `id` queda
    # None en todas las filas y el `drop_duplicates` del SM dejaba UNA fila por casilla.
    d, col = cargar_canonico(entrada, lambda h: resolver_columnas(h, MAPA_ATENCIONES),
                             requeridas=("RUN", "ATENID", "FECHA", "ACT", "DIAG",
                                         "INSTR", "TIPO"),
                             no_vacias=("RUN", "ATENID"),
                             solo_iris=SOLO_IRIS_ATENCIONES, log=log, espera="ada")
    d = _una_fila_por_atencion(d, log)
    # Atención sin RUN en NINGUNA de sus filas: no se puede atribuir a un paciente. (Que
    # TODAS vengan sin RUN lo corta `cargar_canonico` con `no_vacias`, por archivo.)
    huerfanas = int(d["RUN"].map(norm).eq("").sum())
    if huerfanas:
        log(f"[atenciones] {huerfanas} atencion(es) sin RUN en ninguna de sus filas: no "
            "se atribuyen a ningun paciente.")
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


# -- Informe Inscritos y Adscritos (IRIS: padrón del centro, snapshot) ----
# Compartido: lo leen `trans_map` (flag TRANS del SM) y `poblacion.cargar_inscritos`
# (base de la tabla Ferrada). Vivía en poblacion.py y trans_map resolvía las mismas
# columnas por su cuenta (ronda 12).
MAPA_INSCRITOS = {
    "RUN":          [("exact", "NUMERO TIPO IDENTIFICACION"), ("exact", "RUN")],
    "TIPOID":       ("exact", "TIPO IDENTIFICACION"),
    "SEXO":         ("exact", "SEXO"),
    "GENERO":       ("exact", "GENERO"),
    "FNAC":         ("exact", "FECHA DE NACIMIENTO"),
    "EDADANOS":     ("exact", "EDAD AÑOS"),
    "SITUACION":    ("exact", "SITUACION"),
    "ESTADO":       ("exact", "ESTADO"),
    "FPASIV":       ("exact", "FECHA PASIVACION"),
    "MPASIV":       ("exact", "MOTIVO PASIVACION"),
    "SECTOR":       ("exact", "SECTOR"),
    "ALERTAS":      ("subs", ["ALERTAS", "ADMINISTRATIVAS"]),
    "PUEBLO":       ("exact", "PUEBLO INDIG"),
    "NACIONALIDAD": ("exact", "NACIONALIDAD"),
}


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
        col = resolver_columnas(list(raw.columns), MAPA_MAESTRO)
        _guard_maestro(col)
        d = pd.DataFrame({k: (raw[c] if c is not None else "") for k, c in col.items()})
    else:
        # Por `cargar_canonico` como cualquier otra planilla del usuario (ronda 12): así
        # hereda el encabezado por columnas requeridas, la guarda de 0 filas, la de hoja
        # única y -- lo que importaba -- el «no es un .xlsx legible» como ArchivoInvalido.
        # Leyéndolo con `leer_xlsx` a mano, un .xls/.html disfrazado salía como
        # `BadZipFile`, que `rem_utils.opcional` no reconoce: el Maestro cargado a mano es
        # un input OPCIONAL, y la GUI tiene que poder preguntar «¿seguir sin él?».
        d, _col = cargar_canonico(entrada, lambda h: resolver_columnas(h, MAPA_MAESTRO),
                                  requeridas=("ACT", "NUMREM"), no_vacias=("ACT",))
    d = d[d["ACT"].map(lambda x: x not in (None, ""))].copy()
    if len(d) == 0:
        raise ArchivoInvalido("sin_datos", "El Maestro de Actividades no trae ninguna fila "
                              "de datos. Revisa que sea el archivo completo, sin modificar.")
    d["ACT_n"] = d["ACT"].map(norm)
    d["NUMREM_n"] = d["NUMREM"].map(norm)
    return d


def _guard_maestro(col):
    """Guarda del Maestro SLIM (el .xlsx pasa por `cargar_canonico`, que ya la hace).
    ArchivoInvalido y no ValueError (ronda 12): es un archivo que no sirve, y el Maestro
    se carga como OPCIONAL -- `opcional()` solo convierte ArchivoInvalido."""
    if not col["ACT"] or not col["NUMREM"]:
        raise ArchivoInvalido(
            "sin_columnas",
            "No reconozco el Maestro de Actividades (faltan 'ACTIVIDAD' y/o 'NUM REM'). "
            "¿Es el archivo correcto?")


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


def aviso_fuera_de_grid(sub, bandas, casilla, log=print):
    """Aviso (casilla, estado, motivo, que_hacer) para la LEEME, o None: filas de `sub`
    que `grid` cuenta en Ambos/Total pero en NINGUNA columna por sexo o banda etaria
    (sexo que no es Hombre/Mujer -- Intersexual, Desconocido, vacio -- o edad ilegible).

    `grid` las deja en Ambos a proposito (la atencion existio), pero entonces las
    columnas H/M y las bandas que se pegan al REM suman MENOS que el total, y eso
    pasaba callado. Se dice, con el conteo."""
    import pandas as pd
    if not len(sub):
        return None
    sin_sexo = sum(1 for s in sub["sexo"] if not (_hombre(s) or _mujer(s)))
    edades = pd.to_numeric(sub["edad"], errors="coerce")
    sin_banda = sum(1 for e in edades if _band_idx(e, bandas) is None)
    if not (sin_sexo or sin_banda):
        return None
    partes = ([f"{sin_sexo} sin sexo Hombre/Mujer"] if sin_sexo else []) + \
             ([f"{sin_banda} sin edad legible"] if sin_banda else [])
    motivo = (f"{' y '.join(partes)}: cuentan en Ambos pero en ninguna columna por "
              "sexo / tramo de edad, que suman MENOS que el total")
    log(f"[aviso] {casilla}: {motivo}.")
    return (casilla, "REVISAR", motivo,
            "Ubicar esas filas en el detalle y registrarlas a mano en el REM")


def grid(sub, bandas, lbls, con_sexo=True, bandas_idx=None):
    """Fila de conteos en el ORDEN del template: Ambos·Hombres·Mujeres y luego cada
    banda × sexo (o solo total por banda si con_sexo=False). `sub` = DataFrame con
    columnas 'sexo' y 'edad'.

    `bandas_idx` = secuencia de índices de banda (o None por fila) ya calculados por el
    llamador, en el orden POSICIONAL de `sub`. Para quien ya clasificó la edad y tendría
    que convertirla de vuelta a una edad representativa solo para que esta función la
    volviera a clasificar (el P6: ~45 filas × cada persona). Con `bandas_idx`, la
    columna 'edad' de `sub` no se lee."""
    import pandas as pd
    hom = sub["sexo"].map(_hombre)
    muj = sub["sexo"].map(_mujer)
    bi = (sub["edad"].map(lambda x: _band_idx(x, bandas)) if bandas_idx is None
          else pd.Series(list(bandas_idx), index=sub.index, dtype=object))
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

    # La columna normalizada se calcula UNA vez y no dentro de `alerta`: no depende de
    # `subs`, y `alerta` se llama CUATRO veces (migrante, SENAME, Mejor Niñez,
    # cuidador), o sea que tres de las cuatro pasadas de `norm` sobre la columna eran
    # puro descarte. Medido sobre 30.000 atenciones: 0,328 s -> 0,104 s (3,2x), con las
    # cuatro máscaras idénticas.
    alertas_n = d["ALERTAS"].map(norm) if "ALERTAS" in d else None

    def alerta(*subs):   # ALERTAS ADMIN contiene ALGUNA subcadena
        if alertas_n is None:
            return d.get("RUN", d.index).map(lambda _: False)
        m = None
        for x in subs:
            c = alertas_n.str.contains(norm(x), regex=False, na=False)
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
    perderia en silencio.

    Por `cargar_canonico` y con `MAPA_INSCRITOS` (ronda 12): es el MISMO export que lee
    `poblacion.cargar_inscritos`, y tenia su propia resolucion de columnas a mano, sus
    propias guardas y sus propios ValueError -- o sea que cada guarda nueva habia que
    acordarse de escribirla dos veces, y un .xls disfrazado no llegaba como
    ArchivoInvalido (la GUI no podia preguntar «¿seguir sin el?»)."""
    d, _col = cargar_canonico(entrada, lambda h: resolver_columnas(h, MAPA_INSCRITOS),
                              requeridas=("RUN", "SEXO", "GENERO"), no_vacias=("RUN",))
    out = {}
    for run, sexo, genero in zip(d["RUN"], d["SEXO"], d["GENERO"]):
        if norm(run) == "":
            continue
        t = trans_de(sexo, genero)
        if t:
            out[str(run).strip()] = t
    return out


# Reporte 'Monitoreo Multiprofesional' (IRIS): composición de las VDI del A26.
MAPA_MULTIPROF = {
    "ATENID": [("subs", ["ATEN", "ID"]), ("subs", ["ATENCION", "ID"])],
    "MULTI1": ("subs", ["MULTIPROFESIONAL", "1"]),   # no vacía = hubo 2º profesional
}


def atenid_multiprofesional(entrada):
    """Set de ATEN ID MULTIPROFESIONALES (2+ profesionales), del reporte 'Monitoreo
    Multiprofesional': la columna 'Multiprofesional-1' no vacía = tuvo >=1 profesional
    adicional. Sirve para marcar composición (Un Profesional vs Dos o Más). Opcional:
    sin este reporte, todo se asume mono-profesional. Por `cargar_canonico` desde la
    ronda 12 (ver `trans_map`)."""
    d, _col = cargar_canonico(entrada, lambda h: resolver_columnas(h, MAPA_MULTIPROF),
                              requeridas=("ATENID", "MULTI1"), no_vacias=("ATENID",))
    return {str(a).strip() for a, m in zip(d["ATENID"], d["MULTI1"])
            if norm(a) != "" and norm(m) != ""}


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


# Token del estamento MEDICO dentro de INSTRUMENTO, ya normalizado. Es el criterio que
# decide la poblacion SALA / Seccion G del A23 y, via `exigir_medico`, el `¿Ingresado?`
# del P6 -- y la Brecha_Medico es por definicion la DIFERENCIA entre dos pasadas de este
# mismo criterio. Estaba escrito a mano en cuatro lugares, con tres ortografias y sin
# ponerse de acuerdo en `regex=`: si RAYEN cambia la etiqueta (un 'PARAMEDICO' que haya
# que excluir, una variante nueva), el que la arregle tiene que encontrar UN lugar.
TOKEN_MEDICO = "MEDIC"


def es_medico(serie_norm):
    """Mascara booleana 'el INSTRUMENTO es de un medico', sobre una serie YA
    normalizada (regla 4). `programas/poblacion` la memoiza por DataFrame con el
    mismo token (`_instr_medico`), porque la pide 28 veces por pasada."""
    return serie_norm.str.contains(TOKEN_MEDICO, regex=False, na=False)


def por_actividad(A, mascara):
    """Aplica `mascara(serie_norm) -> Series[bool]` a CADA actividad de la celda
    canónica (partida por `SEP_ACTIVIDADES`) y devuelve el OR por atención.

    Desde `_una_fila_por_atencion` (1.9.17) la celda ACT trae TODAS las actividades de
    la atención unidas. Para un indicador que es un AND entre actividades DISTINTAS
    («autocuidado» + «control SALA» del A23) eso es justo lo que se quiere, y la celda
    unida lo da gratis. Pero una máscara cuyos tokens parten el nombre de UNA SOLA
    actividad («controles» + «salud mental por», que es «Controles DE Salud Mental POR
    llamadas telefónicas») se satisface con un token de cada actividad y dispara sin
    que esa actividad exista: falso positivo callado. Y al revés: un `~` sobre la celda
    unida («llamada» y NO «videollamada») se apaga porque una actividad HERMANA trae la
    palabra -> falso negativo. Las dos cosas mueven una casilla del REM.

    Regla: si los tokens describen UNA actividad, la máscara va acá dentro."""
    import pandas as pd
    if not len(A):
        return pd.Series([], dtype=bool, index=A.index)
    # Por SEP_ACTIVIDADES y no un ";" a mano: es el MISMO separador con el que
    # `_una_fila_por_atencion` une la celda, y si alguna vez cambia (un nombre de
    # actividad con ";" adentro), un split desincronizado no falla -- deja de partir
    # y devuelve callado el comportamiento de celda unida que este docstring describe.
    partes = A.astype(str).str.split(SEP_ACTIVIDADES.strip()).explode().str.strip()
    return mascara(partes).groupby(level=0).any().reindex(A.index, fill_value=False)


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
