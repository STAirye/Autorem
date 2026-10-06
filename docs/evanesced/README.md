# docs/evanesced/

Trabajo **intermedio** de ramas y worktrees cuyo trabajo ya se cerro: los scripts de
repro, los arneses de medicion, los prompts de cada ronda y las notas que produjeron los
cambios que estan en el `CHANGELOG`. Nada de esto se importa, se distribuye ni se corre en
CI: es **documentacion del porque**, y esta aca porque la rama o el worktree donde vivio
desaparece y una sesion fria no tiene otra fuente ([CLAUDE.md](../../CLAUDE.md) §0 regla 7).

El nombre: la rama se evanesce, sus scripts no.

## Que entra

- `.py` de repro y medicion, `.md` de notas y prompts, `.txt` de salidas cortas.
- Se archiva **como quedo**, sin limpiar ni reescribir: un script arreglado a posteriori ya
  no prueba lo que probo.

## Que NO entra

| Que | Por que | Como se recupera |
|---|---|---|
| Copias de fuentes del repo (`app.py`, `formatos.py`, `poblacion.py`, …) | Una copia rancia de un fuente dentro de `docs/` es peor que no tenerla: se lee como si fuera actual. Ademas llevan `# Version:` y `check_version` bloquea el commit (la version solo la llevan `programas/`, `modulos/`, `tools/`, `gui/` y `autorem.py`) | `git show <commit>:<ruta>` |
| Dumps grandes regenerables (`git merge-tree`, listados de headers, snapshots de `git diff`) | Son salida de UN comando, y pesan mas que el comando | el comando esta anotado en la nota que lo usaba |
| **`.xlsx` / binarios** | El pre-commit anti-RUT **salta los binarios** (tools/CLAUDE.md §8.2), y `.gitignore` ignora `*.xlsx` con **whitelist por archivo** justo para que cada uno lleve un veto humano. Un fixture que hace falta de verdad va a `refs_tablas/` por la skill `limpiar-refs`, con su linea de whitelist y su contrato | el script que lo usaba lo reconstruye |

## Gotchas al archivar

- **cp1252:** `tools/check_cp1252.py` barre TODO `*.py` del repo, y estos scripts traen
  flechas, `OK`/tildes de estado y a veces BOM. Por eso `evanesced` esta en su
  `EXCLUIR_DIRS`, con el mismo criterio que `worktrees`: codigo congelado de otra tanda,
  que no imprime a la consola del exe. **No** reescribir los scripts para que pasen el
  checker.
- **Antes de borrar cualquier archivo del repo**, mirar quien lo cita:
  `grep -rn "<nombre>" --include="*.md" --include="*.py" .`. El `CHANGELOG` es permanente.

## Contenido

### `gui-2.0_revision/`

Las 13 rondas de code-review de la rama `gui-2.0` (sep-2026). El registro de lo que
encontraron es [docs/review_gui-2.0_pendiente.md](../review_gui-2.0_pendiente.md); esto es
el instrumental.

| Carpeta | Que hay |
|---|---|
| `finders/` | Los agentes finder (uno por ronda, con `compact` entre medio): el `review_context.md` que compartian, los arneses de repro por angulo (`alt/`, `b/`, `e/`, `dimtest/`) y los scripts de cada hallazgo |
| `sesion-principal/` | La sesion que aplico los arreglos y anoto el ledger: repros, mediciones, mutantes y los scripts de edicion CRLF-safe del propio ledger |
| `prompts/` | Los prompts de ronda, tal como se pegaron, mas `prompt_merge_2.0.md` (el del merge a `main`) |

Lo mas reutilizable, por si sirve de nuevo:

- `sesion-principal/r13/imports_muertos.py` - imports sin uso en los 4 paquetes (AST).
- `sesion-principal/r13/attrs.py` - todo `mod.attr` del arbol contra el modulo real
  importado: caza una referencia a un simbolo que un refactor borro.
- `sesion-principal/r13/hdr.py` - compara los criterios de fila-de-encabezado sobre las
  referencias de `refs_tablas/`.
- `sesion-principal/r13/anios_discontinuos.py` - repro del hueco de anios en la familia
  poblacion (hallazgo 8 de la ronda 13).
- `sesion-principal/r13/escanea_candidatos.py` / `escanea_xlsx.py` - el gate de PII del
  proyecto aplicado a un directorio cualquiera antes de meterlo al repo. **Ojo:**
  `scan_catalogo.escanear` devuelve una **3-tupla**.
