# Code review `gui-2.0` — REGISTRO de lo revisado (act. 2026-09-19)

Revisión de la rama `gui-2.0` contra `main` (merge-base `03e15f6`, ~3200 líneas).
Sin PII. Borrar este archivo cuando la revisión esté cerrada y mergeada.

---

## ⚠ LEER PRIMERO — protocolo de esta revisión

La revisión se está haciendo con **agentes de `/code-review` corridos DE A UNO**, con
un `compact` entre cada uno. O sea: **el que revisa no recuerda las rondas anteriores.**
Este archivo es la única memoria. Por eso:

1. **Antes de reportar un hallazgo, buscarlo en §1 (corregido) y §2 (descartado).**
   Están ordenados para poder `grep`ear por símbolo (`cargar_estrat`, `after(0`,
   `root.update`, …). Si el hallazgo ya está ahí, **no volver a reportarlo**.
2. **Después de cada ronda, anotar acá lo nuevo** — en §1 si se corrigió, en §2 si se
   revisó y NO era bug. Un hallazgo revisado y no anotado se vuelve a pagar completo
   en la ronda siguiente.
3. Formato de cada línea: `símbolo o archivo:función` — qué pasaba → qué se hizo.
   El **símbolo** es lo que hace greppable el registro; sin él la entrada no sirve.
4. **Por qué de a uno:** el primer intento fue 12 agentes en paralelo y los 12 murieron
   al arrancar (límite de gasto de la API, HTTP 429), sin entregar nada. No reintentar
   el fan-out.
5. Estado del árbol: las rondas 1-4 están en **`fd1b0cc`, un commit de RESPALDO**
   (pusheado a `origin/gui-2.0` solo para no tener 5k líneas sin copia remota; **no es
   un release**: la versión sigue en **1.9.17** y la entrada del CHANGELOG sigue
   abierta — no reportar eso como hallazgo). Las rondas 5 y 6 están en otro respaldo,
   **`f42308d`**; la 7, la 8 y la 9 en **`299e7d4`**; la 10 y la 11 en **`c8aef4e`**; la 12 está sin commit encima. **296 tests verdes.**

**Foco original pedido** (sigue vigente para lo que falte): el **bug recurrente de
c38a8cc** — un export con 0 filas de datos que pasa el loader y revienta abajo con un
error críptico, o peor, da un **0 callado**, en vez de `ArchivoInvalido` sobre la
FUENTE. Ya visto en 1.9.12 (A23, NaT) y en c38a8cc (Inscritos). §1.A lo cierra para
todos los loaders conocidos; si aparece uno nuevo, va ahí. La variante **«trae filas,
pero quedan 0 TRAS un filtro»** (corte, programa, fecha ilegible, Asiste) está en §1.J;
la auditoría ESTÁTICA de cruces entre fuentes, casilleros y columnas opcionales, en §1.K;
cada referencia y fallback contra el export REAL, en §1.L; y la ALTITUD de cada arreglo (¿está donde vive la causa, o emparcha al consumidor?), en §1.M.

---

## §1 — YA CORREGIDO. No volver a reportar

119 hallazgos en 12 rondas con resultado (la 0 entregó cero). Todo verificado con
tests; ver §3.

### §1.A · Bug recurrente «0 filas» — cerrado en TODOS los loaders conocidos

Dos primitivas, una por mundo. **Regla para módulos nuevos:** si el loader es pandas,
pasa por `cargar_canonico` y ya está cubierto; si abre el worksheet a mano, tiene que
llamar `exigir_filas_ws`.

- `rem_utils.exigir_filas(filas, fuente)` — mundo `leer_xlsx` (listas de filas). En el
  grupo pandas la llama `cargar_canonico`, que además exige POR ARCHIVO las columnas
  `requeridas` (y con ellas ubica el encabezado) y las `no_vacias` (ronda 12, §1.M.1).
- `rem_utils.exigir_filas_ws(ws, header_idx, fuente)` — mundo openpyxl-worksheet. **NUEVO
  en esta revisión.**

| Símbolo | Qué daba antes | Guarda |
|---|---|---|
| `rem_utils.cargar_canonico` | 0 filas → columnas `float64` → `AttributeError` en `.str.contains()`. **Cuello de botella del grupo pandas:** cubre de una el ADA, el grupal, Inscritos, NSP y «Otros y Respi» | `exigir_filas` POR ARCHIVO, nombrándolo |
| `rem_utils.leer_xlsx` | hoja sin NINGUNA fila (ni encabezado) → `IndexError` en `filas[hi]` | `sin_datos` |
| `rem_utils.cargar_maestro` | `KeyError 'ACT'` | `sin_datos` |
| `rem_utils.trans_map` (Inscritos) | **TRANS = 0 callado** | `exigir_filas` |
| `rem_utils.atenid_multiprofesional` | composición de VDI mal, callada | `exigir_filas` |
| `rem_saludmental._preparar` (A05 N/O) | 0 eventos con cara de resultado legítimo. La guarda de `mes_vacio` **no** cubría «Archivo completo» (`mes=None`) | `exigir_filas_ws` |
| `rem_a03_d3_instrumentos.abrir_validado` | tabla D.3 entera en 0 | `exigir_filas_ws` |
| `estamentos.cargar_estamentos` («Utilización de Cupos») | todos sin estamento **y pisaba el caché con un dict vacío** | `exigir_filas_ws` |
| `rem_a23_respiratorio.cargar_estrat` | sin col. RUT → `TypeError` en `f[None]`; solo header → gravedad de TODOS en `""` vía `_gate` → **SALA en 0 callado**. No tenía NINGUNA guarda | `sin_columnas` + `exigir_filas` |
| `poblacion.cargar_inscritos` | `AttributeError` en col. PROTECCION NIÑEZ (el bug de c38a8cc) | `sin_datos` |
| `poblacion.cargar_formulario_sm` | `AttributeError` | `sin_datos` |
| `poblacion.construir_poblacion` (ADA) | `AttributeError`. La familia población no pasa por `filtrar_mes` | `sin_datos` |

### §1.B · Trampas de hilos y de Tk (GUI 2.0)

- **`frame.after(0, ...)` DESDE el worker** en `a05.bloque_archivo_formato._detectar` y
  `sm._chequeo_cruce` → `Tk.after` no es thread-safe (registra un comando Tcl):
  `RuntimeError: main thread is not in main loop`, o corrupción intermitente de Tk.
  **Arreglo:** `runner.en_hilo(widget, trabajo, al_terminar)` — cola + poll, el mismo
  patrón que `correr_con_reloj` ya usaba a propósito. **Si ves otro `after(` llamado
  desde un hilo, ESO sí es nuevo: reportarlo.**
- **Carrera de dos elecciones de archivo** en el A05: dos hilos en vuelo y el resultado
  del archivo VIEJO se pintaba sobre el nuevo → podía colar un **Administrativo como
  IRIS**. Arreglo: la categoría se guarda junto a la RUTA para la que se calculó
  (`estado = {"ruta":…, "categoria":…}`) y la que no corresponde se descarta.
- **`root.update()` en `dialogos.dotacion_ada`** → despacha TODOS los eventos
  pendientes, así que un segundo click en Procesar ya encolado **reentraba en
  `on_procesar`**: dos diálogos de dotación y dos workers escribiendo el MISMO archivo
  de salida. Arreglo: `update_idletasks()` (solo repinta) + el botón se deshabilita en
  `app.on_procesar` **antes** de `preparar`, y se rehabilita si `preparar` aborta.

### §1.C · Empaquetado del .exe (`autoREM.spec`)

- **Sidebar VACÍO:** `gui/registro.py` descubre las páginas con `pkgutil.iter_modules` y
  nadie importa `gui.paginas.*` por nombre → PyInstaller no las empaquetaba.
  Arreglo: `collect_submodules('gui.paginas')` + `cargar_registro()` ahora **falla
  ruidoso** si no encuentra ninguna (antes: ventana vacía con cara de funcionar).
- **Temas de `customtkinter`:** `collect_data_files('customtkinter')` (sin eso el exe
  revienta al importar ctk).
- **`tools.scan_catalogo`:** lo importa `about.py` para escanear un catálogo DEIS antes
  de aceptarlo, y `tools/` no se empaquetaba → `ModuleNotFoundError`. Arreglo:
  `tools/__init__.py` (nuevo) + hiddenimport; y si igual faltara, el botón **avisa y no
  carga el catálogo sin escanear** (regla 1).
- `autorem._slim_por_defecto` buscaba el Maestro slim en `refs_tablas/` después de
  moverlo a `catalogos/`; el `.spec` además lo copiaba dos veces.

### §1.C-bis · Layout del sidebar — la posición era orden de EJECUCIÓN, no un dato

Los dos hallazgos de esta sección tienen la misma causa raíz, y es la excepción a lo
declarativo del resto de la arquitectura (`PANTALLA` descubierto por introspección,
`ORDEN_PROGRAMAS`, `TAREA`, `COBERTURA`): **la posición de un widget en el sidebar era
una propiedad emergente del orden de las sentencias**, sin nada que la declarara.

- **`app._grupo_colapsable`: la cabecera del programa se dibujaba DEBAJO de sus páginas**
  («SALUD MENTAL» bajo sus propios botones) en el PRIMER dibujo. `pack` apila en orden de
  LLAMADA, no de creación: `contenido` se tiene que CREAR antes que `header` (la closure
  `alternar` lo necesita) y se empacaba en la misma línea. El síntoma se auto-corregía al
  colapsar/expandir, porque `alternar` llama `contenido.pack()` de nuevo y ahí sí cae al
  final de la pila — de ahí lo desconcertante del bug. Arreglo: `contenido.pack()` va
  **después** de `header.pack()`, con el porqué en el docstring.
- **`PAGINAS_ESPECIALES`: Inicio y Acerca de no estaban ancladas.** Su posición era «donde
  caiga el bucle dentro de `_construir_sidebar`» (después de los grupos) más el orden
  interno del tuple. Nada decía «Inicio va al tope», así que sumar un programa a
  `ORDEN_PROGRAMAS` o reordenar el tuple las movía **en silencio**. Arreglo: la posición
  pasa a ser un DATO (`posicion`: `"arriba"` | `"abajo"`), Inicio fija al tope y Acerca de
  al pie; el toggle de tema queda bajo Acerca de (es un control, no una página).

Los dos tests nuevos miran el orden REAL en pantalla (`pack_slaves()` para el apilado,
`winfo_rooty()` para el anclaje) y se comparan contra los botones de PANTALLA, no contra
índices fijos: siguen valiendo cuando se sume una página. Se verificó que **cada uno falla
al reintroducir su bug** y que ningún otro test se cae con ellos.

### §1.C-ter · Lo mismo, un nivel más abajo: el orden de las páginas dentro del grupo

Tercera aparición de la clase de §1.C-bis, encontrada por la ronda 4 (auditoría de
comportamiento removido): **el orden de las páginas DENTRO de su grupo salía del nombre
del archivo `.py`**. `registro.cargar_registro` ordenaba por `(programa, orden en que
pkgutil encontró el archivo)`, y `pkgutil.iter_modules` va alfabético. `autorem.lanzar_gui`
sí lo declaraba, como secuencia de sentencias: `_tab_a05` → `_tab_a03` → `_tab_a23` →
`_tab_sm` → `_tab_beta`.

Hoy A05 va antes de Actividades **por casualidad**: `"a05" < "sm"`. Renombrar `sm.py` a
`actividades.py` —que es el rename natural, porque el título de la página *es*
«Actividades»— las daba vuelta en silencio, y una página nueva de Salud Mental entraba
donde le tocara alfabéticamente.

Arreglo: `registro.ORDEN_PAGINAS`, hermano de `ORDEN_PROGRAMAS`, con el mismo fail soft
(una página no declarada cae al final de su grupo, y ahí desempata el orden de archivo
para que el resultado sea determinista) y el mismo fail loud en los tests.

**Ojo con el test:** el primero que escribí solo comprobaba que cada `id` **estuviera**
declarado en `ORDEN_PAGINAS`, y sobrevivió a quitarle la clave de orden al `sorted` —
porque con los nombres de archivo actuales el orden alfabético y el declarado **coinciden**,
así que el registro real no puede distinguir una implementación de la otra. El test bueno
parchea `_paginas_encontradas` para que devuelva las páginas **al revés** y exige que el
orden declarado gane igual.

### §1.D · Mensajes y validación de la GUI

