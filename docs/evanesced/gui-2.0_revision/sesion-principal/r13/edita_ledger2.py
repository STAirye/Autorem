# -*- coding: utf-8 -*-
"""Ronda 13, parte 2: §3, §4 (checklist paso 11 + anios discontinuos) y §5."""
import pathlib, sys
p = pathlib.Path(r"E:\git\Autorem\docs\review_gui-2.0_pendiente.md")
raw = p.read_bytes()
crlf = b"\r\n" in raw
t = raw.decode("utf-8").replace("\r\n", "\n")


def rep(viejo, nuevo, n=1):
    global t
    if t.count(viejo) != n:
        sys.exit("ANCLA FALLIDA (%d veces, esperaba %d):\n%s" % (t.count(viejo), n, viejo[:120]))
    t = t.replace(viejo, nuevo, n)


# ---- §3: la ronda 13 no agrego tests; re-corrio todo ------------------------
rep("""- Se instalaron `pytest` y `customtkinter`, que faltaban en el Python 3.9 local:""",
    """- **La ronda 13 no agregó tests** (sus 4 arreglos son documentación, un import muerto y
  dos docstrings: nada que mutar), pero re-corrió todo: `pytest -q` 298 passed, la suite
  archivo por archivo 16/16 sin fallas, los 3 checks en verde y los 37 módulos de
  `gui`/`programas`/`modulos`/`tools` importando. Sigue en **296** `def test_`.
- Se instalaron `pytest` y `customtkinter`, que faltaban en el Python 3.9 local:""")

# ---- §4: checklist del paso 11 + anios discontinuos ------------------------
NUEVO_4 = """### Checklist del paso 11 — abierto tras la ronda 13

Los tres se arreglan **en el commit del merge**, no antes (decisión del autor): tocan
documentación que el propio merge reescribe, y adelantarlos duplicaría el trabajo si la 2.0
mueve algo. Están acá para que el commit del paso 11 los tenga como lista.

1. **La tabla-compuerta del plan dice que la compuerta está cerrada.**
   `docs/GUI_2.0_plan.md` §9.1 («**Antes del paso 11**, esta tabla tiene que estar entera en
   "sí". Es la condición para borrar la GUI vieja») tiene sus DOS filas en «pendiente»:
   dotación (1.9.8/1.9.9) y el título propio de `cruzados` (1.9.10). **Las dos están
   portadas y verificadas dos veces por esta revisión** — `gui/dialogos.py` trae
   `bloque_dotacion` / `dotacion_ada` / `dialogo_dotacion` / `revisar_dotacion` (rondas 3 y
   7) y `runner._TITULO_INVALIDO["cruzados"]` existe, con el docstring de `runner` citando
   «la rama 'cruzados' de 1.9.10». Pasar las dos filas a «sí», cada una con el símbolo que
   lo prueba, y anotar «verificado en la ronda 13». Si se mergea así, quien ejecute el paso
   11 o re-porta trabajo hecho, o le pierde la confianza a la única compuerta escrita del
   merge.
2. **Tres headers de versión apuntan a un release de `main` ANTERIOR a su contenido** —
   misma clase que la colisión de §1.E, que ya se pagó para `rem_utils.VERSION`:
   `gui/paginas/inicio.py` dice 1.9.15 y es un archivo NUEVO de la rama;
   `tools/check_version.py` dice 1.9.10 (en `main` está en 1.9.6) y trae el `"gui"` de
   `DIRS_VERSIONADOS`, que ningún 1.9.10 shippeó; `tools/slim_maestro.py` dice 1.9.15 con el
   cambio de ruta a `catalogos/`. Los tres a 1.9.17 (o a la versión del merge). **Por qué no
   salta el hook:** el chequeo 3 de `check_version` solo mira `staged_py()`, así que un
   header queda viejo para siempre a menos que alguien vuelva a tocar el archivo — vale
   sumarle un modo `--auditar` que compare cada `.py` versionado contra la versión vigente
   cuando lo cambió su último commit, y colgarlo de la skill `versionar`, no del hook.
3. **`gui/` no existe en el mapa del repo.** El `CLAUDE.md` raíz no la nombra en NINGUNA
   parte: ni en el árbol de §2, ni en el reparto compartido/modular, ni en la cadena de
   imports (`rem_utils <- formatos <- capas <- módulos <- autorem`, y `gui/` importa las
   tres) — y es el único paquete de código sin su propio `CLAUDE.md`, con `"gui"` ya en
   `DIRS_VERSIONADOS` y en `CARPETAS` de `check_fuentes`. Lo único que la documenta es un
   PLAN, que declara trabajo futuro: su §11 todavía dice «Hoy la GUI **no tiene cobertura**»
   con 38 tests de GUI escritos. Al mergear: fila `gui/ -> gui/CLAUDE.md` en el árbol, `gui/`
   en el reparto y en la cadena de imports, corregir la fila de `catalogos/` (ahora también
   guarda el `maestro_slim.csv.gz`), y escribir `gui/CLAUDE.md` con el CONTRATO de la carpeta
   (`PANTALLA`, el descubrimiento por `pkgutil`, `runner` como única frontera con el worker,
   qué NO va en una página), apuntando al plan para el resto.

### Abierto tras la ronda 13 — años discontinuos en la familia población (a `main`)

**Hallazgo 8 de la ronda 13, lógica de módulo:** los inputs multi-archivo de población
(`formularios`, `ada`) aceptan años cualesquiera y **un hueco en el medio es invisible**,
porque `poblacion._verificar_cobertura_fechas` compara solo `min` y `max`. Repro en el
scratchpad `r13/anios_discontinuos.py`, corte 2016-08:

```
B) ADA 2016 + 2014 + 2012  (falta 2015 entero)
   LOG cobertura de fechas -> corte: 2016-08 | ADA: 2012-05..2016-08
   avisos: 0
   Activo 12m : ['run_2016_03', 'run_2016_08']
C) lo mismo con 2015 cargado
   Activo 12m : ['run_2015_10', 'run_2016_03', 'run_2016_08']
```

Los dos loguean `ADA: 2012-05..2016-08`, que se lee como cobertura completa, y los dos
devuelven **0 avisos**, así que la hoja LEEME no dice nada. Quien tuvo su única atención de
la ventana en el año que falta sale `¿Activo 12m?` = **NO**: se cae de la población en
control (el P6·A.1 subcuenta) y, como `Activo 12m` y el rescate comparten la lista
`ACTIVIDADES_SM_7`, los flags de rescate subcuentan también. Es el bug recurrente completo:
número plausible, mal, y callado, en un módulo cuya salida se copia al REM.

**Lo que NO es el problema:** cargar un año viejo suelto (2012 reportando 2016) está bien.
Todo se calcula en ventanas hacia atrás desde el corte (`_flags_actividad`, nunca `TODAY()`),
así que las filas fuera de la ventana se ignoran para Activo 12m / rescate / gestante y sí
cuentan para `¿Ingresado?` y `_estado_dx`, que es para lo que existe el histórico. El orden
de los archivos tampoco importa, y cada archivo se valida por separado (`cargar_canonico`:
0 filas, columnas ausentes, clave vacía -> `ArchivoInvalido` nombrándolo).

**Arreglo propuesto, en la guarda que ya existe** (no un caso nuevo): que
`_verificar_cobertura_fechas` compare los **meses calendario presentes** contra los que la
ventana necesita (`_mes_offset(corte, 13)` .. `corte`) en vez de los extremos, y devuelva un
aviso `SUBCONTADO` **listando los meses que faltan**. Un mes sin ninguna atención en un ADA
de CESFAM no existe en la práctica: un mes ausente es un archivo ausente. Aviso y no
`ArchivoInvalido`, igual que esa función ya trata el histórico incompleto.

**No es exclusivo de población:** `rem_a23_respiratorio.py` chequea el historial de la
Sección G con `od["FECHA"].min() > limite`, también solo el extremo. Al arreglarlo, mirar los
dos. Emparentado con §1.K.8, que cerró el caso del año **cargado pero solo-encabezado** (ahí
hay archivo, así que dispara la guarda por archivo); el año que **no se carga** no tiene
archivo y por eso quedaba afuera.

"""
rep("### Deuda conocida, para el paso 11 / el merge",
    NUEVO_4 + "### Deuda conocida, para el paso 11 / el merge")

