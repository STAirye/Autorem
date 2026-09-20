import sys; sys.path.insert(0, r"E:\git\Autorem"); sys.path.insert(0, r"E:\git\Autorem\tests")
import _aislar_cache
from gui.app import App
from tkinter import ttk
import customtkinter as ctk
app = App(); app.mostrar("a05"); app.update()
f = app._frames["a05"]
def walk(w):
    yield w
    for c in w.winfo_children(): yield from walk(c)
radios = [w for w in walk(f) if isinstance(w, ctk.CTkRadioButton)]
spins = [w for w in walk(f) if isinstance(w, ttk.Spinbox)]
r = radios[1]
print("radio", r.winfo_rootx(), r.winfo_rooty(), r.winfo_height())
for s in spins: print("spin", s.winfo_rootx(), s.winfo_rooty(), str(s.cget("state")))
radios[1].invoke(); app.update()
print([str(s.cget("state")) for s in spins])
app.destroy()
