# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# SPDX-License-Identifier: GPL-3.0-or-later
# ==========================================================================
"""CONTRATOS de las fuentes externas (exports RAYEN/IRIS y reportes): cada funcion que
lee una planilla del usuario declara aca como se la llama y una fila VALIDA, y el arnes
la ataca con las formas del bug recurrente de c38a8cc (revision gui-2.0, rondas 1-10):

  C0  fila valida sobre el encabezado REAL           -> carga y trae datos
  C1  solo el encabezado (0 filas)                   -> ArchivoInvalido, no AttributeError/0
  C3  una columna critica renombrada                 -> ArchivoInvalido, nunca un fallback
  C4  filas, pero la columna clave vacia en todas    -> ArchivoInvalido ("vacio TRAS filtrar")
  C5  todas las fechas ilegibles                     -> ArchivoInvalido, no NaT callado
  C6  una columna EXTRA al inicio (todo corrido 1)  -> el MISMO resultado (caza el fallback
                                                        POR POSICION, como la col 11 del A05)
  X   casos propios del contrato (`extra`)           -> ArchivoInvalido (filtros del modulo)

El encabezado sale de `refs_tablas/<ref>` (el export REAL recortado a solo encabezado,
skill `limpiar-refs`). Sin referencia, el contrato declara uno SINTETICO y el reporte
lo avisa: hay que pedirle el export al autor.

Esto NO se corre entero en cada commit: `tools/check_fuentes.py` (pre-commit) corre solo
los contratos cuyas funciones (`cubre`) toco el commit, y BLOQUEA si el commit agrega o
cambia un lector de planillas que no tiene contrato. Cómo escribir uno: skill
`tests-fuentes` (.claude/skills/tests-fuentes/SKILL.md).

Datos SINTETICOS: el RUT de ejemplo es 11111111-1 (CLAUDE.md regla 1)."""

import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _aislar_cache   # noqa: E402,F401  (PRIMERO: nunca tocar el ~/.autorem real)

import openpyxl                                         # noqa: E402

from programas.rem_utils import ArchivoInvalido         # noqa: E402

REFS = REPO / "refs_tablas"
_TMP = Path(tempfile.mkdtemp(prefix="autorem_contratos_"))
MES = (2026, 8)
RUT = "11111111-1"


def _q(*_a, **_k):
    pass


@dataclass
class Contrato:
    id: str
    cubre: tuple            # "ruta.py::funcion" -- si el commit las toca, corre este contrato
    llamar: object          # ruta -> salida: lo que hace TODO consumidor con el archivo
    fila: dict              # UNA fila valida, por NOMBRE EXACTO de columna del encabezado
    ref: str = None         # archivo de refs_tablas/ (encabezado REAL + banner)
    encabezado: tuple = ()  # sin `ref`: encabezado SINTETICO (se avisa)
    banner: tuple = ()      # sin `ref`: filas sobre el encabezado
    criticas: tuple = ()    # C3: renombrar cada una tiene que fallar
    clave: tuple = ()       # C4: vacias en todas las filas tiene que fallar
    fechas: tuple = ()      # C5: ilegibles en todas las filas tiene que fallar
    extra: tuple = ()       # X: (etiqueta, [filas]) que tienen que fallar
    errores: tuple = (ArchivoInvalido,)   # excepciones que cuentan como "fallo claro"
    valida: object = None   # salida de C0 -> bool (por defecto: no vacia)
    conocidos: dict = field(default_factory=dict)   # chequeo -> motivo (pendiente HONESTO)


