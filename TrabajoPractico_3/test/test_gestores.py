import unittest
from unittest.mock import MagicMock, patch
from flask import Flask
from modules.config import db
from modules.dominio import Reclamo, Usuario
from modules.gestores import GestorReclamo, GestorUsuario, GestorBaseDeDatos

class TestGestores(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        cls.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(cls.app)

    def setUp(self):
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        # Mock para el repositorio y gestores
        self.repositorio_mock = MagicMock()
        self.gestor_reclamo = GestorReclamo(self.repositorio_mock)
        self.gestor_usuario = GestorUsuario(self.repositorio_mock)
        self.gestor_base_datos = GestorBaseDeDatos()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_crear_reclamo(self):
        lista_reclamo = ["1", "usuario_1", "contenido", "clasificacion", "estado", "2024-11-20", None]
        reclamo = self.gestor_reclamo.crear_reclamo(lista_reclamo)

        self.assertIsInstance(reclamo, Reclamo)
        self.assertEqual(reclamo.id_reclamo, "1")
        self.assertEqual(reclamo.contenido, "contenido")

    @patch("gestores.db.session")
    def test_guardar_reclamo(self, db_session_mock):
        datos = ["1", "1", "contenido", "clasificacion", "estado", "2024-11-20", None]
        self.gestor_reclamo.guardar_reclamo(datos)

        db_session_mock.add.assert_called_once()
        db_session_mock.commit.assert_called_once()

    def test_registrar_usuario(self):
        self.repositorio_mock.obtener_todos_los_registros.return_value = []
        usuario = self.gestor_usuario.registrar_usuario(
            id="1",
            nombre="John",
            apellido="Doe",
            nombre_usuario="johndoe",
            email="john@example.com",
            contraseña="password123",
            claustro="alumno",
            rol="user",
            departamento="IT"
        )

        self.assertEqual(usuario.nombre, "John")
        self.repositorio_mock.guardar_registro.assert_called_once()

    def test_existe_email(self):
        email = "john@example.com"
        self.repositorio_mock.obtener_usuario_por_email.return_value = None

        resultado = self.gestor_usuario.existe_email(email)
        self.assertFalse(resultado)

    @patch("gestores.db.session")
    def test_guardar_nuevo_objeto(self, db_session_mock):
        datos = ["John", "Doe", "johndoe", "john@example.com", "password123", "alumno", "user", "IT"]
        self.gestor_base_datos.guardar_nuevo_objeto("jefe", datos)

        db_session_mock.add.assert_called_once()
        db_session_mock.commit.assert_called_once()

    def test_guardar_nuevo_objeto_tipo_no_valido(self):
        datos = ["John", "Doe", "johndoe", "john@example.com", "password123", "alumno", "user", "IT"]
        with self.assertRaises(ValueError):
            self.gestor_base_datos.guardar_nuevo_objeto("empleado", datos)


if __name__ == "__main__":
    unittest.main()
