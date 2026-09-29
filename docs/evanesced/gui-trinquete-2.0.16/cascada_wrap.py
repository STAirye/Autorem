"""Experimento 2: cuanto de la cascada de layout la dispara `etiqueta_envolvente`
(cada label re-ajusta su wraplength en CADA <Configure> del padre, y al cambiar de
alto vuelve a disparar <Configure>)? Variantes:
  hoy        : tal cual
  sin_wrap   : la etiqueta NO se ata a <Configure> (wraplength fijo) -- cota inferior
  wrap_igual : se ata, pero solo reconfigura si el wraplength CAMBIA de verdad
Cuenta ademas cuantas veces corre el lambda y cuantos _update_dimensions_event hay."""
import sys, time, statistics
sys.path.insert(0, r"C:\Users\simon.tobar\Dr tobar\AutoREM")
import tests._aislar_cache  # noqa: F401
import customtkinter as ctk
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass
from gui import widgets
from gui.app import App

ORIG_ET = widgets.etiqueta_envolvente
ORIG_UD = CTkBaseClass._update_dimensions_event
cont = {"lambda": 0, "dim": 0}


def et_sin_wrap(parent, text, **kw):
    return ctk.CTkLabel(parent, text=text, justify="left", anchor="w", **kw)


def et_wrap_igual(parent, text, **kw):
    lbl = ctk.CTkLabel(parent, text=text, justify="left", anchor="w", **kw)
    ultimo = [None]

    def ajustar(e):
        cont["lambda"] += 1
        w = max(e.width - 20, 50)
        if w != ultimo[0]:
            ultimo[0] = w
            lbl.configure(wraplength=lbl._reverse_widget_scaling(w))
    parent.bind("<Configure>", ajustar, add="+")
    return lbl


def et_hoy_contada(parent, text, **kw):
    lbl = ctk.CTkLabel(parent, text=text, justify="left", anchor="w", **kw)

    def ajustar(e):
        cont["lambda"] += 1
        lbl.configure(wraplength=lbl._reverse_widget_scaling(max(e.width - 20, 50)))
    parent.bind("<Configure>", ajustar, add="+")
    return lbl


def ud(self, *a, **k):
    cont["dim"] += 1
    return ORIG_UD(self, *a, **k)


CTkBaseClass._update_dimensions_event = ud
VARIANTES = {"hoy": et_hoy_contada, "sin_wrap": et_sin_wrap, "wrap_igual": et_wrap_igual}


def medir(pid, var):
    widgets.etiqueta_envolvente = VARIANTES[var]
    app = App()
    app.update()
    cont.update(dict.fromkeys(cont, 0))
    t = time.perf_counter()
    app.mostrar(pid)
    app.update_idletasks()
    dt = time.perf_counter() - t
    n = dict(cont)
    app.destroy()
    widgets.etiqueta_envolvente = ORIG_ET
    return dt, n


for pid in ("acerca_de", "sm_actividades"):
    for var in VARIANTES:
        r = [medir(pid, var) for _ in range(3)]
        print(f"{pid:<15} {var:<11} mediana {statistics.median(x for x, _ in r):5.2f}s  "
              f"lambda={r[-1][1]['lambda']:>5}  dim_events={r[-1][1]['dim']:>5}", flush=True)
