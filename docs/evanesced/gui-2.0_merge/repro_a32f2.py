# -*- coding: utf-8 -*-
"""MERGE 2.0 - la MISMA clase de falso positivo que el TP, pero en una casilla que SI
tributa al REM: A32-F2 de rem_sm_actividades.

`ctrl_rem = _all(A, "controles", "salud mental por")` son DOS tokens sueltos, y
`llam = _all(A,"llamada") & ~_all(A,"videollamada")` es otro AND sobre la misma celda.
Sobre la forma canonica (ronda 12) la celda trae TODAS las actividades de la atencion.
"""
import sys, pathlib
R = pathlib.Path(r"E:\git\Autorem")
sys.path.insert(0, str(R)); sys.path.insert(0, str(R / "tests"))
import _aislar_cache  # noqa
import pandas as pd
from programas.rem_utils import SEP_ACTIVIDADES, norm, contiene_todos as _all

def ctrl_rem(A):
    return _all(A, "controles", "salud mental por")
def llam(A):
    return _all(A, "llamada") & ~_all(A, "videollamada")

casos = {
 "A32F2 de dos actividades ajenas": ["Controles de pie diabetico",
                                     "Consulta de salud mental por psicologo",
                                     "Consulta de morbilidad por llamada telefonica"],
 "A32F2 real (una sola actividad)": ["Controles de Salud Mental por llamadas telefonicas"],
 "videollamada + otra con llamada": ["Controles de Salud Mental por videollamadas",
                                     "Consulta de morbilidad por llamada telefonica"],
}
for nombre, acts in casos.items():
    unida = norm(SEP_ACTIVIDADES.join(acts))
    s = pd.Series([unida])
    print(f"{nombre}:")
    for a in acts:
        print(f"    - {a}")
    print(f"    A32F2 (ctrl_rem & llam) = {bool((ctrl_rem(s) & llam(s))[0])}")

print("\n-- falso NEGATIVO --")
acts = ["Controles de Salud Mental por llamadas telefonicas",     # A32F2-Llamadas real
        "Acciones remotas de salud mental por videollamada"]      # hermana con 'videollamada'
s = pd.Series([norm(SEP_ACTIVIDADES.join(acts))])
print("    ", acts)
print("     A32F2-Llamadas (ctrl_rem & llam) =", bool((ctrl_rem(s) & llam(s))[0]), "(deberia ser True)")
