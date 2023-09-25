from abc import ABC, abstractmethod
import math #biblioteca para los cálculos numéricos
import numpy as np #biblioteca para cálculos más avanzados.

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

class Manzana(Fruta):
    def __init__(self, p_nombre_del_alimento, p_peso_del_alimento):
        super().__init__(p_nombre_del_alimento, p_peso_del_alimento)
            
    def __str__(self):
        return(f"{self._nombre_del_alimento} {self._peso_del_alimento}")

# Calcula la actividad acuosa de la MANZANA
    def calcular_aw(self):
        awm = 0.97 * ((15 * self._peso_del_alimento) ** 2) / (1 + (15 * self._peso_del_alimento) ** 2)
        return(awm)
            
class Kiwi(Fruta):
    def __init__(self, p_nombre_del_alimento, p_peso_del_alimento):
        super().__init__(p_nombre_del_alimento, p_peso_del_alimento)
        
    def __str__(self):
        return(f"{self._nombre_del_alimento} {self._peso_del_alimento}")

# Calcula la actividad acuosa del KIWI
    def calcular_aw(self):
        awk = 0.96 * ((1 - math.exp(-18 * self._peso_del_alimento)) / (1 + math.exp(-18 * self._peso_del_alimento)))
        return(awk)

class Papa(Verdura):
    def __init__(self, p_nombre_del_alimento, p_peso_del_alimento):
        super().__init__(p_nombre_del_alimento, p_peso_del_alimento)
    
    def __str__(self):
        return(f"{self._nombre_del_alimento} {self._peso_del_alimento}")

# Calcula la actividad acuosa de la PAPA
    def calcular_aw(self):
        awp = 0.66 * (np.arctan(18 * self._peso_del_alimento))
        return(awp)

class Zanahoria(Verdura):
    def __init__(self, p_nombre_del_alimento, p_peso_del_alimento):
        super().__init__(p_nombre_del_alimento, p_peso_del_alimento)
    
    def __str__(self):
        return(f"{self._nombre_del_alimento} {self._peso_del_alimento}")

# Calcula la actividad acuosa de la ZANAHORIA
    def calcular_aw(self):
        awz = 0.96 * ((1 - math.exp(-10 * self._peso_del_alimento)))
        return(awz)