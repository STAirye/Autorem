<!--
This document was generated with the assistance of Claude Opus 5 (Anthropic).
The human author reviewed, modified, and integrated the content.

Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
Copyright (C) 2026 Simón Tobar
SPDX-License-Identifier: GPL-3.0-or-later
Version: 1.9.4 (plan; la implementación bumpea, ver §9)
-->

# Plan — GUI 2.0 (customtkinter)

Documento **autocontenido**: escrito para una sesión fría que solo lee este archivo
y `CLAUDE.md`. Estado al 8-sep-2026, sobre `autorem.py` v1.9.4 (1274 líneas).

---

## 0. Decisiones ya tomadas (con el autor, sep-2026)

| Pregunta | Decisión |
|---|---|
| Profundidad | **Rediseño completo**: sidebar de navegación en vez de `ttk.Notebook`, tema, pantalla de inicio. |
| Alcance funcional | Entra **todo** el roadmap de GUI 2.0: About/contacto/licencia · agrupar por Programa de salud · sacar la pestaña A03 standalone · sacar el selector IRIS/Administrativo. |
| GUI antigua | **Congelada y comprimida** en `legacy/autorem_gui_tk_1.9.4.py.gz` (§8). |
| Base | `customtkinter` — **6.0.0 ya instalado** en la máquina del autor. |

**Ojo con CTk 6:** cambió API respecto de la serie 5.x, que es la de casi todos los
ejemplos que circulan. Verificar cada widget contra la doc/fuente de la versión
instalada (`python -c "import customtkinter,inspect,pathlib;print(pathlib.Path(customtkinter.__file__).parent)"`),
no contra tutoriales. Esto es lo primero que hay que hacer al implementar.

---

## 1. Por qué la 2.0 no es solo pintura

Medido sobre el archivo actual: las pestañas son **~80% declaración** y ~20% lógica.
`_tab_sm` son 150 líneas, de las cuales unas 30 hacen algo. El resto dice: qué
archivos pide, cuáles son obligatorios, si lleva selector de mes, dónde guarda.

Consecuencia: **sumar un módulo cuesta ~150 líneas de Tk a mano**, y ese costo es el
que hace que la GUI se quede atrás de los módulos (hoy el P6 y el rescate viven
apretados en una pestaña llamada "BETA").

Además, el agrupamiento por Programa de salud **obliga** a que algo sepa que el A05
pertenece a Salud Mental. O ese saber se hardcodea en el shell, o vive en un
registro. El repo ya resolvió esto tres veces con el mismo patrón —
`TAREA` (modulos), `COBERTURA` (cobertura.py), `CATALOGOS` (catalogos.py)— y no hay
motivo para inventar un cuarto.

**Por eso el rediseño se implementa sobre una capa declarativa.** No es alcance extra:
es el mecanismo que hace baratos el sidebar, el agrupamiento y los estados BETA.

---

## 2. Estructura de archivos propuesta

```
autorem.py              queda como ENTRY POINT + CLI. La GUI se va; delega en gui.app.lanzar()
gui/                    paquete NUEVO
  __init__.py
  app.py                shell: ventana, sidebar, router, tema, pantalla de inicio
  registro.py           REGISTRO de pantallas (declarativo) + orden de programas
  widgets.py            primitivas CTk: FilaArchivo(s), CarpetaSalida, SelectorMes,
                        CajaLog, Reloj, SeparadorOpcionales, AvisoSinModificar
  runner.py             correr_con_reloj (hilo + queue + poll), portado tal cual
  paginas/
    a05.py  a03.py  a23.py  sm.py  poblacion.py  about.py  inicio.py
legacy/
  autorem_gui_tk_1.9.4.py.gz    congelado, comprimido (§8)
```

**Qué se porta sin tocar la lógica:** `_correr_con_reloj`, `_Reloj`, `_manejar_error`,
`_es_error_formato`, `_valida_ruta`, `_valida_carpeta`, `_dir_salida_default`,
`_slim_por_defecto`, `_abrir_carpeta`, `_bloque_estamentos`, `_resolver_estamentos`.
Son correctos y están validados; solo cambian de módulo y de widget base. **No
aprovechar la migración para reescribirlos.**