- **`runner.valida_mes` (NUEVO)** — el mes se validaba solo con «¿son números?»
  (`app._resolver_ctx`: `if mes is None`), **no por rango**. El `ttk.Spinbox` acota
  únicamente sus FLECHAS: un mes `13` **tecleado** llegaba al worker y reventaba recién
  en `rem_utils._rango_mes` con `ValueError: month must be in 1..12`, que
  `manejar_error` no reconoce → «Error inesperado … pásaselo a Simón» (un typo
  presentado como bug), y después de cargar los archivos. Un año de 2 dígitos (`26`)
  era peor: no revienta, se va a `filtrar_mes` y sale «no hay filas de 07/0026»,
  culpando al export. `_tab_a05` y `_tab_beta` validaban el rango en `autorem.py`; el
  port a `widgets.selector_mes` lo perdió para todas las páginas menos A05. Ahora una
  sola función, usada por `_resolver_ctx`, `dialogos.bloque_dotacion._precargar` y
  `a05.preparar`. `widgets.ANIO_MIN`/`ANIO_MAX` son la ÚNICA fuente del rango (Spinbox
  + guarda), con un test que impide que divergan.
- **`widgets.fila_archivos` no se podía VACIAR** (solo sobreescribir: el diálogo
  cancelado deja la selección anterior). Eso dejaba **sin salida la corrida
  solo-cuestionarios** de SM, que exige «ni ADA ni Grupal» (`sm._es_solo_a03`): un
  click accidental en «Examinar…» sobre el ADA la volvía inalcanzable **hasta
  reiniciar autoREM**, porque las páginas no se destruyen al cambiar de pantalla
  (`App.mostrar`). Arreglo: botón **«Quitar»**, que avisa con `on_elegido([])`.
- **`BannerFuente` sobrevivía a la corrida que lo pintó.** Lo pinta `al_completar`, así
  que: (a) al elegir otro archivo el banner VERDE seguía afirmando «A/D/A de IRIS
  completo» al lado de un export parcial recién cargado; (b) si la corrida siguiente
  fallaba, `al_completar` no corre y quedaba el veredicto de la anterior. El color es
  una AFIRMACIÓN sobre la fuente (plan §5.1 regla 1), no decoración. Arreglo:
  `app.pintar_input` apaga el banner ante cualquier cambio de input (el hook va en el
  SHELL porque el input dueño del banner —A23 `atenciones`— no tiene `on_elegido`
  propio), `on_procesar` lo apaga al arrancar (junto con el log, mismo motivo), y
  `pintar_banner_fuente(df=None)` oculta en vez de dejar lo de antes.
- **`about._volver_a_embebido` llamaba `catalogos.cargar` SIN `try`**, al revés que su
  hermano `_cargar_manual`. `cargar` levanta `FileNotFoundError` si falta el catálogo
  embebido (caso que `refrescar` ya contempla); en un botón Tk de un exe `--windowed`
  esa excepción **no se ve en ninguna parte**: el botón parecía no hacer nada y
  `_OVERRIDES` seguía diciendo «cargado a mano» sobre algo que ya no estaba en el
  caché.
- **`sm.py` afirmaba que `_tab_a03` estaba «YA BORRADA de autorem.py»** — y no lo está:
  sigue definida (`autorem.py:999`) y montada en `lanzar_gui` (`autorem.py:208`), que
  es la GUI que corre el exe. Se borra en el paso 11. Importa el tiempo verbal: §2 de
  este mismo documento cierra la pregunta del resolver de estamentos comparando contra
  `_tab_a03`, y quien ejecute el paso 11 necesita saber que hoy conviven.

- `runner.manejar_error`: volvió el **mapa de títulos por `ArchivoInvalido.categoria`**
  (`_TITULO_INVALIDO`), que vivía dentro de `_tab_a05` y se perdió al centralizar el
  despacho. Ahora lo comparten todas las páginas e incluye las categorías nuevas.
- `runner.manejar_error`: el `ImportError` mandaba a instalar **pandas** siempre, aun
  cuando lo que faltaba era otra librería. Ahora usa `e.name`, y si la excepción se
  levantó a mano (sin `.name`) muestra su texto tal cual.
- **Ruta tecleada/pegada en el A05:** no pasa por «Examinar» → `on_elegido` nunca corría
  y salía «Formato no reconocido» **sobre un archivo perfecto**. Arreglo:
  `detectar_ahora()`, que `preparar` llama antes de procesar.
- **Arrastrar el .xlsx sobre el exe** volvió a precargar la ruta: el `ruta_inicial` de
  `_tab_a05` no tenía canal en el shell nuevo. Arreglo: `gui.app.lanzar(ruta_inicial)`
  → `App(ruta_inicial=)` → `Pagina.datos["ruta_inicial"]`.
- **`motivo_obligatorio`** (nueva clave opcional de `inputs`): el aviso genérico «Carga
  al menos un archivo: X» había perdido el POR QUÉ que el aviso a mano sí daba. Puesto
  en Otros Crónicos (A23), Grupal (SM) y Formulario SM (población).
- **A03·D.3:** el nombre del archivo lleva el mes pero el módulo **no filtra por mes**
  (no tiene ninguna lógica de mes). Se avisa en el log en vez de dejar un archivo que
  promete un período que su contenido no respeta.
- `error_inesperado` perdía el traceback del worker (`format_exc()` no sirve ahí).
- Excepciones en `preparar` / `al_completar` / `resumen` eran invisibles (Tk se las
  traga) → ahora pasan por `manejar_error`.
- Detección de formato del A05 con `read_only=True`: la `<dimension>` ausente o rota de
  RAYEN hacía **rechazar un archivo válido**. Ahora sin `read_only`, igual que
  `sm.abrir_validado`, que es quien procesa después. **[Superado:** la ronda 4 volvió a
  `read_only` para leer solo el encabezado (§1.E-bis) y reabrió este bug; la ronda 5 lo
  cerró de verdad con `rem_utils.abrir_xlsx_ro`, ver §1.F.**]**
- Banner / acuse / caja de cuestionarios se empacaban tarde y quedaban **bajo el botón
  Procesar** → `pack(after=…)`.
- SM solo-cuestionarios: la salida (que lleva RUT) iba al cwd, o sea **al repo** →
  `carpeta_defecto`.

### §1.D-bis · Comportamiento REMOVIDO por el port (ronda 4)

Ángulo: qué hacía `autorem.py` que la GUI 2.0 dejó de hacer. Tres hallazgos, más el
doble parseo de §1.E-bis.

- **`a05._leer_categoria` aplastaba tres errores distintos en uno.** Tenía un
  `except Exception -> "error_lectura"`, y `preparar` despachaba eso como **«Formato no
  reconocido»** con `sm._MSG_DESCONOCIDO` (que habla de las firmas del export). O sea:
  - un `.xls`/`.html` disfrazado de `.xlsx` (el clásico de RAYEN, CLAUDE.md §13 lo
    declara «ya manejado con el diálogo No es un .xlsx») → se le decía «no encontré las
    firmas, vuelve a descargarlo sin modificarlo», sobre un archivo que puede estar
    impecable y cuyo arreglo real es «Guardar como → .xlsx». Verificado: openpyxl levanta
    `zipfile.BadZipFile`, y `runner.es_error_formato` **sí** lo clasifica bien.
  - abierto en Excel / bloqueado por OneDrive (`PermissionError`) → mismo mensaje
    equivocado, en vez de «Permiso denegado».
  - falta `openpyxl` (`ImportError`) → mismo mensaje equivocado; `_tab_a05` lo avisaba en
    el log con el `pip install` (`if not sm.OPENPYXL_OK`), y eso no tenía contraparte en
    ninguna parte de `gui/`.

  Las tres ramas **siguen implementadas** en `runner.manejar_error` y quedaban muertas
  para esta página, porque `preparar` abortaba antes de que corriera el worker. Arreglo:
  la excepción VIAJA (`estado["error"]`, `detectar_ahora()` devuelve `(categoria, error)`)
  y la clasifica quien sabe. El banner usa `runner.motivo_fuente`, que sale del **mismo
  árbol de `isinstance`** que `manejar_error`: si alguien agrega una rama en uno y no en
  el otro, el color y el diálogo empiezan a contradecirse, que es lo que §5.1 del plan
  prohíbe.
- **La salida por defecto de Población se había mudado de carpeta.** `_tab_beta` guardaba
  junto al **Inscritos** (`defecto=entrada.parent`), que es el snapshot del mes reportado.
  El defecto genérico de `_resolver_ctx` es «el primer input CARGADO», o sea el orden en
  que están *escritos*, y Población los declara en el orden numerado de sus instrucciones
  (1. Formulario histórico, 2. ADA, 3. Inscritos) → el P6 y el Rescate del mes se iban en
  silencio a la carpeta del histórico multi-año, que es justo la que se tiene archivada
  aparte. No viola la regla 1 (sigue fuera del repo, junto a un input), pero el usuario
  tiene que ir a buscarlos. Arreglo: `ancla_salida` en el contrato de `inputs` — la
  carpeta ancla es un DATO, no una posición en la lista (misma cura que §1.C-bis/ter).
  A23 y SM no estaban afectadas: su primer input declarado es el mismo archivo que usaban
  las pestañas viejas.
- **El desglose por instrumento del A03·D.3 se perdió.** `_correr_a03` imprimía
  «60 aplicaciones (PSC: 20 · PSC-Y: 18 · GHQ-12: 22)»; la corrida solo-cuestionarios
  dejó solo el total, aunque `procesar_unificado` seguía devolviendo `por_instrumento` (se
  descartaba). No es decoración: los 3 slots fijan el instrumento **a mano**, sin
  autodetección, así que cargar el export del PSC-Y en el slot del PSC no lo caza nadie —
  el desglose es lo único que lo delata antes de copiar la D.3 al SA_26, y un total pelado
  tapa igual un 20/20/20 que un 60/0/0.

  **Ojo con el test:** el primero probaba `_por_instrumento` con un dict a mano y
  sobrevivió a quitar la línea que lo puebla. El bueno corre `sm.correr` de verdad en modo
  solo-cuestionarios, con `procesar_unificado` y `estamentos.tabla_efectiva` stubbeados.

### §1.E-bis · El A05 leía el export COMPLETO dos veces por corrida

Un click en «Examinar…» hacía `load_workbook(ruta, data_only=True)` **sin `read_only`** —
parseo completo del export— solo para mirar el encabezado, y después el worker lo parseaba
otra vez en `sm.abrir_validado`. La GUI 1.x hacía una sola lectura (no detectaba nada).

El comentario que justificaba el parseo completo era correcto pero sacaba la conclusión
equivocada: «SIN read_only: en ese modo `max_row` sale de la `<dimension>` del xlsx, que
RAYEN a veces trae ausente o rota». El problema es **`max_row`**, no `read_only`:
`rem_utils.leer_xlsx` y `verificar_hoja_unica` —los lectores canónicos del proyecto,
documentados como «ROBUSTO a la dimension rota»— usan `read_only=True` y **nunca**
`max_row`: iteran y cortan por cuenta propia. `formatos.detectar_eje` sí dependía de
`ws.max_row` (`tope = min(ws.max_row, MAX_FILAS_HEADER)`), y de ahí venía la obligación.

Arreglo: `formatos.detectar_eje_filas` (mismo veredicto, sobre filas ya leídas) +
`sm.detectar_formato_filas`; `detectar_eje(ws)` delega, así sus otros 3 callers no cambian.
La detección lee con `read_only=True` + `islice(..., MAX_FILAS_HEADER)`. Tests que amarran
que el atajo **no cambie la respuesta** sobre los dos exports A05 reales del repo.

> ⚠ **La premisa de esta sección era FALSA** (la cazó la ronda 5, §1.F). En modo
> `read_only`, `iter_rows` **también** sale de la `<dimension>`: `_cells_by_row` hace
> `max_row = max_row or self.max_row` y corta ahí. «Nunca `max_row`» no protegía de
> nada, y `leer_xlsx`/`verificar_hoja_unica` no eran robustos: truncaban callados. Este
> arreglo reabrió el bug que §1.D ya había cerrado; los dos exports reales del repo
> traen la `<dimension>` bien, así que sus tests no lo podían ver. Lección: un test de
> «robusto a X» tiene que **fabricar X** y comprobar que el fixture de verdad lo arma.

### §1.F · Trazado entre archivos (ronda 5)

