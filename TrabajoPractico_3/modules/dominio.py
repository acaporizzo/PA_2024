from datetime import datetime

class Usuario:
    def __init__(self, id, nombre, apellido, nombre_usuario, email, contraseña, claustro, rol=None, departamento=None):
        self.__id = id
        self.__nombre = nombre
        self.__apellido = apellido
        self.__nombre_usuario = nombre_usuario
        self.__email = email
        self.__contraseña = contraseña
        self.__claustro = claustro
        self.__rol = rol
        self.__departamento = departamento
        self.__reclamos_adheridos = []  # Lista para almacenar los reclamos adheridos (opcional)

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @property
    def apellido(self):
        return self.__apellido

    @property
    def nombre_usuario(self):
        return self.__nombre_usuario

    @property
    def email(self):
        return self.__email

    @property
    def contraseña(self):
        return self.__contraseña

    @property
    def claustro(self):
        return self.__claustro

    @property
    def rol(self):
        return self.__rol

    @property
    def departamento(self):
        return self.__departamento

    @property
    def reclamos_adheridos(self):
        return self.__reclamos_adheridos  # Retorna los reclamos adheridos al usuario

    def agregar_reclamo_adherido(self, reclamo_id):
        if reclamo_id not in self.__reclamos_adheridos:
            self.__reclamos_adheridos.append(reclamo_id)
            self.actualizar_reclamo_adherido(reclamo_id)

class Reclamo:
    def __init__(self, id_reclamo, usuario, contenido, clasificacion, estado="pendiente", fecha_hora=None, imagen=None, usuarios_adheridos=None):
        self.__id_reclamo = id_reclamo
        self.__id_usuario = usuario
        self.__contenido = contenido
        self.__clasificacion = clasificacion
        self.__estado = estado
        self.__fecha_hora = fecha_hora or datetime.now()  # Usa la fecha actual si no se pasa una
        self.__imagen = imagen  # Nuevo atributo para la imagen
        self.__usuarios_adheridos = usuarios_adheridos or []  # Lista de usuarios adheridos (inicialmente vacía)

    @property
    def id_reclamo(self):
        return self.__id_reclamo

    @property
    def id_usuario(self):
        return self.__id_usuario

    @property
    def contenido(self):
        return self.__contenido

    @property
    def clasificacion(self):
        return self.__clasificacion

    @property
    def estado(self):
        return self.__estado

    @property
    def fecha_hora(self):
        return self.__fecha_hora

    @property
    def imagen(self):
        return self.__imagen

    @property
    def usuarios_adheridos(self):
        return self.__usuarios_adheridos

    def agregar_usuario_adherido(self, usuario_id):
        if usuario_id not in self.__usuarios_adheridos:
            self.__usuarios_adheridos.append(usuario_id)
            self.actualizar_usuarios_adheridos(usuario_id)

    def cargar_imagen(self, imagen):
        self.__imagen = imagen
