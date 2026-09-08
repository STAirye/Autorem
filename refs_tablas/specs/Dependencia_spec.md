# Especificación de la página «Dependencia»

Extraído automáticamente de la capa de reporte (PBIR) y del modelo semántico (TMDL).

**39 visuales · 64 campos distintos del modelo.**

## Filtros de página

- `Ferrada[PAD o cuidador?]` (Advanced) → ['null']

## Visuales

### 1. ASMA — `slicer`

- **Values:** `Ferrada[SALA ASMA]` — «ASMA»

### 2. Artrosis — `slicer`

- **Values:** `Ferrada[OTROS Artrosis C/R]` — «Artrosis C/R»

### 3. ¿Oncológico? — `slicer`

- **Values:** `Ferrada[PAD Onco?]`

### 4. ¿PSCV? — `slicer`

- **Values:** `Ferrada[PSCV ¿Ingresado?]` — «¿Ingresado PSCV?»

### 5. Asisten Vent — `slicer`

- **Values:** `Ferrada[SALA Asistencia Ventilatoria]` — «Asistencia Vent?»

### 6. Epilepsia — `slicer`

- **Values:** `Ferrada[OTROS Epilepsia]` — «Epilepsia»

### 7. Sector — `slicer`

- **Values:** `Ferrada[Sector]`

### 8. ECV — `slicer`

- **Values:** `Ferrada[PSCV ECV]` — «ECV»

### 9. DM — `slicer`

- **Values:** `Ferrada[PSCV DM]` — «DM»

### 10. Hipotiroidismo — `slicer`

- **Values:** `Ferrada[OTROS Hipotiroidismo]` — «Hipotiroidismo»

### 11. EMPA — `slicer`

- **Values:** `Ferrada[Citar a EMPA]`

### 12. Número de visitas totales por mes en los últimos 12 meses — `clusteredColumnChart`

- **Category:** `?[Mes]` — «FECHA ATENCION Mes»
- **Tooltips:** MIN(`Atenciones[FECHA ATENCION]`) — «Primera fecha: FECHA ATENCION»
- **Y:** SUM(`Atenciones[VDI (act)]`) — «Suma de VDI (act)1»

### 13. Estado — `slicer`

- **Values:** `Ferrada[Estado]`

### 14. Parkinson — `slicer`

- **Values:** `Ferrada[OTROS Parkinson]` — «Parkinson»

### 15. Dependiente o Cuidador — `slicer`

- **Values:** `Ferrada[PAD o cuidador?]`

### 16. Meses — `slicer`

- **Values:** `Ferrada[Meses]` — «Edad Meses»

### 17. Preventivo Cuidador — `pieChart`

- **Category:** `Ferrada[Citar a Preventivo]`
- **Y:** COUNT(`Ferrada[Citar a Preventivo]`) — «Recuento de Citar a Preventivo»

### 18. Población PAD — `tableEx`

