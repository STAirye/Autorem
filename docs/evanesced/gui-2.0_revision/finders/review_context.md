# Code review context - autoREM, branch `gui-2.0` vs `main`

Repo: `E:\git\Autorem` (Windows, git). Checkout actual = `gui-2.0` en **`f94a0ec`** (limpio).
Merge-base con main: `03e15f6`. Scope = `git diff main...HEAD`
(**80 archivos, 12224 inserciones, 606 supresiones**).

**Genera el diff tu mismo con `git diff main...HEAD`.** Hay un snapshot en
`…\scratchpad\gui20_f94a0ec.diff` (15027 lineas) por comodidad, pero si HEAD se movio, el
comando manda. **STALE, no usar:** `gui20.diff`, `gui20_fd1b0cc.diff`, `gui20_f42308d.diff`.

Los bugs en lineas NO tocadas de funciones que el diff toca o LLAMA entran en scope cuando el
codigo nuevo los re-expone (p. ej. una pagina de la GUI llamando a `programas/` o `modulos/`).

NO modifiques nada dentro de `E:\git\Autorem`: ni edits, ni comandos git que cambien estado,
ni salidas escritas dentro del repo. Los scratch van SOLO en tu scratchpad.

## Entorno

Python 3.9.13 + pandas 2.3.3 + openpyxl 3.1.5 + customtkinter 6.0.0 + pytest 8.4.2, todo
instalado (`python`). El autor ademas prueba con pandas 3.0.5 / Python 3.14. Los modulos de
la GUI importan normalmente; una ventana real necesita display
(`tests/test_gui_construccion.py` muestra como armar paginas y bombear eventos). Llamar a la
funcion de `programas/`/`modulos/` con los mismos argumentos que le pasa el `correr`/`preparar`
de la pagina sigue siendo el repro mas barato.

**Caches:** todo `tests/test_*.py` importa `tests/_aislar_cache.py` PRIMERO, que apunta
`~/.autorem/dotacion.json` y `estamentos.json` a un temp. Si escribes un repro que toque
`programas.dotacion` o `programas.estamentos`, haz lo mismo (o fija tu `RUTA_CACHE`): la suite
llego a pisar el cache REAL del autor y eso no puede volver a pasar.

---

## UPDATE 2026-09-20 - estado tras la ronda 12 (LEER PRIMERO)

Las rondas 1-12 estan committeadas en cinco commits `wip(...)` sobre `origin/gui-2.0`
(`fd1b0cc` r1-4, `f42308d` r5-6, `299e7d4` r7-9, `c8aef4e` r10-11, `f94a0ec` r12).
**Son BACKUPS, no releases.**

- **`docs/review_gui-2.0_pendiente.md` es la fuente de verdad del estado**, no este archivo.
  §1 = ya corregido (por ronda, greppable) · §2 = descartado con motivo · §3 = verificacion ·
  §4 = que falta · §5 = bitacora con el ANGULO de cada ronda. Leelo antes de reportar:
  repetir un hallazgo de §1 o §2 es pagar dos veces.
- **296 tests verdes**, `check_version` OK (1.9.17), `check_cp1252` OK, `check_fuentes --todo`
  OK (18 contratos). Ojo: `pytest --collect-only` dice **298** porque cuenta casos
  parametrizados; `check_version` cuenta `def test_` (296). Las dos cifras son correctas cada
  una en su convencion - **no es un hallazgo**.
- En la corrida completa de pytest sale a veces el `tk.tcl` intermitente de
  `test_gui_construccion` (pasa solo; lo investiga una sesion aparte).

### Angulos YA corridos (§5 del ledger) - no los repitas

| # | Angulo |
|---|---|
| 1-2 | Bug recurrente en la familia poblacion + GUI; auditoria estatica de loaders + paridad del port + trampas de Tk/hilos |
| 3 | **A** - barrido linea por linea del diff, con las firmas de cada callee verificadas |
| 3b | A ojo, el autor corriendo `python -m gui.app` |
| 4 | **B** - comportamiento REMOVIDO por el port (cada linea borrada; cada `_tab_*` portado) |
| 5 | **C** - trazado entre archivos (cada llamada de `gui/` a `programas/`/`modulos/`/`tools/`) |
| 6 | **D** - trampas de lenguaje/framework (Tk, hilos, closures, pandas, rutas Windows) |
| 7 | **E** - envoltorios e indirecciones (`Pagina`, `_resolver_ctx`, `runner`, `widgets`, dialogos) |
| 8 | Reuso: codigo nuevo vs helpers que ya existian |
| 9 | Bug recurrente EMPIRICO: cada `correr` contra exports vacios TRAS un filtro |
| 10 | Bug recurrente ESTATICO: cada loader y filtro alcanzable desde las paginas |
| 11 | Cada referencia y fallback contra el export REAL (interactiva, con el autor) |
| 12 | Altitud: cada arreglo de las rondas 1-11, esta a la altura de su causa? |

