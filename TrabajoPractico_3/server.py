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

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import login_required
from flask_login import logout_user
from sqlalchemy import inspect
from datetime import datetime
from werkzeug.security import generate_password_hash
import uuid, pickle

from modules.gestores import GestorReclamo, GestorBaseDeDatos, GestorUsuario
from modules.factoria import crear_repositorio
from modules.gestor_login import GestorLogin
from modules.modelos import ModeloReclamo, ModeloUsuario
from modules.config import app, login_manager, db
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "instance", "base_datos.db")

with app.app_context():
    db.create_all()
    inspector = inspect(db.engine)

admin_list = [1]
repo_reclamo , repo_usuario = crear_repositorio()

gestor_reclamo = GestorReclamo(repo_reclamo)
gestor_usuario = GestorUsuario(repo_usuario)
gestor_login = GestorLogin(gestor_usuario, login_manager, admin_list)
gestor_BD = GestorBaseDeDatos()

try:
    with open('./data/claims_clf.pkl', 'rb') as archivo:
        clasificador = pickle.load(archivo)
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

        if contraseña != confirmacion:
            flash("Las contraseñas no coinciden", "error")
            return redirect(url_for('registrar'))
        
        if gestor_usuario.existe_email(email):
            flash("El correo electrónico ya está registrado. Usa otro.", "error")
            return redirect(url_for('registrar'))
        
        if gestor_usuario.existe_nombre_usuario(nombre_usuario):
            flash("El nombre de usuario ya está en uso. Elige otro.", "error")
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
            return redirect(url_for('iniciar_sesion'))
        
        except ValueError as e:
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
                tipo_usuario = usuario_valido.rol
                departamento = usuario_valido.departamento

                if tipo_usuario == "Jefe de Departamento":
                    return redirect(url_for('panel_jefe', depto=departamento))
                else:
                    return redirect(url_for('panel_usuario'))
            else:
                flash("Usuario o contraseña incorrectos", "error")

    return render_template("iniciar_sesion.html")

@app.route('/panel_usuario')
def panel_usuario():
    return render_template("panel_usuario.html")

@app.route('/panel_jefe/<depto>', methods=['GET', 'POST'])
def panel_jefe(depto):
    depto = depto.capitalize()
    
    if request.method == 'POST':
        direction = request.form.get("button_value")
        
        if direction == "Manejar reclamos":
            return redirect(url_for('manejar_reclamos', departamento=depto))
        elif direction == "Analítica":
            return redirect(url_for('analitica', departamento=depto))
        elif direction == "Panel general":
            return redirect(url_for('panel_general', departamento=depto))
    
    return render_template('panel_jefe.html', opciones=["Analítica", "Manejar Reclamos", "Ayuda", "Salir"], depto=depto)

@app.route('/crear_reclamo', methods=['GET', 'POST'])
@login_required
def crear_reclamo():
    id_usuario = str(gestor_login.id_usuario_actual)
    usuario = gestor_usuario.cargar_usuario_por_id(id_usuario)

    if request.method == "GET":
        # Renderizar formulario inicial para que el usuario ingrese un reclamo
        return render_template("crear_reclamo.html", reclamos_similares=[])

    if request.method == "POST":
        contenido = request.form.get("description")

        if not contenido:
            return render_template("crear_reclamo.html", reclamos_similares=[])

        try:
            clasificacion = clasificador.clasificar([contenido])[0]
            id_reclamo = str(uuid.uuid4())
            fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            estado = "pendiente"

            lista_reclamo = [id_reclamo, id_usuario, contenido, clasificacion, estado, fecha_hora]
            imagen = request.files.get("imagen")

            if imagen:
                imagen_data = imagen.read()
                lista_reclamo.append(imagen_data)
            else:
                lista_reclamo.append(None)

            # Crear reclamo pero no guardarlo aún
            reclamo = gestor_reclamo.crear_reclamo(lista_reclamo)

            posibles = gestor_reclamo.obtener_reclamo_por_filtro("clasificacion", clasificacion)
            reclamos_similares = [
                {"id": r["id"], "contenido": r["contenido"], "clasificacion": r["clasificacion"]}
                for r in posibles
            ]

            if reclamos_similares:
                # Guardar el reclamo en la sesión temporal para usarlo en la otra ruta
                session['lista_reclamo'] = lista_reclamo
                session['clasificacion_actual'] = clasificacion
                session['reclamos_similares'] = reclamos_similares
                return redirect(url_for('seleccionar_reclamo'))

            gestor_reclamo.guardar_reclamo(lista_reclamo)
            return redirect(url_for('mis_reclamos'))

        except Exception as e:
            return render_template("crear_reclamo.html")

