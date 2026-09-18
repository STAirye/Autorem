#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# Copyright (C) 2026 Simon Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. Distributed WITHOUT ANY WARRANTY. See the GNU
# General Public License for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
Construye la ventana REAL y visita TODAS las paginas.

`test_gui_registro.py` valida el CONTRATO de cada PANTALLA (claves, ids, callables)
sin abrir Tk. Esto es el escalon que faltaba: armar los widgets de verdad y correr
ciclos de eventos. Es lo que caza los errores que solo aparecen al construir --
un `pack(after=...)` sobre un widget que no existe todavia, un atributo que no esta,
o un `after()` llamado desde un hilo (que fue justo el bug que lo motivo: la
deteccion de formato del A05 hacia `frame.after(0, ...)` DESDE el worker, y Tk.after
no es thread-safe -> 'RuntimeError: main thread is not in main loop').

Necesita un display. Sin el, se SALTA (no falla): el .exe se compila en Windows con
sesion grafica, que es donde importa.
"""

import sys
import tempfile
from pathlib import Path

import openpyxl

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
import _aislar_cache   # noqa: E402,F401  (PRIMERO: nunca tocar el ~/.autorem real)

_TMP = Path(tempfile.mkdtemp(prefix="autorem_gui_"))

# Motivo por el que se salto todo (lo imprime _main); None = hay display.
SIN_DISPLAY = None
try:
    import customtkinter as ctk
    _probe = ctk.CTk()
    _probe.destroy()
except Exception as e:   # noqa: BLE001  (sin display, sin customtkinter, sin Tcl...)
    SIN_DISPLAY = f"{type(e).__name__}: {e}"


def _fixture_iris():
    """Export IRIS minimo (con UNA fila de datos): la pagina A05 lo recibe como
    ruta precargada y tiene que detectarlo como 'iris'."""
    p = _TMP / "iris_precargado.xlsx"
    if p.exists():
        return p
    wb = openpyxl.Workbook(); ws = wb.active
    ws.append(["Servicio de Salud", None]); ws.append(["Filtros: bla", None])
    ws.append(["NUMERO TIPO IDENTIFICACION", "AÑO APLICACIÓN FORMULARIO", "SEXO",
               "FECHA FORMULARIO", "18.- ¿ TIENE DEPRESIÓN ?", "18.- ESTADO",
               "20.- TIPO DE DEPRESIÓN"])
    ws.append(["11111111-1", 45, "Mujer", "06/07/2026", "SI", "EGRESO ALTA",
               "Depresión Moderada"])
    wb.save(p)
    return p


def _app(ruta_inicial=""):
    from gui.app import App
    app = App(ruta_inicial=str(ruta_inicial))
    app.geometry("1180x820")
    return app


def _buscar_entry(widget):
    """Primer CTkEntry bajo `widget`, en profundidad. Buscarlo por TIPO y no por
    indice de hijo: la maqueta interna de `widgets.fila_archivo` puede cambiar sin
    que este test tenga nada que decir al respecto."""
    if isinstance(widget, ctk.CTkEntry):
        return widget
    for hijo in widget.winfo_children():
        hallado = _buscar_entry(hijo)
        if hallado is not None:
            return hallado
    return None


def _cerrar(app):
    """Cierra la ventana. Al destruirla, customtkinter tiene `after` propios en vuelo
    (check_dpi_scaling, el icono de la barra de titulo) y Tcl escupe unas lineas de
    'invalid command name' a STDERR. Es ruido de teardown, no un fallo: los asserts ya
    pasaron. Cancelarlos a mano con after_cancel es PEOR -- customtkinter despues
    intenta limpiarlos igual y revienta con 'can't delete Tcl command'."""
    app.destroy()


def _bombear(app, veces=15):
    """Ciclos de eventos (en vez de mainloop, que no vuelve): deja correr los
    `after` pendientes, incluido el poll de `runner.en_hilo`."""
    for _ in range(veces):
        app.update()


def test_todas_las_paginas_se_construyen():
    """Cada pagina del registro + las especiales (Inicio / Acerca de) se arman y
    sobreviven ciclos de eventos. Un fallo aca es una ventana que revienta al
    hacer click en el sidebar."""
    if SIN_DISPLAY:
        return
    from gui.app import PAGINAS_ESPECIALES
    app = _app()
    try:
        ids = [p["id"] for p in app.registro] + [e[0] for e in PAGINAS_ESPECIALES]
        assert len(ids) >= 5, f"solo {len(ids)} paginas: falta alguna del sidebar"
        for pid in ids:
            app.mostrar(pid)
            _bombear(app)
    finally:
        _cerrar(app)


def test_a05_detecta_la_ruta_precargada():
    """Arrastrar un .xlsx sobre el exe precarga la ruta (`datos['ruta_inicial']`).
    Esa ruta NO pasa por 'Examinar', asi que hay que detectarle el formato igual --
    si no, el usuario ve 'Formato no reconocido' sobre un archivo perfecto."""
    if SIN_DISPLAY:
        return
    app = _app(_fixture_iris())
    try:
        app.mostrar("a05")
        _bombear(app, 60)   # la deteccion corre en un hilo: hay que darle tiempo
        archivo = app._frames["a05"]  # construida
        assert archivo is not None
    finally:
        _cerrar(app)


def test_a05_detectar_ahora_cubre_la_ruta_tecleada():
    """El corazon del arreglo, sin depender de los tiempos del hilo: la categoria
    se guarda JUNTO A LA RUTA, y `detectar_ahora()` la resuelve sincronicamente
    para lo que haya en la caja. Cubre la ruta tecleada/pegada Y descarta el
    resultado viejo cuando el archivo cambio (la carrera de dos elecciones)."""
    if SIN_DISPLAY:
        return
    from gui.paginas import a05

    app = _app()
    try:
        frame = ctk.CTkFrame(app)
        pagina = type("P", (), {"datos": {}, "root": app})()
        get = a05.bloque_archivo_formato(frame, pagina)

        # Nadie eligio nada: ni ruta ni categoria, y no se inventa una.
        assert get()["ruta"] == "" and get()["categoria"] is None

        # Ruta TECLEADA (sin pasar por Examinar) -> detectar_ahora la resuelve.
        entry = _buscar_entry(frame)
        assert entry is not None, "no encontre la caja de texto de la fila de archivo"
        entry.insert(0, str(_fixture_iris()))
        assert get()["categoria"] is None, "no deberia haber categoria sin detectar"
        assert get()["detectar_ahora"]() == ("iris", None)   # (categoria, error)
        assert get()["categoria"] == "iris" and get()["error"] is None

        # Cambio de archivo -> la categoria vieja NO se reutiliza (anti-carrera).
        entry.delete(0, "end")
        entry.insert(0, str(_TMP / "no_existe.xlsx"))
        assert get()["categoria"] is None, "la categoria del archivo anterior se colo"
    finally:
        _cerrar(app)


def _buscar_boton(widget, texto):
    """Primer CTkButton cuyo texto es `texto`, en profundidad. Por TEXTO y no por
    indice, igual que `_buscar_entry`: la maqueta de la fila puede cambiar."""
    if isinstance(widget, ctk.CTkButton) and widget.cget("text") == texto:
        return widget
    for hijo in widget.winfo_children():
        hallado = _buscar_boton(hijo, texto)
        if hallado is not None:
            return hallado
    return None


def _buscar_banner(widget):
    from gui.widgets import BannerFuente
    if isinstance(widget, BannerFuente):
        return widget
    for hijo in widget.winfo_children():
        hallado = _buscar_banner(hijo)
        if hallado is not None:
            return hallado
    return None


class _dialogo_devuelve:
    """Context manager: 'Examinar...' devuelve `archivos` en vez de abrir el
    filedialog (que en un test colgaria esperando a un humano). Parchea el modulo
    `tkinter.filedialog` REAL, que es el que `widgets.fila_archivos` importa adentro
    de la funcion -- asi el test recorre el camino de verdad (boton -> examinar ->
    on_elegido) en vez de escribirle la seleccion por dentro."""

    def __init__(self, *archivos):
        self.archivos = tuple(str(a) for a in archivos)

    def __enter__(self):
        from tkinter import filedialog
        self._fd = filedialog
        self._previo = filedialog.askopenfilenames
        filedialog.askopenfilenames = lambda **_kw: self.archivos
        return self

    def __exit__(self, *_exc):
        self._fd.askopenfilenames = self._previo
        return False


def test_fila_archivos_se_puede_vaciar():
    """Un input multiple tiene que poder volver a VACIO, no solo sobreescribirse.

    Sin esto la corrida solo-cuestionarios de SM Actividades (que exige 'ni ADA ni
    Grupal', `sm._es_solo_a03`) quedaba inalcanzable con un solo click accidental en
    Examinar: las paginas no se destruyen al cambiar de pantalla (ver App.mostrar),
    asi que la unica salida era reiniciar autoREM. `on_elegido` tiene que enterarse
    del vaciado para que los previews que cuelgan del archivo (el banner de cruce
    ADA<->Grupal) se apaguen solos."""
    if SIN_DISPLAY:
        return
    from gui import widgets

    app = _app()
    try:
        frame = ctk.CTkFrame(app)
        visto = []
        get = widgets.fila_archivos(frame, "ADA:", "Elige el ADA", on_elegido=visto.append)
        quitar = _buscar_boton(frame, "Quitar")
        examinar = _buscar_boton(frame, "Examinar…")
        assert quitar is not None, "la fila no ofrece ningun boton para vaciar"
        assert examinar is not None, "no encontre el boton Examinar de la fila"

        # Vacia: 'Quitar' es un no-op y NO dispara on_elegido de mas.
        quitar.invoke()
        assert get() == [] and visto == [], "Quitar sobre una fila vacia hizo algo"

        with _dialogo_devuelve(_fixture_iris()):
            examinar.invoke()
        assert get() == [str(_fixture_iris())], "Examinar no registro la seleccion"
        assert visto[-1] == [str(_fixture_iris())]

        quitar.invoke()
        assert get() == [], "Quitar no vacio la seleccion"
        assert visto[-1] == [], (
            f"Quitar no le aviso a on_elegido con la lista vacia (vio {visto})")
    finally:
        _cerrar(app)


