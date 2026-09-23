#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 5.5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
#
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# Copyright (C) 2026 Simon Tobar
# SPDX-License-Identifier: GPL-3.0-or-later
# ==========================================================================
"""
Repro del `tk.tcl` intermitente de test_gui_construccion (docs/tk_tcl_intermitente.md).

Separa tres hipotesis:
  A  disco / antivirus: el open() del .tcl falla de verdad por un instante.
  B  estado de Tcl que se gasta tras muchos Tk() crear/destruir en UN proceso.
  C  algo nuestro que sobrevive a la ventana (after de customtkinter, hilos).

Etapas (cada una en su propio subproceso):
  S0  pytest tests/test_gui_construccion.py, K veces  -> tasa de referencia
  S1  N x tkinter.Tk() + update + destroy            -> Tcl/Tk pelado
  S2  N x ctk.CTk() + update x3 + destroy             -> + customtkinter
  S3  N x App(ruta IRIS) + mostrar a05 + bombear      -> + nuestro codigo e hilos
  S4  S3 con UNA ventana por proceso fresco            -> control (B predice 0)
  S5  3 x S2 en paralelo                               -> concurrencia (A)

En cada falla registra: el mensaje completo, que .tcl fallo, si Python ve y lee
ese archivo EN ESE MOMENTO, si un Tk() nuevo en el MISMO proceso anda, si anda en
un proceso FRESCO, y los handles GDI/USER/kernel + hilos vivos. Cada 25 ventanas
anota los handles, para ver si crecen (fuga) aunque no falle.

Uso (desde la raiz del repo, que es de donde importa gui/ y tests/):
    python repro_tk_tcl.py --maquina trabajo                # todas; S0 (parpadea) al final
    python repro_tk_tcl.py --maquina casa --etapas S1,S2 --n1 1000
Salida: %TEMP%/autorem_repro_tk/<maquina>_<fecha>.csv + .log (fuera del repo).
Compatible con Python 3.9 (el de la casa). Solo ASCII (consola cp1252).
"""

import argparse
import csv
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

ESTA = os.path.abspath(__file__)
# Fuera de pantalla: la ventana se crea, se MAPEA y se pinta igual (withdraw() no),
# solo que no parpadea ~1500 veces en la cara del usuario. --visible lo apaga.
POS = "" if os.environ.get("REPRO_TK_VISIBLE") else "+-4000+-4000"
RE_ARCHIVO = re.compile(r'couldn\'t read file "([^"]+)"')


# ---------------------------------------------------------------- hijo

def _emitir(**ev):
    sys.stdout.write(json.dumps(ev, ensure_ascii=True) + "\n")
    sys.stdout.flush()


def _recursos():
    """Handles del proceso: GDI, USER y kernel. Una fuga lineal aca es la firma de B."""
    r = {"hilos": threading.active_count()}
    if os.name != "nt":
        return r
    import ctypes
    from ctypes import wintypes
    k32, u32 = ctypes.windll.kernel32, ctypes.windll.user32
    # restype/argtypes a mano: el pseudo-handle (-1) se trunca a 32 bits si no.
    k32.GetCurrentProcess.restype = wintypes.HANDLE
    u32.GetGuiResources.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    k32.GetProcessHandleCount.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    h = k32.GetCurrentProcess()
    r["gdi"] = u32.GetGuiResources(h, 0)
    r["user"] = u32.GetGuiResources(h, 1)
    n = wintypes.DWORD()
    k32.GetProcessHandleCount(h, ctypes.byref(n))
    r["handles"] = n.value
    return r


