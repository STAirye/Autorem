# -*- coding: utf-8 -*-
"""Escanea los .py/.md/.txt de los scratchpads con el gate del propio proyecto ANTES de
copiar nada al repo: RUT con DV valido (hook_pre_commit_rut.sospechosos), email y
telefono (scan_catalogo). No imprime el dato, solo el tipo y donde."""
import pathlib, sys

R = pathlib.Path(r"E:\git\Autorem")
sys.path.insert(0, str(R))
from tools.hook_pre_commit_rut import sospechosos
from tools.scan_catalogo import EMAIL, FONO

TMP = pathlib.Path(r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem")
SESIONES = {
    "648a107e-f033-4d56-a55d-a415a58f003e": "finders",
    "a40108ff-012a-4b37-baf2-2a1dc332a634": "sesion-principal",
    "5e2e5aba-a08c-409d-820f-4f7d939a0000": "prompts",
    "5e2e5aba-a08c-409d-820f-4f7d933a0000": "prompts",
}
# la carpeta de prompts real (evito tipear mal el uuid)
for d in TMP.iterdir():
    if d.name.startswith("5e2e5aba"):
        SESIONES[d.name] = "prompts"

total = sucios = 0
limpios = []
for ses, etiqueta in SESIONES.items():
    base = TMP / ses / "scratchpad"
    if not base.is_dir():
        continue
    for f in sorted(base.rglob("*")):
        if not f.is_file() or f.suffix.lower() not in (".py", ".md", ".txt"):
            continue
        total += 1
        try:
            txt = f.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            print("  NO LEIBLE", f.name, e)
            continue
        hall = []
        r = sospechosos(txt)
        if r:
            hall.append("RUT x%d" % len(r))
        if EMAIL.findall(txt):
            hall.append("EMAIL x%d" % len(EMAIL.findall(txt)))
        fonos = [m for m in FONO.findall(txt)]
        if fonos:
            hall.append("FONO x%d" % len(fonos))
        if hall:
            sucios += 1
            print("  SUCIO  %-14s %-34s %s" % (etiqueta, f.name, ", ".join(hall)))
        else:
            limpios.append((etiqueta, f))

print("\ntexto escaneado: %d | con hallazgos: %d | limpios: %d" % (total, sucios, len(limpios)))
salida = pathlib.Path(__file__).with_name("limpios.txt")
salida.write_text("\n".join("%s\t%s" % (e, f) for e, f in limpios), encoding="utf-8")
print("lista de limpios ->", salida)
