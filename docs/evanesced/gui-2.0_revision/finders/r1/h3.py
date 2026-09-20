import sys, traceback, shutil
from pathlib import Path
from datetime import date
sys.path.insert(0, r"E:\git\Autorem")
sys.path.insert(0, r"E:\git\Autorem\tests")
import _aislar_cache  # noqa  FIRST
import openpyxl
OUT = Path(r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\648a107e-f033-4d56-a55d-a415a58f003e\scratchpad\r1")
from programas.rem_utils import ArchivoInvalido, rutas_libres, escribir_atomico
import modulos.rem_a23_respiratorio as a23
import test_a23 as TA
logs = []
def L(*a, **k): logs.append(" ".join(str(x) for x in a))

def run(name, fn, keys=("[a23]", "fecha", "SUBCONT")):
    logs.clear()
    try:
        r = fn()
        print(f"\n=== {name}: SUCCESS -> {r}")
        for l in logs:
            if any(k in l for k in keys):
                print("   log:", l[:260])
    except ArchivoInvalido as e:
        print(f"\n=== {name}: ArchivoInvalido({e.categoria}) {str(e)[:220]!r}")
    except Exception as e:
        print(f"\n=== {name}: CRASH {type(e).__name__}: {e}")
        traceback.print_exc(limit=-4, file=sys.stdout)

ATEN = [{"NUMERO TIPO IDENTIFICACION": "A", "FECHA ATENCION": date(2026, 7, 10), "INSTRUMENTO": "Médico",
         "FECHA DE NACIMIENTO": date(1990, 1, 1), "DIAGNOSTICOS": "J45 Asma"}]
def correr_a23(otros_rows=None, estrat=None, nsp_rows=None, mes=(2026, 7)):
    aten = TA._mk(ATEN)
    a_copy = OUT / "aten.xlsx"; shutil.copy(aten, a_copy)
    otros = None
    if otros_rows is not None:
        o = TA._mk_otros(otros_rows); otros = [OUT / "otros.xlsx"]; shutil.copy(o, otros[0])
    nsp = None
    if nsp_rows is not None:
        n = TA._mk_nsp(nsp_rows); nsp = [OUT / "nsp.xlsx"]; shutil.copy(n, nsp[0])
    fer = a23.procesar([a_copy], otros=otros, estrat=estrat, inasistentes=nsp, mes=mes, log=L)
    salida, = rutas_libres(OUT / "A23_out.xlsx")
    escribir_atomico(salida, lambda p: a23.escribir(fer, p))
    g = fer.attrs.get("seccion_g", {})
    gtxt = " · ".join(f"{lbl.split()[0]}:{d['Total']}" for lbl, d in g.items() if d["Total"])
    sala = {c: int((fer[c] == "SI").sum()) for c in fer.columns if c.startswith("SALA ") and fer[c].isin(["SI", "NO"]).all()}
    return f"len={len(fer)} G='{gtxt or 'ninguno'}' SALA={sala} H={fer.attrs.get('seccion_h') is not None} avisos={[a[:2] for a in fer.attrs.get('avisos', [])]}"

OT_OK = {"RUN": "A", "FECHA": date(2025, 5, 1), "INSTR": "Médico", "ASMA_p": "Si", "ASMA_grav": "Leve",
         "ASMA_ctrl": "Controlado", "ASMA_est": "Ingreso", "ASMA_prox": date(2025, 6, 1)}
run("A23 baseline otros", lambda: correr_a23([OT_OK]))
run("A23 otros fechas ilegibles", lambda: correr_a23([dict(OT_OK, FECHA="xx")]))
run("A23 otros all AFTER corte", lambda: correr_a23([dict(OT_OK, FECHA=date(2026, 9, 1))]))
run("A23 otros sin ninguna condicion (padece vacio)", lambda: correr_a23([{"RUN": "A", "FECHA": date(2025, 5, 1), "INSTR": "Médico"}]))
run("A23 nsp rows none in month", lambda: correr_a23([OT_OK], nsp_rows=[
    {"instr": "Médico", "tipo": "Control IRA", "fecha": "10-06-2026 09:00:00", "run": "E", "anos": 40}]))
run("A23 nsp rows in month, none IRA/ERA", lambda: correr_a23([OT_OK], nsp_rows=[
    {"instr": "Médico", "tipo": "Consulta SAC", "fecha": "10-07-2026 09:00:00", "run": "E", "anos": 40}]))
run("A23 nsp fechas ilegibles", lambda: correr_a23([OT_OK], nsp_rows=[
    {"instr": "Médico", "tipo": "Control IRA", "fecha": "zz", "run": "E", "anos": 40}]))
run("A23 estrat rows no RUT match", lambda: correr_a23([OT_OK], estrat=TA._mk_estrat(["RUT", "DV", "DETALLE DIAGNOSTICOS"], [[22222222, "2", "Asma Leve"]])))
run("A23 estrat DV vacio/RUT texto", lambda: correr_a23([OT_OK], estrat=TA._mk_estrat(["RUT", "DV", "DETALLE DIAGNOSTICOS"], [["", "", "Asma Leve"]])))

# ---- A05 detection on read-only + _correr_tareas
import modulos  # noqa
import programas.rem_saludmental as sm
from programas.rem_utils import abrir_xlsx_ro
for ref in ("Formularios_RAYEN_csm_IRis.xlsx", "Formulario_csm_reporte_Administrativo.xlsx"):
    p = Path(r"E:\git\Autorem\refs_tablas") / ref
    def det(p=p):
        wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
        try:
            return sm.detectar_formato(wb.active)
        finally:
            wb.close()
    run(f"A05 detectar_formato read_only {ref}", det, keys=())
    def det2(p=p):
        wb = abrir_xlsx_ro(p)
        try:
            return sm.detectar_formato(wb.active)
        finally:
            wb.close()
    run(f"A05 detectar_formato abrir_xlsx_ro {ref}", det2, keys=())
