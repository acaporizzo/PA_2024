import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.cajon import Cajon

class TestCajon(unittest.TestCase):

    def test_calcular_aw_promedios(self): # Prueba para el método calcular_aw_promedios

        alimentos = [
            Kiwi(0.07),
            Manzana(0.18),
            Papa(0.15),
            Zanahoria(0.175),
        ]    
        cajon_de_alimentos = Cajon(alimentos)
        aw_promedios = cajon_de_alimentos.calcular_aw_promedios()

        # Verificar que los promedios sean correctos
        self.assertAlmostEqual(aw_promedios[0], 0.54, places=2) # Promedio de Kiwi
        self.assertAlmostEqual(aw_promedios[1], 0.85, places=2) # Promedio de Manzana
        self.assertAlmostEqual(aw_promedios[2], 0.80, places=2) # Promedio de Papa
        self.assertAlmostEqual(aw_promedios[3], 0.79, places=2) # Promedio de Zanahoria
        self.assertAlmostEqual(aw_promedios[4], 0.69, places=2) # Promedio de Frutas: Kiwi y Manzana
        self.assertAlmostEqual(aw_promedios[5], 0.80, places=2) # Promedio de Verduras: Papa y Zanahoria
        self.assertAlmostEqual(aw_promedios[6], 0.75, places=2) # Promedio Total: de todos los alimentos

if __name__ == '__main__':
    unittest.main()
