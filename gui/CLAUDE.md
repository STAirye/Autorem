<!--
This document was generated with the assistance of Claude Opus 5 (Anthropic).
The human author reviewed, modified, and integrated the content.
Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# gui/ — GUI 2.0 (customtkinter)

Se carga al trabajar en `gui/`. Los `§N` son las anclas del [CLAUDE.md raíz](../CLAUDE.md).
Plan: [docs/GUI_2.0_plan.md](../docs/GUI_2.0_plan.md). Registro de la revisión de la rama:
[docs/review_gui-2.0_pendiente.md](../docs/review_gui-2.0_pendiente.md).

**El contrato `PANTALLA` está documentado en el docstring de `gui/app.py`** — no se repite
acá. Este archivo es lo que ese docstring no dice: qué trampa ya mordió, y dónde.

**Cómo se corre:** `python -m gui.app`. `autorem.py` sigue lanzando la GUI 1.x y es el único
entry point del `.exe`; las dos conviven hasta el **paso 11** del plan (§12). No se toca
`autorem.py` antes de eso.

## Archivos

| Archivo | Rol |
|---|---|
| `app.py` | **Shell:** ventana, sidebar, router, `_resolver_ctx`, construcción de cada página desde su `PANTALLA`, `_al_cerrar`. El contrato completo, en su docstring. |
| `registro.py` | **Descubrimiento** de `gui/paginas/*.py` por `pkgutil` + `ORDEN_PROGRAMAS` / `ORDEN_PAGINAS`. Agregar una página no requiere tocar este archivo; sí agregarla al orden. |
| `runner.py` | **Única frontera con el worker:** hilo + cola, despacho de errores (`manejar_error`, `motivo_fuente`, `_TITULO_INVALIDO`), validaciones de entrada (`valida_ruta` / `valida_mes` / `valida_carpeta`, `limpiar_ruta`), avisos de caché, `en_hilo`, `correr_con_reloj`, `sin_opcional`. |
| `widgets.py` | Piezas de UI reutilizables: `fila_archivo(s)`, `fila_carpeta_salida`, `selector_mes`, `crear_log`, `caja_titulada`, `etiqueta_envolvente`, banner de fuente, `texto_avisos`, la paleta (`COLOR_*`). |
| `dialogos.py` | Modales de **Estamentos** y **Dotación** (`bloque_*`, `dotacion_ada`, `dialogo_dotacion`, `revisar_dotacion`) + la lógica pura testeable (`valores_iniciales`, `decisiones_cambiadas`). |
| `paginas/*.py` | Una pantalla por archivo: `a05`, `sm`, `a23`, `poblacion` exponen `PANTALLA`; `inicio` y `about` exponen `construir(frame, app)` y NO son `PANTALLA`. |

## Checklist de página nueva

1. `gui/paginas/<nombre>.py` con `PANTALLA` (claves obligatorias: `id`, `programa`,
   `titulo`, `estado`, `inputs`, `mes`, `carpeta_salida`, `correr`, `resumen` — las amarra
   `tests/test_gui_registro.py::test_claves_obligatorias`).
2. Sumarla a **`registro.ORDEN_PAGINAS`** y su programa a `ORDEN_PROGRAMAS`. Omitirlo no
   revienta (fail soft: se agrega al final), pero el orden deja de ser un dato.
3. **Un** input con `ancla_salida: True` — el que fija la carpeta de salida por defecto.
4. `estado: "beta"` si el módulo está en validación: pinta el badge. **No** se crea un
   programa aparte para decir «en validación» (ver trampa «posición y agrupación»).
5. Entrada en `COBERTURA` (`programas/cobertura.py`) si corresponde a un módulo, o
   `tests/test_cobertura.py` falla.
6. Si lee una planilla del usuario, **contrato** en `tests/contratos_fuentes.py` — lo exige
   `check_fuentes` (`CARPETAS` incluye `gui`). Skill `tests-fuentes`.
7. Header de versión: **`gui/` está en `DIRS_VERSIONADOS`** de `check_version.py`.

## Trampas (todas mordieron de verdad)

**Hilos y Tk**

- **`widget.after(...)` desde el worker NO es thread-safe** (registra un comando Tcl):
  `RuntimeError: main thread is not in main loop`, o corrupción intermitente. Para volver al
  hilo de la GUI, **`runner.en_hilo(widget, trabajo, al_terminar)`** — cola + poll.
- **Una excepción en un callback de Tk es INVISIBLE** en un exe `--windowed`. Todo lo que
  pueda fallar y el usuario deba ver pasa por `runner.manejar_error` / `error_inesperado`.
  Ojo con `preparar`, `al_completar` y `resumen`: corren en el hilo de la GUI, fuera del
  `try` del worker.
- **`ctk.CTkToplevel.__init__` hace un `update()` COMPLETO en Windows** (repinta la barra de
  título), así que despacha eventos encolados *dentro del constructor*: un click en cola
  puede abrir una segunda ventana. Candado: `dialogos._una_ventana_dotacion`.
- **Nada de Tk vars en el worker.** `_resolver_ctx` aplana todos los getters a un `ctx` de
  `Path`/tuplas/listas antes de lanzar el hilo, y valida las rutas ahí — no a mitad de
  corrida.
- **`CTkScrollableFrame` redefine `grid`/`grid_remove`/`lift`** (operan sobre su
  `_parent_frame`) pero **no** `tkraise`.

**Posición y agrupación: es un DATO, nunca el orden en que corrió algo**

