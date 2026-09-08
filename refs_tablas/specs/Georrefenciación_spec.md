# Especificación de la página «Georrefenciación»

Extraído automáticamente de la capa de reporte (PBIR) y del modelo semántico (TMDL).

**56 visuales · 80 campos distintos del modelo.**

_Sin filtros a nivel de página._

## Visuales

### 1. CNS — `slicer`

- **Values:** `Ferrada[Citar a CNS]`

### 2. Parkinson — `slicer`

- **Values:** `Ferrada[OTROS Parkinson]` — «Parkinson»

### 3. ¿Respi? — `slicer`

- **Values:** `Ferrada[SALA Ingresado]` — «SALA Ingresado?»

### 4. ¿Activo 1m? — `slicer`

- **Values:** `Ferrada[¿Atendido 1 mes?]`

### 5. Total de personas — `card`

- **Values:** DISTINCTCOUNT(`Ferrada[RUN]`) — «Nº de personas»

### 6. ECV — `slicer`

- **Values:** `Ferrada[PSCV ECV]` — «ECV»

### 7. Situación — `slicer`

- **Values:** `Ferrada[Situación]`

### 8. Años — `slicer`

- **Values:** `Ferrada[Edad]` — «Edad Años»

### 9. CLAP — `slicer`

- **Values:** `Ferrada[Citar a CLAP]`

### 10. ASMA — `slicer`

- **Values:** `Ferrada[SALA ASMA]` — «ASMA»

### 11. Días — `slicer`

- **Values:** `Ferrada[Días]`

### 12. Hipotiroidismo — `slicer`

- **Values:** `Ferrada[OTROS Hipotiroidismo]` — «Hipotiroidismo»

### 13. Sector — `slicer`

- **Values:** `Ferrada[Sector]`

### 14. Gest. ECICEP — `slicer`

- **Values:** `Ferrada[ECICEP Gestión de Ingreso (act)]` — «ECICEP Gestión de Ingreso G3? (12m)»

### 15. Formulario — `slicer`

- **Values:** `Ferrada[ECICEP Formulario llenado]` — «ECICEP Formulario?»

### 16. Grupo Objetivo — `slicer`

- **Values:** `Ferrada[GObj FLu 26]`

### 17. Estratificacion — `slicer`

- **Values:** `Ferrada[Estratificación]`

### 18. EMPAM — `slicer`

- **Values:** `Ferrada[Citar a EMPAM]`

### 19. Artrosis — `slicer`

- **Values:** `Ferrada[OTROS Artrosis C/R]` — «Artrosis C/R»

### 20. DLP — `slicer`

- **Values:** `Ferrada[PSCV DLP]` — «DLP»

### 21. EMPA — `slicer`

- **Values:** `Ferrada[Citar a EMPA]`

### 22. Estado — `slicer`

- **Values:** `Ferrada[Estado]`

### 23. Protecc NNA — `slicer`

- **Values:** `Ferrada[PROTECCION NIÑEZ]`

### 24. Sexo — `slicer`

- **Values:** `Ferrada[Sexo]`

### 25. HTA — `slicer`

- **Values:** `Ferrada[PSCV HTA]` — «HTA»

### 26. Meses — `slicer`

- **Values:** `Ferrada[Meses]` — «Edad Meses»

### 27. SBOR — `slicer`

- **Values:** `Ferrada[SALA SBOR]` — «SBOR»

### 28. Seguimiento — `slicer`

- **Values:** `Ferrada[ECICEP Seguimiento a distancia (act)]` — «ECICEP Seguimiento G3? (12m)»

### 29. Embarazada — `slicer`

- **Values:** `Ferrada[¿Embarazada?]`

### 30. Validado — `slicer`

- **Values:** `Ferrada[Validado]`

### 31. Mapa de Georreferenciación — `esriVisual`

- **Color:** `Ferrada[Sector]`
- **Location:** `Ferrada[Dirección Completa]`
- **Tooltips:** `Ferrada[RUN]`
- **Tooltips:** `Ferrada[Nombre completo]`
- **Tooltips:** `Ferrada[Edad]` — «Edad1»
- **Tooltips:** `Ferrada[Sexo]`

### 32. ¿PSM? — `slicer`

- **Values:** `Ferrada[SM Ingresado]`

### 33. ¿PSCV? — `slicer`

- **Values:** `Ferrada[PSCV ¿Ingresado?]` — «¿Ingresado PSCV?»

### 34. Compensado — `slicer`

- **Values:** `Ferrada[PSCV HTA ¿compensada?]` — «Compensado»

### 35. DCNO Ind. — `slicer`

- **Values:** `Ferrada[DCNO Indicacion]`

### 36. ASMA G — `slicer`

- **Values:** `Ferrada[SALA ASMA Gravedad]` — «ASMA Gravedad»

### 37. Epilepsia — `slicer`

- **Values:** `Ferrada[OTROS Epilepsia]` — «Epilepsia»

### 38. EPOC T — `slicer`

- **Values:** `Ferrada[SALA EPOC Tipo]` — «EPOC T Otros»

### 39. DCNO Diag — `slicer`

- **Values:** `Ferrada[DCNO Diag]`

### 40. SBOR G — `slicer`

- **Values:** `Ferrada[SALA SBOR Gravedad]` — «SBOR Gravedad»

### 41. (sin título) — `slicer`

- **Values:** `Ferrada[Pertenece a SALA]`

### 42. ¿Plan? — `slicer`

- **Values:** `Ferrada[ECICEP Plan Consensuado]` — «ECICEP Plan Consensuado? (12m)»

### 43. ¿Otros Cr? — `slicer`

- **Values:** `Ferrada[Pertenece a Otros]`

### 44. DM — `slicer`

- **Values:** `Ferrada[PSCV DM]` — «DM»

### 45. Compensado — `slicer`

- **Values:** `Ferrada[PSCV LDL >160]` — «LDL >100»

### 46. ¿Activo 12m? — `slicer`

- **Values:** `Ferrada[¿Atendido en 12m?]` — «Atendido en 12m?»

### 47. ¿PAD? — `slicer`

- **Values:** `Ferrada[Pertenece a PAD]` — «Pertenece PAD?»

### 48. ¿Programa? — `slicer`

- **Values:** `Ferrada[¿Pertenece algún programa?]`

### 49. Runificado Georreferenciado — `tableEx`

- **Values:** `Ferrada[Tipo de identificación]`
- **Values:** `Ferrada[RUN]`
- **Values:** `Ferrada[Nombre Social]`
- **Values:** `Ferrada[Nombre completo]`
- **Values:** `Ferrada[Sexo]`
- **Values:** `Ferrada[Fecha Nacimiento]`
- **Values:** `Ferrada[Edad]` — «Años»
- **Values:** `Ferrada[Meses]` — «Meses1»
- **Values:** `Ferrada[Días]` — «Días1»
- **Values:** `Ferrada[Sector]`
- **Values:** `Ferrada[¿Originario o Migrante?]`
- **Values:** `Ferrada[Nacionalidad]`
- **Values:** `Ferrada[Pueblo Originario]` — «Pueblo Originario1»
- **Values:** `Ferrada[Dirección Completa]`
- **Values:** `Ferrada[Celular]` — «Celular1»
- **Values:** `Ferrada[Mail]`
- **Values:** `Ferrada[Situación]`
- **Values:** `Ferrada[Estado]`
- **Values:** `Inscritos[FECHA DE INSCRIPCION]` — «Fecha inscripción»
- **Values:** `Ferrada[Motivo Pasivación]`
- **Values:** `Ferrada[Fecha Pasivación]`
- **Values:** `Ferrada[Previsión]`
- **Values:** `Ferrada[Validado]`
- **Values:** `Ferrada[Citar a Preventivo]`
- **Values:** `Ferrada[Pertenece a PAD]` — «¿PAD?»
- **Values:** `Ferrada[Cuenta VDI seguimiento 12m (act)]`
- **Values:** `Ferrada[Cuenta VDP 12m (act)]`
- **Values:** `Ferrada[Pertenece a ECICEP]` — «¿ECICEP?»
- **Values:** `Ferrada[PSCV ¿Ingresado?]` — «¿PSCV?»
- **Values:** `Ferrada[PSCV Riesgo CV]` — «Riesgo CV»
- **Values:** `Ferrada[PSCV 1º Control]`
- **Values:** `Ferrada[PSCV 2º Control]`
- **Values:** `Ferrada[PSCV 3º Control]`
- **Values:** `Ferrada[PSCV 4º Control]`
- **Values:** `Ferrada[SALA Ingresado]` — «¿Respiratorio?»
- **Values:** `Ferrada[Pertenece a Otros]` — «¿Otros crónicos?»
- **Values:** `Ferrada[OTROS Artrosis C/R]` — «Artrosis»
- **Values:** `Ferrada[OTROS Hipotiroidismo]` — «Hipotiroidismo»
- **Values:** `Ferrada[OTROS Epilepsia]` — «Epilepsia»
- **Values:** `Ferrada[OTROS Parkinson]` — «Parkinson»
- **Values:** `Ferrada[OTROS Glaucoma]` — «Glaucoma»
- **Values:** `Ferrada[¿Embarazada?]`
- **Values:** `Ferrada[¿Atendido en 12m?]`
- **Values:** `Ferrada[Cuenta At 12m]`
- **Values:** `Ferrada[Última Atención (fecha)]`
- **Values:** `?[Año]` — «ECICEP Ingreso Fecha Año»
- **Values:** `Ferrada[Estratificación]`
- **Values:** SUM(`Ferrada[Trans]`) — «Suma de Trans»

