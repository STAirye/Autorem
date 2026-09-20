<!--
This document was generated with the assistance of Claude Fable 5 and Claude Opus 5 (Anthropic).
The human author reviewed, modified, and integrated the content.
Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# programas/ — capas compartidas

Se carga al trabajar en `programas/`. Los `§N` son las anclas del [CLAUDE.md raíz](../CLAUDE.md).

## Capas

| Archivo | Rol |
|---|---|
| `rem_utils.py` | **Base genérica.** `norm`, `buscar_col`, `encontrar_fila_encabezado` (mundo openpyxl: solo por ancla; sin ancla, `ArchivoInvalido('sin_encabezado')` — desde la ronda 11 no hay fila de repuesto por posición, y devuelve la fila pelada: el `modo` era constante y se fue en la 12), `ArchivoInvalido`, `VERSION`, `grid`, `rut_valido`/`dv_rut`, lectura pandas (`filas_xlsx`/`leer_xlsx`, robustos a la «dimension» rota **desde 1.9.17** — antes la respetaba y truncaba callado; **toda lectura `read_only` pasa por `abrir_xlsx_ro`**, nunca un `load_workbook(read_only=True)` pelado, que acota `iter_rows` a la `<dimension>` del archivo; `resolver_columnas`; `contiene_todos`/`contiene_alguno`), los mapas de columnas COMPARTIDOS (`MAPA_ATENCIONES`, `MAPA_INSCRITOS`, `MAPA_MAESTRO`, `MAPA_MULTIPROF`), `marcar_demografia`, `cargar_maestro`/`maestro_rem_map`, **`filtrar_mes`** (§3.1) y **`rutas_libres`** + **`escribir_atomico`** (toda salida pasa por los dos: nunca se sobreescribe, sale `… (1).xlsx`, y se escribe a un temporal que se renombra al terminar). |
| `formatos.py` | **Eje IRIS vs Administrativo.** Mecanismo compartido + firmas POR REPORTE (no un `detectar_formato` único): `detectar_eje`, `resolver_identidad`, `ANCLA[eje]` (lo único que cambia al ubicar el encabezado; el `fila_encabezado_admin` que solo reenviaba se fue en la ronda 12). **Fase 2 — clasificar la FUENTE:** `clasificar_fuente` / `aviso_fuente`, enganchados en `cargar_canonico` (cuello de botella del grupo pandas). Tres estados: `plena` · `parcial` (no es el A/D/A; le habla al usuario) · `cambiada` (es el A/D/A pero RAYEN movió columnas; le habla al dev). La firma es negativa: claves que solo trae IRIS (`SOLO_IRIS_ATENCIONES`). También `verificar_cruce`: error específico si se cargan cruzados el ADA y el grupal. |
| `rem_saludmental.py` | **Formulario «Control de Salud Mental».** Config clínica (§7), `PERFILES` IRIS/Admin sobre `formatos.py`, motor `marcar_eventos()`. |
| `estamentos.py` | **Funcionario → Estamento** para el formato Admin (que no trae estamento), desde el reporte «Utilización de Cupos». Caché persistente `~/.autorem/estamentos.json` + merge con el reporte fresco (gana el fresco) + failsafe: resolver a mano o ignorar. |
| `dotacion.py` | **Funcionarios EXTERNOS** (hoy la sala AIDIA). Gemelo de `estamentos`. Tri-estado `interno`/`externo`/`desconocido`: un desconocido **cuenta** al REM, pero se reporta siempre. `~/.autorem/dotacion.json` con `funcionarios` (clasificación global) y `omitidos` (por módulo). Plan: [docs/dotacion_externos_plan.md](../docs/dotacion_externos_plan.md). |
| `poblacion.py` | **Tabla «Ferrada» por RUN** (port del DAX). Un motor único `_estado_dx` para los 28 dx/factores, `¿Ingresado?`, `¿Activo 12m?`, rescate, `¿Pertenece?` en sus dos versiones. `exigir_medico=False` solo para `Brecha_Medico`. |
| `cobertura.py` | **Hoja LEEME** (primera hoja de cada salida): qué casillas NO cubre el módulo y por qué (`MANUAL` / `FUERA DE ALCANCE` / `OMITIDO` / `PENDIENTE` / `EN VALIDACION` / `SIN REGISTRO`) + los `avisos` de esa corrida (`.attrs['avisos']`). `tests/test_cobertura.py` falla si un módulo nuevo no tiene su entrada. |
| `catalogos.py` | **Catálogos DEIS** (§14). |

## §3.1 Mes vacío = fail loud, con la guarda sobre la FUENTE

