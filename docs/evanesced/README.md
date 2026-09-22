# docs/evanesced/

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
| `prompts/` | Los prompts de ronda, tal como se pegaron, mas `prompt_merge_2.0.md` (el del merge a `main`) |

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
- `sesion-principal/r13/repro_mask_unida.py` - por que `auditar_atenciones` (main 1.9.16) hay
  que adaptarlo a la forma canonica de `cargar_atenciones` y no al reves: una mascara
  multi-token (`contiene_todos` con 2 tokens) que sobre la celda de actividades UNIDAS matchea
  tokens de actividades DISTINTAS. Es la evidencia del hallazgo del merge (ver el §4 del
  registro de la revision).
- `finders/alt/harness.py` - arnes de contratos de fuentes, antes de que fuera
  `tests/contratos_fuentes.py`.

### `hooks_auditoria-2.0.5/`

La auditoria de los cuatro pre-commit (sep-2026), disparada por el bug que corrigio la
**2.0.5**: `check_version` decia vigilar cuatro contadores de tests y **tres de sus
patrones estaban muertos** -- apuntaban a frases del `CLAUDE.md` monolitico que
desaparecieron al partirlo por carpeta. Un patron que deja de matchear **no falla: deja
de vigilar**, calladito. Estos dos scripts fueron a buscar esa misma clase de bug en los
otros tres checks (no encontraron ninguno) y a confirmar que cada uno caza un positivo.

- `auditar_hooks.py` - busca **referencias muertas**: recorre `TRANSVERSALES` y `EXENTOS`
  de `check_fuentes` (que nombran funciones a mano, `archivo.py::funcion`) y verifica por
  AST que cada una siga existiendo; ademas lista que llamadas con pinta de lectura de
  planilla no estan en `LECTORES`. **Ojo con esa ultima lista:** da falsos positivos a
  proposito -- los wrappers (`cargar_atenciones`, `cargar_inscritos`…) salen como «NO
  VIGILADO» pero el AST SI los caza, porque adentro llaman a un lector de `LECTORES`.
- `probar_hooks.py` - prueba **funcional**: le da a cada check algo que DEBE cazar y
  confirma que lo caza (un check que pasa siempre no sirve). El RUT de prueba se arma en
  runtime, cuerpo aritmetico + DV calculado, para no dejar un literal con forma de RUT en
  disco (§8.1); el `.py` con la flecha Unicode se escribe en `tools/` y se borra en un
  `finally`.

**Los dos llevan `RAIZ` como ruta ABSOLUTA de la maquina del autor** (vivieron en el
scratchpad de la sesion, fuera del repo): archivados como quedaron, hay que ajustar
`RAIZ` para correrlos desde aca.

Lo que la auditoria encontro vivo esta en el `CHANGELOG` de la 2.0.5. Lo unico que quedo
abierto: `check_fuentes --todo` avisa que `rem_utils.cargar_maestro` tiene el contrato con
**encabezado sintetico**, y pide el export real recortado a solo encabezado (skill
`limpiar-refs`). No bloquea.

### `gui-2.0_textos/`

La revision de textos user-facing de la GUI 2.0 (sep-2026), hecha por el autor. El
resultado esta en el codigo y en el commit `722ecbe`; esto es la herramienta.

- `textos.py` - `extraer` recorre por AST los strings de `gui/` (titulos, botones,
  dialogos, resumenes, logs) y escribe dos archivos gemelos, `original.txt` y
  `editable.txt`, para editar uno en un diff lado a lado; `aplicar` vuelca al codigo solo
  los bloques que cambiaron (CRLF-safe, empareja por posicion, respeta los `{placeholders}`
  de las f-strings). **Ojo:** archivado como quedo, con `RAIZ` = la carpeta padre de donde
  vivia (`textos_review/` en la raiz del worktree); hay que ajustar `RAIZ`/`AQUI` para
  correrlo desde aca. Solo cubre `gui/`, no los textos de `programas/` ni `modulos/`.

### `eficiencia-2.0.6/`

Los arneses de los tres primeros arreglos de la **ronda de EFICIENCIA** (sep-2026, sobre
`main`). Estan archivados porque **son la prueba de los numeros del CHANGELOG de la
2.0.6**: los tres cambios se vendieron como equivalencias EXACTAS, y eso hay que poder
volver a verificarlo sin rehacer el razonamiento.

- `bench_3fix.py` - el antes/contra-despues. Mide las tres cosas en una corrida
  (`_estado_dx` de las 28 specs, `norm` sobre 400k celdas, `anotar` de 2000 codigos) y se
  corre **dos veces**: una en un worktree en el commit viejo y otra en el arbol nuevo. Asi
  salieron las cifras del CHANGELOG.
- `equivalencia_estado_dx.py` - 56 comparaciones (28 specs x `instrumento` True/False)
  contra una copia textual de la version 2.0.5, con **fechas llenas de empates a
  proposito**: el unico caso en que recortar columnas podria haber movido un resultado.
- `equivalencia_cruzar.py` - los **12.548 codigos** de la Lista Tabular contra los dos
  catalogos cruzados (25.096 consultas) mas los bordes, tambien contra una copia textual
  de la version vieja.

**Los dos `equivalencia_*` llevan adentro una COPIA de la implementacion vieja** — es
justamente lo que los hace servir, asi que no se actualizan cuando el codigo vivo cambie.
Si vuelven a hacer falta, lo que se compara es «la version de entonces» contra la de hoy.

Los tres se corren con `PYTHONPATH=<raiz del repo>` (viven fuera de `programas/`, y
`equivalencia_cruzar.py` ademas necesita los `catalogos/*.csv.gz` vendorizados). A
diferencia de los otros archivados, **no tienen rutas absolutas**: corren desde aca.

**Lo que midieron y quedo SIN hacer** (el hallazgo que destapo el propio arnes): tras
recortar las columnas, el costo dominante de `_estado_dx` ya no es el `groupby` sino las
tres `str.contains` de las mascaras — 0,44 s de los 0,63 s que quedan —, y una de ellas,
`INSTR_n.str.contains("MEDIC")`, es **invariante entre las 28 specs** y se recalcula 28
veces. Es un hoist de tres lineas; no se hizo porque estaba fuera de los tres hallazgos
que el autor mando aplicar.
