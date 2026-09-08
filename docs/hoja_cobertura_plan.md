<!--
This document was generated with the assistance of Claude Opus 5 (Anthropic).
The human author reviewed, modified, and integrated the content.

Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
Copyright (C) 2026 Simon Tobar
SPDX-License-Identifier: GPL-3.0-or-later
Version: 1.9.2
-->

# Plan — Hoja «LEEME»: qué NO cubre autoREM

> **Estado: IMPLEMENTADO** (v1.8.3, sep-2026) — `programas/cobertura.py` +
> `tests/test_cobertura.py`, enchufado a los dos caminos de escritura (§6). El
> guardarrail anti-olvido del §7 quedo como test que **descubre por introspeccion**
> los modulos de `modulos/` y falla si a alguno le falta su entrada en `COBERTURA`.
>
> Este documento pasa de plan a **referencia del catalogo**: al agregar un modulo o
> cambiar que cubre, se edita `COBERTURA` y se refleja aca (§3). Lo unico que sigue
> abierto es el checklist completo del REM (D1, §8). El aviso de fuente Admin
> parcial del A23 quedo CERRADO en v1.9.2 — ver §4.1.

---

## 0. Problema

El exe corre sin errores, la planilla sale, y **nada en ella dice que las
Consultorias A06·A.2 siguen siendo a mano**. Un colega que no escribio el codigo
asume que el REM esta completo porque la herramienta no se quejo.

Hoy esa informacion existe en tres lugares que el usuario final no ve:

