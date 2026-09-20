# -*- coding: utf-8 -*-
import sys
from datetime import date
from harness import *  # noqa

from gui.paginas import poblacion as pag  # mirrors the GUI page exactly

MES = (2026, 8)
N = 30


def ctx(insc, forms, ada, name):
    carpeta = OUT / name
    carpeta.mkdir(exist_ok=True)
    return {"inscritos": insc, "formularios": list(forms), "ada": list(ada),
            "mes": MES, "carpeta": carpeta}


def go(label, c):
    log = mklog()

    def f():
        res = pag.correr(c, log)
        txt = pag.resumen(res)
        print("  resumen():", txt.replace("\n", " | ")[:500])
        return res
    res, exc = run(label, f)
    tail = [l for l in log.buf if ("rescate" in l or "poblacion" in l or "sp_p6" in l)]
    for l in tail[-12:]:
        print("  log>", l[:300])
    return res, exc


# --- valid fixtures (fake RUTs) ---
insc_ok = mk_insc([insc_row(i) for i in range(N)], "insc_ok.xlsx")
form_ok = mk_form([form_row(i, date(2026, 5, 10)) for i in range(N)], "form_ok.xlsx")
ada_ok = mk_ada([ada_row(i, date(2026, 8, 5)) for i in range(N)] +
                [ada_row(i, date(2025, 7, 10)) for i in range(N)], "ada_ok.xlsx")

# --- header-only refs (copied to scratch) ---
insc_h = copy_ref("Informe_Inscritos__Adscritos_heads.xlsx", "insc_hdr.xlsx")
form_h = copy_ref("Formularios_RAYEN_csm_IRis.xlsx", "form_hdr.xlsx")
ada_h = copy_ref("ATENCIONESDIAGNOSTICOSACTIVIDADES_iris.xlsx", "ada_hdr.xlsx")

go("P0 baseline all valid", ctx(insc_ok, [form_ok], [ada_ok], "P0"))
go("P1 all three header-only refs", ctx(insc_h, [form_h], [ada_h], "P1"))
go("P2 valid inscritos + HEADER-ONLY formularios + valid ADA", ctx(insc_ok, [form_h], [ada_ok], "P2"))
go("P3 valid inscritos + valid formularios + HEADER-ONLY ADA", ctx(insc_ok, [form_ok], [ada_h], "P3"))

ada_old = mk_ada([ada_row(i, date(2020, 3, 5)) for i in range(N)], "ada_2020.xlsx")
go("P4 ADA with rows but none in the 13-month window (all 2020)", ctx(insc_ok, [form_ok], [ada_old], "P4"))

insc_resp = mk_insc([insc_row(i, tipoid="RUN Responsable") for i in range(N)], "insc_resp.xlsx")
go("P5 inscritos rows but all 'RUN Responsable'", ctx(insc_resp, [form_ok], [ada_ok], "P5"))

form_future = mk_form([form_row(i, date(2027, 2, 10)) for i in range(N)], "form_2027.xlsx")
go("P6 formularios rows but none <= month end (all 2027)", ctx(insc_ok, [form_future], [ada_ok], "P6"))

form_norut = mk_form([{**form_row(i, date(2026, 5, 10)), "NUMERO TIPO IDENTIFICACION": None}
                      for i in range(N)], "form_norut.xlsx")
go("P7 formularios rows but RUT column blank in all rows", ctx(insc_ok, [form_norut], [ada_ok], "P7"))

ada_badfecha = mk_ada([{**ada_row(i, date(2026, 8, 5)), "FECHA ATENCION": "sin fecha"} for i in range(N)],
                      "ada_badfecha.xlsx")
go("P8 ADA rows but all FECHA unparseable", ctx(insc_ok, [form_ok], [ada_badfecha], "P8"))

insc_ghost = mk_insc([insc_row(i + 500) for i in range(N)], "insc_ghost.xlsx")
go("P9 inscritos valid but NO overlap with form/ADA RUNs", ctx(insc_ghost, [form_ok], [ada_ok], "P9"))

ada_nosm = mk_ada([ada_row(i, date(2026, 8, 5), act="Curacion simple") for i in range(N)], "ada_nosm.xlsx")
go("P10 ADA rows in window but none of the 7 SM activities", ctx(insc_ok, [form_ok], [ada_nosm], "P10"))

# Monitoreo admin (header-only) in the ADA slot
mon_h = copy_ref("Monitoreo_de_Actividades_anonimizado.xlsx", "monitoreo_hdr.xlsx")
go("P11 Monitoreo admin HEADER-ONLY in ADA slot (valid insc+form)", ctx(insc_ok, [form_ok], [mon_h], "P11"))
