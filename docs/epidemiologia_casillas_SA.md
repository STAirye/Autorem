<!--
This document was generated with the assistance of Claude Opus 5.5 (Anthropic).
The human author reviewed, modified, and integrated the content.

Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
Copyright (C) 2026 Simon Tobar
SPDX-License-Identifier: GPL-3.0-or-later
Version: 2.0.29
-->

# Epidemiología — A04 secciones P a U contra el Maestro y el Comentado (oct-2026)

Punto de partida del módulo de **Epidemiología**, que es una fila nueva en la matriz de
programas (CLAUDE.md §9). **Contexto:** hoy el CESFAM **no reporta NINGUNA** actividad de
epidemiología en el REM, aunque las actividades se hacen. Este documento cruza la tabla
que armó el equipo (qué actividad de RAYEN alimenta cada casilla) contra lo que dicen el
Maestro y el REM Comentado. **El hallazgo principal está en el §2, y no es de código:**
la mitad de la tabla apunta a actividades que no alimentan el A04.

**Fuentes:**
- **Tabla del equipo** — `refs_tablas/Tabla_Actividades_RAYEN_Epidemiologia_2026.xlsx`
  (el original se llamaba «ACTIVIDADES RAYEN PARA REM EPIDEMIOLOGÍA 2026 2.0»). Es una
  copia limpia con los valores de celda solamente: el original trae el nombre de quien lo
  armó en las propiedades y 17 controles ActiveX pegados. Columnas: `SECCIÓN`,
  `CONCEPTO`, `ACTIVIDAD RAYEN` (C), una nota libre (E) y `OTRAS ACTIVIDADES
  EPIDEMIOLÓGICAS` (G). Encabezado: *«Estas actividades se encuentran en perfil de rayen,
  "Otras actividades para la gestión"»*.
- **Comentado** — `refs_tablas/REM_Comentado_Serie_A_2026_15-04-2026.xlsx`, hoja A04,
  filas 184-224 (las notas de celda dicen el módulo de RAYEN y la actividad literal).
- **Maestro** — `catalogos/maestro_slim.csv.gz` (actividad, estamento, NUM REM, sección).
- **Plantilla** — `refs_tablas/SA_26_V1.2.xlsm`, hoja A04, filas 184-224. **Coincide fila
  por fila con el Comentado** en estas secciones (aquí no hay corrimiento de versión,
  a diferencia del PDS).

---

## 1. Estructura de las casillas (SA_26 V1.2, hoja A04)

| Sección | Filas (conceptos) | Columnas | Módulo RAYEN (Comentado) |
|---|---|---|---|
| **P** Encuesta epidemiológica | Visita epidemiológica · A lugar de trabajo · A colegio/sala cuna/jardín · A grupo comunitario | Total · Un profesional/técnico · Dos o más profesionales/técnico | **Registro Atención Comunitaria** |
| **Q** Quimioprofilaxis para bloqueo | Vacunas · Inmunoglobulinas · Antibióticos · Antivirales · Antiparasitarios · Otros medicamentos | Total · <18 · 18-64 · 65+ · Lugar de trabajo · Institución · Grupos comunitarios | **Box / Pacientes citados** |
| **R** Toma de muestras para vigilancia | Sangre · Coprocultivo · Frotis hisopado nasofaríngeo · Aspirado · Hisopado de lesión cutánea | Total · <18 · 18-64 · 65+ | **Box / Pacientes citados** |
| **S** Seguimiento de casos y contactos | Llamadas a casos · a contactos · Visitas a casos · a contactos | Total · <18 · 18-64 · 65+ | **Box / Pacientes citados** |
| **T** Búsqueda activa institucional (BAI) | Sarampión-rubéola · Febriles · Otros eventos | Total · registros revisados <100 · 100-250 · >250 | **Registro Atención Comunitaria** |
| **U** Búsqueda activa comunitaria (BAC) | Febriles · Otros eventos | Total de unidades revisadas | **Registro Atención Comunitaria** |

Reglas del Comentado que el módulo tiene que respetar:
- **P · columnas:** «Un profesional/técnico» = la atención la registra un profesional y
  se agrega UN técnico en «Profesionales que participaron en la atención». «Dos o más»
  = se agregan uno o más profesionales **y** un técnico.
- **Q · total** = suma de las tres columnas de destino (lugar de trabajo, institución,
  grupos comunitarios). Cada destino es **una actividad distinta** en RAYEN (§2).
