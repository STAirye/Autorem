<!--
This document was generated with the assistance of Claude Opus 5 (Anthropic).
The human author reviewed, modified, and integrated the content.
Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# Config por diagnóstico — SP·P6 A.1 (FASE 0)

> **Estado: REVISADA Y APROBADA** por el autor (sep-2026). Extraída **mecánicamente** de las 28 fórmulas `(form)`
> de `refs tablas/specs/Salud_Mental_spec.md` (parseo del DAX, no lectura a ojo) y
> cruzada con los 92 encabezados de pregunta del export IRIS real
> (`refs tablas/Formularios_RAYEN csm IRis.xlsx`) y con el layout del `SP_26_V1.1.xlsm`.
> Al aprobarse, esta tabla se convierte en la constante de `programas/poblacion.py`.
> Plan general: [SP_P6_poblacion_plan.md](SP_P6_poblacion_plan.md).

## Reglas generales aplicadas (del autor)

1. **Diagnóstico SIN subtipo → se usa `xxx (form)`** (el estado Activo / Egresado).
2. **Diagnóstico CON subtipo (depresión, ansiedad, alzheimer) → se usa cada subtipo**,
   no la fila genérica.
3. Solo columnas `(form)`. Las `(fecha)` son variables intermedias y las `(mixto)`/`(dg)`
   están deprecated (§3.2 del plan).
4. Filtro base común a todas: `Estado = Activo` **&** `¿Activo 12m? = SI` **&**
   `¿Ingresado? = SI`.

## El DAX es UNIFORME (corrección)

En el plan yo había dicho que «el DAX no es uniforme entre diagnósticos». **Falso.**
El parseo muestra que **las 28 fórmulas `(form)` siguen exactamente el mismo patrón**:

```
último formulario del RUN donde:
    INSTRUMENTO ⊃ "médico"
    &  pregunta_dx ⊃ "si"
    &  pregunta_ESTADO ⊃ "ingreso" | "seguimien"
→ "Activo"        (y "Egresado" si hubo egreso en el mes; ver §4.3 del plan)
```

La única variación en el DAX es que `SM Abuso Sexual (form)` **no filtra por
instrumento** y todas las demás sí. **Pero eso está al revés de lo correcto:** ver
la decisión **D2**, que le quita el filtro a los factores de riesgo.

**Patrón final del port** (tras las decisiones de abajo):

```
último formulario del RUN donde:
    [INSTRUMENTO ⊃ "MEDIC"]        ← solo para DIAGNÓSTICOS; los FR no filtran
    &  pregunta_dx ⊃ "si"
    &  pregunta_ESTADO ⊃ "ingreso" | "seguimien"
→ "Activo"        (y "Egresado" si hubo egreso en el mes; ver §4.3 del plan)
```

---

## Tabla A — Diagnósticos → filas 25-58 del P6

`dx` y `ESTADO` son números de pregunta del formulario. **Todas** filtran
`INSTRUMENTO ⊃ MEDIC` (D3) — a diferencia de los factores de riesgo (tabla B).

