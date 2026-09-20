"""Extrae / aplica los textos user-facing de gui/ (revision de textos, uso interno).

  python textos_review/textos.py extraer   -> original.txt (derecha) + editable.txt (izquierda)
  python textos_review/textos.py aplicar   -> vuelca las diferencias de editable.txt al codigo
"""
import ast, re, sys
from pathlib import Path

BS, LF, CRLF = chr(92), chr(10), chr(13) + chr(10)
RAIZ = Path(__file__).resolve().parent.parent
AQUI = Path(__file__).resolve().parent
ARCHIVOS = ["gui/app.py", "gui/dialogos.py", "gui/widgets.py", "gui/runner.py",
            "gui/registro.py", "gui/paginas/inicio.py", "gui/paginas/a05.py",
            "gui/paginas/sm.py", "gui/paginas/poblacion.py", "gui/paginas/a23.py",
            "gui/paginas/about.py"]
NOKW = {"key", "id", "programa", "estado", "anchor", "sticky", "side", "fill", "font",
        "state", "mode", "compound", "justify", "wrap", "cursor", "relief"}
HDR = re.compile(r"^@@@ (\S+) \| (\S+) \| (\S+)( \| f)?$")


def parece_texto(s):
    if not re.search(r"[A-Za-zÁÉÍÓÚÑáéíóúñ]{2}", s):
        return False
    if " " in s or "\n" in s:
        return True
    return bool(re.match(r"[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+[.:!?…]*$", s))


def render(node):
    if isinstance(node, ast.Constant):
        return node.value, False
    out = []
    for v in node.values:
        if isinstance(v, ast.Constant):
            out.append(v.value.replace("{", "{{").replace("}", "}}"))
        else:
            e = "{" + ast.unparse(v.value)
            if v.conversion != -1:
                e += "!" + chr(v.conversion)
            if v.format_spec is not None:
                e += ":" + "".join(render(v.format_spec)[0] if not isinstance(x, ast.FormattedValue)
                                   else "{" + ast.unparse(x.value) + "}" for x in v.format_spec.values)
            out.append(e + "}")
    return "".join(out), True


def entradas(rel):
    src = (RAIZ / rel).read_bytes().decode("utf-8").replace(CRLF, LF)
    tree = ast.parse(src)
    padre = {}
    for p in ast.walk(tree):
        for c in ast.iter_child_nodes(p):
            padre[c] = p
    doc = set()
    for n in ast.walk(tree):
        if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if n.body and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant):
                doc.add(n.body[0].value)
    res = []

    def visita(n, dentro_f=False):
        if isinstance(n, ast.JoinedStr) or (isinstance(n, ast.Constant) and isinstance(n.value, str)):
            if n in doc:
                return
            p = padre.get(n)
            if isinstance(p, ast.Dict) and n in p.keys:
                return
            if isinstance(p, (ast.Subscript, ast.Compare, ast.FormattedValue)):
                return
            if isinstance(p, ast.keyword) and p.arg in NOKW:
                return
            if isinstance(p, ast.Call) and getattr(p.func, "id", getattr(p.func, "attr", "")) in (
                    "getattr", "hasattr", "import_module", "setattr", "iter_modules", "get", "pop"):
                return
            txt, esf = render(n)
            if not parece_texto(txt):
                return
            ctx = "-"
            if isinstance(p, ast.keyword):
                ctx = p.arg
            elif isinstance(p, ast.Dict):
                i = p.values.index(n)
                ctx = getattr(p.keys[i], "value", "-")
            elif isinstance(p, ast.Assign):
                ctx = getattr(p.targets[0], "id", "-")
            elif isinstance(p, ast.Call):
                ctx = getattr(p.func, "attr", getattr(p.func, "id", "call"))
            elif isinstance(p, ast.Raise):
                ctx = "raise"
            res.append((n, txt, esf, ctx))
            return
        for c in ast.iter_child_nodes(n):
            visita(c)
    visita(tree)
    res.sort(key=lambda t: (t[0].lineno, t[0].col_offset))
    return src, res


