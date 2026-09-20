import sys, tempfile, os; sys.path.insert(0, "."); sys.stdout.reconfigure(encoding="utf-8")
import tests._aislar_cache
from tests.contratos_fuentes import plantilla, escribir, Contrato
from programas.rem_utils import cargar_atenciones
tmp = tempfile.mkdtemp(); q=lambda *a,**k: None
def fx(ref, filas, n):
    b, h, _p = plantilla(Contrato(id="t", cubre=(), llamar=None, ref=ref, fila={}))
    return escribir(os.path.join(tmp, n), b, h, filas)
A="11111111-1"; B="10000013-K"
# IRIS: fila 2 sin RUN (paciente distinto, sin identificacion) -> se le pega el RUN de A?
iris = fx("ATENCIONESDIAGNOSTICOSACTIVIDADES_iris.xlsx", [
  {"NUMERO TIPO IDENTIFICACION":A, "ATEN ID":"901", "FECHA ATENCION":"05/08/2026", "ACTIVIDADES":"CONTROLES SALUD MENTAL", "DIAGNOSTICOS":"F32", "INSTRUMENTO":"MEDICO", "TIPO ATENCION":"CONTROL", "PROFESIONAL ATENCION":"DR X"},
  {"NUMERO TIPO IDENTIFICACION":"", "ATEN ID":"902", "FECHA ATENCION":"06/08/2026", "ACTIVIDADES":"CONSULTA DE SALUD MENTAL", "DIAGNOSTICOS":"F41", "INSTRUMENTO":"MEDICO", "TIPO ATENCION":"CONSULTA", "PROFESIONAL ATENCION":"DR Y"},
], "iris.xlsx")
d = cargar_atenciones(iris, log=q); print("IRIS ->", d[["RUN","ATENID","FECHA","PROF"]].to_string())
# Monitoreo: padre + hija, luego padre de B
mon = fx("Monitoreo_de_Actividades_anonimizado.xlsx", [
  {"N°":1, "RUN":A, "FECHA CONSULTA":"05/08/2026", "ACTIVIDAD Y/O PROCEDIMIENTO":"CONTROL SALA (IRA, ERA O MIXTA)", "DIAGNÓSTICO":"ASMA", "INSTRUMENTO":"MEDICO", "TIPO DE ATENCIÓN":"CONTROL", "FUNCIONARIO":"DR X", "AÑOS":40},
  {"N°":1, "RUN":"", "FECHA CONSULTA":"", "ACTIVIDAD Y/O PROCEDIMIENTO":"EDUCACION INDIVIDUAL EN SALA - AUTOCUIDADO SEGUN PATOLOGIA", "DIAGNÓSTICO":"", "INSTRUMENTO":"", "TIPO DE ATENCIÓN":"", "FUNCIONARIO":""},
  {"N°":2, "RUN":B, "FECHA CONSULTA":"06/08/2026", "ACTIVIDAD Y/O PROCEDIMIENTO":"CONSULTA SALA (IRA, ERA O MIXTA)", "DIAGNÓSTICO":"J45", "INSTRUMENTO":"KINESIOLOGO(A)", "TIPO DE ATENCIÓN":"CONSULTA", "FUNCIONARIO":"KINE Z", "AÑOS":7},
], "mon.xlsx")
m = cargar_atenciones(mon, log=q); print("MONITOREO ->", m[["RUN","ATENID","ACT"]].to_string())
import modulos.rem_a23_respiratorio as a23
mk = a23._masks_simples(m); print("A23 Autocuidado en Monitoreo (padre+hija de la MISMA atencion):", bool(mk["REMA23 Autocuidado"].any()))
