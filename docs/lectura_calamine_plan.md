<!--
This document was generated with the assistance of Claude Opus 5.5 (Anthropic).
The human author reviewed, modified, and integrated the content.

Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
Copyright (C) 2026 Simon Tobar
SPDX-License-Identifier: GPL-3.0-or-later
Version: 2.0.14
-->

# Plan — Lectura de exports con `python-calamine`

> **LISTO Y MERGEADO** — 2026-09-29, implementado en la rama `lectura-calamine` (como
> 2.0.15) y mergeado como **2.0.17**, tras la revisión ciega. Se conserva como registro:
> lo citan CHANGELOG.md y docs/evanesced/README.md. Lo que cambió respecto del plan
> (`primeras_filas` sigue en openpyxl, memoria) está en §9.

## 1. Qué y por qué (medido, no supuesto)

La pregunta de partida fue «¿cuánto acelera Cython el `.exe`?». Se perfiló una corrida
REAL (agosto 2026, exports de `Datos madre`) y la respuesta fue **~1 %**: el código propio
es el **2 %** del tiempo de SM Actividades y el **6 %** del A05 (medido aparte, sin
profiler: el A05 entero son 6,5 s, §2.3). El resto es **openpyxl
parseando XML en Python puro**. Cython queda descartado.

Después se midió `python-calamine` (lector de `.xlsx` en Rust, **integrado en pandas desde la 2.2**)
contra lo que hace hoy `cargar_canonico` (`verificar_hoja_unica` + `filas_xlsx`), **sin
profiler**:

| Export real | openpyxl hoy | calamine | Celdas comparadas | Distintas |
|---|---|---|---|---|
| ADA 2026 (24 MB) | 12,3 s | 2,5 s | 4,0 M | **0** |
| Informe Inscritos (28 MB) | 16,8 s | 2,8 s | 5,1 M | **0** |
| Formulario PSM (1,5 MB) | 1,1 s | 0,2 s | 0,4 M | **0** |

Misma forma (filas × columnas) en los tres. **Única diferencia de TIPO en datos reales:
una columna entera por archivo sale `float` en calamine e `int` en openpyxl**
(`12345.0` vs `12345`). Si esa columna es el ATEN ID, `str()` cambia la clave y los
cruces con el grupal/multiprofesional quedan en 0 **callados**. Es el bug a evitar.

Una corrida de SM Actividades de agosto lee ADA + Inscritos: **~29 s de lectura pasan
a ~5 s**.

Arneses y salida en [docs/evanesced/lectura-calamine/](evanesced/lectura-calamine/).
**Ojo con los números del perfil:** cProfile infló todo ~2,5× (el ADA daba 31 s con
profiler, 12 s sin él). Las proporciones valen, los absolutos no: para tiempos, medir
sin profiler.

## 2. Decisiones cerradas

1. **Se cambia la lectura de EXPORTS** (lo que pasa por `filas_xlsx`,
   `primeras_filas`, `verificar_hoja_unica`) a calamine. Todos los módulos pandas
   (SM, TP, A23, población, Maestro cargado a mano) lo heredan por `cargar_canonico`, sin
   tocarlos.
2. **No se tocan** `abrir_xlsx_ro` / `filas_hoja`: los siguen usando `catalogos._hojas`,
   `tools/scan_catalogo.py` (el escáner de PII: se queda en openpyxl a propósito, no está
   en la ruta caliente) y los tests. Ajustar su docstring («TODA lectura read_only pasa
   por acá» deja de ser cierto: pasa a ser «toda lectura openpyxl read_only»).
3. **No se toca el A05 ni ningún `load_workbook` en modo normal** (`rem_saludmental.abrir_validado`,
   `poblacion.py:309`, A03, `estamentos`). **El A05 queda como está: DESCARTADO por el
   autor, medido** (2026-09-29, sin profiler, mediana de 3 sobre el formulario real de
   agosto): **6,5 s** en total = abrir con openpyxl 3,1 s + motor 0,8 s + guardar el libro
   entero 2,3 s. Escribir un libro nuevo solo con las hojas de salida lo bajaría a ~4,2 s
   (y la salida perdería la hoja original); sumarle calamine, a ~1 s, pero reescribiendo
   `marcar_eventos` sobre filas, que es el motor validado en producción. Unos segundos al
   mes no justifican ninguna de las dos. **No reabrir sin un motivo nuevo.** Los demás
   lectores openpyxl que quedan, en §8.
