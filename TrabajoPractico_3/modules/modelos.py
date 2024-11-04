from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()

asociacion_usuarios_reclamos = Table(
    'usuarios_reclamos', Base.metadata,
    Column('user_id', Integer, ForeignKey('usuarios.id')),
    Column('reclamo_id', Integer, ForeignKey('reclamos.id'))
)

class ModeloUsuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer(), primary_key=True)
    _nombre = Column('nombre', String(1000), nullable=False)
    _apellido = Column('apellido', String(1000), nullable=False)
    _nombre_usuario = Column('nombre_usuario', String(1000), nullable=False, unique=True)
    _email = Column('email', String(1000), nullable=False, unique=True)
    _contraseña = Column('contraseña', String(1000), nullable=False)
    _claustro = Column('claustro', String(1000), nullable=False)

    reclamos_seguidos = relationship('ModeloReclamo', secondary=asociacion_usuarios_reclamos, backref='usuarios_adheridos')

    @property
    def nombre(self):
        return self._nombre

    @property
    def apellido(self):
        return self._apellido

    @property
    def nombre_usuario(self):
        return self._nombre_usuario

    @property
    def email(self):
        return self._email

    @property
    def contraseña(self):
        return self._contraseña

    @property
    def claustro(self):
        return self._claustro


class ModeloReclamo(Base):
    __tablename__ = 'reclamos'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    _id_reclamo = Column('id_reclamo', String(36), unique=True, default=str(uuid.uuid4()))
    _usuario = Column('usuario', String(1000), nullable=False)
    _contenido = Column('contenido', String(2000), nullable=False)
    _departamento = Column('departamento', String(1000), nullable=False)
    _fecha_hora = Column('fecha_hora', DateTime(), nullable=False)
    _estado = Column('estado', String(1000), nullable=False, default="pendiente")

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, nuevo_estado):
        self._estado = nuevo_estado

    @property
    def id_reclamo(self):
        return self._id_reclamo

    @property
    def usuario(self):
        return self._usuario

    @property
    def contenido(self):
        return self._contenido

    @property
    def departamento(self):
        return self._departamento

    @property
    def fecha_hora(self):
        return self._fecha_hora

    @property
    def usuarios_adheridos(self):
        return self._usuarios_adheridos
