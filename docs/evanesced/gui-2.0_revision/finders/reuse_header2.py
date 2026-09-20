import sys, types
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

from gui.paginas import sm as smpage
from programas.rem_utils import leer_xlsx, cargar_atenciones, ArchivoInvalido
from programas import formatos
import modulos.rem_sm_actividades as smact
import openpyxl

REFS = r"E:\git\Autorem\refs_tablas"
mon = REFS + r"\Monitoreo_de_Actividades_anonimizado.xlsx"
ada = REFS + r"\ATENCIONESDIAGNOSTICOSACTIVIDADES_iris.xlsx"
gru = REFS + r"\Atenciones_Grupales_iris.xlsx"

ws = openpyxl.load_workbook(mon, read_only=True, data_only=True).active
rows = [list(r) for r in ws.iter_rows(values_only=True, max_row=5)]
for i, r in enumerate(rows):
    print(i, sum(v not in (None, "") for v in r), [v for v in r if v not in (None, "")][:8])

def slot(path, espera):
    prev = formatos.parece_reporte(smpage._header_rapido(path))
    banner = "oculto" if (prev is None or prev == espera) else f"ROJO: parece {prev}"
    try:
        if espera == "grupal":
            smact.cargar_grupal(path, log=lambda *a: None)
        else:
            cargar_atenciones(path, log=lambda *a: None)
        real = "carga OK"
    except ArchivoInvalido as e:
        real = f"ArchivoInvalido({e.categoria})"
    except Exception as e:
        real = f"{type(e).__name__}: {e}"
    print(f"{path.split(chr(92))[-1]:45s} slot={espera:7s} preview={banner:22s} procesar={real}")

for p in (ada, gru, mon):
    for e in ("ada", "grupal"):
        slot(p, e)
