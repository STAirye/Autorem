#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Sonnet 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# Copyright (C) 2026 Simon Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.9.17
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. Distributed WITHOUT ANY WARRANTY. See the GNU
# General Public License for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
gui/runner.py - correr un worker en hilo aparte + validar/despachar errores.

Portado de autorem.py sin tocar la logica (docs/GUI_2.0_plan.md, paso 3):
`correr_con_reloj` (hilo + queue + poll) y los helpers que vivian junto a el
("Helpers reutilizables por las pestanias" en el Tk actual) -- validacion de
rutas/carpeta y el despacho de excepciones a un messagebox legible, INCLUIDA
la rama 'cruzados' de 1.9.10. `app.py` (paso 4) los usa para construir `ctx`
antes de lanzar el worker y para interpretar su resultado (SS3.2 del plan:
nada de Tk vars dentro del worker).
"""

import sys
import threading
import queue
from pathlib import Path

import customtkinter as ctk

import programas.rem_saludmental as sm
from gui.widgets import Reloj, ANIO_MAX, ANIO_MIN

_MSG_PERMISO = ("No pude escribir el resultado.\n\nSuele ser porque el archivo está "
                "ABIERTO en Excel (o bloqueado por OneDrive).\n\nCiérralo y reintenta.")

# RAYEN/IRIS exportan en .xls, .csv, .html y .xlsx; la herramienta lee SOLO .xlsx.
_MSG_NO_XLSX = (
    "El archivo no es un Excel .xlsx válido.\n\n"
    "RAYEN/IRIS entregan varios formatos (.xls antiguo, .csv, .html) y esta "
    "herramienta lee SOLO .xlsx.\n\n"
    "Ábrelo en Excel y usa «Guardar como» -> «Libro de Excel (.xlsx)», y carga ese.\n"
    "(Si un .xlsx te da este error, suele ser un .html/.xls disfrazado: mismo arreglo.)")

_FIN = object()   # centinela de fin de trabajo en la cola del runner

# Titulo del messagebox por `ArchivoInvalido.categoria`. En autorem.py este mapa vivia
# DENTRO de _tab_a05 (y solo cubria 4 categorias); al centralizar el despacho en
# `manejar_error` se comparte con todas las paginas. Lo que no esta aca cae al generico.
_TITULO_INVALIDO = {
    "administrativo":         "Parece Administrativo, no IRIS",
    "iris":                   "Parece IRIS, no Administrativo",
    "no_iris":                "Necesito el export IRIS",
    "mes_vacio":              "Sin datos en ese mes",
    "sin_fecha":              "No encuentro la fecha",
    "sin_datos":              "El archivo no trae datos",
    "sin_columnas":           "No reconozco las columnas",
    "modificado":             "El export fue modificado",
    "no_legible":             "No pude leer el archivo",
    "cruzados":               "Archivos cruzados",
    "no_estamentos":          "No es «Utilización de Cupos»",
    "sin_estamento":          "Atenciones sin estamento",
    "no_instrumento":         "No es un export de instrumento",
    "instrumento_desconocido": "No reconozco el instrumento",
}


def dir_salida_default():
    """Carpeta de salida por defecto: donde esta el .exe (empaquetado) o el cwd."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path.cwd()


def slim_por_defecto():
    """Ruta del Maestro SLIM (`maestro_slim.csv.gz`), o None. Ver
    `catalogos.maestro_slim`: busca en las mismas carpetas que los otros
    catalogos (autoREM.spec y tools/slim_maestro.py apuntan ahi)."""
    from programas.catalogos import maestro_slim
    return maestro_slim()


def abrir_carpeta(carpeta):
    from programas.rem_utils import abrir_carpeta as _abrir
    _abrir(carpeta)


def limpiar_ruta(ruta):
    """Ruta tal como la escribio/pego el usuario, sin espacios ni COMILLAS alrededor.

    Las comillas no son un caso raro: el 'Copiar como ruta de acceso' del Explorador
    de Windows (shift + click derecho) las pone siempre, y es LA forma de pegar una
    ruta. Todo lo que lee una ruta de una caja de texto pasa por aca, para que la
    validacion y quien abre el archivo vean la MISMA ruta: el A05 validaba sin
    comillas y detectaba el formato con ellas, y openpyxl respondia 'no es un .xlsx'
    sobre un archivo perfecto."""
    return (ruta or "").strip().strip('"').strip("'").strip()


def valida_ruta(ruta, messagebox):
    """Valida que la ruta exista. Devuelve Path o None (avisa con messagebox)."""
    ruta = limpiar_ruta(ruta)
    if not ruta:
        messagebox.showwarning("Falta el archivo", "Primero elige el Excel.")
        return None
    p = Path(ruta)
    if not p.exists():
        messagebox.showerror("No encontrado", f"No encuentro el archivo:\n{p}")
        return None
    return p