`_correr_tareas` y `main_cli` **se quedan en `autorem.py`**: no son GUI, y
`tests/test_autorem.py:297` los usa.

---

## 3. La capa declarativa: `PANTALLA`

Cada página expone un dict `PANTALLA` (mismo espíritu que `TAREA`):

```python
PANTALLA = {
    "id": "sm_actividades",
    "programa": "Salud Mental",          # agrupa en el sidebar
    "titulo": "Actividades",
    "estado": "estable",                 # "estable" | "beta"  -> badge en el sidebar
    "instrucciones": "...",
    "inputs": [
        {"key": "ada", "etiqueta": "Atenciones/Diag/Activ (ADA)", "multi": True,
         "obligatorio": True, "titulo_dialogo": "...", "ayuda": "..."},
        {"key": "grupal", ...},
        {"key": "inscritos", "obligatorio": False, ...},
    ],
    "mes": True,                         # muestra el selector año/mes
    "carpeta_salida": True,
    "extras": None,                      # opcional: callable(frame) -> get_extras()
    "correr": correr,                    # callable(ctx, log) -> resultado
    "resumen": resumen,                  # callable(resultado) -> str para el messagebox
}
```

`app.py` construye la página entera desde el dict. Los inputs obligatorios van
arriba, los opcionales bajo el separador (comportamiento actual).

### 3.1 El escape hatch `extras` (no es opcional, hace falta)

Las pantallas **no** son todas iguales y forzarlas al mismo molde sería peor que el
Tk actual. Casos reales que no caben en la declaración:

- **A05:** caja "Período" (archivo completo / un mes) — no es el `SelectorMes` normal.
- **SM Actividades:** checkbox "¿Incluir cuestionarios?" que despliega el bloque A03.
- **A03 / cualquier flujo Administrativo:** `_bloque_estamentos`.
- **Población:** corre DOS módulos (P6 + rescate) con try independiente cada uno.

`extras(frame)` recibe el frame de la página, dibuja lo que necesite, y devuelve un
**getter sin argumentos** que `app.py` llama en el hilo de la GUI.

### 3.2 Invariante dura: nada de Tk vars en el worker

`app.py` resuelve **todos** los `StringVar`/`BooleanVar` a un dict plano `ctx`
**antes** de lanzar el hilo. `correr(ctx, log)` no toca widgets ni variables Tk.

