---
name: limpiar-refs
description: Recorta a SOLO EL HEADER cualquier export nuevo agregado a `refs tablas/` (privacy-by-design). Úsalo cuando el usuario agregue/mencione un archivo nuevo de datos en esa carpeta, cuando notes un .xlsx nuevo o modificado ahí, o cuando pida "limpiar refs" / dejar solo encabezados. NO uses para archivos fuera de esa carpeta.
---

# limpiar-refs — refs tablas/ es zona de solo-estructura

Los exports de RAYEN/IRIS pueden traer PII de paciente en sus filas. Regla del
proyecto (CLAUDE.md §8): en `refs tablas/` solo vive la ESTRUCTURA (encabezados),
nunca valores. Cuando entra un export nuevo, se recorta a header-only **sin leer los
datos**.

## Cuándo dispararlo
- El usuario dice que agregó (o va a agregar) un archivo de datos a `refs tablas/`.
- Detectas un `.xlsx` nuevo o modificado en `refs tablas/` durante la sesión.
- El usuario pide "limpiar refs", "deja solo los header", o similar.

## Qué hacer (en orden)
1. **Dry-run primero** (solo reporta filas, NO toca nada, NO imprime valores):
   ```bash
   python tools/limpiar_refs.py
   ```
   O sobre un archivo puntual: `python tools/limpiar_refs.py "nombre.xlsx"`.
2. Mira el reporte. El motor ya protege con **denylist** lo que NO es export plano
   (templates `.xlsm` SA/SP, `calculador`, `minimanual`, `comentado`, `arsenal`,
   `maestro` = Maestro de Actividades). Eso sale "omitido" y está bien.
3. **Aplica** el recorte:
   ```bash
   python tools/limpiar_refs.py --aplicar
   ```
   (o con el nombre del archivo para recortar solo ese).
4. Confirma al usuario en agregados: qué archivo(s) se recortaron y de cuántas filas
   a cuántas. **Nunca** transcribas contenido de celda.

## Reglas duras
- **Nunca leer ni imprimir valores de celda.** El motor solo cuenta no-vacíos para
  ubicar el header; vos tampoco abras el archivo a mirar los datos.
- Si un archivo nuevo es **estructura/spec que debe conservar sus filas** (un template,
  un catálogo tipo Maestro, un manual) y NO está en la denylist, **pregunta al usuario
  antes de recortarlo** y agrégalo a `DENY_NOMBRE` en `tools/limpiar_refs.py` en vez de
  recortarlo. Ver [[preguntar-antes-de-actuar]].
- Si aparece PII real en un archivo que igual se va a versionar, aplica la regla dura:
  avisar sin transcribir el dato. Ver [[privacidad-auditar-solo-si]].
