---
name: tests-fuentes
description: Escribe y corre el CONTRATO de toda función que lee una planilla externa del usuario (exports RAYEN/IRIS, reportes, cualquier input nuevo) para cazar al commitear el bug recurrente de c38a8cc — 0 filas que pasan, vacío tras un filtro, columna leída por posición, fechas ilegibles, cruce entre fuentes vacío. Úsalo al crear o tocar un loader o su filtro, al agregar un input nuevo a un módulo, cuando el pre-commit `check_fuentes` bloquee («lector de planillas SIN contrato» o «falla de contrato»), o al agregar/actualizar una referencia en refs_tablas/.
---

# tests-fuentes — el bug recurrente se caza al commitear, no en la revisión

**Por qué existe.** El mismo bug apareció en las 10 rondas de revisión de `gui-2.0`
(registro: `docs/review_gui-2.0_pendiente.md` §1.A, §1.J y §1.K), siempre después de
escrito: un export que pasa el loader y da un **0 plausible** o un **crash críptico**
en vez de `ArchivoInvalido` sobre la FUENTE (CLAUDE.md regla 2). Ahora cada lector de
planillas tiene un **contrato** y el pre-commit lo corre.

## Las piezas

| Pieza | Qué hace |
|---|---|
| `tests/contratos_fuentes.py` | El **arnés** (chequeos C0–C6 + X) y el **registro** `CONTRATOS`. |
| `tools/check_fuentes.py` | Pre-commit. Corre **solo** los contratos de las funciones que el commit toca (`cubre`). **Bloquea** si el commit agrega o cambia un **lector** sin contrato. `--todo`: todos, más la lista de lectores que todavía no tienen contrato. |
| `tests/test_contratos_fuentes.py` | En la suite: corre todos + un meta-test que prueba que el arnés sí caza cada forma del bug. |

**Lector** = función en `programas/`, `modulos/` o `gui/` que llama directo a
`leer_xlsx`, `cargar_canonico`, `load_workbook`, `abrir_xlsx_ro`, `read_excel`,
`read_csv`, `primeras_filas` o `filas_hoja`. No se revisa todo en cada commit: lo que
no se toca ya pasó cuando se tocó. Los lectores viejos entran al registro la primera
vez que alguien los edita.

## Cuándo dispararlo

- Vas a crear un **input nuevo** (un reporte RAYEN más, otro programa de salud) o un
  loader nuevo → escribe el contrato **junto con** el loader, no después.
- Tocas un loader, o un **filtro** sobre lo que carga (mes, programa, dedupe, cruce).
- El pre-commit dijo `COMMIT BLOQUEADO: lector(es) de planillas SIN contrato` o
  `falla(s) de contrato`.
- Llega a `refs_tablas/` el export real de algo que tenía encabezado sintético.

## Qué hacer

### 1. Conseguir el encabezado REAL
- Si el export ya está en `refs_tablas/` (banner + encabezado; skill `limpiar-refs`),
  usa `ref=`. El arnés toma de ahí el banner, el encabezado y su segundo piso si lo hay,
  con el MISMO criterio con que `tools/limpiar_refs.py` recortó la referencia.
- Si no está, **pídeselo al autor** (recortado con `limpiar-refs`) y mientras tanto
  declara `encabezado=`/`banner=` **sintéticos**. El reporte lo marca como faltante.
  Nunca inventes una columna que el export real no trae, y **desconfía de una referencia
  editada a mano**: la del grupal decía `Columna1` donde el export dice `ASISTE (SI/NO)`
  (se había recortado en Excel), y el contrato parecía gritar que faltaba ASISTE. Ante
  la duda, que el autor la baje de nuevo. Pasar un contrato de sintético a real
  destapó en la ronda 11 un fallback que leía un CONTEO como diagnósticos (la
  Estratificación): ese paso vale la pena siempre.

### 2. Escribir el contrato (en `CONTRATOS`)
```python
Contrato(
    id="modulo.cargar_x",
    cubre=("modulos/rem_x.py::cargar_x", "modulos/rem_x.py::_filtro_x"),  # su lector + sus filtros
    llamar=lambda r: _x().cargar_x(r, log=_q),   # lo que hace TODO consumidor primero
    ref="Export_X_iris.xlsx",                    # o encabezado=(...) sintético
    fila={"NUMERO TIPO IDENTIFICACION": RUT, "FECHA ATENCION": "05/08/2026", ...},
    criticas=(...),   # columnas SIN las que no hay resultado: renombrar = ArchivoInvalido
    clave=(...),      # la que identifica la fila: vacía en todas = ArchivoInvalido
    fechas=(...),     # todas ilegibles = ArchivoInvalido (si la guarda vive acá)
    extra=(("todo de otro programa", [fila_otro_programa]),),   # filtros del módulo
)
```
- `llamar` incluye la guarda que TODO consumidor aplica enseguida (ej. `filtrar_mes`).
  Así el contrato mide la cadena que corre de verdad, no el loader pelado.
