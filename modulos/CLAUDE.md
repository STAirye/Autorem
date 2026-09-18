<!--
This document was generated with the assistance of Claude Fable 5 and Claude Opus 5 (Anthropic).
The human author reviewed, modified, and integrated the content.
Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# modulos/ — reportes REM

Se carga al trabajar en `modulos/`. Los `§N` son las anclas del [CLAUDE.md raíz](../CLAUDE.md).

## Checklist de módulo nuevo

- **Planilla de ejemplo** de cada export que lee, en `refs_tablas/`: **solo header**
  (skill `limpiar-refs`) y habilitada a mano en el whitelist del `.gitignore`. Si el
  módulo no la tiene, **preguntarle al autor si la crea** antes de seguir: sin ella,
  la próxima sesión no puede ver el formato sin tocar datos reales.
- Entrada en `programas/cobertura.py` (`test_cobertura` falla si falta).
- Mes vacío por `rem_utils.filtrar_mes`, nunca un filtro a mano (§3.1).
- Header con versión + bump **Y** (skill `versionar`).
- Fila en la tabla de abajo y en la matriz de programas (§9 raíz).

## Módulos

| Archivo | Qué hace / decisiones clave |
|---|---|
| `rem_a05_o_egresos.py` | **A05 casilla O.** Egresos Alta/Traslado/Otras Causas. Módulo fino sobre `rem_saludmental.marcar_eventos()`; `procesar`/`agregar_hoja` aceptan `mes=(año,mes)`. |
| `rem_a05_n_ingresos.py` | **A05 casilla N.** Gemelo de egresos: token ESTADO `INGRESO`, hoja `A05_Ingresos`. |
| `rem_a03_d3_instrumentos.py` | **A03 D.3** (PSC / PSC-Y / GHQ-12). Reporte distinto al formulario SM, con detección propia. Por aplicación: resultado de RAYEN + resultado calculado (DISAM) + discrepancia (compara BANDAS canónicas) + momento + estamento (IRIS directo; Admin vía `estamentos.py`). `procesar_unificado` → tabla D.3 copiable al SA + detalle auditable. Solo ingresados al PSM; «Sin riesgo» va al detalle pero no al D.3. Sin momento Ingreso/Egreso no hay D.3 (fail loud); sin puntaje, el nivel sale del resultado de RAYEN (`nivel_d3`, con aviso). El tamizaje (PSC-17/PHQ-9) es A03·H: fuera de alcance. |
| `rem_a23_respiratorio.py` | **A23, pandas** (port del PowerBI). 1 fila por RUN: 27 indicadores del mes + SALA bajo control + **Sección G** (inasistentes a control de crónicos: próximo control vencido por umbral de edad al último día del mes; SBO exige recurrente) + **Sección H** (citas IRA/ERA no asistidas, desde el reporte NSP, por estamento × tramo <20/≥20). Inputs aceptan LISTAS (histórico multi-año). Cálculos hacia atrás desde el mes reportado, nunca `TODAY()`. Monitoreo Admin = parcial (§5.1). |
| `rem_sm_actividades.py` | **SM Actividades, pandas:** A04·A24, A06·A.1, A19a·A.3, A26 VDI SM, A27, A32·F. Dos fuentes: **ADA** (cuenta ATEN ID distintos) y **Grupal** (cuenta ASISTENCIA con `Asiste=SI`, sin dedup). Mes por FECHA ATENCIÓN. **Validado casilla por casilla contra el REM manual.** Demografía AN–AV vía `rem_utils.marcar_demografia()` + `gestante_runs()` (ventana de 3 meses) + `trans_map()` (Inscritos opcional). Opcionales: Inscritos, Monitoreo Multiprofesional (composición de las VDI del A26) y Maestro. `ADA_TRIBUTAN` / `mask_tributa_ada` = fuente única de qué tributa. **Dotación:** cada evento se marca interno/externo/desconocido; las secciones se calculan sobre `E[en_rem]` y la hoja `Externos_Delta` compara. **Consultorías A06·A.2 = manuales** porque el centro no registra esa actividad, no porque no exista. Known issue: el grupal no trae demografía. |
| `rem_sm_trabajo_perdido.py` | **Auditoría «saco roto», NO tributa.** Atenciones SM-ish (`mental`/`demencia`) que no caen en ninguna casilla SM, y quién las registra. Autoridad = Maestro de Actividades; si la actividad no está en el Maestro, heurística. **`EXCLUIR_SMISH`:** lo que la palabra gatillo describe a la persona y no a la atención (hoy las 24 VDI del PADDS = A26·A1) sale del universo con conteo en el log. Es ruteo, no borrado: futuro `rem_a26_domiciliaria`. |
| `rem_sp_p6_poblacion.py` | **SP·P6 A.1, pandas.** Grilla filas 13-58 × 17 bandas × sexo + demografía AN..AX desde `PSM_Poblacion`. La máscara de celdas protegidas sale del `SP_26_V1.1.xlsm` (`protection.locked`): los recortes etarios **se pliegan, no se descartan**. Emite la cascada de filtros y el desglose de `Ingresado` al log. Rechaza una `P` construida con `exigir_medico=False`. |
| `rem_sm_rescate_inasistentes.py` | **Rescate, NO tributa.** Reusa la `P` del P6. `Rescate_6m` / `Rescate_13m` (misma lista de 7 actividades que `Activo 12m`) · `Fallecidos_mes` · `Posibles_Fallecidos` / `Posibles_Traslados` · `Brecha_Medico`. **Fallecidos y Traslados se flagean, nunca se excluyen:** `Motivo Pasivación` es un snapshot, no un dato verificado. **Sin datos de contacto, solo RUN**, por dos razones: PII, y porque RAYEN tiene 4 campos de teléfono y el dump de IRIS muestra solo 2 (la lista quedaría incompleta igual). Sectorizado. |

## §2.1 Familia población (SP·P6 + Rescate) — en validación

- `programas/poblacion.py` arma la tabla «Ferrada» (1 fila por RUN) desde el Formulario
  SM histórico + ADA 13m + Informe Inscritos. Es transversal a las 8 páginas del
  PowerBI.
- `Brecha_Medico` corre la tabla dos veces (con y sin filtro de estamento médico). La
  segunda pasada es **exclusiva** de esa hoja, con guardarraíl en `construir_p6`.
- **Brecha abierta:** `Ingresado` da 2972 contra 2226 del PowerBI, mientras `Estado`
  (−18) y `Activo 12m` (−2) calzan casi exacto. Ya descartados: D2 (solo 34), el hueco
  de `Pertenece` (37) y la ventana de histórico. **Siguiente paso:** diffear las listas
  de RUN por diagnóstico contra el PowerBI, en vez de seguir con hipótesis.
- Planes: [docs/SP_P6_poblacion_plan.md](../docs/SP_P6_poblacion_plan.md) (§8 = rescate)
  y [docs/SP_P6_config_por_dx.md](../docs/SP_P6_config_por_dx.md).

## §3 Pipeline A05 (`procesar()`)

**Validado en producción:** el REM de agosto 2026 se hizo completo con la herramienta.

1. Recorta el banner del export (ancla por header → primera fila con A vacía →
   hardcode 16).
2. No modifica la hoja original: escribe `A05_Egresos` / `A05_Ingresos`. Con `mes`
   filtra por FECHA FORMULARIO (`rem_utils.mes_de_celda`, parsea por estructura: IRIS
   `DD/MM/YYYY`, Admin `YYYY/MM/DD`). Mes vacío → `ArchivoInvalido`.
3. Detecta eventos por tokens en las columnas `"N.- ESTADO"`.
4. Patología = pregunta a la izquierda del ESTADO + subtipo (§7).
5. Formato largo: **una fila por evento**, con encabezado congelado y autofiltro.

Columnas: `RUT · Edad_Formulario · Sexo · Tipo_Egreso · Patologia · Subtipo ·
Falta_Subtipo · <DEMOGRAFIA…> · Fila_Origen`. Las demográficas se generan desde
`DEMOGRAFIA.keys()`.

## §6 Demografía A05

Cada flag = `(tokens_header, regla)`. `ALERTAS ADMINISTRATIVAS` trae varios valores
separados por `;`, así que el substring funciona.

**Validado:** `SENAME` (capta `SENAME Justicia Juvenil`) · `Proteccion_Ninez` (`MEJOR
NINEZ` capta `SPE ex Mejor Niñez- Ambulatorio`, separado de SENAME) · `Migrante` (alerta
`MIGRANTE`, no nacionalidad) · `Madre_menor5` (pregunta 1 = SI). `Gestante` eliminado:
no existe en este export.

**Reglas confirmadas por el autor (sep-2026), implementadas en 1.9.11** — valores categóricos reales:

