# Especificación de la página «Respiratorio»

Extraído automáticamente de la capa de reporte (PBIR) y del modelo semántico (TMDL).

**28 visuales · 49 campos distintos del modelo.**

## Filtros de página

- `Ferrada[Pertenece a SALA]` (Categorical) → ['SI']
- `Ferrada[Sexo]` (Categorical) → ['Hombre', 'Mujer']

## Visuales

### 1. EPOC Control — `slicer`

- **Values:** `Ferrada[SALA EPOC Control]`

### 2. Número de controles y consultas (por actividad) por mes en los últimos 12 meses — `clusteredColumnChart`

- **Category:** `?[Año]` — «FECHA ATENCION Año»
- **Category:** `?[Mes]` — «FECHA ATENCION Mes»
- **Series:** `Atenciones[Respiratorio (act)]`
- **Tooltips:** MIN(`Atenciones[FECHA ATENCION]`) — «Primera fecha: FECHA ATENCION»
- **Y:** COUNT(`Atenciones[Respiratorio (act)]`) — «Recuento de Respiratorio (act)»

### 3. SBOR Grado — `slicer`

- **Values:** `Ferrada[SALA SBOR Gravedad]` — «SBOR Gravedad»

### 4. ASMA Control — `slicer`

- **Values:** `Ferrada[SALA ASMA Control]`

### 5. ¿Activo 12m? — `slicer`

- **Values:** `Ferrada[¿Atendido en 12m?]` — «Atendido en 12m?»

### 6. Total de personas — `card`

- **Values:** DISTINCTCOUNT(`Ferrada[RUN]`) — «Nº de personas»

### 7. Migr o Origin — `slicer`

- **Values:** `Ferrada[¿Originario o Migrante?]`

### 8. O2 depen — `slicer`

- **Values:** `Ferrada[SALA O2 Dependiente]`

### 9. Asisten Vent — `slicer`

- **Values:** `Ferrada[SALA Asistencia Ventilatoria]` — «Asistencia Vent?»

### 10. Estado — `slicer`

- **Values:** `Ferrada[Estado]`

### 11. ASMA Grado — `slicer`

- **Values:** `Ferrada[SALA ASMA Gravedad]` — «ASMA Gravedad»

### 12. Sexo — `slicer`

- **Values:** `Ferrada[Sexo]`

### 13. Años — `slicer`

- **Values:** `Ferrada[Edad]` — «Edad Años»

### 14. Sector — `slicer`

- **Values:** `Ferrada[Sector]`

### 15. Situación — `slicer`

- **Values:** `Ferrada[Situación]`

### 16. ¿Ingresado? — `slicer`

- **Values:** `Ferrada[SALA Ingresado]` — «SALA Ingresado?»

### 17. Otras Respi — `slicer`

- **Values:** `Ferrada[SALA Otras Respi]`

### 18. SBOR — `slicer`

- **Values:** `Ferrada[SALA SBOR]` — «SBOR»

### 19. EPOC Tipo — `slicer`

- **Values:** `Ferrada[SALA EPOC Tipo]` — «EPOC T Otros»

### 20. Fibrosis Q — `slicer`

- **Values:** `Ferrada[SALA FQ]`

### 21. Meses — `slicer`

- **Values:** `Ferrada[Meses]` — «Edad Meses»

### 22. Mapa de Georreferenciación — `esriVisual`

- **Color:** `Ferrada[Sector]`
- **Location:** `Ferrada[Dirección Completa]`
- **Tooltips:** `Ferrada[RUN]`
- **Tooltips:** `Ferrada[Nombre completo]`
- **Tooltips:** `Ferrada[Edad]` — «Edad1»
- **Tooltips:** `Ferrada[Sexo]`

### 23. ASMA — `slicer`

- **Values:** `Ferrada[SALA ASMA]` — «ASMA»

### 24. (sin título) — `pieChart`

