<!--
This document was generated with the assistance of Claude Opus 5 (Anthropic).
The human author reviewed, modified, and integrated the content.
Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# Plan — REM SP·P6 A.1 «Población en control PSM» (módulo nuevo, → 1.9.0)

> **Estado: PLAN aprobado, sin implementar.** Decisiones de diseño cerradas con el
> autor (sep-2026). Reemplaza en alcance a la nota `A05_poblacion_psm_plan.md`, que
> sigue vigente para la fase posterior (delta P → A05 N/O).

## 0. Objetivo en una línea

Reemplazar el paso manual «abrir el PowerBI → filtrar → exportar → pivotear» por:
**exports crudos → tabla intermedia por-paciente (la «Ferrada» en Python) → tabla
copy-paste al `SP_26_V1.1.xlsm` hoja P6, sección A.1.**

---

## 1. Fuente de verdad: los specs del PowerBI

`refs tablas/specs/Salud_Mental_spec.md` (generado con la skill `pbip-spec`) trae el
**DAX completo de las ~150 columnas calculadas** de la tabla `Ferrada`, más los 31
visuales de la página. El visual **#17 «Población PSM» (`tableEx`)** es exactamente
la tabla que hoy se exporta a mano; sus nombres de columna de salida están en el
header de `refs tablas/poblacion sm powerbi.xlsx`.

**Hallazgo estructural:** `Ferrada` **no es una tabla de Salud Mental**. Es la tabla
base por-paciente que usan las 8 páginas del PowerBI (Cardiovascular 335 referencias,
ECICEP 240, Dependencia 176, Respiratorio 130, Georreferenciación 191, Preventivos
111, A23 108, Salud Mental 340). Portarla es infraestructura transversal, no un
detalle del P6 → **vive en `programas/`, no dentro del módulo.**

---

## 2. Arquitectura (3 capas)

```
Informe Inscritos ──┐
Formulario SM (hist)├─► programas/poblacion.py ──► tabla «Ferrada» (1 fila por RUN)
ADA (12 meses) ─────┘                                        │
                                                             ▼
                              modulos/rem_sp_p6_poblacion.py ──► P6·A.1 + detalle
```

| Capa | Archivo | Rol |
|---|---|---|
| Base | `programas/poblacion.py` | Construye la tabla por-RUN desde los 3 exports. Port 1:1 del DAX de `Ferrada` (con el corte parametrizado, §4). Reusable por Cardiovascular / Dependencia / ECICEP / A23. |
| Config clínica | `programas/rem_saludmental.py` (existente) | **Fuente única** del mapa Nº-de-pregunta → diagnóstico → subtipo (`OVERRIDE_PATOLOGIA`, `DIAGNOSTICOS_CON_SUBTIPO`, `OVERRIDE_SUBTIPO`). Ya validado contra SP·P6. **Se reusa la config, NO el recorrido `marcar_eventos` (openpyxl fila-a-fila).** |
| Tarea | `modulos/rem_sp_p6_poblacion.py` | Filtra, agrupa por banda etaria × sexo, arma demografía y escribe las hojas. |

**Motor:** pandas. Un PSM histórico son decenas de miles de filas × 129 columnas; el
walker openpyxl del A05 es correcto para un mes, no para el histórico.

**Salida (`escribir()`):**
- `PSM_Poblacion` — la tabla intermedia, con los **mismos nombres de columna del
  export PowerBI** para poder diffear. Es también el snapshot mensual archivable (§4.4).
- `P6_A1` — grilla copy-paste a la hoja P6 del SP.
- `P6_Detalle` — auditable, 1 fila por persona con las banderas que la hicieron
  tributar a cada fila del P6.

---

## 3. Inputs (3, no 5)

| # | Export | Ventana | Obligatorio |
|---|---|---|---|
| 1 | **Informe Inscritos / Adscritos** (IRIS) | snapshot actual | sí |
| 2 | **Formulario «Control de Salud Mental»** (IRIS) | **histórico completo** | sí |
| 3 | **ATENCIONESDIAGNOSTICOSACTIVIDADES (ADA)** | **12 meses** (acepta LISTA de archivos, como el A23) | sí |
| — | Recetas Vigentes / Recetas Externas | — | **no** (§3.1) |

### 3.1 Por qué el ADA no necesita el histórico completo

El ADA entra al DAX en tres lugares:
1. `SM Activo 12m` — actividades SM en los 12 meses cerrados → **12 meses**.
2. `¿Embarazada?` — matrona + control prenatal/formulario gestante → **3 meses**.
3. `_Atenciones` por CIE-10 (F32/F33/F43…) — **sin filtro de fecha** en el DAX.

