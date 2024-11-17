import nltk
import collections
import operator

def reclamos_similares(reclamos_same_depto, texto_objetivo):  
    """
    Devuelve una lista con los IDs de los reclamos similares.
    Si no hay reclamos similares, devuelve una lista vacía.

    reclamos_same_depto: lista de tuplas con la descripción de los reclamos y su ID [(descripcion, ID), ...]
    texto_objetivo: descripción del reclamo a comparar.
    """
    nltk.download('stopwords')
    stopwords_es = nltk.corpus.stopwords.words('spanish')

    # Filtrar palabras del texto objetivo
    palabras_filtradas_objetivo = [palabra for palabra in texto_objetivo.split() if palabra.lower() not in stopwords_es]
    texto_filtrado_objetivo = ' '.join(palabras_filtradas_objetivo)
    
    # Obtener lista de palabras ordenadas por frecuencia
    counter_objetivo = collections.Counter(texto_filtrado_objetivo.split())
    lista_objetivo = [palabra for palabra, _ in counter_objetivo.most_common()]

    similares = []

    # Procesar cada reclamo para filtrar palabras y calcular similitud
    for descripcion, id_reclamo in reclamos_same_depto:
        palabras_filtradas = [palabra for palabra in descripcion.split() if palabra.lower() not in stopwords_es]
        texto_filtrado = ' '.join(palabras_filtradas)

        counter_reclamo = collections.Counter(texto_filtrado.split())
        lista_reclamo = [palabra for palabra, _ in counter_reclamo.most_common()]

        # Comparar palabras significativas
        coincidencias = sum(1 for palabra in lista_objetivo if palabra in lista_reclamo)
        if lista_objetivo:
            prom_objetivo = (coincidencias / len(lista_objetivo)) * 100
        else:
            prom_objetivo = 0
        if lista_reclamo:
            prom_reclamo = (coincidencias / len(lista_reclamo)) * 100
        else:
            prom_reclamo = 0

        # Si el porcentaje de similitud es suficientemente alto, lo consideramos similar
        if prom_objetivo >= 70 and prom_reclamo >= 65:
            similares.append((id_reclamo, prom_objetivo))

    # Ordenar resultados por similitud descendente
    similares.sort(key=operator.itemgetter(1), reverse=True)

    # Devolver solo los IDs de los reclamos similares
    lista_IDs = [id_reclamo for id_reclamo, _ in similares]
    return lista_IDs
