"""Mutantes de la ronda 9: re-rompe cada guarda, corre su test, restaura SIEMPRE."""
import subprocess, sys
from pathlib import Path
R = Path(r"E:\git\Autorem")
M = [
    ("1a a03 momento todo", "modulos/rem_a03_d3_instrumentos.py", "    if filas and sin_momento == len(filas):", "    if False:",
     "tests/test_screening.py", "sin_momento_o_sin_puntaje"),
    ("1b a03 momento parcial", "modulos/rem_a03_d3_instrumentos.py", "    if sin_momento:\n", "    if False:\n",
     "tests/test_screening.py", "sin_momento_o_sin_puntaje"),
    ("2a pob preguntas todas", "programas/poblacion.py", "    if len(faltan) == len(QUESTIONS):", "    if False:",
     "tests/test_sp_p6.py", "preguntas_ausentes"),
    ("2b pob preguntas algunas", "programas/poblacion.py", '    for nombre, faltan in (form.attrs.get("preguntas_faltantes") or {}).items():',
     "    for nombre, faltan in {}.items():", "tests/test_sp_p6.py", "preguntas_ausentes"),
    ("3a grid aviso SM", "modulos/rem_sm_actividades.py", "    if _av:\n        avisos.append(_av)\n    E.attrs", "    if False:\n        avisos.append(_av)\n    E.attrs",
     "tests/test_sm_actividades.py", "fuera_del_grid"),
    ("3b grid aviso A03", "modulos/rem_a03_d3_instrumentos.py", "    if _av:\n        avisos.append(_av)", "    if False:\n        avisos.append(_av)",
     "tests/test_screening.py", "sin_momento_o_sin_puntaje"),
    ("4 a03 banda RAYEN", "modulos/rem_a03_d3_instrumentos.py", "            nivel_d3 = banda_rayen\n", "            pass\n",
     "tests/test_screening.py", "sin_momento_o_sin_puntaje"),
    ("5a otros INSTR requerida", "modulos/rem_a23_respiratorio.py", 'requeridas=("RUN", "FECHA", "INSTR"))', "requeridas=None)",
     "tests/test_a23.py", "otros_sin_medico"),
    ("5b otros sin medico", "modulos/rem_a23_respiratorio.py", '        if not od["_med"].any():', "        if False:",
     "tests/test_a23.py", "otros_sin_medico"),
    ("6 pob ADA sin SM", "programas/poblacion.py", "    if len(en_ventana) and not _runs_actividad_sm(d_ada, ini13, corte):", "    if False:",
     "tests/test_sp_p6.py", "preguntas_ausentes"),
    ("7 a23 nada respiratorio", "modulos/rem_a23_respiratorio.py", '    if not any(fer[c].eq("SI").any() for c in fer.columns if c.startswith("REMA23")):', "    if False:",
     "tests/test_a23.py", "sin_nada_respiratorio"),
    ("8 dotacion sin funcionario", "gui/dialogos.py", "    elif len(ev) == 0:", "    elif False:",
     "tests/test_gui_registro.py", "nada_tributa"),
    ("9 tp maestro sin cobertura", "modulos/rem_sm_trabajo_perdido.py", "    if rem_map and len(dm) and not en_maestro.any():", "    if False:",
     "tests/test_trabajo_perdido.py", "maestro_que_no_reconoce"),
]
res = []
for etq, f, old, new, test, k in M:
    p = R / f
    orig = p.read_bytes()
    txt = orig.decode("utf-8")
    if "\r\n" in txt:
        old, new = old.replace("\n", "\r\n"), new.replace("\n", "\r\n")
    assert txt.count(old) == 1, (etq, txt.count(old))
    try:
        p.write_bytes(txt.replace(old, new).encode("utf-8"))
        r = subprocess.run([sys.executable, "-W", "ignore", "-m", "pytest", "-q", "-p", "no:cacheprovider",
                            test, "-k", k], cwd=R, capture_output=True, text=True)
        cazado = r.returncode != 0
    finally:
        p.write_bytes(orig)
    res.append((etq, cazado))
    print(("CAZADO " if cazado else "VIVO   ") + etq, flush=True)
print(f"{sum(c for _, c in res)}/{len(res)} cazados")
