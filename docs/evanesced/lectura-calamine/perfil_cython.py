"""Cuanto del tiempo de una corrida REAL es Python propio (lo unico que Cython
compilaria)? Perfila SM Actividades y A05 sobre agosto 2026 y reparte el tottime
por origen. Solo imprime tiempos y nombres de funcion: ningun dato."""
import sys, os, time, cProfile, pstats, tempfile, collections
from pathlib import Path
RAIZ = r"C:\Users\simon.tobar\Dr tobar\AutoREM"
sys.path.insert(0, RAIZ)
import tests._aislar_cache  # noqa: F401  (no tocar ~/.autorem real)

DM = Path(os.path.expanduser("~")) / "OneDrive - Ilustre Municipalidad de Maip\u00fa" / "Datos madre"
ADA = DM / "Variables 12m" / "Atenciones" / "2026.xlsx"
PSM = DM / "Variables 12m" / "PSM" / "2026.xlsx"
INSC = DM / "Poblaci\u00f3n" / "Informe_Inscritos__Adscritos_.xlsx"
MES = (2026, 8)
TMP = Path(tempfile.mkdtemp(prefix="perfil_"))


def quiet(*a, **k):
    pass


def bucket(fn):
    f = fn.replace("\\", "/").lower()
    if fn == "~":
        return "C builtins"
    for k in ("openpyxl", "pandas", "numpy", "customtkinter", "et_xmlfile", "lxml"):
        if f"/{k}/" in f:
            return k
    if "site-packages" in f:
        return "otras libs"
    if "/autorem/" in f and "/tests/" not in f:
        return "PROPIO (autoREM)"
    return "stdlib"


def reporte(nombre, pr, total):
    st = pstats.Stats(pr)
    b = collections.Counter()
    propias = []
    for (fn, ln, func), (cc, nc, tt, ct, _) in st.stats.items():
        k = bucket(fn)
        b[k] += tt
        if k == "PROPIO (autoREM)":
            propias.append((tt, f"{Path(fn).name}:{ln} {func}", nc))
    print(f"\n=== {nombre}: {total:.2f} s de pared ===")
    for k, v in b.most_common():
        print(f"  {k:<20} {v:7.2f} s  {v / total:6.1%}")
    print("  -- top 10 funciones PROPIAS por tottime --")
    for tt, lbl, nc in sorted(propias, reverse=True)[:10]:
        print(f"     {tt:6.2f} s  {nc:>9} llamadas  {lbl}")
    print("  -- top 8 builtins C (quien come) --")
    bi = sorted(((tt, func) for (fn, ln, func), (cc, nc, tt, ct, _) in st.stats.items()
                 if fn == "~"), reverse=True)[:8]
    for tt, func in bi:
        print(f"     {tt:6.2f} s  {func[:90]}")
    return b


def correr(nombre, fn):
    pr = cProfile.Profile()
    t = time.perf_counter()
    pr.enable()
    fn()
    pr.disable()
    return reporte(nombre, pr, time.perf_counter() - t)


# --- 1. SM Actividades (ADA + Inscritos), con escritura --------------------
def sm_act():
    import modulos.rem_sm_actividades as smact
    from programas.rem_utils import cargar_atenciones
    t = time.perf_counter()
    d = cargar_atenciones([ADA], log=quiet)
    print(f"  [sm] lectura ADA: {time.perf_counter() - t:.2f} s")
    t = time.perf_counter()
    E = smact.procesar_rango([ADA], inscritos=INSC, meses=[MES], log=quiet, d=d)
    print(f"  [sm] calculo (incl. Inscritos): {time.perf_counter() - t:.2f} s")
    t = time.perf_counter()
    smact.escribir(E, TMP / "sm.xlsx")
    print(f"  [sm] escritura: {time.perf_counter() - t:.2f} s")


# --- 2. A05 (N + O sobre el formulario SM), con escritura -------------------
def a05():
    import autorem
    import programas.rem_saludmental as sm
    from programas.rem_utils import primeras_filas
    perfil = sm.perfil_por_id(sm.detectar_formato_filas(primeras_filas(PSM, 30)))
    t = time.perf_counter()
    autorem._correr_tareas(autorem.TAREAS, PSM, perfil, log=quiet, mes=MES, carpeta=TMP)
    print(f"  [a05] total: {time.perf_counter() - t:.2f} s")


try:
    tot = collections.Counter()
    if "--solo-a05" not in sys.argv:
        tot += correr("SM Actividades agosto", sm_act)
    tot +=correr("A05 N+O agosto", a05)
    T = sum(tot.values())
    print(f"\n=== TOTAL (suma tottime) {T:.2f} s ===")
    for k, v in tot.most_common():
        print(f"  {k:<20} {v:7.2f} s  {v / T:6.1%}")
finally:
    for p in TMP.glob("*"):
        p.unlink()
    TMP.rmdir()
