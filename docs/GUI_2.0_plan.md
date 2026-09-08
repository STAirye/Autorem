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
| Contacto en el About | **Solo URL del repo + licencia. Sin correo** (§7). |
| Formato IRIS/Admin | Detección al elegir el archivo, y **la GUI cambia de color** según el formato (§5). |
| Dónde se desarrolla | Rama `gui-2.0`, **sin bumpear versión en la rama** (§9). |

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

**Diseño (decidido con el autor):**

1. Al **elegir el archivo** —no al procesar— se abre y se corre `sm.detectar_formato(ws)`.
2. El resultado se muestra **en la página** como label vivo:
   `Formato detectado: IRIS` / `Formato detectado: Administrativo`.
3. **La página cambia de color según el formato** (§5.1). Confirmación visual antes de
   apretar Procesar: si el color no es el que esperabas, cargaste otra cosa.
4. Si es **Administrativo**, junto al label va el disclaimer (`_DISCLAIMER_ADMIN`:
   sin demografía) **más un checkbox de acuse** — "Entiendo que las columnas
   demográficas saldrán vacías". Ese formato **degrada datos**, y ahí sí se justifica
   una fricción explícita.
5. Si es `desconocido`, **fail loud**: no se procesa, y el mensaje dice qué se buscó
   (ancla IRIS / banner + markers admin) para que el usuario sepa qué revisar.

### 5.1 El color como canal de estado de la fuente

Dos reglas para que no se degrade a decoración:

- **El color nunca es el único canal.** Va *encima* del label de texto del punto 2, no
  en vez de. Daltonismo, y además un color sin leyenda no se aprende solo. Si el
  usuario tapa el color, la página sigue diciendo qué detectó.
- **El color significa, no solo distingue.** Administrativo es el formato que
  **degrada datos** -> **ámbar**, que ya es el color de aviso del proyecto
  (`#a05a00`). IRIS, que trae todo -> frío/neutro. Así el color dice "cuidado", no
  "opción B". Un esquema tipo rojo/verde arbitrario no serviría para nada.

**Dónde se pinta:** una franja/banner en el borde superior del área de contenido, más
el borde del bloque de inputs. **No** la ventana entera ni el sidebar: el sidebar es
navegación y su color tiene que ser estable, y teñir todo pelea con el tema.

El fondo general queda en el claro/oscuro genérico del tema; el color de estado vive
solo en banner y acentos. Además de verse mejor, es lo **verificable**: tiñendo la
ventana entera habría que comprobar el contraste de cada label, el log, los botones y
los spinbox contra tres fondos distintos; confinado al banner, los pares que deben
estar bien son los seis de §5.2.

**Refinamiento: punto de estado en el sidebar.** Un dot de color chico en el item de
la página deja ver el estado de una pantalla que no estás mirando. Es compatible con
"el sidebar mantiene color estable" (un punto es acento, no tinte) y con la regla 1:
el dot es pista **secundaria**, el dato lo carga el label de la página.

**Widget reutilizable `BannerFuente`.** El mismo problema existe en los módulos pandas:
`formatos.clasificar_fuente` devuelve `plena` / `parcial` / `cambiada` (A23 y SM con el
Monitoreo Admin), que es exactamente el mismo eje "qué tan completa viene la fuente".
Mismo widget, tres estados:

| Estado | Color | Mensaje |
|---|---|---|
| `plena` / IRIS | neutro frío | — |
| `parcial` / Administrativo | ámbar | qué se pierde (le habla al USUARIO) |
| `cambiada` | ámbar fuerte | RAYEN movió el piso (le habla al DEV) |

**Asimetría honesta que hay que respetar:** en A05 la detección es barata (solo mira el
encabezado), así que se puede pintar **al elegir el archivo**. En los módulos pandas la
clasificación ocurre dentro de `cargar_canonico`, o sea **durante** el proceso: ahí el
banner se pinta cuando arranca la corrida, no antes. No se puede prometer preview donde
no lo hay.

**Costo práctico:** abrir el `.xlsx` al seleccionarlo **congela la ventana** si el
export es grande. Va con `load_workbook(read_only=True)` y **en un hilo**, con el label
en "detectando..." mientras tanto. Barato, pero no gratis: no llamarlo directo en el
callback del `Examinar...`.

### 5.2 Paleta (medida, no elegida a ojo)

**Esquema tipo semáforo** (decisión del autor): verde-azulado = IRIS/plena, ámbar =
Administrativo/parcial, rojo = no reconocido. La metáfora se entiende sola en un
contexto clínico y no hay que enseñarla.

