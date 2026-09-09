<!--
This document was generated with the assistance of Claude Opus 5 (Anthropic).
The human author reviewed, modified, and integrated the content.

Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
Copyright (C) 2026 Simon Tobar
SPDX-License-Identifier: GPL-3.0-or-later
Version: 1.9.10
-->

# Plan — Auditoría de filtros contra los catálogos oficiales

> **Estado: PLANIFICADO** (sep-2026). Test guardarraíl + skill de apoyo.
> Documento **autocontenido**: se puede implementar sin haber participado de la
> conversación que lo originó.

---

## 0. Problema

Los filtros de actividad de los módulos son **patrones de subcadena escritos a
ojo**. En 1.9.10 se descubrió que uno estaba muerto: A32·F2 buscaba la subcadena
contigua `"controles salud mental por"`, y los nombres reales de RAYEN llevan un
artículo en medio (`Controles **de** Salud Mental por llamadas telefónicas`). No
matcheaba ninguna de las 4 variantes -> **la casilla era 0 estructural**, con
pinta de dato legítimo. Estuvo así desde `legacy/`, o sea desde antes de que el
proyecto supiera que el **Maestro de Actividades** existía como reporte.

Ese es el punto: **todos los patrones se escribieron sin fuente autoritativa**.
Que uno estuviera muerto obliga a asumir que puede haber hermanos, hoy y sobre
todo cuando entren los programas que faltan (Cardiovascular, SSR, Dependencia).

El agravante que hay que tener presente al diseñar: el bug no solo daba 0, sino
que la hoja **LEEME decía «el 0 es correcto, no lo llenes a mano»**. Un chequeo
que no corre solo no habría servido: nadie sospechaba.

---

## 1. Lo que ya se midió (no repetir el trabajo)

Todo esto se corrió sep-2026 contra `refs_tablas/maestro_slim.csv.gz` y los
módulos en 1.9.10. Los números son el fundamento de las decisiones del §2.

| Medición | Resultado |
|---|---|
| Literales de patrón extraíbles por AST (`_all`/`contiene_todos`/`contiene_alguno`) | **54**, en solo **2** archivos (`rem_a23_respiratorio` 33, `rem_sm_actividades` 21) |
| De esos, los que matchean **0** actividades del Maestro | **3**: `"J20"`, `"J44.1"`, `"j0"` (a23) |
| De esos 3, cuántos son bugs | **0** — son códigos **CIE-10** que se matchean contra `DIAG`, no nombres de actividad |
| Patrones de ACTIVIDAD muertos, tras el fix de 1.9.10 | **ninguno** |

**Tres conclusiones que ya no hay que re-derivar:**

1. **El chequeo ingenuo (patrón vs Maestro) da 100% de falsos positivos.** 3 de 3
   hallazgos eran ruido. Un aviso así se ignora a la semana — el modo de falla
   que este proyecto tiene documentado («un aviso que grita siempre deja de
   leerse», CLAUDE.md §2 sobre `formatos.py`).
2. **La extracción por AST tiene huecos justo donde estuvo el bug.** No ve
   `ADA_TRIBUTAN` (sus entradas llegan a `_all` como *variable*, no como literal)
   ni el idioma `serie.str.contains(norm("..."))`, que carga literales reales en
   `rem_a23_respiratorio` (códigos ICD) y `rem_sm_trabajo_perdido`. O sea: el fix
   de `ADA_TRIBUTAN` de 1.9.10 **no** quedaría cubierto por un auditor AST.
3. **Un patrón vivo no garantiza una máscara viva.** Las máscaras son
   composiciones (`&`, `~`, y `_all(A, "x", "y")` = AND de subcadenas). Dos
   subcadenas pueden existir cada una y su conjunción no matchear nada — que es
   exactamente la forma del bug de A32·F2 en su próxima encarnación.

---

## 2. Diseño: auditar en RUNTIME, no por AST

> **Se pasa el Maestro COMPLETO por las máscaras REALES del módulo y se verifica
> que cada casilla sea alcanzable.**

