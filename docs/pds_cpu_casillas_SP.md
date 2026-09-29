<!--
This document was generated with the assistance of Claude Opus 5.5 (Anthropic).
The human author reviewed, modified, and integrated the content.

Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
Copyright (C) 2026 Simon Tobar
SPDX-License-Identifier: GPL-3.0-or-later
Version: 2.0.20
-->

# PDS + CPU — casillas del SP_26 llenadas a mano (corte junio 2026)

Continúa [pds_cpu_casillas_SA.md](pds_cpu_casillas_SA.md). Es la **Serie P**, o sea
**población en control**: un stock al corte semestral (junio y diciembre), no eventos
del mes. Se generó con la skill `inventario-rem`.

**Fuentes:**
- **SP**: `SP_26_V1.2 JUNIO 26 PDS.xlsm`, llenado a mano por el equipo PDS. Quedó en el
  OneDrive y no está en el repo.
- **Manual REM P 2026 v1.0 (DEIS)**: `OneDrive/REM SM/2026/MANUAL REM  P 2026 Version
  1.0.pdf`. P3 en las págs. 59-70 y P5 en las 91-96. De ahí salen las reglas de este doc.
- **No hay REM Comentado de la Serie P**, así que el Manual dice **qué** contar, pero no
  **de qué formulario o campo de RAYEN**. Eso queda marcado *(RAYEN: por confirmar)*.
- El Maestro no trae nada para P3 ni P5. Es esperable: la población en control sale de
  formularios, no de actividades.

**Formularios que usa el equipo** (jefa PDS, sep-2026): Barthel · Zarit · Programa
Dependencia, PADDS y CPU · EMPA/EMPAM. **En la Serie P aparecen los cuatro**, que en el
SA faltaban. En RAYEN **un formulario alimenta a otro**: el Barthel llena el «Tipo de
Dependencia» del formulario PDS.

---

## 0. Resumen

| Hoja · Sección | Qué es | Criterio (Manual) | Fuente RAYEN probable |
|---|---|---|---|
| P3 · A, filas 33-47 | Existencia por dependencia, PADDS y CPU | **Barthel**: leve ≥ 60 · moderada 40-55 · severa ≤ 35 (o certificado médico). «En control» = citado, sin abandono | Formulario **Programa Dependencia, PADDS y CPU** (el Barthel lo alimenta) |
| P3 · B | Cuidadores de las personas del PADDS | Capacitado = **6 sesiones** en el año (nuevo) o **4** (antiguo) · EMPA/EMPAM vigente · Zarit en los últimos **11 m 29 d** · estipendio MDS | Sección **Cuidador** del formulario PDS + atenciones grupales A27 + **EMPA/EMPAM** del cuidador + **Zarit** |
| P5 · A, filas 16-19 | Mayores de 65 en control por funcionalidad | **EMPAM** (o control de seguimiento) en los últimos 11 m 29 d; funcionalidad por **Barthel** si depende de terceros | **EMPAM**, con su Barthel |
| P5 · B | Estado nutricional de la misma población | Del EMPAM. En dependencia moderada, grave o total, por apreciación diagnóstica | **EMPAM** |

El resto de P3·A (respiratorios, epilepsia, TEA, Parkinson, etc.) y P5·A.1, C, D y E
quedaron vacíos: son de otros programas.

> ⚠ **La P5 es compartida con el Programa del Adulto Mayor.** Las filas 12-14 de P5·A
> (autovalente sin riesgo, con riesgo, riesgo de dependencia) salen del **EFAM** del
> EMPAM y las llena otro equipo. El Manual es explícito: «dependencia grave y total
> deben ser derivadas al PADDS, **siguiendo bajo control** por las acciones antes
> descritas para la población de personas mayores». Es decir, **el mismo paciente se
> cuenta en P3 (PDS) y en P5 (Adulto Mayor)**. El módulo PDS aporta solo una parte de
> la P5, y hay que saber cómo se consolida el REM del CESFAM antes de escribirla: ¿se
> suman las planillas de cada equipo o se llena una sola?

---

## 1. P3 · A — Existencia de población en control (SP filas 33-47)

