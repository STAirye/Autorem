# Especificación de la página «Cardiovascular»

Extraído automáticamente de la capa de reporte (PBIR) y del modelo semántico (TMDL).

**62 visuales · 122 campos distintos del modelo.**

## Filtros de página

- `Ferrada[Pertenece a PSCV]` (Categorical) → ['SI']
- `Ferrada[Sexo]` (Categorical) → ['Hombre', 'Mujer']
- `Ferrada[Edad]` (Advanced) → ['15']

## Visuales

### 1. HEARTS — `slicer`

- **Values:** `Ferrada[PSCV HEARTS]`

### 2. Sector — `slicer`

- **Values:** `Ferrada[Sector]`

### 3. Estatina Ext — `slicer`

- **Values:** `Ferrada[PSCV Estatina]`

### 4. TBQ actual — `slicer`

- **Values:** `Ferrada[PSCV TBQ Actual]`

### 5. ¿ERC? — `slicer`

- **Values:** `Ferrada[PSCV ERC]`

### 6. Estado — `slicer`

- **Values:** `Ferrada[Estado]`

### 7. ¿Candidato? — `slicer`

- **Values:** `Ferrada[PSCV ¿Candidato Vildagliptina?]`

### 8. Amlodipino — `slicer`

- **Values:** `Ferrada[PSCV Amlodipino]` — «Amlodipino»

### 9. Insulina — `slicer`

- **Values:** `Ferrada[PSCV Insulina]` — «Insulina»

### 10. PAP — `slicer`

- **Values:** `Ferrada[Citar a PAP]`

### 11. Sexo — `slicer`

- **Values:** `Ferrada[Sexo]`

### 12. ¿Candidato? — `slicer`

- **Values:** `Ferrada[PSCV ¿Candidato Estatina?]`

### 13. Promedio de Colesteroles y TG — `lineChart`

- **Category:** `Ferrada[Edad rango 10]`
- **Tooltips:** MIN(`Ferrada[Edad]`) — «Mín. de Edad»
- **Y:** MEDIAN(`Ferrada[PSCV HDL]`) — «Mediana de PSCV HDL»
- **Y:** MEDIAN(`Ferrada[PSCV LDL]`) — «Mediana de PSCV LDL»
- **Y:** MEDIAN(`Ferrada[PSCV TG]`) — «Mediana de PSCV TG»

### 14. Vildagliptina — `slicer`

- **Values:** `Ferrada[Vildagliptina]`

### 15. Promedio de presiones arteriales — `lineChart`

- **Category:** `Ferrada[Edad rango 10]`
- **Tooltips:** MIN(`Ferrada[Edad]`) — «Mín. de Edad»
- **Y:** MEDIAN(`Ferrada[PSCV PAS (última)]`) — «Mediana de PSCV PAS (última)»
- **Y:** MEDIAN(`Ferrada[PSCV PAD (última)]`) — «Mediana de PSCV PAD (última)»

### 16. ¿ECICEP? — `slicer`

- **Values:** `Ferrada[Pertenece a ECICEP]` — «Pertenece ECICEP»

### 17. ¿Candidato? — `slicer`

- **Values:** `Ferrada[PSCV ¿Candidato Empaglifozina?]`

### 18. Riesgo CV — `slicer`

- **Values:** `Ferrada[PSCV Riesgo CV]`

### 19. Losartán — `slicer`

- **Values:** `Ferrada[PSCV Losartán]` — «Losartán»

### 20. ¿Triple Alta? — `slicer`

- **Values:** `Ferrada[PSCV PA/Hba1c/LDL alta]`

### 21. Act Física — `slicer`

- **Values:** `Ferrada[PSCV Act Fisica]`

### 22. ¿Refractaria? — `slicer`

- **Values:** `Ferrada[PSCV HTA Refractaria?]`

### 23. Hidrocloro — `slicer`

- **Values:** `Ferrada[PSCV Hidroclorotiazida]`

### 24. Población PSCV — `tableEx`

- **Values:** `Ferrada[Tipo de identificación]`
- **Values:** `Ferrada[RUN]`
- **Values:** `Ferrada[Nombre Social]`
- **Values:** `Ferrada[Nombre completo]`
- **Values:** `Ferrada[Edad]`
- **Values:** `Ferrada[Sexo]`
- **Values:** `Ferrada[Género]`
- **Values:** `Ferrada[Fecha Nacimiento]`
- **Values:** `Ferrada[Sector]`
- **Values:** `Ferrada[¿Originario o Migrante?]`
- **Values:** `Ferrada[Nacionalidad]`
- **Values:** `Ferrada[Pueblo Originario]`
- **Values:** `Ferrada[Dirección Completa]`
- **Values:** `Ferrada[Celular]`
- **Values:** `Ferrada[Mail]`
- **Values:** `Ferrada[Situación]`
- **Values:** `Ferrada[Estado]`
- **Values:** `Ferrada[Motivo Pasivación]`
- **Values:** `Ferrada[Fecha Pasivación]`
- **Values:** `Ferrada[Previsión]`
- **Values:** `Ferrada[Letra]`
- **Values:** `Ferrada[Pertenece a ECICEP]`
- **Values:** `Ferrada[Pertenece a PSCV]`
- **Values:** `Ferrada[PSCV ¿Ingresado?]` — «¿Ingresado?»
- **Values:** `Ferrada[¿Atendido en 12m?]`
- **Values:** `Ferrada[PSCV Asistente]` — «¿Activo?»
- **Values:** `Ferrada[PSCV Riesgo CV]` — «Riesgo CV»
- **Values:** `Ferrada[IMC (resultado)]` — «IMC»
- **Values:** `Ferrada[PSCV Act Fisica]` — «Act Fisica»
- **Values:** `Ferrada[PSCV HTA]` — «HTA»
- **Values:** `Ferrada[PSCV DM]` — «DM»
- **Values:** `Ferrada[PSCV DLP]` — «DLP»
- **Values:** `Ferrada[PSCV ECV]` — «ECV»
- **Values:** `Ferrada[PSCV IAM]` — «IAM»
- **Values:** `Ferrada[PSCV ACV]` — «ACV»
- **Values:** `Ferrada[PSCV HEARTS]` — «HEARTS»
- **Values:** `Ferrada[PSCV ERC]` — «ERC»
- **Values:** `Ferrada[PSCV VFG Etapa]` — «VFG Etapa»
- **Values:** `Ferrada[PSCV TBQ Actual]` — «TBQ Actual»
- **Values:** `Ferrada[PSCV PA (primera)]` — «PA (primera)»
- **Values:** `Ferrada[PSCV PA Fecha (primera)]` — «PA Fecha (primera)»
- **Values:** `Ferrada[PSCV PA (última)]` — «PA (última)»
- **Values:** `Ferrada[PSCV PA Fecha (última)]` — «PA Fecha (última)»
- **Values:** `Ferrada[PSCV HTA ¿compensada?]` — «HTA ¿compensada?»
- **Values:** `Ferrada[PSCV PA >160/100]` — «PA >160/100»
- **Values:** `Ferrada[PSCV Meses sin PA]` — «Meses sin PA»
- **Values:** `Ferrada[PSCV HbA1c (primera)]` — «HbA1c (primera)»
- **Values:** `Ferrada[PSCV HbA1c Fecha (primera)]` — «HbA1c Fecha (primera)»
- **Values:** `Ferrada[PSCV HbA1c (última)]` — «HbA1c (última)»
- **Values:** `Ferrada[PSCV HbA1c Fecha (última)]` — «HbA1c Fecha (última)»
- **Values:** `Ferrada[PSCV DM ¿compensada?]` — «DM ¿compensada?»
- **Values:** `Ferrada[PSCV HbA1c >9]` — «HbA1c >9»
- **Values:** `Ferrada[PSCV Meses sin HbA1c]` — «Meses sin HbA1c»
- **Values:** `Ferrada[PSCV LDL < 70]` — «LDL < 70»
- **Values:** `Ferrada[PSCV LDL >160]` — «LDL >160»
- **Values:** `Ferrada[PSCV PA/Hba1c/LDL alta]` — «PA/Hba1c/LDL alta»
- **Values:** `Ferrada[PSCV ECG]` — «ECG»
- **Values:** `Ferrada[PSCV ECG Fecha]` — «ECG Fecha»
- **Values:** `Ferrada[PSCV ECG ¿Vigente?]` — «ECG ¿Vigente?»
- **Values:** `Ferrada[PSCV Lab Fecha (form)]` — «Lab Fecha»
- **Values:** `Ferrada[PSCV Crea]` — «Crea»
- **Values:** `Ferrada[PSCV VFG]` — «VFG»
- **Values:** `Ferrada[PSCV RAC]` — «RAC»
- **Values:** `Ferrada[PSCV COL]` — «COL»
- **Values:** `Ferrada[PSCV HDL]` — «HDL»
- **Values:** `Ferrada[PSCV LDL]` — «LDL»
- **Values:** `Ferrada[PSCV TG]` — «TG»
- **Values:** `Ferrada[PSCV Hipoglicemias]` — «¿Hipoglicemias?»
- **Values:** `Ferrada[PSCV Pie DM Riesgo]` — «Pie DM»
- **Values:** `Ferrada[PSCV Pie DM ¿Vigente?]` — «¿Pie DM Vigente?»
- **Values:** `Ferrada[PSCV Podología Vigente]` — «¿Podología Vigente?»
- **Values:** `Ferrada[PSCV Úlcera Pie DM]` — «¿Úlcera activa DM?»
- **Values:** `Ferrada[PSCV Amputación DM]` — «¿Amputación DM?»
- **Values:** `Ferrada[PSCV FO ¿Vigente?]` — «¿FO Vigente?»
- **Values:** `Ferrada[PSCV FO Retinopatía?]` — «¿Retinopatía?»
- **Values:** `Ferrada[PSCV RAC ¿Vigente?]` — «¿RAC Vigente?»
- **Values:** `Ferrada[PSCV VFG ¿Vigente?]` — «¿VFG Vigente?»
- **Values:** `Ferrada[PSCV LDL ¿Vigente?]` — «¿LDL Vigente?»
- **Values:** `Ferrada[PSCV IECA o ARA II?]` — «¿IECA o ARA II?»
- **Values:** `Ferrada[PSCV Antiagregante Plaq]` — «¿Antiag Plaquetario?»
- **Values:** `Ferrada[PSCV Estatina]` — «¿Estatina?»
- **Values:** `Ferrada[PSCV Losartán]` — «Losartán»
- **Values:** `Ferrada[PSCV Amlodipino]` — «Amlodipino»
- **Values:** `Ferrada[PSCV Hidroclorotiazida]` — «Hidroclorotiazida»
- **Values:** `Ferrada[PSCV Enalapril]` — «Enalapril»
- **Values:** `Ferrada[PSCV Atenolol]` — «Atenolol»
- **Values:** `Ferrada[PSCV Carvedilol]` — «Carvedilol»
- **Values:** `Ferrada[PSCV Metformina]` — «Metformina»
- **Values:** `Ferrada[PSCV Metformina 1000]` — «Metformina 1000»
- **Values:** `Ferrada[PSCV Insulina]` — «Insulina»
- **Values:** `Ferrada[PSCV Educación Insulina]` — «Educación Insulina»
- **Values:** `Ferrada[PSCV Educación Insulina (fecha)]` — «Educación Insulina (fecha)»
- **Values:** `Ferrada[Vildagliptina]`
- **Values:** `Ferrada[PSCV Empagliflozina]` — «Empaglifozina»
- **Values:** `Ferrada[PSCV Atorvastatina]` — «Atorvastatina»
- **Values:** `Ferrada[PSCV Aspirina]` — «Aspirina»
- **Values:** `Ferrada[PSCV ¿Candidato Vildagliptina?]` — «¿Candidato Vildagliptina?»
- **Values:** `Ferrada[PSCV ¿Candidato Empaglifozina?]` — «¿Candidato Empaglifozina?»
- **Values:** `Ferrada[PSCV ¿Candidato Insulina?]` — «¿Candidato Insulina?»
- **Values:** `Ferrada[PSCV PHQ-9 (fecha)]` — «PHQ-9 (fecha)»
- **Values:** `Ferrada[PSCV Último control]` — «Último control»
- **Values:** `Ferrada[PSCV 1º Control]` — «1º Control»
- **Values:** `Ferrada[PSCV 2º Control]` — «2º Control»
- **Values:** `Ferrada[PSCV 3º Control]` — «3º Control»
- **Values:** `Ferrada[PSCV 4º Control]` — «4º Control»
- **Values:** SUM(`Ferrada[Trans]`) — «Suma de Trans»

### 25. Empagliflozina — `slicer`

- **Values:** `Ferrada[PSCV Empagliflozina]`

### 26. ¿ECV? — `slicer`

- **Values:** `Ferrada[PSCV ECV]`

### 27. ¿IAM? — `slicer`

- **Values:** `Ferrada[PSCV IAM]`

### 28. Receta Vig — `slicer`

- **Values:** `Ferrada[PSCV Receta Vigente?]`

### 29. IMC — `slicer`

- **Values:** `Ferrada[IMC (resultado)]`

### 30. Pie DM Vig — `slicer`

- **Values:** `Ferrada[PSCV Pie DM ¿Vigente?]`

### 31. Metformina — `slicer`

- **Values:** `Ferrada[PSCV Metformina]` — «Metformina»

### 32. DLP — `slicer`

- **Values:** `Ferrada[PSCV DLP]`

### 33. LDL >160 — `slicer`

- **Values:** `Ferrada[PSCV LDL >160]`

### 34. Promedio de VFG y RAC — `lineChart`

- **Category:** `Ferrada[Edad rango 10]`
- **Tooltips:** MIN(`Ferrada[Edad]`) — «Mín. de Edad»
- **Y:** MEDIAN(`Ferrada[PSCV VFG]`) — «Mediana de PSCV VFG»
- **Y:** MEDIAN(`Ferrada[PSCV RAC]`) — «Mediana de PSCV RAC»

### 35. Total de personas — `card`

- **Values:** DISTINCTCOUNT(`Ferrada[RUN]`) — «Nº de personas»

### 36. Atenolol — `slicer`

- **Values:** `Ferrada[PSCV Atenolol]`

### 37. ¿Ingresado? — `slicer`

- **Values:** `Ferrada[PSCV ¿Ingresado?]` — «¿Ingresado PSCV?»

### 38. Etapa VFG — `slicer`

- **Values:** `Ferrada[PSCV VFG Etapa]`

### 39. DM — `slicer`

- **Values:** `Ferrada[PSCV DM]`

### 40. ¿RAC Alta? — `slicer`

- **Values:** `Ferrada[PSCV RAC Alta]`

### 41. Compensado — `slicer`

- **Values:** `Ferrada[PSCV DLP ¿compensado?]`

### 42. Compensado — `slicer`

- **Values:** `Ferrada[PSCV DM ¿compensada?]`

### 43. Meses — `slicer`

- **Values:** `Ferrada[Meses]` — «Edad Meses»

### 44. HTA — `slicer`

- **Values:** `Ferrada[PSCV HTA]`

### 45. ECG Vigente — `slicer`

- **Values:** `Ferrada[PSCV ECG ¿Vigente?]`

### 46. ¿Activo 12m? — `slicer`

- **Values:** `Ferrada[¿Atendido en 12m?]`

### 47. Compensado — `slicer`

- **Values:** `Ferrada[PSCV HTA ¿compensada?]`

### 48. Años — `slicer`

- **Values:** `Ferrada[Edad]`

### 49. Migra/Origin — `slicer`

- **Values:** `Ferrada[¿Originario o Migrante?]`

### 50. PA >160/100 — `slicer`

- **Values:** `Ferrada[PSCV PA >160/100]`

### 51. TBQ historico — `slicer`

- **Values:** `Ferrada[PSCV TBQ historico]`

### 52. Estratificacion — `slicer`

- **Values:** `Ferrada[Estratificación]`

### 53. Promedio de HbA1c — `lineChart`

- **Category:** `Ferrada[Edad rango 10]`
- **Series:** `Ferrada[PSCV Insulina]` — «Insulina»
- **Tooltips:** MIN(`Ferrada[Edad]`) — «Mín. de Edad»
- **Y:** MEDIAN(`Ferrada[PSCV HbA1c (última)]`) — «Mediana de PSCV HbA1c (última)»

### 54. Etapa RAC — `slicer`

- **Values:** `Ferrada[PSCV RAC Etapa]`

### 55. Gemfibrozilo — `slicer`

- **Values:** `Ferrada[PSCV Gemfibrozilo]`

### 56. ¿Activo CV? — `slicer`

- **Values:** `Ferrada[PSCV Asistente]`

### 57. EMPAM — `slicer`

- **Values:** `Ferrada[Citar a EMPAM]`

### 58. Situación — `slicer`

- **Values:** `Ferrada[Situación]`

### 59. HbA1c >9 — `slicer`

- **Values:** `Ferrada[PSCV HbA1c >9]`

### 60. ¿ACV? — `slicer`

- **Values:** `Ferrada[PSCV ACV]`

### 61. Atorvastatina — `slicer`

- **Values:** `Ferrada[PSCV Atorvastatina]`

### 62. ¿PHQ-9? — `slicer`

- **Values:** `Ferrada[PSCV PHQ-9?]` — «PSCV PHQ-9?1»

---

## Anexo: lógica de los campos usados

### `Ferrada[Celular]`

Número de celular desde «Inscritos»; se descartan valores con menos de 8 dígitos (BLANK).

*Tipo:* int64  ·  *calculatedColumn*