Esta clase de bug apareció **cuatro** veces (sidebar, páginas dentro del grupo,
Inicio/Acerca de, y el programa de Población). Si la posición o el agrupamiento sale de
«dónde cayó el bucle» o «cómo se llama el `.py`», está mal:

- El orden de las páginas viene de `ORDEN_PAGINAS`, no de `pkgutil` (que ordena por nombre
  de archivo: renombrar `sm.py` las daba vuelta en silencio).
- Inicio y Acerca de declaran `posicion: "arriba"` / `"abajo"`.
- **Un programa = un grupo del sidebar**, por igualdad exacta. No agrupar por PREFIJO, y no
  inventar un programa para expresar un estado: eso es `estado`.
- **El router muestra/esconde** (`grid` / `grid_remove`), no apila páginas en la misma celda.
  Apilarlas deja la tapada **mapeada**, y el Tab del teclado recorre lo mapeado: se llegaba
  a las cajas de texto de otras páginas y lo tecleado no aparecía en ninguna parte.

**Archivos y datos**

- **Detectar por CONTENIDO, y no cachear por ruta** (regla 5): RAYEN baja todo como
  `Formulario_Rayen.xlsx` y OneDrive entrega el `.xlsx` a medio bajar (§13). Bajo el mismo
  nombre el contenido cambia todo el tiempo → `a05.detectar_ahora()` **re-lee siempre**.
- **Un input de UN archivo va `multi: False`.** Declarado múltiple se pueden elegir varios
  con ctrl-click y `correr` usa `[0]`: el resto se descarta callado.
- **Los opcionales se cargan PRIMERO** en el `procesar` del módulo. Un opcional inválido
  levanta `OpcionalInvalido` → `runner.sin_opcional` pregunta «¿continuar sin él?» y
  **re-corre el módulo entero**: si el opcional se lee al final, la pregunta llega después
  del minuto de corrida y el «Sí» repite todo.
- **La carpeta de salida por defecto es la de los inputs**, nunca el cwd (§2): las salidas
  llevan RUT y van junto a los exports, fuera del repo. Eso es `ancla_salida`.
- Toda salida pasa por `rem_utils.rutas_libres` + `escribir_atomico`: nunca se pisa una
  salida, y un corte no deja un `.xlsx` roto con nombre de resultado.

## Qué NO se re-implementa

La ronda 8 encontró cinco copias de algo que ya existía, y **tres ya habían divergido**.
Antes de escribir un helper acá, buscarlo en:

| Necesito… | Está en |
|---|---|
| Limpiar / validar una ruta, una carpeta o un mes | `runner.limpiar_ruta`, `valida_ruta`, `valida_carpeta`, `valida_mes` |
| El selector de mes (con su rango amarrado por test) | `widgets.selector_mes` (A05 lo usa sin etiqueta y prende/apaga `get.spinboxes`) |
| La ruta del Maestro slim o de un catálogo | `programas.catalogos.maestro_slim` / `_carpetas` |
| Ubicar el encabezado de un export para un preview | `rem_utils.indice_encabezado` + `primeras_filas` (mismo criterio que el loader) |
| Mostrar avisos de una corrida | `widgets.texto_avisos` + `attrs["avisos"]`; el banner, `widgets.pintar_banner_fuente` |
| Volver al hilo de la GUI | `runner.en_hilo` |

## Tests

**51 tests** (`def test_`: 26 + 25). `tests/test_gui_registro.py` amarra el CONTRATO (claves,
ids únicos, orden declarado, `extras[].despues_de` apuntando a un input real, una sola
`ancla_salida`, callables invocables) y `tests/test_gui_construccion.py` **arma la ventana de
verdad** y bombea eventos — es lo que cazó el `after()` desde el hilo. Las dos necesitan
`customtkinter`; en la corrida completa de `pytest` sale a veces un `tk.tcl` intermitente de
`test_gui_construccion` (pasa solo, se investiga aparte).

Convención al escribir estos tests: **no comparar texto plano que ve el usuario** — ver
[tests/CLAUDE.md](../tests/CLAUDE.md). Si el test necesita el texto, éste vive UNA vez como
constante del módulo que lo muestra (`a05.TITULO_FALTA_ACUSE`, `runner.TITULO_NO_ENCONTRADO`,
`widgets.NO_SE_GENERO`) y el test la importa.

## Pendiente al paso 11 (el merge)

- **`autorem.py` todavía corre la GUI 1.x.** Al enchufar la 2.0, pasarle el `ruta_inicial` de
  `main()` a `gui.app.lanzar(ruta_inicial)` — el canal ya existe.
- **El `import` de `gui.app` tiene que ir a NIVEL DE MÓDULO**, o sumar `'gui.app'` a
  `hiddenimports`: todos los imports de `autorem.py` son locales a la función, y PyInstaller
  no los ve → el exe congelado muere con `ModuleNotFoundError` con el `.spec` ya «arreglado».
  `gui/paginas/*` ya entra por `collect_submodules('gui.paginas')` en `autoREM.spec` (se
  descubren en runtime con `pkgutil`, así que el análisis estático no las veía).
- **`runner.py` duplica helpers de `autorem.py` y ya divergieron** (hallazgo #14): se
  resuelve con el merge, no antes.
- Los mensajes de `validar_iris`/`validar_admin` dicen «Cambia el selector de formato», y ese
  selector no existe en la 2.0. Solo se alcanzan desde el CLI y el notebook 1.x, las dos
  superficies **congeladas** (§12); se revisan si el CLI revive.
