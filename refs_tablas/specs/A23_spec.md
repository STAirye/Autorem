# Especificación de la página «A23»

Extraído automáticamente de la capa de reporte (PBIR) y del modelo semántico (TMDL).

**7 visuales · 51 campos distintos del modelo.**

_Sin filtros a nivel de página._

## Visuales

### 1. REM A23 — `tableEx`

- **Values:** `Ferrada[RUN]`
- **Values:** `Ferrada[REMA23 Autocuidado]`
- **Values:** `Ferrada[REMA23 Bronquitis Aguda]`
- **Values:** `Ferrada[REMA23 Campaña Invierno]`
- **Values:** `Ferrada[REMA23 Consulta SALA Kine (act)]`
- **Values:** `Ferrada[REMA23 Control SALA Kine (act)]`
- **Values:** `Ferrada[REMA23 Control SALA Med (act)]`
- **Values:** `Ferrada[REMA23 Coqueluche]`
- **Values:** `Ferrada[REMA23 Edu Integral Sala]`
- **Values:** `Ferrada[REMA23 Educación Antitabaco]`
- **Values:** `Ferrada[REMA23 Encuesta calidad de vida]`
- **Values:** `Ferrada[REMA23 EPOC Exacerbado]`
- **Values:** `Ferrada[REMA23 Espirometría (act)]`
- **Values:** `Ferrada[REMA23 Influenza]`
- **Values:** `Ferrada[REMA23 Inhaloterapia]`
- **Values:** `Ferrada[REMA23 KTR]`
- **Values:** `Ferrada[REMA23 Ira Alta]`
- **Values:** `Ferrada[REMA23 Morbi respiratoria]`
- **Values:** `Ferrada[REMA23 Otras]`
- **Values:** `Ferrada[REMA23 Neumonia]`
- **Values:** `Ferrada[REMA23 Seguimiento Eu]`
- **Values:** `Ferrada[REMA23 Seguimiento Kine]`
- **Values:** `Ferrada[REMA23 VDI Respi]`
- **Values:** `Ferrada[REMA23 Vida Saludable]`
- **Values:** `Ferrada[Nombre completo]`
- **Values:** `Ferrada[Sexo]`
- **Values:** `Ferrada[Sector]`
- **Values:** `Ferrada[¿Originario o Migrante?]`
- **Values:** `Ferrada[Nacionalidad]`
- **Values:** `Ferrada[Pueblo Originario]`
- **Values:** `Ferrada[Situación]`
- **Values:** `Ferrada[Estado]`
- **Values:** `Ferrada[Motivo Pasivación]`
- **Values:** `Ferrada[Última atención (instrumento)]`
- **Values:** `Ferrada[SALA Ingresado]`
- **Values:** `Ferrada[SALA SBOR]`
- **Values:** `Ferrada[SALA SBOR Gravedad]`
- **Values:** `Ferrada[SALA ASMA]`
- **Values:** `Ferrada[SALA ASMA Gravedad]`
- **Values:** `Ferrada[SALA EPOC]`
- **Values:** `Ferrada[SALA EPOC Tipo]`
- **Values:** `Ferrada[SALA FQ]`
- **Values:** `Ferrada[SALA Otras Respi]`
- **Values:** MIN(`Ferrada[Edad]`) — «Mín. de Edad»
- **Values:** `Ferrada[REMA23 Rehab Conti]`
- **Values:** `Ferrada[REMA23 Rehab Ses Act Fca]`
- **Values:** `Ferrada[REMA23 Rehab Ses Educ]`
- **Values:** `Ferrada[¿Atendido 1 mes?]`
- **Values:** `Ferrada[REMA23 Inasistentes]`

### 2. (sin título) — `slicer`

- **Values:** `Ferrada[Pertenece a SALA]`

### 3. (sin título) — `slicer`

- **Values:** `Ferrada[Estado]`

### 4. (sin título) — `slicer`

- **Values:** `Ferrada[¿Atendido 1 mes?]`

### 5. (sin título) — `slicer`

- **Values:** `Ferrada[Situación]`

