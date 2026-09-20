# -*- coding: utf-8 -*-
"""Ronda 12 (altitud) - repros. Datos SINTETICOS (RUT 11111111-1 y dv_rut). No escribe
nada en el repo: todo va a una carpeta temporal."""
import sys
from pathlib import Path
REPO = Path(r"E:\git\Autorem")
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "tests"))
import _aislar_cache  # noqa: F401  PRIMERO
import tempfile
import pandas as pd
from contratos_fuentes import Contrato, escribir, plantilla
from programas.rem_utils import (cargar_atenciones, dv_rut, opcional, OpcionalInvalido,
                                 ArchivoInvalido, trans_map, atenid_multiprofesional)
import modulos.rem_a23_respiratorio as a23
import modulos.rem_sm_trabajo_perdido as tp

TMP = Path(tempfile.mkdtemp(prefix="r12_alt_"))
q = lambda *a, **k: None
logs = []
L = lambda m="": logs.append(str(m))


def fx(ref, filas, nombre):
    b, h, p = plantilla(Contrato(id=ref, cubre=(), llamar=None, fila={}, ref=ref))
    return escribir(TMP / nombre, b, h, filas, p)


R1 = "11111111-1"
R2 = "10000013-" + dv_rut("10000013")

print("=== 1. cargar_atenciones: RUN vacio en TODO un archivo, junto a uno bueno ===")
bueno = fx("ATENCIONESDIAGNOSTICOSACTIVIDADES_iris.xlsx", [
    {"NUMERO TIPO IDENTIFICACION": R1, "ATEN ID": "901", "FECHA ATENCION": "05/08/2026",
     "ACTIVIDADES": "CONTROL SALA (IRA, ERA O MIXTA)", "DIAGNOSTICOS": "J45",
     "INSTRUMENTO": "MEDICO", "TIPO ATENCION": "CONTROL", "PROFESIONAL ATENCION": "DR X"}],
    "ada_bueno.xlsx")
malo_filas = [{"NUMERO TIPO IDENTIFICACION": "", "ATEN ID": str(950 + i), "FECHA ATENCION": "06/08/2026",
               "ACTIVIDADES": "CONTROL SALA (IRA, ERA O MIXTA)", "DIAGNOSTICOS": "J45",
               "INSTRUMENTO": "MEDICO", "TIPO ATENCION": "CONTROL", "PROFESIONAL ATENCION": "DR X"}
              for i in range(5)]
malo = fx("ATENCIONESDIAGNOSTICOSACTIVIDADES_iris.xlsx", malo_filas, "ada_sin_run.xlsx")
try:
    cargar_atenciones(malo, log=q)
    print("  solo el malo: NO fallo (!)")
except ArchivoInvalido as e:
    print("  solo el malo ->", e.categoria)
logs.clear()
d = cargar_atenciones([bueno, malo], log=L)
print("  [bueno, malo] -> NO falla; filas:", len(d), "| RUN nulos:", int(d["RUN"].isna().sum()))
print("  log:", [l for l in logs if "sin RUN" in l])
fer = a23.procesar([bueno, malo], mes=(2026, 8), log=q)
print("  A23 fer: pacientes =", len(fer), "| RUN del detalle:", [str(x) for x in fer["RUN"]])

print("\n=== 2. cargar_otros: RUN vacio en TODO un archivo (el del anio actual) ===")
asma = {"9.- ¿PADECE DE ASMA BRONQUIAL?": "Si", "10.- ESTADO": "Ingreso", "INSTRUMENTO": "Médico"}
b, h, p = plantilla(Contrato(id="o", cubre=(), llamar=None, fila={}, ref="Otros_cronicos_iris.xlsx"))
prox = next(c for c in h if "PROXIMO CONTROL" in str(c).upper().replace("Ó", "O"))
o_bueno = escribir(TMP / "otros_2025.xlsx", b, h, [dict(asma, **{"NUMERO TIPO IDENTIFICACION": R1,
                   "FECHA ATENCION": "01/03/2025", prox: "01/04/2025"})], p)
o_malo = escribir(TMP / "otros_2026.xlsx", b, h, [dict(asma, **{"NUMERO TIPO IDENTIFICACION": "",
                  "FECHA ATENCION": f"0{i+1}/02/2026", prox: "01/03/2026"}) for i in range(4)], p)
try:
    a23.cargar_otros(o_malo, log=q)
    print("  solo 2026: NO fallo (!)")
except ArchivoInvalido as e:
    print("  solo 2026 ->", e.categoria)
od, _ = a23.cargar_otros([o_bueno, o_malo], log=q)
print("  [2025, 2026] -> NO falla; filas:", len(od), "| RUN '' :", int(od["RUN"].map(lambda v: str(v or '').strip() == '').sum()))
g, flags = a23._seccion_g(od, pd.Timestamp(2026, 8, 31))
print("  Seccion G asma: Total =", g["Asma"]["Total"], "| RUNs:", sorted(repr(r) for r in flags["ASMA"]))

print("\n=== 3. opcional() y un opcional ILEGIBLE (.html disfrazado de .xlsx, el clasico de RAYEN) ===")
html = TMP / "Informe_Inscritos.xlsx"
html.write_text("<html><body><table><tr><td>x</td></tr></table></body></html>", encoding="utf-8")
for nombre, fn in [("trans_map (SM, inscritos)", lambda: trans_map(html)),
                   ("atenid_multiprofesional (SM)", lambda: atenid_multiprofesional(html)),
                   ("cargar_estrat (A23)", lambda: a23.cargar_estrat(html)),
                   ("cargar_inasistentes (A23, via cargar_canonico)", lambda: a23.cargar_inasistentes(html, log=q))]:
    try:
        with opcional("x"):
            fn()
    except OpcionalInvalido as e:
        print(f"  {nombre}: OpcionalInvalido({e.categoria}) -> la GUI PREGUNTA")
    except Exception as e:  # noqa
        print(f"  {nombre}: {type(e).__name__} -> NO es OpcionalInvalido: la corrida ENTERA se cae")

print("\n=== 3b. opcional() convierte CUALQUIER ValueError (no solo el del archivo) ===")
try:
    with opcional("inscritos"):
        int("bug de codigo")
except OpcionalInvalido as e:
    print("  ValueError de codigo ->", type(e).__name__, "| categoria:", e.categoria)

print("\n=== 4. Trabajo Perdido: la MISMA atencion en IRIS (1 fila) y en Monitoreo (2 filas) ===")
base = dict(FECHA=pd.Timestamp(2026, 8, 5), PROF="DR X", INSTR="MEDICO", RUN=R1)
act1, act2 = "CONSULTA DE SALUD MENTAL", "CONSEJERIA INDIVIDUAL EN SALUD MENTAL"
from programas.rem_utils import norm
iris = pd.DataFrame([dict(base, ATENID="901", ACT=f"{act1}; {act2}")])
mon = pd.DataFrame([dict(base, ATENID="mon.xlsx|1", ACT=act1), dict(base, ATENID="mon.xlsx|1", ACT=act2)])
for nombre, dd in (("IRIS", iris), ("Monitoreo", mon)):
    dd["ACT_n"] = dd["ACT"].map(norm)
    E = tp.analizar(dd, pd.Timestamp(2026, 8, 1), pd.Timestamp(2026, 8, 31), log=q)
    print(f"  {nombre:<9}: {len(E)} atencion(es) a saco roto")
print("  A23 (misma forma, ya corregido en ronda 11): _act_de_la_atencion SOLO lo usa a23._masks_simples")
