import sys, time
from pathlib import Path
REPO = Path(r"E:\git\Autorem")
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "tests"))
import _aislar_cache  # noqa
from programas.rem_utils import cargar_maestro
p = REPO / "refs_tablas" / "Maestro_de_Actividades.xlsx"
print("Maestro .xlsx:", round(p.stat().st_size / 1e6, 1), "MB")
for i in range(2):
    t = time.perf_counter(); d = cargar_maestro(p); print(f"  cargar_maestro #{i+1}: {time.perf_counter()-t:.1f} s ({len(d)} filas)")
