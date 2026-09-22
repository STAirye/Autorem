"""Equivalencia de la 2a pasada de Brecha_Medico: la version vieja (armar
`construir_poblacion` COMPLETA con exigir_medico=False y filtrar su base) contra la
nueva (`runs_ingresados_sin_filtro_medico` + Estado/Activo12m leidos del P_med).

Lo que hay que probar es la premisa del atajo: que `Estado` y `¿Activo 12m?` salen
IDENTICOS en las dos pasadas, y que el `¿Ingresado?` sin filtro medico tambien.
Se compara el SET de RUN de la brecha, que es lo que consume la hoja.
"""
import sys, time
sys.path.insert(0, r"C:\Users\simon.tobar\Dr tobar\AutoREM")
import numpy as np
import pandas as pd
import programas.poblacion as pob
from programas.rem_utils import norm

sys.path.insert(0, r"C:\Users\SIMON~1.TOB\AppData\Local\Temp\claude"
                   r"\C--Users-simon-tobar-Dr-tobar-AutoREM"
                   r"\c14d7a11-6c40-494d-a18a-193d2271c37e\scratchpad")
from perfil_poblacion import insc, form, d_ada, CORTE   # reusa los frames sinteticos


def _quiet(*a, **k):
    pass


# ---- la corrida normal, que las dos versiones comparten --------------------
t = time.perf_counter()
P_med = pob.construir_poblacion(insc, form, d_ada, mes=CORTE, log=_quiet)
t_med = time.perf_counter() - t


def _base(P):
    return ((P["Estado"].map(norm) == "ACTIVO") & (P["¿Activo 12m?"] == "SI")
            & (P["¿Ingresado?"] == "SI"))


# ---- VIEJA -----------------------------------------------------------------
t = time.perf_counter()
P_todos = pob.construir_poblacion(insc, form, d_ada, mes=CORTE, log=_quiet,
                                  exigir_medico=False)
runs_med_v = set(P_med.loc[_base(P_med), "Número"])
runs_todos_v = set(P_todos.loc[_base(P_todos), "Número"])
brecha_vieja = runs_todos_v - runs_med_v
t_vieja = time.perf_counter() - t

# ---- NUEVA -----------------------------------------------------------------
t = time.perf_counter()
base_comun = (P_med["Estado"].map(norm) == "ACTIVO") & (P_med["¿Activo 12m?"] == "SI")
runs_med_n = set(P_med.loc[base_comun & (P_med["¿Ingresado?"] == "SI"), "Número"])
runs_todos_n = (set(P_med.loc[base_comun, "Número"])
                & pob.runs_ingresados_sin_filtro_medico(P_med, form, mes=CORTE, log=_quiet))
brecha_nueva = runs_todos_n - runs_med_n
t_nueva = time.perf_counter() - t

print(f"1a pasada (compartida)      = {t_med:.2f} s")
print(f"2a pasada VIEJA (tabla)     = {t_vieja:.2f} s")
print(f"2a pasada NUEVA (solo cols) = {t_nueva:.2f} s   ({t_vieja/t_nueva:.1f}x)")
print(f"familia poblacion: {t_med+t_vieja:.2f} s -> {t_med+t_nueva:.2f} s")
print()
print(f"brecha vieja = {len(brecha_vieja)} RUN | nueva = {len(brecha_nueva)} RUN")
print("MISMO SET:", brecha_vieja == brecha_nueva)
if brecha_vieja != brecha_nueva:
    print("  solo en la vieja:", sorted(brecha_vieja - brecha_nueva)[:10])
    print("  solo en la nueva:", sorted(brecha_nueva - brecha_vieja)[:10])

# la premisa, explicita: Estado y Activo 12m no dependen del toggle
print("\npremisa del atajo:")
for c in ("Estado", "¿Activo 12m?", "Sexo", "Edad", "¿Originario o Migrante?",
          "PROTECCION NIÑEZ", "¿Embarazada?", "Madre <5 años", "¿Última atención hace 6m?"):
    igual = P_med[c].astype(str).equals(P_todos[c].astype(str))
    print(f"  {c:28s} identico entre pasadas: {igual}")
# y lo que SI cambia
cambian = [c for c in P_med.columns
           if not P_med[c].astype(str).equals(P_todos[c].astype(str))]
print(f"\ncolumnas que SI cambian con el toggle ({len(cambian)}): {cambian}")
