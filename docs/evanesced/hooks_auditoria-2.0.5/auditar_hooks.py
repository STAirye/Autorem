"""Auditoria de los pre-commit: buscar la misma falla que check_version tenia --
una referencia a mano (patron, nombre de funcion, ruta) que dejo de apuntar a algo
real y por lo tanto DEJO DE VIGILAR, sin fallar."""
import ast
import sys
from pathlib import Path

RAIZ = Path(r"C:\Users\simon.tobar\Dr tobar\AutoREM")
sys.path.insert(0, str(RAIZ))

from tools import check_fuentes as CF

problemas = []


def funciones_de(rel):
    p = RAIZ / rel
    if not p.is_file():
        return None
    return {n.name for n in ast.walk(ast.parse(p.read_text(encoding="utf-8")))
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}


print("=" * 70)
print("check_fuentes: TRANSVERSALES y EXENTOS nombran funciones a mano")
print("=" * 70)
for etiqueta, coleccion in (("TRANSVERSALES", CF.TRANSVERSALES), ("EXENTOS", CF.EXENTOS)):
    for clave in sorted(coleccion):
        rel, _, fn = clave.partition("::")
        fns = funciones_de(rel)
        if fns is None:
            problemas.append(f"{etiqueta}: {clave} -> el ARCHIVO no existe")
            print(f"  MUERTO   {clave}  (archivo ausente)")
        elif fn not in fns:
            problemas.append(f"{etiqueta}: {clave} -> la FUNCION no existe")
            print(f"  MUERTO   {clave}  (funcion ausente)")
        else:
            print(f"  ok       {clave}")

print()
print("=" * 70)
print("check_fuentes: CARPETAS vigiladas")
print("=" * 70)
for c in CF.CARPETAS:
    print(f"  {'ok      ' if (RAIZ / c).is_dir() else 'MUERTO  '} {c}/")
fuera = [d.name for d in RAIZ.iterdir()
         if d.is_dir() and d.name not in CF.CARPETAS
         and d.name in ("tools", "catalogos", "legacy")]
print(f"  (fuera de vigilancia a proposito: {', '.join(fuera)})")

print()
print("=" * 70)
print("check_fuentes: LECTORES vs lo que el codigo REALMENTE llama")
print("=" * 70)
# Cualquier llamada cuyo nombre huela a lectura de planilla y NO este en LECTORES
SOSPECHOSAS = ("read_excel", "read_csv", "load_workbook", "ExcelFile", "open_workbook",
               "read_table", "calamine", "readlines", "leer_", "cargar_", "abrir_")
vistos = {}
for carpeta in CF.CARPETAS:
    for py in (RAIZ / carpeta).rglob("*.py"):
        try:
            arbol = ast.parse(py.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for n in ast.walk(arbol):
            if isinstance(n, ast.Call):
                nombre = getattr(n.func, "attr", getattr(n.func, "id", None))
                if nombre and any(s in nombre for s in SOSPECHOSAS):
                    vistos.setdefault(nombre, set()).add(py.relative_to(RAIZ).as_posix())
for nombre in sorted(vistos):
    marca = "ok      " if nombre in CF.LECTORES else "NO VIGILADO"
    print(f"  {marca} {nombre}  ({len(vistos[nombre])} archivo/s)")

print()
print("=" * 70)
print(f"RESUMEN: {len(problemas)} referencia(s) muerta(s)")
for p in problemas:
    print("  -", p)
