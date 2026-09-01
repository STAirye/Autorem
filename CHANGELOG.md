# Changelog — autoREM

Todos los cambios relevantes de este proyecto se anotan acá.
Formato inspirado en [Keep a Changelog](https://keepachangelog.com/es/).

**Versionado `X.Y.Z`** (ver [CLAUDE.md](CLAUDE.md) §9):
`X` = programa · `Y` = módulos de programa acumulados · `Z` = corrección del
módulo que se está trabajando (reinicia al subir `Y`).

Tipos de cambio: **Agregado** (nuevo) · **Cambiado** · **Corregido** ·
**Eliminado** · **Seguridad**.

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
  incluye `--add-data "refs tablas/maestro_slim.csv.gz;refs tablas"` para EMBEBER el
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
- **Maestro SLIM versionado** (`refs tablas/maestro_slim.csv.gz`, ~1.2 MB) + generador
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
  export nuevo en `refs tablas/` (privacy-by-design, §8), **sin leer valores** (cuenta
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
