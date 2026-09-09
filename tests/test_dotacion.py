#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Sonnet 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# SPDX-License-Identifier: GPL-3.0-or-later
# ==========================================================================
"""
Pruebas de la separación interno/externo (programas/dotacion.py) + su wiring
en modulos/rem_sm_actividades.py (docs/dotacion_externos_plan.md §5).
Datos SINTÉTICOS. Correr: python tests/test_dotacion.py
"""

import sys
import tempfile
from datetime import date
from pathlib import Path

import openpyxl
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from programas import dotacion as dot          # noqa: E402
import modulos.rem_sm_actividades as sm         # noqa: E402

_TMP = Path(tempfile.mkdtemp(prefix="autorem_dot_"))


def _quiet(*_a, **_k):
    pass


def _tabla_vacia():
    return {"funcionarios": {}, "omitidos": {}}


# ======================================================================
# 1. clase()
# ======================================================================
def test_clase_desconocido_por_default_y_normalizado():
    tabla = {"funcionarios": {"JUAN PEREZ SOTO": "externo"}, "omitidos": {}}
    assert dot.clase("nadie que no existe", tabla) == "desconocido"
    assert dot.clase("Juan Pérez Soto", tabla) == "externo"      # tildes/mayúsc.
    assert dot.clase("  juan   perez soto  ", tabla) == "externo"  # espacios
    assert dot.clase("", tabla) == "desconocido"
    assert dot.clase(None, tabla) == "desconocido"


# ======================================================================
# 2. nuevos() — first-run devuelve TODOS, sin duplicados, orden de aparición
# ======================================================================
def test_nuevos_first_run_devuelve_todos():
    ada = pd.DataFrame({
        "PROF": ["Ana Soto", "Beto Ruiz", "Ana Soto", "Carla Diaz"],
        "INSTR": ["Psicólogo(a)", "Kinesiólogo(a)", "Psicólogo(a)", "Médico"],
        "ACT": ["Controles Salud Mental"] * 4,
        "SECTOR": ["Rojo"] * 4,
    })
    ev = dot.evidencia(ada, modulo="sm")
    assert set(ev["funcionario"]) == {"Ana Soto", "Beto Ruiz", "Carla Diaz"}
    n = dot.nuevos(ev, _tabla_vacia(), "sm")
    assert set(n["funcionario"]) == {"Ana Soto", "Beto Ruiz", "Carla Diaz"}
    assert len(n) == len(n["funcionario"].unique())    # sin duplicados


# ======================================================================
# 3. marcar() persiste y cargar() recupera; caché corrupto -> {} sin excepción
# ======================================================================
def test_marcar_persiste_y_cache_corrupto_no_revienta():
    dot.RUTA_CACHE = _TMP / "cache_dot.json"    # no ensuciar el HOME real
    if dot.RUTA_CACHE.exists():
        dot.RUTA_CACHE.unlink()
    tabla = dot.cargar(log=_quiet)
    assert tabla == _tabla_vacia()
    dot.marcar(tabla, {"Juan Perez": True, "Ana Soto": False})
    t2 = dot.cargar(log=_quiet)
    assert dot.clase("juan perez", t2) == "externo"
    assert dot.clase("ana soto", t2) == "interno"

    dot.RUTA_CACHE.write_text("{ esto no es json valido", encoding="utf-8")
    t3 = dot.cargar(log=_quiet)     # no debe reventar
    assert t3 == _tabla_vacia()


# ======================================================================
# 4. en_rem con 'desconocido' es True (§1.3, el test que fija la decisión)
# ======================================================================
def test_en_rem_desconocido_es_true():
    s = pd.Series(["interno", "externo", "desconocido"])
    assert list(dot.en_rem(s)) == [True, False, True]


# ======================================================================
# 5. Caso mixto (§4.2): "A · B" -> clasificacion del EVENTO
# ======================================================================
def test_clasificar_evento_caso_mixto():
    tabla = dot.marcar(_tabla_vacia(), {"A interno": False, "B externo": True})
    ce = sm.clasificar_evento
    assert ce("A interno · B externo", tabla) == "interno"        # 1 interno basta
    assert ce("B externo · B externo", tabla) == "externo"        # ambos externos
    assert ce("B externo · Nadie Sabe", tabla) == "externo"       # externo + desconocido
    assert ce("A interno · Nadie Sabe", tabla) == "interno"       # interno + desconocido
    assert ce("Nadie Sabe · Otro Mas", tabla) == "desconocido"    # solo desconocidos
    assert ce("", tabla) == "desconocido"                         # sin funcionario


# ======================================================================
# 6. Wiring en sm_actividades: Externos_Delta cuadra + SM_Detalle conserva
#    las filas externas
# ======================================================================
_ADA_HDR = ["NUMERO TIPO IDENTIFICACION", "ATEN ID", "FECHA ATENCION", "ACTIVIDADES",
            "DIAGNOSTICOS", "INSTRUMENTO", "TIPO ATENCION", "SEXO", "AÑOS ATENCION",
            "PROFESIONAL ATENCION"]
_K = {"run": 0, "id": 1, "fecha": 2, "act": 3, "dg": 4, "instr": 5, "tipo": 6,
      "sexo": 7, "edad": 8, "prof": 9}


