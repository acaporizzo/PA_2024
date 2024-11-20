from modules.dominio import Reclamo, Usuario
from modules.config import db
from sqlalchemy.orm.exc import NoResultFound
from modules.modelos import ModeloReclamo, ModeloUsuario
from modules.classifier import ClaimsClassifier
from uuid import uuid4
from werkzeug.security import generate_password_hash

class GestorReclamo:
    def __init__(self, repositorio_reclamos):
        self.repositorio = repositorio_reclamos

    def crear_reclamo(self, lista_reclamo): 
        nuevo_reclamo = Reclamo(lista_reclamo[0], lista_reclamo[1], lista_reclamo[2], lista_reclamo[3], lista_reclamo[4], lista_reclamo[5])
        try:
            nuevo_reclamo.cargar_imagen(lista_reclamo[6])
        except: 
            pass
        return nuevo_reclamo

    def obtener_reclamo_por_filtro(self, tipo_de_filtro="todo", filtro="nada"):
        tipo_de_filtro = tipo_de_filtro.lower()
        filtro = filtro.lower()
        if tipo_de_filtro == "nada" and filtro == "nada":
            reclamos = db.session.query(ModeloReclamo).all()
        elif tipo_de_filtro == "usuario":
            reclamos = db.session.query(ModeloReclamo).filter(ModeloReclamo.id_usuario == filtro).all()
        elif tipo_de_filtro == "estado":
            reclamos = db.session.query(ModeloReclamo).filter(ModeloReclamo.estado == filtro).all()
        elif tipo_de_filtro == "clasificacion":
            reclamos = db.session.query(ModeloReclamo).filter(ModeloReclamo.clasificacion.ilike(f'%{filtro}%')).all()
        elif tipo_de_filtro == "id":
            try:
                reclamo = db.session.query(ModeloReclamo).filter(ModeloReclamo.id == filtro).one()
                return self.repositorio._map_modelo_a_entidad(reclamo)  # Llama al método desde el repositorio
            except NoResultFound:
                raise Exception("El reclamo no existe")
        elif tipo_de_filtro == "departamento":
            reclamos = db.session.query(ModeloReclamo).filter(ModeloReclamo.departamento == filtro).all()
        else:
            raise Exception("El filtro que eligió no existe, pruebe con uno válido")

        lista_de_datos_reclamos = []
        for reclamo in reclamos:
            datos = {
                "id": reclamo.id,
                "id_usuario": reclamo.id_usuario,
                "contenido": reclamo.contenido,
                "clasificacion": reclamo.clasificacion,
                "estado": reclamo.estado,
                "imagen": reclamo.imagen,
                "fecha": reclamo.fecha
            }
            lista_de_datos_reclamos.append(datos)

        return lista_de_datos_reclamos
    
    def obtener_numero_adherentes(self, id_reclamo):
        try:
            reclamo = db.session.query(ModeloReclamo).filter_by(id=id_reclamo).first()
            if not reclamo:
                return 0
            
            return len(reclamo.usuarios_adheridos)
        except Exception as e:
            raise Exception(f"Error al obtener el número de adherentes: {str(e)}")

    def obtener_reclamos_adheridos_por_usuario(self, id_usuario):
        try:
            usuario = db.session.query(ModeloUsuario).filter_by(id=id_usuario).first()
            if not usuario:
                raise Exception("Usuario no encontrado")

            return [
                {
                    "id": r.id,
                    "contenido": r.contenido,
                    "clasificacion": r.clasificacion,
                    "estado": r.estado,
                    "fecha": r.fecha
                }
                for r in usuario.reclamos_adheridos
            ]
        except Exception as e:
            raise Exception(f"Error al obtener reclamos adheridos: {str(e)}")
        
    def obtener_id_usuarios_adheridos(self, id_reclamo):
        """
        Obtiene los IDs de los usuarios que están adheridos a un reclamo dado.

        :param id_reclamo: ID del reclamo para el que se quieren obtener los usuarios adheridos.
        :return: Una lista de IDs de usuarios adheridos o una lista vacía si no hay usuarios adheridos.
        """
        try:
            # Busca el reclamo por su ID
            reclamo = self.db_session.query(ModeloReclamo).filter_by(id=id_reclamo).first()
            if not reclamo:
                print(f"Reclamo con ID {id_reclamo} no encontrado.")
                return []
            print(f"Usuarios adheridos encontrados para el reclamo {id_reclamo}: {reclamo.usuarios_adheridos}")
            if reclamo.usuarios_adheridos:
                usuarios_adheridos_ids = [usuario.id for usuario in reclamo.usuarios_adheridos]
                print(f"IDs de usuarios adheridos al reclamo {id_reclamo}: {usuarios_adheridos_ids}")
                return usuarios_adheridos_ids
            else:
                print(f"No hay usuarios adheridos al reclamo {id_reclamo}.")
                return []
        except Exception as e:
            print(f"Error al obtener los usuarios adheridos para el reclamo {id_reclamo}: {e}")
            return[]

    def guardar_reclamo(self, datos):
        imagen = datos[6]

        nuevo_reclamo = ModeloReclamo(
            id=datos[0],
            id_usuario=datos[1],
            contenido=datos[2],
            clasificacion=datos[3],
            estado=datos[4],
            fecha=datos[5],
        )
        try: 
            nuevo_reclamo.añadir_imagen(imagen)
        except IndexError:
            pass

        db.session.add(nuevo_reclamo)
        db.session.commit()

    def adherir_usuario_a_reclamo(self, id_reclamo, usuario):
        try:
            reclamo = db.session.query(ModeloReclamo).filter_by(id=id_reclamo).first()
            if not reclamo:
                return "reclamo_no_encontrado"

            if usuario in reclamo.usuarios_adheridos:
                return "ya_adherido"

            reclamo.usuarios_adheridos.append(usuario)

            db.session.commit()
            return "adherido_exitosamente"
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al adherir usuario al reclamo: {str(e)}")

    def actualizar_estado_reclamo(self, reclamo_id, nuevo_estado):
        reclamo = db.session.query(ModeloReclamo).filter(ModeloReclamo.id == reclamo_id).one_or_none()  # Usa 'id' en lugar de 'id_reclamo'
        if reclamo:
            reclamo.estado = nuevo_estado
            db.session.commit()
        else:
            raise Exception("El reclamo no existe")

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

    def cargar_usuario_por_id(self, id_usuario):
        return self.__repo_usuario.obtener_usuario_por_id(id_usuario)
    
    def cargar_usuario_por_nombre(self, nombre_usuario):
        return self.__repo_usuario.obtener_usuario_por_nombre(nombre_usuario)
 
    def existe_email(self, email):
        usuario = db.session.query(ModeloUsuario).filter_by(email=email).first()
        return usuario is not None
    
    def existe_nombre_usuario(self, nombre_usuario):
        usuario = db.session.query(ModeloUsuario).filter_by(nombre_usuario=nombre_usuario).first()
        return usuario is not None
    
class GestorBaseDeDatos:
        
    def guardar_nuevo_objeto(self, tipo_objeto, datos):
        """
        Guarda un nuevo objeto en la base de datos basado en su tipo.
        
        :param tipo_objeto: Tipo de objeto a guardar (por ejemplo, "jefe").
        :param datos: Lista con los datos del objeto.
        """
        try:
            if tipo_objeto == "jefe":
                nuevo_usuario = ModeloUsuario(
                    id=str(uuid4()),
                    nombre=datos[0],
                    apellido=datos[1],
                    nombre_usuario=datos[2],
                    email=datos[3],
                    contraseña=generate_password_hash(datos[4]),
                    claustro=datos[5],
                    rol=datos[6],
                    departamento=datos[7]
                )
                db.session.add(nuevo_usuario)
                db.session.commit()
                print(f"Jefe {datos[2]} guardado exitosamente.")
            else:
                raise ValueError(f"Tipo de objeto '{tipo_objeto}' no soportado.")
        except Exception as e:
            db.session.rollback()
            print(f"Error al guardar el objeto de tipo '{tipo_objeto}': {e}")
            raise