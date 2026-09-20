# El merge de `gui-2.0` a `main` (2.0.0, 20-sep-2026)

Scripts de la sesion que ejecuto los pasos 11-13 del
[plan](../../GUI_2.0_plan.md) §12, siguiendo
[prompts/prompt_merge_2.0.md](../gui-2.0_revision/prompts/prompt_merge_2.0.md).
Archivados **como quedaron** (§0 regla 7 del CLAUDE.md raiz).

| Archivo | Que es |
|---|---|
| `repro_a32f2.py` | El que destapo que el falso positivo anunciado para el Trabajo Perdido **tambien golpeaba A32·F1/F2**, que SI tributan al REM, y en las dos direcciones (falso positivo y falso negativo). Es el hermano de `../gui-2.0_revision/sesion-principal/r13/repro_mask_unida.py`, que cubria solo el TP. De aca salio `rem_utils.por_actividad`. |
| `medir_cambio_pagina.py` | Mide cuanto tarda cambiar de pagina, separando la PRIMERA visita (el router es perezoso: construye ahi) de las siguientes. Escrito cuando el autor reporto 2-3 s por pestana en el exe de la 2.0.0 y lo atribuyo a customtkinter: **no es ctk**, es construccion, y se paga una sola vez por pagina (SM Actividades: 6943 ms la 1a, 16 ms la 3a). Los numeros estan en el §12 del CLAUDE.md raiz. |
| `conf.py` | Helper de resolucion de conflictos preservando CRLF: lista los bloques `<<<<<<< / ======= / >>>>>>>` de un archivo y los reemplaza sin tocar los fines de linea. El repo es mayoritariamente CRLF y una resolucion a mano lo convierte a LF en silencio. |

El tercer bug de la tanda (el centinela con byte NUL de `_una_fila_por_atencion`) no
tiene script aparte: se reprodujo en una linea,

```python
pd.DataFrame({'x':[1,2,3]}).groupby(pd.Series(['\x00a','\x00b','\x00c'])).ngroups   # -> 1
```

y quedo amarrado por
`tests/test_a23.py::test_monitoreo_mixto_no_fusiona_las_atenciones_de_una_sola_actividad`.
