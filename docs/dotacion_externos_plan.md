<!--
This document was generated with the assistance of Claude Opus 5 (Anthropic).
The human author reviewed, modified, and integrated the content.

Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
Copyright (C) 2026 Simon Tobar
SPDX-License-Identifier: GPL-3.0-or-later
Version: 1.9.8
-->

# Plan — `programas/dotacion.py`: separar atenciones de funcionarios EXTERNOS

> **Estado: IMPLEMENTADO — fase 1** (v1.9.8, sep-2026). Capa compartida
> `programas/dotacion.py` + wiring en `modulos/rem_sm_actividades.py` + diálogo
> en `autorem.py`. Pendiente: validar contra la lista real de la sala AIDIA (o
> lo que responda Estadística SSMC, §0.1/§2.4) y la fase 2 (§4.4: bloques
> apilados REM/externos dentro de cada hoja de sección — hoy alcanza con
> `Externos_Delta` para comparar contra el conteo manual). Documento
> **autocontenido**: se puede seguir trabajando sin haber participado de la
> conversación que lo originó.

---

## 0. Problema

El ADA (`ATENCIONES DIAGNOSTICOS ACTIVIDADES`) del CESFAM incluye atenciones
hechas **a nuestros usuarios pero por funcionarios que no son de nuestra
dotación** — hoy concretamente la gente de la **sala AIDIA**, que trabaja en
nuestro establecimiento y registra en nuestro RAYEN.

Esas atenciones **no deben tributar a nuestro REM** (las reporta el dispositivo
que corresponda; contarlas es doble conteo). Hoy autoREM las cuenta todas, en
silencio.

### 0.1 Lo que YA se descartó (no volver a intentarlo)

Verificado contra exports reales, sep-2026:

| Camino | Por qué no sirve |
|---|---|
| Columna `ESTABLECIMIENTO DE DIAGNOSTICO` (ADA IRIS) | dice `FERRADA` en el **100%** de las filas |
| Columna `CENTRO INSCRIPCION DE PACIENTE` | tiene varios valores, pero es el lado **paciente**; no correlaciona con la sala |
| Reporte de dotación / perfiles de RAYEN o IRIS | **no existe**: se revisaron todos los reportes disponibles, ninguno distingue interno de externo |
| Filtrar por nombre de agenda / actividad / formulario | la misma actividad y el mismo formulario los usan internos y externos -> borraría trabajo legítimo en silencio |

Conclusión: **no hay fuente autoritativa**. La tabla se construye desde las
decisiones del propio usuario, y el ADA es el único punto de entrada.

> Solicitud pendiente a Estadística SSMC (sep-2026): la lista de funcionarios de
> la sala, y/o las actividades que la distinguen. **El diseño de abajo funciona
> sin ellas**, y cuando lleguen cualquiera de las dos enchufa sin rehacer nada
> (§2.4). No bloquear la implementación esperándolas.

---

## 1. Decisiones de diseño (NO deshacer sin motivo)

### 1.1 El eje es el FUNCIONARIO, no la actividad

"Externo" es una propiedad **de la persona**. Agenda, actividad y formulario son
proxies correlacionados que driftean. Se usan, pero como **evidencia para
decidir** (§2.3), nunca como filtro.

### 1.2 Tri-estado, no whitelist ni blacklist

Las dos listas simples fallan igual de callado:

| | falla cuando | consecuencia |
|---|---|---|
| Blacklist (lista de externos) | llega un externo nuevo | se cuenta callado -> REM **inflado** |
| Whitelist (lista de dotación) | llega un interno nuevo | se descarta callado -> REM **subcontado** |

Por eso el estado es **`interno` / `externo` / `desconocido`**, y el
`desconocido` es el guardarraíl: nunca se resuelve solo, se pregunta.

### 1.3 `desconocido` cuenta en el REM, pero se reporta

**Regla: `en_rem = (clase != "externo")`.**

Razonamiento asimétrico: el usuario conoce a su equipo, así que un nombre nuevo
es una decisión de 10 segundos que se toma **una vez**; en cambio la alternativa
(descartar todo lo no clasificado) sangra producción propia de forma difícil de
notar. El fail-loud **no** está en la dirección del default: está en que el
número siempre sale acompañado de *"N atenciones de M funcionarios sin
clasificar"* en el log y en la hoja LEEME, con los nombres.