def test_solo_cuestionarios_sigue_alcanzable_tras_elegir_un_ada_por_error():
    """El caso de usuario que motivo el boton 'Quitar': marco cuestionarios, cargo un
    PSC, y de puro dedo eligio un ADA. `_es_solo_a03` exige 'ni ADA ni Grupal', asi
    que la corrida solo-cuestionarios se volvia inalcanzable -- y con ADA cargado y
    Grupal vacio, Procesar solo sabia pedir el Grupal."""
    if SIN_DISPLAY:
        return
    from gui.paginas import sm
    from gui import widgets

    app = _app()
    try:
        frame = ctk.CTkFrame(app)
        get_ada = widgets.fila_archivos(frame, "ADA:", "Elige el ADA")
        a03 = {"incluir": True, "instrumentos": {"PSC": str(_fixture_iris())}}

        assert sm._es_solo_a03(a03, get_ada(), []), "sin ADA ya deberia ser solo-A03"
        with _dialogo_devuelve(_fixture_iris()):
            _buscar_boton(frame, "Examinar…").invoke()
        assert not sm._es_solo_a03(a03, get_ada(), []), "con ADA no es solo-A03"

        _buscar_boton(frame, "Quitar").invoke()
        assert sm._es_solo_a03(a03, get_ada(), []), (
            "tras Quitar el ADA, la corrida solo-cuestionarios sigue inalcanzable")
    finally:
        _cerrar(app)


def test_el_grupo_del_sidebar_dibuja_la_cabecera_sobre_sus_paginas():
    """`pack` apila en ORDEN DE LLAMADA, no de creacion. `_grupo_colapsable` creaba
    `contenido` antes que `header` (la closure `alternar` lo necesita) y lo empacaba
    ahi mismo, asi que en el PRIMER dibujo los botones de pagina quedaban ARRIBA de
    su propia cabecera ('SALUD MENTAL' debajo de sus paginas). Se auto-corregia al
    colapsar y expandir -- `alternar` re-empaca `contenido`, que entonces si cae al
    final de la pila --, y por eso el sintoma era tan raro: solo el primer dibujo.

    El test mira el orden de `pack_slaves()` (que SI refleja la pila) antes y despues
    de un ciclo colapsar/expandir: los dos tienen que dar lo mismo."""
    if SIN_DISPLAY:
        return
    from gui.app import _grupo_colapsable

    app = _app()
    try:
        barra = ctk.CTkFrame(app)
        contenido = _grupo_colapsable(barra, "Salud Mental")
        grupo = contenido.master

        def orden():
            slaves = grupo.pack_slaves()
            cabecera = next((w for w in slaves if isinstance(w, ctk.CTkButton)), None)
            assert cabecera is not None, "el grupo no tiene cabecera clickeable"
            assert contenido in slaves, "el contenido del grupo no quedo empacado"
            return cabecera, slaves.index(cabecera), slaves.index(contenido)

        cabecera, i_cab, i_cont = orden()
        assert i_cab < i_cont, (
            "primer dibujo: la cabecera del programa quedo DEBAJO de sus paginas "
            f"(pack_slaves: {[type(w).__name__ for w in grupo.pack_slaves()]})")

        cabecera.invoke()                      # colapsar
        assert contenido not in grupo.pack_slaves(), "colapsar no oculto el contenido"
        cabecera.invoke()                      # expandir
        _cab, i_cab, i_cont = orden()
        assert i_cab < i_cont, "tras colapsar/expandir la cabecera quedo debajo"
    finally:
        _cerrar(app)


def test_inicio_queda_al_tope_del_sidebar_y_acerca_de_al_pie():
    """Inicio ANCLADO arriba y Acerca de ANCLADO abajo (feedback del autor, sep-2026).

    Antes la posicion de las dos era implicita: 'donde caiga el bucle de
    PAGINAS_ESPECIALES dentro de _construir_sidebar' (o sea, despues de los grupos de
    programa) mas el orden interno del tuple. Nada declaraba 'Inicio va al tope', asi
    que sumar un programa a ORDEN_PROGRAMAS o reordenar el tuple las movia en silencio.
    Ahora la posicion es un DATO (`posicion` en PAGINAS_ESPECIALES) y esto lo amarra:
    el test compara contra los botones de PANTALLA, no contra indices fijos, asi que
    sigue valiendo cuando se sume una pagina nueva."""
    if SIN_DISPLAY:
        return
    app = _app()
    try:
        # Orden VERTICAL real de todos los botones del sidebar: el widget de cada boton
        # esta en `_botones_sidebar`, y su posicion en pantalla la da winfo_rooty()
        # (vale para los de programa, que viven anidados en su grupo colapsable).
        app.update_idletasks()
        y = {pid: btn.winfo_rooty() for pid, btn in app._botones_sidebar.items()}
        de_programa = [p["id"] for p in app.registro]
        assert de_programa, "el registro no trajo ninguna pantalla"

        assert y["inicio"] < min(y[pid] for pid in de_programa), (
            f"Inicio no quedo al tope del sidebar (y={y})")
        assert y["acerca_de"] > max(y[pid] for pid in de_programa), (
            f"Acerca de no quedo al pie del sidebar (y={y})")
    finally:
        _cerrar(app)


