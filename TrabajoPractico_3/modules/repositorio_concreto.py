from modules.dominio import Reclamo, Usuario
from modules.repositorio_abstracto import RepositorioAbstracto
from modules.modelos import ModeloReclamo, ModeloUsuario
from modules.config import db

class RepositorioReclamosSQLAlchemy(RepositorioAbstracto):
    def __init__(self, session):
        self.__session = session

    def guardar_registro(self, reclamo):
        if not isinstance(reclamo, Reclamo):
            raise ValueError("El parámetro no es una instancia de la clase Reclamo")
        modelo_reclamo = self._map_entidad_a_modelo(reclamo)
        self.__session.add(modelo_reclamo)
        self.__session.commit()

    def obtener_todos_los_registros(self) -> list:
        modelo_reclamos = self.__session.query(ModeloReclamo).all()
        return [self._map_modelo_a_entidad(reclamo) for reclamo in modelo_reclamos]
    
    def obtener_reclamos_de_usuario(self, usuario) -> list:
        modelo_reclamos = self.__session.query(ModeloReclamo).filter(ModeloReclamo.usuarios_adheridos.contains(usuario)).all()
        return [self._map_modelo_a_entidad(reclamo) for reclamo in modelo_reclamos]

    def _map_entidad_a_modelo(self, entidad: Reclamo):
        return ModeloReclamo(
            id=entidad.id,
            id_usuario=entidad.id_usuario,
            contenido=entidad.contenido,
            clasificacion=entidad.clasificacion,
            estado=entidad.estado,
            imagen=entidad.imagen,
            fecha=entidad.fecha_hora 
        )

    def _map_modelo_a_entidad(self, modelo: ModeloReclamo):
        return Reclamo(
            id_reclamo=modelo.id,
            usuario=modelo.id_usuario,
            contenido=modelo.contenido,
            clasificacion=modelo.clasificacion,
            fecha_hora=modelo.fecha,
            estado=modelo.estado,
            usuarios_adheridos=None
        )

class RepositorioUsuariosSQLAlchemy(RepositorioAbstracto):
    def __init__(self, session=None):
        self.__session = session or db.session

    def guardar_registro(self, usuario):
        if not isinstance(usuario, Usuario):
            raise ValueError("El parámetro no es una instancia de la clase Usuario")
        modelo_usuario = self.__map_entidad_a_modelo(usuario)
        self.__session.add(modelo_usuario)
        self.__session.commit()
    def obtener_todos_los_registros(self):
        print(self.__session)  # Para depuración
        modelo_usuarios = self.__session.query(ModeloUsuario).all()
        print(modelo_usuarios)  # Para depuración
        return modelo_usuarios if modelo_usuarios else []  # Garantiza que siempre devuelva una lista

    def obtener_usuario_por_nombre(self, nombre_usuario):
        """Obtiene un usuario de la base de datos por nombre de usuario."""
        modelo_usuario = self.__session.query(ModeloUsuario).filter_by(nombre_usuario=nombre_usuario).first()
        return self.__map_modelo_a_entidad(modelo_usuario) if modelo_usuario else None
    
    def obtener_usuario_por_id(self, id_usuario):
            """Obtiene un usuario de la base de datos por ID."""
            modelo_usuario = self.__session.query(ModeloUsuario).filter_by(id=id_usuario).first()
            return self.__map_modelo_a_entidad(modelo_usuario) if modelo_usuario else None

    def __map_entidad_a_modelo(self, entidad: Usuario):

        modelo_usuario = ModeloUsuario(
            id=entidad.id,
            nombre=entidad.nombre,
            apellido=entidad.apellido,
            email=entidad.email,
            nombre_usuario=entidad.nombre_usuario,
            contraseña=entidad.contraseña,
            claustro=entidad.claustro
        )
        
        if entidad.claustro == "PAyS":
            modelo_usuario.rol = entidad.rol
            if entidad.rol == "Jefe de Departamento":
                modelo_usuario.departamento = entidad.departamento
        
        return modelo_usuario

    def __map_modelo_a_entidad(self, modelo: ModeloUsuario):
        return Usuario(
        id=modelo.id,
        nombre=modelo.nombre,
        apellido=modelo.apellido,
        nombre_usuario=modelo.nombre_usuario,
        email=modelo.email,
        contraseña=modelo.contraseña,
        claustro=modelo.claustro,
        rol=modelo.rol if modelo.claustro == "PAyS" else None,
        departamento=modelo.departamento if modelo.rol == "Jefe de Departamento" else None
    )