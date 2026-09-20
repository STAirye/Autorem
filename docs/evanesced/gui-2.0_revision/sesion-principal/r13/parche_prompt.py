# -*- coding: utf-8 -*-
"""Actualiza el prompt del merge: direccion del arreglo del TP + esquema de versiones."""
import pathlib, sys

p = pathlib.Path(r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem"
                 r"\a40108ff-012a-4b37-baf2-2a1dc332a634\scratchpad\r13\prompt_merge_2.0.md")
t = p.read_text(encoding="utf-8")


def rep(viejo, nuevo):
    global t
    if t.count(viejo) != 1:
        sys.exit("ANCLA FALLIDA (%d):\n%s" % (t.count(viejo), viejo[:120]))
    t = t.replace(viejo, nuevo, 1)


# ---- 1. La direccion del arreglo, decidida ---------------------------------
rep("""O sea: los dos lados resolvieron «una atención = varias filas» en capas distintas, la
misma semana, sin saber el uno del otro. Después del merge, el `groupby` de `main` corre
sobre un frame que **ya viene colapsado**, y `_aten_id` duplica una normalización que
ahora vive en `rem_utils`. Qué revisar, con número en la mano:

1. ¿`auditar_atenciones` sigue dando lo mismo sobre el frame canónico? Corré el TP con el
   **mismo** export antes y después del merge y compará las hojas `Ctrl_sin_Formulario` y
   `Sin_Consejeria` fila por fila.
2. Los dos formatos tienen que dar **lo mismo**: el sentido entero de
   `_una_fila_por_atencion` es que IRIS y el Monitoreo coincidan. Probalo con los dos.
3. `_aten_id` de `main` vs `norm()` + `ATENID` de la rama: si sobra, se va (la rama borró
   tres envoltorios equivalentes por esto mismo, §1.M.11). Si NO sobra, el motivo va en
   un comentario.
4. `FORMCLIN` se agrega con `_primero` (1er valor no vacío del grupo). Confirmá que en el
   **Monitoreo** los formularios vengan en la fila padre; si vienen en una hija, `_primero`
   igual los toma, pero escribilo.
5. El arnés de contratos cubre `cargar_atenciones` (IRIS y Monitoreo) y el TP: corré
   `python tools/check_fuentes.py --todo` y, si hace falta, sumá el caso.

**Regla 2 del proyecto aplica de lleno acá:** un número plausible pero mal es peor que un
crash, porque se copia al REM.""",
    """O sea: los dos lados resolvieron «una atención = varias filas» en capas distintas, la
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
crash, porque se copia al REM.""")

# ---- 2. Esquema de versiones, decidido ------------------------------------
rep("""- **Bump a `2.0.0`** con la skill `versionar` (CLAUDE.md §9: X = GUI 2.0).
- **CHANGELOG:** `main` trae 1.9.16 y la rama tiene la entrada **1.9.17 abierta** con las
  13 rondas. Decidir <<<¿se funden las dos en `## [2.0.0]`, o 1.9.17 se cierra y 2.0.0
  es la entrada del merge?>>> — el CHANGELOG es el árbitro anti-colisión, así que esto se
  resuelve explícito, no por accidente.""",
    """- **Esquema de versiones, decidido por el autor** (arbitrario a propósito: es un
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
  arquitectura; el plan ya lo tenía anotado como 2.0.0 = GUI 2.0).""")

p.write_text(t, encoding="utf-8")
print("prompt actualizado:", p.name)