def extraer():
    bloques = []
    for rel in ARCHIVOS:
        _, res = entradas(rel)
        for n, txt, esf, ctx in res:
            bloques.append(f"@@@ {rel}:{n.lineno} | {ctx.replace(' ', '_')} | "
                           f"{'f' if esf else 's'}\n<<<\n{txt}\n>>>\n")
    cuerpo = ("# REVISION DE TEXTOS gui 2.0. Edita solo lo que hay entre <<< y >>>.\n"
              "# No toques las lineas @@@. En strings f, deja los {placeholders} intactos.\n"
              "# Un texto tal cual esta entre <<< y >>> (los saltos de linea son literales).\n\n"
              + "\n".join(bloques))
    (AQUI / "original.txt").write_text(cuerpo, encoding="utf-8")
    if not (AQUI / "editable.txt").exists():
        (AQUI / "editable.txt").write_text(cuerpo, encoding="utf-8")
    print(f"{len(bloques)} textos")


def parsear(path):
    d, cur, buf, dentro = [], None, [], False
    for ln in path.read_text(encoding="utf-8").split("\n"):
        if not dentro:
            m = HDR.match(ln.rstrip())
            if m:
                cur = m.group(1)
            elif ln.rstrip() == "<<<" and cur:
                dentro, buf = True, []
        elif ln.rstrip() == ">>>":
            d.append((cur, "\n".join(buf)))
            dentro, cur = False, None
        else:
            buf.append(ln)
    return d


def literal(txt, esf, col):
    def esc(s):
        s = s.replace("\\", "\\\\").replace('"', '\\"')
        return s if esf else s
    partes = txt.split("\n")
    pref = "f" if esf else ""
    lineas = [pref + '"' + esc(p) + (BS + "n" if i < len(partes) - 1 else "") + '"'
              for i, p in enumerate(partes)]
    if len(lineas) == 1:
        return lineas[0]
    return "(" + ("\n" + " " * (col + 1)).join(lineas) + ")"


def aplicar():
    orig = parsear(AQUI / "original.txt")
    edit = parsear(AQUI / "editable.txt")
    if [h for h, _ in orig] != [h for h, _ in edit]:
        sys.exit("ERROR: las cabeceras @@@ de editable.txt no coinciden con original.txt "
                 "(borraste, agregaste o cambiaste un bloque). No toco nada.")
    # Un texto se identifica por (archivo, linea, posicion dentro de esa linea):
    # titulo y mensaje de un mismo showwarning comparten linea.
    vistos, por_archivo, n_cambios = {}, {}, 0
    for (h, t0), (_, t1) in zip(orig, edit):
        rel, ln = h.rsplit(":", 1)
        k = (rel, int(ln))
        i = vistos[k] = vistos.get(k, -1) + 1
        if t0 != t1:
            n_cambios += 1
            por_archivo.setdefault(rel, {})[(int(ln), i)] = t1
    print(f"{n_cambios} textos cambiados")
    for rel, mods in por_archivo.items():
        src, res = entradas(rel)
        lineas = src.split("\n")
        orden, cnt = {}, {}
        for n, *_ in res:   # res ya viene en orden de codigo
            cnt[n.lineno] = orden[id(n)] = cnt.get(n.lineno, -1) + 1
        for n, txt, esf, ctx in sorted(res, key=lambda t: (-t[0].lineno, -t[0].col_offset)):
            if (n.lineno, orden[id(n)]) not in mods:
                continue
            nuevo = mods[(n.lineno, orden[id(n)])]
            if esf and re.findall(r"(?<!\{)\{[^{}]*\}", txt) != re.findall(r"(?<!\{)\{[^{}]*\}", nuevo):
                print(f"  SALTADO {rel}:{n.lineno} (cambiaste un {{placeholder}})")
                continue
            l0, l1 = n.lineno - 1, n.end_lineno - 1
            b0 = lineas[l0].encode()[:n.col_offset].decode()
            b1 = lineas[l1].encode()[n.end_col_offset:].decode()
            lit = literal(nuevo, esf, len(b0))
            lineas[l0:l1 + 1] = (b0 + lit + b1).split("\n")
        out = "\n".join(lineas)
        ast.parse(out)
        (RAIZ / rel).write_bytes(out.replace(LF, CRLF).encode("utf-8"))
        print("  ok", rel)


if __name__ == "__main__":
    {"extraer": extraer, "aplicar": aplicar}[sys.argv[1]]()
