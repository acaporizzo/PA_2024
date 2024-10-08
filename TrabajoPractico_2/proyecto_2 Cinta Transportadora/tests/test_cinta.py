import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.cajon import Cajon
from modules.cinta_transportadora import Cinta_Transportadora

class TestCintaTransportadora(unittest.TestCase):

    def test_clasificar_alimento(self):
        n_alimentos = 8
        cinta = Cinta_Transportadora()
        cajon=Cajon()
        while len(cajon) <= n_alimentos:
            alimento = cinta.clasificar_alimento()
            cajon.agregar_alimento(alimento)
        # para cada alimento, llama a clasificar_alimento y verifica el tipo y el peso del alimento
        for alimento in cajon:
            if alimento != "undefined":

                if isinstance(alimento, Kiwi):
                    self.assertIsInstance(alimento, Kiwi, "El alimento no es un Kiwi")
            
                elif isinstance(alimento, Manzana):
                    self.assertIsInstance(alimento, Manzana, "El alimento no es una Manzana")
    
                elif isinstance(alimento, Papa):
                    self.assertIsInstance(alimento, Papa, "El alimento no es una Papa")
                   
                elif isinstance(alimento, Zanahoria):
                    self.assertIsInstance(alimento, Zanahoria, "El alimento no es una Zanahoria")
                    
            else:
                self.fail("El alimento es None")

if __name__ == '__main__':
    unittest.main()