<!--
Documento de contexto para el módulo de screening/instrumentos (rem_a03_d3_instrumentos).
Sin PII. Autor: Simón Tobar. SPDX-License-Identifier: GPL-3.0-or-later
-->

# CONTEXTO: Automatización REM A03 Sección D.3 — PSC / PSC-Y / GHQ-12

## ✅ RESUELTO (jul-2026): los "dos resultados"

RAYEN **precalcula** por cada aplicación tanto el **PUNTAJE** como un **RESULTADO**
(su clasificación automática), y ambos vienen como columnas en el export. Entonces:

- **Resultado AUTOMÁTICO** = leer la columna `RESULTADO` de RAYEN tal cual.
- **Resultado CALCULADO (DISAM)** = tomar el `PUNTAJE` y reclasificar con los cortes
  de este doc (`clasificar_*`, más abajo) — que es lo que pasó DISAM.
- El reporte muestra **las dos** para poder comparar (RAYEN a veces difiere).

Estructura de columnas del export **confirmada** contra ejemplos reales
anonimizados en `refs tablas/` (goldberg/pscy/psc): ver «Estructura real» abajo.

## Setup general
- **Centro:** CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC, Maipú)
- **Serie REM:** SA_26_V1_2.xlsm → REM A03 → Sección D.3
- **Stack:** Python + openpyxl. Sin dependencias externas. Offline obligatorio (Ley 20.584 / Ley 21.719).
- **Hardware:** i5, 16 GB RAM

---

## Qué hace esta sección del REM

REM A03 Sección D.3 registra el **resultado de aplicación de instrumentos de monitoreo de resultados** del Programa de Salud Mental (PSM), aplicados al **ingreso y al egreso** del programa.

> ⚠️ Solo se registra en personas **ingresadas al PSM**. No aplica a tamizajes ni a personas sin ingreso formal.

Desagregación requerida: **rango etario × sexo × resultado (Bajo / Medio / Alto) × momento (Ingreso / Egreso)**

---

## Los tres instrumentos

### PSC — Cuestionario Pediátrico de Síntomas
| Campo | Valor |
|---|---|
| Población | Niños/as 5–9 años ingresados al PSM |
| Informante | Padres / cuidadores |
| Ítems | 35 (Nunca=0 / A veces=1 / A menudo=2) |
| Rango total | 0–70 pts |
| Nombre en RAYEN | `Cuestionario para Padres PSC` |
| Momento aplicación | Ingreso y egreso del PSM |
| Registro REM | A03, Sección D.3 |

**Puntos de corte REM (fuente: Manual REM SA 2026):**
- BAJO: 33–63 pts
- MEDIO (Riesgo): 64–69 pts
- ALTO (Riesgo crítico): ≥70 pts

---

### PSC-Y — Cuestionario para Adolescentes
| Campo | Valor |
|---|---|
| Población | Adolescentes 10–14 años ingresados al PSM |
| Informante | El/la adolescente (autorreporte) |
| Ítems | 35 (mismos que PSC, misma escala) |
| Rango total | 0–70 pts |
| Nombre en RAYEN | `Cuestionario para Adolescentes (PSC-Y) 10 a 14 años` |
| Momento aplicación | Ingreso y egreso del PSM |
| Registro REM | A03, Sección D.3 |

**Puntos de corte REM (idénticos al PSC):**
- BAJO: 33–63 pts
- MEDIO (Riesgo): 64–69 pts
- ALTO (Riesgo crítico): ≥70 pts

---

### GHQ-12 — Cuestionario de Salud de Goldberg
| Campo | Valor |
|---|---|
| Población | 15+ años ingresados al PSM |
| Informante | El/la usuario/a (autoaplicado) |
| Ítems | 12 |
| Escala | Bimodal 0-0-1-1 (resp. 1-2 → 0 pts; resp. 3-4 → 1 pt) |
| Rango total | 0–12 pts |
| Nombre en RAYEN | `Cuestionario de Salud de Goldberg` |
| Momento aplicación | Ingreso y egreso del PSM |
| Registro REM | A03, Sección D.3 |

