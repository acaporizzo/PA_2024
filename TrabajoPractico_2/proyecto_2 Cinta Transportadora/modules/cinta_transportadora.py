from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.detector_alimentos import DetectorAlimento

class Cinta_Transportadora:
    def __init__(self):
        self._detector= DetectorAlimento() #instanciamos un detector de alimentos 

    def clasificar_alimento(self):
        """
        Clasifica el alimento detectado y crea una instancia del objeto correspondiente.

        Returns:
            objeto: Una instancia de la clase correspondiente al tipo de alimento detectado,
            o None si el tipo de alimento es "undefined".

        Raises:
            KeyError: Si los datos del alimento no contienen las claves 'alimento' o 'peso'.
        """
        
        datos_alimento = self._detector.detectar_alimento()
        tipo_alimento = datos_alimento['alimento']
        peso_alimento = datos_alimento['peso']

        if tipo_alimento == "undefined":
            alimento = None
            
        if tipo_alimento == "kiwi":
            alimento = Kiwi(peso_alimento)

        elif tipo_alimento == "manzana":
            alimento = Manzana(peso_alimento)

        elif tipo_alimento  == "papa":
            alimento = Papa(peso_alimento)
            
        elif tipo_alimento == "zanahoria":
            alimento = Zanahoria(peso_alimento)

        return(alimento)
