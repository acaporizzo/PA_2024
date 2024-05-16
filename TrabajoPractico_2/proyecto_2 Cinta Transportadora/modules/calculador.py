from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.cajon import Cajon
import math 
import numpy as np 

def calcular_aw (alimento):
    """
    Calcula la actividad acuosa (aw) del alimento proporcionado.

    Args:
        alimento (Alimento): El alimento del que se va a calcular la actividad acuosa.

    Returns:
        float: El valor de la actividad acuosa calculada para el alimento.

    Raises:
        ValueError: Si el tipo de alimento no es compatible con los tipos esperados.
    """
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
    """
    Calcula el promedio de la actividad acuosa (aw) para los alimentos de la clase especificada en un cajón.
    """
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
    """
    Calcula el peso total de los alimentos en un cajón.

    Args:
        cajon (Cajon): El cajón que contiene los alimentos.

    Returns:
        float: El peso total de los alimentos en el cajón. Si el cajón está vacío, devuelve 0.0.
    """
    peso_total = 0
    contador = 0
    for alimento in cajon:
        peso_total += alimento.peso_del_alimento
        contador += 1

    if contador == 0:
        return (0.0)
    else:
        return (peso_total)