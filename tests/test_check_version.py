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
Pruebas de los CONTADORES de tools/check_version.py (el check del pre-commit).

Por que existen: hasta la 2.0.5 el check solo miraba CLAUDE.md, asi que el
contador del README derivo sin que nadie lo notara -- decia 311 pruebas cuando
habia 309. El numero no rompe codigo; rompe la confianza en la documentacion,
que es lo unico con lo que se orienta una sesion fria.

Lo que se amarra aca:
  - los patrones MATCHEAN el texto real de CLAUDE.md y del README (un patron que
    dejo de matchear no falla: deja de vigilar, en silencio);
  - son ESPECIFICOS (no cazan cualquier numero suelto del README);
  - `_sub_contador` toca solo el grupo, no todas las apariciones del numero;
  - el repo de hoy esta sincronizado.

Datos SINTETICOS (texto armado aca). Correr: python tests/test_check_version.py
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
import _aislar_cache   # noqa: E402,F401  (PRIMERO: nunca tocar el ~/.autorem real)

from tools.check_version import (CONTADORES, ETIQUETAS, RAIZ, _sub_contador,   # noqa: E402
                                 contar_tests, cuentas, revisar)


def _texto(nombre):
    return (RAIZ / nombre).read_text(encoding="utf-8")


# -- Los patrones siguen enganchados a la documentacion real -------------------

def test_todo_archivo_vigilado_existe():
    for nombre in CONTADORES:
        assert (RAIZ / nombre).is_file(), f"{nombre} no existe"


def test_cada_patron_matchea_de_verdad():
    """Un patron que dejo de matchear NO falla el check: deja de vigilar.

    Es el modo de falla silencioso que hay que cazar aca -- si alguien reescribe
    la frase del README, el conteo vuelve a quedar suelto sin que nada avise.
    """
    for nombre, patrones in CONTADORES.items():
        texto = _texto(nombre)
        for pat, que in patrones:
            assert pat.search(texto), (
                f"{nombre}: el patron {pat.pattern!r} ({que}) ya no matchea; "
                f"o se reescribio la frase, o el contador quedo sin vigilancia")


def test_etiqueta_de_cada_patron_es_conocida():
    for patrones in CONTADORES.values():
        for _, que in patrones:
            assert que in ETIQUETAS and que in cuentas()


def test_un_solo_grupo_por_patron():
    """El mecanismo asume grupo 1 = el numero. Dos grupos lo romperian."""
    for patrones in CONTADORES.values():
        for pat, _ in patrones:
            assert pat.groups == 1, f"{pat.pattern!r} tiene {pat.groups} grupos"


# -- Especificidad: el README esta lleno de numeros que NO son el contador -----

def test_el_patron_del_readme_no_caza_cualquier_numero():
    """Un patron laxo en el pre-commit bloquea commits sanos.

    El README nombra versiones (2.0.0), segundos (103 s), leyes (20.584) y
    Python 3.9. Nada de eso es un conteo de tests.
    """
    senuelos = ("la **2.0.0** fue la interfaz nueva",
                "tarda ~103 s, contra ~194 s",
                "Leyes 20.584 y 21.719",
                "**Python 3.9 o superior**",
                "**16 archivos** de otra cosa",
                "311 pruebas sueltas por ahi")
    for pat, _ in CONTADORES["README.md"]:
        for senuelo in senuelos:
            assert not pat.search(senuelo), f"{pat.pattern!r} cazo {senuelo!r}"


def test_el_patron_del_readme_caza_la_frase_real():
    frase = "Datos 100% sintéticos, sin PII. **309 pruebas** en 16 archivos:"
    encontrados = {que: pat.findall(frase) for pat, que in CONTADORES["README.md"]}
    assert encontrados["tests"] == ["309"]
    assert encontrados["archivos"] == ["16"]


# -- _sub_contador: el caso que str.replace arruinaba ---------------------------

def test_sub_contador_reemplaza_solo_su_grupo():
    """Con el MISMO numero en los dos lugares, `str.replace` pisaba ambos."""
    pat_tests, pat_arch = (p for p, _ in CONTADORES["README.md"])
    texto = "**16 pruebas** en 16 archivos:"

    assert _sub_contador(texto, pat_tests, 309) == "**309 pruebas** en 16 archivos:"
    assert _sub_contador(texto, pat_arch, 17) == "**16 pruebas** en 17 archivos:"


def test_sub_contador_deja_el_resto_intacto():
    pat = re.compile(r"\*\*(\d+) pruebas\*\* en \d+ archivos")
    texto = "Antes. **1 pruebas** en 1 archivos. Despues, 1 y 1."
    assert _sub_contador(texto, pat, 42) == (
        "Antes. **42 pruebas** en 1 archivos. Despues, 1 y 1.")


def test_sub_contador_es_idempotente():
    pat, _ = CONTADORES["README.md"][0]
    texto = "**309 pruebas** en 16 archivos"
    assert _sub_contador(_sub_contador(texto, pat, 309), pat, 309) == texto


# -- El repo de hoy ------------------------------------------------------------

def test_cuentas_coinciden_con_el_disco():
    reales = cuentas()
    assert reales["tests"] == contar_tests()
    assert reales["archivos"] == len(list((RAIZ / "tests").glob("test_*.py")))
    assert reales["tests"] > 0 and reales["archivos"] > 0


def test_la_documentacion_declara_los_numeros_reales():
    """Lo mismo que reclama el pre-commit, pero como test."""
    reales = cuentas()
    for nombre, patrones in CONTADORES.items():
        texto = _texto(nombre)
        for pat, que in patrones:
            for declarado in pat.findall(texto):
                assert int(declarado) == reales[que], (
                    f"{nombre} declara {declarado} {ETIQUETAS[que]}, "
                    f"pero hay {reales[que]} (corre: "
                    f"python tools/check_version.py --arreglar)")


def test_revisar_no_reporta_contadores_desincronizados():
    malos = [m for grave, m in revisar() if "declara" in m and "pero hay" in m]
    assert malos == [], malos


if __name__ == "__main__":
    fallos = 0
    for nombre, fn in sorted(globals().items()):
        if nombre.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"  ok  {nombre}")
            except AssertionError as e:
                fallos += 1
                print(f"  FALLA  {nombre}: {e}")
    print(f"\n{'FALLARON ' + str(fallos) if fallos else 'TODO OK'}")
    sys.exit(1 if fallos else 0)
