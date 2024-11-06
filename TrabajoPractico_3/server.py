# server.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_para_formularios'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm_reclamos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Instancia de la base de datos
db = SQLAlchemy(app)

# Definición del modelo Usuario (Tabla usuarios)
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)
    claustro = db.Column(db.String(20), nullable=False)

# Definición del modelo Reclamo (Tabla reclamos)
class Reclamo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    departamento = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(20), default="pendiente")
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    adherentes = db.Column(db.Integer, default=0)

    usuario = db.relationship('Usuario', backref=db.backref('reclamos', lazy=True))

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        nombre_usuario = request.form['nombre_usuario']
        contraseña = request.form['contraseña']
        confirmacion = request.form['confirmacion']
        claustro = request.form['claustro']

        # Validación de contraseñas
        if contraseña != confirmacion:
            flash("Las contraseñas no coinciden", "error")
            return redirect(url_for('registrar'))

        # Validación de email y nombre de usuario únicos
        if Usuario.query.filter_by(email=email).first() or Usuario.query.filter_by(nombre_usuario=nombre_usuario).first():
            flash("El email o nombre de usuario ya están registrados", "error")
            return redirect(url_for('registrar'))

        # Crear el nuevo usuario en la base de datos
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            nombre_usuario=nombre_usuario,
            contraseña=generate_password_hash(contraseña),
            claustro=claustro
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        # Redireccionar a la página de inicio de sesión
        flash("Usuario registrado con éxito. Inicia sesión.", "success")
        return redirect(url_for('iniciar_sesion'))
    return render_template('registro.html')
# Ruta para iniciar sesión
@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        contraseña = request.form['contraseña']

        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        if usuario and check_password_hash(usuario.contraseña, contraseña):
            session['usuario'] = usuario.nombre_usuario
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('panel_usuario'))
        flash("Credenciales incorrectas", "error")
    return render_template('iniciar_sesion.html')

# Ruta para cerrar sesión
@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.pop('usuario', None)
    flash("Sesión cerrada", "success")
    return redirect(url_for('home'))

# Ruta para el panel de usuario después de iniciar sesión
@app.route('/panel_usuario')
def panel_usuario():
    if 'usuario' not in session:
        flash("Inicia sesión para acceder a esta página", "error")
        return redirect(url_for('iniciar_sesion'))
    return render_template('panel_usuario.html')

if __name__ == '__main__':
    app.run(debug=True)
