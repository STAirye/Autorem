<!--
This document was generated with the assistance of Claude Opus 5.5 (Anthropic).
The human author reviewed, modified, and integrated the content.

Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
Copyright (C) 2026 Simon Tobar
SPDX-License-Identifier: GPL-3.0-or-later
Version: 2.0.13
-->

# Plan — Rango de meses (reportes de 3 / 6 meses)

> **PLAN APROBADO, SIN IMPLEMENTAR** — 2026-09-28. Escrito para una sesión fría
> (Sonnet): las decisiones de §2 están **cerradas**, no se re-discuten. Si algo del
> código no calza con lo que dice acá, es una divergencia: anotarla en §8 y preguntar,
> no improvisar.

## 1. Qué y por qué

El autor a veces tiene que entregar reportes de **3 o 6 meses** (casi siempre de
Actividades SM, muy rara vez del A05). Hoy lo hace con un `.xlsx` enlazado que **suma
las salidas mensuales**. La herramienta tiene que poder correr un **rango de meses**
y dar ese mismo total.

**No es un rango de días.** El autor lo descartó: no tiene sentido para lo que se
reporta. Y **nada de calendarios**: spinboxes año/mes, como el selector de hoy.

## 2. Decisiones cerradas

1. **Rango de MESES completos**, `desde (año, mes)` .. `hasta (año, mes)`, con los dos
   extremos incluidos. Un mes suelto = `desde == hasta`, que es el default y se comporta
   **idéntico a hoy** (mismo archivo, mismos nombres, mismos números).
2. **Motor: correr el cálculo MENSUAL una vez por mes, concatenar los eventos, y agregar
   UNA vez al final.** NO filtrar el ADA por el rango entero. Motivo (medido leyendo el
   código, §3): hay reglas ancladas al mes que se rompen con un filtro de rango.
3. **Salida:** las tablas de siempre con el **total del rango** (lo que se copia) + **una
   hoja extra `Por_Mes`** con una columna por mes, para cuadrar contra las salidas
   mensuales.
4. **Un mes del rango sin datos = FALLA**, nombrando el mes (fail loud, CLAUDE.md regla
   2). Un total de 6 meses al que le faltan 3 es el número plausible-pero-mal.
5. **Alcance, en este orden:** fase 1 = página **SM Actividades** (con su Trabajo
   Perdido); fase 2 = **A05**. **Fuera:** A23 y la familia población (P6, Rescate):
   ahí el mes es un CORTE sobre un snapshot, no un filtro (programas/CLAUDE.md §3.1).
6. **Widget:** `Desde [año][mes]  Hasta [año][mes]` con spinboxes, default = mes
   anterior en los dos. Regla de la GUI: la opción por defecto va ARRIBA
   (gui/CLAUDE.md, checklist punto 8).
7. **El A03·D.3 no cambia**: no filtra por mes (su export no tiene una fecha única). Hoy
   el nombre del archivo lleva el mes y el log avisa que no filtra; con rango, igual.
8. **Versión:** `Z` (2.0.14 o la que toque). No es un módulo nuevo (CLAUDE.md §9;
   precedente: la hoja LEEME fue un `Z`). Skill `versionar`.

## 3. Por qué no filtrar el rango entero (las dos trampas)

Si se filtrara el ADA por `[1er día del 1er mes, último día del último mes]` y se
corriera todo una vez:

- **GESTANTE** (`modulos/rem_sm_actividades.py:509-512`): es un flag por RUN con una
  ventana de 3 meses que termina en el mes reportado (`ini3 = ini - 2 meses .. fin`).
  Sobre un rango de 6 meses la ventana pasa a 8, y una persona embarazada solo en junio
  tendría marcadas TAMBIÉN sus atenciones de enero. La planilla sumada del autor nunca
  haría eso. **Plausible y mal.**
- **Trabajo Perdido** (`modulos/rem_sm_trabajo_perdido.py:294-343`) cuenta
  **distintos** (`nunique` de funcionarios, actividades, RUN). Acá el error es al
  revés: sumar los mensuales cuenta 3 veces al mismo paciente de 3 meses; sobre el
  rango tiene que ser distinto en todo el rango.