def _fixture_iris(carpeta):
    """El mismo export IRIS minimo de test_gui_construccion (RUT de ejemplo)."""
    import openpyxl
    p = Path(carpeta) / "iris_repro.xlsx"
    wb = openpyxl.Workbook(); ws = wb.active
    ws.append(["Servicio de Salud", None]); ws.append(["Filtros: bla", None])
    ws.append(["NUMERO TIPO IDENTIFICACION", "A\u00d1O APLICACI\u00d3N FORMULARIO", "SEXO",
               "FECHA FORMULARIO", "18.- \u00bf TIENE DEPRESI\u00d3N ?", "19.- ESTADO",
               "20.- TIPO DE DEPRESI\u00d3N"])
    ws.append(["11111111-1", 45, "Mujer", "06/07/2026", "SI", "EGRESO ALTA",
               "Depresi\u00f3n Moderada"])
    wb.save(p)
    return p


def _fabrica(etapa, repo):
    """Devuelve f(i) que crea, usa y destruye UNA ventana del tipo de la etapa."""
    import tkinter
    if etapa == "S1":
        def f(i):
            r = tkinter.Tk(); r.geometry("200x200" + POS); r.update(); r.destroy()
        return f
    import customtkinter as ctk
    if etapa == "S2":
        def f(i):
            r = ctk.CTk(); r.geometry("400x300" + POS)
            for _ in range(3):
                r.update()
            r.destroy()
        return f
    # S3: lo que hacen los tests que fallaron (App + a05 + deteccion en hilo)
    sys.path.insert(0, repo)
    sys.path.insert(0, os.path.join(repo, "tests"))
    import _aislar_cache  # noqa: F401  (PRIMERO: nunca tocar el ~/.autorem real)
    from gui.app import App
    fx = _fixture_iris(tempfile.mkdtemp(prefix="autorem_repro_"))

    def f(i):
        app = App(ruta_inicial=str(fx), precargar=False)
        app.geometry("1180x820" + POS)
        try:
            app.mostrar("a05")
            for _ in range(60):
                app.update()
        finally:
            app.destroy()
    return f


def _diagnostico_falla(i, e, t0):
    msg = str(e)
    m = RE_ARCHIVO.search(msg)
    archivo = m.group(1) if m else ""
    existe = legible = ""
    if archivo:
        existe = os.path.isfile(archivo)
        try:
            with open(archivo, "rb") as fh:
                legible = len(fh.read())
        except OSError as oe:
            legible = "ERR %s" % oe
    # Un Tk() nuevo en ESTE proceso: B predice que sigue roto, A que se recupera.
    import tkinter
    reint = []
    for _ in range(3):
        try:
            tkinter.Tk().destroy(); reint.append("ok")
        except Exception as e2:  # noqa: BLE001
            reint.append("falla:" + str(e2).splitlines()[0][:60])
    hilos = [t.name for t in threading.enumerate()]
    _emitir(ev="falla", i=i, dt_ms=round((time.perf_counter() - t0) * 1000),
            tipo=type(e).__name__, archivo=archivo, existe=existe, legible=legible,
            reintento_mismo_proc="|".join(reint), nombres_hilos=hilos, msg=msg,
            **_recursos())


def hijo(etapa, n, repo):
    import tkinter
    r = tkinter.Tcl()
    _emitir(ev="inicio", etapa=etapa, n=n, pid=os.getpid(), py=sys.version.split()[0],
            exe=sys.executable, tcl=r.eval("info patchlevel"),
            tk_lib=os.environ.get("TK_LIBRARY", ""), **_recursos())
    del r
    f = _fabrica(etapa, repo)
    for i in range(1, n + 1):
        t0 = time.perf_counter()
        try:
            f(i)
        except Exception as e:  # noqa: BLE001  (TclError y lo que sea: se anota)
            _diagnostico_falla(i, e, t0)
            return
        if i == 1 or i % 25 == 0:
            _emitir(ev="muestra", i=i, dt_ms=round((time.perf_counter() - t0) * 1000),
                    **_recursos())
    _emitir(ev="fin", i=n, **_recursos())


# ---------------------------------------------------------------- padre

