import sys
from pathlib import Path
from datetime import date
sys.path.insert(0, r"E:\git\Autorem"); sys.path.insert(0, r"E:\git\Autorem\tests")
import _aislar_cache  # noqa
import openpyxl, pandas as pd
import modulos.rem_a23_respiratorio as a23
import test_a23 as TA
OUT = Path(r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\648a107e-f033-4d56-a55d-a415a58f003e\scratchpad\r1")
logs = []
L = lambda *a, **k: logs.append(" ".join(map(str, a)))
ATEN = [{"NUMERO TIPO IDENTIFICACION": "A", "FECHA ATENCION": date(2026, 7, 10), "INSTRUMENTO": "Médico",
         "FECHA DE NACIMIENTO": date(1990, 1, 1)}]
OT = {"RUN": "A", "FECHA": date(2025, 5, 1), "INSTR": "Médico", "SEXO": "Mujer", "ASMA_p": "Si", "ASMA_grav": "Leve",
      "ASMA_ctrl": "Controlado", "ASMA_est": "Seguimiento", "ASMA_prox": date(2025, 6, 1)}
def g(rows, hdr_drop=None):
    o = TA._mk_otros(rows)
    if hdr_drop:
        wb = openpyxl.load_workbook(o); ws = wb.active
        for i, c in enumerate(ws[1], 1):
            if c.value == hdr_drop:
                ws.delete_cols(i); break
        wb.save(o)
    fer = a23.procesar(TA._mk(ATEN), otros=o, mes=(2026, 7), log=L)
    return {k: v["Total"] for k, v in fer.attrs["seccion_g"].items()}, [a[:2] for a in fer.attrs["avisos"]]
print("with FNAC       :", g([dict(OT, FNAC=date(1980, 1, 1))]))
print("FNAC blank      :", g([OT]))
print("FNAC col absent :", g([OT], hdr_drop="FECHA DE NACIMIENTO"))
print("FNAC text 'xx'  :", g([dict(OT, FNAC="31-02-1980")]))
