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
ADA (13 meses) ─────┘                                        │
                                     ┌───────────────────────┴────────────────┐
                                     ▼                                        ▼
              modulos/rem_sp_p6_poblacion.py           modulos/rem_sm_rescate_inasistentes.py
                 → P6·A.1 + detalle (REM)                  → rescate 6m/13m (NO tributa, §8)
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
- **`Revisar_Administrativo` + `Revisar_Clinico` — excepciones que requieren decisión
  humana, partidas por tipo (§5.5).** Hojas obligatorias del módulo, no un extra.

---

## 3. Inputs (3, no 5)

| # | Export | Ventana | Obligatorio |
|---|---|---|---|
| **1** | **Formulario «Control de Salud Mental»** (IRIS) | **histórico completo** | sí |
| **2** | **ATENCIONESDIAGNOSTICOSACTIVIDADES (ADA)** | **13 meses** (acepta LISTA de archivos, como el A23) | sí |
| **3** | **Informe Inscritos / Adscritos** (IRIS) — *«Inscritos y Adscritos», NO «archivo Excel» a secas* | snapshot actual | sí |
| — | Recetas Vigentes / Recetas Externas | — | **no** (§3.1) |

**Ese orden (1 Formulario · 2 ADA · 3 Inscritos) es el que debe mostrar la GUI**, tanto
en las instrucciones como en los selectores de carga — decidido así por el autor
(no 1 Inscritos, como quedó escrito acá por error una versión anterior). Cada slot se
rotula con el **nombre del reporte tal como se descarga**, nunca «archivo Excel»: el
usuario baja todo desde RAYEN/IRIS con nombres parecidos y necesita saber cuál va en
cada casilla.

### 3.1 Por qué el ADA no necesita el histórico completo

El ADA entra al DAX en cuatro lugares:
1. `SM Activo 12m` — actividades SM en los 12 meses cerrados → **12 meses**.
2. `¿Embarazada?` — matrona + control prenatal/formulario gestante → **3 meses**.
3. `SM Atendido hace 13m` — el mes que acaba de salir de la ventana → **13 meses** (§8).
4. `_Atenciones` por CIE-10 (F32/F33/F43…) — **sin filtro de fecha** en el DAX.

El (4) alimenta únicamente las columnas de diagnóstico **sin** `(form)`
(`SM Depresión`, `SM Ansiedad`…), y esas solo alimentan `Pertenece a PSM`. El P6
filtra por `Ingresado = SI`, que depende **exclusivamente de las columnas `(form)`**,
y `Ingresado=SI ⟹ Pertenece=SI`. **Conclusión: el histórico completo del ADA no
cambia ni un número del P6.** Solo haría falta para un diff celda-a-celda exacto
contra el PowerBI.

### 3.2 Alcance de la tabla intermedia: SLIM (decidido)

**El DAX tiene MUCHA columna redundante para el cálculo final.** De las ~150 de
`Ferrada`, el P6 necesita ~55. Se portan esas, **con los nombres del export
PowerBI** para poder diffear.

**Regla de oro (decidida):** se usan **solo las columnas `(form)`**. Las `(fecha)` y
las `(mixto)`/`(dg)` **no se emiten**.

| Qué se omite | Cuántas | Por qué |
|---|---|---|
| Todas las `(fecha)` — `Depresión (fecha)`, `Ansiedad (fecha)`… | ~28 | Son **variables intermedias** del DAX (el `LASTDATE` que alimenta a su `(form)`), no resultados. Se calculan en memoria y se descartan. |
| Todas las `(mixto)` / `(dg)` — `SM TGD`, `SM Desintegrativo niñez`, `Bipolaridad (dg)`, `Retraso Mental (dg)` | ~6 | **Deprecated, no se usan actualmente.** |
| Las dx **sin** `(form)` — `SM Depresión`, `SM Ansiedad`… | ~24 | Solo alimentan `Pertenece a PSM`, que es implicado por `¿Ingresado?` (§3.1). |
| `Pertenece a PSM` | (ver abajo) | Se creía redundante por `Ingresado ⟹ Pertenece`. **FALSO, ver §3.3** — se emite en dos versiones. |
| Los 21 fármacos + `¿Receta Vigente?` | 22 | Requieren 2 exports más y **no tributan a ninguna casilla del REM**. |
| `SM Pauta llenada`, `SM último control (fecha)/(instrumento)`, `PAD Es cuidador?` | 4 | El P6·A.1 no tiene ninguna casilla que los consuma. |
| **`Nombre completo`, `Nombre Social`, `Fecha Nacimiento`, `Dirección Completa`, `Celular`, `Mail`, `Tipo de identificación`** | 7 | **Privacidad (§8 CLAUDE.md), no solo economía.** El export PowerBI arrastra nombre, dirección, teléfono y correo; **el P6 no necesita ninguno**. El RUN basta para trazar. Menos PII en circulación. |

Se conservan aunque el A.1 no los use:
- `Estado`, `Motivo Pasivación`, `Fecha Pasivación` → los necesita el delta P→A05 de
  la fase 4 (traslados y fallecidos);
- `Sector`, `SM Atendido hace 6m`, `SM Atendido hace 13m` → los necesita el **reporte
  de rescate de inasistentes** (§8).

Si algún día se quiere el diff celda-a-celda contra el PowerBI, las omitidas se
enchufan sin rediseñar nada.

