# Code review context — autoREM, branch `gui-2.0` vs `main`

Repo: `E:\git\Autorem` (Windows, git). Current checkout = branch `gui-2.0` at `f42308d` (clean; see the UPDATEs below).
Merge-base with main: `03e15f6`. Review scope = `git diff main...HEAD` (saved at
`C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\648a107e-f033-4d56-a55d-a415a58f003e\scratchpad\gui20_f42308d.diff`, 8367 lines).
**STALE, do not use:** `gui20.diff` and `gui20_fd1b0cc.diff` (they predate rounds 5-6).
Bugs in UNCHANGED lines of functions the diff touches or CALLS are in scope when the new
code re-exposes them (e.g. a GUI page calling into `programas/` or `modulos/`).

DO NOT modify anything inside `E:\git\Autorem` (no edits, no git commands that change state,
no outputs written into the repo). Scratch files go ONLY under the scratchpad dir above.
The environment is Python 3.9.13 + pandas 2.3.3 + openpyxl 3.1.5 (`python`). `customtkinter`
6.0.0 and `pytest` ARE installed (see the 2026-09-18 UPDATE; the author also tests with
pandas 3.0.5 / Python 3.14). GUI modules import normally; a real window needs a
display (`tests/test_gui_construccion.py` shows how to build pages and pump events).
Calling the underlying programas/modulos functions with the same arguments the page's
`correr`/`preparar` passes is still the cheapest repro.

## ⚠ UPDATE 2026-09-18 — second backup commit `f42308d` (READ FIRST)
Rounds 5 and 6 are now committed as `f42308d` (the author pushes it) ("wip(gui-2.0): revision rondas
5-6 + fixes, todavia 1.9.17 (sin cerrar)"), on top of `fd1b0cc`. Same rules as below: it
is a BACKUP, not a release. Version stays **1.9.17**, the CHANGELOG entry stays OPEN, and
"wip commit" / "version not bumped" are NOT findings. The diff to review is
`gui20_f42308d.diff` (8367 lines).
- What rounds 5 and 6 already fixed is in `docs/review_gui-2.0_pendiente.md` §1.F (round 5,
  cross-file tracer) and §1.G (round 6, Tk/customtkinter/threads pitfalls). Read them,
  plus §2 (discarded), before reporting anything.
- **customtkinter 6.0.0 IS installed** in the local Python 3.9
  (`C:\Users\Simon\AppData\Local\Programs\Python\Python39\lib\site-packages\customtkinter`),
  and so is `pytest`. The "NOT installed" line further down is outdated: you can import
  the GUI and read CTk's source directly.
- **237 tests.** Every `tests/test_*.py` imports `tests/_aislar_cache.py` FIRST, which
  points the user caches (`~/.autorem/dotacion.json`, `estamentos.json`) at a temp dir.
  If you write a repro script that touches `programas.dotacion` / `programas.estamentos`,
  do the same (or set their `RUTA_CACHE` yourself): the suite used to overwrite the
  author's REAL cache, and that must not happen again.
- New shared pieces a reviewer will meet (all documented in their docstrings):
  `rem_utils.abrir_xlsx_ro`/`filas_hoja` (every read_only read), `rutas_libres` (outputs
  never overwrite: `… (n).xlsx`, same n for a whole run), `escribir_atomico` (temp +
  rename), `leer_cache_json`/`guardar_cache_json`/`apartar_cache` + `_AVISOS_CACHE`
  (cache failures are shown by `gui.runner.avisar_cache`), `runner.Canal` (only the
  latest async preview gets painted), `dialogos._DOTACION_ABIERTA` (one dotación dialog
  at a time: `CTkToplevel.__init__` runs a full `update()` on Windows), and
  `App._al_cerrar` (the X asks when a run is alive).
- Angles already run: A (recurrent empty data), B (behavior removed by the port), C
  (cross-file tracer), D (language/framework pitfalls). Still NOT run: reuse /
  simplification / altitude, efficiency, conventions (version headers of the rest of
  `gui/`), and the port-parity pass for `_tab_beta` and the dotación dialogs (ledger §4).

## ⚠ UPDATE 2026-09-17 — backup commit `fd1b0cc` (superseded by the one above)
The ~2.4k lines of rounds 1-4 fixes that used to be UNCOMMITTED are now committed and
pushed as `fd1b0cc` ("wip(gui-2.0): revision rondas 1-4 + fixes, todavia 1.9.17 (sin
cerrar)") on `origin/gui-2.0`. **It was pushed ONLY as a backup** (the author was nervous
about having 5k lines without a remote copy). It is NOT a release and NOT a finished state:
- The version intentionally stays **1.9.17** and the `## [1.9.17]` CHANGELOG entry is still
  OPEN. Do NOT report "WIP commit", "version not bumped", "CHANGELOG entry reused/open" or
  "commit message says wip" as findings.
- The working tree is clean again, so `git diff main...HEAD` now INCLUDES those fixes.
  The old `gui20.diff` (3209 lines) predates them and is STALE — use
  `gui20_fd1b0cc.diff` (same folder, `git diff main...fd1b0cc`) instead.
- What was already fixed/discarded is in `docs/review_gui-2.0_pendiente.md` §1/§2 (in the
  repo). Read it before reporting, as before.