### 1.4 Marcar, no borrar

Las filas externas **no se eliminan** del detalle. Se marcan y se excluyen sólo
de la tabla REM. Mismo patrón que `Posibles_Fallecidos` en
`rem_sm_rescate_inasistentes` (v1.9.1): si borrás la fila, el día que el filtro
se equivoque no hay forma de verlo. Coherente con la regla del proyecto de dejar
siempre la tabla intermedia auditable.

### 1.5 Dos columnas en el detalle, no una

Hay **tres** motivos por los que una fila no está en la tabla REM:

1. no tributa a ninguna casilla SM
2. tributa, pero el funcionario es **externo**
3. tributa, pero el funcionario está **sin clasificar**

Una sola columna derivada los conflaciona. Van las dos:

- **`externo`** — crudo, tri-estado: `interno` / `externo` / `desconocido`
- **`tabula_en`** — derivada, cómoda para filtrar en Excel: `AMBAS` /
  `SOLO_TOTAL` / `NINGUNA`

### 1.6 Capa transversal desde el arranque

`programas/dotacion.py`, junto a `estamentos.py`. **No sabe nada de Salud
Mental.** Hoy sólo lo consume `rem_sm_actividades`, pero el A23 (salas IRA/ERA)
y los módulos de otros programas tienen el mismo problema. El objetivo de fondo
del proyecto es tabular todos los programas de forma **rutificada, trazable,
auditable y reportable** — a diferencia de RAYEN, que entrega una tabla cerrada
sin rutificación. Esta capa es parte de eso.

---

## 2. `programas/dotacion.py`

Gemelo estructural de `programas/estamentos.py`. **Leerlo antes de escribir
código**: la persistencia, el merge, el failsafe y el manejo de caché corrupto ya
están resueltos ahí y se copian tal cual.

### 2.1 Persistencia

```python
RUTA_CACHE = Path.home() / ".autorem" / "dotacion.json"
{
  "funcionarios": {"<nombre_normalizado>": "interno" | "externo"},
  "omitidos":     {"<modulo>": ["<estamento_norm>", ...]}
}
```

La clave de `funcionarios` es `rem_utils.norm(nombre)`. Nombres de funcionario
**no son PII de paciente** -> cachearlos es aceptable (mismo criterio ya
documentado en `estamentos.py`). El archivo vive en el HOME, **nunca en el repo
ni junto al `.exe`**.

`cargar()` / `guardar()`: copiar literal el patrón de
`estamentos.cargar_cache` / `guardar_cache` — robustos ante JSON corrupto o
disco sin permisos, con aviso y sin reventar la corrida. Un JSON sin la clave
`omitidos` (o plano, de una versión anterior) se lee como `{}` sin fallar.

#### Por qué DOS claves: la clasificación es global, la omisión es por módulo

Son hechos de naturaleza distinta y mezclarlos rompe otros módulos:

- **Que alguien sea o no de la dotación es un hecho de la persona**, invariante
  al REM que se esté corriendo -> `funcionarios` es global.
- **Que un estamento importe o no depende del REM** -> `omitidos` se indexa por
  módulo. Los kinesiólogos son irrelevantes para SM y **centrales para el A23**:
  si la omisión fuera global, omitirlos en SM los omitiría en A23.

Corolario importante: **un funcionario omitido NO se marca `interno`.** Queda
`desconocido` en la tabla global — que es lo honesto, nadie lo miró — y lo único
que cambia es que el diálogo *de ese módulo* deja de preguntar por él. El
diálogo del A23 sí le va a preguntar, que es lo correcto.

### 2.2 API

