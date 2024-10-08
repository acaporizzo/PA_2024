class Cajon:
    def __init__(self):
        self._alimentos = []

    @property
    def alimentos(self):
        return(self._alimentos)
    
    def agregar_alimento(self, alimento):
        """
        Este método añade una instancia de un alimento a la lista de alimentos de la clase.
        El alimento debe ser una instancia de una clase que represente un tipo de alimento.
        """
        self._alimentos.append(alimento)
    
    def __iter__(self):
        """
        Método especial que permite que un objeto sea iterable.

        Returns:
            self: El propio objeto, ya que este objeto se considera iterable.
        """
        self._index = 0
        return self
    
    def __len__(self):
        """
        Este método especial permite utilizar la función `len()` en una instancia de la clase
        para obtener el número de alimentos que contiene.
        """
        return len(self._alimentos)
    
    def __next__(self):
        """
        Este método especial permite iterar sobre los alimentos en la instancia de la clase.
        Cada llamada a `__next__` devuelve el siguiente alimento en la lista. Si se llega al
        final de la lista, se lanza una excepción `StopIteration` para indicar que no hay más
        elementos que iterar.

        """
        if self._index < len(self._alimentos):
            result = self._alimentos[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration