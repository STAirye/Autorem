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

Repo git ya inicializado (rama `main`, fuera de OneDrive). Versión **1.3.2**
(esquema `X.Y.Z`, §9): capa compartida + módulos egresos/ingresos + screening
A03 D.3 + dispatcher con perfiles y GUI de pestañas.

**Layout de carpetas** (raíz limpia: solo `autorem.py` de código):
```
autorem.py            entry point / dispatcher (raíz)
programas/            motor y base compartida (paquete)
  rem_utils.py
  rem_saludmental.py
  estamentos.py
modulos/              módulos de tarea (paquete)
  rem_a05_o_egresos.py
  rem_a05_n_ingresos.py
  rem_a03_d3_instrumentos.py
legacy/               versiones viejas (no se importan)
tests/                pruebas automáticas
refs tablas/          planillas de EJEMPLO anonimizadas (SÍ versionadas)
```
Imports **absolutos** rooteados en la raíz: `from programas.rem_utils import …`,
`import programas.rem_saludmental as sm`, `from modulos import rem_a05_o_egresos`.
Funcionan porque la raíz (donde vive `autorem.py`) está en `sys.path`.

**Convención de nombre de módulo de tarea:** `rem_<pestaña>_<casilla>_<descriptor>`,
donde `<casilla>` es la celda/columna del REM (A05: `n`=ingresos, `o`=egresos).
El descriptor y el `id` del `TAREA` la incluyen (ej. `a05_o_egresos`). El próximo
módulo (screening A03 D.3) será `rem_a03_d3_instrumentos.py`.

| Archivo | Rol |
|---|---|
| `autorem.py` | **ENTRY POINT (dispatcher GUI + CLI).** GUI con **una pestaña por módulo/reporte** (`ttk.Notebook`): A05 egresos/ingresos (selector formato + tareas) y A03 screening (autodetección de instrumento). Registro de módulos, orquestación cargar-una-vez/guardar-una-vez. CLI = solo A05. |
| `programas/rem_utils.py` | **BASE COMÚN genérica REM.** `norm`, `to_year`, `solo_entero`, `edad_anios`, `buscar_col`, `num_pregunta`, `encontrar_fila_encabezado` (parametrizado), `abrir_carpeta`, `ArchivoInvalido`, `VERSION` y la guarda de `openpyxl`. |
| `programas/rem_saludmental.py` | **CAPA COMPARTIDA del formulario 'Control de Salud Mental'.** Config clínica (diagnósticos, subtipos, demografía), `es_estado`, `encontrar_diagnostico`, `limpiar_subtipo`, detección/validación de formato, **PERFILES IRIS/Admin** y el motor `marcar_eventos()`. |
| `programas/estamentos.py` | **Lookup Funcionario→Estamento** desde el reporte 'Utilización de Cupos' (Admin). El screening Admin no trae estamento (solo nombre); esto lo rellena. `cargar_estamentos()` (dedup + aviso de conflictos) y `buscar_estamento()` (match normalizado). La TABLA de nombres queda LOCAL (no al repo). |
| `modulos/rem_a05_o_egresos.py` | **Módulo de tarea (fino).** Egreso (casilla O): config Alta/Traslado/OtrasCausas + wrappers `agregar_hoja`/`procesar` + descriptor `TAREA` (`id: a05_o_egresos`). |
| `modulos/rem_a05_n_ingresos.py` | **Módulo de tarea (fino).** Ingreso (casilla N): gemelo de egresos, token ESTADO = `INGRESO`, hoja `A05_Ingresos`, columna `Tipo_Ingreso` (`id: a05_n_ingresos`). |
| `modulos/rem_a03_d3_instrumentos.py` | **Módulo screening A03 D.3 (PSC/PSC-Y/GHQ-12).** Reporte DISTINTO al de Salud Mental (perfiles + autodetección propios, self-contained). Autodetecta formato + instrumento por contenido; da resultado automático (col RESULTADO) + calculado DISAM (`clasificar_*(puntaje)`) + discrepancia + momento (`1.- Estado`) + estamento (IRIS). Core hecho; **falta integrar a la GUI** y v2 (lookup admin, conteos, popup). |
| `legacy/rem_marcar_egresos 1.2.py` | Monolito v1.2 (pre-split). Referencia validada de equivalencia (la usa el test). |
| `legacy/…` (1.1, v0.2, .py) | Históricas. |
| `LICENSE` / `license ES.txt` | GPL-3.0 (inglés = legal; ES = referencia). |
| `.gitignore` | Excluye `*.xlsx/xls/csv`, salidas y artefactos PyInstaller (red anti-PII). |

