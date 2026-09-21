<!--
This document was generated with the assistance of Claude Opus 5 (Anthropic).
The human author reviewed, modified, and integrated the content.
Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# docs/evanesced/ — reglas

Se carga al trabajar en `docs/evanesced/`. Los `§N` son las anclas del
[CLAUDE.md raíz](../../CLAUDE.md). **Qué hay acá y por qué** está en
[README.md](README.md) — este archivo es solo lo que hay que **hacer y no hacer**.

## Esto es un archivo histórico, no código vivo

Nada de acá se importa, se distribuye ni corre en CI. Es **documentación del porqué**
(§0 regla 7): la rama o el worktree donde vivió ya no existe, y una sesión fría no
tiene otra fuente.

1. **No se reescribe.** Se archiva **como quedó**. Un script arreglado a posteriori ya
   no prueba lo que probó — y eso es justamente lo que vale de él. Si tiene una ruta
   absoluta, un `RAIZ` que apunta a otra carpeta o un bug, **se anota en el README**,
   no se corrige en el archivo.
2. **No se borra**, ni «limpiando». Antes de tocar cualquier cosa acá, mirar quién la
   cita: `grep -rn "<nombre>" --include="*.md" --include="*.py" .`. El `CHANGELOG` es
   permanente y una cita colgada ahí no se arregla después.
3. **No se hace pasar los checks.** `evanesced` está en `EXCLUIR_DIRS` de
   `tools/check_cp1252.py` a propósito (junto con `worktrees`): estos scripts traen
   flechas, tildes de estado y a veces BOM, y no imprimen en la consola del `.exe`.
   **No** los reescribas para que pasen el checker. Por la misma razón no llevan
   `# Version:`: el manifiesto de `check_version.py` cubre `programas/`, `modulos/`,
   `tools/`, `gui/` y `autorem.py`, y un `.py` con versión fuera de esas rutas **bloquea
   el commit**.

## Archivar una tanda

1. Una carpeta por tanda, nombrada por lo que produjo (`gui-2.0_revision/`,
   `hooks_auditoria-2.0.5/`), no por la fecha ni por el número de sesión.
2. Copiar los scripts **tal cual** desde el scratchpad.
3. **Escribir su sección en [README.md](README.md)**, que es lo que los vuelve
   recuperables: qué hacía cada script, qué encontró, y sus trampas (rutas absolutas,
   falsos positivos a propósito, firmas que sorprenden). Un script archivado sin esa
   sección es un `.py` huérfano que nadie va a volver a correr.
4. **Anotarlo en el [CHANGELOG](../../CHANGELOG.md)**, no en el `README.md` de la raíz:
   archivar es una tarea **dev-facing**, y el README de la raíz es para quien usa el
   `.exe`.

## Qué NO entra

La tabla con los motivos está en [README.md](README.md). En corto: **copias de fuentes
del repo** (`git show <commit>:<ruta>` las recupera, y una copia rancia dentro de
`docs/` se lee como si fuera actual), **dumps regenerables** (pesan más que el comando
que los produjo) y **`.xlsx` / binarios** (el anti-RUT **salta los binarios**, §8.2; un
fixture que haga falta de verdad va a `refs_tablas/` por la skill `limpiar-refs`, con
su línea de whitelist y su contrato).
