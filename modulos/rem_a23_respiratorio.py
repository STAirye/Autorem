#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 2.0.10
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. Distributed WITHOUT ANY WARRANTY. See the GNU
# General Public License for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
REM A23 (Respiratorio) — motor de indicadores desde el export de ATENCIONES.

FASE 1: los 27 indicadores REMA23 que salen SOLO de la tabla de atenciones
(actividades / diagnósticos / instrumento / tipo atención), 1 fila por paciente
(RUN), SI/NO por indicador del MES de reporte. Portado del visual PowerBI
'poblacion ferrada 2.5' (ver docs/A23_spec.md). Usa pandas (groupby por RUN).

Columnas por nombre SEMÁNTICO (RAYEN renumera el prefijo 'N.- '). Match de
subcadena = norm() en ambos lados (case- y acento-insensible), robusto ante
'neumonía/neumonia'. Ventana de mes PARAMETRIZABLE (no TODAY()), para recalcular
meses pasados.

Lee atenciones IRIS o Monitoreo admin (rem_utils.cargar_atenciones). SALA bajo
control + Sección G inasistentes ya integrados. PENDIENTE: agregación mensual por
edad×sexo; admin es PARCIAL (los dx por código ICD no vienen -> Ira Alta/Bronquitis/
EPOC exac. = 0, ver rem_utils.MAPA_ATENCIONES). El Otros Crónicos y el NSP también
se aceptan en su formato Administrativo (ronda 11; el estamento del Otros Crónicos admin
sale del funcionario: `_estamento_por_funcionario`).
"""

import pandas as pd

from programas.rem_utils import (norm, cargar_atenciones, cargar_canonico,
                                 resolver_columnas, contiene_todos as _all,
                                 contiene_alguno as _any, _rango_mes, filtrar_mes,
                                 _mujer, _hombre,
                                 grid as _grid, fecha_col, PUEBLO_VACIO, es_medico,
                                 ArchivoInvalido, Path, edad_anios, opcional)
from programas import formatos          # clasificación de fuente plena/parcial (fase 2)
# cargar_atenciones (IRIS | Monitoreo admin) vive en rem_utils y se reexporta acá.


_SALA_IRA = ["control sala (ira", "consulta sala (ira", "kinesioterapi"]

# -- PRE-ESCRITO (NO activo): Educación GRUPAL A23·M.2 — talleres respiratorios --
# Estado ago-2026: los talleres grupales AÚN NO se hacen en el CESFAM -> nada que
# contar hoy. Se esperan en ~2 meses (Simón envió las actividades candidatas al RT
# de Respiratorio). La lógica es CASI IDÉNTICA a rem_sm_actividades: conteo por
# ASISTENCIA del reporte 'Atenciones Grupales' (cada fila Asiste=SI, SIN dedup) ->
# A23·M.2 (Nº sesiones = grupos distintos; Nº participantes = asistencias). Ver
# docs/A23_P3_plan.md ("Educación grupal M.2").
#
# Hallazgo Maestro (ago-2026): hoy TODO lo grupal respiratorio cae a REM-Gestion
# (no tributa). Al activarse, estas deberían apuntar a A23·M.2 (o reclasificarse en
# el Maestro); mientras tanto caen a 'saco roto' (las caza Trabajo perdido):
#   _M2_TALLERES = [
#       "taller grupal cesacion tabaco",   # tema tabaco
#       "ges tabaco sesion",               # AG_GES TABACO Sesión 1-6
#       "taller prevencion ira",
#       "taller era descompensado",
#       "taller rehabilitacion pulmonar",  # ¿M.2 o O? confirmar con el RT
#   ]
# Implementación (cuando haya datos): reciclar cargar_grupal() de rem_sm_actividades
# (mismo reporte grupal), filtrar ACT por _M2_TALLERES + mes por FECHA ATENCIÓN, y
# armar la tabla con _grid. VALIDAR contra un mes real (como se hizo con SM). OJO:
# el tabaco INDIVIDUAL ya tributa por otra vía (A23·M.1 'Educación Antitabaco' de
# _masks_simples y A23·N VDI Hogar Libre de Humo) -> no duplicar.


def _masks_simples(d):
    """dict indicador -> máscara BOOLEANA por fila = por ATENCIÓN.

    Los indicadores con AND entre actividades («autocuidado» Y «control sala», del DAX)
    piden las dos en la MISMA atención, y eso funciona porque `cargar_atenciones` entrega
    UNA fila por atención con todas sus actividades en `ACT` en los dos formatos. Hasta
    1.9.17 el Monitoreo llegaba con una fila por actividad y esto lo arreglaba un
    `_act_de_la_atencion` local (ronda 11): la forma se normaliza en la FUENTE desde la
    ronda 12 (`rem_utils._una_fila_por_atencion`), así que acá no hay nada que agrupar."""
    A, D, I, T = d["ACT_n"], d["DIAG_n"], d["INSTR_n"], d["TIPO_n"]
    return {
        "REMA23 Autocuidado":        _all(A, "autocuidado") & _all(A, "control sala"),
        "REMA23 Bronquitis Aguda":   _all(D, "J20"),
        "REMA23 Campaña Invierno":   _any(A, ["ira alta", "s.b.o", "neumon", "exacerbacion asma", "epoc", "otras respir"]),
        "REMA23 Consulta SALA Kine (act)": _all(A, "consulta sala (ira") & _all(I, "kine"),
        "REMA23 Control SALA Kine (act)":  _all(A, "control sala (ira") & _all(I, "kine"),
        "REMA23 Control SALA Med (act)":   _all(A, "control sala (ira") & _all(I, "medico") & ~_all(I, "tecnico"),
        "REMA23 Coqueluche":         _all(D, "coquelu"),
        "REMA23 Edu Integral Sala":  _all(A, "educacion integral en salud respiratoria") & _any(A, _SALA_IRA),
        "REMA23 Educación Antitabaco": _all(A, "tabaco") & _any(A, _SALA_IRA),
        "REMA23 EPOC Exacerbado":    _all(D, "J44.1"),
        "REMA23 Espirometría (act)": _all(A, "espirometr"),
        "REMA23 Influenza":          _all(D, "influenz"),
        "REMA23 Inhaloterapia":      _all(A, "inhalatoria") & _all(A, "control sala"),
        "REMA23 KTR":                _all(A, "kinesioterapia res"),
        "REMA23 Ira Alta":           _all(D, "j0"),
        "REMA23 Otras":              _all(A, "consejerias individuales otras areas") & _all(A, "control sala"),
        "REMA23 Neumonia":           _all(D, "neumonia"),
        "REMA23 Vida Saludable":     _all(A, "consejer") & _any(A, ["activi", "aliment"]) & _any(A, _SALA_IRA),
        "REMA23 Rehab Conti":        _all(A, "rehabilitacion pulmonar - artic"),
        "REMA23 Rehab Ses Act Fca":  _all(A, "rehabilitacion pulmonar - sesion act"),
        "REMA23 Rehab Ses Educ":     _all(A, "rehabilitacion pulmonar - sesion educ"),
        "REMA23 VDI Respi (aten)":   _all(T, "domiciliaria"),   # + SALA Ingresado en Fase 2
    }


_RESP_BASE = ["REMA23 Ira Alta", "REMA23 Influenza", "REMA23 Neumonia",
              "REMA23 Bronquitis Aguda", "REMA23 EPOC Exacerbado", "REMA23 Coqueluche"]


def _sino(index, runs):
    return pd.Series(index.isin(set(runs)), index=index).map({True: "SI", False: "NO"})


def procesar(entrada, otros=None, estrat=None, inasistentes=None, mes=None, log=print):
    """Devuelve el DataFrame DETALLE (1 fila por RUN) con los indicadores REMA23
    del `mes` (año, mes) — default mes anterior.
    `entrada` = export de atenciones. `otros`/`estrat` (opcionales) = formulario
    'Otros y Respi' + 'Estratificación' -> agregan SALA bajo control + Sección G.
    `inasistentes` (opcional) = reporte NSP -> Sección H (citas Control/Ingreso
    IRA/ERA no asistidas, por estamento × tramo etario).

    Los OPCIONALES se cargan y validan PRIMERO, antes del ADA: un opcional que no sirve
    hace que la GUI pregunte «¿seguir sin él?» y RE-CORRA (§3.1 de programas/CLAUDE.md)."""
    ini, fin = _rango_mes(mes)
    # Los OPCIONALES se cargan PRIMERO, antes del ADA y de todo el trabajo pesado
    # (ronda 12). Si uno no sirve, la GUI pregunta «¿seguir sin él?» y re-corre: antes se
    # cargaban donde se usan -- la Estratificación después del formulario, el NSP al final,
    # con SALA y la Sección G ya calculadas --, así que la pregunta llegaba tras el minuto
    # de corrida y el «Sí» repetía todo desde cero. No dependen de nada de acá.
    est = pd.Series(dtype="object")
    if estrat is not None:
        with opcional("estrat"):   # opcional invalida: la GUI pregunta si seguir sin ella
            est = cargar_estrat(estrat, log=log)
        if otros is None:
            log("[a23] la Estratificacion solo aporta a SALA bajo control, y SALA necesita "
                "el formulario 'Otros Cronicos': sin el, este reporte no se usa.")
    h = None
    if inasistentes is not None:
        # La Seccion H es independiente del ADA: se calcula entera aca (incluido su
        # filtro de mes, que es donde falla un NSP de otro periodo).
        with opcional("inasistentes"):   # opcional invalido: la GUI pregunta si seguir sin el
            h = _seccion_h(cargar_inasistentes(inasistentes, log=log), ini, fin)

    d = cargar_atenciones(entrada, log=log)
    # Sin fechas (export vacio o header-only) min/max dan NaT y el strftime revienta
    # criptico: se loguea igual y el ArchivoInvalido claro lo tira filtrar_mes, abajo.
    span = (f"{d['FECHA'].min():%Y-%m-%d}..{d['FECHA'].max():%Y-%m-%d}"
            if d["FECHA"].notna().any() else "sin fechas")
    log(f"[a23] {len(d)} atenciones | datos {span} | mes reporte {ini:%Y-%m}")

    from pathlib import Path
    runs = pd.Index(d["RUN"].unique(), name="RUN")
    fer = pd.DataFrame(index=runs)
    fer.attrs["mes"] = (ini.year, ini.month)
    fer.attrs["avisos"] = []
    # Fuente PARCIAL (fase 2): el Monitoreo Admin trae el dx en TEXTO sin codigo ICD,
    # asi que los indicadores que matchean por codigo salen 0 aunque la columna
    # DIAGNOSTICO resuelva bien. Antes eso pasaba callado. Ver formatos.clasificar_fuente.
    _av = formatos.aviso_fuente(
        *d.attrs.get("fuente", (formatos.FUENTE_PLENA, [])),
        "Ira Alta, Bronquitis y EPOC exacerbado se detectan por CODIGO ICD (j0/J20/"
        "J44.1) y van a salir en 0; ademas se pierde la demografia (pueblo, migrante).",
        casilla="Atenciones (fuente del A23)", archivos=d.attrs.get("fuente_mezcla"))
    if _av:
        fer.attrs["avisos"].append(_av)
    fuentes = [Path(p).name for p in (entrada if isinstance(entrada, (list, tuple)) else [entrada])]
    for extra in (otros, estrat, inasistentes):
        if extra is not None:
            fuentes += [Path(p).name for p in (extra if isinstance(extra, (list, tuple)) else [extra])]
    fer.attrs["fuentes"] = fuentes

    # Fail loud (§3): sin NINGUNA atención del mes, los 27 indicadores salen "NO" y el
    # detalle parece un mes de cero actividad. Guarda sobre la FUENTE, no por indicador.
    dm = filtrar_mes(d, ini, fin, "el export de atenciones (A/D/A)")
    log(f"[a23] atenciones en el mes: {len(dm)} | pacientes atendidos: {dm['RUN'].nunique()}")

    masks = _masks_simples(dm)
    si = {name: dm.loc[m, "RUN"].unique() for name, m in masks.items()}
    for name in masks:
        fer[name] = _sino(fer.index, si[name])

    # base respiratoria del mes (por RUN) para los compuestos
    resp = set().union(*(set(si[n]) for n in _RESP_BASE))
    A, I, T = dm["ACT_n"], dm["INSTR_n"], dm["TIPO_n"]
    morbi = dm.loc[_all(I, "medic") & _any(T, ["morbilida", "consulta sac", "teletriage"]), "RUN"].unique()
    seg_eu = dm.loc[(_all(I, "enfermer") & ~_all(I, "tecnic")) & _any(A, ["control sala (ira", "consulta sala (ira"]), "RUN"].unique()
    seg_ki = dm.loc[(_all(I, "kine") & ~_all(I, "tecnic")) & _any(A, ["control sala (ira", "consulta sala (ira"]), "RUN"].unique()
    fer["REMA23 Morbi respiratoria"] = _sino(fer.index, set(morbi) & resp)
    fer["REMA23 Seguimiento Eu"] = _sino(fer.index, set(seg_eu) & resp)
    fer["REMA23 Seguimiento Kine"] = _sino(fer.index, set(seg_ki) & resp)
    fer["¿Atendido 1 mes?"] = _sino(fer.index, dm["RUN"].unique())
    if not any(fer[c].eq("SI").any() for c in fer.columns if c.startswith("REMA23")):
        # Fail loud (§3), gemelo del SM sin nada que tribute: el mes esta cubierto
        # (filtrar_mes paso), pero NINGUNA atencion es respiratoria -> los 27
        # indicadores en NO. Un indicador en 0 es legitimo; TODOS, es un ADA filtrado
        # por otro programa o un export cuyas actividades/diagnosticos ya no calzan.
        raise ArchivoInvalido(
            "sin_datos",
            f"El export de atenciones trae {len(dm)} atención(es) de {ini:%m/%Y}, pero "
            "NINGUNA cuenta para un indicador respiratorio del A23 (IRA/ERA, SALA, "
            "espirometría, diagnósticos J...).\n\nTodo el A23 saldría en 0. Revisa que "
            "sea el export COMPLETO del centro (no filtrado por otro programa) y que "
            "esté SIN modificar.")

    # fila más reciente por RUN (una sola pasada: instrumento + demografía).
    # De toda la historia, no del mes. groupby.last() = último no-nulo por columna.
    dem = d.sort_values("FECHA").groupby("RUN").last()
    fer["Última atención (instrumento)"] = dem["INSTR"].reindex(fer.index).fillna("")
    # NO se emite el nombre del paciente: §8 = el único identificador en la salida es
    # el RUN (=RUT-DV), que basta para trazar la fila a la ficha. No reañadir NOMBRES/APAT/AMAT.
    for c in ("SEXO", "SECTOR", "NACION", "PUEBLO"):
        fer[c.title()] = dem[c].reindex(fer.index)
    fer["Edad"] = _edad(dem, fin).reindex(fer.index)
    fer["¿Originario o Migrante?"] = _origen(dem).reindex(fer.index)

    # -- Fase 2: SALA bajo control (si se dieron los inputs) --
    if otros is not None:
        od, _ = cargar_otros(otros, log=log)
        fer.attrs["avisos"].extend(_estamento_por_funcionario(od, d, log=log))   # Admin
        for nombre, falt in od.attrs.get("condiciones_incompletas", {}).items():
            fer.attrs["avisos"].append((
                "SALA / Seccion G (preguntas del formulario)", "SUBCONTADO",
                f"«{nombre}» no trae todas las columnas de: {', '.join(falt)} (encabezado "
                "renombrado o export viejo): esas condiciones pueden salir en 0",
                "Revisar que 'Otros Cronicos' sea el export completo, sin modificar"))
        if not od["_med"].any():
            # SALA y la Seccion G cuentan SOLO formularios aplicados por medico (DAX).
            # Si ninguno lo es, las dos salen enteras en 0: decirlo, no callarlo.
            log("[a23] NINGÚN formulario 'Otros Cronicos' lo aplicó un médico (columna "
                "INSTRUMENTO): SALA bajo control y la Sección G van a salir en 0.")
            fer.attrs["avisos"].append((
                "SALA bajo control / Seccion G", "EN 0",
                "ningun formulario 'Otros Cronicos' fue aplicado por medico (INSTRUMENTO), "
                "y SALA / Seccion G cuentan solo esos",
                "Revisar la columna INSTRUMENTO del export, o quien llena el formulario"))
        # Sección G solo sirve con historial largo: el inasistente tiene su ÚLTIMO
        # formulario/control hace >1 año. El reporte 'Otros y Respi' se baja POR AÑO
        # calendario, así que reportar un mes exige AL MENOS el año del reporte + el
        # anterior (12 meses atrás). Fail loud si el historial no llega tan atrás
        # (chequeo por FECHA MÍNIMA, no por span: un solo año da ~365 días pero igual
        # deja fuera el año previo).
        if od["FECHA"].notna().any():
            limite = ini - pd.DateOffset(months=12)   # G mira >=12 meses hacia atrás
            if od["FECHA"].min() > limite:
                log(f"[a23] Sección G SUBCONTARÁ: los formularios 'Otros y Respi' "
                    f"arrancan en {od['FECHA'].min():%Y-%m}, pero el mes reportado "
                    f"({ini:%Y-%m}) necesita historial hasta {limite:%Y-%m}. Como el "
                    f"reporte se baja POR AÑO, carga AMBOS: el año del reporte Y el "
                    f"ANTERIOR (ideal 5, como el PowerBI). Selecciónalos juntos (ctrl-click).")
                fer.attrs["avisos"].append((
                    "Seccion G (inasistentes cronicos)", "SUBCONTADO",
                    f"'Otros y Respi' arranca en {od['FECHA'].min():%Y-%m}, se necesita "
                    f"historial hasta {limite:%Y-%m}",
                    "Cargar el año del reporte Y el anterior (ideal 5, como el PowerBI)"))
        sala, _ing = _sala(fer.index, fer["Edad"], d, od, est)
        for c in sala.columns:
            fer[c] = sala[c]
        if not fer["Pertenece a SALA"].eq("SI").any():
            # Fail loud (CLAUDE.md regla 2): las hojas copy-paste del A23 se calculan SOLO
            # sobre 'Pertenece a SALA' (_tablas_a23). Nadie bajo control = TODAS en 0, con
            # el detalle lleno de atenciones respiratorias. No es un mes real: es un
            # formulario que no cruza con el ADA, o sin formularios validos.
            raise ArchivoInvalido(
                "sin_datos",
                f"El formulario 'Otros Cronicos' trae {len(od)} formulario(s), pero NINGUNA "
                f"de las {len(fer)} personas del ADA queda bajo control en SALA: todas las "
                "hojas del A23 saldrían en 0.\n\nRevisa que el formulario sea el export "
                "completo (con las preguntas '¿Padece...?' y su ESTADO, aplicado por "
                f"médico: {int(od['_med'].sum())} de {len(od)} lo son) y que el RUN venga en "
                "el mismo formato que en el ADA.")
        vdi =fer.pop("REMA23 VDI Respi (aten)").eq("SI") & fer["SALA Ingresado"].eq("SI")
        fer["REMA23 VDI Respi"] = vdi.map({True: "SI", False: "NO"})
        om = od[(od["FECHA"] >= ini) & (od["FECHA"] <= fin)]
        cdv = om.sort_values("FECHA").groupby("RUN")["CDV"].last()
        fer["REMA23 Encuesta calidad de vida"] = cdv.reindex(fer.index).fillna("")
        log(f"[a23] SALA Ingresado={(fer['SALA Ingresado']=='SI').sum()} | "
            f"ASMA={(fer['SALA ASMA']=='SI').sum()} EPOC={(fer['SALA EPOC']=='SI').sum()} "
            f"SBOR={(fer['SALA SBOR']=='SI').sum()} FQ={(fer['SALA FQ']=='SI').sum()} "
            f"Otras={(fer['SALA Otras Respi']=='SI').sum()}")
        # Sección G: inasistentes a control de crónicos (corte = último día del mes)
        # La edad del ADA rellena la que falte en el formulario; lo que siga sin edad
        # se cuenta con el umbral >=2 años y se AVISA (antes se descartaba callado).
        sin_edad = set()
        gcounts, gflags = _seccion_g(od, fin, edad_extra=fer["Edad"], sin_edad=sin_edad)
        n_sin_edad = len(sin_edad)
        if n_sin_edad:
            log(f"[a23] Sección G: {n_sin_edad} paciente(s) crónico(s) sin fecha de "
                "nacimiento (ni en 'Otros Cronicos' ni en el ADA) -> evaluados con el "
                "umbral de >=2 años. Si alguno es menor de 2, puede estar mal clasificado.")
            fer.attrs["avisos"].append((
                "Seccion G (inasistentes cronicos)", "REVISAR",
                f"{n_sin_edad} paciente(s) cronico(s) sin fecha de nacimiento: se uso el "
                "umbral de >=2 años (11m29d); para <2 años el umbral es menor",
                "Revisar la FECHA DE NACIMIENTO de esos RUN en el export"))
        for pref, _lbl in _G_COND:
            fer["Inasistente " + pref] = pd.Series(fer.index.isin(gflags[pref]), index=fer.index).map({True: "SI", False: "NO"})
        fer.attrs["seccion_g"] = gcounts
        log("[a23] Sección G inasistentes crónicos: " + " · ".join(
            f"{lbl.split()[0]}={d['Total']}" for lbl, d in gcounts.items()))
    else:
        fer.attrs["avisos"].append((
            "SALA bajo control / Seccion G", "NO CALCULADO",
            "no se cargo el formulario 'Otros Cronicos' -> no se puede filtrar "
            "'Pertenece a SALA': el A23 NO queda acotado a la poblacion bajo control",
            "Cargar 'Otros Cronicos' (obligatorio para SALA y Seccion G)"))

    # -- Sección H: inasistentes a citación agendada (reporte NSP, independiente) --
    # Ya calculada arriba, con los demás opcionales; acá solo se cuelga de `fer`.
    if h is not None:
        if h.attrs.get("sin_edad"):
            n = h.attrs["sin_edad"]
            log(f"[a23] Sección H: {n} inasistencia(s) sin AÑOS legible -> contadas en "
                "'20 y más'.")
            fer.attrs["avisos"].append((
                "Seccion H (inasistentes a citacion)", "REVISAR",
                f"{n} inasistencia(s) sin edad (AÑOS) legible en el reporte NSP: van en "
                "'20 y mas' (pueden ser menores de 20)",
                "Revisar la columna AÑOS de esas citas en el reporte NSP"))
        fer.attrs["seccion_h"] = h
        tot = int(h.loc[h["Profesional"] == "TOTAL", "Total"].iloc[0])
        log(f"[a23] Sección H inasistentes a citación (Control/Ingreso IRA/ERA): total={tot} · "
            + " · ".join(f"{r['Profesional'].split('/')[0]}={r['Total']}"
                         for _, r in h.iterrows() if r["Profesional"] != "TOTAL"))

    log(f"[a23] listo: {len(fer)} pacientes, {sum(c.startswith('REMA23') for c in fer.columns)} indicadores REMA23")
    return fer.reset_index()


def _edad(dem, ref):
    """Edad en años a la fecha `ref`, desde FECHA NACIMIENTO; fallback col AÑOS."""
    fnac = pd.to_datetime(dem["FNAC"], errors="coerce", dayfirst=True)
    e = ((ref - fnac).dt.days // 365.25).astype("Int64")
    fb = pd.to_numeric(dem["ANOS"], errors="coerce").astype("Int64")
    return e.fillna(fb)


def _origen(dem):
    nac, pue = dem["NACION"].map(norm), dem["PUEBLO"].map(norm)
    es_chileno = nac.str.contains("CHILEN", regex=False, na=False)   # CHILENA/CHILENO/variantes
    mig = ~es_chileno & (nac != "") & (nac != "DESCONOCIDO")
    ori = es_chileno & ~pue.isin(PUEBLO_VACIO)
    return pd.Series(["Migrante" if m else "Originario" if o else "NO"
                      for m, o in zip(mig, ori)], index=dem.index)


# +===================================================================+
# |  FASE 2 — SALA bajo control (formulario 'Otros y Respi' + Estratif) |
# +===================================================================+


def _resolver_otros(cols):
    """Mapea las columnas del formulario 'Otros y Respi' por nombre SEMÁNTICO.
    Las 'N.- ESTADO' (ingreso/seguimiento) = 1ª que termina en ESTADO tras el ancla."""
    hn = [(c, norm(c)) for c in cols]

    def find(*subs, no=()):
        sn, nn = [norm(s) for s in subs], [norm(x) for x in no]
        return next((c for c, n in hn if all(s in n for s in sn) and not any(x in n for x in nn)), None)

    def tras(anchor, pred):   # 1ª columna tras el ancla que cumple pred(norm)
        ai = next((i for i, (c, n) in enumerate(hn) if norm(anchor) in n), None)
        return None if ai is None else next((c for c, n in hn[ai + 1:] if pred(n)), None)

    def estado_tras(a): return tras(a, lambda n: n.endswith("ESTADO"))
    def prox_tras(a): return tras(a, lambda n: "PROXIMO CONTROL" in n)

    def exacto(nombre): return next((c for c, n in hn if n == norm(nombre)), None)

    # IRIS | Administrativo (ronda 11, contra refs_tablas/Otros_cronicos_*.xlsx): el Admin
    # trae 'RUT', 'Fecha Formulario' y 'Funcionario', y NO trae INSTRUMENTO (el estamento
    # sale del nombre del funcionario, ver `_estamento_por_funcionario`) ni fecha de
    # nacimiento (la edad sale del ADA, como ya hacia la Seccion G sin FNAC).
    return {
        "RUN": find("NUMERO", "IDENTIFICACION") or exacto("RUT"),
        "FECHA": find("FECHA ATENCION") or find("FECHA FORMULARIO"),
        "FUNC": exacto("FUNCIONARIO"),
        "INSTR": find("INSTRUMENTO", no=["ESTABLECIMIENTO"]),
        "SEXO_o": find("SEXO"), "FNAC_o": find("FECHA", "NACIMIENTO"),
        "SBOR_p": find("SINDROME BRONQUIAL OBSTRUCTIVO"), "SBOR_rec": find("ES RECURRENTE"),
        "SBOR_est": estado_tras("SINDROME BRONQUIAL OBSTRUCTIVO"), "SBOR_grav": find("GRAVEDAD SBOR"),
        "ASMA_p": find("PADECE DE ASMA BRONQUIAL"), "ASMA_est": estado_tras("PADECE DE ASMA BRONQUIAL"),
        "ASMA_grav": find("GRAVEDAD ASMA BRONQUIAL"), "ASMA_ctrl": find("ESTADO DE CONTROL ASMA"),
        "EPOC_p": find("ENFERMEDAD PULMONAR CRONICA"), "EPOC_est": estado_tras("ENFERMEDAD PULMONAR CRONICA"),
        "EPOC_tipo": find("TIPO EPOC"), "EPOC_ctrl": find("ESTADO DE CONTROL EPOC"),
        "O2_p": find("OXIGENO DEPENDIENTE"), "O2_est": estado_tras("OXIGENO DEPENDIENTE"),
        "AV_p": find("NECESITA ASISTENCIA VENTILATORIA"), "AV_val": find("ASISTENCIA VENTILATORIA", no=["NECESITA", "ESTADO", "FECHA"]),
        "AV_est": find("ESTADO ASISTENCIA VENTILATORIA"),
        "FQ_p": find("FIBROSIS QUISTICA"), "FQ_est": estado_tras("FIBROSIS QUISTICA"),
        "OTRAS_p": find("OTRAS ENFERMEDADES RESPIRATORIAS"), "OTRAS_est": estado_tras("OTRAS ENFERMEDADES RESPIRATORIAS"),
        "DISP_p": find("DISPLASIA BRONCOPULMONAR"), "DISP_est": estado_tras("DISPLASIA BRONCOPULMONAR"),
        "CDV": find("RESULTADO ENCUESTA CALIDAD DE VIDA"),
        # Fecha del Próximo Control por condición (Sección G: inasistentes a control de crónicos)
        "SBOR_prox": prox_tras("SINDROME BRONQUIAL OBSTRUCTIVO"), "ASMA_prox": prox_tras("PADECE DE ASMA BRONQUIAL"),
        "EPOC_prox": prox_tras("ENFERMEDAD PULMONAR CRONICA"), "FQ_prox": prox_tras("FIBROSIS QUISTICA"),
        "OTRAS_prox": prox_tras("OTRAS ENFERMEDADES RESPIRATORIAS"), "DISP_prox": prox_tras("DISPLASIA BRONCOPULMONAR"),
    }


# Columnas que necesita cada condicion (SALA y/o Seccion G). La 1a es la pregunta
# '¿Padece?': si NINGUNA resuelve, el archivo no es el formulario 'Otros Cronicos'.
_OTROS_CONDICIONES = {
    "SBOR": ("SBOR_p", "SBOR_rec", "SBOR_est", "SBOR_grav", "SBOR_prox"),
    "Asma": ("ASMA_p", "ASMA_est", "ASMA_grav", "ASMA_ctrl", "ASMA_prox"),
    "EPOC": ("EPOC_p", "EPOC_tipo", "EPOC_est", "EPOC_ctrl", "EPOC_prox"),
    "O2 dependiente": ("O2_p", "O2_est"),
    "Asistencia ventilatoria": ("AV_p", "AV_val", "AV_est"),
    "Fibrosis quistica": ("FQ_p", "FQ_est", "FQ_prox"),
    "Otras respiratorias": ("OTRAS_p", "OTRAS_est", "OTRAS_prox"),
    "Displasia broncopulmonar": ("DISP_p", "DISP_est", "DISP_prox"),
}


def cargar_otros(entrada, log=print):
    """Formulario(s) Otros y Respi -> DataFrame canónico + FECHA. `entrada` puede ser
    una ruta o una lista (varios años: la Sección G / SALA necesitan el histórico)."""
    # RUN/FECHA requeridas (ubican el encabezado y son lo mínimo del formulario); el
    # estamento se exige más abajo, porque puede venir por INSTRUMENTO (IRIS) o por
    # Funcionario (Administrativo). `columnas_por_archivo` da la resolución POR ARCHIVO
    # (un histórico viejo puede no traer una pregunta) -- antes se la llevaba un efecto
    # secundario dentro del propio resolver, que ahora se llama una vez por fila candidata.
    d, col = cargar_canonico(entrada, _resolver_otros, requeridas=("RUN", "FECHA"),
                             no_vacias=("RUN",), log=log)
    for nombre, c in d.attrs["columnas_por_archivo"]:
        if not (c.get("INSTR") or c.get("FUNC")):
            # Sin estamento ni funcionario no hay como saber que formularios son de
            # medico: SALA y la Seccion G en 0 callados.
            raise ArchivoInvalido(
                "sin_columnas",
                f"Archivo «{nombre}»:\n\nNo encuentro ni la columna INSTRUMENTO (IRIS) ni "
                "'Funcionario' (Administrativo): no se puede saber qué formularios aplicó "
                "un médico.\n\nCárgalo tal como sale de RAYEN, sin editar.")
    # (El RUN vacío en TODAS las filas de un archivo lo corta `cargar_canonico` con
    # `no_vacias`, POR ARCHIVO: escrito acá sobre el concatenado, un año con el RUN en
    # blanco cargado junto a otro bueno pasaba callado, y la Sección G contaba como
    # inasistente a quien sí se había controlado -- ronda 12.)
    # Las preguntas de cada condicion son opcionales para el loader, y una que no
    # resuelve (RAYEN reformulo el encabezado: 'TIENE' por 'PADECE DE') deja esa
    # condicion en 0 en SALA y en la Seccion G, callada. Ninguna -> no es este
    # formulario; algunas -> aviso por archivo (lo agrega procesar a la LEEME).
    incompletas = {}
    for nombre, c in d.attrs["columnas_por_archivo"]:
        if not any(c.get(ks[0]) for ks in _OTROS_CONDICIONES.values()):
            raise ArchivoInvalido(
                "sin_columnas",
                f"Archivo «{nombre}»:\n\nNo encuentro NINGUNA pregunta de condición "
                "respiratoria ('¿PADECE DE ASMA BRONQUIAL?', '¿PADECE DE SÍNDROME BRONQUIAL "
                "OBSTRUCTIVO?', ...): SALA bajo control y la Sección G saldrían en 0.\n\n"
                "¿Es el formulario 'Otros Cronicos' de RAYEN, sin modificar?")
        falt = [cond for cond, ks in _OTROS_CONDICIONES.items() if any(not c.get(k) for k in ks)]
        if falt:
            incompletas[nombre] = falt
            log(f"[a23] «{nombre}» no trae todas las columnas de: {', '.join(falt)} -> esas "
                "condiciones pueden SUBCONTAR en SALA y en la Sección G.")
    # fecha_col y no un to_datetime pelado: las fechas ilegibles se CUENTAN en el log
    # en vez de volverse NaT callados (como en el ADA y el formulario SM).
    d["FECHA"] = fecha_col(d["FECHA"], log, "FECHA ATENCION (Otros Cronicos)")
    if not d["FECHA"].notna().any():
        # Sin NINGUNA fecha legible, el chequeo de historial de la Seccion G (procesar)
        # se saltaba entero y la Encuesta de calidad de vida del mes quedaba en blanco,
        # sin un solo aviso. Mismo criterio que rem_utils.filtrar_mes.
        raise ArchivoInvalido(
            "sin_fecha",
            "En el formulario 'Otros Cronicos' ninguna fila tiene una FECHA ATENCION "
            "legible, así que no se puede saber qué período cubre.\n\n"
            "Revisa que sea el export correcto y que esté SIN modificar "
            "(una columna de fecha reformateada a mano rompe la lectura).")
    d["_med"] = es_medico(d["INSTR"].map(norm))   # criterio unico: rem_utils.TOKEN_MEDICO
    d.attrs["condiciones_incompletas"] = incompletas
    return d, col


def _estamento_por_funcionario(od, aten, log=print):
    """Formularios SIN estamento (el 'Otros Cronicos' Administrativo no trae INSTRUMENTO):
    se lo busca por el nombre del funcionario, primero en el propio export de atenciones
    (PROF -> INSTR: el mismo nombre de RAYEN con su estamento) y despues en el cache de
    estamentos (`programas/estamentos`, el mismo del A03 Administrativo). Recalcula
    `_med`. Devuelve avisos para la LEEME; si NINGUNO se resuelve, ArchivoInvalido
    (SALA y la Seccion G saldrian en 0)."""
    falta = od["INSTR"].map(norm).eq("")
    if not falta.any():
        return []
    from programas import estamentos as estam
    tabla = dict(estam.tabla_efectiva(None, log=log))            # cache (nombre norm -> estamento)
    if "PROF" in aten.columns:
        par = aten[["PROF", "INSTR"]].dropna()
        tabla.update({norm(p): i for p, i in zip(par["PROF"], par["INSTR"]) if norm(p) and norm(i)})
    od.loc[falta, "INSTR"] = od.loc[falta, "FUNC"].map(lambda f: tabla.get(norm(f), ""))
    od["_med"] = es_medico(od["INSTR"].map(norm))   # mismo criterio que al cargar
    quedan = od["INSTR"].map(norm).eq("")
    log(f"[a23] 'Otros Cronicos' sin INSTRUMENTO: estamento por funcionario en "
        f"{int(falta.sum() - quedan.sum())} de {int(falta.sum())} formulario(s)")
    if quedan.all():
        raise ArchivoInvalido(
            "sin_estamento",
            "El formulario 'Otros Cronicos' no trae el estamento de quien lo aplicó (el "
            "Administrativo no tiene INSTRUMENTO), y ninguno de sus funcionarios aparece en "
            "el export de atenciones ni en tus estamentos guardados: no se puede saber qué "
            "formularios son de médico (SALA y la Sección G saldrían en 0).\n\nCarga el "
            "reporte 'Utilización de Cupos' en Salud Mental > Actividades (bloque de "
            "estamentos) una vez para guardarlos, o usa el export IRIS del formulario.")
    if not quedan.any():
        return []
    sin = sorted({str(f).strip() or "(sin funcionario)" for f in od.loc[quedan, "FUNC"]})
    muestra = ", ".join(sin[:5]) + (f" y {len(sin) - 5} más" if len(sin) > 5 else "")
    return [("SALA / Seccion G (estamento del formulario)", "SUBCONTADO",
             f"{int(quedan.sum())} formulario(s) 'Otros Cronicos' sin estamento conocido "
             f"({len(sin)} funcionario(s): {muestra}): no cuentan como de médico",
             "Cargar 'Utilizacion de Cupos' (bloque de estamentos) o usar el export IRIS")]


# Reporte de Estratificación de Riesgo (IRIS). El RUT viene partido (RUT + DV).
# Solo por NOMBRE: hasta la ronda 11 había un fallback a "CONDICIONES CRONICAS", armado
# sin el export a la vista, que en el real (refs_tablas/Estratificacion_de_Riesgo_iris.xlsx)
# calza PRIMERO con 'Cantidad de Condiciones Crónicas' -- un CONTEO -- y dejaba la SALA sin
# diagnósticos, callada.
MAPA_ESTRAT = {
    "RUT":  ("subs", ["RUT"]),
    "DV":   ("subs", ["DV"]),
    "DIAG": ("subs", ["DETALLE", "DIAGNOSTICOS"]),
}


def cargar_estrat(entrada, log=print):
    """DataFrame de Estratificación: RUN (=RUT-DV) -> Diagnósticos (normalizado).

    Por `cargar_canonico` desde la ronda 12: es un opcional, y leyéndolo con `leer_xlsx`
    a mano un .xls/.html disfrazado salía como `BadZipFile` -- que `opcional()` no
    reconoce, así que tumbaba la corrida entera en vez de preguntar «¿seguir sin él?».
    De paso hereda la guarda de hoja única, la de 0 filas y la de RUT vacío en todas las
    filas (`no_vacias`), que antes estaban escritas acá a mano."""
    d, _col = cargar_canonico(entrada, lambda h: resolver_columnas(h, MAPA_ESTRAT),
                              requeridas=("RUT", "DIAG"), no_vacias=("RUT",), log=log)
    d = d[d["RUT"].map(norm).ne("")]
    run = [f"{r}-{dv}" if norm(dv) != "" else str(r) for r, dv in zip(d["RUT"], d["DV"])]
    return (pd.DataFrame({"RUN": run, "DIAG": d["DIAG"].map(norm).values})
            .drop_duplicates("RUN").set_index("RUN")["DIAG"])


def _gate(idx, runs, vals):
    """Valor (gravedad/tipo) del último formulario, SOLO si el RUN está en `runs`."""
    v = vals.reindex(idx)
    return pd.Series([str(x) if (r in runs and pd.notna(x) and str(x) != "") else ""
                      for r, x in zip(idx, v)], index=idx)


def _sala(idx, edad, aten, otros, estrat):
    """Columnas SALA bajo control (población respiratoria crónica). Patrón por
    condición: 'último formulario médico válido en ingreso/seguimiento' + cruce con
    diagnósticos de atenciones médicas y de Estratificación. Devuelve (df, set_ing)."""
    o = otros
    def N(k): return o[k].map(norm)
    med = o["_med"]
    si  = lambda k: N(k).eq("SI")   # padece/recurrente = 'Si'
    nn  = lambda k: N(k).str.len() > 0                               # campo obligatorio no vacío
    # Por `_any` (= rem_utils.contiene_alguno) y no dos `.str.contains` sueltos: la versión a mano llamaba
    # a `N(k)` DOS veces, o sea normalizaba la misma columna ESTADO dos veces por
    # condición. Entre esta función y `_seccion_g` eran 47 pasadas de `norm` sobre el
    # formulario, de las cuales 13 eran ese duplicado. Y de paso es el idioma de la
    # regla 4, que ya existía en rem_utils.
    est = lambda k: _any(N(k), ("INGRESO", "SEGUIMIENTO"))

    valid = {   # formulario válido por condición (máscara de fila de 'Otros y Respi')
        "SBOR":  med & si("SBOR_p") & si("SBOR_rec") & nn("SBOR_grav") & est("SBOR_est"),
        "ASMA":  med & si("ASMA_p") & nn("ASMA_grav") & nn("ASMA_ctrl") & est("ASMA_est"),
        "EPOC":  med & si("EPOC_p") & nn("EPOC_tipo") & nn("EPOC_ctrl") & est("EPOC_est"),
        "O2":    si("O2_p") & est("O2_est"),                    # DAX O2: NO exige médico
        "AV":    si("AV_p") & nn("AV_val") & est("AV_est"),      # DAX AV: NO exige médico
        "FQ":    med & si("FQ_p") & est("FQ_est"),
        "OTRAS": med & si("OTRAS_p") & est("OTRAS_est"),
    }
    fv = {k: set(o.loc[m, "RUN"]) for k, m in valid.items()}

    def last_val(m, c):
        s = o.loc[m, ["RUN", "FECHA", c]].sort_values("FECHA")
        return s.groupby("RUN")[c].last()
    gsbor = last_val(valid["SBOR"], "SBOR_grav")
    gasma = last_val(valid["ASMA"], "ASMA_grav")
    tepoc = last_val(valid["EPOC"], "EPOC_tipo")

    am = aten[es_medico(aten["INSTR_n"])]
    adx = lambda code: set(am.loc[am["DIAG_n"].str.contains(norm(code), regex=False, na=False), "RUN"])
    edx = (lambda code: set(estrat.index[estrat.str.contains(norm(code), regex=False, na=False)])) \
          if len(estrat) else (lambda code: set())

    e = edad
    lt5 = set(e.index[(e < 5).fillna(False)])
    ge40 = set(e.index[(e >= 40).fillna(False)])

    sbor = (adx("bronquial obstructivo recurrente") | edx("bronquial obstructivo recurrente") | fv["SBOR"]) & lt5
    asma = (adx("J45") | edx("J45") | fv["ASMA"]) - sbor            # asma requiere SBOR=NO
    epoc = (adx("J44") | edx("J44") | fv["EPOC"]) & ge40
    fq   = adx("E84") | edx("E84") | fv["FQ"]
    ing  = (fv["SBOR"] & lt5) | (fv["ASMA"] - sbor) | (fv["EPOC"] & ge40) | fv["OTRAS"] | fv["O2"] | fv["AV"] | fv["FQ"]

    def cs(runs): return pd.Series(idx.isin(runs), index=idx).map({True: "SI", False: "NO"})
    s = pd.DataFrame(index=idx)
    s["SALA Ingresado"] = cs(ing)
    s["SALA SBOR"] = cs(sbor); s["SALA ASMA"] = cs(asma); s["SALA EPOC"] = cs(epoc)
    s["SALA FQ"] = cs(fq); s["SALA Otras Respi"] = cs(fv["OTRAS"])
    s["SALA O2 Dependiente"] = cs(fv["O2"]); s["SALA Asistencia Ventilatoria"] = cs(fv["AV"])
    # 'Pertenece a SALA' = OR de los 7 flags (DAX del PowerBI). Es el FILTRO base de la
    # tabla 'Ferrada': el A23 se reporta SOLO sobre quienes están bajo control en sala.
    pert = sbor | asma | epoc | fq | fv["OTRAS"] | fv["O2"] | fv["AV"]
    s["Pertenece a SALA"] = cs(pert)
    s["SALA SBOR Gravedad"] = _gate(idx, sbor, gsbor)
    s["SALA ASMA Gravedad"] = _gate(idx, asma, gasma)
    s["SALA EPOC Tipo"] = _gate(idx, epoc, tepoc)
    return s, ing


# -- Sección G: INASISTENTES A CONTROL DE CRÓNICOS (del formulario Otros y Respi) --
# Def. REM (comentario A23 B78-83): paciente con formulario válido (¿Padece?=Si +
# Estado ingreso/reingreso/seguimiento) cuya ÚLTIMA 'Fecha del Próximo Control' está
# vencida > umbral por edad al CORTE (último día del mes reportado). NO usa el reporte
# de inasistencias (eso es la Sección H). Población = todos los crónicos del formulario.
_G_COND = [
    ("SBOR", "S.B.O. recurrente"), ("DISP", "Displasia broncopulmonar"),
    ("FQ", "Fibrosis quística"), ("ASMA", "Asma"),
    ("EPOC", "Enfermedad Pulmonar Obstructiva Crónica"), ("OTRAS", "Otras respiratorias crónicas"),
]
_UMBRAL = {0: (2, 29), 1: (5, 29)}   # (meses, días) de gracia; <1año / 12-23m ; >=2 años -> (11, 29)
_UMBRAL_ADULTO = (11, 29)


def _seccion_g(otros, corte, edad_extra=None, sin_edad=None):
    """Devuelve (conteos_por_dx_y_sexo, flags_por_RUN). `corte` = último día del
    mes reportado. Edad y sexo salen del propio formulario (población crónica completa).

    Sin FECHA DE NACIMIENTO legible en el formulario, la edad se toma de `edad_extra`
    (Serie RUN -> edad al corte, p.ej. la del ADA). Si tampoco está ahí, el paciente
    NO se descarta: se usa el umbral de >=2 años (el único que difiere es el de <2) y
    su RUN se agrega a `sin_edad` (un set, si se pasa) para avisarlo. Antes se
    descartaba callado: un export sin esa columna daba la Sección G ENTERA en 0."""
    o = otros
    def N(k): return o[k].map(norm)
    med = o["_med"]
    si  = lambda k: N(k).eq("SI")
    est = lambda k: _any(N(k), ("INGRESO", "SEGUIMIENTO"))   # ver `_sala`
    ed = ((corte - pd.to_datetime(o["FNAC_o"], errors="coerce", dayfirst=True)).dt.days // 365.25)
    edad_run = ed.groupby(o["RUN"]).max()
    if edad_extra is not None:
        edad_run = edad_run.fillna(pd.to_numeric(edad_extra, errors="coerce")
                                   .astype("float64").reindex(edad_run.index))
    sexo_run = o.groupby("RUN")["SEXO_o"].agg(lambda s: next((x for x in s if str(x).strip()), ""))

    counts, flags = {}, {}
    for pref, lbl in _G_COND:
        valid = med & si(pref + "_p") & est(pref + "_est")
        if pref == "SBOR":                       # S.B.O.: además exige recurrente (DAX)
            valid = valid & si("SBOR_rec")
        prox = pd.to_datetime(o[pref + "_prox"], errors="coerce", dayfirst=True)
        ult = (o.loc[valid, ["RUN"]].assign(p=prox[valid]).dropna(subset=["p"])
                 .sort_values("p").groupby("RUN")["p"].last())
        s = set()
        for run, p in ult.items():
            e = edad_run.get(run)
            if pd.isna(e):
                if sin_edad is not None:
                    sin_edad.add(run)
                m, dd = _UMBRAL_ADULTO
            else:
                m, dd = _UMBRAL.get(int(e), _UMBRAL_ADULTO)
            if corte > p + pd.DateOffset(months=m, days=dd):
                s.add(run)
        flags[pref] = s
        muj = sum(1 for r in s if _mujer(sexo_run.get(r, "")))
        hom = sum(1 for r in s if _hombre(sexo_run.get(r, "")))
        counts[lbl] = {"Hombre": hom, "Mujer": muj, "Total": len(s)}
    return counts, flags


# -- Sección H: INASISTENTES A CITACIÓN AGENDADA (del reporte NSP) --
# Citas Control/Ingreso IRA/ERA (NO KTR) que el paciente NO asistió (NSP), por
# estamento (Médico/Kinesiólogo/Enfermera) y tramo etario (<20 / >=20). Conteo por
# CITA (cada fila = una inasistencia). Mes por FECHA HORA CITA (no fecha NSP).
# Dos formatos, verificados contra refs_tablas/ (ronda 11): IRIS 'Pacientes Inasistentes'
# y el Administrativo 'Monitoreo de Inasistentes' (RUN, FECHA CITA, EDAD en vez de AÑOS;
# la edad puede venir en texto '55 años 3 meses' -> edad_anios en el loader).
MAPA_NSP = {
    "RUN":   [("subs", ["NUMERO", "IDENTIFICACION"]), ("exact", "RUN")],
    "INSTR": ("exact", "INSTRUMENTO"),
    "TIPO":  ("subs", ["TIPO", "ATENCION"]),
    "FECHA": [("subs", ["FECHA", "HORA", "CITA"]), ("exact", "FECHA CITA")],
    "ANOS":  [("exact", "AÑOS"), ("exact", "EDAD")],
}
_H_ESTAM = [("Médico/a", "MEDICO"), ("Kinesiólogo/a", "KINE"), ("Enfermera/o", "ENFERMER")]


def cargar_inasistentes(entrada, log=print):
    """Reporte NSP ('pacientes inasistentes') -> DataFrame + FECHA CITA parseada."""
    # Todo lo que la Seccion H usa es requerido: sin TIPO o INSTRUMENTO la H daba 0
    # callada (otro reporte de citas cargado por error), y sin AÑOS todas las
    # inasistencias caian en '20 y mas' (NaN < 20 es False).
    d, _col = cargar_canonico(entrada, lambda h: resolver_columnas(h, MAPA_NSP),
                              requeridas=("FECHA", "TIPO", "INSTR", "ANOS"), log=log)
    d["FECHA"] = fecha_col(d["FECHA"], log, "FECHA HORA CITA (NSP)")
    d["ANOS"] = d["ANOS"].map(edad_anios)   # numero (IRIS) o '55 años 3 meses' (Admin)
    d["TIPO_n"] = d["TIPO"].map(norm)
    d["INSTR_n"] = d["INSTR"].map(norm)
    return d


def _seccion_h(nsp, ini, fin):
    """Inasistencias a citas Control/Ingreso IRA/ERA del mes, por estamento × tramo
    (<20 / >=20). Devuelve DataFrame con la forma del template (Sección H)."""
    # El mes se guarda (NSP de otro período = archivo equivocado); el filtro
    # Control/Ingreso IRA/ERA va DESPUÉS y sí puede dejar 0 (legítimo).
    m = filtrar_mes(nsp, ini, fin, "el reporte NSP (inasistentes a citación)")
    t = m["TIPO_n"]
    resp = (t.str.contains(r"\b(?:CONTROL|INGRESO)\b", regex=True, na=False) &
            t.str.contains(r"\b(?:IRA|ERA)\b", regex=True, na=False))    # excluye KTR (sin control/ingreso)
    m = m[resp]
    edad = pd.to_numeric(m["ANOS"], errors="coerce")
    men20 = edad < 20
    filas, tmen, tmay = [], 0, 0
    for lbl, key in _H_ESTAM:
        est = m["INSTR_n"].str.contains(key, regex=False, na=False)
        nm, ny = int((est & men20).sum()), int((est & ~men20).sum())
        filas.append({"Profesional": lbl, "Total": nm + ny, "Menor de 20": nm, "20 y más": ny})
        tmen += nm; tmay += ny
    filas.append({"Profesional": "TOTAL", "Total": tmen + tmay, "Menor de 20": tmen, "20 y más": tmay})
    out = pd.DataFrame(filas)
    # Sin AÑOS legible la cita cae en '20 y mas' (NaN < 20 es False): se cuenta para
    # que procesar lo avise, en vez de repartirla callada en el tramo equivocado.
    out.attrs["sin_edad"] = int(edad.isna().sum())
    return out


# -- Tablas agregadas edad×sexo (forma exacta del template SA_26, hoja A23) --
# Bandas del template (fila 10): Menor de 1 · 1-4 · 5-9 · … · 80 y más (18 bandas).
# `grid()` emite Ambos·Hombres·Mujeres + por banda H/M, EN EL ORDEN de las columnas
# del SA_26 -> copy-paste directo (la etiqueta va en la col 1).
LBL_A23 = ["Menor de 1", "1-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34",
           "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74",
           "75-79", "80+"]
BANDAS_A23 = [(0, 0), (1, 4), (5, 9), (10, 14), (15, 19), (20, 24), (25, 29), (30, 34),
              (35, 39), (40, 44), (45, 49), (50, 54), (55, 59), (60, 64), (65, 69),
              (70, 74), (75, 79), (80, 200)]


def _tablas_a23(fer):
    """Construye las tablas por sección (edad×sexo) con la forma del SA_26. PROTOTIPO:
    cubre las secciones cuyo indicador por-RUN ya existe y es 1:1. Filas sin fuente
    fiable (o de otra forma) van en 0 y ANOTADAS para validar 1:1 contra el PowerBI:
    A (semántica 'ingreso a sala' != 'tuvo dx'), I espirometría basal/post BD (hoy 1
    indicador), y O (forma EPOC A/B) -> pendientes. B/C/P/Q/M.2/J/K/L fuera de alcance."""
    import pandas as pd

    # FILTRO base del PowerBI: el A23 se reporta SOLO sobre quienes 'Pertenecen a SALA'
    # (bajo control). Sin el formulario Otros y Respi no hay flags -> no se puede filtrar.
    if "Pertenece a SALA" in fer.columns:
        fer = fer[fer["Pertenece a SALA"].eq("SI")]

    def sub(mask):
        s = fer.loc[mask, ["Edad", "Sexo"]] if mask is not None else fer.iloc[0:0][["Edad", "Sexo"]]
        return s.rename(columns={"Edad": "edad", "Sexo": "sexo"})

    def g(ind):   # grid del indicador SI/NO (o zeros si la columna no existe)
        m = fer[ind].eq("SI") if ind in fer.columns else None
        return _grid(sub(m), BANDAS_A23, LBL_A23)

    def gmask(mask):
        return _grid(sub(mask), BANDAS_A23, LBL_A23)

    cero = _grid(sub(None), BANDAS_A23, LBL_A23)

    def fila(nombre, datos):
        return {"Concepto": nombre, **datos}

    tablas = {}

    # SECCIÓN D — Consultas de morbilidad en salas (solo médico)
    tablas["A23_D_Morbilidad"] = pd.DataFrame([fila("Médico/a", g("REMA23 Morbi respiratoria"))])

    # SECCIÓN E — Controles crónicos (Enfermera/o NO existe -> 0; ver reglas)
    med = fer["REMA23 Control SALA Med (act)"].eq("SI")
    kin = fer["REMA23 Control SALA Kine (act)"].eq("SI")
    tablas["A23_E_Controles_Cronicos"] = pd.DataFrame([
        fila("Médico/a", gmask(med)),
        fila("Enfermera/o", cero),                        # no existe control de enfermería
        fila("Kinesiólogo/a", gmask(kin)),
        fila("TOTAL", gmask(med | kin))])

    # SECCIÓN F — Seguimiento en agudos
    eu = fer["REMA23 Seguimiento Eu"].eq("SI")
    ki = fer["REMA23 Seguimiento Kine"].eq("SI")
    tablas["A23_F_Seguimiento_Agudos"] = pd.DataFrame([
        fila("Enfermera/o", gmask(eu)),
        fila("Kinesiólogo/a", gmask(ki)),
        fila("TOTAL", gmask(eu | ki))])

    # SECCIÓN I — Procedimientos (espirometría basal/post BD: HOY un solo indicador ->
    # va todo a 'basal', post BD queda 0 PENDIENTE de split por texto de actividad).
    tablas["A23_I_Procedimientos"] = pd.DataFrame([
        fila("Espirometría basal", g("REMA23 Espirometría (act)")),
        fila("Espirometría post BD  (PENDIENTE split)", cero),
        fila("Flujometría basal", cero), fila("Flujometría post BD", cero),
        fila("Pimometría", cero), fila("Test de provocación con ejercicio", cero),
        fila("Test de marcha 6 minutos", cero),
        fila("Sesiones de kinesioterapia respiratoria", g("REMA23 KTR")),
        fila("Toma de muestra secreción mucosa/bronquial", cero)])

    # SECCIÓN M.1 — Educación individual en sala
    m1 = [("Antitabaco", "REMA23 Educación Antitabaco"),
          ("Autocuidado según patología", "REMA23 Autocuidado"),
          ("Uso de terapia inhalatoria", "REMA23 Inhaloterapia"),
          ("Educacion integral en salud respiratoria", "REMA23 Edu Integral Sala"),
          ("Estilo de vida saludables", "REMA23 Vida Saludable"),
          ("Otras", "REMA23 Otras")]
    filas_m1 = [fila(lbl, g(ind)) for lbl, ind in m1]
    tot_m1 = fer[[i for _, i in m1]].eq("SI").any(axis=1)
    filas_m1.append(fila("TOTAL", gmask(tot_m1)))
    tablas["A23_M1_Educacion_Individual"] = pd.DataFrame(filas_m1)

    # SECCIÓN N — Visitas domiciliarias (solo 'Otras visitas' desde VDI Respi; resto
    # sin fuente -> 0). VDI Respi existe solo si se cargó el formulario Otros y Respi.
    tablas["A23_N_Visitas"] = pd.DataFrame([
        fila("Hogar libre del humo del tabaco", cero),
        fila("Por muerte de neumonía en domicilio", cero),
        fila("Programa oxigenoterapia ambulatoria, AVNI, AVI, AVNIA, AVIA", cero),
        fila("Seguimiento telefónico realizado por kinesiologo sala", cero),
        fila("Otras visitas", g("REMA23 VDI Respi"))])

    # SECCIÓN A — Ingresos agudos por diagnóstico. PROTOTIPO: mapea los dx directos
    # que ya tenemos; el resto (Otras IRAS bajas, exacerbación SBOR/Asma/FQ/otras) va 0.
    # OJO semántico: A es 'INGRESO agudo derivado a sala', no 'tuvo una atención con
    # ese dx' -> VALIDAR 1:1 contra el PowerBI antes de confiar.
    a_dx = [("I.R.A. alta", "REMA23 Ira Alta"), ("Influenza", "REMA23 Influenza"),
            ("Neumonía", "REMA23 Neumonia"), ("Coqueluche", "REMA23 Coqueluche"),
            ("Bronquitis obstructiva aguda", "REMA23 Bronquitis Aguda")]
    filas_a = [fila(lbl, g(ind)) for lbl, ind in a_dx]
    filas_a += [fila("Otras IRAS bajas", cero),
                fila("Exacerbación síndrome bronquial obstructivo recurrente (SBOR)", cero),
                fila("Exacerbación Asma  (PENDIENTE: confirmado + J09-J22)", cero),
                fila("Exacerbación de enfermedad pulmonar obstructiva crónica (EPOC)",
                     g("REMA23 EPOC Exacerbado")),
                fila("Exacerbación fibrosis quística", cero),
                fila("Exacerbación otras respiratorias crónicas", cero)]
    tablas["A23_A_Ingresos_Agudos"] = pd.DataFrame(filas_a)

    return tablas


def escribir(fer, salida):
    """Escribe el DETALLE por paciente (paso intermedio, siempre disponible) + una
    hoja POR SECCIÓN del REM A23 (forma copy-paste al SA_26) + las Secciones G y H
    agregadas, en un solo .xlsx."""
    from programas import cobertura
    contexto = {"mes": fer.attrs.get("mes"), "archivos": fer.attrs.get("fuentes")}
    with pd.ExcelWriter(salida) as xw:
        cobertura.escribir_hoja(xw.book, "a23_respiratorio", contexto,
                                avisos=fer.attrs.get("avisos", ()))
        # Detalle: RUN, luego 'Pertenece a SALA' y '¿Atendido 1 mes?' al frente (col 2 y
        # 3) para revisar de un vistazo, y el resto en su orden.
        frente = [c for c in ("Pertenece a SALA", "¿Atendido 1 mes?") if c in fer.columns]
        orden = [fer.columns[0]] + frente + [c for c in fer.columns[1:] if c not in frente]
        fer[orden].to_excel(xw, index=False, sheet_name="A23_Detalle")
        # Una hoja por sección (edad×sexo), forma copy-paste al SA_26.
        for nombre, df in _tablas_a23(fer).items():
            df.to_excel(xw, index=False, sheet_name=nombre[:31])
        g = fer.attrs.get("seccion_g")
        if g:
            (pd.DataFrame(g).T.reset_index().rename(columns={"index": "Diagnóstico"})
             .to_excel(xw, index=False, sheet_name="A23_Seccion_G"))
        h = fer.attrs.get("seccion_h")
        if h is not None:
            h.to_excel(xw, index=False, sheet_name="A23_Seccion_H")
    return str(salida)
