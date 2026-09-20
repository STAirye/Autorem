# -*- coding: utf-8 -*-
"""Ronda 13: anota el ledger. CRLF-safe (lee bytes, normaliza, edita, restaura)."""
import pathlib, sys
p = pathlib.Path(r"E:\git\Autorem\docs\review_gui-2.0_pendiente.md")
raw = p.read_bytes()
crlf = b"\r\n" in raw
t = raw.decode("utf-8").replace("\r\n", "\n")


def rep(viejo, nuevo, n=1):
    global t
    if t.count(viejo) != n:
        sys.exit("ANCLA FALLIDA (%d veces, esperaba %d):\n%s" % (t.count(viejo), n, viejo[:120]))
    t = t.replace(viejo, nuevo, n)


# ---- 1. El archivo NO se borra (orden del autor, 2026-09-20) ----------------
rep("Sin PII. Borrar este archivo cuando la revisión esté cerrada y mergeada.",
    """Sin PII.

> **Este archivo NO se borra al mergear** (orden del autor, 20-sep-2026: un documento de
> trabajo intermedio es documentación del *por qué*, y una sesión fría no tiene otra
> fuente). Lo que se hace al cerrarlo es ponerle el **header de cierre** que pide
> [CLAUDE.md §0 regla 7](../CLAUDE.md): `LISTO Y MERGEADO` + fecha + versión en que dejó de
> usarse. Lo citan `CHANGELOG.md` (11 veces), `CLAUDE.md` (2) y la skill `tests-fuentes`
> (1): borrarlo dejaría 14 referencias colgando.""")

# ---- 2. Bloque §1.N -------------------------------------------------------
BLOQUE_N = """### §1.N · Coherencia estructural tras 12 rondas (ronda 13, última compuerta)

Ángulo: las rondas 1-12 son la SALIDA de la revisión y nadie las había leído como un
CUERPO. Ocho hallazgos, **ninguno de cálculo en la GUI**: los doce parches no dejaron un
número mal. Lo que quedó descuadrado es el andamio que orienta a la sesión siguiente — y
cuatro de los ocho se volvían permanentes justo al mergear. Casi todo fue decidible por
comando (los 3 checks, `pytest`, la suite archivo por archivo, import de los 37 módulos,
barridos AST de imports / atributos / constantes, y un repro de años discontinuos); los
scripts quedaron en el scratchpad de la ronda (`r13/`).

**Corregido en la ronda (4):**

1. **El ledger no se borra, se cierra con header.** Había 14 citas a este archivo desde
   archivos PERMANENTES — `CHANGELOG.md` 11, `CLAUDE.md` 2, skill `tests-fuentes` 1 — y el
   propio archivo mandaba borrarse al mergear: el merge dejaba las 14 colgando. Tres ya
   estaban rotas porque el ledger creció de §1..§5 a §1.A..§1.N y las citas no siguieron:
   `CLAUDE.md` decía «§6» (no existe; es §4), y el `CHANGELOG` «§4, puntos 2 a 5» para la
   paridad del port (es §1.C-ter/§1.D-bis) y «§5, ronda 3» para el barrido línea por línea
   (es §1.D). Las tres corregidas, la línea de borrado reemplazada por el header de cierre,
   y la regla generalizada a **CLAUDE.md §0 regla 7**: ningún documento de trabajo
   intermedio se borra, ni el de una rama chica.
2. **`docs/auditoria_filtros_plan.md`** quedó con `refs_tablas/maestro_slim.csv.gz` tres
   veces tras la mudanza a `catalogos/`: una medición histórica (se conserva, con la ruta
   de hoy entre paréntesis), un snippet copiable que daba `FileNotFoundError` y un
   `skipif` que habría saltado el test SIEMPRE. El resto de la mudanza estaba completo
   (código, `.spec`, `.gitignore`, `slim_maestro`, `tools/CLAUDE.md`).
3. **`programas/estamentos.py`: `from programas import formatos`** quedó muerto cuando
   §1.M.11 borró `formatos.fila_encabezado_admin`, su único uso — el módulo tiene su propia
   `ANCLA` y su propio `detectar`. Es el ÚNICO import muerto que introdujeron las 12 rondas
   (los otros tres del barrido AST —`catalogos.gzip`, `rem_sm_actividades._band_idx`,
   `rem_sp_p6_poblacion.re`— vienen igual de `main`).
4. **Dos afirmaciones falsas: el criterio de encabezado y el alcance del arnés.**
   `rem_utils.indice_encabezado` decía «Fuente UNICA del criterio» cuando desde §1.M.10 hay
   TRES reglas vivas (`>3` celdas ahí, `>=5` en `limpiar_refs.MIN_CELDAS_HEADER`, y las
   columnas requeridas en `encabezado_por_columnas`); y `check_fuentes.CARPETAS` excluía
   `tools/` sin motivo escrito, cuando cada exclusión de `EXENTOS` sí lleva el suyo — y en
   `tools/` están los dos lectores que abren exports CRUDOS (`limpiar_refs`, la compuerta de
   privacidad, y `slim_maestro`). Las dos ahora dicen lo que pasa, y la de `CARPETAS` anota
   la intención del autor: **`tools/` va a viajar en el exe en algún momento** (baja
   prioridad), y ahí entra al arnés.

**Al paso 11, en el commit del merge (3):** la tabla-compuerta del plan, los tres headers de
versión y `gui/` ausente del mapa del repo. Ver §4, «Checklist del paso 11».

**A `main`, lógica de módulo (1):** años discontinuos en la familia población. Ver §4.

**Medido, no opinado** (los números de esta ronda):

```
python tools/check_version.py         -> OK 1.9.17, 296 tests
python tools/check_cp1252.py          -> OK 64 archivos
python tools/check_fuentes.py --todo  -> OK 18 contratos, 0 lectores sin contrato
python -m pytest -q                   -> 298 passed
suite archivo por archivo             -> 16/16 ok, 0 fallas
import de los 4 paquetes              -> 37 modulos, 0 fallos
git diff fd1b0cc^..HEAD --stat        -> 74 archivos, +9718/-1007
```

"""
rep("### §1.E · Estructura y versionado", BLOQUE_N + "### §1.E · Estructura y versionado")

