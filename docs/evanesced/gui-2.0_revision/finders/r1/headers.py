import sys, glob, os
sys.path.insert(0, r"E:\git\Autorem")
import openpyxl
for p in sorted(glob.glob(r"E:\git\Autorem\refs_tablas\*.xlsx")):
    if "CALCULADOR" in p or "poblacion_sm_powerbi" in p or "comparativo" in p:
        continue
    wb = openpyxl.load_workbook(p, data_only=True)
    ws = wb.active
    print("=====", os.path.basename(p))
    for r in ws.iter_rows(values_only=True):
        if any(v not in (None, "") for v in r):
            print([v for v in r])
    wb.close()
