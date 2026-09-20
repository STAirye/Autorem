import sys
from datetime import date
sys.path.insert(0, r"E:\git\Autorem"); sys.path.insert(0, r"E:\git\Autorem\tests")
import _aislar_cache  # noqa
import openpyxl
import test_sm_actividades as TS
import modulos.rem_sm_actividades as smact
from programas.rem_utils import ArchivoInvalido
SIN = {"funcionarios": {}, "omitidos": {}}
logs = []
L = lambda *a, **k: logs.append(" ".join(map(str, a)))
ada = TS._mk_ada(TS._RELLENO_ADA)
def taller(**kw):
    r = {"run": "G", "fecha": date(2026, 7, 3), "act": "Educación grupal prevención suicidio", "asiste": "SI",
         "sexo": "Mujer", "edad": 30, "instr": "Psicólogo(a)", "prest": "X"}
    r.update(kw); return r
def go(rows, drop=None):
    g = TS._mk_grupal(rows)
    if drop:
        wb = openpyxl.load_workbook(g); ws = wb.active
        for i, c in enumerate(ws[1], 1):
            if c.value == drop:
                ws.delete_cols(i); break
        wb.save(g)
    logs.clear()
    try:
        E = smact.procesar(ada, grupal=g, mes=(2026, 7), log=L, dotacion_tabla=SIN)
        r = {x["Casilla"] + " " + x["Qué se registra"][:25]: x["Total mes"] for x in E.attrs["tablas"]["SM_Resumen"].to_dict("records") if "A27" in x["Casilla"] or "Grupal" in x["Qué se registra"]}
        return r, [l for l in logs if "Grupal" in l]
    except ArchivoInvalido as e:
        return f"ArchivoInvalido({e.categoria}) {str(e)[:150]}"
    except Exception as e:
        return f"CRASH {type(e).__name__}: {e}"
print("baseline         :", go([taller()]))
print("asiste blank     :", go([taller(asiste="")]))
print("asiste col absent:", go([taller()], drop="ASISTE (SI/NO)"))
print("asiste 'Sí'      :", go([taller(asiste="Sí")]))
print("asiste 'S'       :", go([taller(asiste="S")]))
