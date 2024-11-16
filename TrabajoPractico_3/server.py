import nltk
import os

nltk_data_path = os.path.join(os.path.dirname(__file__), 'nltk_data')
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)
nltk.data.path.append(nltk_data_path)

try:
    nltk.download('punkt', download_dir=nltk_data_path)
    nltk.download('stopwords', download_dir=nltk_data_path)
    print("Recursos NLTK descargados exitosamente.")
except Exception as e:
    print(f"Error al descargar recursos NLTK: {str(e)}")


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
import uuid, pickle

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
    usuario_actual = gestor_login.id_usuario_actual

    if request.method == "POST":
        texto_reclamo = request.form.get("description")

        if not texto_reclamo:
            flash("La descripción del reclamo es obligatoria.", "error")
            return render_template("crear_reclamo.html")

        try:
            clasificacion = clasificador.clasificar([texto_reclamo])[0]
            reclamo = gestor_reclamo.crear_reclamo([str(uuid.uuid4()), usuario_actual, texto_reclamo, clasificacion, "pendiente"])
        except Exception as e:
            flash(f"Error al clasificar el reclamo: {str(e)}", "error")
            return render_template("crear_reclamo.html")

        session = db.session  # Aquí obtenemos la sesión de SQLAlchemy directamente

        posibles = gestor_reclamo.buscar_reclamos_por_departamento(reclamo.clasificacion, db.session)

        if posibles:
            posibles_data = [(r.descripcion, r.id) for r in posibles]
            # Buscar reclamos similares
            similares = gestor_reclamo.reclamos_similares(posibles_data, texto_reclamo)
        else:
            similares = []

        if not similares:
            # No se encontraron reclamos similares
            try:
                # Preparar los datos del reclamo para guardar
                data = [
                    reclamo.get_descripcion(),
                    reclamo.get_estado(),
                    reclamo.get_clasificacion(),
                    reclamo.get_fecha(),
                    reclamo.get_id_usuario()
                ]
                if reclamo.get_imagen():
                    data.append(reclamo.get_imagen())
                
                # Guardar el reclamo en la base de datos
                gestor_reclamo.guardar_reclamo(data)
                flash("Reclamo creado exitosamente.", "success")
            except Exception as e:
                flash(f"Error al guardar el reclamo: {str(e)}", "error")
            return render_template("reclamo.html", reclamos_similares="no hay reclamos similares")
        else:
            # Se encontraron reclamos similares
            lista_similares = []
            for id_similar in similares:
                reclamo_data = gestor_reclamo.buscar_reclamo_por_id(id_similar, db.session)
                if reclamo_data:
                    lista_similares.append(reclamo_data)

            return render_template("reclamo.html", lista_similares=lista_similares, reclamo=reclamo)

    return render_template("crear_reclamo.html")

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