Columnas de input: edad × sexo en pares H/M por quinquenio, `F`/`G` 0-4 … `AL`/`AM`
80+. Es el mismo patrón que la A05·J del SA: `F`/`G` 0-4 · `H`/`I` 5-9 · `J`/`K` 10-14 ·
`L`/`M` 15-19 · `N`/`O` 20-24 · `P`/`Q` 25-29 · `R`/`S` 30-34 · `T`/`U` 35-39 · `V`/`W`
40-44 · `X`/`Y` 45-49 · `Z`/`AA` 50-54 · `AB`/`AC` 55-59 · `AD`/`AE` 60-64 · `AF`/`AG`
65-69 · `AH`/`AI` 70-74 · `AJ`/`AK` 75-79 · `AL`/`AM` 80+. Además, `AO`/`AP` Pueblos
originarios **H/M** y `AQ`/`AR` Migrantes **H/M**: en la P3 van abiertos por sexo, a
diferencia del SA. Una persona puede estar en las dos. Fórmulas en `C`, `D`, `E`, `AS`
y las validaciones.

| Fila | Etiqueta | Casillas llenas | Σ |
|---|---|---|---|
| 33 | Dependencia leve | — | 0 |
| 34 | Dependencia moderada | `Y34` 45-49 M: **1** · `AM34` 80+ M: **1** | 2 |
| 35 | DS · Oncológica | `AA35` 50-54 M: **1** · `AC35` 55-59 M: **1** · `AF35` 65-69 H: **1** · `AH35` 70-74 H: **1** · `AI35` 70-74 M: **1** · `AJ35` 75-79 H: **2** · `AK35` 75-79 M: **2** · `AL35` 80+ H: **3** · `AM35` 80+ M: **8** | 20 |
| 36 | DS · No oncológica | `H36` 5-9 H: **2** · `J36` 10-14 H: **1** · `L36` 15-19 H: **2** · `N36` 20-24 H: **2** · `P36` 25-29 H: **2** · `Q36` 25-29 M: **4** · `T36` 35-39 H: **2** · `U36` 35-39 M: **3** · `V36` 40-44 H: **2** · `W36` 40-44 M: **2** · `X36` 45-49 H: **1** · `Y36` 45-49 M: **1** · `AB36` 55-59 H: **3** · `AD36` 60-64 H: **3** · `AE36` 60-64 M: **4** · `AF36` 65-69 H: **7** · `AG36` 65-69 M: **4** · `AH36` 70-74 H: **4** · `AI36` 70-74 M: **10** · `AJ36` 75-79 H: **8** · `AK36` 75-79 M: **16** · `AL36` 80+ H: **18** · `AM36` 80+ M: **73** · `AP36` P.Orig M: **5** · `AQ36` Migr H: **1** · `AR36` Migr M: **6** | 174 |
| 37 | DS · Total con lesión por presión | `V37` 40-44 H: **1** · `AE37` 60-64 M: **1** · `AI37` 70-74 M: **1** · `AK37` 75-79 M: **2** · `AL37` 80+ H: **1** · `AM37` 80+ M: **12** | 18 |
| 38 | Atención domiciliaria por DS · Total personas | Casilla por casilla = **35 + 36** (p. ej. `AF38` **8** = 1 + 7 · `AM38` **81** = 8 + 73) · `AP38` **5** · `AQ38` **1** · `AR38` **6** | 194 |
| 39 | Atención domiciliaria · Oncológica | Idéntica a la fila 35 | 20 |
| 40 | Atención domiciliaria · No oncológica | Idéntica a la fila 36, incluidos pueblos y migrantes | 174 |
| 41 | Atención domiciliaria · Con demencia | `AD41` 60-64 H: **1** · `AF41` 65-69 H: **4** · `AG41` 65-69 M: **1** · `AH41` 70-74 H: **1** · `AI41` 70-74 M: **2** · `AJ41` 75-79 H: **5** · `AK41` 75-79 M: **11** · `AL41` 80+ H: **12** · `AM41` 80+ M: **38** · `AP41` P.Orig M: **2** · `AQ41` Migr H: **1** · `AR41` Migr M: **2** | 75 |
| 42 | Atención domiciliaria · Institucionalizada | — | 0 |
| 43 | Atención domiciliaria · Total con lesión por presión | Idéntica a la fila 37 | 18 |
| 44 | Atención domiciliaria · Con indicación de NED | `J44` 10-14 H: **2** · `N44` 20-24 H: **1** · `O44` 20-24 M: **1** · `P44` 25-29 H: **1** · `R44` 30-34 H: **1** · `AD44` 60-64 H: **1** · `AF44` 65-69 H: **1** · `AM44` 80+ M: **3** | 11 |
| 45 | CPU · Oncológico progresivo | — | 0 |
| 46 | CPU · Oncológico no progresivo | — | 0 |
| 47 | CPU · No oncológico | `AD47` 60-64 H: **1** · `AE47` 60-64 M: **1** · `AF47` 65-69 H: **1** · `AG47` 65-69 M: **1** · `AH47` 70-74 H: **2** · `AJ47` 75-79 H: **1** · `AM47` 80+ M: **14** · `AP47` P.Orig M: **1** | 21 |

