# Especificación de la página «Preventivos»

Extraído automáticamente de la capa de reporte (PBIR) y del modelo semántico (TMDL).

**28 visuales · 28 campos distintos del modelo.**

_Sin filtros a nivel de página._

## Visuales

### 1. CLAP — `pieChart`

- **Category:** `Ferrada[Citar a CLAP]`
- **Y:** COUNT(`Ferrada[Citar a CLAP]`) — «Recuento de Citar a CLAP»

### 2. Situación — `slicer`

- **Values:** `Ferrada[Situación]`

### 3. Meses — `slicer`

- **Values:** `Ferrada[Meses]` — «Edad Meses»

### 4. Validado — `slicer`

- **Values:** `Ferrada[Validado]`

### 5. 1º EMPA (próximo mes) — `tableEx`

- **Values:** `Ferrada[RUN]`
- **Values:** `Ferrada[Nombre Social]`
- **Values:** `Ferrada[Nombre completo]`
- **Values:** `Ferrada[Sexo]`
- **Values:** `Ferrada[Edad]` — «Años»
- **Values:** `Ferrada[Fecha Nacimiento]`
- **Values:** `Ferrada[Sector]`
- **Values:** `Ferrada[¿Originario o Migrante?]`
- **Values:** `Ferrada[Dirección Completa]`
- **Values:** `Ferrada[Celular]` — «Celular Inscripción»
- **Values:** `Ferrada[Mail]`

### 6. 1º PAP (próximo mes) — `tableEx`

- **Values:** `Ferrada[RUN]`
- **Values:** `Ferrada[Nombre Social]`
- **Values:** `Ferrada[Nombre completo]`
- **Values:** `Ferrada[Sexo]`
- **Values:** `Ferrada[Edad]` — «Años»
- **Values:** `Ferrada[Fecha Nacimiento]`
- **Values:** `Ferrada[Sector]`
- **Values:** `Ferrada[¿Originario o Migrante?]`
- **Values:** `Ferrada[Dirección Completa]`
- **Values:** `Ferrada[Celular]` — «Celular Inscripción»
- **Values:** `Ferrada[Mail]`

### 7. EMPAM — `pieChart`

- **Category:** `Ferrada[Citar a EMPAM]`
- **Y:** COUNT(`Ferrada[Citar a EMPAM]`) — «Recuento de Citar a EMPAM»

### 8. EMPA — `slicer`

- **Values:** `Ferrada[Citar a EMPA]`

### 9. Años — `slicer`

- **Values:** `Ferrada[Edad]` — «Edad Años»

### 10. Número de preventivos realizados por mes en los últimos 12 meses — `clusteredColumnChart`

- **Category:** `?[Año]` — «FECHA ATENCION Año»
- **Category:** `?[Mes]` — «FECHA ATENCION Mes»
- **Series:** `Atenciones[Preventivo]`
- **Tooltips:** MIN(`Atenciones[FECHA ATENCION]`) — «Primera fecha: FECHA ATENCION»
- **Tooltips:** MIN(`Atenciones[AÑOS ATENCION]`) — «Mín. de AÑOS ATENCION»
- **Y:** COUNT(`Atenciones[Preventivo]`) — «Recuento de Preventivo»

### 11. EMPA — `pieChart`

- **Category:** `Ferrada[Citar a EMPA]`
- **Y:** COUNT(`Ferrada[Citar a EMPA]`) — «Recuento de Citar a EMPA»

### 12. Embarazada — `slicer`

- **Values:** `Ferrada[¿Embarazada?]`

### 13. Runificado Preventivo — `tableEx`

- **Values:** `Ferrada[RUN]`
- **Values:** `Ferrada[Nombre Social]`
- **Values:** `Ferrada[Nombre completo]`
- **Values:** `Ferrada[Sexo]`
- **Values:** `Ferrada[Edad]`
- **Values:** `Ferrada[Fecha Nacimiento]`
- **Values:** `Ferrada[Sector]`
- **Values:** `Ferrada[¿Originario o Migrante?]`
- **Values:** `Ferrada[Dirección Completa]`
- **Values:** `Ferrada[Celular]`
- **Values:** `Ferrada[Mail]`
- **Values:** `Ferrada[Citar a Preventivo]`
- **Values:** `Ferrada[Última Atención (fecha)]`

### 14. EMPAM — `slicer`

- **Values:** `Ferrada[Citar a EMPAM]`

### 15. ¿Activo 1m? — `slicer`

- **Values:** `Ferrada[¿Atendido 1 mes?]`

### 16. Estado — `slicer`

- **Values:** `Ferrada[Estado]`

### 17. ¿Activo 12m? — `slicer`

- **Values:** `Ferrada[¿Atendido en 12m?]` — «Atendido en 12m?»

### 18. CLAP — `slicer`

- **Values:** `Ferrada[Citar a CLAP]`

### 19. PAP — `slicer`

- **Values:** `Ferrada[Citar a PAP]`

### 20. Sexo — `slicer`

