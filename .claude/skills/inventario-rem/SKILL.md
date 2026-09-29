---
name: inventario-rem
description: Inventaria las casillas de un REM (SA_26 / SP_26 .xlsm) que un equipo llenó A MANO y las cruza con el REM Comentado (regla RAYEN por casilla), el Maestro de Actividades y el Manual DEIS, para planificar un módulo nuevo de cualquier programa de salud. Úsalo cuando el usuario traiga un REM llenado a mano de un programa (PDS, CPU, Cardiovascular, SSyR, ...) y pida "qué casillas llenan", "extraer las casillas", "contrastar con el comentado/maestro", o arranque la planificación de un módulo nuevo desde un REM real.
---

# inventario-rem — de un REM llenado a mano al mapa del módulo

El punto de partida de un módulo nuevo es un REM que el equipo del programa llena a
mano. De él se saca **qué casillas le tocan al programa**, **qué regla de RAYEN las
alimenta** y **los valores reales, que sirven de oráculo** para validar el módulo
después. El primer caso fue PDS/CPU: `docs/pds_cpu_casillas_SA.md` es el formato de
salida de referencia.

## Fuentes

| Fuente | Dónde | Qué aporta |
|---|---|---|
| **REM llenado** (`.xlsm`) | La trae el usuario, casi siempre desde OneDrive | Casillas llenas = valores reales. **Nunca entra al repo** |
| **REM Comentado Serie A** | `refs_tablas/REM_Comentado_Serie_A_2026_15-04-2026.xlsx` | Notas de celda: «Ref DEIS» (definición) + «RAYEN» (formulario/campo/actividad). **Solo existe para la Serie A** |
| **Maestro slim** | `catalogos/maestro_slim.csv.gz` | Actividad → estamento → REM/sección. La Serie P no tiene actividades: es población en control, que sale de formularios |
| **Manual DEIS** | `OneDrive/REM SM/2026/MANUAL REM  P 2026 Version  1.0.pdf` y `Manual Series REM 2026 SERIE A BS BM DV1.0.pdf` | Definiciones oficiales. Para la Serie P es la única fuente de reglas |

## Pasos

1. **Confirmar con el usuario** qué archivo es y a qué programa y mes corresponde. Se
   detecta por contenido, no por el nombre del archivo.
2. **Correr el script** con la salida en el **scratchpad** (el borrador trae valores
   reales y no se versiona):
   ```bash
   python .claude/skills/inventario-rem/inventario.py "<REM.xlsm>" --salida "<scratchpad>/inv.md" --maestro --comentado refs_tablas/REM_Comentado_Serie_A_2026_15-04-2026.xlsx
   ```
   - Sin `--hojas` ni `--secciones`, toma **solo las secciones con alguna casilla
     llena**. Con `--secciones "A05:J,V;A33:*"` se fuerzan secciones vacías que el
     programa también debería llenar (las hermanas de una sección llena).
   - `--filas "PADDS|CUIDADOR"` limpia las secciones que comparten varios programas
     (A27, A03): muestra solo las filas con valor o con una etiqueta que calce.
   - Para la Serie P, sin `--comentado`, porque no existe un Comentado P.
3. **Leer el borrador entero.** Lo que hay que revisar:
   - `AVISO: filas del Comentado sin par` o `filas del REM sin nota`. Pueden ser
     etiquetas que cambiaron entre versiones o filas nuevas.
   - `Alertas de validación ya disparadas`: el propio REM se queja, por ejemplo con
     «Digite CERO», y eso significa que el módulo tiene que escribir 0 explícito.
   - Encabezados `?` o `(sin encabezado)`: hay que resolverlos a mano mirando la hoja.
4. **Manual DEIS** (sobre todo para la Serie P). Se lee con **`pypdf`**, que está
   instalado en el Python global del PC del trabajo desde sep-2026. Es una herramienta
   del dev, no una dependencia del proyecto: no va al `.exe`. El Read de PDF no sirve
   ahí, porque le falta `pdftoppm`.
   1. Buscar las páginas por palabra clave. Por ejemplo, con `PdfReader(...).pages` se
      buscan `REM-?P3|dependencia severa` con una regex sobre `extract_text()`.
   2. Volcar solo esas páginas a un `.txt` en el **scratchpad** y leerlo.
   3. Al doc va la regla **resumida y citando la página**. Nunca se pega el Manual.
   4. Si `pypdf` falta, **pedirle al usuario** que lo instale (es una descarga, así que
      no se hace sin permiso). Mientras tanto, la regla queda marcada como «pendiente
      Manual».

   El Manual dice **qué** contar, no **de qué campo de RAYEN**: eso lo da el Comentado
   (solo existe el de la Serie A) o el equipo.
5. **Escribir `docs/<programa>_casillas_<SA|SP>.md`** con el formato de
   `pds_cpu_casillas_SA.md`:
   1. Header de licencia con la versión **actual**, la que reporta el hook
      `check_version`, no la de `CLAUDE.md` si quedó atrás.
   2. Las fuentes, y el aviso de versión si el Comentado es de otra versión que el REM.
   3. Un **resumen**: sección → fuente RAYEN → si está en el Maestro.
   4. Una sección por hoja: el mapa de columnas compacto, la tabla de filas con los
      valores y la suma, y la regla en prosa corta.
   5. Los **cruces entre hojas** (✅ / ❓ / ❌).
   6. **Lo que falta**: inputs que hoy no se bajan y preguntas para el equipo.
6. **Commitear solo el doc.** El push lo hace el usuario.

## Reglas duras

- **Etiqueta, nunca coordenada.** El Comentado y el REM son de versiones distintas:
  las filas se corren y las columnas se reordenan. En A33·B 2026, `AT` era «Consulta
  nueva» en uno y «DS Hombres» en el otro. El script empareja por etiqueta
  normalizada, con un match aproximado y en orden. El **módulo** que salga de esto
  también tiene que ubicar cada casilla por su encabezado.
- **Input = casilla desbloqueada.** Las hojas REM vienen protegidas, y ese es el
  criterio que separa input, vacío y fórmula. Si una hoja llega **sin protección**, el
  criterio no sirve: avisar y no inventar.
- **La planilla no entra al repo.** Al doc van los valores ya sacados de la grilla, en
  texto, con su casilla y su etiqueta. Son conteos agregados sin PII. Si aparece
  cualquier cosa con RUT o nombre, **parar y avisar**.
- **No se audita el programa ajeno.** Una inconsistencia del llenado manual se anota
  una sola vez, en tono informativo: «el módulo calculará X según la regla; el valor
  manual de este mes no sirve de oráculo». No se persigue. El equipo del programa sabe
  cosas que el REM no dice (ejemplo: el 100 % de cuidadores con Zarit vigente de la
  P3·B 2026 era real, por un operativo con una universidad). **Preguntar, no
  corregir.**
- **Descuadres de sexo** entre hojas que cuentan a las mismas personas: una hipótesis
  a revisar es que un formulario use el sexo registral y otro el de identidad de género
  (el mismo problema que dieron los TRANS en el SM, 1.5.5).
- **Los formularios alimentan formularios** en RAYEN. Por ejemplo, el Barthel llena
  «Tipo de Dependencia» del formulario PDS. Si el REM lee el campo copiado, esa es la
  fuente del módulo, y el formulario de origen queda como chequeo cruzado (un severo
  con Barthel leve se avisa).
- El script es **solo ASCII** (cp1252). Si se toca, correr la skill `check-cp1252`.
