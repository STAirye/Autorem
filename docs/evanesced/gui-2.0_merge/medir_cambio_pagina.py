# -*- coding: utf-8 -*-
"""Cuanto tarda cambiar de pagina en la GUI 2.0, separando la PRIMERA visita
(construye la pagina: el router es perezoso) de las siguientes (solo grid/grid_remove).
Correr desde la raiz del repo."""
import sys, time, pathlib
R = pathlib.Path(__file__).resolve()
sys.path.insert(0, r"E:\git\Autorem"); sys.path.insert(0, r"E:\git\Autorem\tests")
import _aislar_cache  # noqa
from gui.app import App
from gui.registro import cargar_registro

app = App()
app.update()
ids = [p["id"] for p in cargar_registro()] + ["inicio", "about"]
print(f"{'pagina':<24} {'1a visita':>10} {'2a':>8} {'3a':>8}")
for pid in ids:
    ts = []
    for i in range(3):
        t0 = time.perf_counter()
        app.mostrar(pid)
        app.update()
        ts.append(time.perf_counter() - t0)
        if i == 0:
            app.mostrar("inicio"); app.update()   # salir y volver
    print(f"{pid:<24} {ts[0]*1000:>8.0f}ms {ts[1]*1000:>6.0f}ms {ts[2]*1000:>6.0f}ms")
app.destroy()
