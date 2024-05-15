import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria, Fruta, Verdura, Alimentos
from modules.calculador import calcular_aw_promedio, calcular_peso, calcular_aw
from modules.cajon import Cajon

class TestCalculador(unittest.TestCase):
    
    def setUp(self): #Para evitar repetir muchas veces los datos y que disminuya el cover
        self.kiwi = Kiwi(0.07)
        self.manzana = Manzana(0.18)
        self.papa = Papa(0.15)
        self.zanahoria = Zanahoria(0.175)

        self.cajon = Cajon()
        self.cajon.agregar_alimento(self.kiwi)
        self.cajon.agregar_alimento(self.manzana)
        self.cajon.agregar_alimento(self.papa)
        self.cajon.agregar_alimento(self.zanahoria)

    def test_calcular_aw(self):
        
        awk = calcular_aw(self.kiwi)
        awm = calcular_aw(self.manzana)
        awp = calcular_aw(self.papa)
        awz = calcular_aw(self.zanahoria)

        self.assertAlmostEqual(awk, 0.5357, places=3) 
        self.assertAlmostEqual(awm, 0.853, places=3)
        self.assertAlmostEqual(awp, 0.803, places=3)
        self.assertAlmostEqual(awz, 0.793, places=3) 

    def test_calcular_aw_promedio(self):
        
        aw_frutas = round(calcular_aw_promedio(Fruta, self.cajon), 2)
        aw_verduras = round(calcular_aw_promedio(Verdura, self.cajon), 2)
        aw_total = round(calcular_aw_promedio(Alimentos, self.cajon), 2)

        self.assertAlmostEqual(aw_frutas, 0.69, places=2)
        self.assertAlmostEqual(aw_verduras, 0.80, places=2)
        self.assertAlmostEqual(aw_total, 0.75, places=2)

    def test_calcular_peso(self):
       
        resultado = calcular_peso(self.cajon)
        self.assertAlmostEqual(resultado, 0.575, places=2)

if __name__ == '__main__':
    unittest.main()