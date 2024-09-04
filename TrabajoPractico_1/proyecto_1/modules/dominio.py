def trivia (lista_de_pelis_y_frases,frases_utilizadas):
    """
    Selecciona una frase y su película correcta para la trivia, asegurando que no se repita,
    y genera opciones al azar para que el jugador elija.

    Args:
        lista_de_pelis_y_frases (list): Lista de tuplas donde cada tupla contiene una frase y su película asociada.
        frases_utilizadas (list): Lista de frases que ya han sido utilizadas en el juego.

    Returns:
        list: Lista con la frase seleccionada, la película correcta y una lista de opciones 
        (incluyendo la correcta y dos al azar).
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