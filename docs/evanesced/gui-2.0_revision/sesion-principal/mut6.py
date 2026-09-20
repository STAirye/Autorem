import subprocess, sys
from pathlib import Path
M = [
 ("M1 dotacion_ada sin candado", "gui/dialogos.py",
  "    if _DOTACION_ABIERTA[0]:\n        log(", "    if False:\n        log(", ["reg"]),
 ("M2 revisar sin candado", "gui/dialogos.py",
  "    if _DOTACION_ABIERTA[0]:\n        return\n", "    if False:\n        return\n", ["reg"]),
 ("M3 wraplength doble escala", "gui/widgets.py",
  "wraplength=lbl._reverse_widget_scaling(max(e.width - 20, 50))", "wraplength=max(e.width - 20, 50)", ["gui"]),
 ("M4 banner ignora cambios en corrida", "gui/app.py",
  "cambiados = [k for k, v in inicio.items() if getters[k]() != v]", "cambiados = []", ["gui"]),
 ("M5 cruce sm sin canal", "gui/paginas/sm.py",
  "                       canal=canal)", "                       canal=None)", ["gui"]),
 ("M6 quitar no invalida", "gui/paginas/sm.py",
  "            canal.invalidar()   #", "            pass   #", ["gui"]),
 ("M7 en_hilo ignora canal", "gui/runner.py",
  "        if canal is not None and not canal.vigente(pedido):", "        if False:", ["gui"]),
 ("M8 a05 pisa salida", "autorem.py",
  "    salida, = rutas_libres(destino / (entrada.stem + \"_procesado\" + sufijo + \".xlsx\"))",
  "    salida = destino / (entrada.stem + \"_procesado\" + sufijo + \".xlsx\")", ["aut"]),
 ("M9 rutas_libres numero por archivo", "programas/rem_utils.py",
  "        if not any(c.exists() for c in cands):\n            return cands",
  "        if not any(c.exists() for c in cands) or n > 0:\n            return [r if not r.exists() else c for r, c in zip(rutas, cands)]", ["aut", "reg"]),
 ("M10 sm pisa salidas", "gui/paginas/sm.py",
  "    salidas = dict(zip(salidas, rutas_libres(*salidas.values())))", "", ["reg"]),
 ("M11 resumen calla fallo a03", "gui/paginas/sm.py",
  "                    res[\"fallo_a03\"] = str(e)\n", "", ["reg"]),
 ("M12 a23 pisa", "gui/paginas/a23.py",
  "    salida, = rutas_libres(ctx[\"carpeta\"] / f\"REM_A23_{y}_{m:02d}_procesado.xlsx\")",
  "    salida = ctx[\"carpeta\"] / f\"REM_A23_{y}_{m:02d}_procesado.xlsx\"", ["reg"]),
 ("M13 poblacion calla rescate", "gui/paginas/poblacion.py",
  "        fallo_rescate = str(e)", "        pass", ["reg"]),
]
CMD = {"gui": [sys.executable, "tests/test_gui_construccion.py"],
       "reg": [sys.executable, "tests/test_gui_registro.py"],
       "aut": [sys.executable, "tests/test_autorem.py"]}
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
            print(f"{nombre:38s} [{s}] rc={r.returncode}")
            for l in fallos[:4]: print("      ", l[:150])
    finally:
        p.write_bytes(orig)
