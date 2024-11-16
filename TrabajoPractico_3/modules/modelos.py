from datetime import datetime
from sqlalchemy import Column, String
from modules.base_datos import db

class ModeloUsuario(db.Model):
    __tablename__ = 'usuarios'

    id = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    nombre_usuario = Column(String, nullable=False, unique=True)
    contraseña = Column(String, nullable=False)
    claustro = Column(String, nullable=False)
    rol = Column(String, nullable=True)         
    departamento = Column(String, nullable=True)

    def obtener_id(self):
        return str(self.id)

class ModeloReclamo(db.Model):
    __tablename__ = 'reclamos'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    clasificacion = db.Column(db.String(50), nullable=True)
    estado = db.Column(db.String(20), default="pendiente")
    #clasificacion = db.Column(db.String(100), nullable=True)
    imagen = db.Column(db.LargeBinary, nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