**Reglas (Manual págs. 60-66):**
- **«En control»** (válido para toda la P3): la persona está siendo tratada y **tiene
  citación a un próximo control**. Si pasan **11 meses 29 días sin asistir desde la
  última citación** (15 años o más; hay plazos más cortos para los menores de 2 años),
  cuenta como abandono y sale. También sale si no es ubicable, cambió de previsión, se
  inscribió en otro centro o falleció. **Es la misma regla que el P6 de SM** (ver
  `SP_P6_poblacion_plan.md`), así que probablemente se reusa `programas/poblacion.py`.
- **Grado de dependencia por Barthel:** leve **≥ 60** · moderada **40-55** · severa
  **≤ 35**. La severa también incluye a los **menores de 6 años** y a personas con
  diagnóstico **psiquiátrico o intelectual** con certificado del médico APS, aunque el
  Barthel no lo refleje. «Oncológica» = tiene alguna patología cancerígena.
- **DS = oncológica + no oncológica.** Las LPP (fila 37) **están incluidas** en esas
  dos filas.
- **PADDS en control** (filas 38-44): la persona ingresó al programa y se mantiene en
  atención, lo que exige **al menos 2 VDI en el período anual** y las acciones del plan
  de cuidado. Sus reglas de consistencia:
  - **R.1:** total = onco + no onco.
  - **R.2:** demencia, institucionalizada, LPP y NED son **subgrupos** del total. Una
    persona puede estar en varios o en ninguno. El Manual dice «constituyen
    necesariamente el total», pero es una redacción rara que no puede significar una
    partición: la fila 41 sola tiene 75 de 194.
  - Institucionalizada = vive en un ELEAM o similar (hogares SENAME), siempre que no sea
    un establecimiento de salud o penitenciario.
  - NED = indicación desde especialidad, por la Ley de alto costo.
- **CPU en control:** ingresado y en seguimiento, **con prestaciones mensuales en los
  últimos 12 meses** antes del corte, excluyendo a los egresados. El primer corte cubre
  del 1 de julio del año anterior al 30 de junio. Las filas onco progresivo / no
  progresivo siguen los criterios del GES 4.
  - **R.5:** total = H + M.
  - **R.6:** total = Σ rango etario.
- **R.4:** escribir **0 explícito** en Migrantes.

*(RAYEN: por confirmar)* Se probaría con el formulario **Programa Dependencia, PADDS y
CPU** vigente al corte: «Tipo de Dependencia», «Tipo de Paciente», «Lesión por
Presión», «Estado PADDS», «Estado CPU» y «Enfermedad (No) Oncológica». Faltan por
ubicar los campos de demencia, institucionalización (¿alerta ELEAM?) y NED. **La regla
de «2 VDI anuales» se cruza con la A26·A.1**: quien está en el PADDS sin 2 VDI no
debería contar.

