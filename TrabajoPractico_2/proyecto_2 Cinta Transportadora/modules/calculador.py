from modules.cajon import Cajon

def calcular_aw_promedio(p_clase, cajon: Cajon):
    """
    Calcula el promedio de la actividad acuosa (aw) para los alimentos de la clase especificada en un cajón.
    """
    total_aw = 0.0
    contador = 0
    
    for alimento in cajon:
        if isinstance(alimento,p_clase):
            total_aw += alimento.calcular_aw()
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