### 6. (sin título) — `slicer`

- **Values:** `Ferrada[Validado]`

### 7. Total de personas — `card`

- **Values:** DISTINCTCOUNT(`Ferrada[RUN]`) — «Nº de personas»

---

## Anexo: lógica de los campos usados

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

### `Ferrada[Pueblo Originario]`

Trae por cruce de RUN el valor de «PUEBLO INDIG» desde la tabla «Inscritos» hacia esta tabla (LOOKUPVALUE). Copia directa, sin transformación.

```dax
LOOKUPVALUE(Inscritos[PUEBLO INDIG],Inscritos[RUN],'Ferrada'[RUN])
```

### `Ferrada[REMA23 Autocuidado]`

Indicador REMA mensual: actividad de autocuidado en control de sala durante el mes anterior.

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            (CONTAINSSTRING('Atenciones'[ACTIVIDADES],"autocuidado") && 
            CONTAINSSTRING('Atenciones'[ACTIVIDADES],"control sala"))))

RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Bronquitis Aguda]`

Indicador SI/NO mensual (REMA): tuvo al menos una atención durante el mes anterior completo donde [DIAGNOSTICOS] contiene «J20».

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            CONTAINSSTRING(Atenciones[DIAGNOSTICOS],"J20")
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Campaña Invierno]`

Indicador REMA mensual: actividad de campaña de invierno (IRA alta, SBO, neumonía, exacerbación de asma, EPOC, otras respiratorias) durante el mes anterior.

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            (
                CONTAINSSTRING(Atenciones[ACTIVIDADES],"ira alta") ||
                CONTAINSSTRING(Atenciones[ACTIVIDADES],"s.b.o") ||
                CONTAINSSTRING(Atenciones[ACTIVIDADES],"neumon") ||
                CONTAINSSTRING(Atenciones[ACTIVIDADES],"exacerbación asma") ||
                CONTAINSSTRING(Atenciones[ACTIVIDADES],"epoc") ||
                CONTAINSSTRING(Atenciones[ACTIVIDADES],"otras respir")
            )
        )
    )

RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Consulta SALA Kine (act)]`

Indicador SI/NO mensual (REMA): atención del mes anterior donde [ACTIVIDADES] contiene «consulta sala (ira» y [INSTRUMENTO] contiene «kine».

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            (CONTAINSSTRING('Atenciones'[ACTIVIDADES],"consulta sala (ira") && 
            CONTAINSSTRING('Atenciones'[INSTRUMENTO],"kine"))
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Control SALA Kine (act)]`

Indicador SI/NO mensual (REMA): atención del mes anterior donde [ACTIVIDADES] contiene «control sala (ira» y [INSTRUMENTO] contiene «kine».

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            (CONTAINSSTRING('Atenciones'[ACTIVIDADES],"control sala (ira") && 
            CONTAINSSTRING('Atenciones'[INSTRUMENTO],"kine"))
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Control SALA Med (act)]`

Indicador REMA mensual: control de sala IRA/ERA realizado por médico (no técnico) durante el mes anterior.

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            (CONTAINSSTRING('Atenciones'[ACTIVIDADES],"control sala (ira") && 
            CONTAINSSTRING('Atenciones'[INSTRUMENTO],"médico") &&
            NOT CONTAINSSTRING(Atenciones[INSTRUMENTO],"técnico"))
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Coqueluche]`

Indicador SI/NO mensual (REMA): tuvo al menos una atención durante el mes anterior completo donde [DIAGNOSTICOS] contiene «coquelu».

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"coquelu")
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 EPOC Exacerbado]`

Indicador SI/NO mensual (REMA): tuvo al menos una atención durante el mes anterior completo donde [DIAGNOSTICOS] contiene «J44.1».

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"J44.1")
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Edu Integral Sala]`

