<!--
This document was generated with the assistance of Claude Opus 5.5 (Anthropic).
The human author reviewed, modified, and integrated the content.

Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
Copyright (C) 2026 Simon Tobar
SPDX-License-Identifier: GPL-3.0-or-later
Version: 2.0.20
-->

# PDS + CPU — casillas del SA_26 llenadas a mano (agosto 2026)

Contexto para el módulo nuevo de **Dependencia Severa** (PADDS) y **Cuidados Paliativos
Universales** (CPU). Es la fila «Dependencia / Domiciliaria» de la matriz de programas
(CLAUDE.md §9), que en el §12 aparecía como `rem_a26_domiciliaria`. **Este inventario
muestra que el módulo es bastante más grande que eso: toca cinco hojas del SA.**

**Fuentes** (ninguna planilla se versiona: aquí los valores quedan sacados de la
grilla y escritos en texto):
- **SA** — `SA_26_V1.2 PDS CPU AGOSTO 2026.xlsm`, el REM de **agosto 2026** que llenó a
  mano el equipo PDS. Contiene solo lo de PDS/CPU. Quedó en el OneDrive del trabajo y
  no está en el repo.
- **Comentado** — `refs_tablas/REM_Comentado_Serie_A_2026_15-04-2026.xlsx`: las notas
  de celda de cada casilla, con la definición DEIS y **qué formulario/campo/actividad de
  RAYEN la alimenta**.
- **Maestro** — `catalogos/maestro_slim.csv.gz` (actividad → estamento → REM/sección).

**Cómo se leyó el SA:** las hojas están protegidas, y **solo las casillas de input
están desbloqueadas** (`protection.locked == False`). Así se distinguen tres clases:
input llena (tiene valor), input vacía (—) y fórmula (total, no se escribe). Las
etiquetas de fila y columna se resolvieron a partir de las celdas combinadas.

> ⚠ **El Comentado es de otra versión que el SA V1.2.** Hay filas corridas: el A03·D.6
> está en la 194 del Comentado y en la 188 del SA. En A33·B también cambió el
> **orden de las columnas** (ver §6). **El cruce se hace por ETIQUETA, nunca por
> coordenada**, y el módulo tiene que escribir el SA ubicando cada casilla por su
> encabezado, no por la letra de columna.

---

## 0. Resumen

| Hoja · Sección | Qué es | Fuente RAYEN (según el Comentado) | ¿En el Maestro? |
|---|---|---|---|
| A03 · D.6 / D.6.1 | Zarit abreviado en cuidadores (y cuidadores NANEAS) | **Formulario clínico «Zarit Abreviado»** | No: solo como `REM-Gestion` («Aplicación de Zarit Abreviado», «Escala Zarit…») |
| A05 · J | Ingresos/egresos al programa de dependencia (leve/moderada/severa, onco/no onco, LPP) | **Formulario «Programa Dependencia, PADDS y CPU»**, título *Programa de pacientes con dependencia* | No: no hay actividad A05·J |
| A05 · V | Ingresos/egresos PADDS (persona + cuidador) | El **mismo formulario** (título *PADDS*, sección *Cuidador*) **Y** además la actividad | Sí: 15 actividades `Ingresos/Egresos del PADDS - …` |
| A26 · A.1 | VDI a personas con DS y sus cuidadores | **Actividad** `Visita domiciliaria integral a personas con PADDS - <condición> - <tipo visita>` | Sí: 28 actividades, calzan 1:1 con el Comentado |
| A26 · C | Visitas de tratamiento/procedimiento por estamento | **Actividad** `Tratamientos y/o Procedimientos en Domicilio - …` × **estamento** | Sí: 8 actividades |
| A27 · A / B | Educación grupal «Capacitación a Cuidadores PADDS» (4 temas) | **Atenciones grupales**, actividad `Educación en grupo - Capacitación a cuidadores PADDS - <tema>` | **No**: el Maestro no trae esas actividades (ver §5) |
| A33 · A | Ingresos CPU por diagnóstico, egresos por causal | **Formulario «Programa Dependencia, PADDS y CPU»**, título *CPU* | No: solo `AG_Ingreso/Egreso Cuidados Paliativos Universal …` (`REM-Gestion`, con **otra lista de dx**) |
| A33 · B | Atenciones CPU por tipo y estamento | **Actividad** `… - CPU` × estamento; las columnas *DS en APS* y *oncológicas* salen del formulario | Sí: 14 actividades |
| A33 · C / D / E | Talleres, capacitaciones, comités | Comentado: **«No Disponible»** | **Sí**: A33·C (2) y A33·E (6). Contradice al Comentado (ver §6) |

**Formularios que usa el equipo PDS** (lo confirmó la encargada PDS, sep-2026):
*Barthel*, *Zarit*, *Programa Dependencia, PADDS y CPU*, *EMPA/EMPAM*. En las secciones
del SA solo aparecen **Zarit** y **Programa Dependencia, PADDS y CPU**. El Barthel y el
EMP alimentan el **SP**. Los cuatro se bajan desde 2021 (§8).

**Variables transversales** (en todas las secciones, según el Comentado):
- Pueblo originario: Admisión o Box, «pertenece a pueblo indígena».
- Migrante: alerta administrativa «MIGRANTE».
- ECICEP: estratificación de riesgo G0-G3. OJO: en A26·C el Comentado dice **G1-G5**.
- ELEAM: alerta «Población ELEAM» / «Población ELEAM Institucionada».
- Discapacidad con RND: Box, «Origen Discapacidad».
- SENAME y SPE: alertas administrativas.