Ángulo C: cada llamada de `gui/` hacia `programas/`/`modulos/`/`autorem.py`/`tools/`,
contra la firma, la forma de retorno, las excepciones y las precondiciones del callee.
Cinco hallazgos, los cinco corregidos y con test mutado (10 mutantes, 10 cazados).

1. **`rem_utils.leer_xlsx` truncaba EN SILENCIO con la `<dimension>` rota** — el peor.
   `A1:D5` en una hoja de 10 filas → 4, sin error. Es el cuello de botella del grupo
   pandas (ADA, grupal, NSP, Otros y Respi, Inscritos, Multiprofesional): conteo de MENOS
   con cara de legítimo. Su docstring decía lo contrario, y culpaba a pandas, que lee
   las 10 (llama `reset_dimensions()` por dentro). Arreglo: **`rem_utils.abrir_xlsx_ro`**
   (read_only + `reset_dimensions()` en cada hoja) + **`filas_hoja`** (rellena al mismo
   ancho, porque sin `<dimension>` las filas llegan desparejas). **Regla: toda lectura
   `read_only` pasa por ahí** (anotada en `programas/CLAUDE.md`). Cubre también
   `verificar_hoja_unica` (una tabla dinámica fuera de la `<dimension>` de su hoja
   pasaba por vacía), `catalogos._hojas` y **`tools/scan_catalogo`** — un RUT fuera de
   la etiqueta **pasaba el escaneo de PII** del About.
2. **`a05._leer_categoria` rechazaba un IRIS válido con la `<dimension>` rota** (y
   `sm._header_rapido` no acusaba el cruce). Regresión de la ronda 4, ver el ⚠ de
   §1.E-bis. Mismo arreglo.
3. **`rem_utils.cargar_canonico` clasificaba la FUENTE mirando solo el PRIMER archivo**
   (`col0`). [IRIS, Monitoreo] → «plena», banner VERDE y sin aviso en LEEME sobre filas
   sin demografía; [Monitoreo, IRIS] → «parcial». Ahora por archivo, gana el peor, y
   `attrs['fuente_mezcla']` + `formatos.aviso_fuente(archivos=)` nombran los afectados y
   dicen que lo suyo sale de MENOS (no en 0).
4. **Ruta pegada con comillas en el A05** («Copiar como ruta de acceso» de Windows):
   `valida_ruta` las sacaba, la detección no → `InvalidFileException` → «No es un .xlsx
   real» sobre un archivo perfecto. **`runner.limpiar_ruta`**, usado por la validación,
   la detección (`_ruta_caja`) y los inputs opcionales de `_resolver_ctx`.
5. **Funcionario SIN estamento** → el diálogo de dotación lo mostraba como el grupo
   «(sin estamento)», cuyo «Omitir» no guardaba nada (`dotacion.omitir` descarta la
   clave vacía) aunque el grupo desaparecía. **Decisión del autor:** RAYEN no puede
   registrar eso, así que es un export modificado → **`rem_utils.exigir_estamento`** en
   `cargar_atenciones`, `ArchivoInvalido('sin_estamento')` nombrando a quién. Sobre la
   FUENTE (§3.1), no en el diálogo. Una fila sin funcionario no dispara.

**Revisado y NO era bug** (ronda 5): firmas/retornos/attrs de `_correr_tareas`,
`_resumen_texto`, `buscar_tarea`, `perfil_por_id`, `smact.procesar` (`d=` es el ADA
COMPLETO, que es lo que devuelve `dotacion_ada`), `tpmod.procesar` (maestro como str),
`procesar_unificado`, `tabla_efectiva`, `a23.procesar` + `seccion_g`, `rescate.procesar`
con DataFrames precargados + `P`/`fuentes`, `dotacion.evidencia`/`nuevos`/`por_estamento`.
`ArchivoInvalido` hereda de `Exception` (no de `ValueError`), así que los
`except ValueError` de `trans_map`/Multiprofesional no lo tragan. `maestro_slim.csv.gz`
en `catalogos/` no confunde a `catalogos.cargar`/`fuentes` (buscan por nombre).
`tools.scan_catalogo` se empaqueta, y el hook que importa no tiene efectos al importar.

### §1.G · Trampas de Tk / customtkinter / hilos (ronda 6)

Ángulo D (trampas de lenguaje y framework). customtkinter **6.0.0 SÍ está instalado**
en el Python 3.9 local (`site-packages/customtkinter`): se verificó contra su fuente,
no de memoria. Nueve corregidos, con test mutado (37 mutantes, 37 cazados).

1. **`dialogos.dialogo_dotacion` → `ctk.CTkToplevel(root)` hace un `update()` COMPLETO
   en su constructor** (Windows, `_windows_set_titlebar_color`: withdraw + update). Eso
   despachaba los clicks encolados durante la carga del ADA, y **reabría el agujero de
   §1.B** que `update_idletasks()` había cerrado. Solo Procesar estaba deshabilitado: un
   «Revisar/Precargar dotación…» se abría ANIDADO con otra copia de la tabla; el
   «Aplicar» de afuera (`dotacion.guardar` escribe el dict entero) revertía lo de
   adentro, y la corrida usaba la tabla vieja (externo → interno, doble conteo).
   Arreglo: candado `_DOTACION_ABIERTA` en `dotacion_ada` y `revisar_dotacion`. **Ojo:
   cualquier `CTkToplevel` bombea eventos**; un modal nuevo necesita el mismo cuidado.
   Premisa amarrada por `test_ctktoplevel_despacha_los_clicks_encolados`.
2. **`widgets.etiqueta_envolvente` escalaba el `wraplength` DOS veces**: `e.width` ya
   viene escalado y `CTkLabel.configure(wraplength=)` aplica `_apply_widget_scaling`. Al
   150% de Windows el texto pedía 787 px en una caja de 570 y se cortaba (incluido el
   mensaje del BannerFuente). Arreglo: `_reverse_widget_scaling`.
3. **`app.on_procesar`: el banner de fuente se pintaba aunque los inputs hubieran
   cambiado DURANTE la corrida** (solo Procesar se deshabilita). Arreglo: foto de los
   getters al arrancar; si difieren al terminar, no se pinta y se dice en el log.
4. **`sm._chequeo_cruce` sin descarte de resultados viejos**, el gemelo de la carrera
   del A05 (§1.B): pintaba el hilo que terminara último, y «Quitar» con un hilo en vuelo
   dejaba el banner rojo sobre una casilla vacía. Arreglo: `runner.Canal` +
   `en_hilo(..., canal=)`. **El patrón** (resultado asíncrono pintado sobre una
   pantalla que ya cambió) está documentado en `runner.Canal`, con sus tres apariciones.
5. **Un paso opcional que fallaba solo se decía en el log** (A03·D.3 dentro de SM,
   Trabajo Perdido, Rescate), y la salida de una corrida ANTERIOR del mismo mes seguía
   ahí con el mismo nombre. Arreglo, por decisión del autor: **las salidas nunca se
   sobreescriben** (`rem_utils.rutas_libres`: toda la corrida sale como `… (n)` con el
   MISMO número), y el resumen dice «NO se generó (motivo)».
6. **Cerrar la ventana con una corrida viva** la mataba sin avisar (worker `daemon`,
   sin `WM_DELETE_WINDOW`), incluso escribiendo el `.xlsx`. Arreglo, sin timeout:
   `App._al_cerrar` pregunta si hay corridas vivas (`App._corridas`, «No» por defecto),
   y **toda salida se escribe vía `rem_utils.escribir_atomico`** (temporal +
   `os.replace`): un corte deja un `….escribiendo.xlsx`, nunca un `.xlsx` roto con
   nombre de resultado.
7. **`rem_utils.verificar_hoja_unica`: `wb.close()` sin `finally`** — una excepción a
   mitad de la lectura dejaba el export bloqueado mientras seguía abierto el diálogo.
8. **`dotacion.guardar` / `estamentos.guardar_cache` fallaban CALLADO** (el `print` no se
   ve en el exe), y **leer un caché dañado daba tabla vacía** → todos los externos
   volvían a contar. Arreglo (segunda pasada, encolada por el autor):
   `rem_utils.leer_cache_json` / `guardar_cache_json` / `apartar_cache` + la cola
   `_AVISOS_CACHE` que la GUI muestra (`runner.avisar_cache`, al cerrar los diálogos de
   dotación, tras `preparar` y al terminar cada corrida).
   - Dañado → se aparta como `.corrupto-<fecha>.json`.
   - Ilegible → NO se sobreescribe.
   - Bloqueo pasajero → se reintenta.
   - Escritura vía temporal.
   - Re-leer y fusionar al guardar (`dotacion._persistir`, `quitar_omision`).

   **Decisión: sin carpeta de respaldo** (partiría la tabla en dos). «Acerca de» →
   «Preferencias guardadas» + una línea en cada caja (`dialogos.REF_PREFERENCIAS`). El
   perfil temporal de Windows NO se puede detectar desde adentro: por eso la sección
   muestra dónde está el caché y cuándo se guardó.
9. **La suite pisaba el `~/.autorem/dotacion.json` REAL** —
   `test_externos_delta_y_detalle_conserva_filas` guardaba sin redirigir, y corría antes
   que el único test que redirigía. Arreglo: `tests/_aislar_cache.py`, importado primero
   por todo test, y `test_todos_los_tests_aislan_el_cache_del_usuario` lo exige.

### §1.H · Envoltorios e indirecciones (ronda 7)

Ángulo E: cada envoltorio (`Pagina`, `getters`/`_resolver_ctx`, los de `runner`, los
diálogos de dotación, el override de catálogos del About, el descubrimiento de
`registro`) ¿llega al destino correcto, con todo lo que usa quien llama? Con repros.

1. **`dialogos.dialogo_dotacion` / `_revisar_dotacion`: «Aplicar» mandaba TODOS los
   ticks a `dotacion.marcar`** — la foto de cuando se abrió la ventana se escribía sobre
   el disco, y el re-leer-y-fusionar de §1.G.8 no servía para los nombres que el diálogo
   mostraba: otra ventana marca externa a Ana, esta aplica sin tocarla → Ana vuelve a
   interna y cuenta en el REM. (El test de §1.G.8 usaba nombres disjuntos llamando a
   `marcar` directo, así que no lo veía.) Arreglo: `dialogos.decisiones_cambiadas` (solo
   lo que difiere de la tabla abierta; un `desconocido` sin tick SÍ cuenta: queda
   interno) vía `_aplicar_ticks`, en los dos diálogos.
2. **`about._cargar_manual` + `catalogos.cargar`: el override de sesión no llegaba a
   nadie** — `_CACHE` va por `(nombre, str(entrada))`; el About cargaba con `entrada=` y
   toda consulta (`existe`, `descripcion`, `_cruzar`, `anotar`, el futuro `en_rango`)
   llama sin ella → clave `(nombre, 'None')` = el embebido. «Volver al embebido» recargaba
   una clave nunca pisada. Arreglo: `catalogos._SESION` + `usar_en_sesion` / `en_sesion`,
   un paso de la cascada solo en memoria (persistirlo sigue siendo de `main`); el About
   ya no lleva su propio `_OVERRIDES`. De paso, `cargar(entrada=<no existe>)` caía
   CALLADO al embebido: ahora `FileNotFoundError`.

Revisado y limpio en esta ronda: `pagina.log` nunca llega al worker (solo `preparar` /
`dotacion_ada`, hilo GUI; `ctx` no lleva log); `Pagina.mes()` da None sin `SelectorMes`
y su único usuario (SM) lo tiene; `get_ada` da `list[str]` y `cargar_atenciones` acepta
lista; `quitar_omision`/`omitir` sin clave `omitidos[modulo]`; ninguna `key` de extra
choca hoy con un input, `mes` o `carpeta` (el `"carpeta"` del A05 convive con
`carpeta_salida: False`); `runner.abrir_carpeta`/`slim_por_defecto` = sus pares;
`pkgutil.iter_modules` en el exe (PyInstaller lo soporta sobre el PYZ; el hueco real es
`gui.app` fuera del bundle, ya en §4).

### §1.I · Reuso (ronda 8)

Código nuevo que re-implementaba algo que ya existía. En 3 de los 5 la copia ya se
había apartado del original.

1. **`runner.slim_por_defecto` / `autorem._slim_por_defecto`: cada GUI con su lista a
   mano** de dónde buscar el Maestro slim, y ninguna miraba `<exe>/catalogos/` (donde
   `catalogos._carpetas` busca los drop-in) → un maestro dejado ahí se ignoraba, el TP
   caía callado a la heurística y el About decía «no encontrado». El docstring de
   `_carpetas` juraba «mismo criterio». Arreglo: `catalogos.maestro_slim` (las carpetas
   de `_carpetas` + suelto junto al exe); las dos GUI la llaman.
