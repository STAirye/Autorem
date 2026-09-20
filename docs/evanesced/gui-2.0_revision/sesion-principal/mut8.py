import subprocess, sys
from pathlib import Path
R = Path(r"E:\git\Autorem")
MUT = [
 ("slim: lista a mano sin <exe>/catalogos", "programas/catalogos.py",
  'cands = [c / "maestro_slim.csv.gz" for c in _carpetas()]',
  'cands = [c / "maestro_slim.csv.gz" for c in _carpetas() if "exe_slim" not in str(c)]',
  "tests/test_catalogos.py", "test_maestro_slim"),
 ("runner con copia propia", "gui/runner.py",
  "    from programas.catalogos import maestro_slim\n    return maestro_slim()",
  "    return str(Path(__file__).resolve().parent.parent / 'catalogos' / 'maestro_slim.csv.gz')",
  "tests/test_catalogos.py", "test_maestro_slim"),
 ("sin validar Cupos", "gui/paginas/sm.py",
  'if a03["incluir"] and a03["instrumentos"] and a03["est_ruta"]:',
  'if False:', "tests/test_gui_registro.py", "test_sm_valida_la_ruta"),
 ("header criterio a mano", "gui/paginas/sm.py",
  "return list(filas[indice_encabezado(filas, max_scan=max_scan)]) if filas else []",
  "return next((list(r) for r in filas if sum(v not in (None, '') for v in r) > 3), list(filas[0]) if filas else [])",
  "tests/test_gui_registro.py", "test_el_preview_de_cruce"),
 ("revisar calla el aborto", "gui/dialogos.py",
  "with _una_ventana_dotacion(log, messagebox) as libre:\n        if libre:",
  "with _una_ventana_dotacion(None, messagebox) as libre:\n        if libre:",
  "tests/test_gui_registro.py", "test_un_click"),
]
for nombre, f, a, b, test, clave in MUT:
    p = R / f; orig = p.read_text(encoding="utf-8")
    assert orig.count(a) == 1, (nombre, orig.count(a))
    p.write_text(orig.replace(a, b), encoding="utf-8")
    try:
        out = subprocess.run([sys.executable, str(R / test)], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=R).stdout
    finally:
        p.write_text(orig, encoding="utf-8")
    fallas = [l for l in out.splitlines() if l.startswith(("FAIL", "ERROR"))]
    print(("CAZADO " if fallas else "VIVO   ") + nombre, "|", fallas[:2])
