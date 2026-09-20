# Diagnostico SIN valores de datos: conteos, tipos, merges, ListObjects y SOLO la fila de encabezado.
import sys, openpyxl; sys.path.insert(0,"tools"); sys.stdout.reconfigure(encoding="utf-8")
import limpiar_refs as L
from pathlib import Path
for f in sys.argv[1:]:
    p = Path("refs_tablas")/f
    wb = openpyxl.load_workbook(p)
    for ws in wb.worksheets:
        h = L._fila_header(ws)
        print(f"===== {f} :: {ws.title!r} max_row={ws.max_row} max_col={ws.max_column} header_elegido={h}")
        if ws.max_row <= 1 and ws.max_column <= 1: continue
        tope = (h or 10) + 3
        for r in range(1, tope + 1):
            row = [c.value for c in ws[r]]
            tipos = sorted({type(v).__name__ for v in row if v not in (None, "")})
            print(f"   r{r}: no_vacias={sum(v not in (None,'') for v in row)} tipos={tipos}")
        mer = [str(m) for m in ws.merged_cells.ranges if m.min_row <= tope]
        if mer: print("   merges arriba:", mer[:20], "..." if len(mer) > 20 else "")
        for t in ws.tables.values():
            print("   ListObject", t.name, t.ref, "cols:", [c.name for c in t.tableColumns])
        if h:
            print("   HEADER:", [c.value for c in ws[h]])
    wb.close()
