#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Sonnet 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# SPDX-License-Identifier: GPL-3.0-or-later
# ==========================================================================
"""Pruebas de las utilidades de RANGO DE MESES (docs/rango_meses_plan.md §4.1):
`meses_del_rango`, `etiqueta_periodo`, `exigir_cada_mes`.
    python tests/test_rango_meses.py"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
import _aislar_cache   # noqa: E402,F401  (PRIMERO: nunca tocar el ~/.autorem real)

from programas.rem_utils import (meses_del_rango, etiqueta_periodo, exigir_cada_mes,
                                 ArchivoInvalido)   # noqa: E402


def test_meses_del_rango_inclusive():
    assert meses_del_rango((2026, 1), (2026, 3)) == [(2026, 1), (2026, 2), (2026, 3)]


def test_meses_del_rango_cruza_anio():
    assert meses_del_rango((2025, 11), (2026, 2)) == [
        (2025, 11), (2025, 12), (2026, 1), (2026, 2)]


def test_meses_del_rango_un_solo_mes():
    assert meses_del_rango((2026, 7), (2026, 7)) == [(2026, 7)]


def test_meses_del_rango_desde_posterior_a_hasta_falla():
    try:
        meses_del_rango((2026, 7), (2026, 3))
        assert False, "debió levantar ValueError"
    except ValueError as e:
        assert "2026-07" in str(e) and "2026-03" in str(e), str(e)


def test_etiqueta_periodo_un_mes():
    assert etiqueta_periodo([(2026, 7)]) == "2026-07"


def test_etiqueta_periodo_rango():
    assert etiqueta_periodo([(2026, 1), (2026, 2), (2026, 3)]) == "2026-01 a 2026-03"


def test_etiqueta_periodo_a_nombre_de_archivo():
    """La transformación que usa la GUI para el nombre de archivo (plan §4.1): sin
    espacios, mismo separador '_' para año-mes y '-' entre los dos extremos."""
    def a_archivo(meses):
        return etiqueta_periodo(meses).replace("-", "_").replace(" a ", "-")
    assert a_archivo([(2026, 7)]) == "2026_07"
    assert a_archivo([(2026, 1), (2026, 2), (2026, 3)]) == "2026_01-2026_03"


def test_exigir_cada_mes_pasa_si_todos_tienen_datos():
    import pandas as pd
    d = pd.DataFrame({"FECHA": pd.to_datetime(["2026-01-15", "2026-02-10", "2026-03-05"])})
    exigir_cada_mes(d, [(2026, 1), (2026, 2), (2026, 3)], "el ADA de prueba")   # no debe levantar


def test_exigir_cada_mes_falla_nombrando_el_mes_vacio():
    import pandas as pd
    d = pd.DataFrame({"FECHA": pd.to_datetime(["2026-01-15", "2026-03-05"])})   # falta febrero
    try:
        exigir_cada_mes(d, [(2026, 1), (2026, 2), (2026, 3)], "el ADA de prueba")
        assert False, "debió levantar ArchivoInvalido"
    except ArchivoInvalido as e:
        assert e.categoria == "mes_vacio" and "02/2026" in str(e), str(e)


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
