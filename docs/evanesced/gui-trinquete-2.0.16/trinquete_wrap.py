"""Experimento 3: que anchos (e.width) ve el <Configure> de cada etiqueta_envolvente
de acerca_de, en orden? Si baja de a 20 px, es un trinquete: el label pide ancho =
wraplength = ancho_padre - 20, el padre se encoge a lo que piden sus hijos, y otra vuelta."""
import sys, collections
sys.path.insert(0, r"C:\Users\simon.tobar\Dr tobar\AutoREM")
import tests._aislar_cache  # noqa: F401
import customtkinter as ctk
from gui import widgets
from gui.app import App

seq = collections.defaultdict(list)


def et(parent, text, **kw):
    lbl = ctk.CTkLabel(parent, text=text, justify="left", anchor="w", **kw)
    clave = f"{text[:25]!r}"

    def ajustar(e):
        seq[clave].append(e.width)
        lbl.configure(wraplength=lbl._reverse_widget_scaling(max(e.width - 20, 50)))
    parent.bind("<Configure>", ajustar, add="+")
    return lbl


widgets.etiqueta_envolvente = et
app = App()
app.update()
print("ancho ventana:", app.winfo_width(), " escala:", ctk.ScalingTracker.get_widget_scaling(app))
app.mostrar("acerca_de")
app.update_idletasks()
for k, v in seq.items():
    dif = collections.Counter(b - a for a, b in zip(v, v[1:]))
    print(f"{k:<30} n={len(v):>4}  primeros={v[:8]}  ultimos={v[-4:]}  pasos={dict(dif.most_common(4))}")
app.destroy()
