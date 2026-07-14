# Changelog — autoREM

Todos los cambios relevantes de este proyecto se anotan acá.
Formato inspirado en [Keep a Changelog](https://keepachangelog.com/es/).

**Versionado `X.Y.Z`** (ver [CLAUDE.md](CLAUDE.md) §9):
`X` = programa · `Y` = módulos de programa acumulados · `Z` = corrección del
módulo que se está trabajando (reinicia al subir `Y`).

Tipos de cambio: **Agregado** (nuevo) · **Cambiado** · **Corregido** ·
**Eliminado** · **Seguridad**.

---

## [1.3.1] — 2026-07-14

### Corregido
- **Screening: la discrepancia RAYEN vs DISAM compara BANDAS, no texto.** RAYEN
  no usa un vocabulario único: GHQ-12 (Goldberg) devuelve frases clínicas
  («Ausencia de psicopatología» = Bajo, «Sospecha … subumbral» = Medio,
  «Indicativos de presencia …» = Alto), mientras PSC/PSC-Y devuelven
  «Bajo/Medio/Alto» (y **blanco** bajo el corte). El match exacto anterior
  marcaba el **100 % de los Goldberg como discrepancia falsa**. Ahora se canoniza
  la redacción (`canon_resultado` + `_MAP_RESULTADO`) antes de comparar.
  Verificado contra 4 exports reales (Goldberg/PSC-Y × IRIS/Admin): **0
  discrepancias falsas**.
- Nueva columna **`Banda_RAYEN`** en la salida (banda a la que se mapeó el texto
  de RAYEN, para auditar la comparación); aviso en el log si aparece una
  redacción no mapeada.

## [1.3.0] — 2026-07-13

Suma el **tercer módulo** (screening A03 D.3) → `Y` pasa de 2 a 3, `Z` reinicia.

### Agregado
- **Módulo screening A03 D.3** (`modulos/rem_a03_d3_instrumentos.py`): procesa
  PSC / PSC-Y / GHQ-12. Autodetecta formato (IRIS/Admin) e instrumento por
  contenido; por cada aplicación reporta puntaje, resultado automático (RAYEN),
  resultado calculado (cortes DISAM), discrepancia, momento (Ingreso/Egreso) y
  estamento (IRIS). Tests en `tests/test_screening.py` (5/5). Validado también
  sobre exports Administrativos reales (goldberg/pscy).
- **GUI con PESTAÑAS por módulo** (`ttk.Notebook`): «REM A05 · Egresos/Ingresos»
  y «REM A03 D.3 · Screening», cada una con sus instrucciones, archivo y log. El
  screening ya se usa desde la GUI (detecta el instrumento; dropdown para
  corregir). Sumar un módulo = sumar una pestaña.

### Cambiado
- **Nombres de patología limpios** en el output A05 (`LIMPIAR_NOMBRE_PATOLOGIA=True`):
  `OVERRIDE_PATOLOGIA` con nombres canónicos por Nº de pregunta (tomados de SP·P6).
  Nuevo `EXCLUIR_PATOLOGIA = {75,77,79,81}`: epilepsia (→ REM adulto) y programas
  de rehabilitación/acompañamiento se excluyen del output de egresos/ingresos.
- **Subtipos:** verificados contra un export real (junio). Depresión / Violencia /
  Suicidio / Alzheimer ya salen limpios por el recorte del header. Nuevo
  `OVERRIDE_SUBTIPO` para Ansiedad (Q43): nombres cortos (Fobia social / Pánico /
  Generalizada / TEPT / Otros) y **junta los dos "Pánico"** en uno (el REM solo
  tiene "Pánico" a secas).
- **Convención de nombre de módulos de tarea:** `rem_<pestaña>_<casilla>_<descriptor>`
  (`<casilla>` = celda REM). `rem_a05_egresos` → `rem_a05_o_egresos`,
  `rem_a05_ingresos` → `rem_a05_n_ingresos`. Los `id` de `--tarea` cambian a
  `a05_o_egresos` / `a05_n_ingresos`. Sin cambio de comportamiento (tests 7/7).
- `edad_anios()` movida de `rem_saludmental` a `rem_utils` (parsing RAYEN
  genérico; la usan tanto A05 como screening).

### Corregido
- **Screening PSC/PSC-Y bajo el corte (<33):** antes salía como `None` (celda
  vacía, sin contar en el total, sin comparar contra RAYEN). Ahora se etiqueta
  **«Sin riesgo»** (constante `LABEL_SIN_RIESGO`, renombrable) — es un resultado
  válido y **el más común**. Se cuenta y se compara con RAYEN como cualquier otra
  banda. Nuevo desglose `por_resultado` en el resumen (GUI + retorno) para ver
  cuántos caen en cada categoría. GHQ-12 no cambia (0-4 ya es «Bajo»).

## [1.2.0] — 2026-07-07

Primer estado bajo la convención `X.Y.Z`. Equivale a la suma de las iteraciones
previas (etiquetadas informalmente v1.2–v1.6; el detalle vive en el historial de
git). Programa **autoREM** (X=1) con **2 módulos** (Y=2: egresos, ingresos).

### Agregado
- **Módulo A05 · Egresos** (`rem_a05_o_egresos.py`): marca Altas / Traslados /
  Otras Causas de Salud Mental, con patología, subtipo y demografía.
- **Módulo A05 · Ingresos** (`rem_a05_n_ingresos.py`): gemelo del anterior para
  eventos de INGRESO.
- **Dispatcher GUI + CLI** (`autorem.py`): selector de tareas; corre varias en
  una pasada y produce un solo `…_procesado.xlsx` con una hoja por tarea.
- **Perfiles de formato IRIS / Administrativo**: el usuario elige al inicio de
  qué reporte cargó, con disclaimer para el Administrativo (columnas
  demográficas ausentes, edad tomada de 'Edad de registro formulario').
- **Capa compartida** (`rem_saludmental.py`) y **utilidades genéricas**
  (`rem_utils.py`); base para sumar módulos nuevos.
- Detección de formato con validación cruzada ("elegiste IRIS pero esto parece
  Administrativo…").
- `edad_anios()`: parsea la edad del Administrativo (`'99 años 12 meses…'` → 99;
  menor de 1 año → 0).

### Corregido
- Consola Windows (cp1252): los símbolos `▶·→«»✔` reventaban al imprimir en el
  CLI. Forzado UTF-8 en `stdout`.

### Seguridad
- `.gitignore` excluye `*.xlsx/xls/csv` y salidas: red de seguridad para que
  NUNCA entre PII (datos de pacientes) al repositorio.

---

Historia previa (pre-convención): ver `git log` y los archivos
`rem_marcar_egresos *.py`, conservados como referencia validada.