| Fila P6 | Concepto (P6) | Columna | dx | ESTADO | Texto de la pregunta dx |
|---|---|---|---|---|---|
| **25-27** | Depresión leve / moderada / grave *(+ las 25/27/29 caen en la 27, D4)* | `Depresión (form)` + gravedad | 18 | 19 | ¿TIENE DEPRESIÓN? |
| 28 | Depresión post parto *(mujeres 10-59; ≥60 se **pliega** a 55-59)* | `Depresión Postparto (form)` | 21 | 22 | ¿TIENE DEPRESIÓN POST-PARTO? |
| 29 | Trastorno bipolar | `Bipolaridad (form)` | 23 | 24 | ¿TIENE TRANSTORNO BIPOLAR? *(typo de RAYEN)* |
| 30 | Consumo perjudicial de alcohol | `OH Perjudical (form)` | 31 | 32 | CONSUMO PERJUDICIAL DE ALCOHOL |
| 31 | Consumo dependiente de alcohol | `OH Dependiente (form)` | 33 | 34 | CONSUMO DEPENDIENTE DEL ALCOHOL |
| 32 | Consumo perjudicial de drogas | `Drogas Perjudical (form)` | 35 | 36 | CONSUMO PERJUDICIAL DE DROGAS |
| 33 | Consumo dependiente de drogas | `Drogas Dependiente (form)` | 37 | 38 | CONSUMO DEPENDIENTE DE DROGAS |
| 34 | Consumo de drogas y alcohol | `OH y Drogas (form)` | 39 | 40 | CONSUMO DE DROGAS Y ALCOHOL |
| 35 | Trastorno hipercinético (TDAH) *(**sin recorte etario en el SP**; el tope 0-24 es del SA·A05, §5.0.1)* | `TDAH (form)` | 57 | 58 | ¿TIENE TRASTORNOS HIPERCINÉTICOS…? |
| 36 | Disocial desafiante y oposicionista | `Oposicionista desafiante (form)` | 69 | 70 | ¿TIENE TRASTORNO DISOCIAL DESAFIANTE Y OPOSICIONISTA? |
| 37 | Ansiedad de separación *(0-14; ≥15 se **pliega** a 10-14)* | `Ansiedad separación (form)` | 71 | 72 | ¿TIENE TRASTORNO DE ANSIEDAD DE SEPARACIÓN EN LA INFANCIA? |
| 38 | Otros comportamiento/emociones infancia *(0-24; ≥25 se **pliega** a 20-24)* | `Otras Infancia/Adolescencia (form)` | 73 | 74 | ¿TIENE OTROS TRASTORNOS DEL COMPORTAMIENTO Y DE LAS…? |
| **39-43** | Ansiedad: TEPT / pánico / fobia social / TAG / otros | `Ansiedad (form)` + tipo | 41 | **42** | ¿TIENE TRASTORNO DE ANSIEDAD? |
| **44-46** | Demencias leve / moderado / avanzado *(solo CON etapa, D5)* | `Demencia (form)` + etapa | 44 | **46** | ¿TIENE ALZHEIMER Y/O OTRAS DEMENCIAS? |
| 47 | Esquizofrenia | `Esquizofrenia (form)` | 51 | 52 | ¿TIENE ESQUIZOFRENIA? |
| 48 | Trastorno adaptativo | `Adaptativo (form)` | 49 | 50 | ¿TIENE TRASTORNO ADAPTATIVO? |
| 49 | Conducta alimentaria | `Conducta Alimentaria (form)` | 55 | 56 | ¿TIENE TRASTORNO DE LA CONDUCTA ALIMENTARIA? |
| 50 | Retraso mental | `Retraso Mental (form)` | 59 | 60 | ¿TIENE RETRASO MENTAL? |
| 51 | Trastorno de personalidad | `Personalidad (form)` | 61 | 62 | ¿TIENE TRASTORNO DE PERSONALIDAD? |
| 52 | TGD · Autismo | `Autismo (form)` | 83 | 84 | ¿TIENE AUTISMO? |
| 53 | TGD · Asperger | `Asperger (form)` | 85 | 86 | ¿TIENE ASPERGER? |
| 54 | TGD · Síndrome de Rett | `Rett (form)` | 87 | 88 | ¿TIENE SÍNDROME DE RETT? |
| 55 | TGD · Desintegrativo de la infancia | `Desintegrativo niñez (form)` | 89 | 90 | ¿TIENE TRASTORNO DESINTEGRATIVO DE LA INFANCIA? |
| **56** | TGD · no especificado | **pregunta 91**, con la 63 de fallback (**D1**) | **91** | 92 | ¿TIENE TRASTORNO GENERALIZADO DEL DESARROLLO DE LA…? |
| 57 | Epilepsia | — | — | — | **NO SE REPORTA** (no es del programa SM) |
| 58 | Otras | `Otras (form)` | 65 | 66 | OTRAS (TRASTORNOS NO INCLUIDOS EN SECCIÓN) |

---

## Tabla B — Factores de riesgo → filas 15-23 del P6

**NINGUNO filtra por instrumento** (decisión **D2**): un factor de riesgo lo puede
registrar cualquier estamento, no solo médico.

