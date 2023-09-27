# Archivo de test para realizar pruebas unitarias del modulo1
import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.cinta_transportadora import Cinta_Transportadora
from modules.cajon import Cajon

class TestAlimentos(unittest.TestCase):

    def test_kiwi_calcular_aw(self):
        kiwi = Kiwi(0.07)  # instanciamos un kiwi
        resultado_de_aw = kiwi.calcular_aw()
        self.assertAlmostEqual(resultado_de_aw, 0.5357, places=3) 

    def test_manzana_calcular_aw(self):
        manzana = Manzana(0.18)  # instanciamos una manzana
        resultado_de_aw = manzana.calcular_aw()
        self.assertAlmostEqual(resultado_de_aw, 0.853, places=3)

    def test_papa_calcular_aw(self):
        papa = Papa(0.15)  # instanciamos una papa
        resultado_de_aw = papa.calcular_aw()
        self.assertAlmostEqual(resultado_de_aw, 0.803, places=3) 

    def test_zanahoria_calcular_aw(self):
        zanahoria = Zanahoria(0.175)  # instanciamos una zanahoria
        resultado_de_aw = zanahoria.calcular_aw()
        self.assertAlmostEqual(resultado_de_aw, 0.793, places=3)  

class TestCintaTransportadora(unittest.TestCase):

    def test_clasificar_alimentos(self):
    
        cinta_transportadora = Cinta_Transportadora()
        n_alimentos = 5  
        lista_de_alimentos = cinta_transportadora.clasificar_alimentos(n_alimentos)

        self.assertEqual(len(lista_de_alimentos), n_alimentos)

        for alimento in lista_de_alimentos:
            
            self.assertTrue(isinstance(alimento, (Kiwi, Manzana, Papa, Zanahoria)))

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
    
        cajon_de_n_alimentos = Cajon(diccionario_aw)
    #def test_calcular_aw_prom(self)





if __name__ == '__main__':
    unittest.main()