- **Values:** `Ferrada[Tipo de identificación]`
- **Values:** `Ferrada[RUN]` — «Número»
- **Values:** `Ferrada[Nombre Social]`
- **Values:** `Ferrada[Nombre completo]`
- **Values:** `Ferrada[Sexo]`
- **Values:** `Ferrada[Género]`
- **Values:** `Ferrada[Edad]` — «Años»
- **Values:** `Ferrada[Sector]`
- **Values:** `Ferrada[¿Originario o Migrante?]`
- **Values:** `Ferrada[Nacionalidad]`
- **Values:** `Ferrada[Dirección Completa]`
- **Values:** `Ferrada[Celular]`
- **Values:** `Ferrada[Mail]`
- **Values:** `Ferrada[Situación]`
- **Values:** `Ferrada[Estado]`
- **Values:** `Ferrada[IMC (resultado)]`
- **Values:** `Ferrada[Cuenta Condiciones Crónicas]`
- **Values:** `Ferrada[Cuenta VDI seguimiento 12m (act)]` — «Cuenta VDI seguimiento (act)»
- **Values:** `Ferrada[Cuenta VDI seguimiento Enf 12m (act)]` — «Cuenta VDI Seguimiento Enf (act)»
- **Values:** `Ferrada[PAD VDI Seguimiento Enf útima (fecha)]` — «VDI Seguimiento Enf (fecha)»
- **Values:** `Ferrada[Cuenta VDI seguimiento TENS 12m (act)]` — «Cuenta VDI seguimiento TENS (act)»
- **Values:** `Ferrada[Cuenta VDI seguimiento Med 12m (act)]` — «Cuenta VDI seguimiento Med (act)»
- **Values:** `Ferrada[Cuenta VDI seguimiento Nutri 12m (act)]` — «Cuenta VDI seguimiento Nutri»
- **Values:** `Ferrada[Cuenta VDI seguimiento Nutri NED 12m (act)]` — «Cuenta VDI seguimiento NED Nutri (act)»
- **Values:** `Ferrada[Cuenta VDI seguimiento Kine 12m (act)]` — «Cuenta VDI seguimiento Kine (act)»
- **Values:** `Ferrada[Cuenta VDI seguimiento Odonto 12m (act)]` — «Cuenta VDI seguimiento Odonto (act)»
- **Values:** `Ferrada[Cuenta VDI seguimiento TO 12m (act)]` — «Cuenta VDI seguimiento TO (act)»
- **Values:** `Ferrada[Cuenta VDI seguimiento TS 12m (act)]` — «Cuenta VDI seguimiento TS (act)»
- **Values:** `Ferrada[Cuenta VDP 12m (act)]`
- **Values:** `Ferrada[Barthel (Resultado)]`
- **Values:** `Ferrada[Barthel Fecha]`
- **Values:** `Ferrada[Receta vigencia (mes)]`
- **Values:** `Ferrada[PSCV ¿Ingresado?]`
- **Values:** `Ferrada[SALA Ingresado]` — «Respiratorio ¿Ingresado?»
- **Values:** `Ferrada[SM Demencia]` — «¿Demencia?»
- **Values:** `Ferrada[PAD Onco?]` — «¿Oncológico?»
- **Values:** `Ferrada[PAD CPU]` — «¿CPU?»
- **Values:** `Ferrada[Pertenece a ECICEP]` — «¿ECICEP?»
- **Values:** `Ferrada[Citar a EMPA]`
- **Values:** `Ferrada[Citar a EMPAM]`
- **Values:** `Ferrada[Citar a PAP]`

### 19. CLAP — `slicer`

- **Values:** `Ferrada[Citar a CLAP]`

### 20. Migr o Origin — `slicer`

- **Values:** `Ferrada[¿Originario o Migrante?]`

### 21. EPOC — `slicer`

- **Values:** `Ferrada[SALA EPOC]` — «EPOC»

### 22. ¿Otros Cr? — `slicer`

- **Values:** `Ferrada[Pertenece a Otros]`

### 23. Dependientes — `card`

- **Values:** DISTINCTCOUNT(`Ferrada[RUN]`) — «Nº de personas»

### 24. Mapa de Georreferenciación — `esriVisual`

- **Color:** `Ferrada[Sector]`
- **Location:** `Ferrada[Dirección Completa]`
- **Tooltips:** `Ferrada[RUN]`
- **Tooltips:** `Ferrada[Nombre completo]`
- **Tooltips:** `Ferrada[Edad]` — «Edad1»
- **Tooltips:** `Ferrada[Sexo]`
- **Tooltips:** `Ferrada[PAD o cuidador?]` — «Es»

### 25. Población Cuidadores — `tableEx`

- **Values:** `Ferrada[Tipo de identificación]`
- **Values:** `Ferrada[RUN]` — «Número»
- **Values:** `Ferrada[Nombre Social]`
- **Values:** `Ferrada[Nombre completo]`
- **Values:** `Ferrada[Sexo]`
- **Values:** `Ferrada[Género]`
- **Values:** `Ferrada[Edad]` — «Años»
- **Values:** `Ferrada[Sector]`
- **Values:** `Ferrada[¿Originario o Migrante?]`
- **Values:** `Ferrada[Nacionalidad]`
- **Values:** `Ferrada[Pueblo Originario]`
- **Values:** `Ferrada[Dirección Completa]`
- **Values:** `Ferrada[Celular]`
- **Values:** `Ferrada[Mail]`
- **Values:** `Ferrada[Situación]`
- **Values:** `Ferrada[Estado]`
- **Values:** `Ferrada[Previsión]`
- **Values:** `Ferrada[GObj FLu 26]` — «¿Crónico?»
- **Values:** `Ferrada[PAD Cuidador (Zarit)]` — «Zarit (resultado)»
- **Values:** `Ferrada[Pertenece a ECICEP]` — «Pertenece ECICEP»
- **Values:** `Ferrada[Citar a PAP]`
- **Values:** `Ferrada[Citar a EMPA]`
- **Values:** `Ferrada[Citar a EMPAM]`

