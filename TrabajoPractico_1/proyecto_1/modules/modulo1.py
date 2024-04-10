# Módulo para organizar funciones o clases utilizadas en nuestro proyecto
import matplotlib.pyplot as plt
import io, base64, datetime
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime

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
    lista_sin_repetir = []
    for linea in lista_de_pelis_y_frases:
        frase,pelicula=linea.rstrip("\n").split(";") # Separamos la frase y la película.
        lista_sin_repetir.append(pelicula.lower()) # Agregamos las frases en minúscula.

    lista_sin_repetir = sorted(set(lista_sin_repetir)) # Se ordenan alfabéticamente y se eliminan las repetidas.
    return [(i+1, pelicula.capitalize()) for i, pelicula in enumerate(lista_sin_repetir)] #Se indexan las frases.

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

def guardar_datos_del_juego(nombre_de_usuario, calificacion, fecha_hora):
    """Función que toma estos tres parámetros y escribe linea por linea

    Args:
        nombre_de_usuario (text): nombre dado por la persona
        calificacion (str): es una cadena que muestra aciertos/N (N=veces que se juega la trivia)
        fecha_hora (str): fecha y hora en la que se inicializa la trivia
    """
    with open("./data/resultados_historicos.txt", "a") as f:
        f.write(f"{nombre_de_usuario},{calificacion},{fecha_hora}\n")

    
def generar_grafica(lista_de_valores):
    """
    Genera una gráfica lineal de aciertos y desaciertos en función de la fecha.

    Args:
        lista_de_valores (list): lista, en la cual cada linea tiene 3 elementos:
        [0]: nombre del jugador.
        [1]: calificacion. 
        [2]: fecha en la que se llevó a cabo esa partida en formato datetime.datetime.now().

    Returns:
        str: imagen codificada en base64 de la gráfica lineal de aciertos y desaciertos según la fecha.
    """
    resultados_por_fecha = {}

    for valor in lista_de_valores:
        #fecha, hora = valor[2].split(" ")  # Obtener solo la fecha (sin la hora)
        fecha = valor[2].date() #datetime.strptime(fecha, '%Y-%m-%d').date()
        aciertos, total_partidas = map(int, valor[1].split('/'))
        desaciertos = total_partidas - aciertos
        
        if fecha not in resultados_por_fecha:
            resultados_por_fecha[fecha] = [aciertos, desaciertos]
        else:
            resultados_por_fecha[fecha][0] += aciertos
            resultados_por_fecha[fecha][1] += desaciertos
    
    fechas = list(resultados_por_fecha.keys())
    fechas.sort()  # Ordenar las fechas
    aciertos_acumulados = [resultados_por_fecha[fecha][0] for fecha in fechas]
    desaciertos_acumulados = [resultados_por_fecha[fecha][1] for fecha in fechas]
    # Formatear las fechas para mostrar solo el día y el mes
    fechas_formateadas = [fecha.strftime('%d-%m-%Y') for fecha in fechas]  
    plt.figure(figsize=(10, 5))
    plt.plot(fechas_formateadas, aciertos_acumulados, label='Aciertos', marker='o', color='blue')
    plt.plot(fechas_formateadas, desaciertos_acumulados, label='Desaciertos', marker='x', color='red')
    plt.xlabel('Fechas de juego')
    plt.ylabel('Cantidad')
    plt.title('Aciertos y desaciertos acumulados por fecha')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Codificación base64 (devuelve str)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    plt.close()  

    return (imagen_base64)

