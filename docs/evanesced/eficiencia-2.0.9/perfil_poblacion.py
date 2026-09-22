"""Perfil REAL de `construir_poblacion` (la pasada del P6 + la de Brecha_Medico),
a tamano de centro, para ordenar el trabajo que queda por impacto MEDIDO y no por
lectura del codigo. Datos sinteticos (nunca datos de pacientes en el repo)."""
import sys, time, cProfile, pstats, io
sys.path.insert(0, r"C:\Users\simon.tobar\Dr tobar\AutoREM")
import numpy as np
import pandas as pd
import programas.poblacion as pob
from programas.rem_utils import norm

rng = np.random.default_rng(42)
N_PERS, N_FORM, N_ATEN = 30000, 60000, 120000
CORTE = (2026, 8)


def _runs(n):
    return np.array([f"{10000000 + i}-{i % 10}" for i in range(n)])


RUNS = _runs(N_PERS)


def inscritos():
    d = pd.DataFrame({
        "RUN": RUNS,
        "TIPOID": rng.choice(["RUN", "RUN RESPONSABLE", "PASAPORTE"], N_PERS, p=[.95, .01, .04]),
        "SEXO": rng.choice(["Hombre", "Mujer", ""], N_PERS, p=[.45, .53, .02]),
        "GENERO": rng.choice(["Masculino", "Femenina", "Femenino Trans", ""], N_PERS,
                             p=[.44, .52, .01, .03]),
        "FNAC": [f"{1 + i % 28:02d}/{1 + i % 12:02d}/{1950 + i % 70}" for i in range(N_PERS)],
        "EDADANOS": rng.integers(0, 95, N_PERS),
        "SITUACION": "Inscrito",
        "ESTADO": rng.choice(["Activo", "Pasivo"], N_PERS, p=[.9, .1]),
        "FPASIV": "", "MPASIV": rng.choice(["", "FALLECIDO", "TRASLADO"], N_PERS, p=[.95, .03, .02]),
        "SECTOR": rng.choice(["AZUL", "VERDE", "ROJO"], N_PERS),
        "ALERTAS": rng.choice(["", "SENAME Justicia Juvenil", "SPE ex Mejor Ninez", "CUIDADOR"],
                              N_PERS, p=[.9, .04, .03, .03]),
        "PUEBLO": rng.choice(["Ninguno", "Mapuche", "No Contesta", ""], N_PERS, p=[.8, .1, .05, .05]),
        "NACIONALIDAD": rng.choice(["Chilena", "Venezolana", "Haitiana"], N_PERS, p=[.9, .07, .03]),
    })
    d.attrs["columnas_ausentes"] = []
    return d


def formulario():
    idx = rng.choice(N_PERS, N_FORM)
    d = pd.DataFrame({
        "RUN": RUNS[idx],
        "FECHA": pd.to_datetime("2024-01-01") + pd.to_timedelta(rng.integers(0, 970, N_FORM), "D"),
        "INSTR": rng.choice(["MEDICO", "PSICOLOGO(A)", "TRABAJADOR(A) SOCIAL"], N_FORM,
                            p=[.5, .3, .2]),
    })
    d["INSTR_n"] = d["INSTR"].map(norm)
    for n in pob.QUESTIONS:
        if n in pob.ESTADOS_TODOS:
            v = rng.choice(["INGRESO", "SEGUIMIENTO", "EGRESO", ""], N_FORM, p=[.1, .2, .05, .65])
        else:
            v = rng.choice(["SI", "NO", ""], N_FORM, p=[.12, .3, .58])
        d[f"q{n}"] = v
        d[f"q{n}_n"] = v
    d.attrs["preguntas_faltantes"] = {}
    return d


def ada():
    idx = rng.choice(N_PERS, N_ATEN)
    actos = ["CONTROL SALUD MENTAL", "CONSULTA DE SALUD MENTAL", "CONTROL PRENATAL",
             "CONTROLES SALUD MENTAL", "CURACION SIMPLE", "CONTROL CRONICO"]
    d = pd.DataFrame({
        "RUN": RUNS[idx],
        "FECHA": pd.to_datetime("2025-07-01") + pd.to_timedelta(rng.integers(0, 430, N_ATEN), "D"),
        "ACT_n": rng.choice(actos, N_ATEN),
        "INSTR_n": rng.choice(["MEDICO", "MATRONA", "PSICOLOGO(A)"], N_ATEN),
        "FORMCLIN": rng.choice(["", "GESTANTE"], N_ATEN, p=[.95, .05]),
    })
    return d


print("armando los frames sinteticos...")
insc, form, d_ada = inscritos(), formulario(), ada()
print(f"  inscritos={len(insc)}  formularios={len(form)} x {len(form.columns)} cols  "
      f"atenciones={len(d_ada)}")


def _quiet(*a, **k):
    pass


# --- 1. cuanto cuesta cada pasada -------------------------------------------
t = time.perf_counter()
P_med = pob.construir_poblacion(insc, form, d_ada, mes=CORTE, log=_quiet, exigir_medico=True)
t1 = time.perf_counter() - t
t = time.perf_counter()
P_todos = pob.construir_poblacion(insc, form, d_ada, mes=CORTE, log=_quiet, exigir_medico=False)
t2 = time.perf_counter() - t
print(f"\n1a pasada (P6)            = {t1:.2f} s")
print(f"2a pasada (Brecha_Medico) = {t2:.2f} s   <- hallazgo 5: el {t2/(t1+t2):.0%} del total")
print(f"TOTAL familia poblacion   = {t1+t2:.2f} s")

# --- 2. donde se va el tiempo DENTRO de una pasada ---------------------------
pr = cProfile.Profile()
pr.enable()
pob.construir_poblacion(insc, form, d_ada, mes=CORTE, log=_quiet)
pr.disable()
s = io.StringIO()
pstats.Stats(pr, stream=s).sort_stats("tottime").print_stats(18)
texto = s.getvalue()
print("\n--- tottime dentro de UNA pasada -------------------------------------")
for linea in texto.splitlines()[:28]:
    print(linea[:155])
