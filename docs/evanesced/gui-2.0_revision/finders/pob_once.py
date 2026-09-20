import sys, types
sys.path.insert(0, r"E:\git\Autorem"); sys.path.insert(0, r"E:\git\Autorem\tests")
from datetime import date
from pathlib import Path
import tempfile
import test_rescate_inasistentes as R
import gui.paginas.poblacion as pag
out = Path(tempfile.mkdtemp())
ctx = {"mes": (2026, 8), "carpeta": out,
       "inscritos": R._mk_inscritos([{"rut": "11111111-1"}]),
       "formularios": [R._mk_formulario([{"rut": "11111111-1", "fecha": date(2026, 1, 1)}])],
       "ada": [R._mk_ada([R._sm("11111111-1", date(2026, 3, 3))])]}
logs = []
res = pag.correr(ctx, logs.append)
print("n_rescate:", res["n_rescate"])
print("lecturas Inscritos:", sum("Inscritos:" in str(l) for l in logs))
import openpyxl
ws = openpyxl.load_workbook(out / "REM_SM_Rescate_2026_08_BETA.xlsx").worksheets[0]
print("LEEME nombra:", [c for r in ws.iter_rows(values_only=True) for c in r if c and ("inscritos.xlsx" in str(c) or "ada.xlsx" in str(c))][:3])
print(pag.resumen(res).splitlines()[0])
