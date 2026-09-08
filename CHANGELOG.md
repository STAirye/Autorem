# Changelog — autoREM

Todos los cambios relevantes de este proyecto se anotan acá.
Formato inspirado en [Keep a Changelog](https://keepachangelog.com/es/).

**Versionado `X.Y.Z`** (ver [CLAUDE.md](CLAUDE.md) §9):
`X` = programa · `Y` = módulos de programa acumulados · `Z` = corrección del
módulo que se está trabajando (reinicia al subir `Y`).

Tipos de cambio: **Agregado** (nuevo) · **Cambiado** · **Corregido** ·
**Eliminado** · **Seguridad**.

## [1.9.5] — 2026-09-08

Los módulos pandas no cumplían la regla de fail loud (CLAUDE.md §3) para un mes SIN
datos: el A05 levanta `ArchivoInvalido` cuando el mes no tiene formularios, pero
cargar el export del año pasado —o equivocarse de mes en el spinbox— producía un
`.xlsx` completo con todas las tablas en cero, con pinta de resultado legítimo y
copiable al SA_26.

### Agregado
- **`rem_utils.filtrar_mes(d, ini, fin, fuente)`** — punto único del filtro de mes
  con guardarraíl. 0 filas del mes -> `ArchivoInvalido("mes_vacio")` con el span real
  del archivo en el mensaje ("cubre 01/2025 a 12/2025, pediste 07/2026"), y mensaje
  aparte cuando ninguna fecha es legible (ahí lo que se revisa es el archivo, no el
  spinbox). Misma categoría que el A05, así que `autorem._manejar_error` ya la muestra.
- Tests de los DOS casos en A23, SM Actividades, Trabajo Perdido, P6 y Rescate
  (143 -> 157).

### Cambiado
- **La guarda va sobre la FUENTE, nunca sobre la casilla.** Esa es la distinción que
  hace al fix seguro: un mes cubierto con A27/A32·F2 en 0 es LEGÍTIMO y no falla. Por
  eso los filtros que vienen DESPUÉS del mes se aplican aparte, sobre lo que devuelve
  `filtrar_mes`: `Asiste=SI` del grupal y Control/Ingreso IRA/ERA de la Sección H.
- Enganchada en las cinco fuentes que se filtran por mes: ADA de `sm_actividades`,
  grupal, atenciones del `a23`, NSP de la Sección H y el ADA de `sm_trabajo_perdido`.
  Las opcionales (grupal, NSP) también fallan duro: cargarlas fue decisión del usuario,
  y un archivo de otro período deja sus casillas en cero sin que nadie lo note.
- **NO se engancha** en `om` (el 'Otros y Respi' del A23 es histórico multi-año: un mes
  sin formulario de calidad de vida es normal) ni en la familia población, donde el mes
  es un CORTE sobre el snapshot de inscritos y no un filtro de filas.
- **`poblacion._verificar_cobertura_fechas` ahora DEVUELVE sus avisos** y quedan en
  `P.attrs['avisos']` -> hoja **LEEME** del P6 y del Rescate. Ahí el desfase no bloquea
  (elegir un mes que el export no cubre es una decisión legítima del usuario; el mes
  reportado no tiene por qué ser el anterior), pero deja de vivir solo en el log de la
  corrida: queda escrito en la planilla, que es lo que se mira después.

## [1.9.4] — 2026-09-08

Herramienta de mantención: la versión arrastra cinco archivos y hacerlo a mano venía
fallando.

### Agregado
- **`tools/check_version.py` + skill `versionar`**, encadenado al pre-commit detrás
  del anti-RUT y del cp1252. Verifica:
  - **el manifiesto en las DOS direcciones** — código distribuible sin `# Version:`,
    y archivos fuera de esas rutas que se cuelan *con* versión. Se deriva de la RUTA,
    no es una lista a mano (una lista sería otra cosa que se pudre: ya pasó con el
    `.spec` ignorado). Al estrenarlo cazó un caso real: un header de versión que se
    había colado en `tests/test_formatos_fuente.py`.
  - que la versión esté declarada en **§2 y §9 de CLAUDE.md** (los dos sitios
    concretos, no «que aparezca en algún lado» — la versión se cita también en prosa
    y eso hacía pasar el chequeo con §2 desfasada);
  - que exista la entrada del CHANGELOG;
  - que los `.py` que se commitean declaren la versión actual;
  - que los **contadores de tests** de CLAUDE.md calcen. Se cuenta **estáticamente**
    (`def test_` da 143, igual que pytest): un hook de 30 segundos no lo usa nadie.
- **`--arreglar`** sincroniza contadores y headers; **`--bump X.Y.Z`** sube la fuente
  de verdad, los headers de lo modificado y CLAUDE.md de un viaje. La entrada del
  CHANGELOG queda a mano **a propósito**: el qué y el porqué no los inventa un script.
- **Guardarraíl anti-colisión.** Dos sesiones en paralelo quisieron subir a 1.8.4 y a
  1.9.0 el mismo día, y hubo que detener ambas: los dos números eran defendibles por
  separado, así que nada los frenaba hasta que chocaban. El árbitro es el CHANGELOG —
  si ya tiene una versión mayor que `rem_utils.VERSION`, otra sesión avanzó y esta
  copia quedó atrás. El check bloquea y `--bump` rechaza cualquier número que no
  avance respecto de lo publicado.

### Corregido
- **CLAUDE.md §9 decía una convención que nunca se cumplió**: «todos los `.py` se
  bumpean juntos», con archivos en 1.8.2, 1.8.3, 1.8.4, 1.9.0 y 1.9.1 conviviendo. Se
  corrigió a la práctica real —**cada `.py` lleva la versión de su último cambio**—,
  que además es más informativa: el header dice cuándo cambió ese archivo.
- Se quitó el `# Version:` que se había colado en `tests/test_formatos_fuente.py`
  (los tests no se distribuyen, no llevan versión).

## [1.9.3] — 2026-09-08

Con la muestra del 'Monitoreo de Actividades' en `refs_tablas/` se pudo medir en vez
de suponer, y **SM pasó de inusable a usable** con esa fuente.

### Agregado
- **`ATENID` <- `N°`**: el Monitoreo no tiene ATEN ID, pero su correlativo agrupa las
  filas de una atención (medido: 2625 atenciones en 6590 filas, **0 con cabecera
  inconsistente**). Con esto el conteo de SM deja de colapsar cada casilla a 1.
- **`ANOS_AT` <- `AÑOS`**: confirmado por el autor contra enero-2026 que el `AÑOS` del
  Monitoreo es edad **a la atención**, no a la descarga.
- **`PROF` <- `FUNCIONARIO`**: el mismo dato con otro nombre.
- **Namespacing del correlativo por archivo** en `cargar_canonico`. El `N°` reinicia
  en 1 en cada export, así que concatenar dos Monitoreos fusionaría atenciones
  distintas bajo el mismo id y el conteo subcontaría **en silencio**. El `ATEN ID` de
  IRIS **no** se namespacea: es global y único, y si aparece en dos exports que se
  solapan tiene que deduplicar. Un test por cada lado. **143 tests.**

### Cambiado
- **`SOLO_IRIS_ATENCIONES` pierde `ATENID`.** Al darle equivalente admin, el
  Monitoreo habría pasado a clasificar `cambiada` (mensaje para el dev) en vez de
  `parcial` (mensaje para el usuario). Quedan las **cinco demográficas**, que es
  exactamente lo que ese reporte no puede dar. Anotado como regla: dar equivalente
  admin a una clave obliga a sacarla de la firma.
- **El aviso de SM cambia de sentido**: ya no dice "los conteos salen en 1", dice que
  los conteos son válidos y que lo que sale en 0 es **toda la demografía** (AN–AV del
  SA_26) -> copiar los totales, no esas columnas.

### Notas de diseño
- ⚠ **Trampa semántica documentada**: `AÑOS` significa cosas DISTINTAS en los dos
  reportes — en IRIS es edad a la **descarga** (la buena es `AÑOS ATENCIÓN`), en el
  Monitoreo **ya es a la atención**. El mapa resuelve por orden y en IRIS gana siempre
  `AÑOS ATENCIÓN`; si RAYEN lo renombrara, el fallback daría edad-a-la-descarga en
  silencio, así que hay un test que exige que en IRIS resuelva a una columna que diga
  ATENCIÓN.

## [1.9.2] — 2026-09-08

`formatos.py` **fase 2**: el grupo pandas ya no procesa una fuente degradada en
silencio. (Pese al nombre del roadmap **no es detección de eje**: el lado
Administrativo no tiene equivalente del A/D/A, así que no hay dos formatos del
mismo reporte entre los que elegir — se verifica la IDENTIDAD del reporte.) Era el último agujero de "número plausible pero callado y errado" que
quedaba abierto en el proyecto.

### Agregado
- **Clasificación de fuente `plena` / `cambiada` / `parcial`**
  (`formatos.clasificar_fuente` + `aviso_fuente`), enganchada en
  `rem_utils.cargar_canonico` — el cuello de botella único por el que pasan ADA,
  grupal, NSP y 'Otros y Respi', así que la fase 2 entra en UN punto y no en cinco.
  El veredicto queda en `df.attrs['fuente']` y se loguea cuando no es plena.
- **Aviso de fuente en la hoja LEEME** para A23 y SM Actividades. El texto del A23
  que vivía como advertencia PERMANENTE en `cobertura.py` se borró: ahora sale
  **solo en las corridas donde de verdad pasa**.
- `tests/test_formatos_fuente.py` (12 tests), con un guardarraíl contra falsos
  positivos: el export IRIS versionado **tiene** que clasificar como `plena`, y
  —desde que existe la muestra— el 'Monitoreo de Actividades' real **tiene** que dar
  `parcial`. Los dos extremos medidos contra archivos de verdad, no maquetas.
  **138 tests.**

### Documentado
- **§5.1 de CLAUDE.md: qué soporta realmente el 'Monitoreo de Actividades'.** Con la
  muestra header-only en `refs_tablas/` se pudo medir en vez de suponer. Resultado:
  el soporte parcial del **A23 es real** (indicadores por actividad + edad + sexo
  funcionan; solo caen los 3 por código ICD), y **SM no es usable** con esa fuente
  (falla el conteo por `ATEN ID` y las edades por `AÑOS ATENCIÓN`). Se confirmó
  además por qué el bug era silencioso: el Monitoreo **pasa todas las `requeridas`**
  de `cargar_atenciones`, así que cargaba sin chistar.

### Notas de diseño
- **Se clasifica la FUENTE, no las columnas.** El problema nunca fue una columna
  ausente: en el Monitoreo Admin `DIAGNOSTICO` existe y resuelve perfecto, solo que
  trae texto sin código ICD, y por eso Ira Alta / Bronquitis / EPOC exacerbado
  salían 0. `resolver_columnas` no puede ver eso — solo el eje habla de la CALIDAD
  de una columna, no de su existencia.
- **Firma negativa**, porque no hay UN «otro lado» que reconocer: puede llegar el
  'Monitoreo de Actividades', un archivo editado, o algo que RAYEN aún no inventa.
  Se prueba que ES el A/D/A de IRIS; lo que no se pruebe, avisa — sin necesidad de
  saber qué fue lo que llegó.
- **Tres estados, no dos.** `cambiada` existe para el día que RAYEN renombre una
  columna del A/D/A: sin ese estado sería un falso «parcial» permanente, y un aviso
  que grita siempre deja de leerse. `parcial` le habla al usuario («bajaste el
  archivo equivocado»), `cambiada` al dev («hay que actualizar el mapeo»).
- La firma son **claves canónicas**, no nombres de columna, para que el saber de
  headers viva sólo en `MAPA_ATENCIONES` y no pueda desincronizarse.

### Corregido
- **Descubrimiento colateral: en SM la fuente parcial no degrada, ROMPE.** El
  conteo es `drop_duplicates(casilla, sub, id)` con `id = ATEN ID`; sin esa columna
  todas las filas comparten id `"None"` y **cada casilla colapsa a 1 evento**. Antes
  eso salía sin una palabra. Ahora el aviso lo dice y pide NO copiar esas tablas al
  SA_26.

## [1.9.1] — 2026-09-08

### Corregido
- **`rem_sm_rescate_inasistentes`: Fallecidos ya NO se excluyen de Rescate_6m/13m,
  se FLAGEAN** — mismo tratamiento que Traslados. El filtro duro original (§8.3 del
  plan) sacaba en silencio a todo paciente con `Motivo Pasivación=Fallecido`; era
  inconsistente con Traslados (§8.5, ya flageado desde el 1.8.4) y ambos motivos
  vienen del mismo lugar: un snapshot del Informe Inscritos, no un dato verificado.
  Nueva hoja **`Posibles_Fallecidos`** (mismo formato que `Posibles_Traslados`).
  `Fallecidos_mes` (cohorte del mes, para el A05) no cambió. **124 tests.**

## [1.9.0] — 2026-09-08

Capa nueva (Y++): **catálogos oficiales DEIS/MINSAL** (CIE-10 · ENO · GES) como
backend compartido. No llena ninguna casilla del REM por sí sola: es el
diccionario que le faltaba al resto de la herramienta.

### Agregado
- **`programas/catalogos.py`** — capa compartida con **registro declarativo**
  (`CATALOGOS`, mismo patrón que `COBERTURA`): un catálogo nuevo es una entrada en
  el dict + una función `_leer_*`, no un módulo por catálogo.
  - `cie10` — Lista Tabular CIE-10 del DEIS, **edición agosto 2026** (12.548
    códigos: 8.910 cruz o daga, 331 asterisco, 3.307 causa externa).
  - `eno` — Enfermedades de Notificación Obligatoria (Decreto 7/2019), 56
    enfermedades → 448 pares enfermedad-código.
  - `ges` — GES 90 problemas de salud ↔ CIE-10 (5.936 pares).
  - API: `norm_codigo` / `con_punto` / `en_rango` / `expandir` / `descripcion` /
    `existe` / `eno_de` / `ges_de` / `anotar` (anotador **batch**: lista de códigos
    → `COD · DESC · EXISTE · ENO · ENO_TIPO · GES`).
- **`tools/catalogos_deis.py`** — mantenedor de los catálogos (lado desarrollo, el
  `.exe` nunca lo corre): `--check` compara la edición publicada por el DEIS contra
  la vendorizada, `--fetch` baja los `.xlsx`, `--slim` genera los `.csv.gz` +
  `catalogos/FUENTES.json` (URL, edición, filas, **sha256** del origen, fecha).
- **`tools/scan_catalogo.py`** — escáner de PII previo a versionar: RUT con DV
  válido (reusa `hook_pre_commit_rut.sospechosos`, fuente única del módulo 11),
  emails y teléfonos + volcado de estructura para revisar a ojo. **Existe porque el
  pre-commit anti-RUT SALTA los binarios** (`.xlsx`, `.gz`): un slim vendorizado no
  lo revisaba nadie. `--slim` lo corre solo y **se niega a vendorizar** un catálogo
  con hallazgos. Los tres catálogos actuales escanearon limpios.
- **`catalogos/`** — carpeta nueva, versionada en bloque (`!catalogos/*.csv.gz`),
  distinta de `refs_tablas/` (que es "ejemplo anonimizado con whitelist por
  archivo"; esto es dato público que **shippea** la herramienta). **160 KB** los tres
  catálogos vs 694 KB de `.xlsx`. Los `.xlsx` originales NO se versionan.
- **`tests/test_catalogos.py`** — 14 pruebas. **124 tests** en total.

### Decisiones de diseño
- **Tipo de notificación del ENO transcrito del Decreto 7/2019**, no inferido del
  orden de las filas del Excel (que hoy calza exacto con los literales a/b/c del
  art. 1, pero es un accidente que una reordenación del DEIS rompería en silencio).
  Texto oficial: `leychile.cl/Consulta/obtxml?opt=7&idNorma=1141549`.
- **Las transitorias se distinguen de las del decreto.** Mpox (inmediata) y
  *S. pyogenes* (centinela, diaria solo en hospitales) rigen **mientras dure la
  alerta**, no por el decreto → su campo `ART` dice `alerta vigente`, para que
  cuando la alerta se levante se sepa que esa clasificación caducó.
- **Viruela y Tifus de los matorrales quedan SIN clasificar, a propósito**,
  declaradas en `ENO_SIN_CLASIFICAR` y con aviso ruidoso al generar el slim. Un
  default silencioso ahí sería un hueco que nadie volvería a mirar. Los oficios del
  MINSAL no alcanzaron: el de Mpox no cita el literal del art. 1 y el de
  *S. pyogenes* es un PDF escaneado.
- **Los rangos NO se expanden.** El ENO trae `J00-J99` en la misma columna que las
  listas `A000, A001`; se guarda el patrón y lo resuelve `en_rango` comparando
  lexicográficamente (funciona porque los códigos van con cero a la izquierda).
- **Fallback ante actualizaciones del DEIS**: `.xlsx` explícito > **drop-in** en
  `catalogos/` > slim vendorizado. El drop-in hay que ponerlo a propósito (no se
  barre `refs_tablas/`, donde puede quedar uno viejo) y **avisa ruidoso** de que
  pisa al catálogo embebido.
- **Formato canónico de código = SIN punto** (`J209`, como el DEIS). RAYEN usa
  `J20.9`; todo cruce entre fuentes pasa por `norm_codigo`.

### Cambiado
- **Ningún archivo del repo con espacios en el nombre** (`ffcf800`, `e338e51`):
  `refs tablas/` → `refs_tablas/` y barrido del resto (`legacy/`, `license ES.txt`,
  las planillas de `refs_tablas/`). El espacio era un punto de falla real —
  citarlo mal en un `--add-data`, en una ruta de shell o en un `.gitignore` fallaba
  de formas poco obvias. `tools/catalogos_deis.py` ya baja los `.xlsx` del DEIS
  normalizados (`DEIS_cie10_2026-08.xlsx`), aunque el nombre publicado traiga
  espacios y tildes.

### Pendiente
- Pestaña de **Consultas** en la GUI (buscador código↔glosa, ENO, GES y el anotador
  batch sobre un export). Hoy la capa es solo backend.
- Enchufar `en_rango` en el A23 (asma = J09–J22 menos J19) cuando se toque ese
  módulo — hoy no lo consume nadie todavía.

### Descartado
- **`Homologación CIE-9 ↔ CIE-10` del DEIS** — irrelevante: RAYEN ya usa solo
  CIE-10. (Viene además en `.xls`, que openpyxl no lee.) Si algún día apareciera un
  export con códigos CIE-9, se reevalúa.

## [1.8.4] — 2026-09-08

### Agregado
- **Módulo `modulos/rem_sm_rescate_inasistentes.py`** (§8 del plan SP·P6) — reporte
  OPERATIVO, no tributa al REM: `Rescate_6m` / `Rescate_13m` (misma lista de 7
  actividades validada que `Activo 12m`, no el `contains "salud mental"` laxo del
  DAX original), `Fallecidos_mes` (para no llamarlos, y para el egreso del A05 en
  la fase 4), `Posibles_Traslados` (no se excluyen: se flagean para confirmar en
  vez de perseguir un abandono) y `Brecha_Medico` (dx SM activo registrado SOLO por
  un estamento no-médico). Reusa la tabla «Ferrada» que ya arma el P6 y corre junto
  a él en la pestaña BETA, con `try` propio para que un fallo ahí no tumbe el P6.
  Sin datos de contacto (§8.4: solo RUN). Hoja «LEEME» enganchada. **110 tests.**
- **`poblacion.construir_poblacion(exigir_medico=False)`** — segunda pasada sin el
  filtro de estamento médico, que `Brecha_Medico` necesita para comparar. Va con
  **guardarraíl**: `rem_sp_p6_poblacion.construir_p6()` la **rechaza** si se la
  pasan por error, porque esa pasada es exclusiva de esa hoja y alimentar el P6 con
  ella daría una población inflada sin avisar.

### Corregido
- **`tools/limpiar_refs.py`: tres defectos**, encontrados al preguntar por qué el
  `Informe_Inscritos` *header-only* pesaba 14 MB (55.002 × 92 celdas VACÍAS pero con
  estilo: un recorte manual en Excel borró los valores, no las celdas).
  - **`ListObject` colgando**: la tabla de Excel conservaba `ref="A1:CN55002"` tras
    borrar las filas → Excel abría el archivo con «contenido ilegible» y lo
    reparaba. Ahora se eliminan las tablas y el `auto_filter` de la hoja recortada.
  - **Hoja sin header reconocible se saltaba EN SILENCIO** y el archivo se reportaba
    «ya limpio» con miles de filas intactas (una lista angosta de <5 columnas pasaba
    entera). Ahora emite AVISO por hoja y un total al final.
  - **`_fila_header` inflaba el archivo**: escaneaba con `iter_rows(max_row=50)`,
    que MATERIALIZA el rectángulo → agregaba 50 filas a cada hoja vacía del libro y
    las persistía al guardar. Ahora cuenta sobre `_cells`, sin escribir.
  - Además, `delete_rows()` de 55k × 92 movía ~5M celdas de a una: sobre
    `UMBRAL_TRUNCADO` se trunca la cola directo (no hay nada debajo que desplazar).
  - Resultado: el `Informe_Inscritos` queda en **8 KB** (14.316.495 → 8.257 bytes,
    1733×) y, verificado header-only, entra a la whitelist del `.gitignore`.

## [1.8.3] — 2026-09-07

### Agregado
- **Hoja «LEEME» de cobertura** (`programas/cobertura.py`, implementa
  `docs/hoja_cobertura_plan.md`) — cada `.xlsx` de salida abre con una hoja que dice
  qué casillas del REM de ese módulo **NO** quedaron llenas y por qué (ej. las
  Consultorías A06·A.2, que son manuales). Dos capas: lo **estructural** (catálogo
  declarativo `COBERTURA`, fijo) + los **avisos de ESA corrida** (degradación por
  fuente opcional no cargada), que cada módulo pandas acumula en `.attrs['avisos']`.
  Fuente única que sirve los **dos** caminos de escritura del proyecto (pandas
  `ExcelWriter` vacío y openpyxl con la hoja ya en el índice 0). Enganchada en
  `sm_actividades`, `sm_trabajo_perdido`, `a23_respiratorio`, `sp_p6_poblacion`,
  `a03_d3_instrumentos` y el A05 (vía `autorem._correr_tareas`).
- **Test anti-olvido** `tests/test_cobertura.py`: descubre **por introspección** los
  módulos de `modulos/` con `escribir()`/`TAREA` y falla si a alguno le falta su
  entrada en `COBERTURA`. Un módulo nuevo no puede quedar sin declarar qué no cubre.
  **100 tests.**

### Herramientas
- **`tools/check_cp1252.py --instalar`** — engancha el checker al hook `pre-commit`
  **sin pisar** lo que ya haya (p.ej. `hook_pre_commit_rut.py`): convierte un `exec`
  previo en invocación normal para poder encadenar y agrega este check a
  continuación. Idempotente. Verificado en el repo: bloquea un commit con una flecha
  Unicode de prueba (exit 1, nada se commitea) y deja pasar uno limpio.

## [1.8.2] — 2026-09-02

### Corregido (regla dura: *fallar ruidoso, no callado y mal*)
- **`Madre_menor5` ahora filtra por SEXO REGISTRAL.** La pregunta 1 del formulario
  («¿usted es madre de hijo menor de 5 años?») **a veces se marca en hombres**, y esos
  por definición no cuentan. La columna del A05 (egresos e ingresos) los venía
  **sobrecontando desde siempre**. Nuevo `DEMOGRAFIA_SOLO_FEMENINO` en
  `rem_saludmental` (zona de config): los flags que el REM define solo sobre mujeres se
  anulan cuando el sexo registral no es femenino, y **el log avisa con el conteo** para
  que se corrija la ficha en RAYEN — no se descarta en silencio.
  El filtro va por **SEXO, nunca por GÉNERO**: una persona de sexo femenino y género
  transmasculino **sí cuenta** (puede ser madre). Criterio único en `rem_utils._mujer()`,
  el mismo que ya usaban `grid`, A23 y SM Actividades. Test nuevo
  `test_madre_menor5_filtra_por_sexo_no_por_genero` (mujer cis / hombre mal marcado /
  transmasculino). **62/62 tests.**

### Agregado
- **`docs/SP_P6_poblacion_plan.md`** — plan del módulo REM **SP·P6 A.1 «Población en
  control PSM»**: IRIS → tabla intermedia (la «Ferrada» del PowerBI, portada desde
  `refs_tablas/specs/Salud_Mental_spec.md`) → tabulación directa del SP. Incluye la
  máscara de celdas protegidas del P6 como validador clínico, la hoja de excepciones
  `P6_Revisar`, las unidades de conteo por bloque de filas, y las definiciones cerradas
  de Gestante (3 meses, matrona) y del Plan de Cuidado Integral. Sin implementar.

## [1.8.1] — 2026-09-02

Tanda de **correctitud, privacidad y robustez** surgida de una revisión de código
integral (Claude Octopus / `octo` code-review 🐙). Cada cambio verificado con la
batería de tests (**57/57**) y con checks funcionales puntuales.

### Seguridad / Privacidad
- **A23 deja de emitir el nombre del paciente** (§8). La hoja `A23_Detalle` volcaba
  `NOMBRES + APAT + AMAT` de cada paciente — era la **única** salida del proyecto que
  exponía nombre. Eliminada la columna; el **RUN (=RUT-DV)** queda como identificador,
  suficiente para trazar cada fila a la ficha. `Nación/Pueblo/Sexo/Sector` se mantienen.

### Corregido (regla dura: *fallar ruidoso, no callado y mal*)
- **Fechas ilegibles ya no se descartan en silencio.** Los loaders pandas
  (`cargar_atenciones`, `cargar_grupal`, `cargar_inasistentes`) parseaban la fecha con
  `to_datetime(errors="coerce")`: un valor corrupto pasaba a `NaT` y caía **fuera del
  filtro de mes sin aviso** → indicadores subcontados. Nuevo helper `rem_utils.fecha_col`
  cuenta y avisa los valores no-vacíos ilegibles (distingue vacío legítimo de fecha rota).
- **A05 sobrecontaba Pueblos Originarios.** `flag_demo` (openpyxl) no listaba
  "No sabe / No contesta / No informado" como vacío, mientras el mundo pandas sí →
  misma columna, dos definiciones. Unificado en `rem_utils.PUEBLO_VACIO` (fuente única,
  superset), consumido por A05 y por `marcar_demografia`. Un **tercer** set duplicado en
  `_origen` (A23) también migró a la constante compartida.
- **A05 y A03 ahora aplican `verificar_hoja_unica`.** La guarda que rechaza exports
  modificados (datos en >1 hoja, típico de una tabla dinámica agregada) solo corría en la
  ruta pandas; A05/A03 abrían `wb.active` sin ella → un export tocado pasaba en silencio.
- **A23 — matching por igualdad, no por subcadena.** `si()` en SALA / Sección G usaba
  `contains("SI")`: un futuro "Sin dato" / "Sigue control" (norm → `SIN…` / `SIGUE…`)
  contaba como afirmativo e inflaba el conteo. Ahora `.eq("SI")` exacto. (`est()` con
  INGRESO/SEGUIMIENTO se deja con `contains`: ahí el substring es legítimo.)
- **A23 — Migrante robusto a variantes de nacionalidad.** Comparaba con el literal
  exacto `"CHILENA"`: "Chileno" o cualquier variante marcaba **Migrante**. Ahora
  `contains("CHILEN")`.
- **SM — la edad del ADA parsea texto verboso.** `ANOS_AT` se leía con `to_numeric`
  directo mientras el grupal ya usaba `edad_anios`; si IRIS trajera la edad como
  "55 años 3 meses", caía fuera de toda banda etaria. Ahora `edad_anios` + `to_numeric`.
- **A03 — puntajes GHQ-12 fuera de rango se avisan.** El corte cubre **0–12** (scoring
  binario 0-0-1-1, estándar APS Chile); un puntaje >12 (o <0) caía **callado** al bucket
  "(sin puntaje)". Ahora se acumula y se avisa al final (posible cambio de scoring a
  Likert 0–36). El corte 0–12 se mantiene.

### Cambiado / refactor (sin cambio de comportamiento)
- `rem_utils.indice_col` unifica el helper `ci` (índice de columna por subcadena) que
  estaba reimplementado **idéntico** en `trans_map`, `atenid_multiprofesional` y
  `cargar_estrat`. Las variantes `find`/`tras` de `_resolver_otros` se dejan (son
  especializadas: excluyen tokens / buscan tras un ancla).
- `rem_utils.mes_anterior` = fuente única del "mes por defecto", antes repetido en
  `_rango_mes` y **3 veces** en la GUI (una por pestaña).
- A05 ingresos: documentado que **"REINGRESO" tributa a propósito** — para el REM, un
  reingreso es estadísticamente un ingreso (match por subcadena de "INGRESO").

### Eliminado
- Regla `_no_chileno` de `flag_demo`: código muerto (Migrante deriva de `ALERTAS` desde
  v1.2; ninguna entrada de `DEMOGRAFIA` la usaba).

### Pendiente anotado (no tocado)
- Estamento del **grupal** en SM (`rem_sm_actividades`): guarda el nombre del prestador,
  no un instrumento. Inocuo hoy (ninguna tabla desagrega el grupal por estamento); bomba
  latente si se agrega esa desagregación.

---

## [1.8.0] — 2026-09-01

### Agregado (módulo/reporte — Y++)
- **A23 tabulado por sección = reporte de verdad** (deja de ser prototipo). El
  `…_procesado.xlsx` trae una hoja copy-paste por sección (A/D/E/F/I/M.1/N) + detalle
  + G/H, con el filtro base **«Pertenece a SALA»** alineado al PowerBI. Validado
  contra el PowerBI: **~1679 vs 1585** (target real, filtrado activo+inscrito+
  validado) con span de 3 años — converge al cargar más histórico. Los 7 flags SALA
  replican los DAX 1:1 (verificado SBOR/ASMA/EPOC/FQ/OTRAS/O2/AV).

### Cambiado
- Detalle A23: `Pertenece a SALA` (col 2) y `¿Atendido 1 mes?` (col 3) al frente,
  para revisar de un vistazo.

### Pendiente (afinar con el RT / validar 1:1)
- A (semántica ingreso-a-sala), I espirometría basal vs post BD, sección O (EPOC A/B),
  y el filtro activo+inscrito+validado. B/C/P/Q/M.2/J/K/L fuera de alcance.

---

## [1.7.13] — 2026-09-01

### Corregido (alineación con PowerBI)
- **Filtro base "Pertenece a SALA"** (DAX del PowerBI): el A23 se reporta SOLO sobre
  quienes están bajo control en sala (OR de los 7 flags SALA). Antes las secciones
  contaban sobre TODOS los RUN con atención (~15.860 vs ~1.907 del PowerBI). Ahora
  el detalle expone la columna `Pertenece a SALA` y las **secciones se calculan solo
  sobre ese subconjunto**. Se agregan las columnas `SALA O2 Dependiente` y
  `SALA Asistencia Ventilatoria`.
- **SALA O2 / Asistencia Ventilatoria**: alineado al DAX — **NO exigen médico** (a
  diferencia de ASMA/EPOC, que sí). Antes se les pedía médico → subcontaban.

---

## [1.7.12] — 2026-09-01

### Agregado (PROTOTIPO)
- **A23: salida tabulada por sección (copy-paste al SA_26), estilo SM Actividades.**
  `escribir()` ahora deja, en el MISMO `…_procesado.xlsx`, una hoja por sección
  además del detalle por paciente y las Secciones G/H (todo se SUMA, nada se
  reemplaza): **A** (ingresos agudos), **D** (morbilidad médico), **E** (controles
  crónicos; Enfermera/o=0), **F** (seguimiento agudos), **I** (procedimientos),
  **M.1** (educación individual), **N** (visitas). Forma exacta del template
  (Ambos·H·M + 18 bandas etarias × sexo) vía `_grid` de rem_utils.
  - **PENDIENTE de validar 1:1 vs PowerBI** (filas rotuladas en la propia hoja):
    A semántica "ingreso a sala" (hoy usa el dx por-RUN), asma-A (confirmado +
    J09-J22), I espirometría basal vs post BD (hoy 1 indicador → todo a basal), y
    la Sección **O** (forma EPOC A/B, fuente `EPOC_tipo`/col BA de Otros y Respi).
  - Fuera de alcance: B/C (bajo control → PowerBI), P/Q/M.2/J/K/L.

---

## [1.7.11] — 2026-09-01

### Corregido (fail loud + qué archivo falló)
- **Un archivo de entrada no legible / sin encabezado / modificado ahora da un
  mensaje CLARO** en vez de "Error inesperado → pásaselo a Simón". `cargar_canonico`
  valida CADA archivo y, si falla, levanta `ArchivoInvalido` **nombrando el archivo
  culpable** (`«nombre.xlsx»`) — clave para los módulos que cargan VARIOS (A23:
  atenciones + otros + NSP; SM: ADA + grupal). Cubre 3 casos: no legible (.xls/.csv/
  .html/corrupto), datos en >1 hoja (modificado), y faltan columnas (sin la fila de
  nombres). `cargar_atenciones` y `cargar_grupal` declaran sus columnas requeridas.
- `_error_inesperado`: loguea `Tipo: mensaje` (antes, en el hilo worker, salía
  "NoneType: None" porque `format_exc()` no tenía traceback vivo).

> Nota: los .xlsx de la "datos-madre" (fuente del PowerBI, header en fila 1 sin
> banner, mismo esquema del ADA) **se leen tal cual** — verificado; sirven para
> validar el A23 1:1 contra el PowerBI. No requieren nada especial.

---

## [1.7.10] — 2026-09-01

### Cambiado (fail loud)
- **A23 · Otros Crónicos: aviso preciso si falta el año anterior.** El reporte se baja
  POR AÑO calendario y la Sección G mira ≥12 meses atrás; reportar un mes exige el año
  del reporte **y el anterior**. El chequeo pasó de "span < 365 días" (dejaba pasar
  cargar solo el año en curso) a **fecha mínima ≤ 12 meses antes del mes reportado**
  → avisa exacto cuándo arrancan los formularios vs. hasta dónde se necesita.
- **GUI A23**: instrucciones + labels aclaran que Atenciones puede venir del año
  completo (se filtra al mes) y que Otros Crónicos toma VARIOS años (ctrl-click:
  año del reporte + anterior). **Inasistentes NSP** ahora también acepta VARIOS
  años (antes la GUI tomaba solo el 1er archivo; `cargar_inasistentes` ya concatena)
  → se filtra al mes por FECHA CITA.

---

## [1.7.9] — 2026-09-01

### Corregido
- **Scroll vertical en las pestañas A03 y A23** (antes solo A05 y SM lo tenían): en
  pantallas chicas el contenido se dibujaba fuera de la ventana sin barra. Ahora las
  **4 pestañas** usan `_tab_scroll`. Contenido de altura fija → no aplica el
  known-issue del encoger (ese es solo del toggle de cuestionarios en SM).

---

## [1.7.8] — 2026-09-01

### Agregado (fail loud)
- **Mensaje claro al cargar un archivo que NO es `.xlsx`.** RAYEN/IRIS exportan en
  `.xls`, `.csv`, `.html` y `.xlsx`, pero la herramienta lee SOLO `.xlsx`. Antes,
  elegir cualquier otro caía al genérico "Error inesperado" con traceback; ahora un
  diálogo «No es un .xlsx» explica que hay que abrirlo en Excel y **Guardar como →
  .xlsx**. Cubre las 4 pestañas (GUI) y el CLI, de un solo lugar (`_es_error_formato`
  + `_MSG_NO_XLSX`): atrapa `InvalidFileException` (extensión no soportada: .txt/.csv/
  .xls) y `BadZipFile` (el **HTML disfrazado de .xlsx** que a veces entrega RAYEN).

---

## [1.7.7] — 2026-09-01

### Agregado (fail loud)
- **Aviso ruidoso si el Maestro NO está disponible**: si no se cargó a mano ni se
  encontró embebido/junto al `.exe`, el log avisa que el Trabajo Perdido corre en
  heurística (antes fallaba en silencio a heurística sin avisar).
- **Aviso ruidoso si el Monitoreo Multiprofesional no cubre el mes**: como el
  reporte se cruza por ATEN ID (no se filtra por mes), si NINGUNA VDI de A26 del mes
  coincide con el padrón, probablemente es de otro período → A26 saldría todo "Un
  Profesional". Ahora se avisa en el log.

### Corregido (empaquetado)
- **Build del `.exe`**: el comando de PyInstaller (CLAUDE.md §11 + README) ahora
  incluye `--add-data "refs_tablas/maestro_slim.csv.gz;refs_tablas"` para EMBEBER el
  Maestro slim. Sin esto el `.exe` no lo traía y el Trabajo Perdido caía a heurística.

---

## [1.7.6] — 2026-09-01

### Cambiado
- **La pestaña A05 ahora también tiene el cuadro «Carpeta de salida»** (era la
  única sin él). Vacío = junto al archivo de entrada (el comportamiento clásico del
  A05 vía `with_name`), consistente con A23/SM/A03. `_correr_tareas` acepta `carpeta`.

---

## [1.7.5] — 2026-09-01

### Agregado
- **La tabla Funcionario→Estamento ahora PERSISTE entre corridas.** Antes había que
  cargar el reporte *Utilización de Cupos* en cada corrida (y un mes después de
  nuevo). Ahora se cachea en `~/.autorem/estamentos.json` (por usuario, fuera del
  repo): se carga una vez y los meses siguientes se autocompleta sola. Cargar un
  *Utilización de Cupos* nuevo **fusiona** con lo guardado (el reporte fresco gana;
  los funcionarios que solo estaban en caché se conservan). Nuevas funciones en
  `programas/estamentos.py`: `cargar_cache` / `guardar_cache` / `tabla_efectiva`
  (robustas: un caché corrupto o sin permisos NO tumba la corrida, solo avisa).
  Nombres de funcionario NO son PII de paciente → cachearlos es aceptable.

### Corregido
- Texto engañoso en la GUI (decía cargar la tabla "una vez" dando a entender que
  quedaba guardada; ahora sí queda, y el texto lo refleja).

---

## [1.7.4] — 2026-09-01

### Cambiado
- **Carpeta de salida por defecto = junto al archivo cargado.** Antes las pestañas
  A23 / SM / A03 caían a la carpeta del `.exe` (o el cwd) → corriendo desde el repo
  se llenaba de `.xlsx`. Ahora el campo «Carpeta de salida» **vacío** guarda el
  resultado en la carpeta del archivo de entrada (`_valida_carpeta` acepta `defecto`;
  el A05 ya lo hacía vía `with_name`).

### Docs
- `A23_P3_plan`: fuente CIE-10 identificada = Lista Tabular **DEIS/MINSAL** (dato
  público); quirks anotados (formato `Annn` vs `Ann.n` de RAYEN; RAYEN no tiene
  "maestro de diagnósticos"; lista ~2018). Archivo guardado local, **gitignored**.

---

## [1.7.3] — 2026-08-28

### Agregado
- **Filtro de mes en A05 (Egresos / Ingresos)**: la pestaña deja elegir **Archivo
  completo** o **un mes puntual** (año/mes), filtrando los formularios por **FECHA
  FORMULARIO**. En la GUI es una caja «Período» con radio + spinboxes; en el CLI,
  el flag `--mes AAAA-MM` (por defecto, archivo completo).
  - **Fail loud**: si se pide un mes SIN formularios en el archivo, levanta
    `ArchivoInvalido("mes_vacio")` con aviso claro (no genera un archivo con 0
    filas en silencio). Sin columna de fecha → `ArchivoInvalido("sin_fecha")`.
    Formularios con fecha ilegible se excluyen **y se avisa** en el log.
  - Nuevo helper `rem_utils.mes_de_celda`: `(año, mes)` desde la celda, distingue
    por ESTRUCTURA **IRIS `DD/MM/YYYY`** vs **Admin `YYYY/MM/DD`** (NO `dayfirst`
    a ciegas — leía `2026/07/06` como junio). Acepta datetime de openpyxl y texto.
  - Nombre de salida: al elegir mes, `…_procesado_AAAA_MM.xlsx` (archivo completo
    sigue siendo `…_procesado.xlsx`).

### Corregido
- **Scroll vertical en la pestaña A05**: con la caja «Período» ya no cabía todo;
  ahora usa `_tab_scroll` (como Actividades). Contenido de altura fija → no aplica
  el known-issue del encoger.

---

## [1.7.2] — 2026-08-10

### Cambiado / Arquitectura
- **Nuevo módulo compartido `programas/formatos.py`**: se extrajo el **eje de
  formato IRIS vs Administrativo** (firmas RAYEN, `detectar_eje`, resolución
  RUT/edad/sexo `resolver_identidad`, y los params de encabezado del lado ADMIN
  `HEADER_ADMIN`, transversales a A05/A03/Utilización de Cupos). Antes estaba
  **duplicado** entre `rem_saludmental` y `rem_a03_d3_instrumentos` (firmas +
  `detectar_formato` copiados verbatim) y con literales sueltos en `estamentos`.
  Ahora el MECANISMO vive una sola vez; cada reporte aporta solo SUS firmas.
  Cadena de dependencias: `rem_utils` (primitivas) ← `formatos` (eje) ← módulos.
  - `rem_saludmental.detectar_formato` pasa a ser wrapper de `formatos.detectar_eje`.
  - `a03` deja de reimplementar detección/encabezado; unifica la confirmación por
    RUT (antes solo verificaba el ancla → ahora ancla + RUT, más robusto).
  - `estamentos._fila_encabezado` toma los params admin de `formatos.HEADER_ADMIN`.
  - Preparado para que **cada módulo nuevo con entrada RAYEN** enchufe sus firmas
    acá en vez de recopiar la lógica (grupo pandas —atenciones/NSP— en 2ª fase).

### Cambiado / Limpieza (`/simplify`)
- **`_rango_mes` unificado** a `rem_utils` (estaba duplicado en A23 y SM
  Actividades; Trabajo Perdido lo importaba cruzado). `_mujer`/`_hombre` de
  `rem_utils` reutilizados en la Sección G del A23.
- **Eficiencia**: A23 hace una sola pasada de `sort_values/groupby` sobre el
  histórico (se eliminó un groupby redundante); `marcar_eventos` precomputa las
  columnas ESTADO fuera del loop de filas; TRANS de SM Actividades vectorizado.
- **Código/imports muertos** eliminados: `escribir_detalle` (A23), `solo_entero`
  (rem_saludmental), `calendar`/`date`/`Path` sin uso.

## [1.7.1] — 2026-08-07

### Corregido / UI
- **Scroll vertical en la pestaña Actividades** (`_tab_scroll`): al desplegar los
  cuestionarios A03·D.3 el contenido supera el alto de la ventana; ahora hay barra de
  scroll para llegar al Registro y al botón (antes solo se veía agrandando la ventana).
- **KNOWN ISSUE** (documentado, no se arregla): al DEStickear cuestionarios el
  scrollregion no se encoge de vuelta (queda scroll sobrante). Es el baile
  Canvas+scrollregion de tkinter; se resuelve gratis en la GUI 2.0 (customtkinter →
  `CTkScrollableFrame`).

## [1.7.0] — 2026-08-07

Módulo nuevo (Y++): **reporte A03·D.3 UNIFICADO** (cuestionarios PSC/PSC-Y/GHQ-12 →
tabla lista para copiar-pegar al SA_26) + grilla `grid` compartida.

### Agregado
- **`rem_a03_d3_instrumentos.procesar_unificado`** — junta los 3 instrumentos de
  monitoreo del PSM en la **tabla A03·D.3** del SA_26: 6 filas (Evaluación ingreso/
  egreso × Bajo/Medio/Alto) × [Total(Ambos·H·M) + bandas etarias × sexo] +
  hoja **DETALLE auditable al final** (una fila por aplicación). Solo INGRESADOS al
  PSM; **'Sin riesgo'** (bajo el corte) va al detalle pero **NO** al D.3 (no es
  categoría del REM). Tamizaje (PSC-17/PHQ-9…) = A03·H, fuera de alcance.
- **GUI A03**: 3 slots (PSC / PSC-Y / GHQ-12), cargás los que existan (≥1); el slot
  fija el instrumento (fuera la auto-detección + el dropdown). Reloj threaded +
  carpeta de salida. Estamentos opcional (solo alimenta el detalle).
- **Checkbox "¿Incluir cuestionarios?" en Actividades**: al marcarlo despliega los 3
  slots del A03·D.3 y, al procesar, genera también `REM_A03_D3_AAAA_MM.xlsx` (mismo
  botón). *(Duplicado a propósito con la pestaña A03 standalone; en la GUI 2.0 se
  elimina la standalone y el A03 vive solo acá.)*
- **`rem_utils.grid`** (+ bandas `BANDAS_A04/A06`) — grilla edad×sexo movida a la base
  compartida; la usan SM, A03 (y A23 en P3). `procesar(salida=None)` del A03 devuelve
  las filas sin escribir (para el reporte unificado).
- Tests `test_tabla_d3_excluye_sin_riesgo` + `test_procesar_unificado` (screening 11/11).

## [1.6.1] — 2026-08-07

Feedback en la GUI (ventana ya no se congela) + wins de perf. Fallback seguro antes
del overhaul a customtkinter (2.0.0).

### Agregado
- **Reloj de arena** (indicador indeterminado dibujado que gira, `_Reloj`) + **worker
  en hilo** (`_correr_con_reloj`) en las pestañas lentas (SM y A23): el procesamiento
  corre en un `threading.Thread`, la ventana **ya no se congela** ("No responde"), y el
  log fluye en vivo (cola thread-safe volcada por `root.after`). Sin barras de progreso
  (mienten): solo "estoy trabajando".
- **Dispatch de errores** `_manejar_error`: ImportError/PermissionError/**ArchivoInvalido**
  (p.ej. la guarda multi-hoja) → messagebox claro, sin traceback feo.

### Corregido / UI
- **Etiquetas truncadas** en los selectores de archivo (se cortaban "Inasistentes NSP…"
  y "Maestro Actividades…"): ancho 26→30 + textos acortados.
- **Separador visual** entre inputs OBLIGATORIOS y OPCIONALES en SM y A23
  (`_separador_opcionales`, barrita horizontal + rótulo "Opcionales").
- **Grupal (SM) y Otros Crónicos (A23) ahora son OBLIGATORIOS**: avisan y frenan si
  faltan (antes seguían con casillas en 0). *(Otros Crónicos puede volverse opcional
  según responda el referente.)*

### Cambiado (rendimiento)
- **El ADA se lee UNA sola vez** y se comparte entre SM Actividades y Trabajo Perdido
  (antes se leía dos veces). `procesar(..., d=None)` en ambos módulos acepta el
  DataFrame ya cargado → ~½ del tiempo del bloque SM.
- **Trabajo perdido usa el Maestro slim por defecto**: si no eliges un Maestro en la
  GUI, toma `maestro_slim.csv.gz` del repo/exe (`_slim_por_defecto`, busca también en el
  bundle de PyInstaller) → clasificación precisa sin cargar nada.

## [1.6.0] — 2026-08-07

Módulo nuevo (Y++): **REM SM · Trabajo perdido** ("saco vacío") + **Maestro de
Actividades** como catálogo de clasificación + **guarda de archivo modificado**.

### Agregado
- **Módulo `modulos/rem_sm_trabajo_perdido.py`** — reporte de auditoría (NO tributa al
  REM). Detecta atenciones del ADA cuya ACTIVIDAD trae 'mental'/'demencia' pero **no
  tributan** a las casillas SM que el exe reporta (A04/A06/19A/A26/A27/A32), y **nombra
  al funcionario** (`PROFESIONAL ATENCION`) que las registra → apunta a disminuir el
  trabajo a saco vacío. Salida: `Por_Actividad` (con NUM REM, para ver por qué) +
  `Por_Funcionario` (a quién avisar) + `TP_Resumen` + `TP_Detalle`. Reciclado del módulo
  de actividades (mismo ADA, `_rango_mes`, `mask_tributa_ada`). Reporte aparte, no fork.
  Se genera junto al SM Actividades (mismo ADA) → `REM_SM_trabajo_perdido_AAAA_MM.xlsx`.
- **Maestro de Actividades** (`rem_utils.cargar_maestro` + `maestro_rem_map`): catálogo
  RAYEN actividad↔estamento↔casilla REM (217k filas). Es la **autoridad** para clasificar
  qué tributa; para actividades que RAYEN agregue después y no estén en el Maestro, cae
  la **heurística** substring (sigue siendo heurística, por diseño). Selector opcional en
  la pestaña SM. Definición de "perdido" (elegida por el referente): **todo lo SM-ish que
  no cae en A04/A06/19A/A26/A27/A32** (incluye REM-Gestion, A03, A28…); el NUM REM se
  muestra para poder refinar.
- **Maestro SLIM versionado** (`refs_tablas/maestro_slim.csv.gz`, ~1.2 MB) + generador
  `tools/slim_maestro.py`: el Maestro completo (7.7 MB) queda LOCAL; el script lo recorta a
  actividad × estamento × clasificación REM (sin las 6 flags) y lo comprime. `cargar_maestro`
  lee `.csv.gz` además de `.xlsx`. Whitelisteado en `.gitignore` (sin PII de paciente).
- **`rem_utils.verificar_hoja_unica`** — guarda de integridad: los exports RAYEN/IRIS
  siempre bajan 1 hoja con datos + 2 vacías; datos en **>1 hoja = archivo MODIFICADO**
  (típico: se le agregó una tabla dinámica) → `ArchivoInvalido('modificado', …)`. Enchufada
  en `cargar_canonico` → cubre ADA, grupal, A23 (otros/NSP). Robusta a la 'dimension' rota.
- **`ADA_TRIBUTAN` + `mask_tributa_ada`** en `rem_sm_actividades` — fuente única de qué
  actividades del ADA tributan a algún REM SM (la reciclan el módulo y el detector).
- **`PROFESIONAL ATENCION`** agregado al `MAPA_ATENCIONES` (nombre del funcionario, IRIS).
- **`tools/limpiar_refs.py`** + **skill `limpiar-refs`** — recorta a solo-header cualquier
  export nuevo en `refs_tablas/` (privacy-by-design, §8), **sin leer valores** (cuenta
  celdas para ubicar el header). Denylist protege templates/`calculador`/`minimanual`/
  `comentado`/`arsenal`/`maestro`.
- Tests `tests/test_trabajo_perdido.py` (9/9): clasificación por Maestro, heurística de
  actividad nueva, Por_Funcionario, sin-maestro, filtro de mes, y la guarda multi-hoja.

### Seguridad / privacidad
- La guarda multi-hoja + el recorte a header-only refuerzan que el repo nunca vea PII
  aunque un export venga modificado o sin anonimizar.

## [1.5.6] — 2026-08-04

Ajustes de las tablas de SM Actividades al traspasar al SA oficial + composición
profesional de A26.

### Corregido
- **EDAD del grupal en TEXTO** (`'55 años 3 meses'`): `cargar_grupal` la parsea con
  `edad_anios` → antes la desagregación por banda etaria de A06 Psicosocial Grupal
  (y A19a/A27 grupal) salía **0** (el texto no era numérico). **URGENTE**, corregido.

### Cambiado (formato copy-paste al template)
- **A04**: se quita **Campaña de Invierno** (write-protected en la hoja de SM).
- **A06**: se quita la fila **TOTAL** (write-protected, la calcula el template).
- **A19a**: **fila en blanco** entre 'problema SM' y 'demencia' (en el template hay
  otra fila al medio) → copy-paste directo.
- **A32·F1**: se agregan las columnas **Hombres / Mujeres** (el template agrupa por
  sexo al final de las bandas etarias).
- **A26**: columnas en el orden del template (composición profesional + Primera/
  Segunda/Tercera visita + demografía).

### Agregado
- **A26 composición profesional** vía nuevo input opcional **Monitoreo Multiprofesional**
  (`rem_utils.atenid_multiprofesional`): las VDI cuya ATEN ID tiene un profesional
  adicional pasan a **'Dos o Más Prof.'**; sin el reporte, todo se asume mono-profesional.
  `procesar(..., multiprofesional=None)` + selector opcional en la GUI. Test
  `test_a26_multiprofesional`.

### Nota
- **A03 (screening)** aún NO se integra a Actividades (la carga de archivos se vuelve
  engorrosa) → se mantiene en su pestaña aparte por ahora.

## [1.5.5] — 2026-08-04

### Corregido
- **TRANS ya no falla en silencio**: si el 'Informe Inscritos' viene MODIFICADO o es
  otro reporte (sin columna GÉNERO/RUN), `trans_map` ahora levanta un error claro y
  `procesar` lo captura → avisa fuerte en el log y deja TRANS en 0, en vez de reportar
  0 callado (que se daba por bueno). También avisa si el padrón COMPLETO arroja 0 TRANS
  (sospechoso → archivo filtrado/modificado). Test `test_trans_inscritos_modificado`.

## [1.5.4] — 2026-08-04

### Cambiado
- **Sección G — aviso de span corto**: la Sección G solo sirve con historial largo
  (los inasistentes tienen su último control hace >1 año; el PowerBI usa ~5 años).
  Ahora avisa en el log si los formularios 'Otros y Respi' cubren <1 año → G subcontará.
  Como los formularios se bajan POR AÑO, hay que cargar VARIOS archivos (mín. año actual
  + anterior). Instrucción de la GUI actualizada. (No hay fix posible sin más input;
  el conteo per-mes vs 5-años del PowerBI explica la diferencia de totales.)

## [1.5.3] — 2026-08-04

REM A23: completa las **Secciones G y H** de inasistentes (P2).

### Agregado
- **Sección H (inasistentes a citación agendada)**: nuevo loader `cargar_inasistentes`
  (reporte NSP) + `_seccion_h()` → cuenta citas **Control/Ingreso IRA/ERA** NO asistidas
  del mes (por **FECHA HORA CITA**, NO fecha NSP), por **estamento** (Médico/Kinesiólogo/
  Enfermera) × tramo (**<20 / ≥20 años**). Conteo por cita; excluye KTR (kinesioterapia
  respiratoria sin control/ingreso). `procesar(..., inasistentes=None)` + hoja
  `A23_Seccion_H` + selector opcional en la GUI. Test `test_seccion_h`.
  Julio real: Médico 15 · Kinesiólogo 12 · Enfermera 0 · total 27.

### Corregido
- **Sección G alineada al DAX `REMA23 Inasistentes`**: el S.B.O. recurrente ahora exige
  además **¿ES RECURRENTE? = sí** (antes contaba SBO no recurrentes). Julio: SBO 13→12.
  El resto (umbrales por edad, FPC por patología, estado ingreso/seguimiento) ya cuadraba.
  (Spec en `docs/A23_spec.md/.json` — la página PowerBI de A23.)

## [1.5.2] — 2026-08-04

Completa el flag **TRANS** en SM Actividades usando el 'Informe Inscritos y Adscritos'.

### Agregado
- **`rem_utils.trans_map()`**: lee el 'Informe Inscritos y Adscritos' (padrón completo
  del CESFAM, ~55k filas) → `dict RUN → 'M'/'F'` para personas **TRANS** según la
  **selección explícita en GÉNERO** ('Transgénero Masculino/Femenina', 'Femenino
  Trans'). Se abandona la vieja heurística DAX `género≠sexo` (obsoleta desde que RAYEN
  permite marcar TRANS directo, y ruidosa: 408 mismatches vs 43 explícitos reales).
- `rem_sm_actividades.procesar(..., inscritos=None)` + flags `dem_trans_m`/`dem_trans_f`
  → columnas **TRANS Masculino / TRANS Femenina** en A06 (split del template). Selector
  opcional 'Inscritos' en la pestaña GUI (archivo ENORME → solo para TRANS).
- Test `test_trans_flag`.

### Corregido
- **Bug de índice-cero** en `trans_map`: `ci(...) or ci("RUN")` caía a `ci("RUN")`
  cuando la columna estaba en índice 0 (`0 or x` es falsy). Con check explícito de None.

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
