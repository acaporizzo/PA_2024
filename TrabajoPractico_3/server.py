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
from modules.reclamos_similares import reclamos_similares
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "instance", "base_datos.db")

with app.app_context():
    db.create_all()
    inspector = inspect(db.engine)
    print("Tablas existentes:", inspector.get_table_names())

admin_list = [1]
repo_reclamo , repo_usuario = crear_repositorio()

gestor_reclamo = GestorReclamo(repo_reclamo)
gestor_usuario = GestorUsuario(repo_usuario)
gestor_login = GestorLogin(gestor_usuario, login_manager, admin_list)
gestor_BD = GestorBaseDeDatos()

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
def panel_usuario():
    return render_template("panel_usuario.html")

@app.route('/crear_reclamo', methods=['GET', 'POST'])
@login_required
def crear_reclamo():
    id_usuario = str(gestor_login.id_usuario_actual)
    usuario = gestor_usuario.cargar_usuario_por_id(id_usuario)

    if request.method == "GET":
        # Renderizar formulario inicial para que el usuario ingrese un reclamo
        return render_template("crear_reclamo.html", reclamos_similares=[])

    if request.method == "POST":
        # Paso 1: El usuario ingresa el contenido del reclamo
        contenido = request.form.get("description")
        print(f'Contenido del reclamo recibido: {contenido}')

        if not contenido:
            flash("La descripción del reclamo es obligatoria.", "error")
            print('Descripción del reclamo no proporcionada por el usuario.')
            return render_template("crear_reclamo.html", reclamos_similares=[])

        try:
            # Paso 2: Clasificar el reclamo
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
            print(f'Reclamo creado (sin guardar aún): {lista_reclamo}')

            # Paso 3: Buscar reclamos similares por clasificación
            posibles = gestor_reclamo.obtener_reclamo_por_filtro("clasificacion", clasificacion)
            reclamos_similares = [
                {"id": r["id"], "contenido": r["contenido"], "clasificacion": r["clasificacion"]}
                for r in posibles
            ]
            print(f"Reclamos similares son: {reclamos_similares}")

            # Paso 4: Si hay reclamos similares, redirigir a la nueva ruta para seleccionar un reclamo
            if reclamos_similares:
                # Guardar el reclamo en la sesión temporal para usarlo en la otra ruta
                session['lista_reclamo'] = lista_reclamo
                session['clasificacion_actual'] = clasificacion
                session['reclamos_similares'] = reclamos_similares
                return redirect(url_for('seleccionar_reclamo'))

            # Si no hay reclamos similares, guardar el reclamo directamente
            gestor_reclamo.guardar_reclamo(lista_reclamo)
            print("Reclamo creado exitosamente.", "success")
            return redirect(url_for('mis_reclamos'))

        except Exception as e:
            print(f"Error al procesar el reclamo: {str(e)}", "error")
            return render_template("crear_reclamo.html")

