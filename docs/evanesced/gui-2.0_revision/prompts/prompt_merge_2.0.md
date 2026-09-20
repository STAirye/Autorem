# Prompt — el gran merge de `gui-2.0` a `main` (pasos 11-13 del plan)

> Para abrir una sesión DE CERO. Las decisiones del autor ya están incorporadas (la
> dirección del arreglo del Trabajo Perdido y el esquema de versiones): no quedan huecos
> por llenar. Ajustá lo que quieras antes de pegarlo.
> Guardar en `docs/evanesced/gui-2.0_revision/prompts/` cuando el merge esté hecho
> (CLAUDE.md §0 regla 7).

---

Vas a hacer **el merge de la rama `gui-2.0` a `main`**: los pasos 11, 12 y 13 de
`docs/GUI_2.0_plan.md` §12. Es una tarea de EJECUCIÓN, no de revisión: la rama ya pasó
por 13 rondas de code-review y lo encontrado está corregido y anotado. **No la vuelvas a
revisar** — reportar algo que ya está en §1 o §2 del registro es pagar dos veces.

## Leé primero, en este orden

1. **`CLAUDE.md`** raíz — reglas duras (ojo la **regla 7**: ningún documento de trabajo
   se borra), §2 estado, §9 versionado, §10 git, §12 roadmap.
2. **`docs/GUI_2.0_plan.md`** — §8 (qué se hace con la GUI vieja), §9.1 (las tres reglas
   de branchear y **la tabla de port**), §11 (tests), **§12 (el orden: pasos 11-13)**.
3. **`docs/review_gui-2.0_pendiente.md`** §4 — «Checklist del paso 11», «Deuda conocida
   para el paso 11 / el merge», y «Abierto tras la ronda 13». Es tu lista de trabajo.
   §1 y §2 son historia cerrada: leelos solo si necesitás entender POR QUÉ algo está así.
4. **`gui/CLAUDE.md`** — el contrato de la carpeta y sus trampas. El contrato `PANTALLA`
   completo está en el docstring de `gui/app.py`.

## Estado del mundo (verificalo, no lo asumas)

```bash
git log --oneline -1                      # rama gui-2.0, pusheada
git log --oneline -1 main
git merge-base main HEAD                  # 03e15f6
git log --oneline HEAD..main              # lo que main tiene y la rama no
git diff main...HEAD --stat | tail -1
```

Al 20-sep-2026: rama en `a164716` (pusheada, árbol limpio), `main` en `5053dd3`,
merge-base `03e15f6`, diff de **196 archivos / +19.046**. `main` tiene **5 commits** que
la rama no tiene, y uno es el release **1.9.16**.

## ⚠ LO PRIMERO, Y LO MÁS PELIGROSO: el conflicto SEMÁNTICO del Trabajo Perdido

`git merge main` va a tocar estos 7 archivos en los dos lados:

```
.gitignore · CHANGELOG.md · CLAUDE.md · modulos/CLAUDE.md
modulos/rem_sm_trabajo_perdido.py · programas/rem_utils.py · tests/test_trabajo_perdido.py
```

Seis son triviales (versión, texto, listas). **El séptimo no**, y es el riesgo más alto
de todo el merge, porque puede pasar limpio y cambiar un número en silencio:

- **La rama** (ronda 12) movió la forma canónica AGUAS ARRIBA:
  `rem_utils.cargar_atenciones` ahora entrega **una fila por atención** en los dos
  formatos (`_una_fila_por_atencion`), con `ACT`/`DIAG` unidas por `SEP_ACTIVIDADES`
  (`"; "`), `ATENID` en `requeridas`, la cabecera resuelta con `_primero` (incluido
  `FORMCLIN`) y fail loud si un ATEN ID aparece con RUN distintos.
- **`main` 1.9.16** (`10beb79`) agregó AGUAS ABAJO, en el mismo módulo,
  `auditar_atenciones` — dos auditorías nuevas (`Ctrl_sin_Formulario`, `Sin_Consejeria`)
  con **su propio `_aten_id`** normalizador y **sus propios `groupby("aten_id")`** sobre
  las filas, leyendo `FORMCLIN` y `ACT`.