- **Category:** `Ferrada[SALA EPOC Control]` — «Control EPOC»
- **Y:** DISTINCTCOUNT(`Ferrada[RUN]`) — «Recuento de RUN1»

### 25. ¿Activo SALA? — `slicer`

- **Values:** `Ferrada[SALA Activo 12m (act)]`

### 26. EPOC — `slicer`

- **Values:** `Ferrada[SALA EPOC]` — «EPOC»

### 27. (sin título) — `pieChart`

- **Category:** `Ferrada[SALA ASMA Control]` — «Control ASMA»
- **Y:** DISTINCTCOUNT(`Ferrada[RUN]`) — «Recuento de RUN1»

### 28. Población Respiratorio — `tableEx`

- **Values:** `Ferrada[Tipo de identificación]`
- **Values:** `Ferrada[RUN]` — «Número»
- **Values:** `Ferrada[Nombre Social]`
- **Values:** `Ferrada[Nombre completo]`
- **Values:** `Ferrada[Sexo]`
- **Values:** `Ferrada[Fecha Nacimiento]` — «Fecha Nacimiento1»
- **Values:** `Ferrada[Edad]`
- **Values:** `Ferrada[Meses]`
- **Values:** `Ferrada[Días]`
- **Values:** `Ferrada[Sector]`
- **Values:** `Ferrada[¿Originario o Migrante?]`
- **Values:** `Ferrada[Dirección Completa]`
- **Values:** `Ferrada[Celular]`
- **Values:** `Ferrada[Mail]`
- **Values:** `Ferrada[Estado]`
- **Values:** `Ferrada[Situación]`
- **Values:** `Ferrada[Motivo Pasivación]`
- **Values:** `Ferrada[Fecha Pasivación]`
- **Values:** `Ferrada[SALA Ingresado]` — «¿Ingresado?»
- **Values:** `Ferrada[SALA Activo 12m (act)]` — «¿Activo SALA 12m?»
- **Values:** `Ferrada[SALA SBOR]` — «SBOR»
- **Values:** `Ferrada[SALA SBOR Gravedad]` — «SBOR Gravedad»
- **Values:** `Ferrada[SALA ASMA]` — «ASMA»
- **Values:** `Ferrada[SALA ASMA Gravedad]` — «ASMA Gravedad»
- **Values:** `Ferrada[SALA ASMA Control]` — «ASMA Control»
- **Values:** `Ferrada[SALA EPOC]` — «EPOC»
- **Values:** `Ferrada[SALA EPOC Tipo]` — «EPOC T»
- **Values:** `Ferrada[SALA EPOC Control]` — «EPOC Control»
- **Values:** `Ferrada[SALA Otras Respi]` — «Otras Respi»
- **Values:** `Ferrada[SALA O2 Dependiente]` — «O2 Dependiente»
- **Values:** `Ferrada[SALA Asistencia Ventilatoria]` — «Asistencia Ventilatoria»
- **Values:** `Ferrada[SALA Asistencia Ventilatoria (Tipo)]` — «Asistencia Ventilatoria (Tipo)»
- **Values:** `Ferrada[SALA FQ]` — «FQ»
- **Values:** `Ferrada[SALA Espirometría Vigente 12m (act)]` — «Espirometría Vigente 12m (act)»
- **Values:** `Ferrada[SALA/OTROS Encuesta Calidad de vida resultado]` — «Encuesta Calidad de vida resultado (histórico)»
- **Values:** `Ferrada[SALA Budesonida]` — «Budesonida1»
- **Values:** `Ferrada[SM Fluticasona]` — «Fluticasona»
- **Values:** `Ferrada[SALA Bromuro]` — «Bromuro1»
- **Values:** `Ferrada[Salbutamol]`
- **Values:** `Ferrada[Desloratadina]`
- **Values:** `Ferrada[SALA Loratadina]` — «Loratadina»
- **Values:** `Ferrada[Prednisona]`
- **Values:** `Ferrada[SALA Control último (fecha)]` — «Último control (fecha)»
- **Values:** `Ferrada[SALA Control último (Instrumento)]` — «Último control (Instrumento)»
- **Values:** SUM(`Ferrada[Trans]`) — «Suma de Trans»

