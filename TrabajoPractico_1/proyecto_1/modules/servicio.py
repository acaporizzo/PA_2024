from flask import Flask, render_template, redirect, url_for, send_file, request
import matplotlib.pyplot as plt
import io, base64, datetime
from matplotlib.backends.backend_pdf import PdfPages
from modules.dominio import trivia
from modules.persistencia import leer_archivo2, leer_archivo, guardar_datos_del_juego
frases_utilizadas = [] # Lista donde se guardan las frases que ya se utilizaron en una trivia.
usuario=[]

def datos_del_usuario(metodo):
    if request.method == metodo:
        numero_de_opciones = int(request.form['input_numero'])
        nombre_de_usuario = request.form['input_nombre']
        # Corregir el uso de datetime:
        fecha_hora = datetime.datetime.now().strftime('%d/%m/%y %H:%M')  # Establece cuando comienza la partida.
        fecha_hora = datetime.datetime.strptime(fecha_hora, '%d/%m/%y %H:%M')
        usuario = [numero_de_opciones, nombre_de_usuario, fecha_hora]
        return usuario


def juego_trivia (DIRECCION):
    lista_frases_y_pelis = leer_archivo(DIRECCION)
    lista_para_jugar = trivia(lista_frases_y_pelis,frases_utilizadas)

    return(lista_para_jugar)
    
def resultado_de_respuesta(metodo, lista, usuario, contador_repeticiones, aciertos):
    if request.method == metodo:
        opcion_elegida = request.form['opcion_elegida']
    
    if opcion_elegida == lista[1]:
        aciertos += 1
        calificacion = f"{aciertos}/{usuario[0]}"
        respuesta = "¡Correcta!"  
    else:
        calificacion = f"{aciertos}/{usuario[0]}"
        respuesta = f"¡Incorrecta!, la respuesta correcta es: {lista[1]}."
    
    if contador_repeticiones == usuario[0]:
        guardar_datos_del_juego(usuario[1], calificacion, usuario[2])
    
    resultado = [respuesta, calificacion]
    return resultado, aciertos  # Devuelve 'aciertos' actualizado

def mostrar_resultados(DIRECCION2, resultados_partidas):
    lista_de_resultados = leer_archivo2(DIRECCION2)
    for linea in lista_de_resultados:
        resultados_partidas.append(linea)  # 'linea' ya es una tupla, no es necesario usar 'split'
    return resultados_partidas


def mostrar_lista_peliculas(DIRECCION):
    """
    Esta función recibe una lista con todos los datos y devuelve una lista de tuplas

    Args:
        DIRECCION (str): Ruta del archivo que contiene las frases y películas.

    Returns:
        lista: contiene todas las películas ordenadas alfabéticamente donde se eliminaron las repetidas
        y se indexaron.
    """
    lista_de_pelis_y_frases = leer_archivo(DIRECCION)
    lista_sin_repetir = []

    for frase, pelicula in lista_de_pelis_y_frases:
        lista_sin_repetir.append(pelicula.lower())  # Agregamos las películas en minúscula.

    lista_sin_repetir = sorted(set(lista_sin_repetir))  # Ordenar alfabéticamente y eliminar duplicados.
    return [(i + 1, pelicula.capitalize()) for i, pelicula in enumerate(lista_sin_repetir)]  # Indexar las películas.

# servicio.py

from modules.persistencia import leer_archivo2

def obtener_datos_graficas(direccion):
    """
    Obtiene los datos necesarios para generar las gráficas de resultados.

    Args:
        direccion (str): Ruta al archivo de resultados históricos.

    Returns:
        list: Lista de tuplas con los datos de los resultados históricos.
    """
    try:
        lista_para_graficar1 = leer_archivo2(direccion)
        return lista_para_graficar1
    except FileNotFoundError:
        # Retorna una lista vacía si el archivo no existe
        return []

