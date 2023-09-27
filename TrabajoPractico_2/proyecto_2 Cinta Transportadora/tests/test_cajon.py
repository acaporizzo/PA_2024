import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.cajon import Cajon

class TestCajon (unittest.TestCase):

    def test_agregar_y_calcular_aw (self):

        alimentos = [
            Kiwi(0.07),
            Manzana(0.18),
            Papa(0.15),
            Zanahoria(0.175),
        ]    
        cajon_de_n_alimentos = Cajon(alimentos)
        diccionario_con_listas_aw = cajon_de_n_alimentos.agregar_y_calcular_aw(alimentos)

        self.assertTrue('Kiwi' in diccionario_con_listas_aw)
        self.assertTrue('Manzana' in diccionario_con_listas_aw)
        self.assertTrue('Papa' in diccionario_con_listas_aw)
        self.assertTrue('Zanahoria' in diccionario_con_listas_aw)

    def test_calcular_aw_prom_diccionario(self):

        diccionario_aw = {
            'Kiwi': [0.9, 0.85, 0.92],
            'Manzana': [0.88, 0.91, 0.87],
            'Papa': [0.78, 0.82],
            'Zanahoria': [0.75, 0.79, 0.77],
        }

        cajon = Cajon(diccionario_aw)
        promedios = cajon.calcular_aw_prom_diccionario(diccionario_aw)

        self.assertAlmostEqual(promedios['Kiwi'], 0.89, places=2)
        self.assertAlmostEqual(promedios['Manzana'], 0.89, places=2)
        self.assertAlmostEqual(promedios['Papa'], 0.80, places=2)
        self.assertAlmostEqual(promedios['Zanahoria'], 0.77, places=2)

    def test_calcular_aw_prom(self):

        lista_awf = [0.9, 0.85, 0.92, 0.88, 0.91, 0.87]
        lista_awv= [0.78, 0.82, 0.75, 0.79, 0.77]
        lista_awt=[0.9, 0.85, 0.92, 0.88, 0.91, 0.87, 0.78, 0.82, 0.75, 0.79, 0.77]

        cajonf = Cajon(lista_awf)
        cajonv = Cajon(lista_awv)
        cajont = Cajon(lista_awt)

        awf= cajonf.calcular_aw_prom(lista_awf)
        awv= cajonv.calcular_aw_prom(lista_awv)
        awt= cajont.calcular_aw_prom(lista_awt)

        self.assertAlmostEqual(awf, 0.89, places=2)
        self.assertAlmostEqual(awv, 0.78, places=2)
        self.assertAlmostEqual(awt, 0.84, places=2)

if __name__ == '__main__':
    unittest.main()