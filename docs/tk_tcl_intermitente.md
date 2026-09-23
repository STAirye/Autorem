<!--
This document was generated with the assistance of Claude Opus 5.5 (Anthropic).
The human author reviewed, modified, and integrated the content.

Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
Copyright (C) 2026 Simon Tobar
SPDX-License-Identifier: GPL-3.0-or-later
Version: 2.0.11
-->

# El `tk.tcl` intermitente de `test_gui_construccion`

> **EN CURSO** — abierto 2026-09-23. **Causa encontrada y reproducida sin pytest**
> (§6, «El mecanismo»): la captura por fd de pytest cierra los std handles que Tcl
> tiene anotados, y Windows los reusa. Falta: el arreglo (§7) y confirmarlo en la casa. Lo citan `gui/CLAUDE.md` (Tests) y
> `docs/review_gui-2.0_pendiente.md` §3.

## 1. El síntoma

```
_tkinter.TclError: Can't find a usable tk.tcl in the following directories: ...
This probably means that tk wasn't installed properly.
```

- Sale **solo bajo pytest**, nunca con la app ni con el `.exe` (confirmado por el autor).
- Siempre en `tests/test_gui_construccion.py`, el archivo que crea ~30 `App`/`CTk` en
  **un mismo proceso**. Nunca en el mismo test: en 4 corridas del 22-sep cayeron 4 tests
  distintos. Aislado, el test pasa.
- En **los dos PCs**, con builds muy distintos:

  | | Trabajo | Casa |
  |---|---|---|
  | Python | 3.14.3, Python install manager (`pythoncore-3.14-64`) | 3.9, python.org |
  | Tcl/Tk | 8.6.15 | (anotar al correr el repro) |
  | Antivirus | Windows Defender | Windows Defender |

## 2. Las veces que salió (con evidencia)

| Fecha | Comando | Test caído | Detalle |
|---|---|---|---|
| ~20-sep (ronda 13) | `pytest -q` completo | `test_todas_las_paginas_se_construyen` | sin traceback |
| 21-sep | `tools/correr_tests.py` (3 procesos) | `test_el_banner_de_fuente_no_sobrevive_a_un_cambio_de_archivo` | dentro de `ttk.tcl` (tk.tcl:702) |
| 22-sep | `pytest tests/test_gui_construccion.py` **solo, 1 proceso**, ×4 | 4 tests distintos | mismo error |
| 23-sep | `pytest tests/ -p no:randomly` | `test_el_banner_no_describe_una_corrida_cuyos_archivos_se_cambiaron_mientras_corria` | **traceback completo** ↓ |

El único traceback completo (23-sep) dice cuál es la falla de verdad:

```
couldn't read file ".../tcl/tk8.6/ttk/clamTheme.tcl": no such file or directory
    while executing "source ... clamTheme.tcl"
    (procedure "ttk::LoadThemes" line 18)
    (file ".../ttk/ttk.tcl" line 159)
    (file ".../tk8.6/tk.tcl" line 702)
```

**El archivo existe** (5858 bytes, sin cambios desde abril). Ningún test toca variables
de entorno, el cwd ni borra nada fuera de sus temporales.

## 3. Qué dice internet