4. **Coerción en el adaptador, mínima y explícita:**
   - `float` con `.is_integer()` → `int` (nunca tocar `bool`).
   - `datetime.date` que no es `datetime` → `datetime(y, m, d)` (openpyxl entrega
     `datetime` a medianoche; calamine, `date`).
   - **Nada más.** En particular **NO** se convierte `''` a `None`: RAYEN escribe las
     celdas vacías como string vacío (medido: 270.131 `''` y 0 `None` en el formulario
     PSM; 463.014 y 0 en el ADA), así que openpyxl ya ve `''` en producción. Solo los
     fixtures de los tests (escritos con openpyxl) tenían `None`.
5. **Pérdidas conocidas y ACEPTADAS** (calamine las entrega como `''`): celda de error
   (`#N/A`, `#REF!`…) y string de solo espacios. En los exports reales hay **0** de cada
   una (medido). Se fijan con un test (§5) para que un cambio de versión de calamine se
   note, no para defenderlas.
6. **Qué hoja se lee:** calamine no conoce la «hoja activa». La regla pasa a ser **la
   hoja con datos**: 0 hojas con datos → `ArchivoInvalido("sin_datos")` (mensaje actual
   de `filas_xlsx`); más de 1 → `ArchivoInvalido("modificado")` (mensaje actual de
   `verificar_hoja_unica`, **reusado, no copiado**). Para RAYEN es lo mismo (siempre 1 hoja
   con datos + 2 vacías), y un export con la activa vacía y datos en otra deja de fallar
   por «no reconozco las columnas».
7. **Un solo parseo por archivo en `cargar_canonico`:** hoy llama `verificar_hoja_unica(e)`
   y después `filas_xlsx(e)`. Con la decisión 6, `filas_xlsx` ya verifica: se borra la
   llamada a `verificar_hoja_unica` de `cargar_canonico` (con calamine, verificar = parsear
   todo, así que dejarla duplica el costo). `verificar_hoja_unica` sigue existiendo para
   sus otros llamadores (A03, `rem_saludmental`, `poblacion`), reimplementada sobre calamine.
8. **Los no-`.xlsx` siguen cayendo en el MISMO diálogo de hoy.** Antes de abrir,
   `zipfile.is_zipfile(entrada)`; si no, `raise zipfile.BadZipFile(...)`. Así un `.html`
   disfrazado o un `.xls` siguen en `runner.es_error_formato` → «No es un .xlsx», sin
   tocar `runner.py`. (Sin esta guarda, calamine **LEERÍA** un `.xls` de verdad: se
   aceptaría en los loaders pandas y el A05 lo seguiría rechazando. Inconsistente → no.)
   Sonda: calamine levanta `python_calamine.ZipError` (subclase de `CalamineError`, de
   `Exception`) ante un `.html`; `cargar_canonico` ya envuelve toda excepción en
   `no_legible`.
9. **El archivo se libera siempre:** `wb.close()` en un `finally` (OneDrive, §13). La sonda
   confirmó que tras una excepción el archivo queda renombrable; el test lo fija.
10. **`skip_empty_area=False`** en `to_python`: la grilla arranca en A1, igual que openpyxl,
    así los índices de fila (banner de RAYEN) no se corren. Verificado: misma forma en los
    tres exports reales.

## 3. Mapa de cambios

