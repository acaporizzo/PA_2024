from modules.dominio import Usuario
import uuid

class GestorUsuario:
    def __init__(self, repositorio_usuarios):
        self.repositorio = repositorio_usuarios

    def registrar_usuario(self, nombre, apellido, nombre_usuario, email, contraseña, claustro, rol, departamento):
        if any(usuario.nombre_usuario == nombre_usuario for usuario in self.repositorio.obtener_todos_los_registros()):
            raise ValueError(f"El nombre de usuario '{nombre_usuario}' ya está en uso.")
        nuevo_usuario = Usuario(
            id=uuid.uuid4(),
            nombre=nombre,
            apellido=apellido,
            nombre_usuario=nombre_usuario,
            email=email,
            contraseña=contraseña,
            claustro=claustro,
            rol=rol,
            departamento=departamento
        )
        self.repositorio.guardar_registro(nuevo_usuario)
        return nuevo_usuario