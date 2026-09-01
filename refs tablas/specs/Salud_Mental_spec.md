# Especificación de la página «Salud Mental»

Extraído automáticamente de la capa de reporte (PBIR) y del modelo semántico (TMDL).

**31 visuales · 153 campos distintos del modelo.**

## Filtros de página

- `Ferrada[Pertenece a PSM]` (Categorical) → ['SI']

## Visuales

### 1. Género — `slicer`

- **Values:** `Ferrada[Género]`

### 2. Adaptativo — `slicer`

- **Values:** `Ferrada[SM Adaptativo]`

### 3. OH y Drogas — `slicer`

- **Values:** `Ferrada[SM OH y Drogas]`

### 4. Total de personas — `card`

- **Values:** DISTINCTCOUNT(`Ferrada[RUN]`) — «Nº de personas»

### 5. Tipo de Ansiedad — `slicer`

- **Values:** `Ferrada[SM Ansiedad tipo (form)]`

### 6. Grado de Demencia — `slicer`

- **Values:** `Ferrada[SM Demencia Gravedad (form)]`

### 7. ¿Activo SM? — `slicer`

- **Values:** `Ferrada[SM Activo 12m]`

### 8. ¿Quien es? — `slicer`

- **Values:** `Ferrada[SM Violencia Victima o Agresor (form)]`

### 9. Autismo — `slicer`

- **Values:** `Ferrada[SM Autismo]`

### 10. Años — `slicer`

- **Values:** `Ferrada[Edad]`

### 11. Oposicionista — `slicer`

- **Values:** `Ferrada[SM Oposicionista desafiante]`

### 12. Depresión — `slicer`

- **Values:** `Ferrada[SM Depresión]`

### 13. Estado — `slicer`

- **Values:** `Ferrada[Estado]`

### 14. TDAH — `slicer`

- **Values:** `Ferrada[SM TDAH]`

### 15. Tipo de Violencia — `slicer`

- **Values:** `Ferrada[SM Violencia Tipo (form)]`

### 16. ¿Ingresado? — `slicer`

- **Values:** `Ferrada[SM Ingresado]`

### 17. Población PSM — `tableEx`

- **Values:** `Ferrada[Tipo de identificación]`
- **Values:** `Ferrada[RUN]` — «Número»
- **Values:** `Ferrada[Nombre Social]`
- **Values:** `Ferrada[Nombre completo]`
- **Values:** `Ferrada[Sexo]`
- **Values:** `Ferrada[Género]`
- **Values:** `Ferrada[Fecha Nacimiento]`
- **Values:** `Ferrada[Edad]`
- **Values:** `Ferrada[Sector]`
- **Values:** `Ferrada[Situación]`
- **Values:** `Ferrada[Estado]`
- **Values:** `Ferrada[Motivo Pasivación]`
- **Values:** `Ferrada[Fecha Pasivación]`
- **Values:** `Ferrada[¿Originario o Migrante?]`
- **Values:** `Ferrada[Nacionalidad]`
- **Values:** `Ferrada[Pueblo Originario]`
- **Values:** `Ferrada[PROTECCION NIÑEZ]` — «SENAME»
- **Values:** `Ferrada[Dirección Completa]`
- **Values:** `Ferrada[Celular]`
- **Values:** `Ferrada[Mail]`
- **Values:** `Ferrada[Pertenece a PSM]` — «¿Pertenece?»
- **Values:** `Ferrada[SM Ingresado]` — «¿Ingresado?»
- **Values:** `Ferrada[SM Activo 12m]` — «¿Activo 12m?»
- **Values:** `Ferrada[SM Atendido hace 6m]` — «¿Última atención hace 6m?»
- **Values:** `Ferrada[SM Atendido hace 13m]` — «¿Última atención hace 13m?»
- **Values:** `Ferrada[SM Receta?]` — «¿Receta Vigente?»
- **Values:** `Ferrada[¿Embarazada?]`
- **Values:** `Ferrada[SM Madre <5 años]` — «Madre <5 años»
- **Values:** `Ferrada[PAD Es cuidador?]` — «¿Cuidador?»
- **Values:** `Ferrada[SM Pauta llenada]` — «Pauta llenada (12m)»
- **Values:** `Ferrada[SM Fecha último formulario]` — «Fecha último formulario»
- **Values:** `Ferrada[SM Violencia]` — «Violencia»
- **Values:** `Ferrada[SM Violencia (form)]` — «Violencia (form)»
- **Values:** `Ferrada[SM Violencia Tipo (form)]` — «Violencia Tipo (form)»
- **Values:** `Ferrada[SM Violencia Victima o Agresor (form)]` — «Violencia Victima o Agresor (form)»
- **Values:** `Ferrada[SM Violencia (fecha)]` — «Violencia (fecha)»
- **Values:** `Ferrada[SM Abuso sexual]` — «Abuso Sexual»
- **Values:** `Ferrada[SM Abuso Sexual (form)]` — «Abuso Sexual (form)»
- **Values:** `Ferrada[SM Abuso Sexual (fecha)]` — «Abuso Sexual (fecha)»
- **Values:** `Ferrada[SM Suicidio (form)]` — «Suicidio (form)»
- **Values:** `Ferrada[SM Suicidio Tipo (form)]` — «Suicidio Tipo (form)»
- **Values:** `Ferrada[SM Suicidio (fecha)]` — «Suicidio (fecha)»
- **Values:** `Ferrada[SM Depresión]` — «Depresión»
- **Values:** `Ferrada[SM Depresión (form)]` — «Depresión (form)»
- **Values:** `Ferrada[SM Depresión (fecha)]` — «Depresión (fecha)»
- **Values:** `Ferrada[SM Depresión Gravedad (form)]` — «Depresión gravedad (form)»
- **Values:** `Ferrada[SM Depresión Leve]` — «Depresión Leve»
- **Values:** `Ferrada[SM Depresión Moderada]` — «Depresión Moderada»
- **Values:** `Ferrada[SM Depresión Grave]` — «Depresión Grave»
- **Values:** `Ferrada[SM OH y Drogas]` — «OH y Drogas»
- **Values:** `Ferrada[SM OH Dependiente (form)]` — «OH Dependiente (form)»
- **Values:** `Ferrada[SM OH Dependiente (fecha)]` — «OH Dependiente (fecha)»
- **Values:** `Ferrada[SM OH Perjudical (form)]` — «OH Perjudicial (form)»
- **Values:** `Ferrada[SM OH Perjudicial (fecha)]` — «OH Perjudicial (fecha)»
- **Values:** `Ferrada[SM Drogas Dependiente (form)]` — «Drogas Dependiente (form)»
- **Values:** `Ferrada[SM Drogas Dependiente (fecha)]` — «Drogas Dependiente (fecha)»
- **Values:** `Ferrada[SM Drogas Perjudical (form)]` — «Drogas Perjudicial (form)»
- **Values:** `Ferrada[SM Drogas perjudicial (fecha)]` — «Drogas Perjudicial (fecha)»
- **Values:** `Ferrada[SM OH y Drogas (form)]` — «OH y Drogas (form)»
- **Values:** `Ferrada[SM OH y Drogas (fecha)]` — «OH y Drogas (fecha)»
- **Values:** `Ferrada[SM Ansiedad separación]` — «Ansiedad separación»
- **Values:** `Ferrada[SM Ansiedad separación (form)]` — «Ansiedad separación (form)»
- **Values:** `Ferrada[SM Ansiedad separación (fecha)]` — «Ansiedad separación (fecha)»
- **Values:** `Ferrada[SM Otras Infancia/Adolescencia]` — «Otras Infancia/Adolescencia»
- **Values:** `Ferrada[SM Otras Infancia/Adolescencia (form)]` — «Otras Infancia/Adolescencia (form)»
- **Values:** `Ferrada[SM Otras Infancia/Adolescencia (fecha)]` — «Otras Infancia/Adolescencia (fecha)»
- **Values:** `Ferrada[SM Ansiedad]` — «Ansiedad»
- **Values:** `Ferrada[SM Ansiedad (form)]` — «Ansiedad (form)»
- **Values:** `Ferrada[SM Ansiedad (fecha)]` — «Ansiedad (fecha)»
- **Values:** `Ferrada[SM Ansiedad tipo (form)]` — «Ansiedad (tipo)»
- **Values:** `Ferrada[SM Ansiedad TEPT]` — «Ansiedad TEPT»
- **Values:** `Ferrada[SM Ansiedad Pánico]` — «Ansiedad Pánico»
- **Values:** `Ferrada[SM Ansiedad TAG]` — «Ansiedad TAG»
- **Values:** `Ferrada[SM Ansiedad Otras]` — «Ansiedad Otras»
- **Values:** `Ferrada[SM Demencia]` — «Demencia»
- **Values:** `Ferrada[SM Demencia (form)]` — «Demencia (form)»
- **Values:** `Ferrada[SM Demencia (fecha)]` — «Demencia (fecha)»
- **Values:** `Ferrada[SM Demencia Gravedad (form)]` — «Demencia gravedad (form)»
- **Values:** `Ferrada[SM Demencia Leve]` — «Demencia Leve»
- **Values:** `Ferrada[SM Demencia Moderado]` — «Demencia Moderado»
- **Values:** `Ferrada[SM Demencia Avanzado]` — «Demencia Avanzado»
- **Values:** `Ferrada[SM Esquizofrenia]` — «Esquizofrenia»
- **Values:** `Ferrada[SM Esquizofrenia (form)]` — «Esquizofrenia (form)»
- **Values:** `Ferrada[SM Esquizofrenia (fecha)]` — «Esquizofrenia (fecha)»
- **Values:** `Ferrada[SM Depresión Postparto]` — «Depresión Postparto»
- **Values:** `Ferrada[SM Depresión Postparto (form)]` — «Depresión Postparto (form)»
- **Values:** `Ferrada[SM Depresión Postparto (fecha)]` — «Depresión Postparto (fecha)»
- **Values:** `Ferrada[SM Bipolaridad]` — «Bipolaridad (dg)»
- **Values:** `Ferrada[SM Bipolaridad (form)]` — «Bipolaridad (form)»
- **Values:** `Ferrada[SM Bipolaridad (fecha)]` — «Bipolaridad (fecha)»
- **Values:** `Ferrada[SM TDAH]` — «TDAH»
- **Values:** `Ferrada[SM TDAH (form)]` — «TDAH (form)»
- **Values:** `Ferrada[SM TDAH (fecha)]` — «TDAH (fecha)»
- **Values:** `Ferrada[SM Oposicionista desafiante]` — «Oposicionista desafiante»
- **Values:** `Ferrada[SM Oposicionista desafiante (form)]` — «Oposicionista desafiante (form)»
- **Values:** `Ferrada[SM Oposicionista desafiante (fecha)]` — «Oposicionista desafiante (fecha)»
- **Values:** `Ferrada[SM Adaptativo]` — «Adaptativo»
- **Values:** `Ferrada[SM Adaptativo (form)]` — «Adaptativo (form)»
- **Values:** `Ferrada[SM Adaptativo (fecha)]` — «Adaptativo (fecha)»
- **Values:** `Ferrada[SM Personalidad]` — «Personalidad»
- **Values:** `Ferrada[SM Personalidad (form)]` — «Personalidad (form)»
- **Values:** `Ferrada[SM Personalidad (fecha)]` — «Personalidad (fecha)»
- **Values:** `Ferrada[SM Asperger]` — «Asperger»
- **Values:** `Ferrada[SM Asperger (form)]` — «Asperger (form)»
- **Values:** `Ferrada[SM Asperger (fecha)]` — «Asperger (fecha)»
- **Values:** `Ferrada[SM Otras (form)]` — «Otros (form)»
- **Values:** `Ferrada[SM Otras (fecha)]` — «Otras (fecha)»
- **Values:** `Ferrada[SM Rett]` — «Rett»
- **Values:** `Ferrada[SM Rett (form)]` — «Rett (form)»
- **Values:** `Ferrada[SM Rett (fecha)]` — «Rett (fecha)»
- **Values:** `Ferrada[SM Conducta Alimentaria]` — «Conducta Alimentaria»
- **Values:** `Ferrada[SM Conducta Alimentaria (form)]` — «Conducta Alimentaria (form)»
- **Values:** `Ferrada[SM Conducta Alimentaria (fecha)]` — «Conducta Alimentaria (fecha)»
- **Values:** `Ferrada[SM Retraso Mental]` — «Retraso Mental (dg)»
- **Values:** `Ferrada[SM Retraso Mental (form)]` — «Retraso Mental (form)»
- **Values:** `Ferrada[SM Retraso Mental (fecha)]` — «Retraso Mental (fecha)»
- **Values:** `Ferrada[SM Autismo]` — «Autismo»
- **Values:** `Ferrada[SM Autismo (form)]` — «Autismo (form)»
- **Values:** `Ferrada[SM Autismo (fecha)]` — «Autismo (fecha)»
- **Values:** `Ferrada[SM Desintegrativo niñez]` — «Desintegrativo niñez (mixto)»
- **Values:** `Ferrada[SM Desintegrativo niñez (form)]` — «Desintegrativo niñez (form)»
- **Values:** `Ferrada[SM Desintegrativo niñez (fecha)]` — «Desintegrativo niñez (fecha)»
- **Values:** `Ferrada[SM TGD]` — «TGD (mixto)»
- **Values:** `Ferrada[SM TGD (form)]` — «TGD (form)»
- **Values:** `Ferrada[SM TGD (fecha)]` — «TGD (fecha)»
- **Values:** `Ferrada[Fibromialgia]`
- **Values:** `Ferrada[SM Sertralina]` — «Sertralina»
- **Values:** `Ferrada[Escitalopram]`
- **Values:** `Ferrada[SM Fluoxetina]` — «Fluoxetina»
- **Values:** `Ferrada[SM Paroxetina]` — «Paroxetina»
- **Values:** `Ferrada[SM Venlafaxina]` — «Venlafaxina»
- **Values:** `Ferrada[SM Mirtazapina]` — «Mirtazapina»
- **Values:** `Ferrada[Trazodona]`
- **Values:** `Ferrada[SM Amitriptilina]` — «Amitriptilina»
- **Values:** `Ferrada[SM Clorpromazina]` — «Clorpromazina»
- **Values:** `Ferrada[Quetiapina]`
- **Values:** `Ferrada[Zopiclona]`
- **Values:** `Ferrada[SM Alprazolam]` — «Alprazolam»
- **Values:** `Ferrada[SM Clonazepam]` — «Clonazepam»
- **Values:** `Ferrada[Diazepam]`
- **Values:** `Ferrada[SM Metilfenidato]` — «Metilfenidato»
- **Values:** `Ferrada[Pregabalina]`
- **Values:** `Ferrada[SM Bupropion (Ext)]` — «Bupropion (Ext)»
- **Values:** `Ferrada[Duloxetina (Ext)]`
- **Values:** `Ferrada[Trazodona (Ext)]`
- **Values:** `Ferrada[Quetiapina (Ext)]`
- **Values:** `Ferrada[SM Melatonina (Ext)]` — «Melatonina (Ext)»
- **Values:** `Ferrada[SM último control (fecha)]` — «Último control (fecha)»
- **Values:** `Ferrada[SM último control (instrumento)]` — «Último control (instrumento)»
- **Values:** `Ferrada[SM Ansiedad Fobia]`
- **Values:** SUM(`Ferrada[Trans]`) — «Suma de Trans»

