"""Pico de memoria (PeakWorkingSetSize de Windows) de leer los exports reales, main
(openpyxl) contra la rama lectura-calamine. Cada escenario en un PROCESO NUEVO, para que
el pico sea solo suyo. Sin valores: solo MB y segundos."""
import ctypes, ctypes.wintypes as wt, os, subprocess, sys, json

ARBOLES = {"main (openpyxl)": r"C:\Users\simon.tobar\Dr tobar\AutoREM",
           "rama (calamine)": r"C:\Users\simon.tobar\Dr tobar\AutoREM\.claude\worktrees\lectura-calamine"}

HIJO = r'''
import sys, os, time, json, ctypes, ctypes.wintypes as wt
sys.path.insert(0, os.getcwd())
import tests._aislar_cache
from pathlib import Path
class PMC(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD), ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t), ("a", ctypes.c_size_t), ("b", ctypes.c_size_t),
                ("c", ctypes.c_size_t), ("d", ctypes.c_size_t), ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t)]
k32, psapi = ctypes.windll.kernel32, ctypes.windll.psapi
k32.GetCurrentProcess.restype = wt.HANDLE
psapi.GetProcessMemoryInfo.argtypes = [wt.HANDLE, ctypes.POINTER(PMC), wt.DWORD]
psapi.GetProcessMemoryInfo.restype = wt.BOOL
def mem():
    c = PMC(); c.cb = ctypes.sizeof(c)
    if not psapi.GetProcessMemoryInfo(k32.GetCurrentProcess(), ctypes.byref(c), c.cb):
        raise OSError(ctypes.get_last_error() or "GetProcessMemoryInfo fallo")
    return c.PeakWorkingSetSize / 2**20, c.WorkingSetSize / 2**20
DM = Path(os.path.expanduser("~")) / "OneDrive - Ilustre Municipalidad de Maip\u00fa" / "Datos madre"
ADA = DM / "Variables 12m" / "Atenciones" / "2026.xlsx"
INSC = DM / "Poblaci\u00f3n" / "Informe_Inscritos__Adscritos_.xlsx"
import pandas, openpyxl
from programas import rem_utils as ru
base = mem()[1]
t = time.perf_counter()
esc = sys.argv[1]
if esc == "filas_xlsx ADA":
    x = ru.filas_xlsx(ADA)
elif esc == "filas_xlsx Inscritos":
    x = ru.filas_xlsx(INSC)
elif esc == "cargar_atenciones ADA":
    x = ru.cargar_atenciones(ADA, log=lambda *a, **k: None)
elif esc == "SM agosto (ADA+Inscritos)":
    import modulos.rem_sm_actividades as sm
    x = sm.procesar_rango(ADA, inscritos=INSC, meses=[(2026, 8)], log=lambda *a, **k: None)
dt = time.perf_counter() - t
pico, actual = mem()
print(json.dumps({"base": base, "pico": pico, "retenido": actual, "s": dt}))
'''

class MEMSTAT(ctypes.Structure):
    _fields_ = [("dwLength", wt.DWORD), ("dwMemoryLoad", wt.DWORD), ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong), ("x", ctypes.c_ulonglong * 5)]
m = MEMSTAT(); m.dwLength = ctypes.sizeof(m)
ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
print(f"RAM del PC: {m.ullTotalPhys / 2**30:.1f} GB total, {m.ullAvailPhys / 2**30:.1f} GB libres ahora")
print(f"{'escenario':<28} {'arbol':<17} {'pico':>8} {'retenido':>9} {'tiempo':>7}")
for esc in ("filas_xlsx ADA", "filas_xlsx Inscritos", "cargar_atenciones ADA", "SM agosto (ADA+Inscritos)"):
    for nombre, cwd in ARBOLES.items():
        r = subprocess.run([sys.executable, "-c", HIJO, esc], cwd=cwd, capture_output=True, text=True)
        linea = next((l for l in r.stdout.splitlines() if l.startswith("{")), None)
        if not linea:
            print(f"{esc:<28} {nombre:<17} FALLO: {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else '?'}")
            continue
        d = json.loads(linea)
        print(f"{esc:<28} {nombre:<17} {d['pico']:7.0f}M {d['retenido']:8.0f}M {d['s']:6.1f}s", flush=True)
