from abc import ABC, abstractmethod
import math 
import numpy as np 

"""
clases abstractas
"""

class Alimentos(ABC):
    def __init__(self, p_peso_del_alimento):
        if 0.05<=p_peso_del_alimento <= 0.6:
            self._peso_del_alimento = p_peso_del_alimento
        else:
            raise ValueError ("el peso no se encuentra dentro de los parámetros.")

    @property
    def peso_del_alimento(self):
        return(self._peso_del_alimento)

class Fruta(Alimentos, ABC):
    def __init__(self, p_peso_del_alimento):
        super().__init__(p_peso_del_alimento)
    
class Verdura(Alimentos, ABC):
    def __init__(self, p_peso_del_alimento):
        super().__init__(p_peso_del_alimento)

class Kiwi(Fruta):
    def __init__(self, p_peso_del_alimento):
        """clase que hereda sus atributos de Fruta que a la vez hereda sus atributos de Alimentos 
        """
        super().__init__(p_peso_del_alimento)

    def __str__(self):
        """método que devuelve una cadena de texto que incluye el nombre y el peso del alimento
        """
        return("Kiwi")

class Manzana(Fruta):
    def __init__(self, p_peso_del_alimento):
        """Clase que hereda sus atributos de Fruta que a la vez hereda sus atributos de Alimentos 
        """
        super().__init__(p_peso_del_alimento)
            
    def __str__(self):
        """método que devuelve una cadena de texto que incluye el nombre y el peso del alimento
        """
        return("Manzana")
        
class Papa(Verdura):
    def __init__(self, p_peso_del_alimento):
        """clase que hereda sus atributos de Verdura que a la vez hereda sus atributos de Alimentos 
        """
        super().__init__(p_peso_del_alimento)

    def __str__(self):
        """método que devuelve una cadena de texto que incluye el nombre y el peso del alimento
        """
        return("Papa")
 
class Zanahoria(Verdura):
    def __init__(self, p_peso_del_alimento):
        """clase que hereda sus atributos de Verdura que a la vez hereda sus atributos de Alimentos 
        """
        super().__init__(p_peso_del_alimento)
    
    def __str__(self):
        """método que devuelve una cadena de texto que incluye el nombre y el peso del alimento
        """
        return("Zanahoria")

