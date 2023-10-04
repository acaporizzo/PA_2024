from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.cinta_transportadora import Cinta_Transportadora
#from modules.calculador_aw import calcular_aw_promedio
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
    
    def __next__(self):
        if self._index < len(self._alimentos):
            result = self._alimentos[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration
        
    def agregar_alimento(self, alimento):
        self._alimentos.append(alimento)
    
    def __len__(self):
        return len(self._alimentos)
    
if __name__ == "__main__":

    from modules.calculador_aw import calcular_aw_promedio
    cinta=Cinta_Transportadora()
    alimento1=cinta.clasificar_alimento()
    alimento2=cinta.clasificar_alimento()
    cajon=Cajon()
    cajon.agregar_alimento(alimento1)
    cajon.agregar_alimento(alimento2)
    contador=cajon.contar_alimentos()
    for alimento in cajon:
        print(alimento)
    print(contador)
    print(calcular_aw_promedio(Kiwi,cajon))

