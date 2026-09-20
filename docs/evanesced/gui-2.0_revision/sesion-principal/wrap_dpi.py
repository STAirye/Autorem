import customtkinter as ctk
from gui import widgets
for esc in (1.0, 1.5):
    ctk.set_widget_scaling(esc)
    root = ctk.CTk(); root.geometry("600x300")
    caja = ctk.CTkFrame(root); caja.pack(fill="x", padx=10)
    lbl = widgets.etiqueta_envolvente(caja, "palabra " * 80)
    lbl.pack(fill="x", padx=8)
    for _ in range(5): root.update()
    print(f"scaling={esc}: ancho caja={caja.winfo_width()} wraplength_tk={lbl._label.cget('wraplength')} ancho_label_pedido={lbl._label.winfo_reqwidth()}")
    root.destroy()