- `cubre` lista el lector **y** las funciones de filtro/cruce que decidan si queda algo.
  Tocar cualquiera de ellas corre el contrato.
- `extra` es para lo que el arnés genérico no puede saber: **cada filtro** que pueda
  dejar vacío algo que sí tenía filas (máscara de programa, Asiste, Estado,
  momento Ingreso/Egreso, puntaje en rango, casillero del instrumento…).
- Si el export trae dos formatos (IRIS y Administrativo), un contrato **por formato**.

### 3. Qué verifica el arnés (y qué significa cada falla)
| Chequeo | Falla = |
|---|---|
| C0 fila válida | el encabezado real no carga (fila/encabezado desalineados, o el loader asume otra cosa), o sale vacío |
| C1 solo encabezado | 0 filas pasa de largo, o revienta críptico (c38a8cc, 1.9.12) |
| C3 sin `<col>` | una columna crítica que falta **no** falla: hay un fallback (por posición o por default) |
| C4 clave vacía | «tiene filas pero ninguna sirve» pasa de largo (el RUN `"None"` del Inscritos) |
| C5 fechas ilegibles | NaT callado, o un mensaje que manda a otro lado (el A05 decía «elige Archivo completo») |
| C6 columna extra al inicio | el resultado cambia al correr todo una posición: **índice fijo** (la col 11 del A05 leía «Convenio») |
| X `extra` | un filtro del módulo deja todo vacío y sigue |

`errores=` amplía qué cuenta como «fallo claro» (algunos opcionales levantan
`ValueError` a propósito y el módulo lo vuelve aviso). Justifícalo en un comentario.

### 4. Si falla: arreglar la FUENTE, no el contrato
- La guarda va donde se lee o se filtra, con `ArchivoInvalido` y un mensaje que diga
  el **motivo real**: vacío, fecha ilegible, columna que falta, cruce sin coincidencias.
- **Un fixture de test vacío ES el bug.** Si arreglar la guarda rompe un test que armaba
  un resultado entero en 0, lo que se corrige es el fixture (pasó 3 veces en la revisión).
- ¿No se puede arreglar ahora? Entonces `conocidos={"C4": "motivo + dónde se sigue"}`.
  Queda como PENDIENTE visible y no bloquea. Si después pasa, el arnés obliga a sacarlo.
- Cada guarda nueva: **mutante**. Quítala, confirma que su chequeo falla y restáurala.

### 5. Lo que el contrato NO ve: revisarlo a mano al tocar el módulo
El arnés mira un archivo a la vez. Estas formas salieron en la revisión y van en tests
del módulo (`tests/test_<modulo>.py`), no en el contrato:
- **Cruce entre fuentes vacío:** cada fuente trae datos y el join no (la base del P6
  con ESTADO «Activa» o el RUN con puntos; nadie «Pertenece a SALA»). Guarda sobre el
  resultado del cruce.
- **Resultado entero en 0 con el mes cubierto:** un 0 en una casilla es legítimo; en
  TODAS, no (SM sin nada que tribute, A23 sin nada respiratorio).
- **Tipo fijado por la GUI** (casillero de instrumento) sin mirar el contenido.
- **Avisos que no llegan al resumen** de la página: si no bloquea, tiene que verse en
  el «Listo».
- **Opcional cargada que no aporta nada** (Estratificación sin diagnósticos): si el
  usuario la cargó, falla duro (programas/CLAUDE.md §3.1).

### 6. Correr
```bash
python tools/check_fuentes.py --todo
python tests/test_contratos_fuentes.py
```
El hook se instala con los otros tres: `python tools/hooks_git.py --instalar` (en cada clon).

## Notas
- Datos sintéticos siempre: RUT `11111111-1` (CLAUDE.md regla 1). Los fixtures se
  escriben en un temporal, nunca en el repo.
- Un lector que **no** lee un export del usuario (catálogos DEIS versionados, preview de
  detección en la GUI) va a `EXENTOS` de `tools/check_fuentes.py`, con motivo.
- Tocar una primitiva compartida (`TRANSVERSALES`: `leer_xlsx`, `cargar_canonico`,
  `filtrar_mes`…) o el propio registro corre todos los contratos.