Correr el motor mensual por mes y agregar una vez resuelve las dos: cada regla mensual
queda **exactamente como hoy**, los conteos dan la suma de los mensuales, y los
distintos se calculan una vez sobre todo el rango.

Por qué los conteos SÍ suman: SM cuenta por ATENCIÓN (`drop_duplicates` por
`casilla/sub/id`, `:299`) y las sesiones grupales por `(fecha, estamento, actividad)`
(`:394`). Una atención cae en un solo mes. Esto es lo que amarra el test principal
(§6.1).

## 4. Fase 1 — SM Actividades + Trabajo Perdido

### 4.1 `programas/rem_utils.py`

- **`meses_del_rango(desde, hasta)`** -> lista `[(año, mes), ...]` inclusive. Levanta
  `ValueError` si `desde > hasta` (la GUI lo valida antes; esto es la red).
- **`etiqueta_periodo(meses)`** -> `"2026-07"` si es uno, `"2026-01 a 2026-06"` si son
  varios. Una sola función para el log, la LEEME, el resumen y los nombres de archivo
  (en nombres de archivo: `2026_07` / `2026_01-2026_06`, sin espacios).
- **No tocar** `_rango_mes` ni `filtrar_mes`: el motor mensual los sigue usando igual.

### 4.2 `modulos/rem_sm_actividades.py` — partir `procesar` en dos

Hoy `procesar` (`:458-705`) mezcla la CARGA (`:474-490`: opcionales inscritos y
multiprofesional, dotación, ADA) con el CÁLCULO DEL MES (`:508-702`). El grupal se carga
adentro del bloque del mes (`:554`). Llamar `procesar` 6 veces relee el Inscritos (el
archivo pesado) y el grupal 6 veces.

1. **`_cargar(ada, grupal, inscritos, multiprofesional, d, dotacion_tabla, log)`** ->
   dict con `tmap`, `multi`, `tabla_dot`, `d` (con `marcar_demografia`), `g` (grupal
   cargado o None), `fuentes`, `avisos_carga` (el aviso de fuente parcial `:496-504` y
   los de TRANS `:519-536`, que no dependen del mes). **Los opcionales siguen cargándose
   PRIMERO** (ronda 12: la pregunta «¿seguir sin él?» llega antes del trabajo pesado).
2. **`_eventos_mes(carga, mes, log)`** -> `(E_mes, avisos_mes)`: lo de `:508-610` para UN
   mes. Adentro sigue todo lo mensual: `_rango_mes`, GESTANTE con su ventana,
   `filtrar_mes` (fail loud por mes), el chequeo de ASISTE del grupal, el `len(E) == 0`,
   la marca interno/externo. **Cuidado con `d`**: hoy `procesar` le escribe
   `dem_gestante` / `dem_trans_*` encima. Con varios meses, calcular `dem_gestante` sobre
   una COPIA de las filas del mes (o como Serie aparte), nunca pisando `carga["d"]`
   entre meses: si no, el mes 2 hereda la marca del mes 1.
   - Agregar a `E_mes` una columna **`mes`** (`"2026-03"`), que es lo que arma
     `Por_Mes` y queda en `SM_Detalle` para auditar.
   - Los avisos del mes (GESTANTE subcontado, grupal sin SI/NO, multiprofesional que no
     calza) llevan el mes en el texto.
3. **`_tablas(E, multi, avisos)`**: lo de `:612-701` (avisos de dotación sobre el E
   COMPLETO, `Erem`, las tablas de sección). `_tabla_resumen(E, ini)` usa `ini` solo
   para `attrs["mes"]`: pasarle la etiqueta del período.
4. **`procesar(..., mes=None, ...)`** conserva su firma y su resultado: `_cargar` +
   `_eventos_mes` + `_tablas`. **Los tests actuales no deben cambiar.**