En vez de leer el código buscando strings, se construye un DataFrame sintético
con **una fila por actividad del Maestro** (cruzada con unos pocos instrumentos)
y se corre la función de eventos del módulo tal cual. Si una casilla no aparece,
su filtro está muerto.

Esto **domina** a las dos alternativas que se consideraron:

| Enfoque | Por qué NO |
|---|---|
| AST: extraer literales y cruzarlos con el Maestro | Huecos de cobertura (§1.2) y no ve las composiciones (§1.3). Además obliga a resolver contra qué columna se matchea cada literal (`A`/`I`/`D` hasta su asignación) para no dar falsos positivos |
| Cruzar cada literal contra TODOS los vocabularios (Maestro + CIE-10 con prefijo + estamentos), hallazgo solo si no matchea en ninguno | Resuelve los falsos positivos del §1.1 y es más fuerte (cazaría un ICD mal tipeado), pero **sigue teniendo los huecos del AST**. Buena idea, mal cimiento |

El runtime no necesita nada de eso: no le importa qué columna ni qué idioma de
matcheo, porque **ejecuta el código de verdad**.

**Prototipo ya verificado** (sep-2026, corrió y dio verde):

```python
m = pd.read_csv('refs_tablas/maestro_slim.csv.gz', dtype=str, keep_default_na=False)
acts = sorted(m['ACTIVIDAD'].unique())
instrs = ["Médico", "Psicólogo(a)", "Terapeuta Ocupacional", "Trabajador(a) Social"]
# 1 fila por (actividad x instrumento); ACT_n/INSTR_n normalizados, DEM_COLS en False
E = sm._ada_eventos(dm)
assert {"A04","A06","A19a","A26","A32F1","A32F2"} <= set(E["casilla"])
```

Salida real del prototipo: las 10 combinaciones casilla+sub alcanzadas, ninguna
faltante. Con el patrón viejo de A32·F2, `A32F2` no aparecía — o sea el test
**falla** ante el bug que lo motivó, que es la prueba que importa.

**El instrumento importa:** A04 exige `INSTR == "MEDICO"`. Por eso el sintético
cruza actividades × varios instrumentos; con uno solo, A04 daría falso negativo.

---

## 3. Fase 1 — `tests/test_filtros_vs_maestro.py`

El trinquete. Es la parte con dientes: corre solo, en cada commit (pre-commit ya
encadena la suite vía `check_version`), y no depende de que alguien se acuerde.

Mismo patrón anti-olvido que `tests/test_cobertura.py` (descubre módulos por
introspección y falla si a alguno le falta su entrada).

**Qué verifica:**

1. **Toda casilla es alcanzable.** Por módulo, un set declarado de casillas
   esperadas; si el Maestro completo no produce alguna, falla nombrándola.
2. **Toda `sub` es alcanzable.** No basta con la casilla: A32·F1 tiene 3 vías y
   F2 tiene 2; que la casilla aparezca no prueba que la vía «Videollamadas» viva.
3. **`mask_tributa_ada` no deja fuera nada que sí tributa.** Fuente única de qué
   tributa; si una actividad produce un evento pero la máscara la da por no
   tributante, vuelve a caer como trabajo perdido (fue el síntoma de 1.9.10).
   Asserción: `mask_tributa_ada` es `True` para toda actividad que genere evento.
4. **`skipif`** si falta `refs_tablas/maestro_slim.csv.gz` (está versionado, pero
   el test no debe reventar un clon parcial).

Módulos a cubrir hoy: `rem_sm_actividades` (`_ada_eventos`, `_grupal_eventos`) y
`rem_a23_respiratorio`. Los de población no aplican (no filtran por actividad de
esta forma).

**Ojo con `_grupal_eventos`:** su fuente es el reporte de Atenciones Grupales, no
el ADA, pero sus actividades también salen del mismo Maestro -> mismo test, otro
constructor de DataFrame.

---

## 4. Fase 2 — patrón vs `NUM REM` (el error opuesto)

