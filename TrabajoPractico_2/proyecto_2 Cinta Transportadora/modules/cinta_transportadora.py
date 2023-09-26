from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.detector_alimentos import DetectorAlimento

class Cinta_Transportadora:
    def clasificar_alimentos(self, p_n_alimentos):
        """Método que va a simular el transporte de los alimentos, donde en cada iteración del while se van a 
        determinar n alimentos especificando su nombre (kiwi, manzana, papa, zanahoria o undefined) y peso. 
        Luego cada alimento se agrega a la lista de alimentos. 

        Args:
            p_n_alimentos (int): determina cuantos alimentos van a pasar por la cinta
        """
        lista_de_alimentos= []
        detector= DetectorAlimento() #instanciamos un dectector de alimentos 

        while len(lista_de_alimentos) < p_n_alimentos:            
            datos_alimento = detector.detectar_alimento()  #detector_alimentos.py
            tipo_alimento = datos_alimento['alimento']
            peso_alimento = datos_alimento['peso']

            if tipo_alimento == "undefined":
                continue
            if tipo_alimento == "kiwi":
                alimento= Kiwi(peso_alimento)
            elif tipo_alimento == "manzana":
                alimento= Manzana(peso_alimento)
            elif tipo_alimento  == "papa":
                alimento= Papa(peso_alimento)
            elif tipo_alimento == "zanahoria":
                alimento= Zanahoria(peso_alimento)

            lista_de_alimentos.append(alimento)  
            
        return(lista_de_alimentos)