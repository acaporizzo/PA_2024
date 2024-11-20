import unittest
from unittest.mock import MagicMock
from modules.dominio import Reclamo, Usuario
from modules.modelos import ModeloReclamo, ModeloUsuario
from modules.repositorio_abstracto import RepositorioAbstracto
from modules.repositorio_concreto import RepositorioReclamosSQLAlchemy, RepositorioUsuariosSQLAlchemy


class TestRepositorioReclamosSQLAlchemy(unittest.TestCase):
    def setUp(self):
        # Mock de la sesión de SQLAlchemy
        self.session = MagicMock()
        self.repositorio = RepositorioReclamosSQLAlchemy(self.session)

    def test_guardar_registro(self):
        # Crear un objeto Reclamo
        reclamo = Reclamo(
            id_reclamo="1",
            id_usuario="user_1",
            contenido="contenido del reclamo",
            clasificacion="general",
            estado="pendiente",
            imagen=None,
            fecha_hora="2024-11-20"
        )

        # Llamar a guardar_registro
        self.repositorio.guardar_registro(reclamo)

        # Verificar que se haya llamado a session.add y session.commit
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()

    def test_guardar_registro_error_tipo(self):
        # Probar que se lanza un error si el objeto no es de tipo Reclamo
        with self.assertRaises(ValueError):
            self.repositorio.guardar_registro("no es un reclamo")

    def test_obtener_todos_los_registros(self):
        # Mock de los resultados de la consulta
        mock_reclamo = ModeloReclamo(
            id="1",
            id_usuario="user_1",
            contenido="contenido del reclamo",
            clasificacion="general",
            estado="pendiente",
            imagen=None,
            fecha="2024-11-20"
        )
        self.session.query.return_value.all.return_value = [mock_reclamo]

        # Llamar al método
        resultados = self.repositorio.obtener_todos_los_registros()

        # Verificar que el resultado sea una lista de Reclamos
        self.assertEqual(len(resultados), 1)
        self.assertIsInstance(resultados[0], Reclamo)
        self.assertEqual(resultados[0].contenido, "contenido del reclamo")

    def test_obtener_reclamos_de_usuario(self):
        # Mock de los resultados de la consulta
        usuario_mock = MagicMock()  # Simula un usuario con reclamos adheridos
        mock_reclamo = ModeloReclamo(
            id="1",
            id_usuario="user_1",
            contenido="contenido del reclamo",
            clasificacion="general",
            estado="pendiente",
            imagen=None,
            fecha="2024-11-20"
        )
        self.session.query.return_value.filter.return_value.all.return_value = [mock_reclamo]

        # Llamar al método
        resultados = self.repositorio.obtener_reclamos_de_usuario(usuario_mock)

        # Verificar resultados
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].id, "1")


class TestRepositorioUsuariosSQLAlchemy(unittest.TestCase):
    def setUp(self):
        # Mock de la sesión de SQLAlchemy
        self.session = MagicMock()
        self.repositorio = RepositorioUsuariosSQLAlchemy(self.session)

    def test_guardar_registro(self):
        # Crear un objeto Usuario
        usuario = Usuario(
            id="1",
            nombre="John",
            apellido="Doe",
            email="john@example.com",
            nombre_usuario="johndoe",
            contraseña="hashed_password",
            claustro="PAyS",
            rol="Jefe de Departamento",
            departamento="IT"
        )

        # Llamar a guardar_registro
        self.repositorio.guardar_registro(usuario)

        # Verificar que se haya llamado a session.add y session.commit
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()

    def test_obtener_usuario_por_nombre(self):
        # Mock de un resultado de la consulta
        mock_usuario = ModeloUsuario(
            id="1",
            nombre="John",
            apellido="Doe",
            email="john@example.com",
            nombre_usuario="johndoe",
            contraseña="hashed_password",
            claustro="PAyS",
            rol="Jefe de Departamento",
            departamento="IT"
        )
        self.session.query.return_value.filter_by.return_value.first.return_value = mock_usuario

        # Llamar al método
        resultado = self.repositorio.obtener_usuario_por_nombre("johndoe")

        # Verificar que el resultado sea un objeto Usuario
        self.assertIsInstance(resultado, Usuario)
        self.assertEqual(resultado.nombre_usuario, "johndoe")

    def test_obtener_usuario_por_id(self):
        # Mock de un resultado de la consulta
        mock_usuario = ModeloUsuario(
            id="1",
            nombre="John",
            apellido="Doe",
            email="john@example.com",
            nombre_usuario="johndoe",
            contraseña="hashed_password",
            claustro="PAyS",
            rol="Jefe de Departamento",
            departamento="IT"
        )
        self.session.query.return_value.filter_by.return_value.first.return_value = mock_usuario

        # Llamar al método
        resultado = self.repositorio.obtener_usuario_por_id("1")

        # Verificar que el resultado sea un objeto Usuario
        self.assertIsInstance(resultado, Usuario)
        self.assertEqual(resultado.id, "1")


if __name__ == "__main__":
    unittest.main()