### 3.3 `Ingresado ⟹ Pertenece` es FALSO — el DAX de Pertenece tiene un hueco

**Corrección a §3.1/§3.2** (detectada sep-2026 al comparar la cascada de filtros).
Yo había justificado descartar `Pertenece a PSM` diciendo que `Ingresado = SI` implica
`Pertenece = SI`. **No se cumple.** El DAX de `Pertenece` lista **24** columnas y el
de `Ingresado` usa **28**. Las cuatro que faltan:

```
Ingresado tiene:  OH Perjudicial · OH Dependiente · Drogas Perjudicial · Drogas Dependiente
Pertenece tiene:  solo el agregado "OH y Drogas"
```

El DAX además mezcla columnas con y sin `(form)` sin criterio aparente
(`SM Violencia` sin form, `SM Suicidio (form)` con form…). No hay lógica interna.

**Consecuencia práctica:** el reporte «Población SM» del PowerBI trae `Pertenece` como
**prefiltro de página**. Quien queda `Ingresado=SI` únicamente por «consumo perjudicial
de alcohol» (o cualquiera de esas 4) **cae FUERA del export del PowerBI pero DENTRO de
autoREM**. Es parte de la brecha del comparativo de agosto.

**Se emiten las DOS versiones** en `PSM_Poblacion`, y ambas salen en la cascada del log:

| Columna | Qué es |
|---|---|
| `¿Pertenece? (24 DAX)` | replica el hueco del PowerBI — sirve para comparar contra su prefiltro |
| `¿Pertenece? (28 real)` | la que corresponde: las mismas 28 que usa `Ingresado` |

Ninguna de las dos **filtra** nada: son informativas. Detalles de implementación:

- **Base formulario, sin CIE-10.** El DAX de las columnas sin `(form)` mira además los
  códigos CIE-10 del ADA histórico; replicarlo sería lentísimo y **el objetivo es
  comparar, no reproducir el número exacto**.
- **Cuentan Activo Y Egresado** (el DAX usa `<> "NO"`), que es lo que se necesita en
  el reporte.

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

### 4.2 El DAX SÍ es uniforme *(corregido tras el parseo — fase 0)*

Yo había escrito acá que «el DAX no es uniforme entre diagnósticos». **Es falso.**
El parseo mecánico de las 28 fórmulas `(form)` muestra que **todas siguen el mismo
patrón** (último formulario con `INSTRUMENTO ⊃ médico` + pregunta dx ⊃ «si» +
ESTADO ⊃ ingreso/seguimiento), con **una sola excepción**: `SM Abuso Sexual (form)`
no filtra por instrumento.

Eso simplifica el port: **una función parametrizada por (pregunta_dx, pregunta_estado,
filtra_instrumento)** y una tabla de datos, en vez de 28 casos especiales.

La tabla está extraída y lista para revisión en
**[SP_P6_config_por_dx.md](SP_P6_config_por_dx.md)** — entregable de la fase 0, con
5 anomalías anotadas (la más relevante: la fila 56 del P6 se llena hoy con la
pregunta 63 cuando le corresponde la 91, que no tiene columna en el PowerBI).

### 4.3 Egreso: se corrige el bug del PowerBI *(decidido)*

En el DAX, la variable `_Egreso` de cada `X (form)` **no es específica del
diagnóstico**: busca cualquier `19.- ESTADO` con «egreso» para ese RUN en el mes y
marca «Egresado» **todas** sus columnas dx. Un egreso de depresión también lo saca
de ansiedad, demencia, etc. → la persona desaparece del P6 completo.

**Port: egreso POR DIAGNÓSTICO.** Cada dx se marca `Egresado` solo si la columna
`ESTADO` de *su propio bloque* de preguntas trae «egreso» (el bloque ya está mapeado
en `rem_saludmental`: 4→5, 18→19, 41→42, …).

Consecuencia: **la tabla intermedia deja de cuadrar 1:1 con el export PowerBI**.
Para que la diferencia sea explicable y no misteriosa, el módulo emite la hoja
**`Egreso_Divergencias`** y un aviso en el log. Fail loud, §CLAUDE.md.

**La hoja lleva los RUN, no solo el conteo.** Un «N personas × diagnóstico difieren»
no sirve para revisar nada: hay que poder ir a la ficha. Formato = **tabla anidada por
diagnóstico** (una sección por dx, igual que las listas sectorizadas de §8):

```
Depresión (form)                                    3 personas
    RUN            Port        PowerBI
    11111111-1     Activo      Egresado
    …
Ansiedad (form)                                     1 persona
    RUN            Port        PowerBI
    …
```

Columnas por fila: `RUN · Valor_port · Valor_PowerBI`. Sin datos de contacto (§8.4).

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
| 38 Otros trastornos infancia | 25-29 en adelante + AO | **solo 0-24 años** |
| 35, 36 TDAH / disocial | AO | no aplica «madre de hijo < 5» |
| 44-46 Demencias | AN, AO, AT, AU | no aplica gestante / madre<5 / SENAME / Mejor Niñez |
| todas | C, D, E | son fórmulas (§5) |

Tres consecuencias de diseño:

1. **Los recortes ETARIOS se PLIEGAN, no se descartan** (§5.0.1). Es la regla más
   importante de esta sección y la más fácil de equivocar.
