---
name: limpiar-refs
description: Deja en BANNER + ENCABEZADO (sin filas de datos) cualquier export nuevo agregado a `refs_tablas/` (privacy-by-design) y lo lleva hasta el whitelist del .gitignore y su contrato. Úsalo cuando el usuario agregue/mencione un archivo nuevo de datos en esa carpeta, cuando notes un .xlsx nuevo o modificado ahí, o cuando pida "limpiar refs" / dejar solo encabezados. NO uses para archivos fuera de esa carpeta.
---

# limpiar-refs — refs_tablas/ es zona de solo-estructura

Los exports de RAYEN/IRIS pueden traer PII de paciente en sus filas. Regla del
proyecto (CLAUDE.md §8): en `refs_tablas/` solo vive la ESTRUCTURA, nunca valores.
Cuando entra un export nuevo, se deja en **banner + encabezado sin leer los datos**.

**El banner se conserva** (sep-2026). A los usuarios se les pide cargar el export tal
cual, con su banner, y la herramienta lo salta sola: la referencia tiene que tener la
misma forma, o los contratos (`tests/contratos_fuentes.py`) prueban un archivo que no
existe. Hasta la ronda 11 varias referencias IRIS se recortaron a mano en Excel, sin
banner, y eso escondió dos cosas: que el IRIS de formularios trae 15 filas de banner, y
que el grupal decía `Columna1` donde el export real dice `ASISTE (SI/NO)`. **No se edita
una referencia a mano en Excel**: se baja de nuevo y pasa por el script.

## Cuándo dispararlo
- El usuario dice que agregó (o va a agregar) un archivo de datos a `refs_tablas/`.
- Detectas un `.xlsx` nuevo o modificado en `refs_tablas/` durante la sesión.
- El usuario pide "limpiar refs", "deja solo los header", o similar.

## Qué hacer (en orden)
1. **Dry-run primero** (solo reporta filas, NO toca nada, NO imprime valores):
   ```bash
   python tools/limpiar_refs.py
   ```
   O sobre un archivo puntual: `python tools/limpiar_refs.py "nombre.xlsx"`.
2. Mira el reporte. El motor ya protege con **denylist** lo que NO es export plano
   (templates `.xlsm` SA/SP, `calculador`, `minimanual`, `comentado`, `arsenal`,
   `comparativo`, `maestro` = Maestro de Actividades). Eso sale "omitido" y está bien.
3. **Aplica** el recorte:
   ```bash
   python tools/limpiar_refs.py --aplicar
   ```
   (o con el nombre del archivo para recortar solo ese). El script arma un libro
   **nuevo** con el banner, el bloque de encabezado (dos filas si RAYEN lo parte con
   celdas combinadas, como Utilización de Cupos) y las hojas vacías; lo demás del
   original (tablas de Excel, caché de tablas dinámicas, comentarios, imágenes,
   propiedades) no se copia. Después lo escanea (RUT con DV válido, correo, teléfono):
   con un hallazgo, **no lo escribe** (`NO ESCRITO`, exit 1).
4. **Revisa el banner a mano, enmascarado**: el escáner no reconoce un nombre de
   funcionario, y el banner puede traer `GENERADO PARA: <quien lo bajó>`. Imprime solo
   la etiqueta y si trae texto después (`bool(...)`), nunca el valor.
5. **Nombre limpio**: sin espacios, sin tildes, sin `.xls.xlsx`; sufijo `_iris` /
   `_admin` según el formato.
6. **Whitelist**: agrega `!refs_tablas/<archivo>` al `.gitignore`, con un comentario de
   qué es y que se verificó sin PII.
7. **Contrato**: si un lector lo consume, apunta su contrato (`ref=`) a la referencia y
   saca el encabezado sintético (skill `tests-fuentes`). Corre
   `python tools/check_fuentes.py --todo`: con el encabezado REAL suele aparecer algo.
8. **Test**: `python tests/test_refs_tablas.py` exige que toda referencia versionada
   quede «ya limpio» y sin hallazgos del escáner.
9. Confirma al usuario en agregados: qué archivo(s) se recortaron y de cuántas filas
   a cuántas. **Nunca** transcribas contenido de celda.

## Reglas duras
- **Nunca leer ni imprimir valores de celda de datos.** El motor solo cuenta no-vacíos
  para ubicar el encabezado; tú tampoco abras el archivo a mirar los datos. Los nombres
  de columna sí se pueden leer (son estructura).
- Si un archivo nuevo es **estructura/spec que debe conservar sus filas** (un template,
  un catálogo tipo Maestro, un manual) y NO está en la denylist, **pregunta al usuario
  antes de recortarlo** y agrégalo a `DENY_NOMBRE` en `tools/limpiar_refs.py` en vez de
  recortarlo. Ver [[preguntar-antes-de-actuar]].
- Si aparece PII real en un archivo que igual se va a versionar, aplica la regla dura:
  avisar sin transcribir el dato. Ver [[privacidad-auditar-solo-si]].
- Un crudo que se copió a otro lado para diagnosticar (respaldo, scratchpad) se borra
  apenas termina el recorte.
