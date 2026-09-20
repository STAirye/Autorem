import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import stubctk
import gui.app as app
from gui.paginas import sm, a23, poblacion
class MB:
    def showwarning(self, *a): print("WARN", a)
    def showerror(self, *a): print("ERR", a)
app.messagebox = MB()
q = r"C:\Users\Simon\OneDrive\exports\goldberg_agosto.xlsx"
getters = {
  "ada": lambda: [], "grupal": lambda: [], "inscritos": lambda: [], "multiprofesional": lambda: [], "maestro": lambda: [],
  "a03": lambda: {"incluir": True, "instrumentos": {"GHQ-12": q}, "est_ruta": ""},
}
ctx = app._resolver_ctx(sm.PANTALLA, getters, lambda: (2026, 13), lambda: "")
print("SM solo-cuestionarios ctx:", ctx)
print("cwd:", os.getcwd())