2. **Los recortes DEMOGRÁFICOS sí son un validador.** Un número en AN/AO/AT/AU donde
   la plantilla bloquea (TDAH en una madre de hijo <5, demencia en una gestante o en
   SENAME) no tiene dónde plegarse: **es un error de datos**. No se escribe y va a
   `P6_Revisar` con el RUN y el motivo.
3. **La salida `P6_A1` replica la máscara** (hueco donde la plantilla bloquea) y viene
   partida en **bloques pegables** — rectángulos maximales sin celdas bloqueadas,
   saltando la fila 14 (§5.6).

#### 5.0.1 Rangos etarios recortados: se PLIEGAN al rango reportable más cercano

**El SP y el SA·A05 N/O recortan rangos etarios en filas DISTINTAS.** Un paciente
fuera del rango de su fila no tiene celda donde caer — y **si se descarta, desaparece
del REM**. La práctica del autor (hoy manual) es **sumarlo al último rango etario
reportable de esa fila**, y eso es lo que hay que automatizar en cada planilla.

**Recortes del SP·P6 A.1** — leídos de la máscara de protección del `.xlsm`:

> **Regla de implementación: la máscara se EXTRAE del archivo, no se transcribe.**
> `ws.cell(f, c).protection.locked` sobre las 46 filas de la sección A.1, comparadas
> una por una. Esta tabla es documentación; **la fuente de verdad es el archivo**.
> No es teórico: transcribir a mano ya metió un error acá (la fila 38 abre hasta
> 20-24, no hasta 15-19 — detectado al extraerla mecánicamente, sep-2026).

| Fila P6 | Rango reportable | Fuera de rango → se pliega a |
|---|---|---|
| 37 Ansiedad de separación | 0-14 | ≥15 → **banda 10-14** |
| 38 Otros trastornos infancia | **0-24** | ≥25 → **banda 20-24** |
| 28 Depresión post parto | mujeres 10-59 | ≥60 → **banda 55-59** |
| 22-23 Suicidio | 5 y más | 0-4 → **banda 5-9** *(único recorte por el extremo inferior; a confirmar)* |
| **35 TDAH** | **0-80+ — SIN recorte** | **no se pliega nada** ver abajo |

**Recortes del SA·A05 N/O** (`SA_26_V1.2.xlsm`, secciones N ingresos y su gemela de
egresos) — es **donde el plegado pesa más**:

| Fila SA (N / O) | Concepto | Rango reportable | Se pliega a |
|---|---|---|---|
| **218 / 270** | **Trastorno hipercinético (TDAH)** | **0-24** | ≥25 → **banda 20-24** |
| 219 / 271 | Disocial desafiante y oposicionista | 0-24 | ≥25 → banda 20-24 |
| 220 / 272 | Ansiedad de separación en la infancia | 0-24 | ≥25 → banda 20-24 |

> **TDAH es el caso más significativo**, y va **al revés** de lo intuitivo: en el
> **SP no hay tope** (el adulto con TDAH se cuenta en su banda real), pero en el
> **SA·A05 sí** (se pliega a 20-24). **No plegar TDAH en el P6.**

> **Dato desactualizado en `CONTEXTO_REM_general`:** dice «edad ≥30 → forzar bucket
> **25-29** en el SA». En `SA_26_V1.2` la columna 25-29 (P/Q) está **bloqueada**: el
> último rango reportable es **20-24** (F..O). La plantilla MINSAL cambió. Usar 20-24.

**Todos los plegados se listan igual en `P6_Revisar`** — con RUN, edad real, fila y
banda de destino. El número entra al REM (que es lo correcto), pero queda la
trazabilidad de que esa persona se contó en una banda que no es la suya.

**Impacto en la fase 4 (delta P → A05 N/O):** como SA y SP recortan filas distintas,
el delta **no va a cuadrar banda por banda** en las filas recortadas — TDAH sobre todo.
Hay que conciliar a nivel de fila (total), no de celda, o aplicar el truncamiento de
cada planilla por separado antes de comparar. Anotarlo **antes** de perseguir un
descuadre que no es un error.

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
| 38 | Otros comportamiento/emociones infancia | `Otras Infancia/Adolescencia (form)` |
| 39–43 | Ansiedad: TEPT / pánico / fobia social / TAG / otros | `Ansiedad (form)` + `43.- TIPO DE TRASTORNO DE ANSIEDAD` **(§5.3)** |
| 44–46 | Demencias leve/moderado/avanzado | `Demencia (form)` + `Demencia Leve/Moderado/Avanzado` |
| 47 | Esquizofrenia | `Esquizofrenia (form)` |
| 48 | Trastorno adaptativo | `Adaptativo (form)` |
| 49 | Conducta alimentaria | `Conducta Alimentaria (form)` |
| 50 | Retraso mental | `Retraso Mental (form)` |
| 51 | Trastorno de personalidad | `Personalidad (form)` |
| 52–56 | TGD: autismo / asperger / Rett / desintegrativo / no especificado | respectivas `(form)` |
| 57 | Epilepsia | **NO SE REPORTA** — no es del programa de salud mental *(decidido)*. Coherente con `EXCLUIR_PATOLOGIA` del A05. |
| 58 | Otras | `Otras (form)` |

**Diagnósticos del formulario que NO se cuentan** *(decidido)* — son de psiquiatría
hospitalaria o COSAM, no de APS, así que no tributan al P6·A.1:

