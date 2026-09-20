import sys, tempfile, os; sys.path.insert(0, "."); sys.stdout.reconfigure(encoding="utf-8")
import tests._aislar_cache
from tests.contratos_fuentes import plantilla, escribir, Contrato, RUT
import programas.rem_saludmental as sm, modulos.rem_a05_o_egresos as eg, modulos.rem_a05_n_ingresos as ing
import programas.poblacion as pob
tmp = tempfile.mkdtemp()
def fx(ref, fila, n="x.xlsx"):
    c = Contrato(id="t", cubre=(), llamar=None, ref=ref, fila={})
    b, h, _p = plantilla(c)
    return escribir(os.path.join(tmp, n), b, h, [fila])
q = lambda *a, **k: None
casos = [
 ("goldberg IRIS -> A05 egresos IRIS", "goldberg_iris.xlsx", {"NUMERO TIPO IDENTIFICACION": RUT, "AÑO APLICACIÓN FORMULARIO": 45, "SEXO":"Mujer", "FECHA FORMULARIO":"05/08/2026", "FORMULARIO":"CUESTIONARIO DE SALUD DE GOLDBERG", "1.- ESTADO":"Egreso", "14.- PUNTAJE":3, "15.- RESULTADO":"Ausencia de psicopatología"}, "iris", eg),
 ("goldberg IRIS -> A05 ingresos IRIS", "goldberg_iris.xlsx", {"NUMERO TIPO IDENTIFICACION": RUT, "AÑO APLICACIÓN FORMULARIO": 45, "SEXO":"Mujer", "FECHA FORMULARIO":"05/08/2026", "FORMULARIO":"CUESTIONARIO DE SALUD DE GOLDBERG", "1.- ESTADO":"Ingreso", "14.- PUNTAJE":3, "15.- RESULTADO":"Ausencia"}, "iris", ing),
 ("goldberg Admin -> A05 egresos Admin", "goldberg_administrativo.xlsx", {"RUT": RUT, "Edad de registro formulario":"45 años", "Sexo":"Mujer", "Fecha Formulario":"2026/08/05", "1.- Estado":"Egreso", "14.- Puntaje":3, "15.- Resultado":"Ausencia"}, "administrativo", eg),
 ("PSC Admin -> A05 ingresos Admin", "psc_administrativo.xlsx", {"RUT": RUT, "Edad de registro formulario":"7 años", "Sexo":"Mujer", "Fecha Formulario":"2026/08/05", "1.- Estado":"Ingreso", "40.- Puntaje ":40, "41.- Resultado":"Bajo"}, "administrativo", ing),
]
for tit, ref, fila, per, mod in casos:
    r = fx(ref, fila)
    try:
        wb, ws = sm.abrir_validado(r, sm.perfil_por_id(per))
        res = mod.agregar_hoja(wb, ws, sm.perfil_por_id(per), log=q, mes=(2026, 8))
        out = [list(x) for x in wb[mod.NOMBRE_HOJA_SALIDA].iter_rows(values_only=True)]
        print("SIGUE:", tit, "-> total", res.get("total"), res.get("por_tipo"), out[1:3])
    except Exception as e:
        print("FALLA:", tit, type(e).__name__, str(e)[:150].replace("\n"," "))
r = fx("goldberg_iris.xlsx", casos[0][2], "g2.xlsx")
try:
    d = pob.cargar_formulario_sm(r, log=q); print("SIGUE: goldberg IRIS -> poblacion.cargar_formulario_sm", len(d), "filas")
except Exception as e:
    print("FALLA: goldberg -> poblacion", type(e).__name__, str(e)[:200].replace("\n"," "))
