---
name: versionar
description: Sube de versión el proyecto y sincroniza TODO lo que la versión arrastra (rem_utils.VERSION, headers de los .py tocados, contadores en CLAUDE.md, entrada del CHANGELOG), y verifica el manifiesto de archivos versionados. Úsalo al cerrar una tanda de cambios, cuando el pre-commit bloquee por "versionado/contadores desincronizados", o cuando el usuario pida "bumpear", "subir la versión" o "revisar que esté todo anotado".
---

# versionar — la versión arrastra cinco archivos, no uno

`rem_utils.VERSION` es la fuente de verdad, pero un bump obliga a tocar además el
header de cada `.py` que cambió, dos lugares de `CLAUDE.md`, cuatro contadores de
tests y una entrada del `CHANGELOG`. Hacerlo a mano falla: en una sola sesión de
sep-2026 se hizo cuatro veces y CLAUDE.md llegó a declarar **94 tests cuando había
124**, y **1.8.2 cuando el repo iba en 1.9.1**.

Eso no rompe el código. Rompe la confianza en la documentación, que es lo único con
lo que se orienta una sesión fría. Por eso hay un check y está en el pre-commit.

## Convenciones que codifica (no las cambies sin acordarlo)

- **Cada `.py` lleva la versión de SU ÚLTIMO CAMBIO**, no todos sincronizados. Así el
  header dice *cuándo cambió ese archivo*. (CLAUDE.md §9 decía lo contrario hasta
  sep-2026; se corrigió para reflejar la práctica real.)
- **Manifiesto derivado de la RUTA, no una lista a mano.** Llevan versión:
  `autorem.py`, `programas/`, `modulos/`, `tools/`. No llevan: `tests/`,
  `__init__.py`. **Exento** (ni obligado ni prohibido): `legacy/`, congelado a
  propósito en 1.1/1.2.
- Ojo con esa distinción: *exento* no es lo mismo que *prohibido*. Mezclarlas hace
  que `legacy/` salte como falso positivo.

## Qué hacer

1. **Ver el estado** (es lo que corre el hook):
   ```bash
   python tools/check_version.py
   ```
2. **Sincronizar lo automático** — contadores de tests y headers de lo que estás
   commiteando:
   ```bash
   python tools/check_version.py --arreglar
   ```
3. **Subir de versión** (fuente de verdad + headers de lo modificado + CLAUDE.md):
   ```bash
   python tools/check_version.py --bump X.Y.Z
   ```
4. **Escribir la entrada del CHANGELOG a mano.** El script no la inventa a propósito:
   el *qué* cambió y *por qué* es criterio, no texto generable. Sin esa entrada el
   check bloquea.
5. Correr la suite y `tools/check_cp1252.py` antes de commitear.

## Elegir el número (CLAUDE.md §9)

`X` arquitectura · `Y` **módulo o reporte nuevo** · `Z` corrección del trabajo en
curso. Ante la duda es `Z`: `Y` se reserva para un módulo REM nuevo de verdad.
Precedentes: la hoja LEEME fue `1.8.3` (transversal, no módulo), los catálogos DEIS
se llevaron el `1.9.0` (capa nueva).

## Dos sesiones en paralelo (pasó, sep-2026)

Dos workflows sobre el mismo repo quisieron subir a **1.8.4** y a **1.9.0**. Los dos
números eran defendibles por separado, así que nada los frenaba hasta que chocaban, y
hubo que detener ambos.

El árbitro es el **CHANGELOG**: si ya tiene una versión mayor que `rem_utils.VERSION`,
otra sesión avanzó y esta copia quedó atrás. El check lo bloquea y `--bump` rechaza
cualquier número que no avance respecto de lo publicado.

**Si te pasa:** no fuerces el número. Mira qué tomó la otra sesión (`git log`,
`CHANGELOG`), sincroniza, y re-bumpea **desde ahí**. Si las dos tandas de cambios son
independientes, casi siempre lo correcto es que la segunda sea un `Z` sobre la
versión de la primera, no un número paralelo.

## Reglas duras

- **Si el check bloquea, arregla — no uses `--no-verify`.** Ese escape es para un
  caso consciente y puntual, no para destrabarse.
- **Si agregas otra frase con el conteo de tests a CLAUDE.md**, agrégala a
  `PATRONES_TESTS` en `tools/check_version.py` o quedará desincronizada en silencio.
- **Los hooks no se versionan** (viven en `.git/hooks/`): instalar en cada clon con
  `python tools/check_version.py --instalar`. Se encadena a los hooks que ya haya
  (anti-RUT §8.2, cp1252) sin pisarlos.
- Un `.py` nuevo bajo `programas/`, `modulos/` o `tools/` **necesita el header
  completo** (bloque GPL + autor + `# Version:`). El check lo exige; ver cualquier
  archivo existente como plantilla.
