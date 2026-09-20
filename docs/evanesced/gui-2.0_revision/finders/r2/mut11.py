"""Mutantes de la 2a pasada de la ronda 10: rompe cada guarda, corre SU test, restaura."""
import subprocess
import sys
from pathlib import Path

R = Path(r"E:\git\Autorem")
M = [
    ("programas/poblacion.py", '("INSTRUMENTO", instr_col_i)) if not c]', '("INSTRUMENTO", 1)) if not c]',
     "tests/test_sp_p6.py", "sin_instrumento"),
    ("modulos/rem_sp_p6_poblacion.py", 'elif r["_edad_grid"] is None:', "elif False:",
     "tests/test_sp_p6.py", "sin_instrumento"),
    ("programas/rem_saludmental.py", "if filas_con_rut and filas_fecha_mala == filas_con_rut:",
     "if False:", "tests/test_autorem.py", "ninguna_fecha"),
    ("modulos/rem_a23_respiratorio.py", "    if i_dg is None:\n        # Sin diagnosticos",
     "    if False:\n        # Sin diagnosticos", "tests/test_a23.py", "estratificacion_sin"),
    ("modulos/rem_a23_respiratorio.py", "    if i_dg is None:   # `is None`",
     "    if not i_dg:   # `is None`", "tests/test_a23.py", "estratificacion_sin"),
    ("programas/estamentos.py", "    if not tabla:\n", "    if False:\n",
     "tests/test_estamentos.py", "sin_estamentos"),
    ("gui/paginas/a23.py", "{widgets.texto_avisos(fer.attrs.get('avisos'))}", "",
     "tests/test_gui_registro.py", "resumen_de_a23"),
    ("gui/paginas/sm.py", "{rtxt}{widgets.texto_avisos(avisos)}", "{rtxt}",
     "tests/test_gui_registro.py", "resumen_de_a23"),
    ("gui/paginas/sm.py", 'res["avisos_a03"] = r03.get("avisos", [])', 'res["avisos_a03"] = []',
     "tests/test_gui_registro.py", "desglose_por_instrumento"),
    ("gui/paginas/sm.py", ".{widgets.texto_avisos(res.get('avisos_a03'))}", ".",
     "tests/test_gui_registro.py", "resumen_de_a23"),
]
cazados = 0
for rel, viejo, nuevo, test, k in M:
    p = R / rel
    orig = p.read_bytes()
    s = orig.decode("utf-8")
    nl = "\r\n" if "\r\n" in s else "\n"
    v, n = viejo.replace("\n", nl), nuevo.replace("\n", nl)
    assert s.count(v) == 1, (rel, viejo, s.count(v))
    try:
        p.write_bytes(s.replace(v, n).encode("utf-8"))
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:warnings",
                            "-p", "no:cacheprovider", test, "-k", k],
                           cwd=R, capture_output=True, text=True)
        ok = r.returncode != 0
    finally:
        p.write_bytes(orig)
    cazados += ok
    print(("CAZADO " if ok else "VIVO   ") + rel + " :: " + viejo[:60].replace("\n", " "))
print(f"{cazados}/{len(M)} cazados")
