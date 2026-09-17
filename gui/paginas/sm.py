#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Sonnet 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# Copyright (C) 2026 Simon Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.9.15
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
standalone (`_tab_a03`, YA BORRADA de autorem.py -- ver CLAUDE.md
'gui-2-eliminar-a03-standalone') permitia tabular SOLO los cuestionarios, sin
ADA ni Grupal. Esta pagina reproduce esa capacidad: si 'Incluir cuestionarios'
esta marcado Y no hay ADA ni Grupal, corre SOLO el A03 (con el bloque de
Estamentos que igual se necesita para el perfil Administrativo del
screening) y se salta el bloque de Actividades Y la fase `preparar` de
Dotacion (que necesita el ADA cargado; una corrida solo-cuestionarios no lo
tiene)."""

import customtkinter as ctk

from gui import widgets, dialogos

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


def _ada_grupal_obligatorio(getters):
    """ADA y Grupal dejan de ser obligatorios SOLO si es una corrida
    solo-cuestionarios de verdad: checkbox marcado, con archivos, y NINGUNO
    de los dos elegido (SS6 del plan). Si el checkbox esta marcado pero el
    usuario tambien cargo ADA/Grupal, se hace la corrida COMPLETA de
    siempre -- la casilla no reemplaza el input, solo lo completa."""
    a03 = getters["a03"]()
    return not (a03["incluir"] and a03["instrumentos"]
                and not getters["ada"]() and not getters["grupal"]())


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
    ctk.CTkCheckBox(frame, text="¿Incluir cuestionarios?  (genera además la tabla A03·D.3)",
                    variable=var_incluir, command=lambda: _toggle()).pack(anchor="w", pady=(6, 0))

    caja = widgets.caja_titulada(frame, "Cuestionarios A03·D.3 (PSC / PSC-Y / GHQ-12)")

    def _toggle():
        if var_incluir.get():
            caja.pack(fill="x", pady=(2, 4))
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
    ctx["solo_a03"] = bool(a03["incluir"] and a03["instrumentos"]
                           and not ctx["ada"] and not ctx["grupal"])
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

    y, m = ctx["mes"]
    carpeta = ctx["carpeta"]
    a03 = ctx["a03"]
    res = {"mes": (y, m), "solo_a03": ctx["solo_a03"], "salida": None,
           "salida_a03": None, "n_tp": None, "n_a03": None, "E": None}

    if not ctx["solo_a03"]:
        salida = carpeta / f"REM_SM_actividades_{y}_{m:02d}.xlsx"
        salida_tp = carpeta / f"REM_SM_trabajo_perdido_{y}_{m:02d}.xlsx"
        inscritos = ctx["inscritos"][0] if ctx["inscritos"] else None
        multiprofesional = ctx["multiprofesional"][0] if ctx["multiprofesional"] else None
        maestro = ctx["maestro"][0] if ctx["maestro"] else slim_por_defecto()

        E = smact.procesar(ctx["ada"], grupal=ctx["grupal"], inscritos=inscritos,
                           multiprofesional=multiprofesional, mes=(y, m), log=log,
                           d=ctx["d"], dotacion_tabla=ctx["tabla_dot"])
        smact.escribir(E, salida)
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
            tpmod.escribir(Etp, salida_tp)
            res["n_tp"] = len(Etp)
            log(f"OK Trabajo perdido: {len(Etp)} atenciones a saco roto -> {salida_tp.name}")
        except Exception as e:   # noqa: BLE001
            log(f"[tp] no se generó el reporte de trabajo perdido: {e}")

    if a03["incluir"]:
        if a03["instrumentos"]:
            salida_a03 = carpeta / f"REM_A03_D3_{y}_{m:02d}.xlsx"

            def _correr_a03():
                tabla_est = estam.tabla_efectiva(a03["est_ruta"] or None, log=log)
                r03 = screening.procesar_unificado(a03["instrumentos"], salida_a03,
                                                   estamentos=(tabla_est or None),
                                                   resolver_estamento=None, log=log)
                res["n_a03"] = r03["total"]
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
                    log(f"[a03] no se generó la tabla A03·D.3: {e}")
        else:
            log("[a03] 'Incluir cuestionarios' marcado pero sin archivos -> se omite.")

    return res


def resumen(res):
    y, m = res["mes"]
    if res["solo_a03"]:
        return (f"Listo. A03·D.3 {y}-{m:02d}: {res['n_a03']} aplicaciones.\n\n"
                f"Guardado en:\n{res['salida_a03']}")
    E = res["E"]
    resu = E.attrs["tablas"]["SM_Resumen"]
    rtxt = "\n".join(f"  {r['Casilla']}: {r['Total mes']}" for _, r in resu.iterrows())
    tptxt = f"\nTrabajo perdido: {res['n_tp']} atenciones a saco roto." if res["n_tp"] is not None else ""
    a03txt = f"\nA03·D.3: {res['n_a03']} aplicaciones." if res["n_a03"] is not None else ""
    return (f"Listo. REM SM Actividades {y}-{m:02d}.\n{len(E)} eventos en el detalle.{tptxt}{a03txt}\n\n"
            f"{rtxt}\n\nGuardado en:\n{res['salida']}")


PANTALLA = {
    "id": "sm_actividades",
    "programa": "Salud Mental",
    "titulo": "Actividades",
    "estado": "estable",
    "instrucciones": instrucciones,
    "inputs": [
        {"key": "ada", "etiqueta": "Atenciones/Diag/Activ (ADA):", "multi": True,
         "obligatorio": _ada_grupal_obligatorio,
         "titulo_dialogo": "Atenciones / Diagnósticos / Actividades"},
        {"key": "grupal", "etiqueta": "Atenciones Grupales:", "multi": True,
         "obligatorio": _ada_grupal_obligatorio,
         "titulo_dialogo": "Reporte de Atenciones Grupales"},
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
        {"despues_de": "grupal", "construir": bloque_dotacion_sm},
        {"despues_de": None, "construir": bloque_cuestionarios, "key": "a03"},
    ],
    "preparar": preparar,
    "correr": correr,
    "resumen": resumen,
}