# ---- §4: el angulo de convenciones queda cubierto (con salvedad) -----------
rep("""- **Convenciones**: headers de versión de cada `.py` de `gui/` vs su último cambio real
  (se sincronizaron a 1.9.17 los tocados, no se auditó el resto).""",
    """**Ojo:** la **Eficiencia** es lo único que sigue sin barrerse. El ángulo de
**Convenciones** lo cubrió la ronda 13 (auditoría de los 37 `.py` versionados: header vs
último cambio real), y lo que encontró son los 3 headers del «Checklist del paso 11» de más
arriba — el ángulo está cerrado, el arreglo no.""")

# ---- §5: fila de la ronda 13 ----------------------------------------------
rep("""| 13 | _(siguiente: eficiencia, convenciones —headers de versión del resto de `gui/`—, la prueba a mano del caché en el PC del trabajo (§4), y otra pasada a ojo del autor)_ | | |""",
    """| 13 | **Coherencia estructural tras 12 rondas de parches** — el rango `fd1b0cc^..HEAD` (74 archivos, +9718/-1007) leído como CUERPO y no por ángulo: imports y referencias muertas entre rondas, helpers duplicados, la mudanza de `maestro_slim` a `catalogos/` en todos sus lectores/doc/spec/gitignore, **headers de versión** de cada `.py` tocado vs su último cambio real (cierra el ángulo de convenciones), anclas `§N` citadas desde código y docs, tablas de estado de los 4 `CLAUDE.md`, reglas duras y cobertura de contratos. Casi todo por comando: los 3 checks, `pytest`, la suite archivo por archivo, import de los 37 módulos, barridos AST de imports/atributos/constantes | 8: **4 ✅** + 3 ⏸ al paso 11 + 1 ⏸ a `main` (años discontinuos) | §1.N · §2 · §4 (checklist del paso 11 · años discontinuos) |
| 14 | _(siguiente: EFICIENCIA —el único ángulo sin barrer: ¿la GUI 2.0 relee archivos o rehace trabajo?—, la prueba a mano del caché en el PC del trabajo (§4), y otra pasada a ojo del autor)_ | | |""")

p.write_bytes((t.replace("\n", "\r\n") if crlf else t).encode("utf-8"))
print("ledger parte 2: §3, §4 (checklist + anios discontinuos) y §5 escritos. CRLF =", crlf)
