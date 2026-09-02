<!--
This document was generated with the assistance of Claude Opus 5 (Anthropic).
The human author reviewed, modified, and integrated the content.
Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# Config por diagnóstico — SP·P6 A.1 (FASE 0, para revisar)

> **Estado: PARA REVISIÓN.** Extraída **mecánicamente** de las 28 fórmulas `(form)`
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

**Una sola excepción real** (fila resaltada en la tabla B): `SM Abuso Sexual (form)`
**no filtra por instrumento**. Todas las demás sí.

---

## Tabla A — Diagnósticos → filas 25-58 del P6

`dx` y `ESTADO` son números de pregunta del formulario. Todas filtran
`INSTRUMENTO ⊃ médico` salvo donde se indique.

| Fila P6 | Concepto (P6) | Columna | dx | ESTADO | Texto de la pregunta dx |
|---|---|---|---|---|---|
| **25-27** | Depresión leve / moderada / grave | `Depresión (form)` + gravedad | 18 | 19 | ¿TIENE DEPRESIÓN? |
| 28 | Depresión post parto *(solo mujeres 10-59)* | `Depresión Postparto (form)` | 21 | 22 | ¿TIENE DEPRESIÓN POST-PARTO? |
| 29 | Trastorno bipolar | `Bipolaridad (form)` | 23 | 24 | ¿TIENE TRANSTORNO BIPOLAR? *(typo de RAYEN)* |
| 30 | Consumo perjudicial de alcohol | `OH Perjudical (form)` | 31 | 32 | CONSUMO PERJUDICIAL DE ALCOHOL |
| 31 | Consumo dependiente de alcohol | `OH Dependiente (form)` | 33 | 34 | CONSUMO DEPENDIENTE DEL ALCOHOL |
| 32 | Consumo perjudicial de drogas | `Drogas Perjudical (form)` | 35 | 36 | CONSUMO PERJUDICIAL DE DROGAS |
| 33 | Consumo dependiente de drogas | `Drogas Dependiente (form)` | 37 | 38 | CONSUMO DEPENDIENTE DE DROGAS |
| 34 | Consumo de drogas y alcohol | `OH y Drogas (form)` | 39 | 40 | CONSUMO DE DROGAS Y ALCOHOL |
| 35 | Trastorno hipercinético (TDAH) | `TDAH (form)` | 57 | 58 | ¿TIENE TRASTORNOS HIPERCINÉTICOS…? |
| 36 | Disocial desafiante y oposicionista | `Oposicionista desafiante (form)` | 69 | 70 | ¿TIENE TRASTORNO DISOCIAL DESAFIANTE Y OPOSICIONISTA? |
| 37 | Ansiedad de separación *(solo 0-14)* | `Ansiedad separación (form)` | 71 | 72 | ¿TIENE TRASTORNO DE ANSIEDAD DE SEPARACIÓN EN LA INFANCIA? |
| 38 | Otros comportamiento/emociones infancia *(solo 0-19)* | `Otras Infancia/Adolescencia (form)` | 73 | 74 | ¿TIENE OTROS TRASTORNOS DEL COMPORTAMIENTO Y DE LAS…? |
| **39-43** | Ansiedad: TEPT / pánico / fobia social / TAG / otros | `Ansiedad (form)` + tipo | 41 | **42** | ¿TIENE TRASTORNO DE ANSIEDAD? |
| **44-46** | Demencias leve / moderado / avanzado | `Demencia (form)` + etapa | 44 | **46** | ¿TIENE ALZHEIMER Y/O OTRAS DEMENCIAS? |
| 47 | Esquizofrenia | `Esquizofrenia (form)` | 51 | 52 | ¿TIENE ESQUIZOFRENIA? |
| 48 | Trastorno adaptativo | `Adaptativo (form)` | 49 | 50 | ¿TIENE TRASTORNO ADAPTATIVO? |
| 49 | Conducta alimentaria | `Conducta Alimentaria (form)` | 55 | 56 | ¿TIENE TRASTORNO DE LA CONDUCTA ALIMENTARIA? |
| 50 | Retraso mental | `Retraso Mental (form)` | 59 | 60 | ¿TIENE RETRASO MENTAL? |
| 51 | Trastorno de personalidad | `Personalidad (form)` | 61 | 62 | ¿TIENE TRASTORNO DE PERSONALIDAD? |
| 52 | TGD · Autismo | `Autismo (form)` | 83 | 84 | ¿TIENE AUTISMO? |
| 53 | TGD · Asperger | `Asperger (form)` | 85 | 86 | ¿TIENE ASPERGER? |
| 54 | TGD · Síndrome de Rett | `Rett (form)` | 87 | 88 | ¿TIENE SÍNDROME DE RETT? |
| 55 | TGD · Desintegrativo de la infancia | `Desintegrativo niñez (form)` | 89 | 90 | ¿TIENE TRASTORNO DESINTEGRATIVO DE LA INFANCIA? |
| **56** | TGD · no especificado | ⚠ **`TGD (form)` usa la 63, NO la 91** | 63 | 64 | ver **anomalía A1** |
| 57 | Epilepsia | — | — | — | **NO SE REPORTA** (no es del programa SM) |
| 58 | Otras | `Otras (form)` | 65 | 66 | OTRAS (TRASTORNOS NO INCLUIDOS EN SECCIÓN) |

