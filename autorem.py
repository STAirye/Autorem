#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 4.8 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simón Tobar — CESFAM Dr. Luis Ferrada Urzúa (APS, SSMC)
# Copyright (C) 2026 Simón Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# Version: 2.0.0
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details: <https://www.gnu.org/licenses/>.
# ==========================================================================
"""
autorem.py — dispatcher (arranque + CLI) del proyecto autoREM.

Desde la **2.0.0** este archivo ya no dibuja nada: la interfaz es la **GUI 2.0**
(`gui/`, customtkinter, una pantalla por archivo en `gui/paginas/`; ver gui/CLAUDE.md
y el docstring de gui/app.py). Acá quedan tres cosas:

  1. El REGISTRO de tareas del A05 (`TAREAS`, `buscar_tarea`), que consume la página
     `gui/paginas/a05.py`.
  2. La ORQUESTACIÓN compartida `_correr_tareas` / `_resumen_texto`: la usan la GUI y
     el CLI, y por eso no vive en ninguno de los dos.
  3. El **CLI**, que está CONGELADO (CLAUDE.md §12): no sigue el rediseño de la GUI,
     y es solo del A05.

La GUI 1.x (Tkinter/ttk, una pestaña por módulo) quedó congelada comprimida en
`legacy/autorem_gui_tk_1.9.18.py.gz` (plan de la GUI 2.0 §8). No se descomprime para
arreglarla.

USO:
  - Doble-clic al .exe / .py                 -> ventana (GUI 2.0).
  - Arrastra el .xlsx ENCIMA del .exe / .py  -> GUI con la ruta cargada en el A05.
  - Terminal (solo A05):  python autorem.py --cli entrada.xlsx
                    [--formato iris|administrativo] [--tarea ID[,ID2,...]]
"""

import sys
from pathlib import Path

import programas.rem_saludmental as sm

# La GUI 2.0. El import va a NIVEL DE MÓDULO a propósito: el resto de los imports de
# este archivo son locales a su función, y PyInstaller solo ve los estáticos -> con un
# `from gui.app import lanzar` adentro de main(), el exe congelado muere con
# ModuleNotFoundError al abrirlo, con el .spec ya «arreglado». Las páginas entran
# aparte, por collect_submodules('gui.paginas') en autoREM.spec (se descubren en
# runtime con pkgutil, así que el análisis estático no las ve).
from gui import app as gui_app

# -- Registro de módulos de tarea --------------------------------------
from modulos import rem_a05_o_egresos
from modulos import rem_a05_n_ingresos

MODULOS = [rem_a05_o_egresos, rem_a05_n_ingresos]

TAREAS = [m.TAREA for m in MODULOS]
PERFILES = sm.PERFILES


def buscar_tarea(tarea_id):
    for t in TAREAS:
        if t["id"] == tarea_id:
            return t
    return None


