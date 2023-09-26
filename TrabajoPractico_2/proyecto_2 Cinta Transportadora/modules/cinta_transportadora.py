from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.detector_alimentos import DetectorAlimento

class Cinta_Transportadora:

    def transportar(self, p_n_alimentos):
        """Método que va a simular el transporte de los alimentos, donde en cada iteración del while se van a 
        determinar n alimentos especificando su nombre (kiwi, manzana, papa, zanahoria o undefined) y peso. 
        Luego cada alimento se agrega a la lista de alimentos. 

        Args:
            p_n_alimentos (int): determina cuantos alimentos van a pasar por la cinta
        """
        lista_de_alimentos= []
        detector= DetectorAlimento() #instanciamos un dectector de alimentos 

        while len(lista_de_alimentos) < p_n_alimentos:            
            datos_alimento = detector.detectar_alimento()
            nombre_alimento = datos_alimento['alimento']
            peso_alimento = datos_alimento['peso']

            if nombre_alimento == "undefined":
                continue
            if nombre_alimento == "kiwi":
                alimento= Kiwi(nombre_alimento, peso_alimento)
            elif nombre_alimento == "manzana":
                alimento= Manzana(nombre_alimento, peso_alimento)
            elif nombre_alimento  == "papa":
                alimento= Papa(nombre_alimento, peso_alimento)
            elif nombre_alimento == "zanahoria":
                alimento= Zanahoria(nombre_alimento, peso_alimento)
            lista_de_alimentos.append(alimento)  
            
        return(lista_de_alimentos)