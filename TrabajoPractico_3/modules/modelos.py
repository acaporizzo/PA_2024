from sqlalchemy import Table, Column
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import Column, String, LargeBinary, DateTime
from modules.base_datos import db

# Tabla intermedia para la relación muchos a muchos entre reclamos y usuarios
reclamos_usuarios = Table('reclamos_usuarios', db.Model.metadata,
    Column('usuario_id', db.String(36), db.ForeignKey('usuarios.id'), primary_key=True),
    Column('reclamo_id', db.String(36), db.ForeignKey('reclamos.id'), primary_key=True)
)

class ModeloUsuario(db.Model):
    __tablename__ = 'usuarios'

    id = Column(String(36), primary_key=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    nombre_usuario = Column(String, nullable=False, unique=True)
    contraseña = Column(String, nullable=False)
    claustro = Column(String, nullable=False)
    rol = Column(String, nullable=True)
    departamento = Column(String, nullable=True)

    # Relación muchos a muchos con reclamos a través de la tabla intermedia
    reclamos_adheridos = relationship('ModeloReclamo', secondary=reclamos_usuarios, backref='usuarios_adheridos')

    def obtener_id(self):
        return str(self.id)

class ModeloReclamo(db.Model):
    __tablename__ = 'reclamos'
    
    id = db.Column(db.String(36), primary_key=True)  # UUID como cadena
    id_usuario = db.Column(db.String(36), db.ForeignKey('usuarios.id'), nullable=False)  # UUID como cadena
    contenido = db.Column(db.Text, nullable=False)
    clasificacion = db.Column(db.String(50), nullable=True)
    estado = db.Column(db.String(20), default="pendiente")
    imagen = db.Column(db.LargeBinary, nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación muchos a muchos con usuarios a través de la tabla intermedia
    usuarios_adheridos = relationship('ModeloUsuario', secondary=reclamos_usuarios, backref='reclamos_adheridos')

    def __init__(self, id_reclamo, id_usuario, contenido, clasificacion, estado="pendiente", fecha_hora=None, imagen=None):
        self.id = id_reclamo
        self.id_usuario = id_usuario
        self.contenido = contenido
        self.clasificacion = clasificacion
        self.estado = estado
        self.fecha = fecha_hora or datetime.now()  # Usa la fecha actual si no se pasa una
        self.imagen = imagen
