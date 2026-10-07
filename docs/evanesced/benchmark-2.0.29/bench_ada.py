"""Reparto de cargar_atenciones (ADA 2021-26): lectura calamine por archivo vs el resto
(canonico, colapso por atencion, norm, fechas). Solo tiempos y conteos."""
import sys, time, functools
sys.path.insert(0, r"D:\git\Autorem")
import tests._aislar_cache  # noqa
import programas.rem_utils as ru
from bench_todo import ADA_TODO, quiet
T = []
f = ru._hojas_calamine
@functools.wraps(f)
def w(e):
    t = time.perf_counter(); r = f(e); T.append((str(e).split("\\")[-1], time.perf_counter() - t, sum(len(h[1]) for h in r))); return r
ru._hojas_calamine = w
for nombre in ("_una_fila_por_atencion", "fecha_col", "exigir_estamento", "cargar_canonico"):
    g = getattr(ru, nombre)
    def mk(g, nombre):
        @functools.wraps(g)
        def ww(*a, **k):
            t = time.perf_counter(); r = g(*a, **k); T.append((nombre, time.perf_counter() - t, None)); return r
        return ww
    setattr(ru, nombre, mk(g, nombre))
t0 = time.perf_counter()
d = ru.cargar_atenciones(ADA_TODO, log=quiet)
tot = time.perf_counter() - t0
for n, t, filas in T:
    print(f"  {t:6.2f} s  {n}" + (f"  ({filas} filas)" if filas else ""))
print(f"TOTAL {tot:.2f} s, {len(d)} atenciones")
