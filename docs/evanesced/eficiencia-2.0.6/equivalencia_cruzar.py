"""Prueba de EQUIVALENCIA de catalogos._cruzar tras pasar a indice (2.0.6).

Se corrio inline (`python -c`) antes de commitear; se transcribe tal cual. Lleva
adentro una COPIA de la version vieja (barrido de la columna COD) para comparar.

Barre los 12.548 codigos de la Lista Tabular CIE-10 contra los DOS catalogos que se
cruzan (eno y ges) = 25.096 consultas, mas los bordes: vacio, None, NaN, un codigo
inexistente, uno con punto, uno con espacios, y 'J00-J99' -- un RANGO pasado como si
fuera un codigo exacto, que es el caso raro donde el indice y el barrido podrian
haber divergido. Resultado: 0 diferencias.

Depende de los catalogos vendorizados (catalogos/*.csv.gz), asi que hay que correrlo
desde un arbol que los tenga.

Uso:  PYTHONPATH=<raiz> python equivalencia_cruzar.py
"""
import pandas as pd

from programas import catalogos as cat


def _cruzar_viejo(nombre, cod):
    """La version 2.0.5, textual: barrido de la columna entera en cada consulta."""
    d = cat.cargar(nombre)
    c = cat.norm_codigo(cod)
    if not c:
        return d.iloc[0:0]
    exacto = d[d["COD"] == c]
    rangos = d[d["COD"].str.contains("-", regex=False)]
    if len(rangos):
        rangos = rangos[[cat._casa(c, p) for p in rangos["COD"]]]
    return pd.concat([exacto, rangos]) if len(rangos) else exacto


codigos = list(cat.cargar("cie10")["COD"])
print("codigos a probar:", len(codigos))
malos = []
for nom in ("eno", "ges"):
    for cod in codigos:
        if not _cruzar_viejo(nom, cod).equals(cat._cruzar(nom, cod)):
            malos.append((nom, cod))
print("DIFERENCIAS:", len(malos), malos[:5])

for cod in ["", None, float("nan"), "J20.9", "zzz", "J00-J99", "  j209  "]:
    a, b = _cruzar_viejo("eno", cod), cat._cruzar("eno", cod)
    print(repr(cod), "igual" if a.equals(b) else "DIFIERE", len(b))