- `sesion-principal/r13/repro_mask_unida.py` - por que `auditar_atenciones` (main 1.9.16) hay
  que adaptarlo a la forma canonica de `cargar_atenciones` y no al reves: una mascara
  multi-token (`contiene_todos` con 2 tokens) que sobre la celda de actividades UNIDAS matchea
  tokens de actividades DISTINTAS. Es la evidencia del hallazgo del merge (ver el §4 del
  registro de la revision).
- `finders/alt/harness.py` - arnes de contratos de fuentes, antes de que fuera
  `tests/contratos_fuentes.py`.

### `hooks_auditoria-2.0.5/`

La auditoria de los cuatro pre-commit (sep-2026), disparada por el bug que corrigio la
**2.0.5**: `check_version` decia vigilar cuatro contadores de tests y **tres de sus
patrones estaban muertos** -- apuntaban a frases del `CLAUDE.md` monolitico que
desaparecieron al partirlo por carpeta. Un patron que deja de matchear **no falla: deja
de vigilar**, calladito. Estos dos scripts fueron a buscar esa misma clase de bug en los
otros tres checks (no encontraron ninguno) y a confirmar que cada uno caza un positivo.

- `auditar_hooks.py` - busca **referencias muertas**: recorre `TRANSVERSALES` y `EXENTOS`
  de `check_fuentes` (que nombran funciones a mano, `archivo.py::funcion`) y verifica por
  AST que cada una siga existiendo; ademas lista que llamadas con pinta de lectura de
  planilla no estan en `LECTORES`. **Ojo con esa ultima lista:** da falsos positivos a
  proposito -- los wrappers (`cargar_atenciones`, `cargar_inscritos`…) salen como «NO
  VIGILADO» pero el AST SI los caza, porque adentro llaman a un lector de `LECTORES`.
- `probar_hooks.py` - prueba **funcional**: le da a cada check algo que DEBE cazar y
  confirma que lo caza (un check que pasa siempre no sirve). El RUT de prueba se arma en
  runtime, cuerpo aritmetico + DV calculado, para no dejar un literal con forma de RUT en
  disco (§8.1); el `.py` con la flecha Unicode se escribe en `tools/` y se borra en un
  `finally`.

**Los dos llevan `RAIZ` como ruta ABSOLUTA de la maquina del autor** (vivieron en el
scratchpad de la sesion, fuera del repo): archivados como quedaron, hay que ajustar
`RAIZ` para correrlos desde aca.

Lo que la auditoria encontro vivo esta en el `CHANGELOG` de la 2.0.5. Lo unico que quedo
abierto: `check_fuentes --todo` avisa que `rem_utils.cargar_maestro` tiene el contrato con
**encabezado sintetico**, y pide el export real recortado a solo encabezado (skill
`limpiar-refs`). No bloquea.

### `gui-2.0_textos/`

La revision de textos user-facing de la GUI 2.0 (sep-2026), hecha por el autor. El
resultado esta en el codigo y en el commit `722ecbe`; esto es la herramienta.

- `textos.py` - `extraer` recorre por AST los strings de `gui/` (titulos, botones,
  dialogos, resumenes, logs) y escribe dos archivos gemelos, `original.txt` y
  `editable.txt`, para editar uno en un diff lado a lado; `aplicar` vuelca al codigo solo
  los bloques que cambiaron (CRLF-safe, empareja por posicion, respeta los `{placeholders}`
  de las f-strings). **Ojo:** archivado como quedo, con `RAIZ` = la carpeta padre de donde
  vivia (`textos_review/` en la raiz del worktree); hay que ajustar `RAIZ`/`AQUI` para
  correrlo desde aca. Solo cubre `gui/`, no los textos de `programas/` ni `modulos/`.

### `eficiencia-2.0.6/`

Los arneses de los tres primeros arreglos de la **ronda de EFICIENCIA** (sep-2026, sobre
`main`). Estan archivados porque **son la prueba de los numeros del CHANGELOG de la
2.0.6**: los tres cambios se vendieron como equivalencias EXACTAS, y eso hay que poder
volver a verificarlo sin rehacer el razonamiento.

