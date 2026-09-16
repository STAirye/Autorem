<!--
This document was generated with the assistance of Claude Opus 5 (Anthropic).
The human author reviewed, modified, and integrated the content.

Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
Copyright (C) 2026 Simon Tobar
SPDX-License-Identifier: GPL-3.0-or-later
Version: 1.9.16
-->

# Plan — Auditoría de actividades habilitadas por funcionario

> **Estado: PLAN** (sep-2026, sin implementar). Utilidad **no-REM**: no llena
> casillas. Su destino final es un rincón de «Utilidades» en la GUI 2.0. Documento
> **autocontenido**: se puede implementar sin haber participado de la conversación
> que lo originó.

---

## 0. Problema

En RAYEN/IRIS, cada funcionario tiene activadas las actividades que puede registrar.
Si le falta una, la atención **no se puede registrar como corresponde**, y el REM
pierde casillas en silencio: el funcionario registra otra cosa o no registra nada.

El objetivo es un listado por funcionario de las **actividades mínimas obligatorias
que le faltan**, para mandárselo a la jefatura y que las activen:

| Funcionario | Estamento | Actividades faltantes |
|---|---|---|
| Juanito Pérez | Psicólogo(a) | Consultorías de Salud Mental (A06·A.2) |

### 0.1 Lo que NO es la norma (verificado sep-2026)

| Candidato | Por qué no sirve como norma |
|---|---|
| **Maestro de Actividades** (`maestro_slim.csv.gz`) | Es el **catálogo completo** de lo que RAYEN permite: 5.453 pares actividad×instrumento solo para `Psicólogo(a)`. No dice qué es mínimo. **Sí sirve** como puente de nombres (§2.2). |
| El manual de SM armado en una sesión de Cowork | Desactualizado: es solo de SM y no conoce la actividad de consultorías. **No usarlo.** |
| Heurística por pares («5 de 6 psicólogos la tienen») | Descartada por el autor: la norma dura existe (§1). |
| Columna `NOMBRE REM` del informe | Dice a qué REM cae una actividad, no si es obligatoria. Solo sirve para el crosscheck (§3.3). |

## 1. La norma dura: la plantilla SA del año

**Referencia autoritativa = las filas del `SA_<AA>` que MINSAL publica cada año**
(hoy `refs_tablas/SA_26_V1.2.xlsm`). Si la plantilla tiene una fila para
(actividad, profesional), esa actividad es **obligatoria** para ese estamento: sin
ella, la casilla no se puede llenar.

- **Fila con profesional explícito** → obligatoria para ese estamento.
- **Fila sin profesional** (p. ej. A06·A.2 Consultorías de Salud Mental) → obligatoria
  para **todos los profesionales autorizados**. En la práctica son los funcionarios
  **internos** según `programas/dotacion.py` (el checklist interno/externo), cuyo
  estamento el Maestro habilita para alguna de las actividades RAYEN de ese requisito.
  - `externo` → no se le exige.
  - `desconocido` → **se le exige**, igual que en el REM (el desconocido cuenta), y
    queda marcado en la salida para que se clasifique.
- Lo configurable por centro (actividades extra) queda **fuera de alcance** (§7).

### 1.1 Por qué el SA no se puede parsear a ciegas

Se revisó el `SA_26`: la dimensión «profesional» aparece de **al menos cuatro
formas distintas**.

| Forma | Ejemplo |
|---|---|
| `ACTIVIDAD` en col A + `PROFESIONAL` en col B | A06·A.1, B.1, H, K |
| El profesional **es** la etiqueta de fila, en col A | A04·B (`Psicólogo/a`, `Terapeuta Ocupacional`) |
| Profesional **con calificador** dentro de la etiqueta | A04·B `Trabajador/a Social (Excluye Salud Mental)` |
| Profesionales **como columnas** | A04·J (rondas), A06·A.3 (participantes de consultoría) |

