import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria, Fruta, Verdura, Alimentos
from modules.calculador import calcular_aw_promedio, calcular_peso
from modules.cajon import Cajon

class TestCalculador(unittest.TestCase):
    
    def setUp(self):  # setup para evitar repetir datos
        self.kiwi = Kiwi(0.07)
        self.manzana = Manzana(0.18)
        self.papa = Papa(0.15)
        self.zanahoria = Zanahoria(0.175)

        self.cajon = Cajon()
        self.cajon.agregar_alimento(self.kiwi)
        self.cajon.agregar_alimento(self.manzana)
        self.cajon.agregar_alimento(self.papa)
        self.cajon.agregar_alimento(self.zanahoria)

    def test_calcular_aw_promedio(self):
        aw_frutas = round(calcular_aw_promedio(Fruta, self.cajon), 2)
        aw_verduras = round(calcular_aw_promedio(Verdura, self.cajon), 2)
        aw_total = round(calcular_aw_promedio(Alimentos, self.cajon), 2)

        self.assertAlmostEqual(aw_frutas, 0.69, places=2)
        self.assertAlmostEqual(aw_verduras, 0.80, places=2)
        self.assertAlmostEqual(aw_total, 0.75, places=2)

    def test_calcular_aw_promedio_excepciones(self):
        cajon_vacio = Cajon()
        aw_prom=calcular_aw_promedio(Fruta, cajon_vacio)
        self.assertEqual(aw_prom, 0)

    def test_calcular_peso(self):
        resultado = calcular_peso(self.cajon)
        self.assertAlmostEqual(resultado, 0.575, places=2)

    def test_calcular_peso_excepciones(self):
        cajon_vacio = Cajon()
        peso=calcular_peso(cajon_vacio)
        self.assertEqual(peso, 0)
            

    def test_calcular_aw_promedio_diferentes_combinaciones(self):
        # caso 1: solo frutas
        cajon_frutas = Cajon()
        cajon_frutas.agregar_alimento(Kiwi(0.07))
        cajon_frutas.agregar_alimento(Manzana(0.18))
        aw_frutas = round(calcular_aw_promedio(Fruta, cajon_frutas), 2)
        self.assertAlmostEqual(aw_frutas, 0.69, places=2)  # Ajusta según el valor esperado

        # caso 2: solo verduras
        cajon_verduras = Cajon()
        cajon_verduras.agregar_alimento(Papa(0.15))
        cajon_verduras.agregar_alimento(Zanahoria(0.175))
        aw_verduras = round(calcular_aw_promedio(Verdura, cajon_verduras), 2)
        self.assertAlmostEqual(aw_verduras, 0.80, places=2)  # Ajusta según el valor esperado

if __name__ == '__main__':
    unittest.main()