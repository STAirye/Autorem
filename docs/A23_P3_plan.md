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
| (control crónico Enfermera) | **E** · Enfermera/o | ✅ NO existe → no va (confirmado) |
| `Seguimiento Eu` | **F** · Enfermera/o | alta |
| `Seguimiento Kine` | **F** · Kinesiólogo/a | alta |
| `Morbi respiratoria` | **D** · Médico/a | ✅ dx sala + morbilidad + **solo médico** |
| `Espirometría (act)` | **I** · Espirometría **basal Y post BD** | ✅ se registran las dos |
| `KTR` | **I** · Sesiones KTR respiratoria | alta |
| `Educación Antitabaco` | **M.1** · Antitabaco | alta |
| `Autocuidado` | **M.1** · Autocuidado según patología | alta |
| `Inhaloterapia` | **M.1** · Uso terapia inhalatoria | alta |
| `Edu Integral Sala` | **M.1** · Educación integral salud respi | alta |
| `Vida Saludable` | **M.1** · Estilo de vida saludable | alta |
| `Otras` | **M.1** · Otras | media |
| `VDI Respi` | **N** · fila **162 "Otras visitas"** | ✅ con dx del programa |
| `Rehab Ses Educ` | **O** · Sesiones educativas | alta |
| `Rehab Ses Act Fca` | **O** · Sesiones actividad física | alta |
| `Rehab Conti` | **O** · Articulación continuidad | alta |
| `Encuesta calidad de vida` | **Q** | alta |
| `Ira Alta`·`Neumonia`·`Bronquitis`·`EPOC Exacerbado`·`Influenza`·`Coqueluche`·`Campaña Invierno` | **A** ingresos agudos, **POR DIAGNÓSTICO** | ✅ asma: confirmado + `Jxx` baja (rango x confirmar) |
| SALA (asma/EPOC/SBOR/FQ/otras) + Ingresado | **B/C** bajo control | ⚠ PowerBI madre + calc mes previo (prioridad baja) |

### Respuestas de Simón (confirmadas en día REM, ago-2026) ✅

1. **Sección A (ingresos)** = **todos POR DIAGNÓSTICO**. Caso especial **asma**:
   exige **confirmado + alguna `Jxx` "baja"**. Rango confirmado = **J09–J22 excepto
   J19** (infecciones respiratorias agudas bajas: influenza J09–J11, neumonías
   J12–J18, bronquitis/bronquiolitis aguda J20–J22; se excluye J19 'no especificado').
   ⚠ **Solo IRIS trae el CÓDIGO**; el **Administrativo trae el dx en TEXTO PLANO sin
   código** → en admin habría que mapear nombre→código (ver nota al final). Para el
   rango chico basta un `set`/`range` hardcodeado sobre el código de IRIS.
2. **Sección D** (morbilidad) = **diagnóstico de sala + actividad/morbilidad +
   registrado por MÉDICO**.
3. **Sección E · Enfermera/o**: **NO existe** el control de enfermera → no se computa
   (no va la fila / va 0). Cierra la duda del `⚠` de la tabla de arriba.
4. **Espirometría**: se registran **AMBAS**, basal y post BD → llenar las dos filas de
   la Sección I (no una sola).
5. **VDI / Visitas** → fila **162 "Otras visitas"** de la Sección N, y **solo las que
   tengan diagnóstico del programa**.
