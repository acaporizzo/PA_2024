from modules.dominio import Reclamo, Usuario
from modules.repositorio_abstracto import RepositorioAbstracto
from modules.modelos import ModeloReclamo, ModeloUsuario

class RepositorioReclamosSQLAlchemy(RepositorioAbstracto):
    def __init__(self, session):
        self.__session = session
        tabla_reclamo = ModeloReclamo()
        tabla_reclamo.metadata.create_all(self.__session.bind)

    def guardar_registro(self, reclamo):
        if not isinstance(reclamo, Reclamo):
            raise ValueError("El parámetro no es una instancia de la clase Reclamo")
        modelo_reclamo = self._map_entidad_a_modelo(reclamo)
        self.__session.add(modelo_reclamo)
        self.__session.commit()

    def obtener_todos_los_registros(self) -> list:
        modelo_reclamos = self.__session.query(ModeloReclamo).all()
        return [self._map_modelo_a_entidad(reclamo) for reclamo in modelo_reclamos]

    def modificar_registro(self, reclamo_modificado):
        if not isinstance(reclamo_modificado, Reclamo):
            raise ValueError("El parámetro no es una instancia de la clase Reclamo")
        registro = self.__session.query(ModeloReclamo).filter_by(id_reclamo=reclamo_modificado.id_reclamo).first()
        if registro:
            registro.contenido = reclamo_modificado.contenido
            registro.departamento = reclamo_modificado.departamento
            registro.fecha_hora = reclamo_modificado.fecha_hora
            registro.estado = reclamo_modificado.estado
            registro.usuarios_adheridos = reclamo_modificado.usuarios_adheridos
            self.__session.commit()

    def obtener_registro_por_filtro(self, filtro, valor):
        modelo_reclamo = self.__session.query(ModeloReclamo).filter_by(**{filtro: valor}).first()
        return self._map_modelo_a_entidad(modelo_reclamo) if modelo_reclamo else None

    def obtener_registros_segun_filtro(self, filtro, valor) -> list:
        modelo_reclamos = self.__session.query(ModeloReclamo).filter_by(**{filtro: valor}).all()
        return [self._map_modelo_a_entidad(reclamo) for reclamo in modelo_reclamos]

    def eliminar_registro(self, id_reclamo):
        registro = self.__session.query(ModeloReclamo).filter_by(id_reclamo=id_reclamo).first()
        if registro:
            self.__session.delete(registro)
            self.__session.commit()

    def obtener_registros_seguidas_por_usuario(self, usuario) -> list:
        modelo_reclamos = self.__session.query(ModeloReclamo).filter(ModeloReclamo.usuarios_adheridos.contains(usuario)).all()
        return [self._map_modelo_a_entidad(reclamo) for reclamo in modelo_reclamos]

    def _map_entidad_a_modelo(self, entidad: Reclamo):
        return ModeloReclamo(
            id_reclamo=entidad.id_reclamo,
            usuario=entidad.usuario,
            contenido=entidad.contenido,
            departamento=entidad.departamento,
            fecha_hora=entidad.fecha_hora,
            estado=entidad.estado,
            usuarios_adheridos=entidad.usuarios_adheridos
        )

    def _map_modelo_a_entidad(self, modelo: ModeloReclamo):
        return Reclamo(
            id_reclamo=modelo.id_reclamo,
            usuario=modelo.usuario,
            contenido=modelo.contenido,
            departamento=modelo.departamento,
            fecha_hora=modelo.fecha_hora,
            estado=modelo.estado,
            usuarios_adheridos=modelo.usuarios_adheridos
        )

class RepositorioUsuariosSQLAlchemy(RepositorioAbstracto):
    def __init__(self, session):
        self.__session = session
        tabla_usuario = ModeloUsuario()
        tabla_usuario.metadata.create_all(self.__session.bind)

    def guardar_registro(self, usuario):
        if not isinstance(usuario, Usuario):
            raise ValueError("El parámetro no es una instancia de la clase Usuario")
        modelo_usuario = self.__map_entidad_a_modelo(usuario)
        self.__session.add(modelo_usuario)
        self.__session.commit()

    def obtener_todos_los_registros(self):
        modelo_usuarios = self.__session.query(ModeloUsuario).all()
        return [self.__map_modelo_a_entidad(usuario) for usuario in modelo_usuarios]

    def modificar_registro(self, usuario_modificado):
        if not isinstance(usuario_modificado, Usuario):
            raise ValueError("El parámetro no es una instancia de la clase Usuario")
        register = self.__session.query(ModeloUsuario).filter_by(id=usuario_modificado.id).first()
        if register:
            register.nombre = usuario_modificado.nombre
            register.apellido = usuario_modificado.apellido
            register.email = usuario_modificado.email
            register.password = usuario_modificado.password
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

    def _map_entidad_a_modelo(self, entidad: Usuario):
        return ModeloUsuario(
            id=entidad.id,
            nombre=entidad.nombre,
            apellido=entidad.apellido,
            email=entidad.email,
            password=entidad.password,
            claustro=entidad.claustro,
            rol=entidad.rol,
            departamento=entidad.departamento
        )

    def _map_modelo_a_entidad(self, modelo: ModeloUsuario):
        return Usuario(
            id=modelo.id,
            nombre=modelo.nombre,
            apellido=modelo.apellido,
            email=modelo.email,
            password=modelo.password,
            claustro=modelo.claustro,
            rol=modelo.rol,
            departamento=modelo.departamento
        )
