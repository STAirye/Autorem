import sys, traceback
from pathlib import Path
from datetime import date
sys.path.insert(0, r"E:\git\Autorem")
sys.path.insert(0, r"E:\git\Autorem\tests")
import _aislar_cache  # noqa  FIRST
OUT = Path(r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\648a107e-f033-4d56-a55d-a415a58f003e\scratchpad\r1")
from programas.rem_utils import ArchivoInvalido, cargar_atenciones, rutas_libres, escribir_atomico
import programas.poblacion as pob
import modulos.rem_sp_p6_poblacion as p6
import modulos.rem_sm_rescate_inasistentes as resc
import test_rescate_inasistentes as TR
logs = []
def L(*a, **k): logs.append(" ".join(str(x) for x in a))

def run(name, fn):
    logs.clear()
    try:
        r = fn()
        print(f"\n=== {name}: SUCCESS -> {r}")
        for l in logs:
            if any(k in l for k in ("cobertura", "NO llega", "SUBCONT", "arranca", "Ferrada", "sin fechas", "rescate", "ADVERT", "sanity", "Formulario SM")):
                print("   log:", l[:260])
    except ArchivoInvalido as e:
        print(f"\n=== {name}: ArchivoInvalido({e.categoria}) {str(e)[:200]!r}")
    except Exception as e:
        print(f"\n=== {name}: CRASH {type(e).__name__}: {e}")
        traceback.print_exc(limit=-4, file=sys.stdout)

MES = (2026, 8)
def correr_pob(form_rows, insc_rows, ada_rows, mes=MES):
    """Mirror gui/paginas/poblacion.correr exactly."""
    fi = TR._mk_formulario(form_rows); ii = TR._mk_inscritos(insc_rows); ai = TR._mk_ada(ada_rows)
    y, m = mes
    insc = pob.cargar_inscritos(ii, log=L)
    form = pob.cargar_formulario_sm([fi], log=L)
    ada = cargar_atenciones([ai], log=L)
    P = pob.construir_poblacion(insc, form, ada, mes=(y, m), log=L)
    resultado = p6.construir_p6(P, log=L)
    salida, salida_r = rutas_libres(OUT / f"P6_{y}_{m:02d}.xlsx", OUT / f"R_{y}_{m:02d}.xlsx")
    escribir_atomico(salida, lambda p: p6.escribir(P, resultado, p))
    fallo = None; n_r = None
    try:
        Er = resc.procesar(insc, form, ada, mes=(y, m), log=L, P=P, fuentes=["a"])
        escribir_atomico(salida_r, lambda p: resc.escribir(Er, p))
        n_r = {h: len(t) for h, t in Er.attrs["tablas"].items()}
    except Exception as e:
        fallo = f"{type(e).__name__}: {e}"
    n_ing = int((P["¿Ingresado?"] == "SI").sum())
    n_act = int((P["¿Activo 12m?"] == "SI").sum())
    return (f"P={len(P)} ingresados={n_ing} activo12={n_act} revAdm={len(resultado['revisar_administrativo'])} "
            f"revClin={len(resultado['revisar_clinico'])} rescate={n_r} fallo_rescate={fallo} "
            f"avisos={P.attrs.get('avisos')}")

# baseline: persona ingresada con depresion, atendida en agosto
ING = {"rut": "11111111-1", "fecha": date(2026, 3, 1), "18.- ¿ TIENE  DEPRESIÓN ?": "SI", "19.- ESTADO": "Ingreso"}
INS = [{"rut": "11111111-1", "fnac": date(1990, 1, 1)}]
ADA = [TR._sm("11111111-1", date(2026, 8, 5)), TR._sm("11111111-1", date(2025, 7, 5))]
run("POB baseline", lambda: correr_pob([ING], INS, ADA))
# ADA rows but none in the 13-month window (older year)
run("POB ADA all in 2024", lambda: correr_pob([ING], INS, [TR._sm("11111111-1", date(2024, 3, 5))]))
# ADA rows only AFTER the corte (month chosen one year too early)
run("POB ADA+form all after corte (mes 2025-08)", lambda: correr_pob([ING], INS, ADA, mes=(2025, 3)))
# formularios with rows but none <= corte
run("POB formularios all after corte", lambda: correr_pob(
    [dict(ING, fecha=date(2026, 9, 10))], INS, ADA))
# formularios dates unparseable
run("POB formularios fechas ilegibles", lambda: correr_pob(
    [dict(ING, fecha="no es fecha")], INS, ADA))
# ADA fechas ilegibles -- _mk_ada strftime needs a date; build via 'fecha' object with strftime
class F:
    def strftime(self, _): return "xx/yy/zzzz"
run("POB ADA fechas ilegibles", lambda: correr_pob([ING], INS, [dict(TR._sm("11111111-1", date(2026,8,5)), fecha=F())]))
# inscritos all responsable
run("POB inscritos todos responsables/no-RUN", lambda: correr_pob([ING], [{"rut": "11111111-1", "tipoid": "Pasaporte"}], ADA))
# inscritos no overlap with form
run("POB inscritos sin cruce con form", lambda: correr_pob([ING], [{"rut": "22222222-2"}], ADA))
