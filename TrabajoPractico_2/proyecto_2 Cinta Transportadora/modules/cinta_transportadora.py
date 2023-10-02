from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.detector_alimentos import DetectorAlimento

class Cinta_Transportadora:
    def clasificar_alimentos(self, p_n_alimentos):
        """Clasifica alimentos detectados por un detector y crea una lista de instancias de alimentos clasificados.

    Args:
        p_n_alimentos (int): El número deseado de alimentos a clasificar.

    Returns:
        lista_de_alimentos (list): Una lista de instancias de alimentos clasificados, donde cada instancia 
        pertenece a una de las siguientes clases: Kiwi, Manzana, Papa o Zanahoria.
        """

        detector= DetectorAlimento() #instanciamos un detector de alimentos 
        lista_de_alimentos= []
       
        while len(lista_de_alimentos) < p_n_alimentos:
            datos_alimento = detector.detectar_alimento()
            tipo_alimento = datos_alimento['alimento']
            peso_alimento = datos_alimento['peso']

            if tipo_alimento == "undefined":
                continue
            elif tipo_alimento == "kiwi":
                alimento= Kiwi(peso_alimento)
                lista_de_alimentos.append(alimento)
            elif tipo_alimento == "manzana":
                alimento= Manzana(peso_alimento)
                lista_de_alimentos.append(alimento)
            elif tipo_alimento  == "papa":
                alimento= Papa(peso_alimento)
                lista_de_alimentos.append(alimento)
            elif tipo_alimento == "zanahoria":
                alimento= Zanahoria(peso_alimento)
                lista_de_alimentos.append(alimento)

        return(lista_de_alimentos)