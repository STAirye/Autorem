# -*- coding: utf-8 -*-
"""Los .xlsx de los scratchpads con scan_catalogo.escanear (el gate de binarios del
proyecto: el hook anti-RUT los SALTA). No imprime valores, solo tipo y conteo."""
import pathlib, sys

R = pathlib.Path(r"E:\git\Autorem")
sys.path.insert(0, str(R))
from tools.scan_catalogo import escanear

TMP = pathlib.Path(r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem")
limpios, sucios, rotos = [], [], []
for ses in sorted(TMP.iterdir()):
    base = ses / "scratchpad"
    if not base.is_dir():
        continue
    for f in sorted(base.rglob("*.xlsx")):
        try:
            hall = escanear(f)[0]
        except Exception as e:
            rotos.append((f, type(e).__name__))
            continue
        if hall:
            tipos = {}
            for t, *_ in hall:
                tipos[t] = tipos.get(t, 0) + 1
            sucios.append((f, tipos))
        else:
            limpios.append(f)

print("xlsx limpios:", len(limpios))
print("xlsx CON HALLAZGOS:", len(sucios))
for f, tipos in sucios:
    print("   %-52s %s" % (f.name[:52], tipos))
print("no escaneables:", len(rotos))
for f, e in rotos:
    print("   %-52s %s" % (f.name[:52], e))
