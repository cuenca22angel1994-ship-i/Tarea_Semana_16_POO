import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

class MainView(tk.Frame):
    def __init__(self, master, servicio, usuario_actual, al_salir):
        super().__init__(master, bg="#f7fafc")
        self.servicio = servicio
        self.usuario_actual = usuario_actual
        self.al_salir = al_salir

        self.contenido = None
        self.etiqueta_estado = None
        self.botones_menu = {}
        self.iconos = {}  # Guarda referencias para que no desaparezcan
        # Formularios
        self.usuario_id_entry = None
        self.usuario_nombre_entry = None
        self.usuario_login_entry = None
        self.usuario_clave_entry = None
        self.usuario_rol_combo = None
        self.usuario_rol_etiqueta = None
        self.usuario_seleccionado_id = None
        self.tabla_usuarios = None

        self._definir_estilos()
        self._construir()

    def _definir_estilos(self):
        self.fondo = "#f7fafc"
        self.panel = "#ffffff"
        self.encabezado = "#1f2a44"
        self.texto = "#243447"
        self.secundario = "#dbeafe"
        self.resaltado = "#2563eb"

        est = ttk.Style()
        est.theme_use("clam")
        est.configure("Menu.TButton", background="#334155", foreground="#fff",
                      font=("Arial",10,"bold"), padding=(12,10), borderwidth=0, anchor="w")
        est.map("Menu.TButton", background=[("active","#475569")])
        est.configure("MenuActivo.TButton", background=self.resaltado, foreground="#fff",
                      font=("Arial",10,"bold"), padding=(12,10), borderwidth=0, anchor="w")
        est.map("MenuActivo.TButton", background=[("active","#1d4ed8")])
        est.configure("Sec.TButton", background=self.encabezado, foreground="#fff",
                      font=("Arial",10,"bold"), padding=(10,7), borderwidth=0)
        est.map("Sec.TButton", background=[("active","#334155")])
        est.configure("Ok.TButton", background=self.resaltado, foreground="#fff",
                      font=("Arial",10,"bold"), padding=(10,7), borderwidth=0)
        est.map("Ok.TButton", background=[("active","#1d4ed8")])
        est.configure("Del.TButton", background="#e11d48", foreground="#fff",
                      font=("Arial",10,"bold"), padding=(10,7), borderwidth=0)
        est.map("Del.TButton", background=[("active","#be123c")])
        est.configure("Treeview.Heading", background=self.secundario,
                      foreground=self.encabezado, font=("Arial",10,"bold"))

    def _cargar_icono(self, nombre):
        ruta = Path(__file__).resolve().parent.parent / "assets" / "iconos" / nombre
        if not ruta.exists():
            print(f" Icono no encontrado: {ruta}")
            return None
        try:
            img = tk.PhotoImage(file=str(ruta))
            # Guardar referencia para que no desaparezca
            self.iconos[nombre] = img
            return img
        except Exception as e:
            print(f" Error cargando {nombre}: {e}")
            return None

    def _boton(self, caja, texto, cmd, estilo, icono=None):
        img = self._cargar_icono(icono) if icono else None
        if img:
            return ttk.Button(caja, text=texto, command=cmd, style=estilo,
                              image=img, compound="left")
        return ttk.Button(caja, text=texto, command=cmd, style=estilo)

    def _construir(self):
        # Barra lateral
        sidebar = tk.Frame(self, bg=self.encabezado, width=190, padx=16, pady=18)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="RESTAURANTE", bg=self.encabezado, fg="#fff",
                 font=("Arial",14,"bold")).pack(anchor="w", pady=(0,8))

        tk.Label(sidebar, text=self.usuario_actual.nombre, bg=self.encabezado,
                 fg="#dbeafe", font=("Arial",10), wraplength=150, justify="left").pack(anchor="w", pady=(0,24))

        self._boton_menu(sidebar, "Inicio", self._inicio, "home.png")
        if self.usuario_actual.rol == "Administrador":
            self._boton_menu(sidebar, "Usuarios", self._mostrar_usuarios, "users.png")
        self._boton_menu(sidebar, "Productos", self._mostrar_productos, "restaurant.png")
        self._boton_menu(sidebar, "Ventas", self._mostrar_ventas, "sales.png")

        tk.Frame(sidebar, bg=self.encabezado).pack(fill="both", expand=True)
        self._boton(sidebar, "Cerrar sesión", self.al_salir, "Del.TButton", "logout.png").pack(fill="x", pady=(16,0))

        principal = tk.Frame(self, bg=self.fondo)
        principal.pack(side="left", fill="both", expand=True)
        self.contenido = tk.Frame(principal, bg=self.fondo, padx=28, pady=24)
        self.contenido.pack(fill="both", expand=True)
        pie = tk.Frame(principal, bg=self.secundario, padx=18, pady=8)
        pie.pack(fill="x", side="bottom")
        self.etiqueta_estado = tk.Label(pie, bg=self.secundario, fg=self.texto, font=("Arial",10))
        self.etiqueta_estado.pack(side="left")
        self._inicio()

    def _boton_menu(self, caja, texto, cmd, icono):
        b = self._boton(caja, texto, cmd, "Menu.TButton", icono)
        b.pack(fill="x", pady=(0,8))
        self.botones_menu[texto] = b

    def _marcar(self, seccion):
        for t, b in self.botones_menu.items():
            b.configure(style="MenuActivo.TButton" if t == seccion else "Menu.TButton")

    def _limpiar(self):
        for w in self.contenido.winfo_children():
            w.destroy()

    def _actualizar_estado(self):
        self.etiqueta_estado.config(
            text=f"Usuarios: {self.servicio.cantidad_usuarios()} | "
                 f"Productos: {self.servicio.cantidad_productos()} | "
                 f"Ventas: {self.servicio.cantidad_ventas()} | Datos guardados localmente"
        )

    def _inicio(self):
        self._marcar("Inicio")
        self._limpiar()
        self._actualizar_estado()
        tk.Label(self.contenido, text="Panel Principal", bg=self.fondo,
                 fg=self.encabezado, font=("Arial",20,"bold")).pack(anchor="w", pady=(0,8))
        tk.Label(self.contenido, text="Gestione usuarios, productos y ventas desde el menú.",
                 bg=self.fondo, fg=self.texto, font=("Arial",12)).pack(anchor="w", pady=(0,22))
        caja = tk.Frame(self.contenido, bg=self.fondo)
        caja.pack(fill="x")
        self._tarjeta(caja, "Usuarios", self.servicio.cantidad_usuarios())
        self._tarjeta(caja, "Productos", self.servicio.cantidad_productos())
        self._tarjeta(caja, "Ventas", self.servicio.cantidad_ventas())

    def _tarjeta(self, caja, titulo, valor):
        t = tk.Frame(caja, bg=self.panel, padx=18, pady=16)
        t.pack(side="left", fill="x", expand=True, padx=(0,14))
        tk.Label(t, text=titulo, bg=self.panel, fg=self.texto, font=("Arial",10,"bold")).pack(anchor="w")
        tk.Label(t, text=str(valor), bg=self.panel, fg=self.resaltado,
                 font=("Arial",24,"bold")).pack(anchor="w", pady=(8,0))

    # ══════════════════════════════════════════════════════════════════
    # GESTIÓN DE USUARIOS
    # ══════════════════════════════════════════════════════════════════
    def _mostrar_usuarios(self):
        if self.usuario_actual.rol != "Administrador":
            messagebox.showerror("Acceso denegado", "Solo el administrador puede gestionar usuarios.")
            return

        self._marcar("Usuarios")
        self._limpiar()

        tk.Label(self.contenido, text="Gestión de Usuarios", bg=self.fondo,
                 fg=self.encabezado, font=("Arial",20,"bold")).pack(anchor="w", pady=(0,16))

        cuerpo = tk.Frame(self.contenido, bg=self.fondo)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        form = tk.LabelFrame(cuerpo, text="Datos del Usuario", bg=self.panel,
                             fg=self.encabezado, font=("Arial",10,"bold"), padx=14, pady=14)
        form.grid(row=0, column=0, sticky="n", padx=(0,18))

        self.usuario_id_entry = self._campo(form, "Identificador", 0)
        self.usuario_nombre_entry = self._campo(form, "Nombre", 1)
        self.usuario_login_entry = self._campo(form, "Usuario (login)", 2)
        self.usuario_clave_entry = self._campo(form, "Contraseña", 3, show="*")

        tk.Label(form, text="Rol", bg=self.panel, fg=self.texto, font=("Arial",10,"bold")
                 ).grid(row=4, column=0, sticky="w", pady=(0,8), padx=(0,10))
        self.usuario_rol_combo = ttk.Combobox(form, values=("Empleado", "Cliente"), state="readonly", width=25)
        self.usuario_rol_combo.grid(row=4, column=1, sticky="ew", pady=(0,8))
        self.usuario_rol_combo.set("Cliente")

        self.usuario_rol_etiqueta = tk.Label(form, text="Rol seleccionado: Cliente", bg=self.panel, fg=self.texto, font=("Arial",9))
        self.usuario_rol_etiqueta.grid(row=5, column=0, columnspan=2, sticky="w", pady=(0,8))

        acciones = tk.Frame(form, bg=self.panel)
        acciones.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(12,0))

        botones = [
            ("Registrar", self._registrar_usuario, "Ok.TButton", "add.png"),
            ("Actualizar", self._actualizar_usuario, "Ok.TButton", "edit.png"),
            ("Eliminar", self._eliminar_usuario, "Del.TButton", "delete.png"),
            ("Limpiar", self._limpiar_formulario_usuario, "Sec.TButton", "clean.png"),
        ]
        for txt, cmd, est, ico in botones:
            self._boton(acciones, txt, cmd, est, ico).pack(fill="x", pady=(0,7))

        caja_tabla = tk.LabelFrame(cuerpo, text="Usuarios Registrados", bg=self.panel,
                                   fg=self.encabezado, font=("Arial",10,"bold"), padx=12, pady=12)
        caja_tabla.grid(row=0, column=1, sticky="nsew")
        frame_t = tk.Frame(caja_tabla, bg=self.panel)
        frame_t.pack(fill="both", expand=True)
        self.tabla_usuarios = ttk.Treeview(frame_t, columns=("id","nombre","usuario","rol"), show="headings", height=12)
        barra = ttk.Scrollbar(frame_t, orient="vertical", command=self.tabla_usuarios.yview)
        self.tabla_usuarios.configure(yscrollcommand=barra.set)
        for col, etq in [("id","Identificador"),("nombre","Nombre"),("usuario","Usuario"),("rol","Rol")]:
            self.tabla_usuarios.heading(col, text=etq)
            self.tabla_usuarios.column(col, width=150)
        self.tabla_usuarios.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        self.tabla_usuarios.bind("<<TreeviewSelect>>", self._al_seleccionar_fila)
        self.usuario_rol_combo.bind("<Return>", self._al_presionar_enter)
        for w in (self.usuario_id_entry, self.usuario_nombre_entry,
                  self.usuario_login_entry, self.usuario_clave_entry,
                  self.usuario_rol_combo, self.tabla_usuarios):
            w.bind("<Escape>", self._al_presionar_escape)
        self.usuario_rol_combo.bind("<<ComboboxSelected>>", self._al_cambiar_rol)

        self._refrescar_tabla_usuarios()

    def _campo(self, caja, etiqueta, fila, show=None):
        tk.Label(caja, text=etiqueta, bg=self.panel, fg=self.texto, font=("Arial",10,"bold")
                 ).grid(row=fila, column=0, sticky="w", pady=(0,8), padx=(0,10))
        e = tk.Entry(caja, width=28, font=("Arial",10), show=show)
        e.grid(row=fila, column=1, sticky="ew", pady=(0,8))
        return e

    def _datos_formulario_usuario(self):
        return (
            self.usuario_id_entry.get(),
            self.usuario_nombre_entry.get(),
            self.usuario_login_entry.get(),
            self.usuario_clave_entry.get(),
            self.usuario_rol_combo.get(),
        )

    def _al_seleccionar_fila(self, evento):
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return
        valores = self.tabla_usuarios.item(seleccion[0], "values")
        if not valores:
            return
        identificador = valores[0]
        usuario = self.servicio.buscar_usuario_por_identificador(identificador)
        if not usuario:
            return
        self._limpiar_campos_usuario()
        self.usuario_seleccionado_id = usuario.identificador
        self.usuario_id_entry.insert(0, usuario.identificador)
        self.usuario_nombre_entry.insert(0, usuario.nombre)
        self.usuario_login_entry.insert(0, usuario.usuario)
        self.usuario_clave_entry.insert(0, usuario.contrasena)
        if usuario.identificador == self.usuario_actual.identificador and usuario.rol == "Administrador":
            self.usuario_rol_combo.configure(values=("Administrador",), state="disabled")
        else:
            self.usuario_rol_combo.configure(values=("Empleado", "Cliente"), state="readonly")
        self.usuario_rol_combo.set(usuario.rol)
        self.usuario_rol_etiqueta.config(text=f"Rol seleccionado: {usuario.rol}")

    def _al_presionar_enter(self, evento):
        self._registrar_usuario()

    def _al_presionar_escape(self, evento):
        self._limpiar_formulario_usuario()

    def _al_cambiar_rol(self, evento):
        self.usuario_rol_etiqueta.config(text=f"Rol seleccionado: {self.usuario_rol_combo.get()}")

    def _registrar_usuario(self):
        try:
            self.servicio.registrar_usuario(*self._datos_formulario_usuario())
            self._limpiar_formulario_usuario()
            self._refrescar_tabla_usuarios()
            messagebox.showinfo("Usuarios", "Usuario registrado correctamente.")
        except ValueError as err:
            messagebox.showerror("Error", str(err))

    def _actualizar_usuario(self):
        if not self.usuario_seleccionado_id:
            messagebox.showerror("Usuarios", "Seleccione un usuario de la tabla.")
            return
        datos = self._datos_formulario_usuario()
        if datos[0] != self.usuario_seleccionado_id:
            messagebox.showerror("Usuarios", "No modifique el identificador del usuario seleccionado.")
            return
        try:
            self.servicio.actualizar_usuario(*datos, self.usuario_actual.identificador)
            self._refrescar_tabla_usuarios()
            messagebox.showinfo("Usuarios", "Usuario actualizado correctamente.")
        except ValueError as err:
            messagebox.showerror("Error", str(err))

    def _eliminar_usuario(self):
        if not self.usuario_seleccionado_id:
            messagebox.showerror("Usuarios", "Seleccione un usuario de la tabla.")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar este usuario?"):
            return
        try:
            self.servicio.eliminar_usuario(self.usuario_seleccionado_id, self.usuario_actual.identificador)
            self._limpiar_formulario_usuario()
            self._refrescar_tabla_usuarios()
            messagebox.showinfo("Usuarios", "Usuario eliminado.")
        except ValueError as err:
            messagebox.showerror("Error", str(err))

    def _limpiar_campos_usuario(self):
        for e in (self.usuario_id_entry, self.usuario_nombre_entry,
                  self.usuario_login_entry, self.usuario_clave_entry):
            e.delete(0, tk.END)

    def _limpiar_formulario_usuario(self):
        self._limpiar_campos_usuario()
        self.usuario_seleccionado_id = None
        self.usuario_rol_combo.configure(values=("Empleado", "Cliente"), state="readonly")
        self.usuario_rol_combo.set("Cliente")
        self.usuario_rol_etiqueta.config(text="Rol seleccionado: Cliente")
        for item in self.tabla_usuarios.selection():
            self.tabla_usuarios.selection_remove(item)
        self.usuario_id_entry.focus()

    def _refrescar_tabla_usuarios(self):
        for fila in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(fila)
        for u in self.servicio.listar_usuarios():
            self.tabla_usuarios.insert("", tk.END, values=(u.identificador, u.nombre, u.usuario, u.rol))
        self._actualizar_estado()

    # ══════════════════════════════════════════════════════════════════
    # PRODUCTOS
    # ══════════════════════════════════════════════════════════════════
    def _mostrar_productos(self):
        self._marcar("Productos")
        self._limpiar()

        tk.Label(self.contenido, text="Gestión de Productos", bg=self.fondo,
                 fg=self.encabezado, font=("Arial",20,"bold")).pack(anchor="w", pady=(0,16))

        cuerpo = tk.Frame(self.contenido, bg=self.fondo)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        form = tk.LabelFrame(cuerpo, text="Datos del Producto", bg=self.panel,
                             fg=self.encabezado, font=("Arial",10,"bold"), padx=14, pady=14)
        form.grid(row=0, column=0, sticky="n", padx=(0,18))

        self.prod_codigo_entry = self._campo(form, "Código", 0)
        self.prod_nombre_entry = self._campo(form, "Nombre", 1)
        self.prod_precio_entry = self._campo(form, "Precio", 2)
        self.prod_categoria_entry = self._campo(form, "Categoría", 3)

        acciones = tk.Frame(form, bg=self.panel)
        acciones.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(12,0))

        botones = [
            ("Registrar", self._registrar_producto, "Ok.TButton", "add.png"),
            ("Actualizar", self._actualizar_producto, "Ok.TButton", "edit.png"),
            ("Eliminar", self._eliminar_producto, "Del.TButton", "delete.png"),
            ("Limpiar", self._limpiar_formulario_producto, "Sec.TButton", "clean.png"),
        ]
        for txt, cmd, est, ico in botones:
            self._boton(acciones, txt, cmd, est, ico).pack(fill="x", pady=(0,7))

        caja_tabla = tk.LabelFrame(cuerpo, text="Productos Registrados", bg=self.panel,
                                   fg=self.encabezado, font=("Arial",10,"bold"), padx=12, pady=12)
        caja_tabla.grid(row=0, column=1, sticky="nsew")
        frame_t = tk.Frame(caja_tabla, bg=self.panel)
        frame_t.pack(fill="both", expand=True)
        self.tabla_productos = ttk.Treeview(frame_t, columns=("codigo","nombre","precio","categoria"), show="headings", height=12)
        barra = ttk.Scrollbar(frame_t, orient="vertical", command=self.tabla_productos.yview)
        self.tabla_productos.configure(yscrollcommand=barra.set)
        for col, etq in [("codigo","Código"),("nombre","Nombre"),("precio","Precio"),("categoria","Categoría")]:
            self.tabla_productos.heading(col, text=etq)
            self.tabla_productos.column(col, width=140)
        self.tabla_productos.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        self.tabla_productos.bind("<<TreeviewSelect>>", self._al_seleccionar_producto)
        for w in (self.prod_codigo_entry, self.prod_nombre_entry,
                  self.prod_precio_entry, self.prod_categoria_entry, self.tabla_productos):
            w.bind("<Return>", self._al_enter_producto)
            w.bind("<Escape>", self._al_escape_producto)

        self._refrescar_tabla_productos()

    def _datos_formulario_producto(self):
        return (
            self.prod_codigo_entry.get().strip(),
            self.prod_nombre_entry.get().strip(),
            self.prod_precio_entry.get().strip(),
            self.prod_categoria_entry.get().strip(),
        )

    def _al_seleccionar_producto(self, evento):
        seleccion = self.tabla_productos.selection()
        if not seleccion: return
        valores = self.tabla_productos.item(seleccion[0], "values")
        self._limpiar_campos_producto()
        self.prod_codigo_entry.insert(0, valores[0])
        self.prod_nombre_entry.insert(0, valores[1])
        self.prod_precio_entry.insert(0, valores[2])
        self.prod_categoria_entry.insert(0, valores[3])

    def _al_enter_producto(self, evento):
        self._registrar_producto()

    def _al_escape_producto(self, evento):
        self._limpiar_formulario_producto()

    def _registrar_producto(self):
        try:
            self.servicio.registrar_producto(*self._datos_formulario_producto())
            self._limpiar_formulario_producto()
            self._refrescar_tabla_productos()
            messagebox.showinfo("Productos", "Producto registrado correctamente.")
        except ValueError as err:
            messagebox.showerror("Error", str(err))

    def _actualizar_producto(self):
        try:
            self.servicio.actualizar_producto(*self._datos_formulario_producto())
            self._limpiar_formulario_producto()
            self._refrescar_tabla_productos()
            messagebox.showinfo("Productos", "Producto actualizado correctamente.")
        except ValueError as err:
            messagebox.showerror("Error", str(err))

    def _eliminar_producto(self):
        codigo = self.prod_codigo_entry.get().strip()
        if not codigo:
            messagebox.showerror("Productos", "Seleccione un producto de la tabla.")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar este producto?"):
            return
        try:
            self.servicio.eliminar_producto(codigo)
            self._limpiar_formulario_producto()
            self._refrescar_tabla_productos()
            messagebox.showinfo("Productos", "Producto eliminado.")
        except ValueError as err:
            messagebox.showerror("Error", str(err))

    def _limpiar_campos_producto(self):
        for e in (self.prod_codigo_entry, self.prod_nombre_entry,
                  self.prod_precio_entry, self.prod_categoria_entry):
            e.delete(0, tk.END)

    def _limpiar_formulario_producto(self):
        self._limpiar_campos_producto()
        for item in self.tabla_productos.selection():
            self.tabla_productos.selection_remove(item)
        self.prod_codigo_entry.focus()

    def _refrescar_tabla_productos(self):
        for fila in self.tabla_productos.get_children():
            self.tabla_productos.delete(fila)
        for p in self.servicio.listar_productos():
            self.tabla_productos.insert("", tk.END, values=(p.codigo, p.nombre, p.precio, p.categoria))
        self._actualizar_estado()

    # ══════════════════════════════════════════════════════════════════
    # VENTAS
    # ══════════════════════════════════════════════════════════════════
    def _mostrar_ventas(self):
        self._marcar("Ventas")
        self._limpiar()

        tk.Label(self.contenido, text="Registro de Ventas", bg=self.fondo,
                 fg=self.encabezado, font=("Arial",20,"bold")).pack(anchor="w", pady=(0,16))

        cuerpo = tk.Frame(self.contenido, bg=self.fondo)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        form = tk.LabelFrame(cuerpo, text="Datos de la Venta", bg=self.panel,
                             fg=self.encabezado, font=("Arial",10,"bold"), padx=14, pady=14)
        form.grid(row=0, column=0, sticky="n", padx=(0,18))

        tk.Label(form, text="Usuario", bg=self.panel, fg=self.texto, font=("Arial",10,"bold")
                 ).grid(row=0, column=0, sticky="w", pady=(0,8), padx=(0,10))
        self.venta_usuario_combo = ttk.Combobox(form, state="readonly", width=25)
        self.venta_usuario_combo.grid(row=0, column=1, sticky="ew", pady=(0,8))
        self.venta_usuario_combo['values'] = [f"{u.identificador} - {u.nombre}" for u in self.servicio.listar_usuarios()]

        tk.Label(form, text="Producto", bg=self.panel, fg=self.texto, font=("Arial",10,"bold")
                 ).grid(row=1, column=0, sticky="w", pady=(0,8), padx=(0,10))
        self.venta_producto_combo = ttk.Combobox(form, state="readonly", width=25)
        self.venta_producto_combo.grid(row=1, column=1, sticky="ew", pady=(0,8))
        self.venta_producto_combo['values'] = [f"{p.codigo} - {p.nombre}" for p in self.servicio.listar_productos()]

        tk.Label(form, text="Cantidad", bg=self.panel, fg=self.texto, font=("Arial",10,"bold")
                 ).grid(row=2, column=0, sticky="w", pady=(0,8), padx=(0,10))
        self.venta_cantidad_entry = tk.Entry(form, width=28, font=("Arial",10))
        self.venta_cantidad_entry.grid(row=2, column=1, sticky="ew", pady=(0,8))

        acciones = tk.Frame(form, bg=self.panel)
        acciones.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(12,0))

        botones = [
            ("Registrar Venta", self._registrar_venta, "Ok.TButton", "add.png"),
            ("Limpiar", self._limpiar_formulario_venta, "Sec.TButton", "clean.png"),
        ]
        for txt, cmd, est, ico in botones:
            self._boton(acciones, txt, cmd, est, ico).pack(fill="x", pady=(0,7))

        caja_tabla = tk.LabelFrame(cuerpo, text="Ventas Realizadas", bg=self.panel,
                                   fg=self.encabezado, font=("Arial",10,"bold"), padx=12, pady=12)
        caja_tabla.grid(row=0, column=1, sticky="nsew")
        frame_t = tk.Frame(caja_tabla, bg=self.panel)
        frame_t.pack(fill="both", expand=True)
        self.tabla_ventas = ttk.Treeview(frame_t, columns=("id","usuario","producto","cantidad","fecha"), show="headings", height=12)
        barra = ttk.Scrollbar(frame_t, orient="vertical", command=self.tabla_ventas.yview)
        self.tabla_ventas.configure(yscrollcommand=barra.set)
        for col, etq in [("id","ID Venta"),("usuario","Usuario"),("producto","Producto"),("cantidad","Cantidad"),("fecha","Fecha")]:
            self.tabla_ventas.heading(col, text=etq)
            self.tabla_ventas.column(col, width=110)
        self.tabla_ventas.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        for w in (self.venta_usuario_combo, self.venta_producto_combo, self.venta_cantidad_entry):
            w.bind("<Return>", self._al_enter_venta)
            w.bind("<Escape>", self._al_escape_venta)

        self._refrescar_tabla_ventas()

    def _al_enter_venta(self, evento):
        self._registrar_venta()

    def _al_escape_venta(self, evento):
        self._limpiar_formulario_venta()

    def _registrar_venta(self):
        usuario_sel = self.venta_usuario_combo.get()
        producto_sel = self.venta_producto_combo.get()
        cantidad = self.venta_cantidad_entry.get().strip()

        if not usuario_sel or not producto_sel or not cantidad:
            messagebox.showwarning("Aviso", "Complete todos los campos.")
            return

        usuario_id = usuario_sel.split(" - ")[0]
        producto_codigo = producto_sel.split(" - ")[0]

        try:
            self.servicio.registrar_venta(usuario_id, producto_codigo, cantidad)
            self._limpiar_formulario_venta()
            self._refrescar_tabla_ventas()
            messagebox.showinfo("Ventas", "Venta registrada correctamente.")
        except ValueError as err:
            messagebox.showerror("Error", str(err))

    def _limpiar_formulario_venta(self):
        self.venta_usuario_combo.set("")
        self.venta_producto_combo.set("")
        self.venta_cantidad_entry.delete(0, tk.END)
        self.venta_usuario_combo.focus()

    def _refrescar_tabla_ventas(self):
        for fila in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(fila)
        for v in self.servicio.listar_ventas():
            usuario = self.servicio.buscar_usuario_por_identificador(v.usuario_id)
            nombre_usuario = usuario.nombre if usuario else v.usuario_id
            producto = self.servicio.buscar_producto_por_codigo(v.producto_codigo)
            nombre_producto = producto.nombre if producto else v.producto_codigo
            self.tabla_ventas.insert("", tk.END, values=(
                v.identificador, nombre_usuario, nombre_producto, v.cantidad, v.fecha
            ))
        self._actualizar_estado()