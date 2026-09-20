import sys
sys.path.insert(0, r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\a40108ff-012a-4b37-baf2-2a1dc332a634\scratchpad")
from ed import reemplazar

R = r"E:\git\Autorem"
reemplazar(R + r"\CLAUDE.md", [(
'''  corrida entera sale como `… (1).xlsx`, con el mismo número en todos sus archivos.''',
'''  corrida entera sale como `… (1).xlsx`, con el mismo número en todos sus archivos. Y
  se escribe vía temporal + rename (`escribir_atomico`): un corte deja un
  `….escribiendo.xlsx`, nunca un resultado roto con nombre de resultado.''')])

reemplazar(R + r"\programas\CLAUDE.md", [(
'''**`rutas_libres`** (toda salida pasa por ahí: nunca se sobreescribe, sale `… (1).xlsx`). |''',
'''**`rutas_libres`** + **`escribir_atomico`** (toda salida pasa por los dos: nunca se sobreescribe, sale `… (1).xlsx`, y se escribe a un temporal que se renombra al terminar). |''')])

reemplazar(R + r"\CHANGELOG.md", [(
'''    resumen dice «NO se generó (motivo)», y las salidas ya no se pisan (ver «Cambiado»).
''',
'''    resumen dice «NO se generó (motivo)», y las salidas ya no se pisan (ver «Cambiado»).
  - **Cerrar la ventana con una corrida en curso la mataba sin avisar**, incluso a mitad
    de escribir el `.xlsx` (el worker es un hilo daemon: muere con el proceso). Ahora la
    X pregunta si hay una corrida viva («No» por defecto), y toda salida se escribe a un
    temporal que se renombra al terminar (`rem_utils.escribir_atomico`): un corte deja un
    `….escribiendo.xlsx`, nunca un resultado roto con nombre de resultado.
  - **`verificar_hoja_unica` dejaba el export bloqueado si la lectura reventaba**
    (read_only mantiene el archivo abierto hasta `close()`, y ese `close()` no estaba en
    un `finally`): un export a medio sincronizar por OneDrive quedaba tomado mientras el
    diálogo de error seguía abierto.
'''), (
'''- **Tests de la ronda 6** (224 en total), con 13 mutantes, los 13 cazados por el test
  previsto:''',
'''- **Tests de la ronda 6** (228 en total), con 25 mutantes (13 + 12 del cierre y la
  escritura vía temporal), todos cazados por el test previsto. Los 4 de la segunda
  tanda: `escribir_atomico` (el nombre final no existe mientras se escribe; una
  escritura fallida no deja basura), el A05 escribe vía temporal, la X de la ventana
  pregunta con una corrida viva (por el comando REGISTRADO, no un método llamado a
  mano) y `verificar_hoja_unica` cierra aunque reviente; más el cableado del temporal en
  SM/A23/Población dentro de sus tests. La primera tanda:''')])

L = R + r"\docs\review_gui-2.0_pendiente.md"
reemplazar(L, [(
'''   abierta — no reportar eso como hallazgo). Las rondas 5 y 6 están sin commit encima.
   **224 tests verdes.**''',
'''   abierta — no reportar eso como hallazgo). Las rondas 5 y 6 están sin commit encima.
   **228 tests verdes.**'''), (
'''54 hallazgos en 6 rondas con resultado (la 0 entregó cero; de la 6 quedan 3 abiertos,
ver §4 «Abiertos de la ronda 6»).''',
'''54 hallazgos en 6 rondas con resultado (la 0 entregó cero; de la 6 queda 1 abierto,
ver §4 «Abiertos de la ronda 6»).'''), (
'''no de memoria. Cinco corregidos, con test mutado (13 mutantes, 13 cazados).''',
'''no de memoria. Siete corregidos, con test mutado (25 mutantes, 25 cazados).'''), (
'''   MISMO número), y el resumen dice «NO se generó (motivo)».
''',
'''   MISMO número), y el resumen dice «NO se generó (motivo)».
6. **Cerrar la ventana con una corrida viva** la mataba sin avisar (worker `daemon`,
   sin `WM_DELETE_WINDOW`), incluso escribiendo el `.xlsx`. Arreglo, sin timeout:
   `App._al_cerrar` pregunta si hay corridas vivas (`App._corridas`, «No» por defecto),
   y **toda salida se escribe vía `rem_utils.escribir_atomico`** (temporal +
   `os.replace`): un corte deja un `….escribiendo.xlsx`, nunca un `.xlsx` roto con
   nombre de resultado.
7. **`rem_utils.verificar_hoja_unica`: `wb.close()` sin `finally`** — una excepción a
   mitad de la lectura dejaba el export bloqueado mientras seguía abierto el diálogo.
'''), (
'''- **Cerrar la ventana con una corrida en curso** — pregunta abierta del autor. El worker
  es `daemon=True` y `App` no tiene `WM_DELETE_WINDOW`: al cerrar, el proceso termina y
  mata el hilo donde esté, incluso escribiendo el `.xlsx`. No revienta nada visible: el
  programa simplemente se cierra. Con `rutas_libres` ya no puede destruir una salida
  anterior buena; lo que queda es un archivo NUEVO a medio escribir. Opción propuesta
  (sin timeout): `protocol("WM_DELETE_WINDOW")` que, si hay una corrida viva, pregunte
  «hay una corrida en curso, ¿cerrar igual?»; y opcionalmente escribir a un temporal +
  `os.replace` para que un corte nunca deje un `.xlsx` roto con nombre de resultado.
- **`rem_utils.verificar_hoja_unica` sin `try/finally`** alrededor de `wb.close()` (sus
  hermanos sí lo tienen): una excepción a mitad de la iteración (un export a medio
  sincronizar por OneDrive) deja el `.xlsx` bloqueado mientras el diálogo de error sigue
  abierto. Reportado en la ronda 6; el autor no se pronunció.
''', ''), (
'''- **224 tests verdes** (eran 183 al abrir la revisión, 190 tras la ronda 2, 197 tras la 3,
  206 tras la 4, 215 tras la 5). `check_version` OK (1.9.17, 224 tests), `check_cp1252`
  OK (59 archivos).''',
'''- **228 tests verdes** (eran 183 al abrir la revisión, 190 tras la ronda 2, 197 tras la 3,
  206 tras la 4, 215 tras la 5). `check_version` OK (1.9.17, 228 tests), `check_cp1252`
  OK (59 archivos).'''), (
'''  `test_formatos_fuente` 32/32 · `test_gui_registro` 18/18 · `test_gui_construccion`
  16/16 · `test_autorem` 17/17.''',
'''  `test_formatos_fuente` 33/33 · `test_gui_registro` 18/18 · `test_gui_construccion`
  17/17 · `test_autorem` 19/19.'''), (
'''| 5 ✅ + 3 abiertos (§4) | §1.G |''',
'''| 7 ✅ + 1 encolado (§4) | §1.G |''')])
print("docs ok")
