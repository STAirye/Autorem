import sys, types, os, tempfile, pathlib
sys.path.insert(0, r"E:\git\Autorem")
# stub customtkinter (not installed)
ctk = types.ModuleType("customtkinter")
class _Any:
    def __init__(self, *a, **k): pass
    def __getattr__(self, n): return _Any()
    def __call__(self, *a, **k): return _Any()
for n in ("CTk","CTkFrame","CTkButton","CTkLabel","CTkScrollableFrame","CTkSwitch","CTkFont",
          "StringVar","BooleanVar","CTkCheckBox","CTkEntry","CTkTextbox","CTkToplevel",
          "CTkOptionMenu","CTkTabview","CTkRadioButton"):
    setattr(ctk, n, type(n, (_Any,), {}))
ctk.get_appearance_mode = lambda: "Light"
ctk.set_appearance_mode = lambda m: None
sys.modules["customtkinter"] = ctk

import gui.app as app
import gui.paginas.sm as smpage

class MB:
    def __getattr__(self, n):
        def f(*a, **k):
            print("MESSAGEBOX", n, a)
            return None
        return f
app.messagebox = MB()

# fake questionnaire file in a "OneDrive-like" folder
d = pathlib.Path(tempfile.mkdtemp(prefix="exports_"))
q = d / "goldberg.xlsx"; q.write_bytes(b"x")

getters = {
    "ada": lambda: [], "grupal": lambda: [], "inscritos": lambda: [],
    "multiprofesional": lambda: [], "maestro": lambda: [],
    "a03": lambda: {"incluir": True, "instrumentos": {"GHQ-12": str(q)}, "est_ruta": ""},
}
ctx = app._resolver_ctx(smpage.PANTALLA, getters, lambda: (2026, 8), lambda: "")
print("cwd       :", os.getcwd())
print("input dir :", d)
print("ctx carpeta:", ctx and ctx.get("carpeta"))
