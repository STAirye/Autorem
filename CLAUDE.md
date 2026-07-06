<!--
This document was generated with the assistance of Claude Fable 5 (Anthropic).
The human author reviewed, modified, and integrated the content.
Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# CLAUDE.md — Proyecto autoREM (Salud Mental, SSMC)

Contexto de proyecto para Claude Code. Este archivo se carga automáticamente al
abrir el repo. Compila el estado a **julio 2026**, tras migrar el desarrollo de
Cowork a Claude Code (para usar git y crear módulos nuevos).

---

## 0. Autor y preferencias de trabajo

- **Autor:** Simón Tobar — médico APS, CESFAM Dr. Luis Ferrada Urzúa (SSMC).
- **Idioma:** inglés y español indiferenciado. Usar **"tú"**, nunca "vos".
- **Estilo:** técnico pero no aburrido; conciso, sin verborrea. El autor tiene
  AuDHD: ir al grano, decir explícitamente cuando algo está equivocado.
- **Privacidad (regla dura):** avisar si por error se cargan datos
  identificatorios de pacientes (RUT, nombre, fecha nacimiento, dirección,
  teléfono). Ver §8.

---

## 1. Qué es el proyecto

Herramientas en Python para automatizar la tabulación del **REM** (Registro
Estadístico Mensual, MINSAL Chile) a partir de exports crudos de **RAYEN/IRIS**.

El módulo actual (único terminado) procesa el export de **"Formularios RAYEN —
Control de Salud Mental"** y produce una tabla lista para tabular los **egresos
del REM A05** (Salud Mental).

- Corre **100% local, offline**. Sin nube. Consistente con Ley 20.584 y 21.719.
- Única dependencia externa: **openpyxl**.

---

## 2. Estado actual del repo

Repo git ya inicializado (rama `main`, fuera de OneDrive). Estructura **v1.3**
tras modularizar (§4.4):

| Archivo | Rol |
|---|---|
| `rem_utils.py` | **BASE COMÚN.** Utilidades genéricas sin lógica de sección: `norm`, `to_year`, `solo_entero`, `buscar_col`, `num_pregunta`, `encontrar_fila_encabezado` (parametrizado), `abrir_carpeta`, `ArchivoInvalido` y la guarda de `openpyxl`. |
| `rem_a05_egresos.py` | **VERSIÓN ACTUAL** (ex `rem_marcar_egresos 1.2.py`). Módulo A05: config clínica, `validar_formato` IRIS/admin, `procesar`, GUI Tkinter y CLI. Importa de `rem_utils`. |
| `rem_marcar_egresos 1.2.py` | Monolito v1.2 (pre-split). Referencia validada; se usó para verificar equivalencia. |
| `rem_marcar_egresos 1.1.py` | Versión previa (CLI puro). Base validada del core. |
| `rem_marcar_egresos v0.2.py`, `rem_marcar_egresos.py` | Históricas. |
| `LICENSE` | Texto GPL-3.0 completo (inglés, el que vale legalmente). |
| `license ES.txt` | Traducción no oficial del GPL-3.0 al español (solo referencia). |
| `.gitignore` | Excluye `*.xlsx/xls/csv`, salidas y artefactos PyInstaller (red de seguridad anti-PII). |

Los exports RAYEN/IRIS con PII y `formato rem administrativo.xlsx` viven **solo
en la carpeta de trabajo (OneDrive), NUNCA en el repo** (§8).

**Estado:** el core está estable y modularizado. Los `.py` viejos se conservan
como referencia; mover a `legacy/` cuando se quiera (§10, "Higiene de repo").

---

## 3. Pipeline del módulo de egresos (`procesar()`)

1. **Recorta** filas de banner/filtros del export (detección en cascada:
   ancla por header → primera fila con columna A vacía → hardcode 16).
2. **No modifica la hoja original** — todo va a una hoja nueva `A05_Egresos`.
3. Detecta cada **egreso** (Alta / Traslado / Otras Causas) por tokens en las
   columnas `"N.- ESTADO"`.
4. Identifica la **patología** (pregunta del diagnóstico) y su **subtipo**.
5. Agrega **identificación + demografía** por evento.
6. Escribe `A05_Egresos` en **formato largo: una fila por evento** (un paciente
   con 2 egresos = 2 filas), con encabezado congelado y autofiltro.

**Columnas de salida** (14, tras quitar `Gestante` en v1.2):
`RUT · Edad_Formulario · Sexo · Tipo_Egreso · Patologia · Subtipo ·
Falta_Subtipo · Madre_menor5 · Pueblos_Originarios · SENAME · Proteccion_Ninez ·
Migrante · Trans · Fila_Origen`

