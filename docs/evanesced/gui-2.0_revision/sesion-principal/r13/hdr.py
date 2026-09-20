import sys, pathlib
sys.path.insert(0, r'E:\git\Autorem')
from programas.rem_utils import abrir_xlsx_ro, filas_hoja
dist = []
for p in sorted(pathlib.Path(r'E:\git\Autorem\refs_tablas').glob('*.xlsx')):
    try:
        wb = abrir_xlsx_ro(p)
    except Exception as e:
        print(p.name, "ERR", e)
        continue
    try:
        for ws in wb.worksheets:
            filas = filas_hoja(ws)
            if not filas:
                continue
            n = [sum(1 for v in f if v not in (None, "")) for f in filas[:50]]
            h5 = next((i + 1 for i, c in enumerate(n) if c >= 5), None)
            h3 = next((i + 1 for i, c in enumerate(n[:40]) if c > 3), None)
            if h5 != h3:
                dist.append((p.name, ws.title, len(filas), h5, h3, n[:12]))
    finally:
        wb.close()
print("hojas donde los DOS criterios difieren (ventana propia de cada uno):")
for d in dist:
    print("  ", d)
print("total", len(dist))
