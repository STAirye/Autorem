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
# option) any later version. Distributed WITHOUT ANY WARRANTY. See the GNU
# General Public License for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
formatos.py — EJE de formato IRIS vs Administrativo de los exports RAYEN.

RAYEN entrega el MISMO reporte en dos formatos ("ejes"):
  - IRIS          -> export pleno (códigos ICD, demografía, columnas completas).
  - Administrativo -> mismo dato, PARCIAL (banner 'Servicio de Salud', header más
    abajo, sin varias columnas). El Monitoreo Admin de atenciones es aún más pobre.

Este módulo NO es de ninguna sección del REM. Es la capa que reconoce y ubica ese
eje, compartida por CASI TODOS los módulos con entrada RAYEN. Cada reporte aporta
sus PROPIAS firmas (anclas/markers que lo identifican) como configuración local;
el MECANISMO (barrer la hoja, decidir el eje, resolver identidad, ubicar header
por eje) vive acá una sola vez.

  rem_utils (primitivas de celda: norm, buscar_col, encontrar_fila_encabezado)
      ^
  formatos (este módulo: eje IRIS/Admin)
      ^
  rem_saludmental / rem_a03_d3_instrumentos / estamentos / … (reportes concretos)

Nota de lenguaje: acá "perfil"/"eje" = formato del export. NO confundir con los
"perfiles" de usuario de RAYEN (permisos de la plataforma), que no tienen relación.

Qué es compartido y qué es por-reporte:
  - COMPARTIDO: vocabulario del eje (banner/markers/tokens de identidad y el ANCLA del
    encabezado de cada formato), la lógica `detectar_eje` y la resolución RUT/edad/sexo
    (`resolver_identidad`).
  - POR-REPORTE: las anclas/markers que identifican ESE reporte. Los dos formatos
    traen banner arriba (el IRIS de formularios, 15 filas) y el encabezado se ubica
    SOLO por el ancla: nunca por un número de fila.

