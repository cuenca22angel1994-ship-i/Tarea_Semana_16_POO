import tkinter as tk
from pathlib import Path
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class AppRestaurante:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Restaurante — Sistema de Gestión")
        self.root.geometry("920x560")
        self.root.minsize(780, 500)
        self.icono = None
        self.icono_chico = None

        ruta_base = Path(__file__).resolve().parent
        self.ruta_icono = ruta_base / "assets" / "logo" / "Logo.png"
        
        print(f" Buscando icono en: {self.ruta_icono}")
        print(f" Existe: {self.ruta_icono.exists()}")
        
        if self.ruta_icono.exists():
            self._establecer_icono()
        
        archivo_serv = ArchivoServicio(ruta_base / "datos")
        self.servicio = RestauranteServicio(archivo_serv)

        self.vista_actual = None
        self._mostrar_login()

    def _establecer_icono(self):
        try:
            self.icono = tk.PhotoImage(file=str(self.ruta_icono))
            self.icono_chico = self.icono.subsample(3, 3)  # Versión pequeña para barra
            self.root.iconphoto(True, self.icono_chico, self.icono)
            print(" Icono puesto correctamente")
        except Exception as e:
            print(f" No se pudo poner icono: {e}")

    def _cambiar_vista(self, nueva):
        if self.vista_actual:
            self.vista_actual.destroy()
        self.vista_actual = nueva
        self.vista_actual.pack(fill="both", expand=True)

    def _mostrar_login(self):
        vista = LoginView(self.root, self.servicio, self._mostrar_principal)
        self._cambiar_vista(vista)

    def _mostrar_principal(self, usuario):
        vista = MainView(self.root, self.servicio, usuario, self._mostrar_login)
        self._cambiar_vista(vista)

    def ejecutar(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AppRestaurante()
    app.ejecutar()