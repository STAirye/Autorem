<!--
This document was generated with the assistance of Claude Opus 5 (Anthropic).
The human author reviewed, modified, and integrated the content.
Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# legacy/ — código congelado

Nada de acá se importa. Es referencia de equivalencia: sirve para contestar «¿esto
antes daba el mismo número?», no para arreglarlo. `legacy/` está **exento** del
versionado (CLAUDE.md §9): sus archivos no llevan la versión vigente.

| Archivo | Qué es |
|---|---|
| `rem_marcar_egresos*.py` | Los monolitos previos al split en `programas/` + `modulos/`. |
| `autorem_gui_tk_1.9.18.py.gz` | **La GUI 1.x completa** (Tkinter/ttk, pestañas) + dispatcher + CLI, tal como quedó antes de que la GUI 2.0 la reemplazara en la **2.0.0**. Es el `autorem.py` de la 1.9.18, la última versión que la shippeó. |

**El `.gz` está comprimido a propósito** (decisión del autor, plan de la GUI 2.0 §8):
así ninguna herramienta del repo lo escanea ni lo tropieza — `check_cp1252` y
`check_version` recorren `*.py`, y el hook anti-RUT salta los binarios. No se
descomprime «para arreglarlo». Se lee con:

```bash
python -c "import gzip,sys;sys.stdout.write(gzip.open(sys.argv[1],'rt',encoding='utf-8').read())" legacy/autorem_gui_tk_1.9.18.py.gz
```

No introduce riesgo de PII: es código propio que ya pasó por los hooks y que está en
claro en todo el historial de git. No es un binario de origen externo. **Ojo:** el
`.gitignore` ignora `*.gz` en bloque (son datos), así que el congelado necesita su
línea de whitelist explícita — el plan daba por hecho que un `.py.gz` no matcheaba, y
sí matchea.
