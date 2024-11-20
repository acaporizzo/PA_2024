import unittest
from unittest.mock import MagicMock
from modules.dominio import Reclamo, Usuario
from modules.repositorio_concreto import RepositorioReclamosSQLAlchemy, RepositorioUsuariosSQLAlchemy

class TestRepositorioReclamosSQLAlchemy(unittest.TestCase):
    def setUp(self):
        self.session_mock = MagicMock()
        self.repositorio = RepositorioReclamosSQLAlchemy(self.session_mock)

    def test_guardar_registro_exitoso(self):
        reclamo = Reclamo(1, "usuario1", "contenido", "clasificacion", "pendiente", "2024-01-01", usuarios_adheridos=[])
        self.repositorio.guardar_registro(reclamo)
        self.session_mock.add.assert_called_once()
        self.session_mock.commit.assert_called_once()

    def test_insertar_reclamo_exitoso(self):
        reclamo = Reclamo(1, "usuario1", "contenido", "clasificacion", "pendiente", "2024-01-01", usuarios_adheridos=[])
        self.repositorio.insertar_reclamo(reclamo)
        self.session_mock.add.assert_called_once()
        self.session_mock.commit.assert_called_once()

    def test_modificar_registro_exitoso(self):
        reclamo_modificado = Reclamo(1, "usuario1", "nuevo contenido", "nueva clasificacion", "completado", "2024-01-02", usuarios_adheridos=[])
        mock_reclamo = MagicMock()
        self.session_mock.query.return_value.filter_by.return_value.first.return_value = mock_reclamo
        self.repositorio.modificar_registro(reclamo_modificado)
        self.session_mock.commit.assert_called_once()

class TestRepositorioUsuariosSQLAlchemy(unittest.TestCase):
    def setUp(self):
        self.session_mock = MagicMock()
        self.repositorio = RepositorioUsuariosSQLAlchemy(self.session_mock)

    def test_guardar_registro_exitoso(self):
        usuario = Usuario(1, "Juan", "Perez", "juanperez", "juan@example.com", "1234", "Estudiantes", "Estudiante", "Informática")
        self.repositorio.guardar_registro(usuario)
        self.session_mock.add.assert_called_once()
        self.session_mock.commit.assert_called_once()

    def test_guardar_registro_valor_invalido(self):
        with self.assertRaises(ValueError):
            self.repositorio.guardar_registro("no_es_usuario")

    def test_modificar_registro_exitoso(self):
        usuario_modificado = Usuario(1, "Juan", "Ramirez", "juanperez", "juan@example.com", "5678", "Estudiantes", "Estudiante", "Informática")
        mock_usuario = MagicMock()
        self.session_mock.query.return_value.filter_by.return_value.first.return_value = mock_usuario
        self.repositorio.modificar_registro(usuario_modificado)
        self.session_mock.commit.assert_called_once()

if __name__ == "__main__":
    unittest.main()