2. **`widgets.fila_carpeta_salida` / `dialogos.bloque_estamentos`: limpiaban la ruta a
   mano** (sin el `.strip()` final de `runner.limpiar_ruta`), y la de Cupos no pasaba
   por NINGUNA validación: mal tecleada, `FileNotFoundError` al final de la corrida SM,
   con SM y TP escritos y la D.3 en `fallo_a03`. Arreglo: `limpiar_ruta` en los dos
   getters + `sm.preparar` la valida con `runner.valida_ruta` si viene.
3. **`dialogos.revisar_dotacion`: copia del candado de `dotacion_ada`**, que callaba el
   aborto (la otra lo loguea). Arreglo: `_una_ventana_dotacion` (contextmanager, uno
   para los dos); `_modal` + `_barra_aplicar` para la ventana y la barra repetidas.
4. **`a05.bloque_periodo`: copia de los Spinbox y del parseo de `widgets.selector_mes`**,
   fuera del test que amarra `ANIO_MIN/MAX`. Arreglo: usa `selector_mes(etiqueta=None)`
   y prende/apaga `get.spinboxes`; `preparar` ya no parsea.
5. **`sm._header_rapido`: copia del criterio de encabezado de `leer_xlsx`** (">3 celdas
   llenas"); y tres copias de abrir/`filas_hoja(ws, n)`/cerrar (A05, SM, un test).
   Arreglo: `rem_utils.indice_encabezado` (lo usan `leer_xlsx` y el preview) y
   `rem_utils.primeras_filas`.

Revisado y limpio en esta ronda: `sm.al_completar`/`a23.al_completar` y el banner ya
comparten `widgets.pintar_banner_fuente`/`bloque_banner_fuente` (§1.E); la validación de
mes pasa toda por `runner.valida_mes`; `about._ruta_licencia` no tiene par (y el LICENSE
va junto al exe, §9). Los pares `runner` ↔ `autorem.py` siguen siendo el hallazgo #14.

### §1.J · Bug recurrente, variante «vacío TRAS un filtro» (ronda 9, empírica)

§1.A cierra el export con 0 filas. Esta ronda corrió cada página contra exports que SÍ
traen filas pero ninguna sobrevive al corte / máscara de programa / parseo de fecha /
Asiste. Repros en el scratchpad de la ronda (`r1/h1..h5.py`), 11 mutantes cazados.

1. **`rem_a23_respiratorio._seccion_g`: `if pd.isna(e): continue`** — sin FECHA DE
   NACIMIENTO legible (o sin la columna: `_resolver_otros` la deja opcional) el
   inasistente se descartaba; la G entera daba «ninguno» sin aviso. → edad del ADA como
   respaldo (`edad_extra=fer["Edad"]`); si tampoco, umbral `_UMBRAL_ADULTO` (solo <2
   años difiere) + aviso `REVISAR` con el conteo (`sin_edad`).
2. **`poblacion._verificar_cobertura_fechas`: solo miraba `form_max < corte`** — un
   formulario (o ADA) con TODO posterior al corte daba 0 ingresados con `avisos=[]`. →
   `ArchivoInvalido("mes_vacio")` si `min > corte`, para las dos fuentes.
3. **Ídem, sin UNA fecha legible** (`form_min is None` → se saltaban todos los chequeos)
   → `ArchivoInvalido("sin_fecha")`, las dos fuentes.
4. **`rem_sm_actividades.procesar`: E vacío tras `filtrar_mes`** (ADA del mes, nada SM:
   bajado filtrado por otro programa) → todo el REM SM en 0 con «Listo». →
   `ArchivoInvalido("sin_datos")` si `len(E) == 0`. Una casilla en 0 sigue siendo legítima.
5. **`rem_a23_respiratorio.cargar_otros`: `pd.to_datetime` pelado** → NaT callado, y sin
   ninguna fecha el chequeo de historial de la G (`od["FECHA"].notna().any()`) se
   saltaba. → `fecha_col` (cuenta las ilegibles) + `sin_fecha` si no queda ninguna.
6. **`gui/paginas/poblacion.resumen` no mostraba `P.attrs["avisos"]`** — los avisos de
   cobertura no bloquean a propósito (§3.1 de programas/CLAUDE.md), así que tienen que
   verse: quedaban en el log y la LEEME, con un «Listo» idéntico al de una corrida
   completa. → el resumen los lista.
7. **`rem_sm_actividades.procesar`: `gm[gm["ASISTE_n"] == "SI"]`** leía una ASISTE en
   blanco o «S» como NO → A27 / A06 grupal / A19a grupal en 0. → toda la columna sin
   SI/NO del mes = `sin_datos`; algunas filas = aviso `SUBCONTADO`. Un NO explícito
   sigue siendo 0 legítimo.
8. **`dialogos._dotacion_ada`: «sin funcionarios nuevos que clasificar»** con `trib`
   vacío (nada del mes tributa) se leía como «todo en orden». → log propio.

**Un fixture era el bug:** `test_cobertura::test_avisos_sin_grupal_aparecen_en_la_hoja`
armaba un SM entero en 0 (`instr="Medico(a)"`, y A04 exige `MEDICO` exacto) y verificaba
sus avisos. Se corrigió el fixture, no la guarda.

Revisado y limpio: 0 filas en todos los loaders (§1.A se sostiene); grupal / NSP de
otro mes y NSP sin fechas legibles → `mes_vacio` (vía `filtrar_mes`); Multiprofesional
sin ninguna fila marcada y Inscritos sin TRANS → avisan; Trabajo Perdido con 0 a saco roto
es un resultado legítimo; Estratificación sin cruce de RUT es un dato, no una fuente vacía;
el A05 detecta sobre `primeras_filas` (un `abrir_xlsx_ro` + `detectar_formato` pelado
revienta en `ws.max_row=None`, pero ninguna ruta de la GUI lo hace).

**Segunda pasada (sin tope), 9 más** — 13 mutantes cazados (`r1/h6.py`, `h7.py`):

9. **`rem_a03_d3_instrumentos.procesar`: momento fuera de Ingreso/Egreso** (columna
   `1.- ESTADO` ausente, en blanco u otro vocabulario) → la D.3 ENTERA en 0 con «N
   aplicaciones» en el resumen. → todas = `ArchivoInvalido`; algunas = aviso SUBCONTADO.
10. **Ídem, sin puntaje pero con RESULTADO de RAYEN** → fuera del D.3 callado. → nuevo
    campo `nivel_d3` (DISAM, o la banda de RAYEN si no hay puntaje) + aviso REVISAR;
    columna `Nivel_D3` en el detalle.
11. **`poblacion._leer_formulario_1`: preguntas por NÚMERO, la ausente quedaba None** →
    encabezados renombrados = 0 ingresados, `avisos=[]`. → ninguna = `sin_columnas`;
    algunas = aviso SUBCONTADO por archivo (un histórico viejo puede no traer las nuevas).
12. **`poblacion.construir_poblacion`: ADA con filas en la ventana de 13 meses y NINGUNA
    de las 7 actividades SM** → Activo 12m = NO para todos. → `sin_datos` (gemelo del
    ítem 4).
13. **`rem_a23_respiratorio.procesar`: mes cubierto, NADA respiratorio** → 27
    indicadores en NO con «Listo». → `sin_datos` (gemelo del ítem 4).
14. **`cargar_otros`: sin columna INSTRUMENTO** → `_med` False para todos, SALA y G en
    0. → `requeridas=("RUN", "FECHA", "INSTR")`; con la columna pero sin ningún médico,
    aviso EN 0.
15. **`rem_utils.grid`: Ambos cuenta lo que H/M y los tramos no** (sexo Intersexual,
    Desconocido o vacío; edad ilegible) → columnas pegables que suman menos que el
    total, callado. → `rem_utils.aviso_fuera_de_grid` (REVISAR) en SM y en el D.3.
    `grid` NO cambia: la atención existió y va en Ambos.
16. **`dialogos._dotacion_ada`: tributa pero sin FUNCIONARIO** → otra vez «sin
    funcionarios nuevos» (el ítem 8 solo cubría `trib` vacío). → log propio.
17. **`rem_sm_trabajo_perdido.analizar`: Maestro que no reconoce ninguna actividad del
    mes** → todo a heurística sin el aviso HEURISTICA. → aviso.

**Fixtures ajustados** (eran el caso cazado, no el test): `test_a23` (SALA/G sin nada
respiratorio en el mes → fila de relleno `_RESP`), `test_sp_p6::test_gestante...` (ADA
sin actividad SM → una fila SM de otro RUN).

### §1.K · Bug recurrente, auditoría ESTÁTICA de loaders y filtros (ronda 10, R2)

Lectura de cada loader y cada filtro alcanzable desde las páginas, buscando lo que la
ronda empírica no podía ver: **cruces entre fuentes** (cada una con datos, el join
vacío), **casilleros que fijan el tipo** sin mirar el contenido, y **columnas opcionales**
que quedan en None para todos. Repros en `r2/*.py` del scratchpad; 14 mutantes cazados
(`r2/mut10.py` + el de la edad del A05).

1. **`rem_sp_p6_poblacion._base_valida`: base (Estado=Activo × Activo 12m × Ingresado)
   vacía** → P6 entero en 0 con «Listo»; solo un log. Casos: ESTADO «Activa», RUN del
   ADA con puntos. → `sin_datos` con el conteo de cada filtro.
2. **`rem_a23_respiratorio.procesar`: nadie «Pertenece a SALA»** → `_tablas_a23`
   filtra por eso, así que TODAS las hojas copy-paste en 0 (con el detalle lleno de
   IRA). → `sin_datos`. El aviso EN 0 de «sin médico» sigue para cuando SALA no queda
   vacía.
3. **`rem_a03_d3_instrumentos.procesar`: el casillero fija `instrumento` y se saltaba
   `detectar_instrumento`** → PSC-Y en el de GHQ-12 (todo fuera de rango) o GHQ-12 en
   el del PSC (todo bajo 33) = D.3 en 0, y el desglose por instrumento no lo delataba
   («GHQ-12: 3»). → `instrumento_cruzado` si el contenido dice otro.
4. **Ídem, `fuera_rango` solo al log** → todos = `sin_datos`; algunos = aviso SUBCONTADO.
5. **`rem_a23_respiratorio.cargar_otros`: preguntas de condición opcionales** (RAYEN
   cambia «PADECE DE» por «TIENE») → esa condición en 0 en SALA y en la G, callada.
   → `_OTROS_CONDICIONES`: aviso SUBCONTADO POR ARCHIVO (resolución por archivo, no la
   del primero); ninguna «¿Padece?» = `sin_columnas`.
6. **`rem_a23_respiratorio.cargar_inasistentes`: sin `requeridas`** → sin TIPO/
   INSTRUMENTO la H daba 0, sin AÑOS todo en «20 y más» (`NaN < 20` es False). →
   requeridas `FECHA/TIPO/INSTR/ANOS`; edad ilegible = aviso REVISAR (`attrs["sin_edad"]`).
7. **`rem_sm_rescate_inasistentes.procesar`: sin MOTIVO/FECHA PASIVACION** (opcionales
   para `cargar_inscritos`) → Posibles_Fallecidos/Fallecidos_mes/Traslados vacías, y la
   lista de a quién llamar sin la marca de fallecido. → `sin_columnas` (vía
   `insc.attrs["columnas_ausentes"]`); el P6 no se entera.
8. **`poblacion._leer_formulario_1`: sin guarda POR ARCHIVO** → un año del histórico
   solo-encabezado se perdía en el concat, y la cobertura por min/max no lo ve. →
   `sin_datos` nombrando el archivo (la guarda sobre el concat quedó muerta y se sacó).
9. **`poblacion.cargar_inscritos`: el guard de c38a8cc quedó DETRÁS de
   `cargar_canonico`** (que ya corta el solo-encabezado) → su mensaje «no trae ninguna
   fila» era falso para el único caso que lo alcanza, y su test ya no lo ejercitaba. →
   mensaje con N sin RUN / M «RUN Responsable» + test propio. De paso: una fila sin RUN
   sobrevivía como la persona `"None"` (`astype(str)`); ya no.
10. **`rem_saludmental._preparar`: `ANIO_COL_FALLBACK = 11`** — sin la columna de edad
    por nombre, se tomaba la col 11 POR POSICIÓN (layout IRIS, armado a ciegas antes de
    `refs_tablas/`). En el Administrativo la 11 es **Convenio** (confirmado por el autor
    contra `refs_tablas/Formulario_csm_reporte_Administrativo.xlsx`; la edad es la col 4).
    En IRIS era código muerto (el encabezado de edad ES el ancla de `detectar_eje`). →
    constante borrada; sin edad por nombre = `sin_columnas`. Test con el encabezado real.

**2a pasada sin tope, corregidos también (6)** — 10 mutantes más (`r2/mut11.py`):

11. **`poblacion._leer_formulario_1`: `INSTRUMENTO` opcional** → todos los dx que exigen
    médico en NO y el P6 subcontando con `avisos=[]` (la base sigue viva por los FR, así
    que el ítem 1 no lo ve). → requerida junto a RUT y FECHA FORMULARIO (`sin_columnas`).
12. **`rem_saludmental.marcar_eventos` (A05): todas las FECHA FORMULARIO ilegibles** →
    `mes_vacio` aconsejaba «elige Archivo completo», que cuenta el año entero como el mes.
    → `sin_fecha` (contador `filas_con_rut`) con el consejo contrario.
13. **`rem_sp_p6_poblacion._grid_y_detalle`: persona sin edad** → Ambos sí, ninguna
    banda, sin Revisar. → fila «Sin edad: cuenta en Ambos, en ninguna banda» en
    Revisar_Administrativo (el gemelo de §1.J.15 para el P6).
14. **`gui/paginas/a23.resumen` / `sm.resumen`: sin los avisos** (y `sm.correr` botaba
    `r03["avisos"]`) → «Listo» igual a una corrida limpia. → `widgets.texto_avisos`,
    compartido con Población (que tenía su copia en línea); `res["avisos_a03"]`. El test
    de SM corre `correr` de verdad (el de `_por_instrumento` ya había caído en la trampa
    del dict a mano).
15. **`rem_a23_respiratorio.cargar_estrat`: sin columna de diagnósticos** → cargaba sin
    aportar nada → `sin_columnas`. Y el `x or y` entre las dos columnas trataba el índice
    0 como ausente → `is None`.
16. **`estamentos.cargar_estamentos`: filas sin Profesional/Instrumento** → `{}` callado
    (`exigir_filas_ws` va antes del filtro) → `sin_datos`.

**Fixtures ajustados** (eran el caso cazado): `test_sp_p6::test_desfase...` y
`test_resumen_de_poblacion...` (formulario vacío = nadie en la base → `_ING_FEB`),
`test_a23::test_mes_sin_nada_respiratorio...` (sin médico y sin J45 = SALA vacía → una
atención J45 para seguir probando el aviso EN 0).

Revisado y limpio: `dotacion.evidencia`/`nuevos` y el tramo de `_dotacion_ada` fuera
del `try` (corre en `preparar`, que ya pasa por `manejar_error`; todas las columnas de
la evidencia son str); `marcar_demografia` y `gestante_runs` con 0 filas;
`rem_saludmental.marcar_eventos` (0 filas en el mes → `mes_vacio`); `trans_map` /
`atenid_multiprofesional` (guardas + avisos de §1.A/§1.J); `filtrar_mes` con NaT parcial.
Queda como está a propósito: `trans_map` falla duro con 0 filas pero solo avisa con
columnas faltantes (`except ValueError`) — las dos cosas son ruidosas.

### §1.L · Cada referencia y cada fallback contra el export REAL (ronda 11, interactiva)

Pedida por el autor tras §1.K.10 (la edad del A05 por posición). Método: cada mapa de
columnas, número de pregunta, ancla y literal de actividad contrastado contra
`refs_tablas/` y el Maestro, con un repro por sospecha; el autor bajó los exports que
faltaban. **Verificados y correctos** (no re-auditar): `MAPA_ATENCIONES` (IRIS y
Monitoreo), `MAPA_INSCRITOS`, `MAPA_GRUPAL`, `MAPA_NSP`, `_resolver_otros` (IRIS, las 35
claves), `trans_map`, `atenid_multiprofesional`, `MAPA_MAESTRO`, identidad/fecha/demografía
del formulario SM en los dos formatos, los ~50 números de pregunta (P6, `OVERRIDE_*`,
subtipos, `EXCLUIR`, TGD 63/64), las columnas del A03 en los 5 instrumentos, y las
columnas de salida del P6 contra el export del PowerBI.

1. **`rem_saludmental` / `poblacion._leer_formulario_1`: un cuestionario pasaba como
   formulario SM** (mismas firmas de eje; su «1.- ESTADO» dice Ingreso) → el A05 contaba
   ingresos con patología «Estado» y el P6 leía el ítem 3 de Goldberg como Violencia.
   → `verificar_formulario_sm` (`FIRMA_FORMULARIO_SM` + `ESTADOS_FORMULARIO_SM`):
   `no_formulario_sm` si calza menos de la mitad de las preguntas de diagnóstico (Otros
   Crónicos coincide en la 75, Epilepsia), `formulario_cambiado` si es el SM renumerado.
2. **`rem_utils.encontrar_fila_encabezado`: fallbacks POSICIONALES** («1ª fila con A
   vacía», fila 16/8 fija) → una fila de datos como encabezado. → solo ancla, o
   `sin_encabezado`. Se fueron `HEADER_ADMIN` y `usar_blanco_en_a`/`n_hardcode` de los
   perfiles. **Corrección a la ronda:** se dijo primero que el IRIS no trae banner; SÍ lo
   trae (15 filas en los formularios). Las referencias no lo mostraban porque se habían
   recortado a mano (ítem 10).
3. **`rem_utils.cargar_atenciones`: ffill GLOBAL del RUN** (el comentario decía «en IRIS
   no se toca nada», el código no miraba el formato) → en IRIS una fila sin RUN heredaba
   el paciente de otra atención. → `groupby(ATENID).ffill()` (el `N°` del Monitoreo se
   repite en las hijas: confirmado por el autor) + log de las huérfanas.
4. **`a23._masks_simples`: AND entre actividades fila por fila** → en el Monitoreo (una
   actividad por fila) Autocuidado, Inhaloterapia, Otras, Edu Integral, Antitabaco y Vida
   Saludable en NO callados. → `_act_de_la_atencion` (decisión del autor: el AND se queda,
   por ATENID en IRIS y por `N°` en el Monitoreo).
5. **`poblacion.ACTIVIDADES_SM_7`: 3 de 7 literales del DAX no existen en el Maestro**
   («…con **patología** de salud mental», «…a familia con adulto mayor con demencia»,
   «visita integral de salud mental a domicilio») → Activo 12m / rescate ciegos a esas
   visitas. → nombres reales del Maestro. **Pendiente del autor:** la de demencia hoy
   calza solo con actividades de gestión (`AG_…`); la VDI A26 equivalente es la del
   PADDS, que el Trabajo Perdido excluye de SM.
6. **`a23.cargar_estrat`: el fallback «CONDICIONES CRONICAS»** calzaba primero con
   «Cantidad de Condiciones Crónicas» del export real (un CONTEO) → SALA sin
   diagnósticos, callada. Lo destapó pasar el contrato de sintético a real. → fuera.
7. **RUN / ATEN ID vacío en TODAS las filas** (el pendiente C4 de los contratos) no
   fallaba en `cargar_atenciones`, `cargar_otros`, `cargar_estrat`, `trans_map` ni
   `atenid_multiprofesional` → `sin_datos` / `ValueError` (los dos opcionales del SM).
8. **`tools/limpiar_refs.py` no arrancaba en Python 3.9** (`int | None` sin
   `from __future__ import annotations`) y no tenía ni un test.
9. **`limpiar_refs.recortar` editaba el original**: partía el encabezado de dos pisos
   (Utilización de Cupos), no abría un export con una imagen rota (Otros Crónicos IRIS) y
   conservaba lo que no son celdas (caché de tabla dinámica, comentarios, propiedades).
   → libro NUEVO con banner + bloque de encabezado + hojas; escaneo antes de escribir.
10. **Referencias editadas a mano en Excel**: el grupal sin banner y con `Columna1`/
    `Columna2` donde el export dice `ASISTE (SI/NO)`/`ESTADO CITA` (el «pendiente ASISTE»
    de los contratos era esto), y los formularios IRIS SM y Goldberg sin su banner. →
    re-bajados por el autor y recortados con el script. El banner **se conserva** en toda
    referencia (decisión del autor: al usuario se le pide no borrarlo).
11. **Arnés de contratos**: `plantilla` tomaba como encabezado la ÚLTIMA fila no vacía
    (con un encabezado de dos pisos, la de abajo) y el C6 comparaba salidas que llevan el
    nombre del archivo adentro (`c0.xlsx|1` vs `c6.xlsx|1`) → mismo criterio que
    `limpiar_refs` + el C6 escribe con el mismo nombre en otra carpeta.

**Segunda parte: decisiones del autor sobre lo que quedó abierto.**

12. **`poblacion.ACTIVIDADES_SM_7`**: la VDI del PADDS con demencia («dependencia severa
    con diagnostico de demencia») **cuenta para Activo 12m**. El Trabajo Perdido la sigue
    sacando de SM: eso dice a qué REM tributa, no si la persona está activa.
13. **El Otros Crónicos y el NSP Administrativos se soportan.** `_resolver_otros` acepta
    `RUT` / `Fecha Formulario` / `Funcionario`; sin INSTRUMENTO, el estamento sale del
    nombre del funcionario (`a23._estamento_por_funcionario`: primero el export de
    atenciones, `PROF -> INSTR`, después el caché de estamentos). Los que no se resuelven
    dan un aviso SUBCONTADO, y si no se resuelve ninguno, `sin_estamento`. `MAPA_NSP` acepta `RUN` /
    `FECHA CITA` / `EDAD` (en texto -> `edad_anios`). Contratos nuevos para los dos.
14. **Opcional inválido → «¿continuar sin él?».** `rem_utils.OpcionalInvalido` +
    `with opcional("<param>")` en el A23 (Estratificación, NSP) y el SM (Inscritos para
    TRANS, Multiprofesional, y el Maestro cargado a mano, validado ANTES de escribir nada).
    La app (`runner.sin_opcional`, llamada desde `lanzar_corrida` en `gui/app.py`) pregunta; si
    la respuesta es sí, re-corre sin ese archivo y sin repetir `preparar`, y la LEEME dice `OMITIDO`
    (`runner.avisos_descartados`). Antes, TRANS y Multiprofesional quedaban en el log.
    Los inputs cuyo `key` no es el parámetro del módulo lo declaran con `entrada`.
    `test_sm_actividades::test_trans_inscritos_modificado` fijaba el comportamiento viejo
    («no crashea, TRANS en 0») y se actualizó a la decisión.

**Fixture ajustado** (era el caso cazado): los IRIS del A05 traían «18.- ESTADO» — en el
formulario real es la 19, y la 18 quedaba duplicada. **Contratos:** 16, todos contra el
export real salvo el Maestro `.xlsx` (no se versiona; banner + encabezado copiados a
mano). **Guardarraíles nuevos:** `test_refs_tablas.py` (toda referencia versionada limpia
+ todo literal de actividad calza con el Maestro, leído por AST). 15/15 mutantes, más
12/12 de la segunda parte.

### §1.M · Altitud: cada arreglo a la altura donde vive la causa (ronda 12)

Ángulo: ¿cada arreglo de las rondas 1-11 está puesto donde está la causa, o emparcha al
consumidor y deja la clase abierta para el resto? Once hallazgos, los once corregidos,
**11/11 mutantes cazados** (`r12/mut12.py` del scratchpad). Lo que NO se hizo, por decisión
del autor: llevar los arreglos de `programas/`+`modulos/` a `main` (ver §4, hallazgo #4;
se cierra con el merge de la 2.0).

1. **`cargar_canonico(..., no_vacias=)`** — la guarda «columna clave presente pero VACÍA en
   todas las filas» (§1.L.7) estaba escrita a mano en SEIS loaders (`cargar_atenciones`,
   `cargar_otros`, `cargar_estrat`, `trans_map`, `atenid_multiprofesional`,
   `cargar_inscritos`), dos de ellos con `ValueError`, y en `cargar_otros`/`cargar_atenciones`
   sobre el DataFrame **ya concatenado**: un año con el RUN entero en blanco cargado junto a
   uno bueno pasaba callado, sus formularios quedaban sin paciente y la **Sección G contaba
   como inasistente a quien SÍ se controló** (1 en vez de 0); en el A23 las atenciones de ese
   archivo se juntaban bajo un paciente `nan`. Ahora es un parámetro del cuello de botella,
   POR ARCHIVO y nombrándolo. Arnés: **`C4b`** (clave vacía en 1 de 2 archivos) + campo
   `multiarchivo` en `Contrato`, en los 6 contratos que aceptan listas.
2. **`rem_utils._una_fila_por_atencion`** — la forma PADRE-HIJO del Monitoreo se
   normalizaba a medias: ffill de la cabecera en el loader (§1.L.3) y el AND entre
   actividades en UN consumidor (`a23._act_de_la_atencion`, §1.L.4). Los demás seguían
   viendo una fila por actividad: el **Trabajo Perdido** marcaba «saco roto» una actividad
   cuya hermana de la misma atención SÍ tributaba (0 desde IRIS, 1 desde el Monitoreo, con
   los mismos datos) y su tabla dice «atenciones»; `dotacion.evidencia` inflaba
   `n_atenciones`. Ahora `cargar_atenciones` entrega **una fila por atención en los dos
   formatos** (ACT/DIAG unidas con el separador de IRIS) y `_act_de_la_atencion` se borró.
   De paso: **ATENID pasa a `requeridas`** (sin ella el `drop_duplicates` del SM dejaba UNA
   fila por casilla) y un ATEN ID repetido entre pacientes distintos es `modificado` — no
   identifica una atención, y juntar esas filas mezclaba dos personas.
3. **`opcional()` solo convierte `ArchivoInvalido`** y los cuatro opcionales que leían con
   `leer_xlsx` a mano (`trans_map`, `atenid_multiprofesional`, `cargar_estrat`,
   `cargar_maestro` .xlsx) pasan por `cargar_canonico`. Eran dos fallas de una misma causa:
   el filtro por TIPO de excepción era **estrecho** (un .xls/.html disfrazado levantaba
   `BadZipFile` → la corrida entera se caía en vez de preguntar «¿seguir sin él?», que era
   la decisión del autor de §1.L.14; solo el NSP, que sí pasaba por el cuello de botella,
   preguntaba) y **ancho** (atrapaba cualquier `ValueError`, así que un bug de código dentro
   del bloque — que en el A23 abarca el procesamiento de la Sección H — se le mostraba al
   usuario como «tu archivo opcional no sirve», y el «Sí» descartaba un archivo bueno con la
   LEEME culpándolo). `_guard_maestro` levanta `ArchivoInvalido`; el `_OPCIONAL` del arnés se
   fue.
4. **Los opcionales se cargan PRIMERO** (`a23.procesar`, `smact.procesar`). El mecanismo de
   §1.L.14 RE-CORRE el módulo, y la Estratificación se cargaba después del formulario y el
   NSP al final, con SALA y la Sección G ya calculadas: la pregunta llegaba tras el minuto
   de corrida y el «Sí» repetía todo. Ahora fallan antes de leer el ADA.
5. **`tpmod.procesar(..., dfm=)`** — gemelo del `d=` del ADA. `sm.correr` abría el Maestro
   cargado a mano para validarlo ANTES de escribir nada (bien: el TP tiene su propio `try`
   que lo habría dejado en un «no se generó»), **botaba el resultado**, y el TP lo volvía a
   abrir: 8,6 MB y ~12,5 s cada vez, medidos. Además el aviso `OMITIDO` iba solo a la LEEME
   del SM, no a la del TP, que es el reporte que usa el Maestro.
6. **`a05.detectar_ahora()` re-detecta SIEMPRE** (y `preparar` lo llama siempre). La
   categoría **y el error** se cacheaban con la RUTA como clave, y bajo el mismo nombre el
   contenido cambia todo el tiempo: RAYEN baja todo como `Formulario_Rayen.xlsx` (regla 5) y
   OneDrive entrega el `.xlsx` a medio bajar (§13). (a) El archivo elegido a medio
   sincronizar dejaba cacheado un «no es un .xlsx» que se repetía en CADA Procesar aunque ya
   estuviera completo — incluso tras el «Guardar como .xlsx» que el propio mensaje pide, si
   conserva el nombre; (b) un IRIS reemplazado por el Administrativo se procesaba con el
   perfil viejo, sin pedir el acuse y reventando en el worker con «Cambia el selector de
   formato» — el mensaje que CLAUDE.md §12 da por inalcanzable desde la 2.0. Leer el
   encabezado cuesta ~60 filas; la detección en hilo queda solo para el banner.
7. **Los opcionales de UN archivo dejan de ser `multi`** (Estratificación en A23; Inscritos,
   Multiprofesional y Maestro en SM). Declarados múltiples —herencia de la 1.x— se podían
   elegir varios con ctrl-click (la fila decía «2: a.xlsx, b.xlsx», y las instrucciones de
   los inputs de al lado invitan al ctrl-click) y `correr` usaba `[0]`: el resto se
   descartaba callado, sin salir ni en `fuentes` de la LEEME. Y `_resolver_ctx` no validaba
   la ruta de un opcional: mal tecleada, reventaba al abrirla, a mitad de corrida
   (`FileNotFoundError` → «Error inesperado»).
8. **Una cabecera de sidebar por programa.** Población declaraba el programa «Salud Mental —
   Población» y `app._cabecera_sidebar` lo volvía a juntar con «Salud Mental» por PREFIJO.
   El estado de validación ya es un dato de la PANTALLA (`estado: beta` → badge [BETA]), y
   la unión dependía de que los dos quedaran PEGADOS en `ORDEN_PROGRAMAS`: un programa nuevo
   que empezara con «Salud Mental» dibujaba una SEGUNDA cabecera «SALUD MENTAL» (verificado).
   Misma clase que §1.C-bis/ter. Se fue el programa aparte, el helper y sus dos comentarios.
9. **El router muestra/esconde** (`grid` / `grid_remove`) en vez de apilar las páginas en la
   misma celda y traer una al frente. La tapada seguía **mapeada**, y el Tab del teclado
   recorre lo mapeado: desde la página visible se llegaba a las cajas de texto de las OTRAS
   (3 de 5 paradas, medido) y lo tecleado no aparecía en ninguna parte. Sin pila, además,
   no hay `lift()`-vs-`tkraise` que explicar (el muro de comentario se fue con él).
10. **El encabezado del grupo pandas sale de las columnas REQUERIDAS**
    (`encabezado_por_columnas`), que es el ancla que cada loader ya declaraba. Era «la 1ª
    fila con más de 3 celdas llenas» — un conteo, y los banners del Monitoreo ya traen una
    fila de 3: una columna más y el encabezado pasaba a ser una fila de filtros, o sea un
    export válido rechazado. `indice_encabezado` devuelve `None` en vez de caer a la fila 0
    (el mismo fallback posicional callado que la ronda 11 sacó de `encontrar_fila_encabezado`),
    y `leer_xlsx` levanta `sin_encabezado`. Se fue el parámetro `ancla` de `cargar_canonico`.
11. **Envoltorios que solo reenviaban**, vacíos desde que la ronda 11 borró los fallbacks
    posicionales: `formatos.fila_encabezado_admin` y los `_fila_encabezado` del A03 y de
    estamentos (la única diferencia entre formatos es qué ancla se pasa → `formatos.ANCLA`),
    más el `modo` que devolvía `encontrar_fila_encabezado` (constante `"ancla"`, y se logueaba).
    Y `MAPA_INSCRITOS` se mudó a `rem_utils`: el mismo export lo leen `cargar_inscritos` y
    `trans_map`, que resolvía las mismas columnas por su cuenta.

**Fixtures que eran el bug** (no el test): el ADA de `test_a23` no traía ATEN ID; el de
`test_sp_p6` le ponía `"A"` a TODAS las filas y el de `test_trabajo_perdido` derivaba el id
de las 3 primeras letras de la actividad, así que colisionaba entre pacientes — con la forma
canónica eso ya no es un detalle cosmético, y por eso la guarda del ítem 2 existe. El toy del
arnés tenía 3 columnas (no lo tomaba como encabezado el criterio de >3 celdas).

### §1.E · Estructura y versionado

- **Colisión de versión:** `main` y la rama tenían cada una su 1.9.16 → la rama pasó a
  **1.9.17**. El árbitro anti-colisión es el CHANGELOG (CLAUDE.md §9).
- La familia población cargaba Inscritos / Formulario / ADA **dos veces** (P6 + Rescate)
  → se pasan los DataFrames ya cargados, con `fuentes=` para la hoja LEEME.
- Código muerto y duplicados: `resolver_estamentos`, `_on_procesar`/`_getters`, el
  predicado solo-A03, el banner A23/SM.
- `requirements.txt` no listaba `customtkinter` (y ahora menciona `pytest` como dep de
  desarrollo, que solo pide `tests/test_formatos_fuente.py`).

---

## §2 — DESCARTADO: revisado y NO es bug. No volver a perseguir

Estas fueron sospechas explícitas de rondas anteriores. **Están cerradas con motivo.**

- **`widgets.estado_fuente_de_avisos` desempaca tuplas de 4** — correcto, no frágil.
  `programas/cobertura.py:285` (el escritor de la hoja LEEME, por el que pasan TODOS los
  módulos) **también** desempaca 4, así que la forma ya está fijada aguas arriba. Un
  aviso mal formado reventaría antes, en `cobertura`, que es donde corresponde
  arreglarlo. Poner un guard defensivo en el banner solo taparía ese bug.
- ~~**`catalogos.cargar(entrada=, recargar=)` y el override del About**~~ —
  **DESCARTE EQUIVOCADO, reabierto y corregido en la ronda 7 (§1.H.2).** La premisa «no
  hay consumidor que pueda ignorar el override» era falsa: por la clave del caché, TODO
  consumidor lo ignoraba, apenas existiera uno.
- **El resolver manual de estamentos del A03 standalone borrado** — no se perdió nada.
  `_tab_a03` también pasaba `resolver_estamento=None`: el diálogo Tk no puede abrirse
  desde el worker, y el estamento solo alimenta el DETALLE, no la tabla D.3.
- **`gui/paginas/sm.py` decía «saco vacío» en 4 lugares** (estaba en el roadmap de
  CLAUDE.md §12) — ya estaba renombrado a «saco roto». Sacado del roadmap.
- **`refs_tablas/*.xlsx` son header-only y `cargar_canonico` ahora los rechaza** — es
  correcto: son planillas de EJEMPLO (privacidad), no exports. Los 3 tests de
  `test_formatos_fuente.py` que se las pasaban usan ahora `_con_una_fila()`, que agrega
  una fila sintética **conservando el encabezado REAL** como guardarraíl de la firma.

---

## §3 — Verificación (estado actual)

- **296 tests verdes** (eran 183 al abrir la revisión, 190 tras la ronda 2, 197 tras la 3,
  206 tras la 4, 215 tras la 5, 237 tras la 6, 241 tras la 7, 245 tras la 8, 257 tras la 9,
  268 tras la 10, 271 con los contratos, 278 tras la 11, 283 con las decisiones del
  autor y 296 tras la 12). `check_version` OK (1.9.17, 296 tests),
  `check_cp1252` OK, `check_fuentes --todo` OK (18 contratos, ahora con el chequeo C4b). En la
  corrida completa de pytest sigue saliendo a veces el `tk.tcl` intermitente de
  `test_gui_construccion` (pasa solo; lo investiga una sesión aparte).
- Se instalaron `pytest` y `customtkinter`, que faltaban en el Python 3.9 local: los
  **dos** test files que antes no se podían correr ahora corren.
  `test_formatos_fuente` 33/33 · `test_gui_registro` 19/19 · `test_gui_construccion`
  19/19 · `test_autorem` 19/19 · `test_dotacion` 14/14 · `test_estamentos` 7/7.
- **Tests nuevos (23):** `test_gui_construccion.py` (8: construcción de las 6 páginas,
  ruta precargada del A05, `detectar_ahora`, vaciar un input múltiple, solo-cuestionarios
  alcanzable tras un ADA elegido por error, banner de fuente que no sobrevive al cambio
  de archivo, cabecera del grupo sobre sus páginas, Inicio al tope y Acerca de al pie)
  · `test_gui_registro.py` (2: rango de `valida_mes`, Spinbox amarrado a
  `ANIO_MIN`/`ANIO_MAX`) · A05 sin filas (`test_autorem`) · A03 sin filas
  (`test_screening`) · Cupos sin filas (`test_estamentos`) · `cargar_estrat`
  (`test_a23`).
- **Tests de la ronda 4 (9):** `test_gui_construccion.py` (2: el `.xls` disfrazado no se
  confunde con «formato no reconocido»; salida de Población junto al Inscritos) ·
  `test_gui_registro.py` (4: `motivo_fuente` sigue las ramas de `manejar_error`; el
  desglose A03 llega al resumen; el orden de páginas no depende del nombre del archivo;
  toda página declarada en `ORDEN_PAGINAS`; una sola `ancla_salida` por pantalla) ·
  `test_formatos_fuente.py` (3: `detectar_eje_filas` == `detectar_eje` sobre los dos
  exports A05 reales, y le alcanza el encabezado).
  **De la primera pasada, 2 sobrevivieron a la mutación** (probaban la pieza suelta, no
  el cableado) y se rehicieron — ver §1.C-ter y §1.D-bis.
- **Tests de la ronda 5 (9):** `test_formatos_fuente.py` (6, 7 casos: `leer_xlsx` no
  trunca; `verificar_hoja_unica` ve la hoja extra; detección A05 sobre el IRIS real con
  la `<dimension>` en `A1`; el escaneo de PII ve un RUT fuera de la etiqueta; el catálogo
  se lee entero; fuente multi-archivo igual en los dos órdenes) · `test_gui_construccion.py`
  (2: la PÁGINA del A05 y el preview del SM con la `<dimension>` rota; ruta con comillas)
  · `test_dotacion.py` (1: `sin_estamento`). Cada test de `<dimension>` comprueba
  **primero** que el fixture arma la trampa (un read_only pelado sí trunca), para no
  quedar verde por un fixture que dejó de reproducirla.
- **Un test cambió de expectativa a propósito:**
  `test_a23::test_export_sin_filas_falla_claro` esperaba `mes_vacio` y ahora corta antes
  con `sin_datos`, nombrando el archivo. Es la guarda más temprana y más precisa, no un
  enmascaramiento.
- **Repro empírico de 0 filas:** SM grupal / Inscritos / Multiprofesional, Trabajo
  Perdido / Maestro, Población Formulario / ADA / Inscritos, A05 (IRIS y Admin, con mes
  y sin mes), A03 (4 instrumentos), Cupos, Estratificación → **todos** dan
  `ArchivoInvalido`.
- **La GUI se construye de verdad** (`test_gui_construccion.py`): las 6 páginas (4 del
  registro + Inicio + Acerca de) se arman y sobreviven ciclos de eventos. Eso es lo que
  cazó el `after()`-desde-hilo.

---

## §4 — QUÉ FALTA

### Para probar a mano (ronda 6)

- **El caché que no se puede escribir, en el PC del trabajo** (el autor lo va a probar en
  OTRO perfil, no en el suyo): quitarle la escritura a `~/.autorem`, procesar SM con
  dotación, y confirmar el diálogo + la línea «NO se puede escribir» en «Acerca de».
  Mismo ejercicio con un `dotacion.json` dañado a mano.

### Lo que no se puede automatizar (no es para un agente)

1. **Mirar la ventana con ojos humanos** — `python -m gui.app`. Que el banner y el acuse
   del A05 queden DONDE se espera, que la caja de cuestionarios del SM se vea bien, que
   el tema claro/oscuro no rompa nada. El test de construcción prueba que no revienta,
   no que se vea bien.
2. **Compilar el .exe y abrirlo** — `pyinstaller autoREM.spec`. Los arreglos de §1.C
   están razonados pero **no probados contra un build real**. Confirmar: el sidebar trae
   las 4 páginas, y el botón de catálogos del About no dice que falta el escáner.

### Abierto tras la ronda 11 (referencias contra el export real, §1.L)

**Decisiones del autor, ya implementadas (ronda 11, 2a parte; ver §1.L.12-14):**
- La VDI del PADDS con demencia **cuenta para «Activo 12m»**, y sigue fuera del Trabajo
  Perdido de SM (tributa al REM del PADDS).
- **Se soportan** el Otros Crónicos Administrativo y el Monitoreo de Inasistentes
  Administrativo.
- Un opcional inválido **pregunta «¿continuar sin él?»**.

**Referencias:** el autor re-bajó el ADA IRIS y el Inscritos con su banner (18 y 17
filas). Siguen sin banner `pscy_10_14_iris.xlsx` (RAYEN no la deja bajar, probablemente
por 0 filas) y `poblacion_sm_powerbi.xlsx` (export del PowerBI, sin banner de RAYEN). El
PSC para padres IRIS no existe como export. El Maestro `.xlsx` (8.6 MB) no se versiona:
su contrato va con encabezado copiado a mano.

**Supuesto sin verificar (necesita datos, no encabezados):** que el nombre del
funcionario del Otros Crónicos Admin se escribe IGUAL que en el export de atenciones y en
«Utilización de Cupos». Si no, todos sus formularios caen en `sin_estamento` (ruidoso,
no callado); el A03 Admin ya cruza por nombre contra Cupos y funciona.

**Lo que una referencia de solo-encabezado no puede verificar:** el VOCABULARIO de los
valores (ESTADO del formulario, «Activo» del Inscritos, el nombre en la columna
FORMULARIO de los cuestionarios IRIS, el separador de actividades en la celda
ACTIVIDADES del IRIS). Una fila inventada con el vocabulario real (sin PII) por export lo
cubriría; no se ha decidido. Del separador cuelga ahora una decisión cosmética:
`rem_utils.SEP_ACTIVIDADES` (`"; "`) es con lo que se juntan las actividades del Monitoreo
al darle la forma de IRIS (§1.M.2). No cambia ningún conteo -- todo se busca por subcadena
con `contiene_*` --, pero si el IRIS real usa otro separador, ese es el valor que hay que
corregir para que el detalle se lea igual en los dos formatos.

- Ojo al diseñar el chequeo de posición: los formularios RAYEN SÍ dependen del orden
  RELATIVO (el ESTADO va pegado a su pregunta: `encontrar_diagnostico`, `estado_tras`).
  El contrato por eso corre las columnas una posición (C6), no las invierte.

### Ángulos de revisión que NO se han corrido todavía

Los agentes en paralelo murieron antes de entregar; lo hecho a mano fue más acotado que
el `max` planeado. Sin cubrir de forma sistemática:

- **Eficiencia**: nadie miró si la GUI 2.0 relee archivos o rehace trabajo (el caso de
  la familia población, §1.E, se encontró de casualidad).
- **Convenciones**: headers de versión de cada `.py` de `gui/` vs su último cambio real
  (se sincronizaron a 1.9.17 los tocados, no se auditó el resto).
- **Paridad del port**: se comparó a mano `_tab_sm`, `_tab_a05`, `_tab_a23`, `_tab_a03`
  y `_manejar_error`. **Falta `_tab_beta`** (vs `gui/paginas/poblacion.py`) y los
  **diálogos de dotación** (`gui/dialogos.py` vs `_dialogo_dotacion`).

### Deuda conocida, para el paso 11 / el merge

- **Hallazgo #14, sin resolver:** `gui/runner.py` duplica helpers de `autorem.py` y **ya
  divergieron**. Se resuelve con el merge limpio del paso 11.
- **`autorem.py` todavía corre la GUI 1.x:** `main()` llama `lanzar_gui`; la GUI 2.0 se
  arranca con `python -m gui.app`. Al enchufarla, pasar el `ruta_inicial` de `main()` a
  `gui.app.lanzar(ruta_inicial)` — el canal ya existe (§1.D).
- **`autoREM.spec`: `gui.app` y `gui.registro` NO entran al bundle** (hallazgo de la
  ronda 3, **postergado a propósito al merge** — decisión del autor). Verificado:

  ```
  $ python -c "from PyInstaller.utils.hooks import collect_submodules; print(collect_submodules('gui.paginas'))"
  ['gui.paginas', 'gui.paginas.a05', 'gui.paginas.a23', 'gui.paginas.about',
   'gui.paginas.inicio', 'gui.paginas.poblacion', 'gui.paginas.sm']
  ```

  No aparecen `gui.app` ni `gui.registro`, y **nadie más los importa**: `autorem.py`
  (el único entry point del `.spec`) no tiene ni un import de `gui`. Dos consecuencias:
  1. **El punto 2 de «lo que no se puede automatizar» (más arriba) hoy no se puede
     cumplir:** compilar el exe y «confirmar que el sidebar trae las 4 páginas» es
     imposible, porque la GUI 2.0 no está en el exe. Los arreglos de §1.C quedan
     razonados pero sin build que los pruebe — y eso es *esperado* hasta el paso 11, no
     un bug nuevo.
  2. **Trampa para el paso 11:** todos los imports de `autorem.py` son locales a la
     función (`lanzar_gui` hace `import tkinter as tk` adentro). Si se enchufa con un
     `from gui.app import lanzar` **dentro** de `main()`/`lanzar_gui`, PyInstaller no lo
     ve y el exe congelado muere con `ModuleNotFoundError: gui.app` al abrirlo — con el
     `.spec` ya «arreglado». Al hacer el paso 11: import a NIVEL DE MÓDULO, o sumar
     `'gui.app'` a `hiddenimports`.
- **Hallazgo #4 — `main` necesita los fixes de `programas/`+`modulos/` igual:** empezó
  por los de §1.A (`cargar_canonico`, `exigir_filas_ws`, `leer_xlsx`, `cargar_maestro`,
  `trans_map`, `cargar_estrat`, los de `poblacion.py`) y creció con cada ronda: §1.J, §1.K,
  §1.L y §1.M suman **+1483/-268 líneas** en capas compartidas, varias de ellas números
  plausibles-pero-mal que el exe de `main` sigue produciendo hoy — Activo 12m ciego a 3 de
  las 7 actividades SM, el RUN heredado de otra atención en IRIS, un cuestionario contado
  como formulario SM en el A05, 6 indicadores del A23 en NO con el Monitoreo. El plan
  (§13) dice que un bug de módulo encontrado durante la migración **se anota y se arregla
  en `main`**, no en la rama. **Decisión del autor (ronda 12): NO se porta ahora**, se
  cierra con el release de la 2.0 (un solo merge). Consecuencia aceptada: hasta entonces
  el exe en producción calcula con los bugs, y el merge del paso 11 mezcla GUI con lógica
  de módulos en un diff grande.
- **CHANGELOG al merge:** 1.9.16 de `main` + 1.9.17 de la rama. Renumerar si `main`
  avanzó.
- **`maestro_slim.csv.gz` entró a `catalogos/` sin los controles de ese vecindario**
  (hallazgo de la ronda 4, **fuera de alcance por ahora — decisión del autor**: el plan es
  una sección de *utils* + una **skill de Claude** que genere el slim desde un Maestro
  completo de IRIS y que sí chequee los guardarraíles del proyecto; cuando eso exista,
  este ítem se cierra ahí).

  El diff mueve el archivo de `refs_tablas/` (ignorado en bloque + **whitelist POR
  ARCHIVO**, o sea un veto humano por archivo: la línea `!refs_tablas/maestro_slim.csv.gz`
  se borra en este mismo diff) a `catalogos/`, que está whitelisteado **en bloque**
  (`!catalogos/*.csv.gz`). Hereda el versionado automático y **ninguno de los dos
  controles** que el propio comentario del `.gitignore` da como justificación de ese bloque:

  1. **El escaneo de PII.** El `.gitignore` dice: «el pre-commit anti-RUT SALTA los
     binarios (.gz), así que un slim no lo revisa nadie → `tools/catalogos_deis.py --slim`
     corre `scan_catalogo.py` antes de escribirlo y se niega a vendorizar un catálogo con
     hallazgos». Pero el slim del Maestro **no lo escribe ese script**, lo escribe
     `tools/slim_maestro.py`, que no importa `escanear` (verificado: `grep -n
     "scan_catalogo\|escanear" tools/slim_maestro.py tools/catalogos_deis.py` → 0 hits en
     el primero). El texto que el diff agrega afirma que «el Maestro slim la tiene resuelta
     aparte, en su propio script», y su script no la resuelve.
  2. **La procedencia.** «Al repo va el slim + FUENTES.json, que registra QUÉ EDICIÓN es» —
     pero `catalogos/FUENTES.json` tiene solo `cie10`, `eno`, `ges`. El Maestro se
     actualiza ~semestral, y su clasificación decide qué actividad cuenta como saco roto:
     sin registro de edición, un número de Trabajo Perdido ya tabulado no se puede
     rastrear a la versión del catálogo que lo produjo. `tests/test_catalogos.py` tampoco
     lo cubre: itera `cat.CATALOGOS`, no el directorio.

  No hay fuga demostrada (el slim recorta a 5 columnas de catálogo, sin PII de paciente).
  Lo que se perdió es **el portón**, no un dato.
- **⚠ REVISAR A MANO TODO EL TEXTO QUE VE EL USUARIO — pega del AUTOR, no de un agente.**
  Es un code-review que solo puede hacer quien conoce RAYEN/IRIS y el REM: un agente
  puede verificar que el string exista y esté bien escrito, no que la instrucción sea
  **cierta**. Y una instrucción equivocada es el mismo bug que la regla 2 persigue: si
  el texto manda a descargar el reporte equivocado, el usuario tabula un número
  plausible-pero-mal sin que nada falle. La GUI 2.0 reescribió o movió casi todos estos
  textos, así que ninguno viene «ya revisado» de la 1.x. Las superficies, para que la
  pasada sea mecánica:

  | Qué | Dónde |
  |---|---|
  | Instrucciones de cada página (los pasos «1. Descarga…») | `instrucciones = (` en `gui/paginas/*.py` |
  | Títulos y cuerpos de los avisos modales | `messagebox.show*` en `gui/` |
  | Títulos por categoría de `ArchivoInvalido` | `runner._TITULO_INVALIDO` |
  | Mensajes de error compartidos | `runner._MSG_PERMISO`, `_MSG_NO_XLSX`, `sm._MSG_DESCONOCIDO`, `sm._DISCLAIMER_ADMIN` |
  | El «por qué» de los obligatorios | `motivo_obligatorio` en las `PANTALLA` |
  | Textos de los bloques Estamentos / Dotación / Cuestionarios | `gui/dialogos.py`, `sm.bloque_cuestionarios` |
  | Etiquetas de input y de carpeta/mes | `etiqueta` / `titulo_dialogo` en las `PANTALLA`, `gui/widgets.py` |
  | Líneas de log que el usuario lee de verdad | `log(` en `gui/` y en `modulos/` |
  | Mensajes de `ArchivoInvalido` (los que más se leen) | `programas/`, `modulos/` |
  | Hoja LEEME + `no_cubre` | `programas/cobertura.py` |

  Para enumerarlas:

  ```bash
  grep -rn "messagebox.show\|^instrucciones\|motivo_obligatorio" gui/
  grep -rn "ArchivoInvalido(" programas/ modulos/ | wc -l
  ```

  Ojo con dos cosas al pasar: que el texto **no prometa** lo que el módulo no hace (ya
  mordió dos veces — el mes en el nombre del A03·D.3 y los catálogos DEIS que ningún
  módulo consulta todavía, §1.D), y las tildes (son cp1252-safe, `check_cp1252` solo
  bloquea flechas/cajas/emoji, así que el checker **no** va a cazar una tilde faltante).

---

## §5 — Bitácora de rondas

Una línea por ronda. **Anotar el ÁNGULO** que se cubrió, no solo la fecha: es lo que
evita que la ronda siguiente repita el mismo barrido. Los ángulos sin marcar están
listados en §4.

| # | Ángulo cubierto | Hallazgos | Anotados en |
|---|---|---|---|
| 0 | 12 agentes en paralelo (A–E + reuso/simplificación/eficiencia/altitud/convenciones + 2 del bug recurrente) | **0 — murieron al arrancar** (HTTP 429) | — |
| 1 | A mano, alcance acotado: bug recurrente en la familia población + GUI (empaquetado del log, salidas con RUT, código muerto) | 15 | §1 (13 ✅) · §4 (2 ⏸ al merge) |
| 2 | A mano: auditoría estática de los loaders que faltaban + paridad del port (B/C/D/E) + trampas de Tk/hilos | 12 ✅ + 4 descartados | §1.A–E · §2 |
| 3 | **Ángulo A — barrido LÍNEA POR LÍNEA del diff** (todo `gui/`, `tools/check_version.py`, `tools/slim_maestro.py`, `autoREM.spec`, hunk de `programas/poblacion.py`), con las firmas de cada callee verificadas contra `programas/`+`modulos/` | 6: **5 ✅** + 1 ⏸ al merge | §1.D (5) · §4 deuda (el `.spec`) |
| 3b | **A OJO, el autor corriendo `python -m gui.app`** — lo que ningún test ve. Dio los 2 hallazgos de layout del sidebar, con la misma causa raíz (posición = orden de ejecución) | 2 ✅ | §1.C-bis |
| 4 | **Ángulo B — auditor de comportamiento REMOVIDO**: (a) cada línea que el diff borra o reemplaza (`.gitignore`, el rename del maestro slim, `autoREM.spec`, `tools/slim_maestro.py`) → ¿qué invariante sostenía y dónde se re-establece?; (b) cada página portada contra su `_tab_*` original en `autorem.py` (`_tab_a05`, `_tab_a23`, `_tab_sm`, `_tab_a03`, `_tab_beta`, `_correr_con_reloj`, `_manejar_error`, `_valida_ruta`/`_valida_carpeta`, los helpers de dotación/estamentos, y el selector de perfil que se eliminó) → ¿qué guarda, validación, aviso, `try`, línea de log, default o argumento se cayó? | 7: **4 ✅** + 1 ⏸ (utils/skill) + 1 ⏸ (CLI congelado) + 1 ✅ del ángulo A pendiente | §1.C-ter · §1.D-bis · §1.E-bis · §4 deuda (2) |
| 5 | **Ángulo C — trazado entre archivos**: cada llamada de `gui/` a `programas/`/`modulos/`/`autorem.py`/`tools/` contra firma, retorno, attrs, excepciones y precondiciones del callee; y al revés, los consumidores de lo que el diff cambió (`cargar_inscritos`, `catalogos/`). Con repros empíricos (`<dimension>` fabricada, ADA mixto IRIS+Monitoreo, ruta con comillas) | 5 ✅ (1 era regresión de la ronda 4) | §1.F |
| 6 | **Ángulo D — trampas de lenguaje/framework**: thread-safety de Tk, re-entrada de eventos, excepciones en callbacks, closures, fugas de recursos, pandas, customtkinter (contra su fuente 6.0.0 instalada), rutas de Windows. Con repros empíricos (click encolado despachado dentro de `CTkToplevel`, `wraplength` a 150%) | 9 ✅ (1 era la suite pisando el caché real) | §1.G |
| 7 | **Ángulo E — envoltorios e indirecciones**: `Pagina` (getters, `mes` y `log` perezosos, `datos` compartido), `_resolver_ctx` y las `key` de extras, los envoltorios de `runner`, los getters de `widgets`, los diálogos de dotación contra el esquema de `dotacion.py`, el override de catálogos del About contra `catalogos._CACHE`, y `registro` + `pkgutil` en el exe. Con repros | 2 ✅ (1 reabre un descarte de §2) | §1.H |
| 8 | **Reuso**: código nuevo del diff contra los helpers que ya existían en `programas/`, `autorem.py`, `tools/` y los archivos vecinos (Maestro slim vs `catalogos._carpetas`, limpieza de rutas, candado y ventana de dotación, Spinbox de mes, criterio de encabezado) | 5 ✅ (3 ya se habían apartado del original) | §1.I |
| 9 | **Bug recurrente, EMPÍRICO (R1)**: cada `correr` de página (SM, TP, dotación, Población, A23, A05) contra exports que traen filas pero quedan vacíos TRAS un filtro (corte, máscara de programa, fecha ilegible, Asiste, fecha de nacimiento), clasificando OK / crash críptico / 0 callado | 8 ✅ + 9 ✅ de una 2a pasada sin tope (3 fixtures de test eran el bug) | §1.J |
| 10 | **Bug recurrente, ESTÁTICO (R2)**: lectura de cada loader y filtro alcanzable desde las páginas (A05, A03, A23, SM, TP, Población, Rescate, dotación), con foco en cruces entre fuentes, casilleros que fijan el tipo y columnas opcionales; cada candidato confirmado con un repro | 8 ✅ (9 ítems; 3 fixtures eran el bug) + 7 ✅ de la 2a pasada sin tope (la edad del A05 por posición + 6) | §1.K |
| 11 | **Cada referencia y fallback contra el export REAL, interactiva**: todo mapa de columnas, número de pregunta, ancla y literal de actividad contra `refs_tablas/` y el Maestro; el autor bajó los exports que faltaban y re-bajó los editados a mano; `limpiar_refs` revisado (lo pidió el autor) | 11 ✅ (1 fixture era el caso) + 3 decisiones del autor, implementadas (§1.L.12-14) | §1.L · §4 «Abierto tras la ronda 11» |
| 12 | **Altitud**: ¿cada arreglo de las rondas 1-11 está a la altura de su causa, o emparcha al consumidor y deja la clase abierta? Cada guarda repetida a mano, la forma de la atención del Monitoreo, el filtro por tipo de excepción de los opcionales, la detección cacheada del A05, el sidebar por prefijo, el router por pila, el encabezado por conteo de celdas y los envoltorios vacíos. Con repros y mediciones | 11 ✅ (1 no se hace acá: los fixes de `programas/` a `main`, §4) | §1.M |
| 13 | _(siguiente: eficiencia, convenciones —headers de versión del resto de `gui/`—, la prueba a mano del caché en el PC del trabajo (§4), y otra pasada a ojo del autor)_ | | |

**Lo que la ronda 3 revisó y NO era bug** (además de §2, para no repetir el barrido):
la paridad de los diálogos de dotación contra `_dialogo_dotacion`/`_grupo_dotacion` es
fiel línea por línea (incluido el `orden` por `attrs['por_estamento']`); el reuso de
DataFrames de la familia población (§1.E) es seguro porque `construir_poblacion` y el
rescate **solo leen** `insc`/`form`/`d_ada` (ningún `df[col] = …` ni `inplace`);
`scan_catalogo.escanear` devuelve 3-tupla con hallazgos de 5 campos, como los desempaca
el About; `formatos.parece_reporte` solo devuelve claves de `FIRMAS_CRUCE`, así que el
`nombres[otro]` de `sm._chequeo_cruce` no puede dar `KeyError`; `check_version` sí cubre
`gui/paginas/*.py` (usa `git ls-files`, recursivo, y `parts[0] in DIRS_VERSIONADOS`).

**Lo que la ronda 4 revisó y NO era bug:** correr desde FUENTE no perdió el Maestro slim
(`autorem._slim_por_defecto` y `runner.slim_por_defecto` apuntan los dos a `catalogos/`;
verificado: `autorem._slim_por_defecto()` → `E:\git\Autorem\catalogos\maestro_slim.csv.gz`),
y el `.spec` ya quedó coherente en los cambios sin commitear (la entrada de compatibilidad
a `_MEIPASS/refs_tablas` se borró y el comentario apunta a `catalogos/`, así que **no** hay
copia muerta de 1.2 MB en el bundle ni comentario mintiendo); ningún test leía
`refs_tablas/maestro_slim.csv.gz` (los de Trabajo Perdido arman su propio maestro
sintético con `_mk_maestro`), así que no hay tests saltándose en silencio;
`autorem._resolver_estamentos` ya era código muerto en la 1.x (definido y nunca llamado,
`resolver_estamento=None` en todos los call sites), así que no portarlo no pierde nada;
la detección del A05 no necesita `verificar_hoja_unica` porque el worker la corre igual y
`ArchivoInvalido("modificado")` ya tiene su título; `HOJA` es `None`, así que el `wb.active`
de la detección y el `wb[HOJA] if HOJA else wb.active` de `abrir_validado` son la misma
hoja; el defecto de carpeta de A23 y SM sí coincide con el de las pestañas viejas (su
primer input declarado es el mismo archivo); `_aviso_sin_modificar` y
`_separador_opcionales` sí se portaron (`widgets.aviso_sin_modificar`,
`widgets.separador_opcionales`); y `correr_con_reloj`/`crear_log` son ports fieles.
La nueva página de A03 standalone **no** perdió el aviso de «Sin archivos»: lo cubre
`_ada_grupal_obligatorio` + el aviso genérico de `_resolver_ctx`.

**Al cerrar una ronda, además de anotar acá:** correr la suite completa
(`for t in tests/test_*.py; do python "$t"; done` + `pytest tests/test_formatos_fuente.py`),
`tools/check_version.py` y `tools/check_cp1252.py`, y actualizar el contador de §3.
