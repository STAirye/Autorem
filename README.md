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

Corre **100% local y offline**. Sin nube. Consistente con las Leyes 20.584 y
21.719 (datos sensibles de salud). Licencia **GPL-3.0-or-later**.

> Desarrollado por un médico de APS para uso propio y de colegas. El contexto
> técnico profundo (decisiones de diseño, quirks de RAYEN) está en
> [CLAUDE.md](CLAUDE.md); el detalle de cambios en [CHANGELOG.md](CHANGELOG.md).

## Qué cubre hoy

La herramienta es **una sola** (un binario, una versión), y va sumando reportes
de distintos **programas de salud**:

| Programa de salud | Reportes REM | Estado |
|---|---|---|
| **Salud Mental** | A05 egresos · A05 ingresos · A03 D.3 screening (PSC/PSC-Y/GHQ-12) · **Actividades** (A04·A06·A19a·A26·A27·A32) | ✅ |
| **Respiratorio** | A23 (indicadores del mes · SALA bajo control · Sección G inasistentes crónicos · Sección H inasistentes a citación) | 🚧 IRIS pleno · Admin parcial · falta agregación mensual |

Cada reporte es una **pestaña** en la interfaz. La salida deja una planilla lista
para tabular (**tu archivo original nunca se modifica**).

---

## 🔒 Privacidad (regla dura)

Los exports de RAYEN/IRIS traen **datos identificatorios de pacientes** (RUT,
nombre, dirección, teléfono, fecha de nacimiento). **Nunca** se versionan en git:

- El repositorio vive **fuera** de las carpetas de trabajo sincronizadas; los
  exports se quedan donde estén y la herramienta los lee **por ruta**.
- `.gitignore` bloquea `*.xlsx / *.xls / *.xlsm / *.csv / *.tsv` y la carpeta
  `SENSITIVE_PII/` (donde viven las tablas reales para correr localmente) como
  red de seguridad.
- El único identificador en la salida es el **RUT / RUN** (necesario para el REM).
- El procesamiento es local; nada se sube a ningún lado.

---

## Requisitos

- **Python 3.10+** (probado con 3.14).
- **openpyxl** (lectura/escritura .xlsx) y **pandas** (módulos data-heavy, como el
  respiratorio A23). Instalar con:

  ```bash
  pip install -r requirements.txt
  ```

  (`tkinter`, la interfaz gráfica, viene con el Python de Windows.) En el `.exe`
  todo va empaquetado; el usuario final no instala nada.

---

## Uso

### Interfaz gráfica (recomendado)

Doble-clic a `autorem.py` (o al `.exe`), o desde IDLE abrir `autorem.py` y
apretar **F5**. La ventana tiene **una pestaña por reporte**:

- **REM A05 · Egresos / Ingresos** — formulario *Control de Salud Mental*. Elige
  el **formato** (IRIS o Administrativo), el **archivo** y la(s) **tarea(s)**
  (Egresos / Ingresos). Salida: `…_procesado.xlsx` con una hoja por tarea.
- **REM A03 D.3 · Screening** — instrumentos PSC / PSC-Y / GHQ-12. Autodetecta el
  instrumento por contenido; da el resultado automático (RAYEN) + calculado
  (cortes DISAM) + discrepancia. En formato Administrativo puede cargar la tabla
  *Utilización de Cupos* para rellenar el estamento por nombre de funcionario.
- **REM A23 · Respiratorio** — carga el/los export(s) de **atenciones** (del mes), el
  **formulario Otros Crónicos** (histórico: **cárgalo por varios años**, si no la Sección G
  subcuenta) y, opcionalmente, **Estratificación** y el reporte de **Inasistentes NSP**
  (para la Sección H); elige el **mes a reportar**. Salida: hoja *detalle* por paciente +
  *Sección G* (inasistentes a control de crónicos) + *Sección H* (inasistentes a citación
  Control/Ingreso IRA/ERA, por estamento × tramo etario).