def test_el_banner_de_fuente_no_sobrevive_a_un_cambio_de_archivo():
    """El banner de fuente lo pinta `al_completar` con el resultado de la corrida
    ANTERIOR. Elegir otro archivo lo dejaba encendido: un banner verde ('A/D/A de
    IRIS completo') al lado de un export parcial recien cargado es un color que
    afirma algo falso (SS5.1 del plan, regla 1: el color nunca va solo, y nunca puede
    decir algo distinto del estado real). Tambien tiene que apagarse cuando
    `al_completar` recibe `df=None` (corrida solo-cuestionarios: no hubo ADA)."""
    if SIN_DISPLAY:
        return
    from gui import widgets

    app = _app()
    try:
        app.mostrar("a23_respiratorio")
        _bombear(app)
        frame = app._frames["a23_respiratorio"]
        banner = _buscar_banner(frame)
        assert banner is not None, "la pagina A23 no armo su BannerFuente"

        # Un cambio de input invalida el veredicto de la corrida anterior.
        banner.mostrar("plena", "Fuente: A/D/A de IRIS completo.")
        assert banner._visible, "el banner no se encendio"
        with _dialogo_devuelve(_fixture_iris()):
            _buscar_boton(frame, "Examinar…").invoke()
        assert not banner._visible, (
            "el banner sobrevivio a un cambio de input: sigue afirmando el veredicto "
            "de fuente de una corrida cuyos archivos ya no son los cargados")

        # `df=None` (solo-cuestionarios) apaga, no deja lo de antes.
        banner.mostrar("plena", "Fuente: A/D/A de IRIS completo.")
        pagina = type("P", (), {"datos": {"banner_fuente": banner}})()
        widgets.pintar_banner_fuente(pagina, None)
        assert not banner._visible, "pintar_banner_fuente(df=None) dejo el banner viejo"
    finally:
        _cerrar(app)


def _fixture_disfrazado():
    """El clasico de RAYEN (CLAUDE.md SS13): un .html con extension .xlsx. openpyxl
    lo rechaza con `zipfile.BadZipFile`, NO con un problema de firmas."""
    p = _TMP / "rayen_disfrazado.xlsx"
    p.write_text("<html><table><tr><td>Formulario</td></tr></table></html>",
                 encoding="utf-8")
    return p


def test_a05_no_confunde_un_xls_disfrazado_con_un_formato_no_reconocido():
    """Un .xls/.html con extension .xlsx no es un problema de FIRMAS, es un problema
    de FORMATO DE ARCHIVO, y el arreglo es otro ('Guardar como .xlsx', no
    're-descarga el export sin modificarlo').

    `_leer_categoria` tenia un `except Exception -> 'error_lectura'` que aplastaba
    BadZipFile, PermissionError y el ImportError de openpyxl en un solo veredicto, y
    `preparar` los despachaba a los tres como "Formato no reconocido" con el mensaje
    de las firmas -- mandando a re-descargar un archivo que puede estar perfecto y
    dejando muerta la rama `es_error_formato` de `manejar_error`, que existe justo
    para esto. Ahora la excepcion VIAJA y la clasifica quien sabe."""
    if SIN_DISPLAY:
        return
    from gui.paginas import a05

    app = _app()
    try:
        frame = ctk.CTkFrame(app)
        pagina = type("P", (), {"datos": {}, "root": app})()
        get = a05.bloque_archivo_formato(frame, pagina)

        entry = _buscar_entry(frame)
        entry.insert(0, str(_fixture_disfrazado()))
        categoria, error = get()["detectar_ahora"]()

        assert categoria is None, f"no deberia haber categoria, y dio {categoria!r}"
        assert error is not None, (
            "la excepcion se perdio: `preparar` no puede distinguir 'no es un .xlsx' "
            "de 'no reconozco las firmas' sin ella")
        from gui import runner
        assert runner.es_error_formato(error), (
            f"{type(error).__name__} no se reconoce como problema de formato de "
            "archivo -> el usuario recibiria el dialogo equivocado")

        # Y el banner tiene que decir lo MISMO que dira el dialogo, no culpar al Excel.
        banner = _buscar_banner(frame)
        assert banner is not None and banner._visible, "el banner no se encendio"
        assert "xlsx" in runner.motivo_fuente(error), (
            f"el banner no menciona el problema real: {runner.motivo_fuente(error)!r}")
    finally:
        _cerrar(app)


def test_la_salida_por_defecto_de_poblacion_va_junto_al_inscritos():
    """`_tab_beta` guardaba junto al INSCRITOS (`defecto=entrada.parent`): es el
    snapshot DEL MES reportado. Al portarla, el defecto generico pasó a ser 'el primer
    input cargado', que es el orden en que estan ESCRITOS -- y Poblacion los declara
    en el orden NUMERADO de sus instrucciones (1. Formulario historico, 2. ADA, 3.
    Inscritos), asi que el P6 y el Rescate del mes se iban a la carpeta del historico
    multi-anio. Se arregla con `ancla_salida`, que es un DATO y no una posicion."""
    if SIN_DISPLAY:
        return
    from gui.app import _resolver_ctx
    from gui.registro import cargar_registro

    pantalla = next(p for p in cargar_registro() if p["id"] == "sp_p6_poblacion")
    hist, snap = _TMP / "historico", _TMP / "mes_actual"
    hist.mkdir(exist_ok=True); snap.mkdir(exist_ok=True)
    form, ada, insc = hist / "form.xlsx", hist / "ada.xlsx", snap / "inscritos.xlsx"
    for f in (form, ada, insc):
        f.write_bytes(_fixture_iris().read_bytes())

    getters = {"formularios": lambda: [str(form)], "ada": lambda: [str(ada)],
               "inscritos": lambda: str(insc)}
    # Carpeta de salida VACIA = "junto al archivo cargado" (el defecto que se prueba).
    ctx = _resolver_ctx(pantalla, getters, lambda: (2026, 8), lambda: "")
    assert ctx is not None, "_resolver_ctx rechazo inputs validos"
    assert ctx["carpeta"] == snap, (
        f"la salida por defecto quedo en {ctx['carpeta']}, no junto al Inscritos "
        f"({snap}) -- el ancla_salida no se esta respetando")


