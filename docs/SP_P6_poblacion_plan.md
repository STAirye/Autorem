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
- `P6_A1` — grilla para llevar al SP, respetando la máscara de celdas bloqueadas (§5.0).
- `P6_Detalle` — auditable, 1 fila por persona con las banderas que la hicieron
  tributar a cada fila del P6.
- **`P6_Revisar` — excepciones que requieren decisión humana (§5.5).** Hoja
  obligatoria del módulo, no un extra.

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

### 4.4 El Inscritos es un snapshot, pero los SP/SA anteriores existen

`Estado`, `Situación`, `Motivo/Fecha Pasivación` del Inscritos son al día de la
descarga: **no se puede reconstruir desde cero quién estaba Activo hace 3 meses.**

Ahora bien, **los SP y SA de cada mes se guardan aparte**, así que los meses
anteriores sí se rescatan sin problema. Consecuencias:

- Para el **delta P(m) − P(m−1) del A05** (fase 4) basta con el SP guardado del mes
  anterior: el `CALCULADOR A05` trabaja sobre la matriz agregada (dx × edad × sexo),
  que es justamente lo que el SP contiene. **No es un bloqueador.**
- Archivar `PSM_Poblacion` cada mes sigue valiendo la pena, pero por otra razón: da
  el **detalle por RUN** que el SP agregado no tiene. Sirve para auditar el delta,
  para identificar nominalmente el residual «abandono» de la parte O, y para resolver
  las excepciones de `P6_Revisar` mirando el mes anterior. Es una mejora, no un
  requisito de arranque.

### 4.5 Escribir 0, nunca celda vacía

El control de errores del SP (cols CN..CX) cuenta como **error** una celda de
demografía vacía cuando el total de la fila es > 0. El módulo escribe ceros.

Ojo con `AV` «Plan de Cuidado Integral»: no tiene fuente, pero **tampoco va vacía** —
se llena por una regla operativa explícita. Ver §5.4.2.

### 4.6 Alcance

Solo **sección A.1** (filas 13–58). Fuera: A.2 rehabilitación tipo I/II, A.3
acompañamiento psicosocial, y toda la sección B (especialidades, filas 75–126).

### 4.7 Gestante = control prenatal con matrona en 3 meses *(decidido)*

**Definición operativa adoptada:** `rem_utils.gestante_runs()` con ventana de
**3 meses cerrados terminando en el mes reportado** — **fuente única para SA y SP**.
Se descarta replicar el DAX del PowerBI.

**Por qué es un proxy y no un registro:** *no existe un registro en tiempo real de
gestación que tribute al REM*. Existe en la ficha clínica, y todo el punto de esta
herramienta es **no abrir la ficha**. Entonces se infiere: si tuvo control prenatal,
está embarazada.

**Por qué se filtra por matrona:** el control prenatal **lo hace únicamente matrona
o matrón**, ningún otro estamento. El filtro no excluye casos, los **precisa**.

Divergencias contra el PowerBI (esperadas, documentadas, no son bugs del port):

| | PowerBI (DAX) | autoREM (adoptado) |
|---|---|---|
| Ventana | `EOMONTH(-3)+1 … EOMONTH(-1)` = **2 meses** (off-by-one; para 3 sería `-4`) | **3 meses** cerrados hasta el mes reportado |
| «Matrón» | `CONTAINSSTRING(…,"matron")` **no matchea** «Matrón»: DAX ignora mayúsculas pero **no acentos** → pierde a los matrones | `norm()` quita acentos → **captura Matrona y Matrón** |
| Anclaje | `TODAY()` | corte del mes reportado (§4.1) |

Limitación aceptada por diseño: no verifica que el embarazo siga en curso. Quien
parió dentro de la ventana sigue marcada; quien está embarazada con su último
control fuera de la ventana no aparece. Sin abrir la ficha no hay alternativa, y la
ventana de 3 meses es justamente la tolerancia elegida (el control prenatal es
~mensual: 3 meses absorben una inasistencia sin arrastrar puérperas demasiado).

Sin costo de input: el P6 ya carga 12 meses de ADA para `Activo 12m` (§3.1); la
ventana de gestante es un subconjunto.

Aplica además el filtro por **sexo registral femenino** de §5.4.1.

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

### 5.0 La hoja está PROTEGIDA y la máscara es información clínica

`ws.protection.sheet = True`. Pegar un bloque rectangular 13→58 × F..AX **falla con
error de celdas protegidas** — es el problema reportado. Las celdas bloqueadas dentro
de la zona de captura no son arbitrarias: **codifican restricciones etarias y
demográficas por fila.**

