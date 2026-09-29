"""Por que `acerca_de` tarda ~7 s en construirse? Hipotesis del autor: lee archivos.
1) tiempo de pared de App.mostrar("acerca_de"), 3 veces en procesos... (misma App: la
   2a vez ya esta construida, asi que se mide una App nueva por corrida);
2) cProfile: tottime por origen (Tk / I/O de archivos / resto) + cuantas llamadas a
   Tk hace cada bloque de about.py."""
import sys, time, cProfile, pstats, collections
sys.path.insert(0, r"C:\Users\simon.tobar\Dr tobar\AutoREM")
import tests._aislar_cache  # noqa: F401
from gui.app import App
from gui.paginas import about


def pared():
    app = App()
    app.update()
    t = time.perf_counter()
    app.mostrar("acerca_de")
    app.update_idletasks()
    dt = time.perf_counter() - t
    app.destroy()
    return dt


print("pared mostrar('acerca_de'):", ", ".join(f"{pared():.2f}s" for _ in range(2)))

# --- por bloque: cronometrar cada funcion de about.py envolviendola ---------------
tiempos = collections.defaultdict(float)
for nombre in ("_bloque_catalogos", "_bloque_preferencias", "_fila_maestro",
               "_resumen_cache"):
    orig = getattr(about, nombre)
    def envuelta(*a, _o=orig, _n=nombre, **k):
        t = time.perf_counter()
        try:
            return _o(*a, **k)
        finally:
            tiempos[_n] += time.perf_counter() - t
    setattr(about, nombre, envuelta)

app = App()
app.update()
pr = cProfile.Profile()
t = time.perf_counter()
pr.enable()
app.mostrar("acerca_de")
app.update_idletasks()
pr.disable()
total = time.perf_counter() - t
print(f"\ncon profiler: {total:.2f}s. Por bloque (inclusivo):")
for k, v in tiempos.items():
    print(f"  {k:<22} {v:6.2f}s")

st = pstats.Stats(pr)
tk = io = 0.0
ncall_tk = 0
for (fn, ln, func), (cc, nc, tt, ct, _) in st.stats.items():
    if "tkapp" in func:
        tk += tt; ncall_tk += nc
    if func in ("<built-in method io.open>", "<method 'read' of '_io.BufferedReader' objects>",
                "<built-in method nt.stat>", "<built-in method _io.open>") or "stat" in func and fn == "~":
        io += tt
print(f"  Tk (_tkinter.tkapp.*)   {tk:6.2f}s en {ncall_tk} llamadas")
print(f"  I/O de archivos (aprox) {io:6.2f}s")
print("\n-- top 12 por tottime --")
for (fn, ln, func), (cc, nc, tt, ct, _) in sorted(st.stats.items(), key=lambda x: -x[1][2])[:12]:
    print(f"  {tt:6.2f}s {nc:>8}  {fn.split(chr(92))[-1]}:{ln} {func[:60]}")
print("\n-- top 15 por cumtime (quien dispara) --")
for (fn, ln, func), (cc, nc, tt, ct, _) in sorted(st.stats.items(), key=lambda x: -x[1][3])[:15]:
    print(f"  {ct:6.2f}s {nc:>8}  {fn.split(chr(92))[-1]}:{ln} {func[:60]}")
app.destroy()