| Archivo | Cambio |
|---|---|
| `programas/rem_utils.py` | Nuevo `_hojas_calamine(entrada, max_filas=None)` → `[(nombre, filas)]` con la coerción (§2.4), la guarda zip (§2.8) y el `finally` (§2.9). `filas_xlsx`, `primeras_filas` y `verificar_hoja_unica` pasan a usarlo. `cargar_canonico` pierde la llamada a `verificar_hoja_unica`. Docstrings de `abrir_xlsx_ro`/`filas_hoja` ajustados. Bump de versión del header. |
| `tools/check_fuentes.py` | `_hojas_calamine` a `LECTORES` y a `TRANSVERSALES` (y al docstring que los enumera). Si no, el hook deja de vigilar al lector nuevo: un patrón que no matchea **no falla, deja de vigilar**. |
| `tests/test_formatos_fuente.py` | Reescribir `test_verificar_hoja_unica_cierra_el_archivo_aunque_la_lectura_reviente`: hoy mockea `abrir_xlsx_ro`, que ya no se llama. Nueva forma = archivo REAL truncado → la excepción sale → `os.replace` del archivo funciona. Los tests de `<dimension>` rota **se quedan como están** (son la prueba de que calamine tampoco trunca). |
| `tests/test_lectura_calamine.py` | Nuevo (§5). |
| `requirements.txt` | `python-calamine` con cota (`pip show python-calamine` → `>=<menor instalada>,<1` si es 0.x) y su comentario, como los otros. |
| `autoREM.spec` | `hiddenimports += ['python_calamine']`. Import con nombre fijo, pero el `.spec` lo lista igual: es la trampa del `gui.app` de la 2.0.0 (tools/CLAUDE.md §11). |
| `CLAUDE.md` raíz | §1 Dependencias (+calamine); §12: cerrar «Rendimiento de lectura» (va al CHANGELOG, con el A05 descartado del §2.3 y su número). |
| `programas/CLAUDE.md` | Fila `rem_utils`: la lectura de exports es calamine; `abrir_xlsx_ro` queda para catálogos/escáner. |
| `tools/CLAUDE.md` §11 | Una línea: el `hiddenimports` de `python_calamine` y por qué. |
| `README.md` | Línea de dependencias (junto a openpyxl/pandas). |

## 4. Pasos

1. Worktree + rama `lectura-calamine` desde `main`. `pip show python-calamine` (el autor
   ya lo instaló).
2. `_hojas_calamine` + los tres lectores + `cargar_canonico` (§3). Nombres y mensajes de
   error: **reusar** los de hoy (tests/CLAUDE.md: los tests importan constantes, no texto).
3. `python tools/correr_tests.py`. **Si un test falla por `None` → `''`** (fixture escrito
   con openpyxl): primero preguntarse si el CÓDIGO distingue `None` de `''`. Producción ya
   ve `''`, así que si el código los trata distinto, **el bug es del código** y el test
   acaba de destaparlo: se arregla ahí y se anota en §9 de este plan. **No** se agrega una
   coerción `''`→`None` para que el test pase (rompería la paridad con RAYEN real).
4. `tests/test_lectura_calamine.py` (§5) + reescribir el test de cierre (§3).
5. **Paridad y tiempo sobre los exports REALES** con un arnés en el scratchpad (partir de
   `docs/evanesced/lectura-calamine/bench_calamine.py`, **sin reescribir el archivado**):
   la versión NUEVA de `filas_xlsx` contra la referencia openpyxl (`abrir_xlsx_ro` +
   `filas_hoja` + `verificar_hoja_unica`, que quedan en el repo), comparando por
   `repr` celda a celda, **sin normalizar nada**. Criterio en §6. Solo imprime conteos.
6. `python tools/check_fuentes.py --todo`, `python tools/check_cp1252.py`,
   `python tools/check_version.py`.
7. `pyinstaller --clean autoREM.spec` (el comando documentado, no uno equivalente) y
   buscar `python_calamine` en `build/autoREM/warn-autoREM.txt`: no debe aparecer como
   faltante. La prueba de abrir el exe es del autor (§6).
8. Docs (§3), skill **`versionar`** (bump **Z** → 2.0.15 si nadie lo tomó; el árbitro es el
   CHANGELOG), y en la entrada del CHANGELOG: los números de §1, la regla de hoja (§2.6),
   las pérdidas aceptadas (§2.5) y **el archivado de `docs/evanesced/lectura-calamine/`**
   (esta sesión de planificación lo dejó hecho y sin entrada propia).
9. Commit en la rama. **No mergear:** primero la revisión ciega
   ([revision_ciega_prompt.md](revision_ciega_prompt.md)), que corre el autor en otra
   sesión. El push lo hace el autor.

