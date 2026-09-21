<!--
This document was generated with the assistance of Claude Fable 5 and Claude Opus 5 (Anthropic).
The human author reviewed, modified, and integrated the content.
Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# CLAUDE.md — autoREM

Herramienta local para tabular el **REM** (Registro Estadístico Mensual, MINSAL
Chile) desde exports crudos de **RAYEN/IRIS**. Nació en Salud Mental del CESFAM
Dr. Luis Ferrada Urzúa (SSMC) y apunta a ser **universal**: cualquier programa de
salud, cualquier centro.

**Este archivo es corto a propósito.** El detalle vive en un `CLAUDE.md` por carpeta,
que Claude Code carga solo cuando trabaja con archivos de esa carpeta. Los `§N` son
**anclas estables** (el código y los `docs/` los citan como «CLAUDE.md §N»):

| § | Tema | Dónde |
|---|---|---|
| 0 · 1 · 2 · 9 · 10 · 12 · 13 | preferencias, qué es, estado, versionado, git, roadmap, gotchas | aquí |
| 2.1 · 3 · 6 · 7 | familia población, pipeline A05, demografía, decisiones SM | [modulos/CLAUDE.md](modulos/CLAUDE.md) |
| 3.1 · 5 · 5.1 · 14 | filtro de mes, formatos IRIS/Admin, Monitoreo, catálogos DEIS | [programas/CLAUDE.md](programas/CLAUDE.md) |
| 8 · 10.1 · 11 | privacidad en detalle + hooks, worktrees, build del `.exe` | [tools/CLAUDE.md](tools/CLAUDE.md) |
| — | GUI: contrato de pantalla, trampas de Tk/hilos, reuso | [gui/CLAUDE.md](gui/CLAUDE.md) |
| — | convenciones de tests (no comparar texto plano de la GUI) | [tests/CLAUDE.md](tests/CLAUDE.md) |
| 4 | historia v1.2–1.6 | [CHANGELOG.md](CHANGELOG.md) |

> 🔎 **¿Vas a tocar la GUI, o revisarla?** El registro de las 13 rondas de
> code-review de la 2.0 está en
> [docs/review_gui-2.0_pendiente.md](docs/review_gui-2.0_pendiente.md), CERRADO y
> mergeado: §1 es lo **ya corregido** (greppable por símbolo) y §2 lo **descartado con
> motivo**. Reportar algo que ya está ahí es pagar dos veces el mismo hallazgo. Lo que
> sigue abierto vive en §4 de ese archivo y en el §12 de acá.

---

## 0. Autor y preferencias de trabajo

- **Autor:** Simón Tobar — médico APS, CESFAM Dr. Luis Ferrada Urzúa (SSMC).
- **Idioma:** inglés y español indiferenciado. Usar **"tú"**, nunca "vos".
- **Estilo:** técnico pero no aburrido; conciso, sin verborrea. Ir al grano, decir
  explícitamente cuando algo está equivocado.

## Reglas duras (leer antes de tocar nada)

1. **Privacidad** (detalle en §8). Nunca datos de pacientes en el repo: RUT, nombre,
   fecha de nacimiento, dirección, teléfono. **Avisar** si por error se cargan. Un RUT
   de ejemplo es siempre `11111111-1` (hubo un RUT real 2 meses en el repo público).
   Los exports reales viven solo en la carpeta de trabajo (OneDrive). Los hooks de
   pre-commit se instalan **en cada clon** (`python tools/hooks_git.py --instalar`).
2. **Fallar ruidoso, nunca callado y errado.** Un número plausible pero mal es el peor
   bug posible, porque se copia al REM. Mes sin datos → `ArchivoInvalido`, con la
   guarda sobre la FUENTE y no sobre la casilla (§3.1).
3. **Solo ASCII en los `.py`**: la consola cp1252 de Windows revienta con flechas,
   cajas o emoji (`tools/check_cp1252.py`, skill `check-cp1252`).
