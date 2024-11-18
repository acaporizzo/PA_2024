from sqlalchemy import Table, Column
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import Column, String
from modules.config import db

# Tabla intermedia para la relación muchos a muchos entre reclamos y usuarios
reclamos_usuarios = Table('reclamos_usuarios', db.Model.metadata,
    Column('usuario_id', db.String(36), db.ForeignKey('usuarios.id'), primary_key=True),
    Column('reclamo_id', db.String(36), db.ForeignKey('reclamos.id'), primary_key=True)
)

class ModeloUsuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.String(36), primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    apellido = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    nombre_usuario = db.Column(db.String, nullable=False, unique=True)
    contraseña = db.Column(db.String, nullable=False)
    claustro = db.Column(db.String, nullable=False)
    rol = db.Column(db.String, nullable=True)
    departamento = db.Column(db.String, nullable=True)

    # Relación muchos a muchos con reclamos a través de la tabla intermedia
    reclamos_creados = relationship('ModeloReclamo', backref='usuario_creador')  # Relación con reclamos creados
    reclamos_adheridos = relationship('ModeloReclamo', secondary=reclamos_usuarios, back_populates='usuarios_adheridos')

    def obtener_id(self):
        return str(self.id)

class ModeloReclamo(db.Model):
    __tablename__ = 'reclamos'
    
    id = db.Column(db.String(36), primary_key=True)  
    id_usuario = db.Column(db.String(36), db.ForeignKey('usuarios.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    clasificacion = db.Column(db.String(50), nullable=True)
    estado = db.Column(db.String(20), default="pendiente")
    imagen = db.Column(db.LargeBinary)
    fecha = db.Column(db.String, nullable=True)

    # Relación muchos a muchos con usuarios
    usuarios_adheridos = relationship('ModeloUsuario', secondary=reclamos_usuarios, back_populates='reclamos_adheridos')

    def __init__(self, id, id_usuario, contenido, clasificacion, estado, fecha): #cuando instancio utilizo estos nombres
        self.id = id
        self.id_usuario = id_usuario
        self.contenido = contenido
        self.clasificacion = clasificacion
        self.estado = estado
        self.imagen = None
        self.fecha = fecha

    def añadir_imagen (self, imagen):
        self.imagen = imagen
