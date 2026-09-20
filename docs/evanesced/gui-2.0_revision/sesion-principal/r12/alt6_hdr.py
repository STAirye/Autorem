import sys
from pathlib import Path
REPO = Path(r"E:\git\Autorem")
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "tests"))
import _aislar_cache  # noqa
from programas.rem_utils import primeras_filas, indice_encabezado
from tools import limpiar_refs
refs = sorted(p for p in (REPO / "refs_tablas").glob("*.xlsx")
              if not p.name.startswith(("CALCULADOR", "PSC_PSC", "poblacion_sm", "Maestro")))
print(f"{'ref':<46} runtime(>3)  limpiar_refs(>=5)  llenas_por_fila_banner")
for p in refs:
    filas = primeras_filas(p, 40)
    rt = indice_encabezado(filas)
    lr = limpiar_refs._fila_header(filas) - 1
    llenas = [sum(v not in (None, "") for v in r) for r in filas[:max(rt, lr) + 1]]
    flag = "" if rt == lr else "   <-- DISTINTOS"
    print(f"{p.name:<46} {rt:>6}      {lr:>6}           {llenas}{flag}")