---

## Anexo: lógica de los campos usados

### `Atenciones[FECHA ATENCION]`

_Campo base (no calculado): proviene de la carga de Power Query._

### `Atenciones[Respiratorio (act)]`

Clasifica la atención respiratoria: «KTR» (kinesioterapia), «Control» (control sala IRA), «Consulta» (consulta sala IRA); si no, BLANK.

```dax
SWITCH(
    TRUE(),
    CONTAINSSTRING(Atenciones[ACTIVIDADES],"kinesioter"),"KTR",
    CONTAINSSTRING(Atenciones[ACTIVIDADES],"control sala (ira"),"Control",
    CONTAINSSTRING(Atenciones[ACTIVIDADES],"consulta sala (ira"),"Consulta",
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

### `Ferrada[Desloratadina]`

Indicador SI/NO: existe receta vigente cuya descripción contiene «desloratadina».

```dax
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
        FILTER(
            'Recetas Vigentes',
            'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
            CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"desloratadina"
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

### `Ferrada[Fecha Pasivación]`

Trae por cruce de RUN el valor de «FECHA PASIVACION» desde la tabla «Inscritos» hacia esta tabla (LOOKUPVALUE). Copia directa, sin transformación.

```dax
LOOKUPVALUE(Inscritos[FECHA PASIVACION],Inscritos[RUN],'Ferrada'[RUN])
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

### `Ferrada[Prednisona]`

Indicador SI/NO: el paciente tiene al menos una receta vigente del establecimiento (tabla «Recetas Vigentes») cuya descripción de artículo contiene «predniso».

```dax
IF(CALCULATE(count('Recetas Vigentes'[RUN]),
FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"predniso"))),
"SI","NO")
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

### `Ferrada[SALA ASMA Control]`

Estado de control del asma (pregunta 13) según el último formulario «Otros y Respi» médico con asma=«sí». BLANK si no hay.

```dax
var _Fecha = 
LASTDATE(
CALCULATETABLE(VALUES('Otros y Respi'[FECHA ATENCION]),
FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
(CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médico") &&
CONTAINSSTRING('Otros y Respi'[9.- ¿PADECE DE ASMA BRONQUIAL?],"si")) &&
'Otros y Respi'[13.- ESTADO DE CONTROL ASMA]<>"")))

var _Formularios =
TOPN(1,
CALCULATETABLE(VALUES('Otros y Respi'[13.- ESTADO DE CONTROL ASMA]),
FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
'Otros y Respi'[FECHA ATENCION] = _Fecha)),
'Otros y Respi'[13.- ESTADO DE CONTROL ASMA],DESC)

var _Resultado = 
IF(_Formularios="",BLANK(),_Formularios
)

RETURN

IF(
    _Resultado="",BLANK(),_Resultado)
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

### `Ferrada[SALA Activo 12m (act)]`

Actividad en sala 12m: «SI» si tuvo control de sala IRA/ERA en los últimos 12 meses (DATEDIFF 1-12 meses hacia atrás).

```dax
IF(
    CALCULATE(count('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    (DATEDIFF(Atenciones[FECHA ATENCION],TODAY(),MONTH) > 0 &&
    DATEDIFF(Atenciones[FECHA ATENCION],TODAY(),MONTH) <= 12) &&
    CONTAINSSTRING('Atenciones'[ACTIVIDADES],"control sala (ira"))),
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

### `Ferrada[SALA Asistencia Ventilatoria (Tipo)]`

Tipo de asistencia ventilatoria (pregunta 27) del último formulario médico válido. BLANK si no hay.

