# -*- coding: utf-8 -*-
"""Ronda 13: arregla los hallazgos 4, 5, 6 y 7. CRLF-safe archivo por archivo."""
import pathlib, sys

RAIZ = pathlib.Path(r"E:\git\Autorem")


class Arch:
    def __init__(self, rel):
        self.p = RAIZ / rel
        b = self.p.read_bytes()
        self.crlf = b"\r\n" in b
        self.t = b.decode("utf-8").replace("\r\n", "\n")
        self.rel = rel

    def rep(self, viejo, nuevo, n=1):
        if self.t.count(viejo) != n:
            sys.exit("ANCLA FALLIDA en %s (%d veces, esperaba %d):\n%s"
                     % (self.rel, self.t.count(viejo), n, viejo[:140]))
        self.t = self.t.replace(viejo, nuevo, n)
        return self

    def guardar(self):
        self.p.write_bytes((self.t.replace("\n", "\r\n") if self.crlf else self.t)
                           .encode("utf-8"))
        print("  %-38s ok (%s)" % (self.rel, "CRLF" if self.crlf else "LF"))


print("Hallazgo 4 - documentos de trabajo intermedios + citas al ledger")

# -- CLAUDE.md: regla 7 nueva + la cita rota al §6 del ledger ----------------
c = Arch("CLAUDE.md")
c.rep("""6. **100% local, offline.** Sin nube (Ley 20.584 y 21.719).""",
      """6. **100% local, offline.** Sin nube (Ley 20.584 y 21.719).
7. **Ningún documento de trabajo intermedio se borra** — planes de `docs/`, registros de
   revisión, contextos de una rama chica, notas de una tanda de arreglos. Son la
   documentación del *por qué* de cada decisión, y una sesión fría (`compact` entre medio)
   no tiene otra fuente. Al terminar de usarlos **no se eliminan: se cierran con un header**
   arriba del archivo, para que el que lo abra sepa en una línea que ya no es una tarea
   pendiente:

   ```markdown
   > **LISTO Y MERGEADO** — 2026-09-20, dejó de usarse en 1.9.17.
   > Se conserva como registro: lo citan CHANGELOG.md y CLAUDE.md.
   ```

   Vale igual si el documento tiene 10 líneas o 1000. Y antes de borrar cualquier archivo
   del repo, mirar quién lo cita (`grep -rn "<nombre>" --include="*.md" --include="*.py" .`):
   el `CHANGELOG` es permanente, y una cita colgada ahí no se arregla después.""")
c.rep("""  [docs/review_gui-2.0_pendiente.md](docs/review_gui-2.0_pendiente.md) §6.""",
      """  [docs/review_gui-2.0_pendiente.md](docs/review_gui-2.0_pendiente.md) §4.""")
c.guardar()

# -- CHANGELOG.md: las dos citas que quedaron apuntando a la numeracion vieja -
ch = Arch("CHANGELOG.md")
ch.rep("""  roto; `docs/review_gui-2.0_pendiente.md` §4, puntos 2 a 5):""",
       """  roto; `docs/review_gui-2.0_pendiente.md` §1.C-ter y §1.D-bis):""")
ch.rep("""- **GUI 2.0, barrido línea por línea del diff** (`docs/review_gui-2.0_pendiente.md` §5,
  ronda 3):""",
       """- **GUI 2.0, barrido línea por línea del diff** (`docs/review_gui-2.0_pendiente.md` §1.D,
  ronda 3):""")
ch.guardar()

print("Hallazgo 5 - rutas viejas del maestro slim")
a = Arch("docs/auditoria_filtros_plan.md")
a.rep("""Todo esto se corrió sep-2026 contra `refs_tablas/maestro_slim.csv.gz` y los
módulos en 1.9.10.""",
      """Todo esto se corrió sep-2026 contra `refs_tablas/maestro_slim.csv.gz` (hoy
`catalogos/maestro_slim.csv.gz`: el archivo se mudó en la rama `gui-2.0`) y los
módulos en 1.9.10.""")
a.rep("""m = pd.read_csv('refs_tablas/maestro_slim.csv.gz', dtype=str, keep_default_na=False)""",
      """m = pd.read_csv('catalogos/maestro_slim.csv.gz', dtype=str, keep_default_na=False)""")
a.rep("""4. **`skipif`** si falta `refs_tablas/maestro_slim.csv.gz` (está versionado, pero""",
      """4. **`skipif`** si falta `catalogos/maestro_slim.csv.gz` (está versionado, pero""")
a.guardar()

print("Hallazgo 6 - import muerto")
e = Arch("programas/estamentos.py")
e.rep("""    leer_cache_json, guardar_cache_json,
)
from programas import formatos
""",
      """    leer_cache_json, guardar_cache_json,
)
""")
e.guardar()

print("Hallazgo 7 - las dos afirmaciones falsas")
u = Arch("programas/rem_utils.py")
u.rep("""    `ancla` = nombres de columna que deben estar TODOS en esa fila; sin ancla, la 1ª
    fila con >3 celdas llenas. Fuente UNICA del criterio: la usan `leer_xlsx` y el
    preview de cruce del SM, que antes lo copiaba a mano.""",
      """    `ancla` = nombres de columna que deben estar TODOS en esa fila; sin ancla, la 1ª
    fila con >3 celdas llenas. La usan `leer_xlsx` y el preview de cruce del SM, que
    antes lo copiaba a mano.

    OJO, no es el unico criterio del proyecto (lo decia este docstring hasta la ronda
    13, y era falso): el grupo pandas ubica el encabezado por las columnas REQUERIDAS
    (`encabezado_por_columnas`, ronda 12) porque contar celdas rechazaba exports validos,
    y `tools/limpiar_refs.py` tiene su propio umbral (`MIN_CELDAS_HEADER = 5`) para
    recortar las referencias. Si hay que mover un umbral, son TRES lugares.""")
u.guardar()

f = Arch("tools/check_fuentes.py")
f.rep("""RAIZ = Path(__file__).resolve().parent.parent
CARPETAS = ("programas", "modulos", "gui")""",
      """RAIZ = Path(__file__).resolve().parent.parent
# Codigo que lee planillas DEL USUARIO y viaja en el exe. `tools/` queda afuera hoy
# porque no se distribuye -- pero ahi estan los dos lectores que abren el export CRUDO,
# sin recortar: `limpiar_refs` (la compuerta de privacidad, §8) y `slim_maestro` (el
# Maestro de 8,6 MB). Hoy los cubre `tests/test_refs_tablas.py`, no un contrato.
# INTENCION DEL AUTOR (ronda 13): `tools/` va a viajar en el exe en algun momento (baja
# prioridad); cuando pase, sumarlo aca y escribirles su contrato.
CARPETAS = ("programas", "modulos", "gui")""")
f.guardar()

print("\nlisto: 4, 5, 6 y 7.")
