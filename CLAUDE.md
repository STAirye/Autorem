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
   reescribirlos, y sin copias de fuentes del repo ni binarios (el README dice qué hay y
   cómo se recupera; las reglas de la carpeta están en
   [docs/evanesced/CLAUDE.md](docs/evanesced/CLAUDE.md)).

---

## 1. Dependencias

- **Runtime:** `openpyxl` (escribir) + `python-calamine` (leer los exports) + `pandas`. `tkinter` viene con el Python de Windows.
  La GUI (2.0, desde sep-2026): `customtkinter`.
- **Build:** `PyInstaller` (§11). Todo se empaqueta en el `.exe`, así que sumar deps
  no cuesta: prima **minimizar líneas de código**.

---

## 2. Estado actual del repo

Versión **2.0.29** (§9). **394 tests.**

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
  orquestación compartida (`_correr_tareas`) y el CLI **congelado** (ver «Arranque»).

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
.claude/skills/   limpiar-refs · check-cp1252 · versionar · tests-fuentes · inventario-rem
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
El CLI quedó **CONGELADO** en la 2.0.0 (decisión del autor, cerrada): no se le portan
los cambios ni se va a actualizar. Consecuencia conocida y aceptada: los mensajes
cruzados de `validar_iris`/`validar_admin` dicen «Cambia el selector de formato» (ya no
existe) y el `--cli` manda el A03 «a la pestaña Screening» (tampoco). Solo se alcanzan
desde el CLI y el notebook 1.x, las dos superficies congeladas.

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

Con puntos (`1.4.10`), para que Z pase de 9. Estado actual: **2.0.29**.

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
| **Dependencia (PDS) + Cuidados Paliativos (CPU)** | A03·D.6 · A05·J/V · A26·A.1/C · A27 · A33 · P3 · P5 | 📌 inventariado (docs/pds_cpu_casillas_*.md), sin implementar (§12) |
| **Epidemiología** | A04·P a U (encuesta, quimioprofilaxis, muestras, seguimiento de contactos, BAI, BAC) | 📌 inventariado ([docs/epidemiologia_casillas_SA.md](docs/epidemiologia_casillas_SA.md)), **bloqueado por registro**: hoy todo se anota como gestión y T/U no están habilitadas |
| Cardiovascular · SSyR · otros | — | pendiente |

---

## 10. Git

- El repo vive **fuera** del OneDrive del trabajo; los exports con PII se quedan allá.
- Rama `main`. Claude Code trabaja en worktrees: **el stash y los hooks son
  compartidos** entre todos los árboles (§10.1). Usar commits WIP, no stash.
- Cuatro checks de pre-commit, instalados **en cada clon** (§8.2). Uno de ellos,
  `check_fuentes`, exige un CONTRATO para todo lector de planillas del usuario (skill
  `tests-fuentes`): un input nuevo se escribe **con** su contrato.
- **Tag por versión del `.exe`:** toda versión que cambie el comportamiento del
  ejecutable lleva un `git tag X.Y.Z` (lightweight, **sin** `v`, como los 37 que ya
  hay) sobre el **último commit funcional** de esa versión, no sobre uno de solo docs.
  Lo pone la sesión que cierra la versión. Los commits de solo docs no llevan tag. El
  push es a mano: `git push --follow-tags` no sube tags lightweight, así que van con
  `git push origin X.Y.Z` o `git push --tags`.

---

## 12. Roadmap — pendiente

(Lo hecho está en el [CHANGELOG](CHANGELOG.md).)

**En curso**
- **Validar la familia población** (§2.1) — **LO MÁS CALIENTE** (oct-2026): la brecha
  `Ingresado` del P6 y el rescate contra datos reales.

**Módulos**
- **Módulo PDS + CPU** (antes anotado como `rem_a26_domiciliaria`, que se quedaba
  corto): toca **A03·D.6, A05·J/V, A26·A.1/C, A27·A/B, A33, P3·A/B y P5·A/B**. El
  inventario con los valores reales de agosto (SA) y junio (SP), las reglas del
  Comentado y del Manual P, y los formularios que faltan bajar está en
  [docs/pds_cpu_casillas_SA.md](docs/pds_cpu_casillas_SA.md) y
  [docs/pds_cpu_casillas_SP.md](docs/pds_cpu_casillas_SP.md) (skill `inventario-rem`).
  Su punto de entrada es `EXCLUIR_SMISH` del Trabajo Perdido. Base: página
  «Dependencia» del PowerBI + `poblacion.py`.
