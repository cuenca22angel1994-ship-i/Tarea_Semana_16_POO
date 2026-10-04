class Venta:
    def __init__(self, identificador, usuario_id, producto_codigo, cantidad, fecha):
        self.identificador = identificador
        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.cantidad = cantidad
        self.fecha = fecha

    @staticmethod
    def validar_texto(valor, campo):
        if not valor or not valor.strip():
            raise ValueError(f"El campo {campo} no puede estar vacío.")
        return valor.strip()

    @property
    def identificador(self):
        return self._identificador

    @identificador.setter
    def identificador(self, valor):
        self._identificador = self.validar_texto(valor, "identificador")

    @property
    def usuario_id(self):
        return self._usuario_id

    @usuario_id.setter
    def usuario_id(self, valor):
        self._usuario_id = self.validar_texto(valor, "usuario")

    @property
    def producto_codigo(self):
        return self._producto_codigo

    @producto_codigo.setter
    def producto_codigo(self, valor):
        self._producto_codigo = self.validar_texto(valor, "producto")

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        try:
            numero = int(valor)
            if numero <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            raise ValueError("La cantidad debe ser un entero mayor a cero.")
        self._cantidad = numero

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        self._fecha = self.validar_texto(valor, "fecha")