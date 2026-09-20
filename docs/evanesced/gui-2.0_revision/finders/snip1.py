import pandas as pd, numpy as np, sys
print(sys.version, pd.__version__)
def norm(v):
    import re
    if v is None or v != v: return ""
    s = str(v).upper().strip()
    return re.sub(r"\s+", " ", s)
d = pd.DataFrame({"a": [], "b": []})
print("DataFrame({a: []}) dtypes:", dict(d.dtypes))
s = pd.Series([], dtype=object)
print("empty obj .map(norm):", s.map(norm).dtype)
print("empty float .map(norm):", d["a"].map(norm).dtype)
try:
    print(d["a"].map(norm).str.contains("X", na=False))
except Exception as e:
    print("str on mapped empty:", type(e).__name__, e)
try:
    print(d["a"].astype(str).str.strip().dtype)
except Exception as e:
    print("astype str:", type(e).__name__, e)
# rows-based construction as in cargar_canonico
filas = []
col = {"RUN": "X", "FECHA": "Y", "NONE": None}
idx = {"X": 0, "Y": 1}
parte = pd.DataFrame({k: [f[idx[c]] if c is not None and idx[c] < len(f) else None for f in filas] for k, c in col.items()})
print("cargar_canonico 0 rows dtypes:", dict(parte.dtypes))
filas = [("a", None)]
parte = pd.DataFrame({k: [f[idx[c]] if c is not None and idx[c] < len(f) else None for f in filas] for k, c in col.items()})
print("cargar_canonico 1 row dtypes:", dict(parte.dtypes))