| Nº pregunta | Diagnóstico |
|---|---|
| 47 | Psicosis |
| 53 | Primer episodio de esquizofrenia |
| 67 | Trastornos conductuales asociados a demencia |

No van a «Otras» (fila 58): se **descartan**. Ojo con no confundir la **pregunta 51**
(Esquizofrenia, que **sí** cuenta y va a la fila 47 del P6) con la **pregunta 53**
(primer episodio, que no).

**Exclusiones comodín — ELIMINADAS** *(decidido sep-2026, validado contra el REM
manual de agosto)*. El `CONTEXTO_REM_general` las traía del CALCULADOR original: las
filas cajón de sastre (38, 43, 48) solo tributaban si la persona no acumulaba
demasiados diagnósticos específicos. **Ya no se aplican** — el autor las sacó de su
metodología manual del P6, y el módulo tampoco las aplica. Las tres filas tributan
igual que cualquier otro diagnóstico.

**Por qué se sacaron:** el filtro con umbral 0 de la fila 43 («otros trastornos de
ansiedad») excluía a **~199 personas** que en el REM manual sí cuentan — era la
diferencia más grande del comparativo de agosto (autoREM 228 vs manual 427). El resto
de las filas cajón de sastre movían poco, pero por coherencia se remueve el mecanismo
completo, no caso por caso.

Reglas retiradas (se dejan documentadas por si algún día MINSAL las reintroduce):

| Diagnóstico | Regla retirada |
|---|---|
| Trastorno adaptativo (48) | contaba solo si ≤1 otro dx de {25-36, 51-56} |
| Otros trastornos de ansiedad (43) | contaba solo si 0 otros dx de {25-38, 44-56} |
| Otros infancia/adolescencia (38) | contaba solo si ≤2 otros dx de {25-53, 54-56} |

> Consecuencia en `Revisar_Clinico`: **desaparece el motivo «Excluido por
> comorbilidad»** (§5.5). Nadie se saca ya por esta vía.

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

**Foot-gun de AW/AX:** el control de errores compara `AW ≤ E (Mujeres)` y
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
| 25, 26, 27, **28** (depresión leve/moderada/grave **y post parto**) | = total de la fila | GES depresión |
| 44, 45, 46 (demencias / Alzheimer) | = total de la fila | GES Alzheimer |
| resto | 0 | — |
| 13 | = SUMA(AV 15:24) | regla general de la fila 13 (§5.2) |

**No entran otras GES** *(decidido)*: esquizofrenia y consumo perjudicial en menores
de 20 son GES, pero se atienden en **psiquiatría hospitalaria o COSAM**, no en APS →
fuera de la regla del PIC.

**Excepción de la fila 24 (importante):** en el resto de la fila 24 cada celda es un
`DISTINCTCOUNT(RUN)` — una persona cuenta una vez tenga los diagnósticos que tenga
(§5.2). **`AV` es la única celda de la fila 24 que NO es un distinct:** se acumula
por diagnóstico, `AV24 = SUMA(AV25:AV58)`. Con la regla WIP eso se reduce a
`AV25+AV26+AV27 + AV44+AV45+AV46`.

**`AV24` va a REVISIÓN MANUAL** *(decidido)*. Si `AV24 > C24` hay comorbilidad
depresión + demencia sumándose dos veces, y el control de errores del SP lo marca
(`AV ≤ C`). En teoría el **GES demencia tiene primacía** sobre el de depresión, pero
**la primacía NO se aplica automáticamente**: los RUN con ambas GES se listan en
`P6_Revisar` para que se decidan a mano. La regla clínica queda anotada como ayuda a
quien revise, no como lógica del código.

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

**Hallazgo colateral (fuera del alcance de este plan):** hoy
`rem_saludmental.DEMOGRAFIA["Madre_menor5"]` es solo `pregunta 1 == "SI"`, **sin
filtro de sexo** → la columna `Madre_menor5` del **A05 egresos/ingresos** sobrecuenta
a los hombres mal marcados. Es un fix aparte de este módulo; conviene extraer la
regla a una función compartida para que A05, SA y SP usen la misma.

### 5.5 Hoja `P6_Revisar` — excepciones para decisión humana

**La plantilla del REM es binaria (Hombres / Mujeres) y RAYEN reporta personas no
binarias.** Eso no tiene solución automática correcta: asignar por sexo registral
sería inventar el dato, y descartar la fila perdería a la persona. **Va a revisión
manual, siempre.**

Esa es la razón de ser de la hoja, pero no el único contenido. La revisión junta
**todo lo que requiere criterio humano antes de pegar al SP**, con RUN, la fila del
P6 afectada y el motivo.

**Se parte en DOS hojas** *(decidido — una sola era demasiado unwieldy)*, porque las
dos mitades las resuelven personas y momentos distintos:

- **`Revisar_Administrativo`** — problemas de **identidad y registro**. Se resuelven
  corrigiendo la ficha en RAYEN (o pidiéndoselo a SOME/admin), **sin criterio clínico**.
- **`Revisar_Clinico`** — casos que exigen **criterio clínico** para decidir si la
  persona tributa o no, y a qué fila.

Ambas: `RUN · Motivo · Fila_P6 · Detalle · Valor_crudo`, ordenadas por motivo.

#### `Revisar_Administrativo`

