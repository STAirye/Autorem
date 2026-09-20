import sys, types, os
from pathlib import Path
sys.path.insert(0, r"E:\git\Autorem")
# --- stub customtkinter (not installed) ---
class _D:
    def __init__(self, *a, **k): pass
    def __getattr__(self, n): return lambda *a, **k: None
ctk = types.ModuleType("customtkinter")
ctk.__getattr__ = lambda name: _D
sys.modules["customtkinter"] = ctk
import gui.app as app
import gui.paginas.sm as smpage

calls = []
class MB:
    def showwarning(self, *a): calls.append(("warn",) + a)
    def showerror(self, *a): calls.append(("err",) + a)
app.messagebox = MB()

S = Path(sys.argv[1])
psc = S / "exports" / "psc_iris.xlsx"; psc.write_bytes(b"x")   # dummy, only its folder matters
getters = {
    "ada": lambda: [], "grupal": lambda: [], "inscritos": lambda: [],
    "multiprofesional": lambda: [], "maestro": lambda: [],
    "a03": lambda: {"incluir": True, "instrumentos": {"PSC": str(psc)}, "est_ruta": ""},
}
os.chdir(r"E:\git\Autorem")  # e.g. `python -m gui.app` launched from the repo
ctx = app._resolver_ctx(smpage.PANTALLA, getters, lambda: (2026, 8), lambda: "")
print("messagebox calls:", calls)
print("ctx['carpeta'] =", ctx["carpeta"])
print("questionnaire folder =", psc.parent)
print("A03 output would be:", ctx["carpeta"] / "REM_A03_D3_2026_08.xlsx")