```dax
IF(
    LEN(
        LOOKUPVALUE(Inscritos[MOVIL CONTACTO],Inscritos[RUN],'Ferrada'[RUN]))<8,
        BLANK(),
        LOOKUPVALUE(Inscritos[MOVIL CONTACTO],Inscritos[RUN],'Ferrada'[RUN]
    )
)
```

### `Ferrada[Citar a EMPAM]`

Estado EMPAM (≥65 años): «Rescatar» si el último EMP tiene más de 365 días al cierre del mes anterior; «Vigente» si no. BLANK en menores.

```dax
VAR FechaReferencia = EOMONTH(TODAY(), -1) // Último día del mes anterior
VAR FechaInicioVigencia = FechaReferencia - 365

VAR FechaEMPA =
    CALCULATE(
        MAX(Atenciones[FECHA ATENCION]),
        FILTER(
            ALL(Atenciones),
            Atenciones[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING(Atenciones[FORMULARIOS CLINICOS], "emp -")
        )
    )

RETURN
SWITCH(
    TRUE(),
    'Ferrada'[Edad] < 65, BLANK(),
    ISBLANK(FechaEMPA) || FechaEMPA < FechaInicioVigencia, "Rescatar",
    FechaEMPA >= FechaInicioVigencia, "Vigente",
    BLANK()
)
```

### `Ferrada[Citar a PAP]`

Estado PAP (mujeres 25-64): vigencia de 3 años (1095 días) considerando actividades PAP, diagnóstico z12.4 y el PAP histórico. «Rescatar» / «Vigente» / BLANK si no corresponde.

```dax
VAR FechaReferencia = EOMONTH(TODAY(), -1)
VAR FechaInicioVigencia = FechaReferencia - 1095 

VAR FechaAtencion =
    CALCULATE(
        MAX(Atenciones[FECHA ATENCION]),
        FILTER(
            ALL(Atenciones),
            Atenciones[RUN] = 'Ferrada'[RUN] &&
            (
                CONTAINSSTRING(Atenciones[ACTIVIDADES], "examen pap") ||
                CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "z12.4")
            )
        )
    )

VAR FechaFormulario =
    CALCULATE(
        MAX('PAP Histórico'[1.- Fecha Examen PAP]),
        FILTER(
            ALL('PAP Histórico'),
            'PAP Histórico'[RUN] = 'Ferrada'[RUN]
        )
    )

VAR FechaPAP = MAXX({FechaAtencion, FechaFormulario}, [Value])

RETURN
SWITCH(
    TRUE(),
    'Ferrada'[Sexo] <> "mujer" ||
    'Ferrada'[Edad] < 25 ||
    'Ferrada'[Edad] >= 65, BLANK(),
    ISBLANK(FechaPAP) || FechaPAP < FechaInicioVigencia, "Rescatar",
    FechaPAP >= FechaInicioVigencia, "Vigente",
    BLANK()
)
```

### `Ferrada[Dirección Completa]`

Dirección completa concatenada desde «Inscritos» (tipo de vía + calle + número, comuna, provincia, región, país). BLANK si falta calle, tipo de vía, número o comuna.

```dax
VAR Calle     = LOOKUPVALUE(Inscritos[CALLE RESIDENCIAL], Inscritos[RUN], 'Ferrada'[RUN])
VAR TipoVia   = LOOKUPVALUE(Inscritos[TIPO VIA RESIDENCIAL], Inscritos[RUN], 'Ferrada'[RUN])
VAR Numero    = LOOKUPVALUE(Inscritos[NUMERO RESIDENCIAL], Inscritos[RUN], 'Ferrada'[RUN])
VAR Comuna    = LOOKUPVALUE(Inscritos[COMUNA RESIDENCIAL], Inscritos[RUN], 'Ferrada'[RUN])
VAR Provincia = LOOKUPVALUE(Inscritos[PROVINCIA RESIDENCIAL], Inscritos[RUN], 'Ferrada'[RUN])
VAR Region    = LOOKUPVALUE(Inscritos[REGIÓN RESIDENCIAL], Inscritos[RUN], 'Ferrada'[RUN])
VAR Pais      = LOOKUPVALUE(Inscritos[PAIS], Inscritos[RUN], 'Ferrada'[RUN])

VAR CamposFaltantes =
    Calle IN {BLANK(), ""} ||
    TipoVia IN {BLANK(), ""} ||
    Numero IN {BLANK(), ""} ||
    Comuna IN {BLANK(), ""}

RETURN
IF(
    CamposFaltantes,
    BLANK(),
    TRIM(
        TipoVia & " " & Calle & " " & Numero & ", " &
        Comuna & ", " & Provincia & ", " & Region & ", " & Pais
    )
)
```

### `Ferrada[Edad]`

Edad en años cumplidos: días entre nacimiento y hoy divididos por 365,25 (truncado). Si no hay fecha de nacimiento usa EDAD AÑOS de «Inscritos». Al usar TODAY(), cambia con cada actualización del modelo.

*Tipo:* double  ·  *calculatedColumn*

```dax
VAR Hoy = TODAY()
VAR Nacimiento = [Fecha Nacimiento].[Date]
VAR DiasTotales = DATEDIFF(Nacimiento, Hoy, DAY)
VAR EdadExacta = 
    INT(DiasTotales / 365.25)
RETURN

IF(ISBLANK(EdadExacta),
LOOKUPVALUE(Inscritos[EDAD AÑOS],Inscritos[RUN],'Ferrada'[RUN]),
EdadExacta)
```

### `Ferrada[Edad rango 10]`

Tramo etario decenal («0 a 9 años» … «80 o más años»).

```dax
var _Edad = 'Ferrada'[Edad]
RETURN
SWITCH(
    TRUE(),
    _Edad <10,"0 a 9 años",
    _Edad <20,"10 a 19 años",
    _Edad <30,"20 a 29 años",
    _Edad <40,"30 a 39 años",
    _Edad <50,"40 a 49 años",
    _Edad <60,"50 a 59 años",
    _Edad <70,"60 a 69 años",
    _Edad <80,"70 a 79 años"
    ,"80 o más años")
```

### `Ferrada[Estado]`

Trae por cruce de RUN el valor de «ESTADO» desde la tabla «Inscritos» hacia esta tabla (LOOKUPVALUE). Copia directa, sin transformación.

```dax
LOOKUPVALUE(Inscritos[ESTADO],Inscritos[RUN],'Ferrada'[RUN])
```

### `Ferrada[Estratificación]`

Trae por cruce de RUN el valor de «Estratificación de Riesgo Actual» desde la tabla «Estratificacion» hacia esta tabla (LOOKUPVALUE). Copia directa, sin transformación.

```dax
LOOKUPVALUE(Estratificacion[Estratificación de Riesgo Actual],Estratificacion[RUN],'Ferrada'[RUN])
```

### `Ferrada[Fecha Nacimiento]`

Fecha de nacimiento: primero «Inscritos», con respaldo en «PVI actualizada».

*Tipo:* dateTime  ·  *calculatedColumn*

```dax
VAR FechaInscrito = 
LOOKUPVALUE(Inscritos[FECHA DE NACIMIENTO], Inscritos[RUN], 'Ferrada'[RUN])

VAR FechaPVI = 
LOOKUPVALUE('PVI actualizada'[FECHA_NACIMIENTO], 'PVI actualizada'[RUN], 'Ferrada'[RUN])

RETURN 

IF(ISBLANK(FechaInscrito),FechaPVI,FechaInscrito)
```

### `Ferrada[Fecha Pasivación]`

Trae por cruce de RUN el valor de «FECHA PASIVACION» desde la tabla «Inscritos» hacia esta tabla (LOOKUPVALUE). Copia directa, sin transformación.

```dax
LOOKUPVALUE(Inscritos[FECHA PASIVACION],Inscritos[RUN],'Ferrada'[RUN])
```

### `Ferrada[Género]`

Género registrado en «Inscritos». BLANK si no hay.

```dax
IF(ISBLANK(LOOKUPVALUE(Inscritos[GENERO],Inscritos[RUN],'Ferrada'[RUN])),BLANK(),LOOKUPVALUE(Inscritos[GENERO],Inscritos[RUN],'Ferrada'[RUN]))
```

### `Ferrada[IMC (resultado)]`

Clasificación del IMC con cortes diferenciados por edad: <65 años (bajo peso <18,5; normal <25; sobrepeso <30; obesidad ≥30) y ≥65 (bajo peso <23; normal <28; sobrepeso <32; obesidad ≥32). Sin IMC registrado devuelve «Sin Datos» (corregido jul-2026: antes asumía «Normal»).

```dax
SWITCH(
    TRUE(),
    ISBLANK('Ferrada'[IMC]),"Sin Datos",
    ('Ferrada'[Edad] < 65 && 'Ferrada'[IMC] < 18.5 ||
    'Ferrada'[Edad] >= 65 && 'Ferrada'[IMC] < 23),"Bajo Peso",
    ('Ferrada'[Edad] < 65 && 'Ferrada'[IMC] < 25 ||
    'Ferrada'[Edad] >= 65 && 'Ferrada'[IMC] < 28),"Normal",
    ('Ferrada'[Edad] < 65 && 'Ferrada'[IMC] < 30 ||
    'Ferrada'[Edad] >= 65 && 'Ferrada'[IMC] < 32),"Sobrepeso",
    "Obesidad")
```

### `Ferrada[Letra]`

Tramo/letra previsional: convenio previsional de «Inscritos»; si está vacío usa el TRAMO de «PVI actualizada».

```dax
IF(ISBLANK(LOOKUPVALUE(Inscritos[CONVENIO PREVISIONAL],Inscritos[RUN],'Ferrada'[RUN])),LOOKUPVALUE('PVI actualizada'[TRAMO],'PVI actualizada'[RUN],'Ferrada'[RUN]),LOOKUPVALUE(Inscritos[CONVENIO PREVISIONAL],Inscritos[RUN],'Ferrada'[RUN]))
```

### `Ferrada[Mail]`

Correo electrónico desde «Inscritos»; BLANK si vacío.

```dax
var _Inscripcion = 
LOOKUPVALUE(Inscritos[EMAIL],Inscritos[RUN],'Ferrada'[RUN])

RETURN

IF(
    _Inscripcion="",BLANK(),_Inscripcion
)
```

### `Ferrada[Meses]`

Componente «meses» de la edad (para lactantes: edad expresada en años, meses y días). Con respaldo en EDAD MESES de «Inscritos».

```dax
VAR Hoy = TODAY()
VAR Nacimiento = [Fecha Nacimiento].[Date]
VAR MesActual = MONTH(Hoy)
VAR MesNacimiento = MONTH(Nacimiento)
VAR AnioActual = YEAR(Hoy)
VAR AnioNacimiento = YEAR(Nacimiento)
VAR DiaActual = DAY(Hoy)
VAR DiaNacimiento = DAY(Nacimiento)
VAR MesesDelAnioActual = 
    IF(
        ISBLANK(Nacimiento),
        BLANK(),
        IF(
            MesActual > MesNacimiento || (MesActual = MesNacimiento && DiaActual >= DiaNacimiento),
            MesActual - MesNacimiento,
            MesActual - MesNacimiento + 12
        ) - IF(DiaActual < DiaNacimiento, 1, 0)
    )
RETURN

IF(ISBLANK(MesesDelAnioActual),
LOOKUPVALUE(Inscritos[EDAD MESES],Inscritos[RUN],'Ferrada'[RUN]),
MesesDelAnioActual)
```

### `Ferrada[Motivo Pasivación]`

Trae por cruce de RUN el valor de «MOTIVO PASIVACION» desde la tabla «Inscritos» hacia esta tabla (LOOKUPVALUE). Copia directa, sin transformación.

```dax
LOOKUPVALUE(Inscritos[MOTIVO PASIVACION],Inscritos[RUN],'Ferrada'[RUN])
```

### `Ferrada[Nacionalidad]`

Trae por cruce de RUN el valor de «NACIONALIDAD» desde la tabla «Inscritos» hacia esta tabla (LOOKUPVALUE). Copia directa, sin transformación.

```dax
LOOKUPVALUE(Inscritos[NACIONALIDAD],Inscritos[RUN],'Ferrada'[RUN])
```

### `Ferrada[Nombre Social]`

Nombre social desde «Inscritos» (campo NOMBRE RESPONDE). BLANK si está vacío.

```dax
IF(
TRIM(LOOKUPVALUE(Inscritos[NOMBRE RESPONDE],Inscritos[RUN],'Ferrada'[RUN]))="",BLANK(),
TRIM(LOOKUPVALUE(Inscritos[NOMBRE RESPONDE],Inscritos[RUN],'Ferrada'[RUN])))
```

### `Ferrada[Nombre completo]`

Nombre completo: concatena [Nombres] + [Apellido Paterno] + [Apellido Materno].

```dax
CONCATENATE('Ferrada'[Nombres] & " " & 'Ferrada'[Apellido Paterno] & " ",'Ferrada'[Apellido Materno])
```

### `Ferrada[PSCV 1º Control]`

Primer control del año PSCV: si está ingresado y su último control médico CV es anterior al 1 de enero de hace dos años (o no existe), marca «Rescatar»; si no, muestra el mes del último control con «(Med)».

```dax
VAR _FechaUltimoControl = DATEVALUE('Ferrada'[PSCV Último Control Médico (fecha)].[Date])
VAR _FechaLimite = DATE(YEAR(TODAY()) - 2, 1, 1)

VAR _NecesitaRescate = 
    'Ferrada'[PSCV ¿Ingresado?] = "SI" &&
    (ISBLANK(_FechaUltimoControl) || _FechaUltimoControl < _FechaLimite)

VAR _Fecha = 
    IF(_NecesitaRescate, EOMONTH(TODAY(), 1), _FechaUltimoControl)

VAR _Instrumento = IF(ISBLANK(_Fecha), BLANK(), "Med")

RETURN
SWITCH(
    TRUE(),
    _NecesitaRescate, "Rescatar",
    ISBLANK(_Fecha), BLANK(),
    FORMAT(_Fecha, "MMMM") & " (" & _Instrumento & ")"
)
```

### `Ferrada[PSCV 2º Control]`

Segundo control PSCV programado: suma meses al último control médico según riesgo (Alto: +3 meses con Enfermería; Moderado: +4 con Nutrición; Bajo: +6 con Enfermería). Solo si está ingresado y no requiere rescate.

```dax
VAR _FechaUltimoControl = 'Ferrada'[PSCV Último Control Médico (fecha)].[Date]

VAR _Fecha = 
    SWITCH(
        TRUE(),
        ISBLANK(_FechaUltimoControl), BLANK(),
        'Ferrada'[PSCV Riesgo CV] = "Alto", EDATE(_FechaUltimoControl, 3),
        'Ferrada'[PSCV Riesgo CV] = "Moderado", EDATE(_FechaUltimoControl, 4),
        'Ferrada'[PSCV Riesgo CV] = "Bajo", EDATE(_FechaUltimoControl, 6)
    )

VAR _Instrumento = 
    SWITCH(
        TRUE(),
        ISBLANK(_FechaUltimoControl), BLANK(),
        'Ferrada'[PSCV Riesgo CV] = "Alto", "Enf",
        'Ferrada'[PSCV Riesgo CV] = "Moderado", "Nutri",
        'Ferrada'[PSCV Riesgo CV] = "Bajo", "Enf"
    )

RETURN
SWITCH(
    TRUE(),
    Ferrada[PSCV 1º Control]="rescatar",BLANK(),
    'Ferrada'[PSCV ¿Ingresado?] = "SI" && NOT ISBLANK(_Fecha),
    FORMAT(_Fecha, "MMMM") & " (" & _Instrumento & ")",
    BLANK()
)
```

### `Ferrada[PSCV 3º Control]`

Tercer control PSCV programado: Alto +6 meses (Nutrición); Moderado +8 (Enfermería). Bajo no tiene tercer control. Solo si está ingresado y no requiere rescate.

```dax
VAR _FechaUltimoControl = 'Ferrada'[PSCV Último Control Médico (fecha)].[Date]

VAR _Fecha = 
    SWITCH(
        TRUE(),
        ISBLANK(_FechaUltimoControl), BLANK(),
        'Ferrada'[PSCV Riesgo CV] = "Alto", EDATE(_FechaUltimoControl, 6),
        'Ferrada'[PSCV Riesgo CV] = "Moderado", EDATE(_FechaUltimoControl, 8)
    )

VAR _Instrumento = 
    SWITCH(
        TRUE(),
        ISBLANK(_FechaUltimoControl), BLANK(),
        'Ferrada'[PSCV Riesgo CV] = "Alto", "Nutri",
        'Ferrada'[PSCV Riesgo CV] = "Moderado", "Enf"
    )

RETURN
SWITCH(
    TRUE(),
    Ferrada[PSCV 1º Control]="rescatar",BLANK(),
    'Ferrada'[PSCV ¿Ingresado?] = "SI" && NOT ISBLANK(_Fecha),
    FORMAT(_Fecha, "MMMM") & " (" & _Instrumento & ")",
    BLANK()
)
```

### `Ferrada[PSCV 4º Control]`

Cuarto control PSCV programado: solo riesgo Alto, +9 meses (Enfermería). Solo si está ingresado y no requiere rescate.

```dax
VAR _FechaUltimoControl = 'Ferrada'[PSCV Último Control Médico (fecha)].[Date]

VAR _Fecha = 
    SWITCH(
        TRUE(),
        ISBLANK(_FechaUltimoControl), BLANK(),
        'Ferrada'[PSCV Riesgo CV] = "Alto", EDATE(_FechaUltimoControl, 9)
    )

VAR _Instrumento = 
    SWITCH(
        TRUE(),
        ISBLANK(_FechaUltimoControl), BLANK(),
        'Ferrada'[PSCV Riesgo CV] = "Alto", "Enf"
    )

RETURN
SWITCH(
    TRUE(),
    Ferrada[PSCV 1º Control]="rescatar",BLANK(),
    'Ferrada'[PSCV ¿Ingresado?] = "SI" && NOT ISBLANK(_Fecha),
    FORMAT(_Fecha, "MMMM") & " (" & _Instrumento & ")",
    BLANK()
)
```

