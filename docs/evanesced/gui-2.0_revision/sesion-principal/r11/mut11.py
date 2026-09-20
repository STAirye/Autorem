import subprocess, sys
from pathlib import Path
T = lambda t: [sys.executable, "-W", "ignore", f"tests/{t}.py"]
CF = [sys.executable, "tools/check_fuentes.py", "--todo"]
M = [
 ("A05 sin firma de contenido", "programas/rem_saludmental.py", "    verificar_formulario_sm(headers)   # por CONTENIDO", "    pass  # ", T("test_autorem")),
 ("P6 sin firma de contenido", "programas/poblacion.py", "    verificar_formulario_sm(headers, nombre)", "    pass  # ", T("test_autorem")),
 ("ffill global (sin ATENID)", "programas/rem_utils.py", "dd.groupby(aten).ffill()", "dd.ffill()", T("test_a23")),
 ("AND fila por fila", "modulos/rem_a23_respiratorio.py", "    A, D, I, T = _act_de_la_atencion(d), d[", "    A, D, I, T = d[\"ACT_n\"], d[", T("test_a23")),
 ("literal DAX muerto", "programas/poblacion.py", '"visita domiciliaria integral familia con integrante con problema de salud mental",', '"visita domiciliaria integral familia con integrante con patologia de salud mental",', T("test_refs_tablas")),
 ("fallback estrat CONDICIONES", "modulos/rem_a23_respiratorio.py", '    i_dg = indice_col(hn, "DETALLE", "DIAGNOSTICOS")\n', '    i_dg = indice_col(hn, "DETALLE", "DIAGNOSTICOS")\n    i_dg = i_dg if i_dg is not None else indice_col(hn, "CONDICIONES CRONICAS")\n', T("test_a23")),
 ("atenciones sin guarda RUN", "programas/rem_utils.py", "        if huerfanas == len(d):", "        if False:", CF),
 ("otros sin guarda RUN", "modulos/rem_a23_respiratorio.py", '    if not d["RUN"].map(norm).ne("").any():', "    if False:", CF),
 ("estrat sin guarda RUT", "modulos/rem_a23_respiratorio.py", "    filas = [f for f in filas if f[i_rut] not in (None, \"\")]\n    if not filas:", "    if False:", CF),
 ("trans_map sin guarda RUN", "programas/rem_utils.py", "    filas = [f for f in filas if i_run < len(f) and str(f[i_run] or \"\").strip()]\n    if not filas:", "    if False:", CF),
 ("multiprof sin guarda ATEN", "programas/rem_utils.py", "    filas = [f for f in filas if i_aten < len(f) and str(f[i_aten] or \"\").strip()]\n    if not filas:", "    if False:", CF),
 ("limpiar corta 2o piso", "tools/limpiar_refs.py", "    fin = h\n    for rng in combinadas:", "    return h\n    for rng in combinadas:", T("test_refs_tablas")),
 ("limpiar no escanea", "tools/limpiar_refs.py", "        hall = _hallazgos(tmp)", "        hall = {}", T("test_refs_tablas")),
 ("limpiar sin __future__", "tools/limpiar_refs.py", "from __future__ import annotations", "import os", T("test_refs_tablas")),
 ("vuelve el hardcode", "programas/rem_utils.py", "            return r, \"ancla\"\n    raise ArchivoInvalido(", "            return r, \"ancla\"\n    return 9, \"hardcode\"\n    raise ArchivoInvalido(", T("test_autorem")),
]
ok = 0
for nombre, f, a, b, cmd in M:
    p = Path(f); orig = p.read_text(encoding="utf-8")
    if a not in orig:
        print(f"?? {nombre}: no encuentro el texto a mutar"); continue
    p.write_text(orig.replace(a, b, 1), encoding="utf-8")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    finally:
        p.write_text(orig, encoding="utf-8")
    muerto = r.returncode != 0
    ok += muerto
    print(f"{'MUERE ' if muerto else 'VIVE!!'} {nombre}")
print(f"{ok}/{len(M)} mutantes muertos")