Esto ya es un problema conocido: `_tab_sm` lo maneja a mano y lo dice en un
comentario ("Tk vars no son thread-safe -> resolver en el hilo GUI y pasar los
valores capturados al worker"). En la 2.0 deja de ser una precaución que hay que
recordar en cada pantalla y pasa a ser una regla del constructor.

`ctx` contiene: rutas ya validadas (`Path`), `mes=(y, m)`, `carpeta` (Path), y lo que
devolvió `extras`.

---

## 4. Shell: sidebar, router, inicio

**Sidebar** con secciones por programa. Un nivel visible, encabezado no clickeable +
botones de pantalla:

```
autoREM 2.0.0
-----------------------------
SALUD MENTAL
  A05 Egresos / Ingresos
  Actividades
  Población en control    [BETA]
RESPIRATORIO
  A23
-----------------------------
Inicio
Acerca de
```

- Se construye **desde `REGISTRO`**, agrupando por `programa` en el orden declarado.
- `estado: "beta"` pinta un badge. Con esto **desaparece la pestaña "BETA"**: el P6 y
  el rescate pasan a Salud Mental / Población con badge propio. BETA es un estado de
  una pantalla, no un programa de salud — la pestaña actual era un parche.
- **Construcción perezosa:** la página se arma la primera vez que se visita. Hoy las 5
  pestañas se construyen todas al arrancar; con `--onefile` (que ya descomprime ~37 MB,
  CLAUDE.md §11) cada milisegundo de arranque se nota.
- El área de contenido intercambia frames (`grid`/`tkraise`), no destruye: volver a una
  pantalla conserva las rutas ya elegidas y el log de la corrida anterior.

**Pantalla de inicio:** qué hace autoREM en tres líneas, versión, y accesos a lo más
usado. **No** es el lugar del aviso "cargar los exports SIN modificar": ese aviso es
una salvaguarda fail-loud (un archivo tocado rompía el A23 en silencio), y moverlo a
una pantalla que se ve una vez lo debilita. Va **compacto en cada página** que recibe
un export, como hoy.

**Tema:** claro por defecto. El modo oscuro es gratis en CTk (`set_appearance_mode`),
pero **verificar los colores hardcodeados** que se arrastran del Tk actual —
`#a05a00` (avisos), `#888` / `#666` (texto atenuado), `#c8801a` / `#5a3200` (el reloj
de arena) — que en fondo oscuro pueden quedar ilegibles. O se centralizan en una
paleta de `widgets.py`, o el modo oscuro se deja fuera de la 2.0. **No dejar el toggle
puesto sin haber mirado las tres pantallas en oscuro.**

---

## 5. Sacar el selector IRIS / Administrativo

**Por qué se va** (ya razonado en CLAUDE.md §12): `validar_iris`/`validar_admin`
llaman a `detectar_formato` y **bloquean** si tu elección no coincide. La única salida
es cambiar el selector hasta que calce. O sea la detección ya es la autoridad única y
el selector solo aporta una forma de equivocarse.

**Diseño propuesto (revisar con el autor antes de implementar):**

1. Al elegir el archivo, se abre y se corre `sm.detectar_formato(ws)`.
2. El resultado se muestra **en la página**, como label vivo:
   `Formato detectado: IRIS` / `Formato detectado: Administrativo`.
3. Si es **Administrativo**, junto al label va el disclaimer (`_DISCLAIMER_ADMIN`:
   sin demografía) **más un checkbox de acuse** — "Entiendo que las columnas
   demográficas saldrán vacías". Ese formato **degrada datos**, y ahí sí se justifica
   una fricción explícita.
4. Si es `desconocido`, **fail loud**: no se procesa, y el mensaje dice qué se buscó
   (ancla IRIS / banner + markers admin) para que el usuario sepa qué revisar.

**Lo que NO se hace: permitir forzar el perfil.** Procesar un export con el perfil
equivocado da números plausibles, callados y errados — exactamente lo que el proyecto
prohíbe. Si el usuario cree que la detección se equivocó, el camino es revisar qué
descargó, no pisar la detección.

`--perfil` en el CLI **se conserva** como override de experto (el CLI no tiene a quién
preguntarle).

**Diferencia con CLAUDE.md §7**, que pide "confirmar con el usuario (¿correcto? S/N)":
un modal en cada corrida de una tarea mensual rutinaria se convierte en un click
reflejo, y un aviso que grita siempre deja de leerse (mismo argumento que ya se usó
para `parcial` vs `cambiada` en `formatos.py`). El label permanente + acuse solo
cuando hay pérdida de datos conserva el fail-loud sin la fricción muerta.
**Si el autor prefiere el modal, es un cambio chico: el punto de decisión es el mismo.**

---

## 6. Sacar la pestaña A03 standalone

`_bloque_a03` sobrevive dentro de Actividades (checkbox "¿Incluir cuestionarios?");
se borra `_tab_a03` y su `_correr_a03`.

**Regresión que hay que resolver, no solo borrar:** hoy la pestaña standalone permite
tabular **solo** los cuestionarios. La pestaña Actividades exige ADA **y** Grupal. Si
se borra la standalone tal cual, para sacar la tabla A03·D.3 habría que cargar dos
exports que no se usan.

**Solución:** en la página SM, si "Incluir cuestionarios" está marcado **y** no hay ADA
ni Grupal, correr **solo** el A03 y saltarse el bloque de Actividades. La validación de
obligatorios pasa de "ADA y Grupal siempre" a "ADA y Grupal, salvo que la corrida sea
solo-cuestionarios". Es la única forma de que la fusión no pierda una capacidad.

El bloque de estamentos también se mueve con el A03 (lo necesita el perfil
Administrativo del screening).

---

## 7. Pantalla "Acerca de"

Contenido:

- Versión (`rem_utils.VERSION`) y, si se puede, fecha de build.
- Autor: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC).
- Licencia **GPL-3.0-or-later** + botón "Ver licencia" que abre el `LICENSE` que ya se
  distribuye junto al `.exe`.