def valida_mes(mes, messagebox):
    """Valida el (año, mes) de un selector de mes. `mes` None = lo tecleado no son
    numeros. Devuelve la tupla o None (avisa con messagebox).

    POR QUE existe: `ttk.Spinbox` acota SOLO sus flechas -- lo que el usuario TECLEA
    pasa igual. Sin esta guarda un mes 13 llegaba al worker y reventaba recien en
    `rem_utils._rango_mes` con un `ValueError: month must be in 1..12` crudo, que
    `manejar_error` no reconoce y despacha como "Error inesperado ... pasaselo a
    Simon": un error de TIPEO presentado como un bug del programa, y despues de
    cargar los archivos (en la pagina de poblacion son minutos de espera). Un año de
    2 digitos (26 por 2026) es peor todavia: no revienta, se va a `filtrar_mes` y
    sale "no hay filas de 07/0026", culpando al export.

    `_tab_a05` y `_tab_beta` validaban el rango en la GUI (autorem.py); el port a
    `widgets.selector_mes` lo perdio para todas las paginas menos A05, que lo tenia
    inline. Aca se comparte: pagina, dialogo de dotacion y A05 llaman a lo mismo."""
    if mes is None:
        messagebox.showwarning("Mes inválido", "Año y mes deben ser números.")
        return None
    anio, m = mes
    if not (1 <= m <= 12):
        messagebox.showwarning("Mes inválido", "El mes debe estar entre 1 y 12.")
        return None
    if not (ANIO_MIN <= anio <= ANIO_MAX):
        messagebox.showwarning(
            "Año inválido",
            f"El año debe estar entre {ANIO_MIN} y {ANIO_MAX}.\n\n"
            f"Escribe el año completo (2026, no 26).")
        return None
    return mes


def valida_carpeta(ruta, messagebox, defecto=None):
    """Valida la carpeta de salida. Si `ruta` esta vacia, cae a `defecto` (la
    carpeta del archivo de entrada) y, si tampoco hay, a `dir_salida_default()`.
    Devuelve Path o None."""
    ruta = limpiar_ruta(ruta)
    p = Path(ruta) if ruta else (Path(defecto) if defecto else dir_salida_default())
    if not p.exists() or not p.is_dir():
        messagebox.showerror("Carpeta inválida", f"No existe la carpeta de salida:\n{p}")
        return None
    return p


def es_error_formato(e):
    """True si la excepcion viene de intentar abrir algo que NO es un .xlsx
    real (extension no soportada por openpyxl, o zip corrupto = html/xls
    disfrazado)."""
    import zipfile
    try:
        from openpyxl.utils.exceptions import InvalidFileException
    except Exception:   # noqa: BLE001
        InvalidFileException = ()
    return isinstance(e, (zipfile.BadZipFile,) + ((InvalidFileException,) if InvalidFileException else ()))


def motivo_fuente(e):
    """Una linea CORTA para el BannerFuente cuando no se pudo abrir el archivo al
    elegirlo. Sale del mismo arbol de `isinstance` que `manejar_error`, a proposito:
    el banner resume y el dialogo (al apretar Procesar) da el arreglo completo, pero
    los dos tienen que estar diciendo lo MISMO del mismo archivo. Si una rama se
    agrega aca y no alla (o al reves), el color y el texto empiezan a contradecirse,
    que es justo lo que SS5.1 del plan prohibe."""
    if isinstance(e, ImportError):
        return "Falta una librería para leer Excel (el detalle, al procesar)."
    if isinstance(e, PermissionError):
        return "No pude abrirlo: está abierto en Excel o bloqueado por OneDrive."
    if es_error_formato(e):
        return "No es un .xlsx real (suele ser un .xls o un .html disfrazado)."
    if isinstance(e, sm.ArchivoInvalido):
        return str(e).split("\n")[0]
    return f"No pude abrir el archivo ({type(e).__name__}); el detalle, al procesar."


def error_inesperado(e, log, messagebox):
    import traceback
    log(f"[ERROR INESPERADO] {type(e).__name__}: {e}")
    if e.__traceback__ is not None:   # format_exc() no sirve: la excepcion vino del worker
        log("".join(traceback.format_exception(type(e), e, e.__traceback__)))
    messagebox.showerror(
        "Error inesperado",
        f"Ocurrió un error no previsto:\n\n{type(e).__name__}: {e}\n\n"
        "Copia el texto del registro y pásaselo a Simón.")