4. **Normalización:** buscar texto SIEMPRE con `contiene_todos` / `contiene_alguno` o
   `serie_norm.str.contains(norm("literal"))`. Un `.str.contains("minúscula")` crudo
   contra una serie normalizada nunca matchea. Y ojo: una subcadena **contigua** falla
   callada ante un artículo intercalado (A32·F2 dio 0 estructural hasta 1.9.10).
5. **Detectar por CONTENIDO, nunca por nombre de archivo**: RAYEN baja todo como
   `Formulario_Rayen.xlsx`. Identificar por firmas (ancla, banner, columnas) y
   **confirmar con el usuario**.
6. **100% local, offline.** Sin nube (Ley 20.584 y 21.719).
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
   el `CHANGELOG` es permanente, y una cita colgada ahí no se arregla después.

   Los **scripts** de trabajo intermedio (repros, arneses de medición, prompts de ronda)
   viven en el scratchpad de la sesión, que es temporal. Cuando la rama o el worktree que
   los produjo cierra su trabajo, se archivan en
   **[docs/evanesced/](docs/evanesced/README.md)** — se archivan **como quedaron**, sin
   reescribirlos, y sin copias de fuentes del repo ni binarios (el README dice por qué y
   cómo se recuperan).

---

## 1. Dependencias

- **Runtime:** `openpyxl` + `pandas`. `tkinter` viene con el Python de Windows.
  La GUI (2.0, desde sep-2026): `customtkinter`.
- **Build:** `PyInstaller` (§11). Todo se empaqueta en el `.exe`, así que sumar deps
  no cuesta: prima **minimizar líneas de código**.

---

## 2. Estado actual del repo

Versión **2.0.5** (§9). **321 tests.**

**Qué es compartido y qué es modular:**
- **Compartido — `programas/`:** primitivas (`rem_utils`), eje de formato IRIS/Admin
  (`formatos`), lookups transversales (`estamentos`, `dotacion`), tabla por-RUN
  (`poblacion`), hoja LEEME (`cobertura`), catálogos DEIS (`catalogos`) y la capa del
  formulario de Salud Mental (`rem_saludmental`).
- **Modular — `modulos/`:** un reporte por archivo. A05 N/O · A03 D.3 · A23 · SM
  Actividades · SM Trabajo Perdido · SP·P6 y SM Rescate (estos dos **en validación**).
- **Interfaz — `gui/`:** la **GUI** (2.0, `customtkinter`), declarativa: una pantalla por
  archivo en `gui/paginas/`, descubiertas por introspección. Shell y router en `app.py`,
  frontera con el hilo worker en `runner.py` -> [gui/CLAUDE.md](gui/CLAUDE.md). Es la
  que corre el `.exe` desde la **2.0.0**; la 1.x quedó congelada en `legacy/`.
- **Dispatcher — `autorem.py`:** ya no dibuja nada. Registro de tareas del A05,
  orquestación compartida (`_correr_tareas`) y el CLI **congelado** (§12).

Cadena de imports: `rem_utils` ← `formatos` ← capas ← módulos ← `autorem` / `gui`. Imports
**absolutos** rooteados en la raíz (`from programas.rem_utils import …`).

```
autorem.py        entry point / dispatcher (único código en la raíz)
programas/        capas compartidas         -> programas/CLAUDE.md
modulos/          un reporte REM por archivo -> modulos/CLAUDE.md
tools/            utilitarios de desarrollo  -> tools/CLAUDE.md
gui/              la GUI (customtkinter)      -> gui/CLAUDE.md
catalogos/        CIE-10 / ENO / GES + maestro_slim, que shippea el exe (§14)
refs_tablas/      planillas de EJEMPLO, solo header (whitelist por archivo)
  specs/            DAX + visuales del PowerBI por página (skill pbip-spec)
.claude/skills/   limpiar-refs · check-cp1252 · versionar · tests-fuentes
legacy/           monolitos viejos + la GUI 1.x congelada (.py.gz; no se importan)
tests/            pruebas automáticas        -> tests/CLAUDE.md
docs/             planes y contexto por módulo
  evanesced/        scripts de repro de ramas/worktrees ya cerrados (§0 regla 7)
```

