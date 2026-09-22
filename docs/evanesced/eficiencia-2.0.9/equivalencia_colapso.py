"""Equivalencia de `_una_fila_por_atencion`: la version 2.0.8 (copia TEXTUAL aca
adentro) contra la nueva, sobre frames con los bordes que el benchmark no tocaba:
grupos con la cabecera vacia en TODAS sus filas, ACT/DIAG vacios en todo el grupo,
ATEN ID numerico, tipos mezclados y filas sueltas entre atenciones multilinea.

Compara valor a valor con `repr` (no `astype(str)`): un 683016530 que se vuelve
683016530.0 tiene que saltar.
"""
import sys, time
sys.path.insert(0, r"C:\Users\simon.tobar\Dr tobar\AutoREM")
import numpy as np
import pandas as pd
from programas.rem_utils import norm, clave_atencion, SEP_ACTIVIDADES, ArchivoInvalido

CAB = ["RUN", "FECHA", "INSTR", "PROF", "TIPO", "SEXO", "SECTOR", "NACION",
       "EMIG", "ALERTAS", "FORMCLIN", "PUEBLO", "FNAC", "NOMBRES", "APAT",
       "AMAT", "ANOS", "ANOS_AT"]


# ====================================================================== VIEJA
def _clave(d):
    """El tramo COMUN a las dos versiones (identico en las dos)."""
    aten = d["ATENID"].map(clave_atencion)
    dup = aten.ne("") & aten.duplicated(keep=False)
    if not dup.any():
        return None
    grupo = pd.Series(pd.factorize(aten.where(dup))[0], index=d.index)
    solas = pd.Series(range(-1, -len(d) - 1, -1), index=d.index)
    return grupo.where(grupo >= 0, solas)


def vieja(d):
    clave = _clave(d)
    if clave is None:
        return d

    def _juntar(s):
        vals = [str(v).strip() for v in s if norm(v) != ""]
        return SEP_ACTIVIDADES.join(dict.fromkeys(vals)) if vals else None

    def _primero(s):
        vals = [v for v in s if norm(v) != ""]
        return vals[0] if vals else (s.iloc[0] if len(s) else None)

    agg = {c: (_juntar if c in ("ACT", "DIAG") else _primero) for c in d.columns}
    return d.groupby(clave, sort=False).agg(agg).reset_index(drop=True)


# ====================================================================== NUEVA
def nueva(d):
    clave = _clave(d)
    if clave is None:
        return d

    def _juntar(s):
        vals = [str(v).strip() for v in s if norm(v) != ""]
        return SEP_ACTIVIDADES.join(dict.fromkeys(vals)) if vals else None

    pos = np.arange(len(d))
    gpos = pd.Series(pos, index=d.index).groupby(clave, sort=False)
    primera = gpos.min().to_numpy()          # 1a fila de cada grupo, en orden de aparicion
    orden = gpos.min().index                 # las claves, en el MISMO orden

    out = {}
    for c in d.columns:
        col = d[c]
        if c in ("ACT", "DIAG"):
            out[c] = col.groupby(clave, sort=False).agg(_juntar).to_numpy()
            continue
        lleno = col.map(norm).ne("").to_numpy()
        # posicion del 1er valor NO vacio del grupo; len(d) = "el grupo no tiene ninguno"
        pl = (pd.Series(np.where(lleno, pos, len(d)), index=d.index)
              .groupby(clave, sort=False).min().to_numpy())
        elegida = np.where(pl < len(d), pl, primera)
        out[c] = col.to_numpy()[elegida]
    res = pd.DataFrame(out, index=orden).reset_index(drop=True)
    return res


