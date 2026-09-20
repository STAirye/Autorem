import sys, os
sys.path.insert(0, r"E:\git\Autorem")
import pandas as pd
from programas.rem_utils import leer_xlsx
S = sys.argv[1]
for name in ("iris_ok.xlsx", "iris_dimA1.xlsx", "iris_nodim.xlsx"):
    p = os.path.join(S, name)
    h, f = leer_xlsx(p)
    try:
        n = len(pd.read_excel(p, header=None))
    except Exception as e:
        n = f"EXC {e}"
    print(f"{name:18s} leer_xlsx header cells={len(h)} data rows={len(f)} | pandas.read_excel rows={n}")
