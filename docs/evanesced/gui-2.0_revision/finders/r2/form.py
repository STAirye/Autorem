import sys; sys.path.insert(0, r"E:\git\Autorem\tests"); sys.dont_write_bytecode = True
import _aislar_cache  # noqa
import test_sp_p6 as T, openpyxl, shutil
from datetime import date
import programas.poblacion as pob
Q = T._Q
bueno = T._mk_formulario([{"rut": "11111111-1", "fecha": date(2026, 7, 1), **{Q[57]: "SI", Q[58]: "INGRESO"}}])
b2 = T._TMP / "form_2026.xlsx"; shutil.copy(bueno, b2)
# 2025: descarga cortada -> solo banner + encabezado
vacio = T._TMP / "form_2025.xlsx"
wb = openpyxl.load_workbook(bueno); ws = wb.active; ws.delete_rows(18, ws.max_row); wb.save(vacio)
d = pob.cargar_formulario_sm([str(vacio), str(b2)], log=print)
print("OK, sin error:", len(d), "formularios; attrs:", d.attrs)
try:
    pob.cargar_formulario_sm([str(vacio)], log=lambda *a: None)
except Exception as e:
    print("solo el vacio ->", type(e).__name__, getattr(e, "categoria", ""))
