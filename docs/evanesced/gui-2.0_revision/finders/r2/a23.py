import sys; sys.path.insert(0, r"E:\git\Autorem\tests"); sys.dont_write_bytecode = True
import _aislar_cache  # noqa
import test_a23 as T
import openpyxl, pandas as pd
from datetime import date
a23 = T.a23
aten = T._mk([
    {"NUMERO TIPO IDENTIFICACION": "A", "FECHA ATENCION": date(2026, 7, 10), "INSTRUMENTO": "Médico",
     "FECHA DE NACIMIENTO": date(1990, 1, 1), "DIAGNOSTICOS": "J06.9 IRA alta", "SEXO": "Mujer"},
    T._RESP])
# (1) ASMA con el encabezado reformulado por RAYEN ('TIENE' en vez de 'PADECE DE')
T._OHDR[9] = "9.- ¿TIENE ASMA BRONQUIAL?"
otros = T._mk_otros([{"RUN": "A", "FECHA": date(2026, 5, 1), "INSTR": "Médico", "ASMA_p": "Si",
                      "ASMA_grav": "Moderado", "ASMA_ctrl": "Controlado", "ASMA_est": "Ingreso"}])
msgs = []
f = a23.procesar(aten, otros=otros, mes=(2026, 7), log=msgs.append)
print("(1) ASMA_p resuelto:", a23._resolver_otros(T._OHDR)["ASMA_p"], "| SALA ASMA A:",
      f.set_index("RUN").loc["A", "SALA ASMA"], "| avisos:", [a[:2] for a in f.attrs.get("avisos", [])])
# (2) nadie 'Pertenece a SALA' -> TODAS las tablas de seccion en 0, aunque el ADA tenga IRA alta
tabs = a23._tablas_a23(f.set_index("RUN"))
print("(2) Pertenece SI:", int((f["Pertenece a SALA"] == "SI").sum()), "| IRA alta en detalle:",
      int((f["REMA23 Ira Alta"] == "SI").sum()), "| suma Ambos de todas las tablas:",
      sum(int(t["Ambos"].sum()) for t in tabs.values()))
# (3) NSP sin 'TIPO DE ATENCION' (otro reporte de citas) y sin AÑOS
T._NSP_HDR[1] = "PRESTACION"; T._NSP_HDR[4] = "EDAD"
nsp = T._mk_nsp([{"instr": "Médico", "tipo": "Control IRA", "fecha": "10-07-2026 09:00:00", "run": "A", "anos": 5}])
d = a23.cargar_inasistentes(nsp, log=msgs.append)
h = a23._seccion_h(d, pd.Timestamp(2026, 7, 1), pd.Timestamp(2026, 7, 31))
print("(3) NSP sin TIPO/AÑOS -> TOTAL H =", int(h.loc[h.Profesional == "TOTAL", "Total"].iloc[0]), "(sin error)")
T._NSP_HDR[1] = "TIPO DE ATENCION"
nsp = T._mk_nsp([{"instr": "Médico", "tipo": "Control IRA", "fecha": "10-07-2026 09:00:00", "run": "A", "anos": 5}])
h = a23._seccion_h(a23.cargar_inasistentes(nsp, log=msgs.append), pd.Timestamp(2026, 7, 1), pd.Timestamp(2026, 7, 31)).set_index("Profesional")
print("    NSP con TIPO pero sin AÑOS: nino de 5 anos cae en", h.loc["Médico/a", ["Menor de 20", "20 y más"]].to_dict())
