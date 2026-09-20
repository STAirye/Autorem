<!--
This document was generated with the assistance of Claude Fable 5 and Claude Opus 5 (Anthropic).
The human author reviewed, modified, and integrated the content.
Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# tools/ — desarrollo, privacidad y build

Se carga al trabajar en `tools/`. Los `§N` son las anclas del [CLAUDE.md raíz](../CLAUDE.md).

## Herramientas

| Archivo | Rol |
|---|---|
| `hook_pre_commit_rut.py` | **El check anti-RUT** (§8.2), en pre-commit y commit-msg. |
| `check_cp1252.py` | **El check** de que los `.py` sean cp1252-safe. |
| `check_version.py` | **El check** de versionado y contadores (§9). `--arreglar` · `--bump X.Y.Z`. |
| `check_fuentes.py` | **El check** de que todo lector de planillas del usuario tenga CONTRATO (`tests/contratos_fuentes.py`) y lo cumpla. Corre solo lo que el commit toca; `--todo` corre todo. Skill `tests-fuentes`. |
| `hooks_git.py` | **El instalador** que comparten los 4 checks (`encadenar()`) + `--instalar`, que instala y verifica todos (§8.2). |
| `catalogos_deis.py` | Mantenedor de catálogos: `--check` / `--fetch` / `--slim` (§14). |
| `scan_catalogo.py` | Escáner de PII antes de versionar un catálogo. |
| `limpiar_refs.py` | Deja en **banner + encabezado** lo que entra a `refs_tablas/` (libro nuevo, escaneado antes de escribirse). Skill `limpiar-refs`; lo vigila `tests/test_refs_tablas.py`. |
| `slim_maestro.py` | Genera el Maestro de Actividades slim comprimido. |

**¿Por qué el check anti-RUT y `hooks_git.py` son archivos separados?** Porque son
cosas distintas: uno **revisa**, el otro **instala**. Hasta 1.9.5 cada uno de los 3
checks traía su propia copia del instalador, y las copias divergieron: la de
`check_cp1252` dejaba su línea **después** del `exit 0`, o sea instalada y sin correr
nunca. `hooks_git.py` es la fuente única de esa lógica.

## §8 Privacidad (detalle)

- **Repo y datos separados:** el repo fuera de OneDrive, los exports con PII en la
  carpeta de trabajo. La herramienta lee por ruta.
- El único identificador en la salida es el **RUT**.
- El `.gitignore` excluye `*.xlsx/*.xls/*.csv`. `refs_tablas/` usa whitelist por archivo.
- Una planilla para debug dentro del repo va **anonimizada**.

### §8.1 Incidente sep-2026: un RUT real en el repo público

**Qué pasó.** Un RUT de una persona real vivió ~2 meses como «ejemplo» en CLAUDE.md y
`legacy/`, desde el commit inicial. El `.gitignore` esperaba la PII en planillas, no
en un comentario: **la malla tenía el tamaño equivocado**.

**Remediación:**
- Purga del árbol.
- `git filter-repo --replace-text` **y** `--replace-message` (son pasos separados).
- Repo borrado y recreado en GitHub: un `push --force` no basta, porque GitHub sirve
  los SHA viejos por URL.
- Hook anti-RUT.
- **Borrar todo clon anterior a la reescritura:** un `reset --hard` no limpia
  `.git/objects`. Ojo con los clones anidados.

**Desenlace:** jurídica del SSMC confirmó que, sin información clínica asociada, no
requiere acciones formales. **La regla queda igual:** un RUT nunca es un buen ejemplo.
Usar `11111111-1`, y para fixtures un cuerpo que empiece en `1000` con el DV calculado.

### §8.2 Los hooks (cuatro checks)

`hook_pre_commit_rut.py` bloquea cadenas con forma de RUT cuyo **DV cuadra** (módulo
11), tanto en archivos staged como en el mensaje. Deja pasar los placeholders obvios.

```bash
python tools/hooks_git.py --instalar
```

- **Un solo comando instala los cuatro** (desde 1.9.15; `check_fuentes` desde 1.9.17). Llama al instalador de cada
  check, así los args de cada uno viven en un solo lugar, y después **verifica el
  resultado**: `pre-commit` debe listar los cuatro scripts y `commit-msg` el de RUT. Si
  falta alguno, sale con exit 1. Sin argumentos, muestra el uso y sale con exit 2.
  Hasta 1.9.14 ese mismo comando era un no-op silencioso.
- El `--instalar` de cada check (`hook_pre_commit_rut.py`, `check_cp1252.py`,
  `check_version.py`, `check_fuentes.py`) sigue funcionando para instalar uno solo.
