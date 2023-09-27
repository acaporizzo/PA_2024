import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.cinta_transportadora import Cinta_Transportadora

class TestCintaTransportadora(unittest.TestCase):

    def test_clasificar_alimentos(self):
    
        cinta_transportadora = Cinta_Transportadora()
        n_alimentos = 1000  
        lista_de_alimentos = cinta_transportadora.clasificar_alimentos(n_alimentos)

        self.assertEqual(len(lista_de_alimentos), n_alimentos)

        for alimento in lista_de_alimentos:
            
            self.assertTrue(isinstance(alimento, (Kiwi, Manzana, Papa, Zanahoria)))

if __name__ == '__main__':
    unittest.main()