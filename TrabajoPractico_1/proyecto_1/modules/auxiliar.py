#Módulo para funciones auxiliares
from modules.persistencia import guardar_datos_del_juego
import datetime
from flask import request

def obtener_datos_del_usuario(metodo):
    if request.method == metodo:
        numero_de_opciones = int(request.form['input_numero'])
        nombre_de_usuario = request.form['input_nombre']
        fecha_hora = datetime.datetime.now().strftime('%d/%m/%y %H:%M')  # Establece cuando comienza la partida.
        fecha_hora = datetime.datetime.strptime(fecha_hora, '%d/%m/%y %H:%M')
        usuario = [numero_de_opciones, nombre_de_usuario, fecha_hora]
        return (usuario)

def devolver_resultado_de_respuesta(metodo, lista, usuario, contador_repeticiones, aciertos):
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