## What the tool is
autoREM: local tool that tabulates Chile's REM (monthly health statistics) from raw RAYEN/IRIS
Excel exports. Numbers get copied into an official report, so **a plausible-but-wrong number is
the worst possible bug** (worse than a crash). Rules from the root CLAUDE.md (quote them if you
flag a convention violation):
1. Privacy: never patient data in the repo. Outputs carry RUT and must be written NEXT TO the
   input exports (default output folder = folder of the input files, NOT the cwd), outside the repo.
2. "Fallar ruidoso, nunca callado y errado." Month without data -> `ArchivoInvalido`, guard on
   the SOURCE, not on the output cell (§3.1).
3. Only ASCII in `.py` files that print to console (cp1252) — the GUI string literals with
   accents are existing practice; flag only arrows/box chars/emoji in console output paths.
4. Normalization: search text ALWAYS with `contiene_todos`/`contiene_alguno` or
   `serie_norm.str.contains(norm("literal"))`.
5. Detect by CONTENT, never by file name.
6. 100% local/offline.
Versioning §9: `X.Y.Z`; every `.py` in `autorem.py`, `programas/`, `modulos/`, `tools/` (and now
`gui/`) carries the version of ITS last change; `tools/check_version.py` verifies; "Árbitro
anti-colisión entre sesiones paralelas = el CHANGELOG". Folder CLAUDE.md files exist in
`programas/`, `modulos/`, `tools/`; the GUI plan is `docs/GUI_2.0_plan.md`.

## What the branch does
Adds GUI 2.0 (customtkinter): `gui/app.py` (shell, router, `_resolver_ctx`, `Pagina`),
`gui/registro.py` (page discovery), `gui/runner.py` (worker thread + error dispatch),
`gui/widgets.py`, `gui/dialogos.py` (Estamentos + Dotación modals), pages in
`gui/paginas/` (a05, a23, sm, poblacion, inicio, about). Moves
`refs_tablas/maestro_slim.csv.gz` -> `catalogos/maestro_slim.csv.gz` (+ .gitignore, spec,
tools/slim_maestro.py). Adds "gui" to `tools/check_version.py` DIRS_VERSIONADOS.
Old GUI `autorem.py` is still the exe entry point (frozen until step 11 of the plan).
Commit c38a8cc (on this branch only) fixes a bug in `programas/poblacion.py` and bumps 1.9.16.

## THE RECURRENT BUG (user asked for special attention) — c38a8cc
`poblacion.cargar_inscritos()` with an export that has a header but **0 data rows** returned an
empty DataFrame; downstream (`construir_poblacion`) a column built on the empty frame ended up
dtype float64 instead of object and `.str.contains()` raised
`AttributeError: Can only use .str accessor with string values, not floating` — a cryptic crash
instead of a clear `ArchivoInvalido("sin_datos", ...)` at the SOURCE. Fix: guard `len(d)==0`
right after loading. The same family was fixed before in 1.9.12 (6ca8b6e): A23 with an empty
export crashed with `ValueError: NaTType does not support strftime` while logging min/max dates
before reaching `filtrar_mes`'s guard. Both were found by the GUI 2.0 session testing pages
against the header-only example files in `refs_tablas/*.xlsx` (0 data rows by design).
Generalized bug class to hunt:
- a loader that accepts an export with 0 data rows (or a result that becomes empty after a
  filter: month, program mask, dedupe, responsible-person filter, date parse) and lets the empty
  frame flow downstream, where `.str` / `.dt` accessors, `min()/max()` -> NaT formatting,
  `int(NaN)`, `iloc[0]`, `idxmax`, `sorted()` of mixed NaN/str, groupby on empty, `np.where`
  producing float64, `.map/.apply` on empty object series inferring float64, etc. crash
  cryptically — OR, worse, silently produce zeros/wrong numbers instead of `ArchivoInvalido`.
- the same guard present in one loader but missing in its siblings (c38a8cc only guarded
  Inscritos; check formularios, ADA, grupal, multiprofesional, maestro, estamentos, questionnaires,
  Otros Crónicos, estratificación, NSP loaders).
- GUI code paths (preview callbacks, `dialogos.dotacion_ada`, `al_completar`, `resumen`) that
  run on empty/partial data OUTSIDE the worker's error handling, so a crash there is not shown to
  the user at all (Tk callback exception in a windowed exe = invisible).

## Facts already verified by the lead reviewer (don't re-derive; build on them)
- `main` ALSO released a different 1.9.16 (10beb79, 2026-09-16, "saco roto ... por ATEN ID",
  178 tests). This branch's c38a8cc (2026-09-17) claims 1.9.16 too, with a different CHANGELOG
  entry and "183 tests" -> version collision. **[RESOLVED: branch moved to 1.9.17, ledger §1.E]**
- `main`'s `programas/poblacion.py` does NOT have the c38a8cc guard (fix only on gui-2.0).
- ~~`requirements.txt` does not list `customtkinter`.~~ **[RESOLVED, ledger §1.E]**

## Output format (return exactly this, no prose preamble)
Up to 8 candidates, most severe first, each as:
```
- file: <repo-relative path>
  line: <1-indexed line in the CURRENT file on gui-2.0>
  category: <correctness | recurrent-empty-data | reuse | simplification | efficiency | altitude | conventions | test-coverage | ...>
  summary: <one sentence stating the defect>
  failure_scenario: <concrete inputs/state -> wrong output/crash; for cleanup: concrete cost>
  evidence: <quoted line(s) + any command output you ran>
```
If you find nothing real for your angle, return an empty list. Do not pad.
