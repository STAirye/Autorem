# El merge de `gui-2.0` a `main` (2.0.0, 20-sep-2026)

Scripts de la sesion que ejecuto los pasos 11-13 del
[plan](../../GUI_2.0_plan.md) §12, siguiendo
[prompts/prompt_merge_2.0.md](../gui-2.0_revision/prompts/prompt_merge_2.0.md).
Archivados **como quedaron** (§0 regla 7 del CLAUDE.md raiz).

| Archivo | Que es |
|---|---|
| `repro_a32f2.py` | El que destapo que el falso positivo anunciado para el Trabajo Perdido **tambien golpeaba A32·F1/F2**, que SI tributan al REM, y en las dos direcciones (falso positivo y falso negativo). Es el hermano de `../gui-2.0_revision/sesion-principal/r13/repro_mask_unida.py`, que cubria solo el TP. De aca salio `rem_utils.por_actividad`. |
| `medir_cambio_pagina.py` | Mide cuanto tarda cambiar de pagina, separando la PRIMERA visita (el router es perezoso: construye ahi) de las siguientes. Escrito cuando el autor reporto 2-3 s por pestana en el exe de la 2.0.0 y lo atribuyo a customtkinter: **no es ctk**, es construccion, y se paga una sola vez por pagina (SM Actividades: 6943 ms la 1a, 16 ms la 3a). Los numeros y la decision de NO usar hilos estan en el CHANGELOG de la **2.0.2**, que agrego la precarga incremental con barra. |
| `perfilar_sm.py` | cProfile sobre la construccion de `sm_actividades`: el que cerro la pregunta «esto se puede en hilos?». 8,4 s, de los cuales **7,1 s son `_tkinter.tkapp.call`** (101.700 llamadas a Tk) -> el costo es Tk, no I/O ni imports, asi que no hay trabajo puro que mandar a un worker. |
| `perfilar_about.py` | Lo mismo sobre «Acerca de», que el autor reporto como la que «se pega brutal». 7105 ms, de los cuales **6089 ms son `_tkinter.tkapp.call`** (76.181 llamadas): la hipotesis de que fuera I/O de catalogos era FALSA. Es la pagina mas cara de todas, y ademas es ESPECIAL (no esta en `registro`), asi que la precarga ni la cubria. |
| `medir_precarga_real.py` | La precarga ya implementada, medida con un `mainloop` DE VERDAD e instrumentando cada tick. Hace falta un mainloop porque `app.update()` procesa los timers vencidos y **drena la cadena entera de `after`**, que es el estado que no se queria observar (mordio dos veces, tambien en los tests). |
| `conf.py` | Helper de resolucion de conflictos preservando CRLF: lista los bloques `<<<<<<< / ======= / >>>>>>>` de un archivo y los reemplaza sin tocar los fines de linea. El repo es mayoritariamente CRLF y una resolucion a mano lo convierte a LF en silencio. |

El tercer bug de la tanda (el centinela con byte NUL de `_una_fila_por_atencion`) no
tiene script aparte: se reprodujo en una linea,

```python
pd.DataFrame({'x':[1,2,3]}).groupby(pd.Series(['\x00a','\x00b','\x00c'])).ngroups   # -> 1
```

y quedo amarrado por
`tests/test_a23.py::test_monitoreo_mixto_no_fusiona_las_atenciones_de_una_sola_actividad`.