- **Values:** `Ferrada[Sexo]`

### 21. Días — `slicer`

- **Values:** `Ferrada[Días]`

### 22. 1º EMPAM (próximo mes) — `tableEx`

- **Values:** `Ferrada[RUN]`
- **Values:** `Ferrada[Nombre Social]`
- **Values:** `Ferrada[Nombre completo]`
- **Values:** `Ferrada[Sexo]`
- **Values:** `Ferrada[Edad]` — «Años»
- **Values:** `Ferrada[Fecha Nacimiento]`
- **Values:** `Ferrada[Sector]`
- **Values:** `Ferrada[¿Originario o Migrante?]`
- **Values:** `Ferrada[Dirección Completa]`
- **Values:** `Ferrada[Celular]` — «Celular Inscripción»
- **Values:** `Ferrada[Mail]`

### 23. Sector — `slicer`

- **Values:** `Ferrada[Sector]`

### 24. Migr o Origin — `slicer`

- **Values:** `Ferrada[¿Originario o Migrante?]`

### 25. Total de personas — `card`

- **Values:** DISTINCTCOUNT(`Ferrada[RUN]`) — «Nº de personas»

### 26. Mapa de Georreferenciación — `esriVisual`

- **Color:** `Ferrada[Dirección Completa]`
- **Location:** `Ferrada[Edad]` — «Edad1»
- **Time:** `Ferrada[Sector]`

### 27. PAP — `pieChart`

- **Category:** `Ferrada[Citar a PAP]`
- **Y:** COUNT(`Ferrada[Citar a PAP]`) — «Recuento de Citar a PAP»

### 28. 1º CLAP (próximo mes) — `tableEx`

- **Values:** `Ferrada[RUN]`
- **Values:** `Ferrada[Nombre Social]`
- **Values:** `Ferrada[Nombre completo]`
- **Values:** `Ferrada[Sexo]`
- **Values:** `Ferrada[Edad]` — «Años»
- **Values:** `Ferrada[Fecha Nacimiento]`
- **Values:** `Ferrada[Sector]`
- **Values:** `Ferrada[¿Originario o Migrante?]`
- **Values:** `Ferrada[Dirección Completa]`
- **Values:** `Ferrada[Celular]` — «Celular Inscripción»
- **Values:** `Ferrada[Mail]`

---

## Anexo: lógica de los campos usados

### `Atenciones[AÑOS ATENCION]`

_Campo base (no calculado): proviene de la carga de Power Query._

### `Atenciones[FECHA ATENCION]`

_Campo base (no calculado): proviene de la carga de Power Query._

### `Atenciones[Preventivo]`

Etiqueta la atención preventiva según edad y registro: EMPA (20-64 años, formulario «emp -»), EMPAM (≥65, formulario «emp -»), CLAP (10-19, formulario «clap modi»), PAP (mujeres 25-64 por actividad «examen pap» o dx z12.4). Si aplica más de una, las concatena con « | »; si ninguna, BLANK.

```dax
VAR _EMPA =
    IF(
        Atenciones[AÑOS ATENCION] >= 20 &&
        Atenciones[AÑOS ATENCION] < 65 &&
        CONTAINSSTRING(Atenciones[FORMULARIOS CLINICOS], "emp -"),
        "EMPA"
    )

VAR _EMPAM =
    IF(
        Atenciones[AÑOS ATENCION] >= 65 &&
        CONTAINSSTRING(Atenciones[FORMULARIOS CLINICOS], "emp -"),
        "EMPAM"
    )

VAR _CLAP =
    IF(
        Atenciones[AÑOS ATENCION] >= 10 &&
        Atenciones[AÑOS ATENCION] < 20 &&
        CONTAINSSTRING(Atenciones[FORMULARIOS CLINICOS], "clap modi"),
        "CLAP"
    )

VAR _PAP = 
    IF(
        Atenciones[AÑOS ATENCION] >= 25 &&
        Atenciones[AÑOS ATENCION] < 65 &&
        (CONTAINSSTRING(Atenciones[ACTIVIDADES], "examen pap") ||
        CONTAINSSTRING(Atenciones[DIAGNOSTICOS], "z12.4")),
        "PAP")

VAR Lista =
    FILTER(
        {
            ( _EMPA ),
            ( _EMPAM ),
            ( _CLAP ),
            ( _PAP )
        },
        NOT ISBLANK([Value])
    )

VAR Resultado =
    IF(
        COUNTROWS(Lista) = 0,
        BLANK(),
        CONCATENATEX(Lista, [Value], " | ")
    )

RETURN
Resultado
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

### `Ferrada[Última Atención (fecha)]`

Fecha de la última atención registrada del paciente (cualquier tipo).

*Tipo:* dateTime  ·  *calculatedColumn*

```dax
LASTDATE(
    CALCULATETABLE(VALUES(Atenciones[FECHA ATENCION]),
    FILTER(ALL(Atenciones),Atenciones[RUN]='Ferrada'[RUN])))
```
