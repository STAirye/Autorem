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
gui/paginas/sm.py - REM SM Actividades, la pagina mas pesada (paso 7 del plan).

Portada de autorem.py._tab_sm sin tocar la logica (docs/GUI_2.0_plan.md SS7):
ejercita TODO a la vez -- `extras` con posicion (Dotacion debajo del ADA/Grupal,
igual que el ejemplo del propio SS3 del plan), `preparar` (SS3.3, el dialogo
de Dotacion bloquea la GUI a proposito), el checkbox de cuestionarios A03·D.3,
la relajacion de obligatorios para una corrida solo-cuestionarios (SS6), y el
Trabajo Perdido corriendo en el mismo worker con su propio try.

LA REGRESION QUE HAY QUE RESOLVER (SS6 del plan): la vieja pestana A03
standalone permitia tabular SOLO los cuestionarios, sin ADA ni Grupal, y
DESAPARECE en la 2.0 (CLAUDE.md SS12). Ojo con el tiempo verbal: `_tab_a03`
TODAVIA existe en autorem.py (esta definida y montada en `lanzar_gui`, que es
la GUI que sigue corriendo el exe) -- se borra en el paso 11 del plan, cuando
autorem.py deje de armar el notebook 1.x. Hasta entonces las dos conviven, asi
que un cambio aca no la reemplaza todavia.

Esta pagina reproduce esa capacidad: si 'Incluir cuestionarios'
esta marcado Y no hay ADA ni Grupal, corre SOLO el A03 (con el bloque de
Estamentos que igual se necesita para el perfil Administrativo del
screening) y se salta el bloque de Actividades Y la fase `preparar` de
Dotacion (que necesita el ADA cargado; una corrida solo-cuestionarios no lo
tiene).

