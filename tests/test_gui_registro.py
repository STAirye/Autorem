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

from gui.registro import cargar_registro, ORDEN_PAGINAS, ORDEN_PROGRAMAS   # noqa: E402

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


def test_pagina_declarada_en_el_orden_del_sidebar():
    """Hermano del de arriba, para el orden DENTRO del grupo. Sin ORDEN_PAGINAS la
    posicion la decidia `pkgutil`, o sea el NOMBRE DEL ARCHIVO: renombrar sm.py a
    actividades.py reordenaba el sidebar en silencio. `_orden_pagina` deja pasar una
    pagina no declarada (fail SOFT: al final del grupo) -- este es el fail LOUD."""
    for pantalla in _registro():
        assert pantalla["id"] in ORDEN_PAGINAS, (
            f"{pantalla['id']}: no está en registro.ORDEN_PAGINAS -- agrégalo ahí "
            f"(si no, el sidebar lo manda al final de su grupo en silencio)")


def test_el_orden_de_paginas_no_depende_del_nombre_del_archivo():
    """El de arriba asegura que la pagina ESTE declarada; este, que la declaracion se
    APLIQUE. Hace falta un registro sintetico: hoy el orden alfabetico de los .py
    coincide por casualidad con el deseado ("a05" < "sm"), asi que el registro real no
    puede distinguir "ordena por ORDEN_PAGINAS" de "ordena por nombre de archivo" --
    que es justo la confusion que dejo el bug. Aca `_paginas_encontradas` devuelve las
    paginas AL REVES y el orden declarado tiene que ganar igual."""
    from gui import registro as reg

    falsas = [{"id": pid, "programa": "Salud Mental"}
              for pid in ("sm_actividades", "a05")]     # al reves a proposito
    previo = reg._paginas_encontradas
    reg._paginas_encontradas = lambda: list(falsas)
    try:
        ids = [p["id"] for p in reg.cargar_registro()]
    finally:
        reg._paginas_encontradas = previo
    assert ids == ["a05", "sm_actividades"], (
        f"el sidebar quedo en {ids}: el orden sale del orden en que se ENCONTRARON "
        f"los archivos, no de registro.ORDEN_PAGINAS")


def test_una_sola_ancla_de_salida_por_pantalla():
    """`ancla_salida` fija la carpeta de salida por defecto (gui/app.py
    `_resolver_ctx`). Dos anclas en una pantalla = el default lo decide otra vez el
    orden en que estan ESCRITOS los inputs, que es justo lo que la marca elimina."""
    for pantalla in _registro():
        anclas = [i["key"] for i in pantalla.get("inputs", []) if i.get("ancla_salida")]
        assert len(anclas) <= 1, f"{pantalla['id']}: más de un ancla_salida: {anclas}"


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


class _MessageboxFalso:
    """Captura los avisos en vez de abrir una ventana: `valida_mes` es pura salvo
    por el messagebox, asi que se puede probar sin display."""

    def __init__(self):
        self.avisos = []

    def showwarning(self, titulo, mensaje):
        self.avisos.append((titulo, mensaje))


def test_valida_mes_rechaza_el_rango_no_solo_lo_no_numerico():
    """El `ttk.Spinbox` acota SOLO sus flechas: un mes 13 TECLEADO llegaba al worker
    y reventaba en `_rango_mes` con 'month must be in 1..12', que `manejar_error`
    despacha como "Error inesperado ... pasaselo a Simon" -- un typo presentado como
    bug del programa, y despues de cargar los archivos. Un año de 2 digitos era peor:
    no reventaba, salia 'no hay filas de 07/0026' culpando al export.

    `_tab_a05` y `_tab_beta` validaban el rango en autorem.py; el port lo perdio para
    todas las paginas menos A05. Ahora es una sola funcion compartida."""
    from gui.runner import valida_mes
    from gui.widgets import ANIO_MAX, ANIO_MIN

    for malo in (None, (2026, 13), (2026, 0), (2026, -1), (26, 7), (202, 7),
                 (ANIO_MIN - 1, 6), (ANIO_MAX + 1, 6)):
        mb = _MessageboxFalso()
        assert valida_mes(malo, mb) is None, f"{malo} deberia rechazarse"
        assert mb.avisos, f"{malo} se rechazo en SILENCIO (sin avisar al usuario)"

    for bueno in ((2026, 1), (2026, 12), (2026, 7), (ANIO_MIN, 1), (ANIO_MAX, 12)):
        mb = _MessageboxFalso()
        assert valida_mes(bueno, mb) == bueno, f"{bueno} es valido y se rechazo"
        assert not mb.avisos, f"{bueno} es valido y aun asi aviso: {mb.avisos}"


