import sys; sys.path.insert(0, r"E:\git\Autorem\tests"); sys.dont_write_bytecode = True
import _aislar_cache  # noqa
import test_a23 as T, openpyxl, tempfile
from pathlib import Path
a23 = T.a23
s = a23.cargar_estrat(T._mk_estrat(["RUT", "DV", "COMUNA"], [[11111111, "1", "Maipu"]]))
print("(c) estrat sin col. diagnosticos:", s.to_dict(), "(sin error)")
# (d) A05 con TODAS las FECHA FORMULARIO ilegibles
import programas.rem_saludmental as sm
import modulos.rem_a05_o_egresos as eg
tmp = Path(tempfile.mkdtemp())
p = tmp / "a05.xlsx"
wb = openpyxl.Workbook(); ws = wb.active
for r in range(1, 17): ws.cell(row=r, column=1, value=f"banner {r}")
ws.append(["NUMERO TIPO IDENTIFICACION", "AÑO APLICACIÓN FORMULARIO", "SEXO", "FECHA FORMULARIO",
           "18.- ¿ TIENE  DEPRESIÓN ?", "19.- ESTADO"])
ws.append(["11111111-1", 30, "Mujer", "31-31-2026", "SI", "EGRESO POR ALTA"]); wb.save(p)
try:
    eg.procesar(p, tmp / "o.xlsx", mes=(2026, 8), log=lambda m: print("   log:", m) if "fecha" in m.lower() else None)
except Exception as e:
    print("(d) A05 fechas ilegibles ->", type(e).__name__, getattr(e, "categoria", ""), "|", str(e).splitlines()[0], "|", str(e).splitlines()[2])
# (e) Cupos con filas pero sin Instrumento
import programas.estamentos as est
p = tmp / "cupos.xlsx"
wb = openpyxl.Workbook(); ws = wb.active
ws.append(["Fecha", "Profesional", "Instrumento", "Cupos"]); ws.append(["01/08/2026", "ANA PEREZ", "", 10]); wb.save(p)
try:
    print("(e) Cupos sin estamentos ->", est.cargar_estamentos(p, log=print))
except Exception as e:
    print("(e) ->", type(e).__name__, str(e)[:80])
