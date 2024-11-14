from datetime import datetime

class Usuario:
    def __init__(self, id, nombre, apellido, email, nombre_usuario, contraseña, claustro,rol, departamento):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.nombre_usuario = nombre_usuario
        self.contraseña = contraseña
        self.claustro = claustro
        self.rol = rol
        self.departamento = departamento

class Reclamo:
    def __init__(self, id_reclamo, usuario, contenido, departamento, estado="pendiente"):
        self.id_reclamo = id_reclamo
        self.usuario = usuario
        self.contenido = contenido
        self.departamento = departamento
        self.fecha_hora = datetime.now()
        self.estado = estado
        self.usuarios_adheridos = []