O sea: los dos lados resolvieron «una atención = varias filas» en capas distintas, la
misma semana, sin saber el uno del otro.

### La dirección del arreglo ya está decidida: se adapta `auditar_atenciones`

**Decisión del autor (20-sep-2026), y no es negociable acá:** el que cambia es
`auditar_atenciones`, **no** `cargar_atenciones`. El motivo es de altitud, el mismo criterio
con que se hizo la ronda 12:

- `cargar_atenciones` + `_una_fila_por_atencion` son el **cuello de botella compartido**: por
  ahí pasan el A05, el A23, SM Actividades, el TP, Población y la dotación. La forma
  canónica es el MECANISMO general, y existe justamente para que IRIS y el Monitoreo den el
  mismo número en todos los consumidores.
- `auditar_atenciones` es **funcionalidad nueva y específica** (dos auditorías), que resolvió
  el multilínea por su cuenta porque cuando se escribió el cuello de botella todavía no lo
  hacía. Es el caso especial apoyado sobre la infraestructura compartida, o sea exactamente
  lo que §1.M del registro fue a buscar y corregir once veces.
- **Precedente literal:** §1.M.2 borró `a23._act_de_la_atencion`, que era el AND entre
  actividades hecho a mano en UN consumidor, cuando la forma canónica empezó a darlo gratis.
  Esto es el mismo movimiento, con el mismo argumento.

Así que la maquinaria de `auditar_atenciones` que ahora sobra **se borra**, no se adapta a
medias: sobre el frame canónico cada fila YA es una atención, así que `_aten_id`, el
`groupby("id")` con `.any()` y el `groupby("aten_id").agg(...)` del detalle se reducen a
máscaras por fila y una proyección. Menos código, y un solo lugar donde vive la forma.

### PERO ojo: la forma canónica rompe una máscara. Esto es el bug, no el groupby

`_mask_control_sm` usa **`contiene_todos(A, "controles", "salud mental por")`** — dos tokens
buscados **por separado** en la celda. Hoy en `main` corre por FILA y en el Monitoreo cada
fila es UNA actividad, así que los dos tokens tienen que estar en la MISMA actividad. Sobre
la celda canónica, que trae todas las actividades unidas por `SEP_ACTIVIDADES`, **los dos
tokens pueden venir de actividades DISTINTAS**. Verificado:

```
  fila A sola          : False   <- CONTROLES DE PIE DIABETICO
  fila B sola          : False   <- CONSULTA DE SALUD MENTAL POR PSICOLOGO
  MISMA ATENCION unida : True    <- CONTROLES DE PIE DIABETICO; CONSULTA DE SALUD MENTAL POR PSICOLOGO
```

Ninguna de las dos es un Control de Salud Mental, y unidas la máscara dispara: la atención
cae en `Ctrl_sin_Formulario` sin serlo. Un falso positivo **callado**, en una auditoría que
el autor usa para ir a buscar registros incompletos. Repro corrible en
`docs/evanesced/gui-2.0_revision/sesion-principal/r13/repro_mask_unida.py`.

**La forma del arreglo:** partir la celda por `SEP_ACTIVIDADES` y evaluar la máscara **POR
ACTIVIDAD** (`any` sobre las partes). El módulo ya conoce esta disciplina — `_tiene_form`
parte `FORMULARIOS CLINICOS` por `;` y compara EXACTO, con el comentario «Nunca substring:
'mental' capta el Minimental». Hay que aplicarle el mismo criterio a `ACT`. Revisá **todas**
las máscaras multi-token del módulo, no solo esta: `CONSEJERIA_SM` y lo que use
`contiene_todos` con 2+ tokens tiene el mismo problema.

### Y los chequeos, con número en la mano

1. Corré el TP con el **mismo** export antes y después del merge; compará
   `Ctrl_sin_Formulario` y `Sin_Consejeria` **fila por fila**. Si cambian, tiene que haber
   una razón escrita — y si la razón es el falso positivo de arriba, el número nuevo es el
   correcto y va con su test.