### 26. ¿PSM? — `slicer`

- **Values:** `Ferrada[SM Ingresado]`

### 27. ¿Respi? — `slicer`

- **Values:** `Ferrada[SALA Ingresado]` — «SALA Ingresado?»

### 28. ¿Demencia? — `slicer`

- **Values:** `Ferrada[SM Demencia]` — «Demencia»

### 29. Años — `slicer`

- **Values:** `Ferrada[Edad]` — «Edad Años»

### 30. Situación — `slicer`

- **Values:** `Ferrada[Situación]`

### 31. HTA — `slicer`

- **Values:** `Ferrada[PSCV HTA]` — «HTA»

### 32. Cuidadores — `card`

- **Values:** DISTINCTCOUNT(`Ferrada[RUN]`) — «Nº de personas»

### 33. Sexo — `slicer`

- **Values:** `Ferrada[Sexo]`

### 34. PAP — `slicer`

- **Values:** `Ferrada[Citar a PAP]`

### 35. EMPAM — `slicer`

- **Values:** `Ferrada[Citar a EMPAM]`

### 36. Promedio Enf — `card`

- **Values:** AVG(`Ferrada[Cuenta VDI seguimiento Enf 12m (act)]`) — «Promedio de Cuenta VDI seguimiento Enf 12m (act)»

### 37. ¿Activo 12m? — `slicer`

- **Values:** `Ferrada[¿Atendido en 12m?]` — «Atendido en 12m?»

### 38. Otros — `card`

- **Values:** AVG(`Ferrada[Cuenta VDI seguimiento 12m (act)]`) — «Promedio de Cuenta VDI seguimiento 12m (act)»

### 39. Preventivo Dependiente — `pieChart`

- **Category:** `Ferrada[Citar a Preventivo]`
- **Y:** COUNT(`Ferrada[Citar a Preventivo]`) — «Recuento de Citar a Preventivo»

---

## Anexo: lógica de los campos usados

### `Atenciones[FECHA ATENCION]`

_Campo base (no calculado): proviene de la carga de Power Query._

### `Atenciones[VDI (act)]`

Marcador 1/0: la actividad contiene «visita» y «domicilia» (visita domiciliaria integral).

```dax
IF(
    CONTAINSSTRING(Atenciones[ACTIVIDADES],"visita") &&
    CONTAINSSTRING(Atenciones[ACTIVIDADES],"domicilia"),
    1,0)
```

### `Ferrada[Barthel (Resultado)]`

Resultado de dependencia (Barthel): si figura en la planilla PAD devuelve «Dependiente + grado»; si no, usa la severidad del Barthel histórico. BLANK si no hay ninguno.

*Tipo:* string  ·  *calculatedColumn*

```dax
var _PAD = 
IF(
    LOOKUPVALUE('PAD Drive'[DEPENDENCIA],'PAD Drive'[RUN],Ferrada[RUN])="",BLANK(),
    LOOKUPVALUE('PAD Drive'[DEPENDENCIA],'PAD Drive'[RUN],Ferrada[RUN]))

VAR _Formulario = 
IF(
    LOOKUPVALUE('Barthel Histórico'[Severidad], 'Barthel Histórico'[RUN], 'Ferrada'[RUN])="",BLANK(),
    LOOKUPVALUE('Barthel Histórico'[Severidad], 'Barthel Histórico'[RUN], 'Ferrada'[RUN]))

RETURN

SWITCH(
    TRUE(),
    ISBLANK(_PAD) && ISBLANK(_Formulario),BLANK(),
    ISBLANK(_PAD),_Formulario,
    "Dependiente " & _PAD)
```

### `Ferrada[Barthel Fecha]`

Trae por cruce de RUN el valor de «Fecha Formulario» desde la tabla «Barthel Histórico» hacia esta tabla (LOOKUPVALUE). Copia directa, sin transformación.

```dax
LOOKUPVALUE('Barthel Histórico'[Fecha Formulario],'Barthel Histórico'[RUN],'Ferrada'[RUN])
```

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

### `Ferrada[Cuenta Condiciones Crónicas]`

Trae por cruce de RUN el valor de «Cantidad de Condiciones Crónicas» desde la tabla «Estratificacion» hacia esta tabla (LOOKUPVALUE). Copia directa, sin transformación.