**Estructura que ya se ve:** el bloque *Atención domiciliaria* (38-44) repite el bloque
*Dependencia severa* (35-37): **todas las personas con DS de junio estaban en el
PADDS**. El Manual no obliga a que sea así: calcular los dos bloques por separado y, si
difieren, mostrarlo.

---

## 2. P3 · B — Cuidadores de personas con DS (SP fila 52)

Columnas de input:
- `C`/`D` Hombres / Mujeres.
- `E` Capacitados/as · `F` Con Examen de Medicina Preventivo vigente · `G` Con
  condiciones crónicas en control · `H` Con apoyo monetario · `I` En espera de apoyo
  monetario · `J` Con evaluación de sobrecarga vigente · `K` Mayores de 65 · `L`
  Atendidos por ECICEP · `M` En programas de apoyo intersectoriales · `N` Con atención
  preferente.
- `O` Pueblos originarios · `P` Migrantes.

Fórmulas en `B`, `Q` y las validaciones.

| Fila | Casillas llenas |
|---|---|
| 52 | `C52` H: **24** · `D52` M: **170** · `E52` Capacitados: **194** · `F52` EMP vigente: **124** · `G52` Crónicos en control: **156** · `H52` Apoyo monetario: **31** · `I52` En espera de apoyo: **105** · `J52` Sobrecarga vigente: **194** · `K52` >65: **69** · `L52` ECICEP: **6** · `M52` Intersector: — · `N52` Atención preferente: **77** · `O52` P.Orig: **3** · `P52` Migr: **5** |

**Reglas (Manual págs. 67-70):**
- **Universo:** los cuidadores de las personas **del PADDS**, uno por familia (el
  **cuidador principal** que identifica el programa). Aquí 24 + 170 = **194**, igual
  que P3·A fila 38.
- **`E` Capacitado:**
  - Cuidador **nuevo** (ingresó al PADDS en el período anual): **al menos 6 sesiones**
    de 45 min en el año.
  - Cuidador **antiguo**: al menos **4 sesiones**.
  - Las sesiones son las de la **A27** (4 áreas: autocuidado, cuidados de la persona,
    redes, fin de vida y duelo), grupales o remotas. **El módulo tiene que contar
    sesiones por cuidador en las atenciones grupales**, así que el participante tiene
    que venir con RUN.
- **`F` EMP vigente:** **EMPA** si el cuidador tiene menos de 65 años, **EMPAM** si
  tiene 65 o más. Es el EMPA/EMPAM que mencionó la jefa.
- **`G` Crónicos en control:** el Manual define a los cuidadores «**sin** examen
  preventivo, ingresado a programa de salud» (con controles al día). La etiqueta de la
  planilla, en cambio, dice «con condiciones crónicas en control». *(Hay que confirmar
  si son la misma casilla.)*
- **`H` / `I`:** reciben o esperan el **estipendio del MDS**. R.1: `H` ≤ total.
- **`J` Sobrecarga vigente:** tiene una evaluación de sobrecarga (Zarit) en los
  **últimos 11 meses 29 días**.
- **`K`:** tiene **65 años o más**. La etiqueta dice «mayores de 65», pero la
  definición incluye los 65.
- **`N` Atención preferente:** según el reglamento y el protocolo del CESFAM.
- **`L` ECICEP** y **`M` Intersector:** los atiende la estrategia o participan en un
  programa de apoyo intersectorial.

> Nota: el Manual menciona también «cuidadores capacitados **con apoyo monetario**»,
> pero la planilla V1.2 no tiene esa columna. El Manual quedó atrás de la planilla.

`E` y `J` al **100 %** (194 de 194) **es correcto**: hubo un operativo con una
universidad que evaluó y capacitó a todo el universo de cuidadores (jefa PDS, sep-2026).
En otro semestre no hay que esperar un 100 %.

---

## 3. P5 · A — Personas mayores por condición de funcionalidad (SP filas 12-19)