### Angulos que NO se han corrido

- **Eficiencia**: nadie miro si la GUI 2.0 relee archivos o rehace trabajo.
- **Convenciones**: headers de version de cada `.py` de `gui/` vs su ultimo cambio real
  (se sincronizaron a 1.9.17 los tocados; el resto no se audito).
- **Prueba a mano del cache en el PC del trabajo** y otra pasada a ojo del autor
  (no es para un agente).

**§4 del ledger esta desactualizado en un punto:** dice que falta la paridad del port de
`_tab_beta` y de los dialogos de dotacion, pero §5 los da por cubiertos (la ronda 4 lista
`_tab_beta` explicitamente, y la nota de la ronda 3 dice que los dialogos de dotacion son
fieles linea por linea, incluido el `orden` por `attrs['por_estamento']`). Resuelve esa
contradiccion antes de gastar una ronda ahi.

---

## Que es la herramienta

autoREM: herramienta local que tabula el REM chileno (estadistica mensual de salud) desde
exports crudos de RAYEN/IRIS. Los numeros se copian a un informe oficial, asi que **un numero
plausible pero MAL es el peor bug posible** (peor que un crash). Reglas del CLAUDE.md raiz
(citalas si marcas una violacion de convencion):

1. Privacidad: nunca datos de pacientes en el repo. Las salidas llevan RUT y se escriben AL
   LADO de los exports de entrada (carpeta de salida por defecto = la de los inputs, NO el
   cwd), fuera del repo. RUT de ejemplo siempre `11111111-1`.
2. "Fallar ruidoso, nunca callado y errado." Mes sin datos -> `ArchivoInvalido`, con la guarda
   sobre la FUENTE, no sobre la casilla (§3.1).
3. Solo ASCII en los `.py` que imprimen a consola (cp1252). Los literales con tilde de la GUI
   son practica existente: marca solo flechas, cajas o emoji en rutas de consola.
4. Normalizacion: buscar texto SIEMPRE con `contiene_todos`/`contiene_alguno` o
   `serie_norm.str.contains(norm("literal"))`.
5. Detectar por CONTENIDO, nunca por nombre de archivo.
6. 100% local y offline.

Versionado §9: `X.Y.Z`; cada `.py` de `autorem.py`, `programas/`, `modulos/`, `tools/` (y ahora
`gui/`) lleva la version de SU ultimo cambio; `tools/check_version.py` lo verifica; "Arbitro
anti-colision entre sesiones paralelas = el CHANGELOG". Hay `CLAUDE.md` por carpeta en
`programas/`, `modulos/` y `tools/`; el plan de la GUI es `docs/GUI_2.0_plan.md`.

## Que hace la rama

Agrega la GUI 2.0 (customtkinter): `gui/app.py` (shell, router, `_resolver_ctx`, `Pagina`),
`gui/registro.py` (descubrimiento de paginas), `gui/runner.py` (hilo worker + despacho de
errores), `gui/widgets.py`, `gui/dialogos.py` (modales de Estamentos y Dotacion), paginas en
`gui/paginas/` (a05, a23, sm, poblacion, inicio, about). Mueve
`refs_tablas/maestro_slim.csv.gz` -> `catalogos/maestro_slim.csv.gz` (+ `.gitignore`, spec,
`tools/slim_maestro.py`). Suma "gui" a `DIRS_VERSIONADOS` de `tools/check_version.py`. La GUI
vieja de `autorem.py` sigue siendo el entry point del exe (congelada hasta el paso 11 del plan).
El commit `c38a8cc` (solo en esta rama) arregla un bug de `programas/poblacion.py`.

Piezas compartidas nuevas que un revisor se va a encontrar (todas documentadas en su docstring):
`rem_utils.abrir_xlsx_ro`/`filas_hoja` (toda lectura read_only), `rutas_libres` (las salidas
nunca se pisan: `… (n).xlsx`, el mismo n para toda la corrida), `escribir_atomico` (temporal +
rename), `leer_cache_json`/`guardar_cache_json`/`apartar_cache` + `_AVISOS_CACHE` (las fallas de
cache las muestra `gui.runner.avisar_cache`), `runner.Canal` (solo el ultimo preview asincrono
se pinta), `dialogos._DOTACION_ABIERTA` (un dialogo de dotacion a la vez: en Windows
`CTkToplevel.__init__` corre un `update()` completo) y `App._al_cerrar` (la X pregunta si hay
una corrida viva).

---

## EL BUG RECURRENTE (el autor pide atencion especial) - c38a8cc

