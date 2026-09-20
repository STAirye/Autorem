import sys
from pathlib import Path
REPO = Path(r"E:\git\Autorem")
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "tests"))
import _aislar_cache  # noqa
import customtkinter as ctk
from gui.app import App
from gui import registro as reg
real = reg.cargar_registro()
def cabeceras(registro):
    app = App(registro=registro); app.withdraw()
    out = []
    def walk(w):
        for h in w.winfo_children():
            if isinstance(h, ctk.CTkButton) and h.cget("text").startswith(("-  ", "+  ")):
                out.append(h.cget("text")[3:])
            walk(h)
    walk(app); app.destroy(); return out
print("real                         :", cabeceras(real))
nueva = dict(real[0], id="sm_infanto", titulo="Infanto-adolescente", programa="Salud Mental Infanto-adolescente")
print("+ programa nuevo 'Salud Mental Infanto-adolescente' (no declarado en ORDEN_PROGRAMAS):")
print("                              ", cabeceras(real + [nueva]))
