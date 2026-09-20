"""Mutantes de la ronda 9: re-rompe cada guarda, corre su test, restaura SIEMPRE."""
import subprocess, sys
from pathlib import Path
R = Path(r"E:\git\Autorem")
M = [
    ("1a G: sin respaldo de edad ADA", "modulos/rem_a23_respiratorio.py", "    if edad_extra is not None:\n", "    if False:\n",
     "tests/test_a23.py", "no_descarta_callado"),
    ("1b G: descarta callado", "modulos/rem_a23_respiratorio.py", "                m, dd = _UMBRAL_ADULTO\n            else:",
     "                continue\n            else:", "tests/test_a23.py", "no_descarta_callado"),
    ("2 pob: posterior al corte", "programas/poblacion.py", "        if _ym(fmin) > _ym(corte):", "        if False:",
     "tests/test_sp_p6.py", "fuente_vacia_tras_el_corte"),
    ("3 pob: sin fechas", "programas/poblacion.py", "        if fmin is None:", "        if False:",
     "tests/test_sp_p6.py", "fuente_vacia_tras_el_corte"),
    ("4 sm: E vacio", "modulos/rem_sm_actividades.py", "    if len(E) == 0:", "    if False:",
     "tests/test_sm_actividades.py", "nada_que_tribute"),
    ("5a otros: sin fechas", "modulos/rem_a23_respiratorio.py", '    if not d["FECHA"].notna().any():', "    if False:",
     "tests/test_a23.py", "otros_cronicos_sin_fechas"),
    ("5b otros: to_datetime pelado", "modulos/rem_a23_respiratorio.py",
     'd["FECHA"] = fecha_col(d["FECHA"], log, "FECHA ATENCION (Otros Cronicos)")',
     'd["FECHA"] = pd.to_datetime(d["FECHA"], errors="coerce", dayfirst=True)',
     "tests/test_a23.py", "otros_cronicos_sin_fechas"),
    ("6 resumen sin avisos", "gui/paginas/poblacion.py", '    avisos = P.attrs.get("avisos") or []', "    avisos = []",
     "tests/test_sp_p6.py", "resumen_de_poblacion"),
    ("7a asiste toda rara", "modulos/rem_sm_actividades.py", "        if not reconocido.any():", "        if False:",
     "tests/test_sm_actividades.py", "asiste_sin_si_ni_no"),
    ("7b asiste parcial", "modulos/rem_sm_actividades.py", "        if n_raro:", "        if False:",
     "tests/test_sm_actividades.py", "asiste_sin_si_ni_no"),
    ("8 dotacion log", "gui/dialogos.py", "    elif len(trib) == 0:", "    elif False:",
     "tests/test_gui_registro.py", "nada_tributa"),
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
