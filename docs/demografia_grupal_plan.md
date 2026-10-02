<!--
This document was generated with the assistance of Claude Opus 5.5 (Anthropic).
The human author reviewed, modified, and integrated the content.

Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
Copyright (C) 2026 Simon Tobar
SPDX-License-Identifier: GPL-3.0-or-later
Version: 2.0.26
-->

# Plan — Demografía de las actividades grupales (SM Actividades)

> **Estado:** aprobado por el autor (2026-10-02), **sin implementar**. Escrito para una
> sesión fría: todo lo que hace falta está acá o en los archivos citados. Al terminar,
> cerrar este archivo con el header «LISTO Y MERGEADO» (CLAUDE.md §0, regla 7), no
> borrarlo.

## 1. Qué y por qué

El reporte RAYEN «Atenciones Grupales» **no trae demografía** (ni ALERTAS, ni PUEBLO,
ni NACIONALIDAD, ni GENERO). Hoy cada asistencia grupal entra al motor con todos los
flags `dem_*` en `False` (`rem_sm_actividades._ev`, línea «grupal -> False»), así que
las columnas demográficas de la fila **A06 · Intervención Psicosocial Grupal** salen en
0 aunque haya asistentes SENAME, migrantes o TRANS. La LEEME lo declara como
`PENDIENTE` fijo (`programas/cobertura.py`, entrada «Demografia de las actividades
grupales»).

**Pero el grupal sí trae RUN** (`MAPA_GRUPAL["RUN"]`). La demografía se puede buscar
por RUN en otras fuentes que la corrida ya carga.

## 2. Hechos verificados (no re-verificar)

Contra `refs_tablas/SA_26_V1.2.xlsm` y el código al 2.0.26:

| Casilla grupal | ¿Columnas demográficas en el SA_26? | ¿Las calcula el código hoy? |
|---|---|---|
| **A06 · fila 23** «Intervención Psicosocial Grupal» | **Sí**: AN Beneficiarios · AO SENAME · AP Protección Especializada · AQ Pueblos · AR Migrantes · AS Demencia · AT/AU TRANS M/F · AV Cuidadores | Sí, con `DEM_A06` (`_tabla_a06`, `pg = E[E["casilla"] == "A06PG"]`) → hoy en 0 |
| **A19a · A.3** filas 110 / 112 (consejerías familiares 97/99) | **No**: solo «Total Actividades» y «Espacios Amigables» | No aplica |
| **A27 · filas 34/35** (prevención suicidio / trastorno mental) | **Sí**: J..X rango etario, Y-AA Gestantes, AC Pueblos, AD Migrantes, AF/AG TRANS, AH SENAME, AI Protección Especializada | **No**: `_tabla_a27` saca solo «Asistentes» y «Sesiones», sin tramos ni demografía |

Consecuencias:
- El alcance real de este plan es **una fila: A06·23**. El A19a no tiene dónde ponerla.
- El texto de la LEEME de hoy («A06 psicosocial / A19a grupal / A27 salen con
  demografía en 0») está **mal en dos partes**: el A19a no tiene esas columnas y al
  A27 le faltan también los tramos etarios, no solo la demografía. Se corrige en §5.
- El A27 completo (tramos + demografía) queda **fuera** (§7): el autor lo validó como
  `SIN REGISTRO` (el 0 es real, nadie registra la actividad).

## 3. Decisiones cerradas

1. **Cascada por RUN, en este orden** (decisión del autor, roadmap §12):
   1. **Informe Inscritos y Adscritos**, que ya es input OPCIONAL de la página SM (hoy
      solo para TRANS). Cubre a toda la población inscrita.
   2. Si el RUN no está en el Inscritos (o no se cargó): **la última atención de ese
      RUN en el ADA ya cargado** (todo `carga["d"]`, no solo el mes; por `FECHA`).
   3. Si no está en ninguno: **sin dato**.
2. **Tres estados, no dos.** «Sin dato» NO es «NO»: contarlo como NO subcuenta callado
   (CLAUDE.md regla 2). En la tabla el flag queda `False` (no hay otra forma de sumar),
   pero cada asistencia lleva su fuente (`dem_fuente` ∈ `inscritos` / `ada` /
   `sin_dato`) y la LEEME dice cuántas quedaron sin dato (§4.4).
