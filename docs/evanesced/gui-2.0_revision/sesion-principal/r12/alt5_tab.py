import sys
from pathlib import Path
REPO = Path(r"E:\git\Autorem")
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "tests"))
import _aislar_cache  # noqa
import tkinter as tk
import customtkinter as ctk
from gui.app import App
app = App(); app.geometry("1180x820")
app.mostrar("a23_respiratorio"); app.update()
app.mostrar("sm_actividades"); app.update()
oculta, visible = app._frames["a23_respiratorio"], app._frames["sm_actividades"]
def dentro(w, f):
    s = str(w); return s.startswith(str(f._parent_frame))
# primer Entry de la pagina VISIBLE
def entries(f):
    out = []
    def walk(w):
        for h in w.winfo_children():
            if isinstance(h, tk.Entry): out.append(h)
            walk(h)
    walk(f._parent_frame); return out
e0 = entries(visible)[0]
w, pasos, en_oculta = e0, 0, 0
for _ in range(80):
    w = w.tk_focusNext()
    if w is None or w == e0: break
    pasos += 1
    if dentro(w, oculta): en_oculta += 1
print(f"Tab desde la pagina visible (SM): {pasos} paradas, {en_oculta} en la pagina OCULTA (A23)")
print("A23 mapeada/visible?:", bool(oculta._parent_frame.winfo_ismapped()), bool(oculta._parent_frame.winfo_viewable()))
app.destroy()