- **`Pueblos_Originarios`** (col. `PUEBLO ORIGINARIO`): **SI** salvo que venga vacío,
  `Ninguno`, `No Sabe` o `No Contesta`. `Otro` y `Otro pueblo originario declarado`
  cuentan como SI.
  Valores: Aymara · Chango · Colla · Diaguita · Kawésqar · Lickanantay · Mapuche ·
  Quechua · Rapa Nui O Pascuense · Yagán · Otro · Otro pueblo originario declarado ·
  Ninguno · No Contesta · No Sabe.
- **`Trans`**, con dos vías:
  - **Explícita** (col. `GENERO`): `Femenino Trans` · `Masculino Trans` ·
    `Transgénero Femenina` · `Transgénero Masculino`.
  - **Implícita** (sexo ≠ género): `SEXO=Hombre` + `GENERO=Femenina`, o
    `SEXO=Mujer` + `GENERO=Masculino`.
  - Por esta regla **no** cuentan: `No binarie` · `Otra` · `No Revelado` · vacío, ni
    ningún `SEXO` en `Intersexual` / `Desconocido` / `No Informado`. No es un juicio
    clínico: RAYEN sí registra género no binario, pero el REM solo tiene sexo binario +
    Trans, así que `No binarie` no tiene casilla donde ir. Si MINSAL agrega una, se reabre la regla.
  - Valores de `SEXO`: Hombre · Mujer · Intersexual · Desconocido · No Informado.
  - Valores de `GENERO`: Femenina · Masculino · los 4 trans · No binarie · No Revelado ·
    Otra · (vacías).

Fuente única: Pueblo → `rem_utils.PUEBLO_VACIO`; Trans → `rem_utils.trans_de` (la
usan el A05, `trans_map` del SM y AW/AX del P6). En el A05, la columna `Trans` muestra
el sexo en los casos implícitos (`Femenina (sexo Hombre)`).

**P6 AW/AX no filtra por sexo registral.** El control de errores del SP (AW ≤
Mujeres, AX ≤ Hombres) salta cuando el género declarado cambió sin reingreso, y el
SSMC lo acepta. Esos casos cuentan igual y dejan un aviso en `Revisar_Administrativo`.
Regla general del proyecto: **un control de errores de la plantilla avisa, no manda.**

## §7 Decisiones de diseño SM (NO deshacer sin motivo)

- **Diagnóstico = pregunta a la izquierda del ESTADO**, caminando hacia la izquierda y
  saltando las columnas de subtipo/estado (`encontrar_diagnostico()`). Cubre
  `[¿X?][ESTADO][TIPO]` y `[¿X?][TIPO/ETAPA][ESTADO]` (Suicidio, Alzheimer).
- **Subtipos** en `DIAGNOSTICOS_CON_SUBTIPO`: Violencia 4→6 · Suicidio 11→12 ·
  Depresión 18→20 · Ansiedad 41→43 · Alzheimer 44→45 (ETAPA). `limpiar_subtipo()`
  quita el sustantivo del header; `OVERRIDE_SUBTIPO` cubre Ansiedad (Pánico junta dos).
- **Remap deprecated:** Abuso Sexual (pregunta 9) → **Violencia › Víctima › Sexual**
  (`REMAP_DIAGNOSTICO`). Hoy la salida guarda `Violencia` / `Sexual`; el nivel
  «Víctima» está implícito.
- **Nombre de patología canónico:** `OVERRIDE_PATOLOGIA` (nombres del SP·P6).
- **`EXCLUIR_PATOLOGIA = {75,77,79,81}`:** epilepsia y los programas de
  rehabilitación/acompañamiento. **Es una decisión de APS y de este centro:** al
  generalizar a otros centros, va al config y por defecto se incluyen.
- **Quirk RAYEN:** `AÑO APLICACIÓN FORMULARIO` trae la **EDAD** a la fecha de llenado,
  no el año. `EDAD PACIENTE` es a la descarga, así que se ignora.
- **Otras Causas es manual por diseño** (abandono vs clínica, caso a caso): se flaggea,
  no se clasifica.
- Zonas editables arriba de cada archivo: `BUSQUEDAS` · `DIAGNOSTICOS_CON_SUBTIPO` ·
  `REMAP_DIAGNOSTICO` · `DEMOGRAFIA` · `AVISAR_ALTA_SIN_SUBTIPO`.
