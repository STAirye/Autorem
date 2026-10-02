"""SM Actividades (ADA + grupal + Inscritos) antes/despues de la demografia del grupal
(2.0.27). Uso: python bench_sm.py <raiz_del_codigo> [anios_ada...]. Pared por fase, sin
profiler; solo imprime tiempos, conteos y nombres de funcion."""
import sys, os, time, tempfile, functools, collections
from pathlib import Path
RAIZ = sys.argv[1]
sys.path.insert(0, RAIZ)
import tests._aislar_cache  # noqa: F401
import programas.rem_utils as ru
import modulos.rem_sm_actividades as sm

DM = Path(os.path.expanduser("~")) / "OneDrive - Ilustre Municipalidad de Maipú" / "Datos madre"
ANIOS = sys.argv[2:] or ["2026", "2026 09"]
ADA = [DM / "Variables 12m" / "Atenciones" / f"{a}.xlsx" for a in ANIOS]
GRUPAL = [DM / "Variables 12m" / "Atenciones Grupales" / f"{a}.xlsx" for a in ("2026", "2026 09")]
INSC = DM / "Población" / "Informe_Inscritos__Adscritos_.xlsx"
T = collections.defaultdict(float)
N = collections.Counter()


def envolver(mod, nombre):
    if not hasattr(mod, nombre):
        return
    f = getattr(mod, nombre)

    @functools.wraps(f)
    def w(*a, **k):
        t = time.perf_counter()
        try:
            return f(*a, **k)
        finally:
            T[nombre] += time.perf_counter() - t
            N[nombre] += 1
    setattr(mod, nombre, w)


for n in ("cargar_atenciones", "cargar_grupal", "cargar_inscritos", "trans_map",
          "demografia_por_run", "_cargar", "_eventos_mes", "_tablas", "_avisos_grupal"):
    envolver(sm, n)


def quiet(*a, **k):
    pass


def correr(meses):
    T.clear(); N.clear()
    tmp = Path(tempfile.mkdtemp(prefix="bench_sm_"))
    try:
        t0 = time.perf_counter()
        E = sm.procesar_rango(ADA, grupal=GRUPAL, inscritos=INSC, meses=meses, log=quiet)
        t1 = time.perf_counter()
        sm.escribir(E, tmp / "sm.xlsx")
        t2 = time.perf_counter()
    finally:
        for p in tmp.glob("*"):
            p.unlink()
        tmp.rmdir()
    print(f"  meses={len(meses)} | procesar {t1 - t0:5.1f} s | escribir {t2 - t1:4.1f} s | "
          f"TOTAL {t2 - t0:5.1f} s | eventos {len(E)}")
    for k, v in sorted(T.items(), key=lambda x: -x[1]):
        print(f"     {v:5.1f} s  x{N[k]:<2} {k}")


print(f"== {ru.VERSION}  ADA={ANIOS}")
correr([(2026, 9)])
correr([(2026, 7), (2026, 8), (2026, 9)])