Además, la actividad del bloque aparece solo en la primera fila (celdas combinadas),
y hay filas sin profesional (A06·A.1 «Intervención Psicosocial Grupal»).

Los **nombres no calzan** con RAYEN:
- estamentos: SA `Psicólogo/a` vs RAYEN `Psicólogo(a)`;
- actividades: SA «Consultorías de Salud Mental» vs RAYEN «Casos revisados
  consultoria salud mental (Individual)».

**Conclusión:** un parser genera un **borrador**, y un humano lo valida (§2). Nunca se
hace matching difuso en runtime: un match malo produce un «faltante» falso o esconde
uno real, que es exactamente el número plausible pero mal (regla dura 2).

---

## 2. El crosswalk: SA → actividades RAYEN

### 2.1 Forma

Es una tabla de **requisitos**, una fila por (fila SA × estamento):

| Columna | Contenido |
|---|---|
| `REM` | `A06` |
| `SECCION` | `A.2` |
| `FILA_SA` | Etiqueta tal cual del SA: «Consultorías de Salud Mental» |
| `ESTAMENTO` | Estamento **RAYEN** (`Psicólogo(a)`) o `*` = todos los internos autorizados (§1) |
| `ACTIVIDADES_RAYEN` | Lista de actividades RAYEN que **satisfacen** el requisito (basta **una**) |
| `ESTADO` | `validado` / `borrador` |
| `NOTA` | Libre (por qué se mapeó así) |

- El requisito se **cumple** si el funcionario tiene activada **cualquiera** de sus
  `ACTIVIDADES_RAYEN` (con `norm()`). Así se cubren las variantes presencial/remota.
- Las filas en `borrador` **no se evalúan**. Van a la LEEME como `PENDIENTE`: fallar
  ruidoso, sin fingir cobertura.

### 2.2 Borrador (automático)

`tools/borrador_actividades_minimas.py`, o una función de la capa que la GUI también
llame:

1. Recorre las hojas del SA en alcance (§6) y detecta las formas de §1.1. Lo que no
   reconoce **lo lista como no reconocido**, no lo salta.
2. Normaliza los estamentos SA → RAYEN con una tabla de alias chica y explícita
   (`Psicólogo/a` → `Psicólogo(a)`, `Médico/a` → `Médico`, …). Un alias faltante es un
   aviso, no una omisión callada.
3. Propone candidatos RAYEN desde el Maestro, filtrando por `NUM REM` + `NUM SECCION`
   (`A.2,A.3` viene con coma: partir) + estamento, y ordena por similitud de nombre.
   **Solo propone.** Todas las filas salen en `ESTADO=borrador`.

### 2.3 Validación = paso intermedio en la GUI (decisión del autor)

La validación vive en la GUI: una pantalla que muestra requisito por requisito, con
los candidatos como checkboxes, y permite «validar», «editar» o «descartar fila».

- **Persistencia en capas**, con la misma cascada que los catálogos (§14):
  1. **embebido:** `catalogos/actividades_minimas_2026.csv`, validado por el autor.
     Como la norma es MINSAL y el nombre de actividad es RAYEN, sirve para cualquier
     centro;
  2. **override local:** `~/.autorem/actividades_minimas.json`, con lo que el usuario
     valide o edite en la GUI (gana el local, avisando que pisa al embebido).
- **Antes de la GUI 2.0:** el mismo CSV se edita a mano en Excel para debuggear SM.
  La pantalla de la 2.0 lee y escribe **ese mismo formato**, así que no hay migración.
- Cada año: plantillas nuevas → borrador nuevo → `actividades_minimas_2027.csv`. Cae en
  el bump de X de las plantillas (§9 raíz).

---

## 3. Entradas

### 3.1 `Informe Actividades Profesionales` (IRIS, obligatorio)

Existe **solo en IRIS**. Header de ejemplo:
`refs_tablas/Informe_Actividades_Profesionales heads.xlsx`.