- **T y U:** en el campo «Entidad comunitaria» va el centro donde se hace el registro.
- El Comentado tiene una errata en U: la fila 224 dice «BAI otros eventos» y es BAC.

## 2. Cruce sección por sección

| Sección | Actividad que exige el Comentado | ¿En el Maestro? | Qué dice la tabla del equipo | Veredicto |
|---|---|---|---|---|
| **P** | `Encuesta epidemiológica - Visita epidemiológica` · `- A lugar de trabajo` · `- A colegios, salas cuna, jardín infantil` · `- A grupo comunitario` | Solo la primera (A04·P), y habilitada para **un solo estamento** (Enfermero/a). Las otras tres **no están** | `Otras visitas integrales - Visita epidemiológica (Individual)` | ❌ **Esa actividad cuenta en el A26·B** (visitas en domicilio), **no en el A04·P**. Con la tabla tal cual, P sale siempre en 0 |
| **Q** | `Entrega de quimioprofilaxis para bloqueo epidemiológico - <insumo> - {Lugar de trabajo · Institución · A grupo comunitario}` (6 × 3 = **18 actividades**) | ✅ las 18, A04·Q, 43 estamentos | Una línea por insumo con los tres destinos juntos | ✅ en el fondo. Ojo: en RAYEN son **tres actividades distintas** por insumo, no una |
| **R** | `Toma de muestras para vigilancia epidemiológica - N° muestras de …` (5) | ✅ las 5, A04·R | Igual, literal | ✅ calce exacto |
| **S** | `Seguimiento de casos y contactos/expuestos … - Llamadas/Seguimiento - N° de …` (4) | ✅ las 4, A04·S | Igual, literal | ✅ calce exacto |
| **T** | `Busqueda activa institucional (BAI) de casos - BAI <evento> - <rango de registros>` (3 × 3 = **9 actividades**) | ❌ **ninguna** | `Ag-Investigación Epidemiológica` para las tres filas | ❌ esa es `AG_Investigación Epidemiológica`, **REM-Gestión**: no alimenta ningún REM, y aunque lo hiciera no distingue evento ni rango |
| **U** | `Busqueda activa comunitaria (BAC) de casos - BAC febriles` · `- BAC otros eventos epidemiológicos` | ❌ **ninguna** | `AG-Busqueda activa de casos ENO` | ❌ es `AG_Búsqueda activa de casos de ENO`, **REM-Gestión** (6 estamentos) |

**Por qué no se reporta nada (hipótesis, falta confirmarla con datos, §4):**
1. **P, T y U** se registran en el **Registro de Atención Comunitaria**, no en el box. La
   tabla los manda a actividades de gestión (`AG_…`) o a una del A26, así que **aunque
   se registren, nunca llegan al A04**. Las actividades de T y U, y tres de las cuatro
   de P, ni siquiera están en el Maestro: probablemente viven en el catálogo del módulo
   comunitario, que el Maestro no cubre (sin verificar).
2. **Q, R y S** sí apuntan bien. Si igual salen en 0, el equipo registra otra cosa en
   el box: lo más probable son las `AG_…` de la columna G (§3), que son de gestión.
3. El encabezado de la tabla lo dice solo: *«se encuentran en perfil … Otras actividades
   para la gestión»*. **Todo lo que es gestión, por definición, no va a ningún REM.**

## 3. Columna G — «Otras actividades epidemiológicas»

Las 16 son **REM-Gestión** en el Maestro: no alimentan ninguna casilla. Sirven para
auditar qué se hace, pero no suman al A04. Los nombres de la tabla **no son literales**
(`AG-` por `AG_`, erratas): el módulo tiene que buscar el nombre del Maestro, nunca el
de la tabla.

