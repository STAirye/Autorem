# -*- coding: utf-8 -*-
"""Enlaza docs/evanesced/ desde CLAUDE.md y actualiza las rutas del ledger."""
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
            sys.exit("ANCLA FALLIDA en %s (%d, esperaba %d):\n%s"
                     % (self.rel, self.t.count(viejo), n, viejo[:120]))
        self.t = self.t.replace(viejo, nuevo, n)
        return self

    def guardar(self):
        self.p.write_bytes((self.t.replace("\n", "\r\n") if self.crlf else self.t)
                           .encode("utf-8"))
        print("  %-38s ok" % self.rel)


c = Arch("CLAUDE.md")
# La regla 7 ahora dice DONDE viven
c.rep("""   Vale igual si el documento tiene 10 líneas o 1000. Y antes de borrar cualquier archivo
   del repo, mirar quién lo cita (`grep -rn "<nombre>" --include="*.md" --include="*.py" .`):
   el `CHANGELOG` es permanente, y una cita colgada ahí no se arregla después.""",
      """   Vale igual si el documento tiene 10 líneas o 1000. Y antes de borrar cualquier archivo
   del repo, mirar quién lo cita (`grep -rn "<nombre>" --include="*.md" --include="*.py" .`):
   el `CHANGELOG` es permanente, y una cita colgada ahí no se arregla después.

   Los **scripts** de trabajo intermedio (repros, arneses de medición, prompts de ronda)
   viven en el scratchpad de la sesión, que es temporal. Cuando la rama o el worktree que
   los produjo cierra su trabajo, se archivan en
   **[docs/evanesced/](docs/evanesced/README.md)** — se archivan **como quedaron**, sin
   reescribirlos, y sin copias de fuentes del repo ni binarios (el README dice por qué y
   cómo se recuperan).""")
# El arbol de §2 nombra la subcarpeta
c.rep("""docs/             planes y contexto por módulo""",
      """docs/             planes y contexto por módulo
  evanesced/        scripts de repro de ramas/worktrees ya cerrados (§0 regla 7)""")
c.guardar()

led = Arch("docs/review_gui-2.0_pendiente.md")
led.rep("""barridos AST de imports / atributos / constantes, y un repro de años discontinuos); los
scripts quedaron en el scratchpad de la ronda (`r13/`).""",
        """barridos AST de imports / atributos / constantes, y un repro de años discontinuos); los
scripts quedaron archivados en
[docs/evanesced/gui-2.0_revision/](evanesced/gui-2.0_revision/) (CLAUDE.md §0 regla 7),
los de esta ronda en `sesion-principal/r13/`.""")
led.rep("""**Ronda 13 (coherencia estructural).** Todo por comando; los scripts están en el scratchpad
`r13/`. No volver a barrerlo:""",
        """**Ronda 13 (coherencia estructural).** Todo por comando; los scripts están en
`docs/evanesced/gui-2.0_revision/sesion-principal/r13/`. No volver a barrerlo:""")
led.rep("""porque `poblacion._verificar_cobertura_fechas` compara solo `min` y `max`. Repro en el
scratchpad `r13/anios_discontinuos.py`, corte 2016-08:""",
        """porque `poblacion._verificar_cobertura_fechas` compara solo `min` y `max`. Repro en
`docs/evanesced/gui-2.0_revision/sesion-principal/r13/anios_discontinuos.py`, corte 2016-08:""")
led.rep("""**11/11 mutantes cazados** (`r12/mut12.py` del scratchpad)""",
        """**11/11 mutantes cazados**
(`docs/evanesced/gui-2.0_revision/sesion-principal/r12/mut12.py`)""")
led.guardar()
print("\nlisto")