## 5. Tests nuevos (`tests/test_lectura_calamine.py`)

Importar primero `_aislar_cache` (tests/CLAUDE.md). Fixtures sintéticos, RUT de ejemplo
`11111111-1`.

1. **Tipos exactos** a través de `filas_xlsx` en un libro escrito con openpyxl: `1` →
   `int`; `2.5` → `float`; `10000000` → `int`; `True` → `bool`; `datetime(2026,8,1)` →
   `datetime` (no `date`); `datetime(2026,8,1,13,5)` → igual; `time(13,5)` → `time`;
   `"0123"` → `"0123"` (el cero a la izquierda es un RUN/código, no un número); `"ñandú"`.
2. **Pérdidas aceptadas fijadas** (§2.5): `#N/A` y `"  "` salen `''`. El docstring dice
   que es un pin de comportamiento conocido, no un requisito.
3. **Paridad con la referencia openpyxl** sobre CADA `.xlsx` versionado de `refs_tablas/`
   (solo encabezado, whitelist): `filas_xlsx` nuevo vs `abrir_xlsx_ro`+`filas_hoja` de la
   hoja con datos, por `repr`, mapeando en la referencia **solo** `None`→`''` y el relleno
   de cola. Cualquier otra diferencia = falla, nombrando archivo, fila y columna.
4. **Hojas:** una sola hoja vacía → `sin_datos`; dos hojas con datos → `modificado`; datos
   en una hoja que NO es la activa → se leen.
5. **No-xlsx:** un `.html` renombrado `.xlsx` → `zipfile.BadZipFile` desde
   `primeras_filas`, `runner.es_error_formato(e)` es `True`, y vía `cargar_canonico` →
   `ArchivoInvalido("no_legible")`.
6. **`primeras_filas(ruta, n)`** devuelve a lo más `n` filas y las mismas que las primeras
   `n` de `filas_xlsx`.

## 6. Criterios de aceptación

- Suite completa verde, y los 4 checks del pre-commit verdes.
- Paso 5, sobre ADA 2026, Informe Inscritos y Formulario PSM de `Datos madre`:
  **0 celdas distintas por `repr`** (con la coerción de enteros, sin normalizar nada más) y
  la misma forma. Tiempo de `filas_xlsx` sobre el ADA **≤ 4 s** (hoy 12,3 s; calamine
  crudo 2,5 s: la coerción celda a celda no puede comerse la ganancia. Si la pasa,
  coercionar solo las columnas que traen floats, no celda a celda).
- Build sin `python_calamine` en el `warn-*.txt`.
- **Manual, lo hace el autor:** abrir el exe, correr SM Actividades de agosto y comparar
  el `SM_Resumen` contra `REM SM/2026/Agosto/REM_SM_actividades_2026_08.xlsx` (hecho con
  la herramienta vieja y validado contra el REM).

## 7. Divergencias esperadas (no son bugs)

- **Tests con fixtures de openpyxl** que veían `None` en celdas vacías ahora ven `''`
  (§4 paso 3 dice qué hacer si uno falla).
- **Un export con la hoja activa vacía y datos en otra** se lee en vez de fallar (§2.6).
- **`#N/A` / solo espacios** → `''` (§2.5).
- `verificar_hoja_unica` sola pasa a costar un parseo completo en rust (~0,2 s en el
  formulario): la usan A03, `rem_saludmental` y `poblacion` antes de su `load_workbook`,
  que sigue costando lo de hoy. No hay ganancia ahí; tampoco pérdida que importe.

## 8. Fuera de alcance: lectores openpyxl que quedan (candidatos siguientes)

Lectores que abren un export **solo para leerlo**, pero con `load_workbook` en modo normal
(el más lento de openpyxl: materializa cada celda como objeto) y recorriendo celdas. Ninguno
necesita pandas para ganar: basta cambiar a `filas_xlsx` y trabajar sobre la lista de filas,
que ya tiene sus gemelos (`formatos.detectar_eje_filas`, `indice_encabezado`).
**Perfilar antes de tomar cualquiera** (§12: el orden de lectura del código se equivocó tres
veces).

