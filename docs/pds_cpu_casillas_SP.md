<!--
This document was generated with the assistance of Claude Opus 5.5 (Anthropic).
The human author reviewed, modified, and integrated the content.

Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
Copyright (C) 2026 Simon Tobar
SPDX-License-Identifier: GPL-3.0-or-later
Version: 2.0.20
-->

# PDS + CPU — casillas del SP_26 llenadas a mano (corte junio 2026)

> **ESTADO AL 2026-09-29 (fin del día). Reunión con la encargada PDS el 2026-09-30 en
> la mañana.** Este bloque es el punto de entrada del módulo PDS + CPU. El inventario
> está completo; el **plan del módulo todavía no está escrito**.
>
> **Hecho (commiteado):**
> - Inventario del SA (agosto) → [pds_cpu_casillas_SA.md](pds_cpu_casillas_SA.md). Su
>   §8 tiene los formularios, el campo RAYEN de cada casilla y las advertencias.
> - Inventario del SP (junio) → este doc, con las reglas del Manual P, los
>   indicadores PADDS (§5.1) y el Drive del equipo (§5.2).
> - 8 refs de formularios (PDS, Zarit, Barthel, EMP, en Admin e IRIS) vetados y en el
>   whitelist. Todavía **sin contrato**: va junto con el loader (skill `tests-fuentes`).
> - Skill `inventario-rem` (`.claude/skills/inventario-rem/`).
>
> **Pendiente, en orden:**
> 1. **Ref del Drive PDS.** Espera a que el equipo diga qué pestañas se usan de verdad.
>    - `refs_tablas/Drive_PDS_heads.xlsx` es una copia **sin fotos ni el comentario con
>      autor**, que pasó el escáner de PII sin hallazgos. Sigue **ignorada** por git.
>    - Antes del whitelist: el autor borra los comentarios de `Vacunacion 2025` (filas
>      con fecha y texto libre, `B44` incluida), se recorta a las pestañas en uso y se
>      repite la revisión enmascarada.
>    - Después: agregar `drive` a `DENY_NOMBRE` en `tools/limpiar_refs.py`, con un
>      comentario («Drive llenado a mano, varias tablas por pestaña, revisado a mano»)
>      y el header del `.py` a la versión actual. Sin eso, `test_refs_tablas` falla.
>      Luego el whitelist en `.gitignore` y el commit.
>    - **`refs_tablas/Drive 2_heads.xlsx` (el original) sigue ahí, ignorado, con 2 fotos
>      y 1 comentario con el nombre de su autor.** Sacarlo de `refs_tablas/` cuando la
>      copia limpia esté commiteada.
>    - `Datos madre/PAD/Drive 2 anonim.xlsx` (OneDrive) conserva **1 correo real** (fila
>      98) y **nombres de médicos** (`VDI MÉDICA`). Queda local, no circula.
> 2. **Preguntas para la encargada PDS** (ninguna bloquea el diseño):
>    - `28.- Alimentación Enteral?`: ¿equivale a la NED por Ley de alto costo? (§6)
>    - A26·A.1: ¿la evaluación del plan se registra solo en la segunda visita? (doc SA §7)
>    - A27·B: ¿de dónde salen los 14 y 22 sesiones? (doc SA §7)
>    - A05·J contra A05·V: ¿quiénes son los 11 DS que no están en el PADDS? (doc SA §7)
>    - Qué pestañas del Drive se usan (punto 1).
>    - Revisar los **pesos** de los indicadores: la tabla transcrita suma 95 % (§5.1).
> 3. **Escribir el plan del módulo**, autocontenido para implementar en otra sesión.
>    Decisiones que ya están tomadas y el plan tiene que respetar:
>    - Las casillas se ubican por **encabezado**, nunca por coordenada.
>    - Los campos del formulario se leen por **nombre con su número**.
>    - La P5 lleva **solo pacientes PDS**, porque el consolidador suma las planillas.
>    - La A26·C `C` y la A33·C/D/E: la primera la llena el módulo; la A33·C/D/E queda
>      vacía con aviso.
>    - El sexo del cuidador sale de Inscritos, o del override del Drive.
>    - El Drive funciona como override y fuente de avisos.
>    - Un mes anterior a 2023 da `ArchivoInvalido`.
>    - Revisar el reuso de `programas/poblacion.py` para la regla «en control».
> 4. Los scripts de trabajo de esta sesión (el generador del inventario, los
>    extractores) viven en el scratchpad. Al cerrar la rama, se archivan en
>    `docs/evanesced/` según la regla 7 de CLAUDE.md. La versión reutilizable ya es la
>    skill.