**Nombre de módulo:** `rem_<pestaña>_<casilla>_<descriptor>`; la `<casilla>` es la
celda/columna del REM (A05: `n` = ingresos, `o` = egresos). El `id` del `TAREA` la
incluye (`a05_o_egresos`).

**Arquitectura (2 ejes ortogonales):**
- **Formato** `iris` | `administrativo`: **se detecta automáticamente por contenido y
  lo verifica el usuario**. El selector de la 1.x ya no existe (2.0.0): sobraba, porque
  no le podía ganar a la detección -- solo aportaba una forma de equivocarse.
  Aplica a **todos** los reportes RAYEN con dos formatos, no solo al formulario SM (§5).
- **Tarea** (`autorem.TAREAS`): agnóstica al formato. Las tareas del mismo archivo
  corren juntas → un `…_procesado.xlsx` con una hoja por tarea.

**Arranque:** sin args → GUI · arrastrar un `.xlsx` sobre el exe → GUI con la ruta
precargada · `--cli entrada.xlsx [--formato] [--tarea] [--mes AAAA-MM]` → **el CLI es
solo del A05**. El resto de los módulos es solo GUI, y no hay plan de CLI para todos.
El CLI quedó **CONGELADO** en la 2.0.0 (§12): no se le portan los cambios.

**Salidas y caché:**
- La carpeta de salida por defecto es **la de los archivos de entrada**, no el cwd
  desde donde se corre el `.py`: las salidas llevan RUT y deben quedar junto a los
  exports, fuera del repo.
- **Una salida nunca pisa otra** (`rem_utils.rutas_libres`): si el nombre existe, la
  corrida entera sale como `… (1).xlsx`, con el mismo número en todos sus archivos. Y
  se escribe vía temporal + rename (`escribir_atomico`): un corte deja un
  `….escribiendo.xlsx`, nunca un resultado roto con nombre de resultado.
