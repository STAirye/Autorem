# -*- coding: utf-8 -*-
"""Mutacion de la ronda 12: reintroduce cada bug corregido y exige que un test lo cace.
Cada mutante = (archivo, texto viejo -> texto nuevo, tests que DEBEN fallar)."""
import subprocess
import sys
from pathlib import Path

REPO = Path(r"E:\git\Autorem")
PY = sys.executable

MUT = [
    # 1. no_vacias: la guarda de la columna clave vacia, sobre el CONCATENADO (o ausente)
    ("programas/rem_utils.py",
     '        vacias = [k for k in no_vacias if not parte[k].map(norm).ne("").any()]',
     '        vacias = []',
     ["test_a23.py", "test_contratos_fuentes.py", "test_rescate_inasistentes.py"]),
    # 2. forma canonica de la atencion: volver al ffill por atencion (media normalizacion)
    ("programas/rem_utils.py",
     "    d = _una_fila_por_atencion(d, log)",
     "    pass",
     ["test_a23.py"]),
    # 2b. y el guard de ATENID repetido entre pacientes
    ("programas/rem_utils.py",
     "    if len(mezclados):",
     "    if False:",
     ["test_a23.py"]),
    # 3. opcional() atrapando ValueError de nuevo
    ("programas/rem_utils.py",
     "    except ArchivoInvalido as e:\n        raise OpcionalInvalido(entrada, e) from e",
     "    except (ArchivoInvalido, ValueError) as e:\n        raise OpcionalInvalido(entrada, e) from e",
     ["test_sm_actividades.py"]),
    # 4. los opcionales del A23, cargados al final (como antes)
    ("modulos/rem_a23_respiratorio.py",
     "    est = pd.Series(dtype=\"object\")\n    if estrat is not None:",
     "    est = pd.Series(dtype=\"object\")\n    d = cargar_atenciones(entrada, log=log)\n    if estrat is not None:",
     ["test_a23.py"]),
    # 5. A05: cachear la deteccion por ruta otra vez
    ("gui/paginas/a05.py",
     "        ruta = _ruta_caja()\n        if ruta:\n            try:\n                _aplicar(_leer_categoria(ruta), ruta)",
     "        ruta = _ruta_caja()\n        if ruta and estado[\"ruta\"] != ruta:\n            try:\n                _aplicar(_leer_categoria(ruta), ruta)",
     ["test_gui_construccion.py"]),
    # 6. router por pila (lift) en vez de mostrar/esconder
    ("gui/app.py",
     '        for pid, frame in self._frames.items():\n            if pid == pantalla_id:\n                frame.grid(row=0, column=0, sticky="nsew")\n            else:\n                frame.grid_remove()',
     "        self._frames[pantalla_id].lift()",
     ["test_gui_construccion.py"]),
    # 7. sidebar: volver a juntar por prefijo
    ("gui/app.py",
     "            contenido = _grupo_colapsable(barra, programa)",
     '            contenido = _grupo_colapsable(barra, "Salud Mental" if programa.startswith("Salud Mental") else programa)',
     ["test_gui_construccion.py"]),
    # 8. TP: releer el Maestro aunque venga cargado
    ("modulos/rem_sm_trabajo_perdido.py",
     "        dfm = cargar_maestro(maestro) if dfm is None else dfm",
     "        dfm = cargar_maestro(maestro)",
     ["test_trabajo_perdido.py"]),
    # 9. encabezado por conteo de celdas (fallback posicional a la fila 0)
    ("programas/rem_utils.py",
     "        if sum(v not in (None, \"\") for v in r) < minimo:\n            continue",
     "        if i > 0:\n            break",
     ["test_formatos_fuente.py"]),
    # 10. opcional single sin validar la ruta
    ("gui/app.py",
     "                    p = runner.valida_ruta(limpia, messagebox)\n                    if p is None:\n                        return None\n                    ctx[inp[\"key\"]] = p",
     "                    ctx[inp[\"key\"]] = Path(limpia)",
     ["test_gui_construccion.py"]),
]


def corre(test):
    if test == "test_formatos_fuente.py":
        cmd = [PY, "-m", "pytest", f"tests/{test}", "-q"]
    else:
        cmd = [PY, f"tests/{test}"]
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, errors="replace")
    return r.returncode == 0, (r.stdout + r.stderr)[-400:]


cazados = 0
for i, (rel, viejo, nuevo, tests) in enumerate(MUT, 1):
    p = REPO / rel
    original = p.read_bytes()
    s = original.decode("utf-8")
    crlf = "\r\n" in s
    plano = s.replace("\r\n", "\n")
    if plano.count(viejo) != 1:
        print(f"MUT {i:>2} [{rel}]: el texto no calza ({plano.count(viejo)} veces) -- REVISAR")
        continue
    mutado = plano.replace(viejo, nuevo)
    p.write_bytes((mutado.replace("\n", "\r\n") if crlf else mutado).encode("utf-8"))
    try:
        fallo_en = []
        for t in tests:
            ok, cola = corre(t)
            if not ok:
                fallo_en.append(t)
        if fallo_en:
            cazados += 1
            print(f"MUT {i:>2} CAZADO por {', '.join(fallo_en)}")
        else:
            print(f"MUT {i:>2} SOBREVIVE ({rel}: {viejo.strip()[:60]}...) <-- falta test")
    finally:
        p.write_bytes(original)
print(f"\n{cazados}/{len(MUT)} mutantes cazados")