| Fila P6 | Concepto (P6) | Columna | dx | ESTADO | Subtipo | Instrumento |
|---|---|---|---|---|---|---|
| **15-20** | Violencia física/sexual/psicológica × víctima/agresor | `Violencia (form)` | 4 | **5** | **6** (tipo) × **7** (en la violencia es) | **quitar** (el DAX lo tiene) |
| **17-18** | Violencia sexual *(también entra por acá)* | `Abuso Sexual (form)` | 9 | 10 | — | ninguno (el DAX ya estaba bien) |
| 21 | Abuso sexual | — | — | — | — | **no capturable** en la plantilla → 0 |
| **22-23** | Suicidio: ideación / intento *(0-4 se **pliega** a 5-9)* | `Suicidio (form)` | 11 | **13** | **12** (tipo) | **quitar** (el DAX lo tiene) |

**Regla de violencia sexual** (del `CONTEXTO_REM_general`): `Abuso Sexual (form)` **+**
`Violencia Tipo (form) ⊃ "sexual"` van **ambos** a las filas 17/18. La fila 21 queda en 0.

---

## Tabla C — Subtipos (los 5 dx con desglose)

| Pregunta | Header RAYEN | Valor contiene → | Fila P6 |
|---|---|---|---|
| **20** | TIPO DE DEPRESIÓN | `leve` | 25 |
| | | `moderad` | 26 |
| | | `grave` | 27 |
| **43** | TIPO DE TRASTORNO DE ANSIEDAD | `traumatico` / `TEPT` / `estres` | 39 (TEPT) |
| | | `panico` | 40 |
| | | `fobia` *(el DAX usa `sociales`)* | 41 |
| | | `generaliz` | 42 |
| | | `otros` | 43 |
| **45** | ETAPA *(de Alzheimer/demencias)* | `leve` | 44 |
| | | `moderad` | 45 |
| | | `avanza` | 46 |
| **6** | TIPO DE VIOLENCIA | `fisica` / `sexual` / `psicol` | 15-16 / 17-18 / 19-20 |
| **7** | EN LA VIOLENCIA ES | víctima / agresor | columna dentro del par |
| **12** | TIPO DE SUICIDIO | `ideacion` / `intento` | 22 / 23 |

**Ojo con el orden de evaluación en la 43:** en `rem_saludmental.OVERRIDE_SUBTIPO[43]`
hay que evaluar **PÁNICO antes que FOBIA**, porque «Pánico sin **agoraFOBIA**» matchea
las dos. Ya está resuelto ahí y se reusa tal cual; el DAX lo evita por otra vía
(matchea `sociales` en vez de `fobia`).

**Género de los adjetivos:** el DAX usa `moderada` para depresión y `moderado` para
demencia. En Python se usa **`moderad`** para ambos y el problema desaparece.

---

## Decisiones (revisadas y cerradas — sep-2026)

### D1 — Fila 56: se corrige a la pregunta 91, con la 63 como fallback

El formulario tiene **dos** preguntas de TGD:

| Nº | Texto |
|---|---|
| 63 | ¿TIENE TRASTORNO GENERALIZADO DEL DESARROLLO? *(genérica, el «padre» de las 83-91)* |
| **91** | ¿TIENE TRASTORNO GENERALIZADO DEL DESARROLLO **DE LA…**? *(= «no especificado»)* |

La fila 56 del P6 es «TGD no específico» → le corresponde la **91**. El DAX usa la
**63**, y la 91 **no tiene ninguna columna en todo el PowerBI** (cero referencias a
`PSM[91` en el spec).

**Decidido — opción (b):**

```
fila 56  =  pregunta 91 activa
         O  pregunta 63 activa Y ninguna de {83, 85, 87, 89, 91} activa   ← fallback
```

Recupera el dato que hoy se pierde y evita doble conteo con las filas 52-55.

> **Acción upstream del autor:** corregir también el DAX del PowerBI (agregar la
> columna de la 91). Mientras no se haga, este es un punto de divergencia esperado
> entre el port y el export del PowerBI.