---

## Tabla B — Factores de riesgo → filas 15-23 del P6

| Fila P6 | Concepto (P6) | Columna | dx | ESTADO | Subtipo | Instrumento |
|---|---|---|---|---|---|---|
| **15-20** | Violencia física/sexual/psicológica × víctima/agresor | `Violencia (form)` | 4 | **5** | **6** (tipo) × **7** (en la violencia es) | médico |
| **17-18** | Violencia sexual *(también entra por acá)* | `Abuso Sexual (form)` | 9 | 10 | — | 🔴 **SIN filtro de instrumento** |
| 21 | Abuso sexual | — | — | — | — | **no capturable** en la plantilla → 0 |
| **22-23** | Suicidio: ideación / intento *(sin banda 0-4)* | `Suicidio (form)` | 11 | **13** | **12** (tipo) | médico |

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

## Anomalías y puntos a confirmar

### 🔴 A1 — La fila 56 del P6 se está llenando con la pregunta equivocada

El formulario tiene **dos** preguntas de TGD:

| Nº | Texto |
|---|---|
| 63 | ¿TIENE TRASTORNO GENERALIZADO DEL DESARROLLO? *(genérica, el «padre» de las 83-91)* |
| **91** | ¿TIENE TRASTORNO GENERALIZADO DEL DESARROLLO **DE LA…**? *(= «no especificado»)* |

La fila 56 del P6 es **«Trastorno generalizado del desarrollo no específico»** → debería
salir de la **91**. Pero `SM TGD (form)` usa la **63**, y **la 91 no tiene NINGUNA
columna en todo el PowerBI** (verificado: cero referencias a `PSM[91` en el spec).

**A decidir:**
- **a)** Fila 56 ← pregunta **91** (el port corrige el error), y la 63 se descarta.
- **b)** Fila 56 ← pregunta 91, y la 63 se usa como **fallback**: cuenta solo si el
  paciente no tiene ninguna de las específicas (83/85/87/89/91) marcada.
- **c)** Dejarlo como está (63) para cuadrar con el PowerBI.

*(Recomiendo (b): recupera el dato que hoy se pierde y evita doble conteo con 52-55.)*

### 🔴 A2 — `Abuso Sexual (form)` no filtra por instrumento

Es la **única** de las 28 que no exige `INSTRUMENTO ⊃ médico`. ¿Es intencional
(cualquier profesional puede registrar abuso sexual) o es un olvido del DAX?
Cambia quién entra a las filas 17/18.

### 🟡 A3 — El filtro es «médico», no «médica»

`CONTAINSSTRING(INSTRUMENTO, "médico")`. Si el instrumento se llamara «Consulta
Médica» o similar, **no matchearía**. En Python conviene `norm() ⊃ "MEDIC"` para
cubrir médico/médica/medicina. ¿Hay algún instrumento con esa forma?

### 🟡 A4 — Preguntas del formulario que quedan sin usar

| Nº | Pregunta | Destino |
|---|---|---|
| 2 | Adolescentes derivados de espacios amigables | fuera de alcance |
| 3 | Fecha próximo control | no lo usa el P6 |
| 14-17 | Plan ambulatorio básico / intervención preventiva / breve / terapéutica | ¿alguna tributa a otra casilla? |
| 25, 27, 29 | Depresión refractaria / grave con psicosis / alto riesgo suicida | **sección B** (especialidades), fuera del A.1 |
| 47, 53, 67 | Psicosis / primer episodio esquizofrenia / conductuales asociados a demencia | **no se cuentan** (psiquiatría hospitalaria o COSAM) ✔ decidido |
| 75 | Epilepsia | **no se reporta** ✔ decidido |
| 77, 79, 81 | Programa rehabilitación I / II / acompañamiento psicosocial | secciones **A.2 y A.3**, fuera de alcance |
| 91 | TGD no especificado | **ver A1** |

### 🟡 A5 — Confirmar que el ESTADO de suicidio y demencia es el correcto

Son los dos casos con layout `[dx][SUBTIPO][ESTADO]` en vez de `[dx][ESTADO][SUBTIPO]`:
**Suicidio 11 → ESTADO 13** (12 = tipo) y **Demencia 44 → ESTADO 46** (45 = etapa).
Coincide con lo que ya hace `rem_saludmental.encontrar_diagnostico()` y con
`DIAGNOSTICOS_CON_SUBTIPO`. Solo confirmar que se lee igual en el formulario real.