5. **`procesar_rango(..., meses, ...)`**: `_cargar` una vez, `_eventos_mes` por cada mes,
   `pd.concat`, `_tablas` una vez, más **`Por_Mes`**: filas = las de `SM_Resumen`,
   columnas = un mes cada una + `Total` (que tiene que ser igual a la columna de
   `SM_Resumen`; el test lo amarra). Con un solo mes en `meses`, `Por_Mes` **no** se
   escribe (el resultado es el de hoy).
   - Si un mes falla (`ArchivoInvalido`), se re-levanta con el mes en el mensaje:
     «en 03/2026: <mensaje original>». No se sigue con los demás.
   - Avisos repetidos en varios meses (el de TRANS sin Inscritos, por ejemplo) van UNA
     vez a la LEEME.
   - `E.attrs["mes"]` = la etiqueta del período (la LEEME ya acepta un string:
     `programas/cobertura.py:271`). Cambiar el rótulo «Mes reportado:» (`:273`) a
     «Período reportado:» cuando es un rango.

### 4.3 `modulos/rem_sm_trabajo_perdido.py`

Acá NO hay reglas ancladas al mes: `analizar` es por atención, y `auditar_atenciones`
también (formulario en la misma atención, consejería en la misma atención). Filtrar por
el rango entero es equivalente a concatenar, **y es lo que da bien los distintos**.

- **`analizar(d, ini, fin, ...)`** no cambia. `procesar_rango` le pasa `ini` del primer
  mes y `fin` del último.
- **Pero el fail loud es POR MES** (§2.4) y `filtrar_mes` sobre el rango entero solo
  falla si el rango ENTERO está vacío. Antes de `analizar`, correr un chequeo por mes:
  **`rem_utils.exigir_cada_mes(d, meses, fuente)`**, que llama a `filtrar_mes` para cada
  mes (y descarta el resultado). Así el mensaje es el de siempre, con el mes.
- `Por_Mes` del TP: atenciones a saco roto por mes (conteo por la columna `fecha`), con
  una advertencia en el propio encabezado: los distintos NO se suman entre meses.
- Los `nunique` de `TP_Resumen`, `Por_Actividad` y `Por_Funcionario` quedan sobre todo
  el rango: es lo correcto (§3).

### 4.4 GUI

- **`gui/widgets.py`: `selector_rango_meses(parent, defecto)`** -> `get()` que devuelve
  `((a1, m1), (a2, m2))` o `None` si algo no es número. Reusa `selector_mes` dos veces
  (etiquetas «Desde» / «Hasta»), así que los `from_`/`to` siguen saliendo de
  `ANIO_MIN`/`ANIO_MAX` (lo amarra `test_el_spinbox_y_la_guarda_de_anio_no_pueden_divergir`).
- **`gui/runner.py`: `valida_rango_meses(rango, messagebox)`** -> lista de meses o
  `None`. Valida cada extremo con `valida_mes` (mismos mensajes) y además
  `desde <= hasta` («"Desde" es posterior a "Hasta"»). Sin tope de largo: el autor pide 3
  o 6, y 12 es legítimo.
- **La página:** hoy `sm.PANTALLA["mes"] = True` y `app._resolver_ctx` arma
  `ctx["mes"] = (año, mes)` (`gui/app.py:236-242`, selector en `:630`). Agregar una clave
  nueva **`"rango_meses": True`** en `PANTALLA` (en vez de `"mes"`) que pinta
  `selector_rango_meses` y deja **`ctx["meses"]`** (lista). No tocar el camino de
  `"mes"`: lo usan las demás páginas. Sumar la clave al contrato que valida
  `tests/test_gui_registro.py` (claves opcionales conocidas) si hay tal lista.
- **`gui/paginas/sm.py`:**
  - `preparar` (`:227`): `dialogos.dotacion_ada(..., ctx["mes"], ...)` pasa a recibir los
    meses. En `gui/dialogos.py:217-218` el ADA se filtra por mes para preguntar por los
    funcionarios de ESE período: con rango, usar `exigir_cada_mes` + filtrar por el rango
    entero (la pregunta es «quién trabajó en el período», no por mes).
  - `correr` (`:243-299`): `procesar_rango` y el TP con los meses; nombres de archivo con
    `etiqueta_periodo` (`REM_SM_actividades_2026_01-2026_06.xlsx`). Con un solo mes, los
    nombres de hoy (`_2026_07`), sin cambio.
  - `resumen` (`:367-386`): `y, m = res["mes"]` pasa a la etiqueta del período. La
    columna se llama `Total mes` en `SM_Resumen`: dejarla así (la usan tests y el
    resumen) o renombrarla a `Total` en los dos lados a la vez — decidir con el código
    a la vista y anotarlo en §8.
  - Instrucciones: una línea sobre el rango («Para un reporte de 3 o 6 meses, elige
    Desde/Hasta: el total es la suma de los meses, y la hoja Por_Mes los separa»).

## 5. Fase 2 — A05

El A05 **no** pasa por `_rango_mes`/`filtrar_mes`: compara fila por fila
`mes_de_celda(...) != mes` (`programas/rem_saludmental.py:505-509`), con sus propios
mensajes («No hay formularios de 07/2026», `:570-580`).

- `marcar_eventos(..., mes=...)` pasa a aceptar **una lista de meses** (`mes` suelto se
  envuelve en lista: firma compatible con el CLI congelado, que no se toca). La fila
  entra si `ym in meses`. Contar filas POR mes; si alguno queda en 0 -> la misma falla
  de hoy, con ESE mes en el mensaje (§2.4).
- Columna **`Mes`** en la salida larga (una fila por evento), y hoja `Por_Mes` con el
  conteo por tipo de egreso/ingreso × mes. Con un mes, sin hoja extra.
- `gui/paginas/a05.py` `bloque_periodo`: el radio «Un mes» pasa a
  «Meses (desde / hasta)» con `selector_rango_meses`, default mes anterior en los dos,
  **arriba**; «Archivo completo» sigue debajo. `preparar` valida con
  `valida_rango_meses`.
- `rem_saludmental.py` tiene más usuarios (el histórico del P6 usa
  `verificar_formulario_sm`, no `marcar_eventos`, pero confirmarlo con grep antes).

## 6. Tests (lo que prueba que está bien, no que corre)

1. **El principal — rango == suma de mensuales.** Con un ADA + grupal sintéticos de 3
   meses: `procesar_rango(meses)` contra `procesar(mes)` de cada mes, y cada celda
   numérica de cada tabla de sección == la suma de las tres. Incluir en el fixture:
   - una **gestante** con evidencia solo en el 3er mes y atenciones SM en el 1ro: en el
     rango, sus atenciones del 1er mes **no** llevan la marca (la trampa de §3);
   - un **externo** de dotación (tiene que quedar fuera de las tablas en todos los meses).
2. **TP distintos:** el mismo RUN a saco roto en los 3 meses -> `pacientes afectados` = 1
   en el rango (no 3); `N atenciones` = 3.
3. **Mes vacío en el medio:** ADA con enero y marzo, rango ene-mar -> `ArchivoInvalido`
   cuyo mensaje nombra 02/2026. Lo mismo para el TP (`exigir_cada_mes`).
4. **Un solo mes == hoy:** `procesar_rango([m])` da las mismas tablas que `procesar(m)`
   y sin `Por_Mes`.
5. **`Por_Mes`:** la columna `Total` == `SM_Resumen`.
6. GUI: `valida_rango_meses` (desde > hasta rechaza con aviso; extremos fuera de
   `ANIO_MIN/MAX` rechazan; los mismos malos de `valida_mes`), y la página arma y
   bombea con `rango_meses` (en `test_gui_construccion`, sin comparar texto de la
   interfaz: tests/CLAUDE.md).
7. Fase 2: el A05 con rango == unión de los meses sueltos (mismas filas de evento), y
   el mes vacío en el medio falla nombrándolo.
8. **Mutación:** volver a filtrar el rango entero en SM (en vez del bucle) tiene que
   tumbar el test 1 por la gestante. Si no lo tumba, el fixture no ejercita la trampa.

## 7. Lo que NO se hace

- Rango de días, calendario, o escribir fechas a mano.
- A23, P6, Rescate.
- Tocar el CLI congelado (§12): `marcar_eventos` mantiene la firma que él usa.
- Cambiar `_rango_mes` / `filtrar_mes`, que el resto de los módulos usa igual.
- Tope de largo del rango.

## 8. Divergencias encontradas al implementar

*(vacío: anotar acá cualquier cosa del código que no calce con este plan, con la
decisión que se tomó y por qué)*
