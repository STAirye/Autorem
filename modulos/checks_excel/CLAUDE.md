# modulos/checks_excel/ — macros de chequeo pre-envío

Macros VBA de **solo lectura** que el autor importa al REM del mes antes de enviarlo.
Leen el total de cada tabla que autoREM produce y marcan REVISAR los 0 y los errores.
Hay una por **programa y serie**: `REM_<serie>_<programa>.bas`.

| Macro | Cubre | Plantilla |
|---|---|---|
| `REM_A_SM.bas` | A03 D.3 · A04 · A05 N/O · A06 A.1/A.2 · A19a A.3 · A26 · A27 A/B · A32 F1/F2 (sin Trabajo Perdido, que no tributa) | `SA_26_V1.2` |

- **Pendientes:** `REM_A_RESP` (A23), que espera un REM validado de Respiratorio, y
  `REM_P_SM` (P6), que espera que cierre la validación de la familia población.
- **Todo módulo nuevo nace con su check:** se suma a la macro de su programa, o se
  crea una. La receta está en la skill `check-excel`.
- `tests/test_checks_excel.py` parsea cada `.bas` y exige que sus celdas sigan siendo
  fórmulas de total en la plantilla de `refs_tablas/`. Una plantilla nueva lo hace
  fallar.
- Llevan `' Version:` en el header (`check_version` cuenta `.py` y `.bas`) y son solo
  ASCII. Git las deja en CRLF al hacer checkout (`core.autocrlf`), que es lo que pide
  el importador de VBA.
