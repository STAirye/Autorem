Eres la ronda 13 de la revision de `gui-2.0` — la ULTIMA compuerta antes de empezar el
merge a `main`.

Lee, en este orden:

1. `C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\648a107e-f033-4d56-a55d-a415a58f003e\scratchpad\review_context.md`
   (actualizado al 2026-09-20: reglas del repo, entorno, el bug recurrente, que NO es
   hallazgo, y el formato de salida).
2. `docs/review_gui-2.0_pendiente.md` — el registro. §1 = ya corregido, §2 = descartado
   con motivo, §4 = que falta, §5 = el angulo de cada ronda. Reportar algo de §1 o §2 es
   pagar dos veces el mismo hallazgo.

## Tu angulo: COHERENCIA ESTRUCTURAL tras 12 rondas de parches

Las rondas 1-12 metieron **9718 inserciones y 1007 supresiones en 74 archivos**
(`git diff fd1b0cc^..HEAD`), sobre una rama que ya traia la GUI 2.0. Ese codigo es la
SALIDA de la revision: cada ronda lo miro por su angulo, pero **nadie lo reviso como
cuerpo**, ni se pregunto si doce tandas sucesivas de arreglos dejaron el repo coherente
consigo mismo. Esa es tu pregunta, y es la unica.

**Ese rango — `fd1b0cc^..HEAD` — es tu foco**, no el diff completo contra `main`: la
ronda 3 ya barrio linea por linea el estado anterior, y repetirlo es quemar la ronda.
Lo de antes entra solo si un arreglo posterior lo re-expuso.

Lista cerrada. Si no esta aca, no es tu ronda:

- **Imports y referencias.** Todo import resuelve; nada quedo apuntando a un simbolo que
  una ronda posterior renombro o borro; sin imports muertos de refactors intermedios;
  sin helper duplicado porque dos rondas arreglaron lo mismo por separado.
- **Rutas y archivos movidos.** `refs_tablas/maestro_slim.csv.gz` -> `catalogos/`: todo
  lector, `.gitignore`, `autoREM.spec`, `tools/slim_maestro.py` y doc que lo nombre.
- **Versionado (CLAUDE.md §9).** Header de version de CADA `.py` tocado vs su ultimo
  cambio real — **`gui/` es el sospechoso: §4 dice que solo se sincronizaron los
  tocados y el resto no se auditó**. Manifiesto de `check_version.py`, contador de tests
  en CLAUDE.md, entrada del CHANGELOG.
- **Documentacion.** Anclas `§N` citadas desde codigo y docs que apunten a secciones que
  existen; las tablas de estado de CLAUDE.md (modulos, matriz de programas) describiendo
  la realidad; ¿`gui/` necesita su propio `CLAUDE.md`, como `programas/`, `modulos/` y
  `tools/`?
- **Reglas duras del repo** (estan en el contexto): ASCII en rutas de consola,
  `contiene_todos`/`contiene_alguno`, deteccion por CONTENIDO, carpeta de salida = la de
  los inputs, cero PII.
- **Contratos.** Todo lector nuevo de planillas del usuario con su contrato
  (`check_fuentes`).

## Metodo: verifica, no opines

Tu angulo es casi todo decidible por comando. Corre primero, lee despues:

```
python tools/check_version.py ; python tools/check_cp1252.py ; python tools/check_fuentes.py --todo
python -m pytest -q
python -c "import importlib,pkgutil; [importlib.import_module(m.name) for m in pkgutil.walk_packages(['gui','programas','modulos','tools'],'')]"
git diff fd1b0cc^..HEAD --stat
```

Cada hallazgo va con su comando y su salida. Si no lo pudiste ejecutar, dilo en vez de
inferirlo. El resto de la revision corre en modo recall; **esta ronda no**: aca lo
verificable es casi todo, y la sospecha sin verificar cuesta mas de lo que aporta.

Los tres checks pasan hoy (`check_version` OK 1.9.17 / 296 tests). Que pasen no cierra
tu angulo: no cubren anclas de doc, `CLAUDE.md` por carpeta, imports muertos ni helpers
duplicados entre rondas. Ahi es donde hay que mirar con ojos.

## Salida

El formato de `review_context.md` (hasta 8 candidatos, el mas grave primero, con
`file` / `line` / `category` / `summary` / `failure_scenario` / `evidence`), y en cada
uno una linea mas:

```
  bloquea_merge: <si | no> — <por que>
```

`si` = mergear asi deja `main` roto o incoherente. `no` = real, pero se arregla despues.
Los `si` nunca se caen por el tope de 8. Si no hay nada real, devuelve lista vacia: en la
ultima compuerta "limpio" es un resultado, y rellenar es peor que no reportar.

No escribes en el repo. Al cerrar, emite el texto listo para pegar: la fila de §5 con TU
angulo, tu bloque §1.N, y lo que perseguiste y NO era bug para §2. El §2 sale aunque tu
lista venga vacia — saber que ya se miro es la mitad del valor de la ronda.

Ojo al anotar §4: la **Eficiencia** sigue sin barrerse y TU ronda no la cubre. Que no
desaparezca de la lista.
