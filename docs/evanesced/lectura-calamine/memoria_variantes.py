"""Variantes de `_hojas_calamine` (rama lectura-calamine) para bajar el pico de memoria.
Cada (variante, archivo) en un proceso nuevo: pico, retenido, tiempo, y un hash de repr de
TODAS las celdas para verificar que la salida es identica a la de hoy. Sin valores."""
import subprocess, sys, json

RAMA = r"C:\Users\simon.tobar\Dr tobar\AutoREM\.claude\worktrees\lectura-calamine"
HIJO = r'''
import sys, os, time, json, hashlib, ctypes, ctypes.wintypes as wt
from itertools import islice
sys.path.insert(0, os.getcwd())
import tests._aislar_cache
from pathlib import Path
class PMC(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD), ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t), ("a", ctypes.c_size_t), ("b", ctypes.c_size_t),
                ("c", ctypes.c_size_t), ("d", ctypes.c_size_t), ("e", ctypes.c_size_t), ("f", ctypes.c_size_t)]
k32, psapi = ctypes.windll.kernel32, ctypes.windll.psapi
k32.GetCurrentProcess.restype = wt.HANDLE
psapi.GetProcessMemoryInfo.argtypes = [wt.HANDLE, ctypes.POINTER(PMC), wt.DWORD]
def mem():
    c = PMC(); c.cb = ctypes.sizeof(c)
    assert psapi.GetProcessMemoryInfo(k32.GetCurrentProcess(), ctypes.byref(c), c.cb)
    return c.PeakWorkingSetSize / 2**20, c.WorkingSetSize / 2**20
import pandas, openpyxl
from programas import rem_utils as ru
from python_calamine import CalamineWorkbook

def filas_iter(sh, max_filas, conv):
    if sh.start is None:   # hoja vacia: iter_rows hace panic en Rust
        return []
    izq = ("",) * sh.start[1]
    crudas = [izq + tuple(conv(v) for v in f) for f in islice(sh.iter_rows(), max_filas)]
    ancho = max((len(f) for f in crudas), default=0)
    return [f + ("",) * (ancho - len(f)) if len(f) < ancho else f for f in crudas]

def hojas_generica(entrada, max_filas=None, internar=False):
    import zipfile
    if not zipfile.is_zipfile(entrada):
        raise zipfile.BadZipFile("no zip")
    cache = {}
    def conv(v):
        v = ru._celda_openpyxl(v)
        return cache.setdefault(v, v) if internar and type(v) is str else v
    wb = CalamineWorkbook.from_path(str(entrada))
    try:
        return [(n, filas_iter(wb.get_sheet_by_name(n), max_filas, conv)) for n in wb.sheet_names]
    finally:
        wb.close()

var, archivo = sys.argv[1], sys.argv[2]
if var == "iter_rows":
    ru._hojas_calamine = lambda e, m=None: hojas_generica(e, m, internar=False)
elif var == "iter_rows+intern":
    ru._hojas_calamine = lambda e, m=None: hojas_generica(e, m, internar=True)
DM = Path(os.path.expanduser("~")) / "OneDrive - Ilustre Municipalidad de Maip\u00fa" / "Datos madre"
P = {"ADA": DM / "Variables 12m" / "Atenciones" / "2026.xlsx",
     "Inscritos": DM / "Poblaci\u00f3n" / "Informe_Inscritos__Adscritos_.xlsx",
     "PSM": DM / "Variables 12m" / "PSM" / "2026.xlsx"}[archivo]
t = time.perf_counter()
x = ru.filas_xlsx(P)
dt = time.perf_counter() - t
pico, ret = mem()
h = hashlib.sha256()
for f in x:
    h.update(repr(f).encode("utf-8", "surrogatepass"))
print(json.dumps({"pico": pico, "ret": ret, "s": dt, "hash": h.hexdigest()[:12], "filas": len(x)}))
'''

print(f"{'archivo':<10} {'variante':<18} {'pico':>7} {'retenido':>9} {'tiempo':>7}  identico")
for archivo in ("ADA", "Inscritos", "PSM"):
    ref = None
    for var in ("hoy", "iter_rows", "iter_rows+intern"):
        r = subprocess.run([sys.executable, "-c", HIJO, var, archivo], cwd=RAMA,
                           capture_output=True, text=True)
        linea = next((l for l in r.stdout.splitlines() if l.startswith("{")), None)
        if not linea:
            print(f"{archivo:<10} {var:<18} FALLO: {(r.stderr.strip().splitlines() or ['?'])[-1]}")
            continue
        d = json.loads(linea)
        ref = ref or d["hash"]
        print(f"{archivo:<10} {var:<18} {d['pico']:6.0f}M {d['ret']:8.0f}M {d['s']:6.1f}s  "
              f"{'SI' if d['hash'] == ref else 'NO (' + d['hash'] + ')'}", flush=True)
