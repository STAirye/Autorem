# -*- mode: python ; coding: utf-8 -*-
#
# Spec de PyInstaller para autoREM. Equivalente a la linea de comando de
# CLAUDE.md §11:
#
#   pyinstaller --onefile --windowed --name "autoREM" \
#     --add-data "catalogos;catalogos" autorem.py
#
# OJO con `datas`: son DATOS, no imports -> PyInstaller no los descubre solo.
# Los destinos NO son arbitrarios, tienen que calzar con donde los busca el
# codigo dentro del bundle (sys._MEIPASS):
#
#   programas.catalogos._carpetas     -> _MEIPASS / "catalogos"
#   programas.catalogos.maestro_slim  -> _MEIPASS / "catalogos" / "maestro_slim.csv.gz"
#
# El Maestro slim vive en `catalogos/` (catalogo actividad<->estamento<->REM,
# como cie10/eno/ges): la GUI lo pide a `catalogos.maestro_slim`, que busca en
# las mismas carpetas que los otros catalogos. Una sola copia en el bundle.
#
# Si falta el maestro slim, el Trabajo Perdido cae a heuristica (avisa en el log).
# Si faltan los catalogos, `catalogos.cargar()` levanta FileNotFoundError.
#
# Este archivo SI se versiona (excepcion explicita al `*.spec` del .gitignore).
# Mientras estuvo ignorado se desincronizo sin que nadie lo cachara: quedo
# apuntando a 'refs tablas/' despues del rename a 'refs_tablas/'.

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# customtkinter shippea sus temas y fuentes como DATA (assets/themes/*.json,
# assets/fonts/): sin esto el exe revienta al importar ctk. El hook oficial no
# siempre esta, asi que se recolecta explicito.
_CTK_DATAS = collect_data_files('customtkinter')

# `gui.app` y `gui.registro` entran por el import estatico de autorem.py (2.0.0:
# `from gui import app as gui_app`, a NIVEL DE MODULO justamente por esto).
# gui/paginas/*.py se descubren en RUNTIME con pkgutil.iter_modules (gui/registro.py):
# NADIE las importa por nombre, asi que el analisis estatico de PyInstaller no las ve
# y el exe quedaba con el sidebar VACIO. collect_submodules las mete al bundle, con lo
# que FrozenImporter.iter_modules() tambien las encuentra. Una pagina nueva en
# gui/paginas/ entra sola: no hay que tocar este archivo.
_PAGINAS = collect_submodules('gui.paginas')

a = Analysis(
    ['autorem.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('catalogos', 'catalogos'),                          # incluye maestro_slim.csv.gz para la GUI 2.0
    ] + _CTK_DATAS,
    # `programas.catalogos` (§14) es una capa compartida que TODAVIA NO tiene
    # consumidor REM: ningun modulo del exe la importa (la GUI 2.0 si, desde el
    # About). Sin esta linea PyInstaller no la incluye y los catalogos/*.csv.gz
    # de `datas` viajarian huerfanos -> data sin el codigo que la lee.
    #
    # `tools.scan_catalogo`: lo importa gui/paginas/about.py para escanear un
    # catalogo DEIS antes de aceptarlo (CLAUDE.md regla 1). Es el UNICO archivo de
    # tools/ que viaja en el exe -- el resto son utilitarios de desarrollo. Va como
    # hiddenimport porque el import es PEREZOSO (dentro de la funcion), asi que el
    # analisis estatico de PyInstaller no lo ve. tools/__init__.py existe por esto.
    hiddenimports=['programas.catalogos', 'tools.scan_catalogo'] + _PAGINAS,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='autoREM',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
