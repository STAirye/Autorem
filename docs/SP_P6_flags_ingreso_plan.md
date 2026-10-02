<!--
This document was generated with the assistance of Claude Opus 5.5 (Anthropic).
The human author reviewed, modified, and integrated the content.

Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
Copyright (C) 2026 Simon Tobar
SPDX-License-Identifier: GPL-3.0-or-later
Version: 2.0.27
-->

# Plan — Dos flags de ingreso en la familia población (SP·P6)

> **APROBADO, SIN IMPLEMENTAR** — 2026-10-02. Plan autocontenido para una sesión fría
> (Sonnet). Versión destino **2.0.28** (Z: no es un módulo nuevo). Las decisiones
> están cerradas: si algo del código no calza con lo de abajo, anotarlo en §8 y
> preguntar, no reinterpretar.

## 1. Por qué

El 2026-10-02 se diffeó el P6 de septiembre: autoREM 2.0.25 contra el P6 manual del
PowerBI ferrada 2.5, primero celda a celda y después RUN a RUN contra el `DaxResults`
del PBI. Así se encontró la **causa de la brecha `Ingresado`** que el
[SP_P6_poblacion_plan.md](SP_P6_poblacion_plan.md) §9 tenía abierta:

- El Power Query de la tabla `PSM` del PBI hace `Table.LastN(Origen, 3)` sobre una
  carpeta con **un archivo por año** (2021…2026), así que **solo ve formularios de 2024
  en adelante**. autoREM lee el histórico completo.
- Por eso, quien tiene su formulario de ingreso/seguimiento solo antes de 2024 sale
  `Ingresado=SI` en autoREM y `NO` en el PBI. En septiembre: 492 personas, de ellas ~60
  vigentes en la base del P6. P6 R13: autoREM 1636 vs PBI 1515.
- Criterio del autor: **autoREM cuenta bien**. Quien ingresó, sigue en controles y no
  tuvo un hueco de más de 12 meses, sigue en control aunque su formulario sea viejo.

El autor tiene que informar esto a Estadísticas DISAM → SSMC, y además quiere que el
P6 marque a esa gente. Son dos flags con propósitos distintos:

| Flag | Para qué | Hoja de revisión |
|---|---|---|
| **1** — formulario de ingreso fuera de la ventana del PBI | respaldo del informe: quiénes el PBI no cuenta | `Revisar_Administrativo` |
| **2** — control continuo sin formulario reciente | clínico: a quién actualizarle el formulario | `Revisar_Clinico` |

**Ninguno cambia un número del P6.** Son columnas y filas de revisión, nada más.

## 2. Flag 1 — `¿Sin form. ingreso en 3 años calendario?`

**Regla.** Para cada persona con `¿Ingresado?=SI`:

- `Fecha último form. ingreso` = **máximo** de `est["fecha"]` entre las specs donde la
  persona quedó `Activo`. `est` es la tabla que devuelve `_estado_dx` por spec, la
  misma que ya entrega `_poner_diagnosticos(..., por_spec=...)`. Esa `fecha` es la
  del último formulario que cumple dx=SI & ESTADO ingreso|seguimiento & instrumento
  según la spec: exactamente lo que mira el DAX.
- Flag = `SI` si esa fecha es **anterior al 1 de enero del (año del corte − 2)**. En
  septiembre 2026 eso es antes de 2024-01-01. Es la ventana exacta de `LastN(3)` sobre
  archivos anuales (año en curso más los 2 anteriores), y se mueve sola cada año.
  Si no, `NO`. Quien no está Ingresado queda en `""`.

**Nombre de la columna:** clínico, no «invisible al PBI». El PBI se va a arreglar y la
columna tiene que seguir significando algo. El PowerBI aparece solo en el texto del
motivo.

**Salida:**
- `PSM_Poblacion`: columnas `Fecha último form. ingreso` y `¿Sin form. ingreso en 3
  años calendario?`.
- `Revisar_Administrativo`: **una fila por persona de la BASE del P6** (Estado=Activo ×
  Activo 12m × Ingresado) con flag `SI`. Motivo: `Ingreso solo con formulario anterior
  a <AAAA>-01`. Detalle: `el PowerBI ferrada (PSM: Table.LastN 3) no lo cuenta en el
  P6`. Valor_crudo: la fecha.
- LEEME (avisos de la corrida): el conteo en la base del P6. Es el número que va al
  informe.