Continúa [pds_cpu_casillas_SA.md](pds_cpu_casillas_SA.md). Es la **Serie P**, o sea
**población en control**: un stock al corte semestral (junio y diciembre), no eventos
del mes. Se generó con la skill `inventario-rem`.

**Fuentes:**
- **SP**: `SP_26_V1.2 JUNIO 26 PDS.xlsm`, llenado a mano por el equipo PDS. Quedó en el
  OneDrive y no está en el repo.
- **Manual REM P 2026 v1.0 (DEIS)**: `OneDrive/REM SM/2026/MANUAL REM  P 2026 Version
  1.0.pdf`. P3 en las págs. 59-70 y P5 en las 91-96. De ahí salen las reglas de este doc.
- **No hay REM Comentado de la Serie P**, así que el Manual dice **qué** contar, pero no
  **de qué formulario o campo de RAYEN**. Los campos salen de los headers de los
  formularios (`refs_tablas/`, sep-2026). La tabla de formularios y las advertencias
  del lector están en el [§8 del doc SA](pds_cpu_casillas_SA.md#8-fuentes-rayen-confirmadas-headers-sep-2026).
- El Maestro no trae nada para P3 ni P5. Es esperable: la población en control sale de
  formularios, no de actividades.

**Formularios que usa el equipo** (encargada PDS, sep-2026): Barthel · Zarit ·
Programa Dependencia, PADDS y CPU · EMPA/EMPAM. **En la Serie P aparecen los cuatro**,
que en el SA faltaban. En RAYEN **un formulario alimenta a otro** (confirmado): el
«Indice de Barthel» llena el `5.-` del formulario PDS y el `119.-` del EMP.

---

## 0. Resumen

| Hoja · Sección | Qué es | Criterio (Manual) | Fuente RAYEN probable |
|---|---|---|---|
| P3 · A, filas 33-47 | Existencia por dependencia, PADDS y CPU | **Barthel**: leve ≥ 60 · moderada 40-55 · severa ≤ 35 (o certificado médico). «En control» = citado, sin abandono | Formulario **Programa Dependencia, PADDS y CPU** (el Barthel lo alimenta) |
| P3 · B | Cuidadores de las personas del PADDS | Capacitado = **6 sesiones** en el año (nuevo) o **4** (antiguo) · EMPA/EMPAM vigente · Zarit en los últimos **11 m 29 d** · estipendio MDS | Bloque **Cuidador** del formulario PDS; el **sexo** sale del Informe Inscritos (por RUT) |
| P5 · A, filas 16-19 | Mayores de 65 en control por funcionalidad | **EMPAM** (o control de seguimiento) en los últimos 11 m 29 d; funcionalidad por **Barthel** si depende de terceros | **EMP** (`119.- Nivel de Severidad`, que llena el Barthel) |
| P5 · B | Estado nutricional de la misma población | Del EMPAM. En dependencia moderada, grave o total, por apreciación diagnóstica | **EMP** `24.- Estado Nutricional` (adultos y PM) |

El resto de P3·A (respiratorios, epilepsia, TEA, Parkinson, etc.) y P5·A.1, C, D y E
quedaron vacíos: son de otros programas.

> ⚠ **La P5 es compartida con el Programa del Adulto Mayor.** Las filas 12-14 de P5·A
> (autovalente sin riesgo, con riesgo, riesgo de dependencia) salen del **EFAM** del
> EMPAM y las llena otro equipo. El Manual es explícito: «dependencia grave y total
> deben ser derivadas al PADDS, **siguiendo bajo control** por las acciones antes
> descritas para la población de personas mayores». Es decir, **el mismo paciente se
> cuenta en P3 (PDS) y en P5 (Adulto Mayor)**. **Resuelto (autor, sep-2026): las
> planillas de cada equipo se suman en un consolidador.** Por eso el módulo PDS escribe
> en la P5 **solo a sus pacientes**, los que tienen el formulario PDS vigente. Si
> contara a todo mayor de 65 con Barthel grave o total, el consolidador los sumaría dos
> veces (el Barthel se hace también fuera del PDS).

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

**Campos RAYEN** (formulario PDS, el último vigente al corte por paciente):

| Filas | Campos |
|---|---|
| 33-36 | `1.- Tipo de Paciente` (onco / no onco) · `7.- Tipo de Dependencia` · `8.- Estado Dependencia` (para saber si sigue en el programa) |
| 37 / 43 | `44.- Lesión por Presión` |
| 38-40 | `9.- Estado PADDS` |
| 41 | `21.- Demencia?` |
| 42 | `22.- Institucionalizado?` (en la P5 el EMP trae aparte `84.- Adulto Mayor Institucionalizado`) |
| 44 | `28.- Alimentación Enteral?`. OJO: el Manual pide *indicación desde especialidad por la Ley de alto costo*, que es más estricto; confirmar si el campo lo cubre |
| 45-47 | `10.- Estado CPU` · `11.- Enfermedad Oncológica` · `12.- Enfermad No Oncológica` (sic) |
| «En control» | `143.- Fecha próximo control` (citación vigente, abandono a los 11 m 29 d) |

`5.- Resultado Índice de Barthel` viene dentro del mismo formulario: es la severidad que
copió el Barthel. Se cruza contra `7.-` y se avisa si difieren. **La regla de «2 VDI
anuales» se cruza con la A26·A.1**: quien está en el PADDS sin 2 VDI no debería contar.

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
  tiene 65 o más. Es el EMPA/EMPAM que mencionó la encargada PDS.
- **`G` Crónicos en control:** el Manual define a los cuidadores «**sin** examen
  preventivo, ingresado a programa de salud» (con controles al día). La etiqueta de la
  planilla, en cambio, dice «con condiciones crónicas en control». **Resuelto (autor):
  vale la etiqueta. Son los cuidadores con crónicos en control, tengan o no EMP.**
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

**Campos RAYEN.** **Toda la P3·B sale del bloque Cuidador del formulario PDS**, así que
no hace falta contar sesiones en la A27 ni cruzar el EMP del cuidador. Los dos quedan
solo como chequeo.

| Columna | Campo |
|---|---|
| Universo | `73.- Tiene Cuidador?` = Sí · `74.- Estado Cuidador` vigente · identificado por `80.- Rut Cuidador` |
| `C`/`D` H/M | ⚠ **No está en el formulario, ni en ningún otro lado de RAYEN** (autor). Sale del **Informe Inscritos** por `80.- Rut Cuidador`; el Zarit `4.-` sirve de chequeo. Un cuidador no inscrito queda sin dato y se avisa |
| `E` Capacitados | `75.- Cuidador es Capacitado por el Programa`. Chequeo posible: las sesiones A27 del RUT del cuidador (6 si es nuevo, 4 si es antiguo) |
| `F` EMP vigente | `86.- Control Preventivo o Crónico vigente del Cuidador` + `87.- Fecha…`. **El indicador 4 del programa (§5.1) define `F` como «preventivo vigente O controles al día»**, que es exactamente lo que registra el campo 86: se lee directo. El EMP del cuidador (por RUT: EMPA si tiene menos de 65, EMPAM si tiene 65 o más) queda como chequeo |
| `G` Crónicos en control | `90.- Cuidador con Condiciones Crónicas en Control en Ce…`, independiente del EMP (autor) |
| `H` Con estipendio | `25.- Estipendio MIDESO?` = **SI**. Sus valores son SI / NO / vacío; **un vacío es «sin dato», no «NO»**, y se cuenta en la LEEME |
| `I` En espera de estipendio | **No está en el formulario** (`25.-` solo trae SI/NO). Sale del **Drive PDS**, `ESTIPENDIO = ESPERA` (§5.2). Si no hay Drive, el módulo la deja vacía y avisa |
| `J` Sobrecarga vigente | `88.- Zarit Abreviado del Cuidador` + `89.- Fecha Vigencia Zarit…` (vigente = dentro de los 11 m 29 d) |
| `K` 65 o más | `82.- Edad Cuidador` o `81.- Fecha Nacimiento Cuidador` al corte |
| `L` · `M` · `N` | `91.- …ECICEP` · `92.- …Apoyo Intersectorial` · `93.- …Atención Preferente` |
| `O` / `P` | Pueblo originario y migrante **del cuidador**: no están en el formulario, así que salen de su propia ficha (por `80.- Rut`) |

`E` y `J` al **100 %** (194 de 194) **es correcto**: hubo un operativo con una
universidad que evaluó y capacitó a todo el universo de cuidadores (encargada PDS, sep-2026).
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

**Campos RAYEN** (formulario **EMP**, que hoy incluye el EMPAM):

| Qué | Campos |
|---|---|
| Vigencia | `1.- Fecha Vigencia` · `2.- Estado del Examen` · `78.- Estado del paciente` / `79.- Motivo de estado EGRESO` |
| EFAM (filas 12-14) | `89.- Resultado EFAM Parte A` · `92.- Resultado EFAM Parte B` |
| Barthel (filas 16-19) | `118.- Puntaje` · **`119.- Nivel de Severidad`**. Es el mismo «Nivel de Severidad» del formulario «Indice de Barthel» (`12.-`), que probablemente lo alimenta. `121.-` y `125.-` también se llaman «Puntaje»: se leen **siempre con el número** |
| ELEAM (`Z`/`AA`) | `84.- Adulto Mayor Institucionalizado` |
| Seguimiento | `131.- Fecha Próximo Control` |

El Barthel suelto se hace también a usuarios que **no** son del PDS. Para la P5 manda
el EMP, y el Barthel suelto queda como chequeo.

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

**Campos RAYEN** (EMP): **`24.- Estado Nutricional`**, el de adultos y personas mayores
(autor). El `25.-`, con el mismo nombre, es el **pediátrico** (+2 / +1 / eutrófico / −1 /
−2) y aquí no se usa. Como los dos se llaman igual, se leen **siempre por el número**. En
Admin hay además `26.- Calificación nutricional según IMC`; se puede usar como chequeo.

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

## 5.1 Indicadores del programa PADDS (output posible del módulo)

Fuente: la pestaña `INDICADORES` del Drive del equipo PDS. Está como imagen, así que va
transcrita. La tabla original cita las **celdas del REM 2023**; abajo van traducidas a
las secciones del SA/SP 2026. **Otra prueba de que las coordenadas se corren entre
años**: la P3·B pasó de la fila 45 a la 52, y la A26·C de las filas 67-75 a las 64-69.

| # | Indicador | Numerador / denominador (REM 2023, según la tabla) | En el REM 2026 | Meta | Esperado jun · dic | Peso |
|---|---|---|---|---|---|---|
| 1 | % de personas con plan de cuidado integral elaborado y evaluado en el período | A26 F38:40 + G38:41 / P3 C35 | A26·A.1 `G` + `H` (filas 38-40, acumulado del período) / P3·A fila 38 total | 90 % | 45 % · 90 % | 30 % |
| 2 | Promedio de visitas de tratamiento y procedimiento a personas bajo control en el programa | A26 C67, 68, 74, 75 / P3 C35 | A26·C **`C` (N° de visitas)**, filas DS / P3·A fila 38 | 6 | 3 · 6 | 5 % |
| 3 | % de personas con DS **sin** lesiones por presión | (P3 C35 − C39) / C35 | (P3·A 38 − 43) / 38 | 92 % | 92 % · 92 % | 20 % |
| 4 | % de cuidadores con **examen preventivo vigente o controles al día** (OOTT MINSAL) | P3 F45 / B45 | P3·B `F52` / `B52` | 80 % | 40 % · 80 % | 5 % |
| 5 | % de personas con indicación de NED que reciben atención nutricional en domicilio | A26 C72 / P3 C40 | A26·C `U` (Atención nutricional a personas con NED) / P3·A fila 44 | 100 % | 50 % · 100 % | 5 % |
| 6 | % de cuidadores evaluados con Zarit en el período | P3 J45 / B45 | P3·B `J52` / `B52` | 90 % | 45 % · 90 % | 20 % |
| 7 | % de cuidadores capacitados en el período | P3 E45 / B45 | P3·B `E52` / `B52` | 90 % | 45 % · 90 % | 10 % |

**Qué sale de esto:**
- **El indicador 2 usa la A26·C `C` (N° de visitas)**, que el llenado manual de agosto
  dejó vacía (doc SA §3). Es una razón más para que el módulo la llene.
- **El indicador 4 define la P3·B `F` como «preventivo vigente O controles al día»**,
  que es justo lo que registra el campo `86.- Control Preventivo o Crónico vigente del
  Cuidador`. Es decir, **para el programa, `F` se lee directo del campo 86**, sin
  cruzarlo con el EMP. Eso corrige la nota del §2. Queda un solapamiento con `G`
  (crónicos en control): los dos incluyen a los cuidadores con crónicos al día.
- **El indicador 5 usa la A26·C `U`**, que también quedó vacía en agosto.
- **Los pesos suman 95 %**: 30 + 5 + 20 + 5 + 5 + 20 + 10. Puede ser un error de la
  tabla o de la transcripción. Revisarlo contra la imagen.
- Con la P3 de junio: ind. 3 = (194 − 18) / 194 = **90,7 %** (meta 92) · ind. 4 =
  124 / 194 = **63,9 %** (esperado 40) · ind. 6 y 7 = **100 %** (el operativo con la
  universidad). Los indicadores 1, 2 y 5 necesitan la A26 acumulada del período, no un
  mes suelto.

---

## 5.2 El Drive del equipo PDS (override y fuente de avisos)

Es una planilla de Google Drive, llenada a mano por el equipo PDS. Es el input más
difícil de automatizar: tiene ~22 pestañas, **los nombres de las pestañas funcionan
como nombres de tabla**, y hay pestañas con **varias tablas** (`Electrodependientes`
tiene 4). Su rol en el módulo: **override** de lo que RAYEN no trae o trae mal, y
**fuente de avisos** cuando no coincide con los formularios. El autor está definiendo
con el equipo qué pestañas se usan de verdad (sep-2026).

**Pestaña `PDS 2026`** (el padrón): 203 pacientes y 58 columnas, **una fila por
paciente**. Perfil sacado de una copia anonimizada; no se versiona ningún dato.

| Qué | Columnas | Valores |
|---|---|---|
| Condiciones | `GASTROSTOMIA` · `DEMENCIA` · `Paliativo oncologico` · `Paliativo NO oncologico` · `NANEAS` | SI / NO (`No` también) |
| Transversales | `P. ORIGINARIO` · `MIGRANTE` · `sector` (AZUL/ROJO/VERDE) · `PREVISION` | SI / NO |
| **Estipendio** | `ESTIPENDIO` | `CONCEDIDA` · `SI` · **`ESPERA`** · `NO` · `REVISAR` · `no postulable` |
| Dependencia | `DEPENDENCIA` | GRAVE / MODERADO / TOTAL (categorías del Barthel) |
| Cuidador | `SEXO` (**col 39**, la 2ª de ese nombre) · `EMPA/EMPAM/PSCV CUIDADORES` (texto libre) · `VIGENCIA EXAMEN` · `ZARIT` | `VIGENCIA EXAMEN`: SI / NO / NO APLICA / SIN REGISTRO |
| Checks | `ELECTRODEPENDIENTE` · `IRA / ERA` · `CUP` · `PAÑALES` · `BARTHEL` · `CONSENTIMIENTO INFORMADO` · `Capacitacion` · `plan` · `ACTA` | VERDADERO / FALSO / vacío |
| Contactos | `PRIMER CONTACTO ENF` · `SEGUNDO CONTACTO ENF` | 1 / vacío |
| VDI | `VDI MÉDICA` · `VDI NUTRICIONISTA` · … · `VDI PSICOLOGIA PACIENTE` | Fechas, texto y números mezclados |

**Qué resuelve:**
- **P3·B `I` (en espera de estipendio):** `ESTIPENDIO = ESPERA`. Es el dato que el
  formulario PDS no tiene (`25.-` solo trae SI/NO). Con esto se cierra esa pregunta.
- **El sexo del cuidador** (col 39): override del cruce con el Informe Inscritos.
- **NED:** la saca la pestaña `NED` del original (rutificada). `GASTROSTOMIA` **no**
  equivale a NED (autor).

**Quirks que el lector tiene que aguantar:**
1. **Nombres de columna duplicados o casi iguales:** `SEXO` ×2 (col 12 = paciente, col
   39 = cuidador), `sector`/`SECTOR`, `PREVISION`/`prevision`. La col 34 no tiene
   encabezado. **Se lee por orden y columnas vecinas, y con una firma que falle ruidoso
   si el orden cambia.**
2. **Categorías sucias:** `NO`/`No`, `F`/`f`, `FONASAB`/`ONASA B`/`Fonasa B`,
   `BAJOPESO`, `SIN REGSITRO`, `PACAM` con `???`/`C`/`N/C`. Se normalizan con un mapa
   explícito, y **lo que no está en el mapa va a avisos**, no a una categoría adivinada.
3. **Valores en la columna equivocada:** `ZARIT` trae `BAJO PESO`/`SOBREPESO`, que son
   estados nutricionales. Va a avisos para el equipo.
4. **En las columnas `VDI <profesional>`, un número es un error de digitación**. Por
   ejemplo, `45163` es el serial de Excel del 24-ago-2023. **No se reinterpreta como
   fecha en silencio: va a avisos.** El texto de `VDI MÉDICA` son nombres de médicos:
   no se lee ni se copia a ninguna salida.
5. En los checks, **el vacío es «sin dato»**, no FALSO.
6. El Drive trae RUT, nombre, dirección y teléfono, y **nunca entra al repo**. En
   `refs_tablas/` va a quedar solo el encabezado, con las pestañas que se usen.

---

## 6. Lo que falta para diseñar el módulo

1. **Exports de formularios:** ✅ se están bajando desde 2021 (PDS, Zarit, Barthel,
   EMP), con los refs vetados. Lo que queda abierto, con el detalle en el §8 del doc SA:
   - el **sexo del cuidador** no está en el formulario PDS;
   - hay **nombres de campo duplicados**;
   - el formulario PDS **no existe antes de 2023**;
   - `GENERO` **solo aparece en IRIS**.
2. **Reuso:** la regla de «en control» de la P3 (citación vigente, abandono a los 11 m
   29 d) es la del P6 de SM. Revisar `programas/poblacion.py` antes de escribir nada
   nuevo.
3. **Resuelto por el autor (sep-2026):**
   - La P5 se consolida **sumando** las planillas de cada equipo.
   - El Barthel **sí** llena el `5.-` del formulario PDS y el `119.-` del EMP.
   - P3·B `G` = crónicos en control, con o sin EMP.
   - `25.-` Estipendio vale SI / NO / vacío: no existe un valor «en espera».
   - EMP `24.-` = estado nutricional de adultos y personas mayores (el que usa la P5·B);
     `25.-` = pediátrico (+2 / +1 / eutrófico / −1 / −2).
4. **Preguntas que quedan para la encargada PDS:**
   - ~~P3·B `I`: ¿de dónde salen los 105 «en espera»?~~ **Resuelto:** el Drive PDS,
     `ESTIPENDIO = ESPERA` (§5.2).
   - `28.- Alimentación Enteral?`: ¿equivale a la NED por Ley de alto costo que pide el
     Manual? El autor presume que sí.