2. **Los dos formatos tienen que dar lo mismo** (IRIS y Monitoreo): es el sentido entero de
   `_una_fila_por_atencion`. Ese es el test que hay que escribir, y es el que habría cazado
   esto solo.
3. `actividades` del detalle se une con `" | "` en `main` — un TERCER separador. Usar
   `SEP_ACTIVIDADES` y no agregar otro (§4 del registro: si el IRIS real usa otro, ese es el
   único valor que hay que corregir).
4. `FORMCLIN` se agrega con `_primero` (1er valor no vacío del grupo): confirmá que en el
   Monitoreo los formularios vengan en la fila padre, y escribilo.
5. `python tools/check_fuentes.py --todo` — el arnés cubre `cargar_atenciones` en los dos
   formatos y el TP. Si el caso de arriba no está, sumalo.

**Regla 2 del proyecto aplica de lleno acá:** un número plausible pero mal es peor que un
crash, porque se copia al REM.

## Orden de trabajo

### A. `git merge main` en la rama (paso 11 del plan)

- Resolver los 7 conflictos. El del TP, con los números de arriba.
- La **tabla de port** de `GUI_2.0_plan.md` §9.1 tiene sus dos filas en «pendiente» y
  **las dos están hechas y verificadas dos veces** (`gui/dialogos.py` trae la familia de
  dotación; `runner._TITULO_INVALIDO["cruzados"]` existe). Pasalas a «sí» con el símbolo
  que lo prueba. Si `main` agregó algo de GUI en estos días, entra a la tabla primero.
- Después del merge: los 3 checks + las dos formas de correr la suite, ANTES de seguir.

### B. Enchufar la GUI 2.0 (paso 11)

- Congelar la GUI vieja según §8 del plan, con la versión de ese momento.
- `autorem.main()` lanza `gui.app`, pasándole el `ruta_inicial` (el canal ya existe).
- **El `import` de `gui.app` va a NIVEL DE MÓDULO**, o `'gui.app'` a `hiddenimports`:
  todos los imports de `autorem.py` son locales a la función y PyInstaller no los ve →
  el exe muere con `ModuleNotFoundError` con el `.spec` ya «arreglado». `gui/paginas/*`
  ya entra por `collect_submodules('gui.paginas')`.
- **Hallazgo #14:** `gui/runner.py` duplica helpers de `autorem.py` y ya divergieron. Se
  resuelve acá: una sola copia, y la que queda es la que la GUI 2.0 usa.
- Los dos headers de versión desfasados (`tools/check_version.py` dice 1.9.10,
  `tools/slim_maestro.py` 1.9.15) suben a la versión del merge.

### C. Versión y documentación (paso 12)

- **Esquema de versiones, decidido por el autor** (arbitrario a propósito: es un
  recordatorio de QUÉ pasó dónde, no una historia de releases):

  | Número | Qué es |
  |---|---|
  | **1.9.17** | Toda la ronda de bughunting de `gui-2.0` (las 13 rondas). **Se cierra.** |
  | **1.9.18** | Los fixes que venían de `main` y no estaban en la rama. |
  | **2.0.0** | El merge: la GUI 2.0 pasa a ser la GUI. |

  Detalle práctico: los 3 commits de `main` posteriores a 1.9.16 **no tienen entrada en el
  CHANGELOG** (verificado), así que 1.9.18 es donde entran, y 1.9.16 se queda como está —
  ya está publicada y el registro de la revisión la cita por número; renumerarla dejaría
  referencias colgando, que es justo la clase que la ronda 13 arregló.

  **⚠ Trampa del hook:** `check_version.revisar_colision` falla si el CHANGELOG tiene una
  versión MAYOR que `rem_utils.VERSION`. Si creás `## [1.9.18]` mientras `VERSION` dice
  1.9.17, el commit se BLOQUEA con «COLISION DE VERSIONES». Hacé la entrada 1.9.18 y el
  bump a 2.0.0 **en el mismo commit** (ahí el top del CHANGELOG es 2.0.0 = VERSION).
