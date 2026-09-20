"""Cada `mod.attr` de codigo, contra el modulo REAL importado."""
import ast, importlib, pathlib, sys
R = pathlib.Path(r'E:\git\Autorem')
sys.path.insert(0, str(R))
sys.path.insert(0, str(R / 'tests'))
import _aislar_cache  # noqa  (no tocar el cache real del autor)
malos = []
for d in ("programas", "modulos", "gui", "tools", "tests"):
    for f in sorted((R / d).rglob("*.py")):
        rel = f.relative_to(R).as_posix()
        src = f.read_text(encoding="utf-8")
        tree = ast.parse(src)
        alias = {}          # nombre local -> modulo importado
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                for a in n.names:
                    alias[a.asname or a.name.split(".")[0]] = a.name if a.asname else a.name.split(".")[0]
            elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
                for a in n.names:
                    full = f"{n.module}.{a.name}"
                    try:
                        importlib.import_module(full)
                    except Exception:
                        continue
                    alias[a.asname or a.name] = full
        mods = {}
        for loc, full in alias.items():
            try: mods[loc] = importlib.import_module(full)
            except Exception: pass
        for n in ast.walk(tree):
            if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name):
                m = mods.get(n.value.id)
                if m is not None and not hasattr(m, n.attr):
                    malos.append((rel, n.lineno, f"{n.value.id}.{n.attr}", m.__name__))
for x in malos: print("%-40s:%-5d %-34s (modulo %s)" % x)
print("atributos inexistentes:", len(malos))