### `Ferrada[PSCV ACV]`

ACV SI/NO: el último formulario PSCV con la pregunta 38 (¿ha presentado AVE?) respondida dice «sí», o diagnóstico I60-I64/I69 en atención médica.

```dax
var _Fecha =
LASTDATE(
    CALCULATETABLE(VALUES(PSCV[FECHA ATENCION]),
        FILTER(
            PSCV,
            PSCV[RUN]='Ferrada'[RUN] &&
            PSCV[38.- ¿HA PRESENTADO AVE?] <> ""
        )
    )
)

var _Formularios =
IF(
    CALCULATE(COUNT(PSCV[RUN]),
        FILTER(
            PSCV,
            PSCV[RUN]='Ferrada'[RUN] &&
            PSCV[FECHA ATENCION] = _Fecha &&
            CONTAINSSTRING(PSCV[38.- ¿HA PRESENTADO AVE?],"si")
        )
    ),"SI","NO"
)

var _Atenciones = 
IF(
    CALCULATE(count(Atenciones[RUN]),
        FILTER(
            'Atenciones',
            Atenciones[RUN]='Ferrada'[RUN] &&
            CONTAINSSTRING(Atenciones[INSTRUMENTO],"médic") &&
            (
                CONTAINSSTRING(Atenciones[DIAGNOSTICOS],"I60") ||
                CONTAINSSTRING(Atenciones[DIAGNOSTICOS],"I61") ||
                CONTAINSSTRING(Atenciones[DIAGNOSTICOS],"I62") ||
                CONTAINSSTRING(Atenciones[DIAGNOSTICOS],"I63") ||
                CONTAINSSTRING(Atenciones[DIAGNOSTICOS],"I64") ||
                CONTAINSSTRING(Atenciones[DIAGNOSTICOS],"I69")
            )
        )
    ),
    "SI","NO"
)

RETURN

IF(
    _Formularios="SI" ||
    _Atenciones="SI",
    "SI","NO"
)
```

### `Ferrada[PSCV Act Fisica]`

Actividad física según el último formulario PSCV con la pregunta 11 respondida: «SI» si ese registro más reciente dice «sí». (Corregido jul-2026: la versión anterior respondía «SI» ante cualquier «sí» histórico, sin que un «no» posterior la revirtiera.)

```dax
VAR _Fecha =
LASTDATE(
    CALCULATETABLE(VALUES(PSCV[FECHA ATENCION]),
    FILTER(ALL(PSCV),
        PSCV[RUN] = 'Ferrada'[RUN] &&
        PSCV[11.- REALIZA  ACTIVIDAD  FÍSICA] <> "")))

RETURN
IF(
    CALCULATE(COUNT(PSCV[RUN]),
    FILTER(ALL(PSCV),
        PSCV[RUN] = 'Ferrada'[RUN] &&
        PSCV[FECHA ATENCION] = _Fecha &&
        CONTAINSSTRING(PSCV[11.- REALIZA  ACTIVIDAD  FÍSICA],"si"))),
    "SI","NO")
```

### `Ferrada[PSCV Amlodipino]`

Amlodipino SI/NO: receta interna vigente o externa que contenga «amlodipino».

```dax
var _Externa = 
IF(
    CALCULATE(COUNT('Recetas Externas'[RUN]),
    FILTER(ALL('Recetas Externas'),'Recetas Externas'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Recetas Externas'[Medicamento],"amlodipino"))),
    "SI","NO")

var _Interna = 
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"amlodipino"))),
    "SI","NO")

RETURN

IF(
    _Externa="SI" ||
    _Interna="SI",
    "SI","NO")
```

### `Ferrada[PSCV Amputación DM]`

Amputación por DM SI/NO: figura en Estratificación como amputado, o algún formulario PSCV con pregunta 43 (¿amputación debida a DM?) o 143 (historia de úlcera/amputación en pies) marcada «sí».

```dax
IF(
    LOOKUPVALUE(Estratificacion[Amputación por DM],Estratificacion[RUN],'Ferrada'[RUN])="SI" ||
        IF(CALCULATE(COUNT(PSCV[RUN]),
            FILTER(
                PSCV,
                PSCV[RUN]='Ferrada'[RUN] &&
                (
                    CONTAINSSTRING(PSCV[43.- ¿AMPUTACIÓN DEBIDA A DM?],"si") ||
                    CONTAINSSTRING(PSCV[143.- ¿ HISTORIA DE ÚLCERA O AMPUTACIÓN EN UNO O AMBOS P],"si")
                )
            )
        ),"SI","NO")="SI",
    "SI","NO"
)
```

### `Ferrada[PSCV Antiagregante Plaq]`

Antiagregante plaquetario SI/NO: [PSCV Aspirina], [PSCV Clopidogrel (Ext)], o el último formulario PSCV médico con tratamiento farmacológico que mencione antiagregante o ácido acetilsalicílico.

```dax
var _Fecha = 
LASTDATE(
    CALCULATETABLE(VALUES(PSCV[FECHA ATENCION]),
    FILTER(ALL(PSCV),PSCV[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING(PSCV[INSTRUMENTO],"médic"))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSCV[RUN]),
    FILTER(ALL(PSCV),PSCV[RUN]='Ferrada'[RUN] &&
    PSCV[FECHA ATENCION]=_Fecha &&
    (CONTAINSSTRING(PSCV[15.- EN TRATAMIENTO FARMACOLOGICO],"antiagre") ||
    CONTAINSSTRING(PSCV[15.- EN TRATAMIENTO FARMACOLOGICO],"ácido acetil")))),
    "SI","NO")

RETURN

IF(
    'Ferrada'[PSCV Aspirina]="SI" ||
    'Ferrada'[PSCV Clopidogrel (Ext)]="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[PSCV Asistente]`

Asistencia al PSCV: «SI» si el último control cardiovascular cae dentro de los 12 meses cerrados, o si está ingresado y su última consulta CV cae en esa ventana. (Limpiada jul-2026: se eliminó una variable de receta que no se usaba.)

*Tipo:* string  ·  *calculatedColumn*

```dax
VAR _FechaInicio = 
EOMONTH(TODAY(),-13) + 1

VAR _FechaFinal = 
EOMONTH(TODAY(),-1)

VAR _FechaControl = 
LASTDATE(
    CALCULATETABLE(VALUES('Atenciones'[FECHA ATENCION]), 
    FILTER( ALL('Atenciones'), 'Atenciones'[RUN] = 'Ferrada'[RUN] && 
    (CONTAINSSTRING('Atenciones'[ACTIVIDADES], "control de salud cardiovascular") ||
    CONTAINSSTRING(Atenciones[FORMULARIOS CLINICOS],"cardiovascular")))))

var _AsistenteControl = 
IF( 
    NOT ISBLANK(_FechaControl) &&
    _FechaControl >= _FechaInicio &&
    _FechaControl <= _FechaFinal,
    "SI","NO")

var _FechaConsulta = 
LASTDATE(
    CALCULATETABLE(VALUES(Atenciones[FECHA ATENCION]),
    FILTER(ALL(Atenciones),Atenciones[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING(Atenciones[ACTIVIDADES],"consulta cardiovas"))))

var _AsistentePoli = 
IF(
    'Ferrada'[PSCV ¿Ingresado?]="si" &&
    NOT ISBLANK(_FechaConsulta) &&
    _FechaConsulta >= _FechaInicio &&
    _FechaConsulta <= _FechaFinal,
    "SI","NO")

RETURN

IF(
    _AsistenteControl="SI" ||
    _AsistentePoli="SI",
    "SI","NO")
```

### `Ferrada[PSCV Aspirina]`

Aspirina SI/NO: receta externa con «acetilsali» o receta interna vigente con «cido acetil» (ácido acetilsalicílico).

```dax
var _Externa = 
IF(CALCULATE(COUNT('Recetas Externas'[RUN]),
FILTER(ALL('Recetas Externas'),'Recetas Externas'[RUN]='Ferrada'[RUN] &&
CONTAINSSTRING('Recetas Externas'[Medicamento],"acetilsali"))),
"SI","NO")

Var _Interna = 
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"cido acetil"))),
    "SI","NO")

RETURN

IF(
    _Externa="SI" ||
    _Interna="SI",
    "SI","NO")
```

### `Ferrada[PSCV Atenolol]`

Indicador SI/NO: existe al menos una receta vigente (tabla «Recetas Vigentes») cuya descripción de artículo contiene «atenolo».

```dax
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"atenolo"))),
    "SI","NO")
```

### `Ferrada[PSCV Atorvastatina]`

Indicador SI/NO: el paciente tiene al menos una receta vigente del establecimiento (tabla «Recetas Vigentes») cuya descripción de artículo contiene «atorvastatina».

```dax
IF(CALCULATE(count('Recetas Vigentes'[RUN]),
FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] && 
CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"atorvastatina"))),
"SI","NO")
```

### `Ferrada[PSCV COL]`

Valor de colesterol total consolidado de tres fuentes (formulario PSCV, laboratorio HEC 2024, laboratorio Holanda; búsqueda: «colesterol total/tot» en labs, pregunta 81 del formulario): de cada fuente toma el registro más reciente y gana el de fecha más nueva. (Corregido jul-2026: se eliminó el respaldo histórico erróneo que leía HbA1c de Estratificación, y las columnas que elegían el valor más alto en vez del más reciente.) Nota vigente: las descargas masivas de laboratorio (HEC/Holanda) están descontinuadas desde ~2025; en la práctica hoy alimenta solo el formulario PSCV. La lógica por fecha hace que los datos congelados pierdan naturalmente contra registros nuevos.

```dax
VAR _FechaHEC =
    CALCULATE(
        MAX('Laboratorio (resultado) HEC 2024'[Fecha Ingreso]),
        FILTER(
            'Laboratorio (resultado) HEC 2024',
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "colesterol total")
        )
    )

VAR _HEC =
    CALCULATE(
        FIRSTNONBLANK('Laboratorio (resultado) HEC 2024'[Resultado],1),
        FILTER(
            'Laboratorio (resultado) HEC 2024',
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] &&
            'Laboratorio (resultado) HEC 2024'[Fecha Ingreso] = _FechaHEC &&
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "colesterol total")
        )
    )

VAR _FechaHOLANDA =
    CALCULATE(
        MAX('Laboratorio Holanda'[Fecha Ingreso]),
        FILTER(
            'Laboratorio Holanda',
            'Laboratorio Holanda'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "colesterol tot") &&
            NOT CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "hdl")
        )
    )

VAR _HOLANDA =
    CALCULATE(
        FIRSTNONBLANK('Laboratorio Holanda'[Resultado],1),
        FILTER(
            'Laboratorio Holanda',
            'Laboratorio Holanda'[RUN] = 'Ferrada'[RUN] &&
            'Laboratorio Holanda'[Fecha Ingreso] = _FechaHOLANDA &&
            CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "colesterol tot") &&
            NOT CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "hdl")
        )
    )

VAR _FechaPSCV =
    CALCULATE(
        MAX(PSCV[54.- FECHA DE REALIZACIÓN DE BATERÍA DE EXÁMEN *]),
        FILTER('PSCV',
        PSCV[RUN] = 'Ferrada'[RUN] &&
        NOT ISBLANK(PSCV[81.- COLESTEROL TOTAL (MG/DL)]))
    )

VAR _ValorPSCV =
    CALCULATE(
        FIRSTNONBLANK(PSCV[81.- COLESTEROL TOTAL (MG/DL)],1),
        FILTER(PSCV,
        PSCV[RUN] = 'Ferrada'[RUN] &&
        PSCV[54.- FECHA DE REALIZACIÓN DE BATERÍA DE EXÁMEN *] = _FechaPSCV)
    )



-- Consolidamos fechas y valores
VAR _Tabla =
    {
        (_FechaHEC, _HEC),
        (_FechaHOLANDA, _HOLANDA),
        (_FechaPSCV, _ValorPSCV)
    }

VAR _Ultimo =
    TOPN(
        1,
        FILTER(_Tabla, NOT ISBLANK([Value2])),
        [Value1], DESC
    )

VAR _ResultadoFinal =
    MAXX(_Ultimo, [Value2])

RETURN
    _ResultadoFinal
```

### `Ferrada[PSCV Carvedilol]`

Indicador SI/NO: existe al menos una receta vigente (tabla «Recetas Vigentes») cuya descripción de artículo contiene «carvedilo».

```dax
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"carvedilo"))),
    "SI","NO")
```

### `Ferrada[PSCV Crea]`

Creatinina consolidada de tres fuentes (lab HEC «reatinina», lab Holanda «creatinina» sin clearence, formulario PSCV pregunta 76): gana la fecha más reciente. Sin respaldo histórico.

```dax
VAR _FechaHEC =
    CALCULATE(
        MAX('Laboratorio (resultado) HEC 2024'[Fecha Ingreso]),
        FILTER(
            'Laboratorio (resultado) HEC 2024',
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "reatinina")
        )
    )

VAR _HEC =
    CALCULATE(
        FIRSTNONBLANK('Laboratorio (resultado) HEC 2024'[Resultado],1),
        FILTER(
            'Laboratorio (resultado) HEC 2024',
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] &&
            'Laboratorio (resultado) HEC 2024'[Fecha Ingreso] = _FechaHEC &&
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "reatinina")
        )
    )

VAR _FechaHOLANDA =
    CALCULATE(
        MAX('Laboratorio Holanda'[Fecha Ingreso]),
        FILTER(
            'Laboratorio Holanda',
            'Laboratorio Holanda'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "creatinina") &&
            NOT CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "clearence")
        )
    )

VAR _HOLANDA =
    CALCULATE(
        FIRSTNONBLANK('Laboratorio Holanda'[Resultado],1),
        FILTER(
            'Laboratorio Holanda',
            'Laboratorio Holanda'[RUN] = 'Ferrada'[RUN] &&
            'Laboratorio Holanda'[Fecha Ingreso] = _FechaHOLANDA &&
            CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "creatinina") &&
            NOT CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "clearence")
        )
    )

VAR _FechaPSCV =
    CALCULATE(
        MAX(PSCV[54.- FECHA DE REALIZACIÓN DE BATERÍA DE EXÁMEN *]),
        FILTER('PSCV',
        PSCV[RUN] = 'Ferrada'[RUN] &&
        NOT ISBLANK(PSCV[76.- CREATININA]))
    )

VAR _PSCV =
    CALCULATE(
        FIRSTNONBLANK(PSCV[76.- CREATININA],1),
        FILTER(PSCV,
        PSCV[RUN] = 'Ferrada'[RUN] &&
        PSCV[54.- FECHA DE REALIZACIÓN DE BATERÍA DE EXÁMEN *] = _FechaPSCV)
    )

-- Consolidamos fechas y valores
VAR _Tabla =
    {
        (_FechaHEC, _HEC),
        (_FechaHOLANDA, _HOLANDA),
        (_FechaPSCV, _PSCV)
    }

VAR _Ultimo =
    TOPN(
        1,
        FILTER(_Tabla, NOT ISBLANK([Value2])),
        [Value1], DESC
    )

VAR _ResultadoFinal =
    MAXX(_Ultimo, [Value2])

RETURN
    _ResultadoFinal
```

### `Ferrada[PSCV DLP]`

Dislipidemia SI/NO: último formulario PSCV con pregunta 26 respondida dice «sí», o diagnóstico E78 en Estratificación o en atenciones médicas.

```dax
var _Fecha = 
LASTDATE(
    CALCULATETABLE(VALUES(PSCV[FECHA ATENCION]),
        FILTER(
            PSCV,
            PSCV[RUN]='Ferrada'[RUN] &&
            PSCV[26.- ¿ES DISLIPIDÉMICO?] <> ""
        )
    )
)

var _Formulario = 
IF(
    CALCULATE(COUNT(PSCV[RUN]),
        FILTER(
            PSCV,
            PSCV[RUN]='Ferrada'[RUN] &&
            PSCV[FECHA ATENCION]=_Fecha &&
            CONTAINSSTRING(PSCV[26.- ¿ES DISLIPIDÉMICO?],"si")
        )
    ),"SI","NO"
)


/*var _Atenciones = 
IF(
    CALCULATE(COUNT(Estratificacion[RUN]),
        FILTER(
            Estratificacion,
            Estratificacion[RUN]='Ferrada'[RUN] &&
            CONTAINSSTRING(Estratificacion[Diagnósticos],"E78")
        )
    ) > 0
||
    CALCULATE(count(Atenciones[RUN]),
        FILTER(
            Atenciones,
            Atenciones[RUN]='Ferrada'[RUN] &&
            (
                CONTAINSSTRING(Atenciones[INSTRUMENTO],"médico") &&
                CONTAINSSTRING(Atenciones[DIAGNOSTICOS],"E78")
            )
        )
    ) > 0,
    "SI","NO"
)
*/
RETURN

_Formulario
```

### `Ferrada[PSCV DLP ¿compensado?]`

Compensación de dislipidemia según meta por riesgo: descompensado (NO) si LDL≥130 con riesgo bajo, ≥100 con moderado o ≥70 con alto; «SI» en caso contrario.