```python
def cargar(log=print) -> dict                  # {'funcionarios':…, 'omitidos':…}; vacio si no hay
def guardar(tabla, log=print) -> None
def clase(nombre, tabla) -> str                # 'interno'|'externo'|'desconocido'
def clasificar(serie_nombres, tabla) -> Series # vectorizado, para el DataFrame
def nuevos(ev, tabla, modulo) -> DataFrame     # evidencia SIN clasificar y SIN omitir (§2.3)
def marcar(tabla, decisiones) -> dict          # {nombre: True(externo)/False}; muta y guarda
def omitir(tabla, modulo, estamentos) -> dict  # agrega estamentos a omitidos[modulo]; muta y guarda
def omitidos(tabla, modulo) -> list            # estamentos omitidos para ese modulo
def en_rem(serie_clase) -> Series              # bool: clase != 'externo'   (§1.3)
def evidencia(ada, tabla=None, modulo=None) -> DataFrame   # §2.3
```

`nuevos()` es el gemelo de `estamentos.faltantes()` (mismo dedup normalizado,
mismo orden, ignora vacíos), pero devuelve **la evidencia**, no sólo nombres, y
descuenta dos cosas: los ya clasificados y los de estamentos omitidos para ese
módulo. Si devuelve vacío, **no se abre el diálogo**.

**Separación de fuentes de nombre.** El nombre del funcionario sale de
`rem_utils.MAPA_ATENCIONES["PROF"]` (IRIS `PROFESIONAL ATENCION`, Monitoreo
admin `FUNCIONARIO`) y, en el grupal, de `MAPA_GRUPAL["PREST"]`
(`FUNCIONARIO PRESTADOR`). `dotacion.py` **no conoce esos mapas**: recibe series
de nombres ya resueltas.

### 2.3 `evidencia()` — lo que hace posible decidir

Preguntar por un nombre pelado es inútil si no reconocés a la persona. El
diálogo se puebla con evidencia, y el mix de actividades es lo más sugerente
(la sala tiene un patrón distintivo aunque el nombre no diga nada):

| columna | de dónde |
|---|---|
| `funcionario` | `PROF` (nombre original, no normalizado) |
| `estamento` | `INSTR` del ADA |
| `n_atenciones` | filas del mes que **tributan** (`mask_tributa_ada`) |
| `actividades` | top-3 `ACT` por frecuencia, unidas con ` · ` |
| `sector` | `SECTOR` más frecuente |

Calcular **sólo sobre filas que tributan**: no tiene sentido preguntar por gente
cuyo trabajo no entra al REM SM de todos modos.

> Esto ya recorta mucho: la lista **no** es "todos los funcionarios del ADA",
> son los que registran actividades que tributan a SM. Si aun así sale enorme,
> eso **es información**: significa que `mask_tributa_ada` está pescando ancho y
> hay que mirarla. Loguear el número (`[dotacion] N funcionarios en M
> atenciones que tributan`) antes de abrir el diálogo.

#### Agrupación por estamento

`evidencia()` devuelve además el agregado por estamento, que es lo que ordena el
diálogo (§3.2):

| columna | contenido |
|---|---|
| `estamento` | de `INSTR` |
| `n_funcionarios` | distintos en ese estamento |
| `n_atenciones` | filas que **tributan**, del estamento completo |

Ordenar los grupos por `n_atenciones` **descendente**: lo que pesa queda arriba y
la cola larga es fácil de despachar en bloque.

### 2.4 Cómo enchufan las respuestas de Estadística (cuando lleguen)

Sin código nuevo, sin rehacer nada:

- **Lista de funcionarios de la sala** -> siembra `dotacion.json` directo
  (marcar esos nombres como `externo`).
- **Lista de actividades distintivas** -> pre-marca el tick en el diálogo y
  ordena la lista poniendo primero a los sospechosos. Sigue siendo **decisión
  del usuario**, no filtro automático (§1.1).

Ninguna de las dos es un mecanismo aparte. **No implementar esto todavía** (regla
del proyecto: no codear lo que no se usa); queda anotado para que la fase 1 no
cierre la puerta.

---

## 3. El diálogo GUI

### 3.1 Un solo diálogo, dos poblaciones

**No hay código especial de "primera vez".** La tabla vacía produce sola el
comportamiento de first-run:

- **Primera corrida** (`cargar()` devuelve `{}`) -> `nuevos()` devuelve
  **todos** los funcionarios del ADA -> el usuario vetea la dotación completa de
  un viaje.
