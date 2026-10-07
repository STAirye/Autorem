"""Benchmark de autoREM 2.0.29 completo, con los exports reales del respaldo.
Uso: python bench_todo.py [reps]           -> orquesta (cada escenario en su subproceso)
     python bench_todo.py --uno <escenario> -> corre UNO, imprime JSON de tiempos
Solo imprime tiempos, conteos de filas y RAM. Las salidas van a un temp y se borran."""
import sys, os, time, json, subprocess, tempfile, shutil, statistics, ctypes
from ctypes import wintypes
from pathlib import Path

RAIZ = r"D:\git\Autorem"
DM = Path(r"D:\pega respaldo\Datos madre")
V = DM / "Variables 12m"
ANIOS = ["2021", "2022", "2023", "2024", "2025", "2026"]
ADA_TODO = [V / "Atenciones" / f"{a}.xlsx" for a in ANIOS]
ADA_SM = [V / "Atenciones" / f"{a}.xlsx" for a in ("2025", "2026")]
GRUPAL = [V / "Atenciones Grupales" / f"{a}.xlsx" for a in ("2025", "2026")]
PSM = [V / "PSM" / f"{a}.xlsx" for a in ANIOS]
OTROS = [V / "Otros y Respi" / f"{a}.xlsx" for a in ANIOS]
NSP = [V / "Inasistentes" / f"{a}.xlsx" for a in ANIOS]
EST = DM / "Poblaci\u00f3n" / "Estratificaci\u00f3n_de_Riesgo.xlsx"
INSC = DM / "Poblaci\u00f3n" / "Informe_Inscritos__Adscritos_.xlsx"
MES = (2026, 2)   # el respaldo es del 11-mar-2026: febrero es el ultimo mes completo


class PMC(ctypes.Structure):
    _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                ("a", ctypes.c_size_t), ("b", ctypes.c_size_t), ("c", ctypes.c_size_t),
                ("d", ctypes.c_size_t), ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t)]


def pico_mb():
    k = ctypes.WinDLL("psapi")
    k.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(PMC), wintypes.DWORD]
    h = ctypes.windll.kernel32.GetCurrentProcess
    h.restype = wintypes.HANDLE
    m = PMC(); m.cb = ctypes.sizeof(PMC)
    k.GetProcessMemoryInfo(h(), ctypes.byref(m), m.cb)
    return m.PeakWorkingSetSize / 2**20


def quiet(*a, **k):
    pass


FASES = []


def fase(nombre, fn):
    t = time.perf_counter()
    r = fn()
    FASES.append((nombre, time.perf_counter() - t))
    return r


def esc_import():
    fase("import programas+modulos", lambda: [__import__(m) for m in (
        "programas.rem_utils", "programas.poblacion", "modulos.rem_a23_respiratorio",
        "modulos.rem_sm_actividades", "modulos.rem_sm_trabajo_perdido",
        "modulos.rem_sp_p6_poblacion", "modulos.rem_sm_rescate_inasistentes",
        "modulos.rem_a03_d3_instrumentos", "autorem")])
    fase("import gui (customtkinter + paginas)", lambda: [__import__(m) for m in (
        "customtkinter", "gui.app")])


def esc_a05(tmp, anio):
    import autorem
    import programas.rem_saludmental as sm
    from programas.rem_utils import primeras_filas
    from programas.formatos import MAX_FILAS_HEADER
    ent = V / "PSM" / f"{anio}.xlsx"
    cat = fase("detectar formato", lambda: sm.detectar_formato_filas(primeras_filas(ent, MAX_FILAS_HEADER)))
    perfil = sm.perfil_por_id(cat)
    mes = [(int(anio), 12)] if anio != "2026" else [MES]
    fase("A05 N+O (abrir+marcar+guardar)", lambda: autorem._correr_tareas(
        autorem.TAREAS, ent, perfil, quiet, mes=mes, carpeta=tmp))


def esc_a23(tmp):
    import modulos.rem_a23_respiratorio as a23
    fer = fase("a23.procesar", lambda: a23.procesar(ADA_TODO, otros=OTROS, estrat=EST,
                                                    inasistentes=NSP, mes=MES, log=quiet))
    fase("a23.escribir", lambda: a23.escribir(fer, tmp / "a23.xlsx"))
    return {"filas": len(fer)}


def esc_sm(tmp):
    import modulos.rem_sm_actividades as smact
    import modulos.rem_sm_trabajo_perdido as tp
    from programas.catalogos import maestro_slim
    from programas.rem_utils import cargar_atenciones
    d = fase("cargar_atenciones (ADA 2025+2026)", lambda: cargar_atenciones(ADA_SM, log=quiet))
    E = fase("sm.procesar_rango", lambda: smact.procesar_rango(
        ADA_SM, grupal=GRUPAL, inscritos=INSC, meses=[MES], log=quiet, d=d))
    fase("sm.escribir", lambda: smact.escribir(E, tmp / "sm.xlsx"))
    Etp = fase("tp.procesar_rango", lambda: tp.procesar_rango(
        ADA_SM, maestro=maestro_slim(), meses=[MES], log=quiet, d=d))
    fase("tp.escribir", lambda: tp.escribir(Etp, tmp / "tp.xlsx"))
    return {"eventos": len(E), "tp": len(Etp)}