Indicador REMA mensual: educación integral en salud respiratoria en contexto de sala durante el mes anterior.

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            CONTAINSSTRING('Atenciones'[ACTIVIDADES],"educación integral en salud respiratoria") &&
            (
                CONTAINSSTRING(Atenciones[ACTIVIDADES],"control sala (ira") ||
                CONTAINSSTRING(Atenciones[ACTIVIDADES],"consulta sala (ira") ||
                CONTAINSSTRING(Atenciones[ACTIVIDADES],"kinesioterapi")
            )
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Educación Antitabaco]`

Indicador REMA mensual: educación/consejería antitabaco en contexto de sala (control, consulta o kinesioterapia) durante el mes anterior.

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            (
                CONTAINSSTRING(Atenciones[ACTIVIDADES],"tabaco") && 
                (
                    CONTAINSSTRING(Atenciones[ACTIVIDADES],"control sala (ira") ||
                    CONTAINSSTRING(Atenciones[ACTIVIDADES],"consulta sala (ira") ||
                    CONTAINSSTRING(Atenciones[ACTIVIDADES],"kinesioterapi")
                )
            )
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Encuesta calidad de vida]`

Resultado de la encuesta de calidad de vida (pregunta 99 de «Otros y Respi») registrada durante el mes anterior. BLANK si no hubo.

```dax
VAR FechaInicioMesAnterior = EOMONTH(TODAY(), -2) + 1
VAR FechaFinMesAnterior = EOMONTH(TODAY(), -1)

var _Resultado = 
TOPN(1,
    CALCULATETABLE(VALUES('Otros y Respi'[99.- RESULTADO ENCUESTA CALIDAD DE VIDA]),
    FILTER(ALL('Otros y Respi'),'Otros y Respi'[RUN]='Ferrada'[RUN] &&
    'Otros y Respi'[FECHA ATENCION] >= FechaInicioMesAnterior &&
    'Otros y Respi'[FECHA ATENCION] <= FechaFinMesAnterior)),
    'Otros y Respi'[99.- RESULTADO ENCUESTA CALIDAD DE VIDA],DESC)

RETURN

IF(
    _Resultado="",
    BLANK(),
    _Resultado)
```

### `Ferrada[REMA23 Espirometría (act)]`

Indicador SI/NO mensual (REMA): tuvo al menos una atención durante el mes anterior completo donde [ACTIVIDADES] contiene «espirometr».

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            CONTAINSSTRING('Atenciones'[ACTIVIDADES],"espirometr")
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Inasistentes]`

Inasistencia a control respiratorio según REM A23 sección G. Toma la última «fecha del próximo control» registrada en formularios «Otros y Respi» válidos (padece=sí, estado ingreso/seguimiento) de las seis patologías (SBO recurrente, asma, EPOC, fibrosis quística, displasia broncopulmonar, otras respiratorias crónicas) y aplica el umbral por edad: <1 año 2 meses 29 días; 1 año 5m29d; ≥2 años 11m29d. Devuelve BLANK si no tiene diagnóstico respiratorio, «Sin Fecha formulario» si está ingresado pero nunca se registró próximo control (indicador de calidad de registro — no sumar al conteo REM), «Si» si superó el umbral, «No» si está al día.

```dax
VAR _Hoy = TODAY()

VAR _FpcSBO =
    CALCULATE(MAX('Otros y Respi'[5.- FECHA DEL PRÓXIMO CONTROL]),
        FILTER(ALL('Otros y Respi'),
            'Otros y Respi'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Otros y Respi'[1.- ¿PADECE DE SÍNDROME BRONQUIAL OBSTRUCTIVO?],"si") &&
            CONTAINSSTRING('Otros y Respi'[2.- ¿ES RECURRENTE?],"si") &&
            (CONTAINSSTRING('Otros y Respi'[3.- ESTADO],"ingreso") ||
             CONTAINSSTRING('Otros y Respi'[3.- ESTADO],"seguimiento"))))

VAR _FpcASMA =
    CALCULATE(MAX('Otros y Respi'[12.- FECHA DEL PRÓXIMO CONTROL]),
        FILTER(ALL('Otros y Respi'),
            'Otros y Respi'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Otros y Respi'[9.- ¿PADECE DE ASMA BRONQUIAL?],"si") &&
            (CONTAINSSTRING('Otros y Respi'[10.- ESTADO],"ingreso") ||
             CONTAINSSTRING('Otros y Respi'[10.- ESTADO],"seguimiento"))))