---

## 1. A03 — Zarit abreviado

### A03 · D.6: Zarit abreviado en cuidadores (SA filas 188-194)

Columnas de input: `L`/`M` 15-19 H/M · `N`/`O` 20-24 · `P`/`Q` 25-44 · `R`/`S` 45-64 ·
`T`/`U` 65+. Fórmulas en `C`, `D`, `E`. **La edad es la del cuidador.**

| Fila | Etiqueta | Casillas llenas | Total |
|---|---|---|---|
| 192 | Cuidador/a paciente con DS **con** sobrecarga intensa | `Q192` 25-44 M: **5** · `R192` 45-64 H: **1** · `S192` 45-64 M: **15** · `U192` 65+ M: **6** | 27 |
| 193 | Cuidador/a paciente con DS **sin** sobrecarga intensa | `Q193` 25-44 M: **2** · `R193` 45-64 H: **1** · `S193` 45-64 M: **7** · `T193` 65+ H: **1** · `U193` 65+ M: **1** | 12 |

**Regla (Comentado):** formulario «Zarit Abreviado», con los tres campos:

| Casilla | «Condición del Paciente» | «Puntaje Total» | «Estado de sobrecarga» |
|---|---|---|---|
| Con sobrecarga intensa | «Paciente con Dependencia Severa» | **≥ 17** | «Sobrecarga Intensa» |
| Sin sobrecarga intensa | «Paciente con Dependencia Severa» | < 17 | «Ausencia de Sobrecarga» |

El «Puntaje Total» lo calcula el formulario solo.

> **Frontera en 17 (resuelto, §7).** La Ref DEIS dice «mayor a 17» y el texto RAYEN
> dice «mayor o igual a 17». **Manda el campo «Estado de sobrecarga»**, que es lo que se
> registra, y equivale a ≥ 17. Si el puntaje no coincide con el estado, **se avisa, no
> se corrige callado**.

### A03 · D.6.1: Zarit en cuidadores de NANEAS (SA filas 195-201)

Columnas de input:
- Edad del **cuidador**: `F`/`G` 15-19 H/M · `H`/`I` 20-24 · `J`/`K` 25-44 · `L`/`M`
  45-64 · `N`/`O` 65+. Sale del campo «Edad Cuidador» del formulario.
- Edad del **paciente** NANEAS: `P` 0-4 · `Q` 5-9 · `R` 10-14 · `S` 15-19. Sale de la
  edad del paciente citado.

Fórmulas en `C`, `D`, `E`, `T` y las validaciones `CA`-`CP`.

| Fila | Etiqueta | Casillas llenas |
|---|---|---|
| 199 | Cuidador/a NANEAS con DS con sobrecarga intensa | — |
| 200 | Cuidador/a NANEAS con DS sin sobrecarga intensa | `M200` cuidador 45-64 M: **1** · `R200` paciente 10-14: **1** |

La regla es la misma, pero con «Condición del Paciente» = «Paciente NANEAS» y «Edad
Cuidador» obligatoria. **La fila lleva dos conteos del mismo evento**: uno por edad del
cuidador y otro por edad del paciente, y los dos tienen que sumar lo mismo.

---

## 2. A05 — Ingresos y egresos

### A05 · J: programa de dependencia leve, moderada y severa (SA filas 142-150)

Columnas de input:
- Edad × sexo del **paciente**, en pares H/M por quinquenio: `F`/`G` 0-4 … `AL`/`AM` 80+.
  Es decir: `F`/`G` 0-4 · `H`/`I` 5-9 · `J`/`K` 10-14 · `L`/`M` 15-19 · `N`/`O` 20-24 ·
  `P`/`Q` 25-29 · `R`/`S` 30-34 · `T`/`U` 35-39 · `V`/`W` 40-44 · `X`/`Y` 45-49 ·
  `Z`/`AA` 50-54 · `AB`/`AC` 55-59 · `AD`/`AE` 60-64 · `AF`/`AG` 65-69 · `AH`/`AI`
  70-74 · `AJ`/`AK` 75-79 · `AL`/`AM` 80+.
- Causal de egreso: `AN` Altas · `AO` Abandono/Traslado · `AP` Fallecimiento.
- `AQ` Pueblos originarios · `AR` Migrantes.

Fórmulas en `C`, `D`, `E`, `AS` y las validaciones. **Las columnas de edad cuentan
INGRESOS; las de causal cuentan EGRESOS.**

| Fila | Etiqueta | Casillas llenas | Σ ingresos |
|---|---|---|---|
| 146 | Dependencia Leve | — | 0 |
| 147 | Dependencia Moderada | — | 0 |
| 148 | DS · Oncológico | `V148` 40-44 H: **2** · `AF148` 65-69 H: **1** · `AG148` 65-69 M: **1** · `AL148` 80+ H: **1** · `AM148` 80+ M: **4** · `AP148` Fallecimiento: **5** | 9 |
| 149 | DS · No oncológico | `J149` 10-14 H: **1** · `M149` 15-19 M: **1** · `T149` 35-39 H: **1** · `AC149` 55-59 M: **1** · `AE149` 60-64 M: **1** · `AI149` 70-74 M: **1** · `AK149` 75-79 M: **1** · `AL149` 80+ H: **3** · `AM149` 80+ M: **6** · `AN149` Altas: **2** · `AO149` Abandono/Traslado: **2** · `AP149` Fallecimiento: **2** · `AR149` Migrantes: **1** | 16 |
| 150 | DS (lesiones por presión) | `V150` 40-44 H: **1** · `AE150` 60-64 M: **1** · `AI150` 70-74 M: **2** · `AJ150` 75-79 H: **1** · `AK150` 75-79 M: **3** · `AL150` 80+ H: **1** · `AM150` 80+ M: **13** | 22 |

