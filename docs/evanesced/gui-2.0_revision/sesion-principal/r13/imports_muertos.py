import ast, pathlib, sys, io, tokenize
RAIZ = pathlib.Path(r"E:\git\Autorem")
DIRS = ("programas","modulos","tools","gui","tests")
def usados(tree, src):
    # cualquier Name o atributo base usado en el archivo, mas los nombres en strings
    # de anotaciones/__all__ no se consideran.
    u=set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Name): u.add(n.id)
        elif isinstance(n, ast.Attribute):
            b=n
            while isinstance(b, ast.Attribute): b=b.value
            if isinstance(b, ast.Name): u.add(b.id)
    return u
rep=[]
for d in DIRS:
    for f in sorted((RAIZ/d).rglob("*.py")):
        rel=f.relative_to(RAIZ).as_posix()
        src=f.read_text(encoding="utf-8")
        tree=ast.parse(src)
        u=usados(tree,src)
        # nombres citados en strings (p.ej. __all__, getattr) -> los perdonamos
        for node in ast.walk(tree):
            if isinstance(node,(ast.Import,ast.ImportFrom)):
                for a in node.names:
                    if a.name=="*": continue
                    local = a.asname or a.name.split(".")[0]
                    if local not in u and ('"%s"'%local) not in src and ("'%s'"%local) not in src:
                        mod = getattr(node,'module',None) or a.name
                        rep.append((rel,node.lineno,local,mod))
for r in rep: print("%-40s:%-4d  %-28s (de %s)"%r)
print("total", len(rep))