# -- Fixtures -----------------------------------------------------------
def plantilla(c):
    """(banner, encabezado, pisos) del contrato: de la referencia real, o el sintetico.
    `pisos` = filas del encabezado bajo la principal (encabezado de dos pisos con celdas
    combinadas, como Utilizacion de Cupos). El encabezado se ubica con el MISMO criterio
    que `tools/limpiar_refs.py` usa para recortar la referencia: el banner va entero."""
    if not c.ref:
        return [list(f) for f in c.banner], list(c.encabezado), []
    from tools import limpiar_refs
    _t, filas, combinadas = limpiar_refs._leer(REFS / c.ref)[0]
    h = limpiar_refs._fila_header(filas)
    fin = limpiar_refs._fin_bloque(h, combinadas)
    hdr = list(filas[h - 1])
    while hdr and hdr[-1] in (None, ""):
        hdr.pop()
    return [list(f) for f in filas[:h - 1]], hdr, [list(f) for f in filas[h:fin]]


def escribir(ruta, banner, encabezado, filas, pisos=()):
    wb = openpyxl.Workbook()
    ws = wb.active
    for f in banner:
        ws.append(list(f))
    ws.append(list(encabezado))
    for f in pisos:
        ws.append(list(f))
    for f in filas:
        ws.append([f.get(h, "") for h in encabezado])
    wb.save(ruta)
    return ruta


# -- Comparacion de salidas -------------------------------------------
def firma(x):
    """Forma comparable de una salida (DataFrame, Series, dict, set, lista, tupla)."""
    import pandas as pd
    if isinstance(x, tuple):
        return firma(x[0])
    if isinstance(x, pd.DataFrame):
        d = x.reindex(sorted(x.columns, key=str), axis=1).astype(str)
        return sorted(map(tuple, d.values.tolist()))
    if isinstance(x, pd.Series):
        return sorted((str(k), str(v)) for k, v in x.items())
    if isinstance(x, dict):
        return sorted((str(k), repr(firma(v))) for k, v in x.items())
    if isinstance(x, (set, frozenset)):
        return sorted(map(str, x))
    if isinstance(x, list):
        return [firma(v) for v in x]
    return str(x)


def no_vacia(x):
    if isinstance(x, tuple):
        return no_vacia(x[0])
    try:
        return len(x) > 0
    except TypeError:
        return x is not None


# -- Arnes ----------------------------------------------------------------
def _debe_fallar(c, ruta):
    """(estado, detalle): OK si levanta uno de `c.errores`."""
    try:
        c.llamar(str(ruta))
    except c.errores as e:
        return "OK", f"{type(e).__name__}({getattr(e, 'categoria', '')})"
    except Exception as e:   # noqa: BLE001
        return "FALLA", f"crash CRIPTICO {type(e).__name__}: {str(e)[:120]}"
    return "FALLA", "siguio de largo sin error (un 0 o un vacio callado)"