**Regla (Comentado):** formulario «Programa Dependencia, PADDS y CPU».
- Sección *Sujeto de Cuidado*: «Tipo de Paciente» = Oncológico / No Oncológico.
- Título *Programa de pacientes con dependencia*:
  - «Tipo de Dependencia» = Leve / Moderada / Severa.
  - «Estado Dependencia» = `Ingreso` (va a la edad) · `Egreso Por Alta` (`AN`) ·
    `Egreso por Traslado` o `Egreso po Abandono` (`AO`, sic) · `Egreso por
    Fallecimiento` (`AP`).
- Además hay que anotar «Fecha Próximo Control».
- **LPP (fila 150):** lo mismo, más *Antecedentes personales* con «Lesión por Presión» =
  Sí.

> ⚠ **La fila 150 NO es un subconjunto de los ingresos de las filas 148 y 149.** El
> Comentado la define como «Ingreso + LPP = Sí», pero el SA de agosto dice otra cosa:
>
> | Banda | Ingresos DS (148+149) | LPP (150) |
> |---|---|---|
> | 80+ M | 10 | **13** |
> | 75-79 M | 1 | **3** |
> | 70-74 M | 1 | **2** |
>
> Sin ingresos DS, la fila 150 no podría superarlos. Lo más probable es que la hayan
> llenado con el **stock** de pacientes con LPP y no con los ingresos del mes.
> El autor se lo comenta a la encargada PDS. El módulo sigue la regla del Comentado.

### A05 · V: PADDS (SA filas 367-389)

Columnas de input:
- Edad × sexo en pares H/M por quinquenio: `E`/`F` 0-4 … `AK`/`AL` 80+. Está **una
  columna a la izquierda de la J**: la J empieza en `F`.
- `AQ` Discapacidad (con RND) · `AR` Pueblos originarios · `AS` Migrantes.

Fórmulas en `B`, `C`, `D`, `AT` y las validaciones. Filas 372-382: la persona con DS.
Filas 384-389: el cuidador, con la edad y el sexo **del cuidador**.

| Fila | Etiqueta | Casillas llenas | Σ |
|---|---|---|---|
| 372 | Ingreso con plan de cuidado integral (vía ECICEP) | — | 0 |
| 373 | Ingreso con plan de cuidado integral (no ECICEP) | `I373` 10-14 H: **1** · `L373` 15-19 M: **1** · `S373` 35-39 H: **1** · `U373` 40-44 H: **1** · `AB373` 55-59 M: **1** · `AF373` 65-69 M: **1** · `AK373` 80+ H: **3** · `AL373` 80+ M: **5** | 14 |
| 375 | Ingreso con plan de cuidado al cuidador (vía ECICEP) | — | 0 |
| 376 | Ingreso con plan de cuidado al cuidador (no ECICEP) | `P376` 25-29 M: **1** · `T376` 35-39 M: **2** · `V376` 40-44 M: **1** · `Z376` 50-54 M: **2** · `AB376` 55-59 M: **4** · `AD376` 60-64 M: **2** · `AJ376` 75-79 M: **2** | 14 |
| 378 | Egreso por alta (disminuye dependencia) | `AH378` 70-74 M: **1** · `AL378` 80+ M: **1** | 2 |
| 379 | Egreso por alta administrativa | `AD379` 60-64 M: **1** · `AS379` Migrantes: **1** | 1 |
| 380 | Egreso por traslado | `AJ380` 75-79 M: **1** · `AL380` 80+ M: **1** | 2 |
| 381 | Egreso por fallecimiento | `U381` 40-44 H: **1** · `AE381` 65-69 H: **1** · `AL381` 80+ M: **4** | 6 |
| 382 | Egreso por otras causas | — | 0 |
| 384 | Cuidador: egreso por alta de la persona con dependencia | `AB384` 55-59 M: **1** · `AK384` 80+ H: **1** | 2 |
| 385 | Cuidador: egreso por cambio de cuidador | — | 0 |
| 386 | Cuidador: egreso por alta administrativa | `P386` 25-29 M: **1** · `AS386` Migrantes: **1** | 1 |
| 387 | Cuidador: egreso por traslado | `V387` 40-44 M: **1** · `AB387` 55-59 M: **1** | 2 |
| 388 | Cuidador: egreso por fallecimiento de la persona con dependencia | `T388` 35-39 M: **1** · `AB388` 55-59 M: **1** · `AF388` 65-69 M: **2** · `AG388` 70-74 H: **1** · `AJ388` 75-79 M: **1** | 6 |
| 389 | Cuidador: egreso por fallecimiento del cuidador | — | 0 |

**Regla (Comentado):** formulario «Programa Dependencia, PADDS y CPU».
- **Persona:** «Tipo de Dependencia» = Severa, y en el título *PADDS* el campo «Estado
  PADDS» = <la fila>.