- **Módulo Epidemiología (A04·P a U)** — **bloqueado por registro, no por código**: hoy
  todo se anota como trabajo de gestión (`AG_`), que no va a ningún REM. Q, R y S tienen
  actividad literal habilitada (ADA); P, T y U salen del grupal y, salvo una fila de P,
  no están habilitadas. Se programa cuando haya un mes registrado bien:
  [docs/epidemiologia_casillas_SA.md](docs/epidemiologia_casillas_SA.md) §4.
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
- **Rango de meses** (reportes de 3/6 meses; plan aprobado sep-2026, sin implementar):
  SM Actividades + TP, después A05. Se corre el motor MENSUAL por mes y se agrega una
  vez (filtrar el rango entero rompe GESTANTE y los distintos del TP).
  [docs/rango_meses_plan.md](docs/rango_meses_plan.md).
- **Catálogos en la GUI** (fecha visible + actualización manual en modo
  avanzado): va en [docs/GUI_2.0_plan.md](docs/GUI_2.0_plan.md) §7.1. La parte de
  lógica (drop-in en `~/.autorem/catalogos/`) se hace en `main`.
- **Generalizar a otros centros:** un config en vez de constantes locales
  (`EXCLUIR_PATOLOGIA`, externos de dotación, sectores…).

- **Eficiencia: lo que quedó de las rondas 2.0.6 y 2.0.9**, con su costo MEDIDO (los
  arneses están en [docs/evanesced/eficiencia-2.0.9/](docs/evanesced/eficiencia-2.0.9/)).
  Ninguno urge; van juntos acá para no volver a buscarlos:

  | Qué | Dónde | Medido |
  |---|---|---|
  | El A05 barre y normaliza la hoja ENTERA **una vez por tarea** (ingresos y egresos corren los dos sobre el mismo `ws`), y además normaliza todas las columnas ANTES del filtro de mes | `rem_saludmental.marcar_eventos` | ~0,25 s × 2 |
  | `_sala` y `_seccion_g` normalizan por separado las mismas 11 columnas del MISMO formulario (quedan 34 pasadas donde bastan 23) | `rem_a23_respiratorio` | ~0,20 s |
  | `RUN` se normaliza 2-3 veces en la carga de atenciones y nunca queda como `RUN_n` | `rem_utils.cargar_atenciones` | ~0,18 s |
  | `grid()` normaliza el sexo dos veces por fila y clasifica las bandas en Python | `rem_utils.grid` | 0,15 s (×44 en el P6) |
  | `por_actividad` rehace el mismo `explode` 5 veces | `rem_sm_actividades._ada_eventos` | 0,06 s |
  | `INSTR` normalizado 3 veces en una función | `a23._estamento_por_funcionario` | ~0,05 s |
  | máscara `es_agresor` invariante dentro del bucle de reglas | `rem_sp_p6_poblacion._tributarios_violencia` | <0,01 s |

  **Antes de tomar cualquiera de estos, PERFILAR.** En las dos rondas el orden que salía
  de leer el código estuvo mal las tres veces que se contrastó con un perfil.

- **Simplificación: lo que quedó de la ronda 2.0.11** (17ª pasada, ángulo simplificación
  y reuso sobre el codebase completo). Los cuatro de cabecera se arreglaron en esa
  versión (ver [CHANGELOG](CHANGELOG.md)); estos diez siguen abiertos. Ninguno cambia un
  número: son duplicaciones que **se van a separar** cuando alguien toque una de las dos
  copias. Van juntos acá para no volver a buscarlos:

  | Qué | Dónde |
  |---|---|
  | «basenames de uno-o-varios inputs» escrito inline 6 veces en 4 módulos, y `rescate._nombres` ya ES ese helper (con la guarda de DataFrame que a los otros les falta) | `a23:174,177` · `sm_actividades:501,503` · `trabajo_perdido:372` · mover `_nombres` a `rem_utils` |
  | Edad desde FNAC calculada de **tres** formas (dos con `// 365.25`, una con `.apply` fila a fila); las tres tienen que dar lo mismo, porque una llena la Sección G y otra decide las bandas del P6 | `a23._edad` · `a23._seccion_g` · `poblacion:900` -> un `rem_utils.edad_al()` |
  | `¿Originario o Migrante?` — MISMA columna de salida, MISMOS tres valores, dos reglas distintas: `contains("CHILEN")` vs `== "CHILENA"`. Una nacionalidad `CHILENO` sale chileno en el A23 y **Migrante** en Ferrada | `a23._origen:345` vs `poblacion:906-911` |
  | `runs_fr` se arma con un bucle y se vuelve a armar 30 líneas después con `set().union(*[...])`: dos ortografías de la misma unión, la segunda pisa a la primera | `rem_sp_p6_poblacion:615-618` y `:648` |
  | Cuatro nombres para los dos valores de `_rango_mes` (`fin` muerto tras la línea que lo aliasa; `mes_ini`/`mes_fin` con un uso cada uno) | `poblacion.construir_poblacion:851` |
  | El `span` de fechas con su guarda contra NaT, copiado idéntico 4 veces (la guarda es lo que se olvida en la 5ª copia) | `a23:155` · `sm_actividades:533` · `trabajo_perdido:361` · `poblacion:409` |
  | `_PUEBLO_VACIO = PUEBLO_VACIO`, alias privado con UN uso 33 líneas más abajo, en el mismo archivo. El comentario promete una retrocompat que no existe | `rem_utils:1109` |
  | `g` / `gmask` / `cero`: tres helpers de grilla donde `gmask` sola cubre los tres casos (`sub(None)` ya maneja el vacío), con `BANDAS_A23`/`LBL_A23` repetidas en los tres cuerpos | `a23._tablas_a23:766` |
  | El filtro base del P6 escrito dos veces en la misma función (`_relevante` vs `f_estado & f_a12m & f_ingr`). Editar una y no la otra deja `Revisar_Administrativo` acusando gente con un criterio que ya no es el del P6 | `rem_sp_p6_poblacion:256` y `:282-285` |
  | `detectar_formato` / `detectar_formato_filas`: forwarders de una línea a `formatos.detectar_eje*`, misma clase de envoltorio vacío que la ronda 12 borró. Un solo llamador externo (`a05.py:122`) | `rem_saludmental:305,310` |