### 18. Sexo — `slicer`

- **Values:** `Ferrada[Sexo]`

### 19. Violencia — `slicer`

- **Values:** `Ferrada[SM Violencia]`

### 20. Número de controles y consultas (por actividad) por mes en los últimos 12 meses — `clusteredColumnChart`

- **Category:** `?[Año]` — «FECHA ATENCION Año»
- **Category:** `?[Mes]` — «FECHA ATENCION Mes»
- **Series:** `Atenciones[PSM (act)]`
- **Tooltips:** MIN(`Atenciones[FECHA ATENCION]`) — «Primera fecha: FECHA ATENCION»
- **Y:** COUNT(`Atenciones[PSM (act)]`) — «Recuento de PSM (act)»

### 21. Personalidad — `slicer`

- **Values:** `Ferrada[SM Personalidad]`

### 22. Depresión PP — `slicer`

- **Values:** `Ferrada[SM Depresión Postparto]`

### 23. Demencia — `slicer`

- **Values:** `Ferrada[SM Demencia]`

### 24. Situación — `slicer`

- **Values:** `Ferrada[Situación]`

### 25. Cond Alimen — `slicer`

- **Values:** `Ferrada[SM Conducta Alimentaria]`

### 26. Abuso Sexual — `slicer`

- **Values:** `Ferrada[SM Abuso sexual]`

### 27. Grado de Depresión — `slicer`

- **Values:** `Ferrada[SM Depresión Gravedad (form)]`

### 28. Bipolar — `slicer`

- **Values:** `Ferrada[SM Bipolaridad]`

### 29. Sector — `slicer`

- **Values:** `Ferrada[Sector]`

### 30. Mapa de Georreferenciación — `esriVisual`

- **Color:** `Ferrada[Sector]`
- **Location:** `Ferrada[Dirección Completa]`
- **Tooltips:** `Ferrada[RUN]`
- **Tooltips:** `Ferrada[Nombre completo]`
- **Tooltips:** `Ferrada[Edad]` — «Edad1»
- **Tooltips:** `Ferrada[Sexo]`

### 31. Ansiedad — `slicer`

- **Values:** `Ferrada[SM Ansiedad]`

---

## Anexo: lógica de los campos usados

### `Atenciones[FECHA ATENCION]`

_Campo base (no calculado): proviene de la carga de Power Query._

### `Atenciones[PSM (act)]`

Clasifica la atención de salud mental: «Control SM» si la actividad contiene «controles salud men», «Consulta SM» si contiene «consulta de salud men»; si no, BLANK.

```dax
SWITCH(
    TRUE(),
    CONTAINSSTRING(Atenciones[ACTIVIDADES],"controles salud men"),"Control SM",
    CONTAINSSTRING(Atenciones[ACTIVIDADES],"consulta de salud men"),"Consulta SM",
    BLANK())
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

### `Ferrada[Diazepam]`

Indicador SI/NO: existe receta vigente cuya descripción contiene «diazepam».

```dax
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
        FILTER(
            'Recetas Vigentes',
            'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
            CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"diazepam"
            )
        )
    ),"SI","NO"
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

### `Ferrada[Duloxetina (Ext)]`

Indicador SI/NO: existe receta externa registrada (tabla «Recetas Externas») cuyo medicamento contiene «duloxetina».

```dax
IF(CALCULATE(COUNT('Recetas Externas'[RUN]),
FILTER(ALL('Recetas Externas'),'Recetas Externas'[RUN]='Ferrada'[RUN]),
CONTAINSSTRING('Recetas Externas'[Medicamento],"duloxetina")),
"SI","NO")
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

### `Ferrada[Escitalopram]`

Indicador SI/NO: existe receta interna vigente («Recetas Vigentes») o receta externa registrada («Recetas Externas») que contenga «escitalopram».

```dax
VAR _Receta = 
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
        FILTER(
            'Recetas Vigentes',
            'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
            CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"escitalopram"
            )
        )
    ),"SI","NO"
)

VAR _Externa =
IF(
    CALCULATE(COUNT('Recetas Externas'[RUN]),
        FILTER(
            'Recetas Externas',
            'Recetas Externas'[RUN]='Ferrada'[RUN] &&
            CONTAINSSTRING('Recetas Externas'[Medicamento],"escitalopram"
            )
        )
    ),"SI","NO"
)

RETURN

IF(
    _Externa="SI" ||
    _Receta="SI",
    "SI","NO"
)
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

### `Ferrada[Fecha Pasivación]`

Trae por cruce de RUN el valor de «FECHA PASIVACION» desde la tabla «Inscritos» hacia esta tabla (LOOKUPVALUE). Copia directa, sin transformación.

```dax
LOOKUPVALUE(Inscritos[FECHA PASIVACION],Inscritos[RUN],'Ferrada'[RUN])
```

### `Ferrada[Fibromialgia]`

Fibromialgia SI/NO: diagnóstico «fibromialgia» en alguna atención médica.

```dax
IF(
    CALCULATE(COUNT('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"fibromialgia") &&
    CONTAINSSTRING('Atenciones'[INSTRUMENTO],"médic")))),
    "SI","NO")
```

### `Ferrada[Género]`

Género registrado en «Inscritos». BLANK si no hay.

```dax
IF(ISBLANK(LOOKUPVALUE(Inscritos[GENERO],Inscritos[RUN],'Ferrada'[RUN])),BLANK(),LOOKUPVALUE(Inscritos[GENERO],Inscritos[RUN],'Ferrada'[RUN]))
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

### `Ferrada[Pertenece a PSM]`

Pertenencia al programa de salud mental: «SI» si cualquiera de las 24 columnas de diagnóstico SM listadas en la fórmula es distinta de «NO» (incluye estados «Activo»/«Egresado»).

```dax
IF(
'Ferrada'[SM Violencia]<>"NO" ||
'Ferrada'[SM Abuso sexual]<>"NO" || 
'Ferrada'[SM Suicidio (form)]<>"NO" ||
'Ferrada'[SM Depresión]<>"NO" ||
'Ferrada'[SM Depresión Postparto]<>"NO" ||
'Ferrada'[SM Bipolaridad]<>"NO" ||
'Ferrada'[SM OH y Drogas]<>"NO" ||
'Ferrada'[SM TDAH]<>"NO" ||
'Ferrada'[SM Oposicionista desafiante]<>"NO" ||
'Ferrada'[SM Ansiedad separación]<>"NO" ||
'Ferrada'[SM Otras Infancia/Adolescencia]<>"NO" ||
'Ferrada'[SM Ansiedad]<>"NO" ||
'Ferrada'[SM Demencia]<>"NO" ||
'Ferrada'[SM Esquizofrenia]<>"NO" ||
'Ferrada'[SM Adaptativo]<>"NO" ||
'Ferrada'[SM Conducta Alimentaria]<>"NO" ||
'Ferrada'[SM Retraso Mental]<>"NO" ||
'Ferrada'[SM Personalidad]<>"NO" ||
'Ferrada'[SM Autismo]<>"NO" ||
'Ferrada'[SM Asperger]<>"NO" ||
'Ferrada'[SM Rett]<>"NO" ||
'Ferrada'[SM Desintegrativo niñez]<>"NO" ||
'Ferrada'[SM TGD]<>"NO" ||
'Ferrada'[SM Otras (form)]<>"NO",
"SI","NO")
```

### `Ferrada[Pregabalina]`

Indicador SI/NO: existe receta interna vigente («Recetas Vigentes») o receta externa registrada («Recetas Externas») que contenga «pregabal».

```dax
VAR _Receta =
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
        FILTER(
            'Recetas Vigentes',
            'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
            CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"pregabal"
            )
        )
    ),"SI","NO"
)

VAR _Externa = 
IF(
    CALCULATE(COUNT('Recetas Externas'[RUN]),
        FILTER(
            'Recetas Externas',
            'Recetas Externas'[RUN]='Ferrada'[RUN] &&
            CONTAINSSTRING('Recetas Externas'[Medicamento],"pregabalina"
            )
        )
    ),"SI","NO"
)

RETURN

IF(
    _Externa="SI" ||
    _Receta="SI",
    "SI","NO"
)
```

### `Ferrada[Pueblo Originario]`

Trae por cruce de RUN el valor de «PUEBLO INDIG» desde la tabla «Inscritos» hacia esta tabla (LOOKUPVALUE). Copia directa, sin transformación.

```dax
LOOKUPVALUE(Inscritos[PUEBLO INDIG],Inscritos[RUN],'Ferrada'[RUN])
```

### `Ferrada[Quetiapina]`

Indicador SI/NO: el paciente tiene al menos una receta vigente del establecimiento (tabla «Recetas Vigentes») cuya descripción de artículo contiene «Quetiapina».

```dax
IF(CALCULATE(count('Recetas Vigentes'[RUN]),
FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] && 
CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"Quetiapina"))),
"SI","NO")
```

### `Ferrada[Quetiapina (Ext)]`

Indicador SI/NO: existe receta externa registrada cuyo medicamento contiene «quetiapina».

```dax
IF(CALCULATE(COUNT('Recetas Externas'[RUN]),
FILTER(ALL('Recetas Externas'),'Recetas Externas'[RUN]='Ferrada'[RUN] &&
CONTAINSSTRING('Recetas Externas'[Medicamento],"quetiapina"))),
"SI","NO")
```

### `Ferrada[RUN]`

_Campo base (no calculado): proviene de la carga de Power Query._

### `Ferrada[SM Abuso Sexual (fecha)]`

Fecha del último formulario PSM con la pregunta 9 (abuso sexual) marcada «sí» en ingreso/seguimiento.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
        FILTER(
            PSM,
            PSM[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING(PSM[9.- ¿ SUFRE DE ABUSO SEXUAL ?],"si") &&
            (   
                CONTAINSSTRING(PSM[10.- ESTADO],"ingreso") ||
                CONTAINSSTRING(PSM[10.- ESTADO],"seguimien")
            )
        )
    )
)

RETURN

_FechaFormulario
```

