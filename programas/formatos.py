#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.9.2
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
  - COMPARTIDO: vocabulario del eje (banner/markers/tokens de identidad), la lógica
    `detectar_eje`, la resolución RUT/edad/sexo (`resolver_identidad`) y los params
    de encabezado del lado ADMIN (mismo banner-layout en A05/A03/Utilización de Cupos).
  - POR-REPORTE: las anclas/markers que identifican ESE reporte y los params de
    encabezado del lado IRIS (varían: A05 con banner de 16 filas, instrumentos con 0).
"""

from programas.rem_utils import norm, buscar_col, encontrar_fila_encabezado

# -- Vocabulario del eje (firmas RAYEN estándar del formulario clínico) --
ANCLA_IRIS   = ["AÑO", "APLICACION", "FORMULARIO"]      # encabezado IRIS
ANCLA_ADMIN  = ["EDAD", "REGISTRO", "FORMULARIO"]       # encabezado Administrativo (fila 9)
ADMIN_BANNER = "SERVICIO DE SALUD"                      # A1 del Administrativo
ADMIN_MARKERS = ["NUMERO DE FICHAS", "EDAD DE REGISTRO FORMULARIO", "FECHA FORMULARIO"]
MAX_FILAS_HEADER = 60                                   # tope del barrido de firmas

# Params de localización de encabezado del lado ADMIN. TRANSVERSAL: mismo banner
# (col A con blancos -> no fiarse del blanco; header en fila 9 = n_hardcode+1 como
# último recurso) en A05, A03 y 'Utilización de Cupos'. El lado IRIS varía por
# reporte, así que cada perfil define su propio n_hardcode.
HEADER_ADMIN = dict(usar_blanco_en_a=False, n_hardcode=8)

# -- Identidad del paciente (RUT/edad/sexo), aceptando AMBOS formatos --
# QUIRK RAYEN (IRIS): 'AÑO APLICACIÓN FORMULARIO' NO trae el año; trae la EDAD a la
# fecha de LLENADO. En el Administrativo el equivalente es 'Edad de registro
# formulario' ('99 años 12 meses 31 días'; edad_anios lo parsea).
RUT_TOKENS_IRIS   = ["NUMERO", "IDENTIFICACION"]        # IRIS: 'NUMERO TIPO IDENTIFICACION'
RUT_EXACTO_ADMIN  = "RUT"                               # Admin: columna 'RUT' pelada
EDAD_TOKENS_IRIS  = ["AÑO", "APLICACION", "FORMULARIO"]
EDAD_TOKENS_ADMIN = ["EDAD", "REGISTRO", "FORMULARIO"]
SEXO_HEADER = "SEXO"                                    # igual en ambos


def detectar_eje(ws, *, iris_ancla=ANCLA_IRIS, iris_rut=RUT_TOKENS_IRIS,
                 admin_banner=ADMIN_BANNER, admin_markers=ADMIN_MARKERS):
    """'iris' | 'administrativo' | 'desconocido' según las firmas del reporte.
    Barrido ÚNICO hasta MAX_FILAS_HEADER. IRIS se confirma por su ancla (y por el
    RUT si se pasan tokens en `iris_rut`; pásalo `None`/`()` para no exigirlo).
    Admin por banner en A1 o por markers. Cada reporte puede pasar sus propias
    firmas; las default sirven al formulario RAYEN estándar (A05, instrumentos)."""
    tope = min(ws.max_row, MAX_FILAS_HEADER)
    ancla = [norm(t) for t in iris_ancla]
    rut = [norm(t) for t in (iris_rut or [])]
    ok_ancla = False
    ok_rut = not rut                      # sin tokens de RUT -> no se exige
    for r in range(1, tope + 1):
        vals = [norm(c.value) for c in ws[r]]
        if all(any(tok in v for v in vals) for tok in ancla):
            ok_ancla = True
        if rut and any(all(t in v for t in rut) for v in vals):
            ok_rut = True
    if ok_ancla and ok_rut:
        return "iris"
    if norm(ws.cell(row=1, column=1).value) == norm(admin_banner):
        return "administrativo"
    for r in range(1, tope + 1):
        vals = [norm(c.value) for c in ws[r]]
        if any(any(norm(m) in v for v in vals) for m in admin_markers):
            return "administrativo"
    return "desconocido"


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

# Claves canonicas presentes SOLO en el export IRIS pleno de atenciones.
# Verificadas contra refs_tablas/ATENCIONESDIAGNOSTICOSACTIVIDADES_iris.xlsx
# (45 columnas, sep-2026). Ver MAPA_ATENCIONES en rem_utils.
SOLO_IRIS_ATENCIONES = ("ATENID", "ALERTAS", "PUEBLO", "NACION", "FNAC", "FORMCLIN")

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


def aviso_fuente(estado, ausentes, consecuencia, casilla="Fuente de datos"):
    """Tupla (casilla, estado, motivo, que_hacer) para la hoja LEEME, o None si la
    fuente es plena. `consecuencia` = que se degrada EN ESE MODULO (lo sabe el
    modulo, no esta capa: al A23 le mata los indicadores por codigo ICD, al SM le
    mata el ATEN ID que es su unidad de conteo)."""
    if estado == FUENTE_PLENA:
        return None
    faltan = ", ".join(ausentes)
    if estado == FUENTE_PARCIAL:
        return (casilla, "FUENTE PARCIAL",
                f"El archivo no es el export A/D/A de IRIS (no trae NINGUNA de: "
                f"{faltan}). {consecuencia}",
                "Bajar 'Atenciones, Diagnosticos y Actividades' desde IRIS")
    return (casilla, "EXPORT CAMBIADO",
            f"Parece el IRIS pero le faltan columnas que antes traia: {faltan}. "
            f"O RAYEN cambio el export, o el archivo fue editado. {consecuencia}",
            "Avisar al dev: hay que actualizar MAPA_ATENCIONES / SOLO_IRIS_ATENCIONES")


def fila_encabezado_admin(ws, ancla=ANCLA_ADMIN, max_filas=MAX_FILAS_HEADER):
    """Ubica el encabezado en un export ADMINISTRATIVO con los params compartidos
    (`HEADER_ADMIN`). `ancla` por si el reporte tiene su propia (ej. 'Utilización
    de Cupos' usa Profesional/Instrumento). Devuelve (fila_idx, modo)."""
    return encontrar_fila_encabezado(ws, ancla, HEADER_ADMIN["usar_blanco_en_a"],
                                     HEADER_ADMIN["n_hardcode"], max_filas)


def resolver_identidad(headers_norm):
    """(rut_col, edad_col, sexo_col) 1-based, aceptando IRIS y Admin (robusto ante
    una mala elección de formato). None en la posición que no se encuentre."""
    rut = (buscar_col(headers_norm, tokens=[norm(t) for t in RUT_TOKENS_IRIS])
           or buscar_col(headers_norm, exacto=RUT_EXACTO_ADMIN))
    edad = (buscar_col(headers_norm, tokens=[norm(t) for t in EDAD_TOKENS_IRIS])
            or buscar_col(headers_norm, tokens=[norm(t) for t in EDAD_TOKENS_ADMIN]))
    sexo = buscar_col(headers_norm, exacto=SEXO_HEADER)
    return rut, edad, sexo
