import customtkinter as ctk
root = ctk.CTk()
log = []
b = ctk.CTkButton(root, text="Precargar", command=lambda: log.append("click_precargar"))
b.pack(); root.update()
root.after(0, lambda: log.append("after_cb"))
# click real encolado (como un usuario impaciente durante el congelamiento)
b._canvas.event_generate("<Enter>", when="tail", x=5, y=5)
b._canvas.event_generate("<ButtonRelease-1>", when="tail", x=5, y=5)
log.append("antes_toplevel")
top = ctk.CTkToplevel(root)
log.append("despues_toplevel")
print(log)
top.destroy(); root.destroy()