- **Cuidador:** sección *Cuidador*, con «¿Tiene Cuidador?» = Sí, «Estado Cuidador» =
  <la fila> y, para los ingresos, «Tipo de Ingreso Cuidador PADPDS» (sic).
- **Y además** hay que registrar la actividad `Ingresos/Egresos del PADDS - … - <fila>`,
  que sí está en el Maestro.

**Son dos señales para el mismo evento** (el campo del formulario y la actividad), así
que el módulo tiene que cruzarlas y avisar cuando no coinciden.

> Nota: en la fila 388 la columna `AG` es 70-74 **H**. Es un cuidador hombre de 70-74
> años, no un error: la edad es la del cuidador.

---

## 3. A26 — Visitas domiciliarias

### A26 · A.1: VDI a personas con DS y sus cuidadores (SA filas 36-47)

Columnas de input:
- `C` Visita de ingreso al PADDS · `D` Primera visita anual · `E` Segunda visita anual ·
  `F` Tercera o más de seguimiento.
- `G` Elaboración del plan de cuidado integral a la persona · `H` Evaluación y
  actualización del plan a la persona.
- `I` Elaboración del plan al cuidador · `J` Evaluación y actualización del plan al
  cuidador.
- `K` Migrantes · `L` Pueblos originarios · `M` Población en ECICEP · `N` ELEAM.

Fórmulas: `O` (validación), fila 41 (total por condición) y fila 47 (total por edad).

| Fila | Condición / rango etario | Casillas llenas |
|---|---|---|
| 38 | Familia con integrante con DS **con demencia** | `C38` **4** · `E38` **13** · `F38` **41** · `G38` **4** · `H38` **13** · `I38` **4** · `J38` **13** · `K38` **2** · `L38` **1** |
| 39 | … con DS **en etapa terminal** (excluye demencia avanzada) | `C39` **1** · `E39` **2** · `F39` **11** · `G39` **1** · `H39` **2** · `I39` **1** · `J39` **2** · `L39` **1** |
| 40 | … con DS **sin demencia y/o no terminal** | `C40` **9** · `E40` **10** · `F40` **68** · `G40` **9** · `H40` **10** · `I40` **9** · `J40` **10** · `K40` **3** |
| 42 | por edad · 0-9 años | — |
| 43 | por edad · 10-14 años | `C43` **1** · `F43` **2** · `G43` **1** · `I43` **1** |
| 44 | por edad · 15-19 años | `C44` **1** · `F44` **3** · `G44` **1** · `I44` **1** |
| 45 | por edad · 20-64 años | `C45` **3** · `E45` **4** · `F45` **23** · `G45` **3** · `H45` **4** · `I45` **3** · `J45` **4** |
| 46 | por edad · 65+ años | `C46` **9** · `E46` **21** · `F46` **92** · `G46` **9** · `H46` **21** · `I46` **9** · `J46` **21** · `K46` **5** · `L46` **2** |

**Regla (Comentado):** una actividad por casilla, con el nombre `Visita domiciliaria
integral a personas con PADDS - <condición> - <tipo>`.
- **`G`** = visita de **ingreso** + actividad «Elaboración plan cuidado integral…».
- **`H`** = visita primera/segunda/tercera + «Evaluación y actualización plan de
  cuidados a personas…».
- **`J`** tiene actividades compuestas propias (`… - Primera visita anual - Evaluación y
  actualización plan de cuidados a cuidador`, y lo mismo para la segunda y la tercera).

Las filas 42-46 son **la misma cuenta abierta por edad** del paciente, y el Comentado no
trae una regla aparte.

**Los 28 nombres del Maestro·A26·A1 calzan 1:1 con el Comentado.** Uno trae un espacio
al final: `…etapa terminal - Visita de Ingreso al PADDS `. Hay que comparar normalizado.

Chequeos que **pasan** en agosto:
- Filas 38-40 contra filas 43-46: `C` 14 = 14 · `E` 25 = 25 · `F` 120 = 120 · `K` 5 = 5
  · `L` 2 = 2.
- `G` = `I` = `C` en cada fila, porque cada ingreso trae su plan y el plan del
  cuidador.
- `H` = `J` = `E` en cada fila. Llama la atención que el plan solo se evalúe en la
  **segunda** visita: las 120 visitas de tercera o más no tienen ninguna evaluación.
  Puede ser práctica local, pero **confirmarlo**.

`D` (primera visita anual) quedó en 0 en todas las filas. Es verosímil en agosto, si
todas las primeras visitas del año ya se hicieron.

### A26 · C: visitas de tratamiento/procedimiento a personas con dependencia (SA filas 61-69)

Columnas de input:
- `C` N° de visitas realizadas.
- Estamento: `E` Médico · `F` Odontólogo · `G` Químico farmacéutico · `H` Enfermero ·
  `I` Kinesiólogo · `J` Terapeuta ocupacional · `K` Fonoaudiólogo · `L` Psicólogo ·
  `M` Nutricionista · `N` Trabajador social · `O` Técnico en enfermería · `P` Otro.
- `Q` Pueblos originarios · `R` Migrantes · `S` ECICEP · `T` ELEAM · `U` Atención
  nutricional a personas con NED.

Fórmulas: `D` = `SUM(E:P)` (participaciones por estamento) y `V`.