3. **Qué flag sale de dónde**, con las MISMAS reglas que ya existen (no inventar):

   | Flag (`DEM_A06`) | Inscritos | ADA (última atención) |
   |---|---|---|
   | `dem_sename` | ALERTAS contiene `SENAME` | `dem_sename` ya calculado |
   | `dem_mejorninez` | ALERTAS contiene `MEJOR NINEZ` o `SPE EX MEJOR` | `dem_mejorninez` |
   | `dem_cuidador` | ALERTAS contiene `CUIDADOR` | `dem_cuidador` |
   | `dem_migrante` | ALERTAS contiene `MIGRANTE` (el Inscritos no trae `EMIG`) | `dem_migrante` |
   | `dem_originario` | `PUEBLO` (col. «PUEBLO INDIG») ∉ `rem_utils.PUEBLO_VACIO` | `dem_originario` |
   | `dem_trans_m` / `dem_trans_f` | `rem_utils.trans_de(SEXO, GENERO)` | — (el ADA no trae GENERO): sin dato |
   | `dem_demencia` | — | **NO se deriva** (ver abajo) |

   - Las subcadenas de ALERTAS son las de `rem_utils.marcar_demografia`. **Factorizarlas**
     a una constante o helper compartido, no copiarlas: dos copias divergen (pasó con
     `PUEBLO_VACIO`, CORR-2).
   - **`dem_demencia` del grupal queda en 0 y declarado.** En el ADA sale del
     DIAGNÓSTICO *de esa atención*; tomar el de otra atención del mismo RUN cambia la
     semántica (una persona con demencia que va a un taller por otra cosa). Si el autor
     lo quiere, es una decisión aparte.
4. **Foto al día de la descarga.** ALERTAS y PUEBLO del Inscritos (y del ADA) son el
   estado al bajar el archivo, no el del día del taller. Para un mes es aceptable; la
   LEEME lo dice en el aviso de §4.4.
5. **El Inscritos se lee UNA vez.** Es la población entera del CESFAM (~55k filas). Hoy
   `_cargar` llama `trans_map(inscritos)`. Pasar a **`poblacion.cargar_inscritos`**
   (ya contratado en `tests/contratos_fuentes.py`, ya saca el «RUN Responsable» y
   deduplica por RUN, y trae SEXO/GENERO/ALERTAS/PUEBLO por `MAPA_INSCRITOS`), y derivar
   de ESE DataFrame tanto el `tmap` de TRANS como la demografía del grupal.
   - ⚠ `cargar_inscritos` exige `ESTADO` y `SITUACION` además de `RUN`/`SEXO`. Es el
     mismo export, así que no debería romper nada real, pero **un test del SM que arme
     un Inscritos mínimo** (`tests/test_sm_actividades.py:326` usa `trans_map`) puede
     necesitar esas columnas. Ajustar el fixture, no relajar el loader.
   - `trans_map` queda como está (lo usa su contrato y su test); el SM deja de llamarlo.
     `GENERO` no es requerido por `cargar_inscritos`: si falta, TRANS tiene que fallar
     igual que hoy (hoy `trans_map` lo exige) → `ArchivoInvalido` dentro de
     `opcional("inscritos")`.
6. **Versión:** Z (corrección/mejora de un módulo existente), no Y.

## 4. Implementación

### 4.1 Lookup por RUN — `programas/rem_utils.py`

Una función pura, testeable sin archivos:

```python
def demografia_por_run(runs, inscritos=None, ada=None):
    """{RUN -> dict de flags dem_* + 'dem_fuente'} para la cascada Inscritos -> ADA ->
    sin dato (docs/demografia_grupal_plan.md §3)."""
```

- `inscritos` = DataFrame de `poblacion.cargar_inscritos` (o None).
- `ada` = `carga["d"]` con `marcar_demografia` ya aplicado (o None).
- **Normalizar el RUN de los dos lados con el mismo criterio.** Hoy el grupal guarda
  `RUN` crudo y `cargar_inscritos` hace `astype(str).str.strip()`. Usar `norm()` en los
  dos (mayúsculas, `k` del DV) para que `11111111-k` y `11111111-K` calcen.
- ADA: `ada.sort_values("FECHA").groupby(RUN_normalizado)[flags].last()` — los flags
  son bool, así que el problema de `last()` con `''` (§12, Dev/repo) no aplica.

### 4.2 Enganche — `modulos/rem_sm_actividades.py`

- `_cargar`: con `inscritos`, leer `insc = cargar_inscritos(inscritos, log=log)` dentro
  de `with opcional("inscritos")` (sigue cargándose PRIMERO, ronda 12), derivar `tmap`
  de `insc` con `trans_de`, y guardar `insc` en el dict `carga`.
- Después de `g = cargar_grupal(...)`: agregar a `g` las columnas `dem_*` y
  `dem_fuente` con `demografia_por_run(g["RUN"], insc, d)`. Es por RUN y no depende del
  mes, así que va UNA vez en `_cargar` (igual que TRANS sobre `d`).
- `_ev` ya copia `s[c]` si la columna existe (`for c in DEM_COLS`): con las columnas en
  `g`, los eventos grupales las heredan sin tocar `_ev`. Agregar `dem_fuente` a lo que
  viaja si hace falta para el aviso (o calcularlo antes de `_grupal_eventos`).
