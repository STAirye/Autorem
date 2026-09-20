#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# SPDX-License-Identifier: GPL-3.0-or-later
# ==========================================================================
"""
Pruebas de los CONTRATOS de fuentes (tests/contratos_fuentes.py) y del hook que los
corre al commitear (tools/check_fuentes.py). Datos SINTÉTICOS.
Correr: python tests/test_contratos_fuentes.py
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _aislar_cache   # noqa: E402,F401  (PRIMERO: nunca tocar el ~/.autorem real)

import contratos_fuentes as cf                                  # noqa: E402
from programas.rem_utils import (ArchivoInvalido, leer_xlsx,    # noqa: E402
                                 exigir_filas)
from tools import check_fuentes as hook                         # noqa: E402


def test_los_contratos_registrados_pasan():
    """El barrido completo (el hook corre solo lo que el commit toca; esto, todo)."""
    lineas = []
    fallas = cf.correr(log=lineas.append)
    assert fallas == 0, "\n".join(lineas)


# -- El arnes caza la clase del bug (si no, el hook es decorado) --------------
def _bueno(ruta):
    """Lector correcto: por NOMBRE, con guardas sobre la fuente."""
    hdr, filas = leer_xlsx(ruta)
    exigir_filas(filas, "el toy")
    if "RUN" not in hdr:
        raise ArchivoInvalido("sin_columnas", "sin RUN")
    i = hdr.index("RUN")
    runs = [f[i] for f in filas if f[i] not in (None, "")]
    if not runs:
        raise ArchivoInvalido("sin_datos", "ningun RUN")
    return runs


def _indice_fijo(ruta):
    """El bug de la col 11 del A05: guarda de filas, pero la columna por POSICION."""
    _hdr, filas = leer_xlsx(ruta)
    exigir_filas(filas, "el toy")
    return [f[1] for f in filas]


def _sin_clave(ruta):
    """Guarda de filas, pero ninguna de que la clave venga: 'vacio TRAS filtrar'."""
    _hdr, filas = leer_xlsx(ruta)
    exigir_filas(filas, "el toy")
    return filas


def _toy(llamar, **kw):
    # 4 columnas y no 3: `rem_utils.indice_encabezado` toma como encabezado la 1ª fila con
    # MAS de 3 celdas llenas, y desde la ronda 12 ya no cae a la fila 0 cuando no encuentra
    # ninguna (levanta 'sin_encabezado'), asi que un toy de 3 columnas no se leeria.
    return cf.Contrato(id="toy", cubre=(), llamar=llamar,
                       encabezado=("A", "RUN", "FECHA", "SEXO"),
                       fila={"A": "a", "RUN": cf.RUT, "FECHA": "01/08/2026", "SEXO": "Mujer"},
                       criticas=("RUN",), clave=("RUN",), **kw)


def _estado(filas, prefijo):
    return next(e for chk, e, _ in filas if chk.startswith(prefijo))


def test_el_arnes_caza_cada_forma_del_bug():
    """Cada forma que dio la revision gui-2.0 tiene que salir FALLA en el arnes."""
    assert all(e == "OK" for _, e, _ in cf.chequear(_toy(_bueno))), cf.chequear(_toy(_bueno))

    # c38a8cc: 0 filas pasa de largo (sin guarda) -> C1
    sin_guarda = _toy(lambda r: [f[1] for f in leer_xlsx(r)[1]])
    assert _estado(cf.chequear(sin_guarda), "C1") == "FALLA"
    # crash criptico en vez de ArchivoInvalido -> C1 lo reporta como tal
    critico = _toy(lambda r: leer_xlsx(r)[1][0])
    det = next(d for chk, _e, d in cf.chequear(critico) if chk.startswith("C1"))
    assert "CRIPTICO" in det, det
    # ANIO_COL_FALLBACK: columna por INDICE FIJO -> C6 (y C3: renombrarla no falla)
    filas = cf.chequear(_toy(_indice_fijo))
    assert _estado(filas, "C6") == "FALLA" and _estado(filas, "C3") == "FALLA", filas
    # clave vacia en todas las filas sigue de largo -> C4
    assert _estado(cf.chequear(_toy(_sin_clave)), "C4") == "FALLA"
    # un `conocido` que YA pasa es FALLA (si no, deja de vigilar la regresion)
    viejo = _toy(_bueno, conocidos={"C1": "pendiente viejo"})
    assert _estado(cf.chequear(viejo), "C1") == "FALLA"
    # y uno que sigue fallando queda PENDIENTE, no bloquea
    pend = _toy(lambda r: [f[1] for f in leer_xlsx(r)[1]], conocidos={"C1": "ronda X"})
    assert _estado(cf.chequear(pend), "C1") == "PENDIENTE"


def test_el_hook_distingue_lectores_y_exige_contrato():
    """`_funciones` marca como LECTOR solo a quien llama una primitiva de lectura, y
    `sin_contrato` pide contrato para un lector nuevo, no para uno exento o cubierto."""
    src = ("def cargar_x(r):\n    return leer_xlsx(r)\n\n"
           "def calcular(d):\n    return len(d)\n")
    marcas = {n: lector for n, _i, _f, lector in hook._funciones(src)}
    assert marcas == {"cargar_x": True, "calcular": False}, marcas
    nuevo = "modulos/rem_nuevo.py::cargar_x"
    exento = next(iter(hook.EXENTOS))
    cubierto = cf.CONTRATOS[0].cubre[0]
    assert hook.sin_contrato({nuevo, exento, cubierto}, cf) == [nuevo]
    # Todo contrato apunta a funciones que EXISTEN (un rename no deja un contrato huerfano).
    existentes = set()
    for p in list((REPO / "programas").rglob("*.py")) + list((REPO / "modulos").rglob("*.py")):
        rel = p.relative_to(REPO).as_posix()
        existentes |= {f"{rel}::{n}" for n, *_ in hook._funciones(p.read_text(encoding="utf-8"))}
    huerfanas = [f for c in cf.CONTRATOS for f in c.cubre if f not in existentes]
    assert not huerfanas, f"`cubre` apunta a funciones que no existen: {huerfanas}"


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