def test_a05_acepta_la_ruta_pegada_con_comillas():
    """'Copiar como ruta de acceso' del Explorador (shift + click derecho) pega la ruta
    ENTRE COMILLAS, y es LA forma de pegar una ruta en Windows. `valida_ruta` las
    sacaba, pero la deteccion del A05 abria la ruta con comillas: openpyxl respondia
    InvalidFileException ('.xlsx" no soportado') y el usuario recibia 'No es un .xlsx
    real' sobre un archivo perfecto. Deteccion, `get()` y validacion tienen que ver
    la MISMA ruta."""
    if SIN_DISPLAY:
        return
    from gui.paginas import a05
    from gui import runner

    assert runner.limpiar_ruta('  "C:/x/y.xlsx"  ') == "C:/x/y.xlsx"
    assert runner.limpiar_ruta(None) == ""

    app = _app()
    try:
        frame = ctk.CTkFrame(app)
        pagina = type("P", (), {"datos": {}, "root": app})()
        get = a05.bloque_archivo_formato(frame, pagina)
        entry = _buscar_entry(frame)
        entry.insert(0, f'"{_fixture_iris()}"')
        assert get()["detectar_ahora"]() == ("iris", None)
        assert get()["ruta"] == str(_fixture_iris()), "get() entrega la ruta con comillas"
        assert get()["categoria"] == "iris", "la categoria no quedo amarrada a la ruta limpia"
    finally:
        app.destroy()


def test_a05_y_sm_leen_el_encabezado_aunque_la_dimension_este_rota():
    """La PAGINA, no solo la capa: el A05 detecta y el SM hace el preview de cruce
    leyendo solo el encabezado, y ahi un `read_only=True` pelado respetaba la
    <dimension> del .xlsx. Con la etiqueta en `A1` el encabezado llegaba con UNA
    columna: el A05 daba 'Formato no reconocido' sobre un IRIS valido y el SM nunca
    acusaba un cruce ADA<->Grupal."""
    if SIN_DISPLAY:
        return
    from test_formatos_fuente import _con_dimension, _con_una_fila, ADA_IRIS
    from programas import formatos
    from gui.paginas import a05, sm

    iris_roto = _con_dimension(_fixture_iris(), _TMP / "iris_dim_a1.xlsx", "A1")
    ada_roto = _con_dimension(_con_una_fila(ADA_IRIS, _TMP / "ada_1f.xlsx"),
                              _TMP / "ada_dim_a1.xlsx", "A1")
    assert formatos.parece_reporte(sm._header_rapido(ada_roto)) == "ada", (
        "el preview de cruce del SM leyo el encabezado mocho")

    app = _app()
    try:
        frame = ctk.CTkFrame(app)
        pagina = type("P", (), {"datos": {}, "root": app})()
        get = a05.bloque_archivo_formato(frame, pagina)
        _buscar_entry(frame).insert(0, str(iris_roto))
        assert get()["detectar_ahora"]() == ("iris", None), (
            "un IRIS valido con la <dimension> rota no se reconocio")
    finally:
        app.destroy()


def _esperar(app, segundos=0.6):
    """Como `_bombear`, pero dejando pasar TIEMPO de verdad: el poll de
    `runner.en_hilo` / `correr_con_reloj` es un `after(60/80 ms)`, y un rafaga de
    `update()` termina antes de que venza -- el resultado del hilo nunca llegaba."""
    import time
    fin = time.monotonic() + segundos
    while time.monotonic() < fin:
        app.update()
        time.sleep(0.02)


def test_el_cruce_del_sm_solo_pinta_la_ultima_eleccion():
    """Preview de cruce ADA<->Grupal: dos elecciones seguidas lanzan dos hilos, y
    pintaba el que terminara ULTIMO -- el veredicto del archivo viejo quedaba junto al
    nuevo. Y 'Quitar' apagaba el banner, pero el hilo en vuelo lo volvia a encender
    sobre una casilla VACIA. Gemelo de la carrera del A05 (ledger SS1.B)."""
    if SIN_DISPLAY:
        return
    import threading
    from programas import formatos
    from gui.paginas import sm

    soltar = threading.Event()
    previos = (sm._header_rapido, formatos.parece_reporte)

    def header_falso(ruta):
        if "lento" in str(ruta):
            soltar.wait(5)
        return ruta
    sm._header_rapido = header_falso
    formatos.parece_reporte = lambda h: "grupal" if "grupal" in str(h) else "ada"
    app = _app()
    try:
        frame = ctk.CTkFrame(app)
        on_elegido = sm._chequeo_cruce(frame, None, "ada")
        banner = _buscar_banner(frame)

        # 1. Grupal (lento) en la casilla del ADA, y 'Quitar' antes de que termine.
        on_elegido(["grupal_lento.xlsx"])
        on_elegido([])
        soltar.set(); _esperar(app)
        assert not banner._visible, (
            "el hilo de un archivo ya QUITADO volvio a encender el banner de cruce")

        # Control: sin nada que lo reemplace, el cruce SI se acusa (el test prueba algo).
        on_elegido(["grupal.xlsx"]); _esperar(app)
        assert banner._visible, "el cruce no se acuso nunca: el test no prueba nada"

        # 2. Viejo lento (cruzado) y nuevo rapido (correcto): gana el nuevo.
        soltar.clear()
        on_elegido(["grupal_lento.xlsx"])
        on_elegido(["ada.xlsx"]); _esperar(app)
        assert not banner._visible, "el archivo correcto no apago el banner"
        soltar.set(); _esperar(app)
        assert not banner._visible, (
            "el resultado del archivo VIEJO se pinto sobre el nuevo")
    finally:
        sm._header_rapido, formatos.parece_reporte = previos
        soltar.set()
        _cerrar(app)


