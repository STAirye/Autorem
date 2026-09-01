<!--
This document was generated with the assistance of Claude Opus 4.8 (Anthropic).
The human author reviewed, modified, and integrated the content.
Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# Plan (futuro) — Población PSM bajo control → SP_v1.1  (relacionado a REM A05 N/O)

> **Estado: NOTA / PENDIENTE. NO implementar aún.** Dictado por Simón (fin de un día
> REM largo) para no perder el procedimiento. Cuando se retome, replicar como el A23:
> pedir el/los **DAX del PowerBI** de "población PSM" y validar 1:1 contra el PowerBI.

## Fuente
- **Población PSM desde PowerBI** (tiene todo un DAX propio — conseguirlo al implementar).
- Se arma como una **tabla dinámica**:
  - **Filtros globales:** estado · activo 12m · ingresado · embarazada · madre <5 años ·
    originario · migrante · protección niñez · trans.
  - **Columnas:** sexo / edad.
  - **Valores:** cuenta de **número (RUT)** (= personas distintas).

## Procedimiento para completar el **SP_v1.1** del mes
1. Fijar filtros globales: **estado = Activo · activo 12m = SI · ingresado = SI**.
2. **Sanity check:** con esos 3 filtros el total NO debe ser muy distinto al mes
   anterior — **siempre ~1300-1500**. (Si se dispara, algo está mal.)
3. Ese agregado (total personas) va en la **fila 24**.
4. **Iterar por diagnóstico:** llenar cada dx. La **suma total por diagnóstico debe ser
   MAYOR** que el total de la fila 24 — porque hay personas con **más de un diagnóstico**
   (se cuentan en varias filas de dx).
5. **Ídem con los factores de riesgo** (FR): iterar y llenar.
6. **Fila 13 = FR + PERSONAS**, es decir la suma de las **filas 15 a 24**.

## Al implementar (recordatorios)
- Conseguir el DAX del PowerBI de población PSM (como se hizo con "Pertenece a SALA"
  del A23) y replicarlo 1:1; los 9 filtros globales son la parte fina a alinear.
- Layout exacto (filas 13, 15-24, dx, FR) se lee del **`refs tablas/SP_26_V1.1.xlsm`**
  (no del SA). Confirmar numeración de filas contra ese template al implementar.
- Salida estilo el resto: hoja copy-paste al SP + detalle auditable.
- Es un módulo/reporte nuevo → al terminar, **Y++** en la versión (§9 de CLAUDE.md).