| Motivo | Origen |
|---|---|
| **Identificador no-RUN** (FONASA, pasaporte) | `TIPO IDENTIFICACION` no es RUN (§5.5.2) |
| **`RUN Responsable`** — RN <1 mes inscrito con el RUN de un tercero; colisión de clave | §5.5.2 |
| **Sexo/género no binario** — no cae en columna H ni M | `Sexo` / `Género` fuera de {Hombre, Mujer} |
| **`Sexo = "No informado"`** — el DAX lo genera con el Inscritos vacío | §Ferrada[Sexo] |
| **Hombre marcado como «madre de hijo < 5»** — flag descartado, corregir la ficha | §5.4.1 |
| **Número en celda demográfica bloqueada** — TDAH en madre<5, demencia en gestante/SENAME, post parto en hombre. **No se cuenta** | máscara §5.0 |
| **Edad sin fecha de nacimiento** — cayó al fallback `Inscritos[EDAD AÑOS]` | §Ferrada[Edad] |
| **Fecha de formulario ilegible** | `mes_de_celda()` devolvió None |

#### `Revisar_Clinico`

| Motivo | Origen |
|---|---|
| **Factor de riesgo SIN diagnóstico** — tiene un FR (violencia/suicidio, 15-23) pero ningún dx de trastorno mental (25-58). No debería pasar: registro incompleto → completar la ficha. Solo REPORTA, no cambia números | §5.2 (brecha fila 13 vs 24) |
| **Dx activo sin subtipo registrado** — está Activo pero el subtipo viene vacío → no tributa a ninguna fila | D5 |
| **Edad plegada** — fuera del rango etario de su fila; **se cuenta igual** en la banda de borde, con edad real y destino | §5.0.1 |
| **Egresos por «Otras Causas»** — abandono vs clínica, manual por diseño | `rem_a05_o_egresos` / §CLAUDE.md §7 |
| **Egreso multi-dx divergente** — el PowerBI habría egresado todos los dx, el port solo uno | §4.3 |
| **AV24 con comorbilidad depre+demencia** — GES a resolver a mano | §5.4.2 |
| **Fila 13 vs distinct** — magnitud del doble conteo de FR | §5.2 |
| **Delta negativo** contra el mes anterior (reingresos, inconsistencias) | fase 4, cuando exista |

> El plegado etario y la comorbilidad quedan en la hoja **clínica** aunque el número ya
> entre al REM: el revisor clínico es quien puede confirmar que el cuadro corresponde a
> esa banda/fila, o detectar un registro errado que infla un dx.

**Fail loud** (§CLAUDE.md): si cualquiera de las dos trae filas, el log grita el conteo
por motivo y por hoja; nunca un número plausible y callado. Ambas hojas se emiten
siempre (aunque vengan vacías), para que su ausencia no se confunda con «no revisé».

#### 5.5.1 Guardarraíl: un filtro que descarta demasiado es un BUG del filtro

**Lección de la primera corrida real (sep-2026).** El validador de «identificador
no-RUT» comparaba `Tipo de identificación` contra el literal `"RUT"`. El export trae
otro texto, así que **descartó las 55.331 personas del padrón** — el 100%. El módulo
no se quejó: siguió adelante y emitió un `P6_A1` lleno de ceros, que es exactamente
«un número plausible pero callado y errado».

**Regla:** todo filtro de exclusión declara un **techo esperado**. Si lo supera, es el
filtro el que está roto, no los datos → **`ArchivoInvalido` con mensaje explícito**,
nunca seguir y emitir ceros.

| Filtro | Techo razonable | Si lo supera |
|---|---|---|
| Identificador no-RUN (§5.5.2) | **5%** del padrón | error: «el validador descartó N de M personas; revisa los valores de `TIPO IDENTIFICACION`» |
| Fallecidos (§8.3) | 2% | aviso ruidoso |
| Edad ilegible / sin banda | 1% | aviso ruidoso |

#### 5.5.2 Los valores REALES de `TIPO IDENTIFICACION` (verificados sep-2026)

El export trae exactamente estos cinco. **El valor es `RUN`, no «RUT»** — de ahí que
la whitelist contra el literal `"RUT"` descartara a todo el mundo:

| Valor | ¿Entra al P6? | Por qué |
|---|---|---|
| **`RUN`** | **sí** | es el identificador válido; la inmensa mayoría del padrón |
| `Número de identificador FONASA` | no | no es RUT |
| `Número de Pasaporte` | no | no es RUT |
| `Pasaporte/Otros` | no | no es RUT |
| **`RUN Responsable`** | **no — y es el caso delicado** | ver abajo |

**`RUN Responsable` = recién nacido de menos de un mes que todavía no tiene su RUT.**
Se le inscribe con el RUN de un tercero, **habitualmente la madre**. Consecuencias:

1. **Es una COLISIÓN de clave, no un identificador inválido.** `Ferrada` es *1 fila por
   RUN*: el RN y su madre quedan con el mismo `Número`. Si la madre está en población
   SM, mezclar las dos fichas corrompe la fila.
2. **Un chequeo por FORMA no lo detecta** — el RUN de la madre tiene formato válido.