def avisar_cache(messagebox):
    """Muestra (UN dialogo) los avisos de caché pendientes: el caché de dotacion o de
    estamentos que no se pudo leer, estaba dañado o no se pudo guardar
    (rem_utils.leer_cache_json / guardar_cache_json). Hilo GUI. Se llama al terminar
    cada fase que toca el caché (corrida, `preparar`, los dialogos de dotacion). No es
    un error de la corrida -- lo que esta en memoria la sirve igual --, pero cambia
    cifras de los meses siguientes, asi que no puede quedar solo en el log."""
    from programas.rem_utils import tomar_avisos_cache
    avisos = tomar_avisos_cache()
    if avisos and messagebox is not None:
        messagebox.showwarning("Problema con tus preferencias guardadas", "\n\n".join(avisos))


def manejar_error(e, log, messagebox):
    """Despacha una excepcion de procesamiento a un messagebox claro (hilo
    GUI). Incluye ArchivoInvalido (p.ej. la guarda multi-hoja, o 'cruzados'
    desde 1.9.10) sin volcar traceback feo."""
    if isinstance(e, ImportError):
        # El nombre del modulo que falta sale de la excepcion: los modulos pandas y
        # los openpyxl-only levantan ImportError igual, y hardcodear "pandas" mandaba
        # a instalar la libreria equivocada.
        # Los modulos que la levantan a mano (`raise ImportError("Falta 'openpyxl'...")`)
        # ya traen la instruccion de pip en el texto y no tienen `.name`: ahi se muestra
        # tal cual, sin inventar un nombre de paquete.
        falta = getattr(e, "name", None)
        messagebox.showerror(
            "Falta una librería",
            f"Este módulo necesita «{falta}»:\n\n{e}\n\nInstálala con:  pip install {falta}"
            if falta else f"Falta una librería que este módulo necesita:\n\n{e}")
    elif isinstance(e, PermissionError):
        log("[PERMISO DENEGADO] archivo abierto en Excel / OneDrive")
        messagebox.showerror("Permiso denegado", _MSG_PERMISO)
    elif isinstance(e, sm.ArchivoInvalido):
        cat = getattr(e, "categoria", "")
        log(f"[{'archivos cruzados' if cat == 'cruzados' else 'archivo inválido'}: {cat}] {e}")
        messagebox.showerror(_TITULO_INVALIDO.get(cat, "Archivo inválido"), str(e))
    elif es_error_formato(e):
        log(f"[formato no soportado] {e}")
        messagebox.showerror("No es un .xlsx", _MSG_NO_XLSX)
    else:
        error_inesperado(e, log, messagebox)


def sin_opcional(err, ctx, inputs, messagebox, log):
    """Un archivo OPCIONAL que no sirve (`rem_utils.OpcionalInvalido`): pregunta si
    seguir sin él (decisión del autor, ronda 11). Hilo GUI. Devuelve:
      - el `ctx` NUEVO, sin ese archivo y con él anotado en `ctx['descartados']`, si
        el usuario dijo que sí (quien llama re-corre con él);
      - False si dijo que no (ya vio el motivo en la pregunta: no hay otro diálogo);
      - None si el error no es de un opcional de esta página (va a `manejar_error`).
    `inputs` = los de la PANTALLA; un input se reconoce por `entrada` (el nombre del
    parámetro del módulo) o, si no la declara, por su `key`."""
    from programas.rem_utils import OpcionalInvalido
    if not isinstance(err, OpcionalInvalido):
        return None
    inp = next((i for i in inputs if i.get("entrada", i["key"]) == err.entrada
                and not i.get("obligatorio")), None)
    if inp is None or not ctx.get(inp["key"]):
        return None
    nombre = inp["etiqueta"].rstrip(": ")
    motivo = " ".join(str(err).split())
    log(f"[opcional] «{nombre}» no es válido: {motivo}")
    if not messagebox.askyesno(
            "Archivo opcional inválido",
            f"El archivo opcional «{nombre}» no sirve:\n\n{err}\n\n"
            "¿Quieres continuar sin él?\n\n"
            "Sí: se procesa todo lo demás, y la hoja LEEME dice que se omitió.\n"
            "No: se cancela, para que cargues el archivo correcto."):
        log("[opcional] cancelado.")
        return False
    nuevo = dict(ctx)
    nuevo[inp["key"]] = [] if inp.get("multi") else None
    nuevo["descartados"] = list(ctx.get("descartados") or []) + [(nombre, motivo)]
    log(f"[opcional] se continúa SIN «{nombre}».")
    return nuevo


def avisos_descartados(ctx):
    """Avisos para la hoja LEEME de los opcionales que el usuario decidió omitir
    (ver `sin_opcional`). Cada página los suma a los avisos de su resultado."""
    return [(f"{nombre} (opcional)", "OMITIDO",
             f"el archivo cargado no era válido y se continuó sin él: {motivo}",
             "Cargar el archivo correcto y volver a procesar")
            for nombre, motivo in (ctx.get("descartados") or [])]


