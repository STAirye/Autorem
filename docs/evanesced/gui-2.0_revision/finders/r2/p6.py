import sys; sys.path.insert(0, r"E:\git\Autorem\tests"); sys.dont_write_bytecode = True
import _aislar_cache  # noqa
import test_sp_p6 as T
from datetime import date
Q = T._Q
form = [{"rut": "11111111-1", "fecha": date(2026, 7, 1), **{Q[57]: "SI", Q[58]: "INGRESO"}}]
# caso A: todo calza -> base 1 (control)
P = T._poblacion(form, [{"rut": "11111111-1"}], ada_filas=[T._sm("11111111-1")])
print("control fila35:", T._fila_p6(T._p6(P)["grid"], 35)["Ambos"], "avisos", P.attrs["avisos"])
# caso B: Estado con otro vocabulario ("Activa") -> Estado=Activo filtra a TODOS
P = T._poblacion(form, [{"rut": "11111111-1", "estado": "Activa"}], ada_filas=[T._sm("11111111-1")])
r = T._p6(P); g = r["grid"]
print("B estado 'Activa': suma grid Ambos =", int(g["Ambos"].sum()) if "Ambos" in g else g.sum(numeric_only=True).sum(), "| avisos", P.attrs["avisos"], "| raised? no")
# caso C: el ADA trae el RUN con puntos (otro formato) -> Activo12m NO para todos
P = T._poblacion(form, [{"rut": "11111111-1"}], ada_filas=[T._sm("11.111.111-1")])
r = T._p6(P); g = r["grid"]
print("C RUN ADA con puntos: suma grid =", int(g["Ambos"].sum()), "| ingresados", int((P["¿Ingresado?"]=="SI").sum()), "| activo12m", int((P["¿Activo 12m?"]=="SI").sum()), "| avisos", P.attrs["avisos"])
