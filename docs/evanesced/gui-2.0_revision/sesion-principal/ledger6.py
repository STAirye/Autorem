import sys
sys.path.insert(0, r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\a40108ff-012a-4b37-baf2-2a1dc332a634\scratchpad")
from ed import reemplazar

L = r"E:\git\Autorem\docs\review_gui-2.0_pendiente.md"
reemplazar(L, [(
'''   abierta — no reportar eso como hallazgo). La ronda 5 está sin commit encima.
   **215 tests verdes.**''',
'''   abierta — no reportar eso como hallazgo). Las rondas 5 y 6 están sin commit encima.
   **224 tests verdes.**'''), (
'''46 hallazgos en 5 rondas con resultado (la 0 entregó cero).''',
'''54 hallazgos en 6 rondas con resultado (la 0 entregó cero; de la 6 quedan 3 abiertos,
ver §4 «Abiertos de la ronda 6»).'''), (
'''### §1.E · Estructura y versionado''',
'''### §1.G · Trampas de Tk / customtkinter / hilos (ronda 6)

Ángulo D (trampas de lenguaje y framework). customtkinter **6.0.0 SÍ está instalado**
en el Python 3.9 local (`site-packages/customtkinter`): se verificó contra su fuente,
no de memoria. Cinco corregidos, con test mutado (13 mutantes, 13 cazados).

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

### §1.E · Estructura y versionado'''), (
'''- **215 tests verdes** (eran 183 al abrir la revisión, 190 tras la ronda 2, 197 tras la 3,
  206 tras la 4). `check_version` OK (1.9.17, 215 tests), `check_cp1252` OK (59 archivos).''',
'''- **224 tests verdes** (eran 183 al abrir la revisión, 190 tras la ronda 2, 197 tras la 3,
  206 tras la 4, 215 tras la 5). `check_version` OK (1.9.17, 224 tests), `check_cp1252`
  OK (59 archivos).'''), (
'''  `test_formatos_fuente` 32/32 · `test_gui_registro` 15/15.''',
'''  `test_formatos_fuente` 32/32 · `test_gui_registro` 18/18 · `test_gui_construccion`
  16/16 · `test_autorem` 17/17.'''), (
'''## §4 — QUÉ FALTA
''',
'''## §4 — QUÉ FALTA

### Abiertos de la ronda 6 (§1.G), NO corregidos todavía

- **`dotacion.guardar` falla CALLADO** — ENCOLADO por el autor para una segunda pasada
  de esta revisión («si no se puede guardar el caché, eso rompe MUCHO: necesita un
  manejo de error muy específico»). `guardar(tabla, log=print)` se traga el error, y
  `marcar`/`omitir` lo llaman sin `log`: en el exe `--windowed` `sys.stdout` es None, así
  que un veto de dotación que no llegó al disco no se ve en ninguna parte y el mes
  siguiente vuelve a preguntar todo (con «interno» por defecto). Revisar también
  `estamentos` (mismo patrón de caché en `~/.autorem/`) antes de diseñar el manejo.
- **Cerrar la ventana con una corrida en curso** — pregunta abierta del autor. El worker
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
'''), (
'''| 6 | _(siguiente: quedan reuso/simplificación/altitud, convenciones —headers de versión del resto de `gui/`—, y otra pasada a ojo del autor)_ | | |''',
'''| 6 | **Ángulo D — trampas de lenguaje/framework**: thread-safety de Tk, re-entrada de eventos, excepciones en callbacks, closures, fugas de recursos, pandas, customtkinter (contra su fuente 6.0.0 instalada), rutas de Windows. Con repros empíricos (click encolado despachado dentro de `CTkToplevel`, `wraplength` a 150%) | 5 ✅ + 3 abiertos (§4) | §1.G |
| 7 | _(siguiente: la segunda pasada del caché que falla callado, §4; quedan reuso/simplificación/altitud, convenciones —headers de versión del resto de `gui/`—, y otra pasada a ojo del autor)_ | | |''')])
print("ledger ok")
