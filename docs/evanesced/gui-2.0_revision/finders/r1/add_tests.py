from pathlib import Path
R = Path(r"E:\git\Autorem")


def add_before_main(path, block):
    p = R / path
    t = p.read_text(encoding="utf-8")
    nl = "\r\n" if "\r\n" in t else "\n"
    anchor = "def _main():"
    assert t.count(anchor) == 1, path
    t = t.replace(anchor, block.strip("\n").replace("\n", nl) + nl + nl + nl + anchor)
    p.write_bytes(t.encode("utf-8"))


add_before_main("tests/test_screening.py", '''
def test_d3_sin_momento_o_sin_puntaje_no_queda_en_0_callado():
    """Ronda 9 (bug recurrente, 2a pasada): (a) sin momento Ingreso/Egreso en TODA la
    planilla la D.3 salia entera en 0 con "N aplicaciones" en el resumen -> ahora
    ArchivoInvalido; en ALGUNAS filas, aviso SUBCONTADO. (b) sin puntaje pero con el
    RESULTADO de RAYEN, la fila quedaba fuera del D.3 -> ahora cuenta con esa banda y
    avisa REVISAR. (c) sexo vacio: cuenta en Ambos y en ninguna columna H/M -> aviso."""
    from programas.rem_utils import ArchivoInvalido
    form = "Cuestionario para Padres PSC"
    ok = ("1-1", 7, "Hombre", "", "", "Ingreso", 72, "Alto")
    for mom in ("", "Seguimiento"):
        p = _iris(f"m9_{mom or 'vacio'}.xlsx", form, [ok[:5] + (mom,) + ok[6:]])
        try:
            scr.procesar_unificado({"PSC": p}, _TMP / "m9.xlsx", log=_quiet)
            assert False, f"momento {mom!r}: debio levantar ArchivoInvalido"
        except ArchivoInvalido as e:
            assert e.categoria == "sin_datos", e.categoria
    p = _iris("m9_mixto.xlsx", form, [ok, ok[:5] + ("",) + ok[6:]])
    res = scr.procesar_unificado({"PSC": p}, _TMP / "m9b.xlsx", log=_quiet)
    assert int(res["tabla"]["Ambos"].sum()) == 1
    assert any(a[1] == "SUBCONTADO" and "momento" in a[2] for a in res["avisos"]), res["avisos"]

    p = _iris("m9_sinpunt.xlsx", form, [ok[:6] + (None, "Alto")])
    res = scr.procesar_unificado({"PSC": p}, _TMP / "m9c.xlsx", log=_quiet)
    t = res["tabla"]
    fila = (t["Evaluación"] == "Evaluación al ingreso") & (t["Resultado"] == "Alto")
    assert int(t.loc[fila, "Ambos"].iloc[0]) == 1
    assert any(a[1] == "REVISAR" and "sin puntaje" in a[2] for a in res["avisos"]), res["avisos"]

    p = _iris("m9_sexo.xlsx", form, [ok[:2] + ("",) + ok[3:]])
    res = scr.procesar_unificado({"PSC": p}, _TMP / "m9d.xlsx", log=_quiet)
    assert any("sin sexo" in a[2] for a in res["avisos"]), res["avisos"]
''')

add_before_main("tests/test_sp_p6.py", '''
def test_preguntas_ausentes_y_ada_sin_actividad_sm_no_dan_0_callado():
    """Ronda 9, 2a pasada: (a) las preguntas se ubican por su NUMERO; sin NINGUNA
    (encabezados renombrados) el P6 daba 0 ingresados con avisos=[] -> sin_columnas;
    con ALGUNAS ausentes, aviso SUBCONTADO. (b) un ADA con filas en la ventana de 13
    meses pero ninguna actividad SM daba Activo 12m = NO para todos -> sin_datos."""
    from programas.rem_utils import num_pregunta
    ing = {"rut": "11111111-1", "fecha": date(2026, 8, 1), _Q[18]: "SI", _Q[19]: "19.- INGRESO"}
    ins = [{"rut": "11111111-1"}]

    def _renombrar(p, cuales):
        wb = openpyxl.load_workbook(p); ws = wb.active
        for c in ws[17]:
            if isinstance(c.value, str) and num_pregunta(c.value) in cuales:
                c.value = "PREGUNTA RENOMBRADA"
        wb.save(p)
        return p

    try:
        pob.construir_poblacion(str(_mk_inscritos(ins)),
                                str(_renombrar(_mk_formulario([ing]), set(pob.QUESTIONS))),
                                str(_mk_ada([_sm("11111111-1")])), mes=(2026, 8), log=_quiet)
        assert False, "debio levantar ArchivoInvalido"
    except ArchivoInvalido as e:
        assert e.categoria == "sin_columnas", e.categoria
    P = pob.construir_poblacion(str(_mk_inscritos(ins)),
                                str(_renombrar(_mk_formulario([ing]), {83, 84})),
                                str(_mk_ada([_sm("11111111-1")])), mes=(2026, 8), log=_quiet)
    assert any(a[1] == "SUBCONTADO" and "83" in a[2] for a in P.attrs["avisos"]), P.attrs["avisos"]

    try:
        _poblacion([ing], ins, [{"rut": "11111111-1", "fecha": date(2026, 8, 5), "act": "Curacion"}])
        assert False, "debio levantar ArchivoInvalido"
    except ArchivoInvalido as e:
        assert e.categoria == "sin_datos", e.categoria
''')

