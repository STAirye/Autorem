#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# SPDX-License-Identifier: GPL-3.0-or-later
# ==========================================================================
"""
Pruebas del lookup Funcionario -> Estamento (programas/estamentos.py).
Datos SINTÉTICOS (sin PII). Correr: python tests/test_estamentos.py
"""

import sys
import tempfile
from pathlib import Path

import openpyxl

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from programas import estamentos as est   # noqa: E402

_TMP = Path(tempfile.mkdtemp(prefix="autorem_est_"))


def _reporte(fn, filas):
    """Reporte 'Utilización de Cupos': banner + header fila 9 + data.
    `filas` = lista de (profesional, instrumento[/estamento], tipo, sector)."""
    p = _TMP / fn
    wb = openpyxl.Workbook(); ws = wb.active
    ws.append(["Comuna", "Maipu"]); ws.append(["Establecimiento", "[CESFAM] Dr. Luis Ferrada"])
    ws.append(["Mes", "JULIO"]); ws.append(["Año", "2026"])
    ws.append([]); ws.append(["Utilización de Cupos"]); ws.append([]); ws.append([])
    ws.append(["Profesional", "Instrumento", "Tipo de atención", "Sector",
               "Rendimiento", "Total Cupos"])                         # fila 9
    for prof, inst, tipo, sector in filas:
        ws.append([prof, inst, tipo, sector, "02:00:00", 3])
    wb.save(p)
    return p


def _quiet(*_a, **_k):
    pass


def test_carga_y_dedup():
    p = _reporte("agenda.xlsx", [
        ("Catalina Andrea Mayorga Pino", "Psicólogo(a)", "Control SM", "Rojo"),
        ("Catalina Andrea Mayorga Pino", "Psicólogo(a)", "Otra atención", "Rojo"),  # repetida: dedup
        ("Simón Andre Tobar Vergara",    "Médico",       "Consultoría", "Verde"),
        (None, None, "fila basura", ""),                                            # se ignora
        ("Ana Luisa Mejias Alvarez",     "Odontólogo(a)","Consulta",     "Azul"),
    ])
    tabla, meta = est.cargar_estamentos(p, log=_quiet)
    assert meta["funcionarios"] == 3            # 3 distintos (Catalina dedup)
    assert meta["conflictos"] == 0
    assert est.buscar_estamento("Catalina Andrea Mayorga Pino", tabla) == "Psicólogo(a)"
    # match tolerante a mayúsculas/tildes
    assert est.buscar_estamento("simon andre tobar vergara", tabla) == "Médico"
    assert est.buscar_estamento("Nadie Que No Existe", tabla) == ""
    assert est.buscar_estamento("", tabla) == ""


def test_conflicto_se_avisa():
    p = _reporte("conflicto.xlsx", [
        ("Juan Perez Soto", "Médico",       "A", "Rojo"),
        ("Juan Perez Soto", "Psicólogo(a)", "B", "Rojo"),   # mismo nombre, 2 estamentos
    ])
    tabla, meta = est.cargar_estamentos(p, log=_quiet)
    assert meta["funcionarios"] == 1
    assert meta["conflictos"] == 1
    assert est.buscar_estamento("Juan Perez Soto", tabla) == "Médico"   # conserva el 1º


def test_rechaza_no_reporte():
    p = _TMP / "otro.xlsx"
    wb = openpyxl.Workbook(); ws = wb.active
    ws.append(["Cosa", "Otra"]); ws.append(["1", "2"])
    wb.save(p)
    try:
        est.cargar_estamentos(p, log=_quiet)
        assert False, "debió rechazar"
    except est.ArchivoInvalido as e:
        assert e.categoria == "no_estamentos"


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