- **Corridas siguientes** -> `nuevos()` devuelve sólo los nombres que no están en
  la tabla -> se pregunta sólo por ellos.

Ese veto inicial es **obligatorio**: en las pruebas del beta siempre existe la
posibilidad de que se haya colado un externo, así que la lista completa se revisa
a ojo una vez.

### 3.2 Forma: ticks agrupados por estamento

- **Sin tick = interno** (el default, mayoría de casos)
- **Con tick = externo**

Un `Checkbutton` por funcionario, con las columnas de `evidencia()` al lado, y
**los funcionarios agrupados bajo su estamento** — en la primera corrida son
decenas de nombres y una lista plana es ilegible. Scroll obligatorio. Botones
`Aplicar` / `Cancelar`.

Cada grupo lleva una cabecera con **el costo de omitirlo a la vista**:

```
[v] Psicologo(a)            4 funcionarios · 312 atenciones   [Omitir estamento]
[v] Kinesiologo(a)          3 funcionarios ·  47 atenciones   [Omitir estamento]
```

Dos acciones a nivel de grupo:

- **colapsar/expandir** (el `[v]`) — puramente visual, no persiste nada
- **`Omitir estamento`** — colapsa, deja de preguntar por ese estamento **en este
  módulo**, y lo persiste en `omitidos[modulo]` (§2.1)

**El contador de atenciones NO es decorativo, es el punto.** Un estamento sólo
aparece en la lista si tiene atenciones que **tributan al REM de ese módulo**;
omitirlo significa que esas atenciones **cuentan al REM sin que nadie las haya
mirado**. Ver `47 atenciones` es lo que convierte un "me da lo mismo" en una
decisión informada. Sin ese número, omitir es a ciegas.

Patrón de UI: `autorem._resolver_estamentos` (`autorem.py:499`) — mismo
`Toplevel` + `transient` + `grab_set` + `wait_window`, cambiando `OptionMenu` por
`Checkbutton` y agregando el agrupamiento. Reusar, no reinventar.

**`Cancelar` no clasifica a nadie**: los nombres quedan `desconocido`, la corrida
sigue (§1.3) y el aviso lo dice. Cancelar nunca debe abortar el procesamiento.

### 3.3 Dónde vive

Función `_dotacion_dialogo(root, ev)` en `autorem.py`, llamada desde el flujo de
la pestaña SM, **después** de cargar el ADA y **antes** de tabular. Necesita el
ADA cargado para tener la evidencia, así que va dentro de la corrida, no en la
configuración previa de la pestaña.

Agregar también un cuadro informativo en la pestaña (estilo
`_bloque_estamentos`) explicando el porqué y que la tabla queda guardada en
`~/.autorem`, más un botón **"Revisar dotación…"** que reabra el diálogo con
**todos** los nombres (no sólo los nuevos) **y los estamentos omitidos**,
expandibles, para revertir una clasificación o una omisión equivocada. Sin ese
botón, un tick mal puesto queda enterrado en un JSON.

El diálogo recibe el `modulo` (`"sm"`, `"a23"`, …) porque las omisiones se
indexan por él (§2.1). Es el único parámetro que lo hace específico de un REM.

---

## 4. Wiring en `modulos/rem_sm_actividades.py`

### 4.1 La factorización que hay que aprovechar

Todas las tablas de sección se construyen como `_tabla_a04(E)`, `_tabla_a06(E)`,
… tomando el mismo DataFrame de eventos `E`. Entonces:

> **NO hay que tocar ninguna función `_tabla_*`.** Se llaman **dos veces**, con
> `E` completo y con `E[E["en_rem"]]`.

Esto vale también para `_tabla_resumen(E, ini)`.

### 4.2 Clasificación a nivel de EVENTO, con el caso mixto

`E` ya trae una columna **`funcionario`** (agregada en v1.9.7). **Ojo:**
`_concat_funcionario()` (`rem_sm_actividades.py:157`) junta con ` · ` los nombres
únicos cuando una misma atención la registran varios profesionales, así que ese
campo puede valer `"NOMBRE A · NOMBRE B"`.

