from datetime import date
from modelos.usuario import Usuario
from modelos.producto import Producto
from modelos.venta import Venta


class RestauranteServicio:
    def __init__(self, archivo_servicio):
        self.archivo_servicio = archivo_servicio
        self.usuarios = []
        self.productos = []
        self.ventas = []
        self.cargar_datos()

    def cargar_datos(self):
        usuarios_json = self.archivo_servicio.leer_json("usuarios.json")
        productos_json = self.archivo_servicio.leer_json("productos.json")
        ventas_json = self.archivo_servicio.leer_json("ventas.json")

        self.usuarios = [
            Usuario(
                datos.get("identificador", "").strip(),
                datos.get("nombre", "").strip(),
                datos.get("usuario", "").strip(),
                datos.get("contraseña", datos.get("contrasena", "")).strip(),
                datos.get("rol", "Cliente").strip(),
            )
            for datos in usuarios_json
        ]

        self.productos = []
        for datos in productos_json:
            codigo = datos.get("codigo", "").strip()
            nombre = datos.get("nombre", "").strip()
            precio = datos.get("precio", 0)
            categoria = datos.get("categoria", "").strip()

            if not categoria:
                categoria = "Sin categoría"

            self.productos.append(Producto(codigo, nombre, precio, categoria))

        self.ventas = [
            Venta(
                datos.get("identificador", "").strip(),
                datos.get("usuario_id", "").strip(),
                datos.get("producto_codigo", "").strip(),
                datos.get("cantidad", 1),
                datos.get("fecha", "").strip(),
            )
            for datos in ventas_json
        ]

    def validar_acceso(self, usuario, contrasena):
        for u in self.usuarios:
            if u.usuario == usuario and u.contrasena == contrasena:
                return u
        return None

    def cantidad_usuarios(self): return len(self.usuarios)
    def cantidad_productos(self): return len(self.productos)
    def cantidad_ventas(self): return len(self.ventas)

    def listar_usuarios(self): return self.usuarios
    def listar_productos(self): return self.productos
    def listar_ventas(self): return self.ventas

    def guardar_usuarios(self):
        datos = [
            {
                "identificador": u.identificador,
                "nombre": u.nombre,
                "usuario": u.usuario,
                "contraseña": u.contrasena,
                "rol": u.rol,
            }
            for u in self.usuarios
        ]
        self.archivo_servicio.escribir_json("usuarios.json", datos)

    def guardar_productos(self):
        datos = [
            {
                "codigo": p.codigo,
                "nombre": p.nombre,
                "precio": p.precio,
                "categoria": p.categoria,
            }
            for p in self.productos
        ]
        self.archivo_servicio.escribir_json("productos.json", datos)

    def guardar_ventas(self):
        datos = [
            {
                "identificador": v.identificador,
                "usuario_id": v.usuario_id,
                "producto_codigo": v.producto_codigo,
                "cantidad": v.cantidad,
                "fecha": v.fecha,
            }
            for v in self.ventas
        ]
        self.archivo_servicio.escribir_json("ventas.json", datos)

    def buscar_usuario_por_identificador(self, identificador):
        identificador = identificador.strip()
        for u in self.usuarios:
            if u.identificador == identificador:
                return u
        return None

    def buscar_usuario_por_nombre_usuario(self, nombre_usuario):
        nombre_usuario = nombre_usuario.strip()
        for u in self.usuarios:
            if u.usuario == nombre_usuario:
                return u
        return None

    def buscar_producto_por_codigo(self, codigo):
        codigo = codigo.strip()
        for p in self.productos:
            if p.codigo == codigo:
                return p
        return None

    # === USUARIOS ===
    def registrar_usuario(self, identificador, nombre, usuario, contrasena, rol):
        nuevo = Usuario(identificador, nombre, usuario, contrasena, rol)
        if nuevo.rol == "Administrador":
            raise ValueError("No se pueden registrar nuevos administradores desde esta pantalla.")
        if self.buscar_usuario_por_identificador(nuevo.identificador):
            raise ValueError("Ya existe un usuario con ese identificador.")
        if self.buscar_usuario_por_nombre_usuario(nuevo.usuario):
            raise ValueError("Ya existe un usuario con ese nombre de usuario.")
        self.usuarios.append(nuevo)
        self.guardar_usuarios()
        return nuevo

    def actualizar_usuario(self, identificador, nombre, usuario, contrasena, rol, id_actual=None):
        actual = self.buscar_usuario_por_identificador(identificador)
        if not actual:
            raise ValueError("No existe el usuario.")
        datos = Usuario(identificador, nombre, usuario, contrasena, rol)
        otro = self.buscar_usuario_por_nombre_usuario(datos.usuario)
        if otro and otro.identificador != actual.identificador:
            raise ValueError("Ese nombre de usuario ya está en uso.")
        if id_actual == actual.identificador and actual.rol == "Administrador" and datos.rol != "Administrador":
            raise ValueError("No puede cambiar el rol del administrador actual.")
        actual.nombre = datos.nombre
        actual.usuario = datos.usuario
        actual.contrasena = datos.contrasena
        actual.rol = datos.rol
        self.guardar_usuarios()
        return actual

    def eliminar_usuario(self, identificador, id_actual=None):
        actual = self.buscar_usuario_por_identificador(identificador)
        if not actual:
            raise ValueError("No existe el usuario.")
        if actual.identificador == id_actual:
            raise ValueError("No puede eliminar su propia cuenta.")
        self.usuarios.remove(actual)
        self.guardar_usuarios()
        return actual

    # === PRODUCTOS ===
    def registrar_producto(self, codigo, nombre, precio, categoria):
        categoria = categoria.strip()
        if not categoria:
            raise ValueError("El campo categoría no puede estar vacío.")
        try:
            precio_num = float(precio)
        except (ValueError, TypeError):
            raise ValueError("El precio debe ser un número válido.")
        if precio_num <= 0:
            raise ValueError("El precio debe ser mayor a cero.")
        nuevo = Producto(codigo, nombre, precio_num, categoria)
        if self.buscar_producto_por_codigo(nuevo.codigo):
            raise ValueError("Producto con ese código ya existe.")
        self.productos.append(nuevo)
        self.guardar_productos()
        return nuevo

    def actualizar_producto(self, codigo, nombre, precio, categoria):
        categoria = categoria.strip()
        if not categoria:
            raise ValueError("El campo categoría no puede estar vacío.")
        actual = self.buscar_producto_por_codigo(codigo)
        if not actual:
            raise ValueError("Producto no encontrado.")
        try:
            precio_num = float(precio)
        except (ValueError, TypeError):
            raise ValueError("El precio debe ser un número válido.")
        if precio_num <= 0:
            raise ValueError("El precio debe ser mayor a cero.")
        actual.nombre = nombre
        actual.precio = precio_num
        actual.categoria = categoria
        self.guardar_productos()
        return actual

    def eliminar_producto(self, codigo):
        actual = self.buscar_producto_por_codigo(codigo)
        if not actual:
            raise ValueError("Producto no encontrado.")
        self.productos.remove(actual)
        self.guardar_productos()
        return actual

    # === VENTAS ===
    def generar_id_venta(self):
        return f"V{len(self.ventas)+1:03d}"

    def registrar_venta(self, usuario_id, producto_codigo, cantidad):
        usuario_id = usuario_id.strip()
        producto_codigo = producto_codigo.strip()
        if not usuario_id:
            raise ValueError("Seleccione un usuario.")
        if not producto_codigo:
            raise ValueError("Seleccione un producto.")
        if not self.buscar_usuario_por_identificador(usuario_id):
            raise ValueError("El usuario no existe.")
        if not self.buscar_producto_por_codigo(producto_codigo):
            raise ValueError("El producto no existe.")
        try:
            cant_num = int(cantidad)
        except ValueError:
            raise ValueError("La cantidad debe ser un número entero.")
        if cant_num <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")
        nueva = Venta(
            self.generar_id_venta(),
            usuario_id,
            producto_codigo,
            cant_num,
            date.today().isoformat()
        )
        self.ventas.append(nueva)
        self.guardar_ventas()
        return nueva