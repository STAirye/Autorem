#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# SPDX-License-Identifier: GPL-3.0-or-later
# ==========================================================================
"""Pruebas de programas/catalogos.py (capa de catálogos DEIS: CIE-10, ENO, GES).
    python tests/test_catalogos.py"""

import sys
import tempfile
from pathlib import Path

import openpyxl

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from programas import catalogos as cat            # noqa: E402

_TMP = Path(tempfile.mkdtemp(prefix="autorem_catalogos_"))


def _quiet(*_a, **_k): pass


# -- Normalización de códigos -------------------------------------------
def test_norm_codigo_aguanta_los_dos_formatos():
    """DEIS escribe 'J209', RAYEN 'J20.9': el canónico es sin punto. Es LA
    conversión que separa las dos fuentes; si se rompe, todo cruce da 0."""
    for v in ("J209", "J20.9", " j20.9 ", "J20 9", "j 2 0 . 9"):
        assert cat.norm_codigo(v) == "J209", v
    assert cat.norm_codigo(None) == ""
    assert cat.norm_codigo(float("nan")) == ""      # celda vacía leída por pandas
    assert cat.con_punto("J209") == "J20.9"
    assert cat.con_punto("A33") == "A33"            # 3 caracteres: no lleva punto


def test_en_rango_cubre_el_caso_asma():
    """El caso real del A23: asma = J09-J22 menos J19. La comparación es
    lexicográfica y sólo funciona porque los códigos van con cero a la
    izquierda ('J09' < 'J20'); si alguien 'optimiza' a int, se rompe."""
    assert cat.en_rango("J209", "J09", "J22")
    assert cat.en_rango("J090", "J09", "J22")       # borde inferior
    assert cat.en_rango("J229", "J09", "J22")       # borde superior
    assert not cat.en_rango("J081", "J09", "J22")   # justo abajo
    assert not cat.en_rango("J230", "J09", "J22")   # justo arriba
    assert not cat.en_rango("", "J09", "J22")
    assert not cat.en_rango("I120", "J09", "J22")   # otra letra


def test_expandir_acepta_lista_y_rango():
    """El .xlsx del ENO trae las dos formas en la MISMA columna: lista de
    códigos y, en una fila, el rango 'J00-J99'."""
    assert cat.expandir("A000, A001, A009") == ["A000", "A001", "A009"]
    assert cat.expandir("J00-J99") == ["J00-J99"]   # el rango NO se expande
    assert cat.expandir("A051") == ["A051"]
    assert cat.expandir("") == []
    assert cat.expandir(None) == []
    assert cat.expandir("A220,  A221 ") == ["A220", "A221"]


# -- Lectura de los .xlsx del DEIS --------------------------------------
def _xlsx(nombre, hojas):
    """Escribe un .xlsx sintético: {titulo_hoja: [filas]}."""
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for titulo, filas in hojas.items():
        ws = wb.create_sheet(titulo[:31])
        for fila in filas:
            ws.append(list(fila))
    ruta = _TMP / nombre
    wb.save(ruta)
    return ruta


def test_cie10_detecta_header_movido_y_tipo_por_hoja():
    """La edición 2018 tenía el header en la fila 1 y la de 2026 en la 2 (por un
    banner). Se detecta, no se hardcodea. El TIPO sale del NOMBRE de la hoja."""
    ruta = _xlsx("cie.xlsx", {
        "Códigos, más (cruz o daga)": [("", "Lista tabular CIE-10: banner"),
                                       ("Código", "Descripción"),
                                       ("J209", "Bronquitis aguda")],
        "Códigos (asterisco)": [("Código", "Descripción"),     # sin banner
                                ("B950", "Estreptococo grupo A")],
        "Códigos (causa externa)": [("", "banner"), ("", None),
                                    ("Código", "Descripción"),
                                    ("V010", "Peatón lesionado")],
        "Hoja de notas": [("cualquier", "cosa")],              # se ignora
    })
    d = cat._leer_cie10(ruta, _quiet)
    assert len(d) == 3, f"esperaba 3 códigos, salieron {len(d)}"
    assert dict(zip(d["COD"], d["TIPO"])) == {
        "J209": "cruz o daga", "B950": "asterisco", "V010": "causa externa"}


def test_eno_pone_el_tipo_desde_el_decreto_y_avisa_lo_que_no_conoce():
    """El .xlsx del DEIS NO trae inmediata/diaria/centinela: lo pone ENO_TIPO
    desde el Decreto 7/2019. Una enfermedad nueva sale '?' y se AVISA (no se le
    inventa un default, que es justo el bug que nadie volvería a mirar)."""
    ruta = _xlsx("eno.xlsx", {
        "Actual Decreto 7- 2019": [
            ("Enfermedades de notificacion obligatoria.", None, "Código CIE-10 Edición 2018"),
            ("Botulismo", None, "A051"),
            ("Infección por virus Varicela", None, "B010, B011"),
            ("Peste Bubónica Marciana", None, "Z999"),        # inventada: sin tipo
        ]})
    avisos = []
    d = cat._leer_eno(ruta, avisos.append)
    assert len(d) == 4, f"esperaba 4 pares enfermedad-código, salieron {len(d)}"
    tipos = dict(zip(d["ENFERMEDAD"], d["TIPO"]))
    assert tipos["Botulismo"] == "inmediata"
    assert tipos["Infección por virus Varicela"] == "centinela"
    assert tipos["Peste Bubónica Marciana"] == "?"
    assert any("SIN tipo" in a and "Peste Bubónica Marciana" in a for a in avisos), \
        "una enfermedad sin clasificar tiene que avisar RUIDOSO, no pasar callada"


