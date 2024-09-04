#Módulo para funciones auxiliares

from modules.persistencia import guardar_datos_del_juego
from flask import request
import datetime

def obtener_datos_del_usuario(metodo):
    """
    Obtiene los datos del usuario desde un formulario web y los organiza en una lista.

    Args:
        metodo (str): Método HTTP esperado para el formulario.

    Returns:
        list: Una lista con el número de opciones seleccionadas, el nombre del usuario y la fecha y hora actual.
    """
    if request.method == metodo:
        numero_de_opciones = int(request.form['input_numero'])
        nombre_de_usuario = request.form['input_nombre']
        fecha_hora = datetime.datetime.now().strftime('%d/%m/%y %H:%M')  # Establece cuando comienza la partida.
        fecha_hora = datetime.datetime.strptime(fecha_hora, '%d/%m/%y %H:%M')
        usuario = [numero_de_opciones, nombre_de_usuario, fecha_hora]
        return (usuario)

def devolver_resultado_de_respuesta(metodo, lista, usuario, contador_repeticiones, aciertos):
    """
    Procesa la respuesta del usuario y determina si es correcta o incorrecta, actualizando los aciertos.

    Args:
        metodo (str): Método HTTP esperado para el formulario.
        lista (list): Lista que contiene la frase mostrada y la opción correcta.
        usuario (list): Lista con el número de opciones, nombre del usuario y la fecha y hora de inicio.
        contador_repeticiones (int): Contador de repeticiones del juego.
        aciertos (int): Número actual de aciertos del usuario.

    Returns:
        tuple: Una tupla con la lista de resultados (mensaje y calificación) y los aciertos actualizados.
    """
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
    return (resultado, aciertos)  # Devuelve 'aciertos' actualizado