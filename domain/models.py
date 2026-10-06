# domain/models.py
from dataclasses import dataclass
from domain.exceptions import ProductoInvalidoError

@dataclass
class Producto:
    id: str
    nombre: str
    cantidad: int
    precio_unitario: float

    def __post_init__(self) -> None:
        """
        Se ejecuta automaticamente al construir el objeto.
        Aqui debes VALIDAR las reglas de negocio.
        """
    
        if not self.nombre or not self.nombre.strip():
            raise ProductoInvalidoError('El nombre no puede estar vacio.')

        if self.cantidad < 0:
            raise ProductoInvalidoError('La cantidad no puede ser negativa.')

        if self.precio_unitario < 0:
            raise ProductoInvalidoError ('El precio unitario no puede ser negativo.')
        
    