"""Deteccion A05 de GUI 2.0 (read_only=True) vs export con <dimension> ausente o rota.
Replica gui/paginas/a05.py::_detectar sin customtkinter. Nada se escribe en el repo."""
import re
import shutil
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, r"E:\git\Autorem")
import openpyxl  # noqa: E402
import programas.rem_saludmental as sm  # noqa: E402

SCRATCH = Path(__file__).resolve().parent / "dimtest"
SCRATCH.mkdir(exist_ok=True)
REFS = Path(r"E:\git\Autorem\refs_tablas")


def reescribir_dimension(src, dst, nueva):
    """Copia src->dst cambiando <dimension ref=.../> del sheet1 (nueva=None -> la borra)."""
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if re.match(r"xl/worksheets/sheet\d+\.xml$", item.filename):
                txt = data.decode("utf-8")
                if nueva is None:
                    txt = re.sub(r"<dimension[^>]*/>", "", txt)
                else:
                    txt = re.sub(r'<dimension ref="[^"]*"\s*/>', f'<dimension ref="{nueva}"/>', txt)
                data = txt.encode("utf-8")
            zout.writestr(item, data)


def detectar_como_gui(ruta):
    try:
        wb = openpyxl.load_workbook(ruta, read_only=True, data_only=True)
        cat = sm.detectar_formato(wb.active)
        wb.close()
        return cat
    except Exception as e:  # noqa: BLE001  (igual que la GUI)
        return f"error_lectura  <- {type(e).__name__}: {e}"


def detectar_como_abrir_validado(ruta):
    try:
        wb = openpyxl.load_workbook(ruta)
        return sm.detectar_formato(wb.active)
    except Exception as e:  # noqa: BLE001
        return f"EXC {type(e).__name__}: {e}"


for nombre in ("Formularios_RAYEN_csm_IRis.xlsx", "Formulario_csm_reporte_Administrativo.xlsx"):
    src = REFS / nombre
    with zipfile.ZipFile(src) as z:
        sheet = [n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml$", n)][0]
        m = re.search(r"<dimension[^>]*/>", z.read(sheet).decode("utf-8"))
    print(f"\n== {nombre}  (dimension original: {m.group(0) if m else 'AUSENTE'})")
    print("  original      GUI2 read_only :", detectar_como_gui(src))
    for etiqueta, nueva in (("sin dimension", None), ("dimension A1  ", "A1")):
        dst = SCRATCH / f"{etiqueta.strip().replace(' ', '_')}_{nombre}"
        reescribir_dimension(src, dst, nueva)
        print(f"  {etiqueta} GUI2 read_only :", detectar_como_gui(dst))
        print(f"  {etiqueta} abrir_validado :", detectar_como_abrir_validado(dst))
