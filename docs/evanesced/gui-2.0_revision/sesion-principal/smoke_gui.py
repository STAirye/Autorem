"""Smoke test HEADLESS-ish: construye la App real y TODAS sus paginas, corre un
par de ciclos de eventos y cierra. No reemplaza mirar la ventana, pero atrapa los
errores de construccion (pack/after/atributos) que los tests de registro no ven."""
import sys, traceback
sys.path.insert(0, "E:/git/Autorem")

import customtkinter as ctk
from gui.app import App, PAGINAS_ESPECIALES

fallos = []
app = App(ruta_inicial="refs_tablas/Formularios_RAYEN_csm_IRis.xlsx")
app.geometry("1180x820")
ids = [p["id"] for p in app.registro] + [i for i, _t, _f in PAGINAS_ESPECIALES]
for pid in ids:
    try:
        app.mostrar(pid)
        for _ in range(12):
            app.update()
        print("OK   pagina", pid)
    except Exception as e:
        fallos.append((pid, e))
        print("FAIL pagina", pid, "->", type(e).__name__, e)
        traceback.print_exc()

# A05: la ruta precargada tiene que haber disparado la deteccion (hilo) y dejar
# categoria='iris'. Se le dan ciclos de evento para que el after(0) corra.
app.mostrar("a05")
for _ in range(40):
    app.update()
print("registro:", len(app.registro), "pantallas |", len(ids), "paginas visitadas")
app.destroy()
sys.exit(1 if fallos else 0)
