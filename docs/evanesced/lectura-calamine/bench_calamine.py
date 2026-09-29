"""openpyxl (filas_xlsx + verificar_hoja_unica, lo que hace hoy cargar_canonico)
vs python-calamine, sobre exports REALES. Mide tiempo y compara celda por celda.
Solo imprime tiempos, formas y CONTEOS de discrepancias por tipo: ningun valor."""
import sys, os, time, collections, datetime as dt
from pathlib import Path
sys.path.insert(0, r"C:\Users\simon.tobar\Dr tobar\AutoREM")
from programas.rem_utils import filas_xlsx, verificar_hoja_unica
from python_calamine import CalamineWorkbook

DM = Path(os.path.expanduser("~")) / "OneDrive - Ilustre Municipalidad de Maip\u00fa" / "Datos madre"
ARCHIVOS = {
    "ADA 2026": DM / "Variables 12m" / "Atenciones" / "2026.xlsx",
    "Inscritos": DM / "Poblaci\u00f3n" / "Informe_Inscritos__Adscritos_.xlsx",
    "Formulario PSM": DM / "Variables 12m" / "PSM" / "2026.xlsx",
}


def calamine_filas(p):
    wb = CalamineWorkbook.from_path(str(p))
    hojas = [wb.get_sheet_by_index(i).to_python(skip_empty_area=False)
             for i in range(len(wb.sheet_names))]
    con_datos = [i for i, h in enumerate(hojas)
                 if any(v not in (None, "") for f in h for v in f)]
    return hojas, con_datos


def igual(a, b):
    if a in (None, "") and b in (None, ""):
        return True
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) \
            and not isinstance(a, bool) and not isinstance(b, bool):
        return float(a) == float(b)
    if isinstance(a, dt.datetime) and isinstance(b, dt.date) and not isinstance(b, dt.datetime):
        return a.time() == dt.time(0) and a.date() == b
    return a == b and type(a) is type(b)


for nombre, p in ARCHIVOS.items():
    print(f"\n=== {nombre} ({p.stat().st_size / 1e6:.1f} MB) ===")
    t = time.perf_counter(); verificar_hoja_unica(p); t_v = time.perf_counter() - t
    t = time.perf_counter(); A = filas_xlsx(p); t_f = time.perf_counter() - t
    print(f"  openpyxl: verificar_hoja_unica {t_v:6.2f} s + filas_xlsx {t_f:6.2f} s "
          f"= {t_v + t_f:6.2f} s")
    t = time.perf_counter(); hojas, con_datos = calamine_filas(p); t_c = time.perf_counter() - t
    print(f"  calamine: todas las hojas              {t_c:6.2f} s   "
          f"-> {(t_v + t_f) / t_c:4.1f}x   hojas con datos: {con_datos}")
    B = hojas[con_datos[0]] if con_datos else []
    wa = max((len(f) for f in A), default=0)
    wb_ = max((len(f) for f in B), default=0)
    print(f"  forma: openpyxl {len(A)} x {wa}   calamine {len(B)} x {wb_}")
    # recortar filas vacias al final (openpyxl puede traer colas de None)
    def recorta(F):
        F = list(F)
        while F and all(v in (None, "") for v in F[-1]):
            F.pop()
        return F
    A, B = recorta(A), recorta(B)
    if len(A) != len(B):
        print(f"  !! distinto n de filas tras recortar colas: {len(A)} vs {len(B)}")
    dif = collections.Counter()
    cols = collections.Counter()
    blando = collections.Counter()
    n = 0
    for fa, fb in zip(A, B):
        w = max(len(fa), len(fb))
        fa = tuple(fa) + (None,) * (w - len(fa))
        fb = tuple(fb) + (None,) * (w - len(fb))
        for j, (a, b) in enumerate(zip(fa, fb)):
            n += 1
            if not igual(a, b):
                dif[(type(a).__name__, type(b).__name__)] += 1
                cols[j] += 1
            elif type(a) is not type(b):
                blando[(type(a).__name__, type(b).__name__)] += 1
    print(f"  celdas comparadas: {n}   distintas: {sum(dif.values())}")
    for (ta, tb), c in dif.most_common(8):
        print(f"     openpyxl {ta:<9} vs calamine {tb:<9} {c:>9}")
    print(f"  iguales SOLO tras normalizar (tipo distinto): {sum(blando.values())}")
    for (ta, tb), c in blando.most_common(8):
        print(f"     openpyxl {ta:<9} vs calamine {tb:<9} {c:>9}")
    if cols:
        print(f"  columnas afectadas (indice: n): {dict(cols.most_common(10))}")
