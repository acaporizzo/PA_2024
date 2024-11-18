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

from flask import render_template, request, redirect, url_for, flash
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
    reclamos_similares = []
    usuario = gestor_usuario.cargar_usuario_por_id(id_usuario)
    #logger.debug(f'Usuario autenticado: {usuario}, ID Usuario: {id_usuario}')

    if request.method == "GET":
        return render_template("crear_reclamo.html", reclamos_similares=reclamos_similares)

    if request.method == "POST":
        contenido = request.form.get("description")
        print(f'Contenido del reclamo recibido: {contenido}')

        if not contenido:
            flash("La descripción del reclamo es obligatoria.", "error")
            print('Descripción del reclamo no proporcionada por el usuario.')
            return render_template("crear_reclamo.html", reclamos_similares=reclamos_similares)

        try:
            clasificacion = clasificador.clasificar([contenido])[0]
            print(f'Clasificación obtenida: {clasificacion}')

            id_reclamo = str(uuid.uuid4())
            fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            estado = "pendiente"
            
            lista_reclamo = [id_reclamo, id_usuario, contenido, clasificacion, estado, fecha_hora]

            imagen = request.files.get("imagen")
            if imagen:
                imagen_data = imagen.read()
                lista_reclamo.append(imagen_data)
            else:
                # Añadir None explícitamente si no hay imagen
                lista_reclamo.append(None)

            reclamo = gestor_reclamo.crear_reclamo(lista_reclamo)
            print(f'Reclamo creado (sin guardar aún): {lista_reclamo}')
        except Exception as e:
            flash(f"Error al clasificar el reclamo: {str(e)}", "error")
            print(f'Error al clasificar el reclamo: {str(e)}')
            return render_template("crear_reclamo.html", reclamos_similares=reclamos_similares)

        # Buscar posibles reclamos similares
        try:
            posibles = gestor_reclamo.obtener_reclamo_por_filtro("clasificacion", clasificacion)
            reclamos_similares = [(r.id, r.contenido) for r in posibles]
            logger.debug(f'Reclamos similares encontrados: {reclamos_similares}')
        except Exception as e:
            logger.error(f'Error al buscar reclamos similares: {str(e)}')
            reclamos_similares = []

        if reclamos_similares:
            reclamo_seleccionado = request.form.get("reclamo_seleccionado")
            if reclamo_seleccionado:
                try:
                    indice_reclamo_seleccionado = int(reclamo_seleccionado) - 1
                    if 0 <= indice_reclamo_seleccionado < len(reclamos_similares):
                        reclamo_id = reclamos_similares[indice_reclamo_seleccionado][0]
                        resultado_adherencia = gestor_reclamo.adherir_usuario_a_reclamo(reclamo_id, usuario)
                        if resultado_adherencia is True:
                            flash("Te has adherido al reclamo seleccionado con éxito.", "success")
                        elif resultado_adherencia is False:
                            flash("Ya estás adherido a este reclamo.", "info")
                        else:
                            flash("No se pudo encontrar el reclamo.", "error")
                        return redirect(url_for('crear_reclamo'))
                    else:
                        flash("Selección de reclamo no válida.", "error")
                except (ValueError, IndexError):
                    flash("Selección de reclamo no válida.", "error")
            else:
                # Si el usuario no seleccionó ningún reclamo similar, mostrar la opción de crear uno nuevo
                flash("Hay reclamos similares. Si deseas, puedes adherirte a uno o crear un nuevo reclamo.", "info")
                return render_template("crear_reclamo.html", reclamos_similares=reclamos_similares, permitir_crear_nuevo=True)
        else:
            # Si no existen reclamos similares, guardar el nuevo reclamo

            print(f"ID reclamo: {id_reclamo} - Tipo: {type(id_reclamo)}")
            print(f"ID usuario: {id_usuario} - Tipo: {type(id_usuario)}")
            print(f"Contenido de reclamo: {contenido} - Tipo: {type(contenido)}")
            print(f"Clasificación: {clasificacion} - Tipo: {type(clasificacion)}")
            print(f"Estado: {estado} - Tipo: {type(estado)}")
            print(f"Fecha a insertar: {fecha_hora} - Tipo: {type(fecha_hora)}")
            print(f"Imagen: {imagen} - Tipo: {type(imagen)}")

            try:
                gestor_reclamo.guardar_reclamo(lista_reclamo)
                print("Reclamo creado exitosamente.")
                flash("Reclamo creado exitosamente.", "success")
            except Exception as e:
                flash(f"Error al guardar el reclamo: {str(e)}", "error")
                logger.error(f'Error al guardar el reclamo: {str(e)}')
            return render_template("crear_reclamo.html", reclamos_similares="No hay reclamos similares")



@app.route('/cerrar_sesion')
def cerrar_sesion():
    logout_user()
    flash("Sesión cerrada", "success")
    
    return redirect(url_for('iniciar_sesion'))

@app.route('/listar_reclamos')
def listar_reclamos():
    return render_template('listar_reclamos.html')

@app.route('/mis_reclamos')
@login_required  # Si aplica autenticación
def mis_reclamos():
    # Obtener el usuario actual
    id_usuario = str(gestor_login.id_usuario_actual)
    usuario = gestor_usuario.cargar_usuario_por_id(id_usuario)
    
    # Obtener todos los reclamos asociados al usuario
    reclamos = gestor_reclamo.obtener_reclamo_por_filtro("usuario", id_usuario)
    print(f'Reclamos obtenidos: {reclamos}')
    # Renderizar el template y pasar los reclamos
    return render_template('mis_reclamos.html', reclamos=reclamos)


if __name__ == "__main__":
    app.run(debug=True)