- `bench_3fix.py` - el antes/contra-despues. Mide las tres cosas en una corrida
  (`_estado_dx` de las 28 specs, `norm` sobre 400k celdas, `anotar` de 2000 codigos) y se
  corre **dos veces**: una en un worktree en el commit viejo y otra en el arbol nuevo. Asi
  salieron las cifras del CHANGELOG.
- `equivalencia_estado_dx.py` - 56 comparaciones (28 specs x `instrumento` True/False)
  contra una copia textual de la version 2.0.5, con **fechas llenas de empates a
  proposito**: el unico caso en que recortar columnas podria haber movido un resultado.
- `equivalencia_cruzar.py` - los **12.548 codigos** de la Lista Tabular contra los dos
  catalogos cruzados (25.096 consultas) mas los bordes, tambien contra una copia textual
  de la version vieja.

**Los dos `equivalencia_*` llevan adentro una COPIA de la implementacion vieja** — es
justamente lo que los hace servir, asi que no se actualizan cuando el codigo vivo cambie.
Si vuelven a hacer falta, lo que se compara es «la version de entonces» contra la de hoy.

Los tres se corren con `PYTHONPATH=<raiz del repo>` (viven fuera de `programas/`, y
`equivalencia_cruzar.py` ademas necesita los `catalogos/*.csv.gz` vendorizados). A
diferencia de los otros archivados, **no tienen rutas absolutas**: corren desde aca.

### `eficiencia-2.0.9/`

La **segunda** ronda de eficiencia sobre `main` (sep-2026), pedida despues de la 2.0.6.
Estan archivados por la misma razon que los de la 2.0.6 -- son la prueba de los numeros
del CHANGELOG --, pero la leccion de esta tanda es otra y vale mas que los scripts:

> **Ordenar por lectura del codigo se equivoco TRES veces seguidas.** La lista de
> hallazgos salio de leer, y el orden que proponia estaba mal las tres veces que se
> contrasto con un perfil. `perfil_poblacion.py` reordeno la ronda entera; el hallazgo
> que resulto mas caro (`_ultima_respuesta`) no estaba en NINGUNA de las dos listas de
> revision, y el que parecia grande (el hallazgo 6) resulto valer 0,28 s.

- `perfil_poblacion.py` - **el que cambio el plan.** Arma inscritos/formulario/ADA
  sinteticos del tamano del centro (30.000 / 60.000 x 134 columnas / 120.000) y perfila
  `construir_poblacion` entera, las dos pasadas. Es el que mostro que la 2a pasada de
  Brecha_Medico era el 41% del total y que `_ultima_respuesta` se comia 0,5 s por pasada.
  **Ojo:** sus RUN sinteticos NO llevan DV valido, asi que `construir_p6` sobre su salida
  corta con el guardarrail de `_base_valida` (descarta el 91%, techo 5%). Para medir el P6
  hay que remapear los RUN con `dv_rut`, como se hizo en la sesion.
- `equivalencia_brecha.py` - la brecha calculada por los dos caminos (tabla entera vs
  solo la columna) sobre el mismo frame. Ademas imprime **que columnas cambian de verdad
  con `exigir_medico`**: son 31 de la tabla, y ninguna es `Estado` ni `¿Activo 12m?`. Esa
  salida ES la premisa del atajo de `runs_ingresados_sin_filtro_medico`.
- `equivalencia_colapso.py` - `_una_fila_por_atencion` nueva contra una **copia textual
  de la 2.0.8**, comparando por `repr` y no por texto (un entero que se vuelve float tiene
  que saltar), sobre los bordes: grupo con la columna vacia en TODAS sus filas, nulo antes
  que `''` y al reves, ACT/DIAG vacios en todo el grupo, fila padre que no es la primera,
  ATEN ID numerico, filas sueltas entre medio. Mas 6 frames grandes al azar.
- `medir_hallazgo6.py` - instrumenta `norm` para **contar llamadas reales** en `_sala` y
  `_seccion_g` del A23. Asi se confirmo que eran 47 pasadas sobre el formulario y que solo
  13 eran recuperables barato.
- `bench2.py` / `bench3.py` / `bench4.py` - los candidatos de la ronda, cada uno contra su
  alternativa. `bench4` ademas perfila `_una_fila_por_atencion` y prueba la version
  vectorizada que quedo.
- `bench5.py` - el costo del barrido de filas de `marcar_eventos` (lo que el A05 paga UNA
  VEZ POR TAREA: ingresos y egresos corren los dos sobre el MISMO `ws`).
