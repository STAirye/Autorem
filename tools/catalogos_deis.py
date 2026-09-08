#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# Copyright (C) 2026 Simon Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.9.0
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. Distributed WITHOUT ANY WARRANTY. See the GNU
# General Public License for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
catalogos_deis.py - mantiene los catalogos oficiales que shippea la herramienta.

Es la contraparte de DESARROLLO de programas/catalogos.py: baja los .xlsx del
DEIS, los recorta a .csv.gz versionados y avisa cuando el DEIS publica una
edicion nueva. NO se ejecuta desde el .exe: el .exe corre 100% offline y usa
los slims ya vendorizados.

    python tools/catalogos_deis.py --check           que hay publicado vs lo nuestro
    python tools/catalogos_deis.py --fetch           baja los .xlsx a refs_tablas/
    python tools/catalogos_deis.py --slim            genera catalogos/*.csv.gz
    python tools/catalogos_deis.py --fetch --slim cie10      solo uno

FLUJO CUANDO EL DEIS ACTUALIZA
    1. --check           avisa que el nombre publicado ya no es el de FUENTES.json
    2. --fetch           baja el nuevo .xlsx (queda gitignored en refs_tablas/)
    3. scan_catalogo.py  PII antes de convertirlo en .gz opaco (el pre-commit
                         anti-RUT salta los binarios: aca no lo revisa nadie mas)
    4. --slim            regenera el .csv.gz + FUENTES.json
    5. git add catalogos/

Los .xlsx originales NO se versionan (pesan y se rebajan cuando haga falta);
al repo va solo el slim + FUENTES.json, que deja registro de que edicion es.
"""

import hashlib
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from programas import catalogos as cat                     # noqa: E402
from tools.scan_catalogo import escanear                   # noqa: E402

PAGINA = "https://deis.minsal.cl/centrofic/"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) autoREM/catalogos"}
FUENTE_LOCAL = REPO / "refs_tablas"          # .xlsx originales (gitignored)

# Firma para reconocer, en la pagina del DEIS, el link de cada catalogo: todos
# los tokens tienen que estar en la URL. Se matchea por CONTENIDO del link y no
# por nombre exacto porque el DEIS le mete la fecha al nombre del archivo
# ("Lista tabular CIE-10 - agosto 2026.xlsx") y lo cambia en cada edicion.
FIRMAS = {
    "cie10": ["lista", "tabular", "cie-10"],
    "eno":   ["eno", "decreto"],
    "ges":   ["ges", "cie-10"],
}

MESES = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
         "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11,
         "diciembre": 12}


def _log(msg=""):
    print(msg)


def _bajar(url):
    # El DEIS publica los href SIN escapar ("...Lista tabular CIE-10 - agosto
    # 2026.xlsx"): http.client rechaza el espacio. Se re-escapa dejando '%' como
    # seguro, para no doble-codificar las URL que ya vienen escapadas.
    req = urllib.request.Request(urllib.parse.quote(url, safe=":/?#[]@!$&'()*+,;=%"),
                                 headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:      # noqa: S310 (URL fija, https)
        return r.read()


def _nombre_url(url):
    return urllib.request.unquote(url.rsplit("/", 1)[-1])


def edicion_de(nombre):
    """'Lista tabular CIE-10 - agosto 2026.xlsx' -> '2026-08'. Si no hay mes+anio
    reconocible, cae al nombre del archivo sin extension (p.ej. 'GES 90 ... v1_4'):
    es una etiqueta de procedencia, no una fecha que haya que inventar."""
    n = nombre.lower()
    m = re.search(r"(" + "|".join(MESES) + r")\s+(\d{4})", n)
    if m:
        return f"{m.group(2)}-{MESES[m.group(1)]:02d}"
    # ya-normalizada ('DEIS_cie10_2026-08.xlsx'): re-leer el .xlsx bajado tiene
    # que dar la MISMA edicion que la URL de origen, si no --check ve una
    # diferencia fantasma en cada corrida.
    m = re.search(r"(20\d{2})-(\d{2})", n) or re.search(r"(20\d{2})", n)
    if m:
        return "-".join(m.groups())
    # Sin fecha: el GES se versiona 'v1_4'. Es la etiqueta que trae, no una que
    # convenga inventar.
    # (?<![a-z0-9]) y no \b: en 'DEIS_ges_v1_4.xlsx' el guion bajo ES caracter de
    # palabra, asi que \b no marca limite ahi y la version no matchearia.
    m = re.search(r"(?<![a-z0-9])v\d+[._]\d+", n)
    return m.group() if m else Path(nombre).stem


def publicados():
    """{nombre: url} de los catalogos que la pagina del DEIS ofrece HOY."""
    html = _bajar(PAGINA).decode("utf-8", errors="replace")
    urls = re.findall(r'href="([^"]+\.xlsx?)"', html, flags=re.I)
    out = {}
    for nombre, toks in FIRMAS.items():
        u = next((u for u in urls if all(t in urllib.request.unquote(u).lower() for t in toks)), None)
        if u:
            out[nombre] = u
    return out


def _ruta_local(nombre, url):
    """Nombre estable para el .xlsx bajado (el del DEIS trae espacios y tildes)."""
    return FUENTE_LOCAL / f"DEIS_{nombre}_{edicion_de(_nombre_url(url))}.xlsx"


def _fuentes_json():
    return cat.carpeta_datos(crear=True) / cat.FUENTES


def _leer_fuentes():
    try:
        return json.loads(_fuentes_json().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


# -- Verbos -----------------------------------------------------------------
def check(nombres):
    """Compara lo publicado en el DEIS contra la edicion vendorizada."""
    try:
        pub = publicados()
    except OSError as e:
        _log(f"X no pude leer {PAGINA}: {e}")
        return 1
    mias, pendientes = _leer_fuentes(), 0
    for n in nombres:
        url = pub.get(n)
        if not url:
            _log(f"  {n:<6} ? no encontre el link en la pagina del DEIS "
                 f"(cambio el texto del enlace? revisar FIRMAS)")
            continue
        nueva, tengo = edicion_de(_nombre_url(url)), mias.get(n, {}).get("edicion")
        estado = "al dia" if nueva == tengo else f"HAY EDICION NUEVA ({tengo} -> {nueva})"
        _log(f"  {n:<6} {estado}")
        _log(f"         {_nombre_url(url)}")
        pendientes += nueva != tengo
    if pendientes:
        _log(f"\n{pendientes} catalogo(s) con edicion nueva. Para actualizar:")
        _log("  python tools/catalogos_deis.py --fetch --slim")
    return 0


def fetch(nombres):
    """Baja los .xlsx del DEIS a refs_tablas/ (gitignored)."""
    pub = publicados()
    for n in nombres:
        url = pub.get(n) or cat.CATALOGOS[n]["url"]
        destino = _ruta_local(n, url)
        _log(f"  bajando {n}: {_nombre_url(url)}")
        destino.write_bytes(_bajar(url))
        _log(f"    -> {destino.relative_to(REPO)}  ({destino.stat().st_size / 1024:,.1f} KB)")
    return 0


def _xlsx_de(nombre):
    """El .xlsx local mas reciente de ese catalogo."""
    cands = sorted(FUENTE_LOCAL.glob(f"DEIS_{nombre}_*.xlsx"), key=lambda p: p.stat().st_mtime)
    return cands[-1] if cands else None


def slim(nombres):
    """Genera catalogos/<nombre>.csv.gz + FUENTES.json desde los .xlsx locales.
    Escanea PII antes de escribir: un catalogo con hallazgos NO se vendoriza."""
    fuentes, fallas = _leer_fuentes(), 0
    for n in nombres:
        x = _xlsx_de(n)
        if x is None:
            _log(f"X {n}: no hay .xlsx local. Corre primero  --fetch {n}")
            fallas += 1
            continue
        _log(f"\n{n}: {x.name}")
        hallazgos, _, _ = escanear(x)
        if hallazgos:
            _log(f"  X {len(hallazgos)} hallazgo(s) de PII: NO se vendoriza. "
                 f"Revisar con  python tools/scan_catalogo.py {x}")
            fallas += 1
            continue
        _log("  scan PII: limpio")
        d = cat.CATALOGOS[n]["leer"](x, lambda m: _log("  " + m))
        destino = cat.carpeta_datos(crear=True) / f"{n}.csv.gz"
        d.to_csv(destino, index=False, compression="gzip")
        fuentes[n] = {
            "titulo": cat.CATALOGOS[n]["titulo"],
            "url": cat.CATALOGOS[n]["url"],
            "archivo_origen": x.name,
            "edicion": edicion_de(x.name),
            "filas": len(d),
            "sha256_origen": hashlib.sha256(x.read_bytes()).hexdigest(),
            "generado": date.today().isoformat(),
        }
        _log(f"  -> {destino.relative_to(REPO)}  ({len(d)} filas, "
             f"{destino.stat().st_size / 1024:,.1f} KB)")
    _fuentes_json().write_text(json.dumps(fuentes, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf-8")
    _log(f"\nFUENTES.json actualizado ({len(fuentes)} catalogos).")
    if not fallas:
        _log("Versionar:  git add catalogos/")
    return 1 if fallas else 0


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    verbos = [v for v in ("--check", "--fetch", "--slim") if v in argv]
    nombres = [a for a in argv if not a.startswith("--")] or list(cat.CATALOGOS)
    malos = [n for n in nombres if n not in cat.CATALOGOS]
    if malos:
        _log(f"X catalogo(s) desconocido(s): {', '.join(malos)}. "
             f"Hay: {', '.join(cat.CATALOGOS)}")
        return 2
    if not verbos:
        print(__doc__)
        return 2
    rc = 0
    for v in verbos:
        _log(f"\n=== {v} : {', '.join(nombres)} ===")
        rc |= {"--check": check, "--fetch": fetch, "--slim": slim}[v](nombres)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
