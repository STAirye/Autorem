# -*- coding: utf-8 -*-
"""Al ledger: el conflicto semantico del TP, la direccion del arreglo, el esquema de
versiones y el prompt del merge. Un hallazgo que vive solo en un prompt se pierde."""
import pathlib, sys

p = pathlib.Path(r"E:\git\Autorem\docs\review_gui-2.0_pendiente.md")
b = p.read_bytes()
crlf = b"\r\n" in b
t = b.decode("utf-8").replace("\r\n", "\n")

viejo = "### Deuda conocida, para el paso 11 / el merge"
nuevo = """### El merge: conflicto SEMÁNTICO del Trabajo Perdido + esquema de versiones

**El prompt para hacer el merge en una sesión de cero está escrito:**
[docs/evanesced/gui-2.0_revision/prompts/prompt_merge_2.0.md](evanesced/gui-2.0_revision/prompts/prompt_merge_2.0.md).
Lo de acá es lo que NO puede perderse si ese archivo no se usa.

**`main` tiene 5 commits que la rama no tiene** (el merge-base sigue en `03e15f6`), y uno es
el release **1.9.16** (`10beb79`). `git merge main` desde la rama toca 7 archivos en los dos
lados; seis son triviales (versión, texto, listas) y el séptimo es
`modulos/rem_sm_trabajo_perdido.py`, que es el riesgo más alto del merge **porque puede pasar
limpio y mover un número en silencio**:

- **La rama** (§1.M.2) movió la forma canónica AGUAS ARRIBA: `cargar_atenciones` entrega una
  fila por atención en los dos formatos, con `ACT`/`DIAG` unidas por `SEP_ACTIVIDADES`.
- **`main` 1.9.16** agregó AGUAS ABAJO, en el mismo módulo, `auditar_atenciones` — dos
  auditorías nuevas (`Ctrl_sin_Formulario`, `Sin_Consejeria`) con su propio `_aten_id` y sus
  propios `groupby("aten_id")` sobre las FILAS.

Los dos lados resolvieron «una atención = varias filas» en capas distintas, la misma semana.

**Dirección del arreglo — decisión del autor (20-sep-2026): se adapta `auditar_atenciones`,
NO `cargar_atenciones`.** El cuello de botella es el mecanismo general (por ahí pasan A05,
A23, SM Actividades, TP, Población y dotación); la auditoría es funcionalidad nueva y
específica que resolvió el multilínea por su cuenta porque cuando se escribió el cuello de
botella todavía no lo hacía. Es el caso especial apoyado sobre infraestructura compartida, o
sea lo que §1.M fue a corregir once veces — y el precedente es literal: §1.M.2 **borró**
`a23._act_de_la_atencion` por el mismo argumento. La maquinaria que sobra se borra: sobre el
frame canónico cada fila YA es una atención, así que los dos `groupby` y `_aten_id` se
reducen a máscaras por fila.

**Y el bug no es el `groupby`, es una máscara.** `_mask_control_sm` usa
`contiene_todos(A, "controles", "salud mental por")` — dos tokens buscados por SEPARADO en la
celda. Hoy corre por fila y en el Monitoreo cada fila es UNA actividad, así que los dos tokens
tienen que estar en la misma. Sobre la celda canónica pueden venir de actividades DISTINTAS.
Verificado (repro: `evanesced/gui-2.0_revision/sesion-principal/r13/repro_mask_unida.py`):

```
  fila A sola          : False   <- CONTROLES DE PIE DIABETICO
  fila B sola          : False   <- CONSULTA DE SALUD MENTAL POR PSICOLOGO
  MISMA ATENCION unida : True    <- CONTROLES DE PIE DIABETICO; CONSULTA DE SALUD MENTAL POR PSICOLOGO
```

Ninguna es un Control de Salud Mental y unidas la máscara dispara: la atención cae en
`Ctrl_sin_Formulario` sin serlo — falso positivo **callado**, en una auditoría que el autor usa
para ir a buscar registros incompletos. **Arreglo:** partir la celda por `SEP_ACTIVIDADES` y
evaluar la máscara POR ACTIVIDAD (`any` sobre las partes); el módulo ya conoce la disciplina
(`_tiene_form` parte `FORMULARIOS CLINICOS` por `;` y compara EXACTO, «Nunca substring:
'mental' capta el Minimental»). Revisar TODAS las máscaras multi-token del módulo, no solo
ésa. El test que hay que escribir —y que habría cazado esto solo— es que **IRIS y el Monitoreo
den el mismo número**, que es el sentido entero de `_una_fila_por_atencion`.

**Esquema de versiones — decisión del autor**, arbitrario a propósito (es un recordatorio de
QUÉ pasó dónde, no una historia de releases):

| Número | Qué es |
|---|---|
| **1.9.17** | Toda la ronda de bughunting de `gui-2.0` (las 13 rondas). Se cierra. |
| **1.9.18** | Los fixes que venían de `main` y no estaban en la rama. |
| **2.0.0** | El merge: la GUI 2.0 pasa a ser la GUI. |

Los 3 commits de `main` posteriores a 1.9.16 **no tienen entrada en el CHANGELOG**
(verificado), así que 1.9.18 es donde entran; 1.9.16 se queda como está, que ya está
publicada y §1.E la cita por número. **Trampa del hook:**
`check_version.revisar_colision` bloquea si el CHANGELOG tiene una versión MAYOR que
`rem_utils.VERSION`, así que la entrada `## [1.9.18]` y el bump a 2.0.0 van **en el mismo
commit**.

### Deuda conocida, para el paso 11 / el merge"""

if t.count(viejo) != 1:
    sys.exit("ANCLA FALLIDA (%d)" % t.count(viejo))
t = t.replace(viejo, nuevo, 1)
p.write_bytes((t.replace("\n", "\r\n") if crlf else t).encode("utf-8"))
print("ledger: seccion del merge agregada a §4")