@app.route('/seleccionar_reclamo', methods=['GET', 'POST'])
@login_required
def seleccionar_reclamo():
    reclamos_similares = session.get('reclamos_similares', [])
    lista_reclamo = session.get('lista_reclamo')
    clasificacion_actual = session.get('clasificacion_actual')
    usuario_id = gestor_login.id_usuario_actual
    usuario = db.session.query(ModeloUsuario).filter_by(id=usuario_id).first()

    if request.method == "GET":
        return render_template("reclamos_similares.html", reclamos_similares=reclamos_similares)

    if request.method == "POST":
        if request.form.get("adherirse"):
            reclamo_id = request.form.get("reclamo_seleccionado")

            if reclamo_id:
                try:
                    reclamo_seleccionado = gestor_reclamo.obtener_reclamo_por_filtro(tipo_de_filtro="id", filtro=reclamo_id)
                    if not reclamo_seleccionado:
                        return render_template("reclamos_similares.html", reclamos_similares=reclamos_similares)

                    resultado_adherencia = gestor_reclamo.adherir_usuario_a_reclamo(reclamo_seleccionado.id_reclamo, usuario)

                    if resultado_adherencia == "adherido_exitosamente":
                        return redirect(url_for('mis_reclamos'))
                    elif resultado_adherencia == "ya_adherido":
                        return redirect(url_for('mis_reclamos'))
                    else:
                        print("No se pudo encontrar el reclamo.", "error")
                except Exception as e:
                    return render_template("reclamos_similares.html", reclamos_similares=reclamos_similares)

        # Manejar acción de crear un nuevo reclamo si el usuario no quiere adherirse
        if request.form.get("confirmar_creacion"):
            try:
                # Verificar que los datos del reclamo están en la sesión
                if not lista_reclamo:
                    return redirect(url_for('crear_reclamo'))

                gestor_reclamo.guardar_reclamo(lista_reclamo)
                return redirect(url_for('mis_reclamos'))
            except Exception as e:
                return render_template("reclamos_similares.html", reclamos_similares=reclamos_similares)

@app.route('/mis_reclamos', methods=['GET'])
@login_required
def mis_reclamos():
    id_usuario = str(gestor_login.id_usuario_actual)
    try:
        reclamos_creados = gestor_reclamo.obtener_reclamo_por_filtro("usuario", id_usuario)

        reclamos_adheridos = gestor_reclamo.obtener_reclamos_adheridos_por_usuario(id_usuario)

        return render_template(
            "mis_reclamos.html", 
            reclamos_creados=reclamos_creados, 
            reclamos_adheridos=reclamos_adheridos
        )
    except Exception as e:
        return render_template("mis_reclamos.html", reclamos_creados=[], reclamos_adheridos=[])

@app.route('/listar_reclamos', methods=['GET', 'POST'])
def listar_reclamos():
    filtros = {
        "clasificacion": ["Maestranza", "Secretaría Técnica", "Soporte Informático"],
        "estado": ["Inválido", "Pendiente", "En proceso", "Resuelto"]
    }
    reclamos = []
    filtro_tipo = None
    filtro_valor = None
    mensaje = None

    if request.method == 'POST':
        filtro_tipo = request.form.get('filtro_tipo')
        filtro_valor = request.form.get('filtro_valor')

        if filtro_tipo and filtro_valor:
            reclamos = gestor_reclamo.obtener_reclamo_por_filtro(tipo_de_filtro=filtro_tipo, filtro=filtro_valor)
            if not reclamos:
                mensaje = f"No se encontraron reclamos para el filtro '{filtro_tipo}' con valor '{filtro_valor}'."
        else:
            reclamos = gestor_reclamo.obtener_reclamo_por_filtro(tipo_de_filtro="estado", filtro="pendiente")

        for reclamo in reclamos:
            reclamo["numero_adherentes"] = gestor_reclamo.obtener_numero_adherentes(reclamo["id"])

    return render_template(
        'listar_reclamos.html', 
        reclamos=reclamos, 
        filtros=filtros, 
        filtro_tipo=filtro_tipo, 
        filtro_valor=filtro_valor, 
        mensaje=mensaje
    )

@app.route('/manejar_reclamos/<departamento>', methods=['GET', 'POST'])
def manejar_reclamos(departamento):
    print(f"Accediendo a /manejar_reclamos con departamento: {departamento}")

    try:
        reclamos = gestor_reclamo.obtener_reclamo_por_filtro("clasificacion", departamento)
    except Exception as e:
        reclamos = []

    if request.method == 'POST':
        reclamo_id = request.form.get("reclamo_id")
        nuevo_estado = request.form.get("nuevo_estado")
        
        if reclamo_id and nuevo_estado:
            try:
                gestor_reclamo.actualizar_estado_reclamo(reclamo_id, nuevo_estado)
                reclamos = gestor_reclamo.obtener_reclamo_por_filtro("clasificacion", departamento)
            except Exception as e:
                print(f"Error al actualizar el reclamo: {str(e)}")
        else:
            print("Error: No se proporcionó reclamo_id o nuevo_estado")

    return render_template(
        'manejar_reclamos.html',
        reclamos=reclamos,
        departamento=departamento
    )

@app.route('/cerrar_sesion')
def cerrar_sesion():
    logout_user()
    flash("Sesión cerrada", "success")
    
    return redirect(url_for('iniciar_sesion'))

if __name__ == "__main__":
    app.run(debug=True)
