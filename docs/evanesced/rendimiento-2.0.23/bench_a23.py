"""A23 con ADA 2021..2026-09 (la corrida que se 'pego'): tiempo de pared por fase,
sin profiler. Envuelve funciones del modulo para repartir. Solo imprime tiempos."""
import sys, os, time, tempfile, functools, collections, ctypes
from ctypes import wintypes
from pathlib import Path
RAIZ = r"C:\Users\simon.tobar\Dr tobar\AutoREM"
sys.path.insert(0, RAIZ)
import tests._aislar_cache  # noqa: F401

import programas.rem_utils as ru
import modulos.rem_a23_respiratorio as a23

DM = Path(os.path.expanduser("~")) / "OneDrive - Ilustre Municipalidad de Maip\u00fa" / "Datos madre" / "Variables 12m"
ANIOS = ["2021", "2022", "2023", "2024", "2025", "2026", "2026 09"]
ADA = [DM / "Atenciones" / f"{a}.xlsx" for a in ANIOS]
OTROS = sorted((DM / "Otros y Respi").glob("*.xlsx"))
NSP = [DM / "Inasistentes" / f"{a}.xlsx" for a in ANIOS]
EST = DM.parent / "Poblaci\u00f3n" / "Estratificaci\u00f3n_de_Riesgo.xlsx"
MES = (2026, 9)

T = collections.defaultdict(float)
N = collections.Counter()


def envolver(mod, nombre, etiqueta=None):
    f = getattr(mod, nombre)
    et = etiqueta or nombre

    @functools.wraps(f)
    def w(*a, **k):
        t = time.perf_counter()
        try:
            return f(*a, **k)
        finally:
            T[et] += time.perf_counter() - t
            N[et] += 1
    setattr(mod, nombre, w)


envolver(ru, "_hojas_calamine", "  lectura calamine (dentro de cargas)")
for n in ("cargar_atenciones", "cargar_otros", "cargar_estrat", "cargar_inasistentes",
          "filtrar_mes", "_masks_simples", "_sala", "_seccion_g", "_seccion_h",
          "_estamento_por_funcionario", "_tablas_a23", "_edad", "_origen"):
    envolver(a23, n)


class PMC(ctypes.Structure):
    _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                ("a", ctypes.c_size_t), ("b", ctypes.c_size_t), ("c", ctypes.c_size_t),
                ("d", ctypes.c_size_t), ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t)]


def pico_mb():
    k = ctypes.WinDLL("psapi")
    k.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(PMC), wintypes.DWORD]
    k.GetProcessMemoryInfo.restype = wintypes.BOOL
    h = ctypes.windll.kernel32.GetCurrentProcess
    h.restype = wintypes.HANDLE
    m = PMC(); m.cb = ctypes.sizeof(PMC)
    k.GetProcessMemoryInfo(h(), ctypes.byref(m), m.cb)
    return m.PeakWorkingSetSize / 2**20


def quiet(*a, **k):
    pass


def main():
    TMP = Path(tempfile.mkdtemp(prefix="bench_a23_"))
    try:
        t0 = time.perf_counter()
        fer = a23.procesar(ADA, otros=OTROS, estrat=EST, inasistentes=NSP, mes=MES, log=quiet)
        t1 = time.perf_counter()
        a23.escribir(fer, TMP / "a23.xlsx")
        t2 = time.perf_counter()
        print(f"filas detalle: {len(fer)}")
        print(f"procesar {t1 - t0:6.1f} s | escribir {t2 - t1:6.1f} s | TOTAL {t2 - t0:6.1f} s | pico RAM {pico_mb():.0f} MB")
        for k, v in sorted(T.items(), key=lambda x: -x[1]):
            print(f"  {v:6.1f} s  x{N[k]:<3} {k}")
    finally:
        for p in TMP.glob("*"):
            p.unlink()
        TMP.rmdir()


if __name__ == "__main__":
    main()