El (3) alimenta únicamente las columnas de diagnóstico **sin** `(form)`
(`SM Depresión`, `SM Ansiedad`…), y esas solo alimentan `Pertenece a PSM`. El P6
filtra por `Ingresado = SI`, que depende **exclusivamente de las columnas `(form)`**,
y `Ingresado=SI ⟹ Pertenece=SI`. **Conclusión: el histórico completo del ADA no
cambia ni un número del P6.** Solo haría falta para un diff celda-a-celda exacto
contra el PowerBI.

### 3.2 Alcance de la tabla intermedia: SLIM (decidido)

Se portan las columnas que el P6 necesita, **con los nombres del export PowerBI**.
Quedan **fuera**:
- las 21 columnas de fármacos (`Sertralina`, `Quetiapina`, `Diazepam`… y sus `(Ext)`)
  → requieren 2 exports más y **no tributan a ninguna casilla del REM**;
- `¿Receta Vigente?` (misma razón);
- las columnas dx sin `(form)` que dependen del ADA histórico (§3.1). Si se quiere
  el diff exacto, se enchufan después sin rediseñar nada.

---

## 4. Decisiones de diseño

### 4.1 `TODAY()` → corte parametrizado (regla del proyecto)

Todo el DAX cuelga de `EOMONTH(TODAY(), -n)`. Se reemplaza por el **último día del
mes reportado**, igual que el A23. Traducción mecánica:

| DAX | Python (corte = último día del mes reportado) |
|---|---|
| `TODAY()` | `corte` |
| `EOMONTH(TODAY(),-1)` | `corte` |
| `EOMONTH(TODAY(),-13)+1` | primer día del mes 12 meses antes de `corte` |
| `EOMONTH(TODAY(),-2)+1 … EOMONTH(TODAY(),-1)` | el mes reportado completo |
| `Ferrada[Edad]` (`DATEDIFF(nac, TODAY())/365.25`) | edad **al corte** |

Sin esto no se puede recalcular un mes pasado ni cuadrar el delta P(m)−P(m−1).
Nota: el PowerBI asume que se corre en el mes M+1 para reportar M; con `corte`
explícito eso deja de ser un supuesto implícito.

### 4.2 El DAX **no es uniforme** entre diagnósticos

Algunas fórmulas `(form)` filtran `CONTAINSSTRING(INSTRUMENTO,"médico")` (Depresión)
y otras no (Adaptativo); los códigos CIE-10 del bloque `_Atenciones` varían por dx.
**El core del port es una tabla de config por-dx** extraída de las 28 fórmulas
`(form)` del spec — en el estilo de `OVERRIDE_PATOLOGIA`, con revisión humana
fórmula por fórmula. Esa tabla ES el entregable de la fase 0.

### 4.3 Egreso: se corrige el bug del PowerBI *(decidido)*

En el DAX, la variable `_Egreso` de cada `X (form)` **no es específica del
diagnóstico**: busca cualquier `19.- ESTADO` con «egreso» para ese RUN en el mes y
marca «Egresado» **todas** sus columnas dx. Un egreso de depresión también lo saca
de ansiedad, demencia, etc. → la persona desaparece del P6 completo.

**Port: egreso POR DIAGNÓSTICO.** Cada dx se marca `Egresado` solo si la columna
`ESTADO` de *su propio bloque* de preguntas trae «egreso» (el bloque ya está mapeado
en `rem_saludmental`: 4→5, 18→19, 41→42, …).

⚠ Consecuencia: **la tabla intermedia deja de cuadrar 1:1 con el export PowerBI**.
Para que la diferencia sea explicable y no misteriosa, el módulo emite además una
columna de auditoría con el valor que habría dado el PowerBI y un aviso en el log
(«N personas / M diagnósticos difieren por egreso multi-dx»). Fail loud, §CLAUDE.md.

### 4.4 El Inscritos es un snapshot, no un histórico

`Estado`, `Situación`, `Motivo/Fecha Pasivación` son al día de la descarga; no se
puede reconstruir quién estaba Activo hace 3 meses. **Consecuencia operativa: la
tabla `PSM_Poblacion` hay que archivarla cada mes** — ella misma pasa a ser el
histórico que habilita el delta P(m)−P(m−1) del A05 (fase 4).

### 4.5 Escribir 0, nunca celda vacía

El control de errores del SP (cols CN..CX) cuenta como **error** una celda de
demografía vacía cuando el total de la fila es > 0. El módulo escribe ceros.

### 4.6 Alcance

Solo **sección A.1** (filas 13–58). Fuera: A.2 rehabilitación tipo I/II, A.3
acompañamiento psicosocial, y toda la sección B (especialidades, filas 75–126).

---

## 5. Layout del P6·A.1 (leído del `SP_26_V1.1.xlsm`)

- **Celdas de captura:** `F..AM` = 17 bandas etarias × (Hombres, Mujeres) —
  0-4, 5-9, 10-14, 15-19, 20-24, 25-29, 30-34, 35-39, 40-44, 45-49, 50-54, 55-59,
  60-64, 65-69, 70-74, 75-79, 80+ — y `AN..AX` = demografía.