`rem_utils.filtrar_mes(d, ini, fin, fuente)` es el único filtro de mes de los módulos
pandas.

- **0 filas de la fuente en el mes** → `ArchivoInvalido("mes_vacio")`, con el rango real
  del archivo en el mensaje.
- **Mes cubierto pero una casilla en 0** → legítimo (A27), no falla. Aun así, un 0
  merece verificar el string una vez (A32·F2).

Por eso los filtros posteriores al mes (`Asiste=SI`, Control/Ingreso IRA/ERA) se
aplican **después**, sobre lo que devuelve `filtrar_mes`.

Antes del mes, `cargar_canonico` corta **POR ARCHIVO** y nombrándolo (los reportes
acumulativos se cargan de a varios años): 0 filas de datos (`exigir_filas`), columnas
requeridas ausentes (`sin_columnas`, que es también cómo ubica el encabezado) y **columna
clave presente pero vacía en todas las filas** (`no_vacias`, ronda 12: da el mismo 0
callado que la ausente, y escrita a mano sobre el DataFrame concatenado dejaba pasar el
archivo malo escondido detrás de uno bueno).

- **Enganchado en:** ADA del SM, grupal, atenciones del A23, NSP y el ADA del Trabajo
  Perdido. Las opcionales **también fallan**: cargarlas fue decisión del usuario. Desde la
  ronda 11 fallan como `rem_utils.OpcionalInvalido` (con `with opcional("<param>")`), y la
  GUI pregunta «¿continuar sin él?» (`runner.sin_opcional`): si sí, re-corre sin ese
  archivo y la LEEME lo dice (`OMITIDO`). Nunca seguir callado sin él.
  Dos reglas de la ronda 12, porque la GUI RE-CORRE: los opcionales se cargan
  **PRIMERO** en `procesar` (la pregunta tiene que llegar antes del trabajo pesado, no
  después del minuto de corrida) y `opcional()` convierte **solo ArchivoInvalido** —
  atrapar `ValueError` disfrazaba un bug de código de «tu archivo no sirve», y por eso
  todo loader de un opcional pasa por `cargar_canonico`, que además envuelve el archivo
  ilegible (el .xls/.html disfrazado tumbaba la corrida en vez de preguntar).
- **No se engancha a propósito en:** `om` del A23 (histórico multi-año) y en la
  **familia población**, donde el mes es un CORTE sobre un snapshot y no un filtro.
  Ahí `_verificar_cobertura_fechas` avisa sin bloquear, y los avisos van a la LEEME y
  al resumen de la página. **Sí bloquea** si una fuente queda VACÍA para el corte (todas
  sus filas posteriores al mes, o ninguna fecha legible): eso no es un histórico
  incompleto, es un P6 entero en 0. Por lo mismo bloquea si la **base** del P6 (Estado=Activo × Activo 12m × Ingresado) queda vacía: cada fuente tiene datos pero el cruce no (ESTADO con otro vocabulario, RUN en otro formato).

## §5 Formatos: IRIS vs Administrativo

Casi todos los reportes RAYEN se descargan en **dos formatos**, y ambos se procesan.
El formato se **detecta por contenido** y lo confirma el usuario (§2 raíz).

- **IRIS:** ancla `AÑO APLICACIÓN FORMULARIO` + columna `NÚMERO … IDENTIFICACIÓN`.
- **Administrativo:** banner `Servicio de Salud` en A1 y/o `ADMIN_MARKERS`; encabezado
  en fila 9. El IRIS de formularios también trae banner (15 filas, encabezado en la 17):
  el encabezado se ubica **solo por el ancla** en los dos formatos (`formatos.ANCLA`).
  En el grupo **pandas** el ancla es otra: `cargar_canonico` toma como encabezado la 1ª
  fila que resuelve TODAS las columnas `requeridas` del loader (`encabezado_por_columnas`).
  Hasta la ronda 12 era «la 1ª fila con más de 3 celdas llenas» — un conteo, y los banners
  de RAYEN ya traen filas de 3.
- **Por contenido:** `rem_saludmental.verificar_formulario_sm` contrasta cada número de
  pregunta que se usa con lo que su encabezado dice (`FIRMA_FORMULARIO_SM`). Un
  cuestionario (Goldberg, PSC) u otro formulario RAYEN trae las mismas firmas de eje y
  pasaba entero hasta la ronda 11: ahora es `no_formulario_sm`; un formulario SM
  renumerado, `formulario_cambiado`. Lo usan el A05 y el histórico del P6.

Si detecta el otro formato, `validar_iris` / `validar_admin` levantan `ArchivoInvalido`
con mensaje cruzado.