Los exports con PII (IRIS y Administrativo reales) viven **solo en la carpeta de
trabajo (OneDrive), NUNCA en el repo** (§8). Las planillas de EJEMPLO van en
`refs tablas/` y **sí se versionan**, pero con **whitelist POR-ARCHIVO** en el
`.gitignore` (no del folder entero): cada planilla se habilita a mano SOLO tras
verificar que no tiene PII. Un `.xlsx` que caiga ahí queda **ignorado** hasta
vetarlo (así ya se evitó colar un export IRIS real por error, jul-2026).
Versionados hoy: exports de EJEMPLO (RAYEN/IRIS/PowerBI con datos falsos) para
egresos/ingresos/screening/población, `CALCULADOR A05`, y las **plantillas
target SA/SP `.xlsm`** — estas se versionan para detectar cuándo MINSAL cambia
su estructura (git nota el cambio aunque no muestre diff legible del binario).
El `.xls` de RAYEN NO se versiona: openpyxl no lee `.xls` → convertir a `.xlsx`.

**Arquitectura (2 ejes ortogonales):**
- **Perfil de formato** (`rem_saludmental.PERFILES`): `iris` | `administrativo`.
  Define cómo ubicar encabezado/columnas y qué validar. Lo elige el usuario.
- **Tarea** (`autorem.TAREAS`): egresos | ingresos. Agnóstica al formato; aporta
  qué token de ESTADO flaggear y su hoja. Tareas del mismo archivo corren juntas
  → un solo `…_procesado.xlsx` con una hoja por tarea.

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
(Alta con/sin subtipo, Trans, Migrante, fila sin egreso).

### 4.5 Evolución v1.4 → v1.6
- **v1.4** — GUI/CLI extraídas a `autorem.py` (dispatcher con registro de tareas).
  `rem_a05_egresos.py` quedó headless.
- **v1.5** — capa compartida `rem_saludmental.py` + módulo `rem_a05_ingresos.py`
  (gemelo, token ESTADO `INGRESO`). Motor `marcar_eventos()` parametrizado. El
  dispatcher carga el workbook una vez y cada tarea agrega su hoja → un solo
  `…_procesado.xlsx` multi-hoja.
- **v1.6** — **perfiles de formato IRIS/Administrativo** (§5). El usuario elige el
  formato al inicio; disclaimer visible para admin. `edad_anios()` parsea la
  edad del admin (`'99 años 12 meses 31 días'` → 99; menor de 1 año → 0).
  Fix Windows: `stdout` a UTF-8 en el CLI (los símbolos `▶·→«»✔` reventaban en
  cp1252, y `UnicodeEncodeError` ⊂ `ValueError` disfrazaba el error).

Cada paso verificado contra la salida IRIS de v1.2 (equivalencia) + tests de
ingresos, admin (sintético y archivo real anonimizado) y validación cruzada.

---

## 5. Perfiles de formato: IRIS vs Administrativo (v1.6)

El mismo formulario 'Control de Salud Mental' se descarga en **dos formatos**.
Desde v1.6 **ambos se procesan** (antes el admin se rechazaba). El usuario elige
el formato al inicio; cada uno es un **perfil** en `rem_saludmental.PERFILES`.

**`detectar_formato(ws)`** devuelve `iris | administrativo | desconocido`:
- **IRIS:** ancla `AÑO APLICACIÓN FORMULARIO` **y** columna `NÚMERO ... IDENTIFICACIÓN`.
- **Administrativo:** banner `Servicio de Salud` en A1, y/o `ADMIN_MARKERS`
  (`Numero de Fichas` / `Edad de registro formulario` / `Fecha Formulario`).

