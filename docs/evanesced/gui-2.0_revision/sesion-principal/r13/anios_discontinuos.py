# -*- coding: utf-8 -*-
"""Que hace poblacion.py con ADA de anios DISCONTINUOS.

Dos escenarios, ambos con el mes reportado = 2016-08:
  A) 2016 + 2015 + 2012  -> el hueco (2013-2014) cae FUERA de toda ventana
  B) 2016 + 2014 + 2012  -> el hueco (2015) cae DENTRO de la ventana de 12 meses
Nada de PII: RUN sinteticos.
"""
import sys, pathlib
R = pathlib.Path(r'E:\git\Autorem')
sys.path.insert(0, str(R)); sys.path.insert(0, str(R / 'tests'))
import _aislar_cache  # noqa  el cache real del autor NO se toca
import pandas as pd
from programas import poblacion as pob

ACT = "CONTROL SALUD MENTAL"   # de ACTIVIDADES_SM_7 (serie ya normalizada)
CORTE = pd.Timestamp("2016-08-31")

def ada(pares):
    """pares = [(run, 'AAAA-MM-DD')]"""
    d = pd.DataFrame({"RUN": [p[0] for p in pares],
                      "FECHA": pd.to_datetime([p[1] for p in pares]),
                      "ACT_n": [ACT] * len(pares)})
    return d

def form(fechas):
    return pd.DataFrame({"RUN": ["1"] * len(fechas),
                         "FECHA": pd.to_datetime(fechas)})

def escenario(nombre, pares):
    print("=" * 72)
    print(nombre)
    d = ada(pares)
    f = form([p[1] for p in pares])
    print("  meses presentes en el ADA:", sorted({str(x)[:7] for x in d['FECHA']}))
    avisos = pob._verificar_cobertura_fechas(f, d, CORTE, log=lambda m: print("  LOG", m))
    print("  avisos de cobertura devueltos:", len(avisos))
    for a in avisos:
        print("    ->", a[0], "|", a[1], "|", a[2][:90])
    a12, r6, r13 = pob._flags_actividad(d, CORTE)
    print("  Activo 12m :", sorted(a12))
    print("  rescate 6m :", sorted(r6))
    print("  rescate 13m:", sorted(r13))

# Cada paciente tiene UNA atencion, en el mes que dice su nombre.
escenario("A) ADA 2016 + 2015 + 2012, corte 2016-08 (hueco 2013-2014, fuera de la ventana)",
          [("run_2016_08", "2016-08-10"),
           ("run_2015_12", "2015-12-10"),
           ("run_2015_09", "2015-09-10"),
           ("run_2012_05", "2012-05-10")])

escenario("B) ADA 2016 + 2014 + 2012, corte 2016-08 (hueco 2015 = DENTRO de los 12 meses)",
          [("run_2016_08", "2016-08-10"),
           ("run_2016_03", "2016-03-10"),
           ("run_2014_11", "2014-11-10"),
           ("run_2012_05", "2012-05-10")])

print("=" * 72)
print("Para comparar: el MISMO escenario B pero con el 2015 completo cargado")
escenario("C) ADA 2016 + 2015 + 2014 + 2012 (sin hueco)",
          [("run_2016_08", "2016-08-10"),
           ("run_2016_03", "2016-03-10"),
           ("run_2015_10", "2015-10-10"),
           ("run_2014_11", "2014-11-10"),
           ("run_2012_05", "2012-05-10")])
