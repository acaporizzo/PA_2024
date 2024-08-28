def trivia (lista_de_pelis_y_frases,frases_utilizadas):
    """
    Esta función recibe una lista con todos los datos y devuelve una lista con los datos necesarios
    para que la persona pueda jugar a la trivia

    Args:
        lista_de_pelis_y_frases (lista): es una lista de tuplas en la cual cada tupla contiene 
        una frase y su pelicula, esta lista se obtuvo de abrir el archivo, leerlo.

    Returns:
        Lista: es una lista que contiene:
        * En el índice 0 contiene la frase que se le muestra a la persona.
        * En el índice 1 contiene la opción de película correcta.
        * En el índice 2 contiene una lista con las dos opciones elegidas al azar y la correcta 
    """
    import random
    op_ganadora=random.choice(lista_de_pelis_y_frases) # Tupla con frase y pelicula ganadora.
    while op_ganadora[0] in frases_utilizadas: # Verificar si la frase ya ha sido utilizada.
        op_ganadora = random.choice(lista_de_pelis_y_frases)
    frases_utilizadas.append(op_ganadora[0]) # Agregar la frase a la lista de frases utilizadas.

    pelis_no_ganadoras= [p[1].lower() for p in lista_de_pelis_y_frases if p[1].lower() != op_ganadora[1].lower()] # Lista de todas las peliculas != a op_ganadora.
    pelis_no_ganadoras1=sorted(set(pelis_no_ganadoras)) # Eliminamos las opciones repetidas.
    opciones=random.sample(pelis_no_ganadoras1, k=2) # Lista de las dos opciones no ganadoras.
    opciones.append(op_ganadora[1].lower()) # Le agregamos la opción correcta a la lista de opciones.
    lista=[op_ganadora[0], op_ganadora[1].capitalize(), [i.capitalize() for i in opciones]]
    random.shuffle(lista[2])
    return(lista)

