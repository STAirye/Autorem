import sys, types, os
sys.path.insert(0, r"E:\git\Autorem")
ctk = types.ModuleType("customtkinter")
class _Any:
    def __init__(self, *a, **k): pass
    def __getattr__(self, n): return _Any()
    def __call__(self, *a, **k): return _Any()
for name in ("CTk", "CTkFrame", "CTkLabel", "CTkButton", "CTkEntry", "CTkScrollableFrame",
             "CTkCheckBox", "CTkRadioButton", "CTkToplevel", "CTkTextbox", "CTkTabview",
             "CTkOptionMenu", "CTkSwitch", "CTkFont", "StringVar", "BooleanVar"):
    setattr(ctk, name, _Any)
sys.modules["customtkinter"] = ctk

import tkinter
mb = types.ModuleType("tkinter.messagebox")
calls = []
mb.showerror = lambda t, m: calls.append(("showerror", t, m[:90]))
mb.showwarning = lambda t, m: calls.append(("showwarning", t, m[:90]))
mb.showinfo = lambda t, m: calls.append(("showinfo", t, m[:90]))
sys.modules["tkinter.messagebox"] = mb
tkinter.messagebox = mb

import openpyxl
import programas.rem_saludmental as sm
from gui import runner
from gui.paginas import a05

SCR = r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\648a107e-f033-4d56-a55d-a415a58f003e\scratchpad"
fake = os.path.join(SCR, "Formulario_Rayen_html.xlsx")
with open(fake, "w", encoding="utf-8") as fh:
    fh.write("<html><body><table><tr><td>RUT</td></tr></table></body></html>")

# what the A05 preview thread computes (verbatim logic from a05._detectar.trabajo)
try:
    wb = openpyxl.load_workbook(fake, read_only=True, data_only=True)
    categoria = sm.detectar_formato(wb.active)
    wb.close()
except Exception as e:
    print("preview exception:", type(e).__name__, "| runner.es_error_formato ->", runner.es_error_formato(e))
    categoria = "error_lectura"

ctx = {"archivo": {"ruta": fake, "categoria": categoria, "acuse": False},
       "periodo": {"modo": "todo"}, "tareas": ["a05_o_egresos"], "carpeta": ""}
print("preparar ->", a05.preparar(ctx, None))
print("dialogs:", calls)

# what the old path (_correr_tareas -> abrir_validado) raises for the same file
try:
    sm.abrir_validado(fake, sm.PERFIL_IRIS)
except Exception as e:
    print("abrir_validado exception:", type(e).__name__, "| es_error_formato ->", runner.es_error_formato(e))
