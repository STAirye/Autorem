import sys; sys.path.insert(0, "."); sys.stdout.reconfigure(encoding="utf-8")
import tests._aislar_cache
from programas.rem_utils import cargar_maestro, norm
from modulos.rem_sm_actividades import ADA_TRIBUTAN
from programas.poblacion import ACTIVIDADES_SM_7
from modulos.rem_sm_trabajo_perdido import EXCLUIR_SMISH, TRIBUTA_SM_REM
m = cargar_maestro("catalogos/maestro_slim.csv.gz")
acts = sorted(set(m["ACT_n"])); instr = sorted(set(m["INSTR"].map(norm))); rems = sorted(set(m["NUMREM_n"]))
def hits(*toks):
    t=[norm(x) for x in toks]; return [a for a in acts if all(x in a for x in t)]
casos = {
 "A23": [("autocuidado","control sala"),("consulta sala (ira",),("control sala (ira",),("educacion integral en salud respiratoria",),("tabaco",),("espirometr",),("inhalatoria","control sala"),("kinesioterapia res",),("consejerias individuales otras areas","control sala"),("consejer",),("rehabilitacion pulmonar - artic",),("rehabilitacion pulmonar - sesion act",),("rehabilitacion pulmonar - sesion educ",),("kinesioterapi",)],
 "SM": [(p,) for p in ADA_TRIBUTAN] + [("acciones remotas de salud mental","videollamada"),("acciones remotas de salud mental","mensaj"),("acciones remotas de salud mental","llamada"),("controles","salud mental por"),("intervencion psicosocial grupal",),("consejerias familiares","problema de salud mental"),("consejerias familiares","demencia"),("prevencion","suicid"),("prevencion trastorno mental",)],
 "P6/rescate ACTIVIDADES_SM_7": [(p,) for p in ACTIVIDADES_SM_7],
 "TP EXCLUIR_SMISH": [(p,) for p,_ in EXCLUIR_SMISH],
}
for g, lst in casos.items():
    print("=====", g)
    for toks in lst:
        h = hits(*toks)
        print(f"  {'OK ' if h else '0  '} {len(h):3d}  {' + '.join(toks)!s:70s} {h[:2] if len(h)<=2 else h[:2]+['...']}")
print("===== instrumentos (estamentos) usados vs Maestro")
for t in ["MEDICO","KINE","ENFERMER","MATRON","PSICOLOG","TRABAJADOR","TERAPEUTA OCUPACIONAL","GESTOR","TECNICO"]:
    print("  ", t, [i for i in instr if norm(t) in i][:6])
print("===== TRIBUTA_SM_REM vs NUM REM del Maestro:", {r: (r in rems) for r in TRIBUTA_SM_REM})
