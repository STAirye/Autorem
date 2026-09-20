import subprocess, sys
from pathlib import Path
RAW = "load_workbook(X, read_only=True, data_only=True)"
M = [
 ("M1 sin reset_dimensions", "programas/rem_utils.py",
  "    for ws in wb.worksheets:\n        ws.reset_dimensions()\n    return wb", "    return wb", ["ff"]),
 ("M2 a05 read_only pelado", "gui/paginas/a05.py",
  "        wb = abrir_xlsx_ro(ruta)", "        import openpyxl; wb = openpyxl.load_workbook(ruta, read_only=True, data_only=True)", ["gui"]),
 ("M3 sm _header_rapido pelado", "gui/paginas/sm.py",
  "    wb = abrir_xlsx_ro(ruta)", "    import openpyxl; wb = openpyxl.load_workbook(ruta, read_only=True, data_only=True)", ["gui"]),
 ("M4 catalogos._hojas pelado", "programas/catalogos.py",
  "    wb = abrir_xlsx_ro(entrada)", "    import openpyxl; wb = openpyxl.load_workbook(entrada, read_only=True, data_only=True)", ["ff"]),
 ("M5 scan pelado", "tools/scan_catalogo.py",
  "    wb = abrir_xlsx_ro(ruta)", "    import openpyxl; wb = openpyxl.load_workbook(ruta, read_only=True, data_only=True)", ["ff"]),
 ("M6 fuente solo del primero", "programas/rem_utils.py",
  "for n, c in cols_por_archivo]", "for n, c in cols_por_archivo[:1]]", ["ff"]),
 ("M7 a05 sin limpiar comillas", "gui/paginas/a05.py",
  "        return runner.limpiar_ruta(var_ruta.get())", "        return var_ruta.get().strip()", ["gui"]),
 ("M8 sin exigir_estamento", "programas/rem_utils.py",
  "    exigir_estamento(d)\n    return d", "    return d", ["dot"]),
 ("M9 verificar_hoja_unica pelado", "programas/rem_utils.py",
  "    wb = abrir_xlsx_ro(entrada)\n    con_datos", "    wb = openpyxl.load_workbook(entrada, data_only=True, read_only=True)\n    con_datos", ["ff"]),
 ("M10 aviso ignora archivos", "programas/formatos.py",
  "              if archivos else \"\")", "              if False else \"\")", ["ff"]),
]
CMD = {"ff": [sys.executable, "-m", "pytest", "-q", "tests/test_formatos_fuente.py"],
       "gui": [sys.executable, "tests/test_gui_construccion.py"],
       "dot": [sys.executable, "tests/test_dotacion.py"]}
for nombre, f, viejo, nuevo, suites in M:
    p = Path(f); orig = p.read_bytes(); crlf = b"\r\n" in orig
    t = orig.decode().replace("\r\n", "\n")
    assert t.count(viejo) == 1, (nombre, t.count(viejo))
    m = t.replace(viejo, nuevo)
    p.write_bytes((m.replace("\n", "\r\n") if crlf else m).encode())
    try:
        for s in suites:
            r = subprocess.run(CMD[s], capture_output=True, text=True, errors="replace")
            out = (r.stdout + r.stderr).strip().splitlines()
            fallos = [l for l in out if "FAIL" in l or l.startswith("FAILED")]
            print(f"{nombre:32s} [{s}] rc={r.returncode} -> {out[-1][:60] if out else ''}")
            for l in fallos[:4]: print("      ", l[:130])
    finally:
        p.write_bytes(orig)
