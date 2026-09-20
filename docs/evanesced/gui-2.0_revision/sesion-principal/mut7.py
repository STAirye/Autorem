import subprocess, sys
from pathlib import Path
M = [
 ("N1 verificar_hoja_unica sin finally", "programas/rem_utils.py",
  "                            for row in ws.iter_rows(values_only=True))]\n    finally:\n        wb.close()",
  "                            for row in ws.iter_rows(values_only=True))]\n    finally:\n        pass", ["ff"]),
 ("N2 escribir_atomico directo", "programas/rem_utils.py",
  "        escribir(tmp)\n        os.replace(tmp, salida)", "        escribir(salida)", ["aut"]),
 ("N3 escribir_atomico no limpia", "programas/rem_utils.py",
  "        try:\n            tmp.unlink()\n        except OSError:\n            pass\n        raise",
  "        raise", ["aut"]),
 ("N4 a05 save directo", "autorem.py",
  "    escribir_atomico(salida, wb.save)", "    wb.save(salida)", ["aut"]),
 ("N5 sm actividades directo", "gui/paginas/sm.py",
  "        escribir_atomico(salida, lambda p: smact.escribir(E, p))", "        smact.escribir(E, salida)", ["reg"]),
 ("N6 sm tp directo", "gui/paginas/sm.py",
  "            escribir_atomico(salida_tp, lambda p: tpmod.escribir(Etp, p))", "            tpmod.escribir(Etp, salida_tp)", ["reg"]),
 ("N7 a23 directo", "gui/paginas/a23.py",
  "    escribir_atomico(salida, lambda p: a23.escribir(fer, p))", "    a23.escribir(fer, salida)", ["reg"]),
 ("N8 p6 directo", "gui/paginas/poblacion.py",
  "    escribir_atomico(salida, lambda p: p6.escribir(P, resultado, p))", "    p6.escribir(P, resultado, salida)", ["reg"]),
 ("N9 sin protocol", "gui/app.py",
  "        self.protocol(\"WM_DELETE_WINDOW\", self._al_cerrar)\n", "", ["gui"]),
 ("N10 no cuenta la corrida", "gui/app.py",
  "            self._corridas += 1\n", "", ["gui"]),
 ("N11 no descuenta", "gui/app.py",
  "                self._corridas -= 1   #", "                pass   #", ["gui"]),
 ("N12 cierra sin preguntar", "gui/app.py",
  "        if self._corridas and not messagebox.askyesno(", "        if False and not messagebox.askyesno(", ["gui"]),
]
CMD = {"gui": [sys.executable, "tests/test_gui_construccion.py"],
       "reg": [sys.executable, "tests/test_gui_registro.py"],
       "aut": [sys.executable, "tests/test_autorem.py"],
       "ff": [sys.executable, "-m", "pytest", "-q", "tests/test_formatos_fuente.py"]}
for nombre, f, viejo, nuevo, suites in M:
    p = Path(f); orig = p.read_bytes(); crlf = b"\r\n" in orig
    t = orig.decode("utf-8").replace("\r\n", "\n")
    assert t.count(viejo) == 1, (nombre, t.count(viejo))
    m = t.replace(viejo, nuevo)
    p.write_bytes((m.replace("\n", "\r\n") if crlf else m).encode("utf-8"))
    try:
        for s in suites:
            r = subprocess.run(CMD[s], capture_output=True, text=True, encoding="utf-8", errors="replace")
            out = (r.stdout + r.stderr).strip().splitlines()
            fallos = [l for l in out if l.startswith(("FAIL", "ERROR"))]
            print(f"{nombre:36s} [{s}] rc={r.returncode}")
            for l in fallos[:3]: print("      ", l[:150])
    finally:
        p.write_bytes(orig)