add_before_main("tests/test_a23.py", '''
def test_mes_sin_nada_respiratorio_y_otros_sin_medico_no_dan_0_callado():
    """Ronda 9, 2a pasada: (a) atenciones del mes sin NADA respiratorio -> los 27
    indicadores en NO con "Listo" -> ahora sin_datos. (b) 'Otros Cronicos' sin columna
    INSTRUMENTO -> _med False para todos y SALA/G en 0 -> sin_columnas; con la columna
    pero sin ningun medico -> aviso EN 0."""
    from programas.rem_utils import ArchivoInvalido
    nada = [{"NUMERO TIPO IDENTIFICACION": "A", "FECHA ATENCION": date(2026, 7, 10),
             "INSTRUMENTO": "Enfermero(a)", "ACTIVIDADES": "Curacion simple"}]
    try:
        a23.procesar(_mk(nada), mes=(2026, 7), log=_quiet)
        assert False, "debio levantar ArchivoInvalido"
    except ArchivoInvalido as e:
        assert e.categoria == "sin_datos", e.categoria

    o = _mk_otros([dict(_G_OT, FNAC=date(1980, 1, 1))])
    wb = openpyxl.load_workbook(o); ws = wb.active; ws.delete_cols(3); wb.save(o)   # sin INSTRUMENTO
    try:
        a23.procesar(_mk(_G_ATEN), otros=o, mes=(2026, 7), log=_quiet)
        assert False, "debio levantar ArchivoInvalido"
    except ArchivoInvalido as e:
        assert e.categoria == "sin_columnas", e.categoria

    fer = a23.procesar(_mk(_G_ATEN), otros=_mk_otros([dict(_G_OT, INSTR="Kinesiologo(a)")]),
                       mes=(2026, 7), log=_quiet)
    assert any(a[0].startswith("SALA") and a[1] == "EN 0" for a in fer.attrs["avisos"]), fer.attrs["avisos"]
''')

add_before_main("tests/test_sm_actividades.py", '''
def test_sexo_o_edad_fuera_del_grid_se_avisa():
    """Ronda 9, 2a pasada: `grid` cuenta en Ambos una fila sin sexo Hombre/Mujer o sin
    edad, pero en ninguna columna H/M ni tramo -> las columnas que se pegan suman menos
    que el total, callado. Ahora aviso REVISAR con el conteo."""
    E, _ = _run([{"run": "A", "id": "1", "fecha": date(2026, 7, 3), "act": "Consulta De Salud Mental  ;",
                  "instr": "Médico", "sexo": "Intersexual", "edad": 30},
                 {"run": "B", "id": "2", "fecha": date(2026, 7, 3), "act": "Consulta De Salud Mental  ;",
                  "instr": "Médico", "sexo": "Mujer", "edad": ""}])
    av = [a for a in E.attrs["avisos"] if a[1] == "REVISAR" and "Ambos" in a[2]]
    assert av and "1 sin sexo" in av[0][2] and "1 sin edad" in av[0][2], E.attrs["avisos"]
    E, _ = _run([{"run": "A", "id": "1", "fecha": date(2026, 7, 3), "act": "Consulta De Salud Mental  ;",
                  "instr": "Médico", "sexo": "Mujer", "edad": 30}])
    assert not any("Ambos" in a[2] for a in E.attrs["avisos"])
''')

add_before_main("tests/test_trabajo_perdido.py", '''
def test_maestro_que_no_reconoce_nada_del_mes_se_avisa():
    """Ronda 9, 2a pasada: un Maestro cargado que no reconoce NINGUNA actividad del mes
    dejaba todo en la heuristica sin aviso (el aviso HEURISTICA solo salia sin Maestro)."""
    ada = _mk_ada([_a("Taller de salud mental comunitaria", "ANA")])
    E = tp.procesar(ada, maestro=_mk_maestro([("OTRA COSA DISTINTA", "")]), mes=(2026, 7), log=_quiet)
    assert any(a[1] == "HEURISTICA" for a in E.attrs["avisos"]), E.attrs["avisos"]
    E = tp.procesar(ada, maestro=_mk_maestro([("Taller de salud mental comunitaria", "")]),
                    mes=(2026, 7), log=_quiet)
    assert not any(a[1] == "HEURISTICA" for a in E.attrs["avisos"]), E.attrs["avisos"]
''')
print("ok")