La fase 1 caza el **falso negativo** (casilla muerta). El error espejo es el
**falso positivo**: un patrón que captura actividades cuyo `NUM REM`/`SECCION` en
el Maestro es **otra** casilla -> sobreconteo silencioso.

Se obtiene casi gratis del mismo sintético: cada evento producido sabe su
actividad, y el Maestro sabe a qué casilla la asigna RAYEN. Diferencia =
candidato a hallazgo.

**Requiere baseline, sí o sí.** El proyecto tiene divergencias DELIBERADAS y sin
declararlas el chequeo grita siempre:

- `Control Salud Mental a Paciente SENAME` — excluido a propósito (hacen su REM).
- Espacios Amigables / Familias en Riesgo — omitidos (no se usan en el centro).
- Las 24 VDI del PADDS (`EXCLUIR_SMISH`) — son A26·**A1**, no A26·**A**.
- Actividades `REM-Gestion` que el centro usa como equivalentes.

Formato del baseline: catálogo **declarativo** en el test (mismo idioma que
`COBERTURA` en `cobertura.py` y `ENO_SIN_CLASIFICAR` en `catalogos.py`): lista de
`(actividad, casilla_nuestra, casilla_maestro, motivo)`. Una divergencia NUEVA
rompe el test; una declarada, no. **Los huecos se declaran, no se rellenan.**

---

## 5. El skill — `auditar-filtros`

El envoltorio ergonómico, para cuando se **incorpora un programa nuevo**. Hoy los
strings se escriben a ojo y después se descubre si viven; el skill invierte eso.

Flujo:

1. Se le da un `NUM REM` (ej. `REM-A23`) y opcionalmente una sección.
2. Filtra el Maestro por ese `NUM REM` y lista las actividades **agrupadas por
   `NUM SECCION`**, con el conteo de estamentos de cada una (proxy de cuán usada
   es).
3. Propone patrones candidatos y muestra, por cada uno, **qué actividades captura
   y cuáles deja fuera** de su sección.
4. Corre la fase 1 sobre el módulo en construcción.

Ahí está la eficiencia que se busca: el Maestro pasa de ser algo contra lo que se
valida *después* a ser el punto de partida.

---

## 6. Qué NO hacer

- **NO convertir el Maestro en fuente de verdad de RUNTIME.** Es validador en
  tiempo de TEST. Se actualiza ~semestralmente y una actividad nueva no está en
  él; por eso `rem_sm_trabajo_perdido` conserva su heurística además del Maestro.
  Reemplazar los patrones por lookups al Maestro rompería el mes siguiente a que
  RAYEN agregue una actividad, **en silencio**.
- **NO auditar por AST** (§2). Ya se evaluó y tiene huecos medidos.
- **NO hacer fallar el test por los códigos CIE-10** (`"J20"`, `"j0"`,
  `"J44.1"`): no son actividades y no viven en el Maestro. Si algún día se
  quieren auditar, es contra `programas/catalogos.py` y **con semántica de
  prefijo** — `J44.1` existe como código, pero `J20` y `j0` son prefijos
  (medido: `existe("J441")` es True, `existe("J20")` es False).
- **NO arreglar de paso** ninguna divergencia que aparezca en la fase 2 sin
  preguntar: varias son deliberadas y la lista del §4 no pretende ser completa.
- **NO codear la fase 2 antes que la 1.** La 1 es corta, cierra el agujero que ya
  mordió y no necesita baseline.

---

## 7. Versionado

Fase 1 es **solo un test** -> no toca el manifiesto de archivos versionados
(`tests/` no lleva versión, CLAUDE.md §9), pero **sí mueve el contador de tests**
en CLAUDE.md §2 y §9, que `tools/check_version.py` verifica. Bump de **Z**.

El skill vive en `.claude/skills/` junto a `limpiar-refs` / `check-cp1252` /
`versionar`; tampoco lleva versión propia.

Correr la skill **`versionar`** antes de commitear.
