from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria

class Cajon:
    def __init__(self, p_lista_de_alimentos):
        self._lista_de_alimentos= p_lista_de_alimentos

    @property
    def lista_de_alimentos(self):
        return(self._lista_de_alimentos)
    
    def agregar_y_calcular_aw(self, p_lista_de_alimentos):
        """método que calcula la actividad acuosa de cada alimento que pasa por la cinta transportadora y lo agrega a la lista del
        alimento correspondiente 

        Args:
            p_lista_de_alimentos (lista): todos los alimentos que pasan por la cinta transportadora
        """
        diccionario_con_listas_aw = {'Kiwi': [], 'Manzana': [], 'Papa': [], 'Zanahoria': []}

        for alimento in p_lista_de_alimentos:
            if isinstance(alimento, (Kiwi, Manzana, Papa, Zanahoria)):
                aw_de_alimento = alimento.calcular_aw()
                tipo_alimento = type(alimento).__name__
                aw_valor = [aw_de_alimento]
                diccionario_con_listas_aw[tipo_alimento].extend(aw_valor)

        return (diccionario_con_listas_aw)
    
    def calcular_aw_prom_diccionario(self,diccionario_con_listas_aw):
        """Calcula el promedio de la actividad acuosa para cada tipo de alimento.

        Args:
            diccionario_con_listas_aw (dict): Diccionario con listas de actividad acuosa para cada tipo de alimento.

        Returns:
            promedios (dict): Diccionario con los promedios de actividad acuosa para cada tipo de alimento.
        """
        promedios = {}

        for tipo, lista_aw in diccionario_con_listas_aw.items():
            if lista_aw:
                promedio = round(sum(lista_aw) / len(lista_aw), 2)
                promedios[tipo] = promedio
            else:
                promedios[tipo] = 0.0

        return(promedios)
    
    def calcular_aw_prom(self,lista_aw):
        if not lista_aw:  
            return 0
        
        promedio= sum(lista_aw)/len(lista_aw)
        promedio= round(promedio, 2)

        return(promedio) 
        