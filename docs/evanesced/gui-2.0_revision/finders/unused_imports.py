import ast, sys, pathlib
root = pathlib.Path(r"E:\git\Autorem\gui")
for f in sorted(root.rglob("*.py")):
    src = f.read_text(encoding="utf-8")
    tree = ast.parse(src)
    # collect imported names per scope (module-level and function-level), check usage anywhere in file text via Name/Attribute nodes
    used = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used.add(node.id)
        elif isinstance(node, ast.Attribute):
            # base name
            base = node
            while isinstance(base, ast.Attribute):
                base = base.value
            if isinstance(base, ast.Name):
                used.add(base.id)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for a in node.names:
                name = (a.asname or a.name).split(".")[0]
                if name not in used:
                    print(f"{f.relative_to(root.parent)}:{node.lineno}: unused import {a.name} as {name}")
