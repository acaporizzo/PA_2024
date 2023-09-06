# módulo para organizar funciones o clases utilizadas en nuestro proyecto

import datetime
frases_utilizadas=[]
def mostrar_lista_peliculas (lista_de_pelis_y_frases):
    """
    Esta función recibe una lista con todos los datos y devuelve una lista de tuplas

    Args:
        lista_de_pelis_y_frases (lista): es una lista de tuplas en la cual cada tupla contiene 
        una frase y su pelicula, esta lista se obtuvo de abrir el archivo, leerlo.

    Returns:
        lista: contiene todas las peliculas ordenadas alfabéticamente donde se eliminaron las repetidas
        y se indexaron.
    """
    lista=[]
    lista_sin=[]
    for linea in lista_de_pelis_y_frases:
        frase,pelicula=linea.rstrip("\n").split(";")
        lista.append(pelicula)
    lista_sin=set(lista)
    return [(i+1,elemento) for i,elemento in enumerate (sorted(lista_sin))] #elemento no es variable, es como i, en el fo

def trivia (lista_de_pelis_y_frases):
    """
    Esta función recibe una lista con todos los datos y devuelve una lista con los datos necesarios
    para que la persona pueda jugar a la trivia

    Args:
        lista_de_pelis_y_frases (lista): es una lista de tuplas en la cual cada tupla contiene 
        una frase y su pelicula, esta lista se obtuvo de abrir el archivo, leerlo.

    Return:
        Lista: es una lista que contiene:
        * En el índice 0 contiene la frase que se le muestra a la persona.
        * En el índice 1 contiene la opción de película correcta.
        * En el índice 2 contiene una lista con las dos opciones elegidas al azar y la correcta 
    """
    import random
    global frases_utilizadas 
 
    op_ganadora=random.choice(lista_de_pelis_y_frases) #tupla con frase y pelicula ganadora
    while op_ganadora[0] in frases_utilizadas: # Verificar si la frase ya ha sido utilizada
        op_ganadora = random.choice(lista_de_pelis_y_frases)
    frases_utilizadas.append(op_ganadora[0]) # Agregar la frase a la lista de frases utilizadas

    pelis_no_ganadoras= [p[1] for p in lista_de_pelis_y_frases if p[1] != op_ganadora[1]] #lista de todas las peliculas != a op_ganadora
    pelis_no_ganadoras1=sorted(set(pelis_no_ganadoras)) #eliminamos las opciones repetidas
    opciones=random.sample(pelis_no_ganadoras1, k=2) #lista de las dos opciones no ganadoras
    opciones.append(op_ganadora[1]) #le agregamos la opcion correcta a la lista de opciones
    lista=[op_ganadora[0],op_ganadora[1],opciones]
    random.shuffle(lista[2])
    return(lista)

def guardar_opciones (opciones):
    """
    Función que crea y escribe el archivo con la opción elegida junto con la fecha y la hora

    Args:
        opciones (int): el parámetro va a tomar el valor de la opción que elige la persona
    """
    if opciones >=1 and opciones <=5: #solo se añaden las opciones que sean mayor igual a 1 y menor igual a 5
        current_datetime = datetime.datetime.now()  #proporciona fecha actual
        formatted_datetime = current_datetime.strftime("%d/%m/%y %H:%M")  #le damos formato cadena de texto
        with open ("./data/registro de opciones selecionadas.txt","a") as f:
            f.write(f"Opciones: {opciones}, Fecha y hora {formatted_datetime}\n")  #escribimos el archivo con los datos
    else:
        pass 
def mostrar_opciones_seleccionadas(archivo):
    """
    Función que muestra el archivo que contiene el historial de las opciones elegidas, y en caso
    de que no se encuentre ese achrivo cuando se lo quiere leer, lo crea.
    """
    try:
        with open (archivo,"r") as f:
            linea=f.readlines()                    #se lee el archivo con los datos
            return(linea)                 #se muestra el historial
    except FileNotFoundError:
        with open ("data\registro de opciones selecionadas.txt","w") as f:   #excepción en el caso de que el historial esté vacío
            f.write()
def borrar_opciones (archivo):
    with open (archivo,"w") as f:                 #se reescribe el archivo, dejandolo vacío
        return(f.write(""))
def guardar_datos_del_juego(nombre_de_usuario, calificacion, fecha_hora):
    """Función que toma estos tres parámetros y escribe linea por linea

    Args:
        nombre_de_usuario (text): nombre dado por la persona
        calificacion (str): es una cadena que muestra aciertos/N (N=veces que se juega la trivia)
        fecha_hora (str): fecha y hora en la que se inicializa la trivia
    """
    with open("./data/resultados_historicos.txt", "a") as f:
        f.write(f"Hola, {nombre_de_usuario}. {calificacion} y su partida inició el: {fecha_hora}\n")


if __name__=="_main":
    pass