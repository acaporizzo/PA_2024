from abc import ABC, abstractmethod
import math 
import numpy as np 

"""Clases abstractas
    """
class Alimentos(ABC):
    def __init__(self, p_nombre_del_alimento, p_peso_del_alimento):
        self._nombre_del_alimento = p_nombre_del_alimento
        self._peso_del_alimento = p_peso_del_alimento

    @abstractmethod 
    def calcular_aw(self):
        pass 

class Fruta(Alimentos, ABC):
    def __init__(self, p_nombre_del_alimento, p_peso_del_alimento):
        super().__init__(p_nombre_del_alimento, p_peso_del_alimento)
        
    @abstractmethod
    def calcular_aw(self):
        pass
    
class Verdura(Alimentos, ABC):
    def __init__(self, p_nombre_del_alimento, p_peso_del_alimento):
        super().__init__(p_nombre_del_alimento, p_peso_del_alimento)

    @abstractmethod
    def calcular_aw(self):
        pass

class Kiwi(Fruta):
    def __init__(self, p_nombre_del_alimento, p_peso_del_alimento):
        """Clase que hereda sus atributos de Fruta que a la vez hereda sus atributos de Alimentos 
        """
        super().__init__(p_nombre_del_alimento, p_peso_del_alimento)

    def calcular_aw(self):
        """Calcula la actividad acuosa de la KIWI
        """
        awk = 0.96 * ((1 - math.exp(-18 * self._peso_del_alimento)) / (1 + math.exp(-18 * self._peso_del_alimento)))
        return(awk)

    def __str__(self):
        """Método que devuelve una cadena de texto que incluye el nombre y el peso del alimento
        """
        return(f"{self._nombre_del_alimento} {self._peso_del_alimento}")

class Manzana(Fruta):
    def __init__(self, p_nombre_del_alimento, p_peso_del_alimento):
        """Clase que hereda sus atributos de Fruta que a la vez hereda sus atributos de Alimentos 
        """
        super().__init__(p_nombre_del_alimento, p_peso_del_alimento)

    def calcular_aw(self):
        """Calcula la actividad acuosa de la MANZANA
        """
        awm = 0.97 * ((15 * self._peso_del_alimento) ** 2) / (1 + (15 * self._peso_del_alimento) ** 2)
        return(awm)
            
    def __str__(self):
        """Método que devuelve una cadena de texto que incluye el nombre y el peso del alimento
        """
        return(f"{self._nombre_del_alimento} {self._peso_del_alimento}")
        
class Papa(Verdura):
    def __init__(self, p_nombre_del_alimento, p_peso_del_alimento):
        """Clase que hereda sus atributos de Verdura que a la vez hereda sus atributos de Alimentos 
        """
        super().__init__(p_nombre_del_alimento, p_peso_del_alimento)
    
    def calcular_aw(self):
        """Calcula la actividad acuosa de la PAPA
        """
        awp = 0.66 * (np.arctan(18 * self._peso_del_alimento))
        return(awp)

    def __str__(self):
        """Método que devuelve una cadena de texto que incluye el nombre y el peso del alimento
        """
        return(f"{self._nombre_del_alimento} {self._peso_del_alimento}")
 

class Zanahoria(Verdura):
    def __init__(self, p_nombre_del_alimento, p_peso_del_alimento):
        """Clase que hereda sus atributos de Verdura que a la vez hereda sus atributos de Alimentos 
        """
        super().__init__(p_nombre_del_alimento, p_peso_del_alimento)
 
    def calcular_aw(self):
        """Calcula la actividad acuosa de la ZANAHORIA
        """
        awz = 0.96 * ((1 - math.exp(-10 * self._peso_del_alimento)))
        return(awz)
    
    def __str__(self):
        """Método que devuelve una cadena de texto que incluye el nombre y el peso del alimento
        """
        return(f"{self._nombre_del_alimento} {self._peso_del_alimento}")