> ⚠ **Privacidad:** ese archivo hoy trae **una fila de datos del autor** y está
> ignorado por el `.gitignore`. **Antes** de agregarlo a la whitelist, hay que
> recortarlo a solo header (skill `limpiar-refs`). Nada de datos del autor en el repo.

- Banner (título, disclaimer Ley 19.628/20.584, `Servicio de Salud`, `Comuna`,
  `Establecimientos`, `Instrumento`) + **encabezado en la fila 8**.
- Columnas: `N ACTIVIDAD · ID ESTABLECIMIENTO · ESTABLECIMIENTO · NOMBRES · PRIMER
  APELLIDO · SEGUNDO APELLIDO · RUT · ACTIVIDAD · INSTRUMENTO · PERFIL ASOCIADO · ES
  PRESTADOR · ESTADO FUNCIONARIO · NOMBRE REM`.
- **Una fila por funcionario × actividad × instrumento.**
- `INSTRUMENTO` = **estamento** (como en todo RAYEN). Un funcionario puede tener más de
  uno: se evalúa **por cada estamento** que tenga.
- `RUT` viene **todo junto** (`11111111`), sin puntos ni guion (y a veces vacío). No es
  la llave: la persona se identifica por nombre completo + RUT si viene. Con
  `rut_valido`/`dv_rut` se puede reconstruir el DV para mostrarlo.
- `NOMBRE REM` es texto largo (`REM-BM18. ACTIVIDADES DE APOYO…`): el código se parsea
  del prefijo, hasta el primer punto.
- **Filtros:** `ESTADO FUNCIONARIO == ACTIVO`. Además, un `ES PRESTADOR == NO` se deja
  fuera de la norma, pero **se cuenta en la LEEME**. ⚠ Confirmar con datos reales que
  no deja fuera a nadie clínico.
- **Detección por contenido** (regla dura 5): ancla `ESTADO FUNCIONARIO` + `NOMBRE REM`
  + `PERFIL ASOCIADO` + banner «Informe Actividades Profesionales». Otra cosa →
  `ArchivoInvalido`.

### 3.2 Opcionales / implícitas

- **Maestro slim** (ya embebido): lo usan el borrador (§2.2) y el crosscheck (§3.3).
- **Dotación** (`~/.autorem/dotacion.json`): para las filas `*`. ⚠ La tabla de
  dotación se indexa por `norm(FUNCIONARIO del ADA)`. **Verificar con datos reales**
  que `NOMBRES + PRIMER APELLIDO + SEGUNDO APELLIDO` normalizado produce la misma
  llave. Si no calza, **avisar ruidoso** (el funcionario queda `desconocido`) y no
  inventar un fuzzy match.

### 3.3 Crosscheck `NOMBRE REM`

Para cada actividad activada, se compara el `NOMBRE REM` del informe contra el
`NUM REM` del Maestro y contra el `REM` del crosswalk. Si difieren, la fila va a la
hoja de inconsistencias. **No corrige nada:** solo informa (puede ser un error de
parametrización de RAYEN, y eso también es algo que reportar a jefatura).

---

## 4. Salida (`<informe>_procesado.xlsx`, junto al input)

| Hoja | Contenido |
|---|---|
| `LEEME` | Primera hoja, vía `programas/cobertura.py`: fuente, año del SA, requisitos evaluados / en borrador (`PENDIENTE`), funcionarios excluidos (inactivos, no prestadores, externos), avisos (alias faltantes, nombres sin llave de dotación). |
| `Resumen` | **La hoja para jefatura:** `Funcionario · Estamento · Actividades faltantes`, con los faltantes unidos por salto de línea, cada uno como «Fila SA (REM·Sección)». Una fila por funcionario × estamento, **solo los que tienen faltantes**. |
| `A06`, `A04`, … | Lo mismo filtrado por REM. Una hoja por REM con al menos un faltante. |
| `Detalle` | Formato largo: `Funcionario · RUT · Estamento · Dotación · REM · Sección · Fila SA · Actividades RAYEN que la cumplirían`. Una fila por faltante, filtrable (regla de la tabla intermedia siempre disponible). |
| `Inconsistencias_REM` | §3.3 |