def _forzar_utf8_stdout():
    """En consola Windows (cp1252) los símbolos > · -> «» OK revientan con
    UnicodeEncodeError. Forzar UTF-8 en stdout/stderr lo evita (no afecta a la GUI)."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


# -- Orquestación (compartida GUI/CLI) ---------------------------------
def _correr_tareas(tareas, entrada, perfil, log=print, mes=None, carpeta=None):
    """Carga el workbook UNA vez (validando contra `perfil`), cada tarea agrega
    su hoja, y guarda UN solo «…_procesado.xlsx». Devuelve (resultados, salida).
    `mes`=(año,mes) filtra por FECHA FORMULARIO; None = archivo completo.
    `carpeta`=dónde guardar; None = junto al archivo de entrada (comportamiento clásico)."""
    wb, ws = sm.abrir_validado(entrada, perfil)
    resultados = []
    for tarea in tareas:
        log(f"> {tarea['nombre']}   ({perfil['nombre']})")
        res = tarea["agregar"](wb, ws, perfil, log=log, mes=mes)
        resultados.append((tarea, res))

    from programas import cobertura
    avisos = []
    if perfil.get("disclaimer"):
        avisos.append((
            "Pueblos Originarios / SENAME / Prot. Ninez / Migrante / Trans", "VACIAS",
            f"perfil {perfil['nombre']} no trae esas columnas",
            "Usar el formato IRIS si se necesitan esos flags"))
    cobertura.escribir_hoja(wb, [t["id"] for t in tareas],
                            {"mes": mes, "archivos": [entrada.name]}, avisos=avisos)

    sufijo = f"_{mes[0]}_{mes[1]:02d}" if mes else ""   # mes elegido -> …_procesado_2026_07.xlsx
    destino = Path(carpeta) if carpeta else entrada.parent
    # Nunca pisa una salida anterior: `… (1).xlsx` (ver rem_utils.rutas_libres).
    from programas.rem_utils import rutas_libres, escribir_atomico
    salida, = rutas_libres(destino / (entrada.stem + "_procesado" + sufijo + ".xlsx"))
    escribir_atomico(salida, wb.save)   # un corte a medias no deja un .xlsx roto con este nombre
    log(f"[ok] guardado: {salida}")
    return resultados, str(salida)


def _resumen_texto(resultados, salida):
    """Arma el texto de confirmación a partir de (resultados, salida)."""
    partes = []
    for tarea, res in resultados:
        det = ""
        if "por_tipo" in res:
            det = " · ".join(f"{t}: {c}" for t, c in res["por_tipo"].items())
        linea = f"{tarea['nombre']}  ->  hoja «{res.get('hoja', '?')}»: {res.get('total', '?')} filas"
        if det:
            linea += f"  ({det})"
        partes.append(linea)
    texto = "Listo.\n" + "\n".join(partes)
    if salida:
        texto += f"\n\nGuardado en:\n{salida}"
    return texto


# -- Lo único que sobrevive de la GUI 1.x: los usa el CLI (congelado, CLAUDE.md
#    §12). La interfaz vive en gui/ desde la 2.0.0, y la 1.x quedó congelada en
#    legacy/autorem_gui_tk_1.9.18.py.gz (plan de la GUI 2.0 §8).
# RAYEN/IRIS exportan en .xls, .csv, .html y .xlsx; la herramienta lee SOLO .xlsx.
_MSG_NO_XLSX = (
    "El archivo no es un Excel .xlsx válido.\n\n"
    "RAYEN/IRIS entregan varios formatos (.xls antiguo, .csv, .html) y esta "
    "herramienta lee SOLO .xlsx.\n\n"
    "Ábrelo en Excel y usa «Guardar como» -> «Libro de Excel (.xlsx)», y carga ese.\n"
    "(Si un .xlsx te da este error, suele ser un .html/.xls disfrazado: mismo arreglo.)")


def _es_error_formato(e):
    """True si la excepción viene de intentar abrir algo que NO es un .xlsx real
    (extensión no soportada por openpyxl, o zip corrupto = html/xls disfrazado)."""
    import zipfile
    try:
        from openpyxl.utils.exceptions import InvalidFileException
    except Exception:   # noqa: BLE001
        InvalidFileException = ()
    return isinstance(e, (zipfile.BadZipFile,) + ((InvalidFileException,) if InvalidFileException else ()))


# +===================================================================+
# |  MODO CONSOLA (experto) y ARRANQUE                                 |
# +===================================================================+
def main_cli(args):
    # args: entrada.xlsx [--formato iris|administrativo] [--tarea ID[,ID2,...]]
    _forzar_utf8_stdout()

    perfil = PERFILES[0]
    if "--formato" in args:
        i = args.index("--formato")
        if i + 1 >= len(args):
            print("ERROR: --formato requiere un ID (iris | administrativo).")
            return 2
        perfil = sm.perfil_por_id(args[i + 1])
        if perfil is None:
            print(f"ERROR: formato inválido. Disponibles: "
                  f"{', '.join(p['id'] for p in PERFILES)}")
            return 2
        args = args[:i] + args[i + 2:]

    tarea_ids = None
    if "--tarea" in args:
        i = args.index("--tarea")
        if i + 1 >= len(args):
            print("ERROR: --tarea requiere uno o más IDs (separados por coma).")
            return 2
        tarea_ids = [s for s in args[i + 1].split(",") if s]
        args = args[:i] + args[i + 2:]

    mes = None
    if "--mes" in args:
        i = args.index("--mes")
        if i + 1 >= len(args):
            print("ERROR: --mes requiere un valor AAAA-MM (ej. 2026-07).")
            return 2
        try:
            y_s, m_s = args[i + 1].split("-")
            mes = (int(y_s), int(m_s))
            if not (1 <= mes[1] <= 12):
                raise ValueError
        except ValueError:
            print("ERROR: --mes debe ser AAAA-MM con mes 1-12 (ej. 2026-07).")
            return 2
        args = args[:i] + args[i + 2:]

    if not args:
        ids = ", ".join(t["id"] for t in TAREAS)
        fmts = ", ".join(p["id"] for p in PERFILES)
        print("USO: python autorem.py --cli entrada.xlsx "
              "[--formato iris|administrativo] [--tarea ID[,ID2,...]] [--mes AAAA-MM]")
        print(f"Formatos: {fmts}  (por defecto: {PERFILES[0]['id']})")
        print(f"Tareas:   {ids}  (por defecto: la primera)")
        print("--mes:    filtra por FECHA FORMULARIO (por defecto: archivo completo)")
        print("(El screening A03 por ahora solo desde la GUI, pestaña 'Screening'.)")
        return 2

    if tarea_ids:
        seleccionadas = []
        for tid in tarea_ids:
            t = buscar_tarea(tid)
            if t is None:
                print(f"ERROR: no existe la tarea '{tid}'. "
                      f"Disponibles: {', '.join(x['id'] for x in TAREAS)}")
                return 2
            seleccionadas.append(t)
    else:
        seleccionadas = [TAREAS[0]]

    entrada = Path(args[0].strip().strip('"').strip("'"))
    if not entrada.exists():
        print(f"ERROR: no encuentro el archivo:\n  {entrada}")
        return 1

    if perfil["disclaimer"]:
        print(perfil["disclaimer"] + "\n")
    try:
        resultados, salida = _correr_tareas(seleccionadas, entrada, perfil, mes=mes)
    except sm.ArchivoInvalido as e:
        print(f"\n[ARCHIVO EQUIVOCADO — {e.categoria}]\n{e}")
        return 1
    except PermissionError:
        print("\n[PERMISO DENEGADO] ¿está abierto en Excel? Ciérralo y reintenta.")
        return 1
    except Exception as e:   # noqa: BLE001
        if _es_error_formato(e):
            print("\n[NO ES .XLSX] " + _MSG_NO_XLSX)
            return 1
        raise
    print(_resumen_texto(resultados, salida))
    return 0


def main():
    _forzar_utf8_stdout()
    argv = sys.argv[1:]

    # Modo consola explícito para usuarios avanzados.
    if argv and argv[0] in ("--cli", "-c"):
        sys.exit(main_cli(argv[1:]))

    # Si arrastraron un archivo encima del .exe/.py, Windows lo pasa como argv[1].
    ruta_inicial = ""
    if argv:
        cand = argv[0].strip().strip('"').strip("'")
        if cand and not cand.startswith("-"):
            ruta_inicial = cand

    try:
        gui_app.lanzar(ruta_inicial)
    except Exception as e:
        # Si la ventana no se puede abrir (raro), caemos a un modo texto mínimo.
        print(f"No pude abrir la ventana ({e}).")
        print("Modo texto: pega la ruta del .xlsx (Enter para salir).")
        try:
            ruta = input("> ").strip().strip('"').strip("'")
        except EOFError:
            return
        if ruta:
            sys.exit(main_cli([ruta]))


if __name__ == "__main__":
    main()