### D2 — Los FACTORES DE RIESGO no filtran por estamento

**Contraintuitivo pero es la regla:** ningún factor de riesgo debe filtrar por
instrumento. Un episodio de violencia o de suicidio lo puede registrar cualquier
estamento, no solo médico.

| Columna | El DAX hoy | Correcto |
|---|---|---|
| `Violencia (form)` (4/5) | filtra `médico` | **sin filtro** |
| `Suicidio (form)` (11/13) | filtra `médico` | **sin filtro** |
| `Abuso Sexual (form)` (9/10) | sin filtro | ya estaba bien |

O sea: la excepción del DAX (Abuso Sexual) era la única **correcta**, y las otras dos
son las que están mal. **Efecto esperado: suben las filas 15-20 y 22-23.** El log
reporta cuántos registros entran por esta vía que el PowerBI no contaba, para que la
diferencia sea explicable.

Los **diagnósticos** (filas 25-58) **sí** mantienen el filtro de instrumento.

### D3 — El filtro de instrumento se generaliza a `MEDIC`

El DAX usa el literal `"médico"`. Se porta como `norm(INSTRUMENTO) ⊃ "MEDIC"`, que
cubre médico / médica / medicina. Hoy el instrumento solo existe en masculino, así
que no cambia ningún número: es **a prueba de futuro** por si RAYEN agrega una
variante. Además `norm()` hace el match insensible a tildes, cosa que el DAX no.

### D4 — Preguntas del formulario que no van al P6·A.1

| Nº | Pregunta | Destino |
|---|---|---|
| 2 | Adolescentes derivados de espacios amigables | **todo 0** — no hay espacios amigables, por ahora |
| 3 | Fecha próximo control | no se usa |
| 14-17 | Plan ambulatorio básico · intervención preventiva / breve / terapéutica | **COSAM**, no APS |
| **25, 27, 29** | Depresión refractaria · grave con psicosis · con alto riesgo suicida | **nadie debería usarlas**, pero si vienen marcadas → **suman a la fila 27 (Depresión grave)** y el RUN va a `P6_Revisar` |
| 47, 53, 67 | Psicosis · primer episodio esquizofrenia · conductuales asociados a demencia | no se cuentan (psiquiatría hospitalaria o COSAM) |
| 75 | Epilepsia | no se reporta (no es del programa SM) |
| 77, 79, 81 | Programa rehabilitación I / II · acompañamiento psicosocial | secciones **A.2 y A.3**, fuera de alcance |
| 91 | TGD no especificado | **fila 56** — ver D1 |

### D5 — Subtipo vacío: NO tributa, y va a revisión

Confirmado el layout de los dos casos invertidos: **Suicidio 11 → ESTADO 13** (12 =
tipo) y **Demencia 44 → ESTADO 46** (45 = etapa).

Y la regla que se desprende de cómo se reporta hoy:

> **Las demencias se reportan SOLO si tienen ETAPA.** No hay fila «demencia sin
> especificar» en el P6: si la pregunta 45 viene vacía, la persona **no tributa a
> ninguna** de las filas 44-46.

Se generaliza a los tres dx con subtipo: **si el dx está Activo pero su subtipo viene
vacío, no tributa a ninguna fila** —

| dx | subtipo | Si el subtipo está vacío |
|---|---|---|
| Depresión (18) | 20 · TIPO DE DEPRESIÓN | no entra a 25/26/27 |
| Ansiedad (41) | 43 · TIPO DE ANSIEDAD | no entra a 39-43 |
| Demencia (44) | 45 · ETAPA | no entra a 44/45/46 |
| Violencia (4) | 6 · TIPO + 7 · víctima/agresor | no entra a 15-20 |
| Suicidio (11) | 12 · TIPO | no entra a 22/23 |

**Esos casos van a `P6_Revisar`** con motivo «dx activo sin subtipo registrado»: es
población en control que se está perdiendo por un campo sin llenar, y el REM lo
subcuenta en silencio si nadie avisa. Reusa el mecanismo `Falta_Subtipo` /
`AVISAR_ALTA_SIN_SUBTIPO` que el A05 ya tiene.
