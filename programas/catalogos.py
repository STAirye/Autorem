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
catalogos.py - CAPA COMPARTIDA de catalogos oficiales del DEIS/MINSAL.

QUE ES
  Backend, no modulo de tarea: no llena ninguna casilla del REM por si solo.
  Es el diccionario que le falta al resto de la herramienta -- que significa
  un codigo, si es de notificacion obligatoria, si es GES. Lo consumen A23
  (asma = J09-J22 sin J19), el futuro anotador batch, y lo que venga.

REGISTRO DECLARATIVO
  Un catalogo nuevo = una entrada en CATALOGOS + una funcion _leer_*.
  No un modulo por catalogo. Mismo patron que COBERTURA en cobertura.py.

  cie10  Lista Tabular CIE-10 (DEIS)          COD | DESC | TIPO
  eno    Enfermedades de Notif. Obligatoria   ENFERMEDAD | TIPO | ART | COD
  ges    GES 90 problemas <-> CIE-10          ID | PROBLEMA | COD | OBS

CASCADA DE CARGA (y por que en ese orden)
  1. `entrada` explicita          -> el usuario eligio un .xlsx a mano.
  2. .xlsx en la carpeta catalogos/ -> DROP-IN: si el DEIS publica una edicion
     nueva, se deja el .xlsx ahi y manda, sin esperar un .exe nuevo. Hay que
     PONERLO a proposito (no se barre refs_tablas/, donde puede haber uno viejo
     olvidado). Se avisa RUIDOSO en el log: cambiar la fuente cambia resultados.
  3. catalogos/<nombre>.csv.gz    -> el slim vendorizado que shippea el .exe.
  Siempre se loguea cual gano y de que edicion, via catalogos/FUENTES.json.

FORMATO DE CODIGO
  El DEIS escribe `J209` (sin punto), RAYEN `J20.9`. Canonico = SIN punto
  (`norm_codigo`); `con_punto` es solo para mostrar.

PRIVACIDAD
  Documentos publicos, cero PII. Aun asi cada catalogo se pasa por
  tools/scan_catalogo.py antes de versionarlo: el pre-commit anti-RUT SALTA
  los binarios (.xlsx, .gz), o sea que un slim vendorizado no lo revisa nadie.