```dax
LOOKUPVALUE(Estratificacion[Cantidad de Condiciones Crónicas],Estratificacion[RUN],'Ferrada'[RUN])
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

### `Ferrada[Cuenta VDI seguimiento Enf 12m (act)]`

Cuenta de visitas domiciliarias integrales de enfermería (excluyendo técnicos) en 12 meses cerrados, incluyendo visitas «primera», «segunda» y «tercera». Contexto: por protocolo, solo enfermería realiza primera y segunda visita; el resto de los profesionales registra únicamente tercera. (Corregido jul-2026: antes omitía la tercera.)

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
        (CONTAINSSTRING('Atenciones'[INSTRUMENTO],"enferme") && 
        NOT CONTAINSSTRING(Atenciones[INSTRUMENTO],"técnico") &&
        CONTAINSSTRING('Atenciones'[ACTIVIDADES],"visita domicilia")) && 
        (CONTAINSSTRING('Atenciones'[ACTIVIDADES],"primera") ||
        CONTAINSSTRING('Atenciones'[ACTIVIDADES],"segunda") ||
        CONTAINSSTRING('Atenciones'[ACTIVIDADES],"tercera"))
    )
)

RETURN

IF(
    ISBLANK(_Resultado),0,_Resultado)
```

### `Ferrada[Cuenta VDI seguimiento Kine 12m (act)]`

Cuenta de visitas domiciliarias integrales de seguimiento («tercera» visita) realizadas por kinesiólogo/a (excluyendo técnicos) en la ventana de 12 meses cerrados (desde 13 meses atrás hasta el último día del mes anterior). Devuelve 0 si no hay.

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
        (CONTAINSSTRING('Atenciones'[INSTRUMENTO],"kinesi") && 
        NOT CONTAINSSTRING(Atenciones[INSTRUMENTO],"técnic") &&
        CONTAINSSTRING('Atenciones'[ACTIVIDADES],"visita domicilia") && 
        CONTAINSSTRING('Atenciones'[ACTIVIDADES],"tercera"))
    )
)

RETURN

IF(
    ISBLANK(_Resultado),0,_Resultado)
```

### `Ferrada[Cuenta VDI seguimiento Med 12m (act)]`

Cuenta de visitas domiciliarias integrales de seguimiento («tercera» visita) realizadas por médico/a (excluyendo técnicos) en la ventana de 12 meses cerrados (desde 13 meses atrás hasta el último día del mes anterior). Devuelve 0 si no hay.

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
        (CONTAINSSTRING('Atenciones'[INSTRUMENTO],"médic") && 
        NOT CONTAINSSTRING(Atenciones[INSTRUMENTO],"técnic") &&
        CONTAINSSTRING('Atenciones'[ACTIVIDADES],"visita domicilia") && 
        CONTAINSSTRING('Atenciones'[ACTIVIDADES],"tercera"))
    )
)

RETURN

IF(
    ISBLANK(_Resultado),0,_Resultado)
```

### `Ferrada[Cuenta VDI seguimiento Nutri 12m (act)]`

Cuenta de visitas domiciliarias integrales de seguimiento («tercera» visita) realizadas por nutricionista (excluyendo técnicos) en la ventana de 12 meses cerrados (desde 13 meses atrás hasta el último día del mes anterior). Devuelve 0 si no hay.

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
        (CONTAINSSTRING('Atenciones'[INSTRUMENTO],"nutrici") && 
        NOT CONTAINSSTRING(Atenciones[INSTRUMENTO],"técnic") &&
        CONTAINSSTRING('Atenciones'[ACTIVIDADES],"visita domicilia") && 
        CONTAINSSTRING('Atenciones'[ACTIVIDADES],"tercera"))
    )
)

RETURN

IF(
    ISBLANK(_Resultado),0,_Resultado)
```

### `Ferrada[Cuenta VDI seguimiento Nutri NED 12m (act)]`

Cuenta de visitas domiciliarias de nutricionista a personas con NED (necesidades especiales de alimentación), visita «tercera», en 12 meses cerrados.

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
        (CONTAINSSTRING('Atenciones'[INSTRUMENTO],"nutrici") && 
        CONTAINSSTRING('Atenciones'[ACTIVIDADES],"personas con ned") && 
        CONTAINSSTRING('Atenciones'[ACTIVIDADES],"visita domici") &&
        CONTAINSSTRING('Atenciones'[ACTIVIDADES],"tercera"))
    )
)

RETURN

IF(
    ISBLANK(_Resultado),0,_Resultado)
```

