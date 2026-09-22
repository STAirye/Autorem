"""Prueba de EQUIVALENCIA de poblacion._estado_dx tras el recorte de columnas (2.0.6).

Se corrio inline (`python -c`) antes de commitear el cambio; se transcribe tal cual.
Lleva adentro una COPIA de la version vieja (la de 2.0.5) para comparar contra ella:
esa copia es el valor del script y por eso no se toca.

Lo que amarra: 28 specs x instrumento True/False = 56 comparaciones, con fechas
llenas de EMPATES a proposito (25 fechas distintas sobre 8000 filas), que es el unico
caso donde recortar columnas podria haber cambiado el resultado si `sort_values`
ordenara por algo mas que la clave FECHA. Resultado: 0 diferencias.

Uso:  PYTHONPATH=<raiz> python equivalencia_estado_dx.py
"""
import random

import numpy as np
import pandas as pd

import programas.poblacion as pob


def _estado_dx_viejo(df, dx, estado, corte, mes_ini, mes_fin, *, instrumento=True,
                     subtipo=None, subtipo2=None):
    """La version 2.0.5, textual: sin recorte de columnas."""
    qd, qe = f"q{dx}_n", f"q{estado}_n"
    cond_si = df[qd] == "SI"
    cond_ing = cond_si & (df[qe].str.contains("INGRES", na=False) |
                          df[qe].str.contains("SEGUIMIEN", na=False))
    cond_egr = cond_si & df[qe].str.contains("EGRES", na=False)
    if instrumento:
        ok = df["INSTR_n"].str.contains("MEDIC", na=False)
        cond_ing &= ok
        cond_egr &= ok
    activos = (df[cond_ing & (df["FECHA"] <= corte)]
               .sort_values("FECHA").groupby("RUN").last())
    egr = set(df.loc[cond_egr & df["FECHA"].between(mes_ini, mes_fin), "RUN"])
    out = pd.DataFrame(index=sorted(set(activos.index) | egr))
    out["activo_base"] = out.index.isin(activos.index)
    out["estado"] = np.where(out.index.isin(egr), "Egresado",
                             np.where(out["activo_base"], "Activo", ""))
    if subtipo:
        c = f"q{subtipo}"
        out["subtipo"] = activos[c].reindex(out.index) if c in activos.columns else ""
    if subtipo2:
        c = f"q{subtipo2}"
        out["subtipo2"] = activos[c].reindex(out.index) if c in activos.columns else ""
    out["instr"] = activos["INSTR"].reindex(out.index) if "INSTR" in activos.columns else ""
    out["fecha"] = activos["FECHA"].reindex(out.index) if "FECHA" in activos.columns else pd.NaT
    return out


random.seed(7)
np.random.seed(7)
n = 8000
qs = pob.QUESTIONS
df = pd.DataFrame({f"q{q}": [random.choice(["Si", "No", "", "Ingreso", "Egreso",
                                            "Seguimiento", "Leve", "Grave", None])
                             for _ in range(n)] for q in qs})
df["RUN"] = np.random.randint(0, 900, n).astype(str)
# MUCHOS empates de fecha a proposito: es el caso delicado.
df["FECHA"] = pd.to_datetime("2026-01-01") + pd.to_timedelta(np.random.randint(0, 25, n), "D")
df["INSTR"] = [random.choice(["Medico", "Psicologo(a)", "MEDICO GENERAL", None]) for _ in range(n)]
df["INSTR_n"] = df["INSTR"].map(pob.norm)
for q in qs:
    df[f"q{q}_n"] = df[f"q{q}"].map(pob.norm)
corte = pd.Timestamp("2026-01-31")
mi, mf = pd.Timestamp("2026-01-01"), corte

dif = 0
for spec in pob.TODAS_LAS_SPECS:
    for instr in (True, False):
        kw = dict(instrumento=instr, subtipo=spec["subtipo"], subtipo2=spec["subtipo2"])
        a = _estado_dx_viejo(df, spec["dx"], spec["estado"], corte, mi, mf, **kw)
        b = pob._estado_dx(df, spec["dx"], spec["estado"], corte, mi, mf, **kw)
        if not a.equals(b):
            dif += 1
            print("DIFIERE", spec["col"], instr)
print("specs comparadas:", len(pob.TODAS_LAS_SPECS) * 2, "| diferencias:", dif)

# Guardas del else: frame SIN INSTR y con subtipos que no existen como columna.
d2 = df.drop(columns=["INSTR"])
s = pob.TODAS_LAS_SPECS[0]
a = _estado_dx_viejo(d2, s["dx"], s["estado"], corte, mi, mf, subtipo=999, subtipo2=998)
b = pob._estado_dx(d2, s["dx"], s["estado"], corte, mi, mf, subtipo=999, subtipo2=998)
print("sin INSTR / subtipo inexistente:", "igual" if a.equals(b) else "DIFIERE")
