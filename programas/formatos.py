#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.7.10
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
  - IRIS          → export pleno (códigos ICD, demografía, columnas completas).
  - Administrativo → mismo dato, PARCIAL (banner 'Servicio de Salud', header más
    abajo, sin varias columnas). El Monitoreo Admin de atenciones es aún más pobre.

Este módulo NO es de ninguna sección del REM. Es la capa que reconoce y ubica ese
eje, compartida por CASI TODOS los módulos con entrada RAYEN. Cada reporte aporta
sus PROPIAS firmas (anclas/markers que lo identifican) como configuración local;
el MECANISMO (barrer la hoja, decidir el eje, resolver identidad, ubicar header
por eje) vive acá una sola vez.

  rem_utils (primitivas de celda: norm, buscar_col, encontrar_fila_encabezado)
      ↑
  formatos (este módulo: eje IRIS/Admin)
      ↑
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

# ── Vocabulario del eje (firmas RAYEN estándar del formulario clínico) ──
ANCLA_IRIS   = ["AÑO", "APLICACION", "FORMULARIO"]      # encabezado IRIS
ANCLA_ADMIN  = ["EDAD", "REGISTRO", "FORMULARIO"]       # encabezado Administrativo (fila 9)
ADMIN_BANNER = "SERVICIO DE SALUD"                      # A1 del Administrativo
ADMIN_MARKERS = ["NUMERO DE FICHAS", "EDAD DE REGISTRO FORMULARIO", "FECHA FORMULARIO"]
MAX_FILAS_HEADER = 60                                   # tope del barrido de firmas

# Params de localización de encabezado del lado ADMIN. TRANSVERSAL: mismo banner
# (col A con blancos → no fiarse del blanco; header en fila 9 = n_hardcode+1 como
# último recurso) en A05, A03 y 'Utilización de Cupos'. El lado IRIS varía por
# reporte, así que cada perfil define su propio n_hardcode.
HEADER_ADMIN = dict(usar_blanco_en_a=False, n_hardcode=8)

# ── Identidad del paciente (RUT/edad/sexo), aceptando AMBOS formatos ──
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
    ok_rut = not rut                      # sin tokens de RUT → no se exige
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
