from modules.dominio import Reclamo, Usuario
from modules.config import db
from sqlalchemy.orm.exc import NoResultFound
from modules.modelos import ModeloReclamo, ModeloUsuario
from modules.classifier import ClaimsClassifier
from modules.dominio import Usuario

class GestorReclamo:
    def __init__(self, repositorio_reclamos):
        self.repositorio = repositorio_reclamos

    def mostrar_reclamos(self):
        return self.repositorio.obtener_todos_los_registros()

    def mostrar_reclamos_de_usuario(self, usuario):
        return self.repositorio.obtener_registros_seguidas_por_usuario(usuario)

    def clasificar_reclamo(self, reclamo):
        reclamo.clasificacion = ClaimsClassifier().clasificar(reclamo.descripcion)

    def crear_reclamo(self, lista_reclamo): 
        nuevo_reclamo = Reclamo(lista_reclamo[0], lista_reclamo[1], lista_reclamo[2], lista_reclamo[3], lista_reclamo[4], lista_reclamo[5])
        try:
            nuevo_reclamo.cargar_imagen(lista_reclamo[6])
        except: 
            pass
        return nuevo_reclamo

    def obtener_reclamo_por_filtro (self, tipo_de_filtro = "todo", filtro = "nada"):

        tipo_de_filtro = tipo_de_filtro.lower()
        if tipo_de_filtro == "nada" and filtro == "nada":
            reclamos= db.session.query(ModeloReclamo).all()

        elif tipo_de_filtro == "usuario":
             reclamos=db.session.query(ModeloReclamo).filter(ModeloReclamo.id_usuario == filtro).all()

        elif tipo_de_filtro == "estado":
            reclamos=db.session.query(ModeloReclamo).filter(ModeloReclamo.estado == filtro).all()
        
        elif tipo_de_filtro == "clasificacion":
            reclamos= db.session.query(ModeloReclamo).filter(ModeloReclamo.clasificacion == filtro).all()

        elif tipo_de_filtro == "id":
            try:
                reclamo = db.session.query(ModeloReclamo).filter(ModeloReclamo.id == filtro).one()
                return self._map_modelo_a_entidad(reclamo)
            except NoResultFound:
                raise Exception("El reclamo no existe")

        else:
            raise Exception ("El filtro que eligió no existe, pruebe con ")

        lista_de_datos_reclamos = []
        for reclam in reclamos:
            datos = [
                reclam.id,
                reclam.id_usuario,
                reclam.contenido,
                reclam.clasificacion,
                reclam.estado,
                reclam.imagen,
                reclam.fecha
            ]
            lista_de_datos_reclamos.append(datos)

        return lista_de_datos_reclamos
    
    def guardar_reclamo(self, datos):
        # Asegúrate de que 'imagen' sea manejada desde 'datos'
        imagen = datos[6]  # Extraer 'imagen' de la lista de datos

        nuevo_reclamo = ModeloReclamo(
            id=datos[0],
            id_usuario=datos[1],
            contenido=datos[2],
            clasificacion=datos[3],
            estado=datos[4],
            fecha=datos[5],  # Si es None, debería ser aceptado
        )

        try: 
            nuevo_reclamo.añadir_imagen(imagen)
        except IndexError: #no hay dato[5], es decir, imagen
            pass

        db.session.add(nuevo_reclamo)
        db.session.commit()

    def derivar_reclamo(self, id_reclamo, nuevo_departamento):
        reclamo = self.repositorio.obtener_registro_por_filtro("id_reclamo", id_reclamo)
        if reclamo:
            reclamo.clasificacion = nuevo_departamento
            self.repositorio.modificar_registro(reclamo)
            return reclamo
        return None

    def modificar_estado_reclamo(self, id_reclamo, nuevo_estado):
        reclamo = self.repositorio.obtener_registro_por_filtro("id_reclamo", id_reclamo)
        if reclamo:
            reclamo.estado = nuevo_estado
            self.repositorio.modificar_registro(reclamo)
            return reclamo
        return None

class GestorUsuario:
    def __init__(self, repo_usuario):
        self.__repo_usuario = repo_usuario

    def registrar_usuario(self, id, nombre, apellido, nombre_usuario, email, contraseña, claustro, rol, departamento):
        with db.session.begin():  # Garantiza que la sesión esté activa
            if any(usuario.nombre_usuario == nombre_usuario for usuario in self.__repo_usuario.obtener_todos_los_registros()):
                raise ValueError(f"El nombre de usuario '{nombre_usuario}' ya está en uso.")

            nuevo_usuario = Usuario(
                id=id,
                nombre=nombre,
                apellido=apellido,
                nombre_usuario=nombre_usuario,
                email=email,
                contraseña=contraseña,
                claustro=claustro,
                rol=rol,
                departamento=departamento
            )
            self.__repo_usuario.guardar_registro(nuevo_usuario)
        return nuevo_usuario


    def cargar_usuario_por_nombre(self, nombre_usuario):
        """Carga el usuario desde el repositorio por su nombre de usuario."""
        return self.__repo_usuario.obtener_usuario_por_nombre(nombre_usuario)

    def cargar_usuario_por_id(self, id_usuario):
        """Carga el usuario desde el repositorio por su ID."""
        return self.__repo_usuario.obtener_usuario_por_id(id_usuario)
    
class GestorBaseDeDatos:
    def obtener_usuario_por_nombre(self, nombre_usuario):
        try:
            usuario = db.session.query(ModeloUsuario).filter_by(nombre_usuario=nombre_usuario).one()
            return usuario
        except NoResultFound: 
            raise Exception("El usuario no fue encontrado")
    