| Fila | Etiqueta | Casillas llenas | Σ estamentos (`D`) |
|---|---|---|---|
| 64 | Dependencia leve | — | 0 |
| 65 | Dependencia moderada | — | 0 |
| 66 | DS · Oncológicos | `E66` Méd **1** · `F66` Odont **1** · `H66` Enf **3** · `I66` Kine **2** · `K66` Fono **2** · `M66` Nutri **1** · `N66` TS **2** · `O66` TENS **6** · `Q66` P.Orig **2** | 18 |
| 67 | DS · No oncológicos | `E67` Méd **23** · `F67` Odont **8** · `H67` Enf **156** · `I67` Kine **52** · `J67` TO **5** · `K67` Fono **10** · `L67` Psic **3** · `M67` Nutri **12** · `N67` TS **26** · `O67` TENS **29** · `Q67` P.Orig **5** · `R67` Migr **3** | 324 |
| 68 | DS · Entrega de fármacos/alimentos | — | 0 |
| 69 | DS · Seguimiento remoto | — | 0 |

**Regla (Comentado):** la actividad `Tratamientos y/o Procedimientos en Domicilio -
Personas con dependencia <leve|moderada|severa - Oncológicos|No oncológicos|…>`, contada
**por el estamento de quien la registra**. `U` sale de la actividad «Atención nutricional
a personas con NED». En la fila 68, el Comentado dice «Entrega fármacos / Entrega
Alimentos» y el Maestro «Entrega de fármacos a domicilio / Entrega de alimentos a
domicilio»: comparar con `contiene_todos`, nunca por igualdad.

> ⚠ **`C` (N° de visitas realizadas) quedó VACÍA**, aunque es input. La Ref DEIS la
> define como «el número de visitas», y no es lo mismo que `D`: una visita con dos
> estamentos cuenta 1 en `C` y 2 en `D`. Una visita multiprofesional se agrupa por
> paciente + fecha. **Resuelto (§7): el módulo la llena.**

---

## 4. A27 — Educación grupal a cuidadores PADDS

Solo se muestran las filas PADDS. El resto de las secciones A y B son de otros
programas.

### A27 · A: personas que ingresan a educación grupal (SA filas 47-50)

Columnas de input:
- Edad: `K` 15-19 · `L` 20-24 · `M` 25-29 · `N` 30-34 · `O` 35-39 · `P` 40-44 · `Q`
  45-49 · `R` 50-54 · `S` 55-59 · `T` 60-64 · `U` 65-69 · `V` 70-74 · `W` 75-79 · `X`
  80+. **No se abre por sexo.**
- `Y` Gestantes · `AB` Familias en riesgo · `AC` Pueblos originarios · `AD` Migrantes ·
  `AE` Espacios amigables · `AF`/`AG` Trans M/F · `AH` SENAME · `AI` SPE.

| Fila | Tema | Casillas llenas | Σ |
|---|---|---|---|
| 47 | Autocuidado del cuidador/a | `O47` 35-39: **1** · `Q47` 45-49: **1** · `R47` 50-54: **3** · `S47` 55-59: **4** · `T47` 60-64: **7** · `U47` 65-69: **2** · `V47` 70-74: **2** · `W47` 75-79: **1** · `X47` 80+: **1** | 22 |
| 48 | Cuidados de la persona con dependencia | `N48` 30-34: **1** · `O48` 35-39: **2** · `P48` 40-44: **1** · `R48` 50-54: **2** · `S48` 55-59: **4** · `T48` 60-64: **2** · `W48` 75-79: **2** | 14 |
| 49 | Redes y sistemas de apoyo a la díada del cuidado | — | 0 |
| 50 | Cuidados de fin de vida y duelo | `T50` 60-64: **1** | 1 |

**Regla (Comentado):** se registran como *atenciones grupales*, con la actividad
`Educación en grupo - Capacitación a cuidadores PADDS - <tema>`. Cada participante lleva
el check «Ingreso» marcado, «¿Es ingreso?» activado y el tipo de participante = su rango
etario.

> **Validación del propio SA:** en las filas 47 y 50 se dispararon las alertas «No
> olvide ingresar … (Digite CERO si no tiene)» de `AB`, `AC`, `AD`, `AE`, `AH` e `AI`.
> **El módulo tiene que escribir 0 explícito** en esas columnas, no dejarlas vacías.
> (La fila 48 no muestra la alerta, pero probablemente es solo el caché de Excel.)

### A27 · B: sesiones según personal (SA filas 92-95)

Columnas de input: `E` Un profesional · `F` Dos o más profesionales · `G` Un
profesional + TENS · `H` TENS · `I` Facilitador intercultural. Fórmula: `D` = `SUM(E:H)`.

| Fila | Tema | Casillas llenas | Σ sesiones |
|---|---|---|---|
| 92 | Autocuidado del cuidador/a | `E92` **14** · `F92` **22** | 36 |
| 93 | Cuidados de la persona con dependencia | `E93` **14** | 14 |
| 94 | Redes y sistemas de apoyo a la díada | `E94` **14** · `F94` **22** | 36 |
| 95 | Cuidados de fin de vida y duelo | `E95` **1** | 1 |

> ⚠ **Los números de la B no se ven como sesiones.** Se repiten 14 y 22, que son
> justamente los **participantes** de la A (22 en autocuidado, 14 en cuidados).
> «Redes» tiene 36 sesiones y **0 ingresos**, y 36 sesiones de autocuidado para 22
> personas es mucho en un mes. Parece que se copiaron conteos de personas en la tabla
> de sesiones. **No sirve de oráculo hasta que la encargada PDS lo confirme.**

