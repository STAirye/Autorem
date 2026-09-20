import sys, traceback
from pathlib import Path
from datetime import date
sys.path.insert(0, r"E:\git\Autorem"); sys.path.insert(0, r"E:\git\Autorem\tests")
import _aislar_cache  # noqa
import pandas as pd
from programas.rem_utils import ArchivoInvalido
OUT = Path(r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\648a107e-f033-4d56-a55d-a415a58f003e\scratchpad\r1")
logs = []
def L(*a, **k): logs.append(" ".join(str(x) for x in a))
def run(name, fn, keys=()):
    logs.clear()
    try:
        r = fn()
        print(f"\n=== {name}: SUCCESS -> {r}")
        for l in logs:
            if any(k in l for k in keys):
                print("   log:", l[:240])
    except ArchivoInvalido as e:
        print(f"\n=== {name}: ArchivoInvalido({e.categoria}) {str(e)[:200]!r}")
    except Exception as e:
        print(f"\n=== {name}: CRASH {type(e).__name__}: {e}")
        traceback.print_exc(limit=-3, file=sys.stdout)

# ---------- A03 ----------
import test_screening as TSC
import modulos.rem_a03_d3_instrumentos as scr
def a03(filas, formulario="Cuestionario para Padres PSC", inst="PSC"):
    p = TSC._iris(f"h6_{abs(hash(str(filas)))}.xlsx", formulario, filas)
    res = scr.procesar_unificado({inst: p}, OUT / "a03.xlsx", log=L)
    t = res["tabla"]
    return f"total={res['total']} D3_Ambos={int(t['Ambos'].sum())} D3_H={int(t['Hombres'].sum()) if 'Hombres' in t else '?'} D3_M={int(t['Mujeres'].sum()) if 'Mujeres' in t else '?'} cols={list(t.columns)[:6]}"
base = [("1-1", 7, "Hombre", "", "", "Ingreso", 72, "Alto"), ("2-2", 8, "Mujer", "", "", "Ingreso", 40, "Bajo")]
run("A03 baseline", lambda: a03(base))
run("A03 momento blank", lambda: a03([r[:5] + ("",) + r[6:] for r in base]))
run("A03 momento 'Seguimiento'", lambda: a03([r[:5] + ("Seguimiento",) + r[6:] for r in base]))
run("A03 sexo blank", lambda: a03([r[:2] + ("",) + r[3:] for r in base]))
run("A03 edad blank", lambda: a03([r[:1] + (None,) + r[2:] for r in base]))
run("A03 puntaje blank, resultado RAYEN only", lambda: a03([r[:6] + (None,) + r[7:] for r in base]))

# ---------- A23: ADA in month, nothing respiratory ----------
import test_a23 as TA
import modulos.rem_a23_respiratorio as a23
def a23_nada():
    fer = a23.procesar(TA._mk([{"NUMERO TIPO IDENTIFICACION": "A", "FECHA ATENCION": date(2026, 7, 10),
                                "INSTRUMENTO": "Enfermero(a)", "ACTIVIDADES": "Curacion simple"}]),
                       mes=(2026, 7), log=L)
    ind = [c for c in fer.columns if c.startswith("REMA23")]
    return f"len={len(fer)} indicadores_SI={int((fer[ind] == 'SI').sum().sum())} avisos={[a[:2] for a in fer.attrs['avisos']]}"
run("A23 ADA mes sin nada respiratorio", a23_nada)
def a23_otros_nomed():
    o = TA._mk_otros([{"RUN": "A", "FECHA": date(2025, 5, 1), "INSTR": "Enfermero(a)", "ASMA_p": "Si",
                       "ASMA_est": "Ingreso", "ASMA_grav": "Leve"}])
    fer = a23.procesar(TA._mk([{"NUMERO TIPO IDENTIFICACION": "A", "FECHA ATENCION": date(2026, 7, 10),
                                "INSTRUMENTO": "Médico", "FECHA DE NACIMIENTO": date(1990, 1, 1)}]),
                       otros=o, mes=(2026, 7), log=L)
    return f"SALA Ingresado={int((fer['SALA Ingresado']=='SI').sum())} ASMA={int((fer['SALA ASMA']=='SI').sum())} avisos={[a[:2] for a in fer.attrs['avisos']]}"
run("A23 otros sin ningun formulario medico", a23_otros_nomed, keys=("SALA",))

# ---------- Poblacion: ADA in window, no SM activity ----------
import test_rescate_inasistentes as TR
import programas.poblacion as pob
def pob_nosm():
    ING = {"rut": "11111111-1", "fecha": date(2026, 3, 1), "18.- ¿ TIENE  DEPRESIÓN ?": "SI", "19.- ESTADO": "Ingreso"}
    P = pob.construir_poblacion(TR._mk_inscritos([{"rut": "11111111-1"}]), TR._mk_formulario([ING]),
                                TR._mk_ada([{"rut": "11111111-1", "fecha": date(2026, 8, 5), "act": "Curacion"},
                                            {"rut": "11111111-1", "fecha": date(2025, 7, 5), "act": "Curacion"}]),
                                mes=(2026, 8), log=L)
    return f"activo12={int((P['¿Activo 12m?']=='SI').sum())} ingresados={int((P['¿Ingresado?']=='SI').sum())} avisos={P.attrs['avisos']}"
run("POB ADA 13m sin ninguna actividad SM", pob_nosm)
def p6_base0():
    import modulos.rem_sp_p6_poblacion as p6
    P = pob.construir_poblacion(TR._mk_inscritos([{"rut": "11111111-1"}]),
                                TR._mk_formulario([{"rut": "11111111-1", "fecha": date(2026, 3, 1)}]),
                                TR._mk_ada([TR._sm("11111111-1", date(2026, 8, 5)), TR._sm("11111111-1", date(2025, 7, 5))]),
                                mes=(2026, 8), log=L)
    r = p6.construir_p6(P, log=L)
    return f"ingresados={int((P['¿Ingresado?']=='SI').sum())} keys={list(r)[:6]}"
run("P6 con 0 ingresados (formulario sin dx)", p6_base0)

# ---------- TP: maestro that covers none of the month's activities ----------
import test_sm_actividades as TS
import test_trabajo_perdido as TT
import modulos.rem_sm_trabajo_perdido as tpmod
def tp_maestro_nada():
    m = TT._mk_maestro([("OTRA COSA DISTINTA", "")])
    E = tpmod.procesar(TS._mk_ada([{"run": "A", "id": "1", "fecha": date(2026, 7, 3),
                                    "act": "Taller de salud mental comunitaria", "instr": "Psicólogo(a)", "edad": 30}]),
                       maestro=m, mes=(2026, 7), log=L)
    return f"len={len(E)} avisos={[a[:2] for a in E.attrs.get('avisos', [])]}"
run("TP maestro sin cobertura del mes", tp_maestro_nada, keys=("[tp]",))

# ---------- grid: sexo desconocido ----------
import modulos.rem_sm_actividades as smact
def sm_sexo_raro():
    E = smact.procesar(TS._mk_ada([{"run": "A", "id": "1", "fecha": date(2026, 7, 3), "act": "Consulta De Salud Mental  ;",
                                    "instr": "Médico", "sexo": "Intersexual", "edad": 30},
                                   {"run": "B", "id": "2", "fecha": date(2026, 7, 3), "act": "Consulta De Salud Mental  ;",
                                    "instr": "Médico", "sexo": "", "edad": 30}]),
                       mes=(2026, 7), log=L, dotacion_tabla={"funcionarios": {}, "omitidos": {}})
    t = E.attrs["tablas"]["A04_Consultas_Medicas"]
    resu = E.attrs["tablas"]["SM_Resumen"]
    return f"E={len(E)} A04 Ambos={t['Ambos'].iloc[0]} H={t['Hombres'].iloc[0]} M={t['Mujeres'].iloc[0]} resumenA04={resu.iloc[0]['Total mes']} avisos={[a[:2] for a in E.attrs['avisos']]}"
run("SM sexo Intersexual/blank", sm_sexo_raro)
def sm_edad_raro():
    E = smact.procesar(TS._mk_ada([{"run": "A", "id": "1", "fecha": date(2026, 7, 3), "act": "Consulta De Salud Mental  ;",
                                    "instr": "Médico", "sexo": "Mujer", "edad": ""}]),
                       mes=(2026, 7), log=L, dotacion_tabla={"funcionarios": {}, "omitidos": {}})
    t = E.attrs["tablas"]["A04_Consultas_Medicas"]
    resu = E.attrs["tablas"]["SM_Resumen"]
    bandas = [c for c in t.columns if c not in ("Consulta", "Ambos", "Hombres", "Mujeres") and not str(c).startswith("dem")]
    return f"Ambos={t['Ambos'].iloc[0]} M={t['Mujeres'].iloc[0]} suma_bandas={pd.to_numeric(t[bandas].iloc[0], errors='coerce').sum()} resumenA04={resu.iloc[0]['Total mes']} avisos={[a[:2] for a in E.attrs['avisos']]}"
run("SM edad blank", sm_edad_raro)

# ---------- dotacion: trib > 0 but no funcionario ----------
import programas.dotacion as dot
from programas.rem_utils import cargar_atenciones, filtrar_mes, _rango_mes
def dot_sin_func():
    d = cargar_atenciones(TS._mk_ada([{"run": "A", "id": "1", "fecha": date(2026, 7, 3), "act": "Consulta De Salud Mental  ;",
                                       "instr": "Médico", "sexo": "Mujer", "edad": 30}]), log=L)
    ini, fin = _rango_mes((2026, 7)); dm = filtrar_mes(d, ini, fin, "x")
    tabla = dot.cargar(log=L)
    trib = dm[smact.mask_tributa_ada(dm["ACT_n"])]
    ev = dot.evidencia(trib, tabla, modulo="sm")
    return f"trib={len(trib)} ev={len(ev)} PROF_col={'PROF' in dm.columns} PROF_vals={list(dm.get('PROF', pd.Series()).head())}"
run("dotacion trib>0 sin funcionario", dot_sin_func)
