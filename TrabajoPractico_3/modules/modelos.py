from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from modules.config import db
from flask_login import UserMixin

class ModeloUsuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)
    contraseña = db.Column(db.String(120), nullable=False)
    claustro = db.Column(db.String(20))
    reclamos_seguidos = db.relationship('ModeloReclamo', backref='usuarios_adheridos')

    def obtener_id(self):
        return str(self.id)

class ModeloReclamo(db.Model):
    __tablename__ = 'reclamos'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    departamento = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(20), default="pendiente")
    clasificacion = db.Column(db.String(100), nullable=True)  # Agregar columna clasificacion
    imagen = db.Column(db.LargeBinary, nullable=True)  # Para almacenar imagen, si es necesario
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