- `bench_cell.py` - **un hallazgo DESCARTADO, archivado a proposito.** La hipotesis era
  que `ws.cell(row,col).value` por celda es el patron lento de openpyxl. Es falso: en modo
  normal openpyxl ya materializa todas las celdas al cargar, asi que `ws.cell()` es un
  lookup de diccionario. Medido: 0,33 s contra 0,35 s de `iter_rows(values_only=True)`, y
  `ws._cells` queda igual en los dos. **No volver a reportarlo.**

Los tres `bench_*` y `medir_hallazgo6` corren desde aca con `PYTHONPATH=<raiz>`.
`perfil_poblacion.py`, `equivalencia_brecha.py` y `equivalencia_colapso.py` llevan la
**ruta absoluta de la maquina del autor** en un `sys.path.insert` (vivieron en el
scratchpad): hay que ajustarla. `equivalencia_brecha.py` ademas importa a
`perfil_poblacion` por su ruta absoluta del scratchpad.

**Lo que quedo sin hacer**, con su numero medido, esta en el §12 del CLAUDE.md raiz.

### `eficiencia-2.0.6/` (continuacion)

**Lo que midieron de yapa** (el hallazgo que destapo el propio arnes): tras recortar las
columnas, el costo dominante de `_estado_dx` dejo de ser el `groupby` y paso a ser las
tres `str.contains` de las mascaras — 0,44 s de los 0,63 s que quedaban —, y una de ellas,
`INSTR_n.str.contains("MEDIC")`, es **invariante entre las 28 specs**. Eso se cerro en la
**2.0.7** (memo de una ranura por weakref); `equivalencia_estado_dx.py` se volvio a correr
para esa version y sigue dando 0 diferencias, porque compara contra la 2.0.5.

Lo que sigue SIN hacer de ese mismo perfil: las otras dos `str.contains` (`INGRES` y
`SEGUIMIEN`) SI dependen de la spec, asi que no se pueden izar igual — habria que
precalcularlas por pregunta, que es otro diseno y no estaba pedido.

### `lectura-calamine/`

La medición que dio origen a [docs/lectura_calamine_plan.md](../lectura_calamine_plan.md)
(sep-2026). Empezó como «¿cuánto acelera Cython el exe?» y terminó en «Cython nada, el
lector de `.xlsx` todo». Archivados **antes** de implementar, por pedido del autor: son la
prueba de los números del §1 del plan.

- `perfil_cython.py` - cProfile de SM Actividades y A05 sobre agosto 2026 REAL, con el
  `tottime` repartido por origen (código propio / openpyxl / pandas / builtins C). Dio
  código propio = 2 % (SM) y 6 % (A05): el techo de Cython. **Ojo:** el profiler infla los
  absolutos ~2,5× (ADA 31 s con profiler, 12 s sin él); valen las proporciones.
- `bench_calamine.py` - openpyxl (`verificar_hoja_unica` + `filas_xlsx`) contra
  `python-calamine` sobre ADA, Inscritos y Formulario PSM reales: tiempo + comparación
  celda a celda. La primera versión normalizaba tipos y dio 0 diferencias; la segunda cuenta
  aparte las celdas iguales **solo tras normalizar**, y eso destapó el `int`->`float` (una
  columna entera por archivo). **Lección: una comparación que normaliza esconde justo lo que
  rompe un join.**
- `sonda_calamine.py` - la API de calamine sobre un `.xlsx` SINTÉTICO: tipo por tipo contra
  openpyxl (vacío -> `''`, `#N/A` y solo-espacios -> `''`, fecha a medianoche -> `date`),
  la excepción ante un `.html` disfrazado (`ZipError`) y que el archivo queda liberado tras
  una excepción.
- `medir_a05.py` - el A05 N+O **sin profiler**, fase por fase (los mismos pasos de
  `autorem._correr_tareas`), más la alternativa de escribir un libro nuevo `write_only`
  solo con las hojas de salida. Dio 6,5 s en total (abrir 3,1 · motor 0,8 · guardar 2,3;
  la alternativa 0,04 s) y con eso el autor **descartó** tocar el A05 (§2.3 del plan).
  **Bug conocido, archivado como quedó:** la última línea abre `hoy_0.xlsx` en
  `read_only` para contar hojas y no lo cierra, así que el `finally` revienta con
  `PermissionError` al borrar el temporal, que **lleva RUT**. En la sesión se borró a mano
  (`%TEMP%\a05_*`). Si se vuelve a correr, cerrar ese workbook o revisar `%TEMP%` después.

