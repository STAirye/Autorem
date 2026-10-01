"""P6 + Rescate con historia larga, como gui/paginas/poblacion.correr: tiempo de pared
por fase (funciones envueltas), sin profiler. --perfil N: cProfile de la fase N. Solo
imprime tiempos y nombres de funcion."""
import sys, time, tempfile, functools, collections, cProfile, pstats
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from bench_a23 import DM, ADA, pico_mb, quiet   # mismas rutas del A23 (ADA 2021..2026 09)

import programas.poblacion as pob
import programas.rem_utils as ru
import modulos.rem_sp_p6_poblacion as p6
import modulos.rem_sm_rescate_inasistentes as resc

FORM = sorted((DM / "PSM").glob("*.xlsx"))
INSC = DM.parent / "Población" / "Informe_Inscritos__Adscritos_.xlsx"
MES = (2026, 8)
ADA = [p for p in ADA if p.stem != "2026 09"]   # (el 2026 09 lo modificaron a las 17:17: 2 hojas)
T = collections.defaultdict(float)
N = collections.Counter()


def envolver(mod, nombre, et=None):
    f = getattr(mod, nombre)
    et = et or f"{mod.__name__.split('.')[-1]}.{nombre}"

    @functools.wraps(f)
    def w(*a, **k):
        t = time.perf_counter()
        try:
            return f(*a, **k)
        finally:
            T[et] += time.perf_counter() - t
            N[et] += 1
    setattr(mod, nombre, w)


envolver(ru, "_hojas_calamine", "  (lectura calamine, dentro de cargas)")
for n in [x for x in dir(pob) if x.startswith("_") and callable(getattr(pob, x))
          and getattr(getattr(pob, x), "__module__", "") == pob.__name__]:
    envolver(pob, n)
for n in [x for x in dir(p6) if x.startswith("_") and callable(getattr(p6, x))
          and getattr(getattr(p6, x), "__module__", "") == p6.__name__]:
    envolver(p6, n)

FASES = []


def fase(nombre, fn):
    t = time.perf_counter()
    r = fn()
    FASES.append((nombre, time.perf_counter() - t))
    return r


def main():
    tmp = Path(tempfile.mkdtemp(prefix="bench_p6_"))
    try:
        t0 = time.perf_counter()
        insc = fase("cargar_inscritos", lambda: pob.cargar_inscritos(INSC, log=quiet))
        form = fase("cargar_formulario_sm", lambda: pob.cargar_formulario_sm(FORM, log=quiet))
        ada = fase("cargar_atenciones", lambda: ru.cargar_atenciones(ADA, log=quiet))
        P = fase("construir_poblacion", lambda: pob.construir_poblacion(insc, form, ada, mes=MES, log=quiet))
        res = fase("construir_p6", lambda: p6.construir_p6(P, log=quiet))
        fase("p6.escribir", lambda: p6.escribir(P, res, tmp / "p6.xlsx"))
        Er = fase("rescate.procesar", lambda: resc.procesar(insc, form, ada, mes=MES, log=quiet, P=P, fuentes=[]))
        fase("rescate.escribir", lambda: resc.escribir(Er, tmp / "resc.xlsx"))
        tot = time.perf_counter() - t0
        print(f"P: {P.shape[0]} filas x {P.shape[1]} cols | TOTAL {tot:.1f} s | pico RAM {pico_mb():.0f} MB")
        for i, (n, v) in enumerate(FASES):
            print(f"  [{i}] {v:6.1f} s  {n}")
        print("  -- funciones internas (>= 0.3 s) --")
        for k, v in sorted(T.items(), key=lambda x: -x[1]):
            if v >= 0.3:
                print(f"     {v:6.1f} s  x{N[k]:<4} {k}")
    finally:
        for p in tmp.glob("*"):
            p.unlink()
        tmp.rmdir()


if __name__ == "__main__":
    main()