**Dev / repo**
- **`groupby().last()` sobre columnas que RAYEN deja en `''`** (anotado al implementar la
  2.0.17): `last()` salta NA pero NO `''`, así que una última fila en blanco pisa el dato de
  las anteriores. En el A23 (demografía) se arregló en 2.0.17; tienen la misma forma y la
  suite no los toca `poblacion.py:532,724` y a23 `:295,:596,:674`. Revisar si sus columnas
  pueden venir `''` en la última fila.
- **`tools/correr_tests.py` revienta con `UnicodeEncodeError` (cp1252)** al imprimir la
  salida de un grupo que falla con un carácter fuera de cp1252, y oculta QUÉ test falló.
  Mientras tanto: `PYTHONIOENCODING=utf-8 python -m pytest tests`.
- **Pestaña de Consultas de catálogos** + enchufar `en_rango` en el A23.
- **Deuda:** `rem_utils.grid()` dispara `Pandas4Warning` (`m & muj` con dtype mixto);
  pandas 4 lo vuelve error.
- **`norm(pd.NA)` revienta** con `TypeError: boolean value of NA is ambiguous`, porque
  `pd.NA != pd.NA` devuelve `NA` y no un bool. Hoy no se alcanza (las columnas que arma
  `cargar_canonico` entregan `nan` float al iterar), pero el docstring promete «`''` si
  es None/NaN» y una columna de dtype nullable (`Int64`, `boolean`, un `StringDtype`
  armado de otra forma) lo tumbaría. Falla ruidoso, que es el modo bueno; lo que está
  mal es el docstring.
- **El orden de filas de `Revisar_Clinico` NO es determinista entre corridas.** Dos
  bloques se arman iterando un `set` (`comorbidos_ges` y `fr_sin_dx`,
  `rem_sp_p6_poblacion.construir_p6`), y el orden de un set de strings cambia con el
  hash seed del proceso. El CONTENIDO es siempre el mismo (verificado), pero dos
  corridas del mismo mes dan planillas que no se pueden diffear — y esa hoja existe
  para auditar. Se arregla con un `sorted()`.

---

## 13. Gotchas generales

- **OneDrive:** los exports sí están en OneDrive. Un `.xlsx` recién sincronizado puede
  leerse a medio bajar (truncado). Fue la fuente de la mitad de los dolores de cabeza
  del arranque: si un test falla raro tras tocar un archivo ahí, forzar la
  sincronización antes de culpar al código.
- **Excel abierto:** `wb.save()` → `PermissionError`, ya manejado con un mensaje amable.
- **Formato distinto de `.xlsx`:** la herramienta lee solo `.xlsx`. El HTML disfrazado
  de `.xlsx` típico de RAYEN (`BadZipFile`) y los `.xls` caen en el diálogo «No es un
  .xlsx» (`runner.es_error_formato` + `runner._MSG_NO_XLSX`, **un solo lugar** desde la
  2.0.11: el CLI los importa de ahí en vez de tener su copia).
- **`norm()` mapea NaN → `''`**: `nan or ''` es truthy y daba `"NAN"`, inflando flags.
