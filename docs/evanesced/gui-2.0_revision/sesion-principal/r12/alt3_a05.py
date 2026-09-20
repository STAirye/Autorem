# -*- coding: utf-8 -*-
"""A05 2.0: la categoria/ERROR se cachean por RUTA (string). Mismo nombre, contenido nuevo
(RAYEN baja todo como Formulario_Rayen.xlsx; OneDrive a medio sincronizar, CLAUDE.md 13)."""
import sys, shutil
from pathlib import Path
REPO = Path(r"E:\git\Autorem")
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "tests"))
import _aislar_cache  # noqa
import tempfile
import tkinter.messagebox as mb
import customtkinter as ctk
from contratos_fuentes import Contrato, escribir, plantilla
from gui.paginas import a05
import programas.rem_saludmental as sm
from programas.rem_utils import ArchivoInvalido
TMP = Path(tempfile.mkdtemp(prefix="r12_a05_"))
vistos = []
for f in ("showerror", "showwarning", "showinfo"):
    setattr(mb, f, lambda t, m, _f=f, **k: vistos.append((_f, t, m.split("\n")[0])))
def fx(ref, fila, nombre):
    b, h, p = plantilla(Contrato(id=ref, cubre=(), llamar=None, fila={}, ref=ref))
    return escribir(TMP / nombre, b, h, [fila], p)
iris = fx("Formularios_RAYEN_csm_IRis.xlsx", {"NUMERO TIPO IDENTIFICACION": "11111111-1",
         "AÑO APLICACIÓN FORMULARIO": 45, "SEXO": "Mujer", "FECHA FORMULARIO": "05/08/2026",
         "18.- ¿ TIENE  DEPRESIÓN ?": "SI", "19.- ESTADO": "EGRESO POR ALTA"}, "iris.xlsx")
adm = fx("Formulario_csm_reporte_Administrativo.xlsx", {"RUT": "11111111-1",
         "Edad de registro formulario": "45 años", "Sexo": "Mujer", "Fecha Formulario": "2026/08/05",
         "18.- ¿ Tiene  Depresión ?": "SI", "19.- Estado": "Egreso Alta"}, "adm.xlsx")
P = TMP / "Formulario_Rayen.xlsx"
from autorem import TAREAS
app = ctk.CTk(); app.withdraw()
def bloque():
    frame = ctk.CTkFrame(app)
    pag = type("P", (), {"datos": {}, "root": app, "log": staticmethod(lambda m="": None)})()
    get = a05.bloque_archivo_formato(frame, pag)
    entry = next(w for w in frame.winfo_children() for w in [w] + list(w.winfo_children())
                 if isinstance(w, ctk.CTkEntry))
    entry.insert(0, str(P))
    return get, pag
def ctx(get):
    return {"archivo": get(), "periodo": {"modo": "todo"}, "tareas": [t["id"] for t in TAREAS], "carpeta": str(TMP)}

print("=== A. al elegir, el archivo esta a medio bajar (OneDrive); despues termina ===")
P.write_bytes(b"PK\x03\x04 truncado")        # zip cortado
get, pag = bloque()
print("  deteccion al elegir ->", get()["detectar_ahora"]())
shutil.copy(iris, P)                           # OneDrive termino / 'Guardar como' al mismo nombre
vistos.clear()
r = a05.preparar(ctx(get), pag)
print("  preparar con el archivo YA BUENO ->", r, "| dialogo:", vistos)
vistos.clear(); r = a05.preparar(ctx(get), pag)
print("  2o click en Procesar            ->", r, "| dialogo:", vistos)

print("\n=== B. elegido el IRIS, reemplazado por el Administrativo con el MISMO nombre ===")
shutil.copy(iris, P)
get, pag = bloque()
print("  deteccion al elegir ->", get()["detectar_ahora"]())
shutil.copy(adm, P)
vistos.clear()
r = a05.preparar(ctx(get), pag)
print("  preparar -> perfil:", r and r["perfil"]["id"], "| acuse pedido?:", bool(vistos))
try:
    sm.abrir_validado(P, r["perfil"])
except ArchivoInvalido as e:
    print("  worker ->", e.categoria, "|", str(e).split("\n\n")[1][:70])
app.destroy()
