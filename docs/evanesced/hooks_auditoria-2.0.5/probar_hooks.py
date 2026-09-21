"""Prueba FUNCIONAL de los tres pre-commit: darle a cada uno algo que DEBE cazar
y confirmar que lo caza. Un check que pasa siempre es un check que no sirve.

No escribe nada dentro del repo salvo un .py temporal para cp1252, que se borra.
El RUT de prueba se ARMA EN RUNTIME (cuerpo aritmetico + DV calculado): nunca hay
un literal con forma de RUT en disco (CLAUDE.md SS8.1).
"""
import ast
import subprocess
import sys
from pathlib import Path

RAIZ = Path(r"C:\Users\simon.tobar\Dr tobar\AutoREM")
sys.path.insert(0, str(RAIZ))

from tools import check_fuentes as CF
from tools import hook_pre_commit_rut as HR
from programas.rem_utils import dv_rut

ok = lambda b: "CAZADO" if b else "*** NO LO CAZA ***"

print("=" * 70)
print("1. anti-RUT: un RUT con DV valido")
print("=" * 70)
cuerpo = str(2 * 11000007)
rut_valido = f"{cuerpo}-{dv_rut(cuerpo)}"
rut_invalido = f"{cuerpo}-{'0' if dv_rut(cuerpo) != '0' else '9'}"
print(f"  RUT con DV bueno  -> {ok(bool(HR.sospechosos(rut_valido)))}")
print(f"  RUT con DV malo   -> {'dejado pasar (correcto)' if not HR.sospechosos(rut_invalido) else '*** FALSO POSITIVO ***'}")
print(f"  placeholder 11111111-1 -> {'dejado pasar (correcto)' if not HR.sospechosos('11111111-1') else '*** FALSO POSITIVO ***'}")

print()
print("=" * 70)
print("2. cp1252: un .py con una flecha Unicode")
print("=" * 70)
tmp = RAIZ / "tools" / "_zz_prueba_cp1252.py"
tmp.write_text('# -*- coding: utf-8 -*-\nprint("paso \u2192 siguiente")\n', encoding="utf-8")
try:
    r = subprocess.run([sys.executable, "tools/check_cp1252.py"], cwd=RAIZ,
                       capture_output=True, text=True, encoding="utf-8", errors="ignore")
    print(f"  exit={r.returncode} -> {ok(r.returncode != 0)}")
    for linea in (r.stdout or "").splitlines():
        if "_zz_prueba" in linea or "flecha" in linea.lower():
            print("   ", linea.strip())
finally:
    tmp.unlink()
r = subprocess.run([sys.executable, "tools/check_cp1252.py"], cwd=RAIZ,
                   capture_output=True, text=True, encoding="utf-8", errors="ignore")
print(f"  tras borrarlo: exit={r.returncode} (debe ser 0)")

print()
print("=" * 70)
print("3. check_fuentes: un lector SIN contrato")
print("=" * 70)
fuente = ("def cargar_cosa(ruta):\n"
          "    wb = load_workbook(ruta)\n"
          "    return list(filas_hoja(wb))\n"
          "\n"
          "def no_lee_nada(x):\n"
          "    return x + 1\n")
detectadas = CF._funciones(fuente)
for nombre, _, _, es_lector in detectadas:
    esperado = nombre == "cargar_cosa"
    marca = "ok" if es_lector == esperado else "*** MAL ***"
    print(f"  {marca}  {nombre}: es_lector={es_lector} (esperado {esperado})")

print()
print("  -- y el barrido completo del repo --")
r = subprocess.run([sys.executable, "tools/check_fuentes.py", "--todo"], cwd=RAIZ,
                   capture_output=True, text=True, encoding="utf-8", errors="ignore")
print(f"  exit={r.returncode}")
for linea in (r.stdout or "").splitlines()[-4:]:
    print("   ", linea.strip())