def chequear(c):
    """Lista de (chequeo, estado, detalle) de UN contrato. Estados: OK · FALLA ·
    PENDIENTE (falla y esta en `conocidos`, con su motivo)."""
    banner, hdr, pisos = plantilla(c)
    faltan = [k for k in c.fila if k not in hdr]
    if faltan:
        return [("C0 fila valida", "FALLA",
                 f"la fila usa columnas que NO estan en el encabezado"
                 f"{' REAL' if c.ref else ''}: {faltan}")]
    carpeta = _TMP / "".join(ch if ch.isalnum() else "_" for ch in c.id)
    carpeta.mkdir(parents=True, exist_ok=True)
    res = []

    ruta = escribir(carpeta / "c0.xlsx", banner, hdr, [c.fila], pisos)
    base = None
    try:
        base = c.llamar(str(ruta))
        ok = (c.valida or no_vacia)(base)
        res.append(("C0 fila valida", "OK" if ok else "FALLA",
                    "" if ok else "cargo, pero la salida esta VACIA con una fila valida"))
    except Exception as e:   # noqa: BLE001
        res.append(("C0 fila valida", "FALLA",
                    f"no carga el encabezado{' REAL' if c.ref else ''}: "
                    f"{type(e).__name__}: {str(e)[:160]}"))

    res.append(("C1 solo encabezado",
                *_debe_fallar(c, escribir(carpeta / "c1.xlsx", banner, hdr, [], pisos))))
    for col in c.criticas:
        h2 = ["COLUMNA_RENOMBRADA" if h == col else h for h in hdr]
        f2 = {("COLUMNA_RENOMBRADA" if k == col else k): v for k, v in c.fila.items()}
        res.append((f"C3 sin '{col}'",
                    *_debe_fallar(c, escribir(carpeta / "c3.xlsx", banner, h2, [f2], pisos))))
    if c.clave:
        f4 = dict(c.fila, **{k: "" for k in c.clave})
        res.append((f"C4 {'/'.join(c.clave)} vacia",
                    *_debe_fallar(c, escribir(carpeta / "c4.xlsx", banner, hdr, [f4, f4], pisos))))
    if c.fechas:
        f5 = dict(c.fila, **{k: "no es fecha" for k in c.fechas})
        res.append((f"C5 {'/'.join(c.fechas)} ilegible",
                    *_debe_fallar(c, escribir(carpeta / "c5.xlsx", banner, hdr, [f5], pisos))))
    if base is not None:
        # Una columna EXTRA al inicio corre TODAS las posiciones en 1 y conserva el orden
        # relativo (en los formularios RAYEN el ESTADO va pegado a su pregunta, y eso SI
        # es estructura). Un indice fijo -- `ANIO_COL_FALLBACK = 11` del A05 -- lee otra
        # cosa; algo resuelto por nombre da lo mismo.
        h6 = ["COLUMNA_EXTRA"] + hdr
        f6 = dict(c.fila, COLUMNA_EXTRA="x")
        try:
            # MISMO nombre de archivo que el C0, en otra carpeta: hay salidas que llevan el
            # nombre adentro (el 'N°' del Monitoreo se namespacea con el archivo).
            (carpeta / "c6").mkdir(exist_ok=True)
            otra = c.llamar(str(escribir(carpeta / "c6" / "c0.xlsx", banner, h6, [f6],
                                         [[None] + p for p in pisos])))
            igual = firma(otra) == firma(base)
            res.append(("C6 columna extra al inicio", "OK" if igual else "FALLA",
                        "" if igual else "el resultado CAMBIA al correr las columnas una "
                        "posicion: algo se lee por INDICE FIJO, no por nombre"))
        except Exception as e:   # noqa: BLE001
            res.append(("C6 columna extra al inicio", "FALLA",
                        f"revienta al correr las columnas una posicion (indice fijo?): "
                        f"{type(e).__name__}: {str(e)[:120]}"))
    for etiqueta, filas in c.extra:
        res.append((f"X {etiqueta}",
                    *_debe_fallar(c, escribir(carpeta / "x.xlsx", banner, hdr, filas, pisos))))

    # Pendientes HONESTOS: un conocido que falla no bloquea; uno que YA pasa, si (hay
    # que sacarlo de `conocidos`, o dejaria de vigilar la regresion).
    out = []
    for chk, estado, det in res:
        motivo = next((m for k, m in c.conocidos.items() if chk.startswith(k)), None)
        if motivo and estado == "FALLA":
            out.append((chk, "PENDIENTE", f"{motivo} [{det}]"))
        elif motivo:
            out.append((chk, "FALLA", f"estaba en `conocidos` y YA PASA: sacarlo ({motivo})"))
        else:
            out.append((chk, estado, det))
    return out


def correr(ids=None, log=print):
    """Corre los contratos `ids` (todos si None). Devuelve el numero de FALLAS."""
    fallas = 0
    for c in CONTRATOS:
        if ids is not None and c.id not in ids:
            continue
        filas = chequear(c)
        malos = [f for f in filas if f[1] == "FALLA"]
        fallas += len(malos)
        pend = [f for f in filas if f[1] == "PENDIENTE"]
        log(f"[contrato] {c.id}: {len(filas) - len(malos) - len(pend)} OK"
            + (f", {len(pend)} pendiente(s)" if pend else "")
            + (f", {len(malos)} FALLA(S)" if malos else "")
            + ("" if c.ref else "   (encabezado SINTETICO: falta el export real en refs_tablas/)"))
        for chk, estado, det in filas:
            if estado != "OK":
                log(f"    {estado:<9} {chk}: {det}")
    return fallas