def _mk_ada(rows, nombre="ada_dot.xlsx"):
    p = _TMP / nombre
    wb = openpyxl.Workbook(); ws = wb.active
    ws.append(_ADA_HDR)
    for r in rows:
        line = [""] * len(_ADA_HDR)
        for k, v in r.items():
            line[_K[k]] = v
        ws.append(line)
    wb.save(p)
    return p


def test_externos_delta_y_detalle_conserva_filas():
    tabla = dot.marcar(_tabla_vacia(), {"Func Externa": True, "Func Interna": False})
    dot.guardar(tabla, log=_quiet)
    ada = _mk_ada([
        {"run": "A", "id": "1", "fecha": date(2026, 7, 3), "act": "Controles Salud Mental  ;",
         "instr": "Médico", "edad": 30, "prof": "Func Interna"},
        {"run": "B", "id": "2", "fecha": date(2026, 7, 4), "act": "Controles Salud Mental  ;",
         "instr": "Psicólogo(a)", "edad": 20, "prof": "Func Externa"},
        {"run": "C", "id": "3", "fecha": date(2026, 7, 5), "act": "Controles Salud Mental  ;",
         "instr": "Psicólogo(a)", "edad": 25, "prof": "Sin Clasificar"},
    ])
    E = sm.procesar(ada, mes=(2026, 7), log=_quiet, dotacion_tabla=tabla)
    assert set(E.loc[E["funcionario"] == "Func Externa", "externo"]) == {"externo"}
    assert set(E.loc[E["funcionario"] == "Func Interna", "externo"]) == {"interno"}
    assert set(E.loc[E["funcionario"] == "Sin Clasificar", "externo"]) == {"desconocido"}
    # SM_Detalle conserva TODAS las filas (§1.4: marcar, no borrar)
    assert len(E) == 3
    # Externos_Delta: Total == Externos + REM por casilla
    delta = E.attrs["tablas"]["Externos_Delta"]
    fila_a06 = delta[delta["Casilla"].str.startswith("A06")].iloc[0]
    assert fila_a06["Total"] == fila_a06["Externos"] + fila_a06["REM"]
    assert fila_a06["Total"] == 3 and fila_a06["Externos"] == 1 and fila_a06["REM"] == 2
    # las tablas de sección (SM_Resumen incl.) se calculan SOLO sobre en_rem
    resumen = E.attrs["tablas"]["SM_Resumen"]
    fila_r = resumen[resumen["Casilla"].str.startswith("A06")].iloc[0]
    assert fila_r["Total mes"] == 2   # sin la externa
    # La hoja LEEME tiene que DECIR que se excluyo gente a proposito: es lo unico
    # que la herramienta efectivamente saco de las tablas, y sin ese aviso el mes
    # que alguien cuadre contra RAYEN ve una diferencia sin explicacion.
    avisos = E.attrs["avisos"]
    exc = [a for a in avisos if "EXCLUIDAS" in a[0].upper()]
    assert len(exc) == 1, f"falta el aviso de exclusion en LEEME: {[a[0] for a in avisos]}"
    assert "1 atencion" in exc[0][2] and "externo" in " ".join(exc[0]).lower()


# ======================================================================
# 7. Omisión por módulo: omitir en "sm" no afecta a "a23"
# ======================================================================
def test_omision_es_por_modulo():
    tabla = _tabla_vacia()
    dot.omitir(tabla, "sm", ["Kinesiólogo(a)"])
    ada = pd.DataFrame({
        "PROF": ["Kine Uno"], "INSTR": ["Kinesiólogo(a)"],
        "ACT": ["Curacion"], "SECTOR": ["Rojo"],
    })
    ev = dot.evidencia(ada, modulo="sm")
    assert len(dot.nuevos(ev, tabla, "sm")) == 0        # omitido en sm -> no pregunta
    assert len(dot.nuevos(ev, tabla, "a23")) == 1        # a23 no lo omitió -> sigue preguntando


# ======================================================================
# 8. Un omitido NO queda 'interno'
# ======================================================================
def test_omitido_no_queda_interno():
    tabla = _tabla_vacia()
    dot.omitir(tabla, "sm", ["Kinesiólogo(a)"])
    assert dot.clase("Kine Uno", tabla) == "desconocido"
    s = pd.Series(["desconocido"])
    assert list(dot.en_rem(s)) == [True]                # sigue contando al REM


def _main():
    pruebas = [v for k, v in sorted(globals().items())
               if k.startswith("test_") and callable(v)]
    fallos = 0
    for fn in pruebas:
        try:
            fn(); print(f"PASS  {fn.__name__}")
        except AssertionError as e:
            fallos += 1; print(f"FAIL  {fn.__name__} -> {e or 'assert'}")
        except Exception as e:  # noqa: BLE001
            import traceback
            fallos += 1; print(f"ERROR {fn.__name__} -> {type(e).__name__}: {e}")
            traceback.print_exc()
    print("-" * 50)
    print(f"{len(pruebas) - fallos}/{len(pruebas)} OK" + (f" ({fallos} problemas)" if fallos else ""))
    return 1 if fallos else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(_main())