`poblacion.cargar_inscritos()` con un export con encabezado pero **0 filas de datos** devolvia
un DataFrame vacio; mas abajo (`construir_poblacion`) una columna construida sobre el frame
vacio terminaba dtype float64 y `.str.contains()` tiraba
`AttributeError: Can only use .str accessor with string values, not floating` - un crash
criptico en vez de un `ArchivoInvalido("sin_datos", ...)` claro en la FUENTE. La misma familia
ya se habia arreglado en 1.9.12 (6ca8b6e): el A23 con un export vacio reventaba con
`ValueError: NaTType does not support strftime` al loguear min/max de fechas antes de llegar a
la guarda de `filtrar_mes`.

**Estado: la clase se dio por CERRADA** en todos los loaders conocidos (§1.A) y se barrio dos
veces mas, empirica (ronda 9, §1.J) y estaticamente (ronda 10, §1.K), mas la ronda 11 contra
los exports reales (§1.L). Repro empirico de 0 filas hecho sobre SM grupal / Inscritos /
Multiprofesional, Trabajo Perdido / Maestro, Poblacion Formulario / ADA / Inscritos, A05 (IRIS
y Admin, con y sin mes), A03 (4 instrumentos), Cupos y Estratificacion: **todos** dan
`ArchivoInvalido`.

Lo que queda por cazar es la clase en codigo NUEVO o tocado por rondas posteriores:
- un loader que acepta un export con 0 filas (o un resultado que queda vacio TRAS un filtro:
  mes, mascara de programa, dedupe, responsable, parseo de fechas) y deja fluir el frame vacio,
  donde `.str`/`.dt`, `min()/max()` -> NaT formateado, `int(NaN)`, `iloc[0]`, `idxmax`,
  `sorted()` de NaN/str mezclados, groupby vacio, `np.where` dando float64, `.map`/`.apply`
  sobre object vacio infiriendo float64, etc. revientan criptico - O, peor, producen ceros o
  numeros errados en silencio en vez de `ArchivoInvalido`.
- la misma guarda presente en un loader y ausente en sus hermanos.
- rutas de la GUI (callbacks de preview, `dialogos.dotacion_ada`, `al_completar`, `resumen`)
  que corren sobre datos vacios o parciales FUERA del manejo de errores del worker: un crash
  ahi no se le muestra al usuario (excepcion en callback de Tk dentro de un exe windowed =
  invisible).

---

## Hechos ya verificados (no los re-derives)

- `main` publico su propio 1.9.16 (10beb79) y la rama reclamaba el mismo numero -> colision.
  **RESUELTO: la rama paso a 1.9.17** (ledger §1.E).
- **`main` NO tiene la guarda de `c38a8cc`** en `programas/poblacion.py` (verificado el
  2026-09-20: 4 ocurrencias de `sin_datos` en la rama, 0 en main). El arreglo existe solo en
  `gui-2.0`, asi que el merge tiene que llevarlo.
- `requirements.txt` ya lista `customtkinter` (y menciona `pytest` como dep de desarrollo).
  **RESUELTO** (ledger §1.E).

## NO son hallazgos (ya decidido - no los reportes)

- Version congelada en **1.9.17** y la entrada `## [1.9.17]` del CHANGELOG ABIERTA; los commits
  `wip(...)`. Son backups a proposito.
- `autoREM.spec` no empaqueta `gui.app` ni `gui.registro`: **postergado al paso 11** por
  decision del autor (ledger §4). Consecuencia conocida: hoy no se puede compilar el exe para
  probar los arreglos del sidebar.
- `autorem.py` sigue lanzando la GUI 1.x; la 2.0 arranca con `python -m gui.app`.
- `gui/runner.py` duplica helpers de `autorem.py` y ya divergieron (hallazgo #14; se resuelve
  con el merge limpio del paso 11).
- El CLI congelado, y los mensajes de `validar_iris`/`validar_admin` que nombran un selector de
  formato que la 2.0 ya no tiene (CLAUDE.md §12).
- Literales con tilde en strings de la GUI (practica existente).
- La diferencia 296 / 298 tests (ver arriba).

---

## Formato de salida (devuelve exactamente esto, sin preambulo)

Hasta 8 candidatos, el mas grave primero, cada uno asi:
```
- file: <ruta relativa al repo>
  line: <linea 1-indexed en el archivo ACTUAL de gui-2.0>
  category: <correctness | recurrent-empty-data | reuse | simplification | efficiency | altitude | conventions | test-coverage | ...>
  summary: <una frase con el defecto>
  failure_scenario: <inputs/estado concretos -> numero errado o crash; para limpieza: el costo concreto>
  evidence: <linea(s) citada(s) + la salida de los comandos que corriste>
```
Si no encuentras nada real para tu angulo, devuelve lista vacia. No rellenes.

Al cerrar, emite ademas el texto listo para pegar en el ledger: la fila de §5 (bitacora, con
TU angulo) y tu bloque en §1 - o en §2 lo que perseguiste y NO era bug. Que el §2 salga aunque
tu lista venga vacia: saber que ya se miro es la mitad del valor de la ronda.
