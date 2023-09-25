from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria

class Cajon_Alimentos:
    def __init__(self, p_lista_de_alimentos):
        self._lista_de_alimentos= p_lista_de_alimentos

    def calcular_aw_prom(self, p_lista_aw):
        if not p_lista_aw:  
            return(0)
        promedio= sum(p_lista_aw)/len(p_lista_aw)
        promedio= round(promedio,2)
        return(promedio) 
    
    def agregar_y_calcular_aw(self, p_lista_de_alimentos):
        aw_kiwis= []
        aw_manzanas= []
        aw_papas= []
        aw_zanahorias= []

        for alimento in p_lista_de_alimentos:
            aw_de_alimento = alimento.calcular_aw()
            if isinstance(alimento, Kiwi):
                aw_kiwis.append(aw_de_alimento)
            if isinstance(alimento, Manzana):
                aw_manzanas.append(aw_de_alimento)
            if isinstance(alimento,Papa):
                aw_papas.append(aw_de_alimento)
            if isinstance(alimento, Zanahoria):
                aw_zanahorias.append(aw_de_alimento)
        return(aw_kiwis, aw_manzanas, aw_papas, aw_zanahorias)