> **Corrección a §5.5.1:** dije «validar la forma del dato, no cómo se llama».
> Está incompleto. `RUN Responsable` prueba que **la etiqueta lleva información que la
> forma no tiene**. La regla correcta es **las dos cosas**:
>
> - **forma** — `^\d{6,9}-[\dkK]$` sobre `Número` normalizado → descarta FONASA y
>   pasaportes, y sobrevive a que RAYEN renombre las etiquetas;
> - **+ lista explícita de tipos que son válidos en forma pero incorrectos en
>   significado** — hoy solo `RUN Responsable`.
>
> Ninguno de los dos chequeos basta solo.

**Además: `Número` debe ser ÚNICO tras el filtro.** Assert explícito; si hay
duplicados, `ArchivoInvalido` (quedó una colisión sin resolver). Es barato y ataja
justo el modo de falla que este caso introduce.

**Por qué excluir es exactamente lo correcto (y no una pérdida):** un RN de <1 mes no
se ve por salud mental prácticamente por definición, así que el impacto numérico en el
P6 es ~0. Al descartar la fila del RN, **la fila de la madre queda intacta** — que es
la que sí importa.

> **El escenario de riesgo es concreto, no teórico.** La fila 28 del P6 es
> **depresión post parto**. La paciente con más probabilidad de tener un
> `RUN Responsable` colisionando con su ficha es justamente la que acaba de parir —
> o sea la candidata natural a un dx SM activo de esa misma fila. Resolver mal la
> colisión corrompería precisamente esa ficha. **Es el caso de test obligatorio:**
> madre con `Depresión Postparto (form) = Activo` + RN inscrito con su mismo RUN.

**El conjunto ROTA mes a mes.** El Registro Civil demora ~5 días en entregar el RUT:
llegan al control de díada (10 días) sin RUT y al control del mes ya con el suyo. O
sea los `RUN Responsable` de este mes no son los del siguiente. Consecuencias:
**no cachear ninguna lista de exclusión** (se recalcula en cada corrida), y esperar que
el conteo varíe entre meses sin que eso signifique nada.

Los cuatro tipos no-RUN juntos deberían ser un puñado de personas: si superan el techo
del 5%, salta el guardarraíl de §5.5.1.

### 5.6 Cómo llega el resultado al SP: COPY-PASTE en bloques *(decidido)*

Se descarta escribir directo en una copia del `SP_26.xlsm` (openpyxl podría hacerlo:
la protección es de UI, no del archivo). **Se mantiene el copy-paste a propósito.**

**Por qué:** el paso manual es un **control de calidad humano**. Obliga a mirar los
números antes de que entren al REM y a hacerse una idea de las magnitudes; un pipeline
que escribe solo el archivo final se puede equivocar en silencio y nadie lo nota.
Es una decisión de diseño, no una limitación técnica.

`P6_A1` sale partida en **rectángulos maximales sin celdas bloqueadas**, cada uno
rotulado con su rango destino (ej. «pegar en `F15`»). Los cortes salen de §5.0:
la fila 14, la fila 28, los recortes etarios de 22/23/37/38, y las columnas AN/AO
de 35-36 y AN/AO/AT/AU de 44-46. Son ~10 bloques.

---

## 6. Puntos abiertos

Los bloqueantes de esta sección quedaron todos cerrados (sep-2026): **Gestante**
en §4.7, **PIC / col AV** en §5.4.2, **epilepsia y diagnósticos no-APS** en §5.1,
**solo `(form)`** en §3.2, **copy-paste en bloques** en §5.6.

Queda solo un punto menor, ya aceptado y sin acción:

1. **`Bipolaridad (dg)` vs `(form)`** — hay pacientes legacy con el diagnóstico solo
   en `(dg)`. Como se usan **solo las columnas `(form)`** (§3.2), esos casos no se
   cuentan y el número queda levemente subestimado. Ya aceptado en el
   `CONTEXTO_REM_general`; se mantiene.

---

## 7. Fases

| Fase | Entregable | Validación |
|---|---|---|
| **0** | Tabla de config por-dx extraída de las 28 fórmulas `(form)` del spec (§4.2), revisada fórmula por fórmula con el autor. | Revisión humana. |
| **1** | `programas/poblacion.py` + hoja `PSM_Poblacion`. | **Diff por RUN contra el export PowerBI real del mismo mes.** Las únicas diferencias esperadas son las del §4.3 (egreso por dx), y salen listadas en el log. |
| **2** | `modulos/rem_sp_p6_poblacion.py` + hojas `P6_A1` y `P6_Detalle`. | Contra un **P6 llenado a mano de un mes ya cerrado**, casilla por casilla (como se validó el SM Actividades vs jul-2026). Sanity check del plan: total de fila 24 siempre ~1300-1500. |
| **3** | Pestaña en la GUI + tests (`tests/test_sp_p6.py`) + bump a **1.9.0** (Y++, módulo nuevo) + fila en la matriz de programas de CLAUDE.md. | Suite completa verde. |
| **3.5** | `modulos/rem_sm_rescate_inasistentes.py` — `Rescate_6m`, `Rescate_13m`, `Fallecidos_mes`, `Posibles_Traslados`, `Brecha_Medico` (§8). Recicla la tabla `Ferrada`; no toca el REM. | Revisión a ojo de las listas por sector + que ningún fallecido aparezca en el rescate. |
| **4** *(después)* | Delta P(m) − P(m−1) → A05 N/O. | Ver `docs/A05_poblacion_psm_plan.md`; portar la lógica del `CALCULADOR A05 DESDE P 2.1 junio.xlsx`, no reinventarla. |

