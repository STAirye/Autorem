"""Hallazgo 6: cuanto cuestan de verdad las re-normalizaciones del formulario
'Otros y Respi' en `_sala` y `_seccion_g` del A23, y cuanto se recuperaria.

Cuenta las llamadas reales a `map(norm)` instrumentando `norm`, y cronometra las
dos funciones sobre un formulario del tamano que pide el modulo (se baja POR ANIO
y la Seccion G necesita al menos el anio del reporte + el anterior; el PowerBI usa 5).
"""
import sys, time
sys.path.insert(0, r"C:\Users\simon.tobar\Dr tobar\AutoREM")
import numpy as np
import pandas as pd
import programas.rem_utils as ru
import modulos.rem_a23_respiratorio as a23

rng = np.random.default_rng(23)

CONDS = ["SBOR", "ASMA", "EPOC", "O2", "AV", "FQ", "OTRAS", "DISP"]
EXTRA = {"SBOR": ["rec", "grav", "prox"], "ASMA": ["grav", "ctrl", "prox"],
         "EPOC": ["tipo", "ctrl", "prox"], "O2": [], "AV": ["val"],
         "FQ": ["prox"], "OTRAS": ["prox"], "DISP": ["prox"]}


def otros(n):
    d = pd.DataFrame({
        "RUN": [f"{10000000 + i % (n // 3 + 1)}-1" for i in range(n)],
        "FECHA": pd.to_datetime("2022-01-01") + pd.to_timedelta(rng.integers(0, 1700, n), "D"),
        "_med": rng.random(n) < 0.6,
        "SEXO_o": rng.choice(["Hombre", "Mujer"], n),
        "FNAC_o": [f"{1+i%28:02d}/{1+i%12:02d}/{1950+i%70}" for i in range(n)],
        "CDV": rng.choice(["Buena", "Regular", ""], n),
    })
    for c in CONDS:
        d[f"{c}_p"] = rng.choice(["Si", "No", ""], n, p=[.25, .6, .15])
        d[f"{c}_est"] = rng.choice(["Ingreso", "Seguimiento", "Egreso", ""], n)
        for suf in EXTRA[c]:
            if suf == "prox":
                d[f"{c}_prox"] = pd.to_datetime("2024-01-01") + pd.to_timedelta(
                    rng.integers(0, 900, n), "D")
            else:
                d[f"{c}_{suf}"] = rng.choice(["Leve", "Moderada", "Severa", ""], n)
    return d


# -- instrumentacion: contar llamadas a norm y a que columna ------------------
_orig = ru.norm
CUENTA = {"llamadas": 0}


def contando(v):
    CUENTA["llamadas"] += 1
    return _orig(v)


class Espia:
    """Envuelve el frame para registrar que columnas se piden por `map(norm)`."""
    pass


def perfil(n):
    o = otros(n)
    aten = pd.DataFrame({
        "RUN": o["RUN"], "INSTR_n": "MEDICO",
        "DIAG_n": rng.choice(["J45", "J44", "E84", ""], len(o)),
        "FECHA": o["FECHA"]})
    idx = pd.Index(sorted(set(o["RUN"])), name="RUN")
    edad = pd.Series(rng.integers(0, 90, len(idx)), index=idx).astype(float)
    estrat = pd.Series(dtype=object)
    corte = pd.Timestamp(2026, 8, 31)

    # -- conteo de llamadas a norm, por funcion --
    for nombre, fn in (("_sala", lambda: a23._sala(idx, edad, aten, o, estrat)),
                       ("_seccion_g", lambda: a23._seccion_g(o, corte))):
        ru.norm = contando
        a23.norm = contando
        CUENTA["llamadas"] = 0
        t = time.perf_counter()
        fn()
        dt = time.perf_counter() - t
        llamadas = CUENTA["llamadas"]
        ru.norm = _orig
        a23.norm = _orig
        pasadas = llamadas / len(o)
        print(f"  {nombre:12s} {dt:6.3f} s   {llamadas:>9,} llamadas a norm "
              f"= {pasadas:.0f} pasadas sobre las {len(o)} filas")

    # -- cuanto de ese tiempo es norm: sustituir norm por la identidad ---------
    ru.norm = lambda v: "" if v is None else str(v).upper()
    a23.norm = ru.norm
    t = time.perf_counter(); a23._sala(idx, edad, aten, o, estrat); s1 = time.perf_counter() - t
    t = time.perf_counter(); a23._seccion_g(o, corte); s2 = time.perf_counter() - t
    ru.norm = _orig; a23.norm = _orig
    t = time.perf_counter(); a23._sala(idx, edad, aten, o, estrat); r1 = time.perf_counter() - t
    t = time.perf_counter(); a23._seccion_g(o, corte); r2 = time.perf_counter() - t
    print(f"  total real = {r1+r2:.3f} s")
    print(f"  techo teorico si norm fuera gratis = {s1+s2:.3f} s "
          f"(o sea: norm es {(r1+r2-s1-s2)/(r1+r2)*100:.0f}% de estas dos funciones)")


for n in (5000, 20000):
    print(f"\n=== formulario 'Otros y Respi' de {n} filas "
          f"({'1 anio' if n == 5000 else '~4-5 anios, que es lo que pide la Seccion G'}) ===")
    perfil(n)
