"""Mide `ws.cell(row,col).value` por celda vs `iter_rows(values_only=True)`
sobre un .xlsx con la forma de un formulario 'Control de Salud Mental' IRIS
(banner de 15 filas + ~100 columnas + N filas de datos)."""
import time, tempfile, os
import openpyxl

NCOLS, NFILAS, HDR = 100, 4000, 16
ruta = os.path.join(tempfile.gettempdir(), "bench_form.xlsx")

if not os.path.exists(ruta):
    wb = openpyxl.Workbook()
    ws = wb.active
    for r in range(1, HDR):
        ws.cell(row=r, column=1, value="banner")
    ws.append([f"{c}.- PREGUNTA {c}" for c in range(1, NCOLS + 1)])
    for i in range(NFILAS):
        # ~40% de celdas vacias, como un formulario real (la mayoria de las
        # preguntas vienen en blanco por paciente)
        ws.append([("SI" if (i + c) % 5 == 0 else None) for c in range(NCOLS)])
    wb.save(ruta)
    print("creado", ruta)


def por_celda():
    wb = openpyxl.load_workbook(ruta, data_only=True)
    ws = wb.active
    t = time.perf_counter()
    n = 0
    for r in range(HDR + 1, ws.max_row + 1):
        fila = [ws.cell(row=r, column=c).value for c in range(1, NCOLS + 1)]
        n += sum(1 for v in fila if v is not None)
    dt = time.perf_counter() - t
    celdas_materializadas = len(ws._cells)
    wb.close()
    return dt, n, celdas_materializadas


def por_iter_rows():
    wb = openpyxl.load_workbook(ruta, data_only=True)
    ws = wb.active
    t = time.perf_counter()
    n = 0
    for fila in ws.iter_rows(min_row=HDR + 1, max_col=NCOLS, values_only=True):
        n += sum(1 for v in fila if v is not None)
    dt = time.perf_counter() - t
    celdas = len(ws._cells)
    wb.close()
    return dt, n, celdas


for f in (por_celda, por_iter_rows, por_celda, por_iter_rows):
    dt, n, celdas = f()
    print(f"{f.__name__:14s} {dt:6.3f} s   no_vacias={n}   ws._cells={celdas}")
