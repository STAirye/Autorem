import sys
sys.path.insert(0, r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\a40108ff-012a-4b37-baf2-2a1dc332a634\scratchpad")
from ed import reemplazar

R = r"E:\git\Autorem"

reemplazar(R + r"\CHANGELOG.md", [(
'''    un `finally`): un export a medio sincronizar por OneDrive quedaba tomado mientras el
    diálogo de error seguía abierto.
''',
'''    un `finally`): un export a medio sincronizar por OneDrive quedaba tomado mientras el
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
'''), (
'''- **Tests de la ronda 6** (228 en total), con 25 mutantes (13 + 12 del cierre y la
  escritura vía temporal), todos cazados por el test previsto.''',
'''- **Tests de la ronda 6** (237 en total), con 37 mutantes (13 + 12 del cierre y la
  escritura vía temporal + 12 del caché), todos cazados por el test previsto. Los 9 del
  caché: dañado se aparta y avisa; ilegible no se sobreescribe (dotación y estamentos);
  reintento de un bloqueo pasajero y aviso si no se suelta; dos ventanas no se pisan
  (incluido «Quitar omisión»); los avisos se muestran al cerrar los diálogos de dotación
  y al terminar una corrida; «Acerca de» explica y las dos cajas apuntan ahí; y todo
  test aísla el caché real.''')])

reemplazar(R + r"\CLAUDE.md", [(
'''- El caché de usuario vive en **`~/.autorem/`** (`C:\\Users\\<usuario>\\.autorem\\`), no en
  `%APPDATA%` ni junto al exe: `estamentos.json` y `dotacion.json`.''',
'''- El caché de usuario vive en **`~/.autorem/`** (`C:\\Users\\<usuario>\\.autorem\\`), no en
  `%APPDATA%` ni junto al exe: `estamentos.json` y `dotacion.json`. Se lee y guarda por
  `rem_utils.leer_cache_json`/`guardar_cache_json`: **ningún problema de caché es
  callado** (se muestra, y el detalle para el usuario está en «Acerca de»). Los tests
  **nunca** tocan el real: todo `tests/test_*.py` importa primero `_aislar_cache`.''')])

L = R + r"\docs\review_gui-2.0_pendiente.md"
reemplazar(L, [(
'''   **228 tests verdes.**''', '''   **237 tests verdes.**'''), (
'''54 hallazgos en 6 rondas con resultado (la 0 entregó cero; de la 6 queda 1 abierto,
ver §4 «Abiertos de la ronda 6»).''',
'''55 hallazgos en 6 rondas con resultado (la 0 entregó cero).'''), (
'''no de memoria. Siete corregidos, con test mutado (25 mutantes, 25 cazados).''',
'''no de memoria. Nueve corregidos, con test mutado (37 mutantes, 37 cazados).'''), (
'''7. **`rem_utils.verificar_hoja_unica`: `wb.close()` sin `finally`** — una excepción a
   mitad de la lectura dejaba el export bloqueado mientras seguía abierto el diálogo.
''',
'''7. **`rem_utils.verificar_hoja_unica`: `wb.close()` sin `finally`** — una excepción a
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
'''), (
'''### Abiertos de la ronda 6 (§1.G), NO corregidos todavía

- **`dotacion.guardar` falla CALLADO** — ENCOLADO por el autor para una segunda pasada
  de esta revisión («si no se puede guardar el caché, eso rompe MUCHO: necesita un
  manejo de error muy específico»). `guardar(tabla, log=print)` se traga el error, y
  `marcar`/`omitir` lo llaman sin `log`: en el exe `--windowed` `sys.stdout` es None, así
  que un veto de dotación que no llegó al disco no se ve en ninguna parte y el mes
  siguiente vuelve a preguntar todo (con «interno» por defecto). Revisar también
  `estamentos` (mismo patrón de caché en `~/.autorem/`) antes de diseñar el manejo.

''', '''### Para probar a mano (ronda 6)

- **El caché que no se puede escribir, en el PC del trabajo** (el autor lo va a probar en
  OTRO perfil, no en el suyo): quitarle la escritura a `~/.autorem`, procesar SM con
  dotación, y confirmar el diálogo + la línea «NO se puede escribir» en «Acerca de».
  Mismo ejercicio con un `dotacion.json` dañado a mano.

'''), (
'''- **228 tests verdes** (eran 183 al abrir la revisión, 190 tras la ronda 2, 197 tras la 3,
  206 tras la 4, 215 tras la 5). `check_version` OK (1.9.17, 228 tests), `check_cp1252`
  OK (59 archivos).''',
'''- **237 tests verdes** (eran 183 al abrir la revisión, 190 tras la ronda 2, 197 tras la 3,
  206 tras la 4, 215 tras la 5). `check_version` OK (1.9.17, 237 tests), `check_cp1252`
  OK (60 archivos).'''), (
'''| 7 ✅ + 1 encolado (§4) | §1.G |''', '''| 9 ✅ (1 era la suite pisando el caché real) | §1.G |'''), (
'''| 7 | _(siguiente: la segunda pasada del caché que falla callado, §4; quedan reuso/simplificación/altitud, convenciones —headers de versión del resto de `gui/`—, y otra pasada a ojo del autor)_ | | |''',
'''| 7 | _(siguiente: quedan reuso/simplificación/altitud, convenciones —headers de versión del resto de `gui/`—, la prueba a mano del caché en el PC del trabajo (§4), y otra pasada a ojo del autor)_ | | |''')])
print("docs ok")