El RUT solo va en `Detalle` (el `Resumen` va a jefatura y no lo necesita). No hay
datos de pacientes en esta utilidad.

---

## 5. Código

- **Capa:** `programas/actividades_minimas.py`, con carga del crosswalk (en cascada),
  borrador, alias de estamentos y la evaluación pura
  `faltantes(informe_df, requisitos, tabla_dot) -> DataFrame largo`.
- **Módulo:** `modulos/aud_actividades_profesionales.py`, con lectura y detección del
  informe, filtros, hojas y LEEME. Es el prefijo `aud_` y no `rem_`, porque no es una
  casilla. Ajustar la regla de nombres de `modulos/CLAUDE.md` para admitirlo.
- **Tests** con fixtures sintéticos (nombres inventados, RUT `11111111-1`):
  - requisito cumplido por una sola de varias actividades;
  - estamento múltiple;
  - fila `*` con interno / externo / desconocido;
  - requisito en borrador → no evalúa y va a la LEEME;
  - inactivo excluido;
  - crosscheck `NOMBRE REM`;
  - archivo que no es el informe → `ArchivoInvalido`;
  - alias de estamento faltante → aviso.
- **Entrada en `cobertura.py`** (su test falla si falta).
- **Versión:** módulo nuevo → **Y** (1.10.0 o lo que toque según el CHANGELOG, que es
  el árbitro).
- **Sin CLI** (el CLI es solo del A05) y **sin pestaña en la GUI 1.x**. La pantalla
  vive en la GUI 2.0 bajo «Utilidades»:
  - se declara con `PANTALLA` (`docs/GUI_2.0_plan.md` §3);
  - la validación del crosswalk es un bloque `extras` o una sub-pantalla propia;
  - agregar a `docs/GUI_2.0_plan.md` §4 (sidebar) la sección `UTILIDADES`.
- El CSV embebido en `catalogos/` entra al `autoREM.spec` (§11: lo que shippea el exe
  se edita a mano en el spec).

---

## 6. Alcance del primer corte: Salud Mental

Hojas `A04 · A06 · A19a · A26 · A27 · A32`, solo las filas que corresponden a SM. El
autor se las sabe de memoria, así que sirven para debuggear el mecanismo antes de
generalizar.

- En el scan inicial, solo el **A06** usa la forma `ACTIVIDAD | PROFESIONAL` en cols
  A/B (secciones A.1, B.1, H, K). Las otras hojas usan las formas de §1.1:
  - A04·B → profesional como etiqueta;
  - A19a · A26 · A27 · A32 → actividad sin profesional (`*`) o profesional como
    columna.

  El borrador tiene que manejar esas formas **o listarlas como no reconocidas**.

**Orden sugerido:**
1. `limpiar-refs` sobre el informe + whitelist.
2. Capa + tests con un crosswalk SM **escrito a mano por el autor** (CSV).
3. Módulo + salida, corriendo contra el informe real del CESFAM (fuera del repo).
4. Borrador automático para SM, comparado contra el CSV a mano: si reproduce lo que el
   autor escribió, el borrador es confiable para el resto del SA.
5. Generalizar a todo el SA.
6. Pantalla GUI 2.0 (utilidad + validación).

---

## 7. Fuera de alcance (anotado)

- **Actividades extra por centro** (configurables): después, como otra capa
  `~/.autorem/` encima del mínimo MINSAL.
- **Cruce con uso real** (qué registró cada funcionario en el ADA): útil para detectar
  actividades activadas que nadie usa, pero no es este reporte.
- **Formato Administrativo:** el informe no existe en Admin.
