import unittest
from unittest.mock import MagicMock, patch
from werkzeug.security import generate_password_hash
from flask_login import LoginManager
from modules.gestor_login import GestorLogin, FlaskLoginUser

class UsuarioMock:
    """Mock de un usuario del sistema."""
    def __init__(self, id, nombre, email, contraseña, departamento):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.contraseña = contraseña
        self.departamento = departamento

class TestGestorLogin(unittest.TestCase):
    def setUp(self):
        # Crear mocks necesarios
        self.gestor_usuarios_mock = MagicMock()
        self.login_manager = LoginManager()
        self.admin_list = ['admin@example.com']

        # Instanciar el GestorLogin con mocks
        self.gestor_login = GestorLogin(self.gestor_usuarios_mock, self.login_manager, self.admin_list)

    def test_verificar_credenciales_exitoso(self):
        """Prueba que verificar_credenciales devuelva un usuario válido."""
        usuario = UsuarioMock(1, "test_user", "test@example.com", generate_password_hash("1234"), "TI")
        self.gestor_usuarios_mock.cargar_usuario_por_nombre.return_value = usuario

        resultado = self.gestor_login.verificar_credenciales("test_user", "1234")

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "test_user")
        self.gestor_usuarios_mock.cargar_usuario_por_nombre.assert_called_once_with("test_user")

    def test_verificar_credenciales_incorrecto(self):
        """Prueba que verificar_credenciales falle con credenciales incorrectas."""
        usuario = UsuarioMock(1, "test_user", "test@example.com", generate_password_hash("1234"), "TI")
        self.gestor_usuarios_mock.cargar_usuario_por_nombre.return_value = usuario

        resultado = self.gestor_login.verificar_credenciales("test_user", "wrong_password")

        self.assertIsNone(resultado)
        self.gestor_usuarios_mock.cargar_usuario_por_nombre.assert_called_once_with("test_user")

    #@patch("gestor_login.login_user")
    #def test_login_usuario(self, mock_login_user):
    #    """Prueba que login_usuario invoque a login_user correctamente."""
    #    usuario = UsuarioMock(1, "test_user", "test@example.com", "1234", "TI")

    #    self.gestor_login.login_usuario(usuario)

    #    mock_login_user.assert_called_once()
    #    self.assertEqual(mock_login_user.call_args[0][0].nombre, "test_user")

    def test_cargar_usuario_actual(self):
        """Prueba que _cargar_usuario_actual cargue correctamente un usuario."""
        usuario = UsuarioMock(1, "test_user", "test@example.com", "1234", "TI")
        self.gestor_usuarios_mock.cargar_usuario_por_id.return_value = usuario

        resultado = self.gestor_login._cargar_usuario_actual(1)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "test_user")
        self.gestor_usuarios_mock.cargar_usuario_por_id.assert_called_once_with(1)

    def test_cargar_usuario_actual_no_encontrado(self):
        """Prueba que _cargar_usuario_actual devuelva None si el usuario no existe."""
        self.gestor_usuarios_mock.cargar_usuario_por_id.return_value = None

        resultado = self.gestor_login._cargar_usuario_actual(1)

        self.assertIsNone(resultado)
        self.gestor_usuarios_mock.cargar_usuario_por_id.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()