**Después de la implementación** (rama `lectura-calamine`, cerrada en la **2.0.17**):

- `revision_ciega/informe_fase1.md` y `informe_fase2.md` - el informe del primer uso de
  [docs/revision_ciega_prompt.md](../revision_ciega_prompt.md): la fase ciega (todas las
  salidas reales idénticas; 2 DIFF declarados de `leer_xlsx`) y la des-cegada (4 efectos
  colaterales y lo que ninguna corrida cubrió). Sin valores de celda por diseño.
- `pf_paridad.py` - el hallazgo que la revisión dejó pasar de largo y se midió después:
  `primeras_filas` con calamine parseaba la hoja entera (ADA 0,9 -> 2,0 s). Mide la
  versión vuelta a openpyxl y su paridad por `repr` con `filas_xlsx`. Corre con
  `cwd` = la raíz del árbol a medir.
- `memoria_calamine.py` - pico (`PeakWorkingSetSize`) y retenido de leer los exports
  reales, main contra la rama, cada escenario en un proceso nuevo. **Ojo:** la primera
  corrida dio 0 MB en todo porque faltaba declarar `restype`/`argtypes` de las llamadas a
  Windows (el handle se truncaba a 32 bits y la llamada fallaba callada); el archivado ya
  lo trae arreglado y ahora falla ruidoso.
- `sonda_iter_rows.py` - `iter_rows` arranca en la fila 1 pero en la COLUMNA del primer
  dato (`sheet.start[1]`): hay que rellenar a la izquierda.
- `memoria_variantes.py` - hoy / fila a fila / fila a fila + strings reusados, con hash de
  todas las celdas para exigir salida idéntica. Fila a fila solo no baja el pico (es la
  hoja del lado de Rust); reusar strings sí (558 -> 387 MB). La primera corrida reventó
  con `PanicException` de Rust en las hojas vacías: de ahí la guarda.
- `paridad_iter_rows.py` - el adaptador nuevo contra una copia textual del viejo
  (`to_python`), por `repr` y por tipo, en los tres exports reales y un sintético con
  datos desde C3 y hojas vacías: 0 diferencias.

Llevan las mismas rutas absolutas que los de arriba (`RAIZ`/`RAMA` y `Datos madre`); el
worktree `lectura-calamine` al que apuntan desaparece al cerrarse la rama.

Los cuatro primeros imprimen solo tiempos, formas y conteos, nunca valores. `perfil_cython.py` y
`bench_calamine.py` llevan la **ruta absoluta del repo** en un `sys.path.insert` y leen los
exports de `Datos madre` en el OneDrive del autor: sin esos archivos no corren. Lo mismo
vale para `medir_a05.py`.
`sonda_calamine.py` corre en cualquier parte.

### `suite-2.0.14/`

La remedición de `tools/correr_tests.py` tras pasar a Tcl 9 (sep-2026). La suite había
bajado sola de 103 s a **~47 s**, y el wall pasó a ser **exactamente**
`test_gui_construccion` corriendo solo (~46 s).

- `variantes_suite.py` - el mismo reparto que `correr_tests.py` (importa su `repartir`),
  en cuatro variantes: base, `OPENBLAS/OMP/MKL/NUMEXPR_NUM_THREADS=1`, los procesos no-Tk
  con `BELOW_NORMAL_PRIORITY_CLASS`, y las dos cosas. Las cuatro dieron 47,7-49,9 s:
  **ni la sobresuscripción de hilos de BLAS ni la prioridad explican nada**. Se escribió
  para explicar una corrida de 84 s que después **no se repitió** (ruido del PC): la
  lección es comparar siempre con al menos dos corridas.

Lleva la **ruta absoluta del repo** en `RAIZ`. Solo Windows (`BELOW_NORMAL_PRIORITY_CLASS`).

### `gui-trinquete-2.0.16/`

Por qué construir una página costaba segundos (sep-2026). La hipótesis de partida del
autor era «lee archivos»; el perfil dijo que no (0,03 s de todo `about.py`) y la cadena
de experimentos llegó al **trinquete de layout** de `widgets.etiqueta_envolvente`,
arreglado en la **2.0.16**. En el orden en que se corrieron:

