from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_required
from flask_login import logout_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from modules.modelos import ModeloReclamo, ModeloUsuario
from modules.gestores import GestorReclamo, GestorBaseDeDatos, GestorUsuario
from modules.factoria import crear_repositorio
from modules.gestor_login import GestorDeLogin
from modules.config import app, login_manager, db
from modules.classifier import ClaimsClassifier
from modules.create_csv import crear_csv
import os, uuid, pickle

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

try:
    with open('./data/claims_clf.pkl', 'rb') as archivo:
        clasificador = pickle.load(archivo)
        print("Modelo cargado exitosamente.")
except Exception as e:
    print(f"Error al cargar el modelo: {str(e)}")
    
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
        rol = None 
        departamento = None

        if claustro == "PAyS":
            rol = request.form.get('rol')
            if rol not in ["Jefe de Departamento", "Secretario Técnico"]:
                flash("Debe seleccionar un rol válido para el claustro PAyS", "error")
                return redirect(url_for('registrar'))

            if rol == "Jefe de Departamento":
                departamento = request.form.get('departamento')
                if departamento not in ["maestranza", "soporte informático", "secretaría técnica"]:
                    flash("Debe seleccionar un departamento válido para el rol de Jefe de Departamento", "error")
                    return redirect(url_for('registrar'))

        if contraseña != confirmacion:
            flash("Las contraseñas no coinciden", "error")
            return redirect(url_for('registrar'))
        
        id = str(uuid.uuid4())
        try:
            gestor_usuario.registrar_usuario(
                id=id,
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
        nombre_usuario = request.form["nombre_usuario"]
        contraseña = request.form["contraseña"]
        
        if not nombre_usuario or not contraseña:
            flash("Complete ambos campos", "error")
        else:
            # Verificar credenciales usando GestorDeLogin
            usuario_valido = gestor_login.verificar_credenciales(nombre_usuario, contraseña)
            if usuario_valido:
                gestor_login.login_usuario(usuario_valido)
                tipo_usuario = usuario_valido.departamento

                if tipo_usuario == "jefe":
                    return redirect(url_for('panel_jefe'))
                elif tipo_usuario == "secretario_tecnico":
                    return redirect(url_for('panel_secretario_tecnico'))
                else:
                    return redirect(url_for('panel_usuario'))
            else:
                flash("Usuario o contraseña incorrectos", "error")

    return render_template("iniciar_sesion.html")

@app.route('/panel_usuario')
@login_required
def panel_usuario():
    return render_template('panel_usuario.html')

@app.route('/crear_reclamo', methods=['GET', 'POST'])
@login_required
def crear_reclamo():
    usuario_actual = gestor_login.id_usuario_actual  # ID del usuario autenticado
    datos_usuario = gestor_usuario.cargar_usuario(usuario_actual)  # Datos del usuario actual

    if request.method == "POST":
        # Obtener los datos del formulario
        texto_reclamo = request.form.get("description")  # Descripción del reclamo
        imagen = request.files.get("image")  # Imagen opcional del reclamo

        # Verificar si se proporcionó texto para el reclamo
        if not texto_reclamo:
            flash("La descripción del reclamo es obligatoria.", "error")
            return render_template("crear_reclamo.html")

        # Clasificar el reclamo usando el modelo
        try:
            departamento = clasificador.clasificar([texto_reclamo])[0]  # Clasificar el texto del reclamo
        except Exception as e:
            flash(f"Error al clasificar el reclamo: {str(e)}", "error")
            return render_template("crear_reclamo.html")

        # Crear el formulario de datos para el reclamo
        formulario = [
            texto_reclamo,        # Descripción
            "pendiente",          # Estado inicial
            departamento,         # Departamento clasificado
            str(datetime.now()),  # Fecha y hora actuales
            usuario_actual        # ID del usuario creador
        ]

        # Agregar la imagen si fue proporcionada
        if imagen:
            formulario.append(imagen.read())
        else:
            formulario.append(None)

        # Crear y guardar el reclamo
        nuevo_reclamo = gestor_reclamo.crear_reclamo(formulario)
        gestor_reclamo.guardar_reclamo(nuevo_reclamo)

        # Confirmar éxito al usuario
        flash("Reclamo creado y clasificado exitosamente.", "success")
        return redirect(url_for('panel_usuario'))

    # Renderizar la plantilla de creación de reclamo si no es POST
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
    logout_user()
    flash("Sesión cerrada", "success")
    
    return redirect(url_for('iniciar_sesion'))

@app.route('/listar_reclamos')
def listar_reclamos():
    return render_template('listar_reclamos.html')

@app.route('/mis_reclamos')
def mis_reclamos():
    return render_template('mis_reclamos.html')


if __name__ == '__main__':
    app.run(debug=True)
