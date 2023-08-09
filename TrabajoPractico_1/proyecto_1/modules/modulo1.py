# módulo para organizar funciones o clases utilizadas en nuestro proyecto
lista=[]
lisa_sin=[]
def mostrar_lista_peliculas (archivo_peliculas):
    """Función que lee el archivo con las frases de las peliculas y muestra una lista de tuplas"""
    with open (archivo_peliculas, "r",encoding="utf-8") as f: #reconoce caracteres especiales en la lista
        for linea in f:
            frase,pelicula=linea.rstrip("\n").split(";")
            lista.append(pelicula)
    lista_sin=set(lista)
    return [(i+1,elemento) for i,elemento in enumerate (sorted(lista_sin))] #elemento no es variable, es como i, en el for