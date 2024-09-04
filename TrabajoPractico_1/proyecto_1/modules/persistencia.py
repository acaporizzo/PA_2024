import datetime

def leer_archivo(DIRECCION):
    with open (DIRECCION, "r", encoding="utf-8") as f: # lee el archivo con frases y peliculas que luego se 
                                                  # va a pasar como parámetro de la función trivia.
        lista1 = f.readlines()
        frases_y_pelis = [(linea.strip().split(';')[0], linea.strip().split(';')[1]) for linea in lista1]
    return (frases_y_pelis)

def leer_archivo_resultados(DIRECCION2):
    """
    Lee un archivo de resultados, organizando los datos en una lista de tuplas con nombre, calificación y fecha.

    Args:
        DIRECCION2 (str): Ruta del archivo a leer, que contiene resultados separados por comas.

    Returns:
        list: Lista de tuplas con los resultados, cada una contiene el nombre (str), calificación (str) 
              y fecha (datetime). Si el archivo no existe, lo crea y retorna una lista vacía.
    """
    try:
        with open(DIRECCION2, "r", encoding="utf-8") as a: 
            lista_de_resultados = a.readlines()
            lista_de_resultados1 = [(linea.strip().split(',')[0], linea.strip().split(',')[1], 
                 datetime.datetime.strptime(linea.strip().split(',')[2], '%Y-%m-%d %H:%M:%S')) for linea in lista_de_resultados]
            return (lista_de_resultados1)
    except FileNotFoundError:
        with open(DIRECCION2, "w", encoding="utf-8") as a: 
            pass
        return []

def guardar_datos_del_juego(nombre_de_usuario, calificacion, fecha_hora):
    with open("./data/resultados_historicos.txt", "a") as f:
        f.write(f"{nombre_de_usuario},{calificacion},{fecha_hora}\n")