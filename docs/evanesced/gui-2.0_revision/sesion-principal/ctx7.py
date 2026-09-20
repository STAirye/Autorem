import sys
sys.path.insert(0, r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\a40108ff-012a-4b37-baf2-2a1dc332a634\scratchpad")
from ed import reemplazar

C = r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\648a107e-f033-4d56-a55d-a415a58f003e\scratchpad\review_context.md"
reemplazar(C, [(
"""Repo: `E:\\git\\Autorem` (Windows, git). Current checkout = branch `gui-2.0` (clean; see the UPDATE below about `fd1b0cc`).
Merge-base with main: `03e15f6`. Review scope = `git diff main...HEAD` (saved at
`C:\\Users\\Simon\\AppData\\Local\\Temp\\claude\\E--git-Autorem\\648a107e-f033-4d56-a55d-a415a58f003e\\scratchpad\\gui20_fd1b0cc.diff`, 5815 lines; the old `gui20.diff` is STALE).""",
"""Repo: `E:\\git\\Autorem` (Windows, git). Current checkout = branch `gui-2.0` at `f42308d` (clean; see the UPDATEs below).
Merge-base with main: `03e15f6`. Review scope = `git diff main...HEAD` (saved at
`C:\\Users\\Simon\\AppData\\Local\\Temp\\claude\\E--git-Autorem\\648a107e-f033-4d56-a55d-a415a58f003e\\scratchpad\\gui20_f42308d.diff`, 8367 lines).
**STALE, do not use:** `gui20.diff` and `gui20_fd1b0cc.diff` (they predate rounds 5-6)."""), (
"""## ⚠ UPDATE 2026-09-17 — backup commit `fd1b0cc` (READ BEFORE THE DIFF)""",
"""## ⚠ UPDATE 2026-09-18 — second backup commit `f42308d` (READ FIRST)
Rounds 5 and 6 are now committed and pushed as `f42308d` ("wip(gui-2.0): revision rondas
5-6 + fixes, todavia 1.9.17 (sin cerrar)"), on top of `fd1b0cc`. Same rules as below: it
is a BACKUP, not a release. Version stays **1.9.17**, the CHANGELOG entry stays OPEN, and
"wip commit" / "version not bumped" are NOT findings. The diff to review is
`gui20_f42308d.diff` (8367 lines).
- What rounds 5 and 6 already fixed is in `docs/review_gui-2.0_pendiente.md` §1.F (round 5,
  cross-file tracer) and §1.G (round 6, Tk/customtkinter/threads pitfalls). Read them,
  plus §2 (discarded), before reporting anything.
- **customtkinter 6.0.0 IS installed** in the local Python 3.9
  (`C:\\Users\\Simon\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\customtkinter`),
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

## ⚠ UPDATE 2026-09-17 — backup commit `fd1b0cc` (superseded by the one above)"""), (
"""The environment is Python 3.9.13 + pandas 2.3.3 + openpyxl 3.1.5 (`python`). `customtkinter`
is NOT installed (the author tests with pandas 3.0.5 / Python 3.14).""",
"""The environment is Python 3.9.13 + pandas 2.3.3 + openpyxl 3.1.5 (`python`). `customtkinter`
6.0.0 and `pytest` ARE installed (see the 2026-09-18 UPDATE; the author also tests with
pandas 3.0.5 / Python 3.14)."""),
])
print("ok")
