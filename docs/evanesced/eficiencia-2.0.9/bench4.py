"""Desglose de `_una_fila_por_atencion` y una alternativa vectorizada para
`_primero` (el 1er valor no vacio del grupo), comparando resultado a resultado."""
import sys, time, cProfile, pstats, io
sys.path.insert(0, r"C:\Users\simon.tobar\Dr tobar\AutoREM")
import numpy as np
import pandas as pd
from programas.rem_utils import norm, SEP_ACTIVIDADES, _una_fila_por_atencion

NF = 20000
aten_id = np.repeat(np.arange(NF // 3 + 1), 3)[:NF]
CAB = ["RUN", "FECHA", "INSTR", "PROF", "TIPO", "SEXO", "SECTOR", "NACION",
       "EMIG", "ALERTAS", "FORMCLIN", "PUEBLO", "FNAC", "NOMBRES", "APAT",
       "AMAT", "ANOS", "ANOS_AT"]
d = pd.DataFrame({"ATENID": aten_id})
d["RUN"] = [f"{a}-1" for a in aten_id]
for c in CAB[1:]:
    d[c] = [f"{c}{a}" if i % 3 == 0 else None for i, a in enumerate(aten_id)]
d["ACT"] = [f"Actividad {i % 40}" for i in range(NF)]
d["DIAG"] = [f"J{i % 90}" for i in range(NF)]

pr = cProfile.Profile()
pr.enable()
out_ref = _una_fila_por_atencion(d.copy(), log=lambda *_: None)
pr.disable()
s = io.StringIO()
pstats.Stats(pr, stream=s).sort_stats("cumulative").print_stats(14)
print(s.getvalue()[:3000])

# ---- alternativa: misma clave, agg vectorizado -----------------------------
from programas.rem_utils import clave_atencion, SEP_ACTIVIDADES


def alternativa(d):
    aten = d["ATENID"].map(clave_atencion)
    dup = aten.ne("") & aten.duplicated(keep=False)
    if not dup.any():
        return d
    grupo = pd.Series(pd.factorize(aten.where(dup))[0], index=d.index)
    solas = pd.Series(range(-1, -len(d) - 1, -1), index=d.index)
    clave = grupo.where(grupo >= 0, solas)
    g = d.groupby(clave, sort=False)
    out = {}
    for c in d.columns:
        col = d[c]
        lleno = col.map(norm).ne("")              # UNA pasada de norm por columna
        if c in ("ACT", "DIAG"):
            vals = col.where(lleno).astype(object)
            out[c] = (vals.dropna().astype(str).str.strip()
                      .groupby(clave[vals.notna()], sort=False)
                      .agg(lambda s: SEP_ACTIVIDADES.join(dict.fromkeys(s)))
                      .reindex(g.size().index))
        else:
            primero = col.where(lleno).groupby(clave, sort=False).first()
            respaldo = g[c].first()               # grupo entero vacio -> su 1er valor
            out[c] = primero.where(primero.notna(), respaldo)
    return pd.DataFrame(out).reset_index(drop=True)


t = time.perf_counter()
out_alt = alternativa(d.copy())
dt_alt = time.perf_counter() - t

t = time.perf_counter()
out_ref2 = _una_fila_por_atencion(d.copy(), log=lambda *_: None)
dt_ref = time.perf_counter() - t

print(f"\nactual={dt_ref:.3f}s   alternativa={dt_alt:.3f}s   ({dt_ref/dt_alt:.1f}x)")
print("mismas filas:", len(out_ref2) == len(out_alt))
iguales = all(
    out_ref2[c].astype(str).reset_index(drop=True)
    .equals(out_alt[c].astype(str).reset_index(drop=True))
    for c in out_ref2.columns)
print("mismo contenido:", iguales)
if not iguales:
    for c in out_ref2.columns:
        a = out_ref2[c].astype(str).reset_index(drop=True)
        b = out_alt[c].astype(str).reset_index(drop=True)
        if not a.equals(b):
            print("  difiere:", c, a.head(3).tolist(), b.head(3).tolist())
