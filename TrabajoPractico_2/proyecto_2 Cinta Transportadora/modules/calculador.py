from modules.cajon import Cajon
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
import math 
import numpy as np 

def calcular_aw (alimento):

    if isinstance(alimento,Kiwi):
        aw = 0.96 * ((1 - math.exp(-18 * alimento.peso_del_alimento)) / (1 + math.exp(-18 * alimento.peso_del_alimento)))
    elif isinstance(alimento,Manzana):
        aw = 0.97 * ((15 * alimento.peso_del_alimento) ** 2) / (1 + (15 * alimento.peso_del_alimento) ** 2)
    elif isinstance(alimento,Papa):
        aw = 0.66 * (np.arctan(18 * alimento.peso_del_alimento))
    elif isinstance(alimento,Zanahoria):
        aw = 0.96 * ((1 - math.exp(-10 * alimento.peso_del_alimento)))
    return(aw)

def calcular_aw_promedio(p_clase, cajon: Cajon):
    total_aw = 0.0
    contador = 0
    
    for alimento in cajon:
        if isinstance(alimento,p_clase):
            total_aw += calcular_aw(alimento)
            contador += 1
    
    if contador == 0:
        return (0.0)
    else:
        return (total_aw/contador)


    
def calcular_peso (cajon: Cajon):
    peso_total = 0
    contador = 0
    for alimento in cajon:
        peso_total += alimento.peso_del_alimento
        contador += 1

    if contador == 0:
        return (0.0)
    
    else:
        return (peso_total)