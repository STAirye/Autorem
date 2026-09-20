import sys; sys.path.insert(0, r"E:\git\Autorem\tests"); sys.dont_write_bytecode = True
import _aislar_cache  # noqa
import test_sp_p6 as T
import programas.poblacion as pob
for etq, filas in (("header-only", []),
                   ("filas pero todas RUN Responsable", [{"rut": "11111111-1", "tipoid": "RUN Responsable"}])):
    p = T._mk_inscritos(filas)
    try:
        pob.cargar_inscritos(str(p), log=lambda *a: None); print(etq, "-> sin error")
    except Exception as e:
        print(etq, "->", type(e).__name__, e.categoria, "|", str(e).splitlines()[0])
# motivo pasivacion ausente: el loader no lo exige
T._INS_HDR.remove("MOTIVO PASIVACION"); T._INS_HDR.remove("FECHA PASIVACION")
d = pob.cargar_inscritos(str(T._mk_inscritos([{"rut": "11111111-1", "mpasiv": "Fallecido"}])), log=lambda *a: None)
print("sin MOTIVO/FECHA PASIVACION -> carga OK; MPASIV =", d["MPASIV"].tolist(), "FPASIV =", d["FPASIV"].tolist())