**Puntos de corte REM:**
- BAJO: 0–4 pts
- MEDIO: 5–6 pts
- ALTO: 7–12 pts

---

## Qué NO es esto (confusión frecuente)

| | Monitoreo (D.3) | Tamizaje (Sección H) |
|---|---|---|
| Instrumentos | PSC, PSC-Y, GHQ-12 | PSC-17, PSC-Y-17, PHQ-9, CAPE-P15, C-SSRS, GDS-15 |
| Momento | Ingreso y egreso PSM | Cualquier atención APS |
| Población | Solo ingresados al PSM | Cualquier usuario |
| Propósito | Evaluar evolución | Pesquisa / detección de riesgo |

> PSC-17 y PSC-Y-17 son para tamizaje escolar (HpV). No se mezclan con PSC/PSC-Y de D.3.

---

## Estructura real del export (confirmado jul-2026)

Se exporta **un archivo por instrumento**. Los DOS formatos del proyecto aplican
también acá (reutilizar el sistema de perfiles de `rem_saludmental`):

**Perfil IRIS** (`goldberg iris.xlsx`, `pscy 10 14 iris.xlsx`): encabezado arriba,
1 fila por aplicación. Columnas clave (nombre exacto):
- ⚠ `INSTRUMENTO` (columna **AH**, entre `FUNCIONARIO` y `ESTABLECIMIENTO INSCRIPCION`) —
  **RAYEN la mal-rotula**: en realidad trae el **ESTAMENTO** de quién aplicó
  (`Médico` / `Psicólogo(a)` / `Terapeuta Ocupacional` / `Trabajador(a) Social`),
  NO el instrumento. (Solo IRIS trae el estamento; el Administrativo NO.)
- El **instrumento** (PSC / PSC-Y / Goldberg) NO viene en esa columna → sale del
  `FORMULARIO` (col ~36) o de que cada archivo es un instrumento. CONFIRMAR cuál.
- `NUMERO TIPO IDENTIFICACION` (RUT), `SEXO`, `GENERO`, `FUNCIONARIO` (nombre).
- `AÑO APLICACIÓN FORMULARIO` = **edad al llenado** (usar esta; `EDAD PACIENTE` = edad a la descarga, ignorar).
- `FECHA ATENCION`, `FECHA FORMULARIO`.
- `1.- ESTADO` — candidato a **Momento** (Ingreso/Egreso); confirmar valores con dato real.
- `N.- PUNTAJE` (ej. goldberg `14.- PUNTAJE`) — el puntaje que suma RAYEN.
- `N.- RESULTADO` (ej. goldberg `15.- RESULTADO`) — clasificación AUTOMÁTICA de RAYEN.

**Perfil Administrativo** (`psc administrativo.xlsx`): banner filas 1-7, blanco 8,
encabezado **fila 9**. El **instrumento va en el banner** (fila 7, col 3:
`Formulario: Cuestionario para padres PSC`), NO en columna. RUT en columna `RUT`,
edad en `Edad de registro formulario` (texto → `edad_anios`). Puntaje/Resultado al
final: `40.- Puntaje`, `41.- Resultado`.

> Detección: `PUNTAJE` por token `PUNTAJE`; automático por token `RESULTADO`;
> instrumento por columna `INSTRUMENTO` (IRIS) o por el banner (admin).

> ⚠️ **Quirk RAYEN**: `AÑO APLICACIÓN FORMULARIO` = edad al llenado (usar).
> `EDAD PACIENTE` = edad a la descarga → ignorar.

---

## Output requerido (para llenar A03 D.3)

Tabla de conteos: una celda por combinación de:
- **Instrumento** (PSC / PSC-Y / GHQ-12)
- **Momento** (Ingreso / Egreso)
- **Resultado** (Bajo / Medio / Alto)
- **Rango etario** (según desagregación de la planilla SA — confirmar en SA_26_V1_2.xlsm)
- **Sexo** (Hombre / Mujer / Total)

---

## Reglas de clasificación (Python)