### 50. Migr o Origin — `slicer`

- **Values:** `Ferrada[¿Originario o Migrante?]`

### 51. PAP — `slicer`

- **Values:** `Ferrada[Citar a PAP]`

### 52. ¿ECICEP? — `slicer`

- **Values:** `Ferrada[ECICEP Ingreso]`

### 53. EPOC — `slicer`

- **Values:** `Ferrada[SALA EPOC]` — «EPOC»

### 54. Compensado — `slicer`

- **Values:** `Ferrada[PSCV DM ¿compensada?]` — «HbA1c Alta?»

### 55. Flu 2026 — `slicer`

- **Values:** `Ferrada[Influenza 2026]`

### 56. ¿Cuidador? — `slicer`

- **Values:** `Ferrada[PAD Es cuidador?]`

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

### `Ferrada[Citar a CLAP]`

Estado CLAP (10-19 años): «Rescatar» si no tiene CLAP en los últimos 365 días; «Vigente» si lo tiene. BLANK fuera del rango etario.

```dax
VAR _CLAPFecha = 
CALCULATE(
    MAX(
        Atenciones[FECHA ATENCION].[Date]),
        FILTER(Atenciones,
        Atenciones[RUN]='Ferrada'[RUN] &&
        CONTAINSSTRING(Atenciones[FORMULARIOS CLINICOS],"clap modifica")))

RETURN
SWITCH(
    TRUE(),
    'Ferrada'[Edad] < 10 || 'Ferrada'[Edad] >= 20,BLANK(),
    ISBLANK(_CLAPFecha) || 
    DATEDIFF(_CLAPFecha,EOMONTH(TODAY(),-1),DAY) > 365,"Rescatar",
    DATEDIFF(_CLAPFecha,EOMONTH(TODAY(),-1),DAY) <= 365,"Vigente",
    BLANK()
)
```

### `Ferrada[Citar a CNS]`

Estado control de niño sano (<10 años): «Rescatar» según intervalos por edad sin control sano (<1 año: ≥3 meses; 1-2: ≥6m; 3-4: ≥13m; 5-9: ≥18m); «Vigente» si está al día; «No corresponde» en ≥10 años.

```dax
VAR _CNSControl = 
LASTDATE(
    CALCULATETABLE(
        VALUES(Atenciones[FECHA ATENCION]),
        FILTER(
            Atenciones,
            Atenciones[RUN] = Ferrada[RUN] &&
            CONTAINSSTRING(Atenciones[FORMULARIOS CLINICOS],"control sano")
        )
    )
)

VAR _Fecha = 
EOMONTH(TODAY(),-1)

VAR _CNS =
IF(
AND('Ferrada'[Fecha Nacimiento]>0 && 'Ferrada'[Edad]<1,
DATEDIFF(_CNSControl,_Fecha,MONTH)>=3) ||
AND('Ferrada'[Edad]>=1 && 'Ferrada'[Edad]<3,
DATEDIFF(_CNSControl,_Fecha,MONTH)>=6) ||
AND('Ferrada'[Edad]>=3 && 'Ferrada'[Edad]<5,
DATEDIFF(_CNSControl,_Fecha,MONTH)>=13) ||
AND('Ferrada'[Edad]>=5 && 'Ferrada'[Edad]<10,
DATEDIFF(_CNSControl,_Fecha,MONTH)>=18),
"SI","NO")

RETURN
SWITCH(
    TRUE(),
    'Ferrada'[Edad] >= 10,"No corresponde",
    _CNS="SI","Rescatar",
    _CNS="NO","Vigente",
    BLANK())
```

### `Ferrada[Citar a EMPA]`

Estado EMPA (20-64 años, no embarazada): «Rescatar» si el último EMP es anterior a la ventana de 12 meses cerrados; «Vigente» si está dentro. BLANK si no corresponde.

```dax
VAR FechaReferencia = EOMONTH(TODAY(), -1)
VAR FechaInicioVigencia = EOMONTH(FechaReferencia,-12) + 1 

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
    'Ferrada'[¿Embarazada?] = "si" || 'Ferrada'[Edad] < 20 || 'Ferrada'[Edad] >= 65, BLANK(),
    ISBLANK(FechaEMPA) || FechaEMPA < FechaInicioVigencia, "Rescatar",
    FechaEMPA >= FechaInicioVigencia, "Vigente",
    BLANK()
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

### `Ferrada[Citar a Preventivo]`

Resumen de preventivos pendientes: concatena con « | » los programas en estado «Rescatar» entre CNS, CLAP, EMPA, EMPAM y PAP. BLANK si no debe nada.

```dax
VAR Preventivos =
    UNION(
        SELECTCOLUMNS(
            {"CNS"}, "Nombre", "CNS", "Estado", 'Ferrada'[Citar a CNS]
        ),
        SELECTCOLUMNS(
            {"CLAP"}, "Nombre", "CLAP", "Estado", 'Ferrada'[Citar a CLAP]
        ),
        SELECTCOLUMNS(
            {"EMPA"}, "Nombre", "EMPA", "Estado", 'Ferrada'[Citar a EMPA]
        ),
        SELECTCOLUMNS(
            {"EMPAM"}, "Nombre", "EMPAM", "Estado", 'Ferrada'[Citar a EMPAM]
        ),
        SELECTCOLUMNS(
            {"PAP"}, "Nombre", "PAP", "Estado", 'Ferrada'[Citar a PAP]
        )
    )

VAR Filtrados =
    FILTER(Preventivos, [Estado] = "rescatar")

VAR TextoFinal =
    CONCATENATEX(Filtrados, [Nombre], " | ")

RETURN
    IF(TextoFinal = "", BLANK(), TextoFinal)
```

### `Ferrada[Cuenta At 12m]`

Número de atenciones dentro de la ventana de 12 meses cerrados. Devuelve 0 si no hay. (Corregido jul-2026: el filtro ahora usa ≥ e incluye el primer día de la ventana.)

```dax
VAR _UltimoDiaMesAnterior = EOMONTH(TODAY(), -1)
VAR _FechaInicio = EOMONTH(_UltimoDiaMesAnterior, -13) + 1

var _Resultado =
CALCULATE(
    COUNT('Atenciones'[RUN]),
    FILTER(
        ALL('Atenciones'),
        'Atenciones'[RUN] = 'Ferrada'[RUN] &&
        'Atenciones'[FECHA ATENCION] >= _FechaInicio &&
        'Atenciones'[FECHA ATENCION] <= _UltimoDiaMesAnterior
    )
)

RETURN
IF(
    ISBLANK(_Resultado),0,_Resultado)
```

### `Ferrada[Cuenta VDI seguimiento 12m (act)]`

Total de visitas domiciliarias integrales de seguimiento («tercera») de cualquier profesional en los 12 meses cerrados.

```dax
VAR _UltimoDiaMesAnterior = EOMONTH(TODAY(), -1)
VAR _FechaInicio = EOMONTH(TODAY(), -13) + 1

VAR _Resultado =
CALCULATE(
    COUNT('Atenciones'[RUN]),
    FILTER(
        ALL('Atenciones'),
        'Atenciones'[RUN] = 'Ferrada'[RUN] &&
        'Atenciones'[FECHA ATENCION] >= _FechaInicio &&
        'Atenciones'[FECHA ATENCION] <= _UltimoDiaMesAnterior &&
        (CONTAINSSTRING('Atenciones'[ACTIVIDADES],"visita domicilia") && 
        CONTAINSSTRING('Atenciones'[ACTIVIDADES],"tercera"))
    )
)

RETURN

IF(
    ISBLANK(_Resultado),0,_Resultado)
