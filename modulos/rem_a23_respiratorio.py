#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 1.8.1
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
edad×sexo; admin es PARCIAL (los dx por código ICD no vienen → Ira Alta/Bronquitis/
EPOC exac. = 0, ver rem_utils.MAPA_ATENCIONES) + formulario Otros Crónicos admin.
"""

import pandas as pd

from programas.rem_utils import (norm, leer_xlsx, cargar_atenciones, cargar_canonico,
                                 resolver_columnas, contiene_todos as _all,
                                 contiene_alguno as _any, _rango_mes, _mujer, _hombre,
                                 grid as _grid, fecha_col, PUEBLO_VACIO, indice_col)
# cargar_atenciones (IRIS | Monitoreo admin) vive en rem_utils y se reexporta acá.


_SALA_IRA = ["control sala (ira", "consulta sala (ira", "kinesioterapi"]

# ── PRE-ESCRITO (NO activo): Educación GRUPAL A23·M.2 — talleres respiratorios ──
# Estado ago-2026: los talleres grupales AÚN NO se hacen en el CESFAM → nada que
# contar hoy. Se esperan en ~2 meses (Simón envió las actividades candidatas al RT
# de Respiratorio). La lógica es CASI IDÉNTICA a rem_sm_actividades: conteo por
# ASISTENCIA del reporte 'Atenciones Grupales' (cada fila Asiste=SI, SIN dedup) →
# A23·M.2 (Nº sesiones = grupos distintos; Nº participantes = asistencias). Ver
# docs/A23_P3_plan.md ("Educación grupal M.2").
#
# Hallazgo Maestro (ago-2026): hoy TODO lo grupal respiratorio cae a REM-Gestion
# (no tributa). Al activarse, estas deberían apuntar a A23·M.2 (o reclasificarse en
# el Maestro); mientras tanto caen a 'saco vacío' (las caza Trabajo perdido):
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
# _masks_simples y A23·N VDI Hogar Libre de Humo) → no duplicar.


def _masks_simples(d):
    """dict indicador -> máscara BOOLEANA por fila (atención del mes)."""
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
    'Otros y Respi' + 'Estratificación' → agregan SALA bajo control + Sección G.
    `inasistentes` (opcional) = reporte NSP → Sección H (citas Control/Ingreso
    IRA/ERA no asistidas, por estamento × tramo etario)."""
    d = cargar_atenciones(entrada, log=log)
    ini, fin = _rango_mes(mes)
    span_min, span_max = d["FECHA"].min(), d["FECHA"].max()
    log(f"[a23] {len(d)} atenciones | datos {span_min:%Y-%m-%d}..{span_max:%Y-%m-%d} "
        f"| mes reporte {ini:%Y-%m}")

    runs = pd.Index(d["RUN"].unique(), name="RUN")
    fer = pd.DataFrame(index=runs)

    dm = d[(d["FECHA"] >= ini) & (d["FECHA"] <= fin)]          # atenciones del mes
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

    # ── Fase 2: SALA bajo control (si se dieron los inputs) ──
    if otros is not None:
        od, _ = cargar_otros(otros)
        # Sección G solo sirve con historial largo: el inasistente tiene su ÚLTIMO
        # formulario/control hace >1 año. El reporte 'Otros y Respi' se baja POR AÑO
        # calendario, así que reportar un mes exige AL MENOS el año del reporte + el
        # anterior (12 meses atrás). Fail loud si el historial no llega tan atrás
        # (chequeo por FECHA MÍNIMA, no por span: un solo año da ~365 días pero igual
        # deja fuera el año previo).
        if od["FECHA"].notna().any():
            limite = ini - pd.DateOffset(months=12)   # G mira ≥12 meses hacia atrás
            if od["FECHA"].min() > limite:
                log(f"[a23] ⚠⚠ Sección G SUBCONTARÁ: los formularios 'Otros y Respi' "
                    f"arrancan en {od['FECHA'].min():%Y-%m}, pero el mes reportado "
                    f"({ini:%Y-%m}) necesita historial hasta {limite:%Y-%m}. Como el "
                    f"reporte se baja POR AÑO, carga AMBOS: el año del reporte Y el "
                    f"ANTERIOR (ideal 5, como el PowerBI). Selecciónalos juntos (ctrl-click).")
        est = cargar_estrat(estrat) if estrat is not None else pd.Series(dtype="object")
        sala, _ing = _sala(fer.index, fer["Edad"], d, od, est)
        for c in sala.columns:
            fer[c] = sala[c]
        vdi = fer.pop("REMA23 VDI Respi (aten)").eq("SI") & fer["SALA Ingresado"].eq("SI")
        fer["REMA23 VDI Respi"] = vdi.map({True: "SI", False: "NO"})
        om = od[(od["FECHA"] >= ini) & (od["FECHA"] <= fin)]
        cdv = om.sort_values("FECHA").groupby("RUN")["CDV"].last()
        fer["REMA23 Encuesta calidad de vida"] = cdv.reindex(fer.index).fillna("")
        log(f"[a23] SALA Ingresado={(fer['SALA Ingresado']=='SI').sum()} | "
            f"ASMA={(fer['SALA ASMA']=='SI').sum()} EPOC={(fer['SALA EPOC']=='SI').sum()} "
            f"SBOR={(fer['SALA SBOR']=='SI').sum()} FQ={(fer['SALA FQ']=='SI').sum()} "
            f"Otras={(fer['SALA Otras Respi']=='SI').sum()}")
        # Sección G: inasistentes a control de crónicos (corte = último día del mes)
        gcounts, gflags = _seccion_g(od, fin)
        for pref, _lbl in _G_COND:
            fer["Inasistente " + pref] = pd.Series(fer.index.isin(gflags[pref]), index=fer.index).map({True: "SI", False: "NO"})
        fer.attrs["seccion_g"] = gcounts
        log("[a23] Sección G inasistentes crónicos: " + " · ".join(
            f"{lbl.split()[0]}={d['Total']}" for lbl, d in gcounts.items()))

    # ── Sección H: inasistentes a citación agendada (reporte NSP, independiente) ──
    if inasistentes is not None:
        nsp = cargar_inasistentes(inasistentes, log=log)
        h = _seccion_h(nsp, ini, fin)
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


