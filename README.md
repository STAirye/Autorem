<!--
This document was generated with the assistance of Claude Opus 4.8 (Anthropic).
The human author reviewed, modified, and integrated the content.
Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# autoREM

Herramientas en Python para **automatizar la tabulación del REM** (Registro
Estadístico Mensual, MINSAL Chile) a partir de los exports crudos de
**RAYEN / IRIS**.

Hoy cubre el formulario **"Control de Salud Mental"**: marca los **egresos** e
**ingresos** para el **REM A05** (patología, subtipo y caracterización
demográfica), dejando una planilla lista para tabular.

- Corre **100% local y offline**. Sin nube. Consistente con las Leyes 20.584 y
  21.719 (datos sensibles de salud).
- Única dependencia externa: **openpyxl**.
- Licencia **GPL-3.0-or-later**.

> **Nota:** desarrollado por un médico de APS para uso propio y de colegas. El
> contexto técnico profundo (decisiones de diseño, quirks de RAYEN) está en
> [CLAUDE.md](CLAUDE.md).

---

## 🔒 Privacidad (regla dura)

Los exports de RAYEN/IRIS traen **datos identificatorios de pacientes** (RUT,
nombre, dirección, teléfono). **Nunca** se versionan en git:

- El repositorio vive **fuera** de las carpetas de trabajo sincronizadas; los
  exports se quedan donde estén y la herramienta los lee **por ruta**.
- `.gitignore` bloquea `*.xlsx / *.xls / *.csv` como red de seguridad.
- El único identificador en la salida es el **RUT** (necesario para el A05).
- El procesamiento es local; nada se sube a ningún lado.

---

## Requisitos

- **Python 3.10+** (probado con 3.14).
- **openpyxl** — instalar con:

  ```bash
  pip install -r requirements.txt
  ```

  (`tkinter`, la interfaz gráfica, viene con el Python de Windows.)

---

## Uso

### Interfaz gráfica (recomendado)

Doble-clic a `autorem.py` (o al `.exe`), o desde IDLE abrir `autorem.py` y
apretar **F5**. En la ventana:

1. Elige el **formato** del reporte que descargaste (IRIS o Administrativo).
2. Elige el **archivo** Excel.
3. Marca la(s) **tarea(s)** (Egresos / Ingresos) y presiona **Procesar**.

Se crea una copia `…_procesado.xlsx` con una hoja por tarea
(`A05_Egresos`, `A05_Ingresos`). **Tu archivo original no se modifica.**

### Línea de comandos (avanzado / automatización)

```bash
python autorem.py --cli entrada.xlsx [--formato iris|administrativo] [--tarea ID[,ID2]]
```

- Sin `--formato`: asume **iris**.
- Sin `--tarea`: corre la primera tarea. IDs: `a05_egresos`, `a05_ingresos`.
- Varias tareas → un solo archivo con una hoja por tarea.

---

## Estructura del proyecto

| Archivo | Rol |
|---|---|
| `autorem.py` | **Entry point.** Dispatcher GUI + CLI: selector de formato y tareas. |
| `rem_utils.py` | Utilidades genéricas del REM (texto, columnas, apertura de archivos). |
| `rem_saludmental.py` | Capa compartida del formulario "Control de Salud Mental": validación, diagnóstico/subtipo, demografía, perfiles IRIS/Admin. |
| `rem_a05_egresos.py` | Módulo de tarea: egresos (Alta/Traslado/Otras Causas). |
| `rem_a05_ingresos.py` | Módulo de tarea: ingresos. |
| `tests/` | Pruebas automáticas (datos sintéticos, sin PII). |
| `legacy/` | Versiones históricas (referencia validada). |

---

## Pruebas

Datos 100% sintéticos, sin PII. Se corren sin instalar nada extra:

```bash
python tests/test_autorem.py
```

Verifican, entre otras cosas, que la salida de egresos siga siendo **idéntica**
a la versión validada, que ingresos funcione, y que los perfiles IRIS/Admin
detecten y procesen bien cada formato.

---

## Empaquetado a `.exe` (Windows)

Para que un colega no técnico lo use con doble-clic, sin instalar Python:

```bash
pyinstaller --onefile --windowed --name "autoREM" autorem.py
```

Los 5 `.py` deben estar en la misma carpeta (PyInstaller sigue los `import`
solo). Detalles y gotchas (SmartScreen, antivirus institucional) en
[CLAUDE.md](CLAUDE.md) §11.

---

## Versionado

Esquema `X.Y.Z`: `X` = programa · `Y` = módulos acumulados · `Z` = correcciones
del módulo actual. Ver [CHANGELOG.md](CHANGELOG.md).

## Licencia

[GPL-3.0-or-later](LICENSE). `license ES.txt` es una traducción no oficial al
español (solo referencia; la versión en inglés es la que vale legalmente).
