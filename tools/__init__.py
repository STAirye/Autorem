# tools/ como paquete real (no namespace package implicito).
#
# Razon: `gui/paginas/about.py` hace `from tools.scan_catalogo import escanear` para
# escanear un catalogo DEIS antes de aceptarlo (CLAUDE.md regla 1). Corriendo el .py
# suelto el namespace package alcanza, pero dentro del .exe de PyInstaller no: un
# paquete SIN __init__.py no entra al bundle de forma confiable, y el boton "cargar
# catalogo manual" del About reventaba con ModuleNotFoundError. Ver el hiddenimport
# de `tools.scan_catalogo` en autoREM.spec.
#
# El resto de tools/ son utilitarios de DESARROLLO que se siguen corriendo directo
# (`python tools/check_version.py`) y no viajan en el exe.
