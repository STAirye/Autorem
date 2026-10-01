"""Segunda pasada: lectura por archivo, perfil de cargar_inasistentes y de escribir.
Solo tiempos, nombres de funcion y conteos de filas/columnas."""
import sys, time, cProfile, pstats, io, tempfile, pickle
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from bench_a23 import a23, ru, ADA, OTROS, NSP, EST, MES, quiet  # (envueltas: ~0 overhead)

for p in ADA + NSP + OTROS + [EST]:
    t = time.perf_counter()
    h = ru._hojas_calamine(p)
    filas = sum(len(f) for _, f in h)
    print(f"  {time.perf_counter() - t:5.1f} s  {filas:>7} filas  {p.parent.name}/{p.name}")


def perfil(nombre, fn, n=14):
    pr = cProfile.Profile()
    pr.enable()
    r = fn()
    pr.disable()
    s = io.StringIO()
    pstats.Stats(pr, stream=s).sort_stats("cumulative").print_stats(n)
    print(f"\n=== {nombre} ===")
    print("\n".join(l for l in s.getvalue().splitlines() if l.strip())[:6000])
    return r


perfil("cargar_inasistentes", lambda: a23.cargar_inasistentes(NSP, log=quiet))
fer = a23.procesar(ADA, otros=OTROS, estrat=EST, inasistentes=NSP, mes=MES, log=quiet)
print(f"\nfer: {fer.shape[0]} filas x {fer.shape[1]} columnas")
TMP = Path(tempfile.mkdtemp(prefix="bench_a23_"))
try:
    perfil("escribir", lambda: a23.escribir(fer, TMP / "a23.xlsx"), 20)
finally:
    for p in TMP.glob("*"):
        p.unlink()
    TMP.rmdir()
