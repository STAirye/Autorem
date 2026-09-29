# Revision ciega, fase 1 — lectura_calamine vs a567c1a

Sin valores de celda. Sin hipotesis de causa. Ceguera: no se leyo el diff, commits, CHANGELOG, planes, evanesced ni §12.
(Un hecho de contexto visto de paso: el numero del arbol candidato es 2.0.15 / 362 tests segun `check_version`.)

## 1. Checks y suite
| Item | Base | Candidata | Veredicto |
|---|---|---|---|
| check_fuentes --todo | OK | OK | PASS |
| check_cp1252 | OK (68 .py) | OK (69 .py) | PASS |
| check_version | OK 2.0.14, 356 | OK 2.0.15, 362 | PASS |
| correr_tests.py | 358 passed (169+158+31) 73 s | 364 passed (139+194+31) 65 s | PASS |
| Tests solo en base | — | — | ninguno |
| Tests solo en cand | — | 6, todos en tests/test_lectura_calamine.py (no_xlsx, paridad_con_openpyxl_en_refs_tablas, perdidas_aceptadas_quedan_fijas, primeras_filas, regla_de_hojas, tipos_exactos) | — |
| Conteo por archivo | igual salvo el archivo nuevo | | |
Tcl 9.0: sin tk.tcl intermitente. Ninguna falla en ninguno de los dos.

## 2. Punta a punta (datos reales, mes 2026-08 y rango 2026-06..08)
Inputs (confirmados por el autor): ADA 2026, PSM 2026, Inscritos (tabla); Grupal 2026, Monitoreo Multiprofesional 2026, Otros Cronicos 2025+2026, Estratificacion, NSP 2025+2026, Goldberg 2026 (A03), PSM 2021-2026 + ADA 2025+2026 para P6/Rescate. Sin Maestro manual (slim embebido), sin Cupos, sin PSC/PSC-Y (no hay input).
Corridas: base x2, cand x2, todas terminan sin excepcion.

Ruido medido (base1 vs base2): LEEME 1 celda por libro (celda de la fecha/hora, A3); P6 `Revisar_Clinico` = mismas filas en otro orden (tratado como multiconjunto). Nada mas. Log y resumen: solo cambia la ruta de guardado.

| Modulo / periodo | Archivos | Hojas (orden, forma, headers) | Celdas fuera de ruido | Avisos por categoria | Log | Veredicto |
|---|---|---|---|---|---|---|
| A05 N+O mes | 1 | igual | LEEME A1 (str->str) | sin avisos, igual | igual | DIFF (1 celda) |
| A05 N+O rango | 1 | igual | LEEME A1 | igual | igual | DIFF (1 celda) |
| SM Act + TP + A03 mes | 3 | igual | LEEME A1 en cada libro | PENDIENTE 2, SUBCONTADO 3: igual | igual | DIFF (1 celda x 3) |
| SM Act + TP + A03 rango | 3 | igual | LEEME A1 en cada libro | PENDIENTE 2, SUBCONTADO 6: igual | igual | DIFF (1 celda x 3) |
| A23 mes | 1 | igual (11 hojas) | LEEME A1 | REVISAR 1: igual | igual | DIFF (1 celda) |
| SP·P6 + Rescate mes | 2 | igual | LEEME A1 en cada libro | sin avisos | igual | DIFF (1 celda x 2) |

Todas las demas hojas: 0 celdas distintas, mismos tipos, mismos encabezados. La celda A1 de LEEME es texto -> texto y es el encabezado de esa hoja, que lleva el numero de version (2.0.14 en base). cand1 y cand2 dan lo mismo entre si.

Tiempos de pared (s), base1 / base2 / cand1 / cand2:
| Corrida | base1 | base2 | cand1 | cand2 | |
|---|---|---|---|---|---|
| A05 mes | 6.4 | 6.5 | 6.0 | 5.9 | dentro de +-20 % |
| A05 rango | 7.0 | 6.6 | 6.0 | 7.4 | dentro |
| SM mes | 45.1 | 38.1 | 15.2 | 12.3 | -60 a -70 % (REPORTADO >20 %) |
| SM rango | 41.2 | 38.6 | 18.2 | 13.3 | -55 a -68 % |
| A23 mes | 35.3 | 35.3 | 18.8 | 18.2 | -47 % |
| P6 + Rescate | 107.9 | 104.8 | 66.4 | 63.9 | -40 % |

