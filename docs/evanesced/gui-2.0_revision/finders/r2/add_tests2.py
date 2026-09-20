"""Tests de los 6 de la 2a pasada de la ronda 10 (antes de `def _main`, respeta CRLF)."""
from pathlib import Path

T = Path(r"E:\git\Autorem\tests")

BLOQUES = {
"test_sp_p6.py": '''
def test_formulario_sin_instrumento_falla_y_sin_edad_va_a_revisar():
    """Ronda 10, 2a pasada: (a) sin columna INSTRUMENTO, todos los dx que exigen medico
    salian NO y el P6 subcontaba callado (los FR mantienen viva la base) ->
    sin_columnas. (b) una persona sin edad contaba en Ambos y en NINGUNA banda, sin
    fila en Revisar -> 'Sin edad' en Revisar_Administrativo."""
    tdah = {"rut": "11111111-1", "fecha": date(2026, 7, 1), _Q[57]: "SI", _Q[58]: "INGRESO"}
    p = _mk_formulario([tdah])
    wb = openpyxl.load_workbook(p); ws = wb.active
    ws.delete_cols([c.value for c in ws[17]].index("INSTRUMENTO") + 1); wb.save(p)
    try:
        pob.cargar_formulario_sm(str(p), log=_quiet)
        assert False, "debio levantar ArchivoInvalido"
    except ArchivoInvalido as e:
        assert e.categoria == "sin_columnas" and "INSTRUMENTO" in str(e), (e.categoria, str(e))

    r = _p6(_poblacion([tdah], [{"rut": "11111111-1", "edad": ""}], ada_filas=[_sm("11111111-1")]))
    assert _fila_p6(r["grid"], 35)["Ambos"] == 1
    assert "Sin edad: cuenta en Ambos, en ninguna banda" in _motivos(r), _motivos(r)
    r = _p6(_poblacion([tdah], [{"rut": "11111111-1"}], ada_filas=[_sm("11111111-1")]))
    assert not [m for m in _motivos(r) if m.startswith("Sin edad")]          # control


''',
"test_autorem.py": '''
def test_a05_sin_ninguna_fecha_legible_no_manda_a_archivo_completo():
    """Ronda 10, 2a pasada: con TODAS las FECHA FORMULARIO ilegibles el mes_vacio decia
    "revisa el mes ... o elige Archivo completo", y eso procesa el año entero como si
    fuera el mes. Ahora sin_fecha, que dice lo contrario. Con fechas legibles de otro mes
    sigue siendo mes_vacio."""
    def _cat(fecha):
        p = _TMP / "a05_fecha.xlsx"
        wb = openpyxl.Workbook(); ws = wb.active
        ws.append(["Servicio de Salud", None]); ws.append(["Filtros: bla", None])
        ws.append(["NUMERO TIPO IDENTIFICACION", "AÑO APLICACIÓN FORMULARIO", "SEXO",
                   "FECHA FORMULARIO", "18.- ¿ TIENE DEPRESIÓN ?", "18.- ESTADO"])
        ws.append(["11111111-1", 45, "Mujer", fecha, "SI", "EGRESO ALTA"]); wb.save(p)
        try:
            egresos.procesar(p, _TMP / "no_se_escribe.xlsx", log=_quiet, mes=(2026, 8))
        except sm.ArchivoInvalido as e:
            return e.categoria, str(e)
        return None, ""
    cat, msg = _cat("31-31-2026")
    assert cat == "sin_fecha" and "NO lo proceses" in msg, (cat, msg)
    assert _cat("06/07/2026")[0] == "mes_vacio"                               # otro mes


''',
"test_a23.py": '''
def test_estratificacion_sin_columna_de_diagnosticos_falla():
    """Ronda 10, 2a pasada: sin DETALLE DIAGNOSTICOS / CONDICIONES CRONICAS el reporte
    cargaba y no aportaba NADA a SALA, callado -> sin_columnas. Y el `or` entre las dos
    trataba el indice 0 como 'no esta'."""
    from programas.rem_utils import ArchivoInvalido
    try:
        a23.cargar_estrat(_mk_estrat(["RUT", "DV", "COMUNA"], [[11111111, "1", "Maipu"]]))
        assert False, "debio levantar ArchivoInvalido"
    except ArchivoInvalido as e:
        assert e.categoria == "sin_columnas", e.categoria
    s = a23.cargar_estrat(_mk_estrat(["DETALLE DIAGNOSTICOS", "RUT", "DV"],
                                     [["Asma Moderada", 11111111, "1"]]))
    assert s.loc["11111111-1"] == "ASMA MODERADA"                  # col 0 SI cuenta


''',
"test_estamentos.py": '''
def test_rechaza_reporte_con_filas_pero_sin_estamentos():
    """Ronda 10, 2a pasada: exigir_filas_ws mira que HAYA filas, no que alguna sirva.
    Con Instrumento en blanco en todas, la tabla salia {} y la corrida seguia con el
    cache solo, sin decirlo -> sin_datos."""
    try:
        est.cargar_estamentos(_reporte("cupos_sin_estam.xlsx", [("ANA PEREZ", "", "Control", "A")]),
                              log=_quiet)
        assert False, "debio rechazar un reporte sin ningun estamento"
    except est.ArchivoInvalido as e:
        assert e.categoria == "sin_datos", e.categoria


''',
"test_gui_registro.py": '''
def test_resumen_de_a23_y_sm_muestra_los_avisos():
    """Ronda 10, 2a pasada: los resumenes de A23 y SM decian "Listo" sin sus avisos
    (solo log y LEEME), y SM descartaba los del A03 (gemelo de §1.J.6, que solo arreglo
    Poblacion). Ahora los listan; sin avisos no inventan nada."""
    import pandas as pd
    from gui.paginas import a23 as pa23, sm as psm
    av = ("Seccion G (inasistentes cronicos)", "SUBCONTADO", "falta historial", "cargar mas")
    fer = pd.DataFrame({"RUN": ["A"]}); fer.attrs.update(seccion_g={}, avisos=[av])
    txt = pa23.resumen({"fer": fer, "salida": "x.xlsx", "mes": (2026, 7)})
    assert "SUBCONTADO" in txt and "falta historial" in txt, txt
    fer.attrs["avisos"] = []
    assert "aviso" not in pa23.resumen({"fer": fer, "salida": "x.xlsx", "mes": (2026, 7)})

    av03 = ("Tabla D.3", "SUBCONTADO", "1 aplicacion fuera de rango", "revisar")
    E = pd.DataFrame({"casilla": ["A04"]})
    E.attrs.update(tablas={"SM_Resumen": pd.DataFrame({"Casilla": ["A04"], "Total mes": [1]})},
                   avisos=[av])
    base = {"mes": (2026, 7), "solo_a03": False, "E": E, "n_tp": 0, "n_a03": 3,
            "por_inst_a03": {"PSC": 3}, "salida": "x.xlsx", "salida_a03": "y.xlsx",
            "avisos_a03": [av03]}
    txt = psm.resumen(base)
    assert "falta historial" in txt and "fuera de rango" in txt, txt
    txt = psm.resumen(dict(base, solo_a03=True))
    assert "fuera de rango" in txt, txt


''',
}

for nombre, bloque in BLOQUES.items():
    p = T / nombre
    s = p.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in s else "\n"
    i = s.index("def _main():")
    s = s[:i] + bloque.lstrip("\n").replace("\n", nl) + s[i:]
    p.write_bytes(s.encode("utf-8"))
print("ok")
