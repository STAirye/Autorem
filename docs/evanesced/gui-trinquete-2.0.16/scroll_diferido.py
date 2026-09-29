"""Experimento: si CTkScrollbar.set NO redibuja (y no hace update_idletasks) mientras
se construye la pagina, y se aplica UNA vez al final, cuanto baja? Mide pared de
mostrar(pid) para acerca_de, sm_actividades e inicio, con y sin el diferido."""
import sys, time, statistics
sys.path.insert(0, r"C:\Users\simon.tobar\Dr tobar\AutoREM")
import tests._aislar_cache  # noqa: F401
import customtkinter as ctk
from gui.app import App

ORIG = ctk.CTkScrollbar.set


def medir(pid, diferir):
    app = App()
    app.update()
    pend = {}
    if diferir:
        ctk.CTkScrollbar.set = lambda self, a, b: pend.__setitem__(self, (a, b))
    t = time.perf_counter()
    try:
        app.mostrar(pid)
    finally:
        ctk.CTkScrollbar.set = ORIG
    for sb, (a, b) in pend.items():
        sb.set(a, b)
    app.update_idletasks()
    dt = time.perf_counter() - t
    app.destroy()
    return dt


for pid in ("acerca_de", "sm_actividades", "inicio"):
    for dif in (False, True):
        v = [medir(pid, dif) for _ in range(3)]
        print(f"{pid:<16} {'diferido' if dif else 'hoy     '}  mediana {statistics.median(v):5.2f}s  "
              f"({', '.join(f'{x:.2f}' for x in v)})", flush=True)