### `Ferrada[SM Abuso Sexual (form)]`

Estado del registro de abuso sexual según formulario PSM (pregunta 9): «Egresado» si hubo egreso en el mes anterior, «Activo» si el último formulario con «sí» está en ingreso/seguimiento, «NO» en caso contrario. A diferencia de las demás columnas (form), no exige instrumento médico.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
        FILTER(ALL(PSM),
            PSM[RUN]='Ferrada'[RUN] &&
            CONTAINSSTRING(PSM[9.- ¿ SUFRE DE ABUSO SEXUAL ?],"si") &&
            (
                CONTAINSSTRING(PSM[10.- ESTADO],"ingreso") ||
                CONTAINSSTRING(PSM[10.- ESTADO],"seguimien")
            )
        )
    )
)

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
        FILTER(
            PSM,
            PSM[RUN] = 'Ferrada'[RUN] &&
            PSM[FECHA ATENCION] = _FechaFormulario &&
            CONTAINSSTRING(PSM[9.- ¿ SUFRE DE ABUSO SEXUAL ?],"si") &&
            (
                CONTAINSSTRING(PSM[10.- ESTADO],"ingreso") ||
                CONTAINSSTRING(PSM[10.- ESTADO],"seguimien")
            )
        )
    ),
    "SI","NO"
)

var _Activo =
IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
        FILTER(
            'PSM',
            'PSM'[RUN]='Ferrada'[RUN] &&
            (
                'PSM'[FECHA ATENCION] <= EOMONTH(TODAY(),-1) &&
                'PSM'[FECHA ATENCION] >= EOMONTH(TODAY(),-2) +1 
            ) &&
            CONTAINSSTRING('PSM'[10.- ESTADO],"egreso")
        )
    ),"SI","NO"
)

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Abuso sexual]`

Abuso sexual SI/NO: diagnóstico T74.2 o Y05 en alguna atención, o el último formulario PSM con la pregunta 9 respondida dice «sí» en ingreso/seguimiento.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"T74.2") ||
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"y05")))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[9.- ¿ SUFRE DE ABUSO SEXUAL ?]<>""))
)

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    CONTAINSSTRING(PSM[9.- ¿ SUFRE DE ABUSO SEXUAL ?],"si") &&
        (
            CONTAINSSTRING(PSM[10.- ESTADO],"ingreso") ||
            CONTAINSSTRING(PSM[10.- ESTADO],"seguimien")
        )
    )
    ),
    "SI","NO"
)

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SM Activo 12m]`

Actividad de salud mental en 12 meses cerrados: «SI» si tuvo control, consulta o alguna de las visitas domiciliarias integrales de salud mental listadas en la fórmula.

```dax
VAR _FechaInicio = 
EOMONTH(TODAY(),-13) + 1

VAR _FechaFinal = 
EOMONTH(TODAY(),-1)

RETURN

IF(
    CALCULATE(COUNT('Atenciones'[RUN]),
        FILTER(
            'Atenciones',
            'Atenciones'[RUN] = 'Ferrada'[RUN] &&
                'Atenciones'[FECHA ATENCION] >= _FechaInicio &&
                'Atenciones'[FECHA ATENCION] <= _FechaFinal &&
            (
                CONTAINSSTRING('Atenciones'[ACTIVIDADES],"control salud mental") || 
                CONTAINSSTRING('Atenciones'[ACTIVIDADES],"controles salud mental") || 
                CONTAINSSTRING('Atenciones'[ACTIVIDADES],"consulta de salud mental") ||
                CONTAINSSTRING('Atenciones'[ACTIVIDADES],"visita domiciliaria integral familia con integrante con patologia de salud mental") || 
                CONTAINSSTRING('Atenciones'[ACTIVIDADES],"visita domiciliaria integral a familia con adulto mayor con demencia") ||
                CONTAINSSTRING('Atenciones'[ACTIVIDADES],"visita domiciliaria integral a familia con niños/as de 5 a 9 años con problemas y/o trastorno") || 
                CONTAINSSTRING('Atenciones'[ACTIVIDADES],"visita integral de salud mental a domicilio")
            )
        )
    ),
    "SI","NO"
)
```

### `Ferrada[SM Adaptativo]`

