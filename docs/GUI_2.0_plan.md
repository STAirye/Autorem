<!--
This document was generated with the assistance of Claude Opus 5 (Anthropic).
The human author reviewed, modified, and integrated the content.

Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
Copyright (C) 2026 Simón Tobar
SPDX-License-Identifier: GPL-3.0-or-later
Version: 1.9.10 (plan; la implementación bumpea, ver §9)
-->

# Plan — GUI 2.0 (customtkinter)

Documento **autocontenido**: escrito para una sesión fría que solo lee este archivo
y `CLAUDE.md`. Escrito el 8-sep-2026 sobre `autorem.py` v1.9.4 (1274 líneas);
**actualizado el 15-sep-2026 sobre v1.9.10 (1575 líneas, 170 tests)** — ver §0.1.

---

## 0. Decisiones ya tomadas (con el autor, sep-2026)

| Pregunta | Decisión |
|---|---|
| Profundidad | **Rediseño completo**: sidebar de navegación en vez de `ttk.Notebook`, tema, pantalla de inicio. |
| Alcance funcional | Entra **todo** el roadmap de GUI 2.0: About/contacto/licencia · agrupar por Programa de salud · sacar la pestaña A03 standalone · sacar el selector IRIS/Administrativo. |
| GUI antigua | **Congelada y comprimida** en `legacy/autorem_gui_tk_<VERSION>.py.gz`, con la versión del momento de congelar (§8). |
| Base | `customtkinter` — **6.0.0 ya instalado** en la máquina del autor. |
| Contacto en el About | **Solo URL del repo + licencia. Sin correo** (§7). |
| Formato IRIS/Admin | Detección al elegir el archivo, y **la GUI cambia de color** según el formato (§5). |
| Dónde se desarrolla | Rama `gui-2.0` **en un worktree aparte**, sin bumpear versión en la rama, y **sin tocar `autorem.py` hasta el final** (§9). |

### 0.1 Qué cambió en `main` entre el 8 y el 15 de septiembre

`main` avanzó seis versiones (1.9.4 -> 1.9.10) mientras este plan esperaba. Lo que
toca a la GUI:

| Cambio | Versión | Impacto en este plan |
|---|---|---|
| **Dotación** (`programas/dotacion.py`): cuadro + 2 botones en la pestaña SM y **3 diálogos Tk** (`_dotacion_ada`, `_bloque_dotacion`, `_grupo_dotacion`, `_dialogo_dotacion`, `_revisar_dotacion`) — **+275 líneas** en `autorem.py` | 1.9.8 / 1.9.9 | **Rompe dos supuestos del plan**: el flujo lineal ctx -> worker (§3.3) y la "superficie de conflicto baja" de la rama (§9) |
| **Archivos cruzados** ADA/Grupal: `formatos.parece_reporte` / `verificar_cruce` -> `ArchivoInvalido("cruzados")`, y `_manejar_error` le da su propio título | 1.9.10 | Entra al port de `_manejar_error` (§2) y es un estado natural del `BannerFuente` (§5.1) |
| **Mes vacío fail-loud**: `rem_utils.filtrar_mes` -> `ArchivoInvalido("mes_vacio")` en todos los módulos pandas | 1.9.5 | Ninguno: ya lo despacha `_manejar_error`. Confirma que el port de esa función es crítico |
| **Hooks relativos a `$REPO`** (`tools/hooks_git.py`) + CLAUDE.md §10.1 (worktrees) | 1.9.6 | **Habilita** desarrollar la rama en un worktree con los hooks funcionando (§9) |
| Tests 143 -> 170 | — | `tests/test_autorem.py:297` sigue siendo lo único que toca `autorem` (verificado) |

**Lección para el resto de la vida de la rama:** `main` no se va a quedar quieto. La
validación de la dotación está en pausa esperando una lista de Estadística, y cuando
llegue **cambia el diálogo** (pre-marcar ticks y ordenar sospechosos primero, plan de
dotación §2.4). El §9 está reescrito para que eso no sea un problema.

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
  dialogos.py           modales compartidos: estamentos + dotación (§2)
  runner.py             correr_con_reloj (hilo + queue + poll), portado tal cual
  paginas/
    a05.py  a03.py  a23.py  sm.py  poblacion.py  about.py  inicio.py
legacy/
  autorem_gui_tk_<VERSION>.py.gz    congelado, comprimido (§8)
