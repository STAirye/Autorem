"""Helpers para resolver conflictos preservando CRLF."""
import re, sys

def partes(path):
    s = open(path, encoding="utf-8", newline="").read()
    pat = re.compile(r"<<<<<<< HEAD\r?\n(.*?)(?:\|\|\|\|\|\|\|.*?)?=======\r?\n(.*?)>>>>>>> main\r?\n", re.S)
    return s, pat

def listar(path):
    s, pat = partes(path)
    for i, m in enumerate(pat.finditer(s)):
        print(f"--- conflicto {i} HEAD ---"); print(m.group(1))
        print(f"--- conflicto {i} MAIN ---"); print(m.group(2))

def resolver(path, nuevos):
    """nuevos = lista de strings (uno por conflicto, en orden)."""
    s, pat = partes(path)
    it = iter(nuevos)
    out = pat.sub(lambda m: next(it), s)
    assert "<<<<<<<" not in out and ">>>>>>>" not in out, "quedan marcas"
    open(path, "w", encoding="utf-8", newline="").write(out)
    print("OK", path)
