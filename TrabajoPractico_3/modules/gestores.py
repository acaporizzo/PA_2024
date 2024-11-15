from modules.dominio import Reclamo, Usuario
from modules.config import db
from sqlalchemy.orm.exc import NoResultFound
from modules.modelos import ModeloReclamo, ModeloUsuario
from modules.classifier import ClaimsClassifier
from modules.dominio import Usuario
from datetime import datetime
import uuid

class GestorReclamo:
    def __init__(self, repositorio_reclamos):
        self.repositorio = repositorio_reclamos

    def mostrar_reclamos(self):
        return self.repositorio.obtener_todos_los_registros()

    def mostrar_reclamos_de_usuario(self, usuario):
        return self.repositorio.obtener_registros_seguidas_por_usuario(usuario)

    def crear_reclamo(self, formulario):
        # Crea un nuevo reclamo a partir del formulario
        return Reclamo(*formulario)  # Ajusta según tu clase Reclamo

    def clasificar_reclamo(self, reclamo):
        # Clasifica el reclamo en función de la descripción u otros atributos
        reclamo.departamento = ClaimsClassifier().clasificar(reclamo.descripcion)

    def buscar_reclamos_similares(self, reclamo):
        # Busca reclamos con el mismo departamento y descripción similar
        posibles_reclamos = self.__repo_reclamo.obtener_reclamos_por_departamento(reclamo.departamento)
        return reclamos_similares([(r.descripcion, r.id) for r in posibles_reclamos], reclamo.descripcion)

    def guardar_reclamo(self, reclamo):
        # Guarda el reclamo en el repositorio
        self.__repo_reclamo.guardar_registro(reclamo)

    def adherir_usuario_a_reclamo(self, id_usuario, id_reclamo):
        # Adhiere un usuario a un reclamo
        reclamo = self.__repo_reclamo.obtener_registro_por_id(id_reclamo)
        reclamo.adherir_usuario(id_usuario)
        self.__repo_reclamo.modificar_registro(reclamo)

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
    def __init__(self, repo_usuario):
        self.__repo_usuario = repo_usuario
    def registrar_usuario(self, id, nombre, apellido, nombre_usuario, email, contraseña, claustro, rol, departamento):
        
        if any(usuario.nombre_usuario == nombre_usuario for usuario in self.__repo_usuario.obtener_todos_los_registros()):
            raise ValueError(f"El nombre de usuario '{nombre_usuario}' ya está en uso.")
        
        nuevo_usuario = Usuario(
        id=str(uuid.uuid4()),  #convertimos el UUID a cadena
        nombre=nombre,
        apellido=apellido,
        nombre_usuario=nombre_usuario,
        email=email,
        contraseña=contraseña,
        claustro=claustro,
        rol=rol,
        departamento=departamento
    )
        self.__repo_usuario.guardar_registro(nuevo_usuario)
        return nuevo_usuario
    
    def cargar_usuario_por_nombre(self, nombre_usuario):
        """Carga el usuario desde el repositorio por su nombre de usuario."""
        return self.__repo_usuario.obtener_usuario_por_nombre(nombre_usuario)

    def cargar_usuario(self, id_usuario):
        """Carga el usuario desde el repositorio por su ID."""
        return self.__repo_usuario.obtener_usuario_por_id(id_usuario)
    
class GestorBaseDeDatos:
    def obtener_usuario_por_nombre(self, nombre_usuario):
        try:
            usuario = db.session.query(ModeloUsuario).filtrer_by(nombre_usuario=nombre_usuario).one()
            return usuario
        except NoResultFound: 
            raise Exception("El usuario no fue encontrado")