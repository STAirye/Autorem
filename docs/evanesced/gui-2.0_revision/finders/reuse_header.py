import sys, types
sys.path.insert(0, r"E:\git\Autorem")
# stub customtkinter so gui modules import
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
from programas.rem_utils import leer_xlsx
from programas import formatos

REFS = r"E:\git\Autorem\refs_tablas"
files = ["ATENCIONESDIAGNOSTICOSACTIVIDADES_iris.xlsx", "Atenciones_Grupales_iris.xlsx",
         "Monitoreo_de_Actividades_anonimizado.xlsx", "Informe_Inscritos__Adscritos_heads.xlsx",
         "Formularios_RAYEN_csm_IRis.xlsx", "Formulario_csm_reporte_Administrativo.xlsx"]
for f in files:
    p = REFS + "\\" + f
    hr = smpage._header_rapido(p)
    lx = leer_xlsx(p)[0]
    lg = leer_xlsx(p, ancla=["ACTIVIDADES", "FECHA ATENCION"])[0]
    print(f)
    print("  _header_rapido == leer_xlsx(no ancla):", hr == lx,
          "| == leer_xlsx(ancla grupal):", hr == lg)
    print("  parece_reporte(_header_rapido) =", formatos.parece_reporte(hr),
          "| parece_reporte(leer_xlsx) =", formatos.parece_reporte(lx),
          "| parece_reporte(leer_xlsx ancla grupal) =", formatos.parece_reporte(lg))
