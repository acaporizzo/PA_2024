from datetime import datetime

# Archivo de definición de la clase Usuario

class Usuario:
    def __init__(self, id, nombre, apellido, nombre_usuario, email, contraseña, claustro, rol=None, departamento=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.nombre_usuario = nombre_usuario
        self.email = email
        self.contraseña = contraseña
        self.claustro = claustro
        self.rol = rol
        self.departamento = departamento

    def generar_datos_reclamo(self, descripcion):
        """Genera un formulario de datos para crear un reclamo."""
        # Retorna una lista con los datos básicos del reclamo
        return [
            descripcion,      # Descripción del reclamo
            "pendiente",      # Estado inicial del reclamo
            self.departamento, # Departamento asociado al usuario
            str(datetime.now()),  # Fecha y hora actuales como string
            self.id           # ID del usuario que crea el reclamo
        ]

class Reclamo:
    def __init__(self, id_reclamo, usuario, contenido, departamento, estado="pendiente"):
        self.id_reclamo = id_reclamo
        self.usuario = usuario
        self.contenido = contenido
        self.departamento = departamento
        self.fecha_hora = datetime.now()
        self.estado = estado
        self.usuarios_adheridos = []