def test_eno_tipo_cubre_todo_el_catalogo_vendorizado():
    """Guardarraíl anti-desfase: si el DEIS agrega enfermedades y se regenera el
    slim sin tocar ENO_TIPO, esto lo muestra. El hueco conocido está DECLARADO
    en ENO_SIN_CLASIFICAR; uno que aparezca solo es un bug, no deuda."""
    d = cat.cargar("eno", log=_quiet)
    sin_tipo = set(d.loc[d["TIPO"] == "?", "ENFERMEDAD"])
    assert sin_tipo == set(cat.ENO_SIN_CLASIFICAR), (
        f"desfase con ENO_SIN_CLASIFICAR: nuevas={sorted(sin_tipo - set(cat.ENO_SIN_CLASIFICAR))} "
        f"ya_resueltas={sorted(set(cat.ENO_SIN_CLASIFICAR) - sin_tipo)}. "
        f"Clasifícalas en ENO_TIPO citando la norma, o saca las resueltas de la lista.")


def test_las_transitorias_se_distinguen_del_decreto():
    """Mpox y S. pyogenes rigen MIENTRAS DURE LA ALERTA, no por el Decreto 7. Si
    el ART no lo dijera, en un año nadie sabría que esa clasificación caducó."""
    d = cat.cargar("eno", log=_quiet)
    art = dict(zip(d["ENFERMEDAD"], d["ART"]))
    assert "alerta vigente" in art["Viruela de los monos (Mpox)"]
    assert "alerta vigente" in art["Streptococcus pyogenes. Enfermedad invasora"]
    assert art["Botulismo"] == "art.1 lit.a", "las del decreto citan su literal"


# -- Catálogos vendorizados (los .csv.gz que shippea la herramienta) ----
def test_los_tres_catalogos_cargan():
    for nombre in cat.CATALOGOS:
        d = cat.cargar(nombre, log=_quiet)
        assert len(d) > 0, f"{nombre} vacío"
        assert "COD" in d.columns, f"{nombre} sin columna COD"
        assert d.attrs.get("edicion"), f"{nombre} sin edición en FUENTES.json"


def test_fuentes_json_documenta_cada_catalogo():
    """FUENTES.json es la procedencia: sin él no se puede decir DE QUÉ EDICIÓN
    habla un número reportado."""
    f = cat.fuentes()
    for nombre in cat.CATALOGOS:
        assert nombre in f, f"falta {nombre} en FUENTES.json (correr --slim)"
        for campo in ("url", "edicion", "filas", "sha256_origen"):
            assert f[nombre].get(campo), f"{nombre}.{campo} vacío"


def test_consultas_sobre_datos_reales():
    """Casos concretos, verificables a mano contra los documentos oficiales."""
    assert "ronquitis" in cat.descripcion("J20.9", log=_quiet)
    assert cat.existe("J209", log=_quiet)
    assert not cat.existe("ZZZ99", log=_quiet), "un código inventado no debe existir"
    # A051 = botulismo, notificación inmediata (Decreto 7/2019 art. 1 lit. a)
    enfermedades = {e for e, _, _ in cat.eno_de("A051", log=_quiet)}
    assert "Botulismo" in enfermedades
    assert "inmediata" in {t for _, t, _ in cat.eno_de("A051", log=_quiet)}
    # J101 entra por el RANGO J00-J99 (influenza, centinela), no por código exacto
    assert "centinela" in {t for _, t, _ in cat.eno_de("J101", log=_quiet)}
    # F32.1 (depresión moderada) es GES: problema 34
    assert any(i == "34" for i, _ in cat.ges_de("F321", log=_quiet))


def test_ges_no_repite_el_mismo_problema():
    """El .xlsx del DEIS lista el par problema-código dos veces cuando entra por
    'Lista Tabular' y por 'Término de Inclusión'. Al consultar es ruido."""
    hits = cat.ges_de("I120", log=_quiet)
    assert len(hits) == len(set(hits)), f"problemas GES duplicados: {hits}"


def test_anotar_marca_los_codigos_que_no_existen():
    """La utilidad batch: la columna EXISTE es la que sirve para auditar un
    export (código mal tipeado o de una edición vieja)."""
    d = cat.anotar(["J20.9", "ZZZ99", "J20.9"], log=_quiet)
    assert len(d) == 2, "los códigos repetidos se colapsan"
    fila = d.set_index("COD")
    assert fila.loc["J20.9", "EXISTE"] == "SI"
    assert fila.loc["ZZZ.99", "EXISTE"] == "NO"
    assert fila.loc["ZZZ.99", "DESC"] == ""


def test_cargar_catalogo_inexistente_falla_claro():
    try:
        cat.cargar("colesterol", log=_quiet)
    except KeyError as e:
        assert "colesterol" in str(e)
    else:
        raise AssertionError("un catálogo inexistente tiene que levantar KeyError")


def test_todo_el_modulo_es_cp1252_safe():
    """Regla dura del proyecto: los logs revientan en la consola cp1252 de
    Windows si se cuela una flecha o un emoji."""
    Path(cat.__file__).read_text(encoding="utf-8").encode("cp1252")


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
