import unittest
from datetime import datetime
from modules.dominio import Reclamo, Usuario

class TestUsuario(unittest.TestCase):
    def setUp(self):
        self.usuario = Usuario(
            id=1,
            nombre="Juan",
            apellido="Perez",
            nombre_usuario="juanperez",
            email="juan@example.com",
            contraseña="1234",
            claustro="Estudiantes",
            rol="Estudiante",
            departamento="Informática"
        )

    def test_usuario_atributos(self):
        self.assertEqual(self.usuario.id, 1)
        self.assertEqual(self.usuario.nombre, "Juan")
        self.assertEqual(self.usuario.apellido, "Perez")
        self.assertEqual(self.usuario.nombre_usuario, "juanperez")
        self.assertEqual(self.usuario.email, "juan@example.com")
        self.assertEqual(self.usuario.contraseña, "1234")
        self.assertEqual(self.usuario.claustro, "Estudiantes")
        self.assertEqual(self.usuario.rol, "Estudiante")
        self.assertEqual(self.usuario.departamento, "Informática")

    #def test_agregar_reclamo_adherido(self):
    #    self.assertEqual(len(self.usuario.reclamos_adheridos), 0)
    #    self.usuario.agregar_reclamo_adherido(1001)
    #    self.assertIn(1001, self.usuario.reclamos_adheridos)
    #    self.assertEqual(len(self.usuario.reclamos_adheridos), 1)

class TestReclamo(unittest.TestCase):
    def setUp(self):
        self.usuario = Usuario(
            id=1,
            nombre="Juan",
            apellido="Perez",
            nombre_usuario="juanperez",
            email="juan@example.com",
            contraseña="1234",
            claustro="Estudiantes",
            rol="Estudiante",
            departamento="Informática"
        )
        self.reclamo = Reclamo(
            id_reclamo=2001,
            usuario=self.usuario,
            contenido="Reclamo por falta de materiales",
            clasificacion="Materiales",
            estado="pendiente",
            fecha_hora=datetime.now()
        )

    def test_reclamo_atributos(self):
        self.assertEqual(self.reclamo.id_reclamo, 2001)
        self.assertEqual(self.reclamo.id_usuario, self.usuario)
        self.assertEqual(self.reclamo.contenido, "Reclamo por falta de materiales")
        self.assertEqual(self.reclamo.clasificacion, "Materiales")
        self.assertEqual(self.reclamo.estado, "pendiente")

    #def test_agregar_usuario_adherido(self):
    #    self.assertEqual(len(self.reclamo.usuarios_adheridos), 0)
    #    self.reclamo.agregar_usuario_adherido(1)
    #    self.assertIn(1, self.reclamo.usuarios_adheridos)
    #    self.assertEqual(len(self.reclamo.usuarios_adheridos), 1)

    def test_cargar_imagen(self):
        self.assertIsNone(self.reclamo.imagen)
        self.reclamo.cargar_imagen("imagen.png")
        self.assertEqual(self.reclamo.imagen, "imagen.png")

if __name__ == "__main__":
    unittest.main()
