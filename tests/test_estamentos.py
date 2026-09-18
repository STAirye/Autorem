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
import _aislar_cache   # noqa: E402,F401  (PRIMERO: nunca tocar el ~/.autorem real)

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


def test_rechaza_reporte_sin_filas():
    """Bug recurrente (CLAUDE.md regla 2): con solo el encabezado la tabla salía
    vacía sin fallar, dejando a TODOS los funcionarios sin estamento (y pisando el
    caché con un dict vacío)."""
    try:
        est.cargar_estamentos(_reporte("cupos_vacio.xlsx", []), log=_quiet)
        assert False, "debió rechazar un reporte sin filas"
    except est.ArchivoInvalido as e:
        assert e.categoria == "sin_datos", e.categoria


def test_faltantes_conocidos_y_resoluciones():
    """Failsafe: detectar sin-match, opciones del selector, y resolver/ignorar."""
    from programas.rem_utils import norm
    tabla = {norm("Ana Perez"): "Médico"}
    # faltantes: Ana matchea (dedup, case-insensitive), vacíos se ignoran
    falt = est.faltantes(["Ana Perez", "ana perez", "Beto Ruiz", "", None, "Beto Ruiz"], tabla)
    assert falt == ["Beto Ruiz"]
    # opciones del selector: lo visto primero + el estándar
    ops = est.estamentos_conocidos(tabla)
    assert ops[0] == "Médico" and "Psicólogo(a)" in ops and "Otro" in ops
    # resolver: asignar uno, IGNORAR otro (None)
    est.aplicar_resoluciones(tabla, {"Beto Ruiz": "Enfermero(a)", "Cyn Externa": None})
    assert est.buscar_estamento("Beto Ruiz", tabla) == "Enfermero(a)"
    assert est.buscar_estamento("Cyn Externa", tabla) == ""      # ignorado -> vacío
    assert est.faltantes(["Cyn Externa", "Beto Ruiz"], tabla) == []  # ya ninguno falta


def test_cache_persiste_y_merge():
    """El caché persiste entre corridas y el reporte fresco pisa al caché,
    conservando los funcionarios que solo estaban guardados."""
    est.RUTA_CACHE = _TMP / "cache_estam.json"   # no ensuciar el HOME real
    if est.RUTA_CACHE.exists():
        est.RUTA_CACHE.unlink()
    p1 = _reporte("mes1.xlsx", [
        ("Ana Perez",  "Médico",       "A", "Rojo"),
        ("Beto Ruiz",  "Psicólogo(a)", "B", "Verde"),
    ])
    t1 = est.tabla_efectiva(str(p1), log=_quiet)
    assert est.buscar_estamento("Ana Perez", t1) == "Médico"
    assert est.RUTA_CACHE.exists()                         # se guardó

    # corrida sin archivo: autocarga del caché
    t2 = est.tabla_efectiva(None, log=_quiet)
    assert est.buscar_estamento("Beto Ruiz", t2) == "Psicólogo(a)"

    # mes siguiente con reporte nuevo: Ana cambia de estamento, Caro es nueva,
    # Beto NO viene en el reporte -> se conserva del caché.
    p2 = _reporte("mes2.xlsx", [
        ("Ana Perez",  "Enfermero(a)",  "A", "Rojo"),      # cambió
        ("Caro Díaz",  "Odontólogo(a)", "C", "Azul"),      # nueva
    ])
    t3 = est.tabla_efectiva(str(p2), log=_quiet)
    assert est.buscar_estamento("Ana Perez", t3) == "Enfermero(a)"   # reporte fresco gana
    assert est.buscar_estamento("Caro Díaz", t3) == "Odontólogo(a)"  # nueva
    assert est.buscar_estamento("Beto Ruiz", t3) == "Psicólogo(a)"   # conservada del caché


def test_cache_ilegible_no_se_pisa_con_el_reporte_fresco():
    """Con el caché EXISTENTE pero ilegible (bloqueado, sin permisos), el merge
    'caché + reporte fresco' se guardaba encima con solo el reporte: los funcionarios
    de meses anteriores se perdian en silencio. Ahora no se escribe y se avisa."""
    import programas.rem_utils as ru
    est.RUTA_CACHE = _TMP / "cache_estam_ilegible.json"   # no ensuciar el HOME real
    est.RUTA_CACHE.write_text('{"BETO RUIZ": "Psicólogo(a)"}', encoding="utf-8")
    antes = est.RUTA_CACHE.read_bytes()
    ru.tomar_avisos_cache()
    p = _reporte("mes_ilegible.xlsx", [("Ana Perez", "Médico", "A", "Rojo"),
                                       ("Caro Díaz", "Odontólogo(a)", "C", "Azul")])
    orig = Path.read_text

    def falso(ruta, *a, **k):
        if Path(ruta) == est.RUTA_CACHE:
            raise PermissionError(13, "bloqueado", str(ruta))
        return orig(ruta, *a, **k)
    Path.read_text = falso
    try:
        t = est.tabla_efectiva(str(p), log=_quiet)
    finally:
        Path.read_text = orig
    assert est.buscar_estamento("Ana Perez", t) == "Médico", "ESTA corrida perdio el reporte"
    assert est.RUTA_CACHE.read_bytes() == antes, "piso un caché que no pudo leer"
    assert any("No pude leer" in a for a in ru.tomar_avisos_cache()), "no aviso"


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
