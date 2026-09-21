# -*- coding: utf-8 -*-
"""Mide la precarga con un mainloop DE VERDAD, instrumentando cada tick: cuanto tarda
cada pagina y cuanto queda la ventana bloqueada de corrido."""
import sys, time
sys.path.insert(0, r"E:\git\Autorem"); sys.path.insert(0, r"E:\git\Autorem\tests")
import _aislar_cache  # noqa
import gui.app as A

eventos = []
orig = A.App._construir_pagina
def espia(self, pantalla):
    t = time.perf_counter()
    r = orig(self, pantalla)
    eventos.append((pantalla["id"], time.perf_counter() - t))
    return r
A.App._construir_pagina = espia

T0 = time.perf_counter()
app = A.App()
app.after(50, lambda: eventos.append(("__ventana_visible__", time.perf_counter() - T0)))
def vigilar():
    if app._tick_precarga is None and len(eventos) > 1:
        eventos.append(("__fin__", time.perf_counter() - T0))
        app._al_cerrar()
    else:
        app.after(50, vigilar)
app.after(50, vigilar)
app.mainloop()

print(f"{'pagina':<24} {'bloqueo':>9}")
for nombre, dt in eventos:
    if nombre.startswith("__"):
        print(f"{nombre:<24} {dt:>8.2f} s  (desde el arranque)")
    else:
        print(f"{nombre:<24} {dt*1000:>8.0f} ms de bloqueo")
