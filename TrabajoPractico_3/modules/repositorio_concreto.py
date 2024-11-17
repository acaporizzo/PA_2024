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

    def insertar_reclamo(self, reclamo):
        if not isinstance(reclamo, Reclamo):
            raise ValueError("El parámetro debe ser una instancia de la clase Reclamo")
        
        modelo_reclamo = ModeloReclamo(
            id=reclamo.__id_reclamo,  # Cambiado a id_reclamo
            id_usuario=reclamo.__usuario,
            contenido=reclamo.__contenido,
            clasificacion=reclamo.__clasificacion,
            estado=reclamo.__estado,
            imagen=None,
            fecha=reclamo.__fecha_hora
        )
        self.__session.add(modelo_reclamo)
        self.__session.commit()

    def obtener_todos_los_registros(self) -> list:
        modelo_reclamos = self.__session.query(ModeloReclamo).all()
        return [self._map_modelo_a_entidad(reclamo) for reclamo in modelo_reclamos]

    def modificar_registro(self, reclamo_modificado):
        if not isinstance(reclamo_modificado, Reclamo):
            raise ValueError("El parámetro no es una instancia de la clase Reclamo")
        registro = self.__session.query(ModeloReclamo).filter_by(id=reclamo_modificado.__id_reclamo).first()
        if registro:
            registro.contenido = reclamo_modificado.__contenido
            registro.clasificacion = reclamo_modificado.__clasificacion
            registro.fecha_hora = reclamo_modificado.__fecha_hora
            registro.estado = reclamo_modificado.__estado
            registro.usuarios_adheridos = reclamo_modificado.usuarios_adheridos
            self.__session.commit()

    def obtener_registro_por_filtro(self, filtro, valor):
        modelo_reclamo = self.__session.query(ModeloReclamo).filter_by(**{filtro: valor}).first()
        return self._map_modelo_a_entidad(modelo_reclamo) if modelo_reclamo else None

    def obtener_registros_segun_filtro(self, filtro, valor) -> list:
        modelo_reclamos = self.__session.query(ModeloReclamo).filter_by(**{filtro: valor}).all()
        return [self._map_modelo_a_entidad(reclamo) for reclamo in modelo_reclamos]

    def eliminar_registro(self, id_reclamo):
        registro = self.__session.query(ModeloReclamo).filter_by(id=id_reclamo).first()
        if registro:
            self.__session.delete(registro)
            self.__session.commit()

    def obtener_registros_seguidas_por_usuario(self, usuario) -> list:
        modelo_reclamos = self.__session.query(ModeloReclamo).filter(ModeloReclamo.usuarios_adheridos.contains(usuario)).all()
        return [self._map_modelo_a_entidad(reclamo) for reclamo in modelo_reclamos]

    def buscar_reclamos_similares(self, contenido, clasificacion) -> list:
        modelo_reclamos = self.__session.query(ModeloReclamo).filter(
            (ModeloReclamo.contenido.ilike(f"%{contenido}%")) | 
            (ModeloReclamo.clasificacion == clasificacion)
        ).all()
        return [self._map_modelo_a_entidad(reclamo) for reclamo in modelo_reclamos]

    def _map_entidad_a_modelo(self, entidad: Reclamo):
        return ModeloReclamo(
            id=entidad.__id_reclamo,  # Cambiado de id a id_reclamo
            id_usuario=entidad.__usuario,
            contenido=entidad.__contenido,
            clasificacion=entidad.__clasificacion,
            estado=entidad.__estado,
            imagen=None,          # Ajusta si manejas imágenes
            fecha=entidad.__fecha_hora
        )

    def _map_modelo_a_entidad(self, modelo: ModeloReclamo):
        return Reclamo(
            id=modelo.id_reclamo,  # Cambiado de id a id_reclamo
            usuario=modelo.id_usuario,
            contenido=modelo.contenido,
            clasificacion=modelo.clasificacion,
            fecha_hora=modelo.fecha,
            estado=modelo.estado,
            usuarios_adheridos=None  # Ajusta si es necesario
        )

class RepositorioUsuariosSQLAlchemy(RepositorioAbstracto):
    def __init__(self, session=None):
        self.__session = session or db.session  # Usa la sesión de Flask-SQLAlchemy por defecto

    def guardar_registro(self, usuario):
        if not isinstance(usuario, Usuario):
            raise ValueError("El parámetro no es una instancia de la clase Usuario")
        modelo_usuario = self.__map_entidad_a_modelo(usuario)
        self.__session.add(modelo_usuario)
        self.__session.commit()

    def obtener_todos_los_registros(self):
        print(self.__session)
        modelo_usuarios = self.__session.query(ModeloUsuario).all()
        print(modelo_usuarios)

        return [self.__map_modelo_a_entidad(usuario) for usuario in modelo_usuarios]

    def modificar_registro(self, usuario_modificado):
        if not isinstance(usuario_modificado, Usuario):
            raise ValueError("El parámetro no es una instancia de la clase Usuario")
        register = self.__session.query(ModeloUsuario).filter_by(id=usuario_modificado.id).first()
        if register:
            register.nombre = usuario_modificado.nombre
            register.apellido = usuario_modificado.apellido
            register.email = usuario_modificado.email
            register.contraseña = usuario_modificado.contraseña
            register.claustro = usuario_modificado.claustro
            register.rol = usuario_modificado.rol
            register.departamento = usuario_modificado.departamento
            self.__session.commit()

    def asociar_registro(self, id_usuario, id_asociado):
        register = self.__session.query(ModeloUsuario).filter_by(id=id_usuario).first()
        modelo_asociado = self.__session.query(ModeloUsuario).filter_by(id=id_asociado).first()  # Ajusta esto si id_asociado es otro tipo de entidad
        if register and modelo_asociado:
            register.usuarios_asociados.append(modelo_asociado)
            self.__session.commit()

    def obtener_seguidores_de_registro_asociado(self, id_asociado):
        modelo_asociado = self.__session.query(ModeloUsuario).filter_by(id=id_asociado).first()
        return [self.__map_modelo_a_entidad(usuario) for usuario in modelo_asociado.usuarios_seguidores] if modelo_asociado else []

    def obtener_registro_por_filtro(self, filtro, valor):
        modelo_usuario = self.__session.query(ModeloUsuario).filter_by(**{filtro: valor}).first()
        return self.__map_modelo_a_entidad(modelo_usuario) if modelo_usuario else None

    def eliminar_registro(self, id_usuario):
        register = self.__session.query(ModeloUsuario).filter_by(id=id_usuario).first()
        if register:
            self.__session.delete(register)
            self.__session.commit()

    def obtener_usuario_por_id(self, id_usuario):
            """Obtiene un usuario de la base de datos por ID."""
            modelo_usuario = self.__session.query(ModeloUsuario).filter_by(id=id_usuario).first()
            return self.__map_modelo_a_entidad(modelo_usuario) if modelo_usuario else None

    def obtener_usuario_por_nombre(self, nombre_usuario):
        """Obtiene un usuario de la base de datos por nombre de usuario."""
        modelo_usuario = self.__session.query(ModeloUsuario).filter_by(nombre_usuario=nombre_usuario).first()
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

