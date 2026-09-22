"""Mide los candidatos de la 2a ronda de eficiencia, cada uno contra su
alternativa, sobre frames del tamano real del centro."""
import sys, time
sys.path.insert(0, r"C:\Users\simon.tobar\Dr tobar\AutoREM")
import numpy as np
import pandas as pd
from programas.rem_utils import norm

N = 30000
rng = np.random.default_rng(7)


def cron(f, veces=1):
    t = time.perf_counter()
    for _ in range(veces):
        r = f()
    return time.perf_counter() - t, r


print("=" * 70)
print("1) marcar_demografia.alerta: .map(norm) sobre ALERTAS, 4 veces")
alertas = pd.Series(rng.choice(["SENAME Justicia Juvenil", "MIGRANTE",
                                "SPE ex Mejor Ninez- Ambulatorio", "CUIDADOR", "", None],
                               N))
SUBS = [("MIGRANTE",), ("SENAME",), ("MEJOR NINEZ", "SPE EX MEJOR"), ("CUIDADOR",)]


def ahora():
    out = []
    for subs in SUBS:
        s = alertas.map(norm)          # <-- se recalcula en CADA llamada
        m = None
        for x in subs:
            c = s.str.contains(norm(x), regex=False, na=False)
            m = c if m is None else (m | c)
        out.append(m.fillna(False))
    return out


def izado():
    s = alertas.map(norm)              # una vez
    out = []
    for subs in SUBS:
        m = None
        for x in subs:
            c = s.str.contains(norm(x), regex=False, na=False)
            m = c if m is None else (m | c)
        out.append(m.fillna(False))
    return out


a, ra = cron(ahora, 3)
b, rb = cron(izado, 3)
print(f"   ahora={a:.3f}s  izado={b:.3f}s  ({a/b:.1f}x)  "
      f"iguales={all(x.equals(y) for x, y in zip(ra, rb))}")

print("=" * 70)
print("2) construir_poblacion: P['Numero'].isin(egreso_bug_runs) dentro del for de 28 specs")
numero = pd.Series([f"{i}-{i%10}" for i in range(N)])
bug_runs = set(numero.sample(400, random_state=1))


def dentro():
    acc = 0
    for _ in range(28):
        acc += int((numero.isin(bug_runs)).sum())
    return acc


def fuera():
    m = numero.isin(bug_runs)
    acc = 0
    for _ in range(28):
        acc += int(m.sum())
    return acc


a, ra = cron(dentro)
b, rb = cron(fuera)
print(f"   dentro={a:.3f}s  fuera={b:.3f}s  ({a/b:.1f}x)  igual={ra == rb}")

print("=" * 70)
print("3) mascara EGRES por columna de estado: _egreso_powerbi_bug + _estado_dx la calculan las dos")
NF = 60000            # formularios del historico
cols = {}
for q in range(29):
    cols[f"q{q}_n"] = pd.Series(rng.choice(["INGRESO", "SEGUIMIENTO", "EGRESO", ""], NF))
form = pd.DataFrame(cols)


def dos_veces():
    tot = 0
    for q in range(29):                              # _egreso_powerbi_bug
        tot += int(form[f"q{q}_n"].str.contains("EGRES", na=False).sum())
    for q in range(29):                              # _estado_dx, una por spec
        tot += int(form[f"q{q}_n"].str.contains("EGRES", na=False).sum())
    return tot


def una_vez():
    memo = {q: form[f"q{q}_n"].str.contains("EGRES", na=False) for q in range(29)}
    tot = 0
    for q in range(29):
        tot += int(memo[q].sum())
    for q in range(29):
        tot += int(memo[q].sum())
    return tot


a, ra = cron(dos_veces)
b, rb = cron(una_vez)
print(f"   dos_veces={a:.3f}s  una_vez={b:.3f}s  ({a/b:.1f}x)  igual={ra == rb}")

print("=" * 70)
print("4) _grid_y_detalle: sub[sub[flag]] (copia el frame) vs contar la mascara")
NCOLS = 60
sub = pd.DataFrame({f"c{i}": rng.integers(0, 100, 4000) for i in range(NCOLS)})
sub["Numero"] = [f"{i}-1" for i in range(4000)]
FLAGS = [f"_dem_{i}" for i in range(11)]
for f in FLAGS:
    sub[f] = rng.random(4000) < 0.05


def copiando():
    tot = 0
    for _ in range(44):                 # 44 filas del P6
        for f in FLAGS:
            marcados = sub[sub[f]]
            tot += len(marcados)
    return tot


def contando():
    tot = 0
    for _ in range(44):
        for f in FLAGS:
            tot += int(sub[f].sum())
    return tot


a, ra = cron(copiando)
b, rb = cron(contando)
print(f"   copiando={a:.3f}s  contando={b:.3f}s  ({a/b:.1f}x)  igual={ra == rb}")

print("=" * 70)
print("5) cargar_canonico no_vacias: .map(norm).ne('').any() vs corto circuito")
run = pd.Series([f"{i}-{i%10}" for i in range(N)])


def completo():
    return not run.map(norm).ne("").any()


def corto():
    return not any(norm(v) != "" for v in run)


a, ra = cron(completo, 5)
b, rb = cron(corto, 5)
print(f"   completo={a:.3f}s  corto={b:.3f}s  ({a/b:.1f}x)  igual={ra == rb}")

print("=" * 70)
print("6) _seccion_g: pd.DateOffset construido por RUN vs los 3 distintos izados")
corte = pd.Timestamp(2026, 8, 31)
UMBRAL = {0: (2, 29), 1: (5, 29)}
ADULTO = (11, 29)
runs = [(f"{i}-1", pd.Timestamp(2025, 1 + i % 12, 1 + i % 28), i % 4) for i in range(1500)]


def por_run():
    s = set()
    for r, p, e in runs:
        m, dd = UMBRAL.get(e, ADULTO)
        if corte > p + pd.DateOffset(months=m, days=dd):
            s.add(r)
    return s


_OFF = {k: pd.DateOffset(months=m, days=dd) for k, (m, dd) in
        list(UMBRAL.items()) + [(None, ADULTO)]}


def izados():
    s = set()
    for r, p, e in runs:
        off = _OFF.get(e if e in UMBRAL else None)
        if corte > p + off:
            s.add(r)
    return s


a, ra = cron(por_run)
b, rb = cron(izados)
print(f"   por_run={a:.3f}s  izados={b:.3f}s  ({a/b:.1f}x)  igual={ra == rb}")