- **`C`, `D`, `E` son fórmulas** (`=SUM(D:E)` y la suma de las bandas). No se tocan.
- **Fila 21 «Abuso sexual» NO es capturable** (sin fórmula en C/D/E) → confirma la
  regla del `CONTEXTO_REM_general`: abuso sexual se mapea a **violencia sexual**
  (filas 17/18) y la fila 21 queda en 0.
- **Fila 28 «Depresión post parto» solo tiene C y E** → sin columna de hombres.

### 5.1 Mapeo fila → columna de la tabla intermedia

Todas las filas se filtran primero por: `Estado = "Activo"` **&** `¿Activo 12m? = SI`
**&** `¿Ingresado? = SI`, y el dx correspondiente en estado `Activo`.

| Fila P6 | Concepto | Fuente |
|---|---|---|
| 13 | Nº personas en control | **suma literal de las filas 15–24** *(decidido; ver §5.2)* |
| 15/16 | Violencia física víctima/agresor | `Violencia (form)` + `Violencia Tipo (form)` ⊃ «física» + `Violencia Víctima o Agresor (form)` |
| 17/18 | Violencia sexual víctima/agresor | tipo ⊃ «sexual» **O** `Abuso Sexual (form)` = Activo |
| 19/20 | Violencia psicológica víctima/agresor | tipo ⊃ «psicol» |
| 21 | Abuso sexual | **no capturable** → 0 |
| 22/23 | Suicidio ideación/intento | `Suicidio (form)` + `Suicidio Tipo (form)` |
| 24 | Personas con diagnósticos | `DISTINCTCOUNT(RUN)` con ≥1 dx de las filas 25–58 |
| 25/26/27 | Depresión leve/moderada/grave | `Depresión (form)` + `Depresión Leve/Moderada/Grave` |
| 28 | Depresión post parto | `Depresión Postparto (form)` — solo mujeres |
| 29 | Trastorno bipolar | `Bipolaridad (form)` |
| 30–34 | OH perj./dep., drogas perj./dep., OH+drogas | `OH Perjudicial / OH Dependiente / Drogas Perjudicial / Drogas Dependiente / OH y Drogas (form)` |
| 35 | Trastorno hipercinético | `TDAH (form)` |
| 36 | Disocial desafiante y oposicionista | `Oposicionista desafiante (form)` |
| 37 | Ansiedad de separación | `Ansiedad separación (form)` |
| 38 | Otros comportamiento/emociones infancia | `Otras Infancia/Adolescencia (form)` + exclusión comodín |
| 39–43 | Ansiedad: TEPT / pánico / fobia social / TAG / otros | `Ansiedad (form)` + `43.- TIPO DE TRASTORNO DE ANSIEDAD` **(§5.3)** |
| 44–46 | Demencias leve/moderado/avanzado | `Demencia (form)` + `Demencia Leve/Moderado/Avanzado` |
| 47 | Esquizofrenia | `Esquizofrenia (form)` |
| 48 | Trastorno adaptativo | `Adaptativo (form)` + exclusión comodín |
| 49 | Conducta alimentaria | `Conducta Alimentaria (form)` |
| 50 | Retraso mental | `Retraso Mental (form)` |
| 51 | Trastorno de personalidad | `Personalidad (form)` |
| 52–56 | TGD: autismo / asperger / Rett / desintegrativo / no especificado | respectivas `(form)` |
| 57 | Epilepsia | **sin fuente** en el formulario SM ni en el PBI → manual / 0 *(abierto)* |
| 58 | Otras | `Otras (form)` |

**Exclusiones comodín** (nivel fila, antes de agregar — del `CONTEXTO_REM_general`):

| Diagnóstico | Cuenta solo si |
|---|---|
| Trastorno adaptativo (48) | `COUNT(dx Depresión→Oposicionista + Personalidad→TGD == SI) <= 1` |
| Otros trastornos de ansiedad (43) | `COUNT(dx Depresión→Otras Infancia + Demencia→TGD == SI) == 0` |
| Otros infancia/adolescencia (38) | `COUNT(dx Depresión→Asperger + Rett→TGD == SI) <= 2` |

### 5.2 Fila 13 = suma literal de 15–24 *(decidido)*

Se replica el procedimiento del autor. **Doble-cuenta** a quien tiene factor de
riesgo y diagnóstico a la vez (violencia + depresión es lo habitual), así que el
módulo calcula además el `DISTINCTCOUNT(RUN)` real y **avisa en el log** cuando la
suma lo excede, con la magnitud de la diferencia. Se pega la suma; el aviso queda
para revisar con el referente si algún mes se dispara.