```dax
IF(
    'Ferrada'[PSCV Riesgo CV]="bajo" && 'Ferrada'[PSCV LDL] >= 130 ||
    'Ferrada'[PSCV Riesgo CV]="moderado" && 'Ferrada'[PSCV LDL] >= 100 ||
    'Ferrada'[PSCV Riesgo CV]="alto" && 'Ferrada'[PSCV LDL] >= 70,
    "NO","SI")
```

### `Ferrada[PSCV DM]`

Diabetes tipo 2 SI/NO: el último formulario PSCV con la pregunta 22 respondida dice «sí», o diagnóstico E10-E14 en Estratificación o Atenciones.

```dax
var _Fecha = 
LASTDATE(
    CALCULATETABLE(VALUES(PSCV[FECHA ATENCION]),
        FILTER(
            PSCV,
            PSCV[RUN] = 'Ferrada'[RUN] &&
            PSCV[22.- ¿ES DM2?] <> ""
        )
    )
)

var _Formulario = 
IF(
    CALCULATE(COUNT(PSCV[RUN]),
        FILTER(
            PSCV,
            PSCV[RUN] = 'Ferrada'[RUN] &&
            PSCV[FECHA ATENCION] = _Fecha &&
            CONTAINSSTRING(PSCV[22.- ¿ES DM2?],"si")
        )
    ) > 0,
    "SI","NO"
)

var _Atenciones = 
IF(
    CALCULATE(COUNT(Estratificacion[RUN]),
        FILTER
        (Estratificacion,
        Estratificacion[RUN] = 'Ferrada'[RUN] &&
            (
                CONTAINSSTRING(Estratificacion[Diagnósticos],"E10") ||
                CONTAINSSTRING(Estratificacion[Diagnósticos],"E11") ||
                CONTAINSSTRING(Estratificacion[Diagnósticos],"E12") ||
                CONTAINSSTRING(Estratificacion[Diagnósticos],"E13") ||
                CONTAINSSTRING(Estratificacion[Diagnósticos],"E14")
            )
        )
    ) > 0

    ||

    CALCULATE(COUNT(Atenciones[RUN]),
        FILTER(
            Atenciones,
            Atenciones[RUN] = 'Ferrada'[RUN] &&
            (
                CONTAINSSTRING(Atenciones[DIAGNOSTICOS],"E10") ||
                CONTAINSSTRING(Atenciones[DIAGNOSTICOS],"E11") ||
                CONTAINSSTRING(Atenciones[DIAGNOSTICOS],"E12") ||
                CONTAINSSTRING(Atenciones[DIAGNOSTICOS],"E13") ||
                CONTAINSSTRING(Atenciones[DIAGNOSTICOS],"E14")
            )
        )
    ) > 0,
    "SI","NO"
)

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO"
)
```

### `Ferrada[PSCV DM ¿compensada?]`

Compensación de DM según última HbA1c: «NO» si (<80 años y HbA1c≥7) o (≥80 y ≥8); «SI» si está bajo esos umbrales; «Sin Datos» si no hay HbA1c registrada (corregido jul-2026: antes el paciente sin examen aparecía compensado).

```dax
IF(
    ISBLANK('Ferrada'[PSCV HbA1c (última)]),
    "Sin Datos",
IF(
    ('Ferrada'[Edad] < 80  && 'Ferrada'[PSCV HbA1c (última)] >= 7) ||
    ('Ferrada'[Edad] >= 80 && 'Ferrada'[PSCV HbA1c (última)] >= 8),
    "NO", "SI"))
```

### `Ferrada[PSCV ECG]`

Resultado del ECG más reciente registrado en el formulario PSCV (pregunta 90). BLANK si no hay.

```dax
VAR RUNPaciente = 'Ferrada'[RUN]
VAR FechaUltimoECG =
CALCULATE(
    MAX(PSCV[91.- FECHA Y HORA].[Date]),
    FILTER(
        ALL(PSCV),
        PSCV[RUN] = RUNPaciente &&
        NOT(ISBLANK(PSCV[90.- ELECTROCARDIOGRAMA]))
    )
)

VAR ECGFormularioActual =
CALCULATE(
    MAX(PSCV[90.- ELECTROCARDIOGRAMA]),
    FILTER(
        ALL(PSCV),
        PSCV[RUN] = RUNPaciente &&
        PSCV[91.- FECHA Y HORA].[Date] = FechaUltimoECG &&
        NOT(ISBLANK(PSCV[90.- ELECTROCARDIOGRAMA]))
    )
)

RETURN
IF(
    ISBLANK(ECGFormularioActual),BLANK(),ECGFormularioActual
)
```

### `Ferrada[PSCV ECG Fecha]`

Fecha del último ECG: máximo entre la fecha registrada en el formulario PSCV (pregunta 91) y la última atención con actividad «electrocardio».

```dax
var _Fecha12m = 
LASTDATE(
    CALCULATETABLE(VALUES(PSCV[91.- FECHA Y HORA].[Date]),
    FILTER(ALL(PSCV),PSCV[RUN]='Ferrada'[RUN])))

var _Atenciones = 
LASTDATE(CALCULATETABLE(VALUES(Atenciones[FECHA ATENCION]),
FILTER(ALL(Atenciones),Atenciones[RUN]='Ferrada'[RUN] &&
CONTAINSSTRING(Atenciones[ACTIVIDADES],"electrocardio"))))

RETURN

MAXX(
    {
        _Fecha12m, 
        _Atenciones},
        [Value])
```

### `Ferrada[PSCV ECG ¿Vigente?]`

Vigencia del ECG: «SI» si el último ECG tiene 12 meses o menos al cierre del mes anterior.

```dax
IF(
    ISBLANK('Ferrada'[PSCV ECG Fecha]) ||
    DATEDIFF('Ferrada'[PSCV ECG Fecha].[Date],EOMONTH(TODAY(),-1),MONTH) > 12,
    "NO","SI")
```

### `Ferrada[PSCV ECV]`

Enfermedad cardiovascular ateroesclerótica SI/NO: [PSCV IAM] o [PSCV ACV] en «SI», o último formulario con antecedentes CV (preguntas 28/17) marcado «sí».

```dax
var _Fecha = 
LASTDATE(
    CALCULATETABLE(VALUES(PSCV[FECHA ATENCION]),
        FILTER(
            PSCV,
            PSCV[RUN] = 'Ferrada'[RUN] &&
            (
                PSCV[28.- ¿TIENE ANTECEDENTES ENF. CARDIOVASCULAR ATEROSCLER] <> "" ||
                PSCV[17.- ANTECEDENTES DE OTRAS ENFERMEDADES CARDIOVASCULARE] <> ""
            )
        )
    )
)

var _Formulario = 
IF(
    CALCULATE(COUNT(PSCV[RUN]),
        FILTER(
            PSCV,
            PSCV[RUN] = 'Ferrada'[RUN] &&
            PSCV[FECHA ATENCION]=_Fecha &&
            (
                CONTAINSSTRING(PSCV[28.- ¿TIENE ANTECEDENTES ENF. CARDIOVASCULAR ATEROSCLER],"si") ||
                CONTAINSSTRING(PSCV[17.- ANTECEDENTES DE OTRAS ENFERMEDADES CARDIOVASCULARE],"si")
            )
        )
    ) > 0,
    "SI","NO"
)

RETURN

IF(
    'Ferrada'[PSCV IAM]="SI" || 
    'Ferrada'[PSCV ACV]="SI" ||
    _Formulario="SI",
    "SI","NO"
)
```

### `Ferrada[PSCV ERC]`

ERC SI/NO por criterios de laboratorio: VFG<45, o RAC>30, o (VFG<60 con RAC≤30 en paciente de 15-64 años). Nota: revisar el segundo criterio — exigir RAC≤30 junto a VFG 45-59 es poco habitual (KDIGO clasificaría G3a con cualquier RAC); podría ser intencional para capturar G3a sin albuminuria, pero vale la pena confirmarlo.

```dax
IF(
(NOT ISBLANK(Ferrada[PSCV VFG]) && 'Ferrada'[PSCV VFG]< 45) ||
(NOT ISBLANK(Ferrada[PSCV VFG]) && 'Ferrada'[PSCV VFG]< 60 && NOT ISBLANK(Ferrada[PSCV RAC]) && Ferrada[PSCV RAC] <= 30 && Ferrada[Edad] >= 15 && Ferrada[Edad] < 65) ||
(NOT ISBLANK(Ferrada[PSCV RAC]) && 'Ferrada'[PSCV RAC]>30),
"SI","NO")
```

### `Ferrada[PSCV Educación Insulina]`

Educación en insulina SI/NO: alguna atención de enfermería con actividad «educación insulina».

```dax
IF(
    CALCULATE(COUNT(Atenciones[RUN]),
    FILTER(ALL(Atenciones),Atenciones[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(Atenciones[INSTRUMENTO],"enferme") &&
    CONTAINSSTRING(Atenciones[ACTIVIDADES],"educacion insuli")))),
    "SI","NO")
```

### `Ferrada[PSCV Educación Insulina (fecha)]`

Fecha de la última educación en insulina por enfermería.

```dax
LASTDATE(
    CALCULATETABLE(VALUES(Atenciones[FECHA ATENCION]),
    FILTER(ALL(Atenciones),Atenciones[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(Atenciones[ACTIVIDADES],"educacion insuli") &&
    CONTAINSSTRING(Atenciones[INSTRUMENTO],"enferme")))))
```

### `Ferrada[PSCV Empagliflozina]`

Indicador SI/NO: existe al menos una receta vigente (tabla «Recetas Vigentes») cuya descripción de artículo contiene «empagliflo».

```dax
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"empagliflo"))),
    "SI","NO")
```

### `Ferrada[PSCV Enalapril]`

Indicador SI/NO: existe al menos una receta vigente (tabla «Recetas Vigentes») cuya descripción de artículo contiene «enalapril».

```dax
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"enalapril"))),
    "SI","NO")
```

### `Ferrada[PSCV Estatina]`

Estatina SI/NO: receta externa con «vastatina», formulario PSCV con tratamiento que mencione «estatin», o receta interna de atorvastatina o lovastatina.

```dax
VAR _Externa = 
IF(
    CALCULATE(COUNT('Recetas Externas'[RUN]),
        FILTER(
            'Recetas Externas',
            'Recetas Externas'[RUN]='Ferrada'[RUN] &&
            CONTAINSSTRING('Recetas Externas'[Medicamento],"vastatina"
            )
        )
    ),"SI","NO"
)

VAR _Receta = 
IF(
    CALCULATE(COUNT(PSCV[RUN]),
        FILTER(
            PSCV,PSCV[RUN]='Ferrada'[RUN] &&
            CONTAINSSTRING(PSCV[15.- EN TRATAMIENTO FARMACOLOGICO],"estatin"
            )
        )
    ),"SI","NO"
)

RETURN

IF(
    _Externa="SI" ||
    _Receta="SI" ||
    'Ferrada'[PSCV Atorvastatina]="SI" ||
    'Ferrada'[PSCV Lovastatina]="SI",
    "SI","NO"
)
```

### `Ferrada[PSCV FO Retinopatía?]`

Retinopatía en fondo de ojo SI/NO: pregunta 97 del formulario PSCV marcada «sí» en cualquier registro.

```dax
VAR _RDForm12m = 
    IF(
        CALCULATE(
            COUNT(PSCV[RUN]),
            FILTER(
                ALL(PSCV),
                PSCV[RUN] = 'Ferrada'[RUN] &&
                PSCV[97.- RETINOPATÍA] = "si"
            )
        ) > 0,
        "SI",
        "NO"
    )

RETURN
IF(
    _RDForm12m = "SI",
    "SI",
    "NO"
)
```

### `Ferrada[PSCV FO ¿Vigente?]`

Vigencia del fondo de ojo: «SI» si la fecha de realización (pregunta 107) cae dentro de la ventana de 12 meses cerrados. Nota: un fondo de ojo del mes en curso (posterior al cierre) da «NO» hasta el próximo corte.

```dax
VAR _FechaInicio = 
EOMONTH(TODAY(),-13) + 1

VAR _FechaFinal = 
EOMONTH(TODAY(),-1)

VAR _FechaForm12m = 
    CALCULATE(
        MAX(PSCV[107.- FECHA DE REALIZACIÓN]),
        FILTER(
            ALL(PSCV),
            PSCV[RUN] = 'Ferrada'[RUN]
        )
    )

RETURN
IF(
    _FechaForm12m >= _FechaInicio &&
    _FechaForm12m <= _FechaFinal,
    "SI","NO"
)
```

### `Ferrada[PSCV Gemfibrozilo]`

Indicador SI/NO: existe al menos una receta vigente (tabla «Recetas Vigentes») cuya descripción de artículo contiene «gemfibrozilo».

```dax
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"gemfibrozilo"))),
    "SI","NO")
```

### `Ferrada[PSCV HDL]`

Valor de colesterol HDL consolidado de tres fuentes (formulario PSCV, laboratorio HEC 2024, laboratorio Holanda; búsqueda: «hdl» en labs, pregunta correspondiente del formulario): de cada fuente toma el registro más reciente y gana el de fecha más nueva. (Corregido jul-2026: se eliminó el respaldo histórico erróneo que leía HbA1c de Estratificación, y las columnas que elegían el valor más alto en vez del más reciente.) Nota vigente: las descargas masivas de laboratorio (HEC/Holanda) están descontinuadas desde ~2025; en la práctica hoy alimenta solo el formulario PSCV. La lógica por fecha hace que los datos congelados pierdan naturalmente contra registros nuevos.

```dax
VAR _FechaHEC =
    CALCULATE(
        MAX('Laboratorio (resultado) HEC 2024'[Fecha Ingreso]),
        FILTER(
            'Laboratorio (resultado) HEC 2024',
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "hdl")
        )
    )

VAR _HEC =
    CALCULATE(
        FIRSTNONBLANK('Laboratorio (resultado) HEC 2024'[Resultado],1),
        FILTER(
            'Laboratorio (resultado) HEC 2024',
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] &&
            'Laboratorio (resultado) HEC 2024'[Fecha Ingreso] = _FechaHEC &&
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "hdl")
        )
    )

VAR _FechaHOLANDA =
    CALCULATE(
        MAX('Laboratorio Holanda'[Fecha Ingreso]),
        FILTER(
            'Laboratorio Holanda',
            'Laboratorio Holanda'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "colesterol hdl")
        )
    )

VAR _HOLANDA =
    CALCULATE(
        FIRSTNONBLANK('Laboratorio Holanda'[Resultado],1),
        FILTER(
            'Laboratorio Holanda',
            'Laboratorio Holanda'[RUN] = 'Ferrada'[RUN] &&
            'Laboratorio Holanda'[Fecha Ingreso] = _FechaHOLANDA &&
            CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "colesterol hdl")
        )
    )

VAR _FechaPSCV =
    CALCULATE(
        MAX(PSCV[54.- FECHA DE REALIZACIÓN DE BATERÍA DE EXÁMEN *]),
        FILTER('PSCV',
        PSCV[RUN] = 'Ferrada'[RUN] &&
        NOT ISBLANK(PSCV[82.- COLESTEROL HDL (MG/DL)]))
    )

VAR _ValorPSCV =
    CALCULATE(
        FIRSTNONBLANK(PSCV[82.- COLESTEROL HDL (MG/DL)],1),
        FILTER(PSCV,
        PSCV[RUN] = 'Ferrada'[RUN] &&
        PSCV[54.- FECHA DE REALIZACIÓN DE BATERÍA DE EXÁMEN *] = _FechaPSCV)
    )



-- Consolidamos fechas y valores
VAR _Tabla =
    {
        (_FechaHEC, _HEC),
        (_FechaHOLANDA, _HOLANDA),
        (_FechaPSCV, _ValorPSCV)
    }

VAR _Ultimo =
    TOPN(
        1,
        FILTER(_Tabla, NOT ISBLANK([Value2])),
        [Value1], DESC
    )

VAR _ResultadoFinal =
    MAXX(_Ultimo, [Value2])

RETURN
    _ResultadoFinal
```

### `Ferrada[PSCV HEARTS]`

Protocolo HEARTS SI/NO: algún formulario PSCV médico con pregunta 51 (protocolo HEARTS) marcada «sí», o receta compatible con esquema HEARTS ([PSCV HEARTS receta]).

```dax
var _Formularios = 
IF(
    CALCULATE(COUNT(PSCV[RUN]),
    FILTER(ALL(PSCV),PSCV[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSCV[51.- PROTOCOLO HEARTS],"si") &&
    CONTAINSSTRING(PSCV[INSTRUMENTO],"médic")))),
    "SI","NO")

RETURN

IF(
    _Formularios="SI" ||
    'Ferrada'[PSCV HEARTS receta]="SI",
    "SI","NO"
)
```

### `Ferrada[PSCV HTA]`

Hipertensión SI/NO: diagnóstico CIE-10 I1* en Estratificación o en Atenciones, o pregunta 20 del formulario PSCV («¿es HTA?») marcada «sí» en cualquier registro.

```dax
VAR _Dg = 
    IF(
        CALCULATE(
            COUNT(Estratificacion[RUN]),
            FILTER(
                ALL(Estratificacion),
                Estratificacion[RUN] = 'Ferrada'[RUN] &&
                CONTAINSSTRING(Estratificacion[Diagnósticos], "I1")
            )
        ) > 0 ||
        CALCULATE(
            COUNT(Atenciones[RUN]),
            FILTER(
                ALL(Atenciones),
                Atenciones [RUN] = 'Ferrada'[RUN] &&
                CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "I1")
            )
        ) > 0,
        "SI",
        "NO"
    )

VAR _Form = 
    IF(
        CALCULATE(
            COUNT(PSCV[RUN]),
            FILTER(
                ALL(PSCV),
                PSCV[RUN] = 'Ferrada'[RUN] &&
                PSCV[20.- ¿ES HTA?] = "si"
            )
        ) > 0,
        "SI",
        "NO"
    )

RETURN
    IF(
        _Dg = "SI" || 
        _Form = "SI",
        "SI",
        "NO"
    )
```