- `dem_gestante` del grupal: no se toca (`DEM_A06` no lo usa).

### 4.3 Fail loud del cruce

Si se cargó el Inscritos y **ninguna** asistencia grupal del período calza con él, eso
no es «nadie es SENAME»: es RUN en otro formato o archivo equivocado (bug c38a8cc,
«cruce entre fuentes vacío»). Aviso `REVISAR` en la LEEME con el conteo, sin bloquear
(los conteos totales siguen siendo válidos). Mismo criterio si hay ADA pero 0 RUN del
grupal aparecen en él y tampoco hubo Inscritos.

### 4.4 Avisos de la LEEME

- **Quitar** de `cobertura.COBERTURA["sm_actividades"]["no_cubre"]` la línea fija
  «Demografia de las actividades grupales / PENDIENTE».
- **Aviso dinámico** (solo si hay asistencias A06PG en el período):
  `("A06 Psicosocial Grupal (demografia)", "SUBCONTADO" si hay sin_dato, si no "REVISAR",
  "N asistencias: X desde el Inscritos, Y desde la ultima atencion del ADA, Z sin dato
  (cuentan como NO). Es la foto al dia de la descarga, no la del taller",
  "Cargar el 'Informe Inscritos y Adscritos' para completar")`. Sin Inscritos cargado,
  el texto lo dice. Demencia y gestante del grupal: van dichos en el mismo aviso.
- **Agregar** a `no_cubre` una línea fija honesta para el A27: «A27 rango etario y
  demografía (cols J-AI)» / `PENDIENTE` / «la tabla saca solo Asistentes y Sesiones» /
  «A mano si hay asistentes». (Hoy no existe ninguna línea que lo diga.)

## 5. Tests

En `tests/test_sm_actividades.py` (datos SINTÉTICOS, RUT de ejemplo `11111111-1` y
otros con DV válido vía `dv_rut`; fixtures de Inscritos con ESTADO/SITUACION):

1. Asistente grupal con ALERTAS «SENAME» en el Inscritos → A06PG SENAME = 1.
2. Asistente que NO está en el Inscritos pero sí en el ADA con pueblo «Mapuche» → Pueblos = 1, fuente `ada`.
3. Asistente en ninguno → flags 0 y aviso con «1 sin dato».
4. TRANS del Inscritos llega al grupal (hoy no llega).
5. Sin Inscritos cargado: solo la vía ADA, y el aviso lo dice.
6. RUN con DV en minúscula en el grupal y mayúscula en el Inscritos → calza.
7. Inscritos cargado y 0 cruces → aviso `REVISAR` (§4.3).
8. Regresión: con Inscritos, `dem_trans_*` del ADA da lo mismo que antes (el `tmap`
   ahora sale de `cargar_inscritos`).

Y la skill **`tests-fuentes`**: `check_fuentes` exige contrato para todo lector tocado;
si cambia qué columnas lee el SM del Inscritos, actualizar el contrato correspondiente
en `tests/contratos_fuentes.py`.

## 6. Cierre

- Skill `versionar` (bump Z, CHANGELOG, contadores), `tools/check_cp1252.py`, suite
  completa con `PYTHONIOENCODING=utf-8 python -m pytest tests`.
- Actualizar `modulos/CLAUDE.md` (fila de `rem_sm_actividades.py`: quitar «Known issue:
  el grupal no trae demografía») y el §12 del CLAUDE.md raíz (sacar «Demografía del
  grupal» del roadmap).
- Commit; **no push** (lo hace el autor).

## 7. Fuera de alcance

- **A27 completo** (tramos J..X + demografía Y..AI): hoy el 0 es real (`SIN REGISTRO`,
  validado por el autor con un registro de prueba en sep-2026). Si algún día se
  registra, es un plan aparte: necesita `grid()` con las bandas propias del A27
  (empieza en 10-14, más los «Madre, Padre o Cuidador de» E..I).
- `dem_demencia` del grupal desde otra atención (§3.3).
- Gestantes del grupal (solo A27 las pide).

## 8. Divergencias esperadas al implementar

- Algún test de TRANS puede romper al cambiar `trans_map` por `cargar_inscritos` por
  las columnas extra que exige el loader: es el fixture, no el código.
- Si `cargar_inscritos` resulta más lento que `trans_map` sobre el archivo real,
  **medir** antes de optimizar (§12: «antes de tomar cualquiera de estos, PERFILAR»).
- Si el grupal real trae RUN con puntos (`11.111.111-1`) y el Inscritos sin ellos, la
  normalización de §4.1 tiene que sacarlos: verificar contra
  `refs_tablas/Atenciones_Grupales_iris.xlsx` e `Informe_Inscritos__Adscritos_heads.xlsx`
  (solo headers: el formato del RUN se ve en el contrato, no en datos reales).
