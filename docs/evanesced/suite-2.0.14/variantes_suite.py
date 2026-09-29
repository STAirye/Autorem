"""Por que la GUI se frena 1.9x con 2 procesos no-Tk al lado, en un PC de 12 CPUs?
Mismo reparto que tools/correr_tests.py (GUI sola + el resto en 2), cuatro variantes:
base / hilos BLAS=1 / prioridad baja al resto / las dos. Imprime tiempos por proceso."""
import os, subprocess, sys, time
from pathlib import Path
RAIZ = Path(r"C:\Users\simon.tobar\Dr tobar\AutoREM")
sys.path.insert(0, str(RAIZ / "tools"))
import correr_tests as ct

archivos = sorted((RAIZ / "tests").glob("test_*.py"))
planes = [l for _, l in ct.repartir(archivos, 3)]
HILOS = {k: "1" for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                          "NUMEXPR_NUM_THREADS")}
BAJA = subprocess.BELOW_NORMAL_PRIORITY_CLASS


def correr(nombre, hilos, baja):
    env = dict(os.environ, **(HILOS if hilos else {}))
    t0 = time.time()
    procs = []
    for lista in planes:
        es_gui = any(a.name == "test_gui_construccion.py" for a in lista)
        procs.append((es_gui, len(lista), subprocess.Popen(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *map(str, lista)],
            cwd=str(RAIZ), env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            creationflags=(BAJA if baja and not es_gui else 0))))
    fin = {}
    while len(fin) < len(procs):
        for i, (_, _, p) in enumerate(procs):
            if i not in fin and p.poll() is not None:
                p.communicate()
                fin[i] = (time.time() - t0, p.returncode)
        time.sleep(0.2)
    partes = [f"{'GUI' if g else 'resto'}({n} arch) {fin[i][0]:5.1f}s"
              f"{'' if fin[i][1] == 0 else ' FALLA'}" for i, (g, n, _) in enumerate(procs)]
    print(f"{nombre:<24} WALL {time.time() - t0:5.1f}s   " + "  ".join(partes), flush=True)


print(f"cpus={os.cpu_count()}  reparto={[len(l) for l in planes]}")
for nombre, h, b in (("base", False, False), ("hilos=1", True, False),
                     ("prioridad baja resto", False, True), ("las dos", True, True)):
    correr(nombre, h, b)
