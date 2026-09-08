# -*- mode: python ; coding: utf-8 -*-
#
# Spec de PyInstaller para autoREM. Equivalente a la linea de comando de
# CLAUDE.md §11:
#
#   pyinstaller --onefile --windowed --name "autoREM" \
#     --add-data "refs_tablas/maestro_slim.csv.gz;refs_tablas" \
#     --add-data "catalogos;catalogos" autorem.py
#
# OJO con `datas`: son DATOS, no imports -> PyInstaller no los descubre solo.
# Los destinos NO son arbitrarios, tienen que calzar con donde los busca el
# codigo dentro del bundle (sys._MEIPASS):
#
#   autorem._slim_por_defecto()   -> _MEIPASS / "refs_tablas" / "maestro_slim.csv.gz"
#   programas.catalogos._carpetas -> _MEIPASS / "catalogos"
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
        ('refs_tablas/maestro_slim.csv.gz', 'refs_tablas'),
        ('catalogos', 'catalogos'),
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
