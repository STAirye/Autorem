"""Bloqueo de construir cada pagina (App.mostrar, ventana 1180x820), mediana de 3 Apps
nuevas, con el codigo tal como esta en el arbol. Para la tabla del CLAUDE.md s12."""
import sys, time, statistics
sys.path.insert(0, r"C:\Users\simon.tobar\Dr tobar\AutoREM")
import tests._aislar_cache  # noqa: F401
from gui.app import App

PAGINAS = ("acerca_de", "sm_actividades", "a23_respiratorio", "a05", "sp_p6_poblacion", "inicio")


def una(pid):
    app = App()
    app.geometry("1180x820")
    app.update()
    t = time.perf_counter()
    app.mostrar(pid)
    app.update_idletasks()
    dt = time.perf_counter() - t
    app.destroy()
    return dt * 1000


for pid in PAGINAS:
    v = [una(pid) for _ in range(3)]
    print(f"{pid:<18} {statistics.median(v):6.0f} ms   ({', '.join(f'{x:.0f}' for x in v)})", flush=True)
