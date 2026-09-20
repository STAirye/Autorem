import sys; sys.path.insert(0, r"E:\git\Autorem\tests"); sys.dont_write_bytecode = True
import _aislar_cache  # noqa
import test_screening as T
scr = T.scr
# PSC-Y real (puntajes 35-75, RAYEN dice Bajo/Medio/Alto) puesto en el slot GHQ-12
p = T._iris("pscy.xlsx", "Cuestionario para Adolescentes (PSC-Y)", [
    ("11111111-1", 12, "Hombre", "", "", "Ingreso", 40, "Bajo"),
    ("22222222-2", 13, "Mujer",  "", "", "Ingreso", 66, "Medio"),
    ("33333333-3", 11, "Mujer",  "", "", "Egreso", 75, "Alto")])
msgs = []
res = scr.procesar_unificado({"GHQ-12": p}, T._TMP / "o1.xlsx", log=msgs.append)
print("slot GHQ con PSC-Y: total", res["total"], "por_inst", res["por_instrumento"],
      "| D.3 Ambos =", int(res["tabla"]["Ambos"].sum()), "| avisos", res["avisos"])
print("  log:", [m for m in msgs if "FUERA" in m or "aviso" in m][:2])
# GHQ-12 real (0-12) puesto en el slot PSC -> todo < 33 = 'Sin riesgo'
g = T._iris("ghq.xlsx", "Cuestionario de Salud de Goldberg", [
    ("44444444-4", 30, "Mujer", "", "", "Ingreso", 9, "Indicativos de presencia de psicopatologia"),
    ("55555555-5", 40, "Hombre", "", "", "Ingreso", 6, "Sospecha de psicopatologia subumbral")])
msgs = []
res = scr.procesar_unificado({"PSC": g}, T._TMP / "o2.xlsx", log=msgs.append)
print("slot PSC con GHQ: total", res["total"], "por_inst", res["por_instrumento"],
      "| D.3 Ambos =", int(res["tabla"]["Ambos"].sum()), "| avisos", res["avisos"])
print("  detectado por contenido:", scr.detectar_instrumento(*[None]*0) if False else "n/a")