1. Docstrings de los modulos (`rem_sm_actividades.py:36` — *"A05 y las Consultorias
   A06·A.2 quedan fuera"*).
2. `CLAUDE.md` (repo, no se distribuye con el exe).
3. El **log de la GUI**, que se pierde al cerrar la ventana.

El log es el caso mas grave: ahi viven los avisos de que **esta corrida** salio
degradada (`[sm] sin reporte grupal -> A06 psicosocial / A19a grupal / A27 = 0`).
Eso es exactamente un numero plausible pero callado y errado — lo que la regla del
proyecto *"fallar ruidoso, no silenciosamente mal"* existe para evitar.

**Objetivo:** que cada `.xlsx` que emite autoREM lleve como **primera hoja** un
recordatorio de que casillas del REM de ese modulo NO quedaron llenas, y por que.

---

## 1. Decisiones cerradas

| # | Decision | Detalle |
|---|---|---|
| **D1** | **Alcance = vecindario del modulo** | Solo las casillas del REM que el modulo toca + lo adyacente descartado a proposito. **NO** un checklist completo del REM. Se evaluo extraer los labels de fila del `SA_26.xlsm`/`SP_26.xlsm` versionados (mismo precedente que la mascara de proteccion del P6, §5.0 del plan P6): descartado por ahora — hoja larga, senal diluida, y un mapeo label->cobertura que hay que mantener igual. Queda anotado como posible v2. |
| **D2** | **Dos capas: estructural + esta corrida** | Ademas de lo que el modulo *nunca* cubre, la hoja registra lo que quedo a medias por los inputs de ESTA corrida (sin reporte grupal, sin Informe Inscritos, sin Maestro...). Es la razon principal del feature. |
| **D3** | **Una hoja por archivo de salida** | Cada modulo escribe su propio `.xlsx`, asi que la hoja describe el REM de ESE modulo. No hay hoja global consolidada. |
| **D4** | **Fuente unica declarativa** | El catalogo vive en `programas/cobertura.py`, no repetido en cada modulo. Un modulo nuevo sin entrada en el catalogo **falla el test** (§7). |

---

## 2. Arquitectura

Modulo nuevo: **`programas/cobertura.py`**. Sin dependencias nuevas (openpyxl, que
ya es obligatoria).

```
programas/rem_utils.py   (primitivas)
        ^
programas/cobertura.py   (catalogo + render de la hoja)
        ^
modulos/*.py + autorem.py  (la piden al escribir)
```

### 2.1 Estructura de datos

```python
# Categorias (el "por que" no esta lleno). El texto es lo que ve el usuario.
MANUAL      = "MANUAL"           # no hay reporte/formulario en RAYEN: se llena a mano
FUERA       = "FUERA DE ALCANCE" # otro REM, u otro modulo del exe
OMITIDO     = "OMITIDO"          # existe pero este centro no lo usa
PENDIENTE   = "PENDIENTE"        # se va a implementar, hoy sale 0
VALIDACION  = "EN VALIDACION"    # implementado pero los numeros NO estan cerrados
SIN_REGISTRO = "SIN REGISTRO"    # ver abajo: el 0 es CORRECTO, pero hay trabajo invisible

# Una entrada: (casilla, categoria, motivo, que_hacer)
# `casilla` = nomenclatura REM tal cual la usa el autor ("A06·A.2").
# `que_hacer` = accion concreta, o "" si no aplica.
```

### 2.1.1 `SIN REGISTRO` — la categoria que mas importa

Distinta de `PENDIENTE`. Aca **el codigo funciona y el 0 es correcto**: lo que falta
no es implementacion ni un input, es que **nadie usa el canal de registro**. El
trabajo clinico se hace, pero se escribe donde el REM no lo ve (tipicamente en
**indicaciones** de la ficha, que no tributa).

Es la unica categoria donde el mensaje al usuario es **«no lo arregles a mano»**: si
llena la casilla asumiendo que autoREM fallo, esta inventando un dato. Y es la misma
familia que ya persigue el modulo de **Trabajo Perdido** — trabajo real, invisible al
REM.

Casos actuales:

| Caso | Sintoma | Donde esta escrito |
|---|---|---|
| **PIC** (P6, col. AV) | fuente existe en el Maestro, ~1 registro en 8 meses | `SP_P6_poblacion_plan.md` §5.4.2 |
| **A27 / A32·F2** (SM) | actividad creada hace poco, sin uso | este plan, §3.1 |
| **A23 · M.2** talleres | los talleres aun no se hacen; lo rotulado grupal cae a `REM-Gestion` | `A23_P3_plan.md` §"Educacion grupal (M.2)" |
| **A26·A1** VDI del PADDS | bien registradas, pero ningun modulo las tabula | este plan, §3.2 |

Los primeros tres comparten forma con el PIC, cuyo tratamiento **ya esta razonado en
extenso** en `SP_P6_poblacion_plan.md` §5.4.2 (incluida la condicion de salida: no
espera un formulario nuevo, espera **registro**). Reusar ese razonamiento, no
reinventarlo.

```python

COBERTURA = {
    "sm_actividades": {
        "rem": "SA_26 — Salud Mental (A04 / A06 / A19a / A26 / A27 / A32)",
        "cubre": ["A04·A24", "A06·A.1", "A19a·A.3", "A26·A", "A27", "A32·F"],
        "no_cubre": [ ... ],   # ver §3
    },
    ...
}
```

### 2.2 API

```python
def entradas(modulo_id, avisos=()):
    """Filas de la hoja: lo estructural del catalogo + los `avisos` de esta corrida.
    `avisos` = iterable de (casilla, categoria, motivo, que_hacer)."""

def escribir_hoja(wb, modulo_id, contexto, avisos=(), nombre="LEEME"):
    """Crea la hoja LEEME como PRIMERA del workbook openpyxl `wb`.
    `contexto` = dict con mes reportado, archivos de entrada, perfil/formato."""
```

`escribir_hoja` recibe un **workbook openpyxl**, no un `ExcelWriter`, para servir a
los dos caminos de escritura (§6).

---

## 3. Catalogo por modulo (contenido de `no_cubre`)

Todo lo de abajo esta verificado contra el codigo actual; la referencia entre
parentesis es donde vive hoy la afirmacion.

### 3.1 `sm_actividades` — SA_26 Salud Mental

| Casilla | Cat. | Motivo | Que hacer |
|---|---|---|---|
| **A06·A.2 Consultorias de Salud Mental** | MANUAL | No hay reporte ni formulario en RAYEN que las registre | Contarlas a mano y pegarlas en el SA_26 |
| A05 ingresos / egresos | FUERA | Los cubre otro modulo del exe | Usar la pestana **A05** |
| A03·H Tamizaje (PSC-17, PHQ-9...) | FUERA | El exe cubre A03·**D.3** (instrumentos de personas ya INGRESADAS) | — |
| Espacios Amigables · Familias en Riesgo | OMITIDO | No se usan en este centro (`rem_sm_actividades.py:58`) | Si el centro empieza a usarlos, hay que implementarlos |
| Campana de Invierno (col. demografica) | OMITIDO | Write-protected en la hoja SM del template (`:61`) | — |
| Demografia de las actividades **grupales** | PENDIENTE | El reporte 'Atenciones Grupales' no trae demografia -> A06 psicosocial / A19a grupal / A27 salen con demografia en 0 | Si se necesita, cruzar a mano contra el padron |
| Control SM a paciente **SENAME** | OMITIDO | Excluido a proposito: SENAME hace su propio REM (`:34`) | — |
| **A27** y **A32·F2** | SIN REGISTRO | **La actividad existe en RAYEN pero no se usa** (se agrego hace poco). El trabajo se registra en la ficha, en **indicaciones**, que no tributa -> **0 actividades realizadas**. El filtro esta implementado pero nunca se pudo validar contra datos reales | El 0 es correcto: **no lo llenes a mano asumiendo que falta**. Si sabes que la actividad se hizo, se registro en un canal que el REM no ve |

### 3.2 `sm_trabajo_perdido` — auditoria, no tributa

| Casilla | Cat. | Motivo | Que hacer |
|---|---|---|---|
| *(todas)* | FUERA | Este reporte **no tributa a ninguna casilla del REM**: es auditoria de trabajo mal registrado | No copiar nada de aqui al SA_26 |
| **A26·A1** VDI del PADDS (dependencia severa) | PENDIENTE | Se excluyen del universo SM a proposito (`EXCLUIR_SMISH`) porque no son SM — pero **hoy no las tabula ningun modulo** | Contarlas a mano hasta que exista `rem_a26_domiciliaria` |

### 3.3 `a23_respiratorio` — SA_26 A23

| Casilla | Cat. | Motivo | Que hacer |
|---|---|---|---|
| Secciones **B · C · J · K · L · M.2 · P · Q** | FUERA | Fuera de alcance del modulo (`rem_a23_respiratorio.py:466`) | A mano |
| Seccion **A** (ingreso a sala) | PENDIENTE | Semantica distinta: 'ingreso a sala' != 'tuvo dx' -> sale 0 | A mano |
| Seccion **I** espirometria basal / post BD | PENDIENTE | Hoy hay 1 solo indicador, el REM pide dos | A mano |
| Seccion **O** (EPOC forma A/B) | PENDIENTE | Falta la forma A/B -> sale 0 | A mano |
| Formulario 'Otros Cronicos' en formato **Administrativo** | PENDIENTE | Solo se lee el formato IRIS | Descargar el formulario en IRIS |

### 3.4 `a05_o_egresos` / `a05_n_ingresos` — SA_26 A05

| Casilla | Cat. | Motivo | Que hacer |
|---|---|---|---|
| Egresos por **Otras Causas** (clasificacion) | MANUAL | Requiere decision clinica caso a caso (abandono vs clinica). El modulo los **flaggea**, no los clasifica | Revisar la lista de RUT del detalle y clasificar |
| Epilepsia (pregunta 75) | FUERA | Tributa al REM de adulto, no a SM (`EXCLUIR_PATOLOGIA`) | — |
| Programas de rehabilitacion / acompanamiento (77, 79, 81) | FUERA | No son diagnosticos SM | — |

### 3.5 `a03_d3_instrumentos` — SA_26 A03·D.3

| Casilla | Cat. | Motivo | Que hacer |
|---|---|---|---|
| **A03·H** Tamizaje | FUERA | El modulo cubre D.3 (personas INGRESADAS al PSM) | A mano |
| Aplicaciones 'Sin riesgo' (bajo el corte) | OMITIDO | Van al detalle auditable pero **no** al D.3 (por diseno) | — |
| Conteos agregados por rango etario | PENDIENTE | Planificado para A03 D.3 v2 | — |

### 3.6 `sp_p6_poblacion` — SP_26 P6·A.1

| Casilla | Cat. | Motivo | Que hacer |
|---|---|---|---|
| **Plan de Cuidado Integral** (col. AV) | SIN REGISTRO | **No va vacia ni a mano: la llena una regla operativa WIP** (= total de la fila en GES depresion/Alzheimer y en factores de riesgo; 0 en el resto). La fuente **existe** (actividad `Plan Cuidado Integral Elaborado` del Maestro, llega por el ADA) pero el registro es ~0: 1 caso en 8 meses, porque el PIC se escribe en **indicaciones** de la ficha. Regla completa en `SP_P6_poblacion_plan.md` **§5.4.2** | Revisar **AV24** a mano: si `AV24 > C24` hay comorbilidad depresion+demencia contada dos veces |
| **Toda la grilla** | VALIDACION | Modulo en validacion: el filtro `Ingresado` da **2972** contra **2226** del PowerBI (ver `SP_P6_poblacion_plan.md` §9) | **Contrastar contra el conteo manual antes de entregar** |
| Delta P(m) - P(m-1) -> A05 N/O | PENDIENTE | Fase 4 del plan, no implementada | Seguir usando el `CALCULADOR A05` |

---

## 4. Capa dinamica — avisos de ESTA corrida

Mecanismo: los modulos pandas ya guardan cosas en `df.attrs` (`E.attrs["tablas"]`),
y `escribir()` ya lo lee. **Reusar eso**: `E.attrs["avisos"] = [...]`, sin plumbing
nuevo. Cada punto de degradacion que hoy solo loguea, ademas **anexa** su tupla.

Puntos a instrumentar (linea = donde esta hoy el `log(...)`):

| Modulo | Linea | Condicion | Aviso a agregar |
|---|---|---|---|
| `rem_sm_actividades` | `:412` | sin reporte grupal | A06 psicosocial · A19a grupal · A27 = **0** |
| `rem_sm_actividades` | `:382`/`:388` | sin Informe Inscritos, o 0 TRANS | Columnas **TRANS** de A06/A32 = 0 |
| `rem_sm_actividades` | `:433` | sin Monitoreo Multiprofesional | **A26** queda todo mono-profesional (Un / Dos o mas sin desglosar) |
| `rem_sm_actividades` | `:402` | el ADA no cubre 3 meses | **Gestantes SUBCONTADAS** (la ventana necesita 3 meses) |
| `rem_sm_trabajo_perdido` | `:248`/`:256` | sin Maestro de Actividades | Clasificacion por **heuristica**, menos precisa |
| `rem_a23_respiratorio` | `:168` | formularios 'Otros y Respi' no cubren el periodo | **Seccion G SUBCONTARA** |
| `rem_a23_respiratorio` | `:471` | sin formulario 'Otros y Respi' | No se puede filtrar 'Pertenece a SALA' -> **el A23 no esta acotado a poblacion bajo control** |
| `rem_saludmental` | `:366` | perfil **administrativo** | Pueblos Originarios · SENAME · Prot. Ninez · Migrante · Trans salen **vacias** |
| `rem_a03_d3_instrumentos` | `:253` | sin 'Utilizacion de Cupos' | Columna **Estamento** vacia |

### 4.1 El aviso que no se podia emitir — DESBLOQUEADO (v1.9.2)

El caso **«fuente Monitoreo Administrativo -> Ira Alta / Bronquitis / EPOC-exac.
salen 0»** (A23) era el mas peligroso de todos y quedo fuera de la v1: el grupo
pandas no detectaba eje, asi que el modulo no *sabia* que la fuente era parcial.
Vivio como advertencia **estructural** permanente en `cobertura.py`.

**Cerrado por `formatos.py` fase 2** (v1.9.2). Hoy es un **aviso dinamico**: sale
solo en las corridas donde de verdad pasa, y el texto estructural se borro. Lo
emiten los modulos con `formatos.aviso_fuente(*d.attrs["fuente"], consecuencia)`.

Tres cosas del diseno que conviene no deshacer:

1. **Se clasifica la FUENTE, no las columnas.** El problema nunca fue una columna
   ausente: en el Monitoreo Admin `DIAGNOSTICO` **existe y resuelve perfecto**, solo
   que trae texto sin codigo ICD. `resolver_columnas` no puede verlo — solo el eje
   habla de la CALIDAD de una columna, no de su existencia.
2. **La firma es negativa** (probar que ES el A/D/A de IRIS), porque no hay UN
   "otro lado" que reconocer: el eje Administrativo **no tiene equivalente del
   A/D/A**, asi que lo que llegue puede ser otro reporte, un archivo editado o algo
   que RAYEN aun no inventa. Sale fail-safe: lo que no se prueba, avisa.
3. **Tres estados, no dos.** `cambiada` (algunas claves, no ninguna) existe para el
   dia que RAYEN renombre una columna del A/D/A: sin ese estado seria un falso
   «parcial» permanente, y un aviso que grita siempre deja de leerse.

**Descubrimiento colateral, peor que el original:** en **SM** la fuente parcial no
degrada, **rompe**. El conteo es `drop_duplicates(casilla, sub, id)` con
`id = ATEN ID`; sin esa columna todas las filas comparten id `"None"` y **cada
casilla colapsa a 1 evento**. El aviso lo dice y pide explicitamente NO copiar esas
tablas al SA_26.

---

## 5. Formato de la hoja

Nombre: **`LEEME`** (primera hoja del libro).

```
autoREM 1.9.2 - QUE NO INCLUYE ESTA PLANILLA
REM: SA_26 - Salud Mental (A04 / A06 / A19a / A26 / A27 / A32)
Mes reportado: 2026-07     Generado: 2026-09-07 18:40
Entradas: ADA_julio.xlsx · Grupal_julio.xlsx
Cubre: A04·A24 · A06·A.1 · A19a·A.3 · A26·A · A27 · A32·F

ESTA CORRIDA
  Casilla              | Estado    | Motivo                        | Que hacer
  A06 psicosocial ...  | SIN DATOS | no se cargo el reporte grupal | cargar 'Atenciones Grupales'

SIEMPRE A MANO / FUERA DE ALCANCE
  A06·A.2 Consultorias | MANUAL    | no hay reporte en RAYEN       | contar a mano
  ...
```

Reglas de render:

- **Los avisos de la corrida van ARRIBA**, antes de lo estructural: es lo
  accionable hoy. Si no hay ninguno, escribir literal
  `Sin avisos: todas las fuentes opcionales estaban cargadas.` — **nunca omitir la
  seccion**, para que su ausencia no se lea como "no habia nada que revisar"
  (misma regla que las hojas de revision del P6, §5.5 de su plan).
- Encabezado en negrita + `freeze_panes`, anchos de columna fijos.
- Texto **cp1252-safe**: nada de flechas, emoji ni cajas (revientan la consola de
  Windows). Usar `->` y `·`.
- La hoja se escribe **siempre**, aunque no haya nada degradado.

---

## 6. Integracion — hay DOS caminos de escritura

### 6.1 Modulos pandas (`ExcelWriter`)

`rem_sm_actividades` · `rem_sm_trabajo_perdido` · `rem_a23_respiratorio` ·
`rem_sp_p6_poblacion`. En su `escribir()`, **antes** de cualquier `to_excel`:

```python
with pd.ExcelWriter(salida, engine="openpyxl") as xw:
    cobertura.escribir_hoja(xw.book, "sm_actividades", contexto,
                            avisos=E.attrs.get("avisos", ()))
    ...  # el resto igual
```

Ojo: `pd.ExcelWriter(salida)` sin `engine` en `rem_sm_actividades` y
`rem_a23_respiratorio` — verificar que `xw.book` sea openpyxl (lo es por defecto
para `.xlsx`); si no, fijar `engine="openpyxl"` como ya hace el P6.

Como el libro se crea vacio y la hoja LEEME es la primera en escribirse, queda en
indice 0 sin mover nada.

### 6.2 Camino openpyxl (A05 y A03) — **cuidado**

Aca el workbook **es el export de entrada**, que ya trae la hoja de datos original
en el indice 0. Hay que insertar: `wb.create_sheet("LEEME", 0)`.

Y **A05 corre varias tareas sobre UN mismo libro**: `_correr_tareas`
(`autorem.py:76`) itera egresos+ingresos y guarda una vez. Entonces la hoja se
escribe **una sola vez, despues del loop y antes de `wb.save`**, con la **union**
de la cobertura de las tareas que corrieron — no una hoja por tarea.

El aviso de perfil administrativo (§4, `rem_saludmental.py:366`) se conoce en
`_correr_tareas` sin plumbing: sale del `perfil` que ya recibe.

A03 escribe por su cuenta (`rem_a03_d3_instrumentos.py:328`) -> su propia llamada.

---

## 7. Tests

Agregar `tests/test_cobertura.py`:

1. **Guardarrail anti-olvido:** todo modulo registrado en `autorem.TAREAS` (y todo
   modulo con `escribir()`) **tiene** entrada en `COBERTURA`; y toda entrada del
   catalogo corresponde a un modulo real. Un modulo nuevo sin su disclaimer **rompe
   el test**. Este es el punto del test — que el catalogo no se pudra.
2. La hoja `LEEME` existe y es **la primera** (`wb.sheetnames[0] == "LEEME"`), en
   los dos caminos: un modulo pandas y el camino A05 (que parte de un libro con
   datos ya en el indice 0).
3. Sin fuentes opcionales -> la seccion `ESTA CORRIDA` trae el aviso esperado
   (ej. correr `sm_actividades` sin grupal -> aparece "A06 psicosocial").
4. Con todas las fuentes -> la seccion existe igual, con el texto "Sin avisos".
5. Todo el texto del catalogo es **cp1252-encodable**
   (`texto.encode("cp1252")` no levanta).

Suite actual: **94 tests**. Estos suman ~6.

---

## 8. Fuera de alcance de este plan

- **Checklist completo del REM** extraido del `SA_26.xlsm`/`SP_26.xlsm` (D1). Si
  algun dia se quiere: los templates ya estan versionados y la mascara de
  proteccion del P6 es el precedente de "extraer del archivo, no transcribir".
- ~~Aviso de fuente Monitoreo Admin parcial en el A23~~ — HECHO en v1.9.2 (§4.1).
- Tocar el contenido de las hojas existentes. Esto **solo agrega** una hoja.

---

## 9. Punto abierto (no bloquea) — RESUELTO

**Version.** Se resolvio por **`1.8.3`** (`Z++`): no es un modulo/reporte nuevo, asi
que no gastaba el `Y`. El `1.9.0` termino yendo a la capa de catalogos DEIS
(CLAUDE.md §14), y el bump de la familia poblacion quedo en **1.10.0**.