# ====================================================================== CASOS
def caso_bordes():
    """Bordes a mano: cabecera vacia en todo el grupo, ACT/DIAG vacios, NaN primero."""
    filas = [
        # at. 1: dos filas, cabecera en la 1a (forma Monitoreo normal)
        dict(ATENID=1, RUN="11111111-1", INSTR="MEDICO", ACT="CONTROL", DIAG="J45", SEXO="Mujer"),
        dict(ATENID=1, RUN=None, INSTR=None, ACT="EDUCACION", DIAG=None, SEXO=None),
        # at. 2: SEXO vacio en TODAS sus filas, y la 1a es NaN y la 2a "" -> _primero
        #        devuelve s.iloc[0] (NaN), no el "" de la 2a
        dict(ATENID=2, RUN="10000013-3", INSTR="KINE", ACT="KTR", DIAG="J44", SEXO=np.nan),
        dict(ATENID=2, RUN=None, INSTR=None, ACT="ESPIROMETRIA", DIAG=None, SEXO=""),
        # at. 3: al reves, "" primero y NaN despues
        dict(ATENID=3, RUN="10000021-1", INSTR="MEDICO", ACT="CONSULTA", DIAG="J20", SEXO=""),
        dict(ATENID=3, RUN=None, INSTR=None, ACT=None, DIAG=None, SEXO=np.nan),
        # at. 4: ACT y DIAG vacios en TODO el grupo -> _juntar devuelve None
        dict(ATENID=4, RUN="10000048-4", INSTR="MEDICO", ACT=None, DIAG="   ", SEXO="Hombre"),
        dict(ATENID=4, RUN=None, INSTR=None, ACT="  ", DIAG=None, SEXO=None),
        # at. 5: SUELTA (una sola fila) entre medio
        dict(ATENID=5, RUN="10000056-5", INSTR="MEDICO", ACT="CONTROL", DIAG="J45", SEXO="Mujer"),
        # at. 6: cabecera solo en la SEGUNDA fila (fila padre desordenada)
        dict(ATENID=6, RUN=None, INSTR=None, ACT="CONTROL", DIAG=None, SEXO=None),
        dict(ATENID=6, RUN="10000064-6", INSTR="MATRONA", ACT="EDUCACION", DIAG="J45", SEXO="Mujer"),
        # at. 7: actividades REPETIDAS -> dict.fromkeys dedup, y con espacios al borde
        dict(ATENID=7, RUN="10000072-7", INSTR="MEDICO", ACT=" CONTROL ", DIAG="J45", SEXO="Hombre"),
        dict(ATENID=7, RUN=None, INSTR=None, ACT="CONTROL", DIAG="J45", SEXO=None),
    ]
    return pd.DataFrame(filas)


def caso_atenid_numerico():
    """ATEN ID de IRIS: numerico. openpyxl lo entrega int o float segun la celda."""
    filas = []
    for i, aid in enumerate([683016530, 683016531, 683016532]):
        filas.append(dict(ATENID=aid, RUN=f"1000001{i}-1", INSTR="MEDICO",
                          ACT="CONTROL", DIAG="J45", ANOS=40 + i))
        filas.append(dict(ATENID=aid, RUN=None, INSTR=None,
                          ACT="EDUCACION", DIAG=None, ANOS=None))
    return pd.DataFrame(filas)


def caso_grande(n=20000, semilla=3):
    rng = np.random.default_rng(semilla)
    aten = np.repeat(np.arange(n // 3 + 1), 3)[:n]
    # una de cada 7 atenciones queda SUELTA (id unico) -> export mixto
    aten = np.where(np.arange(n) % 7 == 0, 10 ** 6 + np.arange(n), aten)
    d = pd.DataFrame({"ATENID": aten})
    d["RUN"] = [f"{a % 900 + 100}-1" if i % 3 == 0 else None for i, a in enumerate(aten)]
    for j, c in enumerate(CAB[1:]):
        d[c] = [f"{c}{a}" if (i % 3 == 0 and (i + j) % 11) else
                (None if (i + j) % 2 else "  ") for i, a in enumerate(aten)]
    d["ACT"] = [f"Actividad {i % 40}" if i % 23 else None for i in range(n)]
    d["DIAG"] = [f"J{i % 90}" if i % 17 else "" for i in range(n)]
    return d


def comparar(nombre, d):
    a = vieja(d.copy())
    t = time.perf_counter(); b = nueva(d.copy()); dt_b = time.perf_counter() - t
    t = time.perf_counter(); vieja(d.copy()); dt_a = time.perf_counter() - t
    fallas = []
    if list(a.columns) != list(b.columns):
        fallas.append(f"columnas: {list(a.columns)} vs {list(b.columns)}")
    if len(a) != len(b):
        fallas.append(f"filas: {len(a)} vs {len(b)}")
    else:
        for c in a.columns:
            va, vb = a[c].tolist(), b[c].tolist()
            for i, (x, y) in enumerate(zip(va, vb)):
                mismo = (repr(x) == repr(y)) or (x != x and y != y)   # NaN == NaN
                if not mismo:
                    fallas.append(f"{c}[{i}]: {x!r} ({type(x).__name__}) != "
                                  f"{y!r} ({type(y).__name__})")
    marca = "OK  " if not fallas else "FALLA"
    print(f"[{marca}] {nombre:22s} filas={len(d):>6} -> {len(a):>6}  "
          f"vieja={dt_a:.3f}s nueva={dt_b:.3f}s"
          + (f"  ({dt_a/dt_b:.1f}x)" if dt_b else ""))
    for f in fallas[:12]:
        print("        ", f)
    return not fallas


ok = True
ok &= comparar("bordes", caso_bordes())
ok &= comparar("atenid numerico", caso_atenid_numerico())
for s in range(5):
    ok &= comparar(f"grande semilla={s}", caso_grande(6000, s))
ok &= comparar("grande 20k", caso_grande(20000, 99))
print("\nTODO IGUAL" if ok else "\nHAY DIFERENCIAS")
