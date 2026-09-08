#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# Copyright (C) 2026 Simon Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. Distributed WITHOUT ANY WARRANTY. See the GNU
# General Public License for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
Fase 2 del eje de formatos: clasificar la FUENTE del grupo pandas.

Lo que se protege acá es la distincion de TRES estados. Dos serian suficientes
para atajar el Monitoreo Admin, pero dejarian un falso positivo permanente el dia
que RAYEN renombre una columna del IRIS -- y un aviso que grita siempre deja de
leerse, que es como se pierde el fail-loud.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from programas import formatos
from programas.rem_utils import (leer_xlsx, resolver_columnas, MAPA_ATENCIONES, norm,
                                 cargar_canonico)

RAIZ = Path(__file__).resolve().parent.parent
ADA_IRIS = RAIZ / "refs_tablas" / "ATENCIONESDIAGNOSTICOSACTIVIDADES_iris.xlsx"
MONITOREO = RAIZ / "refs_tablas" / "Monitoreo_de_Actividades_anonimizado.xlsx"

TODAS = formatos.SOLO_IRIS_ATENCIONES


def _col(presentes):
    """Simula el {canonico: columna|None} de resolver_columnas."""
    return {k: (f"col_{k}" if k in presentes else None) for k in TODAS}


# -- Los tres estados ---------------------------------------------------------

def test_todas_las_claves_presentes_es_fuente_plena():
    estado, ausentes = formatos.clasificar_fuente(_col(TODAS))
    assert estado == formatos.FUENTE_PLENA
    assert ausentes == []


def test_ninguna_clave_es_fuente_parcial():
    estado, ausentes = formatos.clasificar_fuente(_col([]))
    assert estado == formatos.FUENTE_PARCIAL
    assert set(ausentes) == set(TODAS)


def test_algunas_claves_es_export_cambiado_no_parcial():
    """RAYEN renombra UNA columna del IRIS: el archivo SIGUE siendo el IRIS pleno.
    Marcarlo 'parcial' seria un falso positivo recurrente -> estado propio."""
    estado, ausentes = formatos.clasificar_fuente(_col(TODAS[1:]))
    assert estado == formatos.FUENTE_CAMBIADA
    assert ausentes == [TODAS[0]]


def test_cambiada_aunque_falte_casi_todo_menos_una():
    """El limite inferior de 'cambiada': con UNA sola clave viva no es 'parcial'."""
    estado, _ = formatos.clasificar_fuente(_col([TODAS[0]]))
    assert estado == formatos.FUENTE_CAMBIADA


# -- El aviso que llega a la hoja LEEME ---------------------------------------

def test_fuente_plena_no_genera_aviso():
    assert formatos.aviso_fuente(formatos.FUENTE_PLENA, [], "lo que sea") is None


def test_aviso_parcial_apunta_al_usuario():
    av = formatos.aviso_fuente(formatos.FUENTE_PARCIAL, list(TODAS), "CONSECUENCIA X")
    casilla, estado, motivo, que_hacer = av
    assert estado == "FUENTE PARCIAL"
    assert "CONSECUENCIA X" in motivo
    assert "IRIS" in que_hacer          # la accion es del usuario: bajar el otro export


def test_aviso_cambiado_apunta_al_dev():
    """Distinto destinatario: no es 'cargaste el archivo equivocado', es
    'RAYEN movio el piso'."""
    av = formatos.aviso_fuente(formatos.FUENTE_CAMBIADA, ["ATENID"], "CONSECUENCIA Y")
    _casilla, estado, motivo, que_hacer = av
    assert estado == "EXPORT CAMBIADO"
    assert "ATENID" in motivo
    assert "dev" in que_hacer.lower()


def test_el_aviso_tiene_la_forma_que_espera_la_hoja_leeme():
    av = formatos.aviso_fuente(formatos.FUENTE_PARCIAL, ["ATENID"], "x")
    assert len(av) == 4 and all(isinstance(p, str) for p in av)


# -- Contra el export IRIS REAL (no una maqueta) ------------------------------

