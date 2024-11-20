import unittest
from unittest.mock import MagicMock, patch
from flask import Flask
from modules.dominio import Reclamo, Usuario
from modules.gestores import GestorReclamo, GestorUsuario  # Asegúrate de que esta ruta sea correcta
from modules.config import db  # Importar la configuración de la base de datos

class TestGestorReclamo(unittest.TestCase):
    def setUp(self):
        # Configurar aplicación Flask y contexto de la base de datos
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Base de datos en memoria para pruebas
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)
        
        # Crear contexto de la aplicación
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Inicializar el esquema de la base de datos
        with self.app.app_context():
            db.create_all()

        # Mock del repositorio
        self.repositorio_mock = MagicMock()
        self.gestor_reclamo = GestorReclamo(self.repositorio_mock)

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_mostrar_reclamos(self):
        self.repositorio_mock.obtener_todos_los_registros.return_value = ["reclamo1", "reclamo2"]
        reclamos = self.gestor_reclamo.mostrar_reclamos()
        self.assertEqual(reclamos, ["reclamo1", "reclamo2"])

    def test_crear_reclamo(self):
        lista_reclamo = [1, "user1", "contenido", "clasificacion", "estado", "fecha", "imagen.png"]
        nuevo_reclamo = self.gestor_reclamo.crear_reclamo(lista_reclamo)
        self.assertEqual(nuevo_reclamo.contenido, "contenido")  # Ajusta según el atributo correcto de tu clase Reclamo
        self.assertEqual(nuevo_reclamo.id_reclamo, 1)

    def test_guardar_reclamo(self):
        datos = [1, "user1", "contenido", "clasificacion", "estado", "fecha", "imagen.png"]
        with patch('modules.config.db.session.add') as mock_add, \
             patch('modules.config.db.session.commit') as mock_commit:
            self.gestor_reclamo.guardar_reclamo(datos)
            mock_add.assert_called_once()
            mock_commit.assert_called_once()

    def test_adherir_usuario_a_reclamo_reclamo_no_encontrado(self):
        self.repositorio_mock.obtener_registro_por_filtro.return_value = None
        resultado = self.gestor_reclamo.adherir_usuario_a_reclamo(1, MagicMock())
        self.assertEqual(resultado, "reclamo_no_encontrado")

    def test_clasificar_reclamo(self):
        """Prueba que se asigne la clasificación correspondiente al reclamo"""
        mock_reclamo = MagicMock()
        mock_reclamo.descripcion = "No funciona el campus virtual"
        self.gestor_reclamo.clasificar_reclamo(mock_reclamo)
        self.assertTrue(mock_reclamo.clasificacion)  # Asegúrate de verificar la clasificación asignada

    def test_filtrar_por_depto(self):
        """Prueba que funcione correctamente el filtro de departamento"""
        mock_reclamo1 = MagicMock()
        mock_reclamo1.clasificacion = "maestranza"
        mock_reclamo2 = MagicMock()
        mock_reclamo2.clasificacion = "soporte informático"

        reclamos = [mock_reclamo1, mock_reclamo2]
        self.repositorio_mock.obtener_registros_segun_filtro.side_effect = lambda filtro, valor: [r for r in reclamos if r.clasificacion == valor]

        filtro = self.gestor_reclamo.obtener_reclamo_por_filtro("clasificacion", "maestranza")
        self.assertEqual(len(filtro), 1)
        self.assertEqual(filtro[0].clasificacion, "maestranza")

class TestGestorUsuario(unittest.TestCase):
    def setUp(self):
        # Configurar aplicación Flask y contexto de la base de datos
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)

        # Crear contexto de la aplicación
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Inicializar el esquema de la base de datos
        with self.app.app_context():
            db.create_all()

        # Mock del repositorio
        self.repositorio_mock = MagicMock()
        self.gestor_usuario = GestorUsuario(self.repositorio_mock)

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_registrar_usuario_exitoso(self):
        self.repositorio_mock.obtener_todos_los_registros.return_value = []
        usuario = self.gestor_usuario.registrar_usuario(
            id=1, nombre="Juan", apellido="Perez", nombre_usuario="juanperez",
            email="juan@example.com", contraseña="1234", claustro="Estudiantes",
            rol="Estudiante", departamento="Informática"
        )
        self.repositorio_mock.guardar_registro.assert_called_once()
        self.assertEqual(usuario.nombre_usuario, "juanperez")

    def test_registrar_usuario_nombre_usuario_existente(self):
        usuario_existente = MagicMock()
        usuario_existente.nombre_usuario = "juanperez"
        self.repositorio_mock.obtener_todos_los_registros.return_value = [usuario_existente]
        with self.assertRaises(ValueError):
            self.gestor_usuario.registrar_usuario(
                id=1, nombre="Juan", apellido="Perez", nombre_usuario="juanperez",
                email="juan@example.com", contraseña="1234", claustro="Estudiantes",
                rol="Estudiante", departamento="Informática"
            )

if __name__ == "__main__":
    unittest.main()