## 3. Caminos de error (342 combinaciones: 19 entradas publicas x 18 fixtures sinteticos)
Fixtures: html renombrado, truncado (3 KB), dos hojas con datos, hoja vacia, sin fila de encabezado, dimension rota, solo encabezado, mes sin filas; en sabor ADA y sabor formulario SM; mas los dos validos de control.
Entradas: cargar_atenciones, +filtrar_mes, cargar_canonico, primeras_filas, detectar_formato_filas, verificar_hoja_unica, leer_xlsx, A05 egresos/ingresos (abrir_validado+agregar_hoja), _correr_tareas (mes y rango), procesar_rango de SM, cargar_grupal, cargar_formulario_sm, cargar_inscritos, a23 cargar_otros/inasistentes/estrat/procesar.

| Comparacion | Resultado |
|---|---|
| Tipo de excepcion, `categoria`, `es_error_formato` | 340/342 iguales; 2 DIFF (abajo) |
| Archivo renombrable tras la excepcion (os.replace, con la excepcion viva y despues) | 0 fallas en ambos arboles |
| Texto del mensaje | 76 combinaciones difieren solo en el texto (todas con html/truncado: base «File is not a zip file …», cand «No es un .xlsx (no es un zip): <ruta completa> …») |

DIFF de comportamiento (2): `leer_xlsx` sobre un libro con datos en dos hojas (sabor ADA y sabor SM): base devuelve (encabezado, filas) sin error; cand levanta `ArchivoInvalido` categoria `modificado`, `es_error_formato`=False.
Nota: en ambos arboles los html/truncados que no envuelven en ArchivoInvalido salen como `BadZipFile` crudo en las mismas 32 combinaciones, con `es_error_formato`=True igual.

## 4. Build
| Item | Base | Candidata |
|---|---|---|
| `pyinstaller --clean autoREM.spec` | OK (41.2 MB exe) | 2 intentos in-tree fallaron con PermissionError de Windows al limpiar `build/autoREM/localpycs` (bloqueo del directorio); OK con `--workpath/--distpath` en el scratchpad (mismo spec) |
| warn-autoREM.txt (missing/excluded/invalid/ignored, sin «imported by») | 284 lineas | 284 lineas, **0 modulos faltantes solo en cand, 0 solo en base** |
| python_calamine en el exe | pyd + paquete + pandas.io.excel._calamine presentes | idem |
No se abrio ningun exe.

## 5. No pude correr / limites
- A03 solo Goldberg (PSC 5-9 vacia, PSC-Y solo 2025, sin input 2026).
- Sin CLI (congelado), sin formato Administrativo real (solo refs con encabezado en los fixtures), sin Monitoreo Admin real.
- Sin Maestro manual ni Cupos, y dotacion con cache aislado vacio (el dialogo Tk de dotacion no se ejercita; se replico su carga sin ventana).
- GUI no ejercitada (solo las llamadas de `correr`).
- Los caminos de error usan fixtures sinteticos pequenos: no cubren un export real grande truncado.

## 6. Prueba manual para el autor (exe de la candidata)
1. Abrir `dist\autoREM.exe` (compilar en la rama; en este arbol el `build/` dio PermissionError, borrar `build\` a mano si vuelve a pasar).
2. Salud Mental -> Actividades: ADA 2026 + Grupal + Inscritos + Multiprofesional, mes 2026-08, correr.
3. Abrir `REM_SM_actividades_2026_08.xlsx`: mirar `SM_Resumen` y LEEME (avisos PENDIENTE 2 / SUBCONTADO 3 esperados por la base) y el Trabajo Perdido.
4. Cargar un `.html` renombrado a `.xlsx` y verificar el dialogo «No es un .xlsx».
5. Cronometrar SM agosto (base ~40 s en esta maquina).
