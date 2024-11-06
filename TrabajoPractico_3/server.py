from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from modules.modelos import db, ModeloReclamo, ModeloUsuario
import pickle

app = Flask("server")
app.config['SECRET_KEY'] = 'clave_secreta_para_formularios'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm_reclamos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

with open('./data/claims_clf.pkl', 'rb') as f:
    classifier = pickle.load(f)

@app.route('/')
def home():
    if 'usuario' in session: #si el usuario ya inició sesión lo lleva directamente al panel
        return redirect(url_for('panel_usuario'))
    return render_template('home.html')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        nombre_usuario = request.form.get('nombre_usuario')
        contraseña = request.form.get('contraseña')
        confirmacion = request.form.get('confirmacion')
        claustro = request.form.get('claustro')

        if contraseña != confirmacion:
            flash("Las contraseñas no coinciden", "error")
            return redirect(url_for('registrar'))

        if ModeloUsuario.query.filter_by(email=email).first() or ModeloUsuario.query.filter_by(nombre_usuario=nombre_usuario).first():
            flash("El email o nombre de usuario ya están registrados", "error")
            return redirect(url_for('registrar'))

        nuevo_usuario = ModeloUsuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            nombre_usuario=nombre_usuario,
            contraseña=generate_password_hash(contraseña),
            claustro=claustro
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Usuario registrado con éxito. Inicia sesión.", "success")
        return redirect(url_for('iniciar_sesion'))

    return render_template('registro.html')

@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        contraseña = request.form['contraseña']

        usuario = ModeloUsuario.query.filter_by(nombre_usuario=nombre_usuario).first()

        if usuario and check_password_hash(usuario.contraseña, contraseña):
            session['usuario'] = usuario.nombre_usuario
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('panel_usuario'))
        
        flash("Credenciales incorrectas. Inténtalo de nuevo.", "error")
        return redirect(url_for('iniciar_sesion'))

    rendered_template = render_template('iniciar_sesion.html')
    session.pop('_flashes', None)  #borra los mensajes flash historicos
    return rendered_template

@app.route('/crear_reclamo', methods=['GET', 'POST'])
def crear_reclamo():
    user = session.get('usuario')
    if not user:
        flash("Inicia sesión para crear un reclamo", "error")
        return redirect(url_for('iniciar_sesion'))
    
    usuario = ModeloUsuario.query.filter_by(nombre_usuario=user).first()
    if not usuario:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('panel_usuario'))

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'volver_a_usuario':
            return redirect(url_for('panel_usuario'))

        elif action == 'crear':
            contenido = request.form.get('description')
            departamento = request.form.get('department')
            imagen = request.files.get('image')
            imagen_data = imagen.read() if imagen else None

            # 1. Clasificar el reclamo
            clasificacion = classifier.clasificar([contenido])[0]

            # 2. Buscar reclamos similares
            reclamos_similares = ModeloReclamo.query.filter_by(clasificacion=clasificacion).all()

            # Si existen reclamos similares, mostrar opción para adherirse
            if reclamos_similares:
                return render_template("seleccionar_reclamo.html", reclamos=reclamos_similares, contenido=contenido, departamento=departamento)

            # 3. Si no existen reclamos similares, crear un reclamo nuevo
            nuevo_reclamo = ModeloReclamo(
                id_usuario=usuario.id,
                contenido=contenido,
                departamento=departamento,
                fecha=datetime.utcnow(),
                estado="pendiente",
                clasificacion=clasificacion,
                imagen=imagen_data
            )

            db.session.add(nuevo_reclamo)
            db.session.commit()
            flash("Reclamo creado exitosamente", "success")
            return redirect(url_for('panel_usuario'))

    return render_template("reclamo.html")


@app.route('/adherir_a_reclamo/<int:reclamo_id>', methods=['POST'])
def adherir_a_reclamo(reclamo_id):
    user = session.get('usuario')
    if not user:
        flash("Inicia sesión para adherirse a un reclamo", "error")
        return redirect(url_for('iniciar_sesion'))
    
    reclamo = ModeloReclamo.query.get(reclamo_id)
    if reclamo:
        flash("Adherido a reclamo", "success")
    else:
        flash("Reclamo no encontrado", "error")
    
    return redirect(url_for('panel_usuario'))

@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.pop('usuario', None)
    flash("Sesión cerrada", "success")
    rendered_template = redirect(url_for('home'))
    session.pop('_flashes', None) 
    return rendered_template

@app.route('/listar_reclamos')
def listar_reclamos():
    return render_template('listar_reclamos.html')

@app.route('/mis_reclamos')
def mis_reclamos():
    return render_template('mis_reclamos.html')

@app.route('/panel_usuario')
def panel_usuario():
    if 'usuario' not in session:
        flash("Inicia sesión para acceder a esta página", "error")
        return redirect(url_for('iniciar_sesion'))
    return render_template('panel_usuario.html')

if __name__ == '__main__':
    app.run(debug=True)