- **"Procesa todo localmente. No envía ningún dato a internet."** Redactado para que
  sirva de argumento ante IT del SSMC al pedir whitelist del `.exe` sin firmar
  (Ley 20.584 y 21.719). Es la frase que ya está en CLAUDE.md §11 y hoy no la ve nadie.
- **Ediciones de los catálogos DEIS**, leídas de `catalogos/FUENTES.json` (edición,
  fecha, filas). Es exactamente para lo que se guarda ese archivo: poder decir de qué
  edición hablan los números. Manejar el `FileNotFoundError` — si el `.spec` no
  incluyó `catalogos/`, esta pantalla es donde se nota.
- Crédito de asistencia de IA (ya está en el header de cada archivo).

**Decisión pendiente del autor: qué dato de contacto va.** Un correo en un archivo
versionado de un repo público es una decisión, no un default. Opciones: correo
personal, correo institucional, solo la URL del repo (issues de GitHub), o nada.
**No inventarlo al implementar: preguntar.**

---

## 8. Qué se hace con la GUI antigua

Se congela **comprimida**: `legacy/autorem_gui_tk_1.9.4.py.gz` — el `autorem.py`
completo (GUI + dispatcher + CLI) tal como quedó antes de la migración.

```bash
git show HEAD:autorem.py | gzip -9 > legacy/autorem_gui_tk_1.9.4.py.gz
```

**Por qué comprimido** (idea del autor, y está bien): así ninguna herramienta del repo
lo escanea ni lo tropieza. Verificado contra el código de los tres checkers:

| Herramienta | Selección de archivos | ¿Toca el `.gz`? |
|---|---|---|
| `tools/check_cp1252.py:124` | `rglob("*.py")` | no |
| `tools/check_version.py` | `*.py`, y además `legacy/` ya está en `EXENTOS_DIR` | no |
| `tools/hook_pre_commit_rut.py:52` | salta la lista `BIN`, que incluye `.gz` | no |

**No introduce riesgo de PII.** El §14 advierte que el hook anti-RUT salta binarios y
que por eso los catálogos necesitan `scan_catalogo.py`; acá no aplica: el contenido es
código propio que ya pasó por los hooks y **ya está en git en claro** en todo el
historial. No es un binario de origen externo.

**Nota para dejar en `legacy/`** (`legacy/README.md`, una línea): que el `.gz` está
congelado a propósito, que no se descomprime "para arreglarlo", y que se lee con
`python -c "import gzip,sys;sys.stdout.write(gzip.open('legacy/autorem_gui_tk_1.9.4.py.gz','rt',encoding='utf-8').read())"`.

Confirmar también que `.gitignore` no lo atrapa (hoy ignora `*.xlsx/xls/csv`; un
`.py.gz` no matchea, y `catalogos/*.csv.gz` ya se versionan sin problema).

---

## 9. Versionado