- El caché de usuario vive en **`~/.autorem/`** (`C:\Users\<usuario>\.autorem\`), no en
  `%APPDATA%` ni junto al exe: `estamentos.json` y `dotacion.json`. Se lee y guarda por
  `rem_utils.leer_cache_json`/`guardar_cache_json`: **ningún problema de caché es
  callado** (se muestra, y el detalle para el usuario está en «Acerca de»). Los tests
  **nunca** tocan el real: todo `tests/test_*.py` importa primero `_aislar_cache`.

**`refs_tablas/`:** planillas de ejemplo **sí versionadas**, con whitelist POR ARCHIVO
en el `.gitignore`: un `.xlsx` nuevo queda ignorado hasta vetarlo (skill
`limpiar-refs` = recortar a solo header). También se versionan las plantillas target
`SA_26` / `SP_26` `.xlsm`, para que git note cuándo MINSAL cambia su estructura. El
`.xls` de RAYEN no: openpyxl no lo lee, hay que convertirlo a `.xlsx`.

---

## 9. Versionado y convenciones

`X.Y.Z` versiona **el software** (un binario, un `rem_utils.VERSION`):
- **X** = cambio grande de arquitectura / incompatible, **o plantillas REM de un año
  nuevo** (SA y SP cambian cada año; actualizarlas es pega del dev). Hecho: **2.0.0**
  = GUI 2.0 (sep-2026). Planeado: **3.0.0** = plantillas REM 2027.
- **Y** = módulo o reporte nuevo (de cualquier programa de salud).
- **Z** = corrección. Reinicia a 0 al subir Y.

**Año de reporte vigente: 2026** (`SA_26` / `SP_26`).

**No se reservan números para hitos:** la versión mide avance, y no se congela
esperando una validación. (El 1.10.0 ya no está apartado para la familia población.)

Con puntos (`1.4.10`), para que Z pase de 9. Estado actual: **2.0.5**.

- **Cada `.py` lleva la versión de SU último cambio**, no todas sincronizadas.
  Llevan versión: `autorem.py`, `programas/`, `modulos/`, `tools/`. No llevan: `tests/`
  y `__init__.py`. **Exento:** `legacy/`.
- `tools/check_version.py` (en el pre-commit) verifica el manifiesto, la versión de
  este archivo (las dos frases en negrita de arriba: **no las reformules**), el
  CHANGELOG y los contadores de tests **de este archivo y del README** (desde la
  2.0.5; antes solo miraba éste, y el del README derivó a 311 con 309 reales).
  Valen igual para el README: **no reformules** la frase «**N pruebas** en M
  archivos» sin actualizar `CONTADORES`, porque un patrón que deja de matchear no
  falla — deja de vigilar. **Skill `versionar`.** Árbitro anti-colisión entre
  sesiones paralelas = el CHANGELOG.
- **Header en cada archivo:** «This code/document was generated with the assistance
  of [modelo]. The human author reviewed, modified, and integrated the code.» + autor
  + `SPDX-License-Identifier: GPL-3.0-or-later` + versión.
- **Licencia GPL-3.0-or-later.** Distribuir `LICENSE` junto al `.exe`.
- Comentarios y mensajes al usuario en español; nombres de función mixtos, OK.

> ⚠ «Programa» tiene dos sentidos: el número versiona el **software**. Los
> **programas de salud** avanzan en paralelo y van en la matriz de abajo.

**Matriz de programas de salud.** Nace de las páginas del PowerBI «poblacion ferrada»
(`refs_tablas/specs/`), pero los módulos se han ido apartando del DAX en el camino. La
semilla de Cardiovascular, SSyR y Dependencia es esa misma spec.

| Programa | Módulos | Estado |
|---|---|---|
| **Salud Mental** | A05 N/O · A03 D.3 · Actividades (A04·A06·A19a·A26·A27·A32) · Trabajo perdido | ✅ (REM de agosto 2026 hecho completo con la herramienta) |
| **Salud Mental — población** | SP·P6 A.1 + Rescate de inasistentes, vía `programas/poblacion.py` | 🚧 en validación (§2.1) |
| **Respiratorio** | A23 (indicadores · SALA · Secciones G y H · tablas por sección) | 🚧 IRIS ✅ · Monitoreo Admin parcial · falta formulario admin y afinar A/I-espiro/O |
| **Dependencia / Domiciliaria** | `rem_a26_domiciliaria` (A26·A1) | 📌 anotado, sin implementar (§12) |
| Cardiovascular · SSyR · otros | — | pendiente |

---

## 10. Git

- El repo vive **fuera** del OneDrive del trabajo; los exports con PII se quedan allá.
- Rama `main`. Claude Code trabaja en worktrees: **el stash y los hooks son
  compartidos** entre todos los árboles (§10.1). Usar commits WIP, no stash.
- Cuatro checks de pre-commit, instalados **en cada clon** (§8.2). Uno de ellos,
  `check_fuentes`, exige un CONTRATO para todo lector de planillas del usuario (skill
  `tests-fuentes`): un input nuevo se escribe **con** su contrato.

---

## 12. Roadmap — pendiente

(Lo hecho está en el [CHANGELOG](CHANGELOG.md).)

**En curso**
- **Cerrar la 2.0 a ojo:** mirar la ventana con ojos humanos (`python -m gui.app`) y
  **compilar el `.exe`** (`pyinstaller autoREM.spec`) para probar los arreglos de
  empaquetado contra un build real -- es el paso 13 del plan, y la primera vez que
  se pueden probar: hasta la 2.0.0 la GUI 2.0 no entraba al bundle. Checklist en
  [docs/review_gui-2.0_pendiente.md](docs/review_gui-2.0_pendiente.md) §4.
- **Ronda de EFICIENCIA y REUSO sobre el codebase completo** (decisión del autor,
  sep-2026): la primera revisión de la era 2.0, sobre `main`. No era parte de la
  revisión de la rama.
- **El CLI queda CONGELADO** (decisión del autor, sep-2026): no sigue el rediseño
  de la GUI. Quizás vuelva a funcionar más adelante, probablemente no. Consecuencia
  conocida y aceptada: los mensajes cruzados de `validar_iris`/`validar_admin` dicen
  «Cambia el selector de formato», y ese selector ya no existe; y el uso del `--cli`
  manda el A03 «a la pestaña Screening», que tampoco existe. Solo se alcanzan desde
  el CLI y el notebook 1.x, las dos superficies congeladas. Si el CLI revive, los
  textos se revisan junto con él.
- **Validar la familia población** (§2.1): la brecha `Ingresado` del P6 y el rescate
  contra datos reales.

**Módulos**
- **`rem_a26_domiciliaria`** (A26·A1): las 24 VDI del PADDS por subtipo × visita +
  planes de cuidado a usuario y cuidador. Su punto de entrada es `EXCLUIR_SMISH` del
  Trabajo Perdido. Base: página «Dependencia» del PowerBI + `poblacion.py`.
- **Delta P(m) − P(m−1) → A05 N/O** (fase 4 del plan P6): portar el
  `CALCULADOR_A05_DESDE_P_2.1_junio.xlsx`, no reinventarlo. **P y A no calzan banda
  por banda** porque tienen algunos diagnósticos distintos, casillas protegidas
  distintas en los rangos etarios y demografía ordenada distinto.
- **Auditoría de actividades habilitadas** (utilidad no-REM, destino GUI ·
  Utilidades): qué actividades mínimas del `SA_26` le faltan activadas a cada
  funcionario ACTIVO, para jefatura. Crosswalk SA → RAYEN validado en la GUI. Primer
  corte: SM. [docs/actividades_profesionales_plan.md](docs/actividades_profesionales_plan.md).
- **A03 D.3 v2:** conteos por rango etario extraídos del `SA_26`.
- **Otras Causas:** popup con los RUT + dropdown abandono/clínica.
- **Dotación fase 2:** bloques apilados REM/externos por sección (validación en pausa
  hasta recibir la lista de externos).

**Correcciones y mejoras**
- **Demografía del grupal.** El grupal sí trae RUN. Fuente por
  RUN en cascada: **Informe Inscritos** (ya es input opcional del SM; cubre a toda la
  población inscrita) → última fila del ADA ya cargado → **sin dato**. Tres estados, no
  dos: un «sin dato» contado como NO subcuenta callado. La cobertura va a la LEEME.
- **Rendimiento de lectura** (sin urgencia): medir primero dónde se va el tiempo
  (lectura del `.xlsx` vs cálculos). Si es la lectura, probar `python-calamine`
  (`engine="calamine"`) contra la «dimension rota» de RAYEN. Cortar un mismo `.xlsx`
  y leer las partes en paralelo no rinde, porque no hay acceso aleatorio por fila.
- **Destrabar la GUI durante la carga de una página** (2.0.2; el autor lo probó y lo
  llamó «VERY JARRING»). Construir una página **bloquea el hilo de la GUI varios
  segundos**, y mientras tanto Windows no puede repintar: la ventana se ve ROTA — sin
  sidebar, con el texto del Inicio a medio dibujar y pedazos de la página que se está
  armando. Pasa igual con el `.exe` y con `python -m gui.app`, o sea **no es empaquetado**.

  **Medido** (con `mainloop` real; arneses en `docs/evanesced/gui-2.0_merge/`):

  | Página | Bloqueo |
  |---|---|
  | `acerca_de` | **7105 ms** |
  | `sm_actividades` | 5753 ms |
  | `a23_respiratorio` | 1813 ms |
  | `a05` | 1090 ms |
  | `sp_p6_poblacion` | 1031 ms |
  | `inicio` | 89 ms |

  **No se arregla con hilos, y está medido, no supuesto.** `cProfile` dice que el costo
  es Tk puro: `sm_actividades` = 7,1 s de 8,4 en `_tkinter.tkapp.call` (101.700 llamadas);
  `acerca_de` = 6,1 s de 7,1 (76.181). No hay I/O ni imports que adelantar, y los widgets
  de Tk solo existen en el hilo del `mainloop` (un intérprete Tcl por hilo), así que
  crearlos en un worker es la trampa #1 de `gui/CLAUDE.md`.

  **El arreglo propuesto:** que `_construir_pagina` **ceda el control**, convirtiéndola en
  un **generador** que hace `yield` entre pasos (título, cada input, extras, mes/carpeta,
  log, botones). El generador conserva sus closures solo, así que encaja con el código
  actual sin desarmar el contrato `PANTALLA`. Los llamadores: `mostrar` lo drena entero
  (comportamiento de hoy) y la precarga lo avanza **un paso por tick**. Con ~10 pasos,
  `sm_actividades` pasa de un bloqueo de 5753 ms a tramos de ~570 ms.

  **Lo que ya está hecho** y no hay que rehacer:
  - La **precarga incremental** con barra al pie (`App._precargar_tick`,
    `widgets.barra_precarga`), con sus tests. Queda **apagada**: `App(precargar=False)`
    por defecto, porque hoy junta los bloqueos al arranque y empeora la primera
    impresión. Encenderla es cambiar ese default, una vez que el generador exista.
  - Las páginas ya **no se gridean mientras se construyen**, que era una causa aparte:
    customtkinter llama `update_idletasks()` al crear cada widget, así que un frame
    gridado se PINTA a medio armar. Eso daba páginas superpuestas; ya no pasa.

  **Ojo al implementarlo:** `acerca_de` e `inicio` son **páginas especiales**, no están en
  `registro` y por eso la precarga no las cubre — y `acerca_de` es justamente la más cara
  de todas. La solución tiene que incluirlas, o se arregla todo menos lo peor.
- **Catálogos en la GUI** (fecha visible + actualización manual en modo
  avanzado): va en [docs/GUI_2.0_plan.md](docs/GUI_2.0_plan.md) §7.1. La parte de
  lógica (drop-in en `~/.autorem/catalogos/`) se hace en `main`.
- **Generalizar a otros centros:** un config en vez de constantes locales
  (`EXCLUIR_PATOLOGIA`, externos de dotación, sectores…).

**Dev / repo**
- **Pestaña de Consultas de catálogos** + enchufar `en_rango` en el A23.
- **Deuda:** `rem_utils.grid()` dispara `Pandas4Warning` (`m & muj` con dtype mixto);
  pandas 4 lo vuelve error.

---

## 13. Gotchas generales

- **OneDrive:** los exports sí están en OneDrive. Un `.xlsx` recién sincronizado puede
  leerse a medio bajar (truncado). Fue la fuente de la mitad de los dolores de cabeza
  del arranque: si un test falla raro tras tocar un archivo ahí, forzar la
  sincronización antes de culpar al código.
- **Excel abierto:** `wb.save()` → `PermissionError`, ya manejado con un mensaje amable.
- **Formato distinto de `.xlsx`:** la herramienta lee solo `.xlsx`. El HTML disfrazado
  de `.xlsx` típico de RAYEN (`BadZipFile`) y los `.xls` caen en el diálogo «No es un
  .xlsx» (`_es_error_formato`).
- **`norm()` mapea NaN → `''`**: `nan or ''` es truthy y daba `"NAN"`, inflando flags.