```

### `Ferrada[Cuenta VDP 12m (act)]`

Cuenta de visitas domiciliarias de tratamiento o procedimiento (VDP) en los 12 meses cerrados.

```dax
VAR _UltimoDiaMesAnterior = EOMONTH(TODAY(), -1)
VAR _FechaInicio = EOMONTH(TODAY(), -13) + 1

VAR _Resultado =
CALCULATE(
    COUNT('Atenciones'[RUN]),
    FILTER(
        ALL('Atenciones'),
        'Atenciones'[RUN] = 'Ferrada'[RUN] &&
        'Atenciones'[FECHA ATENCION] >= _FechaInicio &&
        'Atenciones'[FECHA ATENCION] <= _UltimoDiaMesAnterior &&
        (CONTAINSSTRING('Atenciones'[ACTIVIDADES],"tratamiento o procedimi") ||
        CONTAINSSTRING(Atenciones[ACTIVIDADES],"trat. o proc. en domi"))
    )
)

RETURN

IF(
    ISBLANK(_Resultado),0,_Resultado)
```

### `Ferrada[DCNO Diag]`

Dolor crónico no oncológico (diagnóstico) SI/NO: R52.2 en atenciones o en órdenes internas.

```dax
VAR _run = 'Ferrada'[RUN]
VAR _tieneAtencion =
    CALCULATE(
        COUNTROWS('Atenciones'),
        'Atenciones'[RUN] = _run,
        CONTAINSSTRING(UPPER('Atenciones'[DIAGNOSTICOS]),"R52.2")
    ) > 0
VAR _tieneOrden =
    CALCULATE(
        COUNTROWS('Orden Interna'),
        'Orden Interna'[RUN] = _run,
        CONTAINSSTRING(UPPER('Orden Interna'[Diagnostico]),"R52.2")
    ) > 0
RETURN
IF(_tieneAtencion || _tieneOrden, "SI", "NO")
```

### `Ferrada[DCNO Indicacion]`

Indicación de manejo DCNO SI/NO: orden interna de los últimos 12 meses con motivo relacionado (DCNO, dolor crónico, neuropático), o receta vigente no-morbilidad de analgésicos del programa (tramadol, pregabalina, duloxetina, buprenorfina, celecoxib, metamizol, lidocaína, diclofenaco). La fórmula deja comentada la vía de recetas externas por exceso de falsos positivos.

```dax
VAR _run = 'Ferrada'[RUN]
VAR _hoy = TODAY()
VAR _hace12m = _hoy - 365

VAR _ordenMotivo =
    CALCULATE(
        COUNTROWS('Orden Interna'),
        'Orden Interna'[RUN] = _run,
        'Orden Interna'[Fecha Atencion] >= _hace12m,
        CONTAINSSTRING(UPPER('Orden Interna'[Motivo]), "DCNO") ||
        CONTAINSSTRING(UPPER('Orden Interna'[Motivo]), "DOLOR CRONICO") ||
        CONTAINSSTRING(UPPER('Orden Interna'[Motivo]), "DOLOR CRÓNICO") ||
        CONTAINSSTRING(UPPER('Orden Interna'[Motivo]), "INGRESO DOLOR") ||
        CONTAINSSTRING(UPPER('Orden Interna'[Motivo]), "NEUROPATICO") ||
        CONTAINSSTRING(UPPER('Orden Interna'[Motivo]), "NEUROPÁTICO")
    ) > 0

VAR _recetaVigente =
    CALCULATE(
        COUNTROWS('Recetas Vigentes'),
        'Recetas Vigentes'[RUN] = _run,
        'Recetas Vigentes'[FECHA GENERACION] >= _hace12m,
        'Recetas Vigentes'[TIPO RECETA] <> "Morbilidad",
        CONTAINSSTRING(UPPER('Recetas Vigentes'[DESCRIPCION ARTICULO]), "TRAMADOL") ||
        CONTAINSSTRING(UPPER('Recetas Vigentes'[DESCRIPCION ARTICULO]), "PREGABALINA") ||
        CONTAINSSTRING(UPPER('Recetas Vigentes'[DESCRIPCION ARTICULO]), "DULOXETINA") ||
        CONTAINSSTRING(UPPER('Recetas Vigentes'[DESCRIPCION ARTICULO]), "BUPRENORFINA") ||
        CONTAINSSTRING(UPPER('Recetas Vigentes'[DESCRIPCION ARTICULO]), "CELECOXIB") ||
        CONTAINSSTRING(UPPER('Recetas Vigentes'[DESCRIPCION ARTICULO]), "METAMIZOL") ||
        CONTAINSSTRING(UPPER('Recetas Vigentes'[DESCRIPCION ARTICULO]), "LIDOCAINA") ||
        CONTAINSSTRING(UPPER('Recetas Vigentes'[DESCRIPCION ARTICULO]), "DICLOFENACO") ||
        CONTAINSSTRING(UPPER('Recetas Vigentes'[DESCRIPCION ARTICULO]), "LIDOCAÍNA") 
    ) > 0

/* eliminado: da demasiados falsos positivos. no es realista en la estimacion. 
VAR _recetaExterna =
    CALCULATE(
      COUNTROWS('Recetas externas en curso'),
        'Recetas externas en curso'[RUN] = _run,
        CONTAINSSTRING(UPPER('Recetas externas en curso'[Medicamento]), "TRAMADOL") ||
        CONTAINSSTRING(UPPER('Recetas externas en curso'[Medicamento]), "PREGABALINA") ||
        CONTAINSSTRING(UPPER('Recetas externas en curso'[Medicamento]), "DULOXETINA") ||
        CONTAINSSTRING(UPPER('Recetas externas en curso'[Medicamento]), "BUPRENORFINA") ||
        CONTAINSSTRING(UPPER('Recetas externas en curso'[Medicamento]), "CELECOXIB") ||
        CONTAINSSTRING(UPPER('Recetas externas en curso'[Medicamento]), "METAMIZOL") ||
        CONTAINSSTRING(UPPER('Recetas externas en curso'[Medicamento]), "LIDOCAINA") ||
        CONTAINSSTRING(UPPER('Recetas externas en curso'[Medicamento]), "LIDOCAÍNA") 
    ) > 0 */
RETURN
IF(_ordenMotivo || _recetaVigente, "SI", "NO")
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

### `Ferrada[Días]`

Componente «días» de la edad (para lactantes). Con respaldo en EDAD DIAS de «Inscritos».

```dax
VAR Hoy = TODAY()
VAR Nacimiento = [Fecha Nacimiento].[Date]
VAR DiaActual = DAY(Hoy)
VAR MesActual = MONTH(Hoy)
VAR AnioActual = YEAR(Hoy)
VAR DiaNacimiento = DAY(Nacimiento)
VAR MesNacimiento = MONTH(Nacimiento)
VAR AnioNacimiento = YEAR(Nacimiento)
VAR DiasDelMesActual = 
    IF(
        ISBLANK(Nacimiento),
        BLANK(),
        IF(
            MesActual = MesNacimiento && AnioActual = AnioNacimiento,
            DiaActual - DiaNacimiento,
            IF(
                DiaActual >= DiaNacimiento,
                DiaActual - DiaNacimiento,
                DiaActual + (DAY(EOMONTH(Hoy, -1)) - DiaNacimiento)
            )
        )
    )
RETURN

IF(ISBLANK(DiasDelMesActual),
LOOKUPVALUE(Inscritos[EDAD DIAS],Inscritos[RUN],'Ferrada'[RUN]),
DiasDelMesActual)
```

### `Ferrada[ECICEP Formulario llenado]`

Indicador SI/NO: existe alguna atención cuya actividad contiene «plan de interven».

```dax
IF(
    CALCULATE(COUNT('Atenciones'[RUN]),
        FILTER(
            'Atenciones',
            'Atenciones'[RUN]='Ferrada'[RUN] &&
            CONTAINSSTRING('Atenciones'[FORMULARIOS CLINICOS],"plan de interven")
        )
    ),"SI","NO"
)
```

### `Ferrada[ECICEP Gestión de Ingreso (act)]`

Indicador SI/NO: existe alguna atención cuya actividad contiene «Gestión de casos - Ingreso».

```dax
IF(
    CALCULATE(count('Atenciones'[RUN]),
        FILTER(
            'Atenciones',
            'Atenciones'[RUN]='Ferrada'[RUN] &&
            CONTAINSSTRING('Atenciones'[ACTIVIDADES],"Gestión de casos - Ingreso")
        )
    ),"SI","NO"
)
```

### `Ferrada[ECICEP Ingreso]`

Indicador SI/NO: la columna [ECICEP Ingreso Fecha] no está vacía.

