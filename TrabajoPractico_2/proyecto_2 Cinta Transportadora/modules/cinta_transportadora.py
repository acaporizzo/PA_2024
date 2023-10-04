from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.detector_alimentos import DetectorAlimento

class Cinta_Transportadora:
    def __init__(self):
        self._detector= DetectorAlimento() #instanciamos un detector de alimentos 

    def clasificar_alimento(self):

        datos_alimento = self._detector.detectar_alimento()
        tipo_alimento = datos_alimento['alimento']
        peso_alimento = datos_alimento['peso']

        while tipo_alimento == "undefined":
            datos_alimento = self._detector.detectar_alimento()
            tipo_alimento = datos_alimento['alimento']
            peso_alimento = datos_alimento['peso']
        
        if tipo_alimento == "kiwi":
            alimento= Kiwi(peso_alimento)
        elif tipo_alimento == "manzana":
            alimento= Manzana(peso_alimento)
        elif tipo_alimento  == "papa":
                alimento= Papa(peso_alimento)
        elif tipo_alimento == "zanahoria":
                alimento= Zanahoria(peso_alimento)

        return(alimento)
    
if __name__ == "__main__":
    cinta=Cinta_Transportadora()
    alimento=cinta.clasificar_alimento()
    print(alimento)