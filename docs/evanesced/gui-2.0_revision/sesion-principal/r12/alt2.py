# -*- coding: utf-8 -*-
import sys
from pathlib import Path
REPO = Path(r"E:\git\Autorem")
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "tests"))
import _aislar_cache  # noqa: F401
import tempfile
import pandas as pd
from contratos_fuentes import Contrato, escribir, plantilla
import modulos.rem_a23_respiratorio as a23
TMP = Path(tempfile.mkdtemp(prefix="r12_alt2_"))
q = lambda *a, **k: None
R1 = "11111111-1"
b, h, p = plantilla(Contrato(id="o", cubre=(), llamar=None, fila={}, ref="Otros_cronicos_iris.xlsx"))
col = a23._resolver_otros(h)
asma = {col["ASMA_p"]: "Si", col["ASMA_est"]: "Seguimiento", "INSTRUMENTO": "Médico"}
f25 = dict(asma, **{"NUMERO TIPO IDENTIFICACION": R1, "FECHA ATENCION": "01/03/2025", col["ASMA_prox"]: "01/04/2025"})
def f26(run): return dict(asma, **{"NUMERO TIPO IDENTIFICACION": run, "FECHA ATENCION": "01/06/2026", col["ASMA_prox"]: "01/12/2026"})
o25 = escribir(TMP / "otros_2025.xlsx", b, h, [f25], p)
for etiqueta, run in (("2026 con RUN", R1), ("2026 con el RUN VACIO", "")):
    o26 = escribir(TMP / f"otros_2026_{bool(run)}.xlsx", b, h, [f26(run)], p)
    od, _ = a23.cargar_otros([o25, o26], log=q)
    g, flags = a23._seccion_g(od, pd.Timestamp(2026, 8, 31))
    print(f"  [{etiqueta:<22}] carga sin error | Seccion G Asma (inasistentes) = {g['Asma']['Total']}")