```dax
IF(
    NOT ISBLANK(Ferrada[ECICEP Ingreso Fecha]),
    "SI","NO"
)
```

### `Ferrada[ECICEP Plan Consensuado]`

Plan consensuado ECICEP SI/NO: actividad «plan de cuidado elaborado», formulario de plan de intervención, o figura en la planilla de revisión ECICEP.

```dax
var _Actividad = 
IF(
    CALCULATE(COUNT('Atenciones'[RUN]),
        FILTER(
            'Atenciones',
            'Atenciones'[RUN]='Ferrada'[RUN] &&
            CONTAINSSTRING('Atenciones'[ACTIVIDADES],"plan de cuidado elabora")
        )
    ),"SI","NO"
)

var _Formulario = 
IF(
    CALCULATE(COUNT('Atenciones'[RUN]),
        FILTER(
            'Atenciones',
            'Atenciones'[RUN]='Ferrada'[RUN] &&
            CONTAINSSTRING('Atenciones'[FORMULARIOS CLINICOS],"formulario de plan de interven")
        )
    ),"SI","NO"
)

var _Revision = 
IF(
    CALCULATE(COUNT('ECICEP revisión'[RUN]),
        FILTER(
            'ECICEP revisión',
            'ECICEP revisión'[RUN]='Ferrada'[RUN])
    ),"SI","NO"
)

RETURN

IF(
    _Actividad="SI" ||
    _Formulario="SI" ||
    _Revision="SI",
    "SI","NO")
```

### `Ferrada[ECICEP Seguimiento a distancia (act)]`

Seguimiento a distancia ECICEP SI/NO: atención con actividad «seguimiento a distancia» asociada a riesgo o multimorbilidad.

```dax
IF(
    CALCULATE(count('Atenciones'[RUN]),
        FILTER(
            'Atenciones',
            'Atenciones'[RUN]='Ferrada'[RUN] &&
            (
                CONTAINSSTRING('Atenciones'[ACTIVIDADES],"seguimiento a distancia") &&
                (
                    CONTAINSSTRING(Atenciones[ACTIVIDADES],"riesgo") ||
                    CONTAINSSTRING(Atenciones[ACTIVIDADES],"multimorbi")
                )
            )
        )
    ),"SI","NO"
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

### `Ferrada[GObj FLu 26]`

Grupo objetivo campaña influenza 2026: cumple alguno de — edad <11 o ≥60 años; sala respiratoria con asma/EPOC/SBOR/FQ; PSCV con HTA/DM/ECV; diagnóstico de riesgo en 12 meses cerrados (ERC etapa 4-5 o diálisis, hepatopatía crónica, cardiopatía, esquizofrenia o bipolaridad —criterio nuevo 2026—, TBC activa); embarazo; obesidad; pertenece a PAD o es cuidador PAD. La fórmula deja comentarios con criterios pendientes (fibrosis pulmonar, neuromuscular, epilepsia refractaria, cardiopatía no-ECV).

```dax
-- Edad: <11 (lactantes/niños hasta 5° básico aprox) O ≥60 años
var _Edad = 
    IF(
        'Ferrada'[Edad] < 11 || 'Ferrada'[Edad] >= 60,
        "SI", "NO")

-- Respiratorio: SALA + patología pulmonar crónica
var _Respi = 
    IF(
        'Ferrada'[SALA Ingresado] = "SI" &&
        (   'Ferrada'[SALA ASMA]  = "SI" ||
            'Ferrada'[SALA EPOC]  = "SI" ||
            'Ferrada'[SALA SBOR]  = "SI" ||
            'Ferrada'[SALA FQ]    = "SI"),
        "SI", "NO")
        -- Pendiente: fibrosis pulmonar, patología neuromuscular, epilepsia refractaria
        -- Agregar columnas SALA si existen

-- PSCV: patologías crónicas 11-59 años
var _PSCV = 
    IF(
        'Ferrada'[PSCV ¿Ingresado?] = "SI" &&
        (   'Ferrada'[PSCV HTA]  = "SI" ||
            'Ferrada'[PSCV DM]   = "SI" ||
            'Ferrada'[PSCV ECV]  = "SI"),
        "SI", "NO")
        -- Pendiente: cardiopatía (no idéntica a ECV), agregar columna si existe

-- Diagnósticos por CIE-10 en atenciones recientes (mes anterior completo)
-- Cubre: IRC etapa 4-5, diálisis, hepatopatías, cardiopatías,
--        esquizofrenia, trastorno bipolar (NUEVO 2026), TBC activa
var _FechaDesde = EOMONTH(TODAY(), -13) + 1
var _FechaHasta = EOMONTH(TODAY(), -1)

var _Dg = 
    IF(
        CALCULATE(
            COUNT(Atenciones[RUN]),
            FILTER(
                ALL(Atenciones),
                'Ferrada'[RUN] = Atenciones[RUN] &&
                Atenciones[FECHA ATENCION] >= _FechaDesde &&
                Atenciones[FECHA ATENCION] <= _FechaHasta &&
                (
                    -- Renal crónica etapa 4-5 y diálisis
                    CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "n18.4") ||
                    CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "n18.5") ||
                    CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "y84.1") ||
                    -- Hepatopatías (cirrosis, hepatitis crónica, otras)
                    CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "k70.3") ||
                    CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "k74")   ||
                    CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "k73")   ||
                    CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "b18")   ||
                    -- Cardiopatías isquémica, reumática, miocardiopatías
                    CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "i20")   ||
                    CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "i21")   ||
                    CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "i22")   ||
                    CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "i25")   ||
                    CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "i05")   ||
                    CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "i42")   ||
                    -- Enfermedades mentales graves (NUEVO LTO 2026)
                    CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "f20")   ||
                    CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "f31")   ||
                    -- TBC activa
                    CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "a15")   ||
                    CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "a16")   ||
                    CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "a19")
                )
            )
        ) >= 1,
        "SI", "NO")

var _Embarazo = 
    IF('Ferrada'[¿Embarazada?] = "SI", "SI", "NO")

-- Obesidad: IMC ≥30 adultos / >+2DE adolescentes
-- Asume que la columna IMC ya clasifica correctamente ambos grupos
var _Obesidad = 
    IF(CONTAINSSTRING('Ferrada'[IMC (resultado)], "obesi"), "SI", "NO")

-- PAD: conservado por precaución, no es criterio LTO estricto
var _PAD = 
    IF('Ferrada'[Pertenece a PAD] = "SI", "SI", "NO")

var _CuidadorPAD = 
    IF('Ferrada'[PAD Es cuidador?] = "SI", "SI", "NO")

RETURN
    IF(
        _Edad        = "SI" ||
        _PSCV        = "SI" ||
        _Respi       = "SI" ||
        _Dg          = "SI" ||
        _Embarazo    = "SI" ||
        _Obesidad    = "SI" ||
        _PAD         = "SI" ||
        _CuidadorPAD = "SI",
        "SI", "NO")
```

### `Ferrada[Influenza 2026]`

Indicador SI/NO de vacunación de campaña: tiene al menos una dosis en VacCampana cuya vacuna contiene «Influenza» administrada durante el año 2026.

```dax
IF(
    CALCULATE(
        COUNT(VacCampana[RUN]),
        FILTER(
            VacCampana,
            VacCampana[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING(VacCampana[VAC CAMPANA], "Influenza") &&
            YEAR(VacCampana[FECHA_ADMINISTRACION]) = 2026
        )
    ) > 0,
    "SI", "NO"
)
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

### `Ferrada[OTROS Artrosis C/R]`

Artrosis de cadera/rodilla SI/NO: diagnóstico M16/M17 médico o en Estratificación, formulario de artrosis válido, o receta crónica de paracetamol, celecoxib o tramadol.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING(Atenciones[INSTRUMENTO],"médic") &&
    (CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"M16") ||
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"M17")))),
    "SI","NO")

var _Estratificacion = 
IF(
    CALCULATE(COUNT(Estratificacion[RUN]),
    FILTER(ALL(Estratificacion),Estratificacion[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(Estratificacion[Diagnósticos],"M16") ||
    CONTAINSSTRING(Estratificacion[Diagnósticos],"M17")))),
    "SI","NO")

var _Formulario = 
IF(
    CALCULATE(COUNT('Otros y Respi'[RUN]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médico") &&
    CONTAINSSTRING('Otros y Respi'[84.- ¿PADECE DE ARTROSIS DE CADERA Y RODILLA?],"si") &&
    (CONTAINSSTRING('Otros y Respi'[85.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[85.- ESTADO],"seguimien")))),
    "SI","NO")

var _Receta =
IF(
    CALCULATE(COUNT('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Recetas Vigentes'[TIPO RECETA],"crónica") && 
    (CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"paracetamol") ||
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"celecoxi") ||
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"tramado")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Estratificacion="SI" ||
    _Formulario="SI" ||
    _Receta="SI",
    "SI","NO")