| Tabla del equipo | Nombre en el Maestro | Estamentos |
|---|---|---|
| AG- Agotamiento por calor | `AG_Agotamiento por Calor` | 59 |
| AG- Notificación caso de ENO | `AG_Notificación de caso de Enfermedad de Notificación Obligatoria (ENO)` | 6 |
| AG- Notificación en epidemiología (CESFAM) | `AG_Notificación en epivigila (En cesfam)` | 4 |
| AG_ Notificación en epidemiología (Terreno) | `AG_Notificación en epivigila (En terreno)` | 4 |
| Resultado de test negativo / positivo antígeno-PCR covid-19 | `AG_Resultado Negativo/Positivo Test Antígeno/PCR COVID-19` | 57 |
| AG-Toma de muestras PCR viruela del mono | `AG_Toma de muestra de PCR Viruela del Mono` | 8 |
| AG Toma de muestras test de antígeno | `AG_Toma de Test de Antigeno` | 58 |
| AG Visita epidemiológica adulto mayor institucional para vigilancia ENO | `AG_Visita epidemiológica adulto mayor institucionalizado` | 57 |
| AG Visita epidemiológica adulto mayor domiciliaria para vigilancia ENO | `AG_Visita epidemiológica domiciliaria para vigilancia de ENO` | 6 |
| Consulta telefónica post covid-19 | `Consulta Telefonica Post - COVID-19` | 1 |
| Derivación a inmunización | `Derivacion a Inmunizacion (Actividad de Gestión)` | 16 |
| Hisopado nasofaringeo | `Hisopado Nasofaringeo` (exacto) | 11 |
| Otras visitas integrales | `Otras visitas integrales` (exacto, gestión) | 16 |
| Toma de muestra epidemiológica en domicilio | `Toma de muestra en epidemiología (domicilio)` | 5 |
| Toma de muestra epidemiológica en *(celda truncada)* | probablemente `Toma de muestra en epidemiología (sala)` | 5 |

La columna E es una nota de registro para brotes (consejería, vigilancia, visita, educación
de prevención de brote, «lo que corresponde a REM de llamados casos y contactos»); no
nombra actividades nuevas.

**Del Maestro, cercanas y que la tabla no menciona** (todas gestión, salvo indicación):
`AG_Encuesta Epidemiológica - Con Riesgo` / `- Sin Riesgo` (43 estamentos: candidata
fuerte a ser lo que hoy se registra en vez del P), `AG_Bloqueo epidemiológico
contactos/expuestos de ENO`, `Vigilancia Epidemiologica`, `Consulta Epidemiologica`,
`Rescate epidemiológico)`. Y fuera del A04, el **A19a·D** (*Actividades comunitarias de
orientación y/o educación en el marco epidemiológico*, 60 estamentos), que es donde cae
la «educación para prevención de brote» de la columna E.

## 4. Qué falta para planificar el módulo

**Datos (los consigue el autor; nada de esto entra al repo):**
1. **Un mes de ADA IRIS** (`Atenciones/Diagnósticos/Actividades`), el mismo export que
   usa SM Actividades. Con eso se cuenta qué actividades de epidemiología se registran
   HOY en el box, y cuánto. Confirma o tira la hipótesis del §2.
2. **El export del Registro de Atención Comunitaria.** Hay que averiguar qué reporte de
   RAYEN lo trae: puede ser el mismo «Atenciones Grupales» (tiene `MULTIPROFESIONAL`,
   que serviría para las columnas de P) u otro. Sin él, P, T y U no se pueden tabular.
3. Confirmar en RAYEN si las actividades BAI/BAC y las tres de P que faltan en el
   Maestro **están habilitadas** en el establecimiento, y para qué estamentos.

**Decisiones para el equipo (no son de código):**
- **El registro tiene que cambiar.** Con las `AG_…` ninguna herramienta puede llenar el
  A04: el dato no existe. La corrección es registrar las actividades literales del
  Comentado (§2). Un módulo que «adivine» el A04 desde actividades de gestión sería un
  número plausible pero inventado (regla dura 2).
- **T necesita el rango de registros revisados**, que va EN el nombre de la actividad
  (<100, 100-250, >250). Si no se registra así, no hay de dónde sacarlo.
- El encargado de P tiene que agregar a los participantes en «Profesionales que
  participaron»: si no, todo cae en una columna o en ninguna.

**Diseño probable (a confirmar en el plan):**
- Nombre: `modulos/rem_a04_pu_epidemiologia.py`, `id` `a04_pu_epidemiologia`.
- **Q, R y S** son casi gratis: el ADA ya se carga en SM Actividades
  (`rem_sm_actividades`), las actividades calzan exacto con el Maestro, y los rangos
  etarios (<18, 18-64, 65+) salen de `AÑOS ATENCION`. Q cruza insumo × destino desde el
  nombre de la actividad.
- **P, T y U** dependen del export comunitario (punto 2): sin él, esas secciones van en
  la hoja LEEME como «no cubiertas», nunca en 0.
- Como auditoría (regla de la tabla intermedia), una hoja con las `AG_…` epidemiológicas
  registradas en el mes, con el aviso de que **no suman al REM**: es la evidencia para
  que el equipo vea que lo que hace no se está reportando.
- La columna G se puede volver una lista en el código (`ACT_EPI_GESTION`), con los
  nombres del Maestro, no los de la tabla.
