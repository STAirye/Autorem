"""Segunda tanda: el cuerpo del for de 28 specs, `_una_fila_por_atencion` y
`por_actividad` repetido."""
import sys, time
sys.path.insert(0, r"C:\Users\simon.tobar\Dr tobar\AutoREM")
import numpy as np
import pandas as pd
from programas.rem_utils import norm, SEP_ACTIVIDADES, por_actividad, contiene_todos

rng = np.random.default_rng(11)


def cron(f, veces=1):
    t = time.perf_counter()
    for _ in range(veces):
        r = f()
    return time.perf_counter() - t, r


N = 30000
print("=" * 72)
print("A) cuerpo del for de 28 specs de construir_poblacion (perfil por pieza)")
P = pd.DataFrame({"Número": [f"{i}-{i % 10}" for i in range(N)]})
est_estado = pd.Series(rng.choice(["Activo", "Egresado", ""], 1800),
                       index=[f"{i}-{i % 10}" for i in rng.choice(N, 1800, replace=False)])
est_base = pd.Series(rng.random(len(est_estado)) < 0.8, index=est_estado.index)
bug = set(P["Número"].sample(400, random_state=3))
P["col"] = P["Número"].map(est_estado).fillna("")

piezas = {
    "map(estado)+fillna": lambda: P["Número"].map(est_estado).fillna(""),
    "map(activo_base)":   lambda: P["Número"].map(est_base).fillna(False),
    "isin(bug_runs)":     lambda: P["Número"].isin(bug),
}
for nombre, f in piezas.items():
    dt, _ = cron(f, 28)
    print(f"   {nombre:22s} x28 = {dt:.3f} s")

print("=" * 72)
print("B) _una_fila_por_atencion: agg con funciones Python por columna")
from programas.rem_utils import _una_fila_por_atencion
NF = 20000
aten_id = np.repeat(np.arange(NF // 3 + 1), 3)[:NF]
CAB = ["RUN", "FECHA", "INSTR", "PROF", "TIPO", "SEXO", "SECTOR", "NACION",
       "EMIG", "ALERTAS", "FORMCLIN", "PUEBLO", "FNAC", "NOMBRES", "APAT",
       "AMAT", "ANOS", "ANOS_AT"]
d = pd.DataFrame({"ATENID": aten_id})
d["RUN"] = [f"{a}-1" for a in aten_id]
for c in CAB[1:]:
    # la cabecera solo viene en la 1a fila de cada atencion (forma Monitoreo)
    d[c] = [f"{c}{a}" if i % 3 == 0 else None for i, a in enumerate(aten_id)]
d["ACT"] = [f"Actividad {i % 40}" for i in range(NF)]
d["DIAG"] = [f"J{i % 90}" for i in range(NF)]

dt, out = cron(lambda: _una_fila_por_atencion(d.copy(), log=lambda *_: None))
print(f"   _una_fila_por_atencion sobre {NF} filas -> {len(out)} atenciones: {dt:.3f} s")

print("=" * 72)
print("C) por_actividad: 5 llamadas rehacen el mismo explode")
A = pd.Series([SEP_ACTIVIDADES.join(f"ACTIVIDAD {(i + k) % 40}" for k in range(3))
               for i in range(20000)])
MASCARAS = [lambda s: contiene_todos(s, "actividad 1"),
            lambda s: contiene_todos(s, "actividad 2"),
            lambda s: contiene_todos(s, "actividad 3"),
            lambda s: contiene_todos(s, "actividad 4"),
            lambda s: contiene_todos(s, "actividad 5")]


def cinco_llamadas():
    return [por_actividad(A, m) for m in MASCARAS]


def un_explode():
    partes = A.astype(str).str.split(";").explode().str.strip()
    return [m(partes).groupby(level=0).any().reindex(A.index, fill_value=False)
            for m in MASCARAS]


a, ra = cron(cinco_llamadas)
b, rb = cron(un_explode)
print(f"   5 llamadas={a:.3f}s  1 explode={b:.3f}s  ({a/b:.1f}x)  "
      f"iguales={all(x.equals(y) for x, y in zip(ra, rb))}")