def test_el_spinbox_y_la_guarda_de_anio_no_pueden_divergir():
    """Los `from_`/`to` del Spinbox y el rango que valida `runner.valida_mes` salen de
    las MISMAS constantes. Si alguien mueve una sola, el mensaje de error miente."""
    import inspect
    from gui import widgets
    fuente = inspect.getsource(widgets.selector_mes)
    assert "from_=ANIO_MIN, to=ANIO_MAX" in fuente, (
        "selector_mes volvio a hardcodear los años del Spinbox: tiene que usar "
        "widgets.ANIO_MIN/ANIO_MAX, que es lo que valida runner.valida_mes")


def test_motivo_fuente_sigue_las_mismas_ramas_que_manejar_error():
    """El BannerFuente (al elegir el archivo) y el messagebox (al procesar) describen
    el MISMO archivo, asi que no pueden contradecirse: los dos salen del arbol de
    `isinstance` de `manejar_error`. Un `.xls` disfrazado de `.xlsx` no es un problema
    de firmas y no puede decir que lo sea."""
    import zipfile
    from gui.runner import es_error_formato, motivo_fuente

    disfrazado = zipfile.BadZipFile("File is not a zip file")
    assert es_error_formato(disfrazado), "BadZipFile deberia ser problema de formato"
    assert "xlsx" in motivo_fuente(disfrazado)
    assert "Excel" in motivo_fuente(PermissionError(13, "in use"))
    assert "librería" in motivo_fuente(ImportError("Falta 'openpyxl'"))
    # Cualquier otra cosa: se nombra el tipo, no se inventa una causa.
    assert "ValueError" in motivo_fuente(ValueError("cualquiera"))


def test_el_desglose_por_instrumento_del_a03_llega_hasta_el_resumen():
    """Los 3 slots A03·D.3 fijan el instrumento A MANO (sin autodeteccion), asi que un
    export cargado en el slot equivocado solo se delata en el desglose: un total pelado
    ("60 aplicaciones") tapa igual un 20/20/20 que un 60/0/0. La vieja pestana
    standalone lo mostraba y el port lo perdio.

    Corre `correr` de verdad en modo solo-cuestionarios (con `procesar_unificado` y los
    estamentos stubbeados) para probar TODO el camino: que el dato se guarde en `res` y
    que `resumen` lo imprima. Probar solo `_por_instrumento` con un dict a mano dejaba
    pasar que nadie lo estuviera poblando."""
    import modulos.rem_a03_d3_instrumentos as screening
    import programas.estamentos as estam
    from gui.paginas import sm

    por_inst = {"PSC": 20, "PSC-Y": 18, "GHQ-12": 22}
    previos = (screening.procesar_unificado, estam.tabla_efectiva)
    screening.procesar_unificado = lambda por_instrumento, salida, **kw: {
        "salida": str(salida), "total": 60, "por_instrumento": por_inst, "tabla": None}
    estam.tabla_efectiva = lambda *_a, **_kw: None
    try:
        ctx = {"mes": (2026, 8), "carpeta": Path("."), "solo_a03": True,
               "a03": {"incluir": True, "est_ruta": "",
                       "instrumentos": {k: f"{k}.xlsx" for k in por_inst}}}
        res = sm.correr(ctx, log=lambda *_a: None)
    finally:
        screening.procesar_unificado, estam.tabla_efectiva = previos

    assert res["por_inst_a03"] == por_inst, "el desglose no llego a `res`"
    texto = sm.resumen(res)
    for trozo in ("60 aplicaciones", "PSC: 20", "PSC-Y: 18", "GHQ-12: 22"):
        assert trozo in texto, f"falta {trozo!r} en el resumen: {texto!r}"
    # Sin dato no se inventa un parentesis vacio.
    assert sm._por_instrumento({"por_inst_a03": None}) == ""
    assert sm._por_instrumento({}) == ""


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
