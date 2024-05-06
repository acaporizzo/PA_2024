import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria, Fruta, Verdura, Alimentos
from modules.calculador import calcular_aw_promedio, calcular_peso
from modules.cajon import Cajon

class TestCalculador(unittest.TestCase):

    def test_calcular_aw_promedio(self):
        
        kiwi = Kiwi(0.07)  # instanciamos un kiwi
        manzana = Manzana(0.18)  # instanciamos una manzana
        papa = Papa(0.15)  # instanciamos una papa
        zanahoria = Zanahoria(0.175)  # instanciamos una zanahoria

        cajon = Cajon()

        # Agrega alimentos al cajón
        cajon.agregar_alimento(kiwi)
        cajon.agregar_alimento(manzana)
        cajon.agregar_alimento(papa)
        cajon.agregar_alimento(zanahoria)

        # Prueba calcular_aw_promedio para el tipo de alimento Kiwi
        aw_frutas = round(calcular_aw_promedio(Fruta,cajon),2)
        aw_verduras = round(calcular_aw_promedio(Verdura,cajon),2)
        aw_total = round(calcular_aw_promedio(Alimentos,cajon),2)
        self.assertAlmostEqual(aw_frutas, 0.69, places=2)
        self.assertAlmostEqual(aw_verduras, 0.80, places=2)
        self.assertAlmostEqual(aw_total, 0.75, places=2)

    def test_calcular_peso(self):
        
        kiwi = Kiwi(0.07)  # instanciamos un kiwi
        manzana = Manzana(0.18)  # instanciamos una manzana
        papa = Papa(0.15)  # instanciamos una papa
        zanahoria = Zanahoria(0.175)  # instanciamos una zanahoria

        cajon = Cajon()

        # Agrega alimentos al cajón
        cajon.agregar_alimento(kiwi)
        cajon.agregar_alimento(manzana)
        cajon.agregar_alimento(papa)
        cajon.agregar_alimento(zanahoria)

        # Prueba calcular_peso para el cajón
        resultado = calcular_peso(cajon)
        self.assertAlmostEqual(resultado, 0.575, places=2)

if __name__ == '__main__':
    unittest.main()
