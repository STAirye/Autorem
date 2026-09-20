import subprocess, sys
R = r"E:\git\Autorem"
M = [
 ("gui/dialogos.py", "    cambios = decisiones_cambiadas({n: v.get() for n, v in checks.items()}, tabla)",
  "    cambios = {n: v.get() for n, v in checks.items()}", ["tests/test_gui_construccion.py"]),
 ("gui/dialogos.py", "            if dotacion.clase(n, tabla) != (dotacion.EXTERNO if ext else dotacion.INTERNO)}",
  "            if (dotacion.clase(n, tabla) == dotacion.EXTERNO) != ext}", ["tests/test_gui_registro.py", "tests/test_gui_construccion.py"]),
 ("programas/catalogos.py", "    entrada = entrada or _SESION.get(nombre)\n", "\n", ["tests/test_catalogos.py"]),
 ("programas/catalogos.py", "        if previo is not None:\n            _SESION[nombre] = previo\n", "        pass\n", ["tests/test_catalogos.py"]),
 ("programas/catalogos.py", "    if entrada and not Path(entrada).exists():", "    if False:", ["tests/test_catalogos.py"]),
 ("programas/catalogos.py", "    previo = _SESION.pop(nombre, None)", "    previo = _SESION.get(nombre)", ["tests/test_catalogos.py"]),
]
for i, (f, a, b, tests) in enumerate(M, 1):
    p = f"{R}/{f}"; orig = open(p, encoding="utf-8").read()
    assert orig.count(a) == 1, (i, a)
    open(p, "w", encoding="utf-8").write(orig.replace(a, b))
    try:
        out = [subprocess.run([sys.executable, t], cwd=R, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout for t in tests]
        fails = [l for o in out for l in o.splitlines() if l.startswith(("FAIL", "ERROR"))]
        print(f"M{i}", "CAZADO" if fails else "VIVO", *[x[:110] for x in fails], sep="\n   ")
    finally:
        open(p, "w", encoding="utf-8").write(orig)
