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

    def clasificar_reclamo(self, reclamo):
        reclamo.clasificacion = ClaimsClassifier().clasificar(reclamo.descripcion)

    def crear_reclamo(self, formulario):
        """
        Crea y guarda un nuevo reclamo a partir del formulario.
        """
        nuevo_reclamo = Reclamo(*formulario)
        self.repositorio.insertar_reclamo(nuevo_reclamo)
        return nuevo_reclamo

    def obtener_registro_por_filtro(self, filtro, valor):
        """
        Obtiene un único registro que cumple con el filtro y valor proporcionados.
        """
        modelo_reclamo = self.__session.query(ModeloReclamo).filter_by(**{filtro: valor}).first()
        return self._map_modelo_a_entidad(modelo_reclamo) if modelo_reclamo else None

    
    def adherir_usuario_a_reclamo(self, reclamo_id, usuario_id):
        """
        Añade el usuario a la lista de usuarios adheridos de un reclamo.
        """
        reclamo = self.repositorio.obtener_reclamo_por_id(reclamo_id)
        if usuario_id not in reclamo.usuarios_adheridos:
            reclamo.usuarios_adheridos.append(usuario_id)
            self.repositorio.actualizar_reclamo(reclamo)
        return reclamo

    def guardar_reclamo(self, data):
        nuevo_reclamo = ModeloReclamo(*data)
        db.session.add(nuevo_reclamo)
        db.session.commit()


    def derivar_reclamo(self, id_reclamo, nuevo_departamento):
        reclamo = self.repositorio.obtener_registro_por_filtro("id_reclamo", id_reclamo)
        if reclamo:
            reclamo.clasificacion = nuevo_departamento
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
    
    def reclamos_similares(self, posibles_data, texto_reclamo):
        similares = []
        for descripcion, id_reclamo in posibles_data:
            if self.es_similar(descripcion, texto_reclamo):  # Implementa tu lógica de similitud aquí
                similares.append(id_reclamo)
        return similares

    def buscar_reclamos_por_departamento(self, clasificacion, session):
        return session.query(ModeloReclamo).filter_by(clasificacion=clasificacion).all()
    
    def buscar_reclamo_por_id(self, id_reclamo, session):
        return session.query(ModeloReclamo).filter_by(id=id_reclamo).first()


    def buscar_reclamos_similares(self, contenido, clasificacion, session) -> list:
        """
        Busca reclamos similares basados en el contenido y departamento.
        La sesión se pasa como argumento para evitar depender de un atributo interno.
        """
        modelo_reclamos = session.query(ModeloReclamo).filter(
            (ModeloReclamo.contenido.ilike(f"%{contenido}%")) | 
            (ModeloReclamo.clasificacion == clasificacion)
        ).all()
        return [self._map_modelo_a_entidad(reclamo) for reclamo in modelo_reclamos]

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