# -*- coding: utf-8 -*-
"""Actualiza el ledger tras los 2 commits de fuera de sesion (02106fb el merge de
claudio/gui-2-0-text-review-c85d1c, 3b8cbd4 el archivado de textos.py)."""
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


led = Arch("docs/review_gui-2.0_pendiente.md")

# ---- 1. Encabezado: HEAD y el tamano del diff ------------------------------
led.rep("""Revisión de la rama `gui-2.0` contra `main` (merge-base `03e15f6`; en `f94a0ec` el diff va
en 80 archivos y ~12.200 líneas nuevas, contra las ~3200 con que arrancó la revisión).""",
        """Revisión de la rama `gui-2.0` contra `main` (merge-base `03e15f6`; en `3b8cbd4` el diff va
en 193 archivos y ~18.600 líneas nuevas, contra las ~3200 con que arrancó la revisión — los
~6.200 del último salto son el archivo de `docs/evanesced/`, no código).""")

# ---- 2. El item ⚠ de textos: la parte de gui/ esta HECHA -------------------
led.rep("""- **⚠ REVISAR A MANO TODO EL TEXTO QUE VE EL USUARIO — pega del AUTOR, no de un agente.**
  Es un code-review que solo puede hacer quien conoce RAYEN/IRIS y el REM: un agente
  puede verificar que el string exista y esté bien escrito, no que la instrucción sea
  **cierta**.""",
        """- **⚠ TEXTO QUE VE EL USUARIO — `gui/` HECHO (20-sep-2026, el autor); `programas/` y
  `modulos/` SIGUEN PENDIENTES.**

  La pasada del autor sobre `gui/` está en `722ecbe` + `6ea9985`, mergeada en `02106fb`
  desde `claudio/gui-2-0-text-review-c85d1c`; la herramienta quedó archivada en
  [docs/evanesced/gui-2.0_textos/textos.py](evanesced/gui-2.0_textos/textos.py) (extrae por
  AST los strings de `gui/` a dos archivos gemelos para editarlos en un diff lado a lado, y
  vuelca al código solo los bloques que cambiaron). Cubrió las 8 primeras filas de la tabla
  de abajo, o sea **todo lo que vive en `gui/`**. Lo que NO cubrió, porque la herramienta
  solo recorre `gui/`: las **dos últimas filas** — los mensajes de `ArchivoInvalido` de
  `programas/` y `modulos/` (los que más se leen) y la hoja LEEME de
  `programas/cobertura.py`. Esos siguen sin revisar.

  **Lo que dejó de aprendizaje, y es una convención nueva:** la revisión **rompió un test**
  que comparaba un texto de la interfaz a mano. De ahí salió
  [tests/CLAUDE.md](../tests/CLAUDE.md) («No compares texto plano que ve el usuario»): si un
  test necesita el texto, éste vive UNA vez como constante del módulo que lo muestra y el
  test la importa (`a05.TITULO_FALTA_ACUSE`, `runner.TITULO_NO_ENCONTRADO`,
  `widgets.NO_SE_GENERO`); mejor aún, se afirma el HECHO y no el texto. Con eso, `tests/`
  pasó a tener su propio `CLAUDE.md` — y **`gui/` es ahora el único paquete de código sin
  uno** (ver el «Checklist del paso 11», punto 3).

  Por qué sigue siendo pega del autor y no de un agente: un agente puede verificar que el
  string exista y esté bien escrito, no que la instrucción sea **cierta**.""")