**Regla obligatoria para el caso mixto:**

> Un evento es `externo` **sólo si TODOS** sus funcionarios son externos.
> Si hay al menos uno interno -> el evento es `interno` (hubo gente nuestra en
> esa atención, es producción nuestra).
> Si no hay ninguno externo pero sí alguno desconocido -> `desconocido`.

Implementación: separar por ` · `, clasificar cada nombre, reducir con esa regla.
Sin esto, un evento mixto se clasificaría por el string completo `"A · B"`, que no
está en la tabla, y caería a `desconocido` — plausible pero errado.

Hoy no hay funcionarios mixtos (una persona con horas CESFAM *y* horas de sala),
pero **puede ocurrir**. No implementar la detección todavía; lo único que se pide
hoy es no cerrar la puerta: la clasificación es por nombre, y la evidencia por
funcionario ya queda calculada, así que detectarlo después sale barato.

### 4.3 Columnas nuevas en `SM_Detalle`

Agregar a `_EV_COLS` (`rem_sm_actividades.py:96`):

- `externo` — `interno` / `externo` / `desconocido`
- `tabula_en` — `AMBAS` (tributa y `en_rem`) / `SOLO_TOTAL` (tributa y externo) /
  `NINGUNA`

Nota: dentro de `E` **todas** las filas tributan (E se construye desde los
eventos), así que `NINGUNA` no aparece en `SM_Detalle`. Se deja el valor definido
igual para que la columna signifique lo mismo cuando se reuse en un módulo cuyo
detalle incluya filas no tributantes (p.ej. Trabajo Perdido).

### 4.4 Salida: fase 1 y fase 2

**Fase 1 (lo que se necesita HOY, para comparar contra el conteo manual):**

- las 2 columnas nuevas en `SM_Detalle`
- una hoja nueva **`Externos_Delta`**: una fila por casilla, columnas
  `Casilla · Total · Externos · REM`. Reusa `_tabla_resumen` sobre los dos
  subconjuntos.
- las hojas de sección siguen saliendo como hoy, pero **calculadas sobre
  `E[en_rem]`** (la tabla REM es lo que se informa).

Esto ya permite comparar contra lo hecho a mano sin reescribir el layout de
ninguna sección.

**Fase 2:** en cada hoja de sección, dos bloques apilados:

1. **primero** el bloque REM (sin externos) — es el pegable, es donde va la mano
2. **después** el bloque con externos, rotulado literal
   `INCLUYE EXTERNOS - NO PEGAR AL SA_26`

**Riesgo a mitigar explícitamente:** dos tablas casi idénticas juntas son una
trampa de copy-paste, y equivocarse **sobre-reporta el REM en silencio** — justo
el modo de falla que el proyecto persigue. Por eso el orden y el rótulo no son
cosméticos. Una sola hoja por sección con dos bloques (no dos hojas): ya son
varias hojas y duplicarlas empeora la confusión.

### 4.5 Avisos -> hoja LEEME

Acumular en `E.attrs["avisos"]` (formato existente:
`(casilla, categoria, motivo, que_hacer)`):

- si hay externos: cuántas atenciones se separaron y de cuántos funcionarios
- si hay `desconocido`: cuántas atenciones, **con los nombres**, categoría
  `PENDIENTE`, y el `que_hacer` = "clasificarlos en el diálogo de dotación"
- **si hay estamentos omitidos**: cuáles y cuántas atenciones aportan, categoría
  `OMITIDO`. Texto tipo *"Estamentos omitidos para SM: Kinesiólogo(a),
  Nutricionista — 47 atenciones cuentan al REM sin revisión individual"*. El
  atajo se permite, pero **deja huella**: el día que un número no cuadre, ese
  aviso dice exactamente qué pedazo nunca se miró. Sin él, una omisión en bloque
  queda indistinguible de un `interno` revisado a mano.
- si la tabla está vacía y el usuario canceló el diálogo: aviso fuerte de que
  **ninguna atención se separó** y el total incluye externos

Loguear lo mismo con prefijo `[dotacion]`.

---

## 5. Tests (`tests/test_dotacion.py`)

