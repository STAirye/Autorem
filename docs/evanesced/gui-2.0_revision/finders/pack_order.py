import tkinter as tk

root = tk.Tk()
root.withdraw()
page = tk.Frame(root)
page.pack()

# Mismo orden que gui/app.py._construir_pagina + a05.bloque_archivo_formato / sm.bloque_cuestionarios
titulo = tk.Label(page, text="titulo"); titulo.pack()
banner = tk.Frame(page, name="banner"); banner.pack_forget()          # BannerFuente.__init__
chk_acuse = tk.Checkbutton(page, name="chk_acuse")                    # a05: creado, sin pack
fila_archivo = tk.Frame(page, name="fila_archivo"); fila_archivo.pack()
caja_cuest = tk.Frame(page, name="caja_cuestionarios")                # sm: caja_titulada sin pack
periodo = tk.Frame(page, name="periodo"); periodo.pack()
log = tk.Frame(page, name="log"); log.pack()
barra_botones = tk.Frame(page, name="barra_botones"); barra_botones.pack()

root.update_idletasks()
print("antes :", [w.winfo_name() for w in page.pack_slaves()])

# on_elegido -> banner.mostrar(): `if not winfo_ismapped(): pack(fill='x')`
banner.pack(fill="x")
chk_acuse.pack(anchor="w")          # _aplicar('administrativo')
caja_cuest.pack(fill="x")           # sm._toggle() al marcar 'Incluir cuestionarios'
root.update_idletasks()
print("despues:", [w.winfo_name() for w in page.pack_slaves()])
root.destroy()
