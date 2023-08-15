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
   
def trivia (archivo_peliculas):
    import random
    """Función que lee el archivo con las frases de las peliculas y extrae 3 frases al azar"""
    with open (archivo_peliculas, "r",encoding="utf-8") as f: #reconoce caracteres especiales en la lista
        lista_trivia=f.readlines
        random.randint(0,len(lista_trivia)-1)
        frase,pelicula1=lista_trivia[random.randint(0,len(lista_trivia)-1)].split(";") #frase ganadora
        pelicula2=lista_trivia[random.randint(0,len(lista_trivia)-1)][1]
        pelicula3=lista_trivia[random.randint(0,len(lista_trivia)-1)][1]