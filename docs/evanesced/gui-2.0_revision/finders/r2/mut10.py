"""Mutantes de la ronda 10: rompe cada guarda, corre SU test, restaura el archivo."""
import subprocess
import sys
from pathlib import Path

R = Path(r"E:\git\Autorem")
M = [
    ("modulos/rem_sp_p6_poblacion.py", "if len(P) and not base.any():", "if False:",
     "tests/test_sp_p6.py", "base_vacia"),
    ("programas/poblacion.py", 'if not out["RUN"]:', "if False:",
     "tests/test_sp_p6.py", "base_vacia"),
    ("modulos/rem_a23_respiratorio.py", 'if not fer["Pertenece a SALA"].eq("SI").any():', "if False:",
     "tests/test_a23.py", "sala_vacia"),
    ("modulos/rem_a23_respiratorio.py",
     'for nombre, falt in od.attrs.get("condiciones_incompletas", {}).items():',
     "for nombre, falt in {}.items():", "tests/test_a23.py", "sala_vacia"),
    ("modulos/rem_a23_respiratorio.py",
     "if not any(c.get(ks[0]) for ks in _OTROS_CONDICIONES.values()):", "if False:",
     "tests/test_a23.py", "sala_vacia"),
    ("modulos/rem_a23_respiratorio.py", 'requeridas=("FECHA", "TIPO", "INSTR", "ANOS"))',
     'requeridas=("FECHA",))', "tests/test_a23.py", "sala_vacia"),
    ("modulos/rem_a23_respiratorio.py", 'out.attrs["sin_edad"] = int(edad.isna().sum())',
     'out.attrs["sin_edad"] = 0', "tests/test_a23.py", "sala_vacia"),
    ("modulos/rem_a03_d3_instrumentos.py",
     "elif detectado is not None and detectado != instrumento:", "elif False:",
     "tests/test_screening.py", "casillero_cruzado"),
    ("modulos/rem_a03_d3_instrumentos.py", "if filas and len(fuera_rango) == len(filas):",
     "if False:", "tests/test_screening.py", "casillero_cruzado"),
    ("modulos/rem_a03_d3_instrumentos.py", "    if fuera_rango:\n        avisos.append(",
     "    if False:\n        avisos.append(", "tests/test_screening.py", "casillero_cruzado"),
    ("modulos/rem_sm_rescate_inasistentes.py",
     'if k in insc.attrs.get("columnas_ausentes", ())]', "if False]",
     "tests/test_rescate_inasistentes.py", "pasivacion"),
    ("programas/poblacion.py", 'sin_run = d["RUN"].isin(("", "None", "nan"))',
     'sin_run = d["RUN"].isin(("",))', "tests/test_rescate_inasistentes.py", "ningun_run"),
    ("programas/poblacion.py", "{n_resp} 'RUN Responsable'", "'RUN Responsable'",
     "tests/test_rescate_inasistentes.py", "ningun_run"),
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
    print(("CAZADO " if ok else "VIVO   ") + rel + " :: " + viejo[:60])
print(f"{cazados}/{len(M)} cazados")
