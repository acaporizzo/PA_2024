from flask_login import UserMixin, login_user, logout_user, current_user
from werkzeug.security import check_password_hash

class FlaskLoginUser(UserMixin):
    def __init__(self, usuario):
        self.id = usuario.id
        self.nombre = usuario.nombre
        self.email = usuario.email
        self.password = usuario.contraseña
        self.depto = usuario.departamento

class GestorLogin:
    def __init__(self, gestor_usuarios, login_manager, admin_list):
        self.__gestor_usuarios = gestor_usuarios
        login_manager.user_loader(self._cargar_usuario_actual)
        self.__admin_list = admin_list

    def verificar_credenciales(self, nombre_usuario, contraseña):
        """Verifica si las credenciales son válidas y devuelve un objeto Usuario."""
        try:
            usuario = self.__gestor_usuarios.cargar_usuario_por_nombre(nombre_usuario)
            if usuario and check_password_hash(usuario.contraseña, contraseña):
                return usuario
        except Exception as e:
            print(f"Error al verificar credenciales: {e}")
        return None

    def login_usuario(self, usuario):
        user = FlaskLoginUser(usuario)
        login_user(user)
        print(f"Usuario {current_user.nombre} ha iniciado sesión")

    @property
    def nombre_usuario_actual(self):
        return current_user.nombre

    @property
    def id_usuario_actual(self):
        return current_user.id
    
    @property
    def usuario_autenticado(self):
        return current_user.is_authenticated

    def _cargar_usuario_actual(self, id_usuario):
        dicc_usuario = self.__gestor_usuarios.cargar_usuario_por_id(id_usuario)
        if not dicc_usuario:
            print(f"Usuario con ID {id_usuario} no encontrado.")
            return None
        print(f"Usuario con ID {id_usuario} cargado: {dicc_usuario.nombre}")
        return FlaskLoginUser(dicc_usuario)
