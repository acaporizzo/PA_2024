import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.cajon import Cajon
from modules.cinta_transportadora import Cinta_Transportadora


class TestCintaTransportadora(unittest.TestCase):

    def test_clasificar_alimento(self):
        n_alimentos = 8
        # Crea una Cinta_Transportadora
        cinta = Cinta_Transportadora()
        cajon=Cajon()
        while len(cajon) <= n_alimentos:
            alimento = cinta.clasificar_alimento()
            cajon.agregar_alimento(alimento)
        # Para cada alimento en la lista, llama a clasificar_alimento y verifica el tipo y el peso del alimento devuelto
        for alimento in cajon:
            if alimento != "undifined":

                if isinstance(alimento, Kiwi):
                    # Verifica que el alimento sea un Kiwi
                    self.assertIsInstance(alimento, Kiwi, "El alimento no es un Kiwi")
            
                elif isinstance(alimento, Manzana):
                    # Verifica que el alimento sea una Manzana
                    self.assertIsInstance(alimento, Manzana, "El alimento no es una Manzana")
    
                elif isinstance(alimento, Papa):
                    # Verifica que el alimento sea una Papa
                    self.assertIsInstance(alimento, Papa, "El alimento no es una Papa")
                   
                elif isinstance(alimento, Zanahoria):
                    # Verifica que el alimento sea una Zanahoria
                    self.assertIsInstance(alimento, Zanahoria, "El alimento no es una Zanahoria")
                    
            else:
                # Si el alimento es None, la prueba falla
                self.fail("El alimento es None")

if __name__ == '__main__':
    unittest.main()