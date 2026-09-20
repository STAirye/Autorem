import sys
sys.path.insert(0, r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\a40108ff-012a-4b37-baf2-2a1dc332a634\scratchpad")
from ed import reemplazar

L = r"E:\git\Autorem\docs\review_gui-2.0_pendiente.md"
reemplazar(L, [(
'''5. Estado del árbol: **todo sin commit**, en el working tree de `gui-2.0`, versión
   **1.9.17**, **206 tests verdes**.''',
'''5. Estado del árbol: las rondas 1-4 están en **`fd1b0cc`, un commit de RESPALDO**
   (pusheado a `origin/gui-2.0` solo para no tener 5k líneas sin copia remota; **no es
   un release**: la versión sigue en **1.9.17** y la entrada del CHANGELOG sigue
   abierta — no reportar eso como hallazgo). La ronda 5 está sin commit encima.
   **215 tests verdes.**'''), (
'''41 hallazgos en 4 rondas con resultado (la 0 entregó cero).''',
'''46 hallazgos en 5 rondas con resultado (la 0 entregó cero).'''), (
'''- Detección de formato del A05 con `read_only=True`: la `<dimension>` ausente o rota de
  RAYEN hacía **rechazar un archivo válido**. Ahora sin `read_only`, igual que
  `sm.abrir_validado`, que es quien procesa después.''',
'''- Detección de formato del A05 con `read_only=True`: la `<dimension>` ausente o rota de
  RAYEN hacía **rechazar un archivo válido**. Ahora sin `read_only`, igual que
  `sm.abrir_validado`, que es quien procesa después. **[Superado:** la ronda 4 volvió a
  `read_only` para leer solo el encabezado (§1.E-bis) y reabrió este bug; la ronda 5 lo
  cerró de verdad con `rem_utils.abrir_xlsx_ro`, ver §1.F.**]**'''), (
'''La detección lee con `read_only=True` + `islice(..., MAX_FILAS_HEADER)`. Tests que amarran
que el atajo **no cambie la respuesta** sobre los dos exports A05 reales del repo.
''',
'''La detección lee con `read_only=True` + `islice(..., MAX_FILAS_HEADER)`. Tests que amarran
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
'''), (
'''- **206 tests verdes** (eran 183 al abrir la revisión, 190 tras la ronda 2, 197 tras la 3).
  `check_version` OK (1.9.17, 206 tests), `check_cp1252` OK (59 archivos).''',
'''- **215 tests verdes** (eran 183 al abrir la revisión, 190 tras la ronda 2, 197 tras la 3,
  206 tras la 4). `check_version` OK (1.9.17, 215 tests), `check_cp1252` OK (59 archivos).'''), (
'''  `test_formatos_fuente` 25/25 · `test_gui_registro` 15/15.''',
'''  `test_formatos_fuente` 32/32 · `test_gui_registro` 15/15.'''), (
'''- **Un test cambió de expectativa a propósito:**''',
'''- **Tests de la ronda 5 (9):** `test_formatos_fuente.py` (6, 7 casos: `leer_xlsx` no
  trunca; `verificar_hoja_unica` ve la hoja extra; detección A05 sobre el IRIS real con
  la `<dimension>` en `A1`; el escaneo de PII ve un RUT fuera de la etiqueta; el catálogo
  se lee entero; fuente multi-archivo igual en los dos órdenes) · `test_gui_construccion.py`
  (2: la PÁGINA del A05 y el preview del SM con la `<dimension>` rota; ruta con comillas)
  · `test_dotacion.py` (1: `sin_estamento`). Cada test de `<dimension>` comprueba
  **primero** que el fixture arma la trampa (un read_only pelado sí trunca), para no
  quedar verde por un fixture que dejó de reproducirla.
- **Un test cambió de expectativa a propósito:**'''), (
'''| 5 | _(siguiente: quedan reuso/simplificación/altitud, convenciones —headers de versión del resto de `gui/`—, y otra pasada a ojo del autor)_ | | |''',
'''| 5 | **Ángulo C — trazado entre archivos**: cada llamada de `gui/` a `programas/`/`modulos/`/`autorem.py`/`tools/` contra firma, retorno, attrs, excepciones y precondiciones del callee; y al revés, los consumidores de lo que el diff cambió (`cargar_inscritos`, `catalogos/`). Con repros empíricos (`<dimension>` fabricada, ADA mixto IRIS+Monitoreo, ruta con comillas) | 5 ✅ (1 era regresión de la ronda 4) | §1.F |
| 6 | _(siguiente: quedan reuso/simplificación/altitud, convenciones —headers de versión del resto de `gui/`—, y otra pasada a ojo del autor)_ | | |''')])
print("ledger ok")
