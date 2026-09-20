import sys, os, traceback, tempfile
sys.path.insert(0, r"E:\git\Autorem")
sys.path.insert(0, r"E:\git\Autorem\tests")
from datetime import date
import pandas as pd
print("pandas", pd.__version__)
import test_rescate_inasistentes as T   # reuse fixtures (writes to its own temp dir)
import programas.poblacion as pob
import modulos.rem_sp_p6_poblacion as p6
import modulos.rem_sm_rescate_inasistentes as resc
REFS = r"E:\git\Autorem\refs_tablas"
FORM_EMPTY = os.path.join(REFS, "Formularios_RAYEN_csm_IRis.xlsx")
ADA_EMPTY = os.path.join(REFS, "ATENCIONESDIAGNOSTICOSACTIVIDADES_iris.xlsx")
logs = []
def log(m=""): logs.append(str(m))
ins = str(T._mk_inscritos([{"rut": "11111111-1"}]))
# copy fixtures to unique names since the helpers overwrite the same path
import shutil
tmp = tempfile.mkdtemp()
ins2 = os.path.join(tmp, "ins.xlsx"); shutil.copy(ins, ins2)
form_ok = os.path.join(tmp, "form.xlsx"); shutil.copy(str(T._mk_formulario([{"rut": "11111111-1", "fecha": date(2026, 1, 5), **{T._Q[18]: "SI", T._Q[19]: "19.- INGRESO"}}])), form_ok)
ada_ok = os.path.join(tmp, "ada.xlsx"); shutil.copy(str(T._mk_ada([T._sm("11111111-1", date(2026, 8, 10))])), ada_ok)

def run(name, form, ada):
    logs.clear()
    print("=== ", name)
    try:
        P = pob.construir_poblacion(ins2, [form], [ada], mes=(2026, 8), log=log)
        print("  P rows", len(P), "Ingresado SI:", int((P["¿Ingresado?"] == "SI").sum()), "Activo12m SI:", int((P["¿Activo 12m?"] == "SI").sum()))
        print("  avisos attrs:", P.attrs.get("avisos"))
        r = p6.construir_p6(P, log=log)
        print("  p6 keys", list(r.keys()))
        g = r["grid"]
        num = g.select_dtypes("number")
        print("  p6 grid numeric sum:", int(num.to_numpy().sum()))
        try:
            Er = resc.procesar(ins2, [form], [ada], mes=(2026, 8), log=log, P=P)
            print("  rescate tablas:", {h: len(t) for h, t in Er.attrs["tablas"].items()})
        except Exception as e:
            print("  rescate EXC", type(e).__name__, str(e)[:200])
    except Exception as e:
        print("  EXC", type(e).__name__, str(e)[:300])
        tb = traceback.format_exc().strip().splitlines()
        print("
".join("    " + x for x in tb if "Autorem" in x or "Error" in x))
    for l in logs:
        if "cobertura" in l or "SUBCONT" in l or "NO llega" in l or "arranca" in l:
            print("  LOG:", l[:160])

run("form OK + ada OK", form_ok, ada_ok)
run("form EMPTY(header-only) + ada OK", FORM_EMPTY, ada_ok)
run("form OK + ada EMPTY(header-only)", form_ok, ADA_EMPTY)
