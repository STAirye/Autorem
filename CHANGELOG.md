# Changelog — autoREM

Todos los cambios relevantes de este proyecto se anotan acá.
Formato inspirado en [Keep a Changelog](https://keepachangelog.com/es/).

**Versionado `X.Y.Z`** (ver [CLAUDE.md](CLAUDE.md) §9):
`X` = programa · `Y` = módulos de programa acumulados · `Z` = corrección del
módulo que se está trabajando (reinicia al subir `Y`).

Tipos de cambio: **Agregado** (nuevo) · **Cambiado** · **Corregido** ·
**Eliminado** · **Seguridad**.

---

## [Sin publicar]

- (nada pendiente por ahora)

## [1.2.0] — 2026-07-07

Primer estado bajo la convención `X.Y.Z`. Equivale a la suma de las iteraciones
previas (etiquetadas informalmente v1.2–v1.6; el detalle vive en el historial de
git). Programa **autoREM** (X=1) con **2 módulos** (Y=2: egresos, ingresos).

### Agregado
- **Módulo A05 · Egresos** (`rem_a05_egresos.py`): marca Altas / Traslados /
  Otras Causas de Salud Mental, con patología, subtipo y demografía.
- **Módulo A05 · Ingresos** (`rem_a05_ingresos.py`): gemelo del anterior para
  eventos de INGRESO.
- **Dispatcher GUI + CLI** (`autorem.py`): selector de tareas; corre varias en
  una pasada y produce un solo `…_procesado.xlsx` con una hoja por tarea.
- **Perfiles de formato IRIS / Administrativo**: el usuario elige al inicio de
  qué reporte cargó, con disclaimer para el Administrativo (columnas
  demográficas ausentes, edad tomada de 'Edad de registro formulario').
- **Capa compartida** (`rem_saludmental.py`) y **utilidades genéricas**
  (`rem_utils.py`); base para sumar módulos nuevos.
- Detección de formato con validación cruzada ("elegiste IRIS pero esto parece
  Administrativo…").
- `edad_anios()`: parsea la edad del Administrativo (`'99 años 12 meses…'` → 99;
  menor de 1 año → 0).

### Corregido
- Consola Windows (cp1252): los símbolos `▶·→«»✔` reventaban al imprimir en el
  CLI. Forzado UTF-8 en `stdout`.

### Seguridad
- `.gitignore` excluye `*.xlsx/xls/csv` y salidas: red de seguridad para que
  NUNCA entre PII (datos de pacientes) al repositorio.

---

Historia previa (pre-convención): ver `git log` y los archivos
`rem_marcar_egresos *.py`, conservados como referencia validada.
