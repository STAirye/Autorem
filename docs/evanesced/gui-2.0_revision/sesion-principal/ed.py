"""reemplazar(ruta, [(viejo, nuevo), ...]) preservando CRLF/LF; cada viejo debe aparecer 1 vez."""
from pathlib import Path
def reemplazar(ruta, pares):
    p = Path(ruta); raw = p.read_bytes().decode("utf-8")
    crlf = "\r\n" in raw
    t = raw.replace("\r\n", "\n")
    for viejo, nuevo in pares:
        n = t.count(viejo)
        assert n == 1, (ruta, n, viejo[:80])
        t = t.replace(viejo, nuevo)
    if crlf: t = t.replace("\n", "\r\n")
    p.write_bytes(t.encode("utf-8"))
