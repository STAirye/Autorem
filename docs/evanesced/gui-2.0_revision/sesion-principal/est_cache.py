import sys
sys.path.insert(0, r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\a40108ff-012a-4b37-baf2-2a1dc332a634\scratchpad")
from ed import reemplazar

P = r"E:\git\Autorem\programas\estamentos.py"
reemplazar(P, [
("""import json
from pathlib import Path

from programas.rem_utils import (
    OPENPYXL_OK, OPENPYXL_ERR, openpyxl,
    ArchivoInvalido, norm, buscar_col, exigir_filas_ws,
)""",
"""from pathlib import Path

from programas.rem_utils import (
    OPENPYXL_OK, OPENPYXL_ERR, openpyxl,
    ArchivoInvalido, norm, buscar_col, exigir_filas_ws,
    leer_cache_json, guardar_cache_json,
)"""),
('''def cargar_cache(log=print):
    """Tabla cacheada del disco. {} si no existe o está corrupta (robusto: nunca
    revienta la corrida por un caché malo)."""
    try:
        if RUTA_CACHE.exists():
            with open(RUTA_CACHE, encoding="utf-8") as f:
                d = json.load(f)
            if isinstance(d, dict):
                return {str(k): ("" if v is None else str(v)) for k, v in d.items()}
    except Exception as e:   # noqa: BLE001
        log(f"[estamentos] no pude leer el caché ({e}); sigo sin él")
    return {}


def guardar_cache(tabla, log=print):
    """Escribe la tabla al caché (crea ~/.autorem si falta). Falla silenciosa con
    aviso: no arruina la corrida si el disco/permisos fallan."""
    try:
        RUTA_CACHE.parent.mkdir(parents=True, exist_ok=True)
        with open(RUTA_CACHE, "w", encoding="utf-8") as f:
            json.dump(tabla, f, ensure_ascii=False, sort_keys=True, indent=0)
    except Exception as e:   # noqa: BLE001
        log(f"[estamentos] no pude guardar el caché ({e})")
''',
'''# Textos de los avisos de caché (rem_utils.leer_cache_json / guardar_cache_json).
_QUE = "la tabla de estamentos (del reporte «Utilización de Cupos»)"
_SI_SE_PIERDE = ("los meses que no cargues «Utilización de Cupos», las atenciones del "
                 "formato Administrativo quedan sin estamento. Vuelve a cargarlo.")
_SI_NO_SE_GUARDA = ("el próximo mes vas a tener que volver a cargar «Utilización de "
                    "Cupos».")


def _cargar_cache_con_estado(log=print):
    datos, estado = leer_cache_json(RUTA_CACHE, _QUE, _SI_SE_PIERDE, log=log)
    if estado != "ok":
        return {}, estado
    return {str(k): ("" if v is None else str(v)) for k, v in datos.items()}, "ok"


def cargar_cache(log=print):
    """Tabla cacheada del disco. {} si no existe; si esta dañada o no se puede leer,
    tambien {} pero con aviso RUIDOSO (rem_utils.leer_cache_json). Nunca revienta."""
    return _cargar_cache_con_estado(log=log)[0]


def guardar_cache(tabla, log=print):
    """Escribe la tabla al caché. True si quedo guardada; si no, aviso ruidoso
    (rem_utils.guardar_cache_json): la corrida sigue con la tabla en memoria."""
    return guardar_cache_json(RUTA_CACHE, tabla, _QUE, _SI_NO_SE_GUARDA, log=log)
'''),
('''    cache = cargar_cache(log=log)
    if entrada:
        nueva, _meta = cargar_estamentos(entrada, log=log)
        tabla = {**cache, **nueva}                  # reporte fresco pisa al caché
        guardar_cache(tabla, log=log)
        solo_cache = len(tabla) - len(nueva)
        log(f"[estamentos] caché actualizado: {len(tabla)} funcionarios "
            f"({len(nueva)} del reporte + {solo_cache} sólo en caché) -> {RUTA_CACHE}")''',
'''    cache, estado = _cargar_cache_con_estado(log=log)
    if entrada:
        nueva, _meta = cargar_estamentos(entrada, log=log)
        tabla = {**cache, **nueva}                  # reporte fresco pisa al caché
        if estado == "ilegible":
            # El caché existe pero no se pudo leer: guardar encima lo perderia ENTERO
            # (los funcionarios de meses anteriores). Ya se aviso en la lectura.
            log("[estamentos] no actualizo el caché: no lo pude leer (ver el aviso)")
        elif guardar_cache(tabla, log=log):
            solo_cache = len(tabla) - len(nueva)
            log(f"[estamentos] caché actualizado: {len(tabla)} funcionarios "
                f"({len(nueva)} del reporte + {solo_cache} sólo en caché) -> {RUTA_CACHE}")'''),
])
print("ok")