@pytest.mark.skipif(not ADA_IRIS.exists(), reason="falta el export IRIS de ejemplo")
def test_el_ada_iris_real_clasifica_como_plena():
    """Guardarrail anti-falso-positivo: el export IRIS versionado tiene que dar
    'plena'. Si este test se cae, la firma se desincronizo del export real."""
    hdr, _filas = leer_xlsx(ADA_IRIS)
    col = resolver_columnas(hdr, MAPA_ATENCIONES)
    estado, ausentes = formatos.clasificar_fuente(col)
    assert estado == formatos.FUENTE_PLENA, f"claves no resueltas: {ausentes}"


@pytest.mark.skipif(not ADA_IRIS.exists(), reason="falta el export IRIS de ejemplo")
def test_cargar_canonico_deja_el_veredicto_en_attrs():
    d, _col = cargar_canonico(ADA_IRIS, None,
                              lambda h: resolver_columnas(h, MAPA_ATENCIONES),
                              solo_iris=formatos.SOLO_IRIS_ATENCIONES,
                              log=lambda *a, **k: None)
    assert d.attrs["fuente"][0] == formatos.FUENTE_PLENA


@pytest.mark.skipif(not MONITOREO.exists(), reason="falta el Monitoreo de ejemplo")
def test_el_monitoreo_real_clasifica_como_parcial():
    """El otro extremo, contra el archivo REAL (header-only, sep-2026): el
    'Monitoreo de Actividades' del eje Administrativo tiene que dar 'parcial', con
    las CINCO claves demograficas ausentes. Es la contraparte del test del ADA IRIS: uno protege
    contra falsos positivos, este contra falsos negativos."""
    hdr, _filas = leer_xlsx(MONITOREO)
    col = resolver_columnas(hdr, MAPA_ATENCIONES)
    estado, ausentes = formatos.clasificar_fuente(col)
    assert estado == formatos.FUENTE_PARCIAL
    assert set(ausentes) == set(TODAS)


@pytest.mark.skipif(not MONITOREO.exists(), reason="falta el Monitoreo de ejemplo")
def test_el_monitoreo_igual_pasa_las_requeridas_de_cargar_atenciones():
    """Por esto el bug era SILENCIOSO y no un ArchivoInvalido: el Monitoreo resuelve
    TODAS las columnas requeridas, asi que cargaba sin chistar. Lo que faltaba no
    tenia guardia. Si algun dia esto empieza a fallar, `requeridas` cambio y hay que
    revisar si el camino admin del A23 sigue vivo."""
    hdr, _filas = leer_xlsx(MONITOREO)
    col = resolver_columnas(hdr, MAPA_ATENCIONES)
    for k in ("RUN", "FECHA", "ACT", "DIAG", "INSTR", "TIPO"):
        assert col.get(k), f"{k} dejo de resolver en el Monitoreo"


# -- Equivalencias admin encontradas con la muestra (v1.9.3) ------------------

@pytest.mark.skipif(not ADA_IRIS.exists(), reason="falta el export IRIS de ejemplo")
def test_en_iris_la_edad_del_rem_nunca_cae_al_anos_pelado():
    """GUARDARRAIL de la trampa semantica: 'AÑOS' significa cosas DISTINTAS en los
    dos reportes (IRIS = edad a la DESCARGA; Monitoreo = edad a la ATENCION). El
    mapa resuelve por orden, asi que en IRIS debe ganar SIEMPRE 'AÑOS ATENCION'.
    Si RAYEN lo renombrara, el fallback daria edad-a-la-descarga en silencio: este
    test es lo unico que lo atrapa."""
    col = resolver_columnas(leer_xlsx(ADA_IRIS)[0], MAPA_ATENCIONES)
    assert "ATENCION" in norm(col["ANOS_AT"]), col["ANOS_AT"]
    assert norm(col["ANOS_AT"]) != norm(col["ANOS"])   # no son la misma columna


@pytest.mark.skipif(not MONITOREO.exists(), reason="falta el Monitoreo de ejemplo")
def test_en_el_monitoreo_las_equivalencias_admin_resuelven():
    """El Monitoreo no tiene ATEN ID ni 'AÑOS ATENCION', pero SI equivalentes:
    'N°' agrupa las filas de una atencion, y su 'AÑOS' ya es a la atencion
    (confirmado por el autor contra enero-2026)."""
    col = resolver_columnas(leer_xlsx(MONITOREO)[0], MAPA_ATENCIONES)
    assert col["ATENID"] == "N°"
    assert norm(col["ANOS_AT"]) == norm("AÑOS")
    assert col["PROF"] == "FUNCIONARIO"