Trastorno adaptativo SI/NO: diagnóstico F43 en alguna atención, o el último formulario PSM con la pregunta 49 respondida dice «sí».

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
        FILTER(
            'Atenciones',
            'Atenciones'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"F43")
        )
    ),
    "SI","NO"
)

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
        FILTER(
            PSM,
            PSM[RUN] = 'Ferrada'[RUN] &&
            PSM[49.- ¿TIENE TRASTORNO ADAPTATIVO?] <> ""
        )
    )
)

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
        FILTER(
            PSM,
            PSM[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING(PSM[49.- ¿TIENE TRASTORNO ADAPTATIVO?],"si") &&
            PSM[FECHA ATENCION] = _FechaFormulario
        )
    ),
    "SI","NO"
)
RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SM Adaptativo (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «49.- ¿TIENE TRASTORNO ADAPTATIVO?» está marcada «sí» y el estado (50.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[49.- ¿TIENE TRASTORNO ADAPTATIVO?],"si")) &&
    (CONTAINSSTRING(PSM[50.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[50.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM Adaptativo (form)]`

Estado del trastorno adaptativo según formulario PSM médico (pregunta 49): «Activo» si el último formulario con «sí» está en ingreso/seguimiento; «Egresado» si hubo egreso en el mes anterior; «NO» en otro caso. Nota: a diferencia de las demás columnas (form), aquí «Activo» tiene prioridad sobre «Egresado».

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[49.- ¿TIENE TRASTORNO ADAPTATIVO?],"si")) &&
    (CONTAINSSTRING(PSM[50.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[50.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[49.- ¿TIENE TRASTORNO ADAPTATIVO?],"si")) &&
    (CONTAINSSTRING(PSM[50.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[50.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   PSM[FECHA ATENCION] >= EOMONTH(TODAY(),-2) + 1 &&
   PSM[FECHA ATENCION] <= EOMONTH(TODAY(),-1) &&
   CONTAINSSTRING('PSM'[50.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Activo="SI","Activo",
IF(
    _Egreso="SI","Egresado",
    "NO"))
```

### `Ferrada[SM Alprazolam]`

Indicador SI/NO: existe receta vigente cuya descripción contiene «alprazolam».

```dax
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN]),
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"alprazolam")),
    "SI","NO")
```

### `Ferrada[SM Amitriptilina]`

Indicador SI/NO: existe receta vigente cuya descripción contiene «amitriptilina».

```dax
IF(CALCULATE(COUNT('Recetas Vigentes'[RUN]),
FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN]),
CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"amitriptilina")),
"SI","NO")
```

### `Ferrada[SM Ansiedad]`

Indicador SI/NO de diagnóstico: (a) alguna atención con diagnóstico que contenga «ansiedad», o (b) último formulario PSM médico con «41.- ¿ TIENE TRASTORNO DE ANSIEDAD ?»=«sí» en ingreso/seguimiento.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"ansiedad"))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[41.- ¿ TIENE TRASTORNO DE ANSIEDAD ?],"si")) &&
    (CONTAINSSTRING(PSM[42.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[42.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[41.- ¿ TIENE TRASTORNO DE ANSIEDAD ?],"si")) &&
    (CONTAINSSTRING(PSM[42.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[42.- ESTADO],"seguimien")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SM Ansiedad (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «41.- ¿ TIENE TRASTORNO DE ANSIEDAD ?» está marcada «sí» y el estado (42.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[41.- ¿ TIENE TRASTORNO DE ANSIEDAD ?],"si")) &&
    (CONTAINSSTRING(PSM[42.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[42.- ESTADO],"seguimien")))))


RETURN

_FechaFormulario
```

### `Ferrada[SM Ansiedad (form)]`

Estado del diagnóstico según formulario PSM médico: «Egresado» si hubo estado «egreso» en el mes anterior; «Activo» si el último formulario con «41.- ¿ TIENE TRASTORNO DE ANSIEDAD ?»=«sí» está en ingreso/seguimiento; «NO» si nada de lo anterior.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[41.- ¿ TIENE TRASTORNO DE ANSIEDAD ?],"si")) &&
    (CONTAINSSTRING(PSM[42.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[42.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[41.- ¿ TIENE TRASTORNO DE ANSIEDAD ?],"si")) &&
    (CONTAINSSTRING(PSM[42.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[42.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   (DATEDIFF('PSM'[FECHA ATENCION],TODAY(),MONTH) > 0 &&
   DATEDIFF('PSM'[FECHA ATENCION],TODAY(),MONTH) <= 1) &&
   CONTAINSSTRING('PSM'[42.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Ansiedad Fobia]`

Indicador SI/NO simple: revisa si [SM Ansiedad tipo (form)] contiene «sociales». No consulta otras tablas; opera fila a fila sobre la propia tabla.

```dax
IF(
    CONTAINSSTRING('Ferrada'[SM Ansiedad tipo (form)],"sociales"),
    "SI","NO")
```

### `Ferrada[SM Ansiedad Otras]`

Indicador SI/NO simple: revisa si [SM Ansiedad tipo (form)] contiene «otro». No consulta otras tablas; opera fila a fila sobre la propia tabla.

```dax
IF(
    CONTAINSSTRING('Ferrada'[SM Ansiedad tipo (form)],"otro"),
    "SI","NO")
```

### `Ferrada[SM Ansiedad Pánico]`

Indicador SI/NO simple: revisa si [SM Ansiedad tipo (form)] contiene «pánico». No consulta otras tablas; opera fila a fila sobre la propia tabla.

```dax
IF(
    CONTAINSSTRING('Ferrada'[SM Ansiedad tipo (form)],"pánico"),
    "SI","NO")
```

### `Ferrada[SM Ansiedad TAG]`

Indicador SI/NO simple: revisa si [SM Ansiedad tipo (form)] contiene «generali». No consulta otras tablas; opera fila a fila sobre la propia tabla.

```dax
IF(
    CONTAINSSTRING('Ferrada'[SM Ansiedad tipo (form)],"generali"),
    "SI","NO")
```

### `Ferrada[SM Ansiedad TEPT]`

Indicador SI/NO simple: revisa si [SM Ansiedad tipo (form)] contiene «traumático». No consulta otras tablas; opera fila a fila sobre la propia tabla.

```dax
IF(
    CONTAINSSTRING('Ferrada'[SM Ansiedad tipo (form)],"traumático"),
    "SI","NO")
```

### `Ferrada[SM Ansiedad separación]`

Indicador SI/NO de diagnóstico: (a) alguna atención con diagnóstico que contenga «f93.0», o (b) último formulario PSM médico con «71.- ¿TIENE TRASTORNO DE ANSIEDAD DE SEPARACIÓN EN LA I»=«sí» en ingreso/seguimiento.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"f93.0"))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[71.- ¿TIENE TRASTORNO DE ANSIEDAD DE SEPARACIÓN EN LA I],"si")) &&
    (CONTAINSSTRING(PSM[72.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[72.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[71.- ¿TIENE TRASTORNO DE ANSIEDAD DE SEPARACIÓN EN LA I],"si")) &&
    (CONTAINSSTRING(PSM[72.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[72.- ESTADO],"seguimien")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SM Ansiedad separación (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «71.- ¿TIENE TRASTORNO DE ANSIEDAD DE SEPARACIÓN EN LA I» está marcada «sí» y el estado (72.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[71.- ¿TIENE TRASTORNO DE ANSIEDAD DE SEPARACIÓN EN LA I],"si")) &&
    (CONTAINSSTRING(PSM[72.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[72.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM Ansiedad separación (form)]`

Estado del diagnóstico según formulario PSM médico. Devuelve «Egresado» si hubo un registro con estado «egreso» durante el mes anterior completo; «Activo» si el último formulario con «71.- ¿TIENE TRASTORNO DE ANSIEDAD DE SEPARACIÓN EN LA I»=«sí» está en ingreso/seguimiento; «NO» en caso contrario. El egreso tiene prioridad sobre el activo.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[71.- ¿TIENE TRASTORNO DE ANSIEDAD DE SEPARACIÓN EN LA I],"si")) &&
    (CONTAINSSTRING(PSM[72.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[72.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[71.- ¿TIENE TRASTORNO DE ANSIEDAD DE SEPARACIÓN EN LA I],"si")) &&
    (CONTAINSSTRING(PSM[72.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[72.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   PSM[FECHA ATENCION] >= EOMONTH(TODAY(),-2) + 1 &&
   PSM[FECHA ATENCION] <= EOMONTH(TODAY(),-1) &&
   CONTAINSSTRING('PSM'[72.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Ansiedad tipo (form)]`

Devuelve el valor textual de la pregunta «43.- TIPO DE TRASTORNO DE ANSIEDAD» del formulario PSM más reciente en que esa pregunta no está vacía (p. ej. tipo o gravedad). BLANK si nunca se ha registrado.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[43.- TIPO DE TRASTORNO DE ANSIEDAD]<>"")))

var _Formulario = 
TOPN(1,
    CALCULATETABLE(VALUES(PSM[43.- TIPO DE TRASTORNO DE ANSIEDAD]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario)),
    PSM[43.- TIPO DE TRASTORNO DE ANSIEDAD])

var _Resultado =

IF(
    _Formulario="",BLANK(),_Formulario)

RETURN
IF(
    _Resultado="",BLANK(),_Resultado)
```

### `Ferrada[SM Asperger]`

Indicador SI/NO de diagnóstico: (a) alguna atención con diagnóstico que contenga «asperger», o (b) último formulario PSM médico con «85.- ¿TIENE ASPERGER?»=«sí» en ingreso/seguimiento.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"asperger"))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[85.- ¿TIENE ASPERGER?],"si")) &&
    (CONTAINSSTRING(PSM[86.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[86.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[85.- ¿TIENE ASPERGER?],"si")) &&
    (CONTAINSSTRING(PSM[86.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[86.- ESTADO],"seguimien")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SM Asperger (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «85.- ¿TIENE ASPERGER?» está marcada «sí» y el estado (86.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[85.- ¿TIENE ASPERGER?],"si")) &&
    (CONTAINSSTRING(PSM[86.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[86.- ESTADO],"seguimien")))))


RETURN

_FechaFormulario
```

### `Ferrada[SM Asperger (form)]`

Estado del diagnóstico según formulario PSM médico: «Egresado» si hubo estado «egreso» en el mes anterior; «Activo» si el último formulario con «85.- ¿TIENE ASPERGER?»=«sí» está en ingreso/seguimiento; «NO» si nada de lo anterior.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[85.- ¿TIENE ASPERGER?],"si")) &&
    (CONTAINSSTRING(PSM[86.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[86.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[85.- ¿TIENE ASPERGER?],"si")) &&
    (CONTAINSSTRING(PSM[86.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[86.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   (DATEDIFF('PSM'[FECHA ATENCION],TODAY(),MONTH) > 0 &&
   DATEDIFF('PSM'[FECHA ATENCION],TODAY(),MONTH) <= 1) &&
   CONTAINSSTRING('PSM'[86.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Atendido hace 13m]`

Rescate SM: «Si» si fue atendido en salud mental exactamente hace 13 meses (el mes que acaba de salir de la ventana) y no está activo en los 12 meses — es el paciente que se acaba de «caer» del programa.

```dax
VAR _UltimoDiaMesAnterior = EOMONTH(TODAY(), -1)
VAR _InicioPeriodo = EOMONTH(_UltimoDiaMesAnterior, -13) + 1
VAR _FinPeriodo = EOMONTH(_UltimoDiaMesAnterior, -12)

VAR _Atendido13m = 
    IF(
        CALCULATE(
            COUNT('Atenciones'[RUN]),
            FILTER(
                ALL('Atenciones'),
                'Atenciones'[RUN] = 'Ferrada'[RUN] &&
                'Atenciones'[FECHA ATENCION] >= _InicioPeriodo &&
                'Atenciones'[FECHA ATENCION] <= _FinPeriodo &&
                (
                    CONTAINSSTRING('Atenciones'[ACTIVIDADES], "control salud mental") || 
                    CONTAINSSTRING('Atenciones'[ACTIVIDADES], "controles salud mental") || 
                    CONTAINSSTRING('Atenciones'[ACTIVIDADES], "consulta de salud mental") || 
                    CONTAINSSTRING('Atenciones'[ACTIVIDADES], "visita domiciliaria integral familia con integrante con patologia de salud mental") || 
                    CONTAINSSTRING('Atenciones'[ACTIVIDADES], "visita domiciliaria integral a familia con adulto mayor con demencia") || 
                    CONTAINSSTRING('Atenciones'[ACTIVIDADES], "visita domiciliaria integral a familia con niños/as de 5 a 9 años con problemas y/o trastorno") || 
                    CONTAINSSTRING('Atenciones'[ACTIVIDADES], "visita integral de salud mental a domicilio")
                )
            )
        ) > 0,
        "Si",
        "No"
    )

VAR _Activo = 'Ferrada'[SM Activo 12m]

RETURN
SWITCH(
    TRUE(),
    _Activo = "si", "No",
    _Atendido13m = "Si", "Si",
    "No"
)
```

### `Ferrada[SM Atendido hace 6m]`

Rescate SM a 6 meses: «Si» si tuvo atención de salud mental hace exactamente 6 meses y ninguna posterior (paciente que dejó de asistir).

```dax
VAR _UltimoDiaMesAnterior = EOMONTH(TODAY(), -1)
VAR _InicioPeriodo = EOMONTH(_UltimoDiaMesAnterior, -6) + 1
VAR _FinPeriodo = EOMONTH(_UltimoDiaMesAnterior, -5)

-- Atenciones válidas en el mes objetivo
VAR _Atencion6m = 
    CALCULATE(
        COUNTROWS('Atenciones'),
        FILTER(
            ALL('Atenciones'),
            'Atenciones'[RUN] = 'Ferrada'[RUN] &&
            'Atenciones'[FECHA ATENCION] >= _InicioPeriodo &&
            'Atenciones'[FECHA ATENCION] <= _FinPeriodo &&
            CONTAINSSTRING('Atenciones'[ACTIVIDADES], "salud mental")
        )
    )

-- Atenciones posteriores al mes objetivo
VAR _AtencionDespues = 
    CALCULATE(
        COUNTROWS('Atenciones'),
        FILTER(
            ALL('Atenciones'),
            'Atenciones'[RUN] = 'Ferrada'[RUN] &&
            'Atenciones'[FECHA ATENCION] > _FinPeriodo &&
            CONTAINSSTRING('Atenciones'[ACTIVIDADES], "salud mental")
        )
    )

RETURN
SWITCH(
    TRUE(),
    _Atencion6m > 0 && _AtencionDespues = 0, "Si",
    "No"
)
```

### `Ferrada[SM Autismo]`

Indicador SI/NO de diagnóstico: (a) alguna atención con diagnóstico que contenga «f84», o (b) último formulario PSM médico con «83.- ¿TIENE AUTISMO?»=«sí» en ingreso/seguimiento.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"f84"))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[83.- ¿TIENE AUTISMO?],"si")) &&
    (CONTAINSSTRING(PSM[84.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[84.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[83.- ¿TIENE AUTISMO?],"si")) &&
    (CONTAINSSTRING(PSM[84.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[84.- ESTADO],"seguimien")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SM Autismo (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «83.- ¿TIENE AUTISMO?» está marcada «sí» y el estado (84.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[83.- ¿TIENE AUTISMO?],"si")) &&
    (CONTAINSSTRING(PSM[84.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[84.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM Autismo (form)]`

Estado del diagnóstico según formulario PSM médico: «Egresado» si hubo estado «egreso» en el mes anterior; «Activo» si el último formulario con «83.- ¿TIENE AUTISMO?»=«sí» está en ingreso/seguimiento; «NO» si nada de lo anterior.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[83.- ¿TIENE AUTISMO?],"si")) &&
    (CONTAINSSTRING(PSM[84.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[84.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[83.- ¿TIENE AUTISMO?],"si")) &&
    (CONTAINSSTRING(PSM[84.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[84.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   (DATEDIFF('PSM'[FECHA ATENCION],TODAY(),MONTH) > 0 &&
   DATEDIFF('PSM'[FECHA ATENCION],TODAY(),MONTH) <= 1) &&
   CONTAINSSTRING('PSM'[84.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Bipolaridad]`

Indicador SI/NO de diagnóstico: (a) alguna atención con diagnóstico que contenga «f31», o (b) último formulario PSM médico con «23.- ¿ TIENE TRANSTORNO BIPOLAR ?»=«sí» en ingreso/seguimiento.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"f31"))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[23.- ¿ TIENE TRANSTORNO BIPOLAR ?],"si")) &&
    (CONTAINSSTRING(PSM[24.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[24.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[23.- ¿ TIENE TRANSTORNO BIPOLAR ?],"si")) &&
    (CONTAINSSTRING(PSM[24.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[24.- ESTADO],"seguimien")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SM Bipolaridad (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «23.- ¿ TIENE TRANSTORNO BIPOLAR ?» está marcada «sí» y el estado (24.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[23.- ¿ TIENE TRANSTORNO BIPOLAR ?],"si")) &&
    (CONTAINSSTRING(PSM[24.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[24.- ESTADO],"seguimien")))))


RETURN

_FechaFormulario
```

### `Ferrada[SM Bipolaridad (form)]`

Estado del diagnóstico según formulario PSM médico: «Egresado» si hubo estado «egreso» en el mes anterior; «Activo» si el último formulario con «23.- ¿ TIENE TRANSTORNO BIPOLAR ?»=«sí» está en ingreso/seguimiento; «NO» si nada de lo anterior.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[23.- ¿ TIENE TRANSTORNO BIPOLAR ?],"si")) &&
    (CONTAINSSTRING(PSM[24.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[24.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[23.- ¿ TIENE TRANSTORNO BIPOLAR ?],"si")) &&
    (CONTAINSSTRING(PSM[24.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[24.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   (DATEDIFF('PSM'[FECHA ATENCION],TODAY(),MONTH) > 0 &&
   DATEDIFF('PSM'[FECHA ATENCION],TODAY(),MONTH) <= 1) &&
   CONTAINSSTRING('PSM'[24.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Bupropion (Ext)]`

Indicador SI/NO: receta externa que contenga «bupropi» o «anfebutamona» (bupropión).

```dax
IF(CALCULATE(COUNT('Recetas Externas'[RUN]),
FILTER(ALL('Recetas Externas'),'Recetas Externas'[RUN]='Ferrada'[RUN]),
CONTAINSSTRING('Recetas Externas'[Medicamento],"bupropi") ||
CONTAINSSTRING('Recetas Externas'[Medicamento],"anfebutamona")),
"SI","NO")
```

### `Ferrada[SM Clonazepam]`

Indicador SI/NO: existe receta vigente cuya descripción contiene «clonazepam».

```dax
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN]),
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"clonazepam")),
    "SI","NO")
```

### `Ferrada[SM Clorpromazina]`

Indicador SI/NO: existe receta vigente cuya descripción contiene «Clorproma».

```dax
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN]),
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"Clorproma")),
    "SI","NO")
```

### `Ferrada[SM Conducta Alimentaria]`

Indicador SI/NO de diagnóstico: (a) alguna atención con diagnóstico que contenga «F98.2» o «F50», o (b) último formulario PSM médico con «55.- ¿ TIENE TRASTORNO DE LA CONDUCTA ALIMENTARIA ?»=«sí» en ingreso/seguimiento.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"F98.2") || 
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"F50")))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[55.- ¿ TIENE TRASTORNO DE LA CONDUCTA ALIMENTARIA ?],"si")) &&
    (CONTAINSSTRING(PSM[56.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[56.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[55.- ¿ TIENE TRASTORNO DE LA CONDUCTA ALIMENTARIA ?],"si")) &&
    (CONTAINSSTRING(PSM[56.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[56.- ESTADO],"seguimien")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SM Conducta Alimentaria (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «55.- ¿ TIENE TRASTORNO DE LA CONDUCTA ALIMENTARIA ?» está marcada «sí» y el estado (56.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[55.- ¿ TIENE TRASTORNO DE LA CONDUCTA ALIMENTARIA ?],"si")) &&
    (CONTAINSSTRING(PSM[56.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[56.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM Conducta Alimentaria (form)]`

Estado del diagnóstico según formulario PSM médico: «Egresado» si hubo estado «egreso» en el mes anterior; «Activo» si el último formulario con «55.- ¿ TIENE TRASTORNO DE LA CONDUCTA ALIMENTARIA ?»=«sí» está en ingreso/seguimiento; «NO» si nada de lo anterior.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[55.- ¿ TIENE TRASTORNO DE LA CONDUCTA ALIMENTARIA ?],"si")) &&
    (CONTAINSSTRING(PSM[56.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[56.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[55.- ¿ TIENE TRASTORNO DE LA CONDUCTA ALIMENTARIA ?],"si")) &&
    (CONTAINSSTRING(PSM[56.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[56.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   (DATEDIFF('PSM'[FECHA ATENCION],TODAY(),MONTH) > 0 &&
   DATEDIFF('PSM'[FECHA ATENCION],TODAY(),MONTH) <= 1) &&
   CONTAINSSTRING('PSM'[24.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
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

### `Ferrada[SM Demencia (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «44.- ¿ TIENE ALZHEIMER Y/O OTRAS DEMENCIAS ?» está marcada «sí» y el estado (46.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[44.- ¿ TIENE ALZHEIMER Y/O OTRAS DEMENCIAS ?],"si")) &&
    (CONTAINSSTRING(PSM[46.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[46.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM Demencia (form)]`

Estado del diagnóstico según formulario PSM médico: «Egresado» si hubo estado «egreso» en el mes anterior; «Activo» si el último formulario con «44.- ¿ TIENE ALZHEIMER Y/O OTRAS DEMENCIAS ?»=«sí» está en ingreso/seguimiento; «NO» si nada de lo anterior.

```dax
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

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   (DATEDIFF('PSM'[FECHA ATENCION],TODAY(),MONTH) > 0 &&
   DATEDIFF('PSM'[FECHA ATENCION],TODAY(),MONTH) <= 1) &&
   CONTAINSSTRING('PSM'[46.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Demencia Avanzado]`

Indicador SI/NO simple: revisa si [SM Demencia Gravedad (form)] contiene «avanza». No consulta otras tablas; opera fila a fila sobre la propia tabla.

```dax
IF(
    CONTAINSSTRING('Ferrada'[SM Demencia Gravedad (form)],"avanza"),
    "SI","NO")
```

### `Ferrada[SM Demencia Gravedad (form)]`

Devuelve el valor textual de la pregunta «45.- ETAPA» del formulario PSM más reciente en que esa pregunta no está vacía (p. ej. tipo o gravedad). BLANK si nunca se ha registrado.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[45.- ETAPA]<>"")))

var _Formulario = 
TOPN(1,
    CALCULATETABLE(VALUES(PSM[45.- ETAPA]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario)),
    PSM[45.- ETAPA])

var _Resultado =

IF(
    _Formulario="",BLANK(),_Formulario)

RETURN
IF(
    _Resultado="",BLANK(),_Resultado)
```

### `Ferrada[SM Demencia Leve]`

Indicador SI/NO simple: revisa si [SM Demencia Gravedad (form)] contiene «leve». No consulta otras tablas; opera fila a fila sobre la propia tabla.

```dax
IF(
    CONTAINSSTRING('Ferrada'[SM Demencia Gravedad (form)],"leve"),
    "SI","NO")
```

### `Ferrada[SM Demencia Moderado]`

Indicador SI/NO simple: revisa si [SM Demencia Gravedad (form)] contiene «moderado». No consulta otras tablas; opera fila a fila sobre la propia tabla.

```dax
IF(
    CONTAINSSTRING('Ferrada'[SM Demencia Gravedad (form)],"moderado"),
    "SI","NO")
```

### `Ferrada[SM Depresión]`

Depresión SI/NO: diagnóstico F32/F33 o «distimia» en alguna atención, o último formulario PSM médico con pregunta 18 («¿tiene depresión?») marcada «sí» en ingreso/seguimiento.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"F32") ||
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"F33") ||
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"distimia")))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[18.- ¿ TIENE  DEPRESIÓN ?],"si")) &&
    (CONTAINSSTRING(PSM[19.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[19.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[18.- ¿ TIENE  DEPRESIÓN ?],"si")) &&
    (CONTAINSSTRING(PSM[19.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[19.- ESTADO],"seguimien")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SM Depresión (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «18.- ¿ TIENE  DEPRESIÓN ?» está marcada «sí» y el estado (19.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[18.- ¿ TIENE  DEPRESIÓN ?],"si")) &&
    (CONTAINSSTRING(PSM[19.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[19.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM Depresión (form)]`

Estado del diagnóstico según formulario PSM médico. Devuelve «Egresado» si hubo un registro con estado «egreso» durante el mes anterior completo; «Activo» si el último formulario con «18.- ¿ TIENE  DEPRESIÓN ?»=«sí» está en ingreso/seguimiento; «NO» en caso contrario. El egreso tiene prioridad sobre el activo.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[18.- ¿ TIENE  DEPRESIÓN ?],"si")) &&
    (CONTAINSSTRING(PSM[19.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[19.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[18.- ¿ TIENE  DEPRESIÓN ?],"si")) &&
    (CONTAINSSTRING(PSM[19.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[19.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   PSM[FECHA ATENCION] >= EOMONTH(TODAY(),-2) + 1 &&
   PSM[FECHA ATENCION] <= EOMONTH(TODAY(),-1) &&
   CONTAINSSTRING('PSM'[19.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Depresión Grave]`

Indicador SI/NO simple: revisa si [SM Depresión Gravedad (form)] contiene «grave». No consulta otras tablas; opera fila a fila sobre la propia tabla.

```dax
IF(
    CONTAINSSTRING('Ferrada'[SM Depresión Gravedad (form)],"grave"),
    "SI","NO")
```

### `Ferrada[SM Depresión Gravedad (form)]`

Devuelve el valor textual de la pregunta «20.- TIPO DE DEPRESIÓN» del formulario PSM más reciente en que esa pregunta no está vacía (p. ej. tipo o gravedad). BLANK si nunca se ha registrado.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[20.- TIPO DE DEPRESIÓN]<>"")))

var _Formulario = 
TOPN(1,
    CALCULATETABLE(VALUES(PSM[20.- TIPO DE DEPRESIÓN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario)),
    PSM[20.- TIPO DE DEPRESIÓN])

var _Resultado =

IF(
    _Formulario="",BLANK(),_Formulario)

RETURN
IF(
    _Resultado="",BLANK(),_Resultado)
```

### `Ferrada[SM Depresión Leve]`

Indicador SI/NO simple: revisa si [SM Depresión Gravedad (form)] contiene «leve». No consulta otras tablas; opera fila a fila sobre la propia tabla.

```dax
IF(
    CONTAINSSTRING('Ferrada'[SM Depresión Gravedad (form)],"leve"),
    "SI","NO")
```

### `Ferrada[SM Depresión Moderada]`

Indicador SI/NO simple: revisa si [SM Depresión Gravedad (form)] contiene «moderada». No consulta otras tablas; opera fila a fila sobre la propia tabla.

```dax
IF(
    CONTAINSSTRING('Ferrada'[SM Depresión Gravedad (form)],"moderada"),
    "SI","NO")
```

### `Ferrada[SM Depresión Postparto]`

Indicador SI/NO de diagnóstico. Combina dos fuentes: (a) alguna atención registrada con diagnóstico que contenga «F53», o (b) el último formulario PSM con instrumento médico en que «21.- ¿ TIENE DEPRESIÓN POST - PARTO ?»=«sí» y estado en ingreso/seguimiento. Basta una de las dos.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"F53")))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[21.- ¿ TIENE DEPRESIÓN POST - PARTO ?],"si")) &&
    (CONTAINSSTRING(PSM[22.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[22.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[21.- ¿ TIENE DEPRESIÓN POST - PARTO ?],"si")) &&
    (CONTAINSSTRING(PSM[22.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[22.- ESTADO],"seguimien")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SM Depresión Postparto (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «21.- ¿ TIENE DEPRESIÓN POST - PARTO ?» está marcada «sí» y el estado (22.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[21.- ¿ TIENE DEPRESIÓN POST - PARTO ?],"si")) &&
    (CONTAINSSTRING(PSM[22.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[22.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM Depresión Postparto (form)]`

Estado del diagnóstico según formulario PSM médico: «Egresado» si hubo estado «egreso» en el mes anterior; «Activo» si el último formulario con «21.- ¿ TIENE DEPRESIÓN POST - PARTO ?»=«sí» está en ingreso/seguimiento; «NO» si nada de lo anterior.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[21.- ¿ TIENE DEPRESIÓN POST - PARTO ?],"si")) &&
    (CONTAINSSTRING(PSM[22.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[22.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[21.- ¿ TIENE DEPRESIÓN POST - PARTO ?],"si")) &&
    (CONTAINSSTRING(PSM[22.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[22.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   (DATEDIFF('PSM'[FECHA ATENCION],TODAY(),MONTH) > 0 &&
   DATEDIFF('PSM'[FECHA ATENCION],TODAY(),MONTH) <= 1) &&
   CONTAINSSTRING('PSM'[22.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Desintegrativo niñez]`

Indicador SI/NO de diagnóstico. Combina dos fuentes: (a) alguna atención registrada con diagnóstico que contenga «F84.3», o (b) el último formulario PSM con instrumento médico en que «89.- ¿TIENE TRASTORNO DESINTEGRATIVO DE LA INFANCIA?»=«sí» y estado en ingreso/seguimiento. Basta una de las dos.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"F84.3")))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[89.- ¿TIENE TRASTORNO DESINTEGRATIVO DE LA INFANCIA?],"si")) &&
    (CONTAINSSTRING(PSM[90.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[90.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[89.- ¿TIENE TRASTORNO DESINTEGRATIVO DE LA INFANCIA?],"si")) &&
    (CONTAINSSTRING(PSM[90.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[90.- ESTADO],"seguimien")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SM Desintegrativo niñez (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «89.- ¿TIENE TRASTORNO DESINTEGRATIVO DE LA INFANCIA?» está marcada «sí» y el estado (90.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[89.- ¿TIENE TRASTORNO DESINTEGRATIVO DE LA INFANCIA?],"si")) &&
    (CONTAINSSTRING(PSM[90.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[90.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM Desintegrativo niñez (form)]`

Estado del diagnóstico según formulario PSM médico. Devuelve «Egresado» si hubo un registro con estado «egreso» durante el mes anterior completo; «Activo» si el último formulario con «89.- ¿TIENE TRASTORNO DESINTEGRATIVO DE LA INFANCIA?»=«sí» está en ingreso/seguimiento; «NO» en caso contrario. El egreso tiene prioridad sobre el activo.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[89.- ¿TIENE TRASTORNO DESINTEGRATIVO DE LA INFANCIA?],"si")) &&
    (CONTAINSSTRING(PSM[90.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[90.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[89.- ¿TIENE TRASTORNO DESINTEGRATIVO DE LA INFANCIA?],"si")) &&
    (CONTAINSSTRING(PSM[90.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[90.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   PSM[FECHA ATENCION] >= EOMONTH(TODAY(),-2) + 1 &&
   PSM[FECHA ATENCION] <= EOMONTH(TODAY(),-1) &&
   CONTAINSSTRING('PSM'[90.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Drogas Dependiente (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «37.- CONSUMO DEPENDIENTE DE DROGAS» está marcada «sí» y el estado (38.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[37.- CONSUMO DEPENDIENTE DE DROGAS],"si")) &&
    (CONTAINSSTRING(PSM[38.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[38.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM Drogas Dependiente (form)]`

Estado del diagnóstico según formulario PSM médico: «Egresado» si hubo estado «egreso» en el mes anterior; «Activo» si el último formulario con «37.- CONSUMO DEPENDIENTE DE DROGAS»=«sí» está en ingreso/seguimiento; «NO» si nada de lo anterior.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[37.- CONSUMO DEPENDIENTE DE DROGAS],"si")) &&
    (CONTAINSSTRING(PSM[38.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[38.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[37.- CONSUMO DEPENDIENTE DE DROGAS],"si")) &&
    (CONTAINSSTRING(PSM[38.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[38.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   (DATEDIFF('PSM'[FECHA ATENCION],TODAY(),MONTH) > 0 &&
   DATEDIFF('PSM'[FECHA ATENCION],TODAY(),MONTH) <= 1) &&
   CONTAINSSTRING('PSM'[38.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Drogas Perjudical (form)]`

Estado del diagnóstico según formulario PSM médico. Devuelve «Egresado» si hubo un registro con estado «egreso» durante el mes anterior completo; «Activo» si el último formulario con «35.- CONSUMO PERJUDICIAL DE DROGAS»=«sí» está en ingreso/seguimiento; «NO» en caso contrario. El egreso tiene prioridad sobre el activo.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[35.- CONSUMO PERJUDICIAL DE DROGAS],"si")) &&
    (CONTAINSSTRING(PSM[36.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[36.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[35.- CONSUMO PERJUDICIAL DE DROGAS],"si")) &&
    (CONTAINSSTRING(PSM[36.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[36.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   PSM[FECHA ATENCION] >= EOMONTH(TODAY(),-2) + 1 &&
   PSM[FECHA ATENCION] <= EOMONTH(TODAY(),-1) &&
   CONTAINSSTRING('PSM'[36.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Drogas perjudicial (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «35.- CONSUMO PERJUDICIAL DE DROGAS» está marcada «sí» y el estado (36.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[35.- CONSUMO PERJUDICIAL DE DROGAS],"si")) &&
    (CONTAINSSTRING(PSM[36.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[36.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM Esquizofrenia]`

Indicador SI/NO de diagnóstico. Combina dos fuentes: (a) alguna atención registrada con diagnóstico que contenga «F20», o (b) el último formulario PSM con instrumento médico en que «51.- ¿ TIENE ESQUIZOFRENIA ?»=«sí» y estado en ingreso/seguimiento. Basta una de las dos.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"F20")))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[51.- ¿ TIENE ESQUIZOFRENIA ?],"si")) &&
    (CONTAINSSTRING(PSM[52.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[52.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[51.- ¿ TIENE ESQUIZOFRENIA ?],"si")) &&
    (CONTAINSSTRING(PSM[52.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[52.- ESTADO],"seguimien")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SM Esquizofrenia (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «51.- ¿ TIENE ESQUIZOFRENIA ?» está marcada «sí» y el estado (52.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[51.- ¿ TIENE ESQUIZOFRENIA ?],"si")) &&
    (CONTAINSSTRING(PSM[52.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[52.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM Esquizofrenia (form)]`

Estado del diagnóstico según formulario PSM médico. Devuelve «Egresado» si hubo un registro con estado «egreso» durante el mes anterior completo; «Activo» si el último formulario con «51.- ¿ TIENE ESQUIZOFRENIA ?»=«sí» está en ingreso/seguimiento; «NO» en caso contrario. El egreso tiene prioridad sobre el activo.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[51.- ¿ TIENE ESQUIZOFRENIA ?],"si")) &&
    (CONTAINSSTRING(PSM[52.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[52.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[51.- ¿ TIENE ESQUIZOFRENIA ?],"si")) &&
    (CONTAINSSTRING(PSM[52.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[52.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   PSM[FECHA ATENCION] >= EOMONTH(TODAY(),-2) + 1 &&
   PSM[FECHA ATENCION] <= EOMONTH(TODAY(),-1) &&
   CONTAINSSTRING('PSM'[52.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Fecha último formulario]`

Fecha del último formulario de salud mental (PSM) de cualquier tipo.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN])))

RETURN

_FechaFormulario
```

### `Ferrada[SM Fluoxetina]`

Indicador SI/NO: el paciente tiene al menos una receta vigente del establecimiento (tabla «Recetas Vigentes») cuya descripción de artículo contiene «Fluoxetina».

```dax
IF(CALCULATE(count('Recetas Vigentes'[RUN]),
FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"Fluoxetina"))),
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

### `Ferrada[SM Madre <5 años]`

Respuesta a la pregunta 1 del formulario PSM («¿usted es madre de hijo menor de 5 años?») en su registro más reciente con dato.

```dax
VAR _Fecha = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
        FILTER(
            PSM,
            PSM[RUN] = Ferrada[RUN] &&
            PSM[1.- ¿USTED ES MADRE DE HIJO MENOR DE 5 AÑOS?] <> ""
        )
    )
)

VAR _Resultado = 
MAXX(
    CALCULATETABLE(VALUES(PSM[1.- ¿USTED ES MADRE DE HIJO MENOR DE 5 AÑOS?]),
        FILTER(
            PSM,
            PSM[RUN] = Ferrada[RUN] &&
            PSM[FECHA ATENCION] = _Fecha
        )
    ),PSM[1.- ¿USTED ES MADRE DE HIJO MENOR DE 5 AÑOS?]
)

RETURN

_Resultado
```

### `Ferrada[SM Melatonina (Ext)]`

Indicador SI/NO: existe receta externa registrada cuyo medicamento contiene «melatonina».

```dax
IF(CALCULATE(COUNT('Recetas Externas'[RUN]),
FILTER(ALL('Recetas Externas'),'Recetas Externas'[RUN]='Ferrada'[RUN] &&
CONTAINSSTRING('Recetas Externas'[Medicamento],"melatonina"))),
"SI","NO")
```

### `Ferrada[SM Metilfenidato]`

Indicador SI/NO: existe al menos una receta vigente (tabla «Recetas Vigentes») cuya descripción de artículo contiene «metilfenidato».

```dax
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"metilfenidato"))),
    "SI","NO")
```

### `Ferrada[SM Mirtazapina]`

Indicador SI/NO: el paciente tiene al menos una receta vigente del establecimiento (tabla «Recetas Vigentes») cuya descripción de artículo contiene «mirtazapina».

```dax
IF(CALCULATE(COUNT('Recetas Vigentes'[RUN]),
FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"mirtazapina"))),
"SI","NO")
```

### `Ferrada[SM OH Dependiente (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «33.- CONSUMO DEPENDIENTE DEL ALCOHOL» está marcada «sí» y el estado (34.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[33.- CONSUMO DEPENDIENTE DEL ALCOHOL],"si")) &&
    (CONTAINSSTRING(PSM[34.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[34.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM OH Dependiente (form)]`

Estado del diagnóstico según formulario PSM médico. Devuelve «Egresado» si hubo un registro con estado «egreso» durante el mes anterior completo; «Activo» si el último formulario con «33.- CONSUMO DEPENDIENTE DEL ALCOHOL»=«sí» está en ingreso/seguimiento; «NO» en caso contrario. El egreso tiene prioridad sobre el activo.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[33.- CONSUMO DEPENDIENTE DEL ALCOHOL],"si")) &&
    (CONTAINSSTRING(PSM[34.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[34.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[33.- CONSUMO DEPENDIENTE DEL ALCOHOL],"si")) &&
    (CONTAINSSTRING(PSM[34.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[34.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   PSM[FECHA ATENCION] >= EOMONTH(TODAY(),-2) + 1 &&
   PSM[FECHA ATENCION] <= EOMONTH(TODAY(),-1) &&
   CONTAINSSTRING('PSM'[34.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM OH Perjudical (form)]`

Estado del diagnóstico según formulario PSM médico. Devuelve «Egresado» si hubo un registro con estado «egreso» durante el mes anterior completo; «Activo» si el último formulario con «31.- CONSUMO PERJUDICIAL DE ALCOHOL»=«sí» está en ingreso/seguimiento; «NO» en caso contrario. El egreso tiene prioridad sobre el activo.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[31.- CONSUMO PERJUDICIAL DE ALCOHOL],"si")) &&
    (CONTAINSSTRING(PSM[32.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[32.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[31.- CONSUMO PERJUDICIAL DE ALCOHOL],"si")) &&
    (CONTAINSSTRING(PSM[32.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[32.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   PSM[FECHA ATENCION] >= EOMONTH(TODAY(),-2) + 1 &&
   PSM[FECHA ATENCION] <= EOMONTH(TODAY(),-1) &&
   CONTAINSSTRING('PSM'[32.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM OH Perjudicial (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «31.- CONSUMO PERJUDICIAL DE ALCOHOL» está marcada «sí» y el estado (32.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[31.- CONSUMO PERJUDICIAL DE ALCOHOL],"si")) &&
    (CONTAINSSTRING(PSM[32.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[32.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM OH y Drogas]`

Indicador SI/NO de diagnóstico. Combina dos fuentes: (a) alguna atención registrada con diagnóstico que contenga «F1», o (b) el último formulario PSM con instrumento médico en que «39.- CONSUMO DE DROGAS Y ALCOHOL»=«sí» y estado en ingreso/seguimiento. Basta una de las dos.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"F1")))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[39.- CONSUMO DE DROGAS Y ALCOHOL],"si")) &&
    (CONTAINSSTRING(PSM[40.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[40.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[39.- CONSUMO DE DROGAS Y ALCOHOL],"si")) &&
    (CONTAINSSTRING(PSM[40.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[40.- ESTADO],"seguimien")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SM OH y Drogas (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «39.- CONSUMO DE DROGAS Y ALCOHOL» está marcada «sí» y el estado (40.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[39.- CONSUMO DE DROGAS Y ALCOHOL],"si")) &&
    (CONTAINSSTRING(PSM[40.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[40.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM OH y Drogas (form)]`

Estado del diagnóstico según formulario PSM médico. Devuelve «Egresado» si hubo un registro con estado «egreso» durante el mes anterior completo; «Activo» si el último formulario con «39.- CONSUMO DE DROGAS Y ALCOHOL»=«sí» está en ingreso/seguimiento; «NO» en caso contrario. El egreso tiene prioridad sobre el activo.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[39.- CONSUMO DE DROGAS Y ALCOHOL],"si")) &&
    (CONTAINSSTRING(PSM[40.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[40.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[39.- CONSUMO DE DROGAS Y ALCOHOL],"si")) &&
    (CONTAINSSTRING(PSM[40.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[40.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   PSM[FECHA ATENCION] >= EOMONTH(TODAY(),-2) + 1 &&
   PSM[FECHA ATENCION] <= EOMONTH(TODAY(),-1) &&
   CONTAINSSTRING('PSM'[40.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Oposicionista desafiante]`

Indicador SI/NO de diagnóstico. Combina dos fuentes: (a) alguna atención registrada con diagnóstico que contenga «F91.3», o (b) el último formulario PSM con instrumento médico en que «69.- ¿TIENE TRASTORNO DISOCIAL DESAFIANTE Y OPOSICIONIS»=«sí» y estado en ingreso/seguimiento. Basta una de las dos.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"F91.3")))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[69.- ¿TIENE TRASTORNO DISOCIAL DESAFIANTE Y OPOSICIONIS],"si")) &&
    (CONTAINSSTRING(PSM[70.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[70.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[69.- ¿TIENE TRASTORNO DISOCIAL DESAFIANTE Y OPOSICIONIS],"si")) &&
    (CONTAINSSTRING(PSM[70.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[70.- ESTADO],"seguimien")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SM Oposicionista desafiante (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «69.- ¿TIENE TRASTORNO DISOCIAL DESAFIANTE Y OPOSICIONIS» está marcada «sí» y el estado (70.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[69.- ¿TIENE TRASTORNO DISOCIAL DESAFIANTE Y OPOSICIONIS],"si")) &&
    (CONTAINSSTRING(PSM[70.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[70.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM Oposicionista desafiante (form)]`

Estado del diagnóstico según formulario PSM médico. Devuelve «Egresado» si hubo un registro con estado «egreso» durante el mes anterior completo; «Activo» si el último formulario con «69.- ¿TIENE TRASTORNO DISOCIAL DESAFIANTE Y OPOSICIONIS»=«sí» está en ingreso/seguimiento; «NO» en caso contrario. El egreso tiene prioridad sobre el activo.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[69.- ¿TIENE TRASTORNO DISOCIAL DESAFIANTE Y OPOSICIONIS],"si")) &&
    (CONTAINSSTRING(PSM[70.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[70.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[69.- ¿TIENE TRASTORNO DISOCIAL DESAFIANTE Y OPOSICIONIS],"si")) &&
    (CONTAINSSTRING(PSM[70.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[70.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   PSM[FECHA ATENCION] >= EOMONTH(TODAY(),-2) + 1 &&
   PSM[FECHA ATENCION] <= EOMONTH(TODAY(),-1) &&
   CONTAINSSTRING('PSM'[70.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Otras (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «65.- OTRAS (TRASTORNOS NO INCLUIDOS EN SECCIÓN)» está marcada «sí» y el estado (66.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[65.- OTRAS (TRASTORNOS NO INCLUIDOS EN SECCIÓN)],"si")) &&
    (CONTAINSSTRING(PSM[66.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[66.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM Otras (form)]`

Estado del diagnóstico según formulario PSM médico. Devuelve «Egresado» si hubo un registro con estado «egreso» durante el mes anterior completo; «Activo» si el último formulario con «65.- OTRAS (TRASTORNOS NO INCLUIDOS EN SECCIÓN)»=«sí» está en ingreso/seguimiento; «NO» en caso contrario. El egreso tiene prioridad sobre el activo.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[65.- OTRAS (TRASTORNOS NO INCLUIDOS EN SECCIÓN)],"si")) &&
    (CONTAINSSTRING(PSM[66.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[66.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[65.- OTRAS (TRASTORNOS NO INCLUIDOS EN SECCIÓN)],"si")) &&
    (CONTAINSSTRING(PSM[66.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[66.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   PSM[FECHA ATENCION] >= EOMONTH(TODAY(),-2) + 1 &&
   PSM[FECHA ATENCION] <= EOMONTH(TODAY(),-1) &&
   CONTAINSSTRING('PSM'[66.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Otras Infancia/Adolescencia]`

Indicador SI/NO de diagnóstico: (a) alguna atención con diagnóstico que contenga alguno de «F91.8» o «F93» o «F94» o «F98», o (b) último formulario PSM médico con «73.- ¿TIENE OTROS TRASTORNOS DEL COMPORTAMIENTO Y DE LA»=«sí» en ingreso/seguimiento.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"F91.8") ||
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"F93") ||
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"F94") ||
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"F98")))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[73.- ¿TIENE OTROS TRASTORNOS DEL COMPORTAMIENTO Y DE LA],"si")) &&
    (CONTAINSSTRING(PSM[74.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[74.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[73.- ¿TIENE OTROS TRASTORNOS DEL COMPORTAMIENTO Y DE LA],"si")) &&
    (CONTAINSSTRING(PSM[74.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[74.- ESTADO],"seguimien")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SM Otras Infancia/Adolescencia (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «73.- ¿TIENE OTROS TRASTORNOS DEL COMPORTAMIENTO Y DE LA» está marcada «sí» y el estado (74.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[73.- ¿TIENE OTROS TRASTORNOS DEL COMPORTAMIENTO Y DE LA],"si")) &&
    (CONTAINSSTRING(PSM[74.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[74.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM Otras Infancia/Adolescencia (form)]`

Estado del diagnóstico según formulario PSM médico. Devuelve «Egresado» si hubo un registro con estado «egreso» durante el mes anterior completo; «Activo» si el último formulario con «73.- ¿TIENE OTROS TRASTORNOS DEL COMPORTAMIENTO Y DE LA»=«sí» está en ingreso/seguimiento; «NO» en caso contrario. El egreso tiene prioridad sobre el activo.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[73.- ¿TIENE OTROS TRASTORNOS DEL COMPORTAMIENTO Y DE LA],"si")) &&
    (CONTAINSSTRING(PSM[74.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[74.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[73.- ¿TIENE OTROS TRASTORNOS DEL COMPORTAMIENTO Y DE LA],"si")) &&
    (CONTAINSSTRING(PSM[74.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[74.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   PSM[FECHA ATENCION] >= EOMONTH(TODAY(),-2) + 1 &&
   PSM[FECHA ATENCION] <= EOMONTH(TODAY(),-1) &&
   CONTAINSSTRING('PSM'[74.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Paroxetina]`

Indicador SI/NO: el paciente tiene al menos una receta vigente del establecimiento (tabla «Recetas Vigentes») cuya descripción de artículo contiene «paroxetina».

```dax
IF(CALCULATE(count('Recetas Vigentes'[RUN]),
FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"paroxetina"))),
"SI","NO")
```

### `Ferrada[SM Pauta llenada]`

Pautas de salud mental aplicadas en los 12 meses cerrados, detectadas en los formularios clínicos de las atenciones: PSC («Cuestionario para Padres PSC»), PSC-Y y GHQ-12 («Cuestionario de Salud de Goldberg»). Devuelve «Sin pauta llenada» o la(s) pauta(s) concatenadas («PSC-Y + GHQ-12»). Reescrita jul-2026: la versión anterior evaluaba PHQ-9/C-SSRS/Goldberg con un texto kilométrico. Los tokens de búsqueda están calibrados contra los nombres RAYEN exactos (los PSC-17 de tamizaje no colisionan).

```dax
VAR _FechaInicio = EOMONTH(TODAY(),-13) + 1
VAR _FechaFinal  = EOMONTH(TODAY(),-1)

VAR _Formularios =
    CALCULATETABLE(
        VALUES(Atenciones[FORMULARIOS CLINICOS]),
        FILTER(ALL(Atenciones),
            Atenciones[RUN] = 'Ferrada'[RUN] &&
            Atenciones[FECHA ATENCION] >= _FechaInicio &&
            Atenciones[FECHA ATENCION] <= _FechaFinal
        )
    )

VAR _PSC =
    COUNTROWS(FILTER(_Formularios,
        CONTAINSSTRING(Atenciones[FORMULARIOS CLINICOS], "para padres psc") )) > 0

VAR _PSCY =
    COUNTROWS(FILTER(_Formularios,
        CONTAINSSTRING(Atenciones[FORMULARIOS CLINICOS], "psc-y") )) > 0

VAR _GHQ =
    COUNTROWS(FILTER(_Formularios,
        CONTAINSSTRING(Atenciones[FORMULARIOS CLINICOS], "salud de goldberg"))) > 0

VAR _Pautas =
    FILTER({
        IF(_PSC,  "PSC"),
        IF(_PSCY, "PSC-Y"),
        IF(_GHQ,  "GHQ-12")
    }, NOT ISBLANK([Value]))

RETURN
IF(
    COUNTROWS(_Pautas) = 0,
    "Sin pauta llenada",
    CONCATENATEX(_Pautas, [Value], " + ")
)
```

### `Ferrada[SM Personalidad]`

Indicador SI/NO de diagnóstico. Combina dos fuentes: (a) alguna atención registrada con diagnóstico que contenga «personalidad», o (b) el último formulario PSM con instrumento médico en que «61.- ¿ TIENE TRASTORNO DE PERSONALIDAD ?»=«sí» y estado en ingreso/seguimiento. Basta una de las dos.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"personalidad")))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[61.- ¿ TIENE TRASTORNO DE PERSONALIDAD ?],"si")) &&
    (CONTAINSSTRING(PSM[62.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[62.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[61.- ¿ TIENE TRASTORNO DE PERSONALIDAD ?],"si")) &&
    (CONTAINSSTRING(PSM[62.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[62.- ESTADO],"seguimien")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SM Personalidad (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «61.- ¿ TIENE TRASTORNO DE PERSONALIDAD ?» está marcada «sí» y el estado (62.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[61.- ¿ TIENE TRASTORNO DE PERSONALIDAD ?],"si")) &&
    (CONTAINSSTRING(PSM[62.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[62.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM Personalidad (form)]`

Estado del diagnóstico según formulario PSM médico. Devuelve «Egresado» si hubo un registro con estado «egreso» durante el mes anterior completo; «Activo» si el último formulario con «61.- ¿ TIENE TRASTORNO DE PERSONALIDAD ?»=«sí» está en ingreso/seguimiento; «NO» en caso contrario. El egreso tiene prioridad sobre el activo.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[61.- ¿ TIENE TRASTORNO DE PERSONALIDAD ?],"si")) &&
    (CONTAINSSTRING(PSM[62.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[62.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[61.- ¿ TIENE TRASTORNO DE PERSONALIDAD ?],"si")) &&
    (CONTAINSSTRING(PSM[62.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[62.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   PSM[FECHA ATENCION] >= EOMONTH(TODAY(),-2) + 1 &&
   PSM[FECHA ATENCION] <= EOMONTH(TODAY(),-1) &&
   CONTAINSSTRING('PSM'[62.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Receta?]`

Receta de psicofármaco vigente SI/NO: OR de 13 indicadores (sertralina, fluoxetina, paroxetina, venlafaxina, escitalopram, trazodona, quetiapina, clorpromazina, alprazolam, clonazepam, diazepam, zopiclona, metilfenidato).

```dax
if('Ferrada'[SM Sertralina]="SI" || 'Ferrada'[SM Fluoxetina]="SI" || 'Ferrada'[SM Paroxetina]="SI" || 'Ferrada'[SM Venlafaxina]="SI" || 'Ferrada'[Escitalopram]="SI" || 'Ferrada'[Trazodona]="SI" || 'Ferrada'[Quetiapina]="SI" || 'Ferrada'[SM Clorpromazina]="SI" || 'Ferrada'[SM Alprazolam]="SI" || 'Ferrada'[SM Clonazepam]="SI" || 'Ferrada'[Diazepam]="SI" || 'Ferrada'[Zopiclona]="SI" || 'Ferrada'[SM Metilfenidato]="SI","SI","NO")
```

### `Ferrada[SM Retraso Mental]`

Indicador SI/NO de diagnóstico. Combina dos fuentes: (a) alguna atención registrada con diagnóstico que contenga «f7», o (b) el último formulario PSM con instrumento médico en que «59.- ¿ TIENE RETRASO MENTAL ?»=«sí» y estado en ingreso/seguimiento. Basta una de las dos.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"f7")))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[59.- ¿ TIENE RETRASO MENTAL ?],"si")) &&
    (CONTAINSSTRING(PSM[60.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[60.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[59.- ¿ TIENE RETRASO MENTAL ?],"si")) &&
    (CONTAINSSTRING(PSM[60.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[60.- ESTADO],"seguimien")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SM Retraso Mental (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «59.- ¿ TIENE RETRASO MENTAL ?» está marcada «sí» y el estado (60.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[59.- ¿ TIENE RETRASO MENTAL ?],"si")) &&
    (CONTAINSSTRING(PSM[60.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[60.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM Retraso Mental (form)]`

Estado del diagnóstico según formulario PSM médico. Devuelve «Egresado» si hubo un registro con estado «egreso» durante el mes anterior completo; «Activo» si el último formulario con «59.- ¿ TIENE RETRASO MENTAL ?»=«sí» está en ingreso/seguimiento; «NO» en caso contrario. El egreso tiene prioridad sobre el activo.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[59.- ¿ TIENE RETRASO MENTAL ?],"si")) &&
    (CONTAINSSTRING(PSM[60.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[60.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[59.- ¿ TIENE RETRASO MENTAL ?],"si")) &&
    (CONTAINSSTRING(PSM[60.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[60.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   PSM[FECHA ATENCION] >= EOMONTH(TODAY(),-2) + 1 &&
   PSM[FECHA ATENCION] <= EOMONTH(TODAY(),-1) &&
   CONTAINSSTRING('PSM'[60.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Rett]`

Indicador SI/NO de diagnóstico. Combina dos fuentes: (a) alguna atención registrada con diagnóstico que contenga «f84.2», o (b) el último formulario PSM con instrumento médico en que «87.- ¿TIENE SÍNDROME DE RETT?»=«sí» y estado en ingreso/seguimiento. Basta una de las dos.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"f84.2")))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[87.- ¿TIENE SÍNDROME DE RETT?],"si")) &&
    (CONTAINSSTRING(PSM[88.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[88.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[87.- ¿TIENE SÍNDROME DE RETT?],"si")) &&
    (CONTAINSSTRING(PSM[88.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[88.- ESTADO],"seguimien")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SM Rett (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «87.- ¿TIENE SÍNDROME DE RETT?» está marcada «sí» y el estado (88.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[87.- ¿TIENE SÍNDROME DE RETT?],"si")) &&
    (CONTAINSSTRING(PSM[88.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[88.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM Rett (form)]`

Estado del diagnóstico según formulario PSM médico. Devuelve «Egresado» si hubo un registro con estado «egreso» durante el mes anterior completo; «Activo» si el último formulario con «87.- ¿TIENE SÍNDROME DE RETT?»=«sí» está en ingreso/seguimiento; «NO» en caso contrario. El egreso tiene prioridad sobre el activo.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[87.- ¿TIENE SÍNDROME DE RETT?],"si")) &&
    (CONTAINSSTRING(PSM[88.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[88.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[87.- ¿TIENE SÍNDROME DE RETT?],"si")) &&
    (CONTAINSSTRING(PSM[88.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[88.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   PSM[FECHA ATENCION] >= EOMONTH(TODAY(),-2) + 1 &&
   PSM[FECHA ATENCION] <= EOMONTH(TODAY(),-1) &&
   CONTAINSSTRING('PSM'[88.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Sertralina]`

Indicador SI/NO: existe receta vigente cuya descripción contiene «sertralina».

```dax
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN]),
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"sertralina")),
    "SI","NO")
```

### `Ferrada[SM Suicidio (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «11.- ¿EPISODIO DE SUICIDIO?» está marcada «sí» y el estado (13.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[11.- ¿EPISODIO DE SUICIDIO?],"si")) &&
    (CONTAINSSTRING(PSM[13.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[13.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM Suicidio (form)]`

Estado del diagnóstico según formulario PSM médico. Devuelve «Egresado» si hubo un registro con estado «egreso» durante el mes anterior completo; «Activo» si el último formulario con «11.- ¿EPISODIO DE SUICIDIO?»=«sí» está en ingreso/seguimiento; «NO» en caso contrario. El egreso tiene prioridad sobre el activo.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[11.- ¿EPISODIO DE SUICIDIO?],"si")) &&
    (CONTAINSSTRING(PSM[13.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[13.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[11.- ¿EPISODIO DE SUICIDIO?],"si")) &&
    (CONTAINSSTRING(PSM[13.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[13.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   PSM[FECHA ATENCION] >= EOMONTH(TODAY(),-2) + 1 &&
   PSM[FECHA ATENCION] <= EOMONTH(TODAY(),-1) &&
   CONTAINSSTRING('PSM'[13.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Suicidio Tipo (form)]`

Devuelve el valor textual de la pregunta «12.- TIPO DE SUICIDIO» del formulario PSM más reciente en que esa pregunta no está vacía (p. ej. tipo o gravedad). BLANK si nunca se ha registrado.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[12.- TIPO DE SUICIDIO]<>"")))

var _Formulario = 
TOPN(1,
    CALCULATETABLE(VALUES(PSM[12.- TIPO DE SUICIDIO]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario)),
    PSM[12.- TIPO DE SUICIDIO])

var _Resultado =

IF(
    _Formulario="",BLANK(),_Formulario)

RETURN
IF(
    _Resultado="",BLANK(),_Resultado)
```

### `Ferrada[SM TDAH]`

TDAH SI/NO: diagnóstico F90 o R46.3 en alguna atención, último formulario PSM médico con pregunta 57 (trastornos hipercinéticos) marcada «sí», o receta vigente de metilfenidato.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"F90") ||
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"R46.3")))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[57.- ¿ TIENE TRASTORNOS HIPERCINÉTICOS, DE LA ACTIVIDAD],"si")) &&
    (CONTAINSSTRING(PSM[58.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[58.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[57.- ¿ TIENE TRASTORNOS HIPERCINÉTICOS, DE LA ACTIVIDAD],"si")) &&
    (CONTAINSSTRING(PSM[58.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[58.- ESTADO],"seguimien")))),
    "SI","NO")

var _Receta = 
IF(
    'Ferrada'[SM Metilfenidato]="SI","SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI" ||
    _Receta="SI",
    "SI","NO")
```

### `Ferrada[SM TDAH (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «57.- ¿ TIENE TRASTORNOS HIPERCINÉTICOS, DE LA ACTIVIDAD» está marcada «sí» y el estado (58.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[57.- ¿ TIENE TRASTORNOS HIPERCINÉTICOS, DE LA ACTIVIDAD],"si")) &&
    (CONTAINSSTRING(PSM[58.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[58.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM TDAH (form)]`

Estado del diagnóstico según formulario PSM médico. Devuelve «Egresado» si hubo un registro con estado «egreso» durante el mes anterior completo; «Activo» si el último formulario con «57.- ¿ TIENE TRASTORNOS HIPERCINÉTICOS, DE LA ACTIVIDAD»=«sí» está en ingreso/seguimiento; «NO» en caso contrario. El egreso tiene prioridad sobre el activo.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[57.- ¿ TIENE TRASTORNOS HIPERCINÉTICOS, DE LA ACTIVIDAD],"si")) &&
    (CONTAINSSTRING(PSM[58.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[58.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[57.- ¿ TIENE TRASTORNOS HIPERCINÉTICOS, DE LA ACTIVIDAD],"si")) &&
    (CONTAINSSTRING(PSM[58.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[58.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   PSM[FECHA ATENCION] >= EOMONTH(TODAY(),-2) + 1 &&
   PSM[FECHA ATENCION] <= EOMONTH(TODAY(),-1) &&
   CONTAINSSTRING('PSM'[58.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM TGD]`

Indicador SI/NO de diagnóstico: (a) alguna atención con diagnóstico que contenga «trastornos generalizados» o «F84.9», o (b) último formulario PSM médico con «63.- ¿ TIENE TRASTORNO GENERALIZADO DEL DESARROLLO ?»=«sí» en ingreso/seguimiento.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"trastornos generalizados") ||
    CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"F84.9")))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[63.- ¿ TIENE TRASTORNO GENERALIZADO DEL DESARROLLO ?],"si")) &&
    (CONTAINSSTRING(PSM[64.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[64.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[63.- ¿ TIENE TRASTORNO GENERALIZADO DEL DESARROLLO ?],"si")) &&
    (CONTAINSSTRING(PSM[64.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[64.- ESTADO],"seguimien")))),
    "SI","NO")

RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SM TGD (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «63.- ¿ TIENE TRASTORNO GENERALIZADO DEL DESARROLLO ?» está marcada «sí» y el estado (64.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[63.- ¿ TIENE TRASTORNO GENERALIZADO DEL DESARROLLO ?],"si")) &&
    (CONTAINSSTRING(PSM[64.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[64.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM TGD (form)]`

Estado del diagnóstico según formulario PSM médico. Devuelve «Egresado» si hubo un registro con estado «egreso» durante el mes anterior completo; «Activo» si el último formulario con «63.- ¿ TIENE TRASTORNO GENERALIZADO DEL DESARROLLO ?»=«sí» está en ingreso/seguimiento; «NO» en caso contrario. El egreso tiene prioridad sobre el activo.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[63.- ¿ TIENE TRASTORNO GENERALIZADO DEL DESARROLLO ?],"si")) &&
    (CONTAINSSTRING(PSM[64.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[64.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[63.- ¿ TIENE TRASTORNO GENERALIZADO DEL DESARROLLO ?],"si")) &&
    (CONTAINSSTRING(PSM[64.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[64.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   PSM[FECHA ATENCION] >= EOMONTH(TODAY(),-2) + 1 &&
   PSM[FECHA ATENCION] <= EOMONTH(TODAY(),-1) &&
   CONTAINSSTRING('PSM'[64.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Venlafaxina]`

Indicador SI/NO: existe al menos una receta vigente (tabla «Recetas Vigentes») cuya descripción de artículo contiene «venlafaxina».

```dax
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"venlafaxina"))),
    "SI","NO")
```

### `Ferrada[SM Violencia]`

Indicador SI/NO de diagnóstico. Combina dos fuentes: (a) alguna atención registrada con diagnóstico que contenga «R45.6», o (b) el último formulario PSM con instrumento médico en que «4.- ¿ ES VÍCTIMA O AGRESOR/A DE VIOLENCIA?»=«sí» y estado en ingreso/seguimiento. Basta una de las dos.

```dax
var _Atenciones = 
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"R45.6")))),
    "SI","NO")

var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[4.- ¿ ES VÍCTIMA O AGRESOR/A DE VIOLENCIA?],"si")) &&
    (CONTAINSSTRING(PSM[5.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[5.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[4.- ¿ ES VÍCTIMA O AGRESOR/A DE VIOLENCIA?],"si")) &&
    (CONTAINSSTRING(PSM[5.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[5.- ESTADO],"seguimien")))),
    "SI","NO")


RETURN

IF(
    _Atenciones="SI" ||
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SM Violencia (fecha)]`

Fecha del último formulario de salud mental (tabla PSM) llenado con instrumento médico en que la pregunta «4.- ¿ ES VÍCTIMA O AGRESOR/A DE VIOLENCIA?» está marcada «sí» y el estado (5.- ESTADO) es «ingreso» o «seguimiento». Es la fecha que respalda el diagnóstico correspondiente.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[4.- ¿ ES VÍCTIMA O AGRESOR/A DE VIOLENCIA?],"si")) &&
    (CONTAINSSTRING(PSM[5.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[5.- ESTADO],"seguimien")))))

RETURN

_FechaFormulario
```

### `Ferrada[SM Violencia (form)]`

Estado del diagnóstico según formulario PSM médico. Devuelve «Egresado» si hubo un registro con estado «egreso» durante el mes anterior completo; «Activo» si el último formulario con «4.- ¿ ES VÍCTIMA O AGRESOR/A DE VIOLENCIA?»=«sí» está en ingreso/seguimiento; «NO» en caso contrario. El egreso tiene prioridad sobre el activo.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[4.- ¿ ES VÍCTIMA O AGRESOR/A DE VIOLENCIA?],"si")) &&
    (CONTAINSSTRING(PSM[5.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[5.- ESTADO],"seguimien")))))

var _Formulario = 
IF(
    CALCULATE(COUNT(PSM[RUN]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario &&
    (CONTAINSSTRING(PSM[INSTRUMENTO],"médico") &&
    CONTAINSSTRING(PSM[4.- ¿ ES VÍCTIMA O AGRESOR/A DE VIOLENCIA?],"si")) &&
    (CONTAINSSTRING(PSM[5.- ESTADO],"ingreso") ||
    CONTAINSSTRING(PSM[5.- ESTADO],"seguimien")))),
    "SI","NO")

var _Activo =

IF(
    _Formulario="SI",
    "SI","NO")

var _Egreso = 
IF(
   CALCULATE(COUNT('PSM'[RUN]),
   FILTER(ALL('PSM'),'PSM'[RUN]='Ferrada'[RUN] &&
   PSM[FECHA ATENCION] >= EOMONTH(TODAY(),-2) + 1 &&
   PSM[FECHA ATENCION] <= EOMONTH(TODAY(),-1) &&
   CONTAINSSTRING('PSM'[5.- ESTADO],"egreso"))),"SI","NO")

RETURN
IF(
    _Egreso="SI","Egresado",
IF(
    _Activo="SI","Activo",
    "NO"))
```

### `Ferrada[SM Violencia Tipo (form)]`

Devuelve el valor textual de la pregunta «6.- TIPO DE VIOLENCIA» del formulario PSM más reciente en que esa pregunta no está vacía (p. ej. tipo o gravedad). BLANK si nunca se ha registrado.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[6.- TIPO DE VIOLENCIA]<>"")))

var _Formulario = 
TOPN(1,
    CALCULATETABLE(VALUES(PSM[6.- TIPO DE VIOLENCIA]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario)),
    PSM[6.- TIPO DE VIOLENCIA])

var _Resultado =

IF(
    _Formulario="",BLANK(),_Formulario)

RETURN
IF(
    _Resultado="",BLANK(),_Resultado)
```

### `Ferrada[SM Violencia Victima o Agresor (form)]`

Devuelve el valor textual de la pregunta «7.- EN LA VIOLENCIA ES» del formulario PSM más reciente en que esa pregunta no está vacía (p. ej. tipo o gravedad). BLANK si nunca se ha registrado.

```dax
var _FechaFormulario = 
LASTDATE(
    CALCULATETABLE(VALUES(PSM[FECHA ATENCION]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[7.- EN LA VIOLENCIA ES]<>"")))

var _Formulario = 
TOPN(1,
    CALCULATETABLE(VALUES(PSM[7.- EN LA VIOLENCIA ES]),
    FILTER(ALL(PSM),PSM[RUN]='Ferrada'[RUN] &&
    PSM[FECHA ATENCION] = _FechaFormulario)),
    PSM[7.- EN LA VIOLENCIA ES])

var _Resultado =

IF(
    _Formulario="",BLANK(),_Formulario)

RETURN
IF(
    _Resultado="",BLANK(),_Resultado)
```

### `Ferrada[SM último control (fecha)]`

Fecha del último control de salud mental (actividad «controles salud mental»).

```dax
var _FechaAt = 
LASTDATE(
CALCULATETABLE(VALUES('Atenciones'[FECHA ATENCION]),
FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN]),
CONTAINSSTRING('Atenciones'[ACTIVIDADES],"controles salud mental")))

RETURN

    _FechaAt
```

### `Ferrada[SM último control (instrumento)]`

Instrumento (profesional) del último control de salud mental.

```dax
var _FechaAt = 
LASTDATE(
CALCULATETABLE(VALUES('Atenciones'[FECHA ATENCION]),
FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN]),
CONTAINSSTRING('Atenciones'[ACTIVIDADES],"controles salud mental")))
var _InstrumentoAt = 
TOPN(1,
CALCULATETABLE(VALUES('Atenciones'[INSTRUMENTO]),
FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN]),
'Atenciones'[FECHA ATENCION]=_FechaAt),
'Atenciones'[INSTRUMENTO],ASC)

RETURN

_InstrumentoAt
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

### `Ferrada[Trazodona]`

Indicador SI/NO: existe receta vigente cuya descripción contiene «Trazodona».

```dax
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),
    'Recetas Vigentes'[RUN]='Ferrada'[RUN]),
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"Trazodona")),
    "SI","NO")
```

### `Ferrada[Trazodona (Ext)]`

Indicador SI/NO: existe receta externa registrada (tabla «Recetas Externas») cuyo medicamento contiene «trazodona».

```dax
IF(CALCULATE(COUNT('Recetas Externas'[RUN]),
FILTER(ALL('Recetas Externas'),'Recetas Externas'[RUN]='Ferrada'[RUN]),
CONTAINSSTRING('Recetas Externas'[Medicamento],"trazodona")),
"SI","NO")
```

### `Ferrada[Zopiclona]`

Indicador SI/NO: existe receta vigente cuya descripción contiene «zopiclona».

```dax
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN]),
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"zopiclona")),
    "SI","NO")
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