- `perfil_acerca_de.py` - pared + cProfile de `mostrar("acerca_de")`, cronometrando cada
  bloque de `about.py`. Mostró que el costo estaba entero en una cascada de Tk colgada de
  `CTkScrollbar._draw` -> `update_idletasks` (112 veces) y 2.201 `_update_dimensions_event`.
- `scroll_diferido.py` - **hipótesis DESCARTADA, archivada a propósito:** diferir el
  `set` del scrollbar hasta el final no baja nada (y el SM empeora). El scrollbar era
  dónde se disparaba el layout, no por qué.
- `cascada_wrap.py` - la prueba: sin el `bind("<Configure>")` de las etiquetas,
  acerca_de 3,3 s -> 0,14 s. Reconfigurar solo si el ancho cambia NO sirve (mismos
  conteos): el ancho cambia de verdad en cada vuelta.
- `trinquete_wrap.py` - la secuencia de anchos que ve cada etiqueta: arranca en 1619 px
  (el texto sin partir) y baja de a pocos px hasta ~300 antes de saltar a 920. Ahí se ve
  el trinquete.
- `fix_wrap.py` - el arreglo candidato (wraplength inicial 1 y 300) contra hoy, en 5
  páginas, a escala 1.0 y 1.5, comparando el wraplength FINAL de cada etiqueta tras
  construir y tras agrandar/achicar la ventana. Lo único distinto: etiquetas de cajas que
  nacen escondidas (0 hoy, 300 con el arreglo, hasta mostrarse). **Ojo:** archivado como
  quedó tras la última corrida, recortado a SM y A05 a escala 1.0 para ver QUÉ etiquetas
  diferían; la corrida completa (5 páginas × 2 escalas) era el mismo script con las
  tuplas originales de páginas y escalas.
- `medir_paginas.py` - el bloqueo de cada página con el arreglo puesto: la tabla del
  CHANGELOG de la 2.0.16.

Todos llevan la **ruta absoluta del repo** en un `sys.path.insert` y abren ventanas de
verdad (necesitan display). Los números de esa sesión tienen ruido: corrían en paralelo
con la revisión ciega de `lectura-calamine`.

### `rendimiento-2.0.23/`

Por qué el A23 y el P6 «se pegaban» con historial 2021..2026 (oct-2026). La hipótesis
del autor era «solo volumen»: era cierto para la lectura del ADA (~30 s, irreducible sin
caché, que se descartó por seguridad), pero no para lo demás. Llevó a la **2.0.22** (A23,
69 -> 47 s) y la **2.0.23** (P6, 91 -> 46 s; RAM 1,6 GB -> 716 MB).

- `bench_a23.py` - pared por fase del A23 entero (ADA, Otros, NSP 2021..2026-09 +
  Estratificación, mes 2026-09) envolviendo funciones del módulo, + pico de RAM. Mostró
  los 21 s de `escribir` (detalle con TODO RUN de la historia) y los 9 s del NSP.
- `bench_a23_2.py` - lectura por archivo + cProfile de `cargar_inasistentes` y de
  `escribir`: el NSP caía a `dateutil` celda por celda en `fecha_col` (de ahí salió,
  además, el bug de `AAAA/MM/DD` invertido con `dayfirst`).
- `bench_p6.py` - lo mismo para `gui/paginas/poblacion.correr` (P6 + Rescate): el formulario
  SM con `load_workbook` completo (19 s) y `PSM_Poblacion` con los 55k del Inscritos (30 s).
- `bench_sm.py` - SM Actividades (ADA + grupal + Inscritos, 1 mes y 3 meses) para ver si la
  demografía del grupal de la **2.0.27** costaba tiempo: **no** (11,9 -> 11,0 s y 12,6 ->
  12,3 s; `demografia_por_run` 0,1-0,6 s aun con el ADA 2021..2026). Toma la raíz del
  CÓDIGO como 1er argumento: la versión «antes» se corrió sobre un `git archive c6b8b02`
  extraído al scratchpad (no archivado: copia de fuente). Años del ADA opcionales al final.

