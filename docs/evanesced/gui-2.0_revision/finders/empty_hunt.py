"""Caza del bug de c38a8cc: inputs con 0 filas de datos por los caminos de GUI 2.0."""
import os, sys, tempfile, traceback
from datetime import date
from pathlib import Path
SCR = Path(__file__).resolve().parent / "empty"; SCR.mkdir(exist_ok=True)
os.environ["USERPROFILE"] = str(SCR); os.environ["HOME"] = str(SCR)
sys.path.insert(0, r"E:\git\Autorem"); sys.path.insert(0, r"E:\git\Autorem\tests")
tempfile.tempdir = str(SCR)
import openpyxl
import test_sm_actividades as T
import test_rescate_inasistentes as R
from programas.rem_utils import ArchivoInvalido
import modulos.rem_sm_actividades as smact
import modulos.rem_sm_trabajo_perdido as tp
import programas.poblacion as pob
import modulos.rem_sp_p6_poblacion as p6
import modulos.rem_sm_rescate_inasistentes as resc
q = lambda *a, **k: None

def solo_header(hdr, nombre, banner=0):
    p = SCR / nombre; wb = openpyxl.Workbook(); ws = wb.active
    for r in range(1, banner + 1): ws.cell(row=r, column=1, value=f"banner {r}")
    ws.append(hdr); wb.save(p); return p

def caso(nombre, fn):
    try:
        r = fn(); print(f"SILENT/OK  {nombre}: {type(r).__name__} len={len(r) if hasattr(r,'__len__') else '-'}")
    except ArchivoInvalido as e:
        print(f"LOUD-OK    {nombre}: ArchivoInvalido[{e.categoria}]")
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)[-1]
        print(f"CRYPTIC    {nombre}: {type(e).__name__}: {e} @ {Path(tb.filename).name}:{tb.lineno}")

M = (2026, 7); SD = {"funcionarios": {}, "omitidos": {}}
ada_ok = T._mk_ada([{"run": "11111111-1", "id": "1", "fecha": date(2026, 7, 3), "act": "Consulta De Salud Mental  ;", "instr": "Médico", "sexo": "Mujer", "edad": 30}])
grp0 = solo_header(T._GRP_HDR, "grp0.xlsx")
ins0 = solo_header(T._INS_HDR, "ins0.xlsx")
mul0 = solo_header(["ATEN ID", "Multiprofesional-1"], "mul0.xlsx")
mae0 = solo_header(["ACTIVIDAD", "INSTRUMENTO ASOCIADO", "NUM REM", "NUM SECCION", "REM"], "mae0.xlsx")
caso("SM grupal 0 filas", lambda: smact.procesar(str(ada_ok), grupal=[str(grp0)], mes=M, log=q, dotacion_tabla=SD))
grp_fuera = T._mk_grupal([{"run": "1", "fecha": date(2025, 1, 3), "act": "Intervencion Psicosocial Grupal", "asiste": "SI", "sexo": "Mujer", "edad": 30, "instr": "Psicologo", "prest": "X"}])
caso("SM grupal fuera de mes", lambda: smact.procesar(str(ada_ok), grupal=[str(grp_fuera)], mes=M, log=q, dotacion_tabla=SD))
caso("SM inscritos(TRANS) 0 filas", lambda: smact.procesar(str(ada_ok), grupal=[str(grp_fuera)] and None, inscritos=str(ins0), mes=M, log=q, dotacion_tabla=SD))
caso("SM multiprofesional 0 filas", lambda: smact.procesar(str(ada_ok), multiprofesional=str(mul0), mes=M, log=q, dotacion_tabla=SD))
caso("TP maestro 0 filas", lambda: tp.procesar(str(ada_ok), maestro=str(mae0), mes=M, log=q))
ada_notrib = T._mk_ada([{"run": "11111111-1", "id": "1", "fecha": date(2026, 7, 3), "act": "Curacion simple", "instr": "Enfermero(a)", "sexo": "Mujer", "edad": 30}])
caso("SM ADA sin filas que tributen", lambda: smact.procesar(str(ada_notrib), mes=M, log=q, dotacion_tabla=SD))

# Poblacion
ins_ok = R._mk_inscritos([{"rut": "11111111-1"}])
form0 = solo_header(R._FORM_HDR, "form0.xlsx", banner=16)
ada0 = solo_header(R._ADA_HDR, "ada0.xlsx")
ada_okp = R._mk_ada([R._sm("11111111-1", date(2026, 8, 3))])
form_ok = R._mk_formulario([{"rut": "11111111-1", "fecha": date(2026, 1, 1)}])
def pobl(ins, form, ada):
    P = pob.construir_poblacion(str(ins), str(form), str(ada), mes=(2026, 8), log=q)
    res = p6.construir_p6(P, log=q); p6.escribir(P, res, SCR / "p6.xlsx")
    E = resc.procesar(None, None, None, mes=(2026, 8), log=q, P=P); resc.escribir(E, SCR / "r.xlsx")
    return P
caso("POB formulario 0 filas", lambda: pobl(ins_ok, form0, ada_okp))
caso("POB ADA 0 filas", lambda: pobl(ins_ok, form_ok, ada0))
caso("POB formulario todo posterior al corte", lambda: pobl(ins_ok, R._mk_formulario([{"rut": "11111111-1", "fecha": date(2026, 12, 1)}]), ada_okp))
caso("POB inscritos solo responsables/otros RUN", lambda: pobl(R._mk_inscritos([{"rut": "22222222-2", "tipoid": "PASAPORTE"}]), form_ok, ada_okp))
