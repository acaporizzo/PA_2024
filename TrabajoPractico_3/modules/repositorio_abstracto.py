from abc import ABC, abstractmethod

class RepositorioAbstracto(ABC):
    @abstractmethod
    def guardar_registro(self, entidad):
        """Guarda un registro en el repositorio"""
        raise NotImplementedError

    @abstractmethod
    def obtener_todos_los_registros(self) -> list:
        """Obtiene todos los registros del repositorio"""
        raise NotImplementedError
    
    @abstractmethod
    def modificar_registro(self, entidad_modificada):
        """Modifica un registro existente en el repositorio"""
        raise NotImplementedError   
    
    @abstractmethod
    def obtener_registro_por_filtro(self, filtro, valor):
        """Obtiene un registro que cumpla con un filtro específico"""
        raise NotImplementedError
    
    @abstractmethod
    def eliminar_registro(self, id):
        """Elimina un registro del repositorio por su ID"""
        raise NotImplementedError