### `Ferrada[PSCV HTA Refractaria?]`

HTA refractaria SI/NO: la pregunta 16 del formulario PSCV está marcada «sí» en cualquier registro histórico.

```dax
IF(
    CALCULATE(COUNT(PSCV[RUN]),
        FILTER(
            PSCV,
            Ferrada[RUN] = PSCV[RUN] &&
            PSCV[16.- HIPERTENSIÓN ARTERIAL REFRACTARIA]="si"
        )
    ),"SI","NO"
)
```

### `Ferrada[PSCV HTA ¿compensada?]`

Compensación de HTA según última PA: «NO» si (<80 años y PAS≥140 o PAD≥90) o (≥80 y PAS≥150 o PAD≥90); «SI» bajo umbral; «Sin Datos» si falta PAS o PAD (corregido jul-2026: antes el paciente sin control aparecía compensado).

```dax
IF(
    ISBLANK('Ferrada'[PSCV PAS (última)]) || ISBLANK('Ferrada'[PSCV PAD (última)]),
    "Sin Datos",
IF(
    ('Ferrada'[Edad] < 80  && ('Ferrada'[PSCV PAS (última)] >= 140 || 'Ferrada'[PSCV PAD (última)] >= 90)) ||
    ('Ferrada'[Edad] >= 80 && ('Ferrada'[PSCV PAS (última)] >= 150 || 'Ferrada'[PSCV PAD (última)] >= 90)),
    "NO", "SI"))
```

### `Ferrada[PSCV HbA1c (primera)]`

Primera HbA1c registrada: valor de la fuente con fecha más antigua entre lab HEC, lab Holanda y formulario PSCV (con respaldo histórico de Estratificación).

```dax
VAR _FechaHEC =
    CALCULATE(
        MIN('Laboratorio (resultado) HEC 2024'[Fecha Ingreso]),
        FILTER(
            'Laboratorio (resultado) HEC 2024',
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "glicosilada")
        )
    )

VAR _HEC =
    CALCULATE(
        FIRSTNONBLANK('Laboratorio (resultado) HEC 2024'[Resultado],1),
        FILTER(
            'Laboratorio (resultado) HEC 2024',
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] &&
            'Laboratorio (resultado) HEC 2024'[Fecha Ingreso] = _FechaHEC &&
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "glicosilada")
        )
    )

VAR _FechaHOLANDA =
    CALCULATE(
        MIN('Laboratorio Holanda'[Fecha Ingreso]),
        FILTER(
            'Laboratorio Holanda',
            'Laboratorio Holanda'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "glicada")
        )
    )

VAR _HOLANDA =
    CALCULATE(
        FIRSTNONBLANK('Laboratorio Holanda'[Resultado],1),
        FILTER(
            'Laboratorio Holanda',
            'Laboratorio Holanda'[RUN] = 'Ferrada'[RUN] &&
            'Laboratorio Holanda'[Fecha Ingreso] = _FechaHOLANDA &&
            CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "glicada")
        )
    )

VAR _FechaPSCV =
    CALCULATE(
        MIN(PSCV[58.- FECHA HEMOGLOBINA GLICOSILADA (HBA1C)]),
        FILTER(PSCV,
        PSCV[RUN] = 'Ferrada'[RUN] &&
        NOT ISBLANK(PSCV[59.- HEMOGLOBINA GLICOSILADA (HBA1C)]))
    )

VAR _PSCV =
    CALCULATE(
        FIRSTNONBLANK(PSCV[59.- HEMOGLOBINA GLICOSILADA (HBA1C)],1),
        FILTER(PSCV,
        PSCV[RUN] = 'Ferrada'[RUN] &&
        PSCV[58.- FECHA HEMOGLOBINA GLICOSILADA (HBA1C)] = _FechaPSCV)
    )

VAR _Historica =
    LOOKUPVALUE(Estratificacion[HbA1c], Estratificacion[RUN], 'Ferrada'[RUN])

VAR _ValorPSCV =
    IF(ISBLANK(_PSCV), _Historica, _PSCV)

-- Consolidamos fechas y valores
VAR _Tabla =
    {
        (_FechaHEC, _HEC),
        (_FechaHOLANDA, _HOLANDA),
        (_FechaPSCV, _ValorPSCV)
    }

VAR _Primero =
    TOPN(
        1,
        FILTER(_Tabla, NOT ISBLANK([Value2])),
        [Value1], ASC
    )

VAR _ResultadoFinal =
    MAXX(_Primero, [Value2])


RETURN
    _ResultadoFinal
```

### `Ferrada[PSCV HbA1c (última)]`

HbA1c más reciente consolidada de tres fuentes: laboratorio HEC («glicosilada»), laboratorio Holanda («glicada») y formulario PSCV (pregunta 59, con respaldo histórico de Estratificación). Gana el valor con fecha más nueva. Valida rango clínico: valores >30 o <2 se descartan (BLANK).

```dax
VAR _FechaHEC =
    CALCULATE(
        MAX('Laboratorio (resultado) HEC 2024'[Fecha Ingreso]),
        FILTER(
            'Laboratorio (resultado) HEC 2024',
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "glicosilada")
        )
    )

VAR _HEC =
    CALCULATE(
        FIRSTNONBLANK('Laboratorio (resultado) HEC 2024'[Resultado],1),
        FILTER(
            'Laboratorio (resultado) HEC 2024',
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] &&
            'Laboratorio (resultado) HEC 2024'[Fecha Ingreso] = _FechaHEC &&
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "glicosilada")
        )
    )

VAR _FechaHOLANDA =
    CALCULATE(
        MAX('Laboratorio Holanda'[Fecha Ingreso]),
        FILTER(
            'Laboratorio Holanda',
            'Laboratorio Holanda'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "glicada")
        )
    )

VAR _HOLANDA =
    CALCULATE(
        FIRSTNONBLANK('Laboratorio Holanda'[Resultado],1),
        FILTER(
            'Laboratorio Holanda',
            'Laboratorio Holanda'[RUN] = 'Ferrada'[RUN] &&
            'Laboratorio Holanda'[Fecha Ingreso] = _FechaHOLANDA &&
            CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "glicada")
        )
    )

VAR _FechaPSCV =
    CALCULATE(
        MAX(PSCV[58.- FECHA HEMOGLOBINA GLICOSILADA (HBA1C)]),
        FILTER('PSCV',
        PSCV[RUN] = 'Ferrada'[RUN] &&
        NOT ISBLANK(PSCV[59.- HEMOGLOBINA GLICOSILADA (HBA1C)]))
    )

VAR _PSCV =
    CALCULATE(
        FIRSTNONBLANK(PSCV[59.- HEMOGLOBINA GLICOSILADA (HBA1C)],1),
        FILTER(PSCV,
        PSCV[RUN] = 'Ferrada'[RUN] &&
        PSCV[58.- FECHA HEMOGLOBINA GLICOSILADA (HBA1C)] = _FechaPSCV)
    )

VAR _Historica =
    LOOKUPVALUE(Estratificacion[HbA1c], Estratificacion[RUN], 'Ferrada'[RUN])

VAR _ValorPSCV =
    IF(ISBLANK(_PSCV), _Historica, _PSCV)

-- Consolidamos fechas y valores
VAR _Tabla =
    {
        (_FechaHEC, _HEC),
        (_FechaHOLANDA, _HOLANDA),
        (_FechaPSCV, _ValorPSCV)
    }

VAR _Ultimo =
    TOPN(
        1,
        FILTER(_Tabla, NOT ISBLANK([Value2])),
        [Value1], DESC
    )

VAR _ResultadoFinal =
    MAXX(_Ultimo, [Value2])

RETURN
IF(
    _ResultadoFinal > 30 || _ResultadoFinal < 2,BLANK(),_ResultadoFinal)
```

### `Ferrada[PSCV HbA1c >9]`

Indicador SI/NO: última HbA1c ≥9%. Nota: el nombre dice «>9» pero la fórmula usa ≥9.

```dax
IF('Ferrada'[PSCV HbA1c (última)]>=9,"SI","NO")
```

### `Ferrada[PSCV HbA1c Fecha (primera)]`

Fecha de la primera HbA1c registrada (mínimo entre formulario PSCV, lab HEC y lab Holanda). BLANK si no hay valor.

```dax
var _Formulario12m = 
        CALCULATE(
            MIN(PSCV[58.- FECHA HEMOGLOBINA GLICOSILADA (HBA1C)]),
            FILTER(
                PSCV,
                PSCV[RUN] = 'Ferrada'[RUN] &&
                NOT ISBLANK(PSCV[59.- HEMOGLOBINA GLICOSILADA (HBA1C)])
            )
        )

VAR _FechaHEC = 
    CALCULATE(
        MIN('Laboratorio (resultado) HEC 2024'[Fecha Ingreso].[Date]),
        FILTER(
            'Laboratorio (resultado) HEC 2024',
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "glicosilada")
        )
    )

VAR _FechaHolanda = 
    CALCULATE(
        MIN('Laboratorio Holanda'[Fecha Ingreso].[Date]),
        FILTER(
            'Laboratorio Holanda',
            'Laboratorio Holanda'[RUN]='Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "glicada")
        )
    )

RETURN

IF(
    ISBLANK(Ferrada[PSCV HbA1c (primera)]),BLANK(),
    MINX(
        {
            _Formulario12m,
            _FechaHEC,
            _FechaHolanda
        },
        [Value]
    )
)
```

### `Ferrada[PSCV HbA1c Fecha (última)]`

Fecha de la HbA1c más reciente: máximo entre la fecha del formulario PSCV (pregunta 58), lab HEC y lab Holanda. BLANK si no hay valor de HbA1c.

```dax
var _Formulario12m = 
        CALCULATE(
            MAX(PSCV[58.- FECHA HEMOGLOBINA GLICOSILADA (HBA1C)]),
            FILTER(
                PSCV,
                PSCV[RUN] = 'Ferrada'[RUN]
            )
        )

VAR _FechaHEC = 
    CALCULATE(
        MAX('Laboratorio (resultado) HEC 2024'[Fecha Ingreso].[Date]),
        FILTER(
            'Laboratorio (resultado) HEC 2024',
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "glicosilada")
        )
    )

VAR _FechaHolanda = 
    CALCULATE(
        MAX('Laboratorio Holanda'[Fecha Ingreso].[Date]),
        FILTER(
            'Laboratorio Holanda',
            'Laboratorio Holanda'[RUN]='Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "glicada")
        )
    )

RETURN

IF(
    ISBLANK('Ferrada'[PSCV HbA1c (última)]),BLANK(),
    MAXX(
        {
            _Formulario12m,
            _FechaHEC,
            _FechaHolanda
        },
        [Value]
    )
)
```

### `Ferrada[PSCV Hidroclorotiazida]`

Indicador SI/NO: el paciente tiene al menos una receta vigente del establecimiento (tabla «Recetas Vigentes») cuya descripción de artículo contiene «hidroclorotia».

```dax
IF(CALCULATE(count('Recetas Vigentes'[RUN]),
FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"hidroclorotia"))),
"SI","NO")
```

### `Ferrada[PSCV Hipoglicemias]`

Hipoglicemias recurrentes SI/NO: algún formulario PSCV médico con la pregunta 69 marcada «sí» (revisa el histórico completo).

```dax
VAR _Fecha = 
CALCULATE(
    MIN(PSCV[FECHA ATENCION]),
    FILTER(PSCV,
    PSCV[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING(PSCV[INSTRUMENTO],"médic") &&
    CONTAINSSTRING(PSCV[69.- HIPOGLICEMIAS RECURRENTES *],"si")))

VAR _Formulario = 
IF(
    CALCULATE(COUNT(PSCV[RUN]),
    FILTER(PSCV,
    PSCV[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING(PSCV[INSTRUMENTO],"médic") &&
    PSCV[FECHA ATENCION]=_Fecha)),
    "SI","NO")

RETURN
IF(
    _Formulario="SI",
    "SI","NO"
)
```

### `Ferrada[PSCV IAM]`

Infarto (IAM) SI/NO: diagnóstico I25 en alguna atención o pregunta 36 del formulario PSCV marcada «sí».

```dax
VAR _Dg = 
    IF(
        CALCULATE(
            COUNT(Atenciones[RUN]),
            FILTER(
                ALL(Atenciones),
                Atenciones [RUN] = 'Ferrada'[RUN] &&
                CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "I25")
            )
        ) > 0,
        "SI",
        "NO"
    )

VAR _Form = 
    IF(
        CALCULATE(
            COUNT(PSCV[RUN]),
            FILTER(
                ALL(PSCV),
                PSCV[RUN] = 'Ferrada'[RUN] &&
                PSCV[36.- ¿HA PRESENTADO IAM?] = "si"
            )
        ) > 0,
        "SI",
        "NO"
    )

RETURN
    IF(
        _Dg = "SI" || 
        _Form = "SI",
        "SI",
        "NO"
    )
```

### `Ferrada[PSCV IECA o ARA II?]`

IECA o ARA-II SI/NO: receta de losartán o enalapril, o formulario PSCV cuyo tratamiento farmacológico menciona IECA o ARA.

```dax
IF(
    'Ferrada'[PSCV Losartán]="SI" ||
    'Ferrada'[PSCV Enalapril]="SI" ||
    IF(CALCULATE(COUNT(PSCV[RUN]),
    FILTER(ALL(PSCV),PSCV[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSCV[15.- EN TRATAMIENTO FARMACOLOGICO],"ieca") ||
    CONTAINSSTRING(PSCV[15.- EN TRATAMIENTO FARMACOLOGICO],"ARA")))),"SI","NO")="SI",
    "SI","NO")
```

### `Ferrada[PSCV Insulina]`

Insulina SI/NO: receta interna vigente o receta externa que contenga «insulina».

```dax
var _RecetaVigente = 
IF(CALCULATE(count('Recetas Vigentes'[RUN]),
FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"insulina"))),
"SI","NO")

var _RecetaExterna = 
IF(CALCULATE(COUNT('Recetas Externas'[RUN]),
FILTER(ALL('Recetas Externas'),'Recetas Externas'[RUN] = Ferrada[RUN] &&
CONTAINSSTRING('Recetas Externas'[Medicamento],"insulina"))),
"SI","NO")

RETURN

IF(
    _RecetaVigente = "SI" ||
    _RecetaExterna = "SI",
    "SI","NO")
```

### `Ferrada[PSCV LDL]`

Valor de colesterol LDL consolidado de tres fuentes (formulario PSCV, laboratorio HEC 2024, laboratorio Holanda; búsqueda: «ldl» en labs, pregunta 84 del formulario): de cada fuente toma el registro más reciente y gana el de fecha más nueva. (Corregido jul-2026: se eliminó el respaldo histórico erróneo que leía HbA1c de Estratificación, y las columnas que elegían el valor más alto en vez del más reciente.) Nota vigente: las descargas masivas de laboratorio (HEC/Holanda) están descontinuadas desde ~2025; en la práctica hoy alimenta solo el formulario PSCV. La lógica por fecha hace que los datos congelados pierdan naturalmente contra registros nuevos.

```dax
VAR _FechaHEC =
    CALCULATE(
        MAX('Laboratorio (resultado) HEC 2024'[Fecha Ingreso]),
        FILTER(
            'Laboratorio (resultado) HEC 2024',
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "ldl")
        )
    )

VAR _HEC =
    CALCULATE(
        FIRSTNONBLANK('Laboratorio (resultado) HEC 2024'[Resultado],1),
        FILTER(
            'Laboratorio (resultado) HEC 2024',
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] &&
            'Laboratorio (resultado) HEC 2024'[Fecha Ingreso] = _FechaHEC &&
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "ldl")
        )
    )

VAR _FechaHOLANDA =
    CALCULATE(
        MAX('Laboratorio Holanda'[Fecha Ingreso]),
        FILTER(
            'Laboratorio Holanda',
            'Laboratorio Holanda'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "colesterol ldl")
        )
    )

VAR _HOLANDA =
    CALCULATE(
        FIRSTNONBLANK('Laboratorio Holanda'[Resultado],1),
        FILTER(
            'Laboratorio Holanda',
            'Laboratorio Holanda'[RUN] = 'Ferrada'[RUN] &&
            'Laboratorio Holanda'[Fecha Ingreso] = _FechaHOLANDA &&
            CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "colesterol ldl")
        )
    )

VAR _FechaPSCV =
    CALCULATE(
        MAX(PSCV[54.- FECHA DE REALIZACIÓN DE BATERÍA DE EXÁMEN *]),
        FILTER('PSCV',
        PSCV[RUN] = 'Ferrada'[RUN] &&
        NOT ISBLANK(PSCV[84.- COLESTEROL LDL (MG/DL)]))
    )

VAR _ValorPSCV =
    CALCULATE(
        FIRSTNONBLANK(PSCV[84.- COLESTEROL LDL (MG/DL)],1),
        FILTER(PSCV,
        PSCV[RUN] = 'Ferrada'[RUN] &&
        PSCV[54.- FECHA DE REALIZACIÓN DE BATERÍA DE EXÁMEN *] = _FechaPSCV)
    )



-- Consolidamos fechas y valores
VAR _Tabla =
    {
        (_FechaHEC, _HEC),
        (_FechaHOLANDA, _HOLANDA),
        (_FechaPSCV, _ValorPSCV)
    }

VAR _Ultimo =
    TOPN(
        1,
        FILTER(_Tabla, NOT ISBLANK([Value2])),
        [Value1], DESC
    )

VAR _ResultadoFinal =
    MAXX(_Ultimo, [Value2])

RETURN
    _ResultadoFinal
```