Para ubicar el encabezado se llama directo a `rem_utils.encontrar_fila_encabezado` con
`ANCLA[eje]`. Había un `fila_encabezado_admin` (y un `_fila_encabezado` propio en el A03
y en estamentos) que solo reenviaban: quedaron como envoltorios vacíos cuando la ronda 11
borró los fallbacks posicionales, porque la única diferencia entre formatos es QUÉ ancla
se pasa (ronda 12).
"""

from programas.rem_utils import norm, buscar_col, ArchivoInvalido

# -- Vocabulario del eje (firmas RAYEN estándar del formulario clínico) --
ANCLA_IRIS   = ["AÑO", "APLICACION", "FORMULARIO"]      # encabezado IRIS
ANCLA_ADMIN  = ["EDAD", "REGISTRO", "FORMULARIO"]       # encabezado Administrativo (fila 9)
# Ancla del encabezado POR EJE: lo único que cambia entre formatos al ubicarlo
# (`rem_utils.encontrar_fila_encabezado(ws, ANCLA[eje])`). Un reporte con su propia
# ancla (estamentos, 'Utilización de Cupos') la pasa él.
ANCLA = {"iris": ANCLA_IRIS, "administrativo": ANCLA_ADMIN}
ADMIN_BANNER = "SERVICIO DE SALUD"                      # A1 del Administrativo
ADMIN_MARKERS = ["NUMERO DE FICHAS", "EDAD DE REGISTRO FORMULARIO", "FECHA FORMULARIO"]
MAX_FILAS_HEADER = 60                                   # tope del barrido de firmas


# -- Identidad del paciente (RUT/edad/sexo), aceptando AMBOS formatos --
# QUIRK RAYEN (IRIS): 'AÑO APLICACIÓN FORMULARIO' NO trae el año; trae la EDAD a la
# fecha de LLENADO. En el Administrativo el equivalente es 'Edad de registro
# formulario' ('99 años 12 meses 31 días'; edad_anios lo parsea).
RUT_TOKENS_IRIS   = ["NUMERO", "IDENTIFICACION"]        # IRIS: 'NUMERO TIPO IDENTIFICACION'
RUT_EXACTO_ADMIN  = "RUT"                               # Admin: columna 'RUT' pelada
EDAD_TOKENS_IRIS  = ["AÑO", "APLICACION", "FORMULARIO"]
EDAD_TOKENS_ADMIN = ["EDAD", "REGISTRO", "FORMULARIO"]
SEXO_HEADER = "SEXO"                                    # igual en ambos


def detectar_eje_filas(filas, *, iris_ancla=ANCLA_IRIS, iris_rut=RUT_TOKENS_IRIS,
                       admin_banner=ADMIN_BANNER, admin_markers=ADMIN_MARKERS):
    """Igual que `detectar_eje`, pero sobre FILAS YA LEÍDAS (secuencias de VALORES,
    como las entrega `ws.iter_rows(values_only=True)`), no sobre una hoja openpyxl.

    POR QUÉ existe: las firmas viven en las primeras MAX_FILAS_HEADER filas, así que
    quien solo quiere el formato no necesita el archivo completo. `detectar_eje`
    (abajo) pide una hoja, y para que `ws.max_row` sea confiable esa hoja tiene que
    venir de un `load_workbook` SIN `read_only` — o sea, parsear el export entero.
    Eso es lo que la GUI 2.0 hacía para detectar el formato de un click, y después el
    worker volvía a parsearlo completo para procesarlo: dos lecturas completas por
    corrida. Con las filas por delante, el llamador puede leer solo el encabezado con
    `rem_utils.abrir_xlsx_ro` + `filas_hoja(ws, MAX_FILAS_HEADER)`.

    OJO, no con un `load_workbook(read_only=True)` pelado: en ese modo openpyxl acota
    `iter_rows` a la <dimension> que declara el .xlsx, igual que `max_row`. Con la
    etiqueta rota (`A1`) la fila del encabezado llega con UNA columna y un IRIS valido
    sale 'desconocido' -- fue un bug de la ronda 4 de la revision (sep-2026), que
    habia dado por hecho que el peligro era `max_row` y no `read_only`."""
    filas = list(filas)[:MAX_FILAS_HEADER]
    ancla = [norm(t) for t in iris_ancla]
    rut = [norm(t) for t in (iris_rut or [])]
    ok_ancla = False
    ok_rut = not rut                      # sin tokens de RUT -> no se exige
    normalizadas = [[norm(v) for v in fila] for fila in filas]
    for vals in normalizadas:
        if all(any(tok in v for v in vals) for tok in ancla):
            ok_ancla = True
        if rut and any(all(t in v for t in rut) for v in vals):
            ok_rut = True
    if ok_ancla and ok_rut:
        return "iris"
    a1 = normalizadas[0][0] if (normalizadas and normalizadas[0]) else norm(None)
    if a1 == norm(admin_banner):
        return "administrativo"
    for vals in normalizadas:
        if any(any(norm(m) in v for v in vals) for m in admin_markers):
            return "administrativo"
    return "desconocido"


def detectar_eje(ws, *, iris_ancla=ANCLA_IRIS, iris_rut=RUT_TOKENS_IRIS,
                 admin_banner=ADMIN_BANNER, admin_markers=ADMIN_MARKERS):
    """'iris' | 'administrativo' | 'desconocido' según las firmas del reporte.
    Barrido ÚNICO hasta MAX_FILAS_HEADER. IRIS se confirma por su ancla (y por el
    RUT si se pasan tokens en `iris_rut`; pásalo `None`/`()` para no exigirlo).
    Admin por banner en A1 o por markers. Cada reporte puede pasar sus propias
    firmas; las default sirven al formulario RAYEN estándar (A05, instrumentos).

    Toma una hoja ya abierta (SIN `read_only`, para que `ws.max_row` valga) y
    delega en `detectar_eje_filas`. Si lo único que tienes es la ruta y no
    necesitas el resto del archivo, usa esa otra: ahorra parsear el export entero."""
    tope = min(ws.max_row, MAX_FILAS_HEADER)
    filas = [[c.value for c in ws[r]] for r in range(1, tope + 1)]
    return detectar_eje_filas(filas, iris_ancla=iris_ancla, iris_rut=iris_rut,
                              admin_banner=admin_banner, admin_markers=admin_markers)


# -- Fuente PLENA vs PARCIAL en el grupo pandas (fase 2, sep-2026) ------------
#
# OJO CON EL NOMBRE: esto NO es deteccion de EJE, aunque viva en formatos.py y el
# roadmap lo llamara "fase 2 del eje". Un eje es el MISMO reporte en dos formatos
# (IRIS/Admin), y en el A/D/A eso no existe: **el lado Administrativo no tiene un
# equivalente del A/D/A** (sep-2026, confirmado por el autor). Lo que hay del otro
# lado es OTRO reporte, distinto y mas pobre. Asi que aca no se decide un formato:
# se VERIFICA LA IDENTIDAD DEL REPORTE -- "esto que me diste, ¿es el A/D/A?".
#
# El grupo pandas (atenciones/NSP/grupal/'Otros y Respi') tampoco podria usar
# `detectar_eje`: ese barre una hoja openpyxl buscando el banner y las anclas del
# FORMULARIO clinico, y estos reportes no los traen.
#
# Y por que no basta con mapear columnas: aca no falta una columna, la MISMA
# columna trae menos. En el reporte admin que SI existe ('Monitoreo de Actividades')
# la columna DIAGNOSTICO existe y resuelve perfecto -- solo que viene en TEXTO, sin
# codigo ICD. `resolver_columnas` ve una columna presente y sigue feliz, y los
# indicadores que matchean por codigo (Ira Alta 'j0', Bronquitis 'J20', EPOC
# exacerbado 'J44.1') salen 0 SIN AVISAR. Lo degradado es el CONTENIDO, no la
# presencia, y eso la resolucion de columnas no puede verlo.
#
# COMO se detecta, entonces: NO con una firma positiva del "otro lado", porque no
# hay UN otro lado -- puede llegar el Monitoreo, un archivo editado, o algo que
# RAYEN todavia no inventa. Se prueba que la fuente ES el A/D/A de IRIS, por las
# claves que solo el trae. Fail-safe: lo que no se pruebe, avisa, sin necesidad de
# saber QUE fue lo que llego. Y el mensaje NUNCA dice "bajaste el gemelo
# equivocado": esa eleccion no existe.
#
# La firma son CLAVES CANONICAS, no nombres de columna: el saber de headers vive
# solo en MAPA_ATENCIONES y asi no puede desincronizarse de esto.
#
# EL CONTEO IMPORTA, no es todo-o-nada. Si RAYEN renombra una columna del A/D/A, el
# archivo SIGUE siendo el A/D/A; marcarlo "parcial" seria un falso positivo
# recurrente, y un aviso que grita siempre deja de leerse -- ahi se pierde el
# fail-loud entero. Por eso hay un TERCER desenlace, 'cambiada', que no le habla al
# usuario ("cargaste el archivo equivocado") sino al DEV ("RAYEN movio el piso,
# actualiza el mapeo").

# Claves canonicas presentes SOLO en el A/D/A de IRIS. Verificadas contra los DOS
# archivos versionados: ATENCIONESDIAGNOSTICOSACTIVIDADES_iris.xlsx (45 columnas) y
# Monitoreo_de_Actividades_anonimizado.xlsx (26). Ver MAPA_ATENCIONES en rem_utils.
#
# Son las cinco DEMOGRAFICAS, y no es casualidad: es exactamente lo que el Monitoreo
# no puede dar. Las de identidad/conteo salieron de esta lista al encontrarseles
# equivalente admin (ATENID -> 'N°', PROF -> 'FUNCIONARIO', ANOS_AT -> 'AÑOS').
#
# OJO AL AGREGAR UN EQUIVALENTE ADMIN A MAPA_ATENCIONES: si la clave estaba aca, hay
# que sacarla, o el Monitoreo pasa a clasificar 'cambiada' en vez de 'parcial' y el
# aviso le habla al dev en vez de al usuario. Paso con ATENID (sep-2026).
SOLO_IRIS_ATENCIONES = ("ALERTAS", "PUEBLO", "NACION", "FNAC", "FORMCLIN")

FUENTE_PLENA    = "plena"       # estan todas: es el A/D/A de IRIS completo
FUENTE_CAMBIADA = "cambiada"    # estan algunas: parece el A/D/A pero le faltan
FUENTE_PARCIAL  = "parcial"     # no esta ninguna: no es el A/D/A de IRIS


def clasificar_fuente(col, solo_iris=SOLO_IRIS_ATENCIONES):
    """(estado, claves_ausentes) desde el dict {canonico: columna|None} que
    devuelve `resolver_columnas`. Ver el bloque de arriba para el porque de los
    tres estados."""
    ausentes = [k for k in solo_iris if not col.get(k)]
    if not ausentes:
        return FUENTE_PLENA, []
    return (FUENTE_PARCIAL if len(ausentes) == len(solo_iris)
            else FUENTE_CAMBIADA), ausentes


def aviso_fuente(estado, ausentes, consecuencia, casilla="Fuente de datos", archivos=None):
    """Tupla (casilla, estado, motivo, que_hacer) para la hoja LEEME, o None si la
    fuente es plena. `consecuencia` = que se degrada EN ESE MODULO (lo sabe el
    modulo, no esta capa: al A23 le mata los indicadores por codigo ICD, al SM le
    mata el ATEN ID que es su unidad de conteo). `archivos` = los no-plenos cuando
    se MEZCLARON con plenos (`df.attrs['fuente_mezcla']`): el aviso dice cuales, y
    que lo suyo sale de MENOS (no en 0), porque el resto si trae las columnas."""
    if estado == FUENTE_PLENA:
        return None
    faltan = ", ".join(ausentes)
    mezcla = (f" OJO, afecta SOLO a: {', '.join(archivos)} -- los demas archivos si son "
              f"el IRIS completo, asi que no sale todo en 0: sale de MENOS."
              if archivos else "")
    if estado == FUENTE_PARCIAL:
        return (casilla, "FUENTE PARCIAL",
                f"El archivo no es el export A/D/A de IRIS (no trae NINGUNA de: "
                f"{faltan}). {consecuencia}{mezcla}",
                "Bajar 'Atenciones, Diagnosticos y Actividades' desde IRIS")
    return (casilla, "EXPORT CAMBIADO",
            f"Parece el IRIS pero le faltan columnas que antes traia: {faltan}. "
            f"O RAYEN cambio el export, o el archivo fue editado. {consecuencia}{mezcla}",
            "Avisar al dev: hay que actualizar MAPA_ATENCIONES / SOLO_IRIS_ATENCIONES")


# -- Cruce de reportes: el ADA en la casilla del grupal, o al revés -----
# Las dos casillas de archivo están una al lado de la otra en la pestaña de SM, así
# que cruzarlas es un error de usuario REAL y fácil. Sin esto reventaba con el
# «no reconozco el archivo / faltan columnas» genérico, que no dice lo único útil:
# los cruzaste. Mismo espíritu que el mensaje cruzado de validar_iris/validar_admin
# (§5 de CLAUDE.md) y que la regla §7 «detectar por CONTENIDO, nunca por nombre».
#
# (Para el que venga y crea que el Whitman es decoración: el grupal SÍ contiene
# multitudes -- varias personas por sesión, por eso cuenta por ASISTENCIA -- y el
# ADA es uno a uno, cuenta por ATEN ID. Cruzados, cada uno cuenta lo que no es.
# El chiste se explica acá y no en el mensaje: al usuario se le cuenta, no se le
# disecciona.)
#
# Firmas POSITIVAS de cada reporte, sobre el header CRUDO (no sobre las claves
# canónicas: el resolver del grupal ni siquiera tiene una clave para DIAGNOSTICOS,
# así que desde su dict resuelto el ADA es invisible).
FIRMAS_CRUCE = {
    "ada":    (["DIAGNOSTICO"], ["ATEN", "ID"], ["ALERTAS", "ADMINISTRATIVAS"]),
    "grupal": (["ASISTE"], ["TIPO", "PARTICIPANTE"], ["FUNCIONARIO", "PRESTADOR"],
               ["RUN", "FUNCIONARIO"]),
}
NOMBRE_REPORTE = {
    "ada":    "Atenciones / Diagnosticos / Actividades (ADA)",
    "grupal": "Atenciones Grupales",
}


def parece_reporte(hdr):
    """Qué reporte parece un header CRUDO: 'ada' | 'grupal' | None.
    Cuenta firmas positivas de cada lado; empate (incluido 0-0) -> None, o sea
    'no me consta' — nunca se acusa un cruce sin evidencia."""
    hn = [norm(h) for h in hdr]
    pts = {k: sum(1 for toks in firmas
                  if any(all(norm(t) in h for t in toks) for h in hn))
           for k, firmas in FIRMAS_CRUCE.items()}
    if pts["ada"] == pts["grupal"]:
        return None
    return max(pts, key=pts.get)


def verificar_cruce(hdr, espera, nombre_archivo):
    """Si `hdr` es claramente el OTRO reporte del par ADA/grupal, levanta
    ArchivoInvalido diciéndolo. Si no consta, no hace nada (el llamador sigue con
    su error genérico). `espera` = 'ada' | 'grupal'."""
    otro = parece_reporte(hdr)
    if not otro or otro == espera:
        return
    raise ArchivoInvalido("cruzados", (
        f"Creo que cruzaste los archivos.\n\n"
        f"En la casilla de «{NOMBRE_REPORTE[espera]}» pusiste\n"
        f"«{nombre_archivo}», que parece el reporte de {NOMBRE_REPORTE[otro]}.\n"
        f"Lo mas probable es que el otro este igual de cruzado.\n\n"
        f"    Do I contradict myself?\n"
        f"    Very well then I contradict myself,\n"
        f"    (I am large, I contain multitudes.)\n"
        f"        -- Walt Whitman, «Song of Myself», 51\n\n"
        f"Solucion: intercambia los dos archivos en la pestana."))


def resolver_identidad(headers_norm):
    """(rut_col, edad_col, sexo_col) 1-based, aceptando IRIS y Admin (robusto ante
    una mala elección de formato). None en la posición que no se encuentre."""
    rut = (buscar_col(headers_norm, tokens=[norm(t) for t in RUT_TOKENS_IRIS])
           or buscar_col(headers_norm, exacto=RUT_EXACTO_ADMIN))
    edad = (buscar_col(headers_norm, tokens=[norm(t) for t in EDAD_TOKENS_IRIS])
            or buscar_col(headers_norm, tokens=[norm(t) for t in EDAD_TOKENS_ADMIN]))
    sexo = buscar_col(headers_norm, exacto=SEXO_HEADER)
    return rut, edad, sexo