Formulario SM en Admin: el RUT viene en la columna `RUT`, la edad como `'99 años 12
meses 31 días'` (`edad_anios()`), la numeración de preguntas es idéntica, y **no hay
columnas demográficas** → salen vacías (con disclaimer).

## §5.1 El «Monitoreo de Actividades» NO es el gemelo admin del A/D/A

Es el reporte que el lado Admin ofrece **en lugar** del A/D/A: 26 columnas contra 45.

| Clave | En el Monitoreo | Consecuencia |
|---|---|---|
| `RUN` `FECHA` `ACT` `DIAG` `INSTR` `TIPO` `SEXO` `SECTOR` | sí | carga sin chistar |
| `DIAG` (contenido) | texto **sin código ICD** | Ira Alta · Bronquitis · EPOC exac. = 0 en A23 |
| `ATENID` | equivalente `N°` | correlativo que **reinicia por export** → namespaceado con el nombre del archivo |
| `ANOS_AT` | equivalente `AÑOS` | ⚠ en IRIS `AÑOS` es la edad a la descarga (la buena es `AÑOS ATENCIÓN`); en el Monitoreo ya es a la atención. Un test fija el orden |
| `PROF` | equivalente `FUNCIONARIO` | — |
| `ALERTAS` `PUEBLO` `NACION` `FNAC` `FORMCLIN` | **sin equivalente** | sin demografía |
| forma de la atención | **varias filas** (una actividad cada una, el `N°` repetido, RUN solo en la 1ª); IRIS: **una fila** con todas en `ACTIVIDADES` | **se normaliza en la FUENTE** (`rem_utils._una_fila_por_atencion`): `cargar_atenciones` entrega UNA fila por atención en los dos formatos, con las actividades juntas, así que todo consumidor cuenta igual. Hasta la ronda 11: ffill global y AND fila por fila → 6 indicadores A23 en NO callados; hasta la 12 estaba a medias (ffill acá + `a23._act_de_la_atencion` en UN consumidor) y el Trabajo Perdido marcaba «saco roto» una actividad cuya hermana sí tributaba. Un ATEN ID con dos pacientes = `modificado` |

**Veredicto:** A23 usable, salvo los 3 indicadores por ICD. SM: los conteos sirven, las
columnas demográficas no. Si una clave gana equivalente admin, **hay que sacarla de
`SOLO_IRIS_ATENCIONES`**, o el Monitoreo pasa a clasificar `cambiada`.

## §14 Catálogos oficiales DEIS/MINSAL

Backend compartido: el diccionario de la herramienta, sin casilla REM propia. Armado
**desde cero** con las fuentes oficiales públicas del
[Centro FIC del DEIS](https://deis.minsal.cl/centrofic/#documentacion).

| id | Catálogo | Edición | Contenido |
|---|---|---|---|
| `cie10` | Lista Tabular CIE-10 | ago-2026 | 12.548 códigos (cruz/daga · asterisco · causa externa) |
| `eno` | Notificación Obligatoria (Decreto 7/2019) | ago-2026 | 56 enfermedades → 448 pares |
| `ges` | GES 90 problemas ↔ CIE-10 | v1_4 | 5.936 pares |

API: `norm_codigo` / `con_punto` · `descripcion` · `existe` · `en_rango` · `expandir` ·
`eno_de` · `ges_de` · **`anotar`** (batch).

**Decisiones (NO deshacer sin motivo):**
- **Registro declarativo** `CATALOGOS`: un catálogo nuevo = una entrada + un `_leer_*`.
- **Código canónico SIN punto** (`J209`, como el DEIS; RAYEN usa `J20.9`).
- **Los rangos no se expanden:** `en_rango` compara lexicográficamente, lo que funciona
  por los ceros a la izquierda. Convertir a int lo rompe.
- **`ENO_TIPO` viene del texto del decreto**, no del orden de las filas del Excel.
- Las transitorias (Mpox, *S. pyogenes*) llevan `ART = alerta vigente`, porque caducan.
- **Los huecos se declaran:** `ENO_SIN_CLASIFICAR` (Viruela, Tifus de los matorrales)
  avisa ruidoso, y un test compara la lista.
- **Cascada de carga:** `.xlsx` explícito > drop-in en `catalogos/` (avisa que pisa el
  embebido) > slim vendorizado.
- **Descartado:** la homologación CIE-9 ↔ CIE-10, porque RAYEN usa solo CIE-10.

Mantención (`tools/catalogos_deis.py`) y escáner de PII: ver [tools/CLAUDE.md](../tools/CLAUDE.md).