**Trampas:** las rutas de datos son absolutas, al OneDrive del autor (`Datos madre`); los
dos `bench_a23_2`/`bench_p6` importan `bench_a23` desde la misma carpeta (por eso éste
tiene el `main()` guardado, agregado a mitad de sesión). `bench_a23.py` envuelve
`a23.cargar_atenciones` etc., así que los tiempos internos se SOLAPAN (la lectura calamine
está dentro de las cargas). Solo imprimen tiempos, conteos y nombres de función. La
comparación vieja-vs-nueva del formulario SM (14.489 filas idénticas) se hizo con una copia
de `git show 7985ea2~1:programas/poblacion.py`, que NO se archiva (copia de fuente).

### `tk_tcl_intermitente/`

El `tk.tcl` intermitente de `test_gui_construccion` (sep-2026). El contexto, las rondas y
el mecanismo estan en [docs/tk_tcl_intermitente.md](../tk_tcl_intermitente.md); esto son
sus arneses. **Archivados antes de cerrar**, porque hacia falta correrlos en el PC de la
casa (Python 3.9) ademas del de trabajo (3.14).

| Script | Que prueba |
|---|---|
| `repro_tk_tcl.py` | Ronda 1: etapas S0-S5 (Tk, CTk, App, proceso fresco, paralelo, pytest real). Todo limpio fuera de pytest |
| `matriz_pytest.py` | Rondas 2 y 4: el archivo real con distintas opciones de pytest (`-s`, `--capture=sys`, el pin) |
| `handle_std.py` | Descarta que Tcl cierre los std handles al borrar un interprete |
| `repro_min.py` | Ronda 3: el bug SIN pytest, con `dup2` sobre 0/1/2 |
| `tcl_std_pin.py` | PROTOTIPO del arreglo: tres NUL privados como canales estandar de Tcl |

Corren desde la raiz del repo. `matriz_pytest.py` con la variante `pin` necesita
`PYTHONPATH=docs/evanesced/tk_tcl_intermitente` para encontrar `tcl_std_pin`. El fixture de
`repro_tk_tcl.py` lleva el RUT de ejemplo `11111111-1`.

### `epidemiologia-2.0.29/`

El inventario de Epidemiologia A04 P-U (oct-2026). El resultado esta en
[docs/epidemiologia_casillas_SA.md](../epidemiologia_casillas_SA.md); esto es lo que lo
produjo, mas la hoja de registro y la solicitud que se llevaron a la reunion de epi con el
Servicio.

| Archivo | Que hace |
|---|---|
| `cruce_epi.py` | Cruza la tabla del equipo (columnas C y G, desde la fila 7) contra `catalogos/maestro_slim.csv.gz`: calce exacto con `norm`, y si no, los 3 mas parecidos con `difflib` (cutoff 0.6). Tambien lista lo que el Maestro tiene en A04 P-U y todo lo que suena a epidemiologia |
| `limpiar_epi.py` | Arma la copia limpia de la referencia: un libro nuevo con solo los valores de celda y anchos de columna, sin creador/ultimo-modificador, y verifica que las celdas calcen 1 a 1 con el original |
| `registro_epi_a04.html` | Fuente del artifact privado (claude.ai/artifact/4S9R9QQKK3EP7spcXFnaz3): la hoja de registro por seccion y la solicitud con boton de copiar |
| `epi_docx.js` | La misma hoja en `.docx` A4 para imprimir (pag. 1 registro, pag. 2 solicitud). Node + paquete npm `docx` |

Trampas:
- `cruce_epi.py` corre desde la raiz del repo y toma la ruta de la tabla como argumento.
  Se corrio sobre el original (`ACTIVIDADES RAYEN PARA REM EPIDEMIOLOGÍA 2026 2.0.xlsx`, ya
  borrado); sobre la copia limpia de `refs_tablas/` da lo mismo, porque las celdas son
  identicas. La salida pesa ~200 KB por la lista de actividades con `COVID`: hay que filtrarla.
- El patron de `cruce_epi.py` es ancho a proposito (`NOTIFICACION`, `ANTIGENO`) y trae
  mucho ruido (examenes criticos, H. pylori). Lo que importa es el bloque `=== Tabla epi`.
- `epi_docx.js` necesita `npm install docx` en su carpeta (no estaba preinstalado) y recibe
  la ruta de salida como argumento. El render se reviso exportando a PDF con Word por COM
  (no hay LibreOffice en el PC de trabajo). El `.docx`/`.pdf` generados no se archivan
  (binarios): se regeneran con el script.
