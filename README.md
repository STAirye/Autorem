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

## ⬇️ Descargar

**[Descargar autoREM.exe (última versión)](https://github.com/STAirye/Autorem/releases/latest/download/autoREM.exe)** — Windows, doble-clic, sin instalar nada.

Ese enlace **siempre** apunta a la versión más reciente. Si tu antivirus o
SmartScreen advierte "editor desconocido", es un exe sin firmar: procesa todo
**local, no sube nada** (ver [CLAUDE.md](CLAUDE.md) §11). Todas las versiones y
sus notas están en **[Releases](https://github.com/STAirye/Autorem/releases/latest)**.

## Qué cubre hoy

La herramienta es **una sola** (un binario, una versión), y va sumando reportes
de distintos **programas de salud**:

| Programa de salud | Reportes REM | Estado |
|---|---|---|
| **Salud Mental** | A05 egresos · A05 ingresos · **A03 D.3** (PSC/PSC-Y/GHQ-12 → tabla) · **Actividades** (A04·A06·A19a·A26·A27·A32) · **Trabajo perdido** | ✅ |
| **Salud Mental — población** | **SP·P6 A.1** (población en control) + **Rescate de inasistentes** | 🚧 en validación |
| **Respiratorio** | A23 (indicadores del mes · SALA bajo control · Sección G inasistentes crónicos · Sección H inasistentes a citación) | 🚧 IRIS pleno · Admin parcial |

Cada reporte es una **página** de la interfaz, agrupada por programa en la barra
lateral. La salida deja una planilla lista para tabular (**tu archivo original nunca
se modifica**), y su primera hoja es siempre **LEEME**: qué casillas NO cubre ese
módulo y por qué, más los avisos de esa corrida.


---

## ¿Qué ventajas tiene sobre el REM automático de RAYEN?

- **100% offline** — no requiere conexión a internet y **ningún dato sale de este
  computador**: los exports se leen y las salidas se escriben en tu propio equipo.
- **Trazabilidad** — a diferencia de RAYEN, **cada reporte deja la lista de los RUT que
  lo componen** (el A05 marca el export completo; el resto escribe su hoja `*_Detalle`),
  así que cualquier cifra se puede abrir y revisar caso a caso.
- **Transparencia** — programa de **código abierto**, 100% auditable y revisable por
  cualquiera.
- **Apoyo a la gestión** — genera automáticamente **reportes de auditoría** (Trabajo
  perdido, Rescate de inasistentes) para mejorar los flujos de atención y automatizar
  tareas recurrentes.
- **Criterios explícitos** — los criterios de conteo están revisados y escritos en la
  documentación, y la hoja **LEEME** de cada salida dice qué casillas **no** cubre ese
  módulo.

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

### Si clonas este repo

Los hooks de git **no se versionan**: viven en `.git/hooks/` de cada clon. Antes del
primer commit, instálalos:

```bash
python tools/hooks_git.py --instalar
```

Instala **y verifica** cuatro checks de pre-commit:
- **Anti-RUT:** bloquea cualquier RUT con dígito verificador válido, en los archivos y
  en el mensaje del commit.
- **cp1252:** que el código no reviente la consola de Windows.
- **Coherencia de versión.**
- **Contratos de fuentes:** toda función que lee una planilla del usuario debe tener su
  prueba de contrato (que lea >0 filas, que el filtro no vacíe, que las fechas se
  entiendan). Caza al commitear el bug recurrente de leer un export y tabular cero.

- **El autor no se hace responsable** de datos personales que aparezcan en un clon o
  fork donde no se instalaron los hooks.
- **No se acepta ningún PR externo sin los hooks instalados.** Un PR con commits
  hechos con `--no-verify`, o que el anti-RUT bloquearía, se rechaza sin revisión.

---

## Requisitos

- **Python 3.9 o superior** (el entorno del autor corre 3.9.13).
- **openpyxl** (lectura/escritura .xlsx), **pandas** (los módulos data-heavy: A23,
  Actividades, población) y **customtkinter** (la interfaz). Instalar con:

  ```bash
  pip install -r requirements.txt
  ```

  En el `.exe` va todo empaquetado: el usuario final no instala nada.


---

## Uso

### Interfaz gráfica (recomendado)

Doble-clic al `.exe`, o `python autorem.py` (también sirve abrirlo en IDLE y apretar
**F5**). Desde la **2.0.0** la ventana tiene una **barra lateral agrupada por programa
de salud**, con **Inicio** arriba y **Acerca de** abajo; cada reporte es una página.

**No hay que elegir el formato.** IRIS y Administrativo se **detectan por el contenido**
del archivo y la página lo confirma con un banner de color. El selector manual de la 1.x
se eliminó: no podía ganarle a la detección, solo aportaba una forma de equivocarse.

**Salud Mental**

- **A05 · Egresos / Ingresos** — formulario *Control de Salud Mental*. Eliges el
  **archivo**, el **período** (todo el archivo o un mes puntual, por *FECHA FORMULARIO*)
  y la(s) **tarea(s)** (Egresos / Ingresos). Salida: `…_procesado.xlsx` (o
  `…_procesado_AAAA_MM.xlsx` si eliges un mes), con una hoja por tarea. Si el mes
  elegido no tiene formularios, avisa y **no** genera un archivo vacío.
- **Actividades** — la página más completa: estadística de actividades de SM (A04·A24,
  A06 controles + psicosocial grupal, A19a consejerías familiares, A26 VDI SM, A27
  educación, A32 remotas), **con desagregación demográfica** (pueblos originarios,
  migrantes, SENAME, demencia, gestante…). Obligatorios: el export **ADA**
  (Atenciones/Diagnósticos/Actividades) y el de **Atenciones Grupales**. Opcionales:
    - **Informe Inscritos y Adscritos** — para el flag **TRANS** (split M/F por
      selección explícita de GÉNERO).
    - **Monitoreo Multiprofesional** — composición de profesionales de las VDI del **A26**.
    - **Maestro de Actividades** — catálogo RAYEN, autoridad para clasificar el
      **Trabajo perdido** (sin él se usa el *Maestro slim* que viene en el exe).

  Salida: *SM_Detalle* (auditable) + una hoja por sección REM, lista para
  **copiar-pegar al template SA_26**.

  Desde esta misma página salen, con dos casillas:
    - **A03 · D.3 (cuestionarios)** — junta PSC / PSC-Y / GHQ-12 en la **tabla A03·D.3**
      del SA_26 (ingreso/egreso × Bajo/Medio/Alto × rango etario × sexo) + detalle
      auditable. Solo cuenta ingresados al PSM; los «sin riesgo» quedan en el detalle.
      *(En la 1.x tenía pestaña propia; desde la 2.0.0 vive solo acá.)*
    - **Trabajo perdido («saco roto»)** — auditoría que no tributa a ninguna casilla.
      Detecta atenciones cuya actividad trae *mental*/*demencia* pero **no tributan** a
      ninguna casilla SM, y **nombra al funcionario** que las registra. Más dos
      auditorías **por atención** de registro incompleto: *Control SM sin formulario* y
      *SM sin consejería*. Salida: *Por_Actividad* + *Por_Funcionario* + resumen +
      detalle.
- **Población en control** (🚧 *en validación*) — **SP·P6 A.1** (grilla de población
  bajo control por diagnóstico × banda etaria × sexo) y **Rescate de inasistentes**
  (quién lleva 6 o 13 meses sin control, más posibles fallecidos y traslados a
  verificar). Lleva badge de *beta*: sus números todavía se están contrastando.

**Respiratorio**

- **A23 · Respiratorio** — carga el/los export(s) de **atenciones** (del mes), el
  **formulario Otros Crónicos** (histórico: **cárgalo por varios años**, si no la Sección G
  subcuenta) y, opcionalmente, **Estratificación** y el reporte de **Inasistentes NSP**
  (para la Sección H); eliges el **mes a reportar**. Salida: hoja *detalle* por paciente +
  *Sección G* + *Sección H* (por estamento × tramo etario).

Cada página deja elegir la **carpeta de salida**; si la dejas **vacía**, el resultado se
guarda **junto al archivo que cargaste** — no en la carpeta desde donde corres el
programa, porque las salidas llevan RUT. Una salida **nunca pisa** a otra: si el nombre
existe, la corrida sale como `… (1).xlsx`.

Los exports RAYEN/IRIS **modificados** (datos en más de una hoja, p.ej. con una tabla
dinámica agregada) se **rechazan** con un aviso claro.

> ⚠ Carga los exports **tal como los descargas** de RAYEN/IRIS: sin abrirlos ni
> re-guardarlos. Un archivo modificado puede fallar en silencio o dar cifras erróneas.

### Línea de comandos (CONGELADA)

> **No sigue el rediseño de la interfaz** (decisión del autor, sep-2026). Funciona, y
> cubre **solo el A05**; no se le portan los cambios de la GUI, y algún mensaje suyo
> todavía nombra pestañas que ya no existen. Puede revivir más adelante, probablemente
> no. Para todo lo demás, usa la interfaz.

```bash
python autorem.py --cli entrada.xlsx [--formato iris|administrativo] [--tarea ID[,ID2]] [--mes AAAA-MM]
```

- Sin `--formato`: asume **iris**. Sin `--tarea`: corre la primera.
- IDs de tarea: `a05_o_egresos`, `a05_n_ingresos`.
- `--mes AAAA-MM`: filtra por *FECHA FORMULARIO* (sin él, procesa el archivo completo).


---

## Estructura del proyecto

| Ruta | Rol |
|---|---|
| `autorem.py` | **Entry point.** Lanza la interfaz, registra las tareas del A05 y trae el CLI (congelado). |
| `gui/` | **La interfaz** (customtkinter). Una pantalla por archivo en `gui/paginas/`, descubiertas por introspección; `app.py` es el shell y el router, `runner.py` la única frontera con el hilo worker, `widgets.py` y `dialogos.py` las piezas reutilizables. |
| `programas/` | **Capas compartidas.** `rem_utils` (normalización, lectura robusta de exports, demografía), `formatos` (eje IRIS/Administrativo), `rem_saludmental` (formulario *Control de Salud Mental*), `estamentos` y `dotacion` (lookups por funcionario), `poblacion` (tabla por RUN), `cobertura` (hoja LEEME) y `catalogos` (CIE-10 / ENO / GES). |
| `modulos/` | **Un reporte REM por archivo:** A05 egresos/ingresos, A03 D.3, A23 respiratorio, SM Actividades, SM Trabajo perdido, SP·P6 población y SM Rescate de inasistentes. |
| `catalogos/` | Catálogos oficiales del DEIS que shippea el exe, más el *Maestro de Actividades* slim. |
| `refs_tablas/` | Planillas de **ejemplo**: solo banner + encabezado, **cero filas de datos**. |
| `tools/` | Utilitarios de desarrollo: hooks de git, checks de versión y cp1252, mantención de catálogos. |
| `tests/` | Pruebas automáticas (datos sintéticos, sin PII). |
| `docs/` | Planes y contexto por módulo; el *por qué* de cada decisión. |
| `legacy/` | Congelado, no se importa: los monolitos previos al split y la **interfaz 1.x** comprimida. |


---

## Pruebas

Datos 100% sintéticos, sin PII. **329 pruebas** en 17 archivos:

```bash
python tools/correr_tests.py
```

Reparte los archivos en 3 procesos y tarda ~103 s, contra ~194 s de `pytest` a secas
(la ventana de Tk se lleva la mitad de la suite ella sola y no se paraleliza). Si
prefieres el camino directo, `python -m pytest -q` sigue funcionando.

Cada archivo corre solo también, con su propio runner, que es lo cómodo para mirar
una falla aislada:

```bash
python tests/test_sm_actividades.py
```


---

## Empaquetado a `.exe` (Windows)

Para que un colega no técnico lo use con doble-clic, sin instalar Python:

```bash
pyinstaller --clean autoREM.spec
# -> dist/autoREM.exe
```

> **Correlo desde la raíz del repo** (la carpeta con `autorem.py`): el `.spec` arma el
> bundle importando `gui.paginas`, y desde otra carpeta el exe sale sin ninguna pantalla.
> Desde la 2.0.1 el build se aborta solo si eso pasa, en vez de parir un exe roto.

El `autoREM.spec` versionado es la forma oficial: ya lleva los datos que PyInstaller
no sigue solo, porque no son `import`.
- El **Maestro de Actividades**: sin él, el Trabajo Perdido corre en heurística y lo
  avisa en el log.
- Los **catálogos DEIS** de `catalogos/`.

Si cambia lo que shippea el exe, se edita el `.spec` y se commitea. Gotchas
(`PermissionError` de `--clean`, SmartScreen, antivirus institucional) en
[tools/CLAUDE.md](tools/CLAUDE.md) §11.

---

## Versionado

`X.Y.Z` versiona la **herramienta**:

- **X** = cambio grande de arquitectura, **o** las plantillas REM de un año nuevo
  (el SA y el SP cambian cada año). La **2.0.0** fue la interfaz nueva; la 3.0.0
  serán las plantillas 2027.
- **Y** = módulo o reporte nuevo, de cualquier programa de salud.
- **Z** = corrección.

Los **programas de salud** avanzan en paralelo y NO van en el número: se trackean
en una matriz aparte (ver [CLAUDE.md](CLAUDE.md) §9). Detalle en
[CHANGELOG.md](CHANGELOG.md).

## Licencia

[GPL-3.0-or-later](LICENSE). `license_ES.txt` es una traducción no oficial al
español (solo referencia; la versión en inglés es la que vale legalmente).
