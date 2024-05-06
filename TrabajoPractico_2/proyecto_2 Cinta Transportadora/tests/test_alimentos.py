# Archivo de test para realizar pruebas unitarias del modulo1
import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria

class TestAlimentos(unittest.TestCase):

    def test_kiwi_calcular_aw(self):
        kiwi1 = Kiwi(0.07)  # instanciamos un kiwi
        
        resultado_de_aw = kiwi1.calcular_aw()
        self.assertAlmostEqual(resultado_de_aw, 0.5357, places=3) 

    def test_kiwi_excepciones(self):
        self.assertRaises(ValueError, Kiwi, -0.6)
        self.assertRaises(ValueError, Kiwi, 0.04)
        self.assertRaises(ValueError, Kiwi, 0.7)
        
    def test_manzana_calcular_aw(self):
        manzana = Manzana(0.18)  # instanciamos una manzana
        resultado_de_aw = manzana.calcular_aw()
        self.assertAlmostEqual(resultado_de_aw, 0.853, places=3)

    def test_manzana_excepciones(self):
        self.assertRaises(ValueError, Manzana, -0.6)
        self.assertRaises(ValueError, Manzana, 0.04)
        self.assertRaises(ValueError, Manzana, 0.7)

    def test_papa_calcular_aw(self):
        papa = Papa(0.15)  # instanciamos una papa
        resultado_de_aw = papa.calcular_aw()
        self.assertAlmostEqual(resultado_de_aw, 0.803, places=3)

    def test_papa_excepciones(self):
        self.assertRaises(ValueError, Papa, -0.6) 
        self.assertRaises(ValueError, Papa, 0.04)
        self.assertRaises(ValueError, Papa, 0.7)
        
    def test_zanahoria_calcular_aw(self):
        zanahoria = Zanahoria(0.175)  # instanciamos una zanahoria
        resultado_de_aw = zanahoria.calcular_aw()
        self.assertAlmostEqual(resultado_de_aw, 0.793, places=3) 
        
    def test_zanahoria_excepciones(self): 
        self.assertRaises(ValueError, Zanahoria, -0.6)
        self.assertRaises(ValueError, Zanahoria, 0.04)
        self.assertRaises(ValueError, Zanahoria, 0.7)

if __name__ == '__main__':
    unittest.main()