VAR _FpcEPOC =
    CALCULATE(MAX('Otros y Respi'[18.- FECHA DEL PRÓXIMO CONTROL]),
        FILTER(ALL('Otros y Respi'),
            'Otros y Respi'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Otros y Respi'[14.- ¿PADECE ENFERMEDAD PULMONAR CRONICA?],"si") &&
            (CONTAINSSTRING('Otros y Respi'[17.- ESTADO],"ingreso") ||
             CONTAINSSTRING('Otros y Respi'[17.- ESTADO],"seguimiento"))))

VAR _FpcFQ =
    CALCULATE(MAX('Otros y Respi'[32.- FECHA DEL PRÓXIMO CONTROL]),
        FILTER(ALL('Otros y Respi'),
            'Otros y Respi'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Otros y Respi'[30.- ¿PADECE DE FIBROSIS QUISTICA?],"si") &&
            (CONTAINSSTRING('Otros y Respi'[31.- ESTADO],"ingreso") ||
             CONTAINSSTRING('Otros y Respi'[31.- ESTADO],"seguimiento"))))

VAR _FpcDBP =
    CALCULATE(MAX('Otros y Respi'[52.- FECHA PRÓXIMO CONTROL]),
        FILTER(ALL('Otros y Respi'),
            'Otros y Respi'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Otros y Respi'[50.- ¿PADECE DE DISPLASIA BRONCOPULMONAR?],"si") &&
            (CONTAINSSTRING('Otros y Respi'[51.- ESTADO],"ingreso") ||
             CONTAINSSTRING('Otros y Respi'[51.- ESTADO],"seguimiento"))))

VAR _FpcOTR =
    CALCULATE(MAX('Otros y Respi'[56.- FECHA PRÓXIMO CONTROL]),
        FILTER(ALL('Otros y Respi'),
            'Otros y Respi'[RUN] = 'Ferrada'[RUN] &&
            CONTAINSSTRING('Otros y Respi'[53.- ¿PADECE OTRAS ENFERMEDADES RESPIRATORIAS?],"si") &&
            (CONTAINSSTRING('Otros y Respi'[55.- ESTADO],"ingreso") ||
             CONTAINSSTRING('Otros y Respi'[55.- ESTADO],"seguimiento"))))

VAR _TieneDx =
    NOT ISBLANK(_FpcSBO) || NOT ISBLANK(_FpcASMA) || NOT ISBLANK(_FpcEPOC) ||
    NOT ISBLANK(_FpcFQ)  || NOT ISBLANK(_FpcDBP)  || NOT ISBLANK(_FpcOTR) ||
    'Ferrada'[SALA Ingresado] = "SI"

VAR _FPC =
    MAXX(FILTER({_FpcSBO, _FpcASMA, _FpcEPOC, _FpcFQ, _FpcDBP, _FpcOTR},
        NOT ISBLANK([Value])), [Value])

VAR _Limite =
    SWITCH(TRUE(),
        'Ferrada'[Edad] < 1, EDATE(_FPC, 2)  + 29,
        'Ferrada'[Edad] < 2, EDATE(_FPC, 5)  + 29,
        EDATE(_FPC, 11) + 29)

RETURN
SWITCH(TRUE(),
    NOT _TieneDx, BLANK(),
    ISBLANK(_FPC), "Sin Fecha formulario",
    _Hoy > _Limite, "Si",
    "No")
```

### `Ferrada[REMA23 Influenza]`

Indicador SI/NO mensual (REMA): tuvo al menos una atención durante el mes anterior completo donde [DIAGNOSTICOS] contiene «influenz».

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            CONTAINSSTRING(Atenciones[DIAGNOSTICOS],"influenz")
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Inhaloterapia]`

