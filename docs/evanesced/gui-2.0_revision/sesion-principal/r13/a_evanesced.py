# -*- coding: utf-8 -*-
"""Mueve el trabajo intermedio de la revision gui-2.0 a docs/evanesced/ (CLAUDE.md
regla 7). Solo texto YA ESCANEADO sin hallazgos. Excluye:
  - copias de fuentes del repo (llevan '# Version:'): se recuperan con `git show`, y
    una copia rancia de app.py dentro de docs/ es peor que no tenerla.
  - dumps regenerables con un comando (mergetree.txt, headers.txt).
Los .xlsx NO se mueven: ver el README que escribe este script.
"""
import pathlib, re, shutil, sys

R = pathlib.Path(r"E:\git\Autorem")
DEST = R / "docs" / "evanesced" / "gui-2.0_revision"
TMP = pathlib.Path(r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem")
RE_H = re.compile(r"^# Version: *([\d.]+) *$", re.M)
EXCLUIR_NOMBRE = {"mergetree.txt", "headers.txt"}

ETIQUETA = {"648a107e": "finders", "a40108ff": "sesion-principal", "5e2e5aba": "prompts"}

copiados, saltados = [], []
for ses in sorted(TMP.iterdir()):
    etq = ETIQUETA.get(ses.name[:8])
    base = ses / "scratchpad"
    if etq is None or not base.is_dir():
        continue
    for f in sorted(base.rglob("*")):
        if not f.is_file() or f.suffix.lower() not in (".py", ".md", ".txt"):
            continue
        txt = f.read_text(encoding="utf-8", errors="replace")
        if f.name in EXCLUIR_NOMBRE:
            saltados.append((f.name, "dump regenerable con un comando"))
            continue
        if RE_H.search(txt):
            saltados.append((f.name, "copia de una fuente del repo (git show la recupera)"))
            continue
        rel = f.relative_to(base)
        out = DEST / etq / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, out)
        copiados.append(out.relative_to(R).as_posix())

print("copiados: %d" % len(copiados))
print("saltados: %d" % len(saltados))
for n, m in sorted(set(saltados)):
    print("   %-34s %s" % (n, m))

README = DEST.parent / "README.md"
README.write_text("""# docs/evanesced/

Trabajo **intermedio** de ramas y worktrees cuyo trabajo ya se cerro: los scripts de
repro, los arneses de medicion, los prompts de cada ronda y las notas que produjeron los
cambios que estan en el `CHANGELOG`. Nada de esto se importa, se distribuye ni se corre en
CI: es **documentacion del porque**, y esta aca porque la rama o el worktree donde vivio
desaparece y una sesion fria no tiene otra fuente ([CLAUDE.md](../../CLAUDE.md) §0 regla 7).

El nombre: la rama se evanesce, sus scripts no.

## Que entra

- `.py` de repro y medicion, `.md` de notas y prompts, `.txt` de salidas cortas.
- Se archiva **como quedo**, sin limpiar ni reescribir: un script arreglado a posteriori ya
  no prueba lo que probo.

## Que NO entra

| Que | Por que | Como se recupera |
|---|---|---|
| Copias de fuentes del repo (`app.py`, `formatos.py`, `poblacion.py`, …) | Una copia rancia de un fuente dentro de `docs/` es peor que no tenerla: se lee como si fuera actual. Ademas llevan `# Version:` y `check_version` bloquea el commit (la version solo la llevan `programas/`, `modulos/`, `tools/`, `gui/` y `autorem.py`) | `git show <commit>:<ruta>` |
| Dumps grandes regenerables (`git merge-tree`, listados de headers, snapshots de `git diff`) | Son salida de UN comando, y pesan mas que el comando | el comando esta anotado en la nota que lo usaba |
| **`.xlsx` / binarios** | El pre-commit anti-RUT **salta los binarios** (tools/CLAUDE.md §8.2), y `.gitignore` ignora `*.xlsx` con **whitelist por archivo** justo para que cada uno lleve un veto humano. Un fixture que hace falta de verdad va a `refs_tablas/` por la skill `limpiar-refs`, con su linea de whitelist y su contrato | el script que lo usaba lo reconstruye |

## Gotchas al archivar

- **cp1252:** `tools/check_cp1252.py` barre TODO `*.py` del repo, y estos scripts traen
  flechas, `OK`/tildes de estado y a veces BOM. Por eso `evanesced` esta en su
  `EXCLUIR_DIRS`, con el mismo criterio que `worktrees`: codigo congelado de otra tanda,
  que no imprime a la consola del exe. **No** reescribir los scripts para que pasen el
  checker.
- **Antes de borrar cualquier archivo del repo**, mirar quien lo cita:
  `grep -rn "<nombre>" --include="*.md" --include="*.py" .`. El `CHANGELOG` es permanente.

## Contenido

### `gui-2.0_revision/`

Las 13 rondas de code-review de la rama `gui-2.0` (sep-2026). El registro de lo que
encontraron es [docs/review_gui-2.0_pendiente.md](../review_gui-2.0_pendiente.md); esto es
el instrumental.

| Carpeta | Que hay |
|---|---|
| `finders/` | Los agentes finder (uno por ronda, con `compact` entre medio): el `review_context.md` que compartian, los arneses de repro por angulo (`alt/`, `b/`, `e/`, `dimtest/`) y los scripts de cada hallazgo |
| `sesion-principal/` | La sesion que aplico los arreglos y anoto el ledger: repros, mediciones, mutantes y los scripts de edicion CRLF-safe del propio ledger |
| `prompts/` | Los prompts de ronda, tal como se pegaron |

Lo mas reutilizable, por si sirve de nuevo:

- `sesion-principal/r13/imports_muertos.py` - imports sin uso en los 4 paquetes (AST).
- `sesion-principal/r13/attrs.py` - todo `mod.attr` del arbol contra el modulo real
  importado: caza una referencia a un simbolo que un refactor borro.
- `sesion-principal/r13/hdr.py` - compara los criterios de fila-de-encabezado sobre las
  referencias de `refs_tablas/`.
- `sesion-principal/r13/anios_discontinuos.py` - repro del hueco de anios en la familia
  poblacion (hallazgo 8 de la ronda 13).
- `sesion-principal/r13/escanea_candidatos.py` / `escanea_xlsx.py` - el gate de PII del
  proyecto aplicado a un directorio cualquiera antes de meterlo al repo. **Ojo:**
  `scan_catalogo.escanear` devuelve una **3-tupla**.
- `finders/alt/harness.py` - arnes de contratos de fuentes, antes de que fuera
  `tests/contratos_fuentes.py`.
""", encoding="utf-8")
print("\nREADME ->", README.relative_to(R).as_posix())
