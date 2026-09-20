import sys
sys.path.insert(0, r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\a40108ff-012a-4b37-baf2-2a1dc332a634\scratchpad")
from ed import reemplazar

G = r"E:\git\Autorem\gui\paginas"
reemplazar(G + r"\a23.py", [
("    from programas.rem_utils import rutas_libres\n",
 "    from programas.rem_utils import rutas_libres, escribir_atomico\n"),
("    a23.escribir(fer, salida)\n",
 "    escribir_atomico(salida, lambda p: a23.escribir(fer, p))   # temporal + rename\n"),
])
reemplazar(G + r"\poblacion.py", [
("    from programas.rem_utils import cargar_atenciones, rutas_libres\n",
 "    from programas.rem_utils import cargar_atenciones, rutas_libres, escribir_atomico\n"),
("    p6.escribir(P, resultado, salida)\n",
 "    # Temporal + rename (rem_utils.escribir_atomico): un corte no deja un .xlsx roto.\n"
 "    escribir_atomico(salida, lambda p: p6.escribir(P, resultado, p))\n"),
("        resc.escribir(Er, salida_rescate)\n",
 "        escribir_atomico(salida_rescate, lambda p: resc.escribir(Er, p))\n"),
])
reemplazar(G + r"\sm.py", [
("    from programas.rem_utils import rutas_libres\n",
 "    from programas.rem_utils import rutas_libres, escribir_atomico\n"),
("        smact.escribir(E, salida)\n",
 "        # Temporal + rename (rem_utils.escribir_atomico): un corte no deja un .xlsx roto.\n"
 "        escribir_atomico(salida, lambda p: smact.escribir(E, p))\n"),
("            tpmod.escribir(Etp, salida_tp)\n",
 "            escribir_atomico(salida_tp, lambda p: tpmod.escribir(Etp, p))\n"),
("                r03 = screening.procesar_unificado(a03[\"instrumentos\"], salida_a03,\n"
 "                                                   estamentos=(tabla_est or None),\n"
 "                                                   resolver_estamento=None, log=log)\n",
 "                r03 = {}\n"
 "                escribir_atomico(salida_a03, lambda p: r03.update(screening.procesar_unificado(\n"
 "                    a03[\"instrumentos\"], p, estamentos=(tabla_est or None),\n"
 "                    resolver_estamento=None, log=log)))\n"),
])
print("ok")