- Bump a **`2.0.0`** con la skill `versionar` (CLAUDE.md §9: X = cambio grande de
  arquitectura; el plan ya lo tenía anotado como 2.0.0 = GUI 2.0).
- `check_version` verifica **dos frases exactas** de `CLAUDE.md` (§2 «Versión **X**» y §9
  «Estado actual: **X**») y **cuatro** contadores de tests. **No las reformules.**
- Actualizar `CLAUDE.md` §2 (estado), §9 (versionado) y §12 (roadmap: la GUI 2.0 sale de
  «en curso»), y `docs/GUI_2.0_plan.md` §11, que todavía dice «Hoy la GUI **no tiene
  cobertura**» con 51 tests de GUI escritos.
- **Regla 7:** el registro de la revisión **NO se borra** — lo citan `CHANGELOG.md` (11
  veces), `CLAUDE.md` y la skill `tests-fuentes`. Se le pone el header de cierre:
  `LISTO Y MERGEADO` + fecha + versión en que dejó de usarse. Igual para
  `review_context.md` si lo encontrás. Los scripts de la revisión ya están archivados en
  `docs/evanesced/`.
- Cerrar el worktree (CLAUDE.md §10.1).

### D. Validar el `.exe` (paso 13)

`pyinstaller autoREM.spec`, abrirlo y confirmar: abren las 4 páginas + Inicio + Acerca de;
el sidebar trae los grupos que corresponde; una salida real trae su hoja LEEME; el
Trabajo Perdido **no** dice «heurística» en el log; el botón de catálogos del About no
dice que falta el escáner. Esto **no se puede hacer hoy** (el `.spec` no empaqueta
`gui.app` ni `gui.registro`), y es la primera vez que los arreglos de empaquetado se
prueban contra un build real.

## No hagas

- **No** `--no-verify`. Los cuatro hooks corren: si uno bloquea, se arregla la causa.
- **No** toques el CLI: está **congelado** (§12), incluidos los mensajes de
  `validar_iris`/`validar_admin` que nombran un selector que la 2.0 no tiene.
- **No** borres documentos de trabajo (regla 7): se cierran con header.
- **No** portes «por separado» los arreglos de `programas/`+`modulos/` a `main`: vienen
  con este merge, que es justo la decisión que se tomó en la ronda 12.
- **No** metas mejoras de paso. Si encontrás algo, anotalo en el roadmap de `CLAUDE.md`
  §12 y seguí. La única excepción es un número mal, que se arregla con su test.
- **No** commitees sin que te lo pidan; el autor pushea.

## La compuerta antes de decir «listo»

```bash
python tools/check_version.py && python tools/check_cp1252.py && python tools/check_fuentes.py --todo
python -m pytest -q
for t in tests/test_*.py; do python "$t" || echo "FALLA $t"; done
python -c "import importlib,pkgutil;
[importlib.import_module(m.name) for p in ('gui','programas','modulos','tools')
 for m in pkgutil.walk_packages(importlib.import_module(p).__path__, p+'.')]"
pyinstaller autoREM.spec        # y abrir el exe
```

Reglas del entorno: los tests **nunca** tocan el `~/.autorem` real (todo `tests/test_*.py`
importa `_aislar_cache` primero) · los `.py` son cp1252-safe · nada de PII en el repo, RUT
de ejemplo `11111111-1` · los scratch van solo en tu scratchpad · edición **CRLF-safe**
(la mayoría de los archivos del repo son CRLF: usá la herramienta de edición, o leé bytes
→ normalizá → editá → restaurá).

## Entregable

1. Qué resolviste en cada conflicto, y **para el TP, los números antes/después** en los
   dos formatos.
2. El estado de la compuerta, comando por comando, con su salida.
3. Qué quedó fuera y por qué.
4. Lo nuevo anotado donde corresponde: `CHANGELOG`, `CLAUDE.md` §12, y el header de
   cierre del registro de la revisión.

Después de este merge viene la **ronda de EFICIENCIA y REUSO sobre el codebase completo**
(decisión del autor): ya no es de esta revisión, es la primera de la siguiente sobre `main`.
No la adelantes acá.