def generar_grafica_circular(lista_de_valores):
    """
    Genera una gráfica circular que muestra el porcentaje de aciertos y desaciertos.

    Args:
        lista_de_valores (list): lista, en la cual cada linea tiene 3 elementos: en primer lugar, el
        número de aciertos (int), en segundo lugar el número de desaciertos (int), y en tercer lugar la fecha
        en la que se llevó a cabo esa partida en formato datetime.datetime.now().

    Returns:
        str: imagen codificada en base64 de la gráfica circular.
    """
    calificacion=[valor[1].split('/') for valor in lista_de_valores]
    aciertos = [int(i[0]) for i in calificacion]
    desaciertos = [int(i[1])-int(i[0]) for i in calificacion] 
    fig, ax = plt.subplots()
    # Sumamos el total de aciertos y desaciertos.
    aciertos_totales = sum(aciertos) 
    desaciertos_totales = sum(desaciertos)
    ax.pie([aciertos_totales, desaciertos_totales], labels=['Correcto', 'Incorrecto'], autopct='%1.1f%%')
    # Codificacion base64 (devuelve str)
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    imagen_circular_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    plt.close()
    return(imagen_circular_base64)

def generar_graficas_pdf(lista_de_valores):
    """
    Genera un archivo PDF con dos gráficas: una gráfica de líneas que muestra la cantidad de aciertos y desaciertos
    acumulados por fecha de juego, y una gráfica circular que muestra el porcentaje de aciertos y desaciertos.

    Args:
        lista_de_valores (list): lista de tuplas, en la cual cada tupla tiene 3 elementos: en primer lugar, el
        número de aciertos (int), en segundo lugar el número de desaciertos (int), y en tercer lugar la fecha
        en la que se llevó a cabo esa partida en formato datetime.datetime.now().
    """

    resultados_por_fecha = {}


    for valor in lista_de_valores:
        
        #fecha, hora = valor[2].split(" ")  # Obtener solo la fecha (sin la hora)
        fecha = valor[2].date()#datetime.strptime(fecha, '%Y-%m-%d').date()
        aciertos, total_partidas = map(int, valor[1].split('/'))
        desaciertos = total_partidas - aciertos
        
        if fecha not in resultados_por_fecha:
            resultados_por_fecha[fecha] = [aciertos, desaciertos]
        else:
            resultados_por_fecha[fecha][0] += aciertos
            resultados_por_fecha[fecha][1] += desaciertos
    
    fechas = list(resultados_por_fecha.keys())
    fechas.sort()  # Ordenar las fechas
    aciertos_acumulados = [resultados_por_fecha[fecha][0] for fecha in fechas]
    desaciertos_acumulados = [resultados_por_fecha[fecha][1] for fecha in fechas]
    # Formatear las fechas para mostrar solo el día y el mes
    fechas_formateadas = [fecha.strftime('%d-%m-%Y') for fecha in fechas] 
    # Generar gráfica de líneas.
    fig1 = plt.figure(figsize=(10, 5))
    plt.plot(fechas_formateadas, aciertos_acumulados, label='Aciertos', marker='o', color='blue')
    plt.plot(fechas_formateadas, desaciertos_acumulados, label='Desaciertos', marker='x', color='red')
    plt.xlabel('Fechas de juego')
    plt.ylabel('Cantidad')
    plt.title('Aciertos y desaciertos acumulados por fecha')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Generar gráfica circular.
    calificacion=[valor[1].split('/') for valor in lista_de_valores]
    aciertos = [int(i[0]) for i in calificacion]
    desaciertos = [int(i[1])-int(i[0]) for i in calificacion] 
    fig2, ax = plt.subplots()
    # Sumamos el total de aciertos y desaciertos.
    aciertos_totales = sum(aciertos) 
    desaciertos_totales = sum(desaciertos)
    ax.pie([aciertos_totales, desaciertos_totales], labels=['Correcto', 'Incorrecto'], autopct='%1.1f%%')
    # Guardar ambas gráficas en el archivo PDF.

    # Guardar ambas gráficas en el archivo PDF.
    with PdfPages("graficas.pdf") as pdf:
        pdf.savefig(fig2)  # Guardar gráfica circular.
        pdf.savefig(fig1)  # Guardar gráfica lineal.
    # Cerrar las figuras antes de guardarlas en el PDF.
    plt.close(fig2)
    plt.close(fig1)
