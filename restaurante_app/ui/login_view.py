import tkinter as tk
from pathlib import Path
from tkinter import ttk


class LoginView(tk.Frame):
    def __init__(self, master, servicio, al_ingresar):
        super().__init__(master, bg="#eef3f8")
        self.servicio = servicio
        self.al_ingresar = al_ingresar
        self.usuario_entry = None
        self.clave_entry = None
        self.error_label = None
        self.logo = None
        self._estilo()
        self._construir()

    def _estilo(self):
        est = ttk.Style()
        est.theme_use("clam")
        est.configure(
            "Login.TButton",
            background="#2563eb",
            foreground="#fff",
            font=("Arial", 11, "bold"),
            padding=(14, 8),
            borderwidth=0
        )
        est.map("Login.TButton", background=[("active", "#1d4ed8")])

    def _cargar_logo(self):
        ruta = Path(__file__).resolve().parent.parent / "assets" / "iconos" / "Logo.png"

        if not ruta.exists():
            print(f" No se encontró el logo en: {ruta}")
            return None

        try:
            img = tk.PhotoImage(file=str(ruta))
            self.logo = img.subsample(7, 7)
            return self.logo
        except Exception as e:
            print(f" Error al cargar el logo: {e}")
            return None

    def _construir(self):
        caja = tk.Frame(self, bg="#ffffff", padx=50, pady=20)
        caja.place(relx=0.5, rely=0.5, anchor="center")

        logo = self._cargar_logo()
        if logo:
            tk.Label(caja, image=logo, bg="#ffffff").pack(pady=(0, 10))

        tk.Label(
            caja, text="Inicio de sesión", bg="#ffffff", fg="#516173",
            font=("Arial", 13)
        ).pack(pady=(0, 20))

        tk.Label(
            caja, text="Usuario", bg="#ffffff", fg="#243447",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.usuario_entry = tk.Entry(caja, width=35, font=("Arial", 11))
        self.usuario_entry.pack(pady=(5, 12), ipady=5)
        self.usuario_entry.focus()

        tk.Label(
            caja, text="Contraseña", bg="#ffffff", fg="#243447",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.clave_entry = tk.Entry(caja, width=35, font=("Arial", 11), show="*")
        self.clave_entry.pack(pady=(5, 15), ipady=5)

        self.error_label = tk.Label(
            caja, text="", bg="#ffffff", fg="#b42318", font=("Arial", 10)
        )
        self.error_label.pack(pady=(0, 10))

        btn_ingresar = ttk.Button(
            caja, text="Ingresar", command=self._enviar,
            style="Login.TButton"
        )
        btn_ingresar.pack(fill="x")

        self.clave_entry.bind("<Return>", lambda e: self._enviar())

    def _enviar(self):
        u = self.usuario_entry.get().strip()
        c = self.clave_entry.get().strip()

        if not u or not c:
            self.error_label.config(text="Ingrese usuario y contraseña.")
            return

        usuario = self.servicio.validar_acceso(u, c)
        if not usuario:
            self.error_label.config(text="Credenciales incorrectas.")
            return

        self.error_label.config(text="")
        self.al_ingresar(usuario)