```

**Qué se porta sin tocar la lógica:** `_correr_con_reloj`, `_Reloj`, `_manejar_error`
(**incluida la rama `cruzados`** de 1.9.10, que le da título propio),
`_es_error_formato`, `_valida_ruta`, `_valida_carpeta`, `_dir_salida_default`,
`_slim_por_defecto`, `_abrir_carpeta`, `_bloque_estamentos`, `_resolver_estamentos`,
y **toda la familia de dotación**: `_dotacion_ada`, `_bloque_dotacion`,
`_grupo_dotacion`, `_dialogo_dotacion`, `_revisar_dotacion`. Son correctos y están
validados; solo cambian de módulo y de widget base. **No aprovechar la migración para
reescribirlos.**

Van a `gui/dialogos.py` (estamentos + dotación): son modales reutilizables por más de
una página, no pertenecen a ninguna.

**Invariantes de dotación que el port NO puede perder** (cada una costó un bug o una
decisión explícita, ver `docs/dotacion_externos_plan.md`):

- El tick arranca en la clase **ya guardada**, no en `False`. Con un default fijo, un
  "Aplicar" sobre gente ya clasificada le borraba la marca de externo en silencio
  (fix de 1.9.9).
- "Omitir estamento" es **inmediato** (persiste al click) y **saca a esos nombres de
  `checks`**: si quedaran, "Aplicar" los marcaría `interno`, y un omitido debe seguir
  `desconocido`.
- "Cancelar" no clasifica a nadie; la corrida sigue igual.
- El diálogo recibe `modulo` porque las omisiones se indexan por módulo.

**Reemplazos de widget que salen gratis:** los dos Canvas+Scrollbar armados a mano
(`_tab_scroll` y el de `_dialogo_dotacion`) pasan a `CTkScrollableFrame`, que además
arregla el *known issue* documentado en `_tab_scroll` (el scrollregion que no se
encoge). El `ttk.Notebook` interno de `_revisar_dotacion` pasa a `CTkTabview`.

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
    "extras": [],                        # bloques propios, ver §3.1
    "preparar": None,                    # opcional, HILO GUI, antes del worker (§3.3)
    "correr": correr,                    # callable(ctx, log) -> resultado  (worker)
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
- **SM Actividades:** `_bloque_dotacion` (cuadro + "Precargar dotación..." + "Revisar
  dotación...").
- **Población:** corre DOS módulos (P6 + rescate) con try independiente cada uno.

La dotación obligó a ampliar la firma original (`extras(frame) -> getter`), por dos
motivos concretos:

1. **Necesita leer OTROS inputs de la página.** "Precargar dotación..." usa el ADA
   elegido y el mes del spinbox. Hoy se resuelve pasándole `get_ada` y `get_mes` a
   mano.
2. **Necesita una posición, no "al final".** El cuadro va **debajo del ADA** porque
   sin ADA no tiene nada que mostrar. Hoy se logra con un `holder_dot` vacío que
   reserva el lugar en el orden de `pack` y se rellena más abajo — un hack que la capa
   declarativa debe volver innecesario.

Firma nueva:

```python
"extras": [
    {"despues_de": "grupal",               # key de un input, o None = al final
     "construir": bloque_dotacion},        # callable(frame, pagina) -> getter | None
],
```

`pagina` expone lo que un bloque puede necesitar de su página: `pagina.get(key)` (ruta
o lista de rutas de un input), `pagina.mes()` (`(y, m)` o `None`), `pagina.log` y
`pagina.root`. El getter que devuelve `construir` lo llama `app.py` en el hilo de la
GUI, y su valor entra a `ctx`.

### 3.2 Invariante dura: nada de Tk vars en el worker

`app.py` resuelve **todos** los `StringVar`/`BooleanVar` a un dict plano `ctx`
**antes** de lanzar el hilo. `correr(ctx, log)` no toca widgets ni variables Tk.

Esto ya es un problema conocido: `_tab_sm` lo maneja a mano y lo dice en un
comentario ("Tk vars no son thread-safe -> resolver en el hilo GUI y pasar los
valores capturados al worker"). En la 2.0 deja de ser una precaución que hay que
recordar en cada pantalla y pasa a ser una regla del constructor.

`ctx` contiene: rutas ya validadas (`Path`), `mes=(y, m)`, `carpeta` (Path), y lo que
devolvieron los `extras`.

### 3.3 Fase `preparar`: trabajo que TIENE que ser del hilo GUI (dotación)

La primera versión del plan suponía un flujo lineal: resolver `ctx` en el hilo GUI ->
`correr(ctx, log)` en el worker. **La dotación lo rompe.** Su diálogo es Tk, así que
tiene que abrirse en el hilo GUI; pero necesita el ADA **ya cargado y filtrado al mes**
para tener evidencia que mostrar; y el worker necesita el resultado del diálogo.

Cómo lo resuelve hoy `_tab_sm.on_procesar`: carga el ADA **en el hilo GUI**, abre el
diálogo, y le pasa `d` (el ADA ya leído) y `tabla_dot` al worker para no releerlo. El
propio código lo admite: *"Esto BLOQUEA la GUI y no hay como evitarlo"* — y pone
cursor de espera + un log previo para que no parezca colgada.

**En la 2.0 esa fase se vuelve explícita:**

```python
"preparar": preparar,   # callable(ctx, pagina) -> ctx ampliado | None (= abortar)
```

- Corre en el **hilo GUI**, después de validar inputs y **antes** del worker.
- Devuelve `ctx` con lo que agregó (`ctx["d"]`, `ctx["tabla_dot"]`), o `None` para
  abortar la corrida (ADA ilegible, mes vacío: `_dotacion_ada` ya devuelve
  `(None, None)` en esos casos y muestra el error).
- **Primero se porta tal cual, con el bloqueo incluido.** Es comportamiento validado.

**Mejora posible, DESPUÉS de migrar y en un commit aparte:** el bloqueo se puede
eliminar con una corrida en dos tiempos — el worker carga y filtra el ADA, le pasa la
evidencia al hilo GUI (`root.after` + una `queue`), el diálogo se abre ahí, y el
worker espera la respuesta (`threading.Event`) antes de seguir. El reloj de arena gira
durante la carga y la ventana no se congela. **No hacerlo durante la migración:**
mezclar el cambio de toolkit con un cambio de concurrencia deja un bug imposible de
atribuir a uno u otro.

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
| **cruzado** (1.9.10) | rojo | "este archivo parece el reporte de X" |

**Archivos cruzados: el único estado pandas que SÍ tiene preview barato.** Desde
1.9.10, `formatos.parece_reporte(hdr)` dice si un header crudo parece ADA, Grupal o
"no me consta" — es una función **pura**, que solo cuenta firmas en el encabezado.
Hoy se usa recién al procesar (`verificar_cruce` -> `ArchivoInvalido("cruzados")`).
En la 2.0 se puede correr **al elegir el archivo** en los slots ADA y Grupal y pintar
el banner rojo antes de Procesar. Dos reglas que ya trae la función y hay que
respetar:

- **Empate = `None` = no se acusa.** El banner rojo sale solo si el header es
  *claramente* del otro reporte; "no me consta" no pinta nada.
- **El error al procesar se queda.** El banner es aviso anticipado, no reemplazo: si
  el usuario ignora el rojo y aprieta Procesar, `verificar_cruce` sigue fallando duro.

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

**Desde 1.9.8 hay que saltarse también la dotación.** `preparar` (§3.3) llama a
`_dotacion_ada`, que carga el ADA: en una corrida solo-cuestionarios no hay ADA y
fallaría. Una corrida solo-cuestionarios no pasa por `preparar`.

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
  incluyó `catalogos/`, esta pantalla es donde se nota. Detalle en §7.1.
- Crédito de asistencia de IA (ya está en el header de cada archivo).

**Contacto: SOLO la URL del repo. Sin correo** (decidido, sep-2026). Un correo en un
archivo versionado de un repo público es exposición innecesaria; los issues de GitHub
cumplen la misma función y no publican una dirección. **No agregar un correo al
implementar, aunque parezca que falta.**

### 7.1 Catálogos: fecha visible + actualización manual (agregado sep-2026, pedido del autor)

**a) LASTUPDATE a la vista.** Por cada catálogo (`cie10` · `eno` · `ges`), mostrar la
edición y la fecha de `FUENTES.json`. Si hay un drop-in que pisa al embebido
(cascada de `catalogos.cargar`), mostrar **cuál se está usando**. Ese aviso hoy solo
sale en el log, y cambiar la fuente cambia los resultados.

**b) Actualizar a mano, detrás de un «modo usuario avanzado».** El `.exe` es offline
por diseño, así que no hay «buscar actualizaciones»: el usuario baja el `.xlsx` del
DEIS por su cuenta y lo carga.
- **Confirmación explícita antes de habilitarlo:** «Esto cambia los resultados de
  todos los reportes que usan catálogos. Solo si sabes qué edición estás cargando».
- **Escaneo de PII obligatorio** antes de aceptar el archivo, con la misma lógica que
  `tools/scan_catalogo.py`. Con hallazgos, se rechaza igual que `--slim`.
- **Hay que decidir dónde queda el archivo.** Dentro del `.exe` la carpeta
  `catalogos/` vive en el temporal de `_MEIPASS` y se borra al cerrar, así que el
  drop-in tiene que ir a un directorio del usuario (candidato: `~/.autorem/catalogos/`,
  junto al caché de estamentos y dotación). Eso obliga a extender la cascada de
  `catalogos.cargar` con esa ruta. **Es un cambio de lógica de `programas/`: se hace en
  `main`, no en la rama** (§13), y la GUI solo lo consume.
- Botón «Volver al catálogo embebido», que borra el drop-in.

---

## 8. Qué se hace con la GUI antigua

Se congela **comprimida**: `legacy/autorem_gui_tk_<VERSION>.py.gz` — el `autorem.py`
completo (GUI + dispatcher + CLI) tal como quedó antes de la migración.

**El número se decide al congelar, no hoy.** La primera versión de este plan decía
`1.9.4` y `main` ya va en 1.9.10: congelar la GUI de la fecha en que se escribió el
plan habría archivado una versión sin dotación. Se congela el `autorem.py` de `main`
**en el momento del paso 11** (§12), con la `VERSION` de ese momento:

```bash
V=$(python -c "from programas.rem_utils import VERSION; print(VERSION)")
git show main:autorem.py | gzip -9 > "legacy/autorem_gui_tk_$V.py.gz"
```

**Por qué comprimido** (idea del autor, y está bien): así ninguna herramienta del repo
lo escanea ni lo tropieza. Verificado contra el código de los tres checkers:

| Herramienta | Selección de archivos | ¿Toca el `.gz`? |
|---|---|---|
| `tools/check_cp1252.py:129` | `rglob("*.py")` | no |
| `tools/check_version.py:71` | `*.py`, y además `legacy/` ya está en `EXENTOS_DIR` | no |
| `tools/hook_pre_commit_rut.py:52` | salta la lista `BIN`, que incluye `.gz` | no |

(Líneas re-verificadas el 15-sep sobre 1.9.10.)

**No introduce riesgo de PII.** El §14 advierte que el hook anti-RUT salta binarios y
que por eso los catálogos necesitan `scan_catalogo.py`; acá no aplica: el contenido es
código propio que ya pasó por los hooks y **ya está en git en claro** en todo el
historial. No es un binario de origen externo.

**Nota para dejar en `legacy/`** (`legacy/README.md`, una línea): que el `.gz` está
congelado a propósito, que no se descomprime "para arreglarlo", y que se lee con
`python -c "import gzip,sys;sys.stdout.write(gzip.open(sys.argv[1],'rt',encoding='utf-8').read())" legacy/autorem_gui_tk_<VERSION>.py.gz`.

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

- La rama **no toca `rem_utils.VERSION` ni el CHANGELOG**. Hereda la versión de `main`
  cada vez que se le mergea `main` (ver abajo).
- Los `gui/*.py` nuevos declaran en su header la `VERSION` vigente **en la rama** al
  momento del commit — así el pre-commit (`check_version.py`) queda contento sin
  inventar una versión que todavía no existe. Cuando un merge de `main` sube la
  versión, el siguiente commit que toque esos archivos va a pedir el header nuevo:
  `python tools/check_version.py --arreglar` lo sincroniza.
- El bump a **2.0.0** se hace en **UN solo commit al mergear a `main`**, con la skill
  `versionar` (`tools/check_version.py --bump 2.0.0`), que arrastra headers,
  contadores de tests y la entrada del CHANGELOG de un viaje.

Con esto el **guardarraíl anti-colisión del §9 nunca tiene que arbitrar**: la rama no
toca el CHANGELOG, así que población puede cerrar en `main` y llevarse el 1.10.0
tranquila; la rama mergea después y se lleva el 2.0.0. Si el orden se da al revés,
también funciona: el número se decide recién en el commit de merge.

### 9.1 Branchear seguro: tres reglas

La primera versión decía *"superficie de conflicto: baja"*. **Era falso, y lo probó la
semana siguiente:** la dotación metió +321 líneas en `autorem.py` en `main`, justo el
archivo que la rama iba a vaciar. `main` va a seguir cambiando la GUI (la dotación
tiene pendiente la lista de Estadística, que cambia el diálogo). Estas tres reglas
hacen que eso no importe.

**Regla 1 — La rama vive en un worktree aparte, no en la carpeta de siempre.**

```bash
git worktree add -b gui-2.0 "../AutoREM-gui2"
```

Crea la carpeta hermana `Dr tobar/AutoREM-gui2/`, con la rama `gui-2.0` ya
checkouteada. La sesión de implementación se abre **en esa carpeta**; la carpeta
`AutoREM/` de siempre se queda en `main`.

Por qué worktree y no `git switch -c`: con `switch`, cambiar de rama **cambia los
archivos en disco** de la única carpeta que tienes, y el riesgo concreto es commitear
trabajo de población en `gui-2.0` sin darte cuenta. Con dos carpetas no hay a qué
cambiarse: cada carpeta es una rama, siempre.

- **Hermana, no dentro del repo:** los worktrees de Claude Code viven en
  `.claude/worktrees/`, dentro del repo. Para uno de larga vida, afuera es más limpio.
  (El rglob de `check_cp1252` ya los excluye igual, fix de sep-2026.)
- **Los hooks funcionan ahí** desde 1.9.6 (rutas relativas a `$REPO`, CLAUDE.md §10.1).
- **Lo que se comparte entre las dos carpetas** (CLAUDE.md §10.1): commits, ramas y
  **el stash**. No uses `git stash` mientras vivan las dos; usa commits WIP.
- Para cerrarlo al final, el procedimiento de Windows está en CLAUDE.md §10.1 ("Cerrar
  un worktree en Windows").

**Regla 2 — La rama no toca `autorem.py` hasta el paso 11. Solo AGREGA.**

Todo el desarrollo vive en `gui/`, que no existe en `main`. La GUI nueva se lanza
**sin pasar por `autorem.py`**:

```bash
python -m gui.app
```

(funciona porque `python -m` desde la raíz del repo pone la raíz en `sys.path`, que es
lo que necesitan los imports absolutos `from programas...`). Mientras tanto la GUI
vieja sigue intacta y funcionando en la misma rama.

Consecuencia: **mergear `main` a la rama no tiene conflictos**, por más que `main`
toque `autorem.py`. Los dos lados cambian archivos disjuntos. El único momento de
conflicto posible es el paso 11, y ahí se hace a propósito, una vez.

**Regla 3 — `main` se mergea a la rama seguido; la rama a `main`, una sola vez.**

Desde el worktree de la rama:

```bash
git merge main
```

Cada vez que `main` avance, y **obligatorio cada vez que `main` toque la GUI**. Nunca
al revés hasta que la 2.0 esté terminada.

Y cada cambio de GUI que entre a `main` mientras vive la rama se **anota en la tabla de
abajo**: es trabajo que la GUI 2.0 tiene que portar. Sin la tabla, un botón agregado en
`main` en octubre desaparece en silencio al borrar la GUI vieja en el paso 11.

| Cambio de GUI en `main` | Versión | Portado a la rama |
|---|---|---|
| Dotación: cuadro, 2 botones, 3 diálogos (§2, §3.3) | 1.9.8 / 1.9.9 | pendiente |
| `_manejar_error`: título propio para `cruzados` | 1.9.10 | pendiente |
| *(anotar aquí lo que venga)* | | |

**Antes del paso 11**, esta tabla tiene que estar entera en "sí". Es la condición para
borrar la GUI vieja.

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

Hoy la GUI **no tiene cobertura**: de los 170 tests (re-verificado el 15-sep), lo único que toca `autorem` es
`tests/test_autorem.py:297`, que llama a `_correr_tareas` (headless). La migración es
un cambio grande sin red — la validación es a ojo.

Lo que sí se puede testear, y hay que agregar: **`tests/test_gui_registro.py`**, del
mismo tipo anti-olvido que `tests/test_cobertura.py`. Descubre por introspección las
páginas de `gui/paginas/` y falla si alguna:

- no expone `PANTALLA`, o le faltan claves obligatorias;
- declara un `programa` que no está en el orden del sidebar;
- tiene `correr` no invocable, o `inputs` con `key` duplicada;
- tiene un `extras[].despues_de` que no es la `key` de ningún input de la página
  (el bloque se pintaría en cualquier parte, o no se pintaría);
- tiene `preparar` declarado y no invocable;
- no tiene entrada en `COBERTURA` (si corresponde a un módulo).

**Los invariantes de dotación del §2 SÍ se pueden testear sin ventana**, si el port
separa el "qué valor arranca en cada tick" del widget: una función pura
`valores_iniciales(filas, tabla) -> {nombre: bool}` es testeable, y es justo la que
tuvo el bug de 1.9.9. Vale la pena extraerla — es de las pocas lógicas de GUI que ya
falló una vez.

Eso no prueba que la ventana se vea bien, pero sí que el registro esté completo — que
es donde una migración de este tamaño pierde cosas en silencio.

`tests/test_autorem.py` debe seguir pasando **sin cambios**: si el port de
`_correr_tareas` obliga a tocarlo, es señal de que se movió lógica que no debía moverse.

---

## 12. Orden de implementación sugerido

Cada paso deja el árbol funcionando; no hay un estado "la GUI está a medias y no abre".

0. **Crear el worktree con la rama** (§9.1, regla 1) y abrir la sesión de
   implementación en esa carpeta. No tocar `rem_utils.VERSION` hasta el merge (§9).
1. **Verificar la API de CTk 6** contra la versión instalada. Escribir un spike de
   ~40 líneas: ventana + sidebar + un frame que se intercambia. Nada más.
2. **`--collect-data customtkinter` en el `.spec` y compilar el `.exe` con el spike.**
   Antes de escribir la GUI real. Si esto falla, cambia el plan.
3. `gui/widgets.py` + `gui/runner.py`: portar las primitivas y el hilo. Sin lógica nueva.
4. `gui/app.py` + `gui/registro.py`: shell, sidebar, router, construcción desde
   `PANTALLA`, incluidos `extras` con `despues_de` y la fase `preparar` (§3.1, §3.3).
   Se lanza con `python -m gui.app` — **`autorem.py` no se toca** (§9.1, regla 2).
5. **Migrar UNA página primero: A23.** Sigue siendo la más simple (un input múltiple,
   un mes, una salida) y no arrastra ni estamentos, ni el A03, ni el selector de
   perfil, ni dotación. Si la capa declarativa no le calza a A23, el diseño está mal y
   conviene saberlo con una página hecha, no con cinco.
6. `gui/dialogos.py`: portar estamentos y **la familia de dotación** tal cual, con sus
   invariantes (§2). Extraer `valores_iniciales` y testearla (§11).
7. **SM Actividades — ahora la página más pesada.** Ejercita todo a la vez: `extras`
   con posición (dotación debajo del ADA), `preparar` (§3.3), el checkbox A03, la
   relajación de obligatorios con el salto de dotación (§6), y el Trabajo Perdido en
   el mismo worker. Si algo del diseño no aguanta, aparece acá.
8. A05 (ejercita `extras`: caja Período) + **sacar el selector de perfil** y estrenar
   el `BannerFuente` con cambio de color (§5, §5.1). Al quedar hecho, engancharlo
   también en A23/SM contra `formatos.clasificar_fuente` y el preview de cruce
   (`formatos.parece_reporte`) en los slots ADA/Grupal.
9. Población: P6 + rescate, saliendo de la pestaña BETA a Salud Mental con badge (§4).
10. `inicio.py` + `about.py` (§7) + `tests/test_gui_registro.py` (§11).
11. **Recién acá se toca `autorem.py`.** `git merge main` una última vez, verificar que
    la tabla de port del §9.1 esté entera en "sí", congelar la GUI vieja con la
    versión de ese momento (§8), borrar la GUI de `autorem.py` y hacer que `main()`
    lance `gui.app`.
12. Mergear la rama a `main` + bump a 2.0.0 con la skill `versionar` (§9) + actualizar
    CLAUDE.md §2, §9 y §12. Cerrar el worktree (CLAUDE.md §10.1).
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
- **La corrida en dos tiempos para la dotación** (§3.3): elimina el congelamiento, pero
  es un cambio de concurrencia. Va en un commit aparte **después** de la migración.
- **Cambios del diálogo de dotación cuando llegue la lista de Estadística**
  (`docs/dotacion_externos_plan.md` §2.4) y su **fase 2** (bloques apilados,
  §4.4 de ese plan): si llegan mientras vive la rama, se hacen en `main` y se anotan
  en la tabla de port del §9.1. No se adelantan en la rama.
- **Auditoría de filtros contra el Maestro** (`docs/auditoria_filtros_plan.md`): es
  lógica de módulos, no GUI.
- Cualquier cambio en la lógica de los módulos. Si durante la migración aparece un bug
  de un módulo, se anota; no se arregla acá (mezclado con un rediseño de GUI, nadie
  puede revisar el diff).