Columnas de input: edad × sexo en pares H/M, `F`/`G` 65-69 · `H`/`I` 70-74 · `J`/`K`
75-79 · `L`/`M` 80-84 · `N`/`O` 85-89 · `P`/`Q` 90-94 · `R`/`S` 95-99 · `T`/`U` 100+.
**La P5 abre 80+ en quinquenios hasta 100+, y la P3 no.** Además `V`/`W` Pueblos
originarios H/M · `X`/`Y` Migrantes H/M · `Z`/`AA` ELEAM H/M.

| Fila | Etiqueta | Casillas llenas | Σ |
|---|---|---|---|
| 12-14 | Autovalente sin riesgo · con riesgo · riesgo de dependencia | — (vienen del **EFAM**: otro equipo) | 0 |
| 16 | Dependiente leve | — | 0 |
| 17 | Dependiente moderado | `M17` 80-84 M: **1** | 1 |
| 18 | Dependiente grave | `F18` 65-69 H: **3** · `G18` M: **6** · `H18` 70-74 H: **3** · `I18` M: **8** · `J18` 75-79 H: **7** · `K18` M: **12** · `L18` 80-84 H: **8** · `M18` M: **7** · `N18` 85-89 H: **2** · `O18` M: **20** · `P18` 90-94 H: **5** · `Q18` M: **16** · `R18` 95-99 H: **2** · `S18` M: **6** · `U18` 100+ M: **1** · `W18` P.Orig M: **1** · `X18` Migr H: **1** · `Y18` Migr M: **2** | 106 |
| 19 | Dependiente total | `F19` 65-69 H: **2** · `G19` M: **1** · `H19` 70-74 H: **2** · `I19` M: **3** · `J19` 75-79 H: **3** · `K19` M: **6** · `L19` 80-84 H: **2** · `M19` M: **7** · `N19` 85-89 H: **1** · `O19` M: **10** · `Q19` 90-94 M: **7** · `S19` 95-99 M: **4** · `T19` 100+ H: **1** · `U19` M: **2** · `V19` P.Orig H: **1** · `W19` P.Orig M: **3** · `Y19` Migr M: **2** | 51 |

**Reglas (Manual págs. 92-94):**
- **«En control»:** tiene **65 años o más** y un **EMPAM con su plan de atención**, o un
  **control de seguimiento**, en los **últimos 11 meses 29 días** antes del corte. Un
  control cardiovascular al día **no reemplaza** el EMPAM.
- **Funcionalidad:**
  - **EFAM** (filas 12-14) para los autovalentes.
  - **Índice de Barthel** para quien necesita a un tercero en las actividades de la
    vida diaria. Da leve, moderada, grave o total (filas 16-19).
  - Grave y total se derivan al PADDS y **siguen contando aquí**.
  - La **correspondencia con la P3** es grave + total = «severa» y moderado =
    «moderada».
- **Total** = la suma de las 7 condiciones. Pueblos originarios y migrantes quedan
  **contenidos** en el conteo por edad y sexo.
- **R.1/R.2:** escribir **0 explícito** en Migrantes y en Pueblos originarios.

*(RAYEN: por confirmar)* En el SA, la A05·K/L leen el Barthel como **sección del
formulario EMP** (EMPAM). Falta ver si el formulario «Índice de Barthel» aparte, que
usa la jefa, llena esa sección o va por otro lado.

---

## 4. P5 · B — Estado nutricional (SP filas 34-37)

Mismas columnas que la P5·A.

| Fila | Etiqueta | Casillas llenas | Σ edad |
|---|---|---|---|
| 34 | Bajo peso | `F34` **1** · `G34` **2** · `H34` **1** · `I34` **1** · `J34` **4** · `K34` **3** · `M34` **5** · `O34` **5** · `P34` **1** · `Q34` **7** · `S34` **2** · `T34` **1** · `V34` P.Orig H: **1** | 33 |
| 35 | Normal | `F35` **3** · `G35` **3** · `H35` **3** · `I35` **7** · `J35` **3** · `K35` **10** · `L35` **8** · `M35` **5** · `N35` **3** · `O35` **19** · `P35` **3** · `Q35` **10** · `R35` **1** · `S35` **7** · `U35` **2** · `W35` P.Orig M: **2** · `Y35` Migr M: **3** | 87 |
| 36 | Sobrepeso | `G36` **1** · `J36` **2** · `K36` **2** · `L36` **2** · `M36` **3** · `O36` **1** · `P36` **1** · `Q36` **3** · `R36` **1** · `S36` **1** · `U36` **1** · `W36` P.Orig M: **1** · `X36` Migr H: **1** | 18 |
| 37 | Obeso | `F37` **1** · `G37` **1** · `H37` **1** · `I37` **3** · `J37` **1** · `K37` **3** · `M37` **2** · `O37` **5** · `Q37` **3** · `W37` P.Orig M: **1** · `Y37` Migr M: **1** | 20 |

