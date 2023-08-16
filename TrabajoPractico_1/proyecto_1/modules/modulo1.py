# módulo para organizar funciones o clases utilizadas en nuestro proyecto

import datetime

def mostrar_lista_peliculas (archivo_peliculas):
    """Función que lee el archivo con las frases de las peliculas y muestra una lista de tuplas"""
    lista=[]
    lista_sin=[]
    with open (archivo_peliculas, "r",encoding="utf-8") as f: #reconoce caracteres especiales en la lista
        for linea in f:
            frase,pelicula=linea.rstrip("\n").split(";")
            lista.append(pelicula)
    lista_sin=set(lista)
    return [(i+1,elemento) for i,elemento in enumerate (sorted(lista_sin))] #elemento no es variable, es como i, en el fo

def trivia (archivo_peliculas):
    import random
    """Función que lee el archivo con las frases de las peliculas y extrae 3 películas y 1 frase al azar"""
    with open (archivo_peliculas, "r",encoding="utf-8") as f: # utf-8 reconoce caracteres especiales en la lista
        repeticiones=int(input("Ingrese la cantidad de frases en la que consistirá la trivia (mínimo 3, máximo 10): "))
        while repeticiones<3 or repeticiones>10:
            repeticiones=int(input("Ingrese nuevamente la cantidad. Debe ser un número entre 3 y 10. "))
        lista1=f.readlines()
        frases_y_pelis = [(linea.strip().split(';')[0], linea.strip().split(';')[1]) for linea in lista1]

        for i in range(1,repeticiones+1):   #se recorre la cantidad de veces que el usuario solicita
            op_ganadora=random.choice(frases_y_pelis) #tupla con frase y pelicula ganadora
            pelis_no_ganadoras= [p[1] for p in frases_y_pelis if p != op_ganadora] #lista de todas las peliculas != a op_ganadora
            pelis_no_ganadoras1=sorted(set(pelis_no_ganadoras)) #eliminamos las opciones repetidas
            opciones=random.sample(pelis_no_ganadoras1, k=2) #lista de las dos opciones no ganadoras
            opciones.append(op_ganadora[1]) #le agregamos la opcion correcta a la lista de opciones
            random.shuffle(opciones) #mezcla las opciones
            print("Adivine a que película pertenece la siguiente frase: ",i,": ",op_ganadora[0])
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
                    print("La opción es incorrecta :( , la opción correcta es: ",op_ganadora[1])
            frases_y_pelis.pop(frases_y_pelis.index(op_ganadora))    #eliminamos la frase para que no se repitan

    return("\n ¡¡¡Gracias por participar!!!")

def guardar_opciones (opciones):
    current_datetime = datetime.datetime.now()  #proporciona fecha actual
    formatted_datetime = current_datetime.strftime("%d/%m/%y %H:%M")  #le damos formato cadena de texto
    with open ("./data/registro de opciones selecionadas.txt","a") as f:
        f.write(f"Opciones: {opciones}, Fecha y hora {formatted_datetime}\n")  #escribimos el archivo con los datos
def mostrar_opciones_seleccionadas(archivo):
    try:
        with open (archivo,"r") as f:
            linea=f.read()                    #se lee el archivo con los datos
            print("Las opciones seleccionadas previamente son:")
            return(linea+"\n")                 #se muestra el historial
    except FileNotFoundError:
        print("Aún no se han registrado opciones.")    #excepción en el caso de que el historial esté vacío

def borrar_opciones (archivo):
    with open (archivo,"w") as f:
        f.write("")                     #se reescribe el archivo, dejandolo vacío
    return(print("El historial se eliminó correctamente. "))
    