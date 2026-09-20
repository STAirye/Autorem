<!--
This document was generated with the assistance of Claude Sonnet 5 (Anthropic).
The human author reviewed, modified, and integrated the content.
Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# tests/ — convenciones

Se carga al trabajar en `tests/`. Los `§N` son las anclas del [CLAUDE.md raíz](../CLAUDE.md).

## No compares texto plano que ve el usuario

Un test **no** escribe a mano un texto de la interfaz (`dichos == ["Falta el acuse"]`,
`"NO se generó" in resumen`). Esos textos se revisan y se reescriben —la revisión de
textos de la GUI 2.0 (sep-2026) rompió un test por exactamente esto—, y el test que
falla por una coma cambiada no avisa de ningún bug: solo cuesta tiempo.

**Cómo sí:**
- Si el test necesita el texto, éste vive **una sola vez** como constante del módulo
  que lo muestra (`a05.TITULO_FALTA_ACUSE`, `runner.TITULO_NO_ENCONTRADO`,
  `widgets.NO_SE_GENERO`), el código la usa y el test la importa. Cambiar el texto
  cambia los dos a la vez. Solo se crea la constante cuando un test la necesita, no
  para cada texto de la GUI.
- Mejor aún, si se puede, afirma **el hecho** y no el texto: que se llamó al diálogo
  de aviso (no cuál), que la corrida devolvió `None`, que el archivo no se escribió.
- Un dato que viaja dentro del mensaje (el nombre de un archivo, el motivo de un
  fallo, un número) sí se puede buscar con `in`: no es texto de la interfaz, es el
  dato.