**Reglas (Manual pág. 96):** es la **misma población de la P5·A**, clasificada por el
estado nutricional del EMPAM. En dependencia moderada, grave o total, cuando no se puede
medir peso y talla, vale la **apreciación diagnóstica** del profesional. Regla de
consistencia: **la P5·B tiene que igualar a la P5·A por rango etario y sexo.** En junio
calza en las 21 columnas, incluidos pueblos y migrantes.

---

## 5. Cruces

| Cruce | Valores | ¿Calza? |
|---|---|---|
| P3·A 38 = 35 + 36, casilla por casilla · 39 = 35 · 40 = 36 · 43 = 37 | 194 = 20 + 174 | ✅ (todos los DS estaban en el PADDS) |
| Cuidadores P3·B (`C` + `D`) = personas en atención domiciliaria (P3·A 38) | 194 = 194 | ✅ |
| P5·B = P5·A, columna por columna (regla del Manual) | 21 de 21 columnas iguales | ✅ |
| Personas mayores de P5·A (grave + total) contra DS de 65+ en P3·A 38, por banda | 70-74 y 75-79: idénticas · **65-69: P3 8 H / 4 M, P5 5 H / 7 M** · 80+: P3 21 H / 81 M, P5 21 H / 80 M (+1 moderado en 80-84 M) | ❓ |
| Pueblos originarios 65+: P3 (`AO`/`AP`, todas las edades) contra P5 (`V`/`W`) | P3: 0 H / 5 M · P5: 1 H / 4 M | ❓ |
| LPP: stock de la P3 de junio (fila 37) contra la A05·J 150 del SA de agosto | Casi la misma distribución (18 contra 22; 80+ M: 12 contra 13) | ℹ️ Refuerza que la A05·J 150 se llenó con el stock. **No es pega nuestra auditarlo**: el módulo calculará los ingresos según la regla |

**El descuadre de sexo en 65-69 años** (3 personas) y en pueblos originarios (1) no es
de conteo: el total por banda calza. Hipótesis: la P3 (formulario PDS) y la P5 (EMPAM)
**leen el sexo de lugares distintos**, uno el registral y otro el de identidad de
género. Es el mismo problema que dieron los TRANS en el SM (1.5.5). Revisarlo cuando
estén los exports; el módulo tiene que tomar el sexo de **una sola fuente** para las
dos hojas.

---

## 6. Lo que falta para diseñar el módulo

1. **Exports de formularios** (como en el SA): Programa Dependencia, PADDS y CPU (con la
   sección Cuidador) · Zarit · **Barthel** · **EMP/EMPA/EMPAM** (el del cuidador para
   P3·B `F`, el de la persona mayor para P5). Además, **atenciones grupales con el RUN
   del participante**, para contar las sesiones por cuidador (P3·B `E`).
2. **Reuso:** la regla de «en control» de la P3 (citación vigente, abandono a los 11 m
   29 d) es la del P6 de SM. Revisar `programas/poblacion.py` antes de escribir nada
   nuevo.
3. **Preguntas para la jefa PDS:**
   - ¿Cómo se consolida la P5 del CESFAM con la del Programa del Adulto Mayor?
   - ¿El formulario «Índice de Barthel» alimenta la sección Barthel del EMPAM?
   - ¿La columna `G` de P3·B es «con crónicos en control» o «sin EMP, pero ingresado a
     un programa», como la define el Manual?
   - ¿Qué campos del formulario PDS dan demencia, NED, apoyo monetario, intersector y
     atención preferente?
