import sys, zipfile, re
sys.path.insert(0, r"E:\git\Autorem")
import openpyxl
from programas.rem_utils import leer_xlsx
import programas.rem_saludmental as sm

def patch(src, dst, fn):
    zin = zipfile.ZipFile(src)
    zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == "xl/worksheets/sheet1.xml":
            data = fn(data.decode("utf-8")).encode("utf-8")
        zout.writestr(item, data)
    zout.close()

src = r"E:\git\Autorem\refs_tablas\ATENCIONESDIAGNOSTICOSACTIVIDADES_iris.xlsx"
for tag, fn in [("orig", lambda x: x), ("nodim", lambda x: re.sub(r"<dimension[^>]*/>", "", x)),
                ("dimA1", lambda x: re.sub(r"<dimension[^>]*/>", '<dimension ref="A1"/>', x)),
                ("dimA1B2", lambda x: re.sub(r"<dimension[^>]*/>", '<dimension ref="A1:B2"/>', x))]:
    dst = f"ada_{tag}.xlsx"
    patch(src, dst, fn)
    h, rows = leer_xlsx(dst)
    print(tag, "leer_xlsx header len", len(h), "rows", len(rows))

# A05 path: abrir_validado with IRIS dimA1 (full load)
for f in ["dimA1_Formularios_RAYEN_csm_IRis.xlsx", "nodim_Formularios_RAYEN_csm_IRis.xlsx"]:
    try:
        wb, ws = sm.abrir_validado(f, sm.perfil_por_id("iris"))
        print(f, "abrir_validado OK (old GUI path)")
    except Exception as e:
        print(f, "abrir_validado EXC", type(e).__name__, e)