BANNERS DE FUENTE (SS5.1 del plan, agregado tras migrar A05):
  - Preview de CRUCE en ADA/Grupal: barato (`formatos.parece_reporte` solo
    cuenta firmas en el encabezado), asi que corre al ELEGIR el archivo via
    `on_elegido` -- antes de apretar Procesar, no despues.
  - Banner de fuente (`formatos.clasificar_fuente`, plena/parcial/cambiada):
    corre DENTRO de `cargar_atenciones`, en el worker -- solo se sabe DESPUES
    de Procesar, via `al_completar`. Misma asimetria que A23."""

from pathlib import Path

import customtkinter as ctk

from gui import widgets, dialogos, runner

instrucciones = (
    "Tabula las ACTIVIDADES de Salud Mental (estadística, sin juicio clínico) -> tablas\n"
    "listas para copiar-pegar al template SA_26. Cubre A04·A24, A06·A.1 (controles +\n"
    "psicosocial grupal), A19a·A.3 (consejerías familiares SM/demencia), A26 (VDI SM),\n"
    "A27 (educación prev. SM) y A32·F (acciones/controles remotos SM).\n"
    "1.  Atenciones / Diagnósticos / Actividades (ADA, IRIS)  ->  casi todas las casillas.\n"
    "2.  Atenciones Grupales  ->  A06 psicosocial grupal, A19a grupal y A27 (educación).\n"
    "3.  Inscritos y Adscritos (opcional, ENORME)  ->  solo para el flag TRANS (género).\n"
    "4.  Maestro de Actividades (opcional)  ->  clasifica el reporte extra de TRABAJO PERDIDO:\n"
    "     actividades con 'mental'/'demencia' que NO tributan al REM + qué funcionario las registra.\n"
    "El export puede venir del AÑO COMPLETO: se filtra el mes que elijas (por FECHA ATENCIÓN,\n"
    "hacia atrás desde el último día del mes). ADA cuenta por atención; grupal por asistencia.\n"
    "Para el flag GESTANTE se usa una ventana de 3 MESES -> carga el ADA de los últimos 3 meses.\n"
    "\n"
    "¿Solo necesitas los cuestionarios A03·D.3? Marca la casilla de más abajo y NO cargues\n"
    "ni ADA ni Grupal: corre solo esa tabla (reemplaza a la vieja pestaña A03 standalone)."
)


def _header_rapido(ruta, max_scan=40):
    """Header CRUDO (lista de celdas) de la primera fila con pinta de
    encabezado, leyendo SOLO las primeras `max_scan` filas -- el preview de
    cruce (SS5.1 del plan) no necesita el archivo completo, y un ADA de un
    anio puede ser grande. El criterio es `rem_utils.indice_encabezado`, el MISMO
    de `leer_xlsx` (antes era una copia a mano: si el loader cambiaba de criterio,
    el preview leia otro encabezado que la corrida). `primeras_filas` lee con
    `abrir_xlsx_ro`: un `read_only=True` pelado acota la lectura a la <dimension>
    del .xlsx, y con la etiqueta rota el encabezado llegaba mocho y el cruce ADA<->
    Grupal no se acusaba nunca."""
    from programas.rem_utils import primeras_filas, indice_encabezado
    filas = primeras_filas(ruta, max_scan)
    return list(filas[indice_encabezado(filas, max_scan=max_scan)]) if filas else []


def _chequeo_cruce(frame, pagina, espera):
    """Factory `on_elegido` para el input `espera` ('ada'|'grupal'): preview
    BARATO de cruce (SS5.1 del plan) -- lee solo el encabezado, EN UN HILO
    (no bloquea la ventana), y pinta un BannerFuente rojo si el archivo
    parece el OTRO reporte del par. Empate o sin evidencia -> no se acusa
    (`formatos.parece_reporte`: nunca un falso positivo sin evidencia)."""
    banner = widgets.BannerFuente(frame)
    nombres = {"ada": "Atenciones/Diag/Activ (ADA)", "grupal": "Atenciones Grupales"}
    # Solo pinta el hilo de la ULTIMA eleccion (ver runner.Canal): sin esto, el
    # veredicto de un archivo ya reemplazado -- o ya quitado -- quedaba pintado.
    canal = runner.Canal()

    def on_elegido(archivos):
        if not archivos:
            canal.invalidar()   # un hilo en vuelo no puede volver a encender el banner
            banner.ocultar()
            return

        def trabajo():
            from programas import formatos
            return formatos.parece_reporte(_header_rapido(archivos[0]))

        def _aplicar(otro):
            if otro is None or otro == espera:
                banner.ocultar()
            else:
                banner.mostrar("no_reconocido",
                    f"Esto parece el reporte de {nombres[otro]}, no el que va en esta "
                    f"casilla ({nombres[espera]}). Revisa que no hayas cruzado los archivos.")

        # runner.en_hilo y NO frame.after(0,...) desde el hilo: Tk.after no es
        # thread-safe (ver la nota en runner.en_hilo). Un archivo raro revienta en
        # `trabajo` -> llega como `err` y NO se acusa nada (nunca un falso positivo).
        runner.en_hilo(frame, trabajo,
                       lambda otro, err: _aplicar(otro if err is None else None),
                       canal=canal)
    return on_elegido


def al_completar(res, pagina):
    widgets.pintar_banner_fuente(pagina, res.get("E"))   # E None en solo_a03: no hubo ADA


def _es_solo_a03(a03, ada, grupal):
    """Corrida solo-cuestionarios: checkbox marcado, con archivos, y ni ADA ni Grupal
    (SS6 del plan). Fuente UNICA para la validacion y para preparar."""
    return bool(a03["incluir"] and a03["instrumentos"] and not ada and not grupal)


def _ada_grupal_obligatorio(getters):
    """ADA y Grupal dejan de ser obligatorios SOLO si es una corrida
    solo-cuestionarios de verdad: checkbox marcado, con archivos, y NINGUNO
    de los dos elegido (SS6 del plan). Si el checkbox esta marcado pero el
    usuario tambien cargo ADA/Grupal, se hace la corrida COMPLETA de
    siempre -- la casilla no reemplaza el input, solo lo completa."""
    return not _es_solo_a03(getters["a03"](), getters["ada"](), getters["grupal"]())


def bloque_dotacion_sm(frame, pagina):
    import modulos.rem_sm_actividades as smact
    dialogos.bloque_dotacion(frame, "sm", get_ada=lambda: pagina.get("ada"),
                             get_mes=pagina.mes, log=pagina.log, mask=smact.mask_tributa_ada)
    return None   # Dotacion vive en `preparar` (SS3.3), no aporta nada a ctx


def bloque_cuestionarios(frame, pagina):
    """Checkbox 'Incluir cuestionarios?' que despliega los 3 slots A03·D.3
    (PSC/PSC-Y/GHQ-12, igual que la vieja pestana standalone) + el bloque de
    Estamentos (lo necesita el perfil Administrativo del screening -- SS6 del
    plan: 'el bloque de estamentos tambien se mueve con el A03')."""
    var_incluir = ctk.BooleanVar(value=False)
    chk = ctk.CTkCheckBox(frame, text="¿Incluir cuestionarios?  (genera además la tabla A03·D.3)",
                          variable=var_incluir, command=lambda: _toggle())
    chk.pack(anchor="w", pady=(6, 0))

    caja = widgets.caja_titulada(frame, "Cuestionarios A03·D.3 (PSC / PSC-Y / GHQ-12)")

    def _toggle():
        if var_incluir.get():
            caja.pack(fill="x", pady=(2, 4), after=chk)   # sin after= cae bajo Procesar
        else:
            caja.pack_forget()

    slots = {
        "PSC": widgets.fila_archivos(caja, "PSC (padres, 5-9):", "Cuestionario para Padres PSC"),
        "PSC-Y": widgets.fila_archivos(caja, "PSC-Y (10-14):", "Cuestionario para Adolescentes (PSC-Y)"),
        "GHQ-12": widgets.fila_archivos(caja, "GHQ-12 (Goldberg, 15+):", "Cuestionario de Salud de Goldberg"),
    }
    get_est_ruta = dialogos.bloque_estamentos(caja)

    def get_instrumentos():
        out = {}
        for inst, getf in slots.items():
            fs = getf()
            if fs:
                out[inst] = fs[0]
        return out

    def get():
        return {"incluir": var_incluir.get(), "instrumentos": get_instrumentos(),
               "est_ruta": get_est_ruta()}
    return get


def preparar(ctx, pagina):
    import tkinter.messagebox as messagebox
    import modulos.rem_sm_actividades as smact
    a03 = ctx["a03"]
    # 'Utilizacion de Cupos' es opcional, pero si se escribio una ruta tiene que
    # existir: se valida ACA, antes del worker. Sin esto una ruta mal tecleada
    # recien reventaba al final de la corrida, con SM y TP ya escritos y la tabla
    # A03 perdida en `fallo_a03`.
    if a03["incluir"] and a03["instrumentos"] and a03["est_ruta"]:
        if runner.valida_ruta(a03["est_ruta"], messagebox) is None:
            return None
    ctx["solo_a03"] = _es_solo_a03(a03, ctx["ada"], ctx["grupal"])
    if ctx["solo_a03"]:
        ctx["d"] = None
        ctx["tabla_dot"] = None
        return ctx
    # Dotacion (docs/dotacion_externos_plan.md SS3.3): el dialogo usa Tk ->
    # tiene que correr ACA, en el hilo GUI, ANTES del worker. El ADA se carga
    # y filtra por mes ACA (una vez) y se pasa `d` ya listo al worker en vez
    # de releerlo -- "Esto BLOQUEA la GUI y no hay como evitarlo" (comentario
    # original, sigue siendo cierto tal cual).
    d, tabla_dot = dialogos.dotacion_ada(pagina.root, "sm", ctx["ada"], ctx["mes"], pagina.log,
                                         messagebox, mask=smact.mask_tributa_ada)
    if d is None:
        return None
    ctx["d"] = d
    ctx["tabla_dot"] = tabla_dot
    return ctx


def correr(ctx, log):
    import modulos.rem_sm_actividades as smact
    import modulos.rem_a03_d3_instrumentos as screening
    import programas.estamentos as estam
    from gui.runner import slim_por_defecto
    from programas.rem_utils import rutas_libres, escribir_atomico

    y, m = ctx["mes"]
    carpeta = ctx["carpeta"]
    a03 = ctx["a03"]
    res = {"mes": (y, m), "solo_a03": ctx["solo_a03"], "salida": None,
           "salida_a03": None, "n_tp": None, "n_a03": None, "por_inst_a03": None,
           "E": None, "fallo_tp": None, "fallo_a03": None, "avisos_a03": []}

    # Los nombres de TODA la corrida se resuelven juntos, antes de escribir nada: si
    # alguno ya existe, todos llevan el mismo `(n)` (ver rem_utils.rutas_libres).
    salidas = {}
    if not ctx["solo_a03"]:
        salidas["sm"] = carpeta / f"REM_SM_actividades_{y}_{m:02d}.xlsx"
        salidas["tp"] = carpeta / f"REM_SM_trabajo_perdido_{y}_{m:02d}.xlsx"
    if a03["incluir"] and a03["instrumentos"]:
        salidas["a03"] = carpeta / f"REM_A03_D3_{y}_{m:02d}.xlsx"
    salidas = dict(zip(salidas, rutas_libres(*salidas.values())))

    if not ctx["solo_a03"]:
        salida, salida_tp = salidas["sm"], salidas["tp"]
        inscritos = ctx["inscritos"][0] if ctx["inscritos"] else None
        multiprofesional = ctx["multiprofesional"][0] if ctx["multiprofesional"] else None
        maestro = ctx["maestro"][0] if ctx["maestro"] else slim_por_defecto()
        if ctx["maestro"]:
            # Un Maestro cargado a mano que no sirve se detecta ANTES de escribir nada: la
            # app pregunta si seguir sin el (con el slim embebido). El Trabajo Perdido
            # tiene su propio try, que lo habria dejado en un «no se generó».
            from programas.rem_utils import cargar_maestro, opcional
            with opcional("maestro"):
                cargar_maestro(maestro)

        E = smact.procesar(ctx["ada"], grupal=ctx["grupal"], inscritos=inscritos,
                           multiprofesional=multiprofesional, mes=(y, m), log=log,
                           d=ctx["d"], dotacion_tabla=ctx["tabla_dot"])
        E.attrs.setdefault("avisos", []).extend(runner.avisos_descartados(ctx))   # opcionales omitidos
        # Temporal + rename (rem_utils.escribir_atomico): un corte no deja un .xlsx roto.
        escribir_atomico(salida, lambda p: smact.escribir(E, p))
        res["E"] = E
        res["salida"] = salida

        if not maestro:
            log("[tp] Maestro de Actividades NO encontrado (ni cargado a mano, ni "
                "embebido en el .exe): el Trabajo Perdido usa SOLO la heurística "
                "(mask_tributa_ada), menos preciso. Para embeberlo, reconstruye el .exe "
                "con --add-data del maestro_slim.csv.gz (CLAUDE.md SS11) o déjalo junto al .exe.")
        # Try propio: un fallo aca (p.ej. Monitoreo admin sin 'PROFESIONAL ATENCION')
        # no debe tumbar el SM, que ya se guardo arriba.
        try:
            import modulos.rem_sm_trabajo_perdido as tpmod
            Etp = tpmod.procesar(ctx["ada"], maestro=maestro, mes=(y, m), log=log, d=ctx["d"])
            escribir_atomico(salida_tp, lambda p: tpmod.escribir(Etp, p))
            res["n_tp"] = len(Etp)
            log(f"OK Trabajo perdido: {len(Etp)} atenciones a saco roto -> {salida_tp.name}")
        except Exception as e:   # noqa: BLE001
            res["fallo_tp"] = str(e)   # el resumen lo dice: no basta con el log
            log(f"[tp] no se generó el reporte de trabajo perdido: {e}")

    if a03["incluir"]:
        if a03["instrumentos"]:
            salida_a03 = salidas["a03"]

            def _correr_a03():
                # El nombre del archivo lleva el mes (para no pisar corridas distintas),
                # pero el A03 NO filtra por mes: no hay una sola fecha en su export y el
                # modulo no la mira. Se dice en voz alta, porque un nombre de archivo que
                # promete un periodo que el contenido no respeta es justo el numero
                # plausible-pero-mal que el REM no perdona (CLAUDE.md regla 2).
                log(f"[a03] OJO: la tabla A03·D.3 cubre TODO lo que traigan los exports de "
                    f"cuestionarios, NO solo {m:02d}/{y}. El mes en el nombre del archivo es "
                    f"solo para distinguir corridas: filtra el periodo al descargarlos de RAYEN.")
                tabla_est = estam.tabla_efectiva(a03["est_ruta"] or None, log=log)
                r03 = {}
                escribir_atomico(salida_a03, lambda p: r03.update(screening.procesar_unificado(
                    a03["instrumentos"], p, estamentos=(tabla_est or None),
                    resolver_estamento=None, log=log)))
                res["n_a03"] = r03["total"]
                res["por_inst_a03"] = r03["por_instrumento"]
                res["avisos_a03"] = r03.get("avisos", [])   # al resumen, no solo a la LEEME
                res["salida_a03"] = salida_a03
                log(f"OK A03·D.3: {r03['total']} aplicaciones -> {salida_a03.name}")

            if ctx["solo_a03"]:
                # A03 es el UNICO proposito de esta corrida (reemplaza a la vieja
                # pestana standalone): si falla, tiene que fallar RUIDOSO -- nunca
                # un "Listo" con 'None aplicaciones' tapando el error real.
                _correr_a03()
            else:
                # Mismo criterio que el resto del "saco roto"/Trabajo Perdido:
                # A03 es un AÑADIDO al run de Actividades, que ya se guardo arriba;
                # un fallo aca no debe tumbar ese resultado ya bueno.
                try:
                    _correr_a03()
                except Exception as e:   # noqa: BLE001
                    # En el RESUMEN, no solo en el log: un "Listo" que calla que la
                    # D.3 no salio deja al usuario buscando el archivo -- y encontrando
                    # el de una corrida anterior.
                    res["fallo_a03"] = str(e)
                    log(f"[a03] no se generó la tabla A03·D.3: {e}")
        else:
            log("[a03] 'Incluir cuestionarios' marcado pero sin archivos -> se omite.")

    return res


def _por_instrumento(res):
    """ ' (PSC: 20 · PSC-Y: 18 · GHQ-12: 22)' para el resumen, o '' si no hay dato.

    NO es decoracion: los 3 slots A03·D.3 fijan el instrumento A MANO, sin
    autodeteccion (`bloque_cuestionarios`, igual que la vieja pestana), asi que cargar
    el export del PSC-Y en el slot del PSC no lo cacha nadie. El desglose es lo unico
    que lo delata ANTES de copiar la tabla D.3 al SA_26: un total pelado ("60
    aplicaciones") tapa igual un 20/20/20 que un 60/0/0. `_correr_a03` de autorem.py
    lo mostraba, el port lo perdio, y `procesar_unificado` igual lo venia devolviendo
    en `por_instrumento`."""
    por_inst = res.get("por_inst_a03")
    if not por_inst:
        return ""
    return " (" + " · ".join(f"{k}: {v}" for k, v in por_inst.items()) + ")"


def resumen(res):
    y, m = res["mes"]
    if res["solo_a03"]:
        return (f"Listo. A03·D.3 {y}-{m:02d}: {res['n_a03']} aplicaciones"
                f"{_por_instrumento(res)}.{widgets.texto_avisos(res.get('avisos_a03'))}\n\n"
                f"Guardado en:\n{res['salida_a03']}")
    E = res["E"]
    resu = E.attrs["tablas"]["SM_Resumen"]
    rtxt = "\n".join(f"  {r['Casilla']}: {r['Total mes']}" for _, r in resu.iterrows())
    tptxt = f"\nTrabajo perdido: {res['n_tp']} atenciones a saco roto." if res["n_tp"] is not None else ""
    if res.get("fallo_tp"):
        tptxt = f"\nTrabajo perdido: NO se generó ({res['fallo_tp']})."
    a03txt = (f"\nA03·D.3: {res['n_a03']} aplicaciones{_por_instrumento(res)}."
              if res["n_a03"] is not None else "")
    if res.get("fallo_a03"):
        a03txt = (f"\nA03·D.3: NO se generó ({res['fallo_a03']}). Ningún archivo "
                  f"REM_A03_D3 de esta carpeta es de esta corrida.")
    avisos = list(E.attrs.get("avisos") or []) + list(res.get("avisos_a03") or [])
    return (f"Listo. REM SM Actividades {y}-{m:02d}.\n{len(E)} eventos en el detalle.{tptxt}{a03txt}\n\n"
            f"{rtxt}{widgets.texto_avisos(avisos)}\n\nGuardado en:\n{res['salida']}")


PANTALLA = {
    "id": "sm_actividades",
    "programa": "Salud Mental",
    "titulo": "Actividades",
    "estado": "estable",
    "instrucciones": instrucciones,
    "inputs": [
        {"key": "ada", "etiqueta": "Atenciones/Diag/Activ (ADA):", "multi": True,
         "obligatorio": _ada_grupal_obligatorio,
         "titulo_dialogo": "Atenciones / Diagnósticos / Actividades",
         "on_elegido": lambda frame, pagina: _chequeo_cruce(frame, pagina, "ada")},
        {"key": "grupal", "etiqueta": "Atenciones Grupales:", "multi": True,
         "obligatorio": _ada_grupal_obligatorio,
         "motivo_obligatorio": "De ahí salen A06 psicosocial grupal, A19a grupal y A27.",
         "titulo_dialogo": "Reporte de Atenciones Grupales",
         "on_elegido": lambda frame, pagina: _chequeo_cruce(frame, pagina, "grupal")},
        {"key": "inscritos", "etiqueta": "Inscritos (opcional, TRANS):", "multi": True,
         "obligatorio": False, "titulo_dialogo": "Informe Inscritos y Adscritos - para el flag TRANS"},
        {"key": "multiprofesional", "etiqueta": "Multiprofesional (opc, A26):", "multi": True,
         "obligatorio": False, "titulo_dialogo": "Monitoreo Multiprofesional - composición de VDI en A26"},
        {"key": "maestro", "etiqueta": "Maestro (opc, saco roto):", "multi": True,
         "obligatorio": False,
         "titulo_dialogo": "Maestro de Actividades - catálogo RAYEN para clasificar el trabajo perdido"},
    ],
    "mes": True,
    "carpeta_salida": True,
    "extras": [
        {"despues_de": "ada", "construir": widgets.bloque_banner_fuente},
        {"despues_de": "grupal", "construir": bloque_dotacion_sm},
        {"despues_de": None, "construir": bloque_cuestionarios, "key": "a03"},
    ],
    "preparar": preparar,
    "correr": correr,
    "resumen": resumen,
    "al_completar": al_completar,
    # Salida por defecto sin ADA (solo-cuestionarios): junto a los cuestionarios,
    # nunca el cwd (CLAUDE.md SS2: las salidas llevan RUT).
    "carpeta_defecto": lambda ctx: next(
        (Path(r).parent for r in ctx["a03"]["instrumentos"].values()), None),
}
