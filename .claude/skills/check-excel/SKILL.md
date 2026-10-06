---
name: check-excel
description: Crea o actualiza la macro VBA de chequeo pre-envio de un modulo (modulos/checks_excel/REM_<serie>_<programa>.bas), que lee el TOTAL de cada tabla que autoREM produce y marca REVISAR los 0 y errores en el REM del mes. Usalo al terminar un modulo nuevo (todo modulo nace con su check), cuando el usuario pida "un check / macro / validador pre-envio" de un REM, cuando falle tests/test_checks_excel.py, o al llegar plantillas REM de un año nuevo.
---

# check-excel — un check pre-envio por programa y serie

**Que caza:** una tabla que no se pego, un total que perdio su formula (A05·O de julio
2026: la tabla tenia datos y el total daba 0) o un error de digitacion. No valida el
desglose: el `.xlsm` suma los desgloses solo, asi que basta mirar el total.

**Granularidad:** un `.bas` por **programa y serie** (`REM_A_SM`, `REM_A_RESP`,
`REM_P_SM`), no por modulo: el REM se envia por serie, y `REM_A_SM` ya junta A05, A03
D.3 y Actividades. Un modulo nuevo de un programa que ya tiene check **agrega lineas a
ese `.bas`**; no crea otro.

## Receta

1. **Ubicar los totales** en la plantilla vigente de `refs_tablas/` (`SA_26_V*.xlsm` /
   `SP_26_V*.xlsm`), con openpyxl (scripts en el scratchpad): por cada tabla que el
   modulo produce, la celda o el rango del **Total / Ambos Sexos**. Si la tabla tiene
   varias filas sin una fila TOTAL, se usa el rango de la columna total
   (`C163:C168`). Varias areas se separan con coma (`C110,C112`).
2. **Probar contra un REM ya enviado y validado** del autor (pedir la ruta; vive en
   OneDrive, se lee con `data_only=True` y solo se miran sumas, nunca filas de
   pacientes). Mostrar la tabla de totales y confirmar con el autor que los ceros son
   meses sin actividad.
3. **Escribir o editar el `.bas`**: copiar la forma de `REM_A_SM.bas`, con la primera
   linea `Attribute VB_Name`, el header con `' Version:` (lo vigila `check_version`),
   solo ASCII y un item `"HOJA|descripcion corta|RANGO"` por tabla. Mensajes al
   usuario de una linea por tabla: el autor pidio lo menos verboso posible.
4. **Correr `tests/test_checks_excel.py`**: exige que cada celda sea una formula en la
   plantilla. Si un total es un INPUT de la plantilla (sin formula, como `A19a!C110`),
   se agrega a `MANUALES` con la etiqueta de su fila. Una serie nueva va en
   `PLANTILLA`.
5. Commitear el `.bas` (y el test si cambio). No cambia el `.exe`, asi que **no lleva
   tag**.

## Plantillas de un año nuevo (3.0.0)

Al reemplazar la plantilla en `refs_tablas/`, el test falla con la lista de celdas
que ya no son formula. Rehacer el paso 1 para esas tablas, y el paso 2 con el primer
REM del año nuevo.
