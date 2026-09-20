import sys
sys.path.insert(0, r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\a40108ff-012a-4b37-baf2-2a1dc332a634\scratchpad")
from ed import reemplazar

P = r"E:\git\Autorem\programas\dotacion.py"
reemplazar(P, [
("# Version: 1.9.8\n", "# Version: 1.9.17\n"),
("""import json
from pathlib import Path

import pandas as pd

from programas.rem_utils import norm
""",
"""from pathlib import Path

import pandas as pd

from programas.rem_utils import norm, leer_cache_json, guardar_cache_json, apartar_cache
"""),
('''def cargar(log=print):
    """Tabla cacheada del disco: {'funcionarios': {nombre_norm: 'interno'|
    'externo'}, 'omitidos': {modulo: [estamento_norm, ...]}}. Vacía si no
    existe o el caché está corrupto (robusto: nunca revienta la corrida)."""
    try:
        if RUTA_CACHE.exists():
            with open(RUTA_CACHE, encoding="utf-8") as f:
                d = json.load(f)
            if isinstance(d, dict):
                func = d.get("funcionarios", {})
                omit = d.get("omitidos", {})
                if isinstance(func, dict) and isinstance(omit, dict):
                    return {"funcionarios": dict(func), "omitidos": dict(omit)}
    except Exception as e:   # noqa: BLE001
        log(f"[dotacion] no pude leer el caché ({e}); sigo sin él")
    return _tabla_vacia()


def guardar(tabla, log=print):
    """Escribe la tabla al caché (crea ~/.autorem si falta). Falla silenciosa
    con aviso: no arruina la corrida si el disco/permisos fallan."""
    try:
        RUTA_CACHE.parent.mkdir(parents=True, exist_ok=True)
        with open(RUTA_CACHE, "w", encoding="utf-8") as f:
            json.dump(tabla, f, ensure_ascii=False, sort_keys=True, indent=0)
    except Exception as e:   # noqa: BLE001
        log(f"[dotacion] no pude guardar el caché ({e})")
''',
'''# Textos de los avisos de caché (rem_utils.leer_cache_json / guardar_cache_json): QUE
# se pierde, dicho en lo que le importa al usuario -- no "no pude escribir el JSON".
_QUE = "la tabla de dotación (quién es externo)"
_SI_SE_PIERDE = ("te voy a preguntar por TODOS los funcionarios como si fuera la primera "
                 "vez. OJO: sin tick cuenta como interno, así que vuelve a marcar a los "
                 "externos que ya tenías marcados.")
_SI_NO_SE_GUARDA = ("el próximo mes te va a volver a preguntar por estos funcionarios (y "
                    "sin tick cuentan como internos).")


def _cargar_con_estado(log=print):
    datos, estado = leer_cache_json(RUTA_CACHE, _QUE, _SI_SE_PIERDE, log=log)
    if estado != "ok":
        return _tabla_vacia(), estado
    func = datos.get("funcionarios", {})
    omit = datos.get("omitidos", {})
    if not (isinstance(func, dict) and isinstance(omit, dict)):
        apartar_cache(RUTA_CACHE, _QUE, "no tiene la forma esperada", _SI_SE_PIERDE, log=log)
        return _tabla_vacia(), "corrupto"
    return {"funcionarios": dict(func), "omitidos": dict(omit)}, "ok"


def cargar(log=print):
    """Tabla cacheada del disco: {'funcionarios': {nombre_norm: 'interno'|
    'externo'}, 'omitidos': {modulo: [estamento_norm, ...]}}. Vacía si no existe;
    si esta dañada o no se puede leer, tambien vacia pero con aviso RUIDOSO
    (rem_utils.leer_cache_json): una tabla vacia vuelve a contar a todos los
    externos, asi que eso nunca puede pasar callado. Nunca revienta la corrida."""
    return _cargar_con_estado(log=log)[0]


def guardar(tabla, log=print):
    """Escribe la tabla ENTERA al caché. True si quedo guardada; si no, aviso ruidoso
    (rem_utils.guardar_cache_json). Las decisiones del dialogo NO pasan por aca sino
    por `_persistir`, que no pisa lo que otra ventana haya guardado mientras tanto."""
    return guardar_cache_json(RUTA_CACHE, tabla, _QUE, _SI_NO_SE_GUARDA, log=log)


def _persistir(cambiar, log=print):
    """Relee el disco, le aplica `cambiar(tabla_del_disco)` y guarda: solo ESTOS
    cambios, sobre lo que hay AHORA. Guardar la copia en memoria entera pisaria lo
    que otra ventana de autoREM guardo despues de que esta cargara (la ultima en
    guardar ganaba y revertia el resto). Si el disco no se pudo LEER no se guarda
    nada: el archivo puede estar sano, y escribir encima lo perderia entero."""
    disco, estado = _cargar_con_estado(log=log)
    if estado == "ilegible":
        from programas.rem_utils import _avisar_cache, _SIGUE
        _avisar_cache(log, f"No guardé los cambios en {_QUE}: {_SI_NO_SE_GUARDA} {_SIGUE}")
        return False
    cambiar(disco)
    return guardar(disco, log=log)
'''),
('''def marcar(tabla, decisiones):
    """Aplica decisiones del diálogo: {nombre: True(externo)/False(interno)}.
    Muta `tabla['funcionarios']` y persiste. Devuelve `tabla`."""
    func = tabla.setdefault("funcionarios", {})
    for nombre, es_externo in (decisiones or {}).items():
        if not nombre:
            continue
        func[norm(nombre)] = EXTERNO if es_externo else INTERNO
    guardar(tabla)
    return tabla
''',
'''def marcar(tabla, decisiones, log=print):
    """Aplica decisiones del diálogo: {nombre: True(externo)/False(interno)}.
    Muta `tabla['funcionarios']` (lo que usa ESTA corrida) y persiste solo estas
    decisiones (`_persistir`). Devuelve `tabla`."""
    cambios = {norm(n): (EXTERNO if ext else INTERNO)
               for n, ext in (decisiones or {}).items() if n}
    tabla.setdefault("funcionarios", {}).update(cambios)
    _persistir(lambda t: t.setdefault("funcionarios", {}).update(cambios), log=log)
    return tabla
'''),
('''    Muta y persiste. Devuelve `tabla`."""
    omit = tabla.setdefault("omitidos", {})
    lista = list(dict.fromkeys(omit.get(modulo, [])))
    for e in (estamentos or []):
        k = norm(e)
        if k and k not in lista:
            lista.append(k)
    omit[modulo] = lista
    guardar(tabla)
    return tabla
''',
'''    Muta y persiste (solo este cambio, `_persistir`). Devuelve `tabla`."""
    nuevos_est = [k for k in (norm(e) for e in (estamentos or [])) if k]

    def agregar(t):
        omit = t.setdefault("omitidos", {})
        lista = list(dict.fromkeys(omit.get(modulo, [])))
        lista += [k for k in nuevos_est if k not in lista]
        omit[modulo] = lista
    agregar(tabla)
    _persistir(agregar, log=log)
    return tabla


def quitar_omision(tabla, modulo, estamento, log=print):
    """Deshace `omitir` para UN estamento (el dialogo 'Revisar dotacion'). Muta y
    persiste solo este cambio (`_persistir`). Devuelve `tabla`."""
    k = norm(estamento)

    def quitar(t):
        omit = t.setdefault("omitidos", {})
        omit[modulo] = [x for x in omit.get(modulo, []) if x != k]
    quitar(tabla)
    _persistir(quitar, log=log)
    return tabla
'''),
("def omitir(tabla, modulo, estamentos):\n", "def omitir(tabla, modulo, estamentos, log=print):\n"),
])
print("ok")