**Casos deterministas — no son el nuestro.** Fallan siempre: venv de 3.13.0 en Windows
([cpython#125235](https://github.com/python/cpython/issues/125235), arreglado en 3.13.1),
layout de librerías ([cpython#111754](https://github.com/python/cpython/issues/111754),
[#126549](https://github.com/python/cpython/issues/126549)), uv/python-build-standalone
bajo pytest ([pbs#939](https://github.com/astral-sh/python-build-standalone/issues/939)).
El arreglo es `TCL_LIBRARY`/`TK_LIBRARY`. No aplica: nuestras rutas están bien.

**Casos intermitentes — el nuestro.** Todos son suites de Windows que crean y destruyen
muchos `tk.Tk()` en un proceso:

- [matplotlib#29119](https://github.com/matplotlib/matplotlib/issues/29119):
  `invalid command name "tcl_findLibrary"`, aleatorio, solo en CI. Sin diagnóstico.
- [Hotkey_extension PR#9](https://github.com/TheHCL/Hotkey_extension/pull/9): falla un
  `.tcl` distinto en cada corrida (`init.tcl`, `scale.tcl`). Culpan a Defender y
  reintentan con `pytest-rerunfailures --only-rerun TclError`. Es un parche, no un
  diagnóstico.
- [qsl73#40](https://github.com/kainomatic/qsl73/issues/40) (en alemán), **el más
  parecido**: `init.tcl` / `tcl_findLibrary` que empeoran con la cantidad de tests GUI, a
  veces crash duro (`Tcl_AsyncDelete: async handler deleted by the wrong thread`).
  Diagnóstico: estado de Tcl que se agota tras cientos de ciclos Tk crear/destruir en
  un proceso. Se arregló corriendo los tests GUI en otro proceso; proponen un root de
  sesión compartido, sin implementar.

## 4. Lo que dice el código de Tcl

Dos datos de la fuente de Tcl 8.6 cambian qué hipótesis calzan:

1. **Un lock de antivirus diría otra cosa.** En
   [`win/tclWinError.c`](https://github.com/tcltk/tcl/blob/core-8-6-branch/win/tclWinError.c),
   `ERROR_SHARING_VIOLATION` (32) y `ERROR_LOCK_VIOLATION` (33) mapean a `EACCES`
   (*permission denied*). A `ENOENT` (*no such file*) llegan `FILE_NOT_FOUND`,
   `PATH_NOT_FOUND`, `INVALID_NAME`, `BAD_PATHNAME`, `OPEN_FAILED` y parientes.
2. **Tcl puede decir ENOENT sin tocar el disco.** En
   [`generic/tclIOUtil.c`](https://github.com/tcltk/tcl/blob/core-8-6-branch/generic/tclIOUtil.c),
   `Tcl_FSOpenFileChannel` hace `Tcl_SetErrno(ENOENT)` y devuelve NULL cuando
   `Tcl_FSGetFileSystemForPath` **no le encuentra filesystem a la ruta**. Eso pasa
   entero adentro del proceso, sin llegar a Windows. Y `Tcl_FSEvalFileEx` lo convierte
   en exactamente nuestro `couldn't read file "...": no such file or directory`.

## 5. Hipótesis, y cómo las separa el repro

| | Hipótesis | Predice |
|---|---|---|
| **A** | Disco / antivirus: el `open()` falla de verdad un instante | índice de falla al azar; el mismo proceso se recupera; empeora con procesos en paralelo; falla también Tk pelado |
| **B** | Estado de Tcl que se gasta tras muchos Tk en un proceso (calza con §4.2 y qsl73) | fallas solo pasado un umbral; el mismo proceso queda roto y uno fresco anda; una ventana por proceso = 0 fallas |
| **C** | Algo nuestro que sobrevive a la ventana (`after` de customtkinter, hilos del worker tocando un intérprete muerto) | Tk y CTk pelados limpios; falla solo con `App` |

Orden a priori: **B > C > A**. La app real crea UNA ventana principal, así que lo más
probable es que esto sea **solo de tests**.

**El script:** [`docs/evanesced/tk_tcl_intermitente/repro_tk_tcl.py`](evanesced/tk_tcl_intermitente/repro_tk_tcl.py)
(archivado antes de cerrar, para poder correrlo en la casa). Corre en 3.9 y 3.14, solo ASCII.

| Etapa | Por proceso | Aísla |
|---|---|---|
| S1 | N × `tkinter.Tk()` + update + destroy | Tcl/Tk pelado |
| S2 | N × `ctk.CTk()` + update ×3 + destroy | + customtkinter |
| S3 | N × `App(ruta IRIS)` + `mostrar("a05")` + 60 `update()` | + nuestro código e hilos |
| S4 | S3 con una ventana por proceso fresco | control: B predice 0 |
| S5 | 3 × S2 en paralelo | concurrencia / disco (A) |
| S0 | `pytest tests/test_gui_construccion.py` × K | tasa de referencia (esta parpadea) |

En cada falla anota: el mensaje entero, qué `.tcl` falló, si Python ve y lee ese archivo
en ese momento, si un `Tk()` nuevo anda en el **mismo** proceso y en uno **fresco**, y
los handles GDI/USER/kernel + hilos vivos. Cada 25 ventanas anota los handles aunque no
falle, para ver si crecen. Las ventanas se crean **fuera de pantalla** (−4000,−4000:
mapeadas y pintadas igual, no `withdraw`); `--visible` lo apaga.

Correrlo en la casa (desde la raíz del repo), en este orden — lo que más informa primero:

```bash
python docs/evanesced/tk_tcl_intermitente/repro_min.py dup2 200 repro_min_casa.txt
PYTHONPATH=docs/evanesced/tk_tcl_intermitente python docs/evanesced/tk_tcl_intermitente/matriz_pytest.py 5 base,pin
python docs/evanesced/tk_tcl_intermitente/repro_tk_tcl.py --maquina casa
```

1. ¿El mecanismo también está en 3.9? (`fallas>0`, o archivo vacío = crash duro).
   El `.txt` queda en la raíz: **no commitearlo**, se anota acá y se borra.
2. ¿El pin lo arregla en 3.9? (base con fallas, pin 0).
3. Opcional: la ronda 1 completa. Sale en `%TEMP%\autorem_repro_tk\`, fuera del repo.

Si queda ambiguo: Process Monitor (admin) filtrado por `tk8.6`. Si Windows no registra
ningún `CreateFile` del `.tcl` en el instante de la falla, Tcl nunca tocó el disco -> B.

## 6. Resultados

### Ronda 1 — trabajo, 2026-09-23 (Python 3.14.3, Tcl 8.6.15)

| Etapa | Ventanas | Fallas |
|---|---|---|
| S1 Tk pelado | 500 en 1 proceso | 0 |
| S2 CTk | 300 en 1 proceso | 0 |
| S3 App + a05 + hilo | 60 en 1 proceso | 0 |
| S4 App, proceso fresco | 20 × 1 | 0 |
| S5 CTk × 3 en paralelo | 900 | 0 |
| **S0 pytest real** | ~30 por corrida | **3 de 5 corridas** |

Lo que cambia el cuadro:

- **Fuera de pytest no sale nunca**: S2 solo son ~9000 `source` de `.tcl` (≈30 por
  intérprete) sin una falla. Adentro de pytest sale 3 de 5 veces.
- **Falla en el 2º intérprete del proceso.** En las 3 corridas malas cae
  `test_todas_las_paginas_se_construyen`, el PRIMER test del archivo; el 1º intérprete
  es el `_probe = ctk.CTk()` de nivel de módulo. O sea **B tal como estaba (desgaste
  tras muchos Tk) está descartada**.
- **El `.tcl` que falla cambia cada vez**: `init.tcl`, `spinbox.tcl`, `button.tcl`,
  `clamTheme.tcl`. Cualquier `source` del arranque puede fallar.
- **Dos mensajes distintos**: `no such file or directory` (ENOENT) y, nuevo,
  `couldn't read file ".../init.tcl": No error` — **errno 0**: Tcl anotó un fallo sin
  ningún error del sistema detrás. Es la misma firma «No error» que cita
  Hotkey_extension PR#9.
- **Handles:** 300 `CTk` dejan GDI de 25 a 925 (~3 por ventana; `Tk` pelado no fuga).
  Es una fuga de customtkinter, pero **no** es la causa: S2 no falló con ella.

**Hipótesis nueva, D: algo del proceso de pytest** — lo más sospechoso es la captura a
nivel de fd (pytest hace `dup2` de temporales sobre los fd 1/2 y de `devnull` sobre el
0, y Tcl en Windows arma sus canales estándar desde esos handles). Ronda 2: el archivo
real con `-s`, `--capture=sys` y `-p no:faulthandler` (`matriz_pytest.py`).

### Ronda 2 — qué parte de pytest (trabajo, 2026-09-23)

`test_gui_construccion.py` real, 5 corridas por variante:

| Variante | Corridas con falla |
|---|---|
| base | **4/5** |
| `-p no:faulthandler` | **4/5** |
| `-s` (sin captura) | 0/5 |
| `--capture=sys` (captura sin tocar los fd) | 0/5 |

8/10 con captura por fd contra 0/10 sin ella (Fisher, p ≈ 0,001). **El gatillo es la
captura por fd de pytest.**

Descartado en el camino: que Tcl cierre los std handles al borrar un intérprete
(`handle_std.py`: siguen vivos tras 3 `DeleteInterp`, con stdout en archivo y en consola).

### El mecanismo

En `win/tclWinChan.c`, `OpenFileChannel` guarda **por hilo** una lista de todos los
HANDLE Win32 que ya envolvió, y antes de crear un canal la recorre:

```c
for (infoPtr = tsdPtr->firstFilePtr; infoPtr != NULL; infoPtr = infoPtr->nextPtr) {
    if (infoPtr->handle == (HANDLE) handle) {
        return (permissions==infoPtr->validMask) ? infoPtr->channel : NULL;
    }
}
```

1. El 1er intérprete del hilo (el `_probe` de nivel de módulo, en la colección) envuelve
   los handles de stdin/stdout/stderr como canales estándar. Esos canales **no se
   sueltan** hasta que muere el hilo.
2. La captura por fd de pytest hace `dup2` sobre 0/1/2 en cada fase de cada test, y
   `dup2` **cierra el handle que tenía el fd**: justo los que Tcl tiene anotados.
3. Windows **reusa** los valores de handle liberados. Un `CreateFileW` posterior de un
   `.tcl` puede recibir el valor del viejo stdout.
4. Tcl lo encuentra en la lista: el canal era de escritura y ahora se pide lectura ->
   `NULL`, **sin tocar errno** -> `couldn't read file: No error`, o un `ENOENT` que
   quedó de antes (la búsqueda de `tk.tcl` prueba carpetas que no existen). Si el
   valor reusado era el del viejo stdin (lectura), los permisos CALZAN y Tcl devuelve
   el canal equivocado: el `.tcl` se lee vacío -> la firma
   `invalid command name "tcl_findLibrary"` de matplotlib#29119.

Explica todo lo observado: solo bajo pytest (nadie más hace `dup2` sobre los std fd);
en los dos PCs (es Tcl 8.6 + pytest, no el build de Python); el `.tcl` y el test que
caen son al azar (depende de qué valor reusa Windows); cae ya en el 2º intérprete.

### Ronda 3 — repro mínimo SIN pytest (`repro_min.py`)

Python pelado: un `Tk()`, y antes de cada `Tk()` nuevo, `dup2` de temporales frescos
sobre 0/1/2 (lo que hace `FDCapture`):

| Modo | Ventanas | Fallas |
|---|---|---|
| control (sin `dup2`) | 200 | 0 |
| `dup2` | 200 × 3 corridas | 2 · 2 · **crash duro** (el proceso murió sin escribir su resultado) |

Mismos mensajes que en la suite (`init.tcl`, `tk.tcl`). El crash duro calza con el
`Tcl_AsyncDelete` / `0x80000003` de qsl73#40. **Mecanismo confirmado.**

## 7. Arreglo

Con el mecanismo confirmado, A/B/C ya no aplican. Quedan dos candidatos:

| | Qué | Probado | Costo |
|---|---|---|---|
| **Pin** (`tcl_std_pin.py`, en un `tests/conftest.py`) | Antes del 1er Tk: 3 handles NUL privados como std de Tcl, un `tkinter.Tcl()` que vive todo el proceso para fijarlos, y se restauran los std reales | repro mínimo: 0/3 contra 2·2·crash. Suite real: **0/8 contra 8/8** (ronda 4) | ~25 líneas de ctypes, solo Windows; de yapa el ruido `invalid command name` de Tcl se va a NUL |
| `addopts = --capture=sys` en `pytest.ini` | pytest deja de hacer `dup2` sobre los fd | suite real 0/5 | 1 línea, pero ~170 líneas de ruido de teardown de Tcl a la terminal por corrida del archivo GUI |

La app real y el `.exe` **no** están afectados: nada hace `dup2` sobre sus std fd.

### Ronda 4 — el pin sobre la suite real

Trabajo, 2026-09-23: `matriz_pytest.py 8 base,pin`, intercaladas (mismas condiciones
de máquina para las dos):

| Variante | Corridas con falla |
|---|---|
| base | **8/8** (un test distinto cada vez: `init.tcl` «No error», `menu.tcl`, `panedwindow.tcl`) |
| pin | **0/8** |

p ≈ 0,0002. **El pin arregla la suite real en el PC de trabajo.** Falta la casa (3.9).
