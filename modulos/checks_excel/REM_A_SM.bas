Attribute VB_Name = "REM_A_SM"
' ==========================================================================
' This code was generated with the assistance of Claude Opus 5.5 (Anthropic).
' The human author reviewed, modified, and integrated the code.
'
' Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
' Copyright (C) 2026 Simon Tobar
' SPDX-License-Identifier: GPL-3.0-or-later
' Version: 2.0.29
' ==========================================================================
'
' Chequeo pre-envio del REM serie A, Salud Mental (plantilla SA_26 V1.2).
' Lee SOLO el total de cada tabla que produce autoREM para SM (sin Trabajo
' Perdido): el xlsm suma los desgloses solo, asi que basta el total. Un 0 o un
' error se marca REVISAR: o no hubo actividad ese mes, o falta la tabla, o la
' plantilla perdio la formula del total (paso en el A05 O de julio 2026: la
' tabla tenia datos y C245 daba 0). No modifica nada.
'
' Uso: abrir el REM del mes, Alt+F11 > Archivo > Importar > este .bas, F5.
' Las celdas las vigila tests/test_checks_excel.py contra la plantilla de
' refs_tablas/: si MINSAL la cambia, el test falla (skill check-excel).

Sub ChequeoSM()
    Dim c, p, v, s As String, malo As Boolean
    For Each c In Array( _
        "A03|D.3 instrumentos|C163:C168", _
        "A04|Consulta SM|B24", _
        "A05|N ingresos|C193", _
        "A05|O egresos|C245", _
        "A06|A.1 controles + grupal|C22:C23", _
        "A06|A.2 consultorias|B30:B31", _
        "A19a|A.3 consejerias SM/demencia|C110,C112", _
        "A26|A VDI SM|C30:C31", _
        "A27|A prevencion SM|D34:D35", _
        "A27|B sesiones|D79:D80", _
        "A32|F1 acciones remotas|B123:B125", _
        "A32|F2 controles remotos|C130:C139,C141:C150")
        p = Split(c, "|")
        v = Application.Sum(ActiveWorkbook.Sheets(p(0)).Range(p(2)))
        If IsError(v) Then
            s = s & p(0) & " " & p(1) & ": #ERROR  <-- REVISAR" & vbLf: malo = True
        ElseIf v = 0 Then
            s = s & p(0) & " " & p(1) & ": 0  <-- REVISAR" & vbLf: malo = True
        Else
            s = s & p(0) & " " & p(1) & ": " & v & vbLf
        End If
    Next
    MsgBox s, IIf(malo, vbExclamation, vbInformation), "Chequeo REM A - SM"
End Sub