# ---- 3. Items de §2: lo perseguido que NO era bug ---------------------------
ITEMS_2 = """
**Ronda 13 (coherencia estructural).** Todo por comando; los scripts están en el scratchpad
`r13/`. No volver a barrerlo:

- **Nada quedó apuntando a un símbolo que una ronda posterior renombró o borró.** Barrido
  AST de todo `mod.attr` de los 4 paquetes + `tests/` contra el módulo REAL importado: 7
  hits, los 7 falsos positivos (`urllib.request` x4 —el archivo sí hace ese import—,
  `sys.frozen` y `sys._MEIPASS` parcheados a propósito en `test_catalogos`, y el de abajo).
  Los 37 módulos de `gui`/`programas`/`modulos`/`tools` importan sin error.
- **`gui/app.py:599` nombra `inicio` a un dict local**, tapando el módulo
  `gui.paginas.inicio` importado en la línea 94. Hoy es inofensivo (dentro de
  `lanzar_corrida` nadie necesita el módulo; el uso real, `inicio.construir`, está a nivel
  de módulo en la 108). Queda anotado por si alguien necesita la página desde ahí.
- **No hay helper duplicado por dos rondas arreglando lo mismo.** Nombres de función
  repetidos entre archivos: todos son el protocolo del proyecto (`procesar`, `escribir`,
  `correr`, `resumen`, `preparar`, `main`, `TAREA`, `PANTALLA`) o gemelos documentados
  (`dotacion`/`estamentos`, `a05_n`/`a05_o`). El único par de cuerpos IDÉNTICOS
  (`dialogos.get_ruta` / `widgets.get`) son las dos closures de 2 líneas que §1.I.2 creó a
  propósito para pasar por `runner.limpiar_ruta`. Constantes MAYÚSCULAS repetidas: ninguna
  nueva, y `_QUE`/`_SI_SE_PIERDE`/`_SI_NO_SE_GUARDA` dicen textos DISTINTOS en cada gemelo
  (cada caché nombra lo que pierde), que es lo correcto.
- **Las 61 citas `CLAUDE.md §N` del repo (código, docs y skills) resuelven todas** contra
  los encabezados reales de los 4 `CLAUDE.md`. Las rotas eran las de este ledger (§1.N.1).
- **`programas/CLAUDE.md` y `modulos/CLAUDE.md` describen la realidad**, al día hasta la
  ronda 12 (citan `encabezado_por_columnas`, `MAPA_INSCRITOS` en `rem_utils`, el `dfm=` del
  Trabajo Perdido, «los OPCIONALES se cargan y validan PRIMERO», el `modo` que se fue).
  `tools/CLAUDE.md §8.2` describe los cuatro hooks tal como los instala
  `hooks_git.INSTALADORES`. Las 4 skills del árbol de §2 existen y el contador de tests
  calza en los 4 sitios.
- **La whitelist POR ARCHIVO de `refs_tablas/` está sincronizada:** 23 líneas de veto y 23
  archivos trackeados (sin `specs/`), sin sobrantes ni faltantes en ninguna dirección; el
  `Maestro_de_Actividades.xlsx` de 8,6 MB sigue ignorado.
- **La compuerta de PII de `limpiar_refs` SÍ está en el script** (`_hallazgos` ->
  `scan_catalogo.escanear`; con hallazgos devuelve «NO ESCRITO») y
  `tests/test_refs_tablas.py::test_las_referencias_versionadas_estan_limpias` la cubre. Se
  persiguió el escenario «un header de dos pisos con celdas combinadas se ve angosto ->
  `_fila_header` cae en la 1ª fila de DATOS y esa fila sobrevive al recorte»: medido sobre
  las 23 referencias, los dos criterios difieren en 2 hojas y en las dos `limpiar_refs`
  falla ruidoso. No hay caso realizado; lo que estaba mal era la afirmación (§1.N.4).
- **Reglas duras, limpias.** Regla 4: los 24 `.str.contains(` sin `norm(` del árbol usan
  todos literal en MAYÚSCULA contra una serie ya normalizada (`INGRES`, `MEDIC`, `CHILEN`,
  `FALLECI`); no hay minúscula contra serie normalizada. Regla 5: 0 detecciones por nombre
  de archivo en `programas/`/`modulos/`/`gui/`.
- **Contratos completos:** `check_fuentes --todo` no reporta ningún lector sin contrato en
  las tres carpetas que vigila (18 contratos, 0 huérfanos); el único aviso es el encabezado
  SINTÉTICO de `rem_utils.cargar_maestro`, ya anotado en §4.
- **La suite corre por los dos caminos:** `pytest -q` -> 298 passed; archivo por archivo ->
  16/16 ok, 0 fallas (esta vez no salió el `tk.tcl` intermitente).

---
"""
rep("\n---\n\n## §3 — Verificación (estado actual)", ITEMS_2 + "\n## §3 — Verificación (estado actual)")

p.write_bytes((t.replace("\n", "\r\n") if crlf else t).encode("utf-8"))
print("ledger: bloques 1.N y 2 escritos + header de no-borrado. CRLF =", crlf)