Las columnas demográficas se generan **data-driven** desde `DEMOGRAFIA.keys()`:
agregar/quitar una entrada en ese dict ajusta headers y anchos solos.

---

## 4. Novedades v1.2 (esta iteración)

### 4.1 GUI Tkinter (sin dependencias nuevas)
`lanzar_gui()`: título, caja de instrucciones, cuadro de archivo con
`Examinar…` (o pegar ruta), botón `Procesar`, área de log (mismos mensajes
`[corte]/[A05]/[demo]/[resumen]`) y messagebox de confirmación con conteo por
tipo + opción de abrir la carpeta. `procesar(entrada, salida, log=...)` recibe
un callback `log` (default `print`) para que GUI y CLI compartan el núcleo.

**Arranque (`main()`):**
- Sin args → GUI.
- Arrastrar `.xlsx` sobre el `.exe/.py` → GUI con la ruta precargada.
- `--cli entrada.xlsx [salida.xlsx]` → modo consola (experto/automatización).

### 4.2 Detector de formato (`validar_formato()`) — §5.

### 4.3 Error handler amigable
Mensajes claros para: `openpyxl` faltante, `PermissionError` (abierto en
Excel/OneDrive), archivo inexistente, extensión no-xlsx, formato administrativo
y formato desconocido. En error inesperado vuelca el traceback al log.

### 4.4 Modularización v1.3
El monolito `rem_marcar_egresos 1.2.py` se partió en dos:
- **`rem_utils.py`** — utilidades genéricas reutilizables por cualquier módulo
  del REM (§2). `encontrar_fila_encabezado` quedó **parametrizado** (recibe
  `ancla, usar_blanco_en_a, n_hardcode, max_filas`) en vez de leer globales.
- **`rem_a05_egresos.py`** — solo la lógica A05; importa de `rem_utils`.

Verificado: salida `A05_Egresos` **idéntica** a v1.2 sobre un export sintético
(Alta con/sin subtipo, Trans, Migrante, fila sin egreso). Entry point pasa a ser
`rem_a05_egresos.py` (GUI/CLI viven ahí por ahora; ver §12).

---

## 5. Detector de formato: IRIS vs administrativo

Hay **dos exports RAYEN distintos** y el colega puede confundirlos. El script
solo procesa el de **IRIS** ("Control de Salud Mental") y rechaza el resto.

**Firma IRIS (la que se acepta):** existe fila-encabezado con el ancla
`AÑO APLICACIÓN FORMULARIO` **y** una columna `NÚMERO ... IDENTIFICACIÓN`.

**Firma administrativo (se rechaza con mensaje específico):** banner
`Servicio de Salud` en A1, y/o columnas `Numero de Fichas` /
`Edad de registro formulario` / `Fecha Formulario`. Encabezado en fila 9.
Columnas de estado como `"5.- Estado"` (no `"N.- ESTADO"`). **No** trae el ancla
IRIS. Constantes: `ADMIN_MARKERS`, `ADMIN_BANNER`.

**Desconocido:** cualquier otra cosa → "no reconozco este formato" + checklist.

`ArchivoInvalido(categoria, mensaje)` con `categoria ∈ {"administrativo",
"desconocido"}`. `procesar()` la levanta antes de tocar nada.

---

## 6. Demografía A05: validado vs pendiente

Cada flag: `(tokens_header_fuente, regla)`. Reglas: lista de keywords (match por
substring normalizado → "SI"), `"_no_vacio"`, `"_no_chileno"`. La celda
`ALERTAS ADMINISTRATIVAS` trae **varios valores separados por ';'** → substring
funciona bien.

**Validado (jul-2026, contra valores DISTINTOS reales de `ALERTAS ADMINISTRATIVAS`):**
- `SENAME` → keyword `SENAME` capta `SENAME Justicia Juvenil`.
- `Proteccion_Ninez` → keyword `MEJOR NINEZ` capta `SPE ex Mejor Niñez- Ambulatorio`.
  (SENAME y Proteccion_Ninez quedan **separados**, sin doble conteo.)
- `Migrante` → keyword `MIGRANTE` (alerta explícita). **Cambio v1.2:** antes
  derivaba de `NACIONALIDAD` con `_no_chileno`. Revertible si se prefiere la
  definición por nacionalidad.
- `Madre_menor5` → pregunta 1 del formulario (`¿Usted es Madre de Hijo menor de
  5 años?`), valor "SI". (Ya validado en v1.1.)

**Valores conocidos de `ALERTAS ADMINISTRATIVAS`** (para futuras reglas):
Fonasa Libre Elección · PRAIS · Jubilación de Vejez · Atención Preferente
(Mayor 60 / Cuidador / Discapacidad) · SPE ex Mejor Niñez- Ambulatorio ·
Subsistema Seguridades y Oportunidades · SUF · MIGRANTE · SENAME Justicia Juvenil.