### `Ferrada[Cuenta VDI seguimiento Odonto 12m (act)]`

Cuenta de visitas domiciliarias integrales de seguimiento («tercera» visita) realizadas por odontólogo/a (excluyendo técnicos) en la ventana de 12 meses cerrados (desde 13 meses atrás hasta el último día del mes anterior). Devuelve 0 si no hay.

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
        (CONTAINSSTRING('Atenciones'[INSTRUMENTO],"odont") && 
        NOT CONTAINSSTRING(Atenciones[INSTRUMENTO],"técnic") &&
        CONTAINSSTRING('Atenciones'[ACTIVIDADES],"visita domicilia") && 
        CONTAINSSTRING('Atenciones'[ACTIVIDADES],"tercera"))
    )
)

RETURN

IF(
    ISBLANK(_Resultado),0,_Resultado)
```

### `Ferrada[Cuenta VDI seguimiento TENS 12m (act)]`

Cuenta de visitas domiciliarias integrales de seguimiento («tercera») realizadas por TENS en la ventana de 12 meses cerrados. Devuelve 0 si no hay.

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
        (CONTAINSSTRING('Atenciones'[INSTRUMENTO],"técnico") && 
        CONTAINSSTRING('Atenciones'[ACTIVIDADES],"visita domicilia") && 
        CONTAINSSTRING('Atenciones'[ACTIVIDADES],"tercera"))
    )
)

RETURN

IF(
    ISBLANK(_Resultado),0,_Resultado)
```

### `Ferrada[Cuenta VDI seguimiento TO 12m (act)]`

Cuenta de visitas domiciliarias integrales de seguimiento («tercera») realizadas por terapeuta ocupacional en la ventana de 12 meses cerrados. Devuelve 0 si no hay.

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
        (CONTAINSSTRING('Atenciones'[INSTRUMENTO],"ocupacional") && 
        CONTAINSSTRING('Atenciones'[ACTIVIDADES],"visita domicilia") && 
        CONTAINSSTRING('Atenciones'[ACTIVIDADES],"tercera"))
    )
)

RETURN

IF(
    ISBLANK(_Resultado),0,_Resultado)
```

### `Ferrada[Cuenta VDI seguimiento TS 12m (act)]`

Cuenta de visitas domiciliarias integrales de seguimiento («tercera») realizadas por trabajador(a) social en la ventana de 12 meses cerrados. Devuelve 0 si no hay.

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
        (CONTAINSSTRING('Atenciones'[INSTRUMENTO],"trabajador(a) social") && 
        CONTAINSSTRING('Atenciones'[ACTIVIDADES],"visita domicilia") && 
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

### `Ferrada[Estado]`

Trae por cruce de RUN el valor de «ESTADO» desde la tabla «Inscritos» hacia esta tabla (LOOKUPVALUE). Copia directa, sin transformación.

```dax
LOOKUPVALUE(Inscritos[ESTADO],Inscritos[RUN],'Ferrada'[RUN])
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

### `Ferrada[PAD CPU]`

Indicador SI/NO desde la planilla PAD (Drive): el campo «Paliativo NO oncologico» contiene «sí» para su RUN.

```dax
IF(
    CALCULATE(COUNT('PAD Drive'[RUN]),
    FILTER('PAD Drive',
    'PAD Drive'[RUN] = 'Ferrada'[RUN] &&
    CONTAINSSTRING('PAD Drive'[Paliativo NO oncologico],"si"))),
    "SI","NO")
```

### `Ferrada[PAD Cuidador (Zarit)]`

Resultado Zarit del cuidador (sobrecarga) tomado de la planilla PAD Drive, cruzando por RUN de cuidador. BLANK si no hay.

```dax
var _Resultado = 
TOPN(1,
    CALCULATETABLE(VALUES('PAD Drive'[ZARIT ]),
        FILTER(
            'PAD Drive',
            'PAD Drive'[RUN Cuidador] = 'Ferrada'[RUN])),
            'PAD Drive'[ZARIT ],DESC)

RETURN

IF(
    _Resultado = "",BLANK(),
    _Resultado)
```

### `Ferrada[PAD Onco?]`

Indicador SI/NO desde la planilla PAD (Drive): el campo «Paliativo oncologico» contiene «sí» para su RUN.

