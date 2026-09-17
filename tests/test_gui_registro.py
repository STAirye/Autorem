#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Sonnet 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# ==========================================================================
"""
Pruebas del REGISTRO de pantallas de la GUI 2.0 (gui/registro.py + gui/app.py,
docs/GUI_2.0_plan.md §11).

Anti-olvido, mismo espíritu que tests/test_cobertura.py: descubre por
introspección las páginas de gui/paginas/*.py y falla si una PANTALLA queda
mal declarada — que es justo donde una migración de este tamaño pierde cosas
en silencio. NO prueba que la ventana se vea bien (eso es a ojo, §13); prueba
que el CONTRATO esté completo.

Correr:
    python tests/test_gui_registro.py    # runner propio, imprime PASS/FAIL
    pytest tests/                         # si tienes pytest instalado
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from gui.registro import cargar_registro, ORDEN_PROGRAMAS   # noqa: E402

_CLAVES_OBLIGATORIAS = ("id", "programa", "titulo", "estado", "inputs", "mes",
                        "carpeta_salida", "correr", "resumen")


def _registro():
    r = cargar_registro()
    assert r, "gui/paginas/ no expuso ninguna PANTALLA -- ¿import roto?"
    return r


def test_claves_obligatorias():
    for pantalla in _registro():
        faltantes = [k for k in _CLAVES_OBLIGATORIAS if k not in pantalla]
        assert not faltantes, f"{pantalla.get('id', '?')}: faltan claves {faltantes}"


def test_ids_unicos():
    ids = [p["id"] for p in _registro()]
    dup = {i for i in ids if ids.count(i) > 1}
    assert not dup, f"id(s) de PANTALLA repetidos: {dup}"


def test_programa_declarado_en_el_orden_del_sidebar():
    # `registro._orden_programa` deja pasar un programa desconocido (fail
    # SOFT: cae al final, no revienta el sidebar) -- este test es el fail
    # LOUD que le falta: un programa nuevo hay que declararlo a mano.
    for pantalla in _registro():
        assert pantalla["programa"] in ORDEN_PROGRAMAS, (
            f"{pantalla['id']}: programa {pantalla['programa']!r} no está en "
            f"registro.ORDEN_PROGRAMAS -- agrégalo ahí (si no, el sidebar lo "
            f"manda al final en silencio)")


def test_correr_y_resumen_invocables():
    for pantalla in _registro():
        assert callable(pantalla["correr"]), f"{pantalla['id']}: 'correr' no es invocable"
        assert callable(pantalla["resumen"]), f"{pantalla['id']}: 'resumen' no es invocable"


def test_preparar_y_al_completar_invocables_si_estan():
    for pantalla in _registro():
        if pantalla.get("preparar") is not None:
            assert callable(pantalla["preparar"]), f"{pantalla['id']}: 'preparar' no es invocable"
        if pantalla.get("al_completar") is not None:
            assert callable(pantalla["al_completar"]), (
                f"{pantalla['id']}: 'al_completar' no es invocable")


def test_inputs_key_no_duplicada():
    for pantalla in _registro():
        keys = [inp["key"] for inp in pantalla.get("inputs", [])]
        dup = {k for k in keys if keys.count(k) > 1}
        assert not dup, f"{pantalla['id']}: input key(s) repetida(s) {dup}"


def test_extras_despues_de_apunta_a_un_input_real():
    for pantalla in _registro():
        keys_inputs = {inp["key"] for inp in pantalla.get("inputs", [])}
        for extra in pantalla.get("extras", []):
            despues_de = extra.get("despues_de")
            if despues_de is not None:
                assert despues_de in keys_inputs, (
                    f"{pantalla['id']}: extras[].despues_de={despues_de!r} no es la key "
                    f"de ningún input de esta página (keys: {sorted(keys_inputs)})")


def test_construye_todas_las_paginas_sin_excepcion():
    """Smoke test real (sin mocks): `App()` arma el sidebar y CADA pantalla
    -- incluidas Inicio/Acerca de, que quedan fuera del registro (SS4) --
    sin excepciones. Perezoso (SS4 del plan): una pagina recien se construye
    al visitarla, asi que hay que visitarlas todas a mano para ejercitarlas."""
    import customtkinter as ctk   # noqa: F401  (falla temprano y claro si falta la dep)
    from gui.app import App
    app = App()
    try:
        app.withdraw()   # no hace falta que la ventana se vea para este test
        ids = [p["id"] for p in app.registro] + ["inicio", "acerca_de"]
        for pid in ids:
            app.mostrar(pid)
            assert pid in app._frames, f"{pid}: no quedó construida tras mostrar()"
    finally:
        app.destroy()


def _main():
    pruebas = [v for k, v in sorted(globals().items())
              if k.startswith("test_") and callable(v)]
    fallos = 0
    for fn in pruebas:
        try:
            fn(); print(f"PASS  {fn.__name__}")
        except AssertionError as e:
            fallos += 1; print(f"FAIL  {fn.__name__} -> {e or 'assert'}")
        except Exception as e:   # noqa: BLE001
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
