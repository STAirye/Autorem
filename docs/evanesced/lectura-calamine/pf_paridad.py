"""primeras_filas (openpyxl read_only) en el arbol ACTUAL (cwd): tiempo sobre exports
reales y paridad por repr con las primeras n de filas_xlsx (calamine). Sin valores."""
import sys, os, time, statistics
from pathlib import Path
sys.path.insert(0, os.getcwd())
from programas.rem_utils import primeras_filas, filas_xlsx

DM = Path(os.path.expanduser("~")) / "OneDrive - Ilustre Municipalidad de Maipú" / "Datos madre"
for n, p in (("ADA", DM / "Variables 12m" / "Atenciones" / "2026.xlsx"),
             ("Inscritos", DM / "Población" / "Informe_Inscritos__Adscritos_.xlsx"),
             ("PSM", DM / "Variables 12m" / "PSM" / "2026.xlsx")):
    v = []
    for _ in range(3):
        t = time.perf_counter(); f = primeras_filas(p, 30); v.append(time.perf_counter() - t)
    igual = [tuple(map(repr, r)) for r in f] == [tuple(map(repr, r)) for r in filas_xlsx(p)[:30]]
    print(f"  {n:<10} primeras_filas(30): mediana {statistics.median(v):.2f}s  "
          f"identico a filas_xlsx[:30] por repr: {igual}")