CAMPOS = ["maquina", "etapa", "proc", "ev", "i", "dt_ms", "gdi", "user", "handles",
          "hilos", "archivo", "existe", "legible", "reintento_mismo_proc",
          "proceso_fresco", "tipo", "msg_1a_linea"]


class Registro:
    def __init__(self, salida, maquina):
        salida.mkdir(parents=True, exist_ok=True)
        base = salida / ("%s_%s" % (maquina, time.strftime("%Y%m%d_%H%M%S")))
        self.csv_path, self.log_path = base.with_suffix(".csv"), base.with_suffix(".log")
        self._csv = open(self.csv_path, "w", newline="", encoding="utf-8")
        self.w = csv.DictWriter(self._csv, fieldnames=CAMPOS, extrasaction="ignore")
        self.w.writeheader()
        self.log = open(self.log_path, "w", encoding="utf-8")
        self.maquina = maquina
        self.fallas = {}

    def fila(self, etapa, proc, ev):
        ev = dict(ev, maquina=self.maquina, etapa=etapa, proc=proc)
        if "msg" in ev:
            ev["msg_1a_linea"] = ev["msg"].splitlines()[0][:120] if ev["msg"] else ""
            self.log.write("\n==== %s proc %s falla en i=%s\n%s\n" % (
                etapa, proc, ev.get("i"), ev["msg"]))
            self.log.write("hilos vivos: %s\n" % ev.get("nombres_hilos"))
        if ev["ev"] == "falla":
            self.fallas.setdefault(etapa, []).append(ev.get("i"))
        self.w.writerow(ev); self._csv.flush(); self.log.flush()
        if ev["ev"] in ("inicio", "falla", "fin"):
            print("  [%s/%s] %-6s i=%-4s %s" % (etapa, proc, ev["ev"], ev.get("i", ""),
                  ev.get("msg_1a_linea", "") or "gdi=%s user=%s handles=%s" % (
                  ev.get("gdi"), ev.get("user"), ev.get("handles"))))
            sys.stdout.flush()


def _proceso_fresco():
    r = subprocess.run([sys.executable, "-c", "import tkinter; tkinter.Tk().destroy()"],
                       capture_output=True, text=True)
    return "ok" if r.returncode == 0 else "falla"


def _lanzar(etapa, n, repo, stderr_log):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.Popen([sys.executable, ESTA, "--hijo", etapa, "--n", str(n),
                             "--repo", repo], cwd=repo, env=env, text=True,
                            encoding="utf-8", stdout=subprocess.PIPE, stderr=stderr_log)


def _recoger(reg, etapa, proc, p):
    for linea in p.stdout:
        linea = linea.strip()
        if not linea.startswith("{"):
            reg.log.write("[%s/%s stdout] %s\n" % (etapa, proc, linea)); continue
        ev = json.loads(linea)
        if ev["ev"] == "falla":
            ev["proceso_fresco"] = _proceso_fresco()
        reg.fila(etapa, proc, ev)
    p.wait()
    if p.returncode not in (0, None):
        # Un crash duro (Tcl_AsyncDelete, 0x80000003) no alcanza a emitir la falla.
        reg.fila(etapa, proc, {"ev": "crash", "i": "", "msg": "returncode %s" % p.returncode})


def etapa_hijos(reg, etapa, n, repo, paralelos=1, fabrica=None):
    with open(str(reg.log_path) + ".stderr", "a", encoding="utf-8") as err:
        ps = [_lanzar(fabrica or etapa, n, repo, err) for _ in range(paralelos)]
        hilos = [threading.Thread(target=_recoger, args=(reg, etapa, k, p))
                 for k, p in enumerate(ps)]
        for h in hilos:
            h.start()
        for h in hilos:
            h.join()


def etapa_s4(reg, n, repo):
    """Una ventana App por proceso fresco: si B es cierto, esto nunca falla."""
    with open(str(reg.log_path) + ".stderr", "a", encoding="utf-8") as err:
        for k in range(n):
            _recoger(reg, "S4", k, _lanzar("S3", 1, repo, err))


