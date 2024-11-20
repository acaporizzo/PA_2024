import unittest
from unittest.mock import MagicMock, patch
from flask import Flask
from flask_login import LoginManager, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash
from modules.gestor_login import FlaskLoginUser, GestorLogin  # Reemplaza 'your_module' con el nombre de tu archivo

class MockUsuario:
    def __init__(self, id, nombre, email, contraseña, departamento):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.contraseña = generate_password_hash(contraseña)  # Contraseña encriptada
        self.departamento = departamento

class TestGestorLogin(unittest.TestCase):
    def setUp(self):
        # Configuración del entorno de Flask
        self.app = Flask(__name__)
        self.app.secret_key = 'test_secret_key'
        self.login_manager = LoginManager(self.app)

        # Usuario de prueba
        self.mock_usuario = MockUsuario(
            id=1,
            nombre="Juan",
            email="juan@example.com",
            contraseña="password123",
            departamento="Informática"
        )

        # Mock del gestor de usuarios
        self.mock_gestor_usuarios = MagicMock()
        self.mock_gestor_usuarios.cargar_usuario_por_nombre.return_value = self.mock_usuario
        self.mock_gestor_usuarios.cargar_usuario_por_id.return_value = self.mock_usuario

        self.gestor_login = GestorLogin(self.mock_gestor_usuarios, self.login_manager, admin_list=["admin"])

        # Crear contexto de prueba de Flask
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_verificar_credenciales_correctas(self):
        usuario = self.gestor_login.verificar_credenciales("Juan", "password123")
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.nombre, "Juan")

    def test_verificar_credenciales_incorrectas(self):
        usuario = self.gestor_login.verificar_credenciales("Juan", "wrongpassword")
        self.assertIsNone(usuario)

    #def test_login_usuario(self):
    #    with self.app.test_request_context():  # Contexto de solicitud
    #        with patch('flask_login.login_user') as mock_login_user:
    #            self.gestor_login.login_usuario(self.mock_usuario)
    #            mock_login_user.assert_called_once()

    #def test_logout_usuario(self):
    #    with self.app.test_request_context():  # Contexto de solicitud
    #        with patch('flask_login.logout_user') as mock_logout_user:
    #           self.gestor_login.logout_usuario()
    #           mock_logout_user.assert_called_once()

    def test_nombre_usuario_actual(self):
        with self.app.test_request_context():  # Contexto de solicitud
            login_user(FlaskLoginUser(self.mock_usuario))
            self.assertEqual(self.gestor_login.nombre_usuario_actual, "Juan")

    def test_id_usuario_actual(self):
        with self.app.test_request_context():  # Contexto de solicitud
            login_user(FlaskLoginUser(self.mock_usuario))
            self.assertEqual(self.gestor_login.id_usuario_actual, 1)

    def test_usuario_autenticado(self):
        with self.app.test_request_context():  # Contexto de solicitud
            login_user(FlaskLoginUser(self.mock_usuario))
            self.assertTrue(self.gestor_login.usuario_autenticado)

if __name__ == "__main__":
    unittest.main()