**Eliminado:** `Gestante` — **no existe** en este export (ningún valor de
ALERTAS lo indica). Si aparece la fuente, reañadir la fila en `DEMOGRAFIA`.

**Pendiente de validar (fuente fuera de ALERTAS, keywords aún supuestos):**
- `Pueblos_Originarios` → columna `PUEBLO ORIGINARIO`, regla `_no_vacio`.
- `Trans` → columna `GÉNERO`, si contiene "TRANS" (copia el valor).
- **Acción:** pegar los valores distintos de esas dos columnas (categóricos, sin
  PII) y ajustar.

---

## 7. Decisiones de diseño (NO deshacer sin motivo)

- **Diagnóstico = pregunta a la izquierda del ESTADO**, caminando a la izquierda
  y **saltando** columnas de subtipo/estado (`encontrar_diagnostico()`). Maneja
  los dos layouts: `[¿X?][ESTADO][TIPO X]` (mayoría) y `[¿X?][TIPO/ETAPA][ESTADO]`
  (Suicidio, Alzheimer).
- **Subtipos hardcodeados** en `DIAGNOSTICOS_CON_SUBTIPO` (clave = N.- del
  diagnóstico, valor = N.- de su columna de subtipo): Violencia(4→6),
  Suicidio(11→12), Depresión(18→20), Ansiedad(41→43), Alzheimer(44→45=ETAPA).
- **Subtipo se recorta** quitando el sustantivo del header vía `limpiar_subtipo()`:
  `"Depresión Moderada"` con header `TIPO DE DEPRESIÓN` → `"Moderada"`.
- **Remap deprecated:** Abuso Sexual (pregunta 9) → patología `Violencia`,
  subtipo `Sexual` (`REMAP_DIAGNOSTICO`).
- **Nombre de patología sale crudo** (header tal cual). `LIMPIAR_NOMBRE_PATOLOGIA
  = False` (pendiente cosmético; `limpiar_patologia()` + `OVERRIDE_PATOLOGIA` ya
  existen detrás del flag).
- **Quirk RAYEN clave:** `AÑO APLICACIÓN FORMULARIO` **NO trae el año, trae la
  EDAD a la fecha de llenado** (lo que A05 necesita). `EDAD PACIENTE` es la edad
  a la fecha de descarga → se ignora.
- **RUT** viene de `NUMERO TIPO IDENTIFICACION`, ya con guión y DV (`11111111-1`).
- **Otras Causas es manual por diseño:** requiere decisión clínica caso a caso
  (abandono vs clínica). Solo se flaggea; no se clasifica automático.

### Zonas de configuración editables (arriba del archivo)
`BUSQUEDAS` · `DIAGNOSTICOS_CON_SUBTIPO` · `REMAP_DIAGNOSTICO` · `DEMOGRAFIA` ·
`AVISAR_ALTA_SIN_SUBTIPO` · (técnicas) `ANCLA_ENCABEZADO`, `ADMIN_MARKERS`, etc.

---

## 8. Privacidad (regla dura del proyecto)

- **Repo y datos van separados.** El repo git vive **fuera** del OneDrive del
  trabajo (proyecto personal). Los exports RAYEN/IRIS con PII se quedan en la
  carpeta de trabajo. El repo **nunca** debería ver PII.
- La herramienta lee el export **por ruta** (GUI/CLI apuntan a donde esté el
  archivo); no necesita que el `.xlsx` viva dentro del repo.
- Procesamiento **local, offline**. El único identificador en la salida es el
  **RUT** (necesario para el A05 y para revisar Otras Causas caso a caso).
- **Nunca commitear datos de pacientes.** Si para debug hace falta una planilla
  dentro del repo, que sea **anonimizada** (sin RUT, nombre, fecha nacimiento,
  dirección, teléfono). El `.gitignore` excluye `*.xlsx/*.xls/*.csv` como red de
  seguridad, incluso estando el repo fuera de OneDrive.
- Al trabajar con Claude, avisar si por error se cargan datos identificatorios.

---

## 9. Convenciones de código

- **Header en cada archivo** (código y docs): bloque con
  *"This code/document was generated with the assistance of [modelo]. The human
  author reviewed, modified, and integrated the code."* + autor
  (Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa) + `SPDX-License-Identifier:
  GPL-3.0-or-later` + versión.
- **Licencia:** GPL-3.0-or-later. Al distribuir binarios, incluir `LICENSE`
  con el texto completo (ya está en el repo; `license ES.txt` es traducción de
  referencia, no la versión legal).
- Comentarios y mensajes de usuario en español; nombres de función mixtos OK.

---

## 10. Git — arranque y flujo

