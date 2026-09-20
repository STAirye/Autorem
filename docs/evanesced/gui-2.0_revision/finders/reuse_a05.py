import sys, zipfile, re, shutil, os
sys.path.insert(0, r"E:\git\Autorem")
import openpyxl
import programas.rem_saludmental as sm

SCR = r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\648a107e-f033-4d56-a55d-a415a58f003e\scratchpad"
REFS = r"E:\git\Autorem\refs_tablas"


def preview_a05(ruta):
    # verbatim copy of gui/paginas/a05.py bloque_archivo_formato._detectar.trabajo
    try:
        wb = openpyxl.load_workbook(ruta, read_only=True, data_only=True)
        categoria = sm.detectar_formato(wb.active)
        wb.close()
    except Exception as e:   # noqa: BLE001
        categoria = "error_lectura (%s: %s)" % (type(e).__name__, e)
    return categoria


def real_open(ruta, perfil_id):
    try:
        sm.abrir_validado(ruta, sm.perfil_por_id(perfil_id))
        return "abrir_validado OK"
    except Exception as e:
        return "%s(%s)" % (type(e).__name__, getattr(e, "categoria", e))


def dimension_of(path):
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if n.startswith("xl/worksheets/sheet"):
                m = re.search(rb"<dimension[^>]*>", z.read(n))
                print("   ", n, m.group(0) if m else None)


def rewrite_dimension(src, dst, new):
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.startswith("xl/worksheets/sheet"):
                if new is None:
                    data = re.sub(rb"<dimension[^>]*/>", b"", data)
                else:
                    data = re.sub(rb'<dimension ref="[^"]*"', b'<dimension ref="' + new + b'"', data)
            zout.writestr(item, data)


for f, pid in (("Formularios_RAYEN_csm_IRis.xlsx", "iris"),
               ("Formulario_csm_reporte_Administrativo.xlsx", "administrativo")):
    p = os.path.join(REFS, f)
    print(f)
    dimension_of(p)
    print("  preview:", preview_a05(p), "| real:", real_open(p, pid))
    for tag, new in (("dim=A1", b"A1"), ("no-dim", None)):
        dst = os.path.join(SCR, tag.replace("=", "_") + "_" + f)
        rewrite_dimension(p, dst, new)
        print("  [%s] preview:" % tag, preview_a05(dst), "| real:", real_open(dst, pid))