---

## 5. A33 — Cuidados Paliativos Universales

### A33 · A: ingresos por diagnóstico y egresos por causal (SA filas 8-34)

Columnas de input:
- Edad × sexo en pares H/M por quinquenio: `G`/`H` 0-4 … `AM`/`AN` 80+.
- `AO` Pueblos originarios · `AP` Migrantes · `AQ` SENAME · `AR` SPE.

Filas:
- 12-13 ingresos oncológicos (no progresivas / progresivas).
- 14-23 ingresos no oncológicos: VIH, neurológico, cardiológico, pulmonar, hepático,
  renal, tejido conectivo/musculoesquelético, malformaciones, prematurez, otras.
- 24-29 egresos oncológicos · 30-34 egresos no oncológicos. Las causales son
  fallecimiento < 6 m, 6-12 m o > 12 m, término de tratamiento (solo onco), no
  cumplimiento de criterios y otra.

| Fila | Etiqueta | Casillas llenas |
|---|---|---|
| 15 | Ingreso · no oncológica · de origen neurológico | `AN15` 80+ M: **1** |
| 30 | Egreso · no oncológica · fallecimiento < 6 meses desde el ingreso | `AH30` 65-69 M: **1** · `AN30` 80+ M: **1** |

Todas las demás filas (12-14, 16-29, 31-34) quedaron en —.

**Regla (Comentado):** formulario «Programa Dependencia, PADDS y CPU».
- «Tipo de Paciente» = Onco / No onco.
- Título *CPU*: «Estado CPU» = `Ingreso` o la causal de egreso, y «Enfermedad
  (No) Oncológica» = <la fila>.

> ⚠ **El Maestro tiene otra taxonomía de diagnósticos.** Sus `AG_Ingreso Cuidados
> Paliativos Universal <dx>` (`REM-Gestion`) usan una lista vieja: EPOC, insuficiencia
> cardíaca, ACV-TEC, neurodegenerativas, parálisis cerebral, etc. El SA 2026 usa grupos
> por órgano. **Para A33·A la fuente es el formulario, no las actividades.** Si algún
> día se usaran las actividades, haría falta un crosswalk dx → grupo, validado con la
> encargada PDS.

### A33 · B: tipo de atención y actividades (SA filas 39-51)

Columnas de input del SA V1.2:
- Edad × sexo: `F`/`G` 0-4 … `AH`/`AI` **70+**. Termina en 70+, no en 80+.
- Estamento: `AJ` Médico · `AK` Enfermero · `AL` Kinesiólogo · `AM` TENS · `AN`
  Psicólogo · `AO` Químico farmacéutico · `AP` Nutricionista · `AQ` Fonoaudiólogo · `AR`
  TO · `AS` TS.
- `AT`/`AU` **Dependencia Severa en APS** H/M. Solo existe en las filas 39-41.
- `AV`/`AW` Atenciones a personas oncológicas 0-19 / 20+.

| Fila | Etiqueta | Casillas llenas | Σ edad |
|---|---|---|---|
| 39 | VD APS · VDI de ingreso | `AI39` 70+ M: **1** · `AK39` Enf: **1** · `AU39` DS M: **1** | 1 |
| 40 | VD APS · VDI de seguimiento | `AD40` 60-64 H: **2** · `AF40` 65-69 H: **1** · `AH40` 70+ H: **1** · `AI40` 70+ M: **13** · `AK40` Enf: **5** · `AL40` Kine: **9** · `AQ40` Fono: **3** · `AT40` DS H: **4** · `AU40` DS M: **13** | 17 |
| 41 | VD APS · VD tratamiento/procedimiento/rehabilitación | `AI41` 70+ M: **26** · `AK41` Enf: **8** · `AM41` TENS: **18** · `AU41` DS M: **26** | 26 |
| 42-51 | VD nivel secundario · ambulatoria · remota · cerrada | — | 0 |

**Regla (Comentado):** una actividad `<tipo> - <nivel> - CPU` por fila; los 14 nombres
están en el Maestro. Las columnas por estamento salen de quien la registra. La columna
*DS en APS* cuenta al paciente con el formulario PDS en «Tipo de Dependencia» = Severa
y «Estado» = Ingreso/Seguimiento. La columna *oncológicas* cuenta «Tipo de Paciente» =
Oncológico.

> ⚠ **Cambió el orden de las columnas entre versiones.** En el Comentado, `AT` =
> «Consulta nueva», `AU` = «Dependencia Severa en APS» (una sola columna) y `AW` =
> «oncológicas». En el SA V1.2, `AT`/`AU` = DS H/M y `AV`/`AW` = oncológicas 0-19/20+.
> También cambió la fila 44: «Consulta a paciente» en el Comentado, «Consultas nuevas»
> en el SA. **Se escribe por encabezado.**

Chequeos que **pasan**: en cada fila, la edad suma lo mismo que los estamentos y lo
mismo que la columna DS (1/1/1 · 17/17/17 · 26/26/26). Todo paciente CPU atendido en
agosto también es DS. El ingreso de A33·A (80+ M) cae en la banda 70+ M de B·39.

### A33 · C / D / E: talleres, capacitaciones y comités (SA filas 52-73)