@pytest.mark.skipif(not MONITOREO.exists(), reason="falta el Monitoreo de ejemplo")
def test_atenid_del_monitoreo_no_entra_en_la_firma_iris():
    """Al darle equivalente admin a ATENID hubo que sacarlo de SOLO_IRIS_ATENCIONES:
    si no, el Monitoreo clasificaria 'cambiada' (mensaje para el dev) en vez de
    'parcial' (mensaje para el usuario)."""
    assert "ATENID" not in formatos.SOLO_IRIS_ATENCIONES
    col = resolver_columnas(leer_xlsx(MONITOREO)[0], MAPA_ATENCIONES)
    assert formatos.clasificar_fuente(col)[0] == formatos.FUENTE_PARCIAL


def test_el_correlativo_se_namespacea_por_archivo(tmp_path):
    """El 'N°' del Monitoreo REINICIA en 1 en cada export. Al concatenar dos
    archivos, dos atenciones distintas compartirian id y el conteo por-atencion
    subcontaria EN SILENCIO. Deben quedar 4 ids distintos, no 2."""
    import openpyxl
    from programas.rem_utils import ATENID_CORRELATIVO
    paths = []
    for n in ("ene.xlsx", "feb.xlsx"):
        wb = openpyxl.Workbook(); ws = wb.active
        ws.append([ATENID_CORRELATIVO, "RUN", "FECHA CONSULTA",
                   "ACTIVIDAD Y/O PROCEDIMIENTO", "DIAGNOSTICO", "INSTRUMENTO",
                   "TIPO DE ATENCION"])
        for i in (1, 2):        # el MISMO correlativo en los dos archivos
            ws.append([i, "11111111-1", "01/01/2026", "act", "dx", "Medico", "Esp"])
        p = tmp_path / n; wb.save(p); paths.append(p)

    d, _col = cargar_canonico(list(paths), None,
                              lambda h: resolver_columnas(h, MAPA_ATENCIONES),
                              log=lambda *a, **k: None)
    assert d["ATENID"].nunique() == 4, "dos atenciones distintas se fusionaron"
    assert all("|" in v for v in d["ATENID"])


def test_el_aten_id_de_iris_NO_se_namespacea(tmp_path):
    """Contrapartida: el ATEN ID de IRIS es global y unico, asi que si el mismo
    aparece en dos exports que se solapan tiene que DEDUPLICAR, no contarse dos
    veces. Namespacearlo romperia eso."""
    import openpyxl
    paths = []
    for n in ("a.xlsx", "b.xlsx"):
        wb = openpyxl.Workbook(); ws = wb.active
        ws.append(["ATEN ID", "NUMERO TIPO IDENTIFICACION", "FECHA ATENCION",
                   "ACTIVIDADES", "DIAGNOSTICOS", "INSTRUMENTO", "TIPO ATENCION"])
        ws.append([9001, "11111111-1", "01/01/2026", "act", "dx", "Medico", "Esp"])
        p = tmp_path / n; wb.save(p); paths.append(p)

    d, _col = cargar_canonico(list(paths), None,
                              lambda h: resolver_columnas(h, MAPA_ATENCIONES),
                              log=lambda *a, **k: None)
    assert d["ATENID"].nunique() == 1, "el ATEN ID global no debe namespacearse"


def test_sin_solo_iris_no_clasifica_nada():
    """Compatibilidad: los cargadores que no pasan `solo_iris` siguen igual."""
    d, _col = cargar_canonico(ADA_IRIS, None,
                              lambda h: resolver_columnas(h, MAPA_ATENCIONES),
                              log=lambda *a, **k: None)
    assert "fuente" not in d.attrs


@pytest.mark.skipif(not ADA_IRIS.exists(), reason="falta el export IRIS de ejemplo")
def test_fuente_parcial_se_loguea_ruidosa():
    """No basta con dejarlo en attrs: tiene que salir por el log (fail-loud)."""
    dicho = []
    cargar_canonico(ADA_IRIS, None,
                    lambda h: {k: None for k in TODAS} | {"RUN": "RUN"},
                    solo_iris=TODAS, log=lambda m: dicho.append(str(m)))
    assert any("PARCIAL" in m for m in dicho)