# =========================================================================
# REGISTRO. Uno por lector de planillas (o por pipeline, si el filtro que
# importa vive en el modulo). Agregar aca al crear o tocar uno: skill
# `tests-fuentes`. `cubre` usa rutas con '/' relativas a la raiz del repo.
# =========================================================================
def _poblacion():
    import programas.poblacion as pob
    return pob


def _a23():
    import modulos.rem_a23_respiratorio as a23
    return a23


def _a05(perfil_id):
    def llamar(ruta):
        import programas.rem_saludmental as sm
        import modulos.rem_a05_o_egresos as egresos
        perfil = sm.perfil_por_id(perfil_id)
        wb, ws = sm.abrir_validado(ruta, perfil)
        egresos.agregar_hoja(wb, ws, perfil, log=_q, mes=MES)
        filas = [list(r) for r in wb[egresos.NOMBRE_HOJA_SALIDA].iter_rows(values_only=True)]
        return filas[1:]   # sin el encabezado de la hoja de salida
    return llamar


def _a03(instrumento):
    def llamar(ruta):
        import modulos.rem_a03_d3_instrumentos as scr
        return scr.procesar(ruta, salida=None, instrumento=instrumento, log=_q)
    return llamar


def _seccion_h(ruta):
    import pandas as pd
    a23 = _a23()
    return a23._seccion_h(a23.cargar_inasistentes(ruta, log=_q),
                          pd.Timestamp(2026, 8, 1), pd.Timestamp(2026, 8, 31))


_OTROS = ("modulos/rem_a23_respiratorio.py::cargar_otros",
          "modulos/rem_a23_respiratorio.py::_resolver_otros",
          "modulos/rem_a23_respiratorio.py::_estamento_por_funcionario")


def _otros(ruta):
    """Lo que hace el A23 con el formulario: cargarlo y, si no trae INSTRUMENTO
    (Administrativo), resolver el estamento por funcionario. Sin atenciones ni cache
    (los tests aislan el cache) = no se resuelve ninguno = tiene que fallar."""
    import pandas as pd
    od, _col = _a23().cargar_otros(ruta, log=_q)
    _a23()._estamento_por_funcionario(od, pd.DataFrame(), log=_q)
    return od


def _otros_admin(ruta):
    """El Administrativo no trae INSTRUMENTO: el estamento sale del funcionario, por el
    export de atenciones que el A23 carga igual (aca, uno minimo con ese funcionario)."""
    import pandas as pd
    od, _col = _a23().cargar_otros(ruta, log=_q)
    _a23()._estamento_por_funcionario(
        od, pd.DataFrame({"PROF": ["ANA PEREZ"], "INSTR": ["Médico"]}), log=_q)
    return od


def _grupal(ruta):
    """Lo que hace el SM con el grupal: cargarlo y filtrar el mes (ahi vive la guarda de
    las fechas ilegibles, `filtrar_mes`)."""
    from modulos.rem_sm_actividades import cargar_grupal
    from programas.rem_utils import _rango_mes, filtrar_mes
    ini, fin = _rango_mes(MES)
    return filtrar_mes(cargar_grupal(ruta, log=_q), ini, fin, "el grupal")


def _atenciones(ruta):
    """Lo que hace TODO consumidor del ADA/Monitoreo: cargar y filtrar el mes."""
    from programas.rem_utils import _rango_mes, cargar_atenciones, filtrar_mes
    ini, fin = _rango_mes(MES)
    return filtrar_mes(cargar_atenciones(ruta, log=_q), ini, fin, "el export de atenciones")


def _ru():
    import programas.rem_utils as ru
    return ru