| Lector | Qué hace hoy | Por qué es candidato |
|---|---|---|
| `poblacion._leer_formulario_1` | `load_workbook` completo **solo** para `detectar_eje(ws)` y `encontrar_fila_encabezado(ws)`, y después `iter_rows` a una lista | El más claro: termina en una lista de filas igual. Multi-archivo (histórico de años) → paga por cada año. P6 + Rescate |
| `rem_a03_d3_instrumentos.abrir_validado` | `load_workbook` completo + celdas | En la GUI el A03 va por `procesar_unificado`, que escribe un libro NUEVO: el workbook de entrada solo se lee. Revisar el camino standalone (`salida=`), que sí escribe sobre él |
| `estamentos.cargar_estamentos` | `load_workbook` completo + bucle `ws.cell` | Solo lectura. Reporte chico: probablemente no se note |
| `rem_saludmental.abrir_validado` + `marcar_eventos` (A05) | Lee **y escribe** en el mismo workbook | **Descartado, medido** (§2.3): 6,5 s por corrida mensual; no se toca |

## 9. Lo que apareció al implementar

(La sesión que implemente anota acá lo que no calzó con el plan.)

Implementado en la rama `lectura-calamine` (2.0.15), 2026-09-29.

- **Un test destapó un bug del código, no del fixture** (§4 paso 3): `test_a23::test_demografia`.
  `a23.procesar` toma la demografía con `groupby("RUN").last()`, que salta NA pero no `''`;
  RAYEN escribe las vacías como `''`, así que una última atención con la fecha de
  nacimiento en blanco pisaba el dato de las anteriores. Arreglado en `a23.procesar`
  (`''` → NA solo en SEXO/SECTOR/NACION/PUEBLO/FNAC/ANOS), sin coerción `''`→`None` en el
  adaptador. **Ojo:** otros `groupby().last()` (`poblacion.py:532,724`, a23 `:295,:596,:674`)
  tienen la misma forma y la suite no los tocó; no se cambiaron (deuda: revisar si sus
  columnas pueden venir `''` en la última fila).
- **`tools/correr_tests.py` revienta con `UnicodeEncodeError` (cp1252)** al imprimir la
  salida de un grupo que falla con un carácter `�`; oculta QUÉ test falló. Con
  `PYTHONIOENCODING=utf-8 python -m pytest tests` se ve. No se tocó (fuera de alcance).

**Tras la revisión ciega** (2026-09-29, informes en
`docs/evanesced/lectura-calamine/revision_ciega/`), antes del merge:

- **`primeras_filas` vuelve a openpyxl `read_only`**, contra la decisión §2.1 de este plan:
  calamine parsea la hoja ENTERA aunque se le pida `nrows=30`, y la detección al elegir un
  archivo pasaba de 0,9 s a 2,0 s (ADA). El plan asumió que `nrows` cortaba temprano; no
  se midió hasta después. Misma salida por `repr`.
- **Memoria**, que el plan no miraba: el pico del ADA era 558 MB contra 192 de openpyxl.
  Con `iter_rows` + strings reusados: 387 MB de pico, 149 retenidos.
- El error de no-`.xlsx` llevaba la ruta completa (con el usuario de OneDrive): ahora
  solo el nombre.
- Las dos deudas de arriba (`groupby().last()` y el `UnicodeEncodeError` de
  `correr_tests`) pasaron al §12 del CLAUDE.md, para que no queden enterradas en un plan
  cerrado.
- El test de cierre del archivo (§3) quedó como archivo REAL truncado: la guarda
  `is_zipfile` lo corta antes de abrir con calamine, así que prueba que el archivo queda
  libre, no un `finally` propio de calamine.
- Medido (ADA 2026, sin profiler): `filas_xlsx` 3,4 s (criterio ≤ 4 s) con la coerción
  celda a celda; Inscritos 3,4 s; PSM 0,3 s; 0 celdas distintas por `repr` en los tres.
- `bump` rechazó 2.0.15 porque el CHANGELOG ya tenía mi entrada: se bumpeó con el
  encabezado en `[WIP]` y se restauró.