### `Ferrada[PSCV LDL < 70]`

Indicador SI/NO: LDL <70 mg/dL (meta de alto riesgo alcanzada).

```dax
IF(
    'Ferrada'[PSCV LDL] < 70,
    "SI","NO")
```

### `Ferrada[PSCV LDL >160]`

Indicador SI/NO: LDL ≥160 mg/dL. Nota: el nombre dice «>160» pero la fórmula usa ≥.

```dax
IF(
    'Ferrada'[PSCV LDL]>=160,
    "SI","NO")
```

### `Ferrada[PSCV LDL ¿Vigente?]`

Vigencia del LDL: «SI» si la fecha más reciente entre formulario PSCV, lab HEC y lab Holanda tiene ≤12 meses.

```dax
VAR _HECFecha = 
    CALCULATE(
        MAX('Laboratorio (resultado) HEC 2024'[Fecha Ingreso]),
        FILTER(
            ALL('Laboratorio (resultado) HEC 2024'), 
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] && 
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "ldl")
        )
    )

VAR _FormFecha = 
    CALCULATE(
        MAX(PSCV[54.- FECHA DE REALIZACIÓN DE BATERÍA DE EXÁMEN *]),
        FILTER(
            PSCV, 
            PSCV[RUN] = 'Ferrada'[RUN] &&
            NOT ISBLANK(PSCV[84.- COLESTEROL LDL (MG/DL)])
        )
    )

var _HOLANDAfecha = 
LASTDATE(CALCULATETABLE(VALUES('Laboratorio Holanda'[Fecha Ingreso].[Date]),
FILTER(ALL('Laboratorio Holanda'),'Laboratorio Holanda'[RUN]='Ferrada'[RUN] &&
CONTAINSSTRING('Laboratorio Holanda'[Determinacion],"colesterol ldl"))))

var _FechaFinal =
MAXX(
    {_FormFecha,
    _HECFecha,
    _HOLANDAfecha},
    [Value])

RETURN

SWITCH(
    TRUE(),
    ISBLANK(_FechaFinal),"NO",
    DATEDIFF(_FechaFinal,TODAY(),MONTH) <= 12,"SI",
    "NO")
```

### `Ferrada[PSCV Lab Fecha (form)]`

Fecha de la última batería de exámenes registrada en formulario PSCV (pregunta 54). BLANK si nunca.

```dax
VAR _Fecha12m = 
    CALCULATE(
        MAX(PSCV[54.- FECHA DE REALIZACIÓN DE BATERÍA DE EXÁMEN *]),
        FILTER(
            PSCV,
            PSCV[RUN] = 'Ferrada'[RUN]
        )
    )

RETURN
    IF(
        ISBLANK(_Fecha12m),BLANK(),_Fecha12m
    )
```

### `Ferrada[PSCV Losartán]`

Indicador SI/NO: el paciente tiene al menos una receta vigente del establecimiento (tabla «Recetas Vigentes») cuya descripción de artículo contiene «losartan».

```dax
IF(CALCULATE(count('Recetas Vigentes'[RUN]),
FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] && 
CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"losartan"))),
"SI","NO")
```

### `Ferrada[PSCV Meses sin HbA1c]`

Meses transcurridos desde la última HbA1c hasta hoy.

```dax
DATEDIFF(
    'Ferrada'[PSCV HbA1c Fecha (última)],TODAY(),MONTH)
```

### `Ferrada[PSCV Meses sin PA]`

Meses transcurridos desde la última presión arterial registrada ([PSCV PA Fecha (última)]) hasta hoy (DATEDIFF en meses).

```dax
DATEDIFF(
        'Ferrada'[PSCV PA Fecha (última)].[Date],TODAY(),MONTH)
```

### `Ferrada[PSCV Metformina]`

Indicador SI/NO: el paciente tiene al menos una receta vigente del establecimiento (tabla «Recetas Vigentes») cuya descripción de artículo contiene «metformina».

```dax
IF(CALCULATE(count('Recetas Vigentes'[RUN]),
FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] && 
CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"metformina"))),
"SI","NO")
```

### `Ferrada[PSCV Metformina 1000]`

Indicador SI/NO: el paciente tiene al menos una receta vigente del establecimiento (tabla «Recetas Vigentes») cuya descripción de artículo contiene «metformina clor».

```dax
IF(CALCULATE(count('Recetas Vigentes'[RUN]),
FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] && 
CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"metformina clor"))),
"SI","NO")
```

### `Ferrada[PSCV PA (primera)]`

Concatena la presión arterial como texto «PAS/PAD» usando [PSCV PAS (primera)], [PSCV PAD (primera)]. BLANK si no hay PAS.

```dax
IF(ISBLANK(Ferrada[PSCV PAS (primera)]),BLANK(),
Ferrada[PSCV PAS (primera)] & "/" & Ferrada[PSCV PAD (primera)])
```

### `Ferrada[PSCV PA (última)]`

Concatena la presión arterial como texto «PAS/PAD» usando [PSCV PAS (última)], [PSCV PAD (última)]. BLANK si no hay PAS.

```dax
IF(ISBLANK(Ferrada[PSCV PAS (última)]),BLANK(),
Ferrada[PSCV PAS (última)] & "/" & Ferrada[PSCV PAD (última)])
```

### `Ferrada[PSCV PA >160/100]`

Indicador SI/NO: última PA con PAS≥160 o PAD≥100 (hipertensión etapa 2).

```dax
IF(
'Ferrada'[PSCV PAS (última)] >= 160 ||
'Ferrada'[PSCV PAD (última)] >= 100,
"SI","NO")
```

### `Ferrada[PSCV PA Fecha (primera)]`

Fecha de la primera presión arterial (mínimo entre las tres fuentes). BLANK si no hay PAS primera.

```dax
VAR _FechaFormulario =
    CALCULATE(
        MIN(PSCV[FECHA ATENCION]),
        FILTER(PSCV,
        PSCV[RUN] = Ferrada[RUN] &&
        NOT ISBLANK(PSCV[PAS]))
    )

VAR _FechaEF12m =
    CALCULATE(
        MIN('Examen físico general'[FECHA ATENCION]),
        FILTER('Examen físico general',
        'Examen físico general'[RUN] = Ferrada[RUN] &&
        NOT ISBLANK('Examen físico general'[PAS]))
    )

VAR _FechaEstratificacion =
    LOOKUPVALUE(Estratificacion[Fecha última PAS - PAD], Estratificacion[RUN], Ferrada[RUN])

RETURN

IF(
    ISBLANK(Ferrada[PSCV PAS (primera)]),BLANK(),
    MINX(
        {
            _FechaFormulario,
            _FechaEF12m,
            _FechaEstratificacion
        },
        [Value]
    )
)
```

### `Ferrada[PSCV PA Fecha (última)]`

Fecha de la última presión arterial (máximo entre las tres fuentes). BLANK si no hay PAS última.

```dax
VAR _FechaFormulario =
    CALCULATE(
        MAX(PSCV[FECHA ATENCION]),
        FILTER(PSCV,
        PSCV[RUN] = Ferrada[RUN] &&
        NOT ISBLANK(PSCV[PAS]))
    )

VAR _FechaEF12m =
    CALCULATE(
        MAX('Examen físico general'[FECHA ATENCION]),
        FILTER('Examen físico general',
        'Examen físico general'[RUN] = Ferrada[RUN] &&
        NOT ISBLANK('Examen físico general'[PAS]))
    )

VAR _FechaEstratificacion =
    LOOKUPVALUE(Estratificacion[Fecha última PAS - PAD], Estratificacion[RUN], Ferrada[RUN])

RETURN

IF(
    ISBLANK(Ferrada[PSCV PAS (última)]),BLANK(),
    MAXX(
        {
            _FechaFormulario,
            _FechaEF12m,
            _FechaEstratificacion
        },
        [Value]
    )
)
```

### `Ferrada[PSCV PA/Hba1c/LDL alta]`

Indicador de descompensación combinada: «SI» si la PA está sobre meta (mismos cortes por edad que [PSCV HTA ¿compensada?]), la HbA1c sobre meta (≥7 / ≥8 según edad) o el LDL ≥100. Para priorizar rescates.

```dax
var _PA = 
IF(OR(
    'Ferrada'[Edad] < 80 &&
    ('Ferrada'[PSCV PAS (última)] >= 140 ||
    'Ferrada'[PSCV PAD (última)] >= 90),
    'Ferrada'[Edad] >= 80 &&
    ('Ferrada'[PSCV PAS (última)] >= 150 ||
    'Ferrada'[PSCV PAD (última)] >= 90)),
    "SI","NO")

var _GLI = 
IF(OR(
    'Ferrada'[Edad] < 80 &&
    'Ferrada'[PSCV HbA1c (última)] >= 7,
    'Ferrada'[Edad] >= 80 &&
    'Ferrada'[PSCV HbA1c (última)] >= 8),
    "SI","NO")

var _LDL = 
IF(
    'Ferrada'[PSCV LDL] >= 100,
    "SI","NO")

RETURN

IF(
    _PA = "SI" ||
    _GLI = "SI" ||
    _LDL = "SI",
    "SI","NO")
```

### `Ferrada[PSCV PAD (última)]`

Última PAD: misma lógica de tres fuentes; valida rango 10-200 mmHg.

```dax
VAR _FechaFormulario =
    CALCULATE(
        MAX(PSCV[FECHA ATENCION]),
        FILTER(PSCV,
        PSCV[RUN] = Ferrada[RUN] &&
        NOT ISBLANK(PSCV[PAD]))
    )

VAR _Formulario =
    CALCULATE(
        FIRSTNONBLANK(PSCV[PAD],1),
        FILTER(PSCV,
        PSCV[RUN] = Ferrada[RUN] &&
        PSCV[FECHA ATENCION] = _FechaFormulario)
    )

VAR _FechaEF12m =
    CALCULATE(
        MAX('Examen físico general'[FECHA ATENCION]),
        FILTER('Examen físico general',
        'Examen físico general'[RUN] = 'Ferrada'[RUN] &&
        NOT ISBLANK('Examen físico general'[PAD]))
    )

VAR _EF12m =
    CALCULATE(
        FIRSTNONBLANK('Examen físico general'[PAD],1),
        FILTER('Examen físico general',
        'Examen físico general'[RUN] = 'Ferrada'[RUN] &&
        'Examen físico general'[FECHA ATENCION] = _FechaEF12m)
    )

VAR _FechaEstratificacion =
    LOOKUPVALUE(Estratificacion[Fecha última PAS - PAD], Estratificacion[RUN], 'Ferrada'[RUN])

VAR _Estratificacion =
    LOOKUPVALUE(Estratificacion[Presión Arterial Diastólica (PAD)], Estratificacion[RUN], 'Ferrada'[RUN])

-- Encontrar la fecha más reciente
VAR _MaxFecha =
    MAXX(
        {
            _FechaFormulario,
            _FechaEF12m,
            _FechaEstratificacion
        },
        [Value]
    )

-- Devolver el valor asociado a esa fecha
VAR _ResultadoFinal =
    SWITCH(
        TRUE(),
        _MaxFecha = _FechaFormulario, _Formulario,
        _MaxFecha = _FechaEF12m, _EF12m,
        _MaxFecha = _FechaEstratificacion, _Estratificacion,
        BLANK()
    )

RETURN 

IF(
    _ResultadoFinal < 10 || _ResultadoFinal > 200,BLANK(),_ResultadoFinal
)
```

### `Ferrada[PSCV PAS (última)]`

Última PAS: valor con fecha más reciente entre formulario PSCV, examen físico general y Estratificación. Valida rango 60-300 mmHg (fuera → BLANK).

```dax
VAR _FechaFormulario =
    CALCULATE(
        MAX(PSCV[FECHA ATENCION]),
        FILTER(PSCV,
        PSCV[RUN] = Ferrada[RUN] &&
        NOT ISBLANK(PSCV[PAS]))
    )

VAR _Formulario =
    CALCULATE(
        FIRSTNONBLANK(PSCV[PAS], 1),
        FILTER(PSCV,
        PSCV[RUN] = Ferrada[RUN] &&
        PSCV[FECHA ATENCION] = _FechaFormulario)
    )

VAR _FechaEF12m =
    CALCULATE(
        MAX('Examen físico general'[FECHA ATENCION]),
        FILTER('Examen físico general',
        'Examen físico general'[RUN] = 'Ferrada'[RUN] &&
        NOT ISBLANK('Examen físico general'[PAS]))
    )

VAR _EF12m =
    CALCULATE(
        FIRSTNONBLANK('Examen físico general'[PAS], 1),
        FILTER('Examen físico general',
        'Examen físico general'[RUN] = 'Ferrada'[RUN] &&
        'Examen físico general'[FECHA ATENCION] = _FechaEF12m)
    )

VAR _FechaEstratificacion =
    LOOKUPVALUE(Estratificacion[Fecha última PAS - PAD], Estratificacion[RUN], 'Ferrada'[RUN])

VAR _Estratificacion =
    LOOKUPVALUE(Estratificacion[Presión Arterial Sistólica (PAS)], Estratificacion[RUN], 'Ferrada'[RUN])

-- Encontrar la fecha más reciente
VAR _MaxFecha =
    MAXX(
        {
            _FechaFormulario,
            _FechaEF12m,
            _FechaEstratificacion
        },
        [Value]
    )

-- Devolver el valor asociado a esa fecha
VAR _ResultadoFinal =
    SWITCH(
        TRUE(),
        _MaxFecha = _FechaFormulario, _Formulario,
        _MaxFecha = _FechaEF12m, _EF12m,
        _MaxFecha = _FechaEstratificacion, _Estratificacion,
        BLANK()
    )

RETURN 

IF(
    _ResultadoFinal < 60 || _ResultadoFinal > 300,BLANK(),_ResultadoFinal
)
```

### `Ferrada[PSCV PHQ-9 (fecha)]`

Fecha de la última atención con formulario PHQ-9.

```dax
LASTDATE(
    CALCULATETABLE(
        VALUES(Atenciones[FECHA ATENCION]),
        FILTER(
            Atenciones,
            Atenciones[RUN] = Ferrada[RUN] &&
            CONTAINSSTRING(Atenciones[FORMULARIOS CLINICOS],"phq-9"
            )
        )
    )
)
```

### `Ferrada[PSCV PHQ-9?]`

Indicador SI/NO: la columna [PSCV PHQ-9 (fecha)] no está vacía.

```dax
IF(
    NOT ISBLANK(Ferrada[PSCV PHQ-9 (fecha)]),
    "SI","NO"
)
```

### `Ferrada[PSCV Pie DM Riesgo]`

Riesgo de pie diabético según la última evaluación registrada (preguntas 149-150 del formulario PSCV). BLANK si el paciente no es diabético. Nota: si es DM y no hay evaluación válida, asume «Riesgo Bajo» por defecto.

```dax
VAR _FechaForm12m = 
    CALCULATE(
        MAX(PSCV[150.- FECHA REALIZACIÓN].[Date]),
        FILTER(ALL(PSCV), PSCV[RUN] = 'Ferrada'[RUN])
    )

VAR _ResultadoForm12m =
    CALCULATE(
        MAX(PSCV[149.- RIESGO]),
        FILTER(ALL(PSCV), PSCV[RUN] = 'Ferrada'[RUN] && PSCV[150.- FECHA REALIZACIÓN] = _FechaForm12m)
    )

RETURN
    SWITCH(
        TRUE(),
        Ferrada[PSCV DM] = "no",BLANK(),
        _ResultadoForm12m IN {"Riesgo Bajo", "Riesgo Moderado", "Riesgo Alto", "Riesgo Máximo"}, _ResultadoForm12m,
        "Riesgo Bajo"
    )
```

### `Ferrada[PSCV Pie DM ¿Vigente?]`

Vigencia de la evaluación de pie DM: «NO» si no hay fecha o si tiene más de 36 meses al cierre del mes anterior; «SI» en caso contrario.

```dax
var _Fecha = 
IF(
    OR(
        ISBLANK('Ferrada'[PSCV Pie DM Fecha]),
        DATEDIFF(
            'Ferrada'[PSCV Pie DM Fecha].[Date],
            EOMONTH(TODAY(),-1),
            MONTH
        ) > 36
    ),
    "NO",
    "SI"
)

RETURN

_Fecha
```

### `Ferrada[PSCV Podología Vigente]`

Indicador SI/NO derivado: vale «SI» si [PSCV Podología 12m (act)], [PSCV Podología (form)] (basta una).

```dax
IF(
    'Ferrada'[PSCV Podología 12m (act)]="SI" ||
    'Ferrada'[PSCV Podología (form)]="SI",
    "SI","NO")
```

### `Ferrada[PSCV RAC]`

Valor de relación albúmina/creatinina consolidado de tres fuentes (formulario PSCV, laboratorio HEC 2024, laboratorio Holanda; búsqueda: «(RAC)» en lab HEC, «mau/crea» en lab Holanda, pregunta 72 del formulario PSCV): de cada fuente toma el registro más reciente y gana el de fecha más nueva. (Corregido jul-2026: se eliminó el respaldo histórico erróneo que leía HbA1c de Estratificación, y las columnas que elegían el valor más alto en vez del más reciente.) Nota vigente: las descargas masivas de laboratorio (HEC/Holanda) están descontinuadas desde ~2025; en la práctica hoy alimenta solo el formulario PSCV. La lógica por fecha hace que los datos congelados pierdan naturalmente contra registros nuevos.