`validar_iris()` / `validar_admin()` aceptan su formato y, si detectan el otro,
levantan `ArchivoInvalido` con **mensaje cruzado** ("elegiste IRIS pero esto
parece Administrativo — cambia el selector"). `categoria ∈ {iris, administrativo,
desconocido}`. `abrir_validado(entrada, perfil)` valida antes de tocar nada.

**Diferencias que maneja el perfil admin** (comparado con IRIS):
| | IRIS | Administrativo |
|---|---|---|
| Encabezado | ancla IRIS | **fila 9** (ancla `EDAD/REGISTRO/FORMULARIO`; `usar_blanco_en_a=False` para no caer en fila 7) |
| RUT | `NÚMERO TIPO IDENTIFICACIÓN` | columna `RUT` |
| Edad | `AÑO APLICACIÓN FORMULARIO` (nº) | `Edad de registro formulario` = `'99 años 12 meses 31 días'` → `edad_anios()` saca los años |
| Numeración preguntas / subtipos | idéntica | **idéntica** (el motor de diagnóstico sirve igual) |
| `Pueblos_Originarios`, `SENAME`, `Proteccion_Ninez`, `Migrante`, `Trans` | columnas presentes | **NO existen** → salen VACÍAS (disclaimer lo advierte) |

`_preparar()` acepta los nombres de RUT/edad de **ambos** formatos (robusto ante
mala elección). La detección de columnas demográficas ausentes se loguea
(`[demo] columnas AUSENTES...`). **Disclaimer admin** en `_DISCLAIMER_ADMIN`,
visible en la GUI al elegir el formato y logueado al procesar.

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
  `"Depresión Moderada"` con header `TIPO DE DEPRESIÓN` → `"Moderada"`. Casos que
  no se resuelven así van en `OVERRIDE_SUBTIPO` (mapa por Nº de subtipo): hoy
  Ansiedad (43) → Fobia social / **Pánico** (junta los dos) / Generalizada / TEPT
  / Otros. Verificado contra export real (jun-2026); los demás salen limpios solos.
- **Remap deprecated:** Abuso Sexual (pregunta 9) → patología `Violencia`,
  subtipo `Sexual` (`REMAP_DIAGNOSTICO`).
- **Nombre de patología canónico** (`LIMPIAR_NOMBRE_PATOLOGIA = True`, jul-2026):
  `OVERRIDE_PATOLOGIA` mapea cada Nº de pregunta → nombre limpio (tomados de
  SP·P6 y revisados con el autor). Abuso Sexual (9) lo maneja `REMAP_DIAGNOSTICO`.
- **`EXCLUIR_PATOLOGIA = {75,77,79,81}`:** epilepsia (va al REM adulto) y los
  programas de rehabilitación/acompañamiento NO son diagnósticos SM → se saltan
  del output de egresos/ingresos.
- **Quirk RAYEN clave:** `AÑO APLICACIÓN FORMULARIO` **NO trae el año, trae la
  EDAD a la fecha de llenado** (lo que A05 necesita). `EDAD PACIENTE` es la edad
  a la fecha de descarga → se ignora.
- **RUT** viene de `NUMERO TIPO IDENTIFICACION`, ya con guión y DV (`11111111-1`).
- **Otras Causas es manual por diseño:** requiere decisión clínica caso a caso
  (abandono vs clínica). Solo se flaggea; no se clasifica automático.
- **Detectar por CONTENIDO, nunca por nombre de archivo, + confirmar:** RAYEN baja
  TODO como `Formulario_Rayen.xlsx` sin importar el contenido. El nombre no dice
  nada. Regla del proyecto: identificar formato/instrumento por firmas de
  contenido (ancla, banner, columnas, fingerprint de ítems) y **confirmar con el
  usuario** ("Detecté X — ¿correcto? S/N") antes de procesar. Extiende
  `detectar_formato()`; a futuro puede reemplazar el selector manual del A05 por
  auto-detección + confirmación.

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

### Versionado — `X.Y.Z` (¡respetar!)
Nada de versiones monótonas (que terminan en "v200" y se ven horribles). Esquema:
- **X** = por cada **PROGRAMA** que se agregue. Hoy = **1** (autoREM).
- **Y** = por cada **MÓDULO de programa** acumulado. Hoy = **3** (egresos, ingresos, screening A03 D.3).
- **Z** = por cada **corrección del módulo que se está trabajando**. Reinicia a 0
  al sumar un módulo nuevo (Y++).

Se escribe con puntos (`1.2.0`, `1.2.1`, …, `1.2.10`) para que Z pase de 9 sin
romperse. **Es una versión ÚNICA de proyecto:** fuente de verdad en
`rem_utils.VERSION`; todos los `.py` la repiten en su header y se bumpean juntos.
La GUI la muestra en el título. Estado actual: **1.3.2**.
(Las etiquetas v1.2–v1.6 de §4 son el changelog previo a esta convención; el
estado actual equivale a esas iteraciones acumuladas = 1.2.0.)

- **Header en cada archivo** (código y docs): bloque con
  *"This code/document was generated with the assistance of [modelo]. The human
  author reviewed, modified, and integrated the code."* + autor
  (Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa) + `SPDX-License-Identifier:
  GPL-3.0-or-later` + versión (`X.Y.Z`, sincronizada con `rem_utils.VERSION`).
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
- Los módulos de tarea ya tienen nombre limpio y con convención
  (`rem_a05_o_egresos.py` / `rem_a05_n_ingresos.py`, sin versión ni espacios).

### Higiene pendiente (opcional)
- Mover los `.py` viejos (`1.1`, `1.2`, `v0.2`, `rem_marcar_egresos.py`) a
  `legacy/` — git ya guarda la historia; solo ordenan la carpeta.
- Tag `v1.3` cuando se estabilice.

---

## 11. Empaquetado a .exe (pendiente inmediato)

Meta: colega no técnico hace doble-clic, sin instalar Python.

```bash
# Correr DESDE la raíz del repo (donde está autorem.py + las carpetas
# programas/ y modulos/):
pyinstaller --onefile --windowed --name "autoREM" autorem.py
# -> dist/autoREM.exe
```

**Gotchas:**
- Entry point = `autorem.py` (raíz). Los paquetes `programas/` y `modulos/` deben
  estar junto a él; PyInstaller sigue los `import programas.x` / `from modulos
  import x` solo y los empaqueta. Si por algún motivo no los encuentra, agregar
  `--paths .` (la raíz al path de búsqueda).
- El `.exe` **debe construirse en Windows** (PyInstaller no cross-compila).
- **SmartScreen / antivirus institucional:** exe sin firmar dispara "editor
  desconocido" y a veces falsos positivos; en máquinas SSMC bloqueadas puede
  requerir whitelist de IT. Alternativa: `--onedir` (a veces molesta menos).
  Argumento para IT: **procesa todo local, no sube nada** (Ley 20.584/21.719).
- Junto al `.exe`, distribuir `LICENSE` (GPLv3, `gnu.org/licenses/gpl-3.0.txt`).
- `openpyxl` se empaqueta solo; `tkinter` viene con el Python de Windows.

---

## 12. Roadmap / arquitectura futura

**Hecho:**
- ✅ `rem_utils.py` compartido (v1.3).
- ✅ GUI/CLI en dispatcher común `autorem.py` con registro de tareas (v1.4).
- ✅ Capa compartida `rem_saludmental.py` + módulo **ingresos** (v1.5).
- ✅ **Perfiles IRIS/Administrativo** con selector + disclaimer (v1.6).

**Pendiente:**
- **Módulo screening A03 D.3** (`modulos/rem_a03_d3_instrumentos.py`): ✅ HECHO
  e **integrado a la GUI** (pestaña propia; el multi-reporte se resolvió con
  pestañas por módulo, no con un dispatcher que auto-detecta todo). Autodetecta
  formato+instrumento, da resultado automático + DISAM + discrepancia (compara
  BANDAS canónicas, no texto: RAYEN redacta distinto por instrumento) + momento
  + estamento (IRIS directo, o Admin vía `estamentos.py`). Tests
  `tests/test_screening.py` (8/8) + `tests/test_estamentos.py` (3/3) + validado
  sobre 4 exports reales. Contexto en `docs/CONTEXTO_REM_A03_D3_INSTRUMENTOS.md`.
  **Pendiente v2:** conteos agregados por rango etario (extraer de `SA_26`) y CLI
  para screening (hoy solo GUI). Falta validar la GUI a ojo (doble-clic).
- **Empaquetar a `.exe`** (`autorem.py`, §11) — pendiente inmediato.
- **Otras Causas (post-GUI):** popup con lista de RUTs + dropdown para clasificar
  (abandono vs clínica) y sumar al reporte final.
- **Dos inputs nuevos (mediano plazo):** reporte de **PowerBI** y reporte de
  **atenciones/diagnósticos/actividades**. Cada uno entra como un módulo/tarea
  nuevo; si tienen otro formato de archivo, como perfil nuevo. Atenciones es
  menos prioritario (lo manual desde ese reporte es simple).
- **Abandonos:** dependen del cálculo del "PowerBI madre" — etapa aparte.
- **Cosmético:** `LIMPIAR_NOMBRE_PATOLOGIA = True` + precargar `OVERRIDE_PATOLOGIA`
  para nombres bonitos.
- ~~Higiene: mover los `.py` viejos a `legacy/`~~ ✅ hecho; reorg en paquetes
  `programas/` + `modulos/` ✅; tag `1.2.0` ✅.

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