def esc_sm_6m(tmp):
    import modulos.rem_sm_actividades as smact
    from programas.rem_utils import cargar_atenciones
    meses = [(2025, m) for m in range(9, 13)] + [(2026, 1), (2026, 2)]
    d = fase("cargar_atenciones (ADA 2025+2026)", lambda: cargar_atenciones(ADA_SM, log=quiet))
    E = fase("sm.procesar_rango 6 meses", lambda: smact.procesar_rango(
        ADA_SM, grupal=GRUPAL, inscritos=INSC, meses=meses, log=quiet, d=d))
    fase("sm.escribir", lambda: smact.escribir(E, tmp / "sm.xlsx"))
    return {"eventos": len(E)}


def esc_p6(tmp):
    import programas.poblacion as pob
    import programas.rem_utils as ru
    import modulos.rem_sp_p6_poblacion as p6
    import modulos.rem_sm_rescate_inasistentes as resc
    insc = fase("cargar_inscritos", lambda: pob.cargar_inscritos(INSC, log=quiet))
    form = fase("cargar_formulario_sm (PSM 2021-26)", lambda: pob.cargar_formulario_sm(PSM, log=quiet))
    ada = fase("cargar_atenciones (ADA 2021-26)", lambda: ru.cargar_atenciones(ADA_TODO, log=quiet))
    P = fase("construir_poblacion", lambda: pob.construir_poblacion(insc, form, ada, mes=MES, log=quiet))
    res = fase("construir_p6", lambda: p6.construir_p6(P, log=quiet))
    fase("p6.escribir", lambda: p6.escribir(P, res, tmp / "p6.xlsx"))
    Er = fase("rescate.procesar", lambda: resc.procesar(insc, form, ada, mes=MES, log=quiet, P=P, fuentes=[]))
    fase("rescate.escribir", lambda: resc.escribir(Er, tmp / "resc.xlsx"))
    return {"P": P.shape[0]}


ESC = {
    "import": lambda tmp: esc_import(),
    "a05_2026": lambda tmp: esc_a05(tmp, "2026"),
    "a05_2025": lambda tmp: esc_a05(tmp, "2025"),
    "a23": esc_a23,
    "sm_tp": esc_sm,
    "sm_6meses": esc_sm_6m,
    "p6_rescate": esc_p6,
}


def uno(nombre):
    sys.path.insert(0, RAIZ)
    os.chdir(RAIZ)
    import tests._aislar_cache  # noqa: F401  (nunca toca ~/.autorem real)
    tmp = Path(tempfile.mkdtemp(prefix="bench_"))
    try:
        t0 = time.perf_counter()
        extra = ESC[nombre](tmp) or {}
        tot = time.perf_counter() - t0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("@@" + json.dumps({"total": tot, "fases": FASES, "ram": pico_mb(), "extra": extra}))


def orquestar(reps):
    out = {}
    for n in ESC:
        corridas = []
        for i in range(reps):
            t = time.perf_counter()
            p = subprocess.run([sys.executable, __file__, "--uno", n], capture_output=True,
                               text=True, encoding="utf-8", errors="replace",
                               env={**os.environ, "PYTHONIOENCODING": "utf-8"})
            pared = time.perf_counter() - t
            lin = [l for l in p.stdout.splitlines() if l.startswith("@@")]
            if not lin:
                print(f"[{n}] FALLO rc={p.returncode}\n{p.stderr[-2500:]}")
                break
            r = json.loads(lin[0][2:]); r["proceso"] = pared
            corridas.append(r)
            print(f"[{n}] rep {i + 1}: {r['total']:6.2f} s (proceso {pared:5.2f} s) RAM {r['ram']:.0f} MB {r['extra']}", flush=True)
        out[n] = corridas
    Path(__file__).with_suffix(".json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("\n=== MEDIANAS ===")
    for n, cs in out.items():
        if not cs:
            continue
        print(f"{n:12s} total {statistics.median(c['total'] for c in cs):6.2f} s | "
              f"proceso {statistics.median(c['proceso'] for c in cs):6.2f} s | "
              f"RAM {max(c['ram'] for c in cs):5.0f} MB")
        for j, (fn, _) in enumerate(cs[0]["fases"]):
            print(f"    {statistics.median(c['fases'][j][1] for c in cs):6.2f} s  {fn}")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--uno"]:
        uno(sys.argv[2])
    else:
        orquestar(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