Un rediseño completo de la GUI es **X** por §9 de CLAUDE.md ("cambio grande de
arquitectura"): **2.0.0**.

**Colisión a resolver antes de bumpear:** CLAUDE.md §12 tiene comprometido el
**1.10.0** para cuando cierre la validación de la familia población (P6 + rescate).
Si la GUI 2.0 aterriza primero, ese 1.10.0 deja de existir y la familia población
pasará a ser 2.1.0. **Decidir el orden con el autor**, y si la GUI va primero,
corregir esa línea de §12 en el mismo commit.

Vale el guardarraíl anti-colisión de §9: **el árbitro es el CHANGELOG**. Antes de
bumpear, si el CHANGELOG ya tiene una versión mayor que `rem_utils.VERSION`, otra
sesión avanzó — parar. Usar la skill `versionar` (`tools/check_version.py --bump`),
que arrastra headers, contadores de tests y entrada del CHANGELOG.

---

## 10. Empaquetado (`autoREM.spec`) — riesgo alto, mirar temprano

`customtkinter` trae **temas `.json` y fuentes como DATOS**, no como imports. Es el
mismo problema que ya mordió con `maestro_slim.csv.gz` y con `catalogos/`
(CLAUDE.md §11): PyInstaller no los sigue solo.

- Agregar `--collect-data customtkinter` (o su equivalente en el `.spec`:
  `datas += collect_data_files("customtkinter")`) al **`autoREM.spec` versionado**.
- **Probar el `.exe` temprano, no al final.** Un CTk sin sus temas no falla al importar:
  falla al dibujar, y ya con la migración entera hecha.
- Medir el impacto en tamaño y en tiempo de arranque `--onefile`. Si el arranque se
  degrada mucho, es el argumento que faltaba para evaluar `--onedir`.

---

## 11. Tests

Hoy la GUI **no tiene cobertura**: de los 143 tests, lo único que toca `autorem` es
`tests/test_autorem.py:297`, que llama a `_correr_tareas` (headless). La migración es
un cambio grande sin red — la validación es a ojo.

Lo que sí se puede testear, y hay que agregar: **`tests/test_gui_registro.py`**, del
mismo tipo anti-olvido que `tests/test_cobertura.py`. Descubre por introspección las
páginas de `gui/paginas/` y falla si alguna:

- no expone `PANTALLA`, o le faltan claves obligatorias;
- declara un `programa` que no está en el orden del sidebar;
- tiene `correr` no invocable, o `inputs` con `key` duplicada;
- no tiene entrada en `COBERTURA` (si corresponde a un módulo).

Eso no prueba que la ventana se vea bien, pero sí que el registro esté completo — que
es donde una migración de este tamaño pierde cosas en silencio.

`tests/test_autorem.py` debe seguir pasando **sin cambios**: si el port de
`_correr_tareas` obliga a tocarlo, es señal de que se movió lógica que no debía moverse.

---

## 12. Orden de implementación sugerido

Cada paso deja el árbol funcionando; no hay un estado "la GUI está a medias y no abre".

1. **Verificar la API de CTk 6** contra la versión instalada. Escribir un spike de
   ~40 líneas: ventana + sidebar + un frame que se intercambia. Nada más.
2. **`--collect-data customtkinter` en el `.spec` y compilar el `.exe` con el spike.**
   Antes de escribir la GUI real. Si esto falla, cambia el plan.
3. `gui/widgets.py` + `gui/runner.py`: portar las primitivas y el hilo. Sin lógica nueva.
4. `gui/app.py` + `gui/registro.py`: shell, sidebar, router, construcción desde `PANTALLA`.
5. **Migrar UNA página primero: A23.** Es la más simple (un input múltiple, un mes, una
   salida) y no arrastra ni estamentos ni el A03 ni el selector de perfil. Si la capa
   declarativa no le calza a A23, el diseño está mal y conviene saberlo con una página
   hecha, no con cinco.
6. SM Actividades (ejercita `extras`: checkbox A03 + la relajación de obligatorios de §6).
7. A05 (ejercita `extras`: caja Período) + **sacar el selector de perfil** (§5).
8. Población: P6 + rescate, saliendo de la pestaña BETA a Salud Mental con badge (§4).
9. `inicio.py` + `about.py` (§7).
10. `tests/test_gui_registro.py` (§11).
11. Congelar la GUI vieja (§8) + borrar el código muerto de `autorem.py`.
12. Bump de versión con la skill `versionar` (§9) + actualizar CLAUDE.md §2, §9 y §12.
13. **Validar el `.exe` a ojo**: que abran todas las pantallas, que la hoja LEEME
    aparezca en una salida, y que el Trabajo Perdido **no** diga "heurística" en el log
    (ya está pendiente en §12 de CLAUDE.md).

---

## 13. Fuera de alcance de la 2.0

Anotado para que no se cuele:

- **Pestaña de Consultas de catálogos DEIS** (§14 de CLAUDE.md, el anotador batch). Es
  una pantalla nueva con su propia lógica, no parte de la migración. Va después, y
  entra gratis: es una entrada más en `REGISTRO`.
- **Otras Causas**: popup con lista de RUTs + dropdown (roadmap §12). Mismo criterio.
- Cualquier cambio en la lógica de los módulos. Si durante la migración aparece un bug
  de un módulo, se anota; no se arregla acá (mezclado con un rediseño de GUI, nadie
  puede revisar el diff).
