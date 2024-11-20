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