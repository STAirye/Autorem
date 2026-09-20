import sys; sys.path.insert(0, "."); sys.stdout.reconfigure(encoding="utf-8")
import tests._aislar_cache
from programas.rem_utils import resolver_columnas, MAPA_ATENCIONES, MAPA_MAESTRO, primeras_filas, indice_encabezado, norm, num_pregunta, indice_col
from programas import formatos, poblacion as pob, rem_saludmental as sm
from modulos.rem_sm_actividades import MAPA_GRUPAL
from modulos.rem_a23_respiratorio import _resolver_otros
R = "refs_tablas/"
def hdr(f):
    fl = primeras_filas(R + f, 60)
    return list(fl[indice_encabezado(fl)]), fl
def show(tit, f, mapa):
    h, _ = hdr(f); col = resolver_columnas(h, mapa)
    print(f"--- {tit} vs {f}")
    for k, c in col.items():
        print(f"   {k:10s} -> {c!r}" + ("  (idx %d)" % h.index(c) if c else "   <<< NO RESUELVE"))
show("ATENCIONES", "ATENCIONESDIAGNOSTICOSACTIVIDADES_iris.xlsx", MAPA_ATENCIONES)
show("ATENCIONES", "Monitoreo_de_Actividades_anonimizado.xlsx", MAPA_ATENCIONES)
show("GRUPAL", "Atenciones_Grupales_iris.xlsx", MAPA_GRUPAL)
show("INSCRITOS", "Informe_Inscritos__Adscritos_heads.xlsx", pob.MAPA_INSCRITOS)
for f in ["ATENCIONESDIAGNOSTICOSACTIVIDADES_iris.xlsx","Monitoreo_de_Actividades_anonimizado.xlsx","Atenciones_Grupales_iris.xlsx"]:
    h,_=hdr(f); print("parece_reporte", f, formatos.parece_reporte(h),
      formatos.clasificar_fuente(resolver_columnas(h, MAPA_ATENCIONES)))
# otros resolver on the SM IRIS formulario (shared identity columns only)
h,_ = hdr("Formularios_RAYEN_csm_IRis.xlsx"); o=_resolver_otros(h)
print("--- otros (identidad) sobre layout formulario IRIS:", {k:o[k] for k in ("RUN","FECHA","INSTR","SEXO_o","FNAC_o")})
# formularios: eje + identidad + fecha
for f in ["Formularios_RAYEN_csm_IRis.xlsx","Formulario_csm_reporte_Administrativo.xlsx","goldberg_iris.xlsx","goldberg_administrativo.xlsx","psc_administrativo.xlsx","pscy_10_14_iris.xlsx","pscy_10_14_administrativo.xlsx"]:
    h, fl = hdr(f); hn=[norm(x) for x in h]
    from programas.rem_utils import buscar_col
    rut,edad,sexo = formatos.resolver_identidad(hn)
    print(f"--- {f}: eje={formatos.detectar_eje_filas(fl)} fila_hdr={indice_encabezado(fl)+1} RUT={h[rut-1]!r} EDAD={h[edad-1]!r} SEXO={h[sexo-1]!r} FECHA={h[buscar_col(hn,tokens=['FECHA','FORMULARIO'])-1]!r} FUNC={buscar_col(hn,exacto='FUNCIONARIO')} INSTR={buscar_col(hn,exacto='INSTRUMENTO')} FORMULARIO={buscar_col(hn,exacto='FORMULARIO')} GENERO={buscar_col(hn,tokens=['GENERO'])}")
    for flag,(src,_) in sm.DEMOGRAFIA.items():
        c=buscar_col(hn,tokens=[norm(t) for t in src]); print(f"     demo {flag}: {h[c-1] if c else None!r}")
# numeros de pregunta -> texto, en ambos formularios SM
for f in ["Formularios_RAYEN_csm_IRis.xlsx","Formulario_csm_reporte_Administrativo.xlsx"]:
    h,_=hdr(f); n2h={num_pregunta(x):x for x in h if num_pregunta(x)}
    print("=== preguntas", f)
    for s in pob.TODAS_LAS_SPECS:
        print(f"   {s['col']:38s} dx={s['dx']}:{n2h.get(s['dx'])!r}  est={s['estado']}:{n2h.get(s['estado'])!r}  sub={s['subtipo']}:{n2h.get(s['subtipo'])!r} sub2={s['subtipo2']}:{n2h.get(s['subtipo2'])!r}")
    print("   TGD fallback", n2h.get(63), n2h.get(64), "| q1", n2h.get(1))
    for n,name in sm.OVERRIDE_PATOLOGIA.items(): print(f"   OVR {n}:{name!r} <- {n2h.get(n)!r}")
    print("   EXCLUIR", {n:n2h.get(n) for n in sm.EXCLUIR_PATOLOGIA}, "REMAP", {n:n2h.get(n) for n in sm.REMAP_DIAGNOSTICO})
# salida poblacion vs PBI
h,_=hdr("poblacion_sm_powerbi.xlsx")
print("--- columnas de salida del P6 que NO estan en el export PowerBI:", [c for c in pob.COLUMNAS_SALIDA if c not in h])
# trans_map indices on inscritos
h,_=hdr("Informe_Inscritos__Adscritos_heads.xlsx"); hn=[norm(x) for x in h]
print("--- trans_map:", h[indice_col(hn,"NUMERO","IDENTIFICACION")], h[indice_col(hn,"GENERO")], h[indice_col(hn,"SEXO")])
