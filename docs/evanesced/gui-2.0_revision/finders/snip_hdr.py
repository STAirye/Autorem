import openpyxl
for p in [r"E:\git\Autorem\refs_tablas\Formularios_RAYEN_csm_IRis.xlsx", r"E:\git\Autorem\refs_tablas\goldberg_iris.xlsx", r"E:\git\Autorem\refs_tablas\ATENCIONESDIAGNOSTICOSACTIVIDADES_iris.xlsx", r"E:\git\Autorem\refs_tablas\Informe_Inscritos__Adscritos_heads.xlsx", r"E:\git\Autorem\refs_tablas\Atenciones_Grupales_iris.xlsx"]:
    wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
    r = next(wb.active.iter_rows(values_only=True))
    print(p.split("\\")[-1], len(r))
    print("   ", [c for c in r if c is not None][:60])
    wb.close()
