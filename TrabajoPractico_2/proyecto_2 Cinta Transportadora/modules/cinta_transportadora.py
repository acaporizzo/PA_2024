from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.detector_alimentos import DetectorAlimento

class Cinta_Transportadora:
    def clasificar_alimentos(self, p_n_alimentos):
        """método que simula el transporte de los alimentos, donde en cada iteración del ciclo while se van a 
        clasificar n alimentos especificando su nombre (kiwi, manzana, papa, zanahoria o undefined) y peso. 
        Luego cada alimento se agrega a la lista de alimentos que corresponde. Retorna la lista de alimentos.

        Args:
            p_n_alimentos (int): determina cuantos alimentos van a pasar por la cinta
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