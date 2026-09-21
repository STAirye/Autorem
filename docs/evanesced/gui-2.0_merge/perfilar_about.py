# -*- coding: utf-8 -*-
"""Cuanto tarda «Acerca de» y EN QUE: widgets de Tk (no se puede mover de hilo) vs
trabajo puro como leer catalogos (si se puede)."""
import sys, time, cProfile, pstats, io
sys.path.insert(0, r"E:\git\Autorem"); sys.path.insert(0, r"E:\git\Autorem\tests")
import _aislar_cache  # noqa
from gui.app import App

app = App(precargar=False); app.update()
pr = cProfile.Profile(); pr.enable()
t0 = time.perf_counter()
app.mostrar("acerca_de"); app.update()
dt = time.perf_counter() - t0
pr.disable()
print(f"acerca_de: {dt*1000:.0f} ms\n")
st = pstats.Stats(pr); st.sort_stats("tottime")
s = io.StringIO(); st.stream = s; st.print_stats(12)
for l in s.getvalue().splitlines():
    if "tkapp" in l or "catalog" in l or "gzip" in l or "read" in l or "ncalls" in l or "pandas" in l:
        print(l[:140])
app.destroy()
