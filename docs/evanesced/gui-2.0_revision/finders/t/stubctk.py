import sys, types
class _Dummy:
    def __init__(self, *a, **k): pass
    def __getattr__(self, n): return lambda *a, **k: None
m = types.ModuleType("customtkinter")
def _ga(name):
    return type(name, (_Dummy,), {})
m.__getattr__ = _ga
sys.modules["customtkinter"] = m
sys.path.insert(0, r"E:\git\Autorem")
