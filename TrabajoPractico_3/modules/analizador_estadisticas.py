import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

class AnalizadorEstadisticas:
    
    def _init_(self, reclamos):
        self.reclamos = reclamos
    
    def calcular_mediana(self):
        adherentes = [len(reclamo.adherentes) for reclamo in self.reclamos]
        if adherentes:
            return np.median(adherentes)
        return 0

    def generar_grafico_palabras_claves(self): #falta probar
        palabras = []
        for reclamo in self.reclamos:
            palabras.extend(reclamo.contenido.split())

        contador_palabras = Counter(palabras)
        palabras_comunes = contador_palabras.most_common(10)
        palabras, frecuencias = zip(*palabras_comunes)
        
        plt.barh(palabras, frecuencias)
        plt.xlabel('Frecuencia')
        plt.ylabel('Palabras')
        plt.title('Top 10 Palabras Clave en Reclamos')
        plt.show()