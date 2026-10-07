# domain/exceptions.py

class ErrorDeDominio(Exception):
    """Excepcion base para errores del dominio de inventario."""
    pass
    

class ProductoInvalidoError(ErrorDeDominio):
    """Se lanza cuando los datos de un producto no cumplen las reglas de negocio"""
    def __init__(self, mensaje = 'El producto viola las reglas del dominio.')
        super().__init__(mensaje)


class ProductoNoEncontradoError(ErrorDeDominio):
    """Se lanza cuando se busca un producto que no existe en el inventario"""
    def __init__(self, identificador=None)
        if identificador:
            mensaje = f'No se encontro el mensaje: {identificador}'
        else:
            mensaje = 'El producto solicitado no existe'
        super()__init__(mensaje)



