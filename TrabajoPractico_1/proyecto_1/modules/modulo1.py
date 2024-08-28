# Módulo para organizar funciones o clases utilizadas en nuestro proyecto
import matplotlib.pyplot as plt
import io, base64, datetime
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime

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

def generar_graficas_pdf(lista_de_valores):
    """
    Genera un archivo PDF con dos gráficas: una gráfica de líneas que muestra la cantidad de aciertos y desaciertos
    acumulados por fecha de juego, y una gráfica circular que muestra el porcentaje de aciertos y desaciertos.

    Args:
        lista_de_valores (list): lista de tuplas, en la cual cada tupla tiene 3 elementos: en primer lugar, el
        número de aciertos (int), en segundo lugar el número de desaciertos (int), y en tercer lugar la fecha
        en la que se llevó a cabo esa partida en formato datetime.datetime.now().
    """
    #Generar gráfica lineal:
    resultados_por_fecha = {}
    for valor in lista_de_valores:
        fecha = valor[2].date()
        aciertos, total_partidas = map(int, valor[1].split('/'))
        desaciertos = total_partidas - aciertos
        if fecha not in resultados_por_fecha:
            resultados_por_fecha[fecha] = [aciertos, desaciertos]
        else:
            resultados_por_fecha[fecha][0] += aciertos
            resultados_por_fecha[fecha][1] += desaciertos
    fechas = list(resultados_por_fecha.keys())
    fechas.sort()
    aciertos_acumulados = [resultados_por_fecha[fecha][0] for fecha in fechas]
    desaciertos_acumulados = [resultados_por_fecha[fecha][1] for fecha in fechas]
    fechas_formateadas = [fecha.strftime('%d-%m-%Y') for fecha in fechas] 
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
    #Generar gráfica circular.
    calificacion=[valor[1].split('/') for valor in lista_de_valores]
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