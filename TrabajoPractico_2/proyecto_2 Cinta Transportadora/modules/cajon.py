from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria

class Cajon:
    def __init__(self, p_lista_de_alimentos):
        self._lista_de_alimentos= p_lista_de_alimentos
        self._index = 0

    @property
    def lista_de_alimentos(self):
        return(self._lista_de_alimentos)
    
    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._lista_de_alimentos):
            elemento = self._lista_de_alimentos[self._index]
            self._index += 1
            return elemento
        else:
            raise StopIteration

    def calcular_aw_promedios(self):
        """método que calcula la actividad acuosa de cada alimento que pasa por la cinta transportadora,
        y la agrega a la lista del alimento correspondiente. Luego, calcula el promedio de la actividad acuosa 
        para cada tipo de alimento, incluyendo Frutas, Verduras y Total. Retorna una lista con todos los aw
        promedio
        """
        cajon = Cajon(self._lista_de_alimentos)
        listakiwis = []
        listamanzanas = []
        listapapas = []
        listazanahorias = []

        for alimento in cajon:
            if isinstance(alimento,Kiwi):
                aw_de_alimento = alimento.calcular_aw()
                listakiwis.append(aw_de_alimento)
            if isinstance(alimento, Manzana):
                aw_de_alimento = alimento.calcular_aw()
                listamanzanas.append(aw_de_alimento) 
            if isinstance(alimento,Papa):
                aw_de_alimento = alimento.calcular_aw()
                listapapas.append(aw_de_alimento)
            if isinstance(alimento, Zanahoria):
                aw_de_alimento = alimento.calcular_aw()
                listazanahorias.append(aw_de_alimento)

        awk = sum(listakiwis)/len(listakiwis) if listakiwis else 0.0
        awm = sum(listamanzanas)/len(listamanzanas) if listamanzanas else 0.0
        awp = sum(listapapas)/len(listapapas) if listapapas else 0.0
        awz = sum(listazanahorias)/len(listazanahorias) if listazanahorias else 0.0
        awf = (sum(listakiwis)+sum(listamanzanas))/(len(listakiwis)+len(listamanzanas)) if (listakiwis or listamanzanas) else 0.0
        awv = (sum(listapapas)+sum(listazanahorias))/(len(listapapas)+len(listazanahorias)) if (listapapas or listazanahorias) else 0.0
        awt = (sum(listakiwis)+sum(listamanzanas)+sum(listapapas)+sum(listazanahorias))/(len(listakiwis)+len(listamanzanas)+len(listapapas)+len(listazanahorias)) if (listakiwis or listamanzanas or listapapas or listazanahorias) else 0.0

        lista=[round(awk,2),round(awm,2),round(awp,2),round(awz,2),round(awf,2),round(awv,2),round(awt,2)]
        
        return(lista)




        