```dax
var _Fecha = 
LASTDATE(
CALCULATETABLE(VALUES('Otros y Respi'[FECHA ATENCION]),
FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
(CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médico") &&
CONTAINSSTRING('Otros y Respi'[26.- ¿NECESITA ASISTENCIA VENTILATORIA?],"si")) &&
'Otros y Respi'[27.- ASISTENCIA VENTILATORIA]<>"" &&
(CONTAINSSTRING('Otros y Respi'[28.- ESTADO ASISTENCIA VENTILATORIA],"ingreso") ||
CONTAINSSTRING('Otros y Respi'[28.- ESTADO ASISTENCIA VENTILATORIA],"seguimiento")))))

var _Formularios = 
CALCULATETABLE(VALUES('Otros y Respi'[27.- ASISTENCIA VENTILATORIA]),
FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
'Otros y Respi'[FECHA ATENCION] = _Fecha &&
(CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médico") &&
CONTAINSSTRING('Otros y Respi'[26.- ¿NECESITA ASISTENCIA VENTILATORIA?],"si")) &&
'Otros y Respi'[27.- ASISTENCIA VENTILATORIA]<>"" &&
(CONTAINSSTRING('Otros y Respi'[28.- ESTADO ASISTENCIA VENTILATORIA],"ingreso") ||
CONTAINSSTRING('Otros y Respi'[28.- ESTADO ASISTENCIA VENTILATORIA],"seguimiento"))))

var _Resultado = 
IF(
    _Formularios="",BLANK(),_Formularios)

RETURN

IF(
    _Resultado="",BLANK(),_Resultado)
```

### `Ferrada[SALA Bromuro]`

Indicador SI/NO: existe al menos una receta vigente (tabla «Recetas Vigentes») cuya descripción de artículo contiene «bromuro».

```dax
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"bromuro"))),
    "SI","NO")
```

### `Ferrada[SALA Budesonida]`

Indicador SI/NO: existe al menos una receta vigente (tabla «Recetas Vigentes») cuya descripción de artículo contiene «budesonid».

```dax
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"budesonid"))),
    "SI","NO")
```

### `Ferrada[SALA Control último (Instrumento)]`

Instrumento del último control de sala IRA/ERA.

```dax
var _Fecha = 
LASTDATE(
    CALCULATETABLE(VALUES(Atenciones[FECHA ATENCION]),
    FILTER(ALL(Atenciones),Atenciones[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING(Atenciones[ACTIVIDADES],"control sala (ira"))))

RETURN
TOPN(1,
    CALCULATETABLE(VALUES('Atenciones'[INSTRUMENTO]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    Atenciones[FECHA ATENCION]=_Fecha &&
    CONTAINSSTRING('Atenciones'[ACTIVIDADES],"control sala"))),
    Atenciones[INSTRUMENTO],DESC)
```

### `Ferrada[SALA Control último (fecha)]`

Fecha del último control de sala IRA/ERA.

```dax
LASTDATE(
    CALCULATETABLE(VALUES('Atenciones'[FECHA ATENCION]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    CONTAINSSTRING('Atenciones'[ACTIVIDADES],"control sala (ira"))))
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

### `Ferrada[SALA EPOC Control]`

Del último formulario «Otros y Respi» médico válido de EPOC (padece EPOC=«sí», tipo y estado de control no vacíos, estado ingreso/seguimiento) devuelve «19.- ESTADO DE CONTROL EPOC». Solo se muestra si [SALA EPOC]=«SI»; si no, BLANK.

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
CALCULATETABLE(VALUES('Otros y Respi'[19.- ESTADO DE CONTROL EPOC]),
FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
'Otros y Respi'[FECHA ATENCION] = _Fecha &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Otros y Respi'[14.- ¿PADECE ENFERMEDAD PULMONAR CRONICA?],"si")) &&
    'Otros y Respi'[16.- TIPO EPOC]<>"" &&
    'Otros y Respi'[19.- ESTADO DE CONTROL EPOC]<>"" &&
    (CONTAINSSTRING('Otros y Respi'[17.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[17.- ESTADO],"seguimiento")))),
'Otros y Respi'[19.- ESTADO DE CONTROL EPOC],DESC)

var _Resultado = 
IF(_Formularios="",BLANK(),_Formularios)

RETURN

IF(
    'Ferrada'[SALA EPOC]="SI",
IF(
    _Resultado="",BLANK(),_Resultado))
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

### `Ferrada[SALA Espirometría Vigente 12m (act)]`

Espirometría vigente SI/NO: actividad de espirometría dentro de los últimos 12 meses.

```dax
IF(
    CALCULATE(COUNT('Atenciones'[RUN]),
    FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
    (DATEDIFF(Atenciones[FECHA ATENCION],TODAY(),MONTH) > 0 &&
    DATEDIFF(Atenciones[FECHA ATENCION],TODAY(),MONTH) <= 12 ) &&
    CONTAINSSTRING('Atenciones'[ACTIVIDADES],"espirometr"))),
    "SI","NO")
