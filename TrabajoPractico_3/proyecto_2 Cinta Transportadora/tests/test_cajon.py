import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.cajon import Cajon
from modules.cinta_transportadora import Cinta_Transportadora
from modules.calculador_aw import calcular_aw_promedio

class TestCajon(unittest.TestCase):

    def test_agregar_alimento(self): # Prueba para el método calcular_aw_promedios

        cinta=Cinta_Transportadora()
        alimento1=cinta.clasificar_alimento()
        alimento2=cinta.clasificar_alimento()
        cajon=Cajon()
        while cajon.contar_alimentos() < 1000:
            alimento = cinta.clasificar_alimento()
            if alimento != None:
                cajon.agregar_alimento(alimento)    
        for alimento in cajon:
            self.assertTrue(isinstance(alimento, (Kiwi, Manzana, Papa, Zanahoria)))


    def contar_alimentos(self):
        cinta=Cinta_Transportadora()
        alimento1=cinta.clasificar_alimento()
        alimento2=cinta.clasificar_alimento()
        cajon=Cajon()
        cajon.agregar_alimento(alimento1)
        cajon.agregar_alimento(alimento2)
        contador=cajon.contar_alimentos()
        self.assertEqual(contador,2)

if __name__ == '__main__':
    unittest.main()