```dax
VAR _FechaHEC =
    CALCULATE(
        MAX('Laboratorio (resultado) HEC 2024'[Fecha Ingreso]),
        FILTER(
            'Laboratorio (resultado) HEC 2024',
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "(RAC)")
        )
    )

VAR _HEC =
    CALCULATE(
        FIRSTNONBLANK('Laboratorio (resultado) HEC 2024'[Resultado],1),
        FILTER(
            'Laboratorio (resultado) HEC 2024',
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] &&
            'Laboratorio (resultado) HEC 2024'[Fecha Ingreso] = _FechaHEC &&
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "(RAC)")
        )
    )

VAR _FechaHOLANDA =
    CALCULATE(
        MAX('Laboratorio Holanda'[Fecha Ingreso]),
        FILTER(
            'Laboratorio Holanda',
            'Laboratorio Holanda'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "mau/crea")
        )
    )

VAR _HOLANDA =
    CALCULATE(
        FIRSTNONBLANK('Laboratorio Holanda'[Resultado],1),
        FILTER(
            'Laboratorio Holanda',
            'Laboratorio Holanda'[RUN] = 'Ferrada'[RUN] &&
            'Laboratorio Holanda'[Fecha Ingreso] = _FechaHOLANDA &&
            CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "mau/crea")
        )
    )

VAR _FechaPSCV =
    CALCULATE(
        MAX(PSCV[54.- FECHA DE REALIZACIÓN DE BATERÍA DE EXÁMEN *]),
        FILTER('PSCV',
        PSCV[RUN] = 'Ferrada'[RUN] &&
        NOT ISBLANK(PSCV[72.- RAC RELACIÓN ALBUMINA/CREATININA]))
    )

VAR _ValorPSCV =
    CALCULATE(
        FIRSTNONBLANK(PSCV[72.- RAC RELACIÓN ALBUMINA/CREATININA],1),
        FILTER(PSCV,
        PSCV[RUN] = 'Ferrada'[RUN] &&
        PSCV[54.- FECHA DE REALIZACIÓN DE BATERÍA DE EXÁMEN *] = _FechaPSCV)
    )
  

-- Consolidamos fechas y valores
VAR _Tabla =
    {
        (_FechaHEC, _HEC),
        (_FechaHOLANDA, _HOLANDA),
        (_FechaPSCV, _ValorPSCV)
    }

VAR _Ultimo =
    TOPN(
        1,
        FILTER(_Tabla, NOT ISBLANK([Value2])),
        [Value1], DESC
    )

VAR _ResultadoFinal =
    MAXX(_Ultimo, [Value2])

RETURN
    _ResultadoFinal
```

### `Ferrada[PSCV RAC Alta]`

Indicador SI/NO: RAC >30 mg/g (albuminuria moderada o mayor).

```dax
IF('Ferrada'[PSCV RAC]>30,
"SI","NO")
```

### `Ferrada[PSCV RAC Etapa]`

Etapa de albuminuria (KDIGO): A1 (<30), A2 (30-299), A3 (≥300). BLANK sin RAC.

```dax
VAR RAC = 'Ferrada'[PSCV RAC]
RETURN
SWITCH(
    TRUE(),
    RAC > 0 && RAC < 30, "A1",
    RAC >= 30 && RAC < 300, "A2",
    RAC >= 300, "A3",
    BLANK()
)
```

### `Ferrada[PSCV RAC ¿Vigente?]`

Vigencia SI/NO del examen: toma la fecha más reciente entre formulario PSCV, laboratorio HEC y laboratorio Holanda («Cuociente Microalb/Creatinuria(RAC)», «indice mau/crea») y responde «SI» si tiene 12 meses o menos; «NO» si es más antigua o no existe.

```dax
VAR _HECFecha = 
    CALCULATE(
        MAX('Laboratorio (resultado) HEC 2024'[Fecha Ingreso]),
        FILTER(
            ALL('Laboratorio (resultado) HEC 2024'), 
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] && 
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "Cuociente Microalb/Creatinuria(RAC)")
        )
    )

VAR _FormFecha = 
    CALCULATE(
        MAX(PSCV[54.- FECHA DE REALIZACIÓN DE BATERÍA DE EXÁMEN *]),
        FILTER(
            PSCV, 
            PSCV[RUN] = 'Ferrada'[RUN]
        )
    )

var _HOLANDAfecha = 
LASTDATE(CALCULATETABLE(VALUES('Laboratorio Holanda'[Fecha Ingreso].[Date]),
FILTER(ALL('Laboratorio Holanda'),'Laboratorio Holanda'[RUN]='Ferrada'[RUN] &&
CONTAINSSTRING('Laboratorio Holanda'[Determinacion],"indice mau/crea"))))

var _FechaFinal =
MAXX(
    {_FormFecha,
    _HECFecha,
    _HOLANDAfecha},
    [Value])

RETURN

SWITCH(
    TRUE(),
    ISBLANK(_FechaFinal),"NO",
    DATEDIFF(_FechaFinal,TODAY(),MONTH) <= 12,"SI",
    "NO")
```

### `Ferrada[PSCV Receta Vigente?]`

Receta cardiovascular vigente SI/NO: OR de los 15 indicadores de fármacos CV (losartán, hidroclorotiazida, amlodipino, nifedipino, enalapril, carvedilol, atenolol, furosemida, espironolactona, metformina, vildagliptina, empagliflozina, atorvastatina, insulina, aspirina).

```dax
IF('Ferrada'[PSCV Losartán]="SI" || 
'Ferrada'[PSCV Hidroclorotiazida]="SI" || 
'Ferrada'[PSCV Amlodipino]="SI" || 
'Ferrada'[PSCV Nifedipino]="SI" ||
'Ferrada'[PSCV Enalapril]="SI" || 
'Ferrada'[PSCV Carvedilol]="SI" ||
'Ferrada'[PSCV Atenolol]="SI" ||
'Ferrada'[PSCV Furosemida]="SI" ||
'Ferrada'[PSCV Espironolactona]="SI" ||
'Ferrada'[PSCV Metformina]="SI" || 
'Ferrada'[Vildagliptina]="SI" ||
'Ferrada'[PSCV Empagliflozina]="SI" ||
'Ferrada'[PSCV Atorvastatina]="SI" || 
'Ferrada'[PSCV Insulina]="SI" || 
'Ferrada'[PSCV Aspirina]="SI",
"SI","NO")
```

### `Ferrada[PSCV Riesgo CV]`

Riesgo cardiovascular consolidado. Si pertenece al PSCV: «Alto» automático con DM, ECV, ERC, LDL>190 o HTA refractaria (criterios de alto riesgo por condición); si no, usa el riesgo registrado en el último formulario PSCV médico; sin registro, «Bajo» por defecto. BLANK si no pertenece al programa.

```dax
VAR _12mFecha = 
LASTDATE(
    CALCULATETABLE(VALUES(PSCV[FECHA ATENCION]),
    FILTER(ALL(PSCV),PSCV[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING(PSCV[INSTRUMENTO],"médico"))))

VAR _12mRiesgoCV = 
CALCULATETABLE(VALUES(PSCV[142.- RIESGO CARDIOVASCULAR]),
    FILTER(ALL(PSCV),
    PSCV[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING(PSCV[INSTRUMENTO],"médic") &&
    PSCV[FECHA ATENCION]=_12mFecha))


VAR _RiesgoFinal = 
IF(
    ISBLANK(_12mRiesgoCV),BLANK(),_12mRiesgoCV
)

RETURN
IF(
    'Ferrada'[Pertenece a PSCV]="SI",
    SWITCH(
        TRUE(),
        'Ferrada'[PSCV DM] = "SI" || 'Ferrada'[PSCV ECV] = "SI" || 'Ferrada'[PSCV ERC] = "SI" || 'Ferrada'[PSCV LDL] > 190 || 'Ferrada'[PSCV HTA Refractaria?] = "SI", "Alto",
        _RiesgoFinal = "alto", "Alto",
        _RiesgoFinal = "moderado", "Moderado",
        _RiesgoFinal = "bajo", "Bajo",
        "Bajo"
    ),
    BLANK())
```

### `Ferrada[PSCV TBQ Actual]`

Tabaquismo actual: toma el último formulario PSCV donde la pregunta 30 no está vacía y responde «SI» si ese registro dice «sí». A diferencia de otras columnas, sí respeta el registro más reciente.

```dax
VAR _Fecha = 
LASTDATE(
    CALCULATETABLE(VALUES(PSCV[FECHA ATENCION]),
        FILTER(
            PSCV,
            PSCV[RUN] = Ferrada[RUN] &&
            PSCV[30.- TABAQUISMO ACTUAL *]<>""
        )
    )
)

VAR _Resultado =
IF(
    CALCULATE(COUNT(PSCV[RUN]),
        FILTER(
            PSCV,
            PSCV[RUN]='Ferrada'[RUN] &&
            PSCV[FECHA ATENCION] = _Fecha &&
            PSCV[30.- TABAQUISMO ACTUAL *]="si"
        )
    ),"SI","NO"
)

RETURN

_Resultado
```

### `Ferrada[PSCV TBQ historico]`

Tabaquismo histórico SI/NO (ex [PSCV TBQ], renombrada jul-2026 para no confundir con [PSCV TBQ Actual]): la pregunta 30 del formulario PSCV fue «sí» en cualquier registro histórico. Decisión de diseño: responde «¿ha fumado alguna vez según formularios?»; el estado actual lo da [PSCV TBQ Actual].

```dax
IF(
    CALCULATE(COUNT(PSCV[RUN]),
        FILTER(PSCV,
            PSCV[RUN]='Ferrada'[RUN] &&
            PSCV[30.- TABAQUISMO ACTUAL *]="si"
        )
    ),"SI","NO"
)
```

### `Ferrada[PSCV TG]`

Valor de triglicéridos consolidado de tres fuentes (formulario PSCV, laboratorio HEC 2024, laboratorio Holanda; búsqueda: «triglicéri» en labs (corregido jul-2026: Holanda buscaba RAC por error), pregunta correspondiente del formulario): de cada fuente toma el registro más reciente y gana el de fecha más nueva. (Corregido jul-2026: se eliminó el respaldo histórico erróneo que leía HbA1c de Estratificación, y las columnas que elegían el valor más alto en vez del más reciente.) Nota vigente: las descargas masivas de laboratorio (HEC/Holanda) están descontinuadas desde ~2025; en la práctica hoy alimenta solo el formulario PSCV. La lógica por fecha hace que los datos congelados pierdan naturalmente contra registros nuevos.

```dax
VAR _FechaPSCV =
    CALCULATE(
        MAX(PSCV[54.- FECHA DE REALIZACIÓN DE BATERÍA DE EXÁMEN *]),
        FILTER(
            PSCV,
            PSCV[RUN] = 'Ferrada'[RUN] &&
            NOT ISBLANK(PSCV[83.- TRIGLICÉRIDOS (MG/DL)])
        )
    )

VAR _ValorPSCV =
    CALCULATE(
        MAX(PSCV[83.- TRIGLICÉRIDOS (MG/DL)]),
        FILTER(
            PSCV,
            PSCV[RUN] = 'Ferrada'[RUN] &&
            PSCV[54.- FECHA DE REALIZACIÓN DE BATERÍA DE EXÁMEN *] = _FechaPSCV)
    )

VAR _FechaHEC =
    CALCULATE(
        MAX('Laboratorio (resultado) HEC 2024'[Fecha Ingreso]),
        FILTER(
            'Laboratorio (resultado) HEC 2024',
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "triglicéri")
        )
    )

VAR _ValorHEC =
    CALCULATE(
        MAX('Laboratorio (resultado) HEC 2024'[Resultado]),
        FILTER(
            'Laboratorio (resultado) HEC 2024',
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] &&
            'Laboratorio (resultado) HEC 2024'[Fecha Ingreso] = _FechaHEC &&
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "triglicéri")
        )
    )

VAR _FechaHOLANDA =
    CALCULATE(
        MAX('Laboratorio Holanda'[Fecha Ingreso]),
        FILTER(
            'Laboratorio Holanda',
            'Laboratorio Holanda'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "triglicéri")
        )
    )

VAR _ValorHOLANDA =
    CALCULATE(
        MAX('Laboratorio Holanda'[Resultado]),
        FILTER(
            'Laboratorio Holanda',
            'Laboratorio Holanda'[RUN] = 'Ferrada'[RUN] &&
            'Laboratorio Holanda'[Fecha Ingreso] = _FechaHOLANDA &&
            CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "triglicéri")
        )
    )

-- Tabla con fechas y valores para comparar
VAR _Tabla =
    {
        (_FechaPSCV, _ValorPSCV),
        (_FechaHEC, _ValorHEC),
        (_FechaHOLANDA, _ValorHOLANDA)
    }
    
VAR _Ultimo =
    TOPN(1, FILTER(_Tabla, NOT ISBLANK([Value2])), [Value1], DESC)

RETURN
    MAXX(_Ultimo, [Value2])
```

### `Ferrada[PSCV VFG]`

Valor de velocidad de filtración glomerular consolidado de tres fuentes (formulario PSCV, laboratorio HEC 2024, laboratorio Holanda; búsqueda: «filtración» en HEC, «vfg» en Holanda, pregunta 74 (MDRD-4) del formulario): de cada fuente toma el registro más reciente y gana el de fecha más nueva. (Corregido jul-2026: se eliminó el respaldo histórico erróneo que leía HbA1c de Estratificación, y las columnas que elegían el valor más alto en vez del más reciente.) Nota vigente: las descargas masivas de laboratorio (HEC/Holanda) están descontinuadas desde ~2025; en la práctica hoy alimenta solo el formulario PSCV. La lógica por fecha hace que los datos congelados pierdan naturalmente contra registros nuevos.

```dax
VAR _FechaPSCV =
    CALCULATE(
        MAX(PSCV[54.- FECHA DE REALIZACIÓN DE BATERÍA DE EXÁMEN *]),
        FILTER(
            PSCV,
            PSCV[RUN] = 'Ferrada'[RUN] &&
            NOT ISBLANK(PSCV[74.- VFG MDRD-4])
        )
    )

VAR _ValorPSCV =
    CALCULATE(
        MAX(PSCV[74.- VFG MDRD-4]),
        FILTER(
            PSCV,
            PSCV[RUN] = 'Ferrada'[RUN] &&
            PSCV[54.- FECHA DE REALIZACIÓN DE BATERÍA DE EXÁMEN *] = _FechaPSCV)
    )

VAR _FechaHEC =
    CALCULATE(
        MAX('Laboratorio (resultado) HEC 2024'[Fecha Ingreso]),
        FILTER(
            'Laboratorio (resultado) HEC 2024',
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "filtración")
        )
    )

VAR _ValorHEC =
    CALCULATE(
        MAX('Laboratorio (resultado) HEC 2024'[Resultado]),
        FILTER(
            'Laboratorio (resultado) HEC 2024',
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] &&
            'Laboratorio (resultado) HEC 2024'[Fecha Ingreso] = _FechaHEC &&
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "filtración")
        )
    )

VAR _FechaHOLANDA =
    CALCULATE(
        MAX('Laboratorio Holanda'[Fecha Ingreso]),
        FILTER(
            'Laboratorio Holanda',
            'Laboratorio Holanda'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "vfg")
        )
    )

VAR _ValorHOLANDA =
    CALCULATE(
        MAX('Laboratorio Holanda'[Resultado]),
        FILTER(
            'Laboratorio Holanda',
            'Laboratorio Holanda'[RUN] = 'Ferrada'[RUN] &&
            'Laboratorio Holanda'[Fecha Ingreso] = _FechaHOLANDA &&
            CONTAINSSTRING('Laboratorio Holanda'[Determinacion], "vfg")
        )
    )

-- Tabla con fechas y valores para comparar
VAR _Tabla =
    {
        (_FechaPSCV, _ValorPSCV),
        (_FechaHEC, _ValorHEC),
        (_FechaHOLANDA, _ValorHOLANDA)
    }

VAR _Ultimo =
    TOPN(1, FILTER(_Tabla, NOT ISBLANK([Value2])), [Value1], DESC)

RETURN
    MAXX(_Ultimo, [Value2])
```

### `Ferrada[PSCV VFG Etapa]`

Etapa de la función renal (clasificación tipo KDIGO) según VFG y RAC: G5 (<15), G4 (15-29), G3B (30-44), G3A (45-59), G2 (60-89), G1 (≥90 con RAC≥10), G0 (≥90 con RAC<10). BLANK si no hay VFG.

```dax
VAR VFG = 'Ferrada'[PSCV VFG]
VAR RAC = 'Ferrada'[PSCV RAC]
RETURN
SWITCH(
    TRUE(),
    VFG > 0 && VFG < 15, "G5",
    VFG >= 15 && VFG < 30, "G4",
    VFG >= 30 && VFG < 45, "G3B",
    VFG >= 45 && VFG < 60, "G3A",
    VFG >= 60 && VFG < 90, "G2",
    VFG >= 90 && RAC >= 10, "G1",
    VFG >= 90 && RAC < 10,"G0",
    BLANK()
)
```

### `Ferrada[PSCV VFG ¿Vigente?]`

Vigencia SI/NO del examen: toma la fecha más reciente entre formulario PSCV, laboratorio HEC y laboratorio Holanda («filtración», «vfg») y responde «SI» si tiene 12 meses o menos; «NO» si es más antigua o no existe.