| Fila(s) | Bloqueado dentro de F..AX | Qué significa |
|---|---|---|
| **14** | **F..AX completa** | es la cabecera «FACTORES DE RIESGO» → **es la que rompe el pegado de un bloque corrido** |
| 22, 23 Suicidio | F, G | no aplica banda 0-4 años |
| 28 Depresión post parto | todas las de hombres + 0-9 + 60+ + AN, AP, AR, AX | **solo mujeres de 10 a 59 años** |
| 37 Ansiedad de separación | 15-19 en adelante + AO | **solo 0-14 años** |
| 38 Otros trastornos infancia | 20-24 en adelante + AO | **solo 0-19 años** |
| 35, 36 TDAH / disocial | AO | no aplica «madre de hijo < 5» |
| 44-46 Demencias | AN, AO, AT, AU | no aplica gestante / madre<5 / SENAME / Mejor Niñez |
| todas | C, D, E | son fórmulas (§5) |

Dos consecuencias de diseño:

1. **La máscara es un validador clínico gratis.** Si el cálculo produce un número
   donde la plantilla bloquea (ansiedad de separación en alguien de 40, TDAH en una
   madre de hijo <5, demencia en una gestante, suicidio en un menor de 5, depresión
   post parto en un hombre), **eso es un error de datos**, no un dato. No se escribe:
   va a `P6_Revisar` con el RUN y el motivo.
2. **La salida `P6_A1` debe replicar la máscara** (hueco donde la plantilla bloquea)
   y venir partida en **bloques pegables** — rectángulos maximales sin celdas
   bloqueadas, saltando la fila 14. Ver §5.6 para la alternativa que evita el
   copy-paste por completo.

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

### 5.2 Unidad de conteo por bloque de filas — EXPLÍCITO

Cada bloque del P6·A.1 cuenta una cosa distinta. **No son sumables entre sí y las
diferencias son intencionales, no errores:**

| Filas | Unidad de conteo | Relación |
|---|---|---|
| **15–23** | **Factores de riesgo.** Una persona puede tributar a varias filas (víctima de violencia física *y* psicológica *y* con ideación suicida). **Se cuentan doble a propósito.** | suma ≫ personas |
| **24** | **Pacientes, globalmente.** `DISTINCTCOUNT(RUN)` con los filtros del P6. Una persona = 1, tenga los diagnósticos que tenga. **Excepción: la columna `AV` (PIC) sí se suma por diagnóstico** — §5.4.2. | — |
| **25–58** | **Por diagnóstico, según el FORMULARIO.** Una persona con depresión + ansiedad + TDAH tributa a 3 filas. | suma > fila 24 (esperado) |
| **13** | **Suma literal de las filas 15 a 24** *(decidido)*. Hereda el doble conteo de los factores de riesgo. | — |

**Sanity checks que el módulo emite en el log** (avisos, no errores):
- `suma(25..58) > fila 24` → esperado; si NO se cumple, algo está mal.
- `fila 24` fuera del rango histórico ~1300-1500 → aviso ruidoso.
- `fila 13` vs el `DISTINCTCOUNT(RUN)` real de «tiene FR o dx»: se reporta la
  diferencia (= magnitud del doble conteo de FR) para tenerla a la vista, sin
  cambiar lo que se pega.

### 5.3 Fobia social: el port resuelve un pendiente upstream

El `CONTEXTO_REM_general` lista «Fobia social: no está en el reporte PBI, se sacaba
por descarte» como pendiente. **En Python deja de ser un problema:** leemos
`43.- TIPO DE TRASTORNO DE ANSIEDAD` directo del formulario y `OVERRIDE_SUBTIPO[43]`
ya separa Pánico / Fobia social / Generalizada / TEPT / Otros (con el orden PÁNICO
antes que FOBIA por «agoraFOBIA»). La fila 41 sale calculada, no por descarte.

### 5.4 Demografía `AN..AX`

**Principio (lo confirma el propio control de errores del SP):** el P6 tabula todo
por **sexo registral**, no por género. Las fórmulas de validación son
`AN, AO ≤ E (Mujeres)` · `AP, AR ≤ D (Hombres)` · `AQ, AS ≤ E (Mujeres)` ·
`AT, AU, AV ≤ C (Ambos)`. El género aparece **solo** en AW/AX (TRANS).