Todo quedó en —. El Comentado dice **«No Disponible»** en las tres, o sea que RAYEN no
las entrega. **Pero el Maestro sí mapea actividades a A33·C** (`Taller Educación
Usuarios CPU - Presencial/Remota`) **y a A33·E** (6 `Comité Cuidados Paliativos … -
Modalidad …`). **Resuelto (§7):** los talleres CPU hoy no se registran, y si se
registran irán, casi seguro, como grupales de salud mental, que el módulo no puede
separar. No hay comités CPU en el Servicio. **Las tres quedan vacías** y se avisa en la
LEEME. A33·D (capacitaciones de equipos) no tiene fuente en ningún lado.

---

## 6. Cruces entre hojas (agosto 2026)

| Cruce | Valores | ¿Calza? |
|---|---|---|
| Ingresos PADDS persona (A05·V 373) = VDI de ingreso (A26·A.1 `C`, Σ 38-40) = plan integral (`G`) | 14 = 14 = 14 | ✅ |
| Ingresos PADDS cuidador (A05·V 376) = plan al cuidador (A26·A.1 `I`) = ingresos persona | 14 = 14 = 14 | ✅ |
| Egresos PADDS persona (378/379/380/381) = egresos cuidador por la misma causa (384/386/387/388) | 2/1/2/6 = 2/1/2/6 | ✅ |
| Ingresos DS del programa (A05·J 148+149) contra ingresos PADDS (A05·V 373) | **25 contra 14** | ❓ J cubre a todo DS y V solo al PADDS, así que puede ser legítimo: preguntar |
| Fallecidos DS (A05·J `AP`, 5+2) contra PADDS (A05·V 381) | **7 contra 6** | ❓ igual que arriba |
| Altas (A05·J `AN`) contra PADDS (V 378) · Abandono/Traslado (J `AO`) contra traslado (V 380) | 2 = 2 · 2 = 2 | ✅ (el alta administrativa de V·379 no tiene casilla en J) |
| LPP (A05·J 150) ⊂ ingresos DS (148+149) por banda | 80+ M: 13 > 10 | ❌ ver §2 |
| Sesiones A27·B contra ingresos A27·A | «Redes»: 36 sesiones, 0 ingresos | ❌ ver §4 |
| Ingreso CPU (A33·A) contra VDI de ingreso CPU (A33·B 39) | 1 = 1 (80+ M ⊂ 70+ M) | ✅ |

---

## 7. Lo que falta para diseñar el módulo

**Inputs** (sep-2026: los formularios ya se están bajando desde 2021; campos exactos
en el §8):
1. **Formulario clínico «Programa Dependencia, PADDS y CPU»**, con sus secciones *Sujeto
   de Cuidado*, *Programa de pacientes con dependencia*, *PADDS*, *Cuidador*, *CPU* y
   *Antecedentes personales (LPP)*. Alimenta A05·J, A05·V, A33·A y las columnas DS y
   oncológicas de A33·B.
2. **Formulario clínico «Zarit Abreviado»**, con «Condición del Paciente», «Puntaje
   Total», «Estado de sobrecarga» y «Edad Cuidador». Alimenta A03·D.6 y D.6.1.
3. **Atenciones individuales con actividad + estamento** para A26·A.1, A26·C, las
   actividades de A05·V y A33·B. Es la misma familia de export que ya usa el SM (verificar
   que traiga estos programas).
4. **Atenciones grupales** con participantes, edad y check de ingreso, para A27·A y B.
5. **Barthel** y **EMP** (con el EMPAM adentro): no aparecen en el SA; alimentan el SP
   (confirmado).

**Resuelto por el autor (sep-2026):**
- **Zarit en 17:** se registra lo que sale de RAYEN, es decir el campo `16.- Estado de
  Sobrecarga` (Ausencia / Sobrecarga Intensa). **Manda el campo.** Coincide con
  «≥ 17 = sobrecarga intensa». El puntaje (`15.-`) queda como chequeo: si no calza con
  el estado, se avisa.
- **A26·C `C` (N° de visitas):** probablemente la llena el consolidador. **El módulo la
  llena**, con las visitas únicas (paciente + fecha).
- **A33·C (talleres CPU):** hoy no se registran. Si se registran, casi seguro que irán
  como actividades grupales de **salud mental**, y el módulo no puede separarlas. Queda
  vacía y se avisa en la LEEME.
- **A33·E (comités CPU):** no hay comités en el Servicio por ahora. Queda vacía.
- **A05·J 150 (LPP):** el autor se lo comenta a la encargada PDS. **No es pega nuestra
  auditarlo.** El módulo sigue la regla del Comentado (ingreso + LPP = Sí).

**Preguntas que quedan para la encargada PDS** (son de práctica del programa, no
bloquean el diseño):
- A26·A.1: ¿la evaluación del plan (`H`, `J`) se registra solo en la segunda visita?
- A27·B: ¿de dónde salen los 14 y 22?
- A05·J contra A05·V: ¿quiénes son los 11 ingresos DS que no están en el PADDS? (sirve
  para validar)

**Deuda del Maestro:** el `maestro_slim` no trae las 4 actividades `Educación en grupo -
Capacitación a cuidadores PADDS - <tema>` que nombra el Comentado. Sus equivalentes
locales son `AG_Capacitación - Autocuidado del cuidador/a` y parecidas, todas como
`REM-Gestion`. Revisar contra el Maestro completo antes de concluir que no existen.