```

### `Ferrada[OTROS Epilepsia]`

Epilepsia SI/NO: diagnóstico G40/G41 en atención médica o Estratificación, formulario de epilepsia en ingreso/seguimiento, o receta crónica vigente de anticonvulsivante (levetiracetam, carbamazepina, ácido valproico, lamotrigina, fenitoína o fenobarbital).

```dax
var _Atenciones =
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING(Atenciones[INSTRUMENTO],"médic") &&
    (CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"G40") ||
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"G41")))),
    "SI","NO")

var _Estratificacion = 
IF(
    CALCULATE(COUNT(Estratificacion[RUN]),
    FILTER(ALL(Estratificacion),Estratificacion[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(Estratificacion[Diagnósticos],"G40") ||
    CONTAINSSTRING(Estratificacion[Diagnósticos],"G41")))),
    "SI","NO")

var _Formulario = 
IF(
    CALCULATE(COUNT('Otros y Respi'[RUN]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médico") &&
    CONTAINSSTRING('Otros y Respi'[75.- ¿PADECE DE EPILEPSIA?],"si") &&
    (CONTAINSSTRING('Otros y Respi'[79.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[79.- ESTADO],"seguimien")))),
    "SI","NO")

var _Receta = 
IF(
    CALCULATE(COUNT('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Recetas Vigentes'[TIPO RECETA],"cróni") &&
    (CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"levetiracetam") ||
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"carbamazepina") ||
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"valproico") ||
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"lamotrigina") ||
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"fenitoina") ||
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"fenobarbi")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Estratificacion="SI" ||
    _Formulario="SI" ||
    _Receta="SI",
    "SI","NO")
```

### `Ferrada[OTROS Glaucoma]`

Glaucoma SI/NO: diagnóstico H40 en alguna atención médica o en la Estratificación histórica.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL(Atenciones),Atenciones[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(Atenciones[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"H40")))),
    "SI","NO")

var _Historico =
IF(
    CALCULATE(COUNT(Estratificacion[RUN]),
    FILTER(ALL(Estratificacion),Estratificacion[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING(Estratificacion[Diagnósticos],"H40"))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Historico="SI",
    "SI","NO")
```

### `Ferrada[OTROS Hipotiroidismo]`

Hipotiroidismo SI/NO: diagnóstico E03 en atención médica o Estratificación, formulario «Otros y Respi» (pregunta 95) en ingreso/seguimiento, o receta crónica de levotiroxina. (Corregido jul-2026: el formulario no estaba incluido en el resultado.)

```dax
var _Atenciones =
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL(Atenciones),Atenciones[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(Atenciones[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"E03")))),
    "SI","NO")

var _Estratificacion =     
IF(
    CALCULATE(COUNT(Estratificacion[RUN]),
    FILTER(ALL(Estratificacion),Estratificacion[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING(Estratificacion[Diagnósticos],"E03"))),
    "SI","NO")

var _Formulario = 
IF(
    CALCULATE(COUNT('Otros y Respi'[RUN]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médico") &&
    CONTAINSSTRING('Otros y Respi'[95.- ¿PADECE DE HIPOTIROIDISMO?],"si") &&
    (CONTAINSSTRING('Otros y Respi'[96.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[96.- ESTADO],"seguimien")))),
    "SI","NO")

var _Receta = 
IF(
    CALCULATE(COUNT('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Recetas Vigentes'[TIPO RECETA],"crónica") && 
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"levotiroxina")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Estratificacion="SI" ||
    _Formulario="SI" ||
    _Receta="SI",
    "SI","NO")
```

### `Ferrada[OTROS Parkinson]`

Parkinson SI/NO: diagnóstico G20 médico o en Estratificación, formulario de Parkinson válido, o receta crónica de levodopa, pramipexol, quetiapina 25 o primidona.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(Atenciones[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"G20")))),
    "SI","NO")

var _Estratificacion = 
IF(
    CALCULATE(COUNT(Estratificacion[RUN]),
    FILTER(ALL(Estratificacion),Estratificacion[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING(Estratificacion[Diagnósticos],"G20"))),
    "SI","NO")

var _Formulario = 
IF(
    CALCULATE(COUNT('Otros y Respi'[RUN]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Otros y Respi'[81.- ¿PADECE DE LA ENFERMEDAD DE PARKINSON?],"si") &&
    (CONTAINSSTRING('Otros y Respi'[82.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[82.- ESTADO],"seguimient")))),
    "SI","NO")

var _Receta = 
IF(
    CALCULATE(COUNT('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Recetas Vigentes'[TIPO RECETA],"crónic") &&
    (CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"levodopa") ||
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"pramipexol") ||
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"quetiapina 25") ||
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"primidona")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Estratificacion="SI" ||
    _Formulario="SI" ||
    _Receta="SI",
    "SI","NO")
```

### `Ferrada[PAD Es cuidador?]`

Indicador SI/NO: su RUN figura como RUN de cuidador en la planilla PAD (Drive) — es cuidador/a de un paciente con dependencia.

```dax
IF(
    CALCULATE(COUNT('PAD Drive'[RUN Cuidador]),
    FILTER(ALL('PAD Drive'),'PAD Drive'[RUN Cuidador]='Ferrada'[RUN])),
    "SI","NO")
