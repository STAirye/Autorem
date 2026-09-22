# Changelog — autoREM

Todos los cambios relevantes de este proyecto se anotan acá.
Formato inspirado en [Keep a Changelog](https://keepachangelog.com/es/).

**Versionado `X.Y.Z`** (ver [CLAUDE.md](CLAUDE.md) §9):
`X` = arquitectura grande o plantillas REM de un año nuevo · `Y` = módulo o
reporte nuevo · `Z` = corrección (reinicia al subir `Y`).

Tipos de cambio: **Agregado** (nuevo) · **Cambiado** · **Corregido** ·
**Eliminado** · **Seguridad**.

## [2.0.9] — 2026-09-22

### Cambiado

**Segunda ronda de EFICIENCIA sobre `main`** (decisión del autor, §12). Cinco cambios,
todos con equivalencia verificada contra la versión anterior. Familia población
**4,06 s → ~1,0 s**; el colapso de atenciones del Monitoreo admin, hasta **5,5x**.

- **`rem_utils._una_fila_por_atencion`: la cabecera se ELIGE POR POSICIÓN.** El
  `groupby().agg({col: función Python})` mandaba a pandas por su camino pure-python
  —una rebanada de Serie por cada par (grupo × columna), 140.007 llamadas a `_chop` en
  un Monitoreo de 20.000 filas—. Lo que `_primero` calculaba era, en el fondo, una
  posición: la del 1er valor no vacío del grupo y, si el grupo venía entero vacío, la de
  su 1ª fila. Eso es un `min()` por grupo sobre enteros (que pandas sí hace en C) más un
  indexado numpy sobre los valores ORIGINALES. **1,26 s → 0,50 s**, y **2,15 s → 0,39 s
  (5,5x)** en la forma con más atenciones sueltas, que es la del Monitoreo real.
  ACT/DIAG siguen con `_juntar`: juntar y deduplicar no es elegir una fila.
- **`poblacion._tok`: memo por DataFrame de las máscaras de ESTADO.** No era obvio que
  se repitieran: dentro de una pasada cada columna ESTADO es de UNA spec, pero
  `_egreso_powerbi_bug` recorre las 29 de `ESTADOS_TODOS` calculando el EGRES de todas
  —las mismas que `_estado_dx` recalcula una por spec— y Brecha_Medico repite la pasada
  entera **y además** llama a `_estado_dx` dos veces más por spec, con el mismo dx y
  estado. Cada máscara se calculaba hasta 4 veces. **2,26 s → 0,87 s** en las dos
  pasadas.
- **`poblacion._ultima_respuesta`: recorte de columnas.** Ordenaba y agrupaba las 134
  columnas del formulario histórico para leer UNA. **0,514 s → 0,019 s (28x).**
- **Brecha_Medico ya no arma la tabla entera dos veces.** Corría
  `construir_poblacion` COMPLETA por segunda vez —1,66 s de los 4,06 s de la familia
  población, el 41%— y de esa tabla consumía UNA columna. Ahora pide solo
  `¿Ingresado?` sin filtro de estamento (`runs_ingresados_sin_filtro_medico`), y lee
  `Estado` y `¿Activo 12m?` del `P` que ya existe porque no dependen del toggle.
- **`rem_sp_p6_poblacion._grid_y_detalle`: `zip` en vez de `iterrows`**, y se cuentan
  las máscaras demográficas en vez de materializar el subconjunto de filas.
  `construir_p6` **1,53 s → 0,93 s**.
- Menores, del mismo perfil: el `map(norm)` de ALERTAS izado fuera de
  `marcar_demografia.alerta` (3,2x), la guarda `no_vacias` de `cargar_canonico` con
  corto circuito en vez de normalizar la columna entera, y el `est()` del A23 por
  `contiene_alguno` en vez de dos `.str.contains` que normalizaban la misma columna dos
  veces (47 → 34 pasadas sobre el formulario «Otros y Respi»).

### Agregado

- Seis tests. Los cinco primeros son **mutation-verificados**: la implementación se
  rompió a propósito y cada mutante cae.
  - `test_a23`: la cabecera de una atención sale de SU grupo (sin centinela se lleva el
    SECTOR de otro paciente), el respaldo es la 1ª fila **posicional** (un
    `groupby().first()` de pandas salta los nulos) y el ATEN ID numérico sigue entero.
  - `test_sp_p6`: las máscaras de ESTADO no se filtran de una corrida a la siguiente; la
    máscara cacheada aguanta que el llamador la pise; «Madre <5 años» toma la última
    respuesta **con dato** hasta el corte (contrato que no fijaba ningún test); y **el
    plegado de edad queda colgado de la persona correcta**.
  - `test_rescate`: la brecha da el MISMO set por el atajo y armando la tabla entera,
    con cuatro personas que cubren las dos mitades del filtro base. El mismo test fija
    la PREMISA: si `Estado` o `¿Activo 12m?` pasan a depender del toggle, revienta ahí.

### Notas

- **Dos memos entregan una COPIA de la máscara** (`_tok` y `_instr_medico`): `serie &=
  otra` en pandas SÍ muta la Serie en su lugar, así que devolver el objeto cacheado
  dejaría que el primer llamador lo pise y la spec siguiente leyera una máscara ya
  intersectada. Copiar una de 60k cuesta 0,007 ms contra los 10 ms del `str.contains`.
- **El bucle de las 28 specs quedó en UNA función compartida** (`_poner_diagnosticos`),
  no copiado en los dos lados: lo que Brecha_Medico mide es la DIFERENCIA entre las dos
  pasadas, y con dos copias del bucle la hoja pasaría a medir la distancia entre dos
  implementaciones en vez de la del filtro de estamento.
- **`runs_ingresados_sin_filtro_medico` devuelve un SET y no una columna** a propósito:
  una Serie alineada a `P` se puede escribir de vuelta en la tabla, y ahí el guardarraíl
  del P6 (que mira `attrs['exigir_medico']`) ya no la vería.
- **DESCARTADO, medido:** `ws.cell(row,col).value` por celda NO es lento. En modo normal
  openpyxl ya materializa todas las celdas al cargar, así que es un lookup de
  diccionario: 0,33 s contra 0,35 s de `iter_rows(values_only=True)`. No volver a
  reportarlo (arnés en `docs/evanesced/eficiencia-2.0.9/bench_cell.py`).
- **Cómo se ordenó el trabajo, que es la lección de la ronda:** ordenar por lectura del
  código se equivocó **tres veces seguidas**. El hallazgo más caro
  (`_ultima_respuesta`) no estaba en ninguna de las dos listas de revisión; el que
  parecía grande valía 0,28 s. El perfil de `construir_poblacion` entera reordenó la
  ronda. Arneses en `docs/evanesced/eficiencia-2.0.9/`.
- **Dos cosas encontradas y NO arregladas**, con su motivo, en §12 del CLAUDE.md raíz:
  `norm(pd.NA)` revienta, y el orden de filas de `Revisar_Clinico` no es determinista
  entre corridas.

## [2.0.8] — 2026-09-22

### Corregido
- **Un inscrito SIN RUN sobrevivía como persona fantasma bajo pandas 3.** La guarda de
  `poblacion.cargar_inscritos` era `d["RUN"].isin(("", "None", "nan"))`, y esos literales
  sólo aparecen si `astype(str)` convierte el faltante en TEXTO — que es lo que hacía
  **pandas 2**. **Pandas 3 lo PRESERVA**, así que el `isin` no veía nada y la fila pasaba:
  el snapshot Ferrada salía con una persona de `Número` NaN (y las varias sin RUN
  colapsaban en una sola por el `drop_duplicates`).

  **Qué alcanzaba y qué no:** la grilla del P6 NO se movía — `_base_valida` descarta esa
  fila con `rut_valido` —, pero ensuciaba la hoja `PSM_Poblacion`, que es justamente la
  que se archiva mes a mes para auditar, e inflaba el `N personas en el snapshot` del log.
  Y apagaba la guarda fail-loud en el caso MIXTO (un `RUN Responsable` + una fila sin RUN),
  que es para el que existe. El caso «ninguna fila trae RUN» seguía cortado antes, por el
  `no_vacias` de `cargar_canonico`.

  Ahora lleva **las dos mitades**, una por cada pandas mayor:
  `d["RUN"].isna() | d["RUN"].isin((...))` — el mismo patrón que `rem_utils.fecha_col`,
  que ya lo hacía bien un archivo más allá. Lo cazaba
  `test_inscritos_con_filas_pero_ningun_run_usable_lo_dice`, que llevaba tiempo en rojo.

  **Lo que habría evitado esto:** la regla 4 del CLAUDE.md. Todo el resto del código
  filtra el RUN vacío con `norm(run) == ""`, que maneja el faltante solo y es inmune al
  cambio de pandas; éste era el único punto que se salió del idioma y comparó contra
  literales.

### Cambiado
- **`requirements.txt`: `pandas>=2.0,<4`**, y dice POR QUÉ cada extremo. El piso es que el
  código corre en 2.x y 3.x a propósito (el `.exe` se compila con la versión de turno,
  pero un clon nuevo instala lo que pip tenga ese día), con las diferencias que hay que
  aguantar anotadas: `astype(str)` sobre un faltante y el dtype inferido de las columnas
  de texto. El techo NO es prudencia genérica: `rem_utils.grid()` ya dispara
  `Pandas4Warning` y **pandas 4 lo vuelve error** (§12, «Deuda»), así que sin tope un
  `pip install` el día que salga pandas 4 dejaba la herramienta reventando en la grilla
  edad x sexo, que es la salida.

## [2.0.7] — 2026-09-22

Cierra el hallazgo que había destapado el arnés de la 2.0.6: tras recortar las columnas,
el costo dominante de `_estado_dx` ya no era el `groupby` sino sus máscaras.

### Cambiado
- **La máscara «lo aplicó un médico» se calcula una vez por formulario, no 28.**
  `INSTR_n.str.contains("MEDIC")` es lo único de `_estado_dx` que NO depende del
  diagnóstico ni del estado, y se recalculaba en cada spec de cada pasada (más las de
  `Brecha_Medico`). Medido sobre 30k filas: **0,138 s de los 0,425 s** que cuestan las
  máscaras — un 32% de ellas, ~22% de la función. Equivalencia re-verificada con el mismo
  arnés de la 2.0.6 (56 comparaciones contra la implementación de la 2.0.5): 0 diferencias.

  **Es un memo de una ranura y por weakref, no un parámetro `instr_ok=`**, y las dos
  decisiones son de seguridad, no de estilo:
  - un parámetro dejaría pasar una máscara calculada sobre OTRO DataFrame; alinearía por
    posición y daría un Activo que no existe, callado (regla 2). Derivándola siempre del
    `df` recibido, no hay forma de equivocarse. De paso quedó comprobado que **`pandas` NO
    comparte el objeto índice** entre un DataFrame y una Serie derivada (`serie.index is
    df.index` da `False`), así que la guarda barata por identidad que parecía obvia no
    existe.
  - el weakref evita retener el formulario histórico (cientos de MB) después de la
    corrida; `ref()` devuelve `None` cuando el df murió, nunca un objeto distinto.

### Agregado
- **Test de que esa máscara no se filtra de una corrida a la siguiente.** Dos corridas
  seguidas, mismo largo y estamento opuesto: con el mismo largo la máscara vieja **alinea**
  y no revienta, sólo miente. Verificado por mutación: al romper la invalidación caen 12
  tests, entre ellos éste.

## [2.0.6] — 2026-09-22

Primeros tres arreglos de la **ronda de EFICIENCIA y REUSO** sobre `main` (CLAUDE.md
§12). Los tres son **equivalencias exactas**, no aproximaciones, y así se verificaron:
misma salida comparada fila a fila contra la implementación vieja antes de tocar nada.
Ningún número del REM cambia.

### Cambiado
- **`rem_utils.norm` 2,2x más rápida, con el mismo resultado.** Es la función más
  llamada del proyecto (una vez por CELDA en `encontrar_fila_encabezado`,
  `detectar_eje_filas`, `marcar_eventos` y en cada `.map(norm)` de los loaders pandas).
  Las 7 `str.replace` encadenadas de tildes pasaron a un `str.translate` con la tabla
  construida a nivel de módulo (una pasada en vez de siete, y sin rearmar el `zip()` en
  cada llamada), y el `re.sub` de espacios a un patrón compilado. Medido: 400k celdas
  de 0,47 s a 0,23 s. Verificada contra tildes, ñ, `\xa0` (el espacio duro que traen los
  exports copy-paste), `\r\v\f` y los caracteres cuya mayúscula cambia de largo o de
  forma (la ligadura fi, la i sin punto del turco).

  **Descartado en el camino: cachear `norm` con `lru_cache`.** Parecía el arreglo obvio
  (20x sobre columnas categóricas), pero **es más lenta sobre columnas de alta
  cardinalidad** — 0,36 s contra 0,24 s sobre 200k RUN distintos —, y justamente el RUN,
  el ATEN ID y los nombres de funcionario pasan por ahí en cada loader. Peor: la caché
  colisiona `1`/`1.0`/`True` y `0`/`False` (mismo hash, `str()` distinto), que es
  exactamente el bug que `clave_atencion` existe para evitar. Habría que meter el tipo
  en la clave y aun así perder en la mitad de los usos. No se hace.

- **`poblacion._estado_dx` ya no copia ni ordena 130 columnas para leer 5.** El frame
  del formulario trae `q<N>` y `q<N>_n` de cada una de las ~65 preguntas, y esta función
  corre 29 veces por pasada de `construir_poblacion` (más la pasada entera extra de
  `Brecha_Medico`, §8.6, con otras 44 llamadas). Ahora recorta a `RUN`/`FECHA`/`INSTR` +
  los subtipos pedidos ANTES del filtro y del `sort_values`. Es el mismo resultado:
  `sort_values` ordena por la clave `FECHA` sola (el orden de filas no depende de cuántas
  columnas cuelguen) y `groupby().last()` trabaja columna por columna — comparado contra
  la versión vieja en las 28 specs x `instrumento` True/False, con fechas llenas de
  empates a propósito, 0 diferencias.

  Medido: la parte que se tocó (selección + orden + agrupación) baja de 0,28 s a 0,04 s
  por 28 llamadas, **7x**. La función completa mejora ~30%, porque el costo dominante
  pasó a ser OTRO: las tres `str.contains` de las máscaras, que se recalculan por spec
  (0,44 s de las 0,63 s que quedan) e incluyen un `INSTR_n.str.contains("MEDIC")` que es
  **invariante entre las 28 specs**. Queda anotado, no hecho.

- **Los catálogos DEIS se consultan por índice, no barriendo la columna.**
  `catalogos._cruzar` comparaba `d["COD"] == c` sobre el catálogo entero Y recalculaba
  la máscara de rangos —que es **invariante**— en cada código; `anotar`, que es el uso
  previsto (la columna de diagnósticos de un export), lo llamaba dos veces por código.
  Ahora hay un índice `{COD: posiciones}` + las filas de rango, armado una vez por
  DataFrame cargado. Medido: `anotar` de 2000 códigos de 3,05 s a 0,61 s (**5x**); la
  consulta suelta, de 1,7 ms a ~0. Comparado contra la versión vieja en los **12.548
  códigos** de la Lista Tabular x los dos catálogos cruzados (25.096 consultas):
  0 diferencias.

### Agregado
- **Test de que el índice de catálogos se invalida.** El riesgo propio de un índice es
  quedarse viejo: tras un `usar_en_sesion` las consultas seguirían contestando con el
  catálogo anterior **calladas**, con la página diciendo «cargado a mano» (regla 2, el
  peor desenlace). Se invalida comparando por IDENTIDAD el DataFrame indexado, y el test
  lo amarra en las dos direcciones y sobre las dos mitades del índice (códigos exactos y
  rangos). Verificado por mutación: si se rompe la invalidación, el test falla.

- **Arneses archivados en
  [`docs/evanesced/eficiencia-2.0.6/`](docs/evanesced/eficiencia-2.0.6/)** (§0 regla 7):
  el benchmark antes/después y las dos pruebas de equivalencia, cada una con una copia
  textual de la implementación vieja adentro. Son la prueba de los números de acá arriba.

## [2.0.5] — 2026-09-21

### Corregido
- **El check de contadores ahora mira el README, no solo `CLAUDE.md`.** Era la causa de
  la deriva que se corrigió a mano en la 2.0.4: el README declaraba **311 pruebas
  cuando había 309**, y nada lo vigilaba. `PATRONES_TESTS` (una lista de patrones)
  pasó a ser **`CONTADORES`**, un mapa POR ARCHIVO donde cada patrón lleva la etiqueta
  de qué cuenta. De yapa entra el conteo de ARCHIVOS: el README dice «N pruebas en M
  archivos» y ahora las dos cifras se verifican. `--arreglar` las sincroniza solo, y el
  mensaje de error nombra el archivo real en vez de decir siempre «CLAUDE.md declara…».

- **Tres patrones muertos, sacados.** Al escribir el test de que cada patrón siga
  matcheando aparecieron tres que ya no matcheaban nada: `pruebas automáticas (N)`,
  `suite: N tests` y `**N tests** (§2.1`. Vigilaban frases del `CLAUDE.md` monolítico
  que desaparecieron cuando se partió por carpeta. **No fallaban: dejaron de vigilar**,
  en silencio, y daban confianza falsa — de los cuatro contadores que el check decía
  cuidar, sólo uno seguía vivo.

  Este es el modo de falla que hay que tener presente: un patrón que deja de matchear
  no se queja. Por eso el test nuevo exige que **cada** patrón encuentre su frase.

  **Lo que sigue SIN vigilar, a propósito:** `gui/CLAUDE.md` declara «**56 tests**»,
  pero es un SUBconteo (sólo los dos archivos de GUI), así que compararlo contra el
  total sería peor que no mirarlo. Queda anotado en `CONTADORES`.

- **`_sub_contador` reemplaza sólo su grupo.** El `--arreglar` viejo hacía
  `m.group(0).replace(m.group(1), n)`, y `str.replace` cambia TODAS las apariciones:
  con 16 tests en 16 archivos habría pisado las dos cifras. Ahora se reemplaza por
  posición del grupo.

### Agregado
- **Auditoría de los otros tres pre-commit, archivada en
  [`docs/evanesced/hooks_auditoria-2.0.5/`](docs/evanesced/hooks_auditoria-2.0.5/).**
  Si `check_version` tenía tres referencias muertas, la pregunta obvia es si los demás
  también. `auditar_hooks.py` verifica por AST que cada `archivo.py::funcion` nombrada a
  mano en `TRANSVERSALES` y `EXENTOS` de `check_fuentes` siga existiendo (**0 de 20
  muertas**); `probar_hooks.py` le da a cada check un positivo y confirma que lo caza —
  el anti-RUT caza un DV válido y deja pasar el `11111111-1`, cp1252 caza la flecha
  Unicode, `check_fuentes` detecta por AST el lector sin contrato. **Los tres están
  sanos.**

  Único pendiente que dejó: `check_fuentes --todo` avisa que `rem_utils.cargar_maestro`
  tiene el contrato con **encabezado sintético** y pide el export real recortado a solo
  encabezado (skill `limpiar-refs`). No bloquea.

- **`docs/evanesced/CLAUDE.md`** — las reglas de la carpeta, separadas del README (que
  dice *qué hay*): no reescribir lo archivado, no borrarlo, no hacerlo pasar los checks
  (está excluido de cp1252 a propósito, y un `# Version:` ahí bloquearía el commit), y
  que archivar se anota en este CHANGELOG y **no** en el README de la raíz, que es para
  quien usa el `.exe`.

- **`tests/test_check_version.py`** (12 pruebas): que cada patrón siga matcheando su
  archivo, que sean específicos (no cazan versiones, segundos ni leyes del README —
  un falso positivo en el pre-commit bloquea commits sanos), que `_sub_contador` no
  pise cifras vecinas y sea idempotente, y que el repo de hoy esté sincronizado.

## [2.0.4] — 2026-09-21

### Agregado
- **«¿Qué ventajas tiene sobre el REM automático de RAYEN?» — en el README y en la
  pantalla de Inicio.** Cinco puntos: 100% offline, trazabilidad (la lista de RUT de
  cada reporte), transparencia (código abierto), apoyo a la gestión (los reportes de
  auditoría) y criterios explícitos.

  **Las cinco afirmaciones se verificaron antes de escribirlas**, porque una ventaja
  falsa en un README público es peor que no tenerla: la de trazabilidad se apoya en que
  los siete módulos dejan el RUT/RUN en la salida — el A05 marca el export completo (la
  columna RUT abre su hoja, `rem_saludmental.ANCHOS_BASE`) y el resto escribe su hoja
  `*_Detalle`. Si un módulo nuevo NO deja detalle por paciente, la frase deja de ser
  cierta y hay que corregirla en los dos lugares; queda dicho en el comentario de
  `_VENTAJAS`.

### Cambiado
- **La descripción de Inicio ya no repite el «100% local».** Lo decía en dos líneas
  justo encima de la caja nueva, que abre con el mismo punto. Quedó solo con lo que el
  bullet no cubre: que la PII se procesa en memoria sin guardar copia, y que sin
  conexión no hay actualización automática (se revisa a mano en «Acerca de»).

## [2.0.3] - 2026-09-20

### Agregado
- **`tools/correr_tests.py` — la suite completa en 3 procesos: 194 s -> 103 s.** Reparto
  LPT, un archivo de tests por proceso, sin dependencias nuevas (`subprocess` + `heapq`).
  No reemplaza a `pytest`: para depurar un test suelto se sigue usando pytest directo,
  que da el traceback ordenado. Esto es para la pasada completa.

  **Por que por ARCHIVO y no con `pytest-xdist -n auto`.** La culpa de todo es Tk:
  `test_gui_construccion.py` abre la ventana de verdad, se lleva 90 s de los 191 s de la
  suite y **no se paraleliza** -- dos procesos Tk en Windows se frenan entre si. Medido,
  ese archivo tarda 74 s solo y 96 / 102 / 109 s con 1 / 2 / 3 procesos compitiendo, asi
  que el wall es `max(gui_penalizada(N), resto / (N-1))`. Esa formula predice las
  corridas reales (N=2 -> 106 s, N=3 -> 103 s, N=4 -> 110 s) y deja dos conclusiones:
  mas procesos **no** es mejor pasado N=3, y hay que meter TODO Tk en UN proceso.
  Repartir por test suelto, que es lo que hace `-n auto`, esparce los tests de Tk entre
  todos los workers: es justo el caso malo, y medido dio peor que por archivo. Si algun
  dia se instala xdist, el equivalente honesto es `--dist loadfile`.

  El piso duro son esos 74 s de la GUI sola: **no hay reparto que lo baje**. Para ganar
  mas hay que hacer la GUI mas barata -- lo que ya empezo la 2.0.2 (la GUI bajo de 106 s
  a 90 s pese a sumar 5 tests) --, no sumar procesos.

  Los numeros medidos viven en el docstring del script, y `PESOS` (el costo de cada
  archivo) solo ORDENA el reparto: un archivo que no este ahi entra con un peso por
  defecto y el reparto sigue funcionando. No hay que mantenerlo al dia para que corra,
  solo para que reparta bien.

## [2.0.2] — 2026-09-20

### Corregido
- **Las páginas se pintaban a medio construir.** `_construir_pagina` grideaba su frame
  ANTES de crear los hijos, y customtkinter llama `update_idletasks()` al crear cada
  widget (~100 veces por página, medido con `cProfile`): la página a medio armar se
  dibujaba encima de la que estaba a la vista. Con la construcción perezosa casi no se
  notaba — era la página que ibas a ver igual —, pero al precargar varias se volvía un
  parpadeo seguido. Ahora el frame se arma **sin gridear** y lo mapea `mostrar`, que igual
  lo iba a hacer. Amarrado con un test que verifica el invariante fuerte: una página
  recién construida **no tiene geometry manager**.

### Agregado
- **Precarga incremental de páginas, con barra al pie** — implementada y con tests, pero
  **APAGADA por defecto** (`App(precargar=False)`).

  **Por qué entra apagada, dicho derecho:** funciona, pero hoy **empeora** el arranque. La
  precarga no crea el problema de fondo, lo junta y lo hace visible: construir una página
  bloquea el hilo de la GUI entre 1 y 7 segundos, y mientras tanto Windows no puede
  repintar la ventana, así que se ve rota (sin sidebar, con el texto del Inicio a medio
  dibujar). Probado por el autor en el `.exe` y con `python -m gui.app`: el mismo
  resultado, o sea no es empaquetado. Se enciende cuando `_construir_pagina` ceda el
  control entre paso y paso — ver el §12 de `CLAUDE.md`, «Destrabar la GUI durante la
  carga de una página», que lleva las mediciones y el plan.

  Lo que queda listo para ese día: `App._precargar_iniciar` / `_precargar_tick` /
  `_precargar_terminar` / `_precargar_cancelar`, `widgets.barra_precarga`, y cinco tests
  (que las páginas precargadas no queden **mapeadas** — si no, vuelve el bug del Tab de
  la ronda 12 —, que cerrar cancele el tick pendiente, y que la barra diga qué página va).

### Medido (queda escrito para no re-derivarlo)
- **Bloqueo al construir cada página**, con `mainloop` real: `acerca_de` **7105 ms** ·
  `sm_actividades` 5753 · `a23_respiratorio` 1813 · `a05` 1090 · `sp_p6_poblacion` 1031 ·
  `inicio` 89.
- **El costo es Tk puro, no I/O ni imports:** `sm_actividades` = 7,1 s de 8,4 en
  `_tkinter.tkapp.call` (101.700 llamadas); `acerca_de` = 6,1 s de 7,1 (76.181). Por eso
  **ningún hilo lo arregla** — no hay trabajo puro que mandar afuera, y los widgets de Tk
  solo existen en el hilo del `mainloop`. Se evaluó y se descartó con el perfil en la mano,
  no de oídas.
- `acerca_de` es la página **más cara** y es una **página especial**: no está en `registro`,
  así que la precarga ni siquiera la cubría.

Arneses archivados en `docs/evanesced/gui-2.0_merge/` (`perfilar_sm.py`,
`perfilar_about.py`, `medir_cambio_pagina.py`, `medir_precarga_real.py`).

## [2.0.1] — 2026-09-20 · hotfix de empaquetado

### Corregido
- **El `.exe` de la 2.0.0 nacía sin ninguna página** («Hydra», la 4ª cabeza del cero
  callado). `autoREM.spec` llama a `collect_submodules('gui.paginas')`, que necesita
  poder **importar** el paquete; y el comando documentado en el README,
  `pyinstaller --clean autoREM.spec`, **no pone la raíz del repo en `sys.path`**
  (el script de consola no lo hace; `python -m PyInstaller` sí). Sin eso
  `collect_submodules` devuelve **`[]` sin quejarse**: el build termina OK, el exe pesa
  126 KB menos, y recién al abrirlo muere con `RuntimeError: gui/paginas/ no expuso
  ninguna PANTALLA`. Medido:

  ```
  con la raiz en sys.path -> ['gui.paginas', 'gui.paginas.a05', ... 6 paginas]
  sin la raiz en sys.path -> []
  ```

  Dos arreglos, porque uno solo deja la trampa viva:
  1. El `.spec` se pone **a sí mismo** en `sys.path` (`SPECPATH`), así da igual cómo se
     invoque a PyInstaller; y `pathex` apunta ahí.
  2. **Fail loud:** si `collect_submodules` vuelve vacío, el `.spec` aborta el build con
     `SystemExit` explicando qué pasó. Un build que «funciona» y pare un exe roto es
     peor que uno que no compila (CLAUDE.md regla 2).

  **Por qué no lo cazó la validación de la 2.0.0:** se compiló con
  `python -m PyInstaller autoREM.spec`, que no es el comando del README — y es
  justamente el único que esconde el problema. El guardarraíl de `gui/registro.py` sí
  hizo su trabajo: el error nombró `collect_submodules('gui.paginas')` y el `.spec`.

## [2.0.0] — 2026-09-20

**La GUI 2.0 pasa a ser LA GUI.** Es el merge de la rama `gui-2.0` a `main`: el paso 11
del plan ([docs/GUI_2.0_plan.md](docs/GUI_2.0_plan.md) §12). `X` por CLAUDE.md §9 —
cambio grande de arquitectura de la interfaz.

### Cambiado
- **`autorem.py` ya no dibuja nada.** Pasa de 1571 a ~250 líneas: quedan el registro
  de tareas del A05, la orquestación compartida `_correr_tareas` / `_resumen_texto`
  (la usan la GUI y el CLI) y el **CLI**, que sigue CONGELADO (§12). `main()` lanza
  `gui.app.lanzar(ruta_inicial)`.
  - El `import` de `gui.app` va a **nivel de módulo** a propósito. Todos los demás
    imports de `autorem.py` son locales a su función, y PyInstaller solo ve los
    estáticos: con el import adentro de `main()`, el exe congelado moría con
    `ModuleNotFoundError: gui.app` **con el `.spec` ya «arreglado»**.
  - Con eso se cierra el **hallazgo #14** de la revisión: `gui/runner.py` duplicaba
    nueve helpers de `autorem.py` (`_valida_ruta`, `_manejar_error`, `_Reloj`,
    `_correr_con_reloj`, `_dir_salida_default`…) y ya habían divergido. Queda una sola
    copia, la que usa la GUI 2.0.
- **La GUI 1.x queda congelada** en `legacy/autorem_gui_tk_1.9.18.py.gz` (plan §8),
  con su `legacy/README.md`: comprimida para que ninguna herramienta del repo la
  escanee, y no se descomprime «para arreglarla». **Necesitó whitelist en el
  `.gitignore`**: el plan daba por hecho que un `.py.gz` no matcheaba, y `*.gz` está
  ignorado en bloque desde siempre.
- La pestaña **A03 standalone desaparece**: el A03·D.3 vive solo dentro de SM
  Actividades. El **selector IRIS/Administrativo** se reemplazó por detección +
  confirmación (plan §5).

### Corregido
Tres números mal, los tres de la misma familia: la forma canónica de las atenciones
(`_una_fila_por_atencion`, ronda 12) cambió el significado de la celda `ACTIVIDADES`
y hay código que la seguía leyendo como si fuera UNA actividad.

- **Máscaras multi-token evaluadas sobre la celda unida** (`rem_utils.por_actividad`,
  nuevo). Una máscara cuyos tokens parten el nombre de **una sola** actividad
  («controles» + «salud mental por» = «Controles DE Salud Mental POR llamadas
  telefónicas») se satisfacía con un token de cada actividad de la atención. Afectaba
  a **A32·F1 y A32·F2, que SÍ tributan al REM**, en las dos direcciones:
  - falso POSITIVO: `Controles de pie diabético; Consulta de salud mental por
    psicólogo; Consulta de morbilidad por llamada telefónica` daba A32·F2, sin que
    existiera ningún control remoto de SM;
  - falso NEGATIVO: `Controles de Salud Mental por llamadas telefónicas; Acciones
    remotas de salud mental por videollamada` perdía su A32·F2-Llamadas, porque el
    `~videollamada` leía la palabra en la actividad HERMANA.

    El mismo defecto estaba en `_mask_control_sm` del Trabajo Perdido, donde metía
    atenciones inventadas en la auditoría `Ctrl_sin_Formulario`. La regla, ahora
    escrita: si los tokens describen UNA actividad, la máscara va `por_actividad`; si
    describen actividades DISTINTAS (los indicadores del A23), la celda unida es
    justamente lo que se quiere.
- **El centinela de grupo de `_una_fila_por_atencion` llevaba un byte NUL**
  (`'\x00fila{i}'`), y el `groupby` de pandas hashea el string HASTA el NUL (medido en
  2.3.3): **todas** las atenciones de una sola actividad caían en el MISMO grupo y se
  fusionaban en una, con las actividades de pacientes distintos juntas. Solo mordía en
  un export MIXTO — alguna atención de 2+ actividades y el resto de una —, que es la
  forma del **Monitoreo admin real**; sin ninguna multilínea la función sale antes, y
  por eso los tests de dos filas no lo veían. La clave del grupo ahora es NUMÉRICA:
  no hay centinela que inventar.
- **El ATEN ID numérico de IRIS** (`683016530` / `683016530.0` según la celda) partía
  una atención en dos al agrupar. La normalización que 1.9.16 había hecho dentro del
  Trabajo Perdido sube a la forma canónica, donde vive la identidad de la atención:
  `rem_utils.clave_atencion`.

### Cambiado (Trabajo Perdido)
- **`auditar_atenciones` (1.9.16) se adapta a la forma canónica**, no al revés
  (decisión del autor): sobre el frame canónico cada fila YA es una atención, así que
  `_aten_id`, el `groupby("id").any()` y el `groupby("aten_id").agg(...)` del detalle
  se reducen a máscaras por fila y una proyección. Mismo movimiento que §1.M.2 de la
  revisión, que borró `a23._act_de_la_atencion` por la misma razón. El detalle de
  actividades usa `SEP_ACTIVIDADES` y no el `" | "` propio que traía.

### Agregado (tests)
- **Los dos formatos dan lo mismo**: `test_las_auditorias_dan_lo_mismo_desde_iris_que_desde_el_monitoreo`
  — la misma atención escrita como IRIS y como Monitoreo tiene que dar la misma fila.
  Es el test que habría cazado solo el choque de este merge.
- `test_control_sm_no_se_arma_con_tokens_de_dos_actividades`,
  `test_a32_no_se_arma_con_tokens_de_actividades_distintas` (las dos direcciones) y
  `test_monitoreo_mixto_no_fusiona_las_atenciones_de_una_sola_actividad`. Los tres se
  verificaron contra el código viejo: los tres fallan sin su arreglo.

### Documentación
- `CLAUDE.md` §2, §9 y §12 (la GUI 2.0 sale de «en curso»); `modulos/CLAUDE.md`;
  `docs/GUI_2.0_plan.md` §9.1 (la tabla-compuerta de port entera en «sí») y §11 (decía
  «la GUI no tiene cobertura» con 51 tests de GUI escritos).
- El registro de la revisión, `docs/review_gui-2.0_pendiente.md`, **se conserva** con
  su header de cierre (regla 7): lo citan el CHANGELOG 11 veces, `CLAUDE.md` y la
  skill `tests-fuentes`.
- `tools/check_version.py` (decía 1.9.10) y `tools/slim_maestro.py` (1.9.15) suben a
  la versión del merge: sus headers apuntaban a un release ANTERIOR a su contenido.

## [1.9.18] — 2026-09-20

Los tres commits que `main` sumó después de la 1.9.16 y que no tenían entrada.
Es la última versión que shippeó la GUI 1.x.

### Agregado
- **Plan de la auditoría de actividades habilitadas por funcionario** (SA -> RAYEN):
  [docs/actividades_profesionales_plan.md](docs/actividades_profesionales_plan.md),
  más su fila en el roadmap de `CLAUDE.md`.
- **`refs_tablas/Informe_Actividades_Profesionales_heads.xlsx`** (solo IRIS),
  recortado a banner + encabezado y con su whitelist por archivo. El crudo trae
  nombres y RUT de funcionarios: nunca al repo.

## [1.9.17] — 2026-09-17

### Corregido
- **GUI 2.0, trampas de Tk/customtkinter/hilos** (`docs/review_gui-2.0_pendiente.md` §1.G,
  ronda 6):
  - **Dos ventanas de dotación anidadas, y la de afuera pisaba lo guardado en la de
    adentro.** `ctk.CTkToplevel(root)` hace un `update()` COMPLETO dentro de su propio
    constructor en Windows (repinta la barra de título), así que abrir el diálogo de
    dotación despachaba todos los clicks encolados mientras la ventana estaba congelada
    cargando el ADA: el mismo agujero que `update_idletasks()` había cerrado, reabierto
    por la librería. Un «Revisar dotación…» impaciente se abría ANIDADO con su propia
    copia de la tabla, y el «Aplicar» de afuera (`dotacion.guardar` escribe el dict
    entero) revertía lo guardado adentro. Además, la corrida usaba la tabla vieja → un
    externo contado como interno: doble conteo en el REM. Nuevo candado
    `dialogos._DOTACION_ABIERTA`: una sola ventana de dotación a la vez.
  - **Con Windows escalado (125-150%) los textos largos se cortaban por la derecha**
    (instrucciones, avisos, el mensaje del banner de fuente). `etiqueta_envolvente` le
    pasaba a `CTkLabel` un ancho ya escalado, y CTk lo volvía a escalar: al 150% el texto
    pedía 787 px en una caja de 570.
  - **El banner de fuente describía una corrida cuyos archivos se habían cambiado mientras
    corría** (verde «IRIS completo» junto a un Monitoreo recién elegido). Durante la
    corrida solo se deshabilita Procesar; ahora `on_procesar` compara los inputs con los
    del arranque antes de pintar, y lo dice en el log.
  - **El preview de cruce ADA↔Grupal del SM pintaba el hilo que terminara ÚLTIMO**, no el
    de la última elección; y «Quitar» apagaba el banner pero el hilo en vuelo lo volvía a
    encender sobre una casilla vacía. Era el gemelo de la carrera que ya se había cerrado
    en el A05. Nuevo `runner.Canal` (`en_hilo(..., canal=)`): solo pinta el pedido
    vigente.
  - **Un paso opcional que fallaba (A03·D.3, Trabajo Perdido, Rescate) solo se decía en
    el log**: el «Listo» callaba, y el archivo de una corrida ANTERIOR del mismo mes
    seguía en la carpeta con el mismo nombre, listo para copiarse al REM. Ahora el
    resumen dice «NO se generó (motivo)», y las salidas ya no se pisan (ver «Cambiado»).
  - **Cerrar la ventana con una corrida en curso la mataba sin avisar**, incluso a mitad
    de escribir el `.xlsx` (el worker es un hilo daemon: muere con el proceso). Ahora la
    X pregunta si hay una corrida viva («No» por defecto), y toda salida se escribe a un
    temporal que se renombra al terminar (`rem_utils.escribir_atomico`): un corte deja un
    `….escribiendo.xlsx`, nunca un resultado roto con nombre de resultado.
  - **`verificar_hoja_unica` dejaba el export bloqueado si la lectura reventaba**
    (read_only mantiene el archivo abierto hasta `close()`, y ese `close()` no estaba en
    un `finally`): un export a medio sincronizar por OneDrive quedaba tomado mientras el
    diálogo de error seguía abierto.
  - **El caché de usuario (`~/.autorem`: dotación y estamentos) fallaba CALLADO**, y
    en la dotación eso cambia cifras del REM. Un guardado que no llegaba al disco solo
    se decía con un `print` (invisible en el exe), y el mes siguiente se volvía a
    preguntar todo con «interno» por defecto. Peor: un caché DAÑADO se leía como tabla
    vacía, así que todos los externos volvían a contar sin que nadie se enterara. Nuevo
    manejo compartido (`rem_utils.leer_cache_json` / `guardar_cache_json`):
    - todo problema se MUESTRA en un diálogo al cerrar la fase que lo tocó
      (`runner.avisar_cache`), diciendo qué se pierde en términos del REM;
    - un caché dañado se aparta como `….corrupto-<fecha>.json` en vez de leerse vacío o
      pisarse;
    - uno que existe pero no se puede leer NUNCA se sobreescribe (se perdería entero);
    - un bloqueo pasajero (antivirus, indexador) se reintenta;
    - se escribe vía temporal + rename;
    - cada «Aplicar» guarda solo SUS cambios sobre lo que hay en disco
      (`dotacion._persistir`), así dos ventanas de autoREM ya no se revierten entre sí.

    A propósito NO cae a otra carpeta si esta falla: partiría la tabla en dos y el veto
    volvería en silencio a lo de antes. «Acerca de» tiene una sección nueva,
    «Preferencias guardadas» (dónde está, si se puede escribir, qué guarda, qué hacer),
    y las cajas de Dotación y Estamentos dejan una línea que apunta ahí.
  - **Los tests pisaban el `~/.autorem/dotacion.json` REAL en cada corrida.**
    `test_externos_delta_y_detalle_conserva_filas` guardaba sin redirigir el caché y
    corría (orden alfabético) antes del único test que lo redirigía: en un PC de trabajo
    eso borraba la clasificación de externos del CESFAM. Ahora todo `tests/test_*.py`
    importa primero `tests/_aislar_cache.py`, y un test exige que ninguno lo olvide.
- **GUI 2.0, envoltorios e indirecciones** (`docs/review_gui-2.0_pendiente.md` §1.H,
  ronda 7):
  - **«Aplicar» de «Precargar» y «Revisar dotación» reescribía la foto vieja.** Los dos
    diálogos muestran gente YA clasificada y le mandaban a `dotacion.marcar` TODOS los
    ticks, así que el re-leer-y-fusionar de `_persistir` (arriba) no servía: si otra
    ventana de autoREM había marcado externo a alguien mientras tanto, este «Aplicar» lo
    devolvía a interno sin que nadie lo tocara, y sus atenciones volvían a contar en el
    REM. Ahora se manda solo lo que cambió (`dialogos.decisiones_cambiadas`); un nombre
    nuevo sin tick sí se guarda, como interno.
  - **El catálogo DEIS cargado a mano en «Acerca de» no lo veía ninguna consulta.**
    Quedaba en el caché bajo su propia clave `(nombre, ruta)`, y toda consulta llama
    `catalogos.cargar(nombre)` sin ruta → seguía leyendo el embebido, con la página
    diciendo «cargado a mano» (y prometiendo que se usaría al conectar los catálogos,
    CLAUDE.md §12). «Volver al embebido» tampoco volvía nada. Ahora el elegido para la
    sesión es un paso de la cascada (`catalogos.usar_en_sesion`), solo en memoria. De
    paso: un `entrada=` que no existe ya no cae CALLADO al embebido (otra edición), falla.
- **GUI 2.0, reuso** (`docs/review_gui-2.0_pendiente.md` §1.I, ronda 8): código nuevo
  que copiaba a mano algo que ya existía, y en 3 de 5 casos la copia ya se había apartado.
  - **El Maestro slim en `<exe>/catalogos/` se ignoraba.** La GUI 1.x y la 2.0 tenían
    cada una su lista de dónde buscarlo, y ninguna miraba donde van los drop-in de los
    otros catálogos: el Trabajo Perdido caía callado a la heurística y «Acerca de» decía
    «no encontrado». Ahora las dos le preguntan a `catalogos.maestro_slim`, que busca en
    las mismas carpetas que cie10/eno/ges.
  - **La ruta de «Utilización de Cupos» no se validaba.** Mal tecleada, reventaba al
    final de la corrida de SM, con SM y TP ya escritos y la D.3 perdida. Ahora `preparar`
    la valida antes del worker, y esa caja y la de carpeta de salida limpian comillas con
    `runner.limpiar_ruta` en vez de una copia a mano.
  - **«Revisar dotación…» callaba el aborto** cuando ya había otra ventana de dotación
    abierta (Precargar sí lo decía): un solo candado `_una_ventana_dotacion` para las
    dos, y la ventana y la barra Aplicar de los dos diálogos salen de un solo lugar.
  - Sin efecto visible hoy, pero ya no pueden apartarse: la caja Período del A05 usa
    `widgets.selector_mes` (tenía su propia copia de los Spinbox y del parseo, fuera del
    test que amarra los años), y el preview de cruce ADA↔Grupal elige el encabezado con
    `rem_utils.indice_encabezado`, el mismo criterio de `leer_xlsx` (`primeras_filas`
    reemplaza tres copias de abrir-leer-cerrar).
- **GUI 2.0, bug recurrente «vacío TRAS un filtro»** (`docs/review_gui-2.0_pendiente.md`
  §1.J, ronda 9): la variante de c38a8cc que §1.A no cubría. El export trae filas, pero
  ninguna sobrevive al corte, al filtro de programa o al parseo de fecha, y el
  resultado sale en 0 con «Listo».
  - **Sección G del A23 en 0 sin fecha de nacimiento.** Un paciente sin FECHA DE
    NACIMIENTO legible en «Otros Crónicos» se descartaba callado, y sin la columna la G
    entera daba «ninguno». Ahora la edad sale del ADA si falta, y si tampoco está se usa
    el umbral de ≥2 años con un aviso REVISAR.
  - **Población con un formulario o ADA que no sirve para el corte.** Todas las filas
    posteriores al mes reportado, o ninguna fecha legible → antes ¿Ingresado? o ¿Activo
    12m? = NO para todos, sin aviso; ahora `ArchivoInvalido` (`mes_vacio` / `sin_fecha`).
    Y el resumen de la página muestra los avisos de cobertura, que antes quedaban solo en
    el log y la LEEME.
  - **SM Actividades con el mes cubierto pero NADA de SM** (ADA filtrado por otro
    programa) → todo el REM SM en 0; ahora `sin_datos`. Y una ASISTE del grupal en
    blanco o con otro valor ya no se lee como «nadie asistió»: toda la columna así es
    `sin_datos`, algunas filas dan un aviso SUBCONTADO.
  - **«Otros Crónicos» con fechas ilegibles** ya no queda NaT callado (`fecha_col`, que
    las cuenta en el log); sin ninguna legible, `sin_fecha`.
  - El diálogo de dotación ya no dice «sin funcionarios nuevos que clasificar» cuando
    en realidad nada del mes tributa al REM, ni cuando lo que tributa no trae FUNCIONARIO.
  - **Segunda pasada, sin tope:**
    - **A03·D.3 en 0 con «N aplicaciones»:** si ninguna aplicación trae momento
      Ingreso/Egreso, ahora es `ArchivoInvalido`; si solo algunas, aviso SUBCONTADO.
    - **A03 sin puntaje:** la aplicación va al D.3 con el resultado de RAYEN, con aviso
      REVISAR, en vez de quedar fuera callada.
    - **Población con encabezados de preguntas renombrados:** si faltan todas, antes
      daba 0 ingresados y ahora es `sin_columnas`; si faltan algunas, aviso por archivo.
    - **Población con un ADA sin ninguna actividad SM en 13 meses:** ahora `sin_datos`.
    - **A23 con un mes sin nada respiratorio:** los 27 indicadores ya no salen en NO con
      «Listo»; ahora `sin_datos`.
    - **«Otros Crónicos» sin INSTRUMENTO:** columna requerida. Si ningún formulario lo
      aplicó un médico, aviso EN 0 (SALA y la Sección G cuentan solo esos).
    - **Filas sin sexo Hombre/Mujer o sin edad** cuentan en Ambos pero en ninguna
      columna por sexo o edad: ahora hay aviso REVISAR, en SM y en el D.3
      (`rem_utils.aviso_fuera_de_grid`).
    - **Un Maestro que no reconoce ninguna actividad del mes** ahora avisa HEURISTICA
      igual que la falta de Maestro.
- **Contratos de fuentes, al commitear** (`tools/check_fuentes.py` +
  `tests/contratos_fuentes.py` + skill `tests-fuentes`). Las 10 rondas de revisión de
  esta rama cazaron a mano, y siempre después, el mismo bug: un export que pasa el
  loader y da un 0 plausible o un crash críptico. Ahora cada función que lee una
  planilla del usuario tiene un contrato que la ataca con el encabezado REAL de
  `refs_tablas/`: 0 filas, columna crítica renombrada, clave vacía, fechas ilegibles,
  y una columna extra al inicio (caza el índice fijo, como la col 11 del A05). El
  pre-commit corre solo los contratos de lo que el commit toca, y **bloquea** un lector
  nuevo o cambiado sin contrato. Arrancó con 11 contratos y la ronda 11 lo dejó en 18:
  **todo lector de planillas del proyecto tiene contrato**, y todos corren contra el
  export real salvo el Maestro `.xlsx` (no se versiona). Los 3 pendientes que dejó a la
  vista se cerraron en la ronda 11 (ver abajo): el grupal «sin ASISTE» era una
  referencia editada a mano, y el RUN vacío en todas las filas ya falla.
- **GUI 2.0, ronda 11: cada referencia y cada fallback contra el export REAL**
  (`docs/review_gui-2.0_pendiente.md` §1.L). Llegaron los exports que faltaban (NSP,
  Otros Crónicos IRIS y Admin, Estratificación, Utilización de Cupos, Monitoreo
  Multiprofesional, Monitoreo de Inasistentes) y se re-bajaron el grupal y los
  formularios IRIS de SM y Goldberg, ahora **con su banner**.
  - **El A05 y el P6 aceptaban un cuestionario como formulario de Salud Mental.** Un
    Goldberg o un PSC traen las mismas firmas IRIS/Admin y su «1.- ESTADO» dice Ingreso:
    el A05 contaba ingresos con patología «Estado», y el P6 leía el ítem 3 de Goldberg
    como Violencia. Ahora el formulario se reconoce por CONTENIDO
    (`rem_saludmental.verificar_formulario_sm`: cada número de pregunta que se usa contra
    lo que su encabezado dice, verificado en los dos formatos reales): un cuestionario u
    otro formulario es `no_formulario_sm`, y un formulario SM **renumerado** por RAYEN, que
    antes cruzaba los diagnósticos en silencio, es `formulario_cambiado`.
  - **Sin fallbacks posicionales para el encabezado.** `encontrar_fila_encabezado`
    caía a «la fila siguiente a la primera con la columna A vacía» y a una fila fija (16
    en IRIS, 8 en el Administrativo): los dos devolvían una fila de DATOS como encabezado.
    Ahora sin ancla es `sin_encabezado`. De paso: el IRIS de formularios SÍ trae banner
    (15 filas); las referencias no lo mostraban porque se habían recortado a mano.
  - **El RUN del Monitoreo se heredaba con un ffill global**, sin mirar el formato ni la
    atención: en IRIS una fila sin RUN quedaba atribuida al paciente de la fila de arriba.
    Ahora se hereda solo dentro del mismo ATENID (el `N°` del Monitoreo se repite en las
    filas hijas), y una fila sin RUN ni atención de la cual heredarlo se loguea.
  - **A23 en el Monitoreo: 6 indicadores en NO callados** (Autocuidado, Inhaloterapia,
    Otras, Educación Integral, Antitabaco, Vida Saludable). Piden dos actividades en la
    MISMA atención y se comparaban fila por fila; en el Monitoreo cada actividad es una
    fila. Ahora miran la atención entera (`_act_de_la_atencion`).
  - **3 de las 7 actividades del «Activo 12m» no existían en el Maestro** (venían del
    DAX: «…con **patología** de salud mental», etc.). Quien solo tenía esas visitas salía
    no activo y caía al rescate. Se cambiaron por los nombres reales (la de demencia, en
    consulta con el autor), y un test exige ahora que **todo** literal de actividad de SM,
    A23, Población y Trabajo Perdido calce con alguna actividad del Maestro.
  - **Estratificación: el fallback a «CONDICIONES CRONICAS» caía en «Cantidad de
    Condiciones Crónicas»**, un conteo, y la SALA quedaba sin diagnósticos. Se sacó.
  - **RUN/ATEN ID vacío en todas las filas** ahora falla en el ADA/Monitoreo, Otros
    Crónicos, Estratificación, Inscritos (TRANS) y Monitoreo Multiprofesional.
  - **`tools/limpiar_refs.py`**: no arrancaba en el Python del proyecto (3.9: `int |
    None` sin `from __future__`), partía los encabezados de dos pisos (Utilización de
    Cupos), no abría un export con una imagen rota adentro (Otros Crónicos IRIS) y
    guardaba el original editado, con lo que no son celdas (caché de tablas dinámicas,
    comentarios, propiedades). Ahora arma un libro nuevo con **banner + encabezado** y lo
    escanea antes de escribirlo: con un RUT, correo o teléfono, no lo escribe.
  - **Decisiones del autor sobre lo que quedó abierto:**
    - La VDI del **PADDS con demencia cuenta para «Activo 12m»** (y sigue fuera del
      Trabajo Perdido de SM: tributa al REM del PADDS).
    - **El A23 acepta el Otros Crónicos y el NSP Administrativos.** El Otros Crónicos
      admin no trae INSTRUMENTO: el estamento sale del nombre del funcionario (export de
      atenciones + caché de estamentos), con aviso por los que no se resuelven y
      `sin_estamento` si no se resuelve ninguno. El NSP admin («Monitoreo de
      Inasistentes») trae `RUN` / `FECHA CITA` / `EDAD` en texto.
    - **Un archivo opcional que no sirve pregunta «¿continuar sin él?»** (Estratificación,
      NSP, Inscritos para TRANS, Multiprofesional, Maestro cargado a mano). Si sí, se
      re-corre sin él y la hoja LEEME lo marca `OMITIDO`. Antes TRANS y el
      Multiprofesional inválidos quedaban solo en el log.
- **GUI 2.0, ronda 12: altitud — cada arreglo, a la altura donde vive la causa**
  (`docs/review_gui-2.0_pendiente.md` §1.M). Once arreglos de las rondas anteriores
  estaban puestos un nivel más abajo de donde correspondía: emparchaban al consumidor y
  dejaban la misma clase abierta para el resto.
  - **La guarda de «columna clave vacía en TODAS las filas» estaba escrita a mano en seis
    loaders, y en dos de ellos sobre el DataFrame ya CONCATENADO.** Un año con el RUN
    entero en blanco, cargado junto a uno bueno, pasaba sin decir nada: sus formularios
    quedaban sin paciente y la **Sección G contaba como inasistente a quien SÍ se había
    controlado** (y en el A23 las atenciones de ese archivo se juntaban bajo un paciente
    fantasma). Ahora es un parámetro del cuello de botella (`cargar_canonico(...,
    no_vacias=)`), POR ARCHIVO y nombrándolo, y el arnés de contratos lo ataca también
    con dos archivos (`C4b`).
  - **La forma PADRE-HIJO del Monitoreo se normalizaba a medias.** El relleno de la
    cabecera vivía en el loader y el AND entre actividades en UN consumidor (el A23), así
    que los demás seguían viendo una fila por actividad: el **Trabajo Perdido marcaba
    «saco roto» una actividad cuya hermana de la misma atención SÍ tributaba** (0 desde
    IRIS, 1 desde el Monitoreo, con los mismos datos) y contaba actividades donde su tabla
    dice «atenciones»; la evidencia del diálogo de dotación inflaba `n_atenciones`. Ahora
    `cargar_atenciones` entrega **una fila por atención en los dos formatos**, y ATEN ID
    es requerida (sin ella el `drop_duplicates` del SM dejaba UNA fila por casilla). Si el
    mismo ATEN ID aparece con pacientes distintos, falla: no identifica una atención.
  - **Los cuatro opcionales que no pasaban por `cargar_canonico`** (Inscritos para TRANS,
    Multiprofesional, Estratificación y el Maestro `.xlsx`) señalaban «este archivo no
    sirve» con `ValueError` y no envolvían el archivo ilegible, así que el clásico
    .html/.xls disfrazado de `.xlsx` **tumbaba la corrida entera** en vez de preguntar
    «¿seguir sin él?» — y `opcional()` tenía que atrapar `ValueError`, con lo que
    cualquier bug de código dentro del bloque se le presentaba al usuario como «tu archivo
    opcional no sirve». Los cuatro pasan por el cuello de botella, levantan
    `ArchivoInvalido` y `opcional()` solo convierte eso.
  - **Los opcionales se cargan PRIMERO** (A23 y SM). La pregunta «¿seguir sin él?» llegaba
    después de la corrida completa (el NSP se leía al final, con SALA y la Sección G ya
    calculadas) y el «Sí» repetía todo desde cero.
  - **El Maestro cargado a mano se abría DOS veces** (8,6 MB, ~12 s cada una): la página lo
    validaba y botaba el resultado para que el Trabajo Perdido lo volviera a leer. Ahora
    `tpmod.procesar(..., dfm=)`, gemelo del `d=` del ADA, y el aviso `OMITIDO` llega
    también a la LEEME del TP, que es el reporte que usa el Maestro.
  - **El A05 confiaba en una detección de formato cacheada por NOMBRE de archivo**, y bajo
    el mismo nombre el contenido cambia todo el tiempo (RAYEN baja todo como
    `Formulario_Rayen.xlsx`; OneDrive entrega el `.xlsx` a medio bajar): un archivo elegido
    a medio sincronizar dejaba cacheado un «no es un .xlsx» que **se repetía en cada
    Procesar** aunque ya estuviera completo, y un IRIS reemplazado por el Administrativo
    se procesaba con el perfil viejo, sin pedir el acuse y reventando con «Cambia el
    selector de formato», que en la 2.0 no existe. Ahora se detecta al apretar Procesar.
  - **Los opcionales de un archivo estaban declarados como múltiples** (Estratificación,
    Inscritos, Multiprofesional, Maestro): se podían elegir varios con ctrl-click, la fila
    decía «2: a.xlsx, b.xlsx» y solo se usaba el primero, callado. Y un opcional con la
    ruta mal tecleada no se validaba: reventaba al abrirlo, a mitad de corrida.
  - **El sidebar volvía a juntar «Salud Mental» y «Salud Mental — Población» por
    PREFIJO.** El estado de validación ya es un dato (`estado: beta`), y la unión dependía
    de que los dos quedaran pegados en `ORDEN_PROGRAMAS`: un programa nuevo que empezara
    con «Salud Mental» dibujaba una segunda cabecera «SALUD MENTAL».
  - **El router apilaba todas las páginas y traía una al frente**, así que la tapada
    seguía mapeada y el **Tab del teclado se iba a las cajas de texto de otra página**.
    Ahora se muestra una y se esconde el resto (`grid` / `grid_remove`).
  - **El encabezado del grupo pandas se ubicaba contando celdas llenas** («la 1ª fila con
    más de 3»), y los banners de RAYEN ya traen filas de 3: una columna más en el banner
    del Monitoreo y el encabezado pasaba a ser una fila de filtros. Ahora es la 1ª fila
    que resuelve las columnas REQUERIDAS, que es el ancla que cada loader ya declaraba, y
    `indice_encabezado` dejó de caer callado a la fila 0.
  - Y quedaron sin uso tres envoltorios que solo reenviaban (`fila_encabezado_admin` y los
    `_fila_encabezado` del A03 y de estamentos) más el `modo` que devolvía
    `encontrar_fila_encabezado`, constante desde que la ronda 11 borró los fallbacks
    posicionales: la única diferencia entre formatos es qué ancla se pasa
    (`formatos.ANCLA`). El mapa de columnas del Inscritos (`MAPA_INSCRITOS`) es uno solo y
    vive en `rem_utils`, junto al del ADA.
- **GUI 2.0, bug recurrente: auditoría ESTÁTICA de cada loader y filtro**
  (`docs/review_gui-2.0_pendiente.md` §1.K, ronda 10). Lo que la ronda empírica no
  alcanzó: cruces entre fuentes, casilleros que fijan el tipo y columnas opcionales.
  - **SP·P6 entero en 0 con «Listo».** Si la base (Estado=Activo × Activo 12m ×
    Ingresado) queda vacía, ahora es `sin_datos`, con el conteo de cada filtro. Pasaba
    con ESTADO en otro vocabulario («Activa») o con el RUN del ADA en otro formato que
    el del Inscritos: cada fuente tenía datos, el cruce no.
  - **A23 con nadie en SALA → TODAS las hojas copy-paste en 0.** Se calculan solo sobre
    «Pertenece a SALA», así que ahora `sin_datos`. Y una pregunta de condición renombrada
    («TIENE» por «PADECE DE») ya no deja esa condición en 0 callada: aviso SUBCONTADO por
    archivo; si no hay ninguna, `sin_columnas`.
  - **A03·D.3 con el export en el casillero equivocado.** Los casilleros fijaban el
    instrumento sin mirar el contenido: un PSC-Y en el de GHQ-12 (todo fuera de rango) o
    un GHQ-12 en el del PSC (todo bajo 33) daban la D.3 en 0. Ahora `instrumento_cruzado`.
    Puntajes fuera de rango: todos, `sin_datos`; algunos, aviso SUBCONTADO (antes solo el
    log).
  - **Sección H con un reporte NSP incompleto.** TIPO, INSTRUMENTO y AÑOS pasan a ser
    requeridos: sin los dos primeros la H salía 0, y sin AÑOS todo caía en «20 y más».
    Una edad ilegible da aviso REVISAR.
  - **Rescate sin MOTIVO/FECHA PASIVACION:** la lista de a quién llamar salía sin la
    marca de fallecido. Ahora el rescate falla (`sin_columnas`); el P6 no se entera.
  - **Histórico SM con un año que bajó solo con encabezado:** se perdía callado en el
    concat. Ahora `sin_datos` POR ARCHIVO, nombrándolo.
  - **Inscritos:** el guard de c38a8cc (que ya no ve el solo-encabezado, lo corta antes
    `cargar_canonico`) dice ahora por qué no queda nadie (N sin RUN, M «RUN
    Responsable»). Y una fila sin RUN ya no sobrevive como la persona `"None"`.
  - **A05: la edad ya no se toma de la columna 11 POR POSICIÓN.** Si el encabezado de
    edad no calzaba, el A05 leía la columna 11 — la posición del layout IRIS, armada
    antes de `refs_tablas/` —, que en el Administrativo es **Convenio**: bandas etarias
    con datos de otra columna, callado. En IRIS nunca hacía falta (el encabezado de edad
    es el ancla de la detección). Ahora la edad se busca solo por nombre, o `sin_columnas`.
  - **Histórico SM sin INSTRUMENTO:** todos los diagnósticos que exigen médico salían
    en NO y el P6 subcontaba sin aviso. Ahora es columna requerida.
  - **A05 sin ninguna fecha legible:** el error aconsejaba «Archivo completo», que cuenta
    todo el archivo como el mes. Ahora `sin_fecha`, con el consejo contrario.
  - **P6, persona sin edad:** contaba en Ambos y en ninguna banda, sin rastro. Ahora va a
    Revisar_Administrativo.
  - **Los resúmenes de A23 y SM muestran sus avisos** (y los del A03), como ya lo hacía
    Población: un «Listo» ya no se lee igual que una corrida sin nada que advertir.
  - **Estratificación sin columna de diagnósticos** y **«Utilización de Cupos» sin
    ningún estamento:** cargaban sin aportar nada; ahora fallan claro.
- **GUI 2.0, trazado entre archivos** (`docs/review_gui-2.0_pendiente.md` §1.F, ronda 5):
  - **`rem_utils.leer_xlsx` truncaba EN SILENCIO un export con la `<dimension>` rota**
    (el peor de la ronda). En modo `read_only`, openpyxl acota `iter_rows` a la
    `<dimension>` que declara el propio .xlsx: con `A1:D5` en una hoja de 10 filas
    devolvía 4, sin error ni aviso. Es el cuello de botella de todo el grupo pandas
    (ADA, grupal, NSP, Otros y Respi, Inscritos, Multiprofesional): un conteo de MENOS
    con cara de legítimo. Su docstring decía exactamente lo contrario («ROBUSTO a la
    dimension rota … con la que pandas.read_excel leería 0 filas»), y pandas, al que
    culpaba, lee las 10: llama `reset_dimensions()` por dentro. Nuevo
    `rem_utils.abrir_xlsx_ro` (read_only + `reset_dimensions()` en cada hoja) +
    `filas_hoja` (rellena las filas al mismo ancho, que sin `<dimension>` llegan
    desparejas). **Toda lectura read_only del proyecto pasa por ahí:** `leer_xlsx`,
    `verificar_hoja_unica` (una tabla dinámica fuera de la `<dimension>` de su hoja pasaba
    por vacía), `catalogos._hojas`, `tools/scan_catalogo` (un RUT fuera de la etiqueta
    **pasaba el escaneo de PII** del About), la detección del A05 y el preview de cruce
    del SM.
  - **La detección del A05 rechazaba un IRIS válido con la `<dimension>` rota** —
    regresión que metió la ronda 4 al leer solo el encabezado. Esa ronda había concluido
    que el peligro era `max_row` y no `read_only`; los dos salen de la misma etiqueta.
    Con `A1`, el encabezado llegaba con UNA columna → «Formato no reconocido». Cerrado
    por el mismo `abrir_xlsx_ro`.
  - **Con VARIOS archivos de atenciones, la FUENTE se clasificaba mirando solo el
    PRIMERO** (`cargar_canonico`). [IRIS, Monitoreo] daba «plena»: banner VERDE «A/D/A de
    IRIS completo» y ningún aviso en la LEEME, sobre filas sin demografía;
    [Monitoreo, IRIS] daba «parcial». El veredicto dependía del orden en que se
    eligieron, no del contenido. Ahora se clasifica cada archivo y gana el peor; si se
    mezclan plenos con no-plenos, el aviso nombra los afectados y dice que lo suyo sale
    de MENOS, no en 0 (`attrs['fuente_mezcla']`, `aviso_fuente(archivos=)`).
  - **Ruta pegada con comillas en el A05** (el «Copiar como ruta de acceso» de Windows,
    que es LA forma de pegar una ruta): `valida_ruta` sacaba las comillas y la detección
    no, así que openpyxl abría `…xlsx"` y el usuario recibía «No es un .xlsx real» sobre
    un archivo perfecto. Nuevo `runner.limpiar_ruta`, que usan la validación, la
    detección y los inputs opcionales de `_resolver_ctx`.
  - **Atención con funcionario pero SIN estamento → `ArchivoInvalido('sin_estamento')`**
    en `cargar_atenciones` (decisión del autor: RAYEN no puede registrar eso, así que
    es un export modificado). Antes llegaba al diálogo de dotación como el grupo
    «(sin estamento)», cuyo «Omitir estamento» **no guardaba nada** (`dotacion.omitir`
    descarta la clave vacía) aunque el grupo desaparecía de la ventana; y esas filas no
    caían en ninguna casilla por estamento. La guarda va sobre la FUENTE (§3.1), no en
    el diálogo.
- **GUI 2.0, revisión de paridad contra `autorem.py`** (lo que el port había perdido o
  roto; `docs/review_gui-2.0_pendiente.md` §1.C-ter y §1.D-bis):
  - **`after()` desde un hilo:** la detección de formato del A05 y el chequeo de cruce
    del SM hacían `frame.after(0, ...)` DESDE el worker. `Tk.after` no es thread-safe
    (registra un comando Tcl): tiraba `RuntimeError: main thread is not in main loop`
    o corrompía Tk de forma intermitente. Nuevo `runner.en_hilo` = cola + poll, el
    mismo patrón que `correr_con_reloj` ya usaba a propósito.
  - **Carrera de dos elecciones de archivo en el A05:** con dos hilos en vuelo, el
    resultado del archivo VIEJO podía pintarse sobre el nuevo → un Administrativo
    colado como IRIS. La categoría ahora se guarda junto a la RUTA para la que se
    calculó, y la que no corresponde se descarta.
  - **Ruta tecleada/pegada en el A05:** no pasa por «Examinar», así que nunca se
    detectaba el formato y salía «Formato no reconocido» sobre un archivo perfecto.
    Ahora `preparar` la detecta ahí mismo (`detectar_ahora`).
  - **Arrastrar el .xlsx sobre el exe** volvió a precargar la ruta: el
    `ruta_inicial` de `_tab_a05` no tenía canal en el shell nuevo
    (`lanzar(ruta_inicial)` → `Pagina.datos["ruta_inicial"]`).
  - **Doble click en Procesar:** `dialogos.dotacion_ada` llamaba `root.update()`, que
    despacha eventos pendientes → un segundo click ya encolado reentraba en
    `on_procesar`, con dos diálogos y dos workers escribiendo el MISMO archivo. Ahora
    `update_idletasks()` (solo repinta) + el botón se deshabilita antes de `preparar`.
  - **Sidebar vacío en el .exe:** `gui/registro.py` descubre las páginas con
    `pkgutil.iter_modules` y nadie las importa por nombre, así que PyInstaller no las
    empaquetaba. `autoREM.spec` suma `collect_submodules('gui.paginas')` + los datos de
    tema de `customtkinter`, y `cargar_registro()` falla ruidoso si no encuentra ninguna.
  - **`tools.scan_catalogo` en el .exe:** lo importa el About para escanear un catálogo
    DEIS antes de aceptarlo, y `tools/` no se empaquetaba → `ModuleNotFoundError`.
    Nuevo `tools/__init__.py` + hiddenimport; si igual faltara, el botón avisa y
    **no** carga el catálogo sin escanear (regla 1).
  - **Títulos de error:** el mapa de títulos por `ArchivoInvalido.categoria` vivía
    dentro de `_tab_a05` y se perdió al centralizar; vuelve en `runner.manejar_error`,
    compartido por todas las páginas y con las categorías nuevas. El `ImportError`
    dejó de mandar a instalar «pandas» cuando lo que falta es otra librería.
  - **El «por qué» de los obligatorios** (`motivo_obligatorio`): el aviso genérico
    perdía explicaciones que el aviso a mano sí daba (Otros Crónicos, Grupal).
  - **El nombre del archivo A03·D.3 lleva el mes pero el módulo NO filtra por mes:**
    ahora se dice en el log, en vez de dejar un archivo que promete un período que su
    contenido no respeta.
- **Cierre del bug recurrente «0 filas» en TODOS los loaders** (auditoría estática de
  los que faltaban). Guardas nuevas sobre la FUENTE, no sobre la casilla:
  - `rem_utils.cargar_canonico` exige filas **por archivo y nombrándolo**: cubre de una
    el ADA, el grupal, los Inscritos, el NSP y «Otros y Respi» (el cuello de botella del
    grupo pandas). Antes daba `AttributeError` en `.str.contains()` sobre columnas que
    con 0 filas quedan `float64`.
  - Nuevo `rem_utils.exigir_filas_ws`, gemelo de `exigir_filas` para el mundo
    openpyxl-worksheet. Enganchado en **A05** (`rem_saludmental._preparar`: la guarda de
    mes vacío no cubría «Archivo completo», `mes=None`), en **A03·D.3**
    (`abrir_validado`: dejaba la tabla entera en 0) y en **«Utilización de Cupos»**
    (`estamentos`: dejaba a todos sin estamento y pisaba el caché con un dict vacío).
  - **A23 Estratificación** (`cargar_estrat`) no tenía ninguna guarda: sin columna RUT
    reventaba con `TypeError` en `f[None]`, y con solo el encabezado dejaba la
    gravedad/tipo de todos en `""` vía `_gate` → **SALA en 0 callado**.
  - `rem_utils.leer_xlsx` con una hoja **sin ninguna fila** (ni encabezado) daba
    `IndexError: list index out of range` en `filas[hi]`.
- **Mismo bug en los hermanos de `cargar_inscritos`:** Formulario SM, ADA de la familia
  población, Inscritos (TRANS del SM), Monitoreo Multiprofesional y Maestro sin filas de
  datos ahora levantan `ArchivoInvalido("sin_datos")` (nuevo `rem_utils.exigir_filas`), en
  vez de un `AttributeError`/`KeyError` críptico o un TRANS = 0 callado.
- **GUI 2.0:** detección de formato del A05 sin `read_only` (la `dimension` rota daba
  «no reconocido»); banners, acuse y cuestionarios se pintan junto a su input y no bajo
  Procesar; la salida de una corrida solo-cuestionarios va junto a los cuestionarios; el
  log de errores inesperados trae el traceback del worker; errores en
  `preparar`/`al_completar`/`resumen` se muestran.
- **`autorem._slim_por_defecto`** busca el Maestro slim en `catalogos/` (se movió ahí).
- **GUI 2.0, barrido línea por línea del diff** (`docs/review_gui-2.0_pendiente.md` §1.D,
  ronda 3):
  - **El mes no se validaba por RANGO, solo por «son números»:** `ttk.Spinbox` acota
    únicamente sus flechas, así que un mes **13** tecleado llegaba al worker y reventaba
    recién en `rem_utils._rango_mes` con un `ValueError: month must be in 1..12` crudo,
    que `manejar_error` no reconoce y despacha como «Error inesperado … pásaselo a
    Simón» — un error de tipeo presentado como bug del programa, y **después** de cargar
    los archivos (en la página de población, minutos de espera). Un año de 2 dígitos (26
    por 2026) era peor: no reventaba, se iba a `filtrar_mes` y salía «no hay filas de
    07/0026», culpando al export. `_tab_a05` y `_tab_beta` validaban el rango en
    `autorem.py`; el port a `widgets.selector_mes` lo perdió para todas las páginas menos
    A05. Nuevo `runner.valida_mes`, compartido por `_resolver_ctx`, el diálogo de
    dotación y el A05; los `from_`/`to` del Spinbox salen de las mismas
    `widgets.ANIO_MIN`/`ANIO_MAX` que valida la guarda (un test lo amarra).
  - **Un input múltiple no se podía volver a VACIAR:** `widgets.fila_archivos` solo se
    podía sobreescribir (el diálogo cancelado deja la selección anterior). Eso dejaba
    **sin salida la corrida solo-cuestionarios** de SM Actividades, que exige «ni ADA ni
    Grupal» (`sm._es_solo_a03`): un click accidental en «Examinar…» sobre el ADA la
    volvía inalcanzable hasta reiniciar autoREM, porque las páginas no se destruyen al
    cambiar de pantalla. Botón «Quitar», que además avisa con `on_elegido([])` para que
    los previews que cuelgan del archivo se apaguen solos.
  - **El banner de fuente sobrevivía a la corrida que lo pintó:** lo pinta
    `al_completar`, así que al elegir otro archivo (o si la corrida siguiente fallaba,
    porque ahí `al_completar` no corre) quedaba un banner **verde** afirmando «A/D/A de
    IRIS completo» al lado de un export parcial recién cargado. El color es una
    afirmación sobre la fuente (plan §5.1, regla 1), no una decoración. Ahora se apaga
    al cambiar cualquier input y al empezar cada corrida —junto con el log y por el
    mismo motivo—, y `pintar_banner_fuente(df=None)` (solo-cuestionarios: no hubo ADA)
    oculta en vez de dejar lo de antes.
  - **`about._volver_a_embebido` llamaba `catalogos.cargar` sin `try`**, al revés que su
    hermano `_cargar_manual`. En un botón Tk de un exe `--windowed` esa excepción no se
    ve en ninguna parte: el botón parecía no hacer nada y `_OVERRIDES` seguía diciendo
    «cargado a mano» sobre un catálogo que ya no estaba en el caché.
- **Sidebar: la cabecera del programa se dibujaba DEBAJO de sus páginas** (visto en vivo
  por el autor). `pack` apila en orden de LLAMADA, no de creación: `_grupo_colapsable`
  tiene que crear `contenido` antes que `header` (la closure `alternar` lo necesita) y lo
  empacaba en la misma línea, así que «SALUD MENTAL» quedaba bajo sus propios botones. El
  síntoma se auto-corregía al colapsar/expandir —`alternar` re-empaca `contenido`, que
  ahí sí cae al final de la pila—, y por eso solo se veía en el PRIMER dibujo.
- **GUI 2.0, auditoría de comportamiento REMOVIDO** (`docs/review_gui-2.0_pendiente.md`
  §1.D-bis y §1.E-bis, ronda 4: qué hacía `autorem.py` que el port dejó de hacer):
  - **La detección de formato del A05 aplastaba tres errores distintos en uno.**
    `_leer_categoria` tenía un `except Exception -> "error_lectura"` y `preparar`
    despachaba eso como **«Formato no reconocido»** con el mensaje de las firmas. O sea:
    a un `.xls`/`.html` disfrazado de `.xlsx` (el clásico de RAYEN, §13) se le decía «no
    encontré las firmas del export, vuelve a descargarlo sin modificarlo» — cuando el
    archivo puede estar impecable y el arreglo es «Guardar como → .xlsx». Igual para un
    archivo abierto en Excel/OneDrive (`PermissionError`) y para un `openpyxl` que falta
    (`ImportError`, que `_tab_a05` avisaba en el log con el `pip install`). Las tres
    ramas siguen implementadas en `runner.manejar_error` y quedaban **muertas**, porque
    `preparar` abortaba antes del worker. Ahora la excepción VIAJA y la clasifica quien
    sabe; el banner usa `runner.motivo_fuente`, que sale del MISMO árbol de `isinstance`
    para que el color y el diálogo no puedan contradecirse.
  - **La salida por defecto de Población se había mudado de carpeta.** `_tab_beta`
    guardaba junto al **Inscritos** (`defecto=entrada.parent`), que es el snapshot del
    mes reportado; el defecto genérico de `_resolver_ctx` es «el primer input cargado», o
    sea el orden en que están *escritos*, y Población los declara en el orden numerado de
    sus instrucciones (1. Formulario histórico, 2. ADA, 3. Inscritos). El P6 y el Rescate
    del mes se iban en silencio a la carpeta del histórico multi-año, que es justo la que
    se tiene archivada aparte. Nuevo `ancla_salida` en el contrato de `inputs`: la
    carpeta ancla es un DATO, no una posición en la lista.
  - **El desglose por instrumento del A03·D.3 se perdió en el port.** La pestaña
    standalone imprimía «60 aplicaciones (PSC: 20 · PSC-Y: 18 · GHQ-12: 22)»; la corrida
    solo-cuestionarios dejó solo el total, aunque `procesar_unificado` seguía devolviendo
    `por_instrumento`. No es decoración: los 3 slots fijan el instrumento **a mano**, sin
    autodetección, así que un export cargado en el slot equivocado solo se delata en el
    desglose — un total pelado tapa igual un 20/20/20 que un 60/0/0.
- **A05: el click en «Examinar…» parseaba el export COMPLETO** (y el worker lo parseaba
  otra vez para procesarlo: **dos lecturas completas** por corrida, donde la GUI 1.x
  hacía una). Las firmas viven en las primeras `MAX_FILAS_HEADER` filas, pero
  `detectar_eje` pide una hoja y depende de `ws.max_row`, que solo es confiable con un
  `load_workbook` sin `read_only`. Nuevo `formatos.detectar_eje_filas` (mismo veredicto,
  sobre filas ya leídas) + `sm.detectar_formato_filas`: la detección lee con
  `read_only=True` e `islice`, **nunca** `max_row`. Tests que amarran que el atajo no
  cambie la respuesta sobre los dos exports reales del repo. **Premisa equivocada,
  corregida en la ronda 5:** `read_only` también respeta la `<dimension>` (y
  `leer_xlsx` tampoco era robusto); ver el primer bloque de esta sección.
- (Renumerado: esta rama había tomado 1.9.16, que `main` ya usó.)

### Cambiado
- **Revisión a mano de TODO el texto user-facing de `gui/`** (el autor, 20-sep-2026;
  `722ecbe` + `6ea9985`, mergeados en `02106fb`): instrucciones de cada página, modales,
  títulos de `ArchivoInvalido`, motivos de los obligatorios, etiquetas de input y líneas de
  log. Es un review que solo puede hacer quien conoce RAYEN/IRIS y el REM: un agente
  verifica que el string exista y esté bien escrito, no que la instrucción sea **cierta**, y
  un texto que manda a descargar el reporte equivocado produce un número plausible-pero-mal
  sin que nada falle (regla 2). La herramienta —extracción por AST a dos archivos gemelos
  para editarlos en un diff lado a lado, y volcado al código de solo los bloques que
  cambiaron— quedó archivada en `docs/evanesced/gui-2.0_textos/textos.py`. **Alcance: 283
  textos de los 11 `.py` de `gui/`, revisados uno por uno** — un texto que la herramienta
  mostró y NO se tocó está aprobado, no sin revisar. Lo que la herramienta no recorre y sigue
  pendiente: los mensajes de `ArchivoInvalido` de `programas/` y `modulos/`, los `log(` de
  `modulos/` y la hoja LEEME de `cobertura.py` (`docs/review_gui-2.0_pendiente.md` §4).
- **`tests/CLAUDE.md`** (nuevo) y tres constantes de texto: la revisión de arriba **rompió un
  test** que comparaba a mano un texto de la interfaz. Un test así no avisa de ningún bug
  —falla por una coma— y encarece cambiar lo que el usuario lee. Convención: si el test
  necesita el texto, éste vive UNA vez como constante del módulo que lo muestra
  (`a05.TITULO_FALTA_ACUSE`, `runner.TITULO_NO_ENCONTRADO`, `widgets.NO_SE_GENERO`) y el test
  la importa; mejor aún, se afirma el HECHO (que se llamó al diálogo, que no se escribió el
  archivo) y no el texto. La constante se crea cuando un test la necesita, no para cada
  string de la GUI.
- **Las salidas NUNCA se sobreescriben** (decisión del autor, sep-2026): si un nombre ya
  existe, la corrida entera sale como `… (1).xlsx`, `… (2).xlsx`, con el MISMO número en
  todos sus archivos (`rem_utils.rutas_libres`), así el sufijo dice qué archivos salieron
  juntos. Aplica a la GUI 2.0 (A05, A23, SM, Población) y a `_correr_tareas`, que también
  usan la pestaña A05 1.x y el CLI. Las demás pestañas 1.x siguen pisando: se borran en
  el paso 11. De paso, un archivo abierto en Excel ya no hace fallar la corrida al
  guardar.
- **El orden de las páginas DENTRO de su grupo del sidebar es ahora un dato**
  (`registro.ORDEN_PAGINAS`). Venía del orden en que `pkgutil.iter_modules` encuentra los
  archivos, o sea del **nombre del .py**: hoy A05 va antes de Actividades solo porque
  `"a05" < "sm"`, y renombrar `sm.py` a `actividades.py` (el título de la página *es*
  «Actividades», o sea el rename natural) las daba vuelta en silencio. Misma clase de bug
  que la posición de Inicio/Acerca de, un nivel más abajo. Fail soft igual que
  `ORDEN_PROGRAMAS` (una página no declarada cae al final de su grupo) + el fail loud en
  los tests.
- **El CLI queda CONGELADO en la 2.0** (decisión del autor, sep-2026): no se le portan
  los cambios de la GUI. Consecuencia conocida y aceptada, anotada en CLAUDE.md §12: los
  mensajes cruzados de `validar_iris`/`validar_admin` mandan a «Cambia el selector de
  formato», y ese selector ya no existe en la 2.0 — solo se alcanzan por el `--perfil`
  del CLI y por el notebook 1.x, las dos superficies congeladas.
- **Sidebar: «Inicio» anclado al TOPE y «Acerca de» al PIE** (feedback del autor,
  sep-2026). Antes la posición de las dos era *implícita*: «donde caiga el bucle de
  `PAGINAS_ESPECIALES` dentro de `_construir_sidebar`» (después de los grupos de
  programa) más el orden interno del tuple — nada declaraba que Inicio va arriba, así que
  sumar un programa a `ORDEN_PROGRAMAS` o reordenar el tuple las movía en silencio. Ahora
  la posición es un DATO (`posicion`: `"arriba"` | `"abajo"`), como el resto de esta
  arquitectura (`PANTALLA`, `ORDEN_PROGRAMAS`, `TAREA`, `COBERTURA`). El toggle de tema
  queda bajo «Acerca de»: es un control de la ventana, no una página.

### Documentación
- **`gui/CLAUDE.md`** (nuevo): lo último antes de empezar el merge. `gui/` era el único
  paquete de código sin el suyo, y el `CLAUDE.md` raíz no nombraba la carpeta en NINGUNA
  parte — ni en el árbol de §2, ni en el reparto compartido/modular, ni en la cadena de
  imports —, con `"gui"` ya en `DIRS_VERSIONADOS` y en `CARPETAS` de `check_fuentes`. **No
  repite el contrato `PANTALLA`**, que ya está completo en el docstring de `gui/app.py`:
  lleva lo que una sesión fría no saca leyendo un archivo — tabla de archivos, checklist de
  página nueva, las trampas con su símbolo greppable (`after()` desde el hilo, el `update()`
  de `CTkToplevel` en Windows, la posición como DATO —mordió 4 veces—, el router que
  muestra/esconde en vez de apilar, detección sin cachear por ruta, `multi: False`, los
  opcionales primero), la tabla de «qué NO se re-implementa» que dejó la ronda de reuso, y lo
  que queda para el paso 11. El raíz ahora la nombra en los cuatro lugares.
- **Regla dura nueva (CLAUDE.md §0 regla 7): ningún documento de trabajo intermedio se
  borra** — planes, registros de revisión, contextos de una rama chica. Son la
  documentación del *por qué*, y una sesión fría (`compact` entre medio) no tiene otra
  fuente. Al cerrarlos se les pone un **header de cierre** (`LISTO Y MERGEADO` + fecha +
  versión en que dejaron de usarse) en vez de eliminarlos, y antes de borrar cualquier
  archivo del repo se mira quién lo cita. Lo disparó un hallazgo de la ronda 13: este
  CHANGELOG cita `docs/review_gui-2.0_pendiente.md` **11 veces** y el propio ledger
  mandaba borrarse al mergear — el merge dejaba 11 referencias colgando en el registro
  permanente, más 2 en `CLAUDE.md` y 1 en la skill `tests-fuentes`.
- **`docs/evanesced/`** (nuevo): los scripts de trabajo intermedio de una rama o worktree
  cuyo trabajo ya cerró, archivados **como quedaron**. Las 13 rondas de revisión de
  `gui-2.0` dejaron 106 archivos de repro, arneses de medición y prompts en scratchpads
  temporales; ahora viven en `docs/evanesced/gui-2.0_revision/`. NO entran copias de
  fuentes del repo (se recuperan con `git show`, y una copia rancia de `app.py` dentro de
  `docs/` se lee como si fuera actual), dumps regenerables con un comando, ni **binarios**:
  el pre-commit anti-RUT salta los `.xlsx` y la whitelist de `.gitignore` es por archivo
  justamente para que cada uno lleve un veto humano. Los 106 pasaron el gate de PII del
  proyecto antes de entrar (0 RUT con DV válido, 0 email, 0 teléfono).
- **Cuatro citas al ledger de la revisión apuntaban a secciones que no existen o se
  movieron**, porque el registro creció de §1..§5 a §1.A..§1.N y las citas no siguieron:
  `CLAUDE.md` decía «§6» (es §4) y este CHANGELOG «§4, puntos 2 a 5» (es §1.C-ter y
  §1.D-bis), «§5, ronda 3» (es §1.D) y «§6, ronda 4» (es §1.D-bis y §1.E-bis).
- **`docs/auditoria_filtros_plan.md`** seguía nombrando `refs_tablas/maestro_slim.csv.gz`
  tras la mudanza a `catalogos/`: un snippet copiable que daba `FileNotFoundError` y un
  `skipif` que habría saltado el test SIEMPRE.
- **`rem_utils.indice_encabezado` decía ser la «fuente ÚNICA» del criterio de encabezado**
  y no lo es desde que el grupo pandas pasó a `encabezado_por_columnas`: son TRES lugares
  con umbral (ese, `encabezado_por_columnas` y `limpiar_refs.MIN_CELDAS_HEADER`). El
  docstring ahora los nombra. Y **`check_fuentes.CARPETAS` excluía `tools/` sin motivo
  escrito**, cuando cada exclusión de `EXENTOS` sí lleva el suyo — y ahí están los dos
  lectores que abren el export CRUDO (`limpiar_refs`, `slim_maestro`). Queda anotada la
  intención: `tools/` va a viajar en el exe en algún momento, y ahí entra al arnés.
- **`gui/paginas/sm.py` decía que `_tab_a03` estaba «YA BORRADA de autorem.py»** y no lo
  está: sigue definida y montada en `lanzar_gui`, que es la GUI que corre el exe. Se
  borra en el paso 11 del plan; hasta entonces conviven. El tiempo verbal importa para
  quien ejecute ese paso (y para cualquier argumento de paridad que se apoye en que la
  pestaña vieja ya no existe).

### Agregado
- **`pytest.ini`** (nuevo, y el repo no tenía ninguno): `testpaths = tests`. Sin él
  `pytest` recorre el repo entero y recolecta cualquier `test_*.py` / `*_test.py` que
  encuentre fuera de `tests/` — con `docs/evanesced/` archivado, uno de los scripts de
  repro calzaba con el patrón, así que la suite lo **importaba** y corría su código de
  nivel de módulo (creaba carpetas y leía `refs_tablas/`) en cada corrida. `pytest <ruta>`
  explícito sigue funcionando: `testpaths` solo aplica sin argumentos.
- **Tests de la ronda 6** (237 en total), con 37 mutantes (13 + 12 del cierre y la
  escritura vía temporal + 12 del caché), todos cazados por el test previsto. Los 9 del
  caché: dañado se aparta y avisa; ilegible no se sobreescribe (dotación y estamentos);
  reintento de un bloqueo pasajero y aviso si no se suelta; dos ventanas no se pisan
  (incluido «Quitar omisión»); los avisos se muestran al cerrar los diálogos de dotación
  y al terminar una corrida; «Acerca de» explica y las dos cajas apuntan ahí; y todo
  test aísla el caché real. Más 4 de la ronda 7 (241 en total), con 6 mutantes cazados:
  «Revisar» y «Precargar dotación» no revierten lo que guardó otra ventana (y el segundo
  guarda los nombres nuevos), `decisiones_cambiadas` por sí sola, y el catálogo elegido
  a mano lo ven las consultas, una carga fallida no lo baja y «Volver» vuelve. Más 4 de la
  ronda 8 (245 en total), con 5 mutantes cazados: el Maestro slim en `<exe>/catalogos/` y
  las dos GUI preguntándole a la misma función, la ruta de Cupos validada en `preparar`,
  el preview de cruce siguiendo el criterio del loader, y el Período del A05 hecho con
  `selector_mes`; el test del candado exige además que «Revisar» diga su aborto. Más 7 de
  la ronda 9 (252 en total), con 11 mutantes cazados: la Sección G con y sin fecha de
  nacimiento, «Otros Crónicos» sin fechas legibles, el formulario/ADA de Población
  posterior al corte o sin fechas, el resumen de Población con sus avisos, el SM sin nada
  que tribute, la ASISTE sin SI/NO y el log de dotación; y 5 más de la segunda pasada
  (257 en total, 13 mutantes más): D.3 sin momento / sin puntaje / sin sexo, preguntas
  del formulario y ADA sin actividad SM, A23 sin nada respiratorio y «Otros Crónicos»
  sin médico, el aviso de sexo/edad del SM, y el Maestro que no reconoce nada. Un fixture de `test_cobertura`
  era justo el caso cazado (un SM entero en 0) y se corrigió. Más 11 de la ronda 10
  (268 en total), con 24 mutantes cazados: la base del P6 vacía y el año vacío del
  histórico, SALA vacía + preguntas renombradas + NSP incompleto, el casillero cruzado
  del A03 y sus puntajes fuera de rango, el Inscritos sin RUN usable, el rescate sin
  pasivación y la edad del A05 por nombre (con el encabezado REAL del Administrativo de
  `refs_tablas/` como guardarraíl: edad = col 4, la 11 es Convenio), el formulario sin INSTRUMENTO + la persona sin edad
  del P6, el A05 sin fechas legibles, la Estratificación sin diagnósticos, Cupos sin
  estamentos y los avisos en los resúmenes de A23/SM (el de SM, corriendo `correr`); 3 fixtures de población/A23 eran el caso cazado (nadie en la base, nadie
  en SALA) y llevan ahora un ingreso real. Más 3 de los contratos de fuentes (271) y 7
  de la ronda 11 (278; 283 con las decisiones del autor) y 13 de la ronda 12 (**296**,
  con 11 mutantes cazados: la forma canónica de la atención y el TP contando igual en los
  dos formatos, el ATEN ID repetido entre pacientes, el archivo con el RUN vacío escondido
  entre varios, el opcional ilegible y el que se valida antes de leer el ADA, el `dfm=` del
  Maestro, la re-detección del A05 al procesar, el Tab que se iba a la página oculta, una
  cabecera por programa, el opcional con la ruta mal tecleada y el encabezado por columnas
  requeridas), con 15 + 12 mutantes cazados antes: la firma de contenido del
  formulario SM (un Goldberg, un PSC y el Otros Crónicos reales en el casillero SM; un
  formulario renumerado), la atención multifila del Monitoreo y el RUN heredado solo
  dentro de su atención, la Estratificación con «Cantidad de Condiciones Crónicas» y sin
  «Detalle», todo literal de actividad contra el Maestro, y `test_refs_tablas.py` (4: el
  script arranca en 3.9, deja banner + encabezado de dos pisos y nada más, no escribe
  un banner con RUT, y toda referencia versionada está limpia). Los fixtures IRIS del
  A05 traían «18.- ESTADO» (en el formulario real es la 19, y la 18 quedaba duplicada):
  justo lo que la firma de contenido rechaza, así que se corrigieron. Los 4 de la segunda
  tanda: `escribir_atomico` (el nombre final no existe mientras se escribe; una
  escritura fallida no deja basura), el A05 escribe vía temporal, la X de la ventana
  pregunta con una corrida viva (por el comando REGISTRADO, no un método llamado a
  mano) y `verificar_hoja_unica` cierra aunque reviente; más el cableado del temporal en
  SM/A23/Población dentro de sus tests. La primera tanda: `test_gui_registro.py` (3: candado de dotación ante un click encolado; SM no
  pisa y el resumen dice que la D.3 no salió; A23 y Población tampoco pisan) ·
  `test_gui_construccion.py` (4: el cruce del SM solo pinta la última elección, incluido
  «Quitar» con un hilo en vuelo; el banner no describe una corrida cuyos archivos se
  cambiaron; etiquetas al 150% caben en su caja; y la PREMISA del candado, que
  `CTkToplevel` despacha los clicks encolados, para que avise si customtkinter deja de
  hacerlo) · `test_autorem.py` (2: `rutas_libres` con un solo número por corrida; el A05
  no pisa).
- **Tests de la ronda 5** (215 en total), cada uno verificado reintroduciendo su bug
  (10 mutantes, los 10 cazados por el test previsto). Rompen la `<dimension>` a
  propósito y comprueban primero que el fixture de verdad arma la trampa, para que el
  test no quede verde por un fixture que ya no la reproduce:
  - `test_formatos_fuente.py` (6, 7 casos): `leer_xlsx` no trunca (`A1:D5` y `A1`),
    `verificar_hoja_unica` ve la hoja extra, la detección A05 sobre el IRIS real, el
    escaneo de PII ve un RUT fuera de la etiqueta (el RUT se ARMA en el test, con DV
    calculado, para no dejar uno literal en el repo), el catálogo se lee entero, y la
    fuente multi-archivo da lo mismo en los dos órdenes y nombra al archivo afectado.
  - `test_gui_construccion.py` (2): la PÁGINA (no solo la capa) del A05 y el preview del
    SM leen el encabezado con la `<dimension>` rota; la ruta pegada con comillas se
    detecta.
  - `test_dotacion.py` (1): funcionario sin estamento → `sin_estamento` nombrando a
    quién; una fila sin funcionario ni estamento no dispara.
- **Tests de la ronda 4** (206 en total). Cada uno se verificó reintroduciendo su bug:
  en la primera pasada **dos sobrevivieron** (probaban la pieza suelta, no el cableado),
  así que se rehicieron — el del desglose A03 ahora corre `sm.correr` de verdad con
  `procesar_unificado` stubbeado, y el del orden del sidebar usa un registro sintético
  al revés, porque con los nombres de archivo actuales el orden alfabético coincide con
  el declarado y el registro real no puede distinguir una cosa de la otra.
  - `test_gui_construccion.py`: un `.xls` disfrazado no se confunde con «formato no
    reconocido», y la salida por defecto de Población va junto al Inscritos.
  - `test_gui_registro.py`: `motivo_fuente` sigue las mismas ramas que `manejar_error`,
    el desglose por instrumento llega hasta el resumen, el orden de páginas no depende
    del nombre del archivo, toda página está declarada en `ORDEN_PAGINAS`, y ninguna
    pantalla declara dos `ancla_salida`.
  - `test_formatos_fuente.py`: `detectar_eje_filas` da el mismo veredicto que
    `detectar_eje` sobre los dos exports A05 reales, y le alcanza el encabezado.
- **`tests/test_gui_construccion.py`** (8 tests): arma la ventana REAL y visita todas
  las páginas con ciclos de eventos. `test_gui_registro.py` valida el CONTRATO sin
  abrir Tk; esto es el escalón que faltaba, y es lo que cazó el `after()`-desde-hilo.
  Se SALTA sin display, no falla. Los 5 nuevos cubren los arreglos de la ronda 3:
  vaciar un input múltiple, que la corrida solo-cuestionarios siga alcanzable después
  de elegir un ADA por error, que el banner de fuente no sobreviva a un cambio de
  archivo, el orden de apilado de la cabecera del grupo, y el anclaje de
  Inicio/Acerca de. Los dos de layout miran el orden REAL en pantalla
  (`pack_slaves()` / `winfo_rooty()`), no índices fijos, así que siguen valiendo cuando
  se sume una página; los de archivo parchean `filedialog.askopenfilenames` para
  recorrer el camino real («Examinar…» → `on_elegido`) en vez de escribirle la
  selección por dentro. Se verificó que cada uno FALLA al reintroducir su bug.
- **`tests/test_gui_registro.py`** suma la guarda de rango de `runner.valida_mes` y un
  test que amarra el Spinbox a las mismas constantes que valida la guarda.
- **`requirements.txt`** lista `customtkinter` (y menciona `pytest` como dep de
  desarrollo, que solo pide `tests/test_formatos_fuente.py`).
- **`poblacion.cargar_inscritos` falla ruidoso con un Inscritos sin filas de datos**,
  en vez de reventar más abajo (`construir_poblacion`, columna PROTECCION NIÑEZ) con
  un `AttributeError: Can only use .str accessor with string values, not floating`.
  Con 0 filas, `DataFrame({...: []})` infiere `float64` en vez de `object`, y
  `.str.contains()` sobre esa columna rompe con un traceback críptico en vez de un
  `ArchivoInvalido` claro. Se encontró al probar `gui/paginas/poblacion.py` (GUI 2.0)
  contra los `refs_tablas/*.xlsx` reales del repo, que son solo header (§2 raíz) —
  0 filas de datos, exactamente el caso que dispara esto. No es parte de la
  migración de GUI: es un bug preexistente en la capa compartida `programas/`.
## [1.9.16] — 2026-09-16

### Agregado
- **Saco roto: dos auditorías por ATEN ID** de atenciones que sí tributan, pero con
  el registro incompleto. Salen rutificadas, con estamento y funcionario, cada una en
  su hoja y con su línea en `TP_Resumen`.
  - **`Ctrl_sin_Formulario`:** atenciones con actividad Control SM (el remoto A32·F2
    cuenta; «Acciones remotas» no) que no traen el formulario «Control de Salud
    Mental» en `FORMULARIOS CLINICOS`. La celda se parte por `;` y cada formulario se
    compara **exacto**: una subcadena `mental` captaba el «Minimental». Sin esa
    columna (Monitoreo admin) no se calcula y queda el aviso NO CALCULADO en la
    LEEME, en vez de un 0 callado.
  - **`Sin_Consejeria`:** atenciones con Control, Consulta o VDI de SM sin consejería
    SM (A19a 97/99) **en la misma atención**.
  - El ATEN ID de IRIS llega numérico (`683.016.530,00` en Excel) y se normaliza a
    texto, para que el `int` y el `float` no separen una misma atención.

## [1.9.15] — 2026-09-15

### Agregado
- **`python tools/hooks_git.py --instalar` instala y verifica los 3 hooks** de un
  viaje. Hasta ahora ese comando corría, no imprimía nada, salía 0 y no instalaba
  ningún hook: un no-op silencioso que se confundía con éxito (estaba documentado como
  trampa en CLAUDE.md §8.2).
  - Llama al instalador de cada check, así los args de cada uno siguen viviendo en un
    solo lugar.
  - Verifica **por el resultado**: `pre-commit` debe listar los tres scripts y
    `commit-msg` el anti-RUT. Si falta alguno, sale con exit 1.
  - Sin argumentos muestra el uso y sale con exit 2.
  - El `--instalar` individual de cada check sigue funcionando.
- **README: sección «Si clonas este repo».** Instalar los hooks con el comando nuevo.
  El autor no se hace responsable de PII en clones o forks sin hooks, y no se acepta
  ningún PR externo sin ellos.

### Documentación
- Plan GUI 2.0 §7.1: fecha de los catálogos visible + actualización manual en «modo
  usuario avanzado». Queda anotado que el drop-in necesita un directorio del usuario,
  porque `_MEIPASS` es temporal.
- `modulos/CLAUDE.md`: checklist de módulo nuevo, incluida la planilla de ejemplo
  header-only. Reemplaza la idea de un check automático.

## [1.9.14] — 2026-09-15

### Cambiado
- **«Saco vacío» → «saco roto»** en todo lo visible: el reporte de Trabajo Perdido,
  la columna `N a saco roto` de `Por_Funcionario`, la fila del resumen, la etiqueta
  y los mensajes de la GUI, el README y los comentarios. Las entradas viejas de este
  CHANGELOG conservan el nombre de su época.
  - La rama `gui-2.0` todavía lo tiene en `gui/paginas/sm.py`: renombrarlo ahí antes
    del merge.

### Agregado
- **Rescate: verificar con el certificado de Fonasa antes de llamar.**
  - `Posibles_Fallecidos` trae una columna nueva, `Antes de llamar`.
  - La hoja LEEME del rescate advierte del caso inverso, que el flag no ve: gente
    fallecida que sigue **Activa** en RAYEN meses después, sin Motivo Pasivación.
    Caso real, sep-2026. Esas personas aparecen en `Rescate_6m`/`13m`, no en
    `Posibles_Fallecidos`.

## [1.9.13] — 2026-09-15

### Agregado
- **SP·P6: columnas AW/AX (TRANS Masculino / Femenino) calculadas.** Hasta ahora
  salían siempre en 0, con la nota «pendiente». Usan la misma regla que el A05 y el
  SM (`rem_utils.trans_de`) sobre `Sexo` y `Género` del Informe Inscritos, split por
  género.
  - **No se filtra por sexo registral.** El control de errores de la plantilla
    espera AW ≤ Mujeres y AX ≤ Hombres. Pero el sexo registral es estático y el
    género declarado cambia sin reingreso al programa, así que ese control salta
    seguido, y el SSMC lo acepta.
  - Esos casos cuentan igual y dejan un aviso en `Revisar_Administrativo` (+ log),
    para que la celda roja de la plantilla tenga explicación. No bloquea.

## [1.9.12] — 2026-09-15

### Corregido
- **A23 con un export de atenciones sin filas reventaba con un traceback críptico**
  (`ValueError: NaTType does not support strftime`) en vez de un error claro. El
  log del rango de fechas formateaba `min()`/`max()` de una columna vacía antes de
  llegar a `filtrar_mes`, que sí tenía la guarda. Lo detectó la sesión de la GUI
  2.0 al probar la página nueva con el export de ejemplo header-only de
  `refs_tablas/`. Ahora el log tolera NaT y la guarda de `filtrar_mes` hace su
  trabajo.
- **`filtrar_mes` dice «no trae ninguna fila» cuando el archivo está vacío.** Antes
  caía en el mensaje de «ninguna fecha legible», que manda a revisar una columna
  reformateada cuando el problema es otro. Aplica a todos los módulos pandas.

## [1.9.11] — 2026-09-15

### Cambiado
- **Regla TRANS única para el A05 y el SM** (`rem_utils.trans_de`), confirmada por
  el autor. Antes los dos contaban solo la vía **explícita** (GÉNERO trae «Trans»).
  Ahora suman la **implícita**: sexo registral binario con género binario opuesto
  (Hombre + Femenina → TRANS Femenina, Mujer + Masculino → TRANS Masculino).
  - La implícita es estrecha a propósito, solo esos dos cruces. La heurística vieja
    `género != sexo` se había descartado por ruidosa porque cruzaba contra cualquier
    valor.
  - **No cuentan:** `No binarie`, `Otra`, `No Revelado`, vacío, ni los sexos
    Intersexual / Desconocido / No Informado. RAYEN registra no binario, pero el REM
    solo tiene binario + Trans y no hay casilla donde ponerlo.
  - A05: la columna `Trans` muestra el sexo en los casos implícitos
    (`Femenina (sexo Hombre)`), para poder auditarlos.
  - SM: `trans_map` ahora exige la columna **SEXO** en el Informe Inscritos, igual
    que GÉNERO. Sin ella, la vía implícita se perdería en silencio.
- **Pueblo originario:** la regla acordada (no cuenta vacío / Ninguno / No Sabe /
  No Contesta; `Otro` sí cuenta) ya estaba implementada en `PUEBLO_VACIO`. Solo se
  actualizó la documentación.

## [1.9.10] — 2026-09-09

### Corregido
- **A32·F2 daba 0 SIEMPRE, y el 0 se leía como «ese mes no hubo».** El patrón era
  la subcadena **contigua** `"controles salud mental por"`, y los nombres reales de
  RAYEN llevan un «de» en medio: `Controles DE Salud Mental por llamadas
  telefónicas` / `Controles de salud mental por videollamadas`. Ninguna de las 4
  variantes del Maestro matcheaba -> la casilla era **estructuralmente** cero, con
  pinta de dato legítimo (así quedó anotado en CLAUDE.md, «sin datos para validar
  el string»). Se descubrió porque esas atenciones aparecían en el reporte de
  **Trabajo Perdido**. Ahora son dos subcadenas en AND
  (`_all(A, "controles", "salud mental por")`), verificadas contra el Maestro:
  capturan las 4 variantes F2 y nada más.
  - `ADA_TRIBUTAN` sumó sus dos entradas (`"salud mental por llamadas"` /
    `"...videollamada"`). Sin eso las F2 seguían contándose como trabajo perdido y
    quedaban fuera de `mask_tributa_ada`, que es la fuente única de qué tributa.
  - Regresión cubierta con los nombres literales de RAYEN.
  - **Moraleja para el resto de los filtros:** un patrón de subcadena *contigua*
    falla en silencio ante un artículo intercalado. Un 0 en una casilla merece que
    alguien verifique el string UNA vez antes de anotarlo como «no hubo».
- **La hoja LEEME no decía que se excluye gente a propósito.** Los avisos de
  dotación cubrían lo pendiente (sin clasificar) y lo omitido (estamentos), pero el
  caso en que la herramienta **efectivamente saca atenciones de las tablas** solo
  salía por el log de la corrida, que se pierde al cerrar. Es justo lo que la hoja
  existe para decir: sin ese aviso, el mes que alguien cuadre estas tablas contra
  RAYEN ve una diferencia sin explicación. Ahora sale como `OMITIDO`, con cuántas
  atenciones, cuántos funcionarios y dónde mirarlas (`SM_Detalle` / `Externos_Delta`).
- **La hoja LEEME desaconsejaba activamente corregir el 0 de A32·F2.** La
  entrada `A27 y A32-F2 -> SIN REGISTRO` decía «el 0 es correcto: no lo llenes
  a mano asumiendo que falta». Para A27 sigue siendo cierto; para F2 era una
  mentira construida sobre el bug de arriba. F2 salió de esa entrada.
- **`cobertura.py` afirmaba algo falso sobre A06·A.2.** Decía «no hay reporte ni
  formulario en RAYEN que las registre»; el Maestro tiene **6** actividades mapeadas
  a REM-A06 A.2/A.3 (Consultorías y Teleconsultorías de salud mental adulto /
  infanto adolescente, y los «Casos revisados»). El motivo real es otro: el centro
  no las registra con esa actividad. La distinción le importa al usuario — no es
  imposible, es accionable.

### Agregado
- **Error específico para el ADA y el grupal cargados CRUZADOS** (`formatos.
  parece_reporte` / `verificar_cruce`, enganchado en `cargar_canonico` vía el
  parámetro `espera`). Las dos casillas están una al lado de la otra, cruzarlas es
  fácil, y hasta ahora reventaba con el «no reconozco el archivo / faltan columnas»
  genérico, que no dice lo único útil. Firmas positivas sobre el header CRUDO; ante
  empate (o cero evidencia) no acusa nada y cae al mensaje de siempre. Sólo se
  consulta cuando la carga YA falló -> no puede dar falso positivo sobre un archivo
  válido. Mismo espíritu que el mensaje cruzado de `validar_iris`/`validar_admin`.
  Trae un huésped de Walt Whitman.

## [1.9.9] — 2026-09-09

### Corregido
- **El diálogo de dotación arrancaba TODOS los ticks en `False`.** Hoy no mordía
  porque solo se le pasaban funcionarios sin clasificar, pero en cuanto se le
  muestra gente ya clasificada (el «Precargar dotación» de abajo) un `Aplicar`
  le borraba la marca de `externo` a todo el mundo **en silencio**. Ahora el
  tick nace de `dotacion.clase(...)`; un nombre nuevo sigue dando `desconocido`
  -> sin tick = interno (el default del plan, §1.3).

### Cambiado
- **La corrida CERO de dotación era imposible de descubrir.** El cuadro estaba
  ARRIBA de los selectores de archivo y su único botón («Revisar dotación…»)
  muestra solo lo YA guardado -> en la primera corrida salía vacío, y nada decía
  que había que cargar el ADA primero. Tres arreglos:
  - el cuadro se movió **DEBAJO** del ADA y el grupal (donde ya hay algo que
    mirar), vía un holder que le reserva el lugar en el orden de `pack`;
  - botón nuevo **«Precargar dotación…»**: carga el ADA, lo filtra al mes y abre
    el diálogo con **TODOS** los funcionarios — que es el veto inicial del plan
    (§3.1) y además permite corregir a alguien ya clasificado, con evidencia
    (n_atenciones / actividades) que «Revisar dotación…» no puede dar;
  - el mensaje de vacío de «Revisar dotación…» ahora explica qué hacer en vez de
    decir solo «se puebla al Procesar».
- `autorem._dotacion_ada()` unifica cargar-ADA + filtrar-mes + evidencia +
  diálogo: lo usan el botón nuevo y `on_procesar` (que ya lo hacía inline).
  Devuelve el ADA cargado, así que sigue sin releerse para el worker.

## [1.9.8] — 2026-09-09

### Agregado
- **`programas/dotacion.py`: separar atenciones de funcionarios EXTERNOS** (no
  son de la dotación del CESFAM — hoy la sala AIDIA) de las de la dotación
  propia. Capa compartida nueva, gemela estructural de `estamentos.py` (misma
  persistencia/merge/failsafe): tri-estado `interno`/`externo`/`desconocido`
  por funcionario, cacheado en `~/.autorem/dotacion.json` (`funcionarios`
  global, `omitidos` por módulo). `en_rem = (clase != externo)`: un
  `desconocido` CUENTA al REM por defecto (nunca sangra producción propia en
  silencio), pero se reporta siempre. Ver `docs/dotacion_externos_plan.md`.
- **Wiring en `modulos/rem_sm_actividades.py`:** cada EVENTO se clasifica
  (`clasificar_evento`, caso mixto — visita con más de un profesional: interno
  si hay al menos uno interno, si no externo si hay al menos uno externo, si no
  desconocido) y las tablas de sección pasan a calcularse sobre `E[en_rem]`.
  `SM_Detalle` conserva TODAS las filas (marcar, no borrar) con las columnas
  nuevas `externo`/`tabula_en`; hoja nueva `Externos_Delta` (Total/Externos/REM
  por casilla). Avisos de dotación (externos separados, sin clasificar,
  estamentos omitidos) van a la hoja LEEME.
- **GUI (`autorem.py`):** cuadro informativo + botón "Revisar dotación..." en
  la pestaña SM; al Procesar, si hay funcionarios nuevos tributando, se abre un
  diálogo (ticks agrupados por estamento, con el costo de omitir a la vista)
  ANTES de lanzar el worker — el diálogo usa Tk y no puede correr en el hilo de
  fondo, así que el ADA se carga y filtra por mes en el hilo de la GUI y se
  comparte con `procesar()`.
- `tests/test_dotacion.py` (8 pruebas): clasificación, first-run, persistencia,
  `en_rem` con desconocido, caso mixto, wiring en sm_actividades
  (`Externos_Delta` cuadra, `SM_Detalle` conserva filas externas), omisión por
  módulo, un omitido nunca queda `interno`.

## [1.9.7] — 2026-09-09

### Agregado
- **SM Actividades — columna `funcionario` en `SM_Detalle`:** el nombre del
  profesional que registró cada atención (`PROFESIONAL ATENCION`/`FUNCIONARIO`
  del ADA, `FUNCIONARIO PRESTADOR`/`NOMBRE PROFESIONAL` del grupal), separada de
  `estamento` (que en el ADA es la disciplina/`INSTRUMENTO`, no el nombre). Si el
  dedup por `(casilla, sub, id)` colapsa varias filas de una misma atención con
  distinto profesional (visita con más de uno), se concatenan los nombres ÚNICOS
  en el ORDEN en que aparecen (no alfabético).

## [1.9.6] — 2026-09-08

El pre-commit bloqueó un commit hecho desde un **worktree** describiendo con precisión
un árbol que no se estaba commiteando: reportó headers viejos de `main` mientras el
worktree ya iba en 1.9.5.

### Corregido
- **Los hooks ahora resuelven las rutas contra `$REPO = git rev-parse --show-toplevel`,
  no contra la ruta absoluta del clon donde corriste `--instalar`.** Los hooks viven en
  el `.git` COMPARTIDO, así que el mismo archivo corre desde el checkout principal y
  desde cada worktree; con rutas absolutas, un commit hecho en un worktree ejecutaba
  los checks del OTRO árbol. Efecto colateral bueno: el hook deja de depender de dónde
  está clonado el repo, así que sobrevive a mover la carpeta.
- **`--instalar` migra los hooks viejos en el lugar:** detecta la invocación con ruta
  absoluta del mismo script y la REEMPLAZA (si solo agregara la nueva, quedarían las
  dos y la vieja seguiría mirando el árbol equivocado).
- **Bug latente en `check_cp1252 --instalar`:** su copia del encadenado no sacaba el
  `exit 0` final, así que instalarlo DESPUÉS de `check_version` dejaba su línea después
  del `exit` — instalado y sin correr nunca, callado. La copia de `check_version` sí lo
  hacía; era exactamente la clase de divergencia que justifica el punto siguiente.

### Agregado
- **`tools/hooks_git.py`** — fuente única de `--instalar`. Los tres hooks
  (anti-RUT §8.2, cp1252, check_version) encadenan al MISMO `pre-commit` y cada uno
  traía su propia copia de la lógica; ahora hay una, idempotente y con la migración.

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
