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
    usuario = str(gestor_login.usuario_autenticado)

    if request.method == "POST":
        contenido = request.form.get("description")
        
        if not contenido:
            flash("La descripción del reclamo es obligatoria.", "error")
            return render_template("crear_reclamo.html", reclamos_similares=reclamos_similares)

        try:
            clasificacion = clasificador.clasificar([contenido])[0]

            id_reclamo = str(uuid.uuid4())  # UUID como cadena
            fecha_hora = datetime.now()
            imagen = None  #la imagen es opcional (se queda como None si no se usa)
            
            lista_reclamo = [
                id_reclamo,
                id_usuario,
                contenido,
                clasificacion,
                "pendiente",
                fecha_hora,
                imagen]
            
            #creamos el reclamo en el sistema (pero no lo guardamos aún), SOLO LO INSTANCIAMOS
            reclamo = gestor_reclamo.crear_reclamo(lista_reclamo)

        except Exception as e:
            flash(f"Error al clasificar el reclamo: {str(e)}", "error")
            return render_template("crear_reclamo.html", reclamos_similares=reclamos_similares)

        #buscar posibles reclamos similares
        try:
            posibles = gestor_reclamo.obtener_reclamo_por_filtro("clasificacion", clasificacion)
            posibles_reclamos = [(r.get_contenido(), r.get_id_reclamo()) for r in posibles]  # Formato [(descripcion, ID)]
            reclamos_similares = reclamos_similares(posibles_reclamos, contenido)
        except Exception as e:
            print(f"Error al buscar reclamos similares: {str(e)}")

        if len(reclamos_similares) > 0:
            # Si existen reclamos similares, mostramos los reclamos y el usuario podrá adherirse
            reclamo_seleccionado = request.form.get("reclamo_seleccionado")
       
            indice_reclamo_seleccionado = int(reclamo_seleccionado) - 1  # Restamos 1 porque el índice es 0-based
                
            if reclamo_seleccionado < len(reclamos_similares) and reclamo_seleccionado >= 0:
                # Buscamos el reclamo seleccionado
                reclamo_a_adherirse = reclamos_similares[indice_reclamo_seleccionado]
                    
                # Ahora adherimos el usuario a este reclamo
                try:
                    # Usar la relación para agregar el usuario al reclamo
                    reclamo_a_adherirse.usuarios_adheridos.append(usuario)
                    db.session.commit()  # Guardar los cambios en la base de datos
                    flash("Te has adherido al reclamo exitosamente.", "success")
                except Exception as e:
                    flash(f"Error al adherirse al reclamo: {str(e)}", "error")
                
                return redirect(url_for('crear_reclamo'))
            mensaje = "Ingresó un número de reclamo que no existe"
            return render_template("crear_reclamo.html", reclamos_similares=reclamos_similares, reclamo=reclamo, mensaje=mensaje)
        else:
            # Si no existen reclamos similares, guardamos el nuevo reclamo, ahora sí se crea uno nuevo
            try:
                gestor_reclamo.guardar_reclamo(lista_reclamo)
                flash("Reclamo creado exitosamente.", "success")
            except Exception as e:
                flash(f"Error al guardar el reclamo: {str(e)}", "error")
            return render_template("crear_reclamo.html", reclamos_similares="No hay reclamos similares")

    return render_template("crear_reclamo.html", reclamos_similares=reclamos_similares)

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

if __name__ == "__main__":
    app.run(debug=True)