### 5.3 Fobia social: el port resuelve un pendiente upstream

El `CONTEXTO_REM_general` lista «Fobia social: no está en el reporte PBI, se sacaba
por descarte» como pendiente. **En Python deja de ser un problema:** leemos
`43.- TIPO DE TRASTORNO DE ANSIEDAD` directo del formulario y `OVERRIDE_SUBTIPO[43]`
ya separa Pánico / Fobia social / Generalizada / TEPT / Otros (con el orden PÁNICO
antes que FOBIA por «agoraFOBIA»). La fila 41 sale calculada, no por descarte.

### 5.4 Demografía `AN..AX`

| Col | Concepto | Fuente | Ya existe |
|---|---|---|---|
| AN | Gestantes (solo mujeres) | `¿Embarazada?` — matrona + prenatal/formulario gestante, 3 meses | `rem_utils.gestante_runs()` |
| AO | Madre de hijo < 5 años | pregunta 1 del formulario | `DEMOGRAFIA` en `rem_saludmental` |
| AP/AQ | Pueblos originarios H/M | `¿Originario o Migrante?` = Originario | `rem_utils.PUEBLO_VACIO` |
| AR/AS | Migrantes H/M | `¿Originario o Migrante?` = Migrante | idem |
| AT | SENAME | `PROTECCION NIÑEZ` = «SENAME» (alerta ⊃ SENAME) | `marcar_demografia()` |
| AU | Mejor Niñez | `PROTECCION NIÑEZ` = «Mejor Niñez» (alerta ⊃ SPE) | idem |
| AV | Plan Cuidado Integral Elaborado | `Pauta llenada (12m)` — **a confirmar** *(abierto)* | — |
| AW/AX | TRANS Masculino / Femenino | `Trans` = 1, split por género | `rem_utils.trans_map()` |

⚠ **Foot-gun de AW/AX:** el control de errores compara `AW ≤ E (Mujeres)` y
`AX ≤ D (Hombres)`. O sea «TRANS Masculino» = **sexo registral mujer**, género
masculino. Las etiquetas se invierten respecto del sexo registral; `trans_map()` ya
hace ese split, hay que respetar la orientación al escribir.

---

## 6. Puntos abiertos (no bloquean el arranque)

1. **Fila 57 Epilepsia** — no está en el formulario SM ni en el PBI, y
   `EXCLUIR_PATOLOGIA={75,77,79,81}` la saca del A05 por ser del REM adulto. ¿Queda
   manual, o hay otra fuente?
2. **Col AV «Plan Cuidado Integral Elaborado»** — ¿es `SM Pauta llenada (12m)`?
3. **Diagnósticos del formulario sin fila en A.1:** Psicosis (47), Primer episodio
   de esquizofrenia (53), Trastornos conductuales asociados a demencia (67),
   Depresión refractaria / grave con psicosis / alto riesgo suicida (25/27/29 — esas
   tres sí tienen fila, pero en la sección **B** de especialidades). ¿Caen todas en
   «Otras» (fila 58) o se descartan?
4. **`SM TGD` es «(mixto)»** en el PBI: el formulario tiene una pregunta 63 genérica
   («Trastorno generalizado del desarrollo») además de las 83–91 específicas.
   Verificar que no haya doble conteo entre la fila 56 y las 52–55.
5. **`Bipolaridad (dg)` vs `(form)`** — pacientes legacy solo con `(dg)`; el PBI solo
   cuenta `(form)` y subestima levemente. Ya aceptado en el CONTEXTO; se mantiene.

---

## 7. Fases

| Fase | Entregable | Validación |
|---|---|---|
| **0** | Tabla de config por-dx extraída de las 28 fórmulas `(form)` del spec (§4.2), revisada fórmula por fórmula con el autor. | Revisión humana. |
| **1** | `programas/poblacion.py` + hoja `PSM_Poblacion`. | **Diff por RUN contra el export PowerBI real del mismo mes.** Las únicas diferencias esperadas son las del §4.3 (egreso por dx), y salen listadas en el log. |
| **2** | `modulos/rem_sp_p6_poblacion.py` + hojas `P6_A1` y `P6_Detalle`. | Contra un **P6 llenado a mano de un mes ya cerrado**, casilla por casilla (como se validó el SM Actividades vs jul-2026). Sanity check del plan: total de fila 24 siempre ~1300-1500. |
| **3** | Pestaña en la GUI + tests (`tests/test_sp_p6.py`) + bump a **1.9.0** (Y++, módulo nuevo) + fila en la matriz de programas de CLAUDE.md. | Suite completa verde. |
| **4** *(después)* | Delta P(m) − P(m−1) → A05 N/O. | Ver `docs/A05_poblacion_psm_plan.md`; portar la lógica del `CALCULADOR A05 DESDE P 2.1 junio.xlsx`, no reinventarla. |
