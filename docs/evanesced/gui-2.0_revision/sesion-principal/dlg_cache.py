import sys
sys.path.insert(0, r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\a40108ff-012a-4b37-baf2-2a1dc332a634\scratchpad")
from ed import reemplazar

P = r"E:\git\Autorem\gui\dialogos.py"
reemplazar(P, [
# referencia en la caja de Estamentos
('''"cárgala una vez y los meses siguientes se autocompleta sola.\\nVuelve a cargar "
        "'Utilización de Cupos' solo cuando cambie el equipo (se fusiona con lo guardado).")''',
'''"cárgala una vez y los meses siguientes se autocompleta sola.\\nVuelve a cargar "
        "'Utilización de Cupos' solo cuando cambie el equipo (se fusiona con lo guardado).\\n"
        + REF_PREFERENCIAS)'''),
# referencia en la caja de Dotacion
('''"por los nombres nuevos.\\nLa tabla queda GUARDADA (caché en ~/.autorem/dotacion.json).")''',
'''"por los nombres nuevos.\\nLa tabla queda GUARDADA (caché en ~/.autorem/dotacion.json).\\n"
        + REF_PREFERENCIAS)'''),
('''from programas import dotacion
''',
'''from programas import dotacion

# UNA linea en cada caja que usa un caché (Dotacion, Estamentos): el detalle vive en
# «Acerca de» para no llenar la pagina con un caso borde.
REF_PREFERENCIAS = ("¿No se guardan tus preferencias? Mira «Acerca de», sección "
                    "«Preferencias guardadas».")
'''),
# drenar avisos al cerrar las ventanas de dotacion
('''    _DOTACION_ABIERTA[0] = True
    try:
        return _dotacion_ada(root, modulo, ada, mes, log, messagebox, mask=mask, todos=todos)
    finally:
        _DOTACION_ABIERTA[0] = False
''',
'''    _DOTACION_ABIERTA[0] = True
    try:
        return _dotacion_ada(root, modulo, ada, mes, log, messagebox, mask=mask, todos=todos)
    finally:
        _DOTACION_ABIERTA[0] = False
        from gui.runner import avisar_cache
        avisar_cache(messagebox)   # caché dañado / no guardado: se dice al cerrar
'''),
('''    _DOTACION_ABIERTA[0] = True
    try:
        _revisar_dotacion(root, modulo)
    finally:
        _DOTACION_ABIERTA[0] = False
''',
'''    _DOTACION_ABIERTA[0] = True
    try:
        _revisar_dotacion(root, modulo)
    finally:
        _DOTACION_ABIERTA[0] = False
        import tkinter.messagebox as messagebox
        from gui.runner import avisar_cache
        avisar_cache(messagebox)
'''),
('''            def _quitar(e=est):
                tabla["omitidos"][modulo] = [x for x in tabla["omitidos"].get(modulo, []) if x != e]
                dotacion.guardar(tabla)
                _pintar_omitidos()''',
'''            def _quitar(e=est):
                # `quitar_omision` y no editar + `guardar(tabla)`: guarda SOLO este
                # cambio sobre lo que hay en disco (no pisa otra ventana de autoREM).
                dotacion.quitar_omision(tabla, modulo, e)
                _pintar_omitidos()'''),
])
print("ok")
