# -*- coding: utf-8 -*-
"""MERGE 2.0 - por que `auditar_atenciones` (main 1.9.16) hay que adaptarlo a la forma
canonica de `cargar_atenciones` (rama, ronda 12), y no al reves.

`_mask_control_sm` usa `contiene_todos(A, "controles", "salud mental por")`, o sea DOS
tokens buscados por separado en la celda. Hoy en main corre por FILA, y en el Monitoreo
admin cada fila es UNA actividad, asi que los dos tokens tienen que estar en la misma
actividad. Tras el merge la celda ACT trae TODAS las actividades de la atencion unidas
por SEP_ACTIVIDADES, y los dos tokens pueden venir de actividades DISTINTAS: falso
positivo callado, y la atencion cae en Ctrl_sin_Formulario sin ser un Control SM.

Correr desde la raiz del repo: python <este archivo>
"""
import sys, pathlib
R = pathlib.Path(r"E:\git\Autorem")
sys.path.insert(0, str(R)); sys.path.insert(0, str(R / "tests"))
import _aislar_cache  # noqa  el cache real del autor NO se toca
import pandas as pd
from programas.rem_utils import contiene_todos, SEP_ACTIVIDADES, norm


def mask_control_sm(A):
    """Copia literal de main:rem_sm_trabajo_perdido._mask_control_sm (1.9.16)."""
    return (contiene_todos(A, "controles salud mental")
            | contiene_todos(A, "controles", "salud mental por"))


# Dos actividades de la MISMA atencion; NINGUNA es Control de Salud Mental.
a = "CONTROLES DE PIE DIABETICO"                 # aporta el token "controles"
b = "CONSULTA DE SALUD MENTAL POR PSICOLOGO"     # aporta el token "salud mental por"
unida = SEP_ACTIVIDADES.join([a, b])

s = pd.Series([a, b, unida]).map(norm)
m = mask_control_sm(s)
print("  fila A sola          :", m[0], "  <-", a)
print("  fila B sola          :", m[1], "  <-", b)
print("  MISMA ATENCION unida :", m[2], "  <-", unida)
assert not m[0] and not m[1], "ninguna de las dos es Control SM por separado"
assert m[2], "y unidas, la mascara SI dispara -> falso positivo"
print("\n  => el arreglo va en el CONSUMIDOR: partir la celda por SEP_ACTIVIDADES y")
print("     evaluar la mascara POR ACTIVIDAD (any), como main ya hace en `_tiene_form`")
print("     con FORMULARIOS CLINICOS ('Nunca substring: mental capta el Minimental').")
