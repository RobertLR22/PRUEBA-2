from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models import Producto

class RepositorioInventario(ABC):
    """
    Puerto (interfaz abstracta) que define el contrato para cualquier mecanismo
    
    """
    @abstractmethod
    def guardar(self, producto: Producto) -> None:
        """ Guarda o actualiza un producto en el sistema de almacenamiento """
        pass
    
    @abstractmethod
    def listar(self) -> List[Producto]:
        """ Obtiene y retona la lista completa de productos registrados """
        pass
    
    @abstractmethod
    def buscar_por_id(self, producto_id: str)  -> Optional[Producto]:
        """ Busca un producto por su identificador unico.
        Retorna la instancia de Producto si existe , o None si no se encuentra.
        """
        pass

    @abstractmethod
    def eliminar(self, producto_id: str) -> None:
        """ Elimina un producto del almacenamiento usando su identificador. """
        pass