**El repo vive fuera del OneDrive del trabajo** (proyecto personal, carpeta
aparte). Los exports con PII se quedan en la carpeta de trabajo y NO se copian
al repo. Arranque sugerido:

```bash
# En la carpeta personal del repo (fuera de OneDrive), con los .py + CLAUDE.md
# + .gitignore + license.txt ya copiados (SIN ningún .xlsx):
git init
git add CLAUDE.md .gitignore "rem_marcar_egresos 1.2.py" license.txt CONTEXTO_COWORK_rem_egresos.md
git commit -m "Import inicial: módulo egresos A05 v1.2 + contexto"
```

**Antes del primer commit, confirmar que NINGÚN .xlsx entra** (`git status` no
debe listar planillas). El `.gitignore` ya excluye `*.xlsx/*.xls/*.csv` como red
de seguridad.

### Estado git (jul-2026)
- Repo inicializado en rama `main`, identidad local `Simón Tobar`.
- Commits: `Import inicial` (v1.2 monolito) → `Modularizar` (v1.3, split
  utils/A05). Tag `v1.2` en el import.
- El módulo actual ya tiene nombre limpio (`rem_a05_egresos.py`, sin versión ni
  espacios).

### Higiene pendiente (opcional)
- Mover los `.py` viejos (`1.1`, `1.2`, `v0.2`, `rem_marcar_egresos.py`) a
  `legacy/` — git ya guarda la historia; solo ordenan la carpeta.
- Tag `v1.3` cuando se estabilice.

---

## 11. Empaquetado a .exe (pendiente inmediato)

Meta: colega no técnico hace doble-clic, sin instalar Python.

```bash
pyinstaller --onefile --windowed --name "MarcarEgresos" rem_a05_egresos.py
# -> dist/MarcarEgresos.exe
```

**Gotchas:**
- Entry point = `rem_a05_egresos.py`. `rem_utils.py` debe estar **en la misma
  carpeta**; PyInstaller sigue el `import` solo y lo empaqueta.
- El `.exe` **debe construirse en Windows** (PyInstaller no cross-compila).
- **SmartScreen / antivirus institucional:** exe sin firmar dispara "editor
  desconocido" y a veces falsos positivos; en máquinas SSMC bloqueadas puede
  requerir whitelist de IT. Alternativa: `--onedir` (a veces molesta menos).
  Argumento para IT: **procesa todo local, no sube nada** (Ley 20.584/21.719).
- Junto al `.exe`, distribuir `LICENSE` (GPLv3, `gnu.org/licenses/gpl-3.0.txt`).
- `openpyxl` se empaqueta solo; `tkinter` viene con el Python de Windows.

---

## 12. Roadmap / arquitectura futura

- **`rem_utils.py` compartido:** ✅ HECHO (v1.3, §4.4). Extraídas `norm`,
  `to_year`, `solo_entero`, `buscar_col`, `num_pregunta`,
  `encontrar_fila_encabezado`, `abrir_carpeta`, `ArchivoInvalido`. Pendiente
  posible: un `validar_formato` genérico (hoy cada módulo trae el suyo).
- **Un módulo por sección del REM** (A05 es el primero). Estructura:
  `rem_utils.py` + `rem_a05_egresos.py` + `rem_<seccion>.py`, con una GUI/CLI
  común que despache al módulo correcto según el export detectado. Hoy la GUI/CLI
  vive dentro de `rem_a05_egresos.py`; al sumar el 2º módulo, extraerla a un
  despachador común.
- **Otras Causas (post-GUI):** popup con lista de RUTs + dropdown para clasificar
  (abandono vs clínica) y sumar al reporte final.
- **Abandonos:** dependen del cálculo del "PowerBI madre" — etapa aparte.
- **Cosmético:** `LIMPIAR_NOMBRE_PATOLOGIA = True` + precargar `OVERRIDE_PATOLOGIA`
  para nombres bonitos.

---

## 13. Gotchas técnicos

- **OneDrive + shell:** el repo git NO está en OneDrive, pero los **exports de
  datos sí** (carpeta de trabajo). Al leer un `.xlsx` recién descargado/sincronizado
  desde una shell, se puede ver una versión a medio sincronizar (ej. truncada).
  Si un test falla raro tras tocar un archivo en OneDrive, forzar
  re-lectura/sincronización antes de concluir que es un bug del código.
- **Excel abierto:** si el `.xlsx` de salida está abierto, `wb.save()` lanza
  `PermissionError` — ya manejado con mensaje amable.
- **Validación pendiente end-to-end:** el core está validado contra un export
  real anonimizado de enero 2026 (393 filas → 16 eventos: 11 Alta, 1 Traslado,
  4 Otras Causas). Correr v1.2 sobre un export IRIS real y revisar los dos flags
  demográficos pendientes (§6).
