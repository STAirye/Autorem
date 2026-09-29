# Fase 2 — des-cegado (diff a567c1a..16f589d, CHANGELOG 2.0.15)

Rama: 1 commit, 13 archivos. Codigo tocado: `programas/rem_utils.py` (lectura), `modulos/rem_a23_respiratorio.py` (1 bloque), `autoREM.spec`, `tools/check_fuentes.py`, requirements, tests, docs.

## Cada DIFF de la fase 1
| DIFF | Clasificacion | Detalle |
|---|---|---|
| LEEME A1 (texto con la version) en los 11 libros | **Declarado** (bump 2.0.14 -> 2.0.15, `VERSION`) | Efecto esperado del versionado; ninguna otra celda cambia. |
| Tiempos: SM -55/-70 %, A23 -47 %, P6 -40 %, A05 sin cambio | **Declarado** (calamine; A05 «no se toca») | Coincide con lo medido por el autor (ADA 12,3 -> 3,4 s). |
| `leer_xlsx` con datos en 2 hojas: base lo lee, cand levanta `modificado` | **Declarado** (regla de hoja: >1 con datos -> `modificado`) | `leer_xlsx` no tiene llamadores de produccion (grep: solo `filas_xlsx` desde el propio `rem_utils`), asi que hoy no se alcanza; es deuda, no riesgo. |
| Mensaje de los no-zip: «File is not a zip file» -> «No es un .xlsx (no es un zip): <ruta completa>» | **Explicable, declarado a medias** | El CHANGELOG anuncia la guarda `is_zipfile`, no el cambio de texto. **Efecto colateral:** el mensaje ahora lleva la RUTA ABSOLUTA del archivo (carpeta de OneDrive con el nombre del usuario) dentro del dialogo y del log; antes solo el nombre. Tipo, `categoria` y `es_error_formato` iguales. |
| A23: demografia (`groupby.last()` sobre `''` -> NA) | **Declarado** («Corregido») | **Con los datos reales de agosto no cambio ninguna celda del A23** (hoja por hoja identica). O sea: el arreglo no se ejercito con dato real, y no hay evidencia mia de que sea inocuo ni de que corrija algo aca. |

Sin DIFF/FAIL «no explicado».

## Efectos colaterales explicables pero no declarados (lo valioso)
1. Ruta absoluta en el mensaje de error de no-zip (arriba).
2. `verificar_hoja_unica` ahora parsea TODAS las hojas con calamine; en el A05 (que sigue abriendo con `openpyxl.load_workbook`) el archivo se lee entero dos veces con dos parsers distintos, y la hoja de trabajo la elige openpyxl (la «activa») mientras la guarda de una hoja la decide calamine («con datos»). Un libro con la activa vacia y datos en otra pasa la guarda de calamine y luego el A05 trabaja sobre la activa vacia. No lo probe.
3. Semantica de la coercion: `float` entero -> `int` para TODA celda. openpyxl devuelve `float` si el XML trae «5.0»; el adaptador lo vuelve `int`. En los exports reales dio 0 diferencias (mi comparacion pasa), pero un export re-guardado por otra herramienta podria cambiar de tipo.
4. Strings de solo espacios y celdas de error -> `''` (declarado como perdida aceptada): puede cambiar un conteo de `no_vacias`/`exigir_filas` en un archivo raro; 0 casos reales.

## Sin cobertura de la revision
- **Formato Administrativo real** (Monitoreo de Actividades/Inasistentes, Otros Cronicos admin, Formulario admin, Cupos): solo pase fixtures de encabezado y los 3 tests de paridad del autor sobre `refs_tablas`; ningun export admin real.
- **PSC / PSC-Y / A03 admin**: sin input real; A03 solo con Goldberg (2 filas).
- **`primeras_filas` + `detectar_formato_filas` sobre un export real grande** (lo que hace la GUI al elegir archivo, `a05.py:124` y `sm.py:97` con `nrows`): mi e2e llama a `_correr_tareas` directo, no a `preparar`/`detectar_ahora`; los caminos de `nrows` solo se probaron con fixtures pequenos.
- **Memoria**: `_hojas_calamine` materializa todas las hojas como listas de tuplas (ADA 4 M de celdas, Inscritos 5 M) y ademas las convierte con `_celda_openpyxl`; no medi RSS ni el pico. En el PC del trabajo (menos RAM) puede importar.
- **Libro con la hoja activa vacia y datos en otra** (el cambio de regla): no probe la corrida completa, solo `leer_xlsx`.
- **Coercion de tipos en archivos NO producidos por RAYEN** (ver 3).
- **`.xls` renombrado a `.xlsx`** (guarda `is_zipfile`): probe html y truncado, no un `.xls` binario real.
- **Estamentos, Dotacion, Catalogos, escaner de PII** (siguen con openpyxl segun el diff): sin cambios que probar, pero `abrir_xlsx_ro` cambio de docstring solamente.
- **El exe**: compilado pero no ejecutado; el `hiddenimports` de `python_calamine` no distingue nada en mi comparacion porque la base ya empaqueta `python_calamine` (via `pandas.io.excel._calamine`): la prueba manual del exe sigue siendo necesaria, sobre todo porque el build in-tree de la candidata dio `PermissionError` en `build\autoREM\localpycs`.
- **El test reescrito** `test_verificar_hoja_unica_cierra_el_archivo...`: paso de un mock que verificaba `close()` a un archivo real truncado + `os.replace`; cubre el caso zip roto, no una excepcion a mitad de lectura de un zip valido.