---

## 8. Reporte adicional — Rescate de inasistentes (NO tributa al REM)

Segundo consumidor de la tabla `Ferrada`, en el mismo patrón que
`rem_sm_trabajo_perdido` respecto de `rem_sm_actividades`: **reporte operativo, no
casilla del REM**. Módulo propio, `modulos/rem_sm_rescate_inasistentes.py`, que
recicla la tabla en vez de forkearla.

**Salida: planillas SECTORIZADAS, sin datos de contacto (§8.4).**

| Hoja | Cohorte | Para qué |
|---|---|---|
| `Rescate_6m` | `SM Atendido hace 6m = Si` — su última atención SM fue hace 6 meses | dejó de asistir; rescate temprano |
| `Rescate_13m` | `SM Atendido hace 13m = Si` — tuvo atención en el mes que acaba de salir de la ventana de 12m y nada después | **se acaba de caer del programa**; rescate antes de perder el bajo-control |
| `Fallecidos_mes` | cumple criterios SM, **ya no** está Activo+Ingresado, y `Motivo Pasivación = Fallecido` con `Fecha Pasivación` en el mes reportado | **para NO llamarlos**, y para el egreso del A05 (§8.3) |
| `Posibles_Traslados` | los de las cohortes de rescate con `Motivo Pasivación` de traslado / cambio de domicilio | **no se excluyen del rescate**: se flagean para confirmar el traslado en vez de perseguir un abandono (§8.5) |
| `Brecha_Medico` | dx SM activo registrado **solo por otro estamento** | están **al debe de control médico** (§8.6) |

Cada una **agrupada por `Sector`** (una sección por sector, o una hoja por sector si
se prefiere repartirlas). Ordenadas por sector y luego por fecha de última atención.

### 8.1 Las dos definiciones del DAX NO son consistentes entre sí

| | `SM Atendido hace 6m` | `SM Atendido hace 13m` |
|---|---|---|
| Ventana | **solo el mes −6** | **solo el mes −13** |
| Actividad | `CONTAINSSTRING(ACTIVIDADES,"salud mental")` — **laxo** | **lista explícita de 7** (la misma de `Activo 12m`) |
| Condición extra | ninguna atención SM **posterior** al mes objetivo | `SM Activo 12m = "No"` |

Las **ventanas de un solo mes están bien**: es una cohorte de rescate. Si fueran
acumulativas se llamaría a la misma gente todos los meses.

**El problema es la lista de actividades.** El filtro laxo del 6m:
- **pierde las VDI** — «visita domiciliaria integral a familia con adulto mayor con
  demencia» y «…con niños/as de 5 a 9 años…» **no contienen el string «salud mental»**;
- y a la vez **captura de más**: cualquier actividad futura con «salud mental» en el
  nombre entra sin haber sido validada.

**Decidido: ambas usan la LISTA EXPLÍCITA DE 7, que es la validada** — la misma que
ya usa `Activo 12m`. Se descarta el `contains "salud mental"` laxo del DAX del 6m.

Así las tres definiciones (activo 12m, rescate 6m, rescate 13m) hablan del **mismo
universo de actividades**, y la cohorte de rescate es el complemento exacto de la
población activa en vez de un conjunto que se solapa raro. La lista vive en **una
sola constante compartida** de `programas/poblacion.py`; agregar una actividad nueva
al programa es editar una línea, no cazar tres literales distintos.

Las 7 actividades (del DAX de `SM Activo 12m`, match por `norm()`):
`control salud mental` · `controles salud mental` · `consulta de salud mental` ·
`visita domiciliaria integral familia con integrante con patologia de salud mental` ·
`visita domiciliaria integral a familia con adulto mayor con demencia` ·
`visita domiciliaria integral a familia con niños/as de 5 a 9 años con problemas y/o
trastorno` · `visita integral de salud mental a domicilio`.

### 8.2 Otros detalles del port

- **Ambas anclan en `TODAY()`** → se parametrizan al corte (§4.1). Eso además permite
  recalcular la cohorte de un mes pasado, cosa que el PowerBI no puede.
- El DAX escribe `"patologia de salud mental"` **sin tilde**; en Python `norm()` lo
  resuelve en ambos sentidos, no hay que replicar el typo.
- La `13m` no exige «ninguna posterior» de forma explícita: lo consigue indirecto vía
  `Activo 12m = No`. Con la lista unificada (§8.1) las dos formulaciones convergen.
- Requiere **13 meses de ADA** (§3.1), un mes más de lo que pedía el P6 solo.

### 8.3 Fallecidos — y por qué NO basta con la cohorte del mes

`Fallecidos_mes` = cumple criterios SM · **no** está Activo+Inscrito+Ingresado ·
`Estado = Pasivo` & `Motivo Pasivación = Fallecido` & `Fecha Pasivación` **en el mes
reportado**. Es la misma definición que ya trae el `CONTEXTO_REM_general`.

Sirve para dos cosas distintas:
1. **Que nadie llame a la familia de un paciente que falleció.** Motivo obvio, y la
   razón por la que esta planilla existe.
2. **Egreso del A05** (fase 4): un fallecido salió de la población en control. Si no
   se identifica, cae en el residual «abandono» del delta P(m)−P(m−1) y ensucia la
   parte O.

