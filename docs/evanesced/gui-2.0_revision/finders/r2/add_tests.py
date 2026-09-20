"""Inserta los tests de la ronda 10 antes de `def _main` (respeta CRLF/LF)."""
from pathlib import Path

T = Path(r"E:\git\Autorem\tests")

SP_P6 = '''
def test_base_vacia_del_p6_y_anio_vacio_del_historico_fallan_en_la_fuente():
    """Ronda 10 (R2 estatica): (a) Estado con otro vocabulario, o el RUN del ADA en otro
    formato que el del Inscritos, dejaban la BASE del P6 (Estado x Activo 12m x
    Ingresado) vacia -> P6 entero en 0 con "Listo" -> sin_datos. (b) un año del
    historico que bajo solo con encabezado se perdia callado en el concat -> sin_datos
    NOMBRANDO el archivo."""
    import shutil
    ing = {"rut": "11111111-1", "fecha": date(2026, 7, 1), _Q[18]: "SI", _Q[19]: "19.- INGRESO"}
    assert int(_fila_p6(_p6(_poblacion([ing], [{"rut": "11111111-1"}],
                                       [_sm("11111111-1")]))["grid"], 25)["Ambos"]) >= 0   # control
    for etq, ins, ada in (("Estado 'Activa'", [{"rut": "11111111-1", "estado": "Activa"}],
                           [_sm("11111111-1")]),
                          ("RUN del ADA con puntos", [{"rut": "11111111-1"}], [_sm("11.111.111-1")])):
        P = _poblacion([ing], ins, ada)
        try:
            _p6(P)
            assert False, f"{etq}: debio levantar ArchivoInvalido"
        except ArchivoInvalido as e:
            assert e.categoria == "sin_datos", (etq, e.categoria)

    bueno = _mk_formulario([ing])
    b2 = _TMP / "form_2026.xlsx"; shutil.copy(bueno, b2)
    vacio = _TMP / "form_2025.xlsx"
    wb = openpyxl.load_workbook(bueno); ws = wb.active; ws.delete_rows(18, ws.max_row); wb.save(vacio)
    try:
        pob.cargar_formulario_sm([str(vacio), str(b2)], log=_quiet)
        assert False, "debio levantar ArchivoInvalido por el año vacio"
    except ArchivoInvalido as e:
        assert e.categoria == "sin_datos" and "form_2025.xlsx" in str(e), (e.categoria, str(e))


'''

SCREENING = '''
def test_casillero_cruzado_y_puntajes_fuera_de_rango_no_dan_d3_en_0():
    """Ronda 10 (R2 estatica): los casilleros de la GUI FIJAN el instrumento y el
    contenido no se miraba: un PSC-Y en el casillero GHQ-12 (todo fuera de rango) o un
    GHQ-12 en el del PSC (todo bajo 33) daban la D.3 en 0 con "N aplicaciones" ->
    instrumento_cruzado. Sin nombre detectable y TODO fuera de rango -> sin_datos;
    ALGUNOS fuera de rango -> aviso SUBCONTADO (antes solo el log)."""
    from programas.rem_utils import ArchivoInvalido

    def _cat(slot, p):
        try:
            scr.procesar_unificado({slot: p}, _TMP / "x_out.xlsx", log=_quiet)
        except ArchivoInvalido as e:
            return e.categoria
        return None

    pscy = _iris("x_pscy.xlsx", "Cuestionario para Adolescentes (PSC-Y)", [
        ("1-9", 12, "Hombre", "", "", "Ingreso", 40, "Bajo")])
    ghq = _iris("x_ghq.xlsx", "Cuestionario de Salud de Goldberg", [
        ("2-7", 30, "Mujer", "", "", "Ingreso", 9, "Indicativos de presencia de psicopatologia")])
    assert _cat("GHQ-12", pscy) == "instrumento_cruzado"
    assert _cat("PSC", ghq) == "instrumento_cruzado"
    assert _cat("PSC-Y", pscy) is None and _cat("GHQ-12", ghq) is None           # control

    sin_nombre = _iris("x_anon.xlsx", "", [
        ("3-5", 30, "Mujer", "", "", "Ingreso", 40, ""), ("4-3", 31, "Hombre", "", "", "Egreso", 66, "")])
    assert _cat("GHQ-12", sin_nombre) == "sin_datos"
    uno_fuera = _iris("x_uno.xlsx", "Cuestionario de Salud de Goldberg", [
        ("5-1", 30, "Mujer", "", "", "Ingreso", 15, ""), ("6-K", 31, "Hombre", "", "", "Ingreso", 8, "")])
    res = scr.procesar_unificado({"GHQ-12": uno_fuera}, _TMP / "x_out2.xlsx", log=_quiet)
    assert any(a[1] == "SUBCONTADO" and "fuera del rango" in a[2] for a in res["avisos"]), res["avisos"]


'''

RESCATE = '''
def test_inscritos_con_filas_pero_ningun_run_usable_lo_dice():
    """Ronda 10: el guard de c38a8cc quedo DETRAS de cargar_canonico (que ya corta el
    solo-encabezado), asi que solo lo alcanza un Inscritos CON filas y ninguna usable.
    Su mensaje decia "no trae ninguna fila de datos" -> ahora dice por que. Y las filas
    sin RUN ya no sobreviven como la persona 'None' (astype(str))."""
    for filas, clave in (([{"rut": "11111111-1", "tipoid": "RUN Responsable"}], "1 'RUN Responsable'"),
                         ([{"rut": None}, {"rut": ""}], "2 sin RUN")):
        try:
            pob.cargar_inscritos(_mk_inscritos(filas), log=_quiet)
            assert False, f"{clave}: debio levantar ArchivoInvalido"
        except ArchivoInvalido as ai:
            assert ai.categoria == "sin_datos" and clave in str(ai), str(ai)
    d = pob.cargar_inscritos(_mk_inscritos([{"rut": "11111111-1"}, {"rut": None}]), log=_quiet)
    assert list(d["RUN"]) == ["11111111-1"], list(d["RUN"])


def test_rescate_sin_columnas_de_pasivacion_falla():
    """Ronda 10: sin MOTIVO/FECHA PASIVACION (opcionales para el P6) Posibles_Fallecidos,
    Fallecidos_mes y Posibles_Traslados salian VACIAS sin aviso: la lista de a quien
    llamar sin la marca de fallecido. Ahora el rescate falla (el P6 no se entera)."""
    ada = _mk_ada([_sm("10000001-1", date(2026, 2, 10))])
    for col in ("MOTIVO PASIVACION", "FECHA PASIVACION"):
        _INS_HDR.remove(col)
        try:
            ins = _mk_inscritos([{"rut": "10000001-1"}])
        finally:
            _INS_HDR.append(col)
        try:
            resc.procesar(str(ins), str(_mk_formulario([])), str(ada), mes=MES, log=_quiet)
            assert False, f"sin {col}: debio levantar ArchivoInvalido"
        except ArchivoInvalido as ai:
            assert ai.categoria == "sin_columnas" and col in str(ai), str(ai)


'''


def insertar(nombre, bloque):
    p = T / nombre
    s = p.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in s else "\n"
    i = s.index("def _main():")
    s = s[:i] + bloque.lstrip("\n").replace("\n", nl) + s[i:]
    p.write_bytes(s.encode("utf-8"))


insertar("test_sp_p6.py", SP_P6)
insertar("test_screening.py", SCREENING)
insertar("test_rescate_inasistentes.py", RESCATE)
print("ok")
