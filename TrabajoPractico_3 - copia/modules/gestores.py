from modules.dominio import Reclamo, Usuario
from modules.config import db
from sqlalchemy.orm.exc import NoResultFound
from modules.modelos import ModeloReclamo, ModeloUsuario
from datetime import datetime
import uuid

class GestorReclamo:
    def __init__(self, repositorio_reclamos):
        self.repositorio = repositorio_reclamos

    def mostrar_reclamos(self):
        return self.repositorio.obtener_todos_los_registros()

    def mostrar_reclamos_de_usuario(self, usuario):
        return self.repositorio.obtener_registros_seguidas_por_usuario(usuario)

    def crear_reclamo(self, usuario, contenido, departamento):
        nuevo_reclamo = Reclamo(
            id_reclamo=uuid.uuid4(),
            usuario=usuario,
            contenido=contenido,
            departamento=departamento,
            fecha_hora=datetime.now(),
            estado="pendiente",
            usuarios_adheridos=[usuario]
        )
        self.repositorio.guardar_registro(nuevo_reclamo)
        return nuevo_reclamo
    
    def clasificar_reclamo(self, claim):
        """Recibe el reclamo (objeto) y lo clasifica"""
        depto=self.__clasificador.clasificar([claim.get_descripcion])
        claim.set_depto(depto[0])

    def adherir_a_reclamo(self, id_reclamo, usuario):
        reclamo = self.repositorio.obtener_registro_por_filtro("id_reclamo", id_reclamo)
        if reclamo and usuario not in reclamo.usuarios_adheridos:
            reclamo.usuarios_adheridos.append(usuario)
            self.repositorio.modificar_registro(reclamo)
            return True
        return False

    def derivar_reclamo(self, id_reclamo, nuevo_departamento):
        reclamo = self.repositorio.obtener_registro_por_filtro("id_reclamo", id_reclamo)
        if reclamo:
            reclamo.departamento = nuevo_departamento
            self.repositorio.modificar_registro(reclamo)
            return reclamo
        return None

    def modificar_estado_reclamo(self, id_reclamo, nuevo_estado):
        reclamo = self.repositorio.obtener_registro_por_filtro("id_reclamo", id_reclamo)
        if reclamo:
            reclamo.estado = nuevo_estado
            self.repositorio.modificar_registro(reclamo)
            return reclamo
        return None

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
    
class GestorBaseDeDatos:
    def obtener_usuario_por_nombre(self, nombre_usuario):
        try:
            usuario = db.session.query(ModeloUsuario).filtrer_by(nombre_usuario=nombre_usuario).one()
            return usuario
        except NoResultFound: 
            raise Exception("El usuario no fue encontrado")