<!--
Documento de contexto importado desde Claude.ai → Claude Code (jul-2026).
Sin PII. Autor: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa.
SPDX-License-Identifier: GPL-3.0-or-later
Es la visión GENERAL del proyecto de automatización REM (workflows A y B). El
estado real y las decisiones de diseño del código viven en CLAUDE.md; este doc
es el traspaso original de contexto (referencia).
-->

# CONTEXTO: Automatización REM — CESFAM Dr. Luis Ferrada Urzúa
*Traspaso desde Claude.ai → Claude Code — julio 2026*

---

## CONTEXTO GENERAL

- **Autor:** Simón Tobar — Médico APS, CESFAM Dr. Luis Ferrada Urzúa (Maipú, SSMC)
- **Hardware:** i5, 16 GB RAM
- **Restricción crítica:** Todo procesamiento de datos es offline y manual. Ley 20.584 y Ley 21.719 prohíben subir datos identificatorios a servicios externos.
- **Stack:** Python, Power BI + Power Query, Excel
- **Sistemas fuente:** RAYEN (gestión clínica), IRIS (citas, inscritos), SIGGES, RNI, Telesalud

---

## LICENCIAS Y ENCABEZADOS

Todo código producido debe incluir al inicio:

```python
# This code was generated with the assistance of [modelo]. The human author reviewed, modified, and integrated the code.
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa
# License: GPL-3.0-or-later
```

Documentos distribuibles: CC BY-NC-SA 4.0.

---

## PLANILLAS TARGET

| Planilla | Descripción |
|---|---|
| `SA_26_V1_2.xlsm` | REM SA — actividades/prestaciones |
| `SP_26_V1_2.xlsm` | REM SP — población en control por diagnóstico |

---

## ARQUITECTURA GENERAL

```
RAYEN export (.xlsx) ──┐
                        ├──► Python ──► Excel output ──► copiar a SA/SP
Power BI export (.xlsx)─┘
```

Power BI no se toca desde Python. Python lee exports y genera output listo para copiar.

---

## SCRIPT EXISTENTE: egresos SM ✅

Procesa export RAYEN de formularios SM → detecta egresos (Alta / Traslado / Otras Causas) → genera hoja `A05_EGRESOS`.

**Quirk documentado:** `AÑO APLICACIÓN FORMULARIO` en RAYEN contiene la edad al momento del llenado del formulario, NO el año calendario. `EDAD PACIENTE` contiene edad al momento de descarga del reporte → ignorar para output A05.

> Estado actual del proyecto (mucho más avanzado que este traspaso): ver CLAUDE.md.
> Ya hay egresos + ingresos, perfiles IRIS/Admin, dispatcher GUI/CLI, tests.

---

## WORKFLOW A: Población PSM → CALCULADOR → SA A05 [EN DESARROLLO]

### Lógica

```
SP mes anterior (ANTIGUO) ──┐
                             ├──► CALCULO = NUEVO - ANTIGUO
SP mes actual (NUEVO) ───────┘
  positivo → INGRESOS → SA A05 casilla N
  negativo → EGRESOS  → SA A05 casilla O
```

Matriz de salida: diagnóstico × grupo_etario × sexo

### Input 1: Reporte Población PSM (export Power BI)

Una fila por paciente activo en programa SM.

**Campos demográficos:**
`Sexo`, `Género`, `Edad`, `Estado`, `Situación`, `Motivo Pasivación`, `Fecha Pasivación`, `Pueblo Originario`, `¿Originario o Migrante?`, `SENAME`, `Madre <5 años`, `¿Embarazada?`

**Diagnósticos (usar siempre columna `(form)` cuando existe par):**
`Violencia (form)`, `Violencia Tipo (form)`, `Violencia Victima o Agresor (form)`, `Abuso Sexual (form)`, `Suicidio (form)`, `Suicidio Tipo (form)`, `Depresión (form)`, `Depresión gravedad (form)`, `Depresión Leve/Moderada/Grave`, `Depresión Postparto (form)`, `Bipolaridad (form)`, `OH Perjudicial (form)`, `OH Dependiente (form)`, `Drogas Perjudicial (form)`, `Drogas Dependiente (form)`, `OH y Drogas (form)`, `Ansiedad (form)`, `Ansiedad TEPT/Pánico/TAG/Otras`, `Demencia (form)`, `Demencia gravedad (form)`, `Demencia Leve/Moderado/Avanzado`, `Esquizofrenia (form)`, `Adaptativo (form)`, `Conducta Alimentaria (form)`, `Retraso Mental (form)`, `Personalidad (form)`, `TDAH (form)`, `Oposicionista desafiante (form)`, `Ansiedad separación (form)`, `Otras Infancia/Adolescencia (form)`, `Otros (form)`

**Egresos precalculados por Simón (columnas propias del reporte PBI):**
- `alta` — cualquier col diagnóstico `(form)` == `"Egresado"` en el mes
- `traslado` — `Estado=="Pasivo"` & `Motivo Pasivación` in `["Cambio de Domicilio","Traslado de Inscripción"]` & fecha en mes, O instrumento == "Egreso por Traslado"

