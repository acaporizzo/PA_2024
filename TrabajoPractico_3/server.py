from flask import render_template, request, redirect, url_for, flash, session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from modules.modelos import ModeloReclamo, ModeloUsuario
from modules.gestores import GestorReclamo, GestorBaseDeDatos, GestorUsuario
from modules.factoria import crear_repositorio
from modules.gestor_login import GestorDeLogin
from modules.config import app, login_manager, db
from modules.classifier import ClaimsClassifier
import nltk, os

nltk_data_path = os.path.join(os.path.dirname(__file__), 'nltk_data')
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)
if not os.path.exists(os.path.join(nltk_data_path, 'tokenizers/punkt')):
    try:
        nltk.download('punkt', download_dir=nltk_data_path)
    except Exception as e:
        print("Error al descargar nltk data:", e)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

admin_list = [1]
repo_reclamo , repo_usuario = crear_repositorio()

gestor_reclamo = GestorReclamo(repo_reclamo)
gestor_usuario = GestorUsuario(repo_usuario)
gestor_login = GestorDeLogin(gestor_usuario, login_manager, admin_list)

try:
    with app.app_context():
        db.create_all()
        print("Conexión a la base de datos exitosa y tablas creadas.")
except Exception as e:
    print("Error al conectar con la base de datos:", e)


@app.route('/')
def home():
    if gestor_login.usuario_autenticado:
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
        departamento = request.form.get('departamento', 'general')
        
        if contraseña != confirmacion:
            flash("Las contraseñas no coinciden", "error")
            return redirect(url_for('registrar'))
        
        rol = None
        if claustro == "PAyS":
            rol = request.form.get('rol')
            if rol not in ["Jefe de Departamento", "Secretario Técnico"]:
                flash("Debe seleccionar un rol válido para el claustro PAyS", "error")
                return redirect(url_for('registrar'))

        try:
            gestor_usuario.registrar_usuario(
                nombre=nombre,
                apellido=apellido,
                nombre_usuario=nombre_usuario,
                email=email,
                contraseña=generate_password_hash(contraseña),
                claustro=claustro,
                rol=rol,
                departamento=departamento
            )
            flash("Usuario registrado con éxito. Inicia sesión.", "success")
            return redirect(url_for('iniciar_sesion'))
        
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for('registrar'))

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
            imagen = request.files.get('image')
            imagen_data = imagen.read() if imagen else None

            clasificacion = classifier.clasificar([contenido])[0]

            reclamos_similares = ModeloReclamo.query.filter_by(clasificacion=clasificacion).all()

            if reclamos_similares:
                return render_template("seleccionar_reclamo.html", reclamos=reclamos_similares, contenido=contenido, departamento=departamento)

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

    return render_template("crear_reclamo.html")


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