| Col | Concepto | Fuente | Ya existe |
|---|---|---|---|
| AN | Gestantes — **solo sexo registral femenino** | `¿Embarazada?` — matrona + prenatal/formulario gestante | `rem_utils.gestante_runs()` · **def. abierta §6.0** |
| AO | Madre de hijo < 5 años — **solo sexo registral femenino** (§5.4.1) | pregunta 1 del formulario | `DEMOGRAFIA` en `rem_saludmental` |
| AP/AQ | Pueblos originarios H/M | `¿Originario o Migrante?` = Originario | `rem_utils.PUEBLO_VACIO` |
| AR/AS | Migrantes H/M | `¿Originario o Migrante?` = Migrante | idem |
| AT | SENAME | `PROTECCION NIÑEZ` = «SENAME» (alerta ⊃ SENAME) | `marcar_demografia()` |
| AU | Mejor Niñez | `PROTECCION NIÑEZ` = «Mejor Niñez» (alerta ⊃ SPE) | idem |
| AV | Plan de Cuidado Integral Elaborado | **MANUAL — no hay fuente** (§5.4.2) | — |
| AW/AX | TRANS Masculino / Femenino | `Trans` = 1, split por género | `rem_utils.trans_map()` |

⚠ **Foot-gun de AW/AX:** el control de errores compara `AW ≤ E (Mujeres)` y
`AX ≤ D (Hombres)`. O sea «TRANS Masculino» = **sexo registral mujer**, género
masculino. Las etiquetas se invierten respecto del sexo registral; `trans_map()` ya
hace ese split, hay que respetar la orientación al escribir.

#### 5.4.1 «Madre de hijo menor de 5 años» (AO) — filtrar por SEXO, no por género

La pregunta 1 del formulario **a veces se marca en hombres**. Regla:

```
AO  =  pregunta 1 == "SI"   AND   sexo registral == Mujer
```

- **Sexo registral masculino marcado → NO cuenta, por definición.** Es un error de
  registro en RAYEN: se descarta el flag y **la persona va a `P6_Revisar`** para que
  alguien lo corrija en la ficha.
- **Sexo registral femenino + género transmasculino → SÍ cuenta.** El filtro es por
  **sexo**, no por género: un hombre trans puede ser madre de un hijo menor de 5.

Lo mismo aplica a AN (gestantes): sexo registral femenino, independiente del género.

#### 5.4.2 `AV` «Plan de Cuidado Integral» (PIC) — sin fuente, con regla operativa

**No tiene reporte, ni formulario, ni ninguna otra fuente** en RAYEN/IRIS hoy. No es
`SM Pauta llenada (12m)` ni ninguna otra columna del PowerBI: el dato **no existe**
en ningún sistema consultable. Es la última casilla del P6·A.1 sin automatizar.

**Regla vigente (WIP declarado del autor, sep-2026):** se reporta el PIC solo donde
es **obligatorio**, y ahí se asume completo —

```
AV(fila) = total de la fila     si la fila es GES-obligatoria o factor de riesgo
AV(fila) = 0                    en el resto
```

| Filas | PIC | Motivo |
|---|---|---|
| 15–23 | = total de la fila | factores de riesgo |
| **24** | **= SUMA(AV 25:58)** | **excepción, ver abajo** |
| 25, 26, 27 (depresión leve/moderada/grave) | = total de la fila | GES depresión |
| 44, 45, 46 (demencias / Alzheimer) | = total de la fila | GES Alzheimer |
| resto | 0 | — |
| 13 | = SUMA(AV 15:24) | regla general de la fila 13 (§5.2) |

**Excepción de la fila 24 (importante):** en el resto de la fila 24 cada celda es un
`DISTINCTCOUNT(RUN)` — una persona cuenta una vez tenga los diagnósticos que tenga
(§5.2). **`AV` es la única celda de la fila 24 que NO es un distinct:** se acumula
por diagnóstico, `AV24 = SUMA(AV25:AV58)`. Con la regla WIP eso se reduce a
`AV25+AV26+AV27 + AV44+AV45+AV46`.

Sanity check que el módulo emite: si `AV24 > C24` hay comorbilidad
depresión + demencia sumándose dos veces, y **el control de errores del SP lo va a
marcar** (`AV ≤ C`). Es raro pero posible → aviso en el log con los RUN implicados
para resolverlo a mano.

**Esto es un placeholder por obligación de reporte, no un conteo real de planes
elaborados.** El módulo lo implementa como regla explícita y configurable (una
constante con el set de filas, no repartida por el código), y **el log lo declara en
cada corrida**: «AV PIC llenado por regla WIP = total de fila en GES + factores de
riesgo; no es un conteo de planes reales». Fail loud (§CLAUDE.md): un número
asumido, pero nunca un número asumido y callado.

Si algún día aparece una fuente (formulario nuevo, alerta administrativa), esto pasa
a ser una línea de config y se automatiza como el resto.

*Pendiente de precisar (§6):* si «las depresiones varias» incluye la fila 28
(depresión post parto), y si hay otras filas GES que hoy queden fuera de la regla
(esquizofrenia primer episodio, consumo perjudicial en menores de 20).

