# Archivo de test para realizar pruebas unitarias del modulo1
import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria

class TestAlimentos(unittest.TestCase):

    def test_kiwi_excepciones(self):
        self.assertRaises(ValueError, Kiwi, -0.6)
        self.assertRaises(ValueError, Kiwi, 0.04)
        self.assertRaises(ValueError, Kiwi, 0.7)

    def test_manzana_excepciones(self):
        self.assertRaises(ValueError, Manzana, -0.6)
        self.assertRaises(ValueError, Manzana, 0.04)
        self.assertRaises(ValueError, Manzana, 0.7)

    def test_papa_excepciones(self):
        self.assertRaises(ValueError, Papa, -0.6) 
        self.assertRaises(ValueError, Papa, 0.04)
        self.assertRaises(ValueError, Papa, 0.7)
        
    def test_zanahoria_excepciones(self): 
        self.assertRaises(ValueError, Zanahoria, -0.6)
        self.assertRaises(ValueError, Zanahoria, 0.04)
        self.assertRaises(ValueError, Zanahoria, 0.7)

if __name__ == '__main__':
    unittest.main()