class Canal:
    """El pedido VIGENTE de un preview asincrono: solo el ultimo pintado vale.

    EL PATRON (se repitio tres veces en la GUI 2.0): un resultado que llega DESPUES
    -- de un hilo, de una corrida -- se pinta sobre una pantalla que el usuario ya
    cambio. Dos elecciones seguidas lanzan dos hilos, y si el del archivo VIEJO
    termina ultimo, su veredicto queda pintado junto al archivo nuevo; «Quitar»
    apaga el banner y el hilo en vuelo lo vuelve a encender sobre una casilla vacia.
    Cada pedido nuevo (o un `invalidar()`, p.ej. al vaciar el input) deja obsoletos
    todos los anteriores, y `en_hilo(..., canal=)` los descarta al llegar.

    Hermanos del mismo patron que NO usan esta clase porque tienen una clave mejor:
    el A05 guarda la categoria junto a la RUTA para la que se calculo
    (`a05.bloque_archivo_formato`), y `app.on_procesar` compara los inputs de la
    corrida con los que hay en pantalla antes de pintar el banner de fuente."""

    def __init__(self):
        self._n = 0

    def nuevo(self):
        self._n += 1
        return self._n

    def invalidar(self):
        self._n += 1

    def vigente(self, n):
        return n == self._n


def en_hilo(widget, trabajo, al_terminar, canal=None):
    """Corre `trabajo()` en un hilo y entrega su resultado a `al_terminar(res, err)`
    EN EL HILO DE LA GUI. Version liviana de `correr_con_reloj` para los previews
    baratos de `on_elegido` (deteccion de formato del A05, chequeo de cruce del SM):
    sin reloj, sin boton que deshabilitar, sin log.

    Por que existe y no un `widget.after(0, ...)` desde el hilo: `Tk.after` NO es
    thread-safe -- registra un comando en el interprete Tcl, y llamarlo desde otro
    hilo tira 'RuntimeError: main thread is not in main loop' o, peor, corrompe el
    estado de Tk de forma intermitente. Por eso `correr_con_reloj` usa cola + poll
    a proposito; esto es el mismo patron, y el `after` sale SIEMPRE del hilo GUI.

    `canal` (un `Canal`, opcional): si otro pedido del mismo canal salio despues (o
    se invalido), el resultado de este se DESCARTA en vez de llamar `al_terminar`.

    Si `trabajo` revienta, la excepcion llega como `err` (nunca se pierde callada)."""
    pedido = canal.nuevo() if canal is not None else None
    q = queue.Queue()

    def worker():
        try:
            q.put((trabajo(), None))
        except Exception as e:   # noqa: BLE001  (se re-despacha en el hilo GUI)
            q.put((None, e))

    threading.Thread(target=worker, daemon=True).start()

    def poll():
        try:
            res, err = q.get_nowait()
        except queue.Empty:
            widget.after(60, poll)
            return
        if canal is not None and not canal.vigente(pedido):
            return   # lo reemplazo un pedido posterior (o se vacio el input)
        al_terminar(res, err)
    widget.after(60, poll)


def correr_con_reloj(root, barra, btn, log, trabajo, al_terminar):
    """Corre `trabajo(log)` en un HILO aparte para que la ventana NO se
    congele. Muestra el reloj de arena girando + 'Procesando...' y vuelca el
    log en vivo. Al terminar llama `al_terminar(resultado, error)` en el hilo
    de la GUI (uno es None). `trabajo` debe usar SOLO el `log` que recibe
    (thread-safe); no tocar widgets (SS3.2 del plan)."""
    q = queue.Queue()
    estado = {}

    def log_seguro(msg=""):
        q.put(str(msg))          # el worker solo encola; la GUI escribe el widget

    def worker():
        try:
            estado["res"] = trabajo(log_seguro)
        except Exception as e:   # noqa: BLE001  (se re-despacha en el hilo GUI)
            estado["err"] = e
        finally:
            q.put(_FIN)

    btn.configure(state="disabled")
    reloj = Reloj(barra, root).start(side="left", padx=(10, 4))
    lbl = ctk.CTkLabel(barra, text="Procesando…  (puede tardar ~1 min)")
    lbl.pack(side="left")
    threading.Thread(target=worker, daemon=True).start()

    def poll():
        try:
            while True:
                item = q.get_nowait()
                if item is _FIN:
                    reloj.stop(); lbl.destroy(); btn.configure(state="normal")
                    al_terminar(estado.get("res"), estado.get("err"))
                    return
                log(item)
        except queue.Empty:
            pass
        root.after(80, poll)
    root.after(80, poll)
