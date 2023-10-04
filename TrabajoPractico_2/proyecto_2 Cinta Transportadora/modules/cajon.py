from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.cinta_transportadora import Cinta_Transportadora
class Cajon:
    def __init__(self):
        self._alimentos = []

    @property
    def alimentos(self):
        return(self._alimentos)
    
    def __iter__(self):
        """método especial que permite que un objeto sea iterable.

        Returns:
            self: El propio objeto, ya que este objeto se considera iterable.
        """
        self._index = 0
        return self
    
    def agregar_alimento(self, alimento):
        self._alimentos.append(alimento)
        return (self)

    def __str__(self):
        """método que devuelve una cadena de texto que incluye el nombre y el peso del alimento
        """
        return(self._alimentos)
    
if __name__ == "__main__":
    cinta=Cinta_Transportadora()
    alimento=cinta.clasificar_alimento()
    alimento2=cinta.clasificar_alimento()
    cajon=Cajon()
    cajon2=cajon.agregar_alimento(alimento)
    cajon2=cajon.agregar_alimento(alimento2)
    print(cajon2)