# ╔═══════════════════════════════════════════════════════════════════╗
# ║  FASE 2 — SALA bajo control (formulario 'Otros y Respi' + Estratif) ║
# ╚═══════════════════════════════════════════════════════════════════╝


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

    return {
        "RUN": find("NUMERO", "IDENTIFICACION"), "FECHA": find("FECHA ATENCION"),
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


def cargar_otros(entrada):
    """Formulario(s) Otros y Respi -> DataFrame canónico + FECHA. `entrada` puede ser
    una ruta o una lista (varios años: la Sección G / SALA necesitan el histórico)."""
    d, col = cargar_canonico(entrada, None, _resolver_otros)
    d["FECHA"] = pd.to_datetime(d["FECHA"], errors="coerce", dayfirst=True)
    d["_med"] = d["INSTR"].map(norm).str.contains("MEDIC", regex=False, na=False)
    return d, col


def cargar_estrat(entrada):
    """DataFrame de Estratificación: RUN (=RUT-DV) -> Diagnósticos (normalizado)."""
    hdr, filas = leer_xlsx(entrada)
    hn = [norm(h) for h in hdr]
    i_rut, i_dv = indice_col(hn, "RUT"), indice_col(hn, "DV")
    i_dg = indice_col(hn, "DETALLE", "DIAGNOSTICOS") or indice_col(hn, "CONDICIONES CRONICAS")
    run = [f"{f[i_rut]}-{f[i_dv]}" if i_dv is not None and f[i_rut] not in (None, "") else str(f[i_rut])
           for f in filas]
    dg = [norm(f[i_dg]) if i_dg is not None else "" for f in filas]
    return pd.DataFrame({"RUN": run, "DIAG": dg}).drop_duplicates("RUN").set_index("RUN")["DIAG"]


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
    est = lambda k: N(k).str.contains("INGRESO", na=False) | N(k).str.contains("SEGUIMIENTO", na=False)

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

    am = aten[aten["INSTR_n"].str.contains("MEDIC", regex=False, na=False)]
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


# ── Sección G: INASISTENTES A CONTROL DE CRÓNICOS (del formulario Otros y Respi) ──
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


def _seccion_g(otros, corte):
    """Devuelve (conteos_por_dx_y_sexo, flags_por_RUN). `corte` = último día del
    mes reportado. Edad y sexo salen del propio formulario (población crónica completa)."""
    o = otros
    def N(k): return o[k].map(norm)
    med = o["_med"]
    si  = lambda k: N(k).eq("SI")
    est = lambda k: N(k).str.contains("INGRESO", na=False) | N(k).str.contains("SEGUIMIENTO", na=False)
    ed = ((corte - pd.to_datetime(o["FNAC_o"], errors="coerce", dayfirst=True)).dt.days // 365.25)
    edad_run = ed.groupby(o["RUN"]).max()
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
                continue
            m, dd = _UMBRAL.get(int(e), (11, 29))
            if corte > p + pd.DateOffset(months=m, days=dd):
                s.add(run)
        flags[pref] = s
        muj = sum(1 for r in s if _mujer(sexo_run.get(r, "")))
        hom = sum(1 for r in s if _hombre(sexo_run.get(r, "")))
        counts[lbl] = {"Hombre": hom, "Mujer": muj, "Total": len(s)}
    return counts, flags


# ── Sección H: INASISTENTES A CITACIÓN AGENDADA (del reporte NSP) ──
# Citas Control/Ingreso IRA/ERA (NO KTR) que el paciente NO asistió (NSP), por
# estamento (Médico/Kinesiólogo/Enfermera) y tramo etario (<20 / >=20). Conteo por
# CITA (cada fila = una inasistencia). Mes por FECHA HORA CITA (no fecha NSP).
MAPA_NSP = {
    "RUN":   [("subs", ["NUMERO", "IDENTIFICACION"])],
    "INSTR": ("exact", "INSTRUMENTO"),
    "TIPO":  ("subs", ["TIPO", "ATENCION"]),
    "FECHA": ("subs", ["FECHA", "HORA", "CITA"]),
    "ANOS":  ("exact", "AÑOS"),
}
_H_ESTAM = [("Médico/a", "MEDICO"), ("Kinesiólogo/a", "KINE"), ("Enfermera/o", "ENFERMER")]


def cargar_inasistentes(entrada, log=print):
    """Reporte NSP ('pacientes inasistentes') -> DataFrame + FECHA CITA parseada."""
    d, _col = cargar_canonico(entrada, None, lambda h: resolver_columnas(h, MAPA_NSP))
    d["FECHA"] = fecha_col(d["FECHA"], log, "FECHA HORA CITA (NSP)")
    d["TIPO_n"] = d["TIPO"].map(norm)
    d["INSTR_n"] = d["INSTR"].map(norm)
    return d


def _seccion_h(nsp, ini, fin):
    """Inasistencias a citas Control/Ingreso IRA/ERA del mes, por estamento × tramo
    (<20 / >=20). Devuelve DataFrame con la forma del template (Sección H)."""
    m = nsp[(nsp["FECHA"] >= ini) & (nsp["FECHA"] <= fin)]
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
    return pd.DataFrame(filas)


# ── Tablas agregadas edad×sexo (forma exacta del template SA_26, hoja A23) ──
# Bandas del template (fila 10): Menor de 1 · 1-4 · 5-9 · … · 80 y más (18 bandas).
# `grid()` emite Ambos·Hombres·Mujeres + por banda H/M, EN EL ORDEN de las columnas
# del SA_26 → copy-paste directo (la etiqueta va en la col 1).
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
    A (semántica 'ingreso a sala' ≠ 'tuvo dx'), I espirometría basal/post BD (hoy 1
    indicador), y O (forma EPOC A/B) → pendientes. B/C/P/Q/M.2/J/K/L fuera de alcance."""
    import pandas as pd

    # FILTRO base del PowerBI: el A23 se reporta SOLO sobre quienes 'Pertenecen a SALA'
    # (bajo control). Sin el formulario Otros y Respi no hay flags → no se puede filtrar.
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

    # SECCIÓN E — Controles crónicos (Enfermera/o NO existe → 0; ver reglas)
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

    # SECCIÓN I — Procedimientos (espirometría basal/post BD: HOY un solo indicador →
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
    # sin fuente → 0). VDI Respi existe solo si se cargó el formulario Otros y Respi.
    tablas["A23_N_Visitas"] = pd.DataFrame([
        fila("Hogar libre del humo del tabaco", cero),
        fila("Por muerte de neumonía en domicilio", cero),
        fila("Programa oxigenoterapia ambulatoria, AVNI, AVI, AVNIA, AVIA", cero),
        fila("Seguimiento telefónico realizado por kinesiologo sala", cero),
        fila("Otras visitas", g("REMA23 VDI Respi"))])

    # SECCIÓN A — Ingresos agudos por diagnóstico. ⚠ PROTOTIPO: mapea los dx directos
    # que ya tenemos; el resto (Otras IRAS bajas, exacerbación SBOR/Asma/FQ/otras) va 0.
    # OJO semántico: A es 'INGRESO agudo derivado a sala', no 'tuvo una atención con
    # ese dx' → VALIDAR 1:1 contra el PowerBI antes de confiar.
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
    with pd.ExcelWriter(salida) as xw:
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