- **REM SM · Actividades** — estadística de actividades de Salud Mental (A04·A24,
  A06 controles + psicosocial grupal, A19a consejerías familiares, A26 VDI SM, A27
  educación, A32 remotas), **con desagregación demográfica** (pueblos originarios,
  migrantes, SENAME, demencia, gestante…). Carga el export **ADA** (Atenciones/
  Diagnósticos/Actividades), el de **Atenciones Grupales** y, opcionalmente, el
  **Informe Inscritos y Adscritos** (solo para el flag **TRANS**); elige el mes. Salida:
  hoja *SM_Detalle* (auditable) + una hoja por sección REM, lista para **copiar-pegar al
  template SA_26**.

Cada pestaña de datos (A23 y SM) deja elegir la **carpeta de salida** (por defecto, la
carpeta del `.exe`), para no perder el resultado junto al input.

> ⚠ Carga los exports **tal como los descargas** de RAYEN/IRIS: sin abrirlos ni
> re-guardarlos. Un archivo modificado puede fallar en silencio o dar cifras erróneas.

### Línea de comandos (avanzado / automatización)

Solo para el A05:

```bash
python autorem.py --cli entrada.xlsx [--formato iris|administrativo] [--tarea ID[,ID2]]
```

- Sin `--formato`: asume **iris**. Sin `--tarea`: corre la primera.
- IDs de tarea: `a05_o_egresos`, `a05_n_ingresos`.

---

## Estructura del proyecto

| Ruta | Rol |
|---|---|
| `autorem.py` | **Entry point.** Dispatcher GUI (una pestaña por reporte) + CLI (solo A05). |
| `programas/rem_utils.py` | Base genérica: normalización, búsqueda de columnas, **lectura robusta de reportes** (`leer_xlsx`, `resolver_columnas`, `cargar_atenciones`) + **demografía reutilizable** (`marcar_demografia`, `gestante_runs`, `trans_map`), usada por los módulos. |
| `programas/rem_saludmental.py` | Capa compartida del formulario *Control de Salud Mental*: validación, diagnóstico/subtipo, demografía, perfiles IRIS/Admin, motor de marcado. |
| `programas/estamentos.py` | Lookup Funcionario→Estamento (transversal a lo Administrativo), desde *Utilización de Cupos*, con failsafe de resolución manual. |
| `modulos/rem_a05_o_egresos.py` · `rem_a05_n_ingresos.py` | Tareas A05: egresos (Alta/Traslado/Otras Causas) e ingresos. |
| `modulos/rem_a03_d3_instrumentos.py` | Screening A03 D.3 (PSC/PSC-Y/GHQ-12), integrado a la GUI. |
| `modulos/rem_a23_respiratorio.py` | REM A23 (Respiratorio), con pandas. |
| `modulos/rem_sm_actividades.py` | REM SM Actividades (A04/A06/A19a/A26/A27/A32), con pandas. Tablas copy-paste al SA_26. |
| `tests/` | Pruebas automáticas (datos sintéticos, sin PII). |
| `legacy/` | Versiones históricas (referencia validada). |

---

## Pruebas

Datos 100% sintéticos, sin PII:

```bash
python tests/test_autorem.py
python tests/test_screening.py
python tests/test_estamentos.py
python tests/test_a23.py
python tests/test_sm_actividades.py
```

---

## Empaquetado a `.exe` (Windows)

Para que un colega no técnico lo use con doble-clic, sin instalar Python:

```bash
pyinstaller --onefile --windowed --name "autoREM" autorem.py
```

Correr desde la raíz del repo (con `programas/` y `modulos/` al lado de
`autorem.py`); PyInstaller sigue los `import` solo. Gotchas (SmartScreen,
antivirus institucional) en [CLAUDE.md](CLAUDE.md) §11.

---

## Versionado

`X.Y.Z` versiona la **herramienta** (X = arquitectura · Y = cada módulo/reporte
nuevo · Z = corrección del módulo en curso). Los **programas de salud** avanzan
en paralelo y NO van en el número: se trackean en una matriz aparte (ver
[CLAUDE.md](CLAUDE.md) §9). Detalle en [CHANGELOG.md](CHANGELOG.md).

## Licencia

[GPL-3.0-or-later](LICENSE). `license ES.txt` es una traducción no oficial al
español (solo referencia; la versión en inglés es la que vale legalmente).
