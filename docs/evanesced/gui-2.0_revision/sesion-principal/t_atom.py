import sys
sys.path.insert(0, r"C:\Users\Simon\AppData\Local\Temp\claude\E--git-Autorem\a40108ff-012a-4b37-baf2-2a1dc332a634\scratchpad")
from ed import reemplazar

T = r"E:\git\Autorem\tests\test_gui_registro.py"
reemplazar(T, [
("""    import modulos.rem_sm_actividades as smact
    import modulos.rem_sm_trabajo_perdido as tpmod""",
"""    import modulos.rem_sm_actividades as smact
    import modulos.rem_sm_trabajo_perdido as tpmod
    import programas.rem_utils as ru"""),
("""    parches = [(smact, "procesar", lambda *_a, **_k: E),""",
"""    atomico, atomicos = ru.escribir_atomico, []
    parches = [(ru, "escribir_atomico",
                lambda s, fn: (atomicos.append(Path(s).name), atomico(s, fn))[1]),
               (smact, "procesar", lambda *_a, **_k: E),"""),
("""    assert res["salida"].name == "REM_SM_actividades_2026_08 (1).xlsx", (""",
"""    assert atomicos == ["REM_SM_actividades_2026_08 (1).xlsx",
                        "REM_SM_trabajo_perdido_2026_08 (1).xlsx",
                        "REM_A03_D3_2026_08 (1).xlsx"], (
        f"alguna salida no se escribio via temporal (escribir_atomico): {atomicos}")
    assert res["salida"].name == "REM_SM_actividades_2026_08 (1).xlsx", ("""),
("""    parches = [(a23m, "procesar", lambda *_a, **_k: pd.DataFrame({"x": [1]})),""",
"""    atomico, atomicos = ru.escribir_atomico, []
    parches = [(ru, "escribir_atomico",
                lambda s, fn: (atomicos.append(Path(s).name), atomico(s, fn))[1]),
               (a23m, "procesar", lambda *_a, **_k: pd.DataFrame({"x": [1]})),"""),
("""    assert ra["salida"].name == "REM_A23_2026_08_procesado (1).xlsx", ra["salida"].name""",
"""    assert ra["salida"].name == "REM_A23_2026_08_procesado (1).xlsx", ra["salida"].name
    # El Rescate revienta DENTRO de procesar, antes de escribir: solo A23 y P6 pasan.
    assert atomicos == ["REM_A23_2026_08_procesado (1).xlsx",
                        "REM_SP_P6_2026_08_BETA (1).xlsx"], (
        f"alguna salida no se escribio via temporal (escribir_atomico): {atomicos}")"""),
])
print("ok")