@app.route('/seleccionar_reclamo', methods=['GET', 'POST'])
@login_required
def seleccionar_reclamo():
    reclamos_similares = session.get('reclamos_similares', [])
    lista_reclamo = session.get('lista_reclamo')
    clasificacion_actual = session.get('clasificacion_actual')
    usuario_id = gestor_login.id_usuario_actual
    usuario = db.session.query(ModeloUsuario).filter_by(id=usuario_id).first()
    print(f"El usuario es el siguiente {usuario}")

    if request.method == "GET":
        return render_template("reclamos_similares.html", reclamos_similares=reclamos_similares)

    if request.method == "POST":
        # Manejar acción de adherirse a un reclamo similar
        print("Datos recibidos en la solicitud POST:", request.form)
        if request.form.get("adherirse"):
            print("Se recibió el valor de 'adherirse'")
            reclamo_id = request.form.get("reclamo_seleccionado")
            print(f"ID del reclamo seleccionado para adherirse: {reclamo_id} y es del tipo {type(reclamo_id)}:")

            if reclamo_id:
                try:
                    # Usar el método del gestor para obtener el reclamo por su ID
                    reclamo_seleccionado = gestor_reclamo.obtener_reclamo_por_filtro(tipo_de_filtro="id", filtro=reclamo_id)
                    if not reclamo_seleccionado:
                        print("El reclamo seleccionado no se encontró.", "error")
                        return render_template("reclamos_similares.html", reclamos_similares=reclamos_similares)

                    # Procesar la adhesión
                    resultado_adherencia = gestor_reclamo.adherir_usuario_a_reclamo(reclamo_seleccionado.id_reclamo, usuario)

                    if resultado_adherencia == "adherido_exitosamente":
                        print("Te has adherido al reclamo seleccionado con éxito.", "success")
                        return redirect(url_for('mis_reclamos'))
                    elif resultado_adherencia == "ya_adherido":
                        print("Ya estás adherido a este reclamo.", "info")
                        return redirect(url_for('mis_reclamos'))
                    else:
                        print("No se pudo encontrar el reclamo.", "error")
                except Exception as e:
                    print(f"Error al adherirse al reclamo: {str(e)}", "error")
                    return render_template("reclamos_similares.html", reclamos_similares=reclamos_similares)

        # Manejar acción de crear un nuevo reclamo si el usuario no quiere adherirse
        if request.form.get("confirmar_creacion"):
            try:
                gestor_reclamo.guardar_reclamo(lista_reclamo)
                print("Reclamo creado exitosamente.", "success")
                return redirect(url_for('mis_reclamos'))
            except Exception as e:
                print(f"Error al guardar el reclamo, a pesar de tener similares: {str(e)}", "error")
                return render_template("reclamos_similares.html", reclamos_similares=reclamos_similares)

    
@app.route('/mis_reclamos', methods=['GET'])
@login_required
def mis_reclamos():
    id_usuario = str(gestor_login.id_usuario_actual)
    try:
        # Obtener reclamos creados por el usuario
        reclamos_creados = gestor_reclamo.obtener_reclamo_por_filtro("usuario", id_usuario)

        # Obtener reclamos a los que el usuario se ha adherido
        reclamos_adheridos = gestor_reclamo.obtener_reclamos_adheridos_por_usuario(id_usuario)

        return render_template(
            "mis_reclamos.html", 
            reclamos_creados=reclamos_creados, 
            reclamos_adheridos=reclamos_adheridos
        )
    except Exception as e:
        flash(f"Error al cargar tus reclamos: {str(e)}", "error")
        return render_template("mis_reclamos.html", reclamos_creados=[], reclamos_adheridos=[])

    
@app.route('/cerrar_sesion')
def cerrar_sesion():
    logout_user()
    flash("Sesión cerrada", "success")
    
    return redirect(url_for('iniciar_sesion'))

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
        # Obtener el tipo de filtro y su valor del formulario
        filtro_tipo = request.form.get('filtro_tipo')
        filtro_valor = request.form.get('filtro_valor')

        # Aplicar el filtro si ambos están presentes
        if filtro_tipo and filtro_valor:
            reclamos = gestor_reclamo.obtener_reclamo_por_filtro(tipo_de_filtro=filtro_tipo, filtro=filtro_valor)
            if not reclamos:
                mensaje = f"No se encontraron reclamos para el filtro '{filtro_tipo}' con valor '{filtro_valor}'."
        else:
            # Obtener todos los reclamos pendientes si no hay filtros
            reclamos = gestor_reclamo.obtener_reclamo_por_filtro(tipo_de_filtro="estado", filtro="pendiente")

    return render_template(
        'listar_reclamos.html', 
        reclamos=reclamos, 
        filtros=filtros, 
        filtro_tipo=filtro_tipo, 
        filtro_valor=filtro_valor, 
        mensaje=mensaje
    )


if __name__ == "__main__":
    app.run(debug=True)