## 3. Flag 2 — `¿Control continuo sin formulario 12m?` (SI / NO / SIN DATO)

Las cinco condiciones del autor, todas obligatorias:

1. **Tiene un ingreso por formulario.** Un formulario donde un dx/factor está en SI y
   su columna ESTADO dice **INGRESO**. Seguimiento **no** cuenta. El filtro de
   instrumento es el mismo que aplica cada spec en `_estado_dx` (médico donde la spec
   lo exige), para no tener dos reglas. Se recorre `TODAS_LAS_SPECS`, igual que
   `¿Ingresado?`.
2. **Se ha mantenido en controles** y
3. **nunca tuvo un hueco de más de 12 meses.**
   - **Contactos** = fechas del ADA con `ACTIVIDADES_SM_7` (la misma lista de `Activo
     12m`, `_runs_actividad_sm`) **∪** fechas de **todos** los formularios de Control
     SM, de cualquier instrumento. Decisión del autor: un formulario sin atención no
     debería existir, pero si existe cuenta como contacto.
   - Desde la fecha de ingreso (inclusive) hasta el corte, se ordenan los **meses** con
     contacto. `Hueco máx. (meses)` = la mayor diferencia en meses calendario entre
     dos meses de contacto consecutivos. El ingreso cuenta como el primer contacto.
   - Se cumple si `Hueco máx. <= 12` **y** `¿Activo 12m?=SI`. Lo segundo cubre el
     hueco final, entre el último contacto y el corte, con la regla que ya existe.
4. **No tuvo ningún formulario** de Control SM, de cualquier instrumento y cualquier
   contenido, en la ventana de 12 meses de `Activo 12m`: `[_mes_offset(corte, 11)[0],
   corte]`.
5. **No fue egresado del diagnóstico por el que ingresó**, sea cual sea el motivo. Si
   después de la fecha de ingreso de ese dx (y hasta el corte) hay un formulario con
   ese mismo dx en SI y ESTADO con `EGRES`, ese ingreso **no sirve**. Se usa el mismo
   filtro de instrumento que `cond_egr` en `_estado_dx`.

**Qué ingreso se toma si hay varios.** Por cada spec, el **último** ingreso. Se descartan
los que tienen un egreso posterior (condición 5). Entre los que sobreviven, se toma el
**más reciente**, porque la continuidad se mide desde el último reingreso: quien ingresó
en 2021, se perdió y reingresó en 2023 está en control continuo desde 2023.

**`SIN DATO`** — falla ruidoso (CLAUDE.md regla 2), nunca un NO callado. Si el ADA
cargado empieza (mes de su `FECHA` mínima) **después** del mes de la fecha de ingreso,
el hueco no se puede verificar y el flag sale `SIN DATO`. Nunca `NO`. El conteo de SIN
DATO va a la LEEME, junto con la fecha mínima del ADA y la indicación de cargar más
historial.

**Valores:** `SI` cumple 1-5 · `NO` no cumple alguna · `SIN DATO` cumple 1 y 5 pero el
ADA no cubre desde el ingreso · `""` sin ingreso válido (no cumple 1 o 5).

**Salida:**
- `PSM_Poblacion`: `Fecha ingreso (form)`, `Hueco máx. (meses)` y `¿Control continuo
  sin formulario 12m?`.
- `Revisar_Clinico`: una fila por persona de la **base del P6** con flag `SI`. Motivo:
  `Control continuo sin formulario en 12 meses`. Detalle: fecha de ingreso y hueco máx.
  Fila_P6: 13.
- LEEME: conteos de SI y de SIN DATO.

## 4. El ADA histórico

