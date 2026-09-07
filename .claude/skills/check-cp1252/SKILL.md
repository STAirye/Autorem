---
name: check-cp1252
description: Verifica que el codigo .py del repo sea seguro para la consola cp1252 de Windows (sin flechas/cajas/emoji Unicode que revientan con UnicodeEncodeError). Usalo cuando el usuario pida "revisar cp1252", "chequear que el codigo sea ASCII-safe", despues de agregar un modulo/script nuevo con logs, o antes de compilar el .exe.
---

# check-cp1252 — consola Windows sin wrapper UTF-8 no soporta cualquier simbolo

Regla del proyecto (CLAUDE.md, memoria `solo-ascii-en-el-codigo`): nada de
simbolos decorativos no-cp1252 en el codigo (flechas `-> <- <->`, cajas de
comentario, checks `OK X`, `!`) porque revientan la consola Windows sin el
wrapper UTF-8 con `UnicodeEncodeError` (que ademas hereda de `ValueError`, asi
que se disfraza). El texto en espanol con tildes/enie SI es seguro — no es
"solo ASCII", es "solo cp1252".

## Cuando dispararlo
- El usuario pide revisar/chequear cp1252, o "que el codigo sea seguro para
  Windows".
- Se acaba de agregar un modulo o script nuevo con `print`/logs.
- Antes de empaquetar a `.exe` (PyInstaller no cambia esto, pero es buen
  momento para barrer el repo).
- El usuario pide una limpieza retrospectiva del repo.

## Que hacer
1. **Dry-run primero** (no toca nada, solo reporta):
   ```bash
   python tools/check_cp1252.py
   ```
   Exit code 0 = limpio. Exit code 1 = hay caracteres para revisar (lista
   archivo, linea, columna y el caracter con su nombre Unicode).
2. Si hay hallazgos, **aplica el fix automatico** (solo corrige simbolos
   conocidos e inequivocos: flechas, cajas, checks — ver `REEMPLAZOS` en el
   script):
   ```bash
   python tools/check_cp1252.py --fix
   ```
3. **Vuelve a correr sin `--fix`** para confirmar que quedo en 0. Lo que
   `--fix` no puede resolver (emoji, simbolos raros sin equivalente ASCII
   obvio) queda listado — arreglalo a mano revisando el CONTEXTO de la linea
   (no hay reemplazo generico seguro para eso).
4. Revisa el diff antes de dar por cerrado: el fix solo debe tocar
   comentarios/strings decorativos, nunca logica. Si el diff toca algo que no
   es un simbolo decorativo, revisa a mano.
5. Se puede acotar a un archivo o carpeta: `python tools/check_cp1252.py modulos/`.

## Notas
- El script mismo escribe sus reemplazos como `\uXXXX` (no como el glifo
  literal) para no auto-reportarse al correr sobre el repo completo — si lo
  editas, mantene esa convencion.
- Por diseno cubre solo `.py` (la logica de la regla es sobre la consola al
  ejecutar codigo, no sobre docs `.md`, que sí pueden llevar emoji/tablas con
  simbolos como parte del contenido).
- Se puede instalar como hook pre-commit: `python tools/check_cp1252.py --instalar`.
  Se encadena al pre-commit existente (ej. `hook_pre_commit_rut.py`) sin pisarlo
  -- idempotente, no reinstala dos veces. Los hooks NO se versionan, asi que hay
  que correr `--instalar` en cada clon nuevo.