**La cohorte del mes NO alcanza para el filtro de rescate.** `Rescate_6m` mira
6 meses atrás y `Rescate_13m` mira 13: alguien que falleció hace 8 meses **no** está
en `Fallecidos_mes` pero **sí** puede aparecer en `Rescate_13m` — dejó de asistir,
por razones evidentes. Entonces:

> **Filtro duro en las listas de rescate: se excluye a TODO paciente con
> `Motivo Pasivación = Fallecido`, sin importar la fecha de pasivación.**
> `Fallecidos_mes` es la cohorte del mes (para el A05); el filtro del rescate es
> sobre el histórico completo.

Cuando el filtro saque a alguien, el log lo dice con el conteo: es información útil
(«N de la cohorte de rescate estaban fallecidos»), no ruido.

*A confirmar:* los pasivados por **traslado / cambio de domicilio** tampoco son
rescatables (ya no pertenecen al centro). ¿Se excluyen también de las listas, o se
dejan para que alguien confirme el traslado?

### 8.4 Privacidad: SOLO RUN + Sector *(decidido)*

Un listado de rescate es para llamar, pero **NO lleva datos de contacto**. Quien
llame busca el teléfono en la ficha por RUN. Cero PII de contacto en un archivo que
puede quedar abierto en un escritorio compartido o mandarse por correo interno.

**Fuera, sin excepción:** `Nombre completo` · `Nombre Social` · `Celular` · `Mail` ·
`Dirección Completa` · `Fecha Nacimiento`. Es la misma lista que §3.2 saca de la tabla
base: el reporte de rescate **no reabre** esa puerta.

Columnas de `Rescate_6m` / `Rescate_13m`:

```
RUN · Sector · Edad · Sexo · Diagnósticos activos · Fecha última atención SM
```

`Edad`, `Sexo` y los diagnósticos se quedan porque sin ellos la lista no es
accionable (no se puede priorizar a quién llamar primero) y no son datos de contacto
— el criterio de §8 CLAUDE.md es que **el RUT sea el único identificador**, y se
respeta. Si igual se quieren fuera, es borrar tres columnas de una constante.

### 8.5 Traslados: NO se excluyen, se FLAGEAN aparte *(decidido)*

A diferencia de los fallecidos (§8.3, filtro duro), los pasivados por **cambio de
domicilio / traslado de inscripción** **siguen en las listas de rescate**. Un traslado
registrado no siempre significa que la persona se fue de verdad, y confirmarlo es
parte del trabajo de rescate.

Salida: una **segunda tabla chica**, `Posibles_Traslados`, con los RUN de las cohortes
de rescate cuyo `Motivo Pasivación` es de traslado, y su motivo. Quien llame la mira
primero y sabe que ahí **la gestión es confirmar el traslado**, no perseguir un
abandono.

Mismas columnas que las listas de rescate + `Motivo Pasivación` + `Fecha Pasivación`.

| Situación | En las listas de rescate | Tabla aparte |
|---|---|---|
| `Motivo Pasivación = Fallecido` | **NO** (filtro duro, cualquier fecha) | `Fallecidos_mes` (solo cohorte del mes, para el A05) |
| Traslado / cambio de domicilio | **SÍ** | `Posibles_Traslados` (flag) |

---

### 8.6 Brecha de control médico — toggle `exigir_medico`

**Idea:** correr la revisión formulario-por-formulario **omitiendo el check
`INSTRUMENTO ⊃ MEDIC`** (D3) y comparar contra la corrida normal. El delta son los
pacientes cuyo diagnóstico SM está registrado **solo por otro estamento** (psicólogo,
trabajador social, enfermería…) y que por lo tanto **están al debe de control médico**.

```
P_med    = población con el filtro médico       ← la que tributa al REM
P_todos  = población sin el filtro médico
BRECHA   = P_todos − P_med                      ← al debe de control médico
```

Sale casi gratis: la config por-dx ya tiene `filtra_instrumento` por fila, así que el
toggle es `filtra_instrumento and exigir_medico`. **El módulo corre las dos pasadas y
emite la diferencia** — no se le pide al usuario correr dos veces y restar a mano;
eso es justamente lo que hace útil el reporte.

**Salida:** hoja `Brecha_Medico`, sectorizada como las de rescate, mismas columnas
(`RUN · Sector · Edad · Sexo · Dx activos`, §8.4) **más**:

| Columna extra | Para qué |
|---|---|
| `Estamento que lo registró` | quién lo tiene en control hoy (del `INSTRUMENTO` / `PROFESIONAL ATENCION` del formulario) |
| `Fecha último formulario` | hace cuánto que está sin médico |
| `Dx que entran solo por no-médico` | si tiene otros dx que sí tienen control médico, se ve al tiro |

> **Guardarraíl obligatorio: el toggle NO cambia lo que tributa al REM.**
> El P6 se tabula **siempre** con `exigir_medico = True`. `P_todos` existe únicamente
> para calcular la brecha. El módulo **no debe** poder emitir una hoja `P6_A1` con el
> toggle apagado; si alguien lo intenta, error explícito. Sin esto, un día alguien
> corre con el toggle puesto y pega números inflados al SP.

**Ojo:** los **factores de riesgo ya no filtran por estamento** (D2), así que el
toggle solo mueve los **diagnósticos** (filas 25-58). La brecha es de control médico
del diagnóstico, que es exactamente lo que interesa.
