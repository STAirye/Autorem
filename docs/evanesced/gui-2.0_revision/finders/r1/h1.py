import sys, traceback, tempfile, os
from pathlib import Path
from datetime import date
sys.path.insert(0, r"E:\git\Autorem")
sys.path.insert(0, r"E:\git\Autorem\tests")
import _aislar_cache  # noqa  FIRST
import openpyxl
OUT = Path(r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\648a107e-f033-4d56-a55d-a415a58f003e\scratchpad\r1")
from programas.rem_utils import ArchivoInvalido
logs = []
def L(*a, **k): logs.append(" ".join(str(x) for x in a))

def run(name, fn):
    logs.clear()
    try:
        r = fn()
        print(f"\n=== {name}: SUCCESS -> {r}")
        for l in logs[-6:]: print("   log:", l[:250])
    except ArchivoInvalido as e:
        print(f"\n=== {name}: ArchivoInvalido({e.categoria}) {str(e)[:200]!r}")
    except Exception as e:
        print(f"\n=== {name}: CRASH {type(e).__name__}: {e}")
        traceback.print_exc(limit=-4, file=sys.stdout)

import test_sm_actividades as TS
import modulos.rem_sm_actividades as smact
import modulos.rem_sm_trabajo_perdido as tpmod
SIN = {"funcionarios": {}, "omitidos": {}}
ada_ok = [{"run": "A", "id": "1", "fecha": date(2026, 7, 3), "act": "Consulta De Salud Mental  ;",
           "instr": "Médico", "sexo": "Mujer", "edad": 30}]
ada_nosm = [{"run": "Z", "id": "Z1", "fecha": date(2026, 7, 15), "act": "Curacion simple",
             "instr": "Enfermero(a)", "sexo": "Hombre", "edad": 50}]

def sm_nosm():
    E = smact.procesar(TS._mk_ada(ada_nosm), mes=(2026, 7), log=L, dotacion_tabla=SIN)
    resu = E.attrs["tablas"]["SM_Resumen"]
    return f"len(E)={len(E)} resumen={resu.to_dict('records')}"
run("SM ADA rows in month, none SM", sm_nosm)

def sm_grupal_otro_mes():
    g = TS._mk_grupal([{"run": "G", "fecha": date(2026, 6, 3), "act": "Taller", "asiste": "SI",
                        "sexo": "Mujer", "edad": 30, "instr": "Psicólogo(a)", "prest": "X"}])
    E = smact.procesar(TS._mk_ada(ada_ok), grupal=g, mes=(2026, 7), log=L, dotacion_tabla=SIN)
    return len(E)
run("SM grupal rows only in June", sm_grupal_otro_mes)

def sm_multi_vacio_m1():
    mp = TS._mk_multi([{"aten": "1", "m1": ""}])
    E = smact.procesar(TS._mk_ada(ada_ok), mes=(2026, 7), multiprofesional=mp, log=L, dotacion_tabla=SIN)
    return f"len={len(E)} avisos={E.attrs.get('avisos')}"
run("SM multiprof rows but all m1 empty", sm_multi_vacio_m1)

def sm_insc_nomatch():
    i = TS._mk_inscritos([{"NUMERO TIPO IDENTIFICACION": "Q", "SEXO": "Mujer", "GENERO": "Femenina"}])
    E = smact.procesar(TS._mk_ada(ada_ok), mes=(2026, 7), inscritos=i, log=L, dotacion_tabla=SIN)
    return f"avisos={E.attrs.get('avisos')}"
run("SM inscritos 1 row, 0 trans", sm_insc_nomatch)

# TP
import test_trabajo_perdido as TT
def tp_nosm():
    E = tpmod.procesar(TS._mk_ada(ada_nosm), maestro=None, mes=(2026, 7), log=L)
    return f"len={len(E)} avisos={E.attrs.get('avisos')}"
run("TP ADA none SM-ish, no maestro", tp_nosm)
def tp_slim():
    from programas.catalogos import maestro_slim
    E = tpmod.procesar(TS._mk_ada(ada_nosm), maestro=maestro_slim(), mes=(2026, 7), log=L)
    return f"len={len(E)}"
run("TP slim", tp_slim)
def tp_maestro_filtrado():
    m = TT._mk_maestro([("OTRA COSA", "")])
    E = tpmod.procesar(TS._mk_ada(ada_ok), maestro=m, mes=(2026, 7), log=L)
    return f"len={len(E)}"
run("TP maestro 1 irrelevant row", tp_maestro_filtrado)

# dotacion path with empty trib
import programas.dotacion as dot
from programas.rem_utils import cargar_atenciones, filtrar_mes, _rango_mes
def dot_empty():
    d = cargar_atenciones(TS._mk_ada(ada_nosm), log=L)
    ini, fin = _rango_mes((2026, 7))
    dm = filtrar_mes(d, ini, fin, "x")
    tabla = dot.cargar(log=L)
    trib = dm[smact.mask_tributa_ada(dm["ACT_n"])]
    ev = dot.evidencia(trib, tabla, modulo="sm")
    n = dot.nuevos(ev, tabla, "sm")
    return f"trib={len(trib)} ev={len(ev)} nuevos={len(n)} cols={list(ev.columns)}"
run("dotacion empty trib", dot_empty)
