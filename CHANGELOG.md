# Changelog — autoREM

Todos los cambios relevantes de este proyecto se anotan acá.
Formato inspirado en [Keep a Changelog](https://keepachangelog.com/es/).

**Versionado `X.Y.Z`** (ver [CLAUDE.md](CLAUDE.md) §9):
`X` = programa · `Y` = módulos de programa acumulados · `Z` = corrección del
módulo que se está trabajando (reinicia al subir `Y`).

Tipos de cambio: **Agregado** (nuevo) · **Cambiado** · **Corregido** ·
**Eliminado** · **Seguridad**.

---

## [1.5.1] — 2026-08-04

Corrección del módulo en curso: **datos demográficos** en SM Actividades +
selector de carpeta de salida + fix de `norm()` con NaN.

### Agregado
- **Bloque demográfico** en las tablas de SM Actividades (columnas AN–AV del
  template SA_26 y equivalentes): **Pueblos Originarios, Migrantes, SENAME, Prot.
  Especializada (ex Mejor Niñez), Demencia, Cuidador, Beneficiarios (=todos),
  Campaña de Invierno, Gestante**. Extracción reutilizable en
  `rem_utils.marcar_demografia()` (flags por atención desde ALERTAS ADMINISTRATIVAS
  / ES IMIGRANTE / PUEBLO ORIGINARIO / DIAGNOSTICOS / ACTIVIDADES) + `gestante_runs()`
  (patrón PowerBI: matrona + control prenatal / formulario gestante, ventana de 3
  meses). Volcado por sección en `rem_sm_actividades`. `MAPA_ATENCIONES`: +ALERTAS,
  +EMIG, +FORMCLIN.
- **TRANS** y **Espacios Amigables / Familias en Riesgo** no derivables del ADA →
  0 / omitidos (TRANS requiere el 'Informe inscritos y adscritos', no cargado).
  El **grupal no trae demografía** (A27 etc. quedan en 0): known issue documentado.
- **GUI: selector de carpeta de salida** en SM y A23 (default = carpeta del `.exe`),
  para no perder el resultado junto al input. Aviso en el log si el ADA no cubre la
  ventana de 3 meses del flag gestante.

### Corregido
- **`norm()` con NaN**: una celda vacía leída como `NaN` (float) daba `"NAN"` en vez
  de `""` (porque `nan or ''` es *truthy*) → inflaba `dem_originario` (86→38 real) y
  cualquier lógica que normalizara celdas vacías. Ahora `norm(NaN) == ""`.
- **Bug de normalización** en dos búsquedas nuevas (`dem_demencia`, `gestante_runs`):
  buscaban el término en minúscula contra series ya normalizadas en MAYÚSCULA →
  nunca matcheaban (demencia y gestante salían 0). Corregido: todo `.str.contains`
  normaliza el término (`norm(...)`); las búsquedas de texto van por `contiene_todos`/
  `_all` o con `norm("literal")`.
- Tests `test_sm_actividades.py` 9→11 (agregados `test_demografia_flags` y
  `test_gestante_flag`, que blindan el bug de normalización).

## [1.5.0] — 2026-08-04

Quinto **módulo** de programa (Y: 4→5): **REM Salud Mental — Actividades**
(`modulos/rem_sm_actividades.py`, pandas). Tabula la estadística de actividades de
Salud Mental que hasta ahora se llenaba a mano con tablas dinámicas: **A04·A24,
A06·A.1 (controles + psicosocial grupal), A19a·A.3 (consejerías familiares
SM/demencia), A26 (VDI SM), A27 (educación prev. SM) y A32·F (acciones/controles
remotos SM)**. Salida = tablas listas para copiar-pegar al template SA_26 (sin juicio
clínico, solo conteo). Filtros **validados casilla por casilla** contra el REM manual
de julio 2026 (A04=39 · A06=845 controles + 51 grupal · A19a=111/40 · A26=12 ·
A32·F1=169/1/4 · A27/F2=0).

### Agregado
- **Módulo `rem_sm_actividades.py`** con dos fuentes: **ADA** ('Atenciones/Diagnósticos/
  Actividades', vía `cargar_atenciones`) y un loader nuevo **`cargar_grupal`** para el
  reporte 'Atenciones Grupales'. Salida `escribir()` = hoja **SM_Detalle** (auditable) +
  una hoja por sección REM con la forma del template.
- **Regla ADA = conteo por ATEN ID** (distinct); **grupal = conteo por ASISTENCIA**
  (cada fila `Asiste=SI`, SIN deduplicar: misma persona 2 talleres = 2).
- **Filtro de mes por FECHA ATENCIÓN** (parsea el texto `DD/MM/YYYY` del grupal): el
  export puede venir del año completo y se recorta el mes reportado.
- **Pestaña GUI 'REM SM · Actividades'** (ADA + Grupales multi-archivo + año/mes).
- `rem_utils.MAPA_ATENCIONES`: +`ATENID` y +`ANOS_AT` (edad a la atención) — IRIS.
- Tests `tests/test_sm_actividades.py` (9/9): por casilla, ATEN ID distinct, grupal
  sin dedup, ventana de mes, split etario 5-9 (A26), desagregación A32·F1, consejerías
  grupales sumadas en A19a, exclusión SENAME.

### Cambiado
- **GUI: aviso 'cargar los exports SIN modificar'** en TODAS las pestañas (un archivo
  editado rompía el A23 en silencio). El 3er selector del A23 (Estratificación) pasó al
  mismo estilo que los otros y se etiquetó explícitamente como opcional.

### Notas
- El guion en el filtro de A19a **importa**: `Prioridad - Con integrante con problema de
  salud mental` evita capturar las VDI de A26 (que contienen la misma frase sin guion).
- **SENAME se excluye solo**: 'Control Salud Mental a Paciente SENAME' es un string aparte
  (ellos hacen su propio REM). A05 y las Consultorías A06·A.2 quedan fuera (módulo/manual).

## [1.4.1] — 2026-08-03

### Agregado
- **A23 lee atenciones desde ADMIN (Monitoreo de Actividades), PARCIAL.** El parser
  de atenciones se movió a `rem_utils` (`cargar_atenciones` + `MAPA_ATENCIONES` +
  `cargar_canonico`), reutilizable por cualquier programa, con **nombres de columna
  alternativos IRIS | Admin** (`resolver_columnas` ahora acepta una lista de opciones).
- Manejo de la estructura **PADRE-HIJO** del monitoreo (una atención en varias filas;
  RUN/cabecera solo en la 1ª) → forward-fill de cabecera SOLO a filas hijas (no toca
  IRIS ni contamina campos vacíos entre pacientes).

### Limitaciones (documentadas)
- El **Monitoreo admin es INCOMPLETO**: (a) sin demografía (nacionalidad/pueblo/fecha
  nac/nombres → origen-migrante y nombre vacíos; edad de 'AÑOS'); (b) **diagnóstico en
  TEXTO sin código ICD** → los indicadores por código (**Ira Alta**, **Bronquitis**,
  **EPOC exacerbado**) salen **0**. Los de texto (Neumonía/Influenza/Coqueluche) y los
  de actividad (KTR, espirometría, controles…) sí cuadran (verificado vs IRIS jul-2026:
  Neumonía 71≈72, Influenza 30≈31, KTR 47≈48). **IRIS sigue siendo la fuente plena.**

## [1.4.0] — 2026-08-03

Cuarto **módulo** de programa (Y: 3→4): **REM A23 (Respiratorio)**. Primer módulo
con **pandas** (queda como dependencia de primera clase; se abandona el "única
dependencia = openpyxl", ver §1). Solo formato IRIS / BD PowerBI por ahora.

### Agregado
- **Módulo REM A23** (`modulos/rem_a23_respiratorio.py`), portado del visual
  PowerBI 'poblacion ferrada 2.5'. 1 fila por paciente (RUN):
  - **27 indicadores REMA23 del mes** desde atenciones (IRA, neumonía, bronquitis,
    influenza, coqueluche, EPOC exacerbado, KTR, espirometría, controles/consultas
    de sala por profesión, rehab, educación, campaña invierno, compuestos Morbi /
    Seguimiento…). Ventana de mes PARAMETRIZABLE (no `TODAY()`).
  - **SALA bajo control** (asma/EPOC/SBOR/FQ/otras + gravedades) desde el formulario
    'Otros y Respi' + Estratificación (patrón 'último formulario médico válido').
  - **Sección G — inasistentes a control de crónicos** (def. REM del comentado):
    Fecha del Próximo Control vencida más allá del umbral por edad (<1a 2m29d ·
    12-23m 5m29d · ≥2a 11m29d) al corte = último día del mes reportado. NO usa el
    reporte de inasistencias (NSP es moot: quien nunca tomó hora no aparece).
  - Inputs (atenciones/otros) aceptan **LISTAS** (histórico multi-año, necesario
    para lo crónico/12m). Salida `escribir()` = hoja detalle + hoja Sección G.
  - **Pestaña GUI `REM A23 · Respiratorio`**: selector multi-archivo, mes a reportar,
    y aviso claro de la limitación de RAYEN Admin (solo formulario + monitoreo pobre).
  - Tests `tests/test_a23.py` (6/6). Validado sobre exports reales de jul-2026.
- **`rem_utils`** gana la capa "leer + clasificar reportes" reutilizable: `leer_xlsx`
  (robusto a la 'dimension' rota que dejaba a pandas en 0 filas), `resolver_columnas`
  (semántico), `contiene_todos`/`contiene_alguno`.

### Pendiente
- Agregación de los indicadores mensuales por edad×sexo (celdas de actividades del REM).
- Soporte formato **Administrativo** (monitoreo de actividades + formulario admin;
  este último sin columna INSTRUMENTO → requiere el lookup `estamentos.py`).
- Sección H (inasistentes a citación agendada, por profesional) + validación vs PowerBI.

## [1.3.3] — 2026-07-15

### Agregado
- **Estamentos como capacidad TRANSVERSAL + failsafe.** El lookup
  Funcionario→Estamento (`programas/estamentos.py`) pasa a ser reutilizable por
  cualquier flujo en formato Administrativo (hoy screening; a futuro cualquier
  módulo que reporte por estamento), con **instrucciones y el porqué** en la GUI
  (`_bloque_estamentos`, reutilizable: de dónde bajar 'Utilización de Cupos' y
  por qué se necesita).
- **Failsafe de resolución manual** (`_resolver_estamentos` + `faltantes()` /
  `estamentos_conocidos()` / `aplicar_resoluciones()`): tras cargar el reporte,
  los funcionarios que NO están en la tabla se resuelven en un diálogo (elegir
  estamento) o se **IGNORAN** (externos que prestan servicios transitorios; None
  = ignorar, no se vuelve a preguntar). `procesar(..., resolver_estamento=cb)`.
  Tests: estamentos 4/4, screening 9/9.

## [1.3.2] — 2026-07-15

### Agregado
- **Estamento en el screening Administrativo** (`programas/estamentos.py`): el
  Admin no trae el estamento de quien aplicó, solo el nombre. Nuevo lookup que
  lee el reporte RAYEN **'Utilización de Cupos'** (`Profesional` → `Instrumento`,
  donde 'Instrumento' = estamento, otro mislabel) y rellena la columna Estamento
  del screening por nombre de funcionario (match normalizado, tolerante a
  mayúsculas/tildes). `cargar_estamentos()` deduplica y avisa si un nombre trae
  >1 estamento. Opción en la pestaña de screening: cargar el reporte (opcional,
  solo aplica al Admin). La **tabla de nombres queda LOCAL**, no se versiona.
  Validado end-to-end sobre exports reales (4/4 y 11/11 estamentos rellenados,
  0 sin match). Tests `tests/test_estamentos.py` (3/3).

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