**Sigue:** el mismo inventario sobre el **SP** (`SP_26_V1.2 JUNIO 26 PDS.xlsm`), que
ya está en [pds_cpu_casillas_SP.md](pds_cpu_casillas_SP.md).

---

## 8. Fuentes RAYEN confirmadas (headers, sep-2026)

El autor baja los cuatro formularios **desde 2021** a la carpeta de datos madre (sin
header, en subcarpetas de `pdscpu/`; el EMP ya estaba en `variables 12m/emp`). Las
copias con banner + encabezado están en `refs_tablas/`, vetadas y en el whitelist.

| Formulario (nombre Admin) | En IRIS se llama | Existe desde | Refs | Alimenta |
|---|---|---|---|---|
| «Programa Dependencia, PADDS y CPU» | «VDI1 Ingreso PADPDS CPU» | **2023** | `pdscpu_{admin,iris}.xlsx` | A05·J/V · A33·A · A33·B (columnas DS/onco) · P3·A/B |
| «Zarit Abreviado» | igual | — | `zarit_abreviado_{admin,iris}.xlsx` | A03·D.6/D.6.1 |
| «Indice de Barthel» | igual | — | `Barthel_{admin,iris}.xlsx` | Solo como **chequeo** (se hace también a usuarios que no son del PDS) |
| «EMP» (incluye el **EMPAM**: en los reportes aparece así **desde 2021**, porque RAYEN habría redirigido el EMPAM antiguo al EMP nuevo. **No hace falta excepción por fecha**) | «EMP - Examen de Medicina Preventiva» | — | `emp_{admin,iris}.xlsx` | P5·A/B · chequeo de P3·B `F` |

Las actividades (A26·A.1/C, A05·V, A33·B) y las grupales (A27) salen de los exports que
ya usa el SM: `ATENCIONESDIAGNOSTICOSACTIVIDADES_iris` y `Atenciones_Grupales_iris`.

**Campo de RAYEN por casilla.** La numeración es **la misma en Admin y en IRIS** (en
Admin va en minúsculas):

| Casilla | Campos |
|---|---|
| A03·D.6 filas | Zarit `7.- Condición del paciente` · `15.- Puntaje Total` · `16.- Estado de Sobrecarga` |
| A03·D.6 columnas | Zarit `3.- Edad Cuidador` · `4.- Sexo Cuidador` (**no** el `SEXO` de la fila, que es el del paciente) |
| A03·D.6.1 edad NANEAS | Edad del paciente (`EDAD PACIENTE` en IRIS, `Edad de registro formulario` en Admin) |
| A05·J | PDS `1.- Tipo de Paciente` · `7.- Tipo de Dependencia` · `8.- Estado Dependencia` · `44.- Lesión por Presión` |
| A05·V persona | PDS `9.- Estado PADDS` (+ la actividad `Ingresos/Egresos del PADDS`) |
| A05·V cuidador | PDS `73.- Tiene Cuidador?` · `74.- Estado Cuidador` · `79.- Tipo de Ingreso Cuidador PADDS` · `82.- Edad Cuidador` |
| A33·A | PDS `10.- Estado CPU` · `11.- Enfermedad Oncológica` · `12.- Enfermad No Oncológica` (sic) |
| A33·B `AT`-`AW` | PDS `7.-` + `8.-` (DS en APS) · `1.-` (oncológicas) |

**Advertencias para el lector:**
- ⚠ **El formulario PDS no trae el sexo del cuidador**: solo `80.- Rut`, `81.- Fecha
  Nacimiento` y `82.- Edad`. Las filas del cuidador de la A05·V (y la P3·B `C`/`D`) van
  por sexo del cuidador. **RAYEN no lo registra en ningún otro lado** (confirmado por el
  autor), así que sale del **Informe Inscritos** con match por RUT. El Informe Inscritos
  ya es input opcional del SM. El `4.- Sexo Cuidador` del Zarit sirve solo de chequeo.
  **Un cuidador no inscrito queda sin dato y se avisa. Nunca se usa el sexo del
  paciente.**
- **Formularios que alimentan formularios** (confirmado): el «Indice de Barthel» llena
  el `5.- Resultado Índice de Barthel` del formulario PDS y el `119.- Nivel de Severidad`
  del EMP.
- **Hay nombres repetidos** (`24./25.- Estado Nutricional`, `118./121./125.- Puntaje`,
  `Problema(s) Cuidador` ×3). Hay que leer **por el nombre con su número**, y fallar
  ruidoso si hay ambigüedad.
- **La numeración puede correrse** entre versiones del formulario desde 2021. Hay que
  matchear por el texto después del número y verificarlo contra las cargas históricas.
  El EMPAM **no** es uno de esos casos: en los reportes ya viene dentro del EMP desde
  2021.
- **El formulario PDS no existe antes de 2023.** Un mes de 2021 o 2022 da
  `ArchivoInvalido`, no ceros. La detección va por firma de columnas, no por el nombre
  del formulario (que difiere entre IRIS y Admin).
- **`GENERO` solo existe en IRIS**; en Admin hay solo `Sexo`. La hipótesis de sexo
  registral contra identidad de género (el descuadre P3/P5 de 65-69 años) solo se
  puede probar con IRIS.
- Los refs no tienen contrato todavía: se escribe **junto con el loader** (skill
  `tests-fuentes`).
