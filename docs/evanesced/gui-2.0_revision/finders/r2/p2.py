import sys; sys.path.insert(0, r"E:\git\Autorem\tests"); sys.dont_write_bytecode = True
import _aislar_cache  # noqa
import test_sp_p6 as T, openpyxl
from datetime import date
Q = T._Q
q = lambda *a, **k: None
# (a) formulario SIN columna INSTRUMENTO: TDAH (exige medico) + un FR (no exige) de otro RUN
form = [{"rut": "11111111-1", "fecha": date(2026, 7, 1), **{Q[57]: "SI", Q[58]: "INGRESO"}},
        {"rut": "22222222-2", "fecha": date(2026, 7, 1), **{Q[4]: "SI", Q[5]: "INGRESO"}}]
p = T._mk_formulario(form)
wb = openpyxl.load_workbook(p); ws = wb.active
ci = [c.value for c in ws[17]].index("INSTRUMENTO") + 1
ws.delete_cols(ci); wb.save(p)
import programas.poblacion as pob
P = pob.construir_poblacion(str(T._mk_inscritos([{"rut": "11111111-1"}, {"rut": "22222222-2"}])), str(p),
                            str(T._mk_ada([T._sm("11111111-1"), T._sm("22222222-2")])), mes=(2026, 8), log=q)
print("(a) sin INSTRUMENTO: Ingresado", dict(zip(P["Número"], P["¿Ingresado?"])),
      "| avisos", [a[:2] for a in P.attrs["avisos"]])
r = T._p6(P)
print("    fila35 (TDAH) Ambos =", T._fila_p6(r["grid"], 35)["Ambos"])
# (b) P6: persona sin edad (sin FECHA DE NACIMIENTO ni EDAD AÑOS)
form = [{"rut": "11111111-1", "fecha": date(2026, 7, 1), **{Q[57]: "SI", Q[58]: "INGRESO"}}]
P = T._poblacion(form, [{"rut": "11111111-1", "edad": ""}], ada_filas=[T._sm("11111111-1")])
r = T._p6(P); f = T._fila_p6(r["grid"], 35)
bandas = [c for c in r["grid"].columns if c.endswith(" H") or c.endswith(" M")]
print("(b) sin edad: Edad", P["Edad"].tolist(), "| fila35 Ambos", f["Ambos"], "| suma bandas",
      int(sum(f[c] for c in bandas)), "| motivos revisar", T._motivos(r))
