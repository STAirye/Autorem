# -*- coding: utf-8 -*-
"""Que se lleva los ~7 s de construir gui/paginas/sm.py: widgets de Tk o trabajo puro.
Decide si la precarga puede ir a un worker (trabajo puro) o tiene que ir por after()
en el hilo de la GUI (widgets)."""
import sys, cProfile, pstats, io, time
sys.path.insert(0, r"E:\git\Autorem"); sys.path.insert(0, r"E:\git\Autorem\tests")
import _aislar_cache  # noqa
from gui.app import App

app = App(); app.update()
pr = cProfile.Profile(); pr.enable()
t0 = time.perf_counter()
app.mostrar("sm_actividades"); app.update()
dt = time.perf_counter() - t0
pr.disable()
print(f"construir sm_actividades: {dt*1000:.0f} ms\n")
s = io.StringIO()
pstats.Stats(pr, stream=s).sort_stats("cumulative").print_stats(28)
for linea in s.getvalue().splitlines():
    if "/" in linea or "{" in linea or "ncalls" in linea:
        print(linea[:150])
app.destroy()
