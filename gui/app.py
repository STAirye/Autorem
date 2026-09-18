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
gui/app.py - shell: ventana, sidebar, router, construccion desde PANTALLA.

docs/GUI_2.0_plan.md, paso 4 (SS3, SS3.1, SS3.2, SS3.3, SS4). Arranca con
`python -m gui.app` -- autorem.py no se toca hasta el paso 11 del plan.

EL CONTRATO PANTALLA (lo que expone cada modulo de gui/paginas/*.py):

    PANTALLA = {
        "id": "sm_actividades",        # unico, usado por el router
        "programa": "Salud Mental",    # agrupa en el sidebar (registro.ORDEN_PROGRAMAS)
        "titulo": "Actividades",
        "estado": "estable",           # "estable" | "beta" -> badge en el sidebar
        "instrucciones": "...",        # opcional
        "inputs": [
            {"key": "ada", "etiqueta": "...", "multi": True, "obligatorio": True,
             "titulo_dialogo": "...", "on_elegido": fabrica},
            ...
        ],
        # `obligatorio` puede ser un bool, o callable(getters) -> bool cuando
        # depende de OTRO input (SM Actividades, docs/GUI_2.0_plan.md SS6: ADA
        # y Grupal dejan de serlo SOLO en una corrida solo-cuestionarios).
        # `on_elegido` (opcional) es una FACTORY (frame, pagina) -> callback(valor)
        # -- mismo molde que `extras[].construir` -- que corre apenas se elige
        # el archivo, no recien al apretar Procesar (SS5.1 del plan: preview
        # barato de formato/cruce; A05 lo usa para detectar IRIS/Administrativo,
        # SM para el preview de cruce ADA<->Grupal).
        # `ancla_salida` (opcional, un input por pantalla): ESE input fija la
        # carpeta de salida por defecto. Sin el se usa el primer input cargado,
        # que es el orden en que estan ESCRITOS aca -- ver `_resolver_ctx`.
        "mes": True,                   # muestra SelectorMes
        "carpeta_salida": True,        # muestra CarpetaSalida
        "extras": [                    # opcional, ver SS3.1 del plan
            {"despues_de": "ada", "construir": fn, "key": "tabla_dot"},
        ],
        "preparar": None,              # opcional, hilo GUI, ANTES del worker, ver SS3.3
        "correr": correr,              # callable(ctx, log) -> resultado, EN EL WORKER
        "resumen": resumen,            # callable(resultado) -> str para el messagebox
        "al_completar": None,          # opcional, hilo GUI, DESPUES del worker (SS5.1):
                                       # callable(resultado, pagina) -- p.ej. actualizar
                                       # un BannerFuente con formatos.clasificar_fuente,
                                       # que solo se sabe una vez cargado el archivo.
    }

INVARIANTE DURA (SS3.2): nada de Tk vars en el worker. `_resolver_ctx` resuelve
TODOS los getters a un dict plano `ctx` (Path/tuplas/listas, nunca StringVar)
ANTES de lanzar el hilo; `pantalla["correr"]` no debe tocar widgets.

Los `inputs` obligatorios se pintan arriba, los opcionales bajo el separador
(mismo orden visual que autorem.py). Un `extras[].despues_de` = key de un
input posiciona el bloque justo debajo de ese input (p.ej. Dotacion debajo
del ADA); `despues_de: None` lo pinta al final (antes del boton Procesar).

`Pagina.datos` es un dict COMPARTIDO por todas las `Pagina` de una misma
pantalla (construccion, `on_elegido`, `preparar`, `al_completar`): sirve para
pasarse cosas entre esas fases sin variables de modulo. Ver A23/SM: un extra
arma un `widgets.BannerFuente` y lo guarda en `pagina.datos["banner_fuente"]`;
`al_completar` lo recupera y lo actualiza con el resultado de la corrida. El shell
lo siembra con `datos["ruta_inicial"]`: la ruta que Windows pasa como argv[1] al
arrastrar un .xlsx sobre el exe (hoy solo la lee A05).

PAGINAS ESPECIALES (paso 10 del plan, SS4): "Inicio" y "Acerca de" NO son
PANTALLA -- no procesan nada, no tienen `correr`, y por eso no viven en
`gui.registro` (que descubre paginas por ESE contrato) ni se agrupan por
programa. Van aparte en el sidebar, debajo de un separador (maqueta de SS4),
y su modulo expone `construir(frame, app)` en vez del dict `PANTALLA`.
"""

from pathlib import Path

import tkinter.messagebox as messagebox
import customtkinter as ctk

from programas.rem_utils import VERSION, mes_anterior
from gui import widgets, runner
from gui.registro import cargar_registro, programas_en_orden
from gui.paginas import inicio, about

ANCHO_SIDEBAR = 210

# (id, titulo del boton, construir(frame, app), posicion) -- ver nota "PAGINAS
# ESPECIALES" arriba.
#
# `posicion` ANCLA la pagina en el sidebar y es un DATO, no el orden de este tuple:
# "arriba" = fija al tope, sobre todos los grupos de programa; "abajo" = fija al pie,
# bajo todos (feedback del autor, sep-2026). Inicio es el punto de partida y Acerca de
# es el cierre, asi que ninguna de las dos se mueve cuando se suma un programa nuevo a
# `registro.ORDEN_PROGRAMAS` -- que es justo lo que pasaria si la posicion fuera
# "despues de los grupos, en el orden en que estan escritas aca".
PAGINAS_ESPECIALES = (
    ("inicio", "Inicio", inicio.construir, "arriba"),
    ("acerca_de", "Acerca de", about.construir, "abajo"),
)


def _cabecera_sidebar(programa):
    """Encabezado VISUAL del sidebar para `programa` -- feedback del autor
    (sep-2026): "Salud Mental" y "Salud Mental -- Poblacion" son un solo
    programa de salud en dos estados de VALIDACION (CLAUDE.md SS9, matriz de
    programas), no dos secciones del sidebar. `registro.ORDEN_PROGRAMAS` los
    sigue trackeando aparte (asi el roadmap distingue "SM estable" de
    "SM-poblacion en validacion"); esto solo cambia como se AGRUPAN al
    dibujar, nunca el dato de la PANTALLA."""
    return "Salud Mental" if programa.startswith("Salud Mental") else programa


def _grupo_colapsable(barra, titulo):
    """Cabecera de programa CLICKEABLE que colapsa/expande su contenido
    (feedback del autor, sep-2026). Devuelve el frame `contenido` donde el
    caller sigue empacando los botones de pagina -- el estado
    expandido/colapsado es una variable de Python (`estado["expandido"]`),
    NO `winfo_ismapped()`: ese metodo puede devolver `False` para un widget
    recien empacado hasta el primer ciclo de eventos (ya nos mordio una vez
    con `BannerFuente` en un test, ver spike del paso 8), asi que confiar en
    el ESTADO PROPIO evita ese mismo problema aca.

    OJO CON EL ORDEN DE LOS `pack` (bug visual, sep-2026): `pack` apila en ORDEN DE
    LLAMADA, no en orden de creacion. `contenido` se CREA antes que `header` (la
    closure `alternar` lo necesita), pero se tiene que EMPACAR despues -- si no, los
    botones de pagina se dibujan ARRIBA de su propia cabecera. El sintoma era
    desconcertante porque se auto-corregia: colapsar y expandir llama
    `contenido.pack()` de nuevo y ahi si queda al final de la pila, o sea debajo del
    header. Solo el PRIMER dibujo estaba mal."""
    grupo = ctk.CTkFrame(barra, fg_color="transparent")
    grupo.pack(fill="x")
    contenido = ctk.CTkFrame(grupo, fg_color="transparent")
    estado = {"expandido": True}

    def alternar():
        estado["expandido"] = not estado["expandido"]
        if estado["expandido"]:
            contenido.pack(fill="x")
            header.configure(text=f"-  {titulo.upper()}")
        else:
            contenido.pack_forget()
            header.configure(text=f"+  {titulo.upper()}")

    header = ctk.CTkButton(grupo, text=f"-  {titulo.upper()}", anchor="w",
                           fg_color="transparent", text_color=widgets.COLOR_ATENUADO,
                           font=ctk.CTkFont(size=11, weight="bold"), command=alternar)
    header.pack(fill="x", padx=6, pady=(10, 2))
    contenido.pack(fill="x")   # DESPUES del header, a proposito: ver el docstring
    return contenido


class Pagina:
    """Lo que un `extras[].construir(frame, pagina)` (o un `on_elegido` de
    input, o `al_completar`) puede necesitar de su propia pagina (SS3.1 del
    plan): leer OTRO input ya elegido, el mes, escribir al mismo log / abrir
    dialogos sobre la misma ventana, y un scratch COMPARTIDO (`datos`) para
    pasarse cosas entre construccion y post-corrida (p.ej. un BannerFuente
    que arma un extra y actualiza `al_completar`, ver A23/SM)."""

    def __init__(self, app, getters, get_mes_celda, log, datos):
        self.root = app
        self._getters = getters
        self._get_mes_celda = get_mes_celda   # celda mutable: ver nota en _construir_pagina
        self.log = log
        self.datos = datos   # dict COMPARTIDO por TODAS las Pagina de esta pantalla

    def get(self, key):
        """Valor CRUDO (string o list[str]) del getter de ese input -- el
        mismo que ve `_resolver_ctx`, sin validar todavia (la pagina puede
        llamar a esto ANTES de apretar Procesar, p.ej. 'Precargar dotacion')."""
        return self._getters[key]()

    def mes(self):
        """(anio, mes) del SelectorMes de la pagina, o None si no tiene uno
        (pantalla["mes"] es False) o si lo tecleado no son numeros.

        Resuelto PEREZOSAMENTE (celda mutable, no el getter ya resuelto): un
        extra puede recibir su `Pagina` ANTES de que el SelectorMes exista
        todavia (se pinta despues de los inputs, un extra puede ir pegado a
        uno temprano) -- lo que importa es que funcione cuando la pagina
        LLAME a esto de verdad, dentro de un boton, tras un click real, y
        para entonces la pagina ya esta completa."""
        getter = self._get_mes_celda[0]
        return getter() if getter else None


def _resolver_ctx(pantalla, getters, get_mes, get_carpeta):
    """Valida los inputs/mes/carpeta y arma el `ctx` PLANO que ve el worker
    (SS3.2). Funcion libre (sin `self`) para poder testearla con getters
    falsos, sin ventana real (mismo criterio que SS11 del plan para
    `valores_iniciales` de dotacion). Devuelve None si algo no valida (ya
    avisado con messagebox)."""
    ctx = {}
    inputs = pantalla.get("inputs", [])
    for inp in inputs:
        valor = getters[inp["key"]]()
        obligatorio = inp.get("obligatorio", True)
        if callable(obligatorio):
            # SM Actividades lo necesita (docs/GUI_2.0_plan.md SS6): ADA/Grupal
            # dejan de ser obligatorios SOLO si es una corrida solo-cuestionarios
            # (checkbox 'Incluir cuestionarios' marcado, con archivos, y ni ADA
            # ni Grupal elegidos) -- una condicion que depende de OTRO input, no
            # de esta pantalla en abstracto.
            obligatorio = obligatorio(getters)
        if inp.get("multi"):
            if obligatorio and not valor:
                # `motivo_obligatorio` (opcional): el POR QUE que el aviso a mano de
                # autorem.py traia y el generico perdia (p.ej. "de ahi salen A06 grupal,
                # A19a grupal y A27"). Sin el, solo la etiqueta.
                messagebox.showwarning(
                    "Falta un archivo",
                    f"Carga al menos un archivo: {inp['etiqueta']}"
                    + ("\n\n" + inp["motivo_obligatorio"] if inp.get("motivo_obligatorio") else ""))
                return None
            ctx[inp["key"]] = [Path(v) for v in valor]
        else:
            if obligatorio:
                p = runner.valida_ruta(valor, messagebox)
                if p is None:
                    return None
                ctx[inp["key"]] = p
            else:
                limpia = runner.limpiar_ruta(valor)   # comillas de 'Copiar como ruta'
                ctx[inp["key"]] = Path(limpia) if limpia else None

    if get_mes:
        # valida_mes y no solo `is None`: el Spinbox acota sus flechas, no lo tecleado
        # (ver el porque completo en runner.valida_mes).
        mes = runner.valida_mes(get_mes(), messagebox)
        if mes is None:
            return None
        ctx["mes"] = mes

    for extra in pantalla.get("extras", []):
        key = extra.get("key")
        if key and key in getters:
            ctx[key] = getters[key]()

    if get_carpeta:
        # Defecto = carpeta del input que la pagina declare como ANCLA
        # (`ancla_salida`) y, si no declara ninguno, la del primer input CARGADO
        # (CLAUDE.md SS2: las salidas llevan RUT, van junto a los exports). Sin
        # ninguno (p.ej. SM solo-cuestionarios), la pagina lo resuelve con
        # `carpeta_defecto(ctx)`; nunca cae al cwd si hay archivos.
        #
        # POR QUE el ancla es un DATO y no "el primero de la lista" (sep-2026): el
        # primero de la lista es orden de ESCRITURA, y ahi ya se perdio una vez.
        # `_tab_beta` guardaba junto al INSCRITOS (`defecto=entrada.parent`), que es
        # el snapshot del mes; al portarla, Poblacion declara sus inputs en el orden
        # NUMERADO de las instrucciones (1. Formulario historico, 2. ADA, 3.
        # Inscritos), asi que la salida se fue en silencio a la carpeta del historico
        # multi-anio -- que es justo la que el usuario tiene archivada aparte.
        anclas = [i for i in inputs if i.get("ancla_salida")]
        defecto = None
        for inp in anclas + [i for i in inputs if not i.get("ancla_salida")]:
            v = ctx.get(inp["key"])
            v = v[0] if isinstance(v, list) and v else v
            if isinstance(v, Path):
                defecto = v.parent
                break
        if defecto is None and pantalla.get("carpeta_defecto"):
            defecto = pantalla["carpeta_defecto"](ctx)
        carpeta = runner.valida_carpeta(get_carpeta(), messagebox, defecto=defecto)
        if carpeta is None:
            return None
        ctx["carpeta"] = carpeta

    return ctx


class App(ctk.CTk):
    """Ventana principal: sidebar agrupado por programa + area de contenido
    que intercambia frames por `tkraise` (SS4 del plan: construccion PEREZOSA,
    una pagina se arma recien la primera vez que se visita).

    `registro=None` -> se descubre via `gui.registro.cargar_registro()`
    (comportamiento real). Pasar una lista propia sirve para probar el shell
    con una PANTALLA de mentira sin tener que dejarla en gui/paginas/."""

    def __init__(self, registro=None, ruta_inicial=""):
        super().__init__()
        self.title(f"autoREM {VERSION}")
        # Ancho por defecto (feedback del autor, sep-2026: 1000 quedaba
        # estrecho contra las instrucciones/etiquetas largas de las paginas).
        self.geometry("1180x820")
        self.minsize(980, 680)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.registro = registro if registro is not None else cargar_registro()
        # Ruta ARRASTRADA sobre el exe (Windows la pasa como argv[1]; ver
        # autorem.main). Llega a la pagina por `Pagina.datos['ruta_inicial']`: es el
        # unico canal que ya comparten todas, y solo A05 la usa hoy (era el
        # `ruta_inicial` de _tab_a05 en la GUI 1.x -- sin esto el exe perderia el
        # arrastrar-y-soltar al migrar).
        self.ruta_inicial = (ruta_inicial or "").strip()
        self._frames = {}         # id -> CTkFrame ya construido (perezoso)
        self._logs = {}           # id -> log(msg) (existe recien tras construir la pagina)
        self._botones_sidebar = {}
        # Corridas con el worker vivo (todas las paginas): ver `_al_cerrar`.
        self._corridas = 0
        self.protocol("WM_DELETE_WINDOW", self._al_cerrar)

        self._construir_sidebar()

        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.grid(row=0, column=1, sticky="nsew", padx=(4, 0))
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)

        self.mostrar("inicio")

    # -- Sidebar / router ------------------------------------------------
    def _construir_sidebar(self):
        barra = ctk.CTkScrollableFrame(self, width=ANCHO_SIDEBAR,
                                       label_text=f"autoREM {VERSION}")
        barra.grid(row=0, column=0, sticky="nsw")

        def separador(pady=(12, 4)):
            ctk.CTkFrame(barra, height=1, fg_color=widgets.COLOR_ATENUADO
                        ).pack(fill="x", padx=6, pady=pady)

        def boton_especial(pid, titulo):
            btn = ctk.CTkButton(barra, text=titulo, anchor="w", fg_color="transparent",
                                text_color=widgets.COLOR_TEXTO_TRANSPARENTE,
                                command=lambda pid=pid: self.mostrar(pid))
            btn.pack(fill="x", padx=6, pady=1)
            self._botones_sidebar[pid] = btn

        # Las especiales ANCLADAS arriba (Inicio), antes de cualquier grupo de
        # programa. Ver la nota de PAGINAS_ESPECIALES: la posicion es un dato, no el
        # orden en que este bucle las encuentra.
        for pid, titulo, _construir, posicion in PAGINAS_ESPECIALES:
            if posicion == "arriba":
                boton_especial(pid, titulo)
        separador(pady=(6, 0))

        # Cabecera VISUAL, no `pantalla["programa"]` (feedback del autor,
        # sep-2026): "Salud Mental" y "Salud Mental -- Poblacion" son un
        # solo programa de salud en dos estados de VALIDACION (CLAUDE.md
        # SS9, matriz de programas) -- una sola seccion en el sidebar, sin
        # tocar `registro.ORDEN_PROGRAMAS` (que los sigue trackeando
        # aparte, y de donde sale el orden real de iteracion aca abajo).
        cabecera_actual = None
        contenido = None
        for programa in programas_en_orden(self.registro):
            cabecera = _cabecera_sidebar(programa)
            if cabecera != cabecera_actual:
                cabecera_actual = cabecera
                contenido = _grupo_colapsable(barra, cabecera)
            for pantalla in self.registro:
                if pantalla["programa"] != programa:
                    continue
                texto = pantalla["titulo"]
                if pantalla.get("estado") == "beta":
                    texto += "  [BETA]"
                btn = ctk.CTkButton(contenido, text=texto, anchor="w", fg_color="transparent",
                                    text_color=widgets.COLOR_TEXTO_TRANSPARENTE,
                                    command=lambda pid=pantalla["id"]: self.mostrar(pid))
                btn.pack(fill="x", padx=6, pady=1)
                self._botones_sidebar[pantalla["id"]] = btn

        # Las especiales ANCLADAS abajo (Acerca de), debajo de todos los grupos.
        separador()
        for pid, titulo, _construir, posicion in PAGINAS_ESPECIALES:
            if posicion == "abajo":
                boton_especial(pid, titulo)

        # Toggle claro/oscuro (SS4 del plan): al final de todo, abajo
        # (feedback del autor, sep-2026). Queda DEBAJO de "Acerca de" porque no es una
        # pagina sino un control de la ventana; "Acerca de" sigue siendo la ultima
        # pagina del sidebar. El modo oscuro es "gratis" en CTk
        # (`set_appearance_mode`), pero el plan pide auditar antes los
        # colores hardcodeados que venian del Tk actual -- ver
        # widgets.COLOR_AVISO / COLOR_ATENUADO / Reloj, ya con tupla
        # (claro, oscuro) o resueltos a mano por modo.
        separador()
        switch_oscuro = ctk.CTkSwitch(barra, text="Modo oscuro",
                                      command=self._alternar_tema)
        if ctk.get_appearance_mode() == "Dark":
            switch_oscuro.select()
        switch_oscuro.pack(anchor="w", padx=6, pady=(2, 10))

    def _al_cerrar(self):
        """La X de la ventana. El worker es un hilo `daemon`: al cerrar, el proceso
        termina y lo mata donde este, aunque sea escribiendo el .xlsx. Sin corridas
        vivas cierra de una; con alguna, pregunta (con «No» por defecto). No es un
        timeout: esperar a que termine sola puede ser un minuto con la ventana
        congelada, y matarla sin avisar es perder la corrida sin saberlo. Lo que un
        corte deje a medias es un `… .escribiendo.xlsx` (rem_utils.escribir_atomico),
        nunca un resultado roto con nombre de resultado."""
        if self._corridas and not messagebox.askyesno(
                "Hay una corrida en curso",
                "autoREM todavía está procesando. Si cierras ahora, la corrida se corta "
                "y su resultado NO se guarda (a lo más queda un «….escribiendo.xlsx» a "
                "medio escribir, que puedes borrar).\n\n¿Cerrar igual?",
                icon="warning", default="no"):
            return
        self.destroy()

    def _alternar_tema(self):
        nuevo = "dark" if ctk.get_appearance_mode() == "Light" else "light"
        ctk.set_appearance_mode(nuevo)

    def mostrar(self, pantalla_id):
        """Router: construye la pagina la PRIMERA vez (perezoso) y la trae al
        frente. Volver a una pagina ya visitada conserva sus rutas elegidas y
        el log de la corrida anterior (no se destruye nada). Las PAGINAS
        ESPECIALES (Inicio/Acerca de, ver modulo) no estan en `self.registro`
        -- se resuelven aparte, contra `PAGINAS_ESPECIALES`.

        `.lift()`, NO `.tkraise()` (bug encontrado a mano, sep-2026): una
        pagina es un CTkScrollableFrame, y ESE widget sobreescribe
        `grid()`/`pack()`/`place()`/`lift()` para operar sobre
        `self._parent_frame` (el contenedor real del scroll+canvas) -- pero
        NO sobreescribe `tkraise` (alias de `lift` fijado en la clase base
        `tkinter.Misc`, asi que sigue apuntando al `lift` ORIGINAL). Llamar
        `.tkraise()` reordena el frame de CONTENIDO interno de la pagina
        (invisible, vive dentro de su propio canvas), no el `_parent_frame`
        que de verdad esta gridado en `self.contenedor` -- asi que NO
        cambia que pagina se ve. Efecto: la PRIMERA visita a cada pagina se
        veia bien (recien gridada, Tk la deja arriba de la pila por
        defecto), pero volver a una pagina YA construida quedaba pegada en
        la ultima (verificado con `winfo_children()`, que SI refleja el
        orden de la pila, antes/despues de cada llamada)."""
        if pantalla_id not in self._frames:
            especial = next((c for pid, _t, c, _pos in PAGINAS_ESPECIALES
                             if pid == pantalla_id), None)
            if especial is not None:
                frame = ctk.CTkScrollableFrame(self.contenedor)
                frame.grid(row=0, column=0, sticky="nsew")
                especial(frame, self)
                self._frames[pantalla_id] = frame
            else:
                pantalla = next(p for p in self.registro if p["id"] == pantalla_id)
                self._frames[pantalla_id] = self._construir_pagina(pantalla)
        self._frames[pantalla_id].lift()
        for pid, btn in self._botones_sidebar.items():
            btn.configure(fg_color=("gray75", "gray25") if pid == pantalla_id else "transparent")

    # -- Construccion de una pagina desde su PANTALLA --------------------
    def _construir_pagina(self, pantalla):
        frame = ctk.CTkScrollableFrame(self.contenedor)
        frame.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(frame, text=pantalla["titulo"],
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(0, 6))
        if pantalla.get("instrucciones"):
            caja = widgets.caja_titulada(frame, "Instrucciones")
            caja.pack(fill="x", pady=(0, 8))
            widgets.etiqueta_envolvente(caja, pantalla["instrucciones"]
                                       ).pack(fill="x", padx=8, pady=(2, 8))
        widgets.aviso_sin_modificar(frame)

        getters = {}
        get_mes = [None]   # celda mutable: un extra "despues_de" un input puede
                           # necesitar pagina.mes() antes de que el SelectorMes
                           # exista (se pinta despues de los inputs, SS4 del plan)
        datos = {"ruta_inicial": self.ruta_inicial}   # scratch COMPARTIDO por las Pagina
                     # (p.ej. un BannerFuente que arma un extra y usa `al_completar`)

        def pagina_ctx():
            return Pagina(self, getters, get_mes, self._log_de(pantalla["id"]), datos)

        def pintar_extras(despues_de):
            for extra in pantalla.get("extras", []):
                if extra.get("despues_de") != despues_de:
                    continue
                valor = extra["construir"](frame, pagina_ctx())
                if valor is not None:
                    if "key" not in extra:
                        # Fail loud (CLAUDE.md SS_fail-loud): un extra que devuelve
                        # datos y no dice donde van en ctx es un bug de config de
                        # la pagina, no un caso de usuario -- mejor reventar ahora
                        # que perder el valor en silencio.
                        raise ValueError(
                            f"extras de '{pantalla['id']}' (despues_de={despues_de!r}): "
                            f"construir() devolvio un valor pero el extra no declara 'key'")
                    getters[extra["key"]] = valor

        inputs = pantalla.get("inputs", [])
        obligatorios = [i for i in inputs if i.get("obligatorio", True)]
        opcionales = [i for i in inputs if not i.get("obligatorio", True)]

        def pintar_input(inp):
            # `on_elegido` (opcional) es una FACTORY -- (frame, pagina) -> callback(valor)
            # -- mismo molde que `extras[].construir`. La usa el preview de fuente/cruce
            # (SS5.1 del plan): correr algo barato apenas se elige el archivo, no recien
            # al apretar Procesar. La fila se pinta ANTES de llamar la factory: un
            # BannerFuente que arme se ancla a la fila y aparece justo debajo de ella.
            cb = {}

            def al_elegir(valor, inp=inp):
                # El shell se engancha SIEMPRE, aunque la pagina no declare
                # `on_elegido`: cambiar CUALQUIER input invalida el banner de FUENTE,
                # que lo pinta `al_completar` con el resultado de la corrida ANTERIOR.
                # Sin esto, elegir otro archivo dejaba el banner verde ("A/D/A de IRIS
                # completo") al lado de un export parcial recien cargado -- un color
                # que afirma algo falso (SS5.1 del plan, regla 1). El input al que
                # pertenece el banner (A23 'atenciones') no tiene `on_elegido` propio,
                # asi que el hook no puede vivir en la pagina.
                banner = datos.get("banner_fuente")
                if banner is not None:
                    banner.ocultar()
                if "f" in cb:
                    cb["f"](valor)

            if inp.get("multi"):
                getters[inp["key"]] = widgets.fila_archivos(
                    frame, inp["etiqueta"], inp.get("titulo_dialogo", inp["etiqueta"]),
                    on_elegido=al_elegir)
            else:
                var = ctk.StringVar()
                widgets.fila_archivo(frame, var, inp.get("titulo_dialogo", inp["etiqueta"]),
                                     etiqueta=inp["etiqueta"], on_elegido=al_elegir)
                getters[inp["key"]] = var.get
            if inp.get("on_elegido"):
                cb["f"] = inp["on_elegido"](frame, pagina_ctx())

        for inp in obligatorios:
            pintar_input(inp)
            pintar_extras(inp["key"])

        if opcionales:
            widgets.separador_opcionales(frame)
            for inp in opcionales:
                pintar_input(inp)
                pintar_extras(inp["key"])

        # Carpeta ANTES que mes: mismo orden visual que traian A23/SM/BETA en
        # autorem.py (orden puramente cosmetico, sin efecto funcional).
        get_carpeta = widgets.fila_carpeta_salida(frame) if pantalla.get("carpeta_salida") else None

        if pantalla.get("mes"):
            get_mes[0] = widgets.selector_mes(frame, mes_anterior())

        pintar_extras(None)   # los que van "al final", antes del boton Procesar

        log, limpiar = widgets.crear_log(frame, self)
        self._logs[pantalla["id"]] = log

        barra_botones = ctk.CTkFrame(frame, fg_color="transparent")
        barra_botones.pack(fill="x")
        btn = ctk.CTkButton(barra_botones, text="Procesar")
        btn.pack(side="left")

        def on_procesar():
            limpiar()
            # El banner de fuente se apaga junto con el log y por el mismo motivo:
            # los dos describen la corrida ANTERIOR. Si esta falla, `al_completar` no
            # corre y el banner quedaba afirmando el veredicto de fuente de la corrida
            # pasada como si fuera el de esta. Invariante: el banner solo dice algo
            # cuando hay una corrida terminada que lo respalde.
            banner_previo = datos.get("banner_fuente")
            if banner_previo is not None:
                banner_previo.ocultar()
            ctx = _resolver_ctx(pantalla, getters, get_mes[0], get_carpeta)
            if ctx is None:
                return
            if pantalla.get("preparar"):
                # El boton se deshabilita YA, antes de `preparar`, y no recien en
                # `correr_con_reloj`: `preparar` corre en el hilo GUI y puede bombear
                # eventos (el dialogo de Dotacion del SM abre un Toplevel modal), asi
                # que un segundo click en Procesar ya encolado se despachaba AHI y
                # reentraba en esta funcion -> dos corridas escribiendo el mismo
                # archivo de salida. `correr_con_reloj` lo deshabilita de nuevo (es
                # idempotente) y lo rehabilita al terminar el worker.
                btn.configure(state="disabled")
                try:
                    ctx = pantalla["preparar"](ctx, pagina_ctx())
                except Exception as e:   # noqa: BLE001  (hilo GUI: sin esto Tk se lo traga)
                    ctx = None
                    runner.manejar_error(e, log, messagebox)
                runner.avisar_cache(messagebox)   # `preparar` carga/guarda la dotacion
                if ctx is None:   # abortado (ADA ilegible, mes vacio) o reventado
                    btn.configure(state="normal")   # el usuario tiene que poder reintentar
                    return

            # Los inputs TAL COMO estaban al arrancar. Durante la corrida solo se
            # deshabilita Procesar: el usuario puede elegir otro archivo mientras el
            # worker trabaja, y `al_completar` pintaba entonces el veredicto de fuente
            # de ESTA corrida al lado de un archivo que ya no es el suyo (banner verde
            # «IRIS completo» junto a un Monitoreo recien elegido) -- mismo patron que
            # runner.Canal. Se compara el valor CRUDO de cada getter, asi tambien cuenta
            # una ruta tecleada, que no dispara `al_elegir`.
            inicio = {inp["key"]: getters[inp["key"]]() for inp in inputs}

            def trabajo(log_hilo):
                return pantalla["correr"](ctx, log_hilo)

            def al_terminar(res, err):
                self._corridas -= 1   # primero: el worker ya termino, pase lo que pase abajo
                if err is not None:
                    runner.manejar_error(err, log, messagebox)
                    runner.avisar_cache(messagebox)
                    return
                # El worker puede haber leido/guardado un caché (estamentos, dotacion).
                runner.avisar_cache(messagebox)
                cambiados = [k for k, v in inicio.items() if getters[k]() != v]
                try:
                    if cambiados and pantalla.get("al_completar"):
                        banner = datos.get("banner_fuente")
                        if banner is not None:
                            banner.ocultar()
                        log("[fuente] cambiaste un archivo mientras corría: no pinto el "
                            "veredicto de fuente, describiría archivos que ya no son los "
                            "elegidos. El resultado SÍ es de los archivos con que partió.")
                    elif pantalla.get("al_completar"):
                        # Hilo GUI, simetrico de `preparar` pero DESPUES del worker
                        # (SS5.1 del plan): p.ej. actualizar un BannerFuente con
                        # formatos.clasificar_fuente, que solo se sabe una vez que
                        # el worker termino de cargar y resolver el archivo.
                        pantalla["al_completar"](res, pagina_ctx())
                    texto = pantalla["resumen"](res) if pantalla.get("resumen") else "Listo."
                except Exception as e:   # noqa: BLE001  (hilo GUI: sin esto Tk se lo traga)
                    runner.manejar_error(e, log, messagebox)
                    return
                log(""); log("OK " + texto.replace("\n", " | "))
                carpeta = ctx.get("carpeta")
                if carpeta and messagebox.askyesno(
                        "Listo", texto + "\n\n¿Abrir la carpeta del resultado?"):
                    runner.abrir_carpeta(carpeta)

            self._corridas += 1
            runner.correr_con_reloj(self, barra_botones, btn, log, trabajo, al_terminar)

        btn.configure(command=on_procesar)
        return frame

    def _log_de(self, pantalla_id):
        """Log de una pagina, resuelto PEREZOSAMENTE: un extra puede recibir
        `pagina.log` antes de que `widgets.crear_log` exista todavia (se pinta
        al final de `_construir_pagina`); para cuando alguien lo LLAME de
        verdad (dentro de un boton, tras un click real) la pagina ya esta
        completa."""
        return lambda msg="": self._logs[pantalla_id](msg)


def lanzar(ruta_inicial=""):
    ctk.set_appearance_mode("light")
    App(ruta_inicial=ruta_inicial).mainloop()


if __name__ == "__main__":
    lanzar()
