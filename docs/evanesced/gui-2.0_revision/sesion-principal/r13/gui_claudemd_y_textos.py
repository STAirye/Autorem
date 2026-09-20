# -*- coding: utf-8 -*-
"""1) Corrige el alcance de la revision de textos (revisado != cambiado).
2) Enchufa gui/CLAUDE.md en el raiz y cierra el punto 3 del checklist del paso 11.
3) Anota que la ronda 14 (eficiencia/reuso) corre DESPUES del merge, sobre todo el codebase.
"""
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
                     % (self.rel, self.t.count(viejo), n, viejo[:130]))
        self.t = self.t.replace(viejo, nuevo, n)
        return self

    def guardar(self):
        self.p.write_bytes((self.t.replace("\n", "\r\n") if self.crlf else self.t)
                           .encode("utf-8"))
        print("  %-38s ok" % self.rel)


# =====================================================================
# 1. Revision de textos: lo que la herramienta MOSTRO y no se toco, esta OK
# =====================================================================
led = Arch("docs/review_gui-2.0_pendiente.md")
led.rep("""  desde `claudio/gui-2-0-text-review-c85d1c`; la herramienta quedó archivada en
  [docs/evanesced/gui-2.0_textos/textos.py](evanesced/gui-2.0_textos/textos.py) (extrae por
  AST los strings de `gui/` a dos archivos gemelos para editarlos en un diff lado a lado, y
  vuelca al código solo los bloques que cambiaron). Cubrió las 8 primeras filas de la tabla
  de abajo, o sea **todo lo que vive en `gui/`**. Lo que NO cubrió, porque la herramienta
  solo recorre `gui/`: las **dos últimas filas** — los mensajes de `ArchivoInvalido` de
  `programas/` y `modulos/` (los que más se leen) y la hoja LEEME de
  `programas/cobertura.py`. Esos siguen sin revisar.""",
        """  desde `claudio/gui-2-0-text-review-c85d1c`; la herramienta quedó archivada en
  [docs/evanesced/gui-2.0_textos/textos.py](evanesced/gui-2.0_textos/textos.py) (extrae por
  AST los strings de `gui/` a dos archivos gemelos para editarlos en un diff lado a lado, y
  vuelca al código solo los bloques que cambiaron).

  **Alcance exacto, y leerlo bien importa:** la herramienta extrajo **283 textos** de los
  **11 `.py` de `gui/`** (todos menos `__init__.py`) — cada string y cada f-string que
  parezca texto, salvo docstrings, claves de dict y kwargs de layout. El autor los revisó
  **TODOS, uno por uno**. Un texto que la herramienta mostró y **no** se tocó está
  **APROBADO**, no sin revisar: no volver a proponerlo. Eso cubre las 8 primeras filas de
  la tabla de abajo, o sea todo lo que vive en `gui/`.

  Lo que NO alcanzó a ver, porque la herramienta solo recorre `gui/`: las **dos últimas
  filas** — los mensajes de `ArchivoInvalido` de `programas/` y `modulos/` (los que más se
  leen) y la hoja LEEME de `programas/cobertura.py` —, más los `log(` de `modulos/` de la
  octava fila. Esos siguen sin revisar, y para hacerlo hay que ampliar `ARCHIVOS` en
  `textos.py`.""")

# =====================================================================
# 3. La ronda 14 corre DESPUES del merge, sobre todo el codebase
# =====================================================================
led.rep("""**Ojo:** la **Eficiencia** es lo único que sigue sin barrerse.""",
        """**La Eficiencia (y el reuso) se corre DESPUÉS del merge, contra el codebase COMPLETO** —
decisión del autor, 20-sep-2026: no tiene sentido medir «¿se relee un archivo, se rehace
trabajo?» sobre una rama que va a fundirse con `main`, cuando la mitad del camino caliente
vive en `programas/` y `modulos/`. O sea que no es la ronda 14 de ESTA revisión: es la
primera pasada de la siguiente, ya sobre `main`.

**Ojo:** la **Eficiencia** es lo único que sigue sin barrerse.""")
led.rep("""| 14 | _(siguiente: EFICIENCIA —el único ángulo sin barrer: ¿la GUI 2.0 relee archivos o rehace trabajo?—, la prueba a mano del caché en el PC del trabajo (§4), y otra pasada a ojo del autor)_ | | |""",
        """| 14 | _**Después del merge, y sobre el codebase COMPLETO** (decisión del autor): EFICIENCIA y REUSO — el único ángulo sin barrer. Ya no es una ronda de esta revisión: el camino caliente vive en `programas/` y `modulos/`, así que medirlo sobre la rama sola mide la mitad. Pendientes que no son para un agente: la prueba a mano del caché en el PC del trabajo (§4) y otra pasada a ojo del autor_ | | |""")
led.guardar()

# =====================================================================
# 4. El raiz: indice, arbol, reparto y cadena de imports
# =====================================================================
c = Arch("CLAUDE.md")
c.rep("""| — | convenciones de tests (no comparar texto plano de la GUI) | [tests/CLAUDE.md](tests/CLAUDE.md) |""",
      """| — | GUI 2.0: contrato de pantalla, trampas de Tk/hilos, reuso | [gui/CLAUDE.md](gui/CLAUDE.md) |
| — | convenciones de tests (no comparar texto plano de la GUI) | [tests/CLAUDE.md](tests/CLAUDE.md) |""")
c.rep("""- **Dispatcher — `autorem.py`:** GUI de pestañas + CLI.""",
      """- **Interfaz — `gui/`:** la **GUI 2.0** (`customtkinter`), declarativa: una pantalla por
  archivo en `gui/paginas/`, descubiertas por introspección. Shell y router en `app.py`,
  frontera con el hilo worker en `runner.py` -> [gui/CLAUDE.md](gui/CLAUDE.md).
- **Dispatcher — `autorem.py`:** GUI de pestañas (1.x, la que corre el `.exe`) + CLI.""")
c.rep("""Cadena de imports: `rem_utils` ← `formatos` ← capas ← módulos ← `autorem`. Imports""",
      """Cadena de imports: `rem_utils` ← `formatos` ← capas ← módulos ← `autorem` / `gui`. Imports""")
c.rep("""catalogos/        CIE-10 / ENO / GES que shippea el exe (§14)""",
      """gui/              GUI 2.0 (customtkinter)     -> gui/CLAUDE.md
catalogos/        CIE-10 / ENO / GES + maestro_slim, que shippea el exe (§14)""")
c.guardar()
print("\nlisto")