**Por qué IRIS es verde-AZULADO y no verde puro:** verde contra rojo es justamente el
par que se cae en deuteranopia (~8% de los hombres). Correr el verde hacia el eje azul
lo separa del rojo para cualquier tipo de daltonismo, sin perder la lectura de "OK".
No es crítico —la regla 1 de §5.1 ya obliga al label de texto, así que el color nunca
carga el dato solo— pero sale gratis.

**El texto NO se deriva del fondo en runtime.** Se fija un par (fondo, texto) por
estado y por modo. Estos ya están medidos en **contraste WCAG** (1:1 = invisible,
21:1 = negro sobre blanco; el mínimo AA para texto normal es **4.5:1**):

| Estado | Modo | Fondo | Texto | Contraste |
|---|---|---|---|---|
| IRIS / `plena` | claro | `#E4F2EF` | `#0F4F45` | 8.20:1 |
| IRIS / `plena` | oscuro | `#12312C` | `#8FD8C9` | 8.55:1 |
| Admin / `parcial` | claro | `#FCF0DA` | `#A05A00` | **4.70:1** |
| Admin / `parcial` | oscuro | `#33280F` | `#F0C070` | 8.60:1 |
| No reconocido | claro | `#FBE6E4` | `#8C1D18` | 7.61:1 |
| No reconocido | oscuro | `#3A1A18` | `#F2B8B4` | 9.17:1 |

**Ojo con Admin claro: 4.70:1 es el único par ajustado**, apenas sobre el mínimo. Está
así a propósito porque reusa el `#A05A00` que ya es el color de aviso del proyecto
(continuidad con el Tk actual). **No aclarar ese texto ni oscurecer ese fondo** sin
recalcular; los demás tienen holgura de sobra (todos sobre AAA = 7:1).

Recalcular con esta fórmula si se tocan (WCAG 2.x, luminancia relativa):

```python
def lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
def L(h):
    h = h.lstrip("#"); r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
def ratio(a, b):
    l1, l2 = sorted((L(a), L(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)
```

**Con esta tabla, el modo oscuro deja de ser un riesgo abierto** (§4): los colores
sueltos que arrastra el Tk actual (`#888`, `#666`, `#c8801a`, `#5a3200`) se reemplazan
por tokens de `widgets.py` con par claro/oscuro, en vez de quedar hardcodeados en cada
página. `cambiada` (el estado dev-facing de `clasificar_fuente`) reusa el par ámbar; no
necesita color propio.

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

**Contacto: SOLO la URL del repo. Sin correo** (decidido, sep-2026). Un correo en un
archivo versionado de un repo público es exposición innecesaria; los issues de GitHub
cumplen la misma función y no publican una dirección. **No agregar un correo al
implementar, aunque parezca que falta.**

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

**Colisión con el 1.10.0:** CLAUDE.md §12 tiene comprometido el 1.10.0 para cuando
cierre la validación de la familia población (P6 + rescate). Los dos trabajos avanzan
en paralelo y ninguno debe esperar al otro.

**Solución: rama `gui-2.0`, y NO se bumpea versión dentro de la rama.**

- `rem_utils.VERSION` se queda en **1.9.4** durante todo el desarrollo de la rama.
- Los `gui/*.py` nuevos nacen con header **1.9.4**, que es la versión actual — así el
  pre-commit (`check_version.py`) queda contento en cada commit de la rama, sin
  inventar una versión que todavía no existe.
- El bump a **2.0.0** se hace en **UN solo commit al mergear**, con la skill
  `versionar` (`tools/check_version.py --bump 2.0.0`), que arrastra headers,
  contadores de tests y la entrada del CHANGELOG de un viaje.

Con esto el **guardarraíl anti-colisión del §9 nunca tiene que arbitrar**: la rama no
toca el CHANGELOG, así que población puede cerrar en `main` y llevarse el 1.10.0
tranquila; la rama mergea después y se lleva el 2.0.0. Si el orden se da al revés,
también funciona: el número se decide recién en el commit de merge.

**Superficie de conflicto: baja.** La GUI 2.0 casi solo **crea** archivos bajo `gui/`
y **borra** de `autorem.py`; el trabajo de población vive en `modulos/` y `programas/`.
El punto de roce real es `autorem.py` si población necesitara tocar la pestaña BETA
mientras tanto — si eso pasa, se hace en la rama, no en `main`.

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

0. **Crear la rama `gui-2.0`** y no tocar `rem_utils.VERSION` hasta el merge (§9).
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
7. A05 (ejercita `extras`: caja Período) + **sacar el selector de perfil** y estrenar
   el `BannerFuente` con cambio de color (§5, §5.1). Al quedar hecho, engancharlo
   también en A23/SM contra `formatos.clasificar_fuente`.
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