def generar_grafica_lineal (DIRECCION2):
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
    lista_para_graficar1 = leer_archivo2(DIRECCION2)
    for valor in lista_para_graficar1:
        fecha = valor[2].date() #Extrae sólo la fecha, sin la hora.
        aciertos, total_partidas = map(int, valor[1].split('/'))
        desaciertos = total_partidas - aciertos
        
        if fecha not in resultados_por_fecha:
            resultados_por_fecha[fecha] = [aciertos, desaciertos]
        else:
            resultados_por_fecha[fecha][0] += aciertos
            resultados_por_fecha[fecha][1] += desaciertos
    
    fechas = list(resultados_por_fecha.keys())
    fechas.sort()  #Ordenar las fechas
    aciertos_acumulados = [resultados_por_fecha[fecha][0] for fecha in fechas]
    desaciertos_acumulados = [resultados_por_fecha[fecha][1] for fecha in fechas]
    #Formatear las fechas para mostrar solo el día y el mes
    fechas_formateadas = [fecha.strftime('%d-%m-%Y') for fecha in fechas]  
    #Graficamos la curva lineal
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


def generar_grafica_circular(DIRECCION2):
 
    lista_para_graficar1 = leer_archivo2(DIRECCION2)
    calificacion=[valor[1].split('/') for valor in lista_para_graficar1]
    aciertos = [int(i[0]) for i in calificacion]
    desaciertos = [int(i[1])-int(i[0]) for i in calificacion] 
    fig, ax = plt.subplots()
    #Sumamos el total de aciertos y desaciertos.
    aciertos_totales = sum(aciertos) 
    desaciertos_totales = sum(desaciertos)
    ax.pie([aciertos_totales, desaciertos_totales], labels=['Correcto', 'Incorrecto'], autopct='%1.1f%%')
    #Codificacion base64 (devuelve str)
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    imagen_circular_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    plt.close()
    return(imagen_circular_base64)

def generar_graficas_pdf(DIRECCION2):

    #Generar gráfica lineal:
    resultados_por_fecha = {}
    lista_para_graficar1 = leer_archivo2(DIRECCION2)
    for valor in lista_para_graficar1:
        fecha = valor[2].date() #Extrae sólo la fecha, sin la hora.
        aciertos, total_partidas = map(int, valor[1].split('/'))
        desaciertos = total_partidas - aciertos
        
        if fecha not in resultados_por_fecha:
            resultados_por_fecha[fecha] = [aciertos, desaciertos]
        else:
            resultados_por_fecha[fecha][0] += aciertos
            resultados_por_fecha[fecha][1] += desaciertos
    
    fechas = list(resultados_por_fecha.keys())
    fechas.sort()  #Ordenar las fechas
    aciertos_acumulados = [resultados_por_fecha[fecha][0] for fecha in fechas]
    desaciertos_acumulados = [resultados_por_fecha[fecha][1] for fecha in fechas]
    #Formatear las fechas para mostrar solo el día y el mes
    fechas_formateadas = [fecha.strftime('%d-%m-%Y') for fecha in fechas]  
    #Graficamos la curva lineal
    lista_para_graficar1 = leer_archivo2(DIRECCION2)
    calificacion=[valor[1].split('/') for valor in lista_para_graficar1]
    aciertos = [int(i[0]) for i in calificacion]
    desaciertos = [int(i[1])-int(i[0]) for i in calificacion] 
    fig1, ax = plt.subplots()
    #Sumamos el total de aciertos y desaciertos.
    aciertos_totales = sum(aciertos) 
    desaciertos_totales = sum(desaciertos)
    ax.pie([aciertos_totales, desaciertos_totales], labels=['Correcto', 'Incorrecto'], autopct='%1.1f%%')
    #Generar gráfica circular.
    calificacion=[valor[1].split('/') for valor in lista_para_graficar1]
    aciertos = [int(i[0]) for i in calificacion]
    desaciertos = [int(i[1])-int(i[0]) for i in calificacion] 
    fig2, ax = plt.subplots()
    aciertos_totales = sum(aciertos) 
    desaciertos_totales = sum(desaciertos)
    ax.pie([aciertos_totales, desaciertos_totales], labels=['Correcto', 'Incorrecto'], autopct='%1.1f%%')
    #Guardar ambas gráficas en el archivo PDF.
    with PdfPages("graficas.pdf") as pdf:
        pdf.savefig(fig1)  # Guardar gráfica circular.
        pdf.savefig(fig2)  # Guardar gráfica lineal.
    #Cerrar las figuras antes de guardarlas en el PDF.
    plt.close(fig1)
    plt.close(fig2)