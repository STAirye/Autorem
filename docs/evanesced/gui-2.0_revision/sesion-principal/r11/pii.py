# Solo CUENTA: filas con datos, celdas con forma de RUT y DV valido, celdas no vacias en columnas de nombre. No imprime valores.
import sys, re, openpyxl; sys.path.insert(0, "."); sys.stdout.reconfigure(encoding="utf-8")
from programas.rem_utils import rut_valido, norm
for p in sys.argv[1:]:
    wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
    for ws in wb.worksheets:
        filas = list(ws.iter_rows(values_only=True))
        if len(filas) < 2: continue
        rut = sum(1 for f in filas for v in f if v is not None and rut_valido(v))
        rut_ej = sum(1 for f in filas for v in f if v is not None and rut_valido(v) and norm(v).replace(".","") in ("11111111-1",))
        hi = next((i for i,f in enumerate(filas) if sum(v not in (None,"") for v in f) >= 5), 0)
        hdr = [norm(h) for h in filas[hi]]
        nom = [i for i,h in enumerate(hdr) if any(k in h for k in ("NOMBRE","PACIENTE","APELLIDO","USUARIO","DIRECCION","TELEFONO"))]
        llenas = {filas[hi][i]: sum(1 for f in filas[hi+1:] if i < len(f) and f[i] not in (None,"")) for i in nom}
        print(f"{p.split('/')[-1]} :: {ws.title}: filas_datos={len(filas)-hi-1} ruts_DV_ok={rut} (de ellos 11111111-1: {rut_ej}) celdas_nombre/dir/tel_llenas={llenas}")