6. **A/B/C bajo control** → **NO sale de estos insumos**: depende del **PowerBI madre**
   + una calculadora que compara el mes anterior con el actual (ver sección "Bajo
   control" abajo). Es un formulario/flujo aparte aún no incluido.

Pendiente de confirmar: rango exacto de `Jxx` baja (asma, punto 1); filas de **I** sin
indicador (flujometría, pimometría, tests) → se asumen 0/manual salvo aviso.

---

## Educación grupal (M.2) y talleres — PRE-ESCRITO (pendiente de implementar)

Estado (ago-2026): **los talleres grupales respiratorios aún NO se hacen** en el
CESFAM → hoy **no hay nada que contar** en M.2. Se esperan **en un par de meses**;
Simón ya envió las actividades **candidatas** al jefe de Respiratorio para que las
use al crearlas en RAYEN. Se deja **pre-escrito y comentado** en el módulo porque la
lógica es **casi idéntica a `rem_sm_actividades`** (conteo por asistencia del reporte
grupal, o por ATEN ID del ADA según el caso) → es poco código real.

**Hallazgo del Maestro (ago-2026):** hoy **ninguna actividad grupal respiratoria
tributa** — todo lo rotulado *grupal/taller* cae a `REM-Gestion`. Las candidatas que,
al implementarse, deberían apuntar a **A23 · M.2** (o reclasificarse en el Maestro):

| Actividad (Maestro) | Hoy clasificada | Debería (al activar) |
|---|---|---|
| `Taller Grupal Cesación Tabaco` | REM-Gestion | A23 · M.2 (educación grupal, tema tabaco) |
| `AG_GES TABACO Sesión 1–6` | REM-Gestion | A23 · M.2 (sesiones GES tabaco) |
| `Taller Prevencion Ira` | REM-Gestion | A23 · M.2 |
| `Taller Era descompensado` | REM-Gestion | A23 · M.2 |
| `Taller Rehabilitación Pulmonar` | REM-Gestion | A23 · O (rehab) / M.2 según defina el RT |

**Tabaco que YA tributa a A23 (individual, no grupal)** — referencia para no
duplicar cuando entre M.2:
- `Educación en Salas Individual -Antitabaco-` → **A23 · M.1** (Antitabaco), Enfermero.
- `VDI equipo IRA-ERA … Hogar Libre de Humo de Tabaco (Individual)` → **A23 · N**, Enfermero.

Tabaco que tributa a OTROS REM (fuera de A23): A27·F (intervención breve/mínima/
referencia), A19a·A.1 (consejerías individuales), A09·B (consejería breve odontólogo).

**Cuando se implemente M.2:** definir con el RT si el Maestro reclasifica esas
actividades a `REM-A23` (lo ideal) o si se listan explícitamente en el módulo;
validar contra un mes con datos reales (como se hizo con SM). Mientras tanto, esos
talleres caen a **saco vacío** (los caza el reporte de Trabajo perdido).

---

## Bajo control A/B/C — depende del PowerBI madre (prioridad BAJA)

El "bajo control" (ingresos/egresos crónicos, Secciones B/C) **no se calcula desde
atenciones ni desde el formulario SALA**: sale de la **base de datos del PowerBI
madre** + una **calculadora que compara el mes anterior con el mes actual** (altas/
bajas de la cohorte bajo control). La idea a futuro es **portar todo eso a autoREM**,
pero es **prioridad baja** (hoy vive en PowerBI + Excel y funciona). Relacionado con el
pendiente de "abandonos" y el "PowerBI madre" del roadmap (CLAUDE.md §12).

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

### CIE-10 como referencia (para admin plaintext → código)

El Administrativo trae el dx en **texto plano** (p.ej. "Bronquitis aguda") sin el
`J20`. Para replicar en admin las reglas por código (asma = J09–J22\J19, y los dx
agudos de la Sección A/D en general) haría falta un **mapa nombre↔código CIE-10**.
Fuente autoritativa = estándar público (OMS/DEIS Chile). *(Se está evaluando de dónde
tomar la tabla; pendiente — no decidir acá todavía.)*

Recordatorios: (a) el match por NOMBRE es frágil (RAYEN redacta distinto) → admin
seguirá PARCIAL/heurístico, con aviso de "fuente parcial"; (b) para el rango chico de
asma NO hace falta dataset alguno: basta `set` hardcodeado (`J09..J22` menos `J19`)
sobre el código de IRIS. El mapa CIE-10 completo solo suma si se ataca el admin-por-
nombre en serio (decisión aparte, prioridad baja).