⚠ **Hallazgo colateral (fuera del alcance de este plan):** hoy
`rem_saludmental.DEMOGRAFIA["Madre_menor5"]` es solo `pregunta 1 == "SI"`, **sin
filtro de sexo** → la columna `Madre_menor5` del **A05 egresos/ingresos** sobrecuenta
a los hombres mal marcados. Es un fix aparte de este módulo; conviene extraer la
regla a una función compartida para que A05, SA y SP usen la misma.

### 5.5 Hoja `P6_Revisar` — excepciones para decisión humana

**La plantilla del REM es binaria (Hombres / Mujeres) y RAYEN reporta personas no
binarias.** Eso no tiene solución automática correcta: asignar por sexo registral
sería inventar el dato, y descartar la fila perdería a la persona. **Va a revisión
manual, siempre.**

Esa es la razón de ser de la hoja, pero no el único contenido. `P6_Revisar` junta
**todo lo que requiere criterio humano antes de pegar al SP**, con RUN, la fila del
P6 afectada y el motivo:

| Motivo | Origen |
|---|---|
| **Sexo/género no binario** — no cae en columna H ni M | `Sexo` / `Género` fuera de {Hombre, Mujer} |
| **`Sexo = "No informado"`** — el propio DAX lo genera cuando el Inscritos viene vacío | §Ferrada[Sexo] |
| **Hombre marcado como «madre de hijo < 5»** — flag descartado, hay que corregir la ficha en RAYEN | §5.4.1 |
| **Número en celda bloqueada** — ansiedad de separación en adulto, TDAH en madre<5, demencia en gestante/SENAME, suicidio en 0-4, depresión post parto en hombre o fuera de 10-59 | máscara §5.0 |
| **Egresos por «Otras Causas»** — abandono vs clínica, manual por diseño | `rem_a05_o_egresos` / §CLAUDE.md §7 |
| **Egreso multi-dx divergente** — casos donde el PowerBI habría marcado Egresado todos los dx y el port marca solo uno | §4.3 |
| **Identificador no-RUT** (DNI, pasaporte) | `Tipo de identificación` ≠ RUT → el CONTEXTO manda eliminar la fila; acá se lista antes de eliminarla |
| **Edad sin fecha de nacimiento** — cayó al fallback `Inscritos[EDAD AÑOS]` | §Ferrada[Edad] |
| **Fecha de formulario ilegible** | `mes_de_celda()` devolvió None |
| **Fila 13 vs distinct** — magnitud del doble conteo de FR | §5.2 |
| **Delta negativo** contra el mes anterior (reingresos, inconsistencias) | fase 4, cuando exista |

Diseño: una sola hoja, columnas `RUN · Motivo · Fila_P6 · Detalle · Valor_crudo`,
ordenada por motivo. **Fail loud** (§CLAUDE.md): si la hoja trae filas, el log lo
grita con el conteo por motivo; nunca un número plausible y callado.

### 5.6 Cómo llega el resultado al SP — *(pendiente de decidir)*

El copy-paste choca con la protección de hoja (§5.0). Dos caminos:

- **A — bloques pegables.** `P6_A1` sale partida en rectángulos maximales sin celdas
  bloqueadas (saltando la fila 14, la 28, los recortes etarios de 22/23/37/38 y las
  columnas AN/AO/AT/AU de 44-46). Son ~10 bloques: seguro, pero tedioso de pegar.
- **B — escribir directo en una copia del `SP_26_V1.1.xlsm`.** openpyxl escribe en
  celdas bloqueadas sin problema (la protección es de UI, no del archivo). Salida:
  `SP_26_2026_MM_P6.xlsm` ya llenado, cero pegado. Requiere `keep_vba=True` y
  **verificar que no rompa las macros ni las validaciones** del template MINSAL —
  ese es el riesgo a probar antes de comprometerse.

---

## 6. Puntos abiertos

> La definición de **Gestante** era el bloqueante de esta sección; quedó cerrada
> en **§4.7** (3 meses, matrona, fuente única SA/SP).


1. **Fila 57 Epilepsia** — no está en el formulario SM ni en el PBI, y
   `EXCLUIR_PATOLOGIA={75,77,79,81}` la saca del A05 por ser del REM adulto. ¿Queda
   manual, o hay otra fuente?
2. **Alcance exacto de la regla PIC (§5.4.2)** — «las depresiones varias»: ¿entra la
   fila 28 (depresión post parto)? ¿Y hay otras filas GES que hoy queden fuera
   (esquizofrenia primer episodio, consumo perjudicial en < 20 años)?
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
