# -*- mode: python ; coding: utf-8 -*-
#
# Spec de PyInstaller para autoREM. Equivalente a la linea de comando de
# CLAUDE.md §11:
#
#   pyinstaller --onefile --windowed --name "autoREM" \
#     --add-data "catalogos/maestro_slim.csv.gz;refs_tablas" \
#     --add-data "catalogos;catalogos" autorem.py
#
# OJO con `datas`: son DATOS, no imports -> PyInstaller no los descubre solo.
# Los destinos NO son arbitrarios, tienen que calzar con donde los busca el
# codigo dentro del bundle (sys._MEIPASS):
#
#   autorem._slim_por_defecto()   -> _MEIPASS / "refs_tablas" / "maestro_slim.csv.gz"
#   gui.runner.slim_por_defecto() -> _MEIPASS / "catalogos" / "maestro_slim.csv.gz"
#   programas.catalogos._carpetas -> _MEIPASS / "catalogos"
#
# El archivo FUENTE vive en `catalogos/maestro_slim.csv.gz` (feedback del autor,
# sep-2026: es un catalogo actividad<->estamento<->REM igual que cie10/eno/ges,
# no un ejemplo anonimizado como el resto de refs_tablas/ -- ver
# tools/slim_maestro.py). La entrada `refs_tablas` de mas abajo es SOLO
# compatibilidad con la GUI vieja (`autorem._slim_por_defecto()`, congelada
# hasta el paso 11 de docs/GUI_2.0_plan.md -- no se toca `autorem.py` antes de
# eso): copia el MISMO archivo a los dos destinos del bundle para que ninguna
# de las dos GUI pierda el Trabajo Perdido con Maestro mientras conviven.
#
# Si falta el maestro slim, el Trabajo Perdido cae a heuristica (avisa en el log).
# Si faltan los catalogos, `catalogos.cargar()` levanta FileNotFoundError.
#
# Este archivo esta en .gitignore (`*.spec`), asi que NINGUNA revision del repo
# lo va a cachar si se desincroniza. Ya paso una vez: quedo apuntando a
# 'refs tablas/' despues del rename a 'refs_tablas/'.

a = Analysis(
    ['autorem.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('catalogos/maestro_slim.csv.gz', 'refs_tablas'),   # compat GUI vieja, ver nota arriba
        ('catalogos', 'catalogos'),                          # incluye maestro_slim.csv.gz para la GUI 2.0
    ],
    # `programas.catalogos` (§14) es una capa compartida que TODAVIA NO tiene
    # consumidor: ningun modulo del exe la importa (solo tools/, que no se
    # empaqueta). Sin esta linea PyInstaller no la incluye y los catalogos/*.csv.gz
    # de `datas` viajarian huerfanos -> data sin el codigo que la lee.
    # Cuando algun modulo la importe de verdad, esta entrada deja de hacer falta.
    hiddenimports=['programas.catalogos'],
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