```

### `Ferrada[PROTECCION NIÑEZ]`

Alerta de protección de niñez desde «Inscritos»: «SENAME» si las alertas administrativas contienen SENAME; «Mejor Niñez» si contienen SPE; «NO» en otro caso.

```dax
IF(
    CALCULATE(
        COUNT(Inscritos[RUN]),
        FILTER(ALL(Inscritos), 
            Inscritos[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING(Inscritos[ALERTAS ADMINISTRATIVAS], "SENAME")
        )
    ) > 0,
    "SENAME",
    IF(
        CALCULATE(
            COUNT(Inscritos[RUN]),
            FILTER(ALL(Inscritos),
                Inscritos[RUN] = 'Ferrada'[RUN] &&
                CONTAINSSTRING(Inscritos[ALERTAS ADMINISTRATIVAS], "SPE")
            )
        ) > 0,
        "Mejor Niñez",
        "NO"
    )
)
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

### `Ferrada[PSCV LDL >160]`

Indicador SI/NO: LDL ≥160 mg/dL. Nota: el nombre dice «>160» pero la fórmula usa ≥.

```dax
IF(
    'Ferrada'[PSCV LDL]>=160,
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

### `Ferrada[Pertenece a Otros]`

Pertenencia a «Otros crónicos»: «SI» si cualquiera de Epilepsia, Parkinson, Glaucoma, Artrosis C/R, Hipotiroidismo o Alivio del dolor es «SI».

```dax
IF('Ferrada'[OTROS Epilepsia]="SI" || 
'Ferrada'[OTROS Parkinson]="SI" || 
'Ferrada'[OTROS Glaucoma]="SI" || 
'Ferrada'[OTROS Artrosis C/R]="SI" || 
'Ferrada'[OTROS Hipotiroidismo]="SI" || 
'Ferrada'[OTROS Alivio del dolor]="SI",
"SI","NO")
```

### `Ferrada[Pertenece a PAD]`

Indicador SI/NO: el RUN del paciente aparece en la tabla «PAD Drive».

```dax
IF(LOOKUPVALUE('PAD Drive'[RUN],'PAD Drive'[RUN],'Ferrada'[RUN]) <> "",
"SI","NO")
```

### `Ferrada[Pertenece a SALA]`

Pertenencia a sala respiratoria: «SI» si cualquiera de [SALA ASMA], [SALA SBOR], [SALA EPOC], [SALA Otras Respi], [SALA Asistencia Ventilatoria], [SALA FQ] o [SALA O2 Dependiente] es «SI».

```dax
IF('Ferrada'[SALA ASMA]="SI" || 
'Ferrada'[SALA SBOR]="SI" || 
'Ferrada'[SALA EPOC]="SI" || 
'Ferrada'[SALA Otras Respi]="SI" || 
'Ferrada'[SALA Asistencia Ventilatoria]="SI" || 
'Ferrada'[SALA FQ]="SI" || 
'Ferrada'[SALA O2 Dependiente]="SI",
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

### `Ferrada[SALA ASMA]`

Asma en sala SI/NO: requiere no ser SBOR ([SALA SBOR]=«NO») y cumplir alguna de: diagnóstico J45 en atención médica, J45 en Estratificación, o último formulario «Otros y Respi» de asma válido (asma=«sí», gravedad y estado de control registrados, ingreso/seguimiento).

```dax
var _SBOR = 
IF(
    'Ferrada'[SALA SBOR]="NO","SI","NO")

var _Atenciones = 
IF(
    CALCULATE(count(Atenciones[RUN]),
    FILTER(ALL(Atenciones),Atenciones[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(Atenciones[DIAGNOSTICOS],"J45") &&
    CONTAINSSTRING(Atenciones[INSTRUMENTO],"médic")))),
    "SI","NO")

var _Estratificacion =
IF(
    CONTAINSSTRING(LOOKUPVALUE(Estratificacion[Diagnósticos],Estratificacion[RUN],'Ferrada'[RUN]),"J45"),
     "SI","NO")

var _Fecha = 
LASTDATE(
    CALCULATETABLE(VALUES('Otros y Respi'[FECHA ATENCION]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Otros y Respi'[9.- ¿PADECE DE ASMA BRONQUIAL?],"si")) &&
    'Otros y Respi'[11.- GRAVEDAD ASMA BRONQUIAL]<>"" &&
    'Otros y Respi'[13.- ESTADO DE CONTROL ASMA]<>"" &&
    (CONTAINSSTRING('Otros y Respi'[10.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[10.- ESTADO],"seguimiento")))))

var _Formulario = 
IF(
    CALCULATE(COUNT('Otros y Respi'[RUN]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    'Otros y Respi'[FECHA ATENCION]=_Fecha &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    'Otros y Respi'[11.- GRAVEDAD ASMA BRONQUIAL]<>"" &&
    'Otros y Respi'[13.- ESTADO DE CONTROL ASMA]<>"" &&
    CONTAINSSTRING('Otros y Respi'[9.- ¿PADECE DE ASMA BRONQUIAL?],"si")) &&
    (CONTAINSSTRING('Otros y Respi'[10.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[10.- ESTADO],"seguimiento")))),
    "SI","NO")

RETURN

IF(
    _SBOR="Si" &&
(
    _Atenciones="si" ||
    _Estratificacion="si" ||
    _Formulario="si"
),
    "SI","NO")
```

### `Ferrada[SALA ASMA Gravedad]`

Gravedad del asma bronquial según el último formulario «Otros y Respi» médico con asma=«sí» y gravedad registrada. Solo se muestra si [SALA ASMA]=«SI».

```dax
var _Fecha = 
LASTDATE(
CALCULATETABLE(VALUES('Otros y Respi'[FECHA ATENCION]),
FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
(CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médico") &&
CONTAINSSTRING('Otros y Respi'[9.- ¿PADECE DE ASMA BRONQUIAL?],"si")) &&
'Otros y Respi'[11.- GRAVEDAD ASMA BRONQUIAL]<>"")))

var _Formularios =
TOPN(1,
CALCULATETABLE(VALUES('Otros y Respi'[11.- GRAVEDAD ASMA BRONQUIAL]),
FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
'Otros y Respi'[FECHA ATENCION] = _Fecha)),
'Otros y Respi'[11.- GRAVEDAD ASMA BRONQUIAL],DESC)

var _Resultado = 
IF(_Formularios="",BLANK(),_Formularios
)

RETURN

IF(
    'Ferrada'[SALA ASMA]="SI",
IF(
    _Resultado="",BLANK(),_Resultado))
```

### `Ferrada[SALA EPOC]`

EPOC en sala SI/NO: requiere ≥40 años y alguna de: diagnóstico J44 médico, J44 en Estratificación, o último formulario EPOC válido (padece=«sí», tipo y control registrados, ingreso/seguimiento).

```dax
var _Edad = 
IF(
    'Ferrada'[Edad]>=40,"SI","NO")

var _Atenciones = 
IF(
CALCULATE(count('Atenciones'[RUN]),
FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
(CONTAINSSTRING(Atenciones[INSTRUMENTO],"médic") &&
CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"J44")))),
"SI","NO")

var _Estratificacion = 
IF(
CONTAINSSTRING(LOOKUPVALUE(Estratificacion[Diagnósticos],Estratificacion[RUN],'Ferrada'[RUN]),"J44"),
"SI","NO")

var _Fecha = 
LASTDATE(
    CALCULATETABLE(VALUES('Otros y Respi'[FECHA ATENCION]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Otros y Respi'[14.- ¿PADECE ENFERMEDAD PULMONAR CRONICA?],"si")) &&
    'Otros y Respi'[16.- TIPO EPOC]<>"" &&
    'Otros y Respi'[19.- ESTADO DE CONTROL EPOC]<>"" &&
    (CONTAINSSTRING('Otros y Respi'[17.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[17.- ESTADO],"seguimiento")))))

var _Formulario = 
IF(
    CALCULATE(COUNT('Otros y Respi'[RUN]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    'Otros y Respi'[FECHA ATENCION]=_Fecha &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Otros y Respi'[14.- ¿PADECE ENFERMEDAD PULMONAR CRONICA?],"si")) &&
    'Otros y Respi'[16.- TIPO EPOC]<>"" &&
    'Otros y Respi'[19.- ESTADO DE CONTROL EPOC]<>"" &&
    (CONTAINSSTRING('Otros y Respi'[17.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[17.- ESTADO],"seguimiento")))),
    "SI","NO")

RETURN

IF(
    _Edad="si" &&
(
    _Atenciones="si" ||
    _Estratificacion="si" ||
    _Formulario="si"
),
    "SI","NO")
```

### `Ferrada[SALA EPOC Tipo]`

Del último formulario «Otros y Respi» médico válido de EPOC (padece EPOC=«sí», tipo y estado de control no vacíos, estado ingreso/seguimiento) devuelve «16.- TIPO EPOC». Solo se muestra si [SALA EPOC]=«SI»; si no, BLANK.

```dax
var _Fecha = 
LASTDATE(
CALCULATETABLE(VALUES('Otros y Respi'[FECHA ATENCION]),
FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Otros y Respi'[14.- ¿PADECE ENFERMEDAD PULMONAR CRONICA?],"si")) &&
    'Otros y Respi'[16.- TIPO EPOC]<>"" &&
    'Otros y Respi'[19.- ESTADO DE CONTROL EPOC]<>"" &&
    (CONTAINSSTRING('Otros y Respi'[17.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[17.- ESTADO],"seguimiento")))))

var _Formularios =
TOPN(1,
CALCULATETABLE(VALUES('Otros y Respi'[16.- TIPO EPOC]),
FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
'Otros y Respi'[FECHA ATENCION] = _Fecha &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Otros y Respi'[14.- ¿PADECE ENFERMEDAD PULMONAR CRONICA?],"si")) &&
    'Otros y Respi'[16.- TIPO EPOC]<>"" &&
    'Otros y Respi'[19.- ESTADO DE CONTROL EPOC]<>"" &&
    (CONTAINSSTRING('Otros y Respi'[17.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[17.- ESTADO],"seguimiento")))),
'Otros y Respi'[16.- TIPO EPOC],DESC)

var _Resultado = 
IF(_Formularios="",BLANK(),_Formularios)

RETURN

IF(
    'Ferrada'[SALA EPOC]="SI",
IF(
    _Resultado="",BLANK(),_Resultado))
```

### `Ferrada[SALA Ingresado]`

Ingreso a sala respiratoria SI/NO: consolida los formularios «Otros y Respi» válidos de las siete líneas (SBOR si <5 años, asma si no es SBOR, EPOC si ≥40 años, otras respiratorias, asistencia ventilatoria, O2 dependiente y fibrosis quística). Basta una línea válida. A diferencia de las columnas SALA por patología, aquí solo cuenta el formulario (no diagnósticos ni estratificación).

```dax
var _FechaASMA = 
LASTDATE(
    CALCULATETABLE(VALUES('Otros y Respi'[FECHA ATENCION]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Otros y Respi'[9.- ¿PADECE DE ASMA BRONQUIAL?],"si")) &&
    'Otros y Respi'[11.- GRAVEDAD ASMA BRONQUIAL]<>"" &&
    'Otros y Respi'[13.- ESTADO DE CONTROL ASMA]<>"" &&
    (CONTAINSSTRING('Otros y Respi'[10.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[10.- ESTADO],"seguimiento")))))

var _FormularioASMA = 
IF(
    CALCULATE(COUNT('Otros y Respi'[RUN]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    'Otros y Respi'[FECHA ATENCION]=_FechaASMA &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    'Otros y Respi'[11.- GRAVEDAD ASMA BRONQUIAL]<>"" &&
    'Otros y Respi'[13.- ESTADO DE CONTROL ASMA]<>"" &&
    CONTAINSSTRING('Otros y Respi'[9.- ¿PADECE DE ASMA BRONQUIAL?],"si")) &&
    (CONTAINSSTRING('Otros y Respi'[10.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[10.- ESTADO],"seguimiento")))),
    "SI","NO")

var _FechaEPOC = 
LASTDATE(
    CALCULATETABLE(VALUES('Otros y Respi'[FECHA ATENCION]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Otros y Respi'[14.- ¿PADECE ENFERMEDAD PULMONAR CRONICA?],"si")) &&
    'Otros y Respi'[16.- TIPO EPOC]<>"" &&
    'Otros y Respi'[19.- ESTADO DE CONTROL EPOC]<>"" &&
    (CONTAINSSTRING('Otros y Respi'[17.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[17.- ESTADO],"seguimiento")))))

var _FormularioEPOC = 
IF(
    CALCULATE(COUNT('Otros y Respi'[RUN]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    'Otros y Respi'[FECHA ATENCION]=_FechaEPOC &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Otros y Respi'[14.- ¿PADECE ENFERMEDAD PULMONAR CRONICA?],"si")) &&
    'Otros y Respi'[16.- TIPO EPOC]<>"" &&
    'Otros y Respi'[19.- ESTADO DE CONTROL EPOC]<>"" &&
    (CONTAINSSTRING('Otros y Respi'[17.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[17.- ESTADO],"seguimiento")))),
    "SI","NO")

var _FechaSBOR = 
LASTDATE(
    CALCULATETABLE(VALUES('Otros y Respi'[FECHA ATENCION]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Otros y Respi'[1.- ¿PADECE DE SÍNDROME BRONQUIAL OBSTRUCTIVO?],"si") &&
    CONTAINSSTRING('Otros y Respi'[2.- ¿ES RECURRENTE?],"si")) &&
    'Otros y Respi'[4.- GRAVEDAD SBOR]<>"" &&
    (CONTAINSSTRING('Otros y Respi'[3.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[3.- ESTADO],"seguimiento")))))

var _FormularioSBOR = 
IF(
    CALCULATE(COUNT('Otros y Respi'[RUN]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    'Otros y Respi'[FECHA ATENCION] = _FechaSBOR &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Otros y Respi'[1.- ¿PADECE DE SÍNDROME BRONQUIAL OBSTRUCTIVO?],"si") &&
    CONTAINSSTRING('Otros y Respi'[2.- ¿ES RECURRENTE?],"si")) &&
    'Otros y Respi'[4.- GRAVEDAD SBOR]<>"" &&
    (CONTAINSSTRING('Otros y Respi'[3.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[3.- ESTADO],"seguimiento")))),
    "SI","NO")

var _FechaAV = 
LASTDATE(
CALCULATETABLE(VALUES('Otros y Respi'[FECHA ATENCION]),
FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
(CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médico") &&
CONTAINSSTRING('Otros y Respi'[26.- ¿NECESITA ASISTENCIA VENTILATORIA?],"si")) &&
'Otros y Respi'[27.- ASISTENCIA VENTILATORIA]<>"" &&
(CONTAINSSTRING('Otros y Respi'[28.- ESTADO ASISTENCIA VENTILATORIA],"ingreso") ||
CONTAINSSTRING('Otros y Respi'[28.- ESTADO ASISTENCIA VENTILATORIA],"seguimiento")))))

var _FormularioAV = 
IF(
CALCULATE(COUNT('Otros y Respi'[RUN]),
FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
'Otros y Respi'[FECHA ATENCION] = _FechaAV &&
(CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médico") &&
CONTAINSSTRING('Otros y Respi'[26.- ¿NECESITA ASISTENCIA VENTILATORIA?],"si")) &&
'Otros y Respi'[27.- ASISTENCIA VENTILATORIA]<>"" &&
(CONTAINSSTRING('Otros y Respi'[28.- ESTADO ASISTENCIA VENTILATORIA],"ingreso") ||
CONTAINSSTRING('Otros y Respi'[28.- ESTADO ASISTENCIA VENTILATORIA],"seguimiento")))),
"SI","NO")

var _FechaOtrosR = 
LASTDATE(
CALCULATETABLE(VALUES('Otros y Respi'[FECHA ATENCION]),
FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
(CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médico") &&
CONTAINSSTRING('Otros y Respi'[23.- ¿ES OXIGENO DEPENDIENTE?],"si")) &&
(CONTAINSSTRING('Otros y Respi'[24.- ESTADO],"ingreso") ||
CONTAINSSTRING('Otros y Respi'[24.- ESTADO],"seguimiento")))))

var _FormularioOtrosRespi = 
IF(
CALCULATE(COUNT('Otros y Respi'[RUN]),
FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
'Otros y Respi'[FECHA ATENCION] = _FechaOtrosR &&
(CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médico") &&
CONTAINSSTRING('Otros y Respi'[23.- ¿ES OXIGENO DEPENDIENTE?],"si")) &&
(CONTAINSSTRING('Otros y Respi'[24.- ESTADO],"ingreso") ||
CONTAINSSTRING('Otros y Respi'[24.- ESTADO],"seguimiento")))),
"SI","NO")

var _FechaO2 = 
LASTDATE(
CALCULATETABLE(VALUES('Otros y Respi'[FECHA ATENCION]),
FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
(CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médico") &&
CONTAINSSTRING('Otros y Respi'[23.- ¿ES OXIGENO DEPENDIENTE?],"si")) &&
(CONTAINSSTRING('Otros y Respi'[24.- ESTADO],"ingreso") ||
CONTAINSSTRING('Otros y Respi'[24.- ESTADO],"seguimiento")))))

var _FormularioO2 = 
IF(
CALCULATE(COUNT('Otros y Respi'[RUN]),
FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
'Otros y Respi'[FECHA ATENCION] = _FechaO2 &&
(CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médico") &&
CONTAINSSTRING('Otros y Respi'[23.- ¿ES OXIGENO DEPENDIENTE?],"si")) &&
(CONTAINSSTRING('Otros y Respi'[24.- ESTADO],"ingreso") ||
CONTAINSSTRING('Otros y Respi'[24.- ESTADO],"seguimiento")))),
"SI","NO")

var _FechaFQ = 
LASTDATE(
    CALCULATETABLE(VALUES('Otros y Respi'[FECHA ATENCION]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Otros y Respi'[30.- ¿PADECE DE FIBROSIS QUISTICA?],"si")) &&
    (CONTAINSSTRING('Otros y Respi'[31.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[31.- ESTADO],"seguimiento")))))

var _FormularioFQ = 
IF(
    CALCULATE(COUNT('Otros y Respi'[RUN]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    'Otros y Respi'[FECHA ATENCION]=_FechaFQ &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Otros y Respi'[30.- ¿PADECE DE FIBROSIS QUISTICA?],"si")) &&
    (CONTAINSSTRING('Otros y Respi'[31.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[31.- ESTADO],"seguimiento")))),
    "SI","NO")

var _ASMA = 
IF(
    'Ferrada'[SALA SBOR]="NO" &&
    _FormularioASMA="SI",
    "SI","NO")

var _SBOR = 
IF(
    'Ferrada'[Edad]<5 &&
    _FormularioSBOR="SI",
    "SI","NO")

var _EPOC = 
IF(
    'Ferrada'[Edad]>=40 &&
    _FormularioEPOC="SI",
    "SI","NO")

var _OTROS = 
IF(
    _FormularioOtrosRespi="SI",
    "SI","NO")

var _O2 = 
IF(
    _FormularioO2="SI",
    "SI","NO")

var _AV = 
IF(
    _FormularioAV="SI",
    "SI","NO")

var _FQ = 
IF(
    _FormularioFQ="SI",
    "SI","NO")

RETURN

IF(
    _SBOR="SI" ||
    _ASMA="SI" ||
    _EPOC="SI" ||
    _OTROS="SI" ||
    _AV="SI" ||
    _O2="SI" ||
    _FQ="SI",
    "SI","NO")
```

### `Ferrada[SALA SBOR]`

SBOR en sala SI/NO: requiere <5 años y alguna de: diagnóstico «bronquial obstructivo recurrente» en atención médica o Estratificación, o último formulario SBOR válido (SBO=«sí», recurrente=«sí», gravedad registrada).

```dax
var _Edad = 
IF(
    'Ferrada'[Edad]<5,"SI","NO")

var _Atenciones = 
IF(
CALCULATE(count('Atenciones'[RUN]),
FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
(CONTAINSSTRING(Atenciones[INSTRUMENTO],"médic") &&
CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"bronquial obstructivo recurrente")))),
"SI","NO")

var _Estratificacion = 
IF(
CONTAINSSTRING(LOOKUPVALUE(Estratificacion[Diagnósticos],Estratificacion[RUN],'Ferrada'[RUN]),"bronquial obstructivo recurrente"),
"SI","NO")

var _Fecha = 
LASTDATE(
    CALCULATETABLE(VALUES('Otros y Respi'[FECHA ATENCION]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Otros y Respi'[1.- ¿PADECE DE SÍNDROME BRONQUIAL OBSTRUCTIVO?],"si") &&
    CONTAINSSTRING('Otros y Respi'[2.- ¿ES RECURRENTE?],"si")) &&
    'Otros y Respi'[4.- GRAVEDAD SBOR]<>"" &&
    (CONTAINSSTRING('Otros y Respi'[3.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[3.- ESTADO],"seguimiento")))))

var _Formulario = 
IF(
    CALCULATE(COUNT('Otros y Respi'[RUN]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    'Otros y Respi'[FECHA ATENCION] = _Fecha &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Otros y Respi'[1.- ¿PADECE DE SÍNDROME BRONQUIAL OBSTRUCTIVO?],"si") &&
    CONTAINSSTRING('Otros y Respi'[2.- ¿ES RECURRENTE?],"si")) &&
    'Otros y Respi'[4.- GRAVEDAD SBOR]<>"" &&
    (CONTAINSSTRING('Otros y Respi'[3.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[3.- ESTADO],"seguimiento")))),
    "SI","NO")

RETURN

IF(
    _Edad="si" &&
(
    _Atenciones="si" ||
    _Estratificacion="si" ||
    _Formulario="si"
),
    "SI","NO")
```

### `Ferrada[SALA SBOR Gravedad]`

Gravedad del SBOR según el último formulario «Otros y Respi» médico válido (padece SBO=«sí», recurrente=«sí», gravedad no vacía, estado ingreso/seguimiento). Solo se muestra si el paciente tiene <5 años y [SALA SBOR]=«SI».

```dax
var _Edad = 
IF(
    'Ferrada'[Edad]<5,"SI","NO")

var _Fecha = 
LASTDATE(
    CALCULATETABLE(VALUES('Otros y Respi'[FECHA ATENCION]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Otros y Respi'[1.- ¿PADECE DE SÍNDROME BRONQUIAL OBSTRUCTIVO?],"si") &&
    CONTAINSSTRING('Otros y Respi'[2.- ¿ES RECURRENTE?],"si")) &&
    'Otros y Respi'[4.- GRAVEDAD SBOR]<>"" &&
    (CONTAINSSTRING('Otros y Respi'[3.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[3.- ESTADO],"seguimiento")))))

var _Formulario = 
    CALCULATETABLE(VALUES('Otros y Respi'[4.- GRAVEDAD SBOR]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    'Otros y Respi'[FECHA ATENCION] = _Fecha &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Otros y Respi'[1.- ¿PADECE DE SÍNDROME BRONQUIAL OBSTRUCTIVO?],"si") &&
    CONTAINSSTRING('Otros y Respi'[2.- ¿ES RECURRENTE?],"si")) &&
    (CONTAINSSTRING('Otros y Respi'[3.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[3.- ESTADO],"seguimiento"))))

var _Resultado = 
IF(
    _Formulario="",BLANK(),_Formulario)

RETURN
IF(
    _Edad="SI" && 'Ferrada'[SALA SBOR]="SI",
IF(_Resultado="",BLANK(),_Resultado)    )
```

### `Ferrada[SM Ingresado]`

Ingreso a salud mental SI/NO: alguna de las 28 columnas de estado (form) vale «Activo». (Corregido jul-2026: un typo hacía que Oposicionista desafiante nunca activara el indicador.)

```dax
IF(
'Ferrada'[SM Violencia (form)]="activo" ||
'Ferrada'[SM Abuso Sexual (form)]="activo" || 
'Ferrada'[SM Suicidio (form)]="activo" ||
'Ferrada'[SM Depresión (form)]="activo" ||
'Ferrada'[SM Bipolaridad (form)]="activo" ||
'Ferrada'[SM OH Perjudical (form)]="activo" || 
'Ferrada'[SM OH Dependiente (form)]="activo" ||
'Ferrada'[SM Drogas Perjudical (form)]="activo" || 
'Ferrada'[SM Drogas Dependiente (form)]="activo" ||
'Ferrada'[SM OH y Drogas (form)]="activo" ||
'Ferrada'[SM TDAH (form)]="activo" ||
'Ferrada'[SM Oposicionista desafiante (form)]="activo" ||
'Ferrada'[SM Ansiedad separación (form)]="activo" ||
'Ferrada'[SM Otras Infancia/Adolescencia (form)]="activo" ||
'Ferrada'[SM Ansiedad (form)]="activo" ||
'Ferrada'[SM Demencia (form)]="activo" ||
'Ferrada'[SM Esquizofrenia (form)]="activo" ||
'Ferrada'[SM Adaptativo (form)]="activo" ||
'Ferrada'[SM Conducta Alimentaria (form)]="activo" ||
'Ferrada'[SM Retraso Mental (form)]="activo" ||
'Ferrada'[SM Personalidad (form)]="activo" ||
'Ferrada'[SM Autismo (form)]="activo" ||
'Ferrada'[SM Asperger (form)]="activo" ||
'Ferrada'[SM Rett (form)]="activo" ||
'Ferrada'[SM Desintegrativo niñez (form)]="activo" ||
'Ferrada'[SM TGD (form)]="activo" ||
'Ferrada'[SM Otras (form)]="activo" ||
'Ferrada'[SM Depresión Postparto (form)]="activo",
"SI","NO")
```

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

### `Ferrada[Validado]`

Indicador SI/NO: el RUN del paciente aparece en la tabla «PVI actualizada».

```dax
IF(LOOKUPVALUE('PVI actualizada'[RUN],'PVI actualizada'[RUN],'Ferrada'[RUN]) <> "",
"SI","NO")
```

### `Ferrada[¿Atendido 1 mes?]`

Indicador SI/NO: tuvo al menos una atención durante el mes anterior completo.

```dax
VAR FechaInicioMesAnterior = EOMONTH(TODAY(), -2) + 1
VAR FechaFinMesAnterior = EOMONTH(TODAY(), -1)
VAR AtencionesMesAnterior = 
    CALCULATE(
        COUNTROWS(Atenciones),
        FILTER(
            ALL(Atenciones),
            Atenciones[RUN] = 'Ferrada'[RUN] &&
            Atenciones[FECHA ATENCION] >= FechaInicioMesAnterior &&
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
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

### `Ferrada[¿Embarazada?]`

Embarazo probable SI/NO: control prenatal o formulario de gestante con matrona/matrón dentro de los últimos 3 meses cerrados.

```dax
VAR FechaInicio = EOMONTH(TODAY(), -3) + 1
VAR FechaFin = EOMONTH(TODAY(), -1)
VAR AtencionesGestante =
CALCULATE(
    COUNTROWS(Atenciones),
    FILTER(
        ALL(Atenciones),
        Atenciones[RUN] = 'Ferrada'[RUN] &&
        Atenciones[FECHA ATENCION] >= FechaInicio &&
        Atenciones[FECHA ATENCION] <= FechaFin &&
        CONTAINSSTRING(Atenciones[INSTRUMENTO], "matron") &&
        (
            CONTAINSSTRING(Atenciones[ACTIVIDADES], "control prenatal") ||
            CONTAINSSTRING(Atenciones[FORMULARIOS CLINICOS], "gestante")
        )
    )
)

RETURN
IF(AtencionesGestante > 0, "SI", "NO")
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

### `Ferrada[¿Pertenece algún programa?]`

Pertenencia a cualquier programa: «SI» si pertenece a ECICEP, Otros, PAD, PSCV, PSM o Sala.

```dax
IF(
    [Pertenece a ECICEP] = "SI"
        || [Pertenece a Otros] = "SI"
        || [Pertenece a PAD] = "SI"
        || [Pertenece a PSCV] = "SI"
        || [Pertenece a PSM] = "SI"
        || [Pertenece a Sala] = "SI",
    "SI",
    "NO"
)
```

### `Ferrada[Última Atención (fecha)]`

Fecha de la última atención registrada del paciente (cualquier tipo).

*Tipo:* dateTime  ·  *calculatedColumn*

```dax
LASTDATE(
    CALCULATETABLE(VALUES(Atenciones[FECHA ATENCION]),
    FILTER(ALL(Atenciones),Atenciones[RUN]='Ferrada'[RUN])))
```

### `Inscritos[FECHA DE INSCRIPCION]`

_Campo base (no calculado): proviene de la carga de Power Query._
