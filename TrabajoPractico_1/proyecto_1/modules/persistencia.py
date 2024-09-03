import datetime

def leer_archivo(DIRECCION):
    with open (DIRECCION, "r", encoding="utf-8") as f: # lee el archivo con frases y peliculas que luego se 
                                                  # va a pasar como parámetro de la función trivia.
        lista1 = f.readlines()
        frases_y_pelis = [(linea.strip().split(';')[0], linea.strip().split(';')[1]) for linea in lista1]
    return (frases_y_pelis)

def leer_archivo2(DIRECCION2):
    try:
        with open(DIRECCION2, "r", encoding="utf-8") as a: 
            lista_de_resultados = a.readlines()
            lista_de_resultados1 = [
                (
                    linea.strip().split(',')[0], 
                    linea.strip().split(',')[1], 
                    # Mantener el formato como objeto datetime
                    datetime.datetime.strptime(linea.strip().split(',')[2], '%Y-%m-%d %H:%M:%S')
                ) 
                for linea in lista_de_resultados
            ]
            return lista_de_resultados1
    except FileNotFoundError:
        with open(DIRECCION2, "w", encoding="utf-8") as a: 
            pass
        return []  # Devuelve una lista vacía si no se encuentra el archivo



def guardar_datos_del_juego(nombre_de_usuario, calificacion, fecha_hora):
    """Función que toma estos tres parámetros y escribe linea por linea

    Args:
        nombre_de_usuario (text): nombre dado por la persona
        calificacion (str): es una cadena que muestra aciertos/N (N=veces que se juega la trivia)
        fecha_hora (str): fecha y hora en la que se inicializa la trivia
    """
    with open("./data/resultados_historicos.txt", "a") as f:
        f.write(f"{nombre_de_usuario},{calificacion},{fecha_hora}\n")