```python
def clasificar_psc(puntaje):
    if 33 <= puntaje <= 63: return "Bajo"
    elif 64 <= puntaje <= 69: return "Medio"
    elif puntaje >= 70: return "Alto"
    else: return None  # puntaje < 33: no registrar en REM (no es categoría válida)

def clasificar_psc_y(puntaje):
    return clasificar_psc(puntaje)  # cortes idénticos

def clasificar_ghq12(puntaje):
    if 0 <= puntaje <= 4: return "Bajo"
    elif 5 <= puntaje <= 6: return "Medio"
    elif 7 <= puntaje <= 12: return "Alto"
    else: return None
```

---

## Pendientes antes de codificar

- [x] ~~"cálculo DISAM" vs "real"~~ → RESUELTO: automático = col `RESULTADO`; calculado = `clasificar_*(PUNTAJE)`. Ver arriba.
- [x] ~~Nombres exactos de columnas~~ → confirmados contra ejemplos en `refs tablas/` (ver «Estructura real»).
- [x] ~~¿Puntaje precalculado?~~ → SÍ, RAYEN lo trae en columna `PUNTAJE`.
- [x] ~~¿Instrumento distinguible?~~ → SÍ: columna `INSTRUMENTO` (IRIS) o banner (admin). Se exporta 1 archivo por instrumento.
- [x] ~~Momento (Ingreso/Egreso)~~ → RESUELTO: la columna `1.- ESTADO` es binaria "Ingreso"/"Egreso".
- [ ] **Rangos etarios** exactos de D.3 en la planilla SA_26 (está en `refs tablas/SA_26_V1.2.xlsm` → se puede extraer).
- [ ] Definir forma de salida: ¿1 fila por aplicación (con ambos resultados, estilo A05) + hoja de conteos agregados para pegar en SA?

---

## Idea: reportar ESTAMENTO del funcionario que aplicó (pendiente de diseño)

Además de instrumento/momento/resultado, reportar el **estamento**
(Médico / Psicólogo / Terapeuta Ocupacional / Trabajador Social / Otro) que llenó
el instrumento.

- **IRIS:** el estamento viene **directo** en la columna AH `INSTRUMENTO` (mal
  rotulada; valores `Médico`/`Psicólogo(a)`/`Terapeuta Ocupacional`/`Trabajador(a) Social`).
  No necesita lookup.
- **Administrativo:** NO trae estamento, solo el nombre del `Funcionario` → necesita
  mapeo `funcionario → estamento`.

Diseño propuesto:
- **Tabla auxiliar `funcionario → estamento`, LOCAL (gitignored):** son nombres de
  personal (dato personal de funcionarios, no PII de pacientes, pero igual no se
  versiona) y es un artefacto que cambia con las rotaciones.
- **Auto-sembrado** desde los exports IRIS (donde el estamento sí está); el
  funcionario aparece en muchos reportes → la tabla se llena sola con el uso.
- **Funcionarios desconocidos → popup interactivo** al procesar: lista los no
  clasificados con dropdown (Médico/Psicólogo/TO/TS/Otro). MISMO patrón que el
  popup "Otras Causas" del roadmap → hacer UNO reutilizable.
- **Ubicación:** la LÓGICA (cargar/guardar/lookup del mapeo) es reutilizable; el
  POPUP es GUI (Tkinter) → va en la capa dispatcher (`autorem` o un helper GUI),
  NO en `rem_utils` (que es headless). El core del módulo puede salir SIN esto (v2).
- Probablemente **cross-módulo** (egresos/ingresos también podrían querer "quién
  llenó"), así que conviene un helper compartido.

---

## Archivos de referencia
- `SA_26_V1_2.xlsm` — planilla SA (ver estructura celdas D.3). **No en el repo** (queda en la carpeta de trabajo).
- `Manual_Series_REM_2026_SERIE_A.pdf` — pp. 71-72 (definición D.3 y cortes).
- `refs tablas/PSC_PSC-Y_GHQ12_comparativo_final.xlsx` — tabla comparativa de los instrumentos (en el repo, sin PII).
- `legacy/rem_marcar_egresos*.py` — referencia de patrón de parsing RAYEN (quirks documentados).
