from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

db = SQLAlchemy()

# Tabla de asociación para la relación many-to-many entre usuarios y reclamos
asociacion_usuarios_reclamos = db.Table(
    'usuarios_reclamos',
    db.Column('user_id', db.Integer, db.ForeignKey('usuarios.id')),
    db.Column('reclamo_id', db.Integer, db.ForeignKey('reclamos.id'))
)

class ModeloUsuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer(), primary_key=True)
    _nombre = db.Column(db.String(1000), nullable=False)
    _apellido = db.Column(db.String(1000), nullable=False)
    _nombre_usuario = db.Column(db.String(1000), nullable=False, unique=True)
    _email = db.Column(db.String(1000), nullable=False, unique=True)
    _contraseña = db.Column(db.String(1000), nullable=False)
    _claustro = db.Column(db.String(1000), nullable=False)

    # Relación many-to-many
    reclamos_seguidos = db.relationship('ModeloReclamo', secondary=asociacion_usuarios_reclamos, backref='usuarios_adheridos')

    # Propiedades para acceder a los datos encapsulados
    @property
    def nombre(self):
        return self._nombre

    # Define las demás propiedades de forma similar...

class ModeloReclamo(db.Model):
    __tablename__ = 'reclamos'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    _id_reclamo = db.Column(db.String(36), unique=True, default=str(uuid.uuid4()))
    _usuario = db.Column(db.String(1000), nullable=False)
    _contenido = db.Column(db.String(2000), nullable=False)
    _departamento = db.Column(db.String(1000), nullable=False)
    _fecha_hora = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    _estado = db.Column(db.String(1000), nullable=False, default="pendiente")

    # Define las propiedades como en el código anterior...

