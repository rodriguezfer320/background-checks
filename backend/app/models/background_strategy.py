from abc import ABC, abstractmethod

class BackgroundStrategy(ABC):
    
    def __init__(self):
        self._message_error = 'No se pudo obtener la información del canditato en este antecedente, debido a que, ocurrio un error inesperado.'
        self._description = {
            'title': None,
            'date': None,
            'message': None,
            'data': None,
            'link': None
        }
    
    @abstractmethod
    def get_background_information(self, data):
        pass