```

### `Ferrada[SALA FQ]`

Fibrosis quística SI/NO: diagnóstico E84 en atención médica o Estratificación, o último formulario FQ válido en ingreso/seguimiento.

```dax
var _Atenciones = 
IF(
CALCULATE(count('Atenciones'[RUN]),
FILTER(ALL('Atenciones'),'Atenciones'[RUN]='Ferrada'[RUN] &&
(CONTAINSSTRING(Atenciones[INSTRUMENTO],"médic") &&
CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"E84")))),
"SI","NO")

var _Estratificacion = 
IF(
CALCULATETABLE(VALUES(Estratificacion[Diagnósticos]),
FILTER(ALL(Estratificacion),Estratificacion[RUN]='Ferrada'[RUN] &&
CONTAINSSTRING(Estratificacion[Diagnósticos],"E84"))),
"SI","NO")

var _Fecha = 
LASTDATE(
    CALCULATETABLE(VALUES('Otros y Respi'[FECHA ATENCION]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Otros y Respi'[30.- ¿PADECE DE FIBROSIS QUISTICA?],"si")) &&
    (CONTAINSSTRING('Otros y Respi'[31.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[31.- ESTADO],"seguimiento")))))

var _Formulario = 
IF(
    CALCULATE(COUNT('Otros y Respi'[RUN]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    'Otros y Respi'[FECHA ATENCION]=_Fecha &&
    (CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
    CONTAINSSTRING('Otros y Respi'[30.- ¿PADECE DE FIBROSIS QUISTICA?],"si")) &&
    (CONTAINSSTRING('Otros y Respi'[31.- ESTADO],"ingreso") ||
    CONTAINSSTRING('Otros y Respi'[31.- ESTADO],"seguimiento")))),
    "SI","NO")


RETURN

IF(
    _Atenciones="SI" ||
    _Estratificacion="SI" ||
    _Formulario="SI",
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

### `Ferrada[SALA Loratadina]`

Indicador SI/NO: el paciente tiene al menos una receta vigente del establecimiento (tabla «Recetas Vigentes») cuya descripción de artículo contiene «loratadina».

```dax
IF(CALCULATE(count('Recetas Vigentes'[RUN]),
FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"loratadina"))),
"SI","NO")
```

### `Ferrada[SALA O2 Dependiente]`

Oxígeno-dependiente SI/NO: último formulario «Otros y Respi» con pregunta 23 marcada «sí» en ingreso/seguimiento.

```dax
var _Fecha = 
LASTDATE(
CALCULATETABLE(VALUES('Otros y Respi'[FECHA ATENCION]),
FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
(CONTAINSSTRING('Otros y Respi'[23.- ¿ES OXIGENO DEPENDIENTE?],"si")) &&
(CONTAINSSTRING('Otros y Respi'[24.- ESTADO],"ingreso") ||
CONTAINSSTRING('Otros y Respi'[24.- ESTADO],"seguimiento")))))

var _Formulario = 
IF(
CALCULATE(COUNT('Otros y Respi'[RUN]),
FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
'Otros y Respi'[FECHA ATENCION] = _Fecha &&
(CONTAINSSTRING('Otros y Respi'[23.- ¿ES OXIGENO DEPENDIENTE?],"si")) &&
(CONTAINSSTRING('Otros y Respi'[24.- ESTADO],"ingreso") ||
CONTAINSSTRING('Otros y Respi'[24.- ESTADO],"seguimiento")))),
"SI","NO")

RETURN

IF(
    _Formulario="SI",
    "SI","NO")
```

### `Ferrada[SALA Otras Respi]`

Otras enfermedades respiratorias SI/NO: último formulario «Otros y Respi» médico con la pregunta 53 marcada «sí» en ingreso/seguimiento.

```dax
var _Fecha = 
LASTDATE(
CALCULATETABLE(VALUES('Otros y Respi'[FECHA ATENCION]),
FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
(CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
CONTAINSSTRING('Otros y Respi'[53.- ¿PADECE OTRAS ENFERMEDADES RESPIRATORIAS?],"si")) &&
(CONTAINSSTRING('Otros y Respi'[55.- ESTADO],"ingreso") ||
CONTAINSSTRING('Otros y Respi'[55.- ESTADO],"seguimiento")))))

var _Formulario = 
IF(
CALCULATE(COUNT('Otros y Respi'[RUN]),
FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
'Otros y Respi'[FECHA ATENCION] = _Fecha &&
(CONTAINSSTRING('Otros y Respi'[INSTRUMENTO],"médic") &&
CONTAINSSTRING('Otros y Respi'[53.- ¿PADECE OTRAS ENFERMEDADES RESPIRATORIAS?],"si")) &&
(CONTAINSSTRING('Otros y Respi'[55.- ESTADO],"ingreso") ||
CONTAINSSTRING('Otros y Respi'[55.- ESTADO],"seguimiento")))),
"SI","NO")

RETURN

IF(
    _Formulario="SI",
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

### `Ferrada[SALA/OTROS Encuesta Calidad de vida resultado]`

Resultado más reciente de la encuesta de calidad de vida (pregunta 99 de «Otros y Respi»), sin límite de tiempo. BLANK si nunca.

```dax
VAR _Fecha = 
LASTDATE(
    CALCULATETABLE(VALUES('Otros y Respi'[FECHA ATENCION]),
        FILTER(
            'Otros y Respi',
            'Otros y Respi'[RUN] = Ferrada[RUN] &&
            'Otros y Respi'[99.- RESULTADO ENCUESTA CALIDAD DE VIDA]<>""
        )
    )
)

VAR _Resultado = 
TOPN(1,
    CALCULATETABLE(VALUES('Otros y Respi'[99.- RESULTADO ENCUESTA CALIDAD DE VIDA]),
        FILTER(
            'Otros y Respi',
            'Otros y Respi'[RUN] = Ferrada[RUN] &&
            'Otros y Respi'[FECHA ATENCION] = _Fecha
        )
    ),'Otros y Respi'[99.- RESULTADO ENCUESTA CALIDAD DE VIDA]
)

RETURN

IF(
    _Resultado="",BLANK(),_Resultado
)
```

### `Ferrada[SM Fluticasona]`

Indicador SI/NO: el paciente tiene al menos una receta vigente del establecimiento (tabla «Recetas Vigentes») cuya descripción de artículo contiene «fluticasona».

```dax
IF(CALCULATE(count('Recetas Vigentes'[RUN]),
FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN] &&
CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"fluticasona"))),
"SI","NO")
```

### `Ferrada[Salbutamol]`

Indicador SI/NO: existe receta vigente cuya descripción contiene «Salbutamol».

```dax
IF(
    CALCULATE(count('Recetas Vigentes'[RUN]),
    FILTER(ALL('Recetas Vigentes'),'Recetas Vigentes'[RUN]='Ferrada'[RUN]),
    CONTAINSSTRING('Recetas Vigentes'[DESCRIPCION ARTICULO],"Salbutamol")),
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
