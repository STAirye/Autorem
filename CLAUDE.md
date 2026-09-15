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
| 4 | historia v1.2–1.6 | [CHANGELOG.md](CHANGELOG.md) |

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
   Los exports reales viven solo en la carpeta de trabajo (OneDrive). Los 3 hooks de
   pre-commit se instalan **en cada clon**.
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

---

## 1. Dependencias

- **Runtime:** `openpyxl` + `pandas`. `tkinter` viene con el Python de Windows.
  **GUI 2.0** (rama `gui-2.0`, en curso): `customtkinter`.
- **Build:** `PyInstaller` (§11). Todo se empaqueta en el `.exe`, así que sumar deps
  no cuesta: prima **minimizar líneas de código**.

---

## 2. Estado actual del repo

Versión **1.9.15** (§9). **174 tests.**

**Qué es compartido y qué es modular:**
- **Compartido — `programas/`:** primitivas (`rem_utils`), eje de formato IRIS/Admin
  (`formatos`), lookups transversales (`estamentos`, `dotacion`), tabla por-RUN
  (`poblacion`), hoja LEEME (`cobertura`), catálogos DEIS (`catalogos`) y la capa del
  formulario de Salud Mental (`rem_saludmental`).
- **Modular — `modulos/`:** un reporte por archivo. A05 N/O · A03 D.3 · A23 · SM
  Actividades · SM Trabajo Perdido · SP·P6 y SM Rescate (estos dos **en validación**).
- **Dispatcher — `autorem.py`:** GUI de pestañas + CLI.

Cadena de imports: `rem_utils` ← `formatos` ← capas ← módulos ← `autorem`. Imports
**absolutos** rooteados en la raíz (`from programas.rem_utils import …`).

```
autorem.py        entry point / dispatcher (único código en la raíz)
programas/        capas compartidas         -> programas/CLAUDE.md
modulos/          un reporte REM por archivo -> modulos/CLAUDE.md
tools/            utilitarios de desarrollo  -> tools/CLAUDE.md
catalogos/        CIE-10 / ENO / GES que shippea el exe (§14)
refs_tablas/      planillas de EJEMPLO, solo header (whitelist por archivo)
  specs/            DAX + visuales del PowerBI por página (skill pbip-spec)
.claude/skills/   limpiar-refs · check-cp1252 · versionar
legacy/           monolitos viejos (no se importan; referencia de equivalencia)
tests/            pruebas automáticas
docs/             planes y contexto por módulo
```

**Nombre de módulo:** `rem_<pestaña>_<casilla>_<descriptor>`; la `<casilla>` es la
celda/columna del REM (A05: `n` = ingresos, `o` = egresos). El `id` del `TAREA` la
incluye (`a05_o_egresos`).

**Arquitectura (2 ejes ortogonales):**
- **Formato** `iris` | `administrativo`: **se detecta automáticamente por contenido y
  lo verifica el usuario**. En la GUI 1.x todavía es un selector que la detección
  valida (y bloquea si no calza); la GUI 2.0 lo reemplaza por detección + confirmación.
  Aplica a **todos** los reportes RAYEN con dos formatos, no solo al formulario SM (§5).
- **Tarea** (`autorem.TAREAS`): agnóstica al formato. Las tareas del mismo archivo
  corren juntas → un `…_procesado.xlsx` con una hoja por tarea.

**Arranque:** sin args → GUI · arrastrar un `.xlsx` sobre el exe → GUI con la ruta
precargada · `--cli entrada.xlsx [--formato] [--tarea] [--mes AAAA-MM]` → **el CLI es
solo del A05**. El resto de los módulos es solo GUI, y no hay plan de CLI para todos.

**Salidas y caché:**
- La carpeta de salida por defecto es **la de los archivos de entrada**, no el cwd
  desde donde se corre el `.py`: las salidas llevan RUT y deben quedar junto a los
  exports, fuera del repo.
- El caché de usuario vive en **`~/.autorem/`** (`C:\Users\<usuario>\.autorem\`), no en
  `%APPDATA%` ni junto al exe: `estamentos.json` y `dotacion.json`.

**`refs_tablas/`:** planillas de ejemplo **sí versionadas**, con whitelist POR ARCHIVO
en el `.gitignore`: un `.xlsx` nuevo queda ignorado hasta vetarlo (skill
`limpiar-refs` = recortar a solo header). También se versionan las plantillas target
`SA_26` / `SP_26` `.xlsm`, para que git note cuándo MINSAL cambia su estructura. El
`.xls` de RAYEN no: openpyxl no lo lee, hay que convertirlo a `.xlsx`.

---

## 9. Versionado y convenciones

`X.Y.Z` versiona **el software** (un binario, un `rem_utils.VERSION`):
- **X** = cambio grande de arquitectura / incompatible, **o plantillas REM de un año
  nuevo** (SA y SP cambian cada año; actualizarlas es pega del dev). Planeado: **2.0.0**
  = GUI 2.0 · **3.0.0** = plantillas REM 2027.
- **Y** = módulo o reporte nuevo (de cualquier programa de salud).
- **Z** = corrección. Reinicia a 0 al subir Y.

**Año de reporte vigente: 2026** (`SA_26` / `SP_26`).

**No se reservan números para hitos:** la versión mide avance, y no se congela
esperando una validación. (El 1.10.0 ya no está apartado para la familia población.)

Con puntos (`1.4.10`), para que Z pase de 9. Estado actual: **1.9.15**.

- **Cada `.py` lleva la versión de SU último cambio**, no todas sincronizadas.
  Llevan versión: `autorem.py`, `programas/`, `modulos/`, `tools/`. No llevan: `tests/`
  y `__init__.py`. **Exento:** `legacy/`.
- `tools/check_version.py` (en el pre-commit) verifica el manifiesto, la versión de
  este archivo (las dos frases en negrita de arriba: **no las reformules**), el
  CHANGELOG y el contador de tests. **Skill `versionar`.** Árbitro anti-colisión entre
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
- Tres hooks, instalados **en cada clon** (§8.2).

---

## 12. Roadmap — pendiente

(Lo hecho está en el [CHANGELOG](CHANGELOG.md).)

**En curso**
- **GUI 2.0** (rama `gui-2.0`, [docs/GUI_2.0_plan.md](docs/GUI_2.0_plan.md)):
  customtkinter, pestañas agrupadas por programa, About, la pestaña A03 standalone
  desaparece (queda solo dentro de Actividades), y el selector IRIS/Admin se reemplaza
  por detección + confirmación. El selector sobra porque ya no le puede ganar a la
  detección, que bloquea si no calzan: solo aporta una forma de equivocarse. El
  `--perfil` del CLI queda como override.
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
- **A03 D.3 v2:** conteos por rango etario extraídos del `SA_26`.
- **Otras Causas:** popup con los RUT + dropdown abandono/clínica.
- **Dotación fase 2:** bloques apilados REM/externos por sección (validación en pausa
  hasta recibir la lista de externos).

**Correcciones y mejoras**
- **Demografía del grupal** cruzando con el ADA por RUN. Evaluar primero si el grupal
  trae RUN: si lo trae, es un merge barato.
- **GUI 2.0:** `gui/paginas/sm.py` todavía dice «saco vacío» (4 lugares). Pasarlo a
  «saco roto» antes del merge (en `main` se renombró en 1.9.14).
- **Catálogos en la GUI 2.0** (fecha visible + actualización manual en modo
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
