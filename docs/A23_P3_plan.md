<!--
This document was generated with the assistance of Claude Opus 4.8 (Anthropic).
The human author reviewed, modified, and integrated the content.
Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# P3 — Plan: tablas agregadas del REM A23 (copy-paste al SA_26)

**Objetivo:** llevar el A23 a la misma lógica que SM Actividades — además del detalle
por paciente, generar **tablas agregadas edad×sexo por sección del template A23**,
listas para copiar-pegar al `SA_26` (hoja A23). Hoy el A23 solo entrega detalle +
Sección G + Sección H.

**No hay minimanual de A23** (a diferencia de la hoja "A SM"). El mapeo
indicador→celda hay que armarlo/confirmar tab-por-tab con Simón, como se hizo con SM.

---

## Lo que ya existe (insumo)

`rem_a23_respiratorio.procesar()` devuelve `fer` = **1 fila por RUN** con, por el MES:
- 27 indicadores `REMA23 …` en SI/NO (`_masks_simples` + compuestos).
- `Edad`, `Sexo`, `Sector`, demografía.
- Columnas SALA bajo control (asma/EPOC/SBOR/FQ/otras) + Ingresado.
- Secciones G y H ya agregadas.

**La agregación = por cada celda del template, contar pacientes con el indicador=SI,
desagregado por banda etaria × sexo.** (Igual patrón que `_grid` de `rem_sm_actividades`.)

---

## Layout del template A23 (SA_26) — secciones que reciben los indicadores

Todas con estructura: `PROFESIONAL/CONCEPTO | TOTAL(Ambos·H·M) | RANGO ETARIO Y SEXO`
(bandas: Menor de 1 año, 1-4, 5-9, 10-14, 15-19, 20-24, … cada una H/M).

| Sección | Filas (template) |
|---|---|
| **D** Consultas morbilidad respi en salas | Médico/a |
| **E** Controles crónicos | Médico/a · Enfermera/o · Kinesiólogo/a · TOTAL |
| **F** Seguimiento en agudos | Enfermera/o · Kinesiólogo/a · TOTAL |
| **I** Procedimientos | Espirometría basal · Espirometría post BD · Flujometría basal/post BD · Pimometría · Test provocación ejercicio · Test marcha 6 min · **Sesiones KTR respiratoria** · Toma muestra secreción |
| **M.1** Educación individual en salas | Antitabaco · Autocuidado según patología · Uso terapia inhalatoria · Educación integral salud respi · Estilo de vida saludable · Otras · TOTAL |
| **M.2** Educación grupal | (Nº sesiones / Nº participantes por tema — NO sale de atenciones) |
| **N** Visitas domiciliarias | Hogar libre humo · Muerte neumonía · O2 ambulatorio · Seguimiento telefónico · Otras visitas |
| **O** Rehabilitación pulmonar | Sesiones educativas · Sesiones actividad física · Articulación continuidad · (Planes act. física) |
| **Q** Encuesta calidad de vida | (resultado) |
| **A/B/C** Ingresos agudos/crónicos · Egresos | (probablemente del formulario SALA, no de los indicadores) |

---

## Mapeo PROPUESTO indicador → celda (⚠ CONFIRMAR con Simón)

| Indicador REMA23 | → Sección · fila | Confianza |
|---|---|---|
| `Control SALA Med (act)` | **E** · Médico/a | alta |
| `Control SALA Kine (act)` | **E** · Kinesiólogo/a | alta |
| (control crónico Enfermera) | **E** · Enfermera/o | ⚠ NO se computa hoy — ¿existe? ¿0? |
| `Seguimiento Eu` | **F** · Enfermera/o | alta |
| `Seguimiento Kine` | **F** · Kinesiólogo/a | alta |
| `Morbi respiratoria` | **D** · Médico/a | media |
| `Espirometría (act)` | **I** · Espirometría basal | ⚠ template separa basal/post BD |
| `KTR` | **I** · Sesiones KTR respiratoria | alta |
| `Educación Antitabaco` | **M.1** · Antitabaco | alta |
| `Autocuidado` | **M.1** · Autocuidado según patología | alta |
| `Inhaloterapia` | **M.1** · Uso terapia inhalatoria | alta |
| `Edu Integral Sala` | **M.1** · Educación integral salud respi | alta |
| `Vida Saludable` | **M.1** · Estilo de vida saludable | alta |
| `Otras` | **M.1** · Otras | media |
| `VDI Respi` | **N** · ¿Otras visitas? | ⚠ ¿cuál fila? |
| `Rehab Ses Educ` | **O** · Sesiones educativas | alta |
| `Rehab Ses Act Fca` | **O** · Sesiones actividad física | alta |
| `Rehab Conti` | **O** · Articulación continuidad | alta |
| `Encuesta calidad de vida` | **Q** | alta |
| `Ira Alta`·`Neumonia`·`Bronquitis`·`EPOC Exacerbado`·`Influenza`·`Coqueluche`·`Campaña Invierno` | **A** ingresos agudos / **D** consultas? | ⚠ dónde van los dx agudos |
| SALA (asma/EPOC/SBOR/FQ/otras) + Ingresado | **B** ingreso crónico / **C** egresos | ⚠ ¿desde SALA form? |

**Preguntas clave para Simón (próxima sesión):**
1. Los **dx agudos del mes** (Ira Alta, Neumonía, Bronquitis, EPOC exac, Influenza,
   Coqueluche) → ¿Sección A (ingresos agudos a sala), Sección D, u otra?
2. **Sección E · Enfermera/o** (control crónico): ¿hay un indicador de control por
   enfermería que falte, o va 0?
3. **Espirometría**: el template separa basal / post BD — ¿el indicador actual cuál es?
4. **VDI Respi** → ¿qué fila de la Sección N?
5. Secciones **A/B/C** (ingresos/egresos) → ¿se llenan desde el formulario SALA
   (Otros y Respi), o quedan manuales/fuera de alcance?
6. **M.2** (educación grupal) y filas de **I** sin indicador (flujometría, pimometría,
   tests) → confirmar que van 0 / manual.

---

## Implementación (una vez confirmado el mapeo)

1. **Bandas etarias A23**: definir la lista exacta del template (Menor de 1 · 1-4 ·
   5-9 · 10-14 · 15-19 · 20-24 · … — leer la fila de encabezado de una sección).
2. **`_grid` reutilizable**: portar/compartir la lógica de `rem_sm_actividades._grid`
   (Ambos·H·M + bandas × sexo). Candidata a mover a `rem_utils` (la usan SM y A23).
3. **Constructor de tablas por sección**: para cada sección, filas = (indicador o
   profesional) → `_grid` sobre `fer[fer[indicador]=="SI"]` con Edad/Sexo. Demografía
   si el template la pide (revisar bloque AN+ de cada sección A23).
4. **`escribir()`**: agregar una hoja por sección (A23_Seccion_D/E/F/I/M/N/O/Q) además
   del detalle + G + H.
5. **Validar** contra el REM manual de un mes (como SM) — tab por tab.
6. Tests sintéticos por sección. Bump de versión (Z).

**Archivos:** `modulos/rem_a23_respiratorio.py` (tablas + escribir), quizás
`programas/rem_utils.py` (mover `_grid`), `tests/test_a23.py`, docs.

**Ojo:** el admin/monitoreo es PARCIAL (dx sin código ICD) → varias secciones saldrán
incompletas desde admin; IRIS es la fuente plena (igual que el resto del A23).
