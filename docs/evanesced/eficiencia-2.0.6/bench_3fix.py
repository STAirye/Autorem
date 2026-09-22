"""Benchmark de los 3 arreglos de eficiencia. Corre igual en el arbol viejo y el nuevo.
Uso: python bench_3fix.py   (desde la raiz del arbol a medir)"""
import random
import time

import numpy as np
import pandas as pd

import programas.poblacion as pob
from programas import catalogos as cat
from programas.rem_utils import norm

random.seed(7)
np.random.seed(7)


def cronometrar(fn, repeticiones=1):
    t = time.perf_counter()
    for _ in range(repeticiones):
        fn()
    return time.perf_counter() - t


# -- 1. _estado_dx: una pasada completa de construir_poblacion (29 llamadas) --
n = 30000
qs = pob.QUESTIONS
df = pd.DataFrame({f"q{q}": [random.choice(["Si", "No", "", "Ingreso", "Egreso",
                                            "Seguimiento", "Leve", None])
                             for _ in range(n)] for q in qs})
df["RUN"] = np.random.randint(0, 6000, n).astype(str)
df["FECHA"] = pd.to_datetime("2026-01-01") + pd.to_timedelta(np.random.randint(0, 400, n), "D")
df["INSTR"] = [random.choice(["Medico", "Psicologo(a)", None]) for _ in range(n)]
df["INSTR_n"] = df["INSTR"].map(norm)
for q in qs:
    df[f"q{q}_n"] = df[f"q{q}"].map(norm)
corte = pd.Timestamp("2026-06-30")
mi, mf = pd.Timestamp("2026-06-01"), corte


def pasada_estado_dx():
    for spec in pob.TODAS_LAS_SPECS:
        pob._estado_dx(df, spec["dx"], spec["estado"], corte, mi, mf,
                       instrumento=spec["instrumento"], subtipo=spec["subtipo"],
                       subtipo2=spec["subtipo2"])


print(f"_estado_dx  28 specs x 1 pasada : {cronometrar(pasada_estado_dx):6.2f} s")

# -- 2. norm: mezcla realista (categoricas + alta cardinalidad) --
categoricas = ["Hombre", "Mujer", "MEDICO", "Control de Salud Mental", "Ingreso", ""]
valores = [random.choice(categoricas) for _ in range(300000)]
valores += [f"11{i:06d}-{i % 10}" for i in range(100000)]
random.shuffle(valores)
print(f"norm        400k celdas        : {cronometrar(lambda: [norm(v) for v in valores]):6.2f} s")

# -- 3. catalogos: anotar una columna de diagnosticos --
codigos = list(cat.cargar("cie10")["COD"][:2000])
print(f"anotar      2000 codigos       : {cronometrar(lambda: cat.anotar(codigos)):6.2f} s")