- **`check_fuentes.py`** (sep-2026, tras 10 rondas de revisión cazando el mismo bug a
  mano): un LECTOR de planillas que el commit agrega o cambia y no tiene contrato
  **bloquea**; los contratos de lo tocado **corren** (0 filas, columna renombrada, clave
  vacía, fechas ilegibles, índice fijo). No re-verifica lo que no se tocó. ~5 s el
  barrido completo (`--todo`).
- **Los hooks no se versionan** (viven en `.git/hooks/`): hay que instalarlos en cada
  clon y en cada equipo.
- Se escriben contra `$REPO` (`git rev-parse --show-toplevel`), así corren bien desde
  los worktrees. Reinstalar migra en el lugar las invocaciones viejas con ruta absoluta.
- El pre-commit anti-RUT **salta los binarios** (`.xlsx`, `.gz`). Por eso existe
  `scan_catalogo.py`, y `catalogos_deis.py --slim` se niega a vendorizar un catálogo
  con hallazgos.

## §10.1 Worktrees

Un worktree NO es un clon: es otro árbol de trabajo del mismo `.git`. **Compartidos:**
commits, refs, config, **hooks** y **stash**. **Propios de cada worktree:** los
archivos en disco, el index, `HEAD` y la rama.

- Un commit en el worktree existe de inmediato para `main` (no hay push entre ellos).
- **Stash compartido:** dos sesiones en paralelo comparten la pila → usar commits WIP.
- Una rama no puede estar checkouteada en dos worktrees a la vez.

**Cerrar un worktree en Windows:**
1. Mergear, y después `git worktree remove <ruta>`. Si responde «Deletion … failed. Try
   again?», contestar **n**: algún proceso tiene la carpeta como cwd (normalmente la
   propia sesión de Claude Code). Cerrar la sesión y borrar.
2. Si `git worktree prune` da `Permission denied`, son archivos ReadOnly:
   `attrib -R ".git\worktrees\<nombre>" /S /D` y otra vez `git worktree prune -v`.
3. Al final, `git branch -d <rama>`. Si se niega, el problema es el merge.

Un worktree que ya no aparece en `git worktree list` pero sigue en disco es cascarón:
no hay trabajo en riesgo.

## §11 Build del `.exe`

```bash
pyinstaller --clean autoREM.spec
# -> dist/autoREM.exe
```

- **Un build que «funciona» y pare un exe roto: la trampa de la 2.0.0.**
  `collect_submodules('gui.paginas')` necesita poder **importar** el paquete, y el
  script `pyinstaller` **no pone la raíz del repo en `sys.path`** (`python -m
  PyInstaller` sí). Sin ella devolvía `[]` **en silencio**: el build terminaba OK, el
  exe pesaba 126 KB menos y recién al abrirlo moría con «gui/paginas/ no expuso ninguna
  PANTALLA». Desde la **2.0.1** el `.spec` se agrega a sí mismo a `sys.path` (`SPECPATH`)
  y **aborta el build** si no encuentra ninguna página. Moraleja para validar un
  empaquetado: **compilar con el comando que está documentado**, no con uno equivalente.
- **`autoREM.spec` está versionado** (única excepción al `*.spec` del `.gitignore`):
  lleva a mano los `--add-data` (el `maestro_slim.csv.gz` y la carpeta `catalogos/`,
  con su `FUENTES.json`) y el `hiddenimports` de `programas.catalogos`. Los datos no son
  imports, y PyInstaller no los sigue solo. **Si cambia lo que shippea el exe, se edita
  el `.spec` y se commitea.**
- Sin el Maestro slim en el bundle, el Trabajo Perdido corre en heurística y lo avisa
  en el log. Sin `catalogos/`, `catalogos.cargar()` tira `FileNotFoundError`.
- **`--clean` → `PermissionError [WinError 5]`** sobre `build/`: es el atributo
  ReadOnly, no faltan privilegios (correr como admin no lo arregla).
  `attrib -R "build\*" /S /D`. A `dist/` le pasa igual.
- **Plataforma:** oficialmente Windows (PyInstaller no cross-compila). En Linux lo
  compilas tú, y probablemente corre en Wine. macOS: sin soporte.
- **`--onefile` (oficial):** un solo archivo, pero cada arranque descomprime ~37 MB a
  una carpeta temporal. `--onedir` arranca más rápido y a veces molesta menos al
  antivirus; quien quiera, que lo compile.
- **SmartScreen / antivirus institucional:** un exe sin firmar puede requerir whitelist
  de IT. Argumento para IT: procesa todo local y no sube nada.
- Distribuir `LICENSE` junto al `.exe`.