```dax
VAR _HECFecha = 
    CALCULATE(
        MAX('Laboratorio (resultado) HEC 2024'[Fecha Ingreso]),
        FILTER(
            ALL('Laboratorio (resultado) HEC 2024'), 
            'Laboratorio (resultado) HEC 2024'[RUN] = 'Ferrada'[RUN] && 
            CONTAINSSTRING('Laboratorio (resultado) HEC 2024'[Nombre del Test], "filtración")
        )
    )

VAR _FormFecha = 
    CALCULATE(
        MAX(PSCV[54.- FECHA DE REALIZACIÓN DE BATERÍA DE EXÁMEN *]),
        FILTER(
            PSCV, 
            PSCV[RUN] = 'Ferrada'[RUN]
        )
    )

var _HOLANDAfecha = 
LASTDATE(CALCULATETABLE(VALUES('Laboratorio Holanda'[Fecha Ingreso].[Date]),
FILTER(ALL('Laboratorio Holanda'),'Laboratorio Holanda'[RUN]='Ferrada'[RUN] &&
CONTAINSSTRING('Laboratorio Holanda'[Determinacion],"vfg"))))

var _FechaFinal = 
MAXX(
    {_FormFecha,
    _HECFecha,
    _HOLANDAfecha},
    [Value])

RETURN

SWITCH(
    TRUE(),
    ISBLANK(_FechaFinal),"NO",
    DATEDIFF(_FechaFinal,TODAY(),MONTH) <= 12,"SI",
    "NO")
```

### `Ferrada[PSCV ¿Candidato Empaglifozina?]`

Candidato a empagliflozina SI/NO: DM y sin empagliflozina, con (60-75 años e IMC≥30) o (VFG 30-59).

```dax
IF(
    ('Ferrada'[PSCV DM]="SI" &&
    'Ferrada'[Edad]>=60 &&
    'Ferrada'[Edad]<=75 &&
    'Ferrada'[IMC]>=30 &&
    'Ferrada'[PSCV Empagliflozina]="NO") ||
    ('Ferrada'[PSCV DM]="SI" &&
    'Ferrada'[PSCV VFG]>=30 &&
    'Ferrada'[PSCV VFG]<60 &&
    'Ferrada'[PSCV Empagliflozina]="NO"),
    "SI","NO")
```

### `Ferrada[PSCV ¿Candidato Estatina?]`

Indicador de candidatura SI/NO: se cumple si [PSCV Riesgo CV], [PSCV Estatina] toman los valores exigidos por la fórmula (condición conjunta).

```dax
IF(
    'Ferrada'[PSCV Riesgo CV]="Alto" &&
    'Ferrada'[PSCV Estatina]="NO",
    "SI","NO")
```

### `Ferrada[PSCV ¿Candidato Insulina?]`

Candidato a insulina SI/NO: DM + HbA1c≥9 + sin insulina actual.

```dax
IF(
    'Ferrada'[PSCV DM]="SI" &&
    'Ferrada'[PSCV HbA1c (última)]>=9 &&
    'Ferrada'[PSCV Insulina]="NO",
    "SI","NO")
```

### `Ferrada[PSCV ¿Candidato Vildagliptina?]`

Candidato a vildagliptina SI/NO: DM + edad ≥65 + VFG<60 + sin vildagliptina actual.

```dax
IF(
    'Ferrada'[PSCV DM]="SI" &&
    'Ferrada'[Edad]>=65 &&
    'Ferrada'[PSCV VFG]<60 &&
    'Ferrada'[Vildagliptina]="NO",
    "SI","NO")
```

### `Ferrada[PSCV ¿Ingresado?]`

Ingreso al PSCV SI/NO: en el último formulario PSCV con instrumento médico, alguna de las siete condiciones está marcada «sí»: HTA (p.20), DM2 (p.22), dislipidemia (p.26), AVE (p.38), IAM (p.36), antecedente CV ateroesclerótico (p.28) o ERC etapa G3b-G5 (p.115). Refleja el estado del último formulario, no el histórico.

```dax
VAR _HTA = 
    IF(
        CALCULATE(
            COUNT(PSCV[RUN]),
            FILTER(
                ALL(PSCV),
                PSCV[RUN] = 'Ferrada'[RUN] &&
                PSCV[FECHA ATENCION] = LASTDATE(CALCULATETABLE(VALUES(PSCV[FECHA ATENCION]),
                FILTER(ALL(PSCV),PSCV[RUN]='Ferrada'[RUN] &&
                CONTAINSSTRING(PSCV[INSTRUMENTO],"médico")))) &&
                CONTAINSSTRING(PSCV[20.- ¿ES HTA?], "si")
            )
        ), 
        "SI", 
        "NO"
    )

VAR _DM = 
    IF(
        CALCULATE(
            COUNT(PSCV[RUN]),
            FILTER(
                ALL(PSCV),
                PSCV[RUN] = 'Ferrada'[RUN] &&
                PSCV[FECHA ATENCION] = LASTDATE(CALCULATETABLE(VALUES(PSCV[FECHA ATENCION]),
                FILTER(ALL(PSCV),PSCV[RUN]='Ferrada'[RUN] &&
                CONTAINSSTRING(PSCV[INSTRUMENTO],"médico")))) &&
                CONTAINSSTRING(PSCV[22.- ¿ES DM2?], "si")
            )
        ) > 0, 
        "SI", 
        "NO"
    )

VAR _DLP = 
    IF(
        CALCULATE(
            COUNT(PSCV[RUN]),
            FILTER(
                ALL(PSCV),
                PSCV[RUN] = 'Ferrada'[RUN] &&
                PSCV[FECHA ATENCION] = LASTDATE(CALCULATETABLE(VALUES(PSCV[FECHA ATENCION]),
                FILTER(ALL(PSCV),PSCV[RUN]='Ferrada'[RUN] &&
                CONTAINSSTRING(PSCV[INSTRUMENTO],"médico")))) &&
                CONTAINSSTRING(PSCV[26.- ¿ES DISLIPIDÉMICO?], "si")
            )
        ) > 0, 
        "SI", 
        "NO"
    )

VAR _ACV = 
    IF(
        CALCULATE(
            COUNT(PSCV[RUN]),
            FILTER(
                ALL(PSCV),
                PSCV[RUN] = 'Ferrada'[RUN] &&
                PSCV[FECHA ATENCION] = LASTDATE(CALCULATETABLE(VALUES(PSCV[FECHA ATENCION]),
                FILTER(ALL(PSCV),PSCV[RUN]='Ferrada'[RUN] &&
                CONTAINSSTRING(PSCV[INSTRUMENTO],"médico")))) &&
                CONTAINSSTRING(PSCV[38.- ¿HA PRESENTADO AVE?], "si")
            )
        ) > 0, 
        "SI", 
        "NO"
    )

VAR _IAM = 
    IF(
        CALCULATE(
            COUNT(PSCV[RUN]),
            FILTER(
                ALL(PSCV),
                PSCV[RUN] = 'Ferrada'[RUN] &&
                PSCV[FECHA ATENCION] = LASTDATE(CALCULATETABLE(VALUES(PSCV[FECHA ATENCION]),
                FILTER(ALL(PSCV),PSCV[RUN]='Ferrada'[RUN] &&
                CONTAINSSTRING(PSCV[INSTRUMENTO],"médico")))) &&
                CONTAINSSTRING(PSCV[36.- ¿HA PRESENTADO IAM?], "si")
            )
        ) > 0, 
        "SI", 
        "NO"
    )

VAR _ECV = 
    IF(
        CALCULATE(
            COUNT(PSCV[RUN]),
            FILTER(
                ALL(PSCV),
                PSCV[RUN] = 'Ferrada'[RUN] &&
                PSCV[FECHA ATENCION] = LASTDATE(CALCULATETABLE(VALUES(PSCV[FECHA ATENCION]),
                FILTER(ALL(PSCV),PSCV[RUN]='Ferrada'[RUN] &&
                CONTAINSSTRING(PSCV[INSTRUMENTO],"médico")))) &&
                CONTAINSSTRING(PSCV[28.- ¿TIENE ANTECEDENTES ENF. CARDIOVASCULAR ATEROSCLER], "si")
            )
        ) > 0, 
        "SI", 
        "NO"
    )

VAR _ERC = 
    IF(
        CALCULATE(
            COUNT(PSCV[RUN]),
            FILTER(
                ALL(PSCV),
                PSCV[RUN] = 'Ferrada'[RUN] &&
                PSCV[FECHA ATENCION] = LASTDATE(CALCULATETABLE(VALUES(PSCV[FECHA ATENCION]),
                FILTER(ALL(PSCV),PSCV[RUN]='Ferrada'[RUN] &&
                CONTAINSSTRING(PSCV[INSTRUMENTO],"médico")))) &&
                (
                    CONTAINSSTRING(PSCV[115.- ETAPA DE ERC], "g3b") ||
                    CONTAINSSTRING(PSCV[115.- ETAPA DE ERC], "g4") ||
                    CONTAINSSTRING(PSCV[115.- ETAPA DE ERC], "g5")
                )
            )
        ) > 0, 
        "SI", 
        "NO"
    )

RETURN
    IF(
        _ACV = "SI" || 
        _IAM = "SI" || 
        _DM = "SI" || 
        _HTA = "SI" || 
        _DLP = "SI" || 
        _ECV = "SI" || 
        _ERC = "SI",
        "SI", 
        "NO"
    )
```

### `Ferrada[PSCV Úlcera Pie DM]`

Úlcera de pie diabético SI/NO: curación de úlcera por enfermería dentro de los últimos 12 meses.

```dax
IF(
    CALCULATE(COUNT(Atenciones[RUN]),
    FILTER(Atenciones,
        Atenciones[RUN] = 'Ferrada'[RUN] &&
        DATEDIFF(Atenciones[FECHA ATENCION],TODAY(),MONTH) > 0 &&
        DATEDIFF(Atenciones[FECHA ATENCION],TODAY(),MONTH) <= 12 &&
        CONTAINSSTRING(Atenciones[INSTRUMENTO],"enferm") &&
        CONTAINSSTRING(Atenciones[ACTIVIDADES],"curaci") &&
        CONTAINSSTRING(Atenciones[ACTIVIDADES],"ulcera"))),
        "SI","NO")
```

### `Ferrada[PSCV Último control]`

Último control cardiovascular formateado como «mes-año (profesional)», donde el profesional se abrevia Med/Enf/Nutri. BLANK si nunca ha tenido control CV.

```dax
var _Fecha = 
LASTDATE(
    CALCULATETABLE(VALUES(Atenciones[FECHA ATENCION]),
    FILTER(ALL(Atenciones),Atenciones[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING(Atenciones[ACTIVIDADES],"control de salud cardiovasc"))))

var _Instrumento = 
TOPN(1,
CALCULATETABLE(VALUES('Atenciones'[INSTRUMENTO]),
FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
Atenciones[FECHA ATENCION]=_Fecha &&
CONTAINSSTRING('Atenciones'[ACTIVIDADES],"control de salud cardio"))),
Atenciones[INSTRUMENTO],DESC)

var _InstrumentoFinal = 
SWITCH(
    TRUE(),
    CONTAINSSTRING(_Instrumento,"médic"),"Med",
    CONTAINSSTRING(_Instrumento,"enferm"),"Enf",
    CONTAINSSTRING(_Instrumento,"nutricio"),"Nutri",
    BLANK())

RETURN
IF(
    ISBLANK(_Fecha),BLANK(),
    FORMAT(_Fecha,"MMMM-YY") & " (" & _InstrumentoFinal & ")"
)
```

### `Ferrada[Pertenece a ECICEP]`

Pertenencia a ECICEP: figura en el histórico (drive), o tiene ingreso, control, seguimiento a distancia o gestión de egreso ECICEP.

```dax
IF(
     IF(LOOKUPVALUE('ECICEP Histórico'[RUN],'ECICEP Histórico'[RUN],'Ferrada'[RUN]) <> "",
    "SI","NO")="SI" || 
    'Ferrada'[ECICEP Ingreso]="SI" ||
    'Ferrada'[ECICEP Control (act)]="SI" ||
    'Ferrada'[ECICEP Seguimiento a distancia (act)]="SI" ||
    'Ferrada'[ECICEP Gestión de Egreso (act)]="SI",
    "SI","NO")
```

### `Ferrada[Pertenece a PSCV]`

Pertenencia al PSCV: «SI» si cualquiera de [PSCV HTA], [PSCV DM], [PSCV DLP], [PSCV ECV] o [PSCV ERC] es «SI».

```dax
IF(
'Ferrada'[PSCV HTA]="SI" || 
'Ferrada'[PSCV DM]="SI" || 
'Ferrada'[PSCV DLP]="SI" || 
'Ferrada'[PSCV ECV]="SI" ||
'Ferrada'[PSCV ERC]="SI",
"SI","NO")
```

### `Ferrada[Previsión]`

Previsión: «Fonasa» si el RUN aparece en «PVI actualizada» (población validada FONASA) o si la institución previsional de Inscritos contiene «Fonasa»; cualquier otro caso queda «Isapre». Nota: sin información también cae en «Isapre» por defecto.

```dax
var _PVI = 
IF(LOOKUPVALUE('PVI actualizada'[RUN],'PVI actualizada'[RUN],'Ferrada'[RUN]) <> "","Fonasa",BLANK())

var _Inscripcion = 
LOOKUPVALUE(Inscritos[INSTITUCION PREVISIONAL],Inscritos[RUN],'Ferrada'[RUN])

RETURN

SWITCH(
    TRUE(),
    _PVI="Fonasa","Fonasa",
    CONTAINSSTRING(_Inscripcion,"Fonasa"),"Fonasa",
    "Isapre")
```

### `Ferrada[Pueblo Originario]`

Trae por cruce de RUN el valor de «PUEBLO INDIG» desde la tabla «Inscritos» hacia esta tabla (LOOKUPVALUE). Copia directa, sin transformación.

```dax
LOOKUPVALUE(Inscritos[PUEBLO INDIG],Inscritos[RUN],'Ferrada'[RUN])
```

### `Ferrada[RUN]`

_Campo base (no calculado): proviene de la carga de Power Query._

### `Ferrada[Sector]`

Sector de inscripción desde «Inscritos»; BLANK si vacío.

```dax
IF(
LOOKUPVALUE(Inscritos[SECTOR],Inscritos[RUN],'Ferrada'[RUN])="",BLANK(),
LOOKUPVALUE(Inscritos[SECTOR],Inscritos[RUN],'Ferrada'[RUN]))
```

### `Ferrada[Sexo]`

Sexo registral desde «Inscritos»; si está vacío devuelve «No informado».

```dax
IF(
LOOKUPVALUE(Inscritos[SEXO],Inscritos[RUN],'Ferrada'[RUN])="",
"No informado",
LOOKUPVALUE(Inscritos[SEXO],Inscritos[RUN],'Ferrada'[RUN]))
```

### `Ferrada[Situación]`

Trae por cruce de RUN el valor de «SITUACION» desde la tabla «Inscritos» hacia esta tabla (LOOKUPVALUE). Copia directa, sin transformación.

```dax
LOOKUPVALUE(Inscritos[SITUACION],Inscritos[RUN],'Ferrada'[RUN])
```

### `Ferrada[Tipo de identificación]`

_Campo base (no calculado): proviene de la carga de Power Query._

### `Ferrada[Trans]`

Marcador de identidad trans: 1 si el sexo registral y el género informado no coinciden (hombre/masculino, mujer/femenina); 0 si coinciden; BLANK si falta información.

```dax
VAR _Sexo = LOOKUPVALUE(Inscritos[SEXO], Inscritos[RUN], 'Ferrada'[RUN])
VAR _Genero = LOOKUPVALUE(Inscritos[GENERO], Inscritos[RUN], 'Ferrada'[RUN])
VAR _SexoInformado = NOT(ISBLANK(_Sexo) || _Sexo = "" || _Sexo IN {"Desconocido", "No informado"})
VAR _GeneroInformado = NOT(_Genero IN {"", "Sin registro", "No revelado"})
RETURN
IF(
    _SexoInformado && _GeneroInformado,
    IF(
        (_Sexo = "Hombre" && _Genero = "Masculino") || (_Sexo = "Mujer" && _Genero = "Femenina"),
        0, 1
    ),
    BLANK()
)
```

### `Ferrada[Vildagliptina]`

Indicador SI/NO: existe receta vigente cuya descripción contiene «vildaglipti».

```dax
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN]),
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"vildaglipti")),
    "SI","NO")
```

### `Ferrada[¿Atendido en 12m?]`

Indicador SI/NO: tuvo al menos una atención dentro de los 12 meses cerrados.

```dax
VAR _FechaInicio = 
EOMONTH(TODAY(),-13) + 1

VAR _FechaFinal =
EOMONTH(TODAY(),-1)

RETURN

IF(
    CALCULATE(COUNT(Atenciones[RUN]),
        FILTER(
            Atenciones,
            Atenciones[RUN]='Ferrada'[RUN] &&
            Atenciones[FECHA ATENCION] >= _FechaInicio &&
            Atenciones[FECHA ATENCION] <= _FechaFinal
        )
    ),"SI","NO"
)
```

### `Ferrada[¿Originario o Migrante?]`

Clasificación intercultural: «Migrante» si la nacionalidad no es chilena (ni vacía ni desconocida); «Originario» si es chilena y declara pueblo originario válido; «NO» en otro caso.

```dax
SWITCH(
    TRUE(),
    'Ferrada'[Nacionalidad] <> "Chilena" && 'Ferrada'[Nacionalidad] <> "" && Ferrada[Nacionalidad] <> "desconocido", 
    "Migrante",
    (
        'Ferrada'[Nacionalidad] = "Chilena" && 
        'Ferrada'[Pueblo Originario] <> "Ninguno" && 
        'Ferrada'[Pueblo Originario] <> "No Contesta" && 
        'Ferrada'[Pueblo Originario] <> "No Sabe" && 
        'Ferrada'[Pueblo Originario] <> ""
    ), 
        "Originario",
        "NO"
    )
```