```dax
IF(
    CALCULATE(COUNT('PAD Drive'[RUN]),
    FILTER('PAD Drive',
    'PAD Drive'[RUN] = 'Ferrada'[RUN] &&
    CONTAINSSTRING('PAD Drive'[Paliativo oncologico],"si"))),
    "SI","NO")
```

### `Ferrada[PAD VDI Seguimiento Enf útima (fecha)]`

Fecha de la última visita domiciliaria de enfermería (visita «primera» o «segunda», excluyendo técnicos) — seguimiento PAD.

```dax
LASTDATE(CALCULATETABLE(VALUES('Atenciones'[FECHA ATENCION].[Date]),
FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
(CONTAINSSTRING('Atenciones'[INSTRUMENTO],"enferme") && 
NOT CONTAINSSTRING(Atenciones[INSTRUMENTO],"técnico") &&
CONTAINSSTRING('Atenciones'[ACTIVIDADES],"domicilia")) && 
(CONTAINSSTRING('Atenciones'[ACTIVIDADES],"primera") ||
CONTAINSSTRING('Atenciones'[ACTIVIDADES],"segunda")))))
```

### `Ferrada[PAD o cuidador?]`

Rol en PAD: «Dependiente» si pertenece al programa, «Cuidador» si es cuidador; BLANK si ninguno.

```dax
SWITCH(
    TRUE(),
    Ferrada[Pertenece a PAD]="SI","Dependiente",
    Ferrada[PAD Es cuidador?]="SI","Cuidador",
    BLANK())
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

### `Ferrada[Receta vigencia (mes)]`

Fecha de vigencia más lejana entre las recetas vigentes del paciente (hasta cuándo tiene receta).

```dax
LASTDATE(
CALCULATETABLE(VALUES('Recetas Vigentes'[FECHA VIGENCIA].[Date]),
FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN])))
```

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

### `Ferrada[SALA Asistencia Ventilatoria]`

Asistencia ventilatoria SI/NO: último formulario «Otros y Respi» con pregunta 26 («¿necesita asistencia ventilatoria?») marcada «sí», tipo registrado y estado ingreso/seguimiento.

```dax
var _Fecha = 
LASTDATE(
    CALCULATETABLE(VALUES('Otros y Respi'[FECHA ATENCION]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Otros y Respi'[26.- ¿NECESITA ASISTENCIA VENTILATORIA?],"si")) &&
    'Otros y Respi'[27.- ASISTENCIA VENTILATORIA]<>"" &&
    (CONTAINSSTRING('Otros y Respi'[28.- ESTADO ASISTENCIA VENTILATORIA],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[28.- ESTADO ASISTENCIA VENTILATORIA],"seguimiento")))))

var _Formularios = 
IF(
CALCULATE(COUNT('Otros y Respi'[RUN]),
FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
'Otros y Respi'[FECHA ATENCION] = _Fecha &&
(CONTAINSSTRING('Otros y Respi'[26.- ¿NECESITA ASISTENCIA VENTILATORIA?],"si")) &&
'Otros y Respi'[27.- ASISTENCIA VENTILATORIA]<>"" &&
(CONTAINSSTRING('Otros y Respi'[28.- ESTADO ASISTENCIA VENTILATORIA],"ingreso") ||
CONTAINSSTRING('Otros y Respi'[28.- ESTADO ASISTENCIA VENTILATORIA],"seguimiento")))),
"SI","NO")


RETURN
IF(
    _Formularios="SI",
"SI","NO")
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

### `Ferrada[SM Demencia]`

Indicador SI/NO de diagnóstico: (a) alguna atención con diagnóstico que contenga alguno de «F01» o «F02» o «F03» o «F04», o (b) último formulario PSM médico con «44.- ¿ TIENE ALZHEIMER Y/O OTRAS DEMENCIAS ?»=«sí» en ingreso/seguimiento.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"F01") ||
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"F02") ||
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"F03") ||
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"F04")))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[44.- ¿ TIENE ALZHEIMER Y/O OTRAS DEMENCIAS ?],"si")) &&
    (CONTAINSSTRING(PSM[46.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[46.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[44.- ¿ TIENE ALZHEIMER Y/O OTRAS DEMENCIAS ?],"si")) &&
    (CONTAINSSTRING(PSM[46.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[46.- ESTADO],"seguimien")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
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
