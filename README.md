# Tarea_Semana_16_POO
Manejo de eventos aplicado a la gestión de usuarios en restaurante_app
# Alumno:
Angel Rafael Cuenca Tamayo

# Propósito
Aplicación de gestión para restaurante desarrollada en Python con Tkinter, enfocada en el manejo de eventos aplicado a la administración de usuarios.

# Evolución del proyecto
Esta versión mantiene toda la arquitectura modular de semanas anteriores y amplía la sección de **Usuarios** con:
- Atributo `rol` en el modelo (`Administrador`, `Empleado`, `Cliente`)
- Gestión completa mediante formulario + tabla Treeview
- Eventos de interfaz para mejorar la experiencia de uso

## Estructura
 
restaurante_app/
├── datos/            # Archivos JSON de persistencia
├── modelos/          # Clases de entidad: Usuario, Producto, Venta
├── servicios/        # Lógica de negocio y acceso a datos
├── ui/               # Vistas: Login y Pantalla Principal
├── assets/           # Logo, íconos y recursos visuales
├── main.py           # Punto de entrada
└── README.md
 
# Gestión de Usuarios
- **Administrador**: acceso completo a Usuarios, Productos y Ventas
- **Empleado / Cliente**: no ven la sección de Usuarios
- Se evita eliminar la propia cuenta del administrador activo
- No se puede cambiar el rol del administrador actual

## Eventos implementados
| Evento | Mecanismo | Acción |
|---|---|---|
| `<<TreeviewSelect>>` | `bind()` | Carga los datos del usuario seleccionado en el formulario |
| `<Return>` | `bind()` | Ejecuta el registro del usuario |
| `<Escape>` | `bind()` | Limpia el formulario y quita la selección |
| `<<ComboboxSelected>>` | `bind()` | Actualiza el texto con el rol elegido |
| Botones (`Registrar`, `Actualizar`, `Eliminar`) | `command=` | Ejecutan la acción correspondiente directamente |

> **Diferencia clave**: `command=` asigna la acción al hacer clic; `bind()` asocia respuestas a interacciones del teclado o cambios de componente.

## Persistencia
Los datos se guardan en `datos/usuarios.json` con todos los campos incluyendo el rol. Al reiniciar la aplicación se recuperan automáticamente.

#  Resumen de lo implementado
-  Modelo `Usuario` con atributo `rol` y validación
-  `RestauranteServicio` con CRUD completo y reglas de negocio
-  `MainView` con **todos los eventos de la Semana 16** aplicados: `<<TreeviewSelect>>`, `<Return>`, `<Escape>`, `<<ComboboxSelected>>`
-  Separación clara entre `bind()` para eventos de interfaz y `command=` para botones
-  Persistencia en `usuarios.json`
-  Protección del administrador
