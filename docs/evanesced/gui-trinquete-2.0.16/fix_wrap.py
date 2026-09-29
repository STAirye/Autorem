"""Experimento 4: el arreglo candidato -- crear la etiqueta con un wraplength INICIAL
chico para que su ancho natural (el texto sin partir) no empuje al padre. Verifica que
el estado FINAL sea identico al de hoy: wraplength de cada etiqueta tras construir, y
tras agrandar/achicar la ventana. A escala 1.0 y 1.5. Mide tiempo y <Configure>."""
import sys, time
sys.path.insert(0, r"C:\Users\simon.tobar\Dr tobar\AutoREM")
import tests._aislar_cache  # noqa: F401
import customtkinter as ctk
from gui import widgets
from gui.app import App

etiquetas = []
cont = [0]


def fabrica(inicial):
    def et(parent, text, **kw):
        extra = {} if inicial is None else {"wraplength": inicial}
        lbl = ctk.CTkLabel(parent, text=text, justify="left", anchor="w", **extra, **kw)

        def ajustar(e):
            cont[0] += 1
            lbl.configure(wraplength=lbl._reverse_widget_scaling(max(e.width - 20, 50)))
        parent.bind("<Configure>", ajustar, add="+")
        etiquetas.append(lbl)
        return lbl
    return et


def estado():
    return [(l.cget("text")[:12], l.cget("wraplength")) for l in etiquetas]


def correr(pid, inicial, escala):
    ctk.set_widget_scaling(escala)
    widgets.etiqueta_envolvente = fabrica(inicial)
    etiquetas.clear()
    app = App()
    app.geometry("1180x800")
    app.update()
    cont[0] = 0
    t = time.perf_counter()
    app.mostrar(pid)
    app.update_idletasks()
    app.update()
    dt = time.perf_counter() - t
    n = cont[0]
    e0 = estado()
    app.geometry("1500x800"); app.update(); e1 = estado()
    app.geometry("800x800"); app.update(); e2 = estado()
    app.destroy()
    return dt, n, (e0, e1, e2)


for escala in (1.0,):
    for pid in ("sm_actividades", "a05"):
        base = correr(pid, None, escala)
        print(f"[{escala}] {pid:<16} hoy       {base[0]:5.2f}s configure={base[1]:>4}", flush=True)
        for ini in (1, 300):
            r = correr(pid, ini, escala)
            igual = ["=" if a == b else "DISTINTO" for a, b in zip(base[2], r[2])]
            print(f"[{escala}] {pid:<16} ini={ini:<5} {r[0]:5.2f}s configure={r[1]:>4}  "
                  f"final/ancha/angosta: {igual}", flush=True)
            if "DISTINTO" in igual:
                for fase, a, b in zip(("final", "ancha", "angosta"), base[2], r[2]):
                    for i, (x, y) in enumerate(zip(a, b)):
                        if x != y:
                            print(f"     {fase:<8} #{i} hoy={x}  fix={y}")