"""

import gzip
import json
import re
import sys
from pathlib import Path

from programas.rem_utils import norm, resolver_columnas

CARPETA = "catalogos"
FUENTES = "FUENTES.json"

# ---------------------------------------------------------------------------
# Tipo de notificacion del ENO.
#
# El .xlsx del DEIS trae la enfermedad y sus codigos CIE-10, pero NO dice si la
# notificacion es inmediata, diaria o centinela. Eso vive en el Decreto 7/2019
# (art. 1, literales a/b/c), texto oficial en:
#   https://www.leychile.cl/Consulta/obtxml?opt=7&idNorma=1141549
# Transcrito aca en vez de inferirlo del ORDEN de las filas del Excel (que hoy
# calza, pero es un accidente que una reordenacion del DEIS romperia en silencio).
#
# Clave = nombre de la enfermedad como lo escribe el Excel del DEIS, normalizado.
# Una fila del Excel que no este aca sale con TIPO '?' y se avisa RUIDOSO: es un
# agregado nuevo, no un bug que convenga tapar con un default.
_A = ("inmediata", "art.1 lit.a")     # notificacion inmediata ante sospecha
_B = ("diaria", "art.1 lit.b")        # a la Autoridad Sanitaria dentro de 24 h
_C = ("centinela", "art.1 lit.c")     # vigilancia centinela
_P = ("?", "posterior al decreto")    # agregada por resolucion; POR CONFIRMAR

# TRANSITORIAS: no son literales del decreto, rigen MIENTRAS DURE LA ALERTA
# epidemiologica. Se distinguen a proposito de _A/_B/_C: un dia la alerta se
# levanta y esta clasificacion deja de valer, mientras que la del decreto no.
# Alertas vigentes: https://epi.minsal.cl/alertas-epidemiologicas-vigentes/
def _ALERTA(tipo, nota=""):
    return (tipo, "alerta vigente" + (f" ({nota})" if nota else ""))

ENO_TIPO = {norm(k): v for k, v in {
    "Botulismo": _A,
    "Carbunco (ántrax)": _A,
    "Enfermedad de Chagas aguda": _A,
    "Enfermedad por virus Chikungunya": _A,
    "Cólera": _A,
    "Dengue": _A,
    "Difteria": _A,
    "Fiebre Amarilla": _A,
    "Síndrome Pulmonar por Hantavirus": _A,
    "Enfermedad invasora por Haemophilus influenzae": _A,
    "Infecciones Respiratorias Agudas Graves (incluidas las neumonías que requieren hospitalización)": _A,
    "Leptospirosis": _A,
    "Malaria": _A,
    "Meningitis Bacterianas": _A,
    "Enfermedad invasora por Neisseria Meningitis (Enfermedad Meningocócica)": _A,
    "Fiebres hemorrágicas virales (Ebola, Lassa, Marburg, Crimea-Congo, otros)": _A,
    "Peste (plaga)": _A,
    "Parálisis Flácidas Agudas (poliomielitis)": _A,
    "Rabia": _A,
    "Rubeóla": _A,
    "Sarampión": _A,
    "Rubéola Congénita": _A,
    "Triquinosis": _A,
    "Infección por virus del Nilo Occidental": _A,
    "Enfermedad por virus Zika": _A,
    "Brucelosis": _B,
    "Enfermedad de Chagas crónico (Tripanosomiasis Americana)": _B,
    "Cisticercosis": _B,
    "Enfermedad de Creutzfeldt-Jakob": _B,
    "Coqueluche (tos ferina)": _B,
    "Fiebre Tifoidea y Paratifoidea": _B,
    "Fiebre Q": _B,
    "Hepatitis Virales (por virus A, B, C y E)": _B,
    "Hidatidosis (equinococosis)": _B,
    "Infección gonocócica": _B,
    "Leishmaniasis": _B,
    "Lepra (Enfermedad de Hansen)": _B,
    "Listeriosis": _B,
    "Parotiditis viral (paperas)": _B,
    "Psitacosis": _B,
    "Rickettiosis": _B,
    "Sífilis": _B,
    "Síndrome Hemolítico Urémico": _B,
    "Streptococcus pneumoniae. Enfermedad invasora": _B,
    "Tétanos neonatal": _B,
    "Tétanos": _B,
    "Tuberculosis": _B,
    "Enfermedad por virus de la Inmunodeficiencia Humana": _B,
    "Enfermedades diarreicas agudas en menores de 5 años": _C,
    "Influenza y otras infecciones respiratorias agudas Virales": _C,
    "Infección por virus del Papiloma Humano": _C,
    "Infección por virus Varicela": _C,
    # Agregadas al listado del DEIS DESPUES del decreto (por resolucion): el
    # literal que les corresponde hay que confirmarlo antes de darlo por bueno.
    # Se reviso https://epi.minsal.cl/alertas-epidemiologicas-vigentes/ y NO
    # alcanza: el oficio de Mpox (CP 10500/2026) manda "notificar por la via mas
    # expedita" pero no cita el literal del art. 1 (o sea, es inferencia, no
    # norma), y el de S. pyogenes (Ord. B51 1080) es un PDF escaneado sin texto.
    # Se dejan en '?' A PROPOSITO: un default silencioso aca es peor que un hueco
    # visible, porque nadie volveria a mirarlo.
    "Viruela": _P,
    "Viruela de los monos (Mpox)": _ALERTA("inmediata"),
    "Tifus de los matorrales": _P,
    "Streptococcus pyogenes. Enfermedad invasora": _ALERTA(
        "centinela", "diaria solo en hospitales"),
}.items()}

# Las que siguen SIN clasificar. Declarado explicito para que el test lo compare:
# si el DEIS agrega una enfermedad nueva y nadie la clasifica, el test cae. Un
# hueco conocido y listado es deuda; un hueco que aparece solo es un bug.
ENO_SIN_CLASIFICAR = frozenset({"Viruela", "Tifus de los matorrales"})


# -- Codigos ----------------------------------------------------------------
def norm_codigo(v):
    """Codigo CIE-10 canonico: MAYUSCULA, sin punto ni espacios. '' si no hay.
    'J20.9' / 'j20 9' / ' J209 ' -> 'J209'. Es la forma del DEIS; RAYEN usa el
    punto, asi que TODO cruce entre fuentes pasa por aca."""
    return re.sub(r"[^A-Z0-9]", "", str(v).upper()) if v is not None and v == v else ""


def con_punto(cod):
    """'J209' -> 'J20.9' (solo para MOSTRAR; el canonico es sin punto)."""
    c = norm_codigo(cod)
    return f"{c[:3]}.{c[3:]}" if len(c) > 3 else c


def en_rango(cod, desde, hasta):
    """True si `cod` cae en el rango CIE-10 [desde, hasta] inclusive, comparando
    solo los caracteres que el rango define. `en_rango('J209','J09','J22')`.
    Funciona lexicograficamente porque los codigos son LETRA + digitos con cero
    a la izquierda ('J09' < 'J20' < 'J99'). Evita expandir miles de codigos."""
    c, d, h = norm_codigo(cod), norm_codigo(desde), norm_codigo(hasta)
    return bool(c) and d <= c[:len(d)] and c[:len(h)] <= h


def expandir(txt):
    """Parte la celda de codigos del ENO en patrones. Acepta las DOS formas que
    trae el DEIS: lista 'A000, A001, A009' y rango 'J00-J99'. Devuelve la lista
    de patrones tal cual (los rangos NO se expanden: los resuelve `en_rango`)."""
    out = []
    for parte in re.split(r"[,;]", str(txt or "")):
        parte = parte.strip()
        if not parte:
            continue
        m = re.match(r"^([A-Za-z]\d+)\s*-\s*([A-Za-z]\d+)$", parte)
        out.append(f"{norm_codigo(m.group(1))}-{norm_codigo(m.group(2))}" if m
                   else norm_codigo(parte))
    return [c for c in out if c]


def _casa(cod, patron):
    """El codigo `cod` corresponde al patron ('J209' o 'J00-J99')."""
    if "-" in patron:
        d, h = patron.split("-", 1)
        return en_rango(cod, d, h)
    return norm_codigo(cod) == patron


# -- Lectura de los .xlsx del DEIS ------------------------------------------
def _hojas(entrada):
    """[(titulo, [filas])] de todas las hojas de un .xlsx (no solo la activa,
    como rem_utils.leer_xlsx: la Lista Tabular trae 3)."""
    import openpyxl
    wb = openpyxl.load_workbook(entrada, read_only=True, data_only=True)
    try:
        return [(ws.title, list(ws.iter_rows(values_only=True))) for ws in wb.worksheets]
    finally:
        wb.close()


def _fila_header(filas, *tokens, max_scan=12):
    """Indice de la 1a fila cuyas celdas contienen TODOS los tokens (una celda
    por token). None si no aparece. Detectar el header en vez de hardcodearlo:
    la edicion 2018 lo tenia en la fila 1 y la de 2026 en la 2."""
    want = [norm(t) for t in tokens]
    for i, fila in enumerate(filas[:max_scan]):
        celdas = [norm(v) for v in fila]
        if all(any(t in c for c in celdas) for t in want):
            return i
    return None


def _col(fila, token):
    """Indice de la 1a celda de `fila` que contiene `token` (normalizado)."""
    t = norm(token)
    return next((j for j, v in enumerate(fila) if t in norm(v)), None)


def _leer_cie10(entrada, log):
    """Lista Tabular CIE-10 -> COD | DESC | TIPO. TIPO sale del NOMBRE de la
    hoja (cruz o daga / asterisco / causa externa), que es lo unico que las
    distingue; el DEIS le cambia la redaccion entre ediciones, asi que se
    matchea por substring, no por titulo exacto."""
    import pandas as pd
    marcas = [("asterisco", "asterisco"), ("externa", "causa externa"),
              ("cruz", "cruz o daga"), ("daga", "cruz o daga")]
    filas_out = []
    for titulo, filas in _hojas(entrada):
        tn = norm(titulo)
        tipo = next((v for k, v in marcas if norm(k) in tn), None)
        hi = _fila_header(filas, "codigo", "descripcion")
        if tipo is None or hi is None:
            log(f"[cie10] hoja {titulo!r} ignorada (sin header Codigo/Descripcion)")
            continue
        jc, jd = _col(filas[hi], "codigo"), _col(filas[hi], "descripcion")
        n0 = len(filas_out)
        for fila in filas[hi + 1:]:
            cod = norm_codigo(fila[jc]) if jc < len(fila) else ""
            if cod:
                filas_out.append((cod, str(fila[jd] or "").strip(), tipo))
        log(f"[cie10] {titulo!r}: {len(filas_out) - n0} codigos ({tipo})")
    return pd.DataFrame(filas_out, columns=["COD", "DESC", "TIPO"])


def _leer_eno(entrada, log):
    """Lista ENO -> ENFERMEDAD | TIPO | ART | COD, UNA FILA POR CODIGO (formato
    largo: cruzar por codigo es el 90% del uso). El tipo de notificacion NO
    viene en el archivo: lo pone ENO_TIPO desde el Decreto 7/2019."""
    import pandas as pd
    titulo, filas = _hojas(entrada)[0]
    hi = _fila_header(filas, "codigo cie-10") or 0
    jc = _col(filas[hi], "codigo cie-10")
    filas_out, sin_tipo = [], []
    for fila in filas[hi + 1:]:
        enf = str(fila[0] or "").strip()
        if not enf:
            continue
        tipo, art = ENO_TIPO.get(norm(enf), ("?", "sin clasificar"))
        if tipo == "?":
            sin_tipo.append(enf)
        for cod in expandir(fila[jc] if jc < len(fila) else ""):
            filas_out.append((enf, tipo, art, cod))
    log(f"[eno] {titulo!r}: {len(filas_out)} pares enfermedad-codigo")
    if sin_tipo:
        log(f"[eno] AVISO: {len(sin_tipo)} enfermedad(es) SIN tipo de notificacion "
            f"confirmado (agregadas despues del Decreto 7/2019, o nuevas): "
            + "; ".join(sin_tipo))
    return pd.DataFrame(filas_out, columns=["ENFERMEDAD", "TIPO", "ART", "COD"])


def _leer_ges(entrada, log):
    """GES 90 -> ID | PROBLEMA | COD | OBS. Se descarta el `descriptor` del
    .xlsx: es la glosa CIE-10, que ya esta en el catalogo cie10 (y duplicarla
    aca engordaria el slim al pedo)."""
    import pandas as pd
    mapa = {"ID": ("subs", ["ID", "PROBLEMA"]), "PROBLEMA": ("exact", "problema_salud"),
            "COD": ("exact", "cie10"), "OBS": ("exact", "observaciones")}
    for titulo, filas in _hojas(entrada):
        hi = _fila_header(filas, "id_problema", "cie10")
        if hi is None:
            continue
        col = resolver_columnas(list(filas[hi]), mapa)
        idx = {k: list(filas[hi]).index(c) for k, c in col.items() if c is not None}
        if "COD" not in idx:
            continue
        filas_out = []
        for fila in filas[hi + 1:]:
            cod = norm_codigo(fila[idx["COD"]]) if idx["COD"] < len(fila) else ""
            if not cod:
                continue
            g = lambda k: str(fila[idx[k]] or "").strip() if k in idx and idx[k] < len(fila) else ""
            filas_out.append((g("ID"), g("PROBLEMA"), cod, g("OBS")))
        log(f"[ges] {titulo!r}: {len(filas_out)} pares problema-codigo")
        return pd.DataFrame(filas_out, columns=["ID", "PROBLEMA", "COD", "OBS"])
    raise ValueError("no encontre la hoja del catalogo GES (header id_problema + cie10)")


# -- Registro ---------------------------------------------------------------
CATALOGOS = {
    "cie10": {
        "titulo": "Lista Tabular CIE-10 (DEIS/MINSAL)",
        "url": "https://repositoriodeis.minsal.cl/ContenidoSitioWeb2020/uploads/2021/03/"
               "Lista%20tabular%20CIE-10%20-%20agosto%202026.xlsx",
        "leer": _leer_cie10,
        "clave": "COD",
    },
    "eno": {
        "titulo": "Enfermedades de Notificacion Obligatoria (Decreto 7/2019)",
        "url": "https://repositoriodeis.minsal.cl/ContenidoSitioWeb2020/uploads/2021/03/"
               "DEIS-EPI-ENO-Decreto%207%202019%20actualizaci%C3%B3n%20agosto%202026.xlsx",
        "leer": _leer_eno,
        "clave": "COD",
    },
    "ges": {
        "titulo": "GES 90 problemas de salud <-> CIE-10",
        "url": "https://repositoriodeis.minsal.cl/ContenidoSitioWeb2020/uploads/2021/03/"
               "GES%2090%20CIE-10%20v1_4.xlsx",
        "leer": _leer_ges,
        "clave": "COD",
    },
}


# -- Ubicacion de los datos -------------------------------------------------
def _carpetas():
    """Donde buscar catalogos/, en orden: bundle de PyInstaller, junto al .exe,
    y el repo. Mismo criterio que autorem._slim_por_defecto."""
    out = []
    if getattr(sys, "frozen", False):
        out.append(Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent)) / CARPETA)
        out.append(Path(sys.executable).parent / CARPETA)
    out.append(Path(__file__).resolve().parent.parent / CARPETA)
    return out


def carpeta_datos(crear=False):
    """La 1a carpeta catalogos/ que exista (o la del repo si `crear`)."""
    for c in _carpetas():
        if c.is_dir():
            return c
    destino = _carpetas()[-1]
    if crear:
        destino.mkdir(parents=True, exist_ok=True)
    return destino


def fuentes():
    """Provenance de los slims vendorizados: {nombre: {url, edicion, filas...}}.
    Es lo que permite decir DE QUE EDICION habla el numero que se reporta."""
    f = carpeta_datos() / FUENTES
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _slim(nombre):
    p = carpeta_datos() / f"{nombre}.csv.gz"
    return p if p.exists() else None


def _dropin(nombre):
    """.xlsx dejado A PROPOSITO en catalogos/ para pisar al slim (edicion nueva
    del DEIS sin recompilar el .exe). El mas reciente por fecha de archivo."""
    cands = sorted(carpeta_datos().glob(f"{nombre}*.xlsx"), key=lambda p: p.stat().st_mtime)
    return cands[-1] if cands else None


# -- Carga ------------------------------------------------------------------
_CACHE = {}


def cargar(nombre, entrada=None, log=None, recargar=False):
    """DataFrame del catalogo `nombre` (ver CATALOGOS). Cascada: `entrada`
    explicita > .xlsx drop-in en catalogos/ > slim vendorizado. Cachea por
    proceso (los catalogos no cambian en caliente). `.attrs['fuente']` y
    `.attrs['edicion']` dicen de donde salio."""
    import pandas as pd
    log = log or (lambda *_: None)
    if nombre not in CATALOGOS:
        raise KeyError(f"catalogo desconocido: {nombre!r} (hay: {', '.join(CATALOGOS)})")
    clave = (nombre, str(entrada))
    if not recargar and clave in _CACHE:
        return _CACHE[clave]

    meta = fuentes().get(nombre, {})
    xlsx = Path(entrada) if entrada else _dropin(nombre)
    if xlsx is not None and Path(xlsx).exists():
        origen = "elegido a mano" if entrada else "DROP-IN en catalogos/"
        log(f"[{nombre}] leyendo el .xlsx {origen}: {Path(xlsx).name}")
        log(f"[{nombre}] OJO: pisa al catalogo que trae la herramienta "
            f"(edicion {meta.get('edicion', '?')}). Los resultados salen de ESE archivo.")
        d = CATALOGOS[nombre]["leer"](xlsx, log)
        d.attrs["fuente"], d.attrs["edicion"] = str(xlsx), "(archivo cargado)"
    else:
        p = _slim(nombre)
        if p is None:
            raise FileNotFoundError(
                f"no encuentro el catalogo {nombre!r}: falta '{CARPETA}/{nombre}.csv.gz'. "
                f"Generalo con  python tools/catalogos_deis.py --slim {nombre}  "
                f"o deja el .xlsx del DEIS en '{CARPETA}/'.")
        d = pd.read_csv(p, dtype=str, keep_default_na=False)
        d.attrs["fuente"], d.attrs["edicion"] = str(p), meta.get("edicion", "?")
        log(f"[{nombre}] {CATALOGOS[nombre]['titulo']} - edicion {d.attrs['edicion']} "
            f"({len(d)} filas)")
    _CACHE[clave] = d
    return d


# -- Consultas --------------------------------------------------------------
def descripcion(cod, log=None):
    """Glosa CIE-10 del codigo, o '' si no existe en la Lista Tabular."""
    d = cargar("cie10", log=log)
    hit = d.loc[d["COD"] == norm_codigo(cod), "DESC"]
    return hit.iloc[0] if len(hit) else ""


def existe(cod, log=None):
    """El codigo esta en la Lista Tabular vigente. False = codigo invalido o de
    una edicion anterior -> justamente lo que el anotador batch tiene que gritar."""
    d = cargar("cie10", log=log)
    return bool((d["COD"] == norm_codigo(cod)).any())


def _cruzar(nombre, cod, log=None):
    """Filas del catalogo cuyo patron de codigo casa con `cod` (maneja rangos)."""
    d = cargar(nombre, log=log)
    c = norm_codigo(cod)
    if not c:
        return d.iloc[0:0]
    exacto = d[d["COD"] == c]
    rangos = d[d["COD"].str.contains("-", regex=False)]
    if len(rangos):
        rangos = rangos[[_casa(c, p) for p in rangos["COD"]]]
    import pandas as pd
    return pd.concat([exacto, rangos]) if len(rangos) else exacto


def eno_de(cod, log=None):
    """[(enfermedad, tipo, articulo)] si el codigo es de notificacion obligatoria."""
    h = _cruzar("eno", cod, log)
    return list(zip(h["ENFERMEDAD"], h["TIPO"], h["ART"]))


def ges_de(cod, log=None):
    """[(id_problema, problema)] de los problemas GES que incluyen el codigo.
    Deduplicado: el .xlsx del DEIS repite el par problema-codigo cuando el codigo
    entra al problema por dos vias (Lista Tabular y Termino de Inclusion)."""
    h = _cruzar("ges", cod, log)
    return list(dict.fromkeys(zip(h["ID"], h["PROBLEMA"])))


def anotar(codigos, log=None):
    """Anotador BATCH: lista/Serie de codigos -> DataFrame con una fila por
    codigo distinto y las columnas COD | DESC | EXISTE | ENO | ENO_TIPO | GES.
    Es la utilidad que le da sentido a la pestana: se le pasa la columna de
    diagnostico de un export RAYEN y devuelve que significa cada codigo, cuales
    son notificables y cuales NO EXISTEN en la Lista Tabular vigente."""
    import pandas as pd
    cie = cargar("cie10", log=log)
    glosa = dict(zip(cie["COD"], cie["DESC"]))
    filas = []
    for c in dict.fromkeys(norm_codigo(x) for x in codigos):
        if not c:
            continue
        eno, ges = eno_de(c, log), ges_de(c, log)
        filas.append({
            "COD": con_punto(c),
            "DESC": glosa.get(c, ""),
            "EXISTE": "SI" if c in glosa else "NO",
            "ENO": "; ".join(e for e, _, _ in eno),
            "ENO_TIPO": "; ".join(sorted({t for _, t, _ in eno})),
            "GES": "; ".join(f"{i}. {p}" for i, p in ges),
        })
    return pd.DataFrame(filas, columns=["COD", "DESC", "EXISTE", "ENO", "ENO_TIPO", "GES"])
