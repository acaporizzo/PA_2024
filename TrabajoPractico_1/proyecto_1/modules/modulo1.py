# módulo para organizar funciones o clases utilizadas en nuestro proyecto

def mostrar_lista_peliculas (archivo_peliculas):
    """Función que lee el archivo con las frases de las peliculas y muestra una lista de tuplas"""
    lista=[]
    lista_sin=[]
    with open (archivo_peliculas, "r",encoding="utf-8") as f: #reconoce caracteres especiales en la lista
        for linea in f:
            frase,pelicula=linea.rstrip("\n").split(";")
            lista.append(pelicula)
    lista_sin=set(lista)
    return [(i+1,elemento) for i,elemento in enumerate (sorted(lista_sin))] #elemento no es variable, es como i, en el for
   
def trivia (archivo_peliculas):
    import random
    """Función que lee el archivo con las frases de las peliculas y extrae 3 películas y 1 frase al azar"""
    with open (archivo_peliculas, "r",encoding="utf-8") as f: # utf-8 reconoce caracteres especiales en la lista
        lista1=f.readlines()
        frases_y_pelis = [(linea.strip().split(';')[0], linea.strip().split(';')[1]) for linea in lista1]
        op_ganadora=random.choice(frases_y_pelis) #tupla con frase y pelicula ganadora
        pelis_no_ganadoras= [p[1] for p in frases_y_pelis if p != op_ganadora] #lista de todas las peliculas != a op_ganadora
        pelis_no_ganadoras1=sorted(set(pelis_no_ganadoras)) #eliminamos las opciones repetidas
        opciones=random.sample(pelis_no_ganadoras1, k=2) #lista de las dos opciones no ganadoras
        opciones.append(op_ganadora[1]) #le agregamos la opcion correcta a la lista de opciones
        random.shuffle(opciones) #mezcla las opciones
        print("Adivine a que película pertenece la siguiente frase: ",op_ganadora[0])
        print("Las opciones para elegir son: ")
        for i,j in zip(opciones,range(1,4)): #agrega numero a las opciones de peliculas
            print(j,i)        
        opcion=int(input("Elija la opción correcta, ingresando 1, 2 o 3 : "))
        if opcion-1==opciones.index(op_ganadora[1]):
            print("¡¡¡Felicitaciones, la opción elegida es la correcta!!!")
        elif opcion-1!=opciones.index(op_ganadora[1]):
            if opcion!=1 and opcion!=2 and opcion!=3:
                print("El número ingresado no es una opción posible")
            else:
                print("La opción es incorrecta :( ")

    return("\n ¡¡¡Gracias por participar!!!")

"""def op_seleccionadas (opcion1):
    lista_opciones=[]
    lista_opciones.append(opcion1)
    return(lista_opciones)"""