Mínimo:

1. `clase()` devuelve `desconocido` para un nombre ausente, y respeta el
   normalizado (mismo nombre con tildes/espacios distintos -> misma clase).
2. `nuevos()` con tabla vacía devuelve **todos** los nombres (comportamiento
   first-run), sin duplicados y en orden de aparición.
3. `marcar()` persiste y `cargar()` recupera; caché corrupto -> `{}` sin excepción.
4. **`en_rem` con `desconocido` es `True`** (§1.3) — el test que fija la
   decisión; si alguien la invierte, tiene que hacerlo a propósito.
5. **Caso mixto** (§4.2): `"A · B"` con A interno y B externo -> evento `interno`;
   ambos externos -> `externo`; externo + desconocido -> `externo`;
   interno + desconocido -> `interno`; sólo desconocidos -> `desconocido`.
6. En `sm_actividades`: con un funcionario marcado externo, `Externos_Delta`
   cuadra (`Total == Externos + REM` por casilla) y `SM_Detalle` conserva las
   filas externas.
7. **Omisión por módulo** (§2.1): omitir `kinesiologo(a)` en `"sm"` NO lo omite
   en `"a23"`; `nuevos(..., "sm")` deja de devolverlo y `nuevos(..., "a23")`
   sigue devolviéndolo.
8. **Un omitido NO queda `interno`**: tras omitir su estamento, `clase(nombre)`
   sigue siendo `desconocido` y `en_rem` sigue siendo `True`.

Actualizar el contador de tests en `CLAUDE.md` (§2 y §9) — lo verifica
`tools/check_version.py`.

---

## 6. Qué NO hacer

- **No borrar filas externas** de ningún detalle (§1.4).
- **No marcar como `interno` a los funcionarios de un estamento omitido** (§2.1).
  Quedan `desconocido`. Marcarlos sería más simple y es exactamente el error: un
  bloque que nadie miró pasaría a ser indistinguible de gente verificada a mano.
- **No hacer global la omisión de estamentos** (§2.1). Omitir kinesiólogos en SM
  no puede omitirlos en A23.
- **No omitir un estamento automáticamente** por tener pocas atenciones. La
  omisión es siempre una decisión explícita del usuario; el tool sólo le muestra
  el costo.
- **No filtrar por nombre de actividad / agenda / formulario** (§1.1). La
  actividad es evidencia en el diálogo, nunca criterio automático.
- **No meter la clasificación dentro de `cargar_atenciones`.** Es una decisión
  del módulo que tabula, no de la capa de lectura; y `cargar_atenciones` la usan
  módulos que hoy no quieren este filtro.
- **No arreglar de paso** que `_grupal_eventos` pase `PREST` como `est_col`
  (`rem_sm_actividades.py:248`). Es deuda conocida y anotada aparte; tocarla acá
  ensucia el diff y no la pide nadie.
- **No implementar** la detección de funcionarios mixtos ni la siembra desde
  Estadística (§2.4, §4.2). Anotados, no codeados.

---

## 7. Versionado

**Propuesta: `1.9.8` (Z), no `1.10.0`.**

`programas/dotacion.py` es **capa compartida / infraestructura**, no un módulo de
tarea que llene casillas nuevas del REM. Precedente directo: `programas/
formatos.py` entró como **1.9.2**, un bump de Z, por exactamente ese argumento.

Además `1.10.0` está apalabrado en `CLAUDE.md` §2.1 para el cierre de la familia
población (P6 + rescate). Tomarlo acá obligaría a correr esa reserva sin
necesidad.

Antes de commitear, correr la skill **`versionar`** y `tools/check_version.py`
(el pre-commit lo exige): headers de los `.py` tocados, entrada del CHANGELOG,
contadores de tests, y la versión declarada en `CLAUDE.md` §2 y §9. Recordar el
guardarraíl anti-colisión: si el CHANGELOG ya tiene una versión mayor que
`rem_utils.VERSION`, otra sesión avanzó y hay que rebasear antes de bumpear.

Y actualizar `CLAUDE.md`: fila de `programas/dotacion.py` en la tabla de §2, y
mención en el roadmap §12.
