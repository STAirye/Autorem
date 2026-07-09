<!--
Documento de contexto importado desde el chat de Cowork (jul-2026) para el
futuro módulo de screening/instrumentos. Sin PII. Autor: Simón Tobar.
SPDX-License-Identifier: GPL-3.0-or-later

⚠ ABIERTO / A RESOLVER antes de codificar: el pedido original habla de DOS
resultados — "cálculo DISAM" y "cálculo real". Este doc trae UN set de cortes
(los oficiales del Manual REM SA 2026). Falta aclarar qué es el "cálculo DISAM"
(¿cortes locales distintos? ¿otra convención de puntaje?) vs el "real/oficial".
-->

# CONTEXTO: Automatización REM A03 Sección D.3 — PSC / PSC-Y / GHQ-12

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

## Input esperado desde RAYEN

Export de formularios clínicos. Columnas relevantes probables:

```
INSTRUMENTO          # nombre del formulario (ver nombres RAYEN arriba)
FECHA ATENCION       # o similar
SEXO                 # "Hombre" / "Mujer"
EDAD PACIENTE        # ojo: puede ser edad a la descarga, no al llenado
AÑO APLICACION FORMULARIO  # quirk conocido: en otros exports contiene EDAD al llenado, no año
PUNTAJE TOTAL        # o equivalente — confirmar nombre exacto en export real
RESULTADO            # puede venir calculado como "Bajo/Medio/Alto" o no existir
MOMENTO              # "Ingreso" / "Egreso" — puede no existir como columna separada
```

> ⚠️ **Quirk RAYEN documentado** (de `rem_marcar_egresos.py`): `AÑO APLICACIÓN FORMULARIO` contiene **edad al llenado**, no año calendario. `EDAD PACIENTE` contiene edad a la descarga del reporte → ignorar para cálculos.

> Los nombres exactos de columnas del export de estos formularios **no están verificados aún** — confirmar con export real antes de codificar detección de headers.

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

- [ ] **Aclarar "cálculo DISAM" vs "cálculo real"** (los DOS resultados que pediste): ¿cortes distintos, otra convención de puntaje, o qué?
- [ ] Obtener export real de RAYEN para los formularios PSC/PSC-Y/Goldberg y verificar nombres exactos de columnas
- [ ] Confirmar si el puntaje viene precalculado o hay que sumar ítems individuales
- [ ] Confirmar si el campo "Momento" (Ingreso/Egreso) existe como columna o hay que inferirlo por lógica (¿primer formulario del paciente = ingreso?)
- [ ] Verificar rangos etarios exactos usados en la planilla SA_26 para D.3
- [ ] Confirmar si hay columna `INSTRUMENTO` que permita distinguir PSC vs PSC-Y vs Goldberg en un export unificado, o si se exportan por separado

---

## Archivos de referencia
- `SA_26_V1_2.xlsm` — planilla SA (ver estructura celdas D.3). **No en el repo** (queda en la carpeta de trabajo).
- `Manual_Series_REM_2026_SERIE_A.pdf` — pp. 71-72 (definición D.3 y cortes).
- `refs tablas/PSC_PSC-Y_GHQ12_comparativo_final.xlsx` — tabla comparativa de los instrumentos (en el repo, sin PII).
- `legacy/rem_marcar_egresos*.py` — referencia de patrón de parsing RAYEN (quirks documentados).
