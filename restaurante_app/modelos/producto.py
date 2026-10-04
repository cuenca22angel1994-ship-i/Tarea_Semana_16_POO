class Producto:
    def __init__(self, codigo, nombre, precio, categoria):
        
        self.codigo = self._validar(codigo, "código")
        self.nombre = self._validar(nombre, "nombre")
        self.precio = self._validar_precio(precio)
        self.categoria = self._validar(categoria, "categoría")

    def _validar(self, valor, nombre_campo):
        if valor is None:
            raise ValueError(f"El campo {nombre_campo} no puede estar vacío.")
        limpio = str(valor).strip()
        if not limpio:
            raise ValueError(f"El campo {nombre_campo} no puede estar vacío.")
        return limpio

    def _validar_precio(self, valor):
        try:
            numero = float(valor)
        except (ValueError, TypeError):
            raise ValueError("El precio debe ser un número válido.")
        if numero <= 0:
            raise ValueError("El precio debe ser mayor a cero.")
        return round(numero, 2)