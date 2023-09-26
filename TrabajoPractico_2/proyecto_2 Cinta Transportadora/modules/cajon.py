from modules.alimentos import Fruta, Verdura, Kiwi, Manzana, Papa, Zanahoria

class Cajon:
    def __init__(self, p_lista_de_alimentos):
        self._lista_de_alimentos= p_lista_de_alimentos

    def agregar_y_calcular_aw(self, p_lista_de_alimentos):
        """método que calcula la actividad acuosa de cada alimento que pasa por la cinta transportadora y lo agrega a la lista del
        alimento correspondiente 

        Args:
            p_lista_de_alimentos (lista): todos los alimentos que pasan por la cinta transportadora
        """
        aw_kiwis= []
        aw_manzanas= []
        aw_papas= []
        aw_zanahorias= []
        aw_frutas= []
        aw_verduras= []

        for alimento in p_lista_de_alimentos:
            aw_de_alimento= alimento.calcular_aw()

            if isinstance(alimento, Fruta):
                aw_kiwis.append(aw_de_alimento)
                promedio_frutas= sum(aw_frutas)/len(aw_frutas)
                awf= round(promedio_frutas,2)

                if isinstance(alimento, Kiwi):
                    aw_kiwis.append(aw_de_alimento)
                    promedio_kiwis= sum(aw_kiwis)/len(aw_kiwis)
                    awk= round(promedio_kiwis,2)

                elif isinstance(alimento, Manzana):
                    aw_manzanas.append(aw_de_alimento)
                    promedio_manzanas= sum(aw_manzanas)/len(aw_manzanas)
                    awm= round(promedio_manzanas,2)

            elif isinstance(alimento, Verdura):
                aw_verduras.append(aw_de_alimento)
                promedio_verduras= sum(aw_verduras)/len(aw_verduras)
                awv= round(promedio_verduras,2)

                if isinstance(alimento,Papa):
                    aw_papas.append(aw_de_alimento)
                    promedio_papas= sum(aw_papas)/len(aw_papas)
                    awp= round(promedio_papas,2)

                elif isinstance(alimento, Zanahoria):
                    aw_zanahorias.append(aw_de_alimento)
                    promedio_zanahorias= sum(aw_zanahorias)/len(aw_zanahorias)
                    awz= round(promedio_zanahorias,2)

            else:
                return (0)
                
        return(awk, awm, awp, awz, awf, awv)

