from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.detector_alimentos import DetectorAlimento

class Cinta_Transportadora:

    def transportar(self, n):
        lista_de_alimentos= []
        detector= DetectorAlimento()

        while len(lista_de_alimentos) < n:            
            diccionario= detector.detectar_alimento()
            nombre = diccionario['alimento']
            peso = diccionario['peso']

            if nombre == "undefined":
                continue
            if nombre == "kiwi":
                alimento= Kiwi(nombre, peso)
            elif nombre == "manzana":
                alimento= Manzana(nombre, peso)
            elif nombre  == "papa":
                alimento= Papa(nombre, peso)
            elif nombre == "zanahoria":
                alimento= Zanahoria(nombre, peso)
            lista_de_alimentos.append(alimento)  
            
        return(lista_de_alimentos)