def test_el_banner_no_describe_una_corrida_cuyos_archivos_se_cambiaron_mientras_corria():
    """Durante la corrida solo Procesar esta deshabilitado: el usuario puede elegir otro
    archivo mientras el worker trabaja, y `al_completar` pintaba igual el veredicto de
    fuente de ESTA corrida al lado del archivo nuevo (verde 'IRIS completo' junto a un
    Monitoreo recien elegido)."""
    if SIN_DISPLAY:
        return
    import threading
    import pandas as pd
    from gui import widgets
    from gui.app import App

    soltar = threading.Event()

    def correr(ctx, log):
        soltar.wait(5)
        return pd.DataFrame({"x": [1]})

    pantalla = {"id": "prueba", "programa": "Respiratorio", "titulo": "Prueba",
                "estado": "estable",
                "inputs": [{"key": "atenciones", "etiqueta": "Atenciones:", "multi": True}],
                "mes": False, "carpeta_salida": False,
                "extras": [{"despues_de": "atenciones", "construir": widgets.bloque_banner_fuente}],
                "correr": correr, "resumen": lambda res: "Listo.",
                "al_completar": lambda res, pagina: widgets.pintar_banner_fuente(pagina, res)}
    app = App(registro=[pantalla])
    try:
        app.mostrar("prueba")
        frame = app._frames["prueba"]
        banner = _buscar_banner(frame)
        examinar, procesar = _buscar_boton(frame, "Examinar…"), _buscar_boton(frame, "Procesar")

        # Control: sin cambios, la corrida SI pinta el banner.
        with _dialogo_devuelve(_TMP / "a.xlsx"):
            examinar.invoke()
        soltar.set(); procesar.invoke(); _esperar(app)
        assert banner._visible, "la corrida no pinto el banner: el test no prueba nada"

        # El archivo cambia MIENTRAS corre -> el banner no afirma nada.
        soltar.clear(); procesar.invoke()
        with _dialogo_devuelve(_TMP / "b.xlsx"):
            examinar.invoke()
        soltar.set(); _esperar(app)
        assert not banner._visible, (
            "el banner describe una corrida cuyos archivos ya no son los elegidos")
    finally:
        soltar.set()
        _cerrar(app)


def test_cerrar_la_ventana_con_una_corrida_viva_pregunta_primero():
    """El worker es un hilo daemon: la X de la ventana terminaba el proceso y lo mataba
    donde estuviera, sin avisar (incluso escribiendo el .xlsx). Con una corrida viva
    tiene que preguntar -- y un «No» deja la ventana abierta --; sin corridas, cierra
    de una, sin preguntar nada."""
    if SIN_DISPLAY:
        return
    import threading
    import gui.app as appmod
    from gui.app import App

    soltar = threading.Event()
    pantalla = {"id": "prueba", "programa": "Respiratorio", "titulo": "Prueba",
                "estado": "estable", "inputs": [], "mes": False, "carpeta_salida": False,
                "correr": lambda ctx, log: soltar.wait(5), "resumen": lambda res: "Listo."}
    preguntas = []
    previo = appmod.messagebox.askyesno
    app = App(registro=[pantalla])
    try:
        app.mostrar("prueba")

        def cerrar_con_la_x():
            # Lo que hace el gestor de ventanas: el comando REGISTRADO en la X, no un
            # metodo llamado a mano (si nadie lo registro, esto revienta).
            app.tk.call(app.protocol("WM_DELETE_WINDOW"))
        _buscar_boton(app._frames["prueba"], "Procesar").invoke()
        assert app._corridas == 1, "la corrida no quedo contada como viva"

        appmod.messagebox.askyesno = lambda *a, **k: (preguntas.append(a[0]), False)[1]
        cerrar_con_la_x()
        assert preguntas, "cerro con una corrida viva sin preguntar"
        assert app.winfo_exists(), "el «No» cerro la ventana igual"

        soltar.set(); _esperar(app)
        assert app._corridas == 0, "la corrida terminada sigue contada como viva"
        preguntas.clear()
        cerrar_con_la_x()
        assert not preguntas, "sin corridas vivas no deberia preguntar nada"
        app = None   # ya la cerro `_al_cerrar`
    finally:
        appmod.messagebox.askyesno = previo
        soltar.set()
        if app is not None:
            _cerrar(app)


def _textos(widget):
    """Todo el texto de las etiquetas bajo `widget`, en profundidad."""
    out = []
    if isinstance(widget, ctk.CTkLabel):
        out.append(str(widget.cget("text")))
    for hijo in widget.winfo_children():
        out += _textos(hijo)
    return out


def test_el_aviso_de_cache_de_una_corrida_se_muestra():
    """El worker puede leer/guardar un caché (estamentos en el A03, dotacion en el SM).
    Si falla, el aviso tiene que salir en pantalla al terminar la corrida -- en el exe
    el log de `print` no lo ve nadie."""
    if SIN_DISPLAY:
        return
    import gui.app as appmod
    import programas.rem_utils as ru
    from gui.app import App

    def correr(ctx, log):
        ru._avisar_cache(lambda *_: None, "No pude guardar la tabla de estamentos")
        return "ok"

    pantalla = {"id": "prueba", "programa": "Respiratorio", "titulo": "Prueba",
                "estado": "estable", "inputs": [], "mes": False, "carpeta_salida": False,
                "correr": correr, "resumen": lambda res: "Listo."}
    vistos, previo = [], appmod.messagebox.showwarning
    ru.tomar_avisos_cache()
    app = App(registro=[pantalla])
    try:
        appmod.messagebox.showwarning = lambda t, m, **k: vistos.append(m)
        app.mostrar("prueba")
        _buscar_boton(app._frames["prueba"], "Procesar").invoke()
        _esperar(app)
        assert any("No pude guardar" in m for m in vistos), (
            f"el aviso de caché de la corrida no se mostro: {vistos}")
    finally:
        appmod.messagebox.showwarning = previo
        _cerrar(app)


def test_acerca_de_explica_las_preferencias_y_las_paginas_apuntan_ahi():
    """El detalle de «no se guardan tus preferencias» vive en Acerca de (donde esta el
    caché, su estado, que hacer); las cajas que usan un caché dejan UNA linea que
    apunta ahi, para no llenar la pagina con un caso borde."""
    if SIN_DISPLAY:
        return
    from gui import dialogos
    from programas import dotacion
    app = _app()
    try:
        app.mostrar("acerca_de")
        _bombear(app)
        about = "\n".join(_textos(app._frames["acerca_de"]))
        assert "Preferencias guardadas" in about, "Acerca de no tiene la seccion"
        assert str(dotacion.RUTA_CACHE.parent) in about, "no dice DONDE esta el caché"
        assert "perfil temporal" in about, "faltan las instrucciones"

        app.mostrar("sm_actividades")
        _bombear(app)
        sm = _textos(app._frames["sm_actividades"])
        n = sum(dialogos.REF_PREFERENCIAS in t for t in sm)
        assert n == 2, f"la referencia a Acerca de deberia estar en Dotación y Estamentos ({n})"
    finally:
        _cerrar(app)


def _checkbox(widget, texto):
    """CTkCheckBox bajo `widget` cuyo texto contiene `texto`, en profundidad."""
    if isinstance(widget, ctk.CTkCheckBox) and texto in str(widget.cget("text")):
        return widget
    for hijo in widget.winfo_children():
        hallado = _checkbox(hijo, texto)
        if hallado is not None:
            return hallado
    return None


def _en_el_dialogo(app, accion):
    """Corre `accion(top)` apenas el CTkToplevel del dialogo exista (el dialogo se
    queda en `wait_window`, asi que hay que actuar desde un `after`)."""
    def intentar():
        tops = [w for w in app.winfo_children() if isinstance(w, ctk.CTkToplevel)]
        if tops:
            accion(tops[-1])
        else:
            app.after(50, intentar)
    app.after(50, intentar)


def _dos_ventanas(nombre_cache):
    """Tabla en disco con Ana y Beto internos. Devuelve (dotacion, tabla que abre la
    ventana A, lo que hace la ventana B mientras A esta abierta)."""
    from programas import dotacion
    dotacion.RUTA_CACHE = _TMP / nombre_cache
    q = lambda *_a, **_k: None   # noqa: E731
    dotacion.marcar(dotacion.cargar(log=q), {"Ana Soto": False, "Beto Ruiz": False}, log=q)
    tabla_a = dotacion.cargar(log=q)

    def ventana_b():
        dotacion.marcar(dotacion.cargar(log=q), {"Ana Soto": True}, log=q)
    return dotacion, tabla_a, ventana_b


def test_revisar_dotacion_no_revierte_lo_que_guardo_otra_ventana():
    """Dos autoREM abiertos: A abre «Revisar dotación», B marca externa a Ana, A
    cambia SOLO a Beto y aplica. Ana tiene que seguir externa: sus atenciones no
    pueden volver a contar en el REM por un nombre que A ni toco."""
    if SIN_DISPLAY:
        return
    from gui import dialogos
    dotacion, _tabla_a, ventana_b = _dos_ventanas("dot_revisar.json")
    app = ctk.CTk()
    try:
        def accion(top):
            ventana_b()
            _checkbox(top, "BETO RUIZ").select()
            _buscar_boton(top, "Aplicar").invoke()
        _en_el_dialogo(app, accion)
        dialogos.revisar_dotacion(app, "sm")
        disco = dotacion.cargar(log=lambda *_: None)
        assert dotacion.clase("Beto Ruiz", disco) == dotacion.EXTERNO, "no guardo el cambio de A"
        assert dotacion.clase("Ana Soto", disco) == dotacion.EXTERNO, (
            "«Revisar dotación» devolvio a interna a alguien que no toco")
    finally:
        _cerrar(app)


def test_precargar_dotacion_no_revierte_y_guarda_los_nuevos():
    """Mismo caso por el dialogo de «Precargar» (todos los del mes, clasificados o
    no), con un nombre NUEVO sin tick: ese si se guarda, como interno."""
    if SIN_DISPLAY:
        return
    import pandas as pd
    from gui import dialogos
    dotacion, tabla_a, ventana_b = _dos_ventanas("dot_precargar.json")
    filas = pd.DataFrame({"funcionario": ["Ana Soto", "Beto Ruiz", "Carla Paz"],
                          "estamento": ["PSICOLOGO"] * 3, "n_atenciones": [3, 2, 1],
                          "actividades": [""] * 3, "sector": [""] * 3})
    app = ctk.CTk()
    try:
        def accion(top):
            ventana_b()
            _buscar_boton(top, "Aplicar").invoke()
        _en_el_dialogo(app, accion)
        dialogos.dialogo_dotacion(app, tabla_a, "sm", filas)
        disco = dotacion.cargar(log=lambda *_: None)
        assert dotacion.clase("Ana Soto", disco) == dotacion.EXTERNO, (
            "«Precargar dotación» devolvio a interna a alguien que no toco")
        assert dotacion.clase("Carla Paz", disco) == dotacion.INTERNO, (
            "un nombre nuevo sin tick tiene que quedar guardado como interno")
    finally:
        _cerrar(app)


def test_ctktoplevel_despacha_los_clicks_encolados():
    """PREMISA del candado de `dialogos._DOTACION_ABIERTA`: crear un `CTkToplevel`
    despacha, dentro de su propio constructor, los clicks que estaban encolados
    (en Windows hace withdraw + `update()` para repintar la barra de titulo). Si
    customtkinter deja de hacerlo, este test avisa que el candado sobra -- no que
    este mal."""
    if SIN_DISPLAY or not sys.platform.startswith("win"):
        return
    app = ctk.CTk()   # ventana pelada: `App` usa grid y aca se empaca con pack
    try:
        clicks = []
        boton = ctk.CTkButton(app, text="Revisar", command=lambda: clicks.append(1))
        boton.pack()
        _bombear(app)
        # Un click del usuario mientras la ventana estaba congelada (queda en la cola).
        boton._canvas.event_generate("<Enter>", when="tail", x=5, y=5)
        boton._canvas.event_generate("<ButtonRelease-1>", when="tail", x=5, y=5)
        assert clicks == [], "el click se despacho antes de tiempo: el test no prueba nada"
        top = ctk.CTkToplevel(app)
        assert clicks == [1], (
            "CTkToplevel ya NO despacha los clicks encolados en su constructor: el "
            "candado de dialogos._DOTACION_ABIERTA quizas sobra (revisalo)")
        top.destroy()
    finally:
        _cerrar(app)


def test_las_etiquetas_envolventes_caben_en_su_caja_con_el_dpi_escalado():
    """`e.width` (evento <Configure>) viene en pixeles REALES y `CTkLabel` escala su
    `wraplength` otra vez: con Windows al 150% el texto pedia 1.5x el ancho de la caja
    y se cortaba por la derecha (instrucciones, avisos, el mensaje del BannerFuente)."""
    if SIN_DISPLAY:
        return
    from gui import widgets
    previa = ctk.ScalingTracker.widget_scaling
    ctk.set_widget_scaling(1.5)
    app = ctk.CTk()
    app.geometry("600x300")
    try:
        caja = ctk.CTkFrame(app)
        caja.pack(fill="x", padx=10)
        lbl = widgets.etiqueta_envolvente(caja, "palabra " * 80)
        lbl.pack(fill="x", padx=8)
        _bombear(app)
        assert lbl._get_widget_scaling() > 1.2, "el escalado no se aplico: el test no prueba nada"
        assert lbl._label.winfo_reqwidth() <= caja.winfo_width(), (
            f"la etiqueta pide {lbl._label.winfo_reqwidth()} px en una caja de "
            f"{caja.winfo_width()} px: el texto se corta por la derecha")
    finally:
        _cerrar(app)
        ctk.set_widget_scaling(previa)


def _main():
    if SIN_DISPLAY:
        print(f"SKIP  sin display / sin customtkinter ({SIN_DISPLAY})")
        print("-" * 50)
        print("0/0 OK (saltado)")
        return 0
    pruebas = [v for k, v in sorted(globals().items())
               if k.startswith("test_") and callable(v)]
    fallos = 0
    for fn in pruebas:
        try:
            fn()
            print(f"PASS  {fn.__name__}")
        except AssertionError as e:
            fallos += 1
            print(f"FAIL  {fn.__name__}  -> {e or 'assert'}")
        except Exception as e:  # noqa: BLE001
            fallos += 1
            print(f"ERROR {fn.__name__}  -> {type(e).__name__}: {e}")
    print("-" * 50)
    total = len(pruebas)
    print(f"{total - fallos}/{total} OK" + (f"  ({fallos} problemas)" if fallos else ""))
    return 1 if fallos else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(_main())