Indicador SI/NO mensual (REMA): al menos una atención del mes anterior cuyas actividades cumplen [ACTIVIDADES] contiene «inhalatoria» y [ACTIVIDADES] contiene «control sala».

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            (
                CONTAINSSTRING('Atenciones'[ACTIVIDADES],"inhalatoria") && 
                CONTAINSSTRING('Atenciones'[ACTIVIDADES],"control sala")
            )
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Ira Alta]`

Indicador SI/NO mensual (REMA): tuvo al menos una atención durante el mes anterior completo donde [DIAGNOSTICOS] contiene «j0».

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"j0")
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 KTR]`

Indicador SI/NO mensual (REMA): tuvo al menos una atención durante el mes anterior completo donde [ACTIVIDADES] contiene «kinesioterapia res».

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            CONTAINSSTRING('Atenciones'[ACTIVIDADES],"kinesioterapia res")
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Morbi respiratoria]`

Indicador REMA mensual: consulta médica de morbilidad, SAC o teletriage en el mes anterior en paciente con algún evento respiratorio REMA23 activo (IRA alta, influenza, neumonía, bronquitis, EPOC exacerbado o coqueluche).

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            (
                CONTAINSSTRING('Atenciones'[INSTRUMENTO],"médic") && 
                (
                    CONTAINSSTRING(Atenciones[TIPO ATENCION],"morbilida") ||
                    CONTAINSSTRING(Atenciones[TIPO ATENCION],"consulta sac") ||
                    CONTAINSSTRING(Atenciones[TIPO ATENCION],"teletriage")
                ) 
                &&
                (
                    'Ferrada'[REMA23 Ira Alta]="SI" || 
                    'Ferrada'[REMA23 Influenza]="SI" ||
                    'Ferrada'[REMA23 Neumonia]="SI" || 
                    'Ferrada'[REMA23 Bronquitis Aguda]="SI" || 
                    'Ferrada'[REMA23 EPOC Exacerbado]="SI" || 
                    'Ferrada'[REMA23 Coqueluche]="SI"
                )
            )
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Neumonia]`

Indicador REMA mensual: diagnóstico de neumonía en alguna atención del mes anterior completo.

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            (
                CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"neumonía") ||
                CONTAINSSTRING('Atenciones'[DIAGNOSTICOS],"neumonia")
            )
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Otras]`

Indicador SI/NO mensual (REMA): al menos una atención del mes anterior cuyas actividades cumplen [ACTIVIDADES] contiene «Consejerias individuales otras areas» y [ACTIVIDADES] contiene «control sala».

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            (
                CONTAINSSTRING('Atenciones'[ACTIVIDADES],"Consejerias individuales otras areas") && 
                CONTAINSSTRING('Atenciones'[ACTIVIDADES],"control sala")
            )
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Rehab Conti]`

Indicador SI/NO mensual (REMA): al menos una atención en el mes anterior completo cuya actividad contiene «Rehabilitación Pulmonar - Artic».

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            CONTAINSSTRING('Atenciones'[ACTIVIDADES],"Rehabilitación Pulmonar - Artic")  
            ))

RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Rehab Ses Act Fca]`

Indicador SI/NO mensual (REMA): al menos una atención en el mes anterior completo cuya actividad contiene «Rehabilitación Pulmonar - Sesión Act».

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            CONTAINSSTRING('Atenciones'[ACTIVIDADES],"Rehabilitación Pulmonar - Sesión Act")  
            ))

RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Rehab Ses Educ]`

Indicador SI/NO mensual (REMA): al menos una atención en el mes anterior completo cuya actividad contiene «Rehabilitación Pulmonar - Sesión Educ».

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            CONTAINSSTRING('Atenciones'[ACTIVIDADES],"Rehabilitación Pulmonar - Sesión Educ")  
            ))

RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Seguimiento Eu]`

Indicador SI/NO mensual (REMA): en el mes anterior tuvo control o consulta de sala IRA/ERA atendida por enfermería (excluyendo técnicos), y además tiene activo algún evento respiratorio REMA23 del mismo mes (IRA alta, influenza, neumonía, bronquitis aguda, EPOC exacerbado o coqueluche).

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            (
                CONTAINSSTRING('Atenciones'[INSTRUMENTO],"enfermer") && 
                NOT CONTAINSSTRING(Atenciones[INSTRUMENTO],"técnic")
            )
            &&
            (
                CONTAINSSTRING('Atenciones'[ACTIVIDADES],"control sala (ira") ||
                CONTAINSSTRING('Atenciones'[ACTIVIDADES],"consulta sala (ira")
            )
            &&
            (
                'Ferrada'[REMA23 Ira Alta]="SI" || 
                'Ferrada'[REMA23 Influenza]="SI" ||
                'Ferrada'[REMA23 Neumonia]="SI" || 
                'Ferrada'[REMA23 Bronquitis Aguda]="SI" || 
                'Ferrada'[REMA23 EPOC Exacerbado]="SI" || 
                'Ferrada'[REMA23 Coqueluche]="SI"
            )
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Seguimiento Kine]`

Indicador SI/NO mensual (REMA): en el mes anterior tuvo control o consulta de sala IRA/ERA atendida por kinesiólogo/a (excluyendo técnicos), y además tiene activo algún evento respiratorio REMA23 del mismo mes (IRA alta, influenza, neumonía, bronquitis aguda, EPOC exacerbado o coqueluche).

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            (
                CONTAINSSTRING('Atenciones'[INSTRUMENTO],"kine") && 
                NOT CONTAINSSTRING(Atenciones[INSTRUMENTO],"técnic")
            )
            &&
            (
                CONTAINSSTRING('Atenciones'[ACTIVIDADES],"control sala (ira") ||
                CONTAINSSTRING('Atenciones'[ACTIVIDADES],"consulta sala (ira")
            )
            &&
            (
                'Ferrada'[REMA23 Ira Alta]="SI" || 
                'Ferrada'[REMA23 Influenza]="SI" ||
                'Ferrada'[REMA23 Neumonia]="SI" || 
                'Ferrada'[REMA23 Bronquitis Aguda]="SI" || 
                'Ferrada'[REMA23 EPOC Exacerbado]="SI" || 
                'Ferrada'[REMA23 Coqueluche]="SI"
            )
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 VDI Respi]`

Indicador REMA mensual: atención domiciliaria en el mes anterior en paciente ingresado en sala respiratoria.

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            CONTAINSSTRING('Atenciones'[TIPO ATENCION],"domiciliaria") &&
            Ferrada[SALA Ingresado]="si"
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
```

### `Ferrada[REMA23 Vida Saludable]`

Indicador REMA mensual: consejería en vida saludable (actividad física o alimentación) en contexto de sala durante el mes anterior.

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
            Atenciones[FECHA ATENCION] <= FechaFinMesAnterior &&
            (
                CONTAINSSTRING('Atenciones'[ACTIVIDADES],"Consejer") &&
                (
                    CONTAINSSTRING(Atenciones[ACTIVIDADES],"activi") ||
                    CONTAINSSTRING(Atenciones[ACTIVIDADES],"aliment")
                )
                &&
                (
                    CONTAINSSTRING('Atenciones'[ACTIVIDADES],"control sala (ira") ||
                    CONTAINSSTRING(Atenciones[ACTIVIDADES],"consulta sala (ira") ||
                    CONTAINSSTRING(Atenciones[ACTIVIDADES],"kinesioterapi")
                )
            )
        )
    )
RETURN
    IF(AtencionesMesAnterior > 0, "SI", "NO")
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

### `Ferrada[Última atención (instrumento)]`

Instrumento (profesional) de la última atención registrada.

```dax
var _Fecha =
LASTDATE(
    CALCULATETABLE(VALUES(Atenciones[FECHA ATENCION]),
    FILTER(ALL(Atenciones),Atenciones[RUN]='Ferrada'[RUN])))

var _Instrumento =
TOPN(1,
CALCULATETABLE(VALUES(Atenciones[INSTRUMENTO]),
FILTER(ALL(Atenciones),Atenciones[RUN]='Ferrada'[RUN]),
Atenciones[FECHA ATENCION]=_Fecha),Atenciones[INSTRUMENTO],DESC)

RETURN

_Instrumento
```