### Input 2: Formulario RAYEN control SM

Una fila por atención. Sheet2/Sheet3 siempre vacías (bug IRIS, ignorar).

**Demográficos:** `SEXO`, `GENERO`, `EDAD PACIENTE`, `NUMERO TIPO IDENTIFICACION`, `FECHA ATENCION`, `INSTRUMENTO`

**Diagnósticos por número de campo:**
| Número(s) | Diagnóstico |
|---|---|
| 4+5+7 | Violencia |
| 9+10 | Abuso/Violencia sexual |
| 11+12+13 | Suicidio |
| 18+19+20 | Depresión |
| 21+22 | Depresión Postparto |
| 23+24 | Bipolaridad |
| 31+32 | OH Perjudicial |
| 33+34 | OH Dependiente |
| 35+36 | Drogas Perjudicial |
| 37+38 | Drogas Dependiente |
| 39+40 | OH+Drogas |
| 41+42+43 | Ansiedad |
| 44+45+46 | Demencia |
| 49+50 | Trastorno Adaptativo |
| 51+52 | Esquizofrenia |
| 55+56 | Conducta Alimentaria |
| 57+58 | TDAH |
| 59+60 | Retraso Mental |
| 61+62 | Personalidad |
| 65+66 | Otros |
| 69+70 | Oposicionista Desafiante |
| 71+72 | Ansiedad Separación |
| 73+74 | Otros Infancia/Adolescencia |

### Reglas de transformación

**Trans:**
```python
trans = ((sexo=="Hombre") & (genero=="Femenina")) | ((sexo=="Mujer") & (genero=="Masculino"))
```

**Grupos etarios:** 0-4, 5-9, 10-14, 15-19, 20-24, 25-29, 30-34, 35-39, 40-44, 45-49, 50-54, 55-59, 60-64, 65-69, 70-74, 75-79, 80+

**TDAH truncamiento:** ⚠ DESACTUALIZADO — decía «edad >= 30 → bucket 25-29 en el SA».
En `SA_26_V1.2` la columna 25-29 está BLOQUEADA: el último rango reportable del bloque
«trastornos del comportamiento… de comienzo habitual en la infancia» (TDAH, disocial,
ansiedad de separación; filas 218-220 ingresos / 270-272 egresos) es **20-24**. La
plantilla MINSAL cambió. Sin límite en el SP. Ver `SP_P6_poblacion_plan.md` §5.0.1

**Violencia sexual:** `Abuso Sexual (form)` + `Violencia Tipo (form)` contiene "sexual" → mapear SOLO a violencia sexual (filas 8-9 CALCULADOR). Fila 12 (abuso sexual) = 0.

**Exclusiones comodín (nivel fila, antes de agregar):**

| Diagnóstico | Contar solo si |
|---|---|
| Trastorno Adaptativo | `COUNT(cols Depresión→Oposicionista desafiante + Personalidad→TGD == "SI") <= 1` |
| Otros Ansiedad | `COUNT(cols Depresión→Otras Infancia/Adolescencia + Demencia→TGD == "SI") == 0` |
| Otros Infancia/Adolescencia | `COUNT(cols Depresión→Asperger + Rett→TGD == "SI") <= 2` |

**Población en control (fila 4 SP):** `Estado == "Activo"` (no usar Situación)

### Fallecidos:
`Estado=="Pasivo"` & `Motivo Pasivación=="Fallecido"` & fecha en mes

---

## PENDIENTES WORKFLOW A (upstream — resolver antes de codear)

- [ ] Fobia social: no está en reporte PBI, se sacaba por descarte. Revisar source code reporte PBI, agregar columna.
- [ ] Trans: agregar cálculo al dashboard Power BI
- [ ] "Egreso por Traslado" como instrumento: agregar al reporte basal PBI
- [ ] Bipolaridad (dg) vs (form): hay pacientes legacy solo con (dg). Actualmente solo se cuenta (form), subestima levemente — aceptado.

---

## WORKFLOW B: Actividades → SA A03/A04/A06/etc [DIFERIDO]

Fuentes: IRIS (atenciones por instrumento/actividad), Telesalud, correo electrónico (consultorías), reporte espontáneos.
Ver `minimanual.xlsx` hoja A para mapeo de secciones.
Nota: A03 usa rangos etarios no estándar.

---

## NOTAS CLÍNICAS / QUIRKS

- RUT normalizado siempre a formato `XXXXXXX-X` (split por posición + guión + dígito verificador en mayúscula)
- Registros con DNI u otros identificadores no-RUT → eliminar fila antes de procesar
- RAYEN exporta fechas a veces como texto, requiere dos pasos de conversión (text → datetime → date)
- `AÑO APLICACIÓN FORMULARIO` = edad al llenado (útil). `EDAD PACIENTE` = edad al descargarlo (ignorar para A05)
- **RAYEN a veces exporta en `.xls` (formato viejo), no `.xlsx`** → openpyxl NO lee `.xls`; hay que "Guardar como .xlsx" o usar otro lector.
