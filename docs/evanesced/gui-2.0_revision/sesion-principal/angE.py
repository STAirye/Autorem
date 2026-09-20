import sys, tempfile
from pathlib import Path
sys.path.insert(0, r"E:\git\Autorem\tests"); sys.path.insert(0, r"E:\git\Autorem")
import _aislar_cache  # noqa
import programas.dotacion as dot
q = lambda *a, **k: None
dot.RUTA_CACHE = Path(tempfile.mkdtemp()) / "d.json"
seed = dot.cargar(log=q); dot.marcar(seed, {"Ana Soto": False, "Beto Ruiz": False}, log=q)
# Ventana A abre "Revisar dotacion" (carga la tabla, ticks = clase guardada)
from gui.dialogos import valores_iniciales
ta = dot.cargar(log=q); checks_a = valores_iniciales(ta["funcionarios"].keys(), ta)
# Ventana B marca a Ana externa (Precargar -> Aplicar)
tb = dot.cargar(log=q); dot.marcar(tb, {"Ana Soto": True}, log=q)
print("tras B:", dot.clase("ana soto", dot.cargar(log=q)))
# Ventana A cambia SOLO a Beto y aprieta Aplicar: el dialogo manda TODOS los checks
checks_a[dot.norm("Beto Ruiz")] = True
dot.marcar(ta, checks_a, log=q)
print("tras A:", dot.clase("ana soto", dot.cargar(log=q)), "(esperado externo)")

import programas.catalogos as cat, pandas as pd
cat.CATALOGOS["cie10"] = dict(cat.CATALOGOS["cie10"], leer=lambda x, log: pd.DataFrame({"COD": ["ZZZ"], "DESC": ["override"]}))
f = Path(tempfile.mkdtemp()) / "cie.xlsx"; f.write_bytes(b"x")
cat.cargar("cie10", entrada=str(f), recargar=True)   # lo que hace about._cargar_manual
d = cat.cargar("cie10")                              # lo que hace un consumidor
print("consumidor ve:", d.attrs["fuente"], "| ZZZ existe?", cat.existe("ZZZ"))
print("claves cache:", list(cat._CACHE))