def etapa_s0(reg, k, repo):
    """La suite real del archivo, K veces: la tasa de referencia contra la que se mide."""
    for run in range(k):
        t0 = time.perf_counter()
        r = subprocess.run([sys.executable, "-m", "pytest", "tests/test_gui_construccion.py",
                            "-q", "-p", "no:cacheprovider"], cwd=repo, capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
        out = r.stdout + r.stderr
        fallados = re.findall(r"^FAILED (\S+)", out, re.M)
        tcl = "usable tk.tcl" in out or "usable init.tcl" in out or "tcl_findLibrary" in out
        m = RE_ARCHIVO.search(out)
        ev = {"ev": "falla" if r.returncode else "fin", "i": run,
              "dt_ms": round((time.perf_counter() - t0) * 1000),
              "tipo": "TclError" if tcl else ("" if not r.returncode else "otro"),
              "archivo": m.group(1) if m else "",
              "msg": ("FAILED: %s\n\n%s" % (", ".join(fallados), out[-6000:]))
              if r.returncode else ""}
        reg.fila("S0", run, ev)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hijo"); ap.add_argument("--n", type=int)
    ap.add_argument("--repo", default=os.getcwd())
    ap.add_argument("--maquina", default="sin_nombre")
    ap.add_argument("--visible", action="store_true", help="ventanas en pantalla")
    ap.add_argument("--etapas", default="S1,S2,S3,S4,S5,S0")   # S0 (parpadea) al final
    ap.add_argument("--k0", type=int, default=5, help="corridas de pytest en S0")
    ap.add_argument("--n1", type=int, default=500, help="ventanas Tk en S1")
    ap.add_argument("--n2", type=int, default=300, help="ventanas CTk en S2 y S5")
    ap.add_argument("--n3", type=int, default=60, help="ventanas App en S3")
    ap.add_argument("--n4", type=int, default=20, help="procesos frescos en S4")
    ap.add_argument("--salida", default=os.path.join(tempfile.gettempdir(),
                                                     "autorem_repro_tk"))
    a = ap.parse_args()
    if a.hijo:
        return hijo(a.hijo, a.n, a.repo)

    repo = os.path.abspath(a.repo)
    if not os.path.isfile(os.path.join(repo, "gui", "app.py")):
        sys.exit("--repo no es la raiz de autoREM: %s" % repo)
    reg = Registro(Path(a.salida), a.maquina)
    print("maquina=%s  python=%s  %s" % (a.maquina, sys.version.split()[0], platform.platform()))
    print("csv: %s\nlog: %s" % (reg.csv_path, reg.log_path))
    if a.visible:
        os.environ["REPRO_TK_VISIBLE"] = "1"   # lo heredan los hijos
    etapas = [e.strip().upper() for e in a.etapas.split(",")]
    for e in etapas:
        t0 = time.perf_counter()
        print("\n== %s" % e); sys.stdout.flush()
        if e == "S0":
            etapa_s0(reg, a.k0, repo)
        elif e == "S1":
            etapa_hijos(reg, "S1", a.n1, repo)
        elif e == "S2":
            etapa_hijos(reg, "S2", a.n2, repo)
        elif e == "S3":
            etapa_hijos(reg, "S3", a.n3, repo)
        elif e == "S4":
            etapa_s4(reg, a.n4, repo)
        elif e == "S5":
            etapa_hijos(reg, "S5", a.n2, repo, paralelos=3, fabrica="S2")
        print("   %.0f s" % (time.perf_counter() - t0))

    print("\n==== RESUMEN (%s)" % a.maquina)
    for e in etapas:
        f = reg.fallas.get(e, [])
        print("  %s: %d falla(s)%s" % (e, len(f), (" en i=%s" % f) if f else ""))
    print("csv: %s" % reg.csv_path)


if __name__ == "__main__":
    main()
