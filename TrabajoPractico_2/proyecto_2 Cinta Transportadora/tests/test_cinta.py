import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.cinta_transportadora import Cinta_Transportadora

class TestCintaTransportadora(unittest.TestCase):

    def test_clasificar_alimento(self):
        # Crea una lista de alimentos
        alimentos = [{'alimento': 'kiwi', 'peso': 0.1}, {'alimento': 'manzana', 'peso': 0.2}, 
                     {'alimento': 'papa', 'peso': 0.3}, {'alimento': 'zanahoria', 'peso': 0.4},
                     {'alimento': 'kiwi', 'peso': 0.5}, {'alimento': 'manzana', 'peso': 0.5},
                     {'alimento': 'papa', 'peso': 0.5}, {'alimento': 'zanahoria', 'peso': 0.5},
                     {'alimento': 'kiwi', 'peso': 0.09}, {'alimento': 'manzana', 'peso': 0.08}]

        # Crea una Cinta_Transportadora
        cinta = Cinta_Transportadora()

        # Para cada alimento en la lista, llama a clasificar_alimento y verifica el tipo y el peso del alimento devuelto
        for alimento in alimentos:
            alimento_clasificado = cinta.clasificar_alimento()
            self.assertEqual(alimento_clasificado.__class__.__name__, alimento['alimento'].capitalize())
            self.assertEqual(alimento_clasificado.peso_del_alimento, alimento['peso'])


if __name__ == '__main__':
    unittest.main()