# Archivo de test para realizar pruebas unitarias del modulo1
import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.cinta_transportadora import clasificar_alimentos
from modules.cajon import agregar_y_calcular_aw, calcular_aw_prom_diccionario, calcular_aw_prom

class TestAlimentos(unittest.TestCase):

    def test_kiwi_calcular_aw(self):
        kiwi = Kiwi(0.1)  # Peso del kiwi
        result = kiwi.calcular_aw()
        self.assertAlmostEqual(result, 0.3902285416, delta=1e-6)  # Ajusta el valor esperado según tu implementación

    def test_manzana_calcular_aw(self):
        manzana = Manzana(0.2)  # Peso de la manzana
        result = manzana.calcular_aw()
        self.assertAlmostEqual(result, 0.3548387096, delta=1e-6)  # Ajusta el valor esperado según tu implementación

    def test_papa_calcular_aw(self):
        papa = Papa(0.3)  # Peso de la papa
        result = papa.calcular_aw()
        self.assertAlmostEqual(result, 0.5396284552, delta=1e-6)  # Ajusta el valor esperado según tu implementación

    def test_zanahoria_calcular_aw(self):
        zanahoria = Zanahoria(0.4)  # Peso de la zanahoria
        result = zanahoria.calcular_aw()
        self.assertAlmostEqual(result, 0.783473703, delta=1e-6)  # Ajusta el valor esperado según tu implementación

if __name__ == '__main__':
    unittest.main()
    
class Test_ClasificarAlimentos(unittest.TestCase):


class Test_Agregar_y_Calcular_aw(unittest.TestCase):


class Test_Calcular_aw_Prom_Diccionario(unittest.TestCase):


class Test_Calcular_aw_prom(unittest.TestCase):

