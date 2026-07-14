#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# ==========================================================================
"""
Pruebas del módulo de screening A03 D.3 (PSC/PSC-Y/GHQ-12). Datos SINTÉTICOS.

Correr:  python tests/test_screening.py   (o  pytest tests/)
Cubre: clasificadores, detección de instrumento por contenido, ambos formatos
(IRIS/Admin), los dos resultados (automático vs DISAM) + discrepancia, estamento,
edad en texto, y el rechazo de un export que no es de instrumentos.
"""

import sys
import tempfile
from pathlib import Path

import openpyxl

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

import modulos.rem_a03_d3_instrumentos as scr   # noqa: E402

_TMP = Path(tempfile.mkdtemp(prefix="autorem_scr_"))


# ── Fixtures ──────────────────────────────────────────────────────────
def _iris(fn, formulario, filas):
    """Export IRIS de instrumento: encabezado en fila 1 + filas de datos.
    `filas` = lista de (rut, edad, sexo, funcionario, estamento, estado, puntaje, resultado)."""
    p = _TMP / fn
    wb = openpyxl.Workbook(); ws = wb.active
    ws.append(["NUMERO TIPO IDENTIFICACION", "AÑO APLICACIÓN FORMULARIO", "SEXO",
               "FUNCIONARIO", "INSTRUMENTO", "FORMULARIO", "1.- ESTADO",
               "14.- PUNTAJE", "15.- RESULTADO"])
    for rut, edad, sexo, func, estam, estado, punt, resu in filas:
        ws.append([rut, edad, sexo, func, estam, formulario, estado, punt, resu])
    wb.save(p)
    return p


def _admin(fn, formulario, filas):
    """Export Administrativo: banner + encabezado fila 9. Sin columna estamento.
    `filas` = lista de (rut, edad_txt, sexo, funcionario, estado, puntaje, resultado)."""
    p = _TMP / fn
    wb = openpyxl.Workbook(); ws = wb.active
    ws.append(["Servicio de Salud", "S.S. Metropolitano Central"])
    ws.append(["Comuna", "Maipu"]); ws.append(["Establecimiento", "[CESFAM] Dr. Luis Ferrada"])
    ws.append(["Año", "2026"]); ws.append(["Mes", "ENERO - JULIO"])
    ws.append([None, None, "Reporte Formularios RAYEN"])
    ws.append([None, None, f"Formulario: {formulario}"])
    ws.append([])
    ws.append(["RUT", "Numero de Fichas", "Paciente", "Edad de registro formulario",
               "Sexo", "Funcionario", "1.- Estado", "40.- Puntaje", "41.- Resultado"])
    for rut, edad, sexo, func, estado, punt, resu in filas:
        ws.append([rut, "F", "", edad, sexo, func, estado, punt, resu])
    wb.save(p)
    return p


def _dump(path):
    # Lectura por índice de columna (robusto: las celdas vacías vuelven como None
    # y no desalinean la fila como sí puede pasar con iter_rows).
    ws = openpyxl.load_workbook(path)[scr.NOMBRE_HOJA_SALIDA]
    ncol = ws.max_column
    head = [ws.cell(row=1, column=c).value for c in range(1, ncol + 1)]
    rows = [{head[c - 1]: ws.cell(row=r, column=c).value for c in range(1, ncol + 1)}
            for r in range(2, ws.max_row + 1)]
    return head, rows


def _quiet(*_a, **_k):
    pass


# ── Pruebas ───────────────────────────────────────────────────────────
def test_clasificadores():
    assert scr.clasificar_psc(None) is None          # sin puntaje -> None
    assert scr.clasificar_psc(0) == "Sin riesgo"     # <33: bajo el corte (lo más común)
    assert scr.clasificar_psc(32) == "Sin riesgo"
    assert scr.clasificar_psc(33) == "Bajo"
    assert scr.clasificar_psc(63) == "Bajo"
    assert scr.clasificar_psc(64) == "Medio"
    assert scr.clasificar_psc(70) == "Alto"
    assert scr.clasificar_ghq12(4) == "Bajo"         # GHQ no tiene 'sin riesgo': 0-4 ya es Bajo
    assert scr.clasificar_ghq12(6) == "Medio"
    assert scr.clasificar_ghq12(12) == "Alto"
    assert scr.clasificar_ghq12(None) is None


def test_psc_bajo_el_corte_se_etiqueta():
    """Un PSC <33 (el resultado MÁS común) no se pierde: sale 'Sin riesgo',
    se cuenta en el total y aparece en el desglose por_resultado."""
    p = _iris("psc_bajo.xlsx", "Cuestionario para padres PSC", [
        ("55555555-5", 8, "Hombre", "F", "Médico", "Ingreso", 20, "Sin riesgo"),
    ])
    out = _TMP / "psc_bajo_out.xlsx"
    res = scr.procesar(p, out, log=_quiet)
    assert res["total"] == 1                          # NO se descarta
    assert res["por_resultado"].get("Sin riesgo") == 1
    _, filas = _dump(out)
    assert filas[0]["Resultado_DISAM"] == "Sin riesgo"
    assert filas[0]["Discrepancia"] in (None, "")     # RAYEN también 'Sin riesgo' -> coinciden


def test_iris_goldberg_dos_resultados():
    p = _iris("gold.xlsx", "Cuestionario de Salud de Goldberg", [
        ("11111111-1", 30, "Hombre", "Func Uno", "Psicólogo(a)", "Ingreso", 8, "Alto"),
        ("22222222-2", 40, "Mujer",  "Func Dos", "Médico",       "Egreso",  3, "Medio"),  # RAYEN mal a propósito
    ])
    out = _TMP / "gold_out.xlsx"
    res = scr.procesar(p, out, log=_quiet)
    assert res["instrumento"] == "GHQ-12"
    assert res["formato"] == "iris"
    assert res["total"] == 2
    _, filas = _dump(out)
    by = {f["RUT"]: f for f in filas}
    a = by["11111111-1"]
    assert a["Momento"] == "Ingreso" and a["Puntaje"] == 8
    assert a["Resultado_RAYEN"] == "Alto" and a["Resultado_DISAM"] == "Alto"
    assert a["Discrepancia"] in (None, "")    # coinciden (celda vacía)
    assert a["Estamento"] == "Psicólogo(a)"
    b = by["22222222-2"]
    assert b["Resultado_RAYEN"] == "Medio" and b["Resultado_DISAM"] == "Bajo"  # 3 -> Bajo
    assert b["Discrepancia"] == "SI"          # RAYEN != DISAM
    assert res["discrepancias"] == 1


def test_admin_psc_edad_texto_sin_estamento():
    p = _admin("psc.xlsx", "Cuestionario para padres PSC", [
        ("33333333-3", "12 años 3 meses", "Mujer", "Func Tres", "Ingreso", 65, "Medio"),
    ])
    out = _TMP / "psc_out.xlsx"
    res = scr.procesar(p, out, log=_quiet)
    assert res["instrumento"] == "PSC"
    assert res["formato"] == "administrativo"
    _, filas = _dump(out)
    f = filas[0]
    assert f["Edad"] == 12                     # '12 años 3 meses' -> 12
    assert f["Resultado_DISAM"] == "Medio"     # PSC 65 -> 64-69
    assert f["Estamento"] in (None, "")        # admin no trae estamento
    assert f["Momento"] == "Ingreso"


def test_deteccion_psc_y():
    p = _iris("pscy.xlsx", "Cuestionario para Adolescentes (PSC-Y) 10 a 14 años", [
        ("44444444-4", 12, "Hombre", "F", "Terapeuta Ocupacional", "Ingreso", 40, "Bajo"),
    ])
    out = _TMP / "pscy_out.xlsx"
    res = scr.procesar(p, out, log=_quiet)
    assert res["instrumento"] == "PSC-Y"       # no confundir con PSC


def test_rechaza_no_instrumento():
    """Un export sin PUNTAJE/RESULTADO (ej. el de Control de Salud Mental) se rechaza."""
    p = _TMP / "noinst.xlsx"
    wb = openpyxl.Workbook(); ws = wb.active
    ws.append(["NUMERO TIPO IDENTIFICACION", "AÑO APLICACIÓN FORMULARIO", "SEXO", "18.- ESTADO"])
    ws.append(["1-9", 30, "Mujer", "EGRESO ALTA"])
    wb.save(p)
    try:
        scr.abrir_validado(p)
        assert False, "debió rechazar"
    except scr.ArchivoInvalido as e:
        assert e.categoria == "no_instrumento"


# ── Runner propio ─────────────────────────────────────────────────────
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
            fallos += 1; print(f"ERROR {fn.__name__} -> {type(e).__name__}: {e}")
    print("-" * 50)
    print(f"{len(pruebas) - fallos}/{len(pruebas)} OK" + (f" ({fallos} con problemas)" if fallos else ""))
    return 1 if fallos else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(_main())
