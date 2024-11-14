import json
import numpy as np

class Procesador():
  
  def __init__(self, direccion,):
    
    with open(direccion,'r', encoding='utf-8') as f:
      datos_entrenamiento = json.load(f)

    textos_entrenamiento = []
    etiquetas_entrenamiento = []
    
    for dato in datos_entrenamiento:
      texto = dato['reclamo']
      etiqueta = dato['etiqueta']
      textos_entrenamiento.append(texto)
      etiquetas_entrenamiento.append(etiqueta)
    
    mapeo_etiquetas = {'secretaría técnica': 0, 'soporte informático': 1, 'maestranza': 2}

    etiquetas_entrenamiento = [mapeo_etiquetas[etiqueta] for etiqueta in etiquetas_entrenamiento]
      
    #se unen todos los reclamos en un solo arreglo de numpy
    self.x = np.array(textos_entrenamiento , dtype = object)
    #se crea un arreglo con las etiquetas (areas) correspondientes a cada reclamo
    self.y = np.array(etiquetas_entrenamiento)

  @property
  def datosEntrenamiento(self):
    return self.x,self.y