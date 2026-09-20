"""Caza del bug de c38a8cc: inputs con 0 filas de datos por los caminos de GUI 2.0."""
import os, sys, tempfile, traceback
from datetime import date
from pathlib import Path
SCR = Path(r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\648a107e-f033-4d56-a55d-a415a58f003e\scratchpad") / "empty"; SCR.mkdir(exist_ok=True)
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


import traceback
ins_ok = R._mk_inscritos([{"rut": "11111111-1"}])
for n, f, a in [("form0", solo_header(R._FORM_HDR, "f0.xlsx", 16), R._mk_ada([R._sm("11111111-1", date(2026, 8, 3))])),
                ("ada0", R._mk_formulario([{"rut": "11111111-1", "fecha": date(2026, 1, 1)}]), solo_header(R._ADA_HDR, "a0.xlsx"))]:
    try:
        pob.construir_poblacion(str(ins_ok), str(f), str(a), mes=(2026, 8), log=q)
    except Exception as e:
        print(n, [f"{Path(x.filename).name}:{x.lineno} {x.line}" for x in traceback.extract_tb(e.__traceback__) if "Autorem" in x.filename])
