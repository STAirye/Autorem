import subprocess, sys
from pathlib import Path
T = lambda t: [sys.executable, "-W", "ignore", f"tests/{t}.py"]
CF = [sys.executable, "tools/check_fuentes.py", "--todo"]
M = [
 ("PADDS fuera de Activo 12m", "programas/poblacion.py", '    "dependencia severa con diagnostico de demencia",\n', "", T("test_sp_p6")),
 ("NSP admin: sin FECHA CITA", "modulos/rem_a23_respiratorio.py", ', ("exact", "FECHA CITA")]', "]", T("test_a23")),
 ("NSP admin: EDAD sin edad_anios", "modulos/rem_a23_respiratorio.py", '    d["ANOS"] = d["ANOS"].map(edad_anios)', "    pass", T("test_a23")),
 ("Otros admin: sin RUT", "modulos/rem_a23_respiratorio.py", ' or exacto("RUT")', "", T("test_a23")),
 ("Otros admin: estamento no se busca en el ADA", "modulos/rem_a23_respiratorio.py", '    if "PROF" in aten.columns:', "    if False:", T("test_a23")),
 ("Otros: sin estamento para nadie no falla", "modulos/rem_a23_respiratorio.py", "    if quedan.all():", "    if False:", CF),
 ("Otros: sin aviso de desconocidos", "modulos/rem_a23_respiratorio.py", "    if not quedan.any():\n        return []", "    if True:\n        return []", T("test_a23")),
 ("estrat invalida sin opcional()", "modulos/rem_a23_respiratorio.py", '            with opcional("estrat"):', "            if True:", T("test_a23")),
 ("TRANS vuelve a callarse", "modulos/rem_sm_actividades.py", '        with opcional("inscritos"):\n            tmap = trans_map(inscritos)', "        try:\n            tmap = trans_map(inscritos)\n        except ValueError:\n            tmap = {}", T("test_sm_actividades")),
 ("sin_opcional no quita el archivo", "gui/runner.py", '    nuevo[inp["key"]] = [] if inp.get("multi") else None', "    pass", T("test_gui_registro")),
 ("pagina A23 no anota el omitido", "gui/paginas/a23.py", 'fer.attrs.setdefault("avisos", []).extend(avisos_descartados(ctx))', "None", T("test_gui_registro")),
 ("sin_opcional ofrece omitir un obligatorio", "gui/runner.py", '\n                and not i.get("obligatorio")), None)', "), None)", T("test_gui_registro")),
]
ok = 0
for nombre, f, a, b, cmd in M:
    p = Path(f); orig = p.read_bytes().decode("utf-8")
    aa, bb = (a.replace("\n", "\r\n"), b.replace("\n", "\r\n")) if "\r\n" in orig else (a, b)
    if aa not in orig:
        print(f"?? {nombre}: no encuentro el texto"); continue
    p.write_bytes(orig.replace(aa, bb, 1).encode("utf-8"))
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    finally:
        p.write_bytes(orig.encode("utf-8"))
    ok += r.returncode != 0
    print(f"{'MUERE ' if r.returncode else 'VIVE!!'} {nombre}")
print(f"{ok}/{len(M)} mutantes muertos")