_ATENCIONES = ("programas/rem_utils.py::cargar_atenciones", "programas/rem_utils.py::cargar_canonico",
               "modulos/rem_a23_respiratorio.py::_act_de_la_atencion")
# Los opcionales del SM levantan ValueError a proposito: el modulo lo vuelve un log/aviso
# y sigue sin esa desagregacion (TRANS, composicion A26). Cuenta como fallo CLARO.
_OPCIONAL = (ArchivoInvalido, ValueError)


_A05 = ("programas/rem_saludmental.py::abrir_validado", "programas/rem_saludmental.py::_preparar",
        "programas/rem_saludmental.py::marcar_eventos", "modulos/rem_a05_o_egresos.py::agregar_hoja")
_A03 = ("modulos/rem_a03_d3_instrumentos.py::abrir_validado",
        "modulos/rem_a03_d3_instrumentos.py::procesar",
        "modulos/rem_a03_d3_instrumentos.py::detectar_instrumento")
CONTRATOS = [
    Contrato(
        id="poblacion.cargar_inscritos",
        cubre=("programas/poblacion.py::cargar_inscritos",),
        llamar=lambda r: _poblacion().cargar_inscritos(r, log=_q),
        ref="Informe_Inscritos__Adscritos_heads.xlsx",
        fila={"TIPO IDENTIFICACION": "RUN", "NUMERO TIPO IDENTIFICACION": RUT, "SEXO": "Mujer",
              "GENERO": "Femenina", "FECHA DE NACIMIENTO": "01/01/1990", "EDAD AÑOS": 36,
              "SITUACION": "Inscrito", "ESTADO": "Activo", "SECTOR": "Norte"},
        criticas=("NUMERO TIPO IDENTIFICACION", "SEXO", "ESTADO", "SITUACION"),
        clave=("NUMERO TIPO IDENTIFICACION",),
    ),
    Contrato(
        id="poblacion.cargar_formulario_sm",
        cubre=("programas/poblacion.py::_leer_formulario_1",
               "programas/poblacion.py::cargar_formulario_sm"),
        llamar=lambda r: _poblacion().cargar_formulario_sm(r, log=_q),
        ref="Formularios_RAYEN_csm_IRis.xlsx",
        fila={"NUMERO TIPO IDENTIFICACION": RUT, "FECHA FORMULARIO": "05/08/2026",
              "INSTRUMENTO": "Medico", "AÑO APLICACIÓN FORMULARIO": 30, "SEXO": "Mujer",
              "18.- ¿ TIENE  DEPRESIÓN ?": "SI", "19.- ESTADO": "INGRESO"},
        criticas=("NUMERO TIPO IDENTIFICACION", "FECHA FORMULARIO", "INSTRUMENTO"),
        clave=("NUMERO TIPO IDENTIFICACION",),
        # C5: las fechas ilegibles las corta construir_poblacion (_verificar_cobertura_
        # fechas), no el loader; ahi tienen su test (test_sp_p6).
    ),
    Contrato(
        id="A05 egresos (IRIS)",
        cubre=_A05,
        llamar=_a05("iris"),
        ref="Formularios_RAYEN_csm_IRis.xlsx",
        fila={"NUMERO TIPO IDENTIFICACION": RUT, "AÑO APLICACIÓN FORMULARIO": 45, "SEXO": "Mujer",
              "FECHA FORMULARIO": "05/08/2026", "18.- ¿ TIENE  DEPRESIÓN ?": "SI",
              "19.- ESTADO": "EGRESO POR ALTA", "20.- TIPO DE DEPRESIÓN": "Depresión Moderada"},
        criticas=("NUMERO TIPO IDENTIFICACION", "AÑO APLICACIÓN FORMULARIO", "FECHA FORMULARIO"),
        clave=("NUMERO TIPO IDENTIFICACION",),
        fechas=("FECHA FORMULARIO",),
    ),
    Contrato(
        id="A05 egresos (Administrativo)",
        cubre=_A05,
        llamar=_a05("administrativo"),
        ref="Formulario_csm_reporte_Administrativo.xlsx",
        fila={"RUT": RUT, "Edad de registro formulario": "45 años 3 meses 2 días", "Sexo": "Mujer",
              "Fecha Formulario": "2026/08/05", "18.- ¿ Tiene  Depresión ?": "SI",
              "19.- Estado": "Egreso Alta", "20.- Tipo de depresión": "Depresión Moderada"},
        criticas=("RUT", "Edad de registro formulario", "Fecha Formulario"),
        clave=("RUT",),
        fechas=("Fecha Formulario",),
    ),
    Contrato(
        id="A03 GHQ-12 (IRIS)",
        cubre=_A03,
        llamar=_a03("GHQ-12"),
        ref="goldberg_iris.xlsx",
        fila={"NUMERO TIPO IDENTIFICACION": RUT, "AÑO APLICACIÓN FORMULARIO": 30, "SEXO": "Mujer",
              "FORMULARIO": "Cuestionario de Salud de Goldberg", "1.- ESTADO": "Ingreso",
              "14.- PUNTAJE": 8, "15.- RESULTADO": "Indicativos de presencia de psicopatologia"},
        criticas=("14.- PUNTAJE", "15.- RESULTADO", "1.- ESTADO"),
        valida=lambda out: out["total"] > 0,
    ),
    Contrato(
        id="A03 PSC (Administrativo)",
        cubre=_A03,
        llamar=_a03("PSC"),
        ref="psc_administrativo.xlsx",
        fila={"RUT": RUT, "Edad de registro formulario": "8 años", "Sexo": "Hombre",
              "1.- Estado": "Ingreso", "40.- Puntaje ": 40, "41.- Resultado": "Bajo"},
        criticas=("40.- Puntaje ", "41.- Resultado", "1.- Estado"),
        valida=lambda out: out["total"] > 0,
    ),
    Contrato(
        id="a23.cargar_otros",
        cubre=_OTROS,
        llamar=_otros,
        ref="Otros_cronicos_iris.xlsx",
        fila={"NUMERO TIPO IDENTIFICACION": RUT, "FECHA ATENCION": "01/05/2026",
              "INSTRUMENTO": "Médico", "9.- ¿PADECE DE ASMA BRONQUIAL?": "Si", "10.- ESTADO": "Ingreso"},
        criticas=("NUMERO TIPO IDENTIFICACION", "FECHA ATENCION", "INSTRUMENTO"),
        clave=("NUMERO TIPO IDENTIFICACION",),
        fechas=("FECHA ATENCION",),
    ),
    Contrato(
        id="a23.cargar_estrat",
        cubre=("modulos/rem_a23_respiratorio.py::cargar_estrat",),
        llamar=lambda r: _a23().cargar_estrat(r),
        ref="Estratificacion_de_Riesgo_iris.xlsx",
        fila={"RUT": 11111111, "DV": "1",
              "Detalle de Condiciones Crónicas (Diagnósticos)": "Asma Moderada"},
        criticas=("RUT", "Detalle de Condiciones Crónicas (Diagnósticos)"),
        clave=("RUT",),
    ),
    Contrato(
        id="a23 Seccion H (NSP)",
        cubre=("modulos/rem_a23_respiratorio.py::cargar_inasistentes",
               "modulos/rem_a23_respiratorio.py::_seccion_h"),
        llamar=_seccion_h,
        ref="Pacientes_Inasistentes_iris.xlsx",
        fila={"INSTRUMENTO": "Médico", "TIPO DE ATENCION": "Control IRA",
              "FECHA HORA CITA": "10-08-2026 09:00:00", "NUMERO TIPO IDENTIFICACION": RUT, "AÑOS": 40},
        criticas=("INSTRUMENTO", "TIPO DE ATENCION", "FECHA HORA CITA", "AÑOS"),
        fechas=("FECHA HORA CITA",),
        valida=lambda h: int(h.loc[h["Profesional"] == "TOTAL", "Total"].iloc[0]) > 0,
    ),
    Contrato(
        id="a23 Seccion H (Monitoreo de Inasistentes, Admin)",
        cubre=("modulos/rem_a23_respiratorio.py::cargar_inasistentes",
               "modulos/rem_a23_respiratorio.py::_seccion_h"),
        llamar=_seccion_h,
        ref="Monitoreo_de_Inasistentes_admin.xlsx",
        fila={"FUNCIONARIO": "ANA PEREZ", "INSTRUMENTO": "Médico", "TIPO ATENCION": "Control IRA",
              "FECHA CITA": "10-08-2026", "RUN": RUT, "EDAD": "40 años 2 meses", "SEXO": "Mujer"},
        criticas=("INSTRUMENTO", "TIPO ATENCION", "FECHA CITA", "EDAD"),
        fechas=("FECHA CITA",),
        valida=lambda h: int(h.loc[h["Profesional"] == "TOTAL", "20 y más"].iloc[0]) == 1,
    ),
    Contrato(
        id="a23.cargar_otros (Admin)",
        cubre=_OTROS,
        llamar=_otros_admin,
        ref="Otros_cronicos_admin.xlsx",
        fila={"RUT": RUT, "Fecha Formulario": "2026/05/01", "Funcionario": "ANA PEREZ",
              "Sexo": "Mujer", "9.- ¿Padece de Asma Bronquial?": "Si", "10.- Estado": "Ingreso"},
        criticas=("RUT", "Fecha Formulario", "Funcionario"),
        clave=("RUT",),
        fechas=("Fecha Formulario",),
        valida=lambda od: bool(od["_med"].all()),   # el estamento salio del funcionario
    ),
    Contrato(
        id="sm.cargar_grupal",
        cubre=("modulos/rem_sm_actividades.py::cargar_grupal",),
        llamar=_grupal,
        ref="Atenciones_Grupales_iris.xlsx",
        fila={"NUMERO TIPO IDENTIFICACION": RUT, "FECHA ATENCION": "05/08/2026",
              "ACTIVIDADES": "Intervención psicosocial grupal", "SEXO": "Mujer", "EDAD": "30 años",
              "INSTRUMENTO": "Psicólogo(a)", "FUNCIONARIO PRESTADOR": "ANA PEREZ",
              "ASISTE (SI/NO)": "SI"},
        criticas=("ACTIVIDADES", "FECHA ATENCION", "ASISTE (SI/NO)"),
        fechas=("FECHA ATENCION",),
    ),
    Contrato(
        id="rem_utils.cargar_atenciones (IRIS)",
        cubre=_ATENCIONES,
        llamar=_atenciones,
        ref="ATENCIONESDIAGNOSTICOSACTIVIDADES_iris.xlsx",
        fila={"NUMERO TIPO IDENTIFICACION": RUT, "ATEN ID": "901", "FECHA ATENCION": "05/08/2026",
              "ACTIVIDADES": "CONTROLES SALUD MENTAL", "DIAGNOSTICOS": "F32.1",
              "INSTRUMENTO": "Médico", "TIPO ATENCION": "CONTROL", "PROFESIONAL ATENCION": "ANA PEREZ",
              "AÑOS ATENCION": 40, "SEXO": "Mujer"},
        criticas=("NUMERO TIPO IDENTIFICACION", "FECHA ATENCION", "ACTIVIDADES", "DIAGNOSTICOS",
                  "INSTRUMENTO", "TIPO ATENCION"),
        clave=("NUMERO TIPO IDENTIFICACION",),
        fechas=("FECHA ATENCION",),
    ),
    Contrato(
        id="rem_utils.cargar_atenciones (Monitoreo)",
        cubre=_ATENCIONES,
        llamar=_atenciones,
        ref="Monitoreo_de_Actividades_anonimizado.xlsx",
        fila={"N°": 1, "RUN": RUT, "FECHA CONSULTA": "05/08/2026",
              "ACTIVIDAD Y/O PROCEDIMIENTO": "CONTROLES SALUD MENTAL", "DIAGNÓSTICO": "DEPRESION",
              "INSTRUMENTO": "Médico", "TIPO DE ATENCIÓN": "CONTROL", "FUNCIONARIO": "ANA PEREZ",
              "AÑOS": 40, "SEXO": "Mujer"},
        criticas=("RUN", "FECHA CONSULTA", "ACTIVIDAD Y/O PROCEDIMIENTO", "DIAGNÓSTICO",
                  "INSTRUMENTO", "TIPO DE ATENCIÓN"),
        clave=("RUN",),
        fechas=("FECHA CONSULTA",),
    ),
    Contrato(
        id="rem_utils.trans_map",
        cubre=("programas/rem_utils.py::trans_map",),
        llamar=lambda r: _ru().trans_map(r),
        ref="Informe_Inscritos__Adscritos_heads.xlsx",
        fila={"NUMERO TIPO IDENTIFICACION": RUT, "SEXO": "Mujer", "GENERO": "Masculino"},
        criticas=("NUMERO TIPO IDENTIFICACION", "SEXO", "GENERO"),
        clave=("NUMERO TIPO IDENTIFICACION",),
        errores=_OPCIONAL,
    ),
    Contrato(
        id="rem_utils.atenid_multiprofesional",
        cubre=("programas/rem_utils.py::atenid_multiprofesional",),
        llamar=lambda r: _ru().atenid_multiprofesional(r),
        ref="Monitoreo_Multiprofesional_iris.xlsx",
        fila={"ATEN ID": "901", "NUMERO TIPO IDENTIFICACION": RUT, "PROFESIONAL": "ANA PEREZ",
              "Multiprofesional-1": "LUIS SOTO"},
        criticas=("ATEN ID", "Multiprofesional-1"),
        clave=("ATEN ID",),
        errores=_OPCIONAL,
    ),
    Contrato(
        id="rem_utils.cargar_maestro",
        cubre=("programas/rem_utils.py::cargar_maestro",),
        llamar=lambda r: _ru().cargar_maestro(r),
        # El Maestro .xlsx (8.6 MB) no se versiona: lo cubre catalogos/maestro_slim. Este
        # es su banner y encabezado reales (sep-2026), copiados a mano.
        banner=(("Maestro de Actividades",),),
        encabezado=("ACTIVIDAD", "INSTRUMENTO ASOCIADO", "NUM REM", "NUM SECCION", "REM",
                    "ES PROCEDIMIENTO", "ES COMUNITARIA", "ES GRUPAL", "ES EXAMEN",
                    "ES ODONTOLOGICA", "APLICA URGENCIA"),
        fila={"ACTIVIDAD": "CONTROLES SALUD MENTAL", "INSTRUMENTO ASOCIADO": "Médico",
              "NUM REM": "REM-A06", "NUM SECCION": "A"},
        criticas=("ACTIVIDAD", "NUM REM"),
        clave=("ACTIVIDAD",),
        errores=_OPCIONAL,   # _guard_maestro: ValueError, el TP cae a la heuristica y lo avisa
    ),
    Contrato(
        id="estamentos.cargar_estamentos",
        cubre=("programas/estamentos.py::cargar_estamentos",),
        llamar=lambda r: __import__("programas.estamentos", fromlist=["x"]).cargar_estamentos(r, log=_q),
        ref="Utilizacion_cupos_admin.xlsx",   # encabezado de DOS pisos (celdas combinadas)
        fila={"Profesional": "ANA PEREZ", "Instrumento": "Psicólogo(a)"},
        criticas=("Profesional", "Instrumento"),
        clave=("Profesional",),
    ),
]