- El input ADA del P6 **ya acepta una lista** de archivos (plan P6 §2). Para el flag 2 el
  autor carga la carpeta completa: `OneDrive\Datos madre\Variables 12m\Atenciones\`,
  con `2021.xlsx` … `2025.xlsx`, `2026.xlsx` y `2026 09.xlsx` (~150 MB en total).
- **Traslapes** (`2026.xlsx` y `2026 09.xlsx` se pisan): verificado el 2026-10-02 que
  **todo** uso de `d_ada` en `poblacion.py` trabaja con conjuntos o ventanas
  (`_runs_actividad_sm`, `_flags_actividad`, `gestante_runs`, cobertura), así que los
  duplicados no cambian nada. Si el implementador encuentra un uso que cuente filas,
  hay que deduplicar por `ATENID` y anotarlo en §8.
- **Medir el tiempo de carga** de los 7 archivos con calamine y anotarlo en §8. Si se
  pasa de ~60 s, se le avisa al autor; no hay que optimizar por las suyas.
- **La GUI** (`gui/paginas/` del P6, y la del rescate si comparte input): el texto de
  ayuda del ADA dice «13 meses». Hay que agregar que **cargar el histórico completo
  habilita el flag de control continuo**. Se mantienen los 13 meses como mínimo
  obligatorio.
- `_verificar_cobertura_fechas` no cambia: un ADA largo no es un error.

## 5. Dónde va el código

- **`programas/poblacion.py`**, en `construir_poblacion`: pasar `por_spec={}` a la
  llamada de `_poner_diagnosticos` (hoy en ~:930) para tener las `fecha` por spec (flag
  1). Para el flag 2, una función nueva `_control_continuo(form, d_ada, corte, ...)` que
  devuelve un DataFrame por RUN (`fecha_ingreso`, `hueco_max`, `flag`). Tiene que
  reusar `_tok` / `_instr_medico` y las columnas `q<N>_n` de cada spec. **No** se toca
  `_estado_dx`: su `activos` mira el ÚLTIMO ingreso|seguimiento, y acá se necesita el
  último INGRESO y los egresos posteriores, que es otra consulta.
  - Ojo con el comentario de `_estado_dx` sobre las columnas que se copian (:509-518):
    la función nueva **no** debe copiar las ~130 columnas de `form`, solo las que lee.
- **`modulos/rem_sp_p6_poblacion.py`**: las filas de `Revisar_Administrativo` /
  `Revisar_Clinico` y los avisos de LEEME. Hay que respetar el filtro `base` (:308-311) y
  no reconstruirlo: ver la deuda «filtro base escrito dos veces» del CLAUDE.md §12.
- Las columnas nuevas van a `COL_ACTIVIDAD` o donde `PSM_Poblacion` defina su orden.
  Revisar `escribir`.

## 6. Tests (`tests/test_poblacion*.py` / `tests/test_sp_p6*.py`, según dónde caiga)

Con fixtures armados a mano. Un RUN de ejemplo siempre tiene forma `11111111-1`;
para varios, RUN con DV válido inventado, nunca uno real.

Flag 1 (corte 2026-09):
- Formulario de ingreso solo en 2023-05 → `SI`, y con fila en Revisar_Administrativo si
  está en la base.
- Formulario 2023-05 + seguimiento 2025-02 → `NO`.
- Formulario 2024-01-02 → `NO` (borde de la ventana).
- No ingresado → `""`.

Flag 2 (corte 2026-09):
- Ingreso 2022-03, contactos ADA cada ≤12 meses hasta 2026-08, ningún formulario desde
  2025-09 → `SI`.
- Igual, pero con un hueco de 13 meses entre dos contactos → `NO`, `Hueco máx.=13`.
- Igual, con un formulario en 2026-02 → `NO` (condición 4).
- Igual, con un EGRESO del mismo dx en 2024 → `""` (condición 5).
- EGRESO de **otro** dx: no invalida el ingreso.
- Ingreso 2022-03 con un ADA que empieza en 2025-09 → `SIN DATO`, nunca `NO`.
- Hueco «cubierto» solo por un formulario sin atención ADA → cuenta (`SI`).
- Reingreso: ingreso 2021, hueco de 2 años, reingreso 2023 continuo → `SI` desde 2023.

Corrida completa: los números del P6 (P6_A1) **idénticos** antes y después. Se
comparan las grillas en el test, no el texto.

## 7. Cierre

- `tools/correr_tests.py` / `pytest`, `check_cp1252` (solo ASCII en los `.py`: nada de
  `≤`/`→` en los comentarios nuevos).
- Skill `versionar` → **2.0.28**: VERSION, headers de los `.py` tocados, contadores de
  tests en CLAUDE.md y README, y CHANGELOG.
- **Corregir el §9 de `SP_P6_poblacion_plan.md`:** la hipótesis «ventana de histórico
  distinta» figura como descartada por «mismos inputs, todo 2021 en adelante». Era
  **falso del lado del PBI** (`Table.LastN(Origen, 3)`). Pasa a ser **la causa**, con los
  números de §1. **Pedir el OK del autor antes**: al escribir este plan seguía sin
  confirmar.
- Commit sin push. Cerrar este archivo con el header `LISTO Y MERGEADO`.

## 8. Divergencias encontradas al implementar

(vacío)