# ---- 3. Checklist del paso 11: los headers bajaron de 3 a 2 ----------------
led.rep("""2. **Tres headers de versión apuntan a un release de `main` ANTERIOR a su contenido** —
   misma clase que la colisión de §1.E, que ya se pagó para `rem_utils.VERSION`:
   `gui/paginas/inicio.py` dice 1.9.15 y es un archivo NUEVO de la rama;
   `tools/check_version.py` dice 1.9.10 (en `main` está en 1.9.6) y trae el `"gui"` de
   `DIRS_VERSIONADOS`, que ningún 1.9.10 shippeó; `tools/slim_maestro.py` dice 1.9.15 con el
   cambio de ruta a `catalogos/`. Los tres a 1.9.17 (o a la versión del merge). **Por qué no
   salta el hook:** el chequeo 3 de `check_version` solo mira `staged_py()`, así que un
   header queda viejo para siempre a menos que alguien vuelva a tocar el archivo — vale
   sumarle un modo `--auditar` que compare cada `.py` versionado contra la versión vigente
   cuando lo cambió su último commit, y colgarlo de la skill `versionar`, no del hook.""",
        """2. **Dos headers de versión apuntan a un release de `main` ANTERIOR a su contenido** —
   misma clase que la colisión de §1.E, que ya se pagó para `rem_utils.VERSION`:
   `tools/check_version.py` dice 1.9.10 (en `main` está en 1.9.6) y trae el `"gui"` de
   `DIRS_VERSIONADOS`, que ningún 1.9.10 shippeó; `tools/slim_maestro.py` dice 1.9.15 con el
   cambio de ruta a `catalogos/`. Los dos a 1.9.17 (o a la versión del merge).
   *(Eran tres: `gui/paginas/inicio.py` se arregló solo, porque la revisión de textos del
   20-sep lo tocó y el hook —que sí mira lo staged— le exigió la versión vigente. Buena
   ilustración del punto de abajo.)* **Por qué no salta el hook:** el chequeo 3 de
   `check_version` solo mira `staged_py()`, así que un header queda viejo para siempre a
   menos que alguien vuelva a tocar el archivo — vale sumarle un modo `--auditar` que
   compare cada `.py` versionado contra la versión vigente cuando lo cambió su último
   commit, y colgarlo de la skill `versionar`, no del hook.""")

# ---- 4. Checklist punto 3: tests/ ya tiene el suyo ------------------------
led.rep("""   tres) — y es el único paquete de código sin su propio `CLAUDE.md`, con `"gui"` ya en
   `DIRS_VERSIONADOS` y en `CARPETAS` de `check_fuentes`.""",
        """   tres) — y es el único paquete de código sin su propio `CLAUDE.md`, con `"gui"` ya en
   `DIRS_VERSIONADOS` y en `CARPETAS` de `check_fuentes`. **Más claro desde el 20-sep:**
   `tests/` estrenó `tests/CLAUDE.md` y el raíz lo sumó al índice y al árbol, así que hoy
   `programas/`, `modulos/`, `tools/` y `tests/` tienen el suyo y `gui/` no.""")

# ---- 5. §3: estado tras el merge de textos --------------------------------
led.rep("""- **La ronda 13 no agregó tests**""",
        """- **Tras el merge de la revisión de textos** (`02106fb`, 20-sep) la suite sigue en **296**
  `def test_` y los 3 checks en verde. Ese merge tocó 13 archivos de `gui/` y 2 de `tests/`:
  los tests que comparaban un texto a mano pasaron a importar la constante del módulo que lo
  muestra (convención nueva en `tests/CLAUDE.md`), así que el conteo no cambió.
- **La ronda 13 no agregó tests**""")

# ---- 6. §5: fila del autor, con el precedente de la 3b --------------------
led.rep("""| 14 | _(siguiente: EFICIENCIA""",
        """| 13b | **TEXTO USER-FACING de `gui/`, a mano, el AUTOR** (mismo tipo de pasada que la 3b): los ~8 grupos de strings de `gui/` —instrucciones de cada página, modales, títulos de `ArchivoInvalido`, motivos de los obligatorios, etiquetas, líneas de log— leídos y reescritos con una herramienta de extracción por AST + diff lado a lado (`docs/evanesced/gui-2.0_textos/textos.py`). Rompió un test que comparaba texto de interfaz a mano -> convención nueva | textos reescritos + `tests/CLAUDE.md` + 3 constantes de texto | §4 (el ítem ⚠ de textos, `gui/` cerrado) |
| 14 | _(siguiente: EFICIENCIA""")

led.guardar()
print("\nlisto")
