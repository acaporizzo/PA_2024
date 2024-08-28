import datetime
from flask import Flask, render_template, redirect, url_for, send_file, request
#from modules.modulo1 import trivia, guardar_datos_del_juego, mostrar_lista_peliculas, generar_grafica, generar_grafica_circular, generar_graficas_pdf
from modules.servicio import mostrar_lista_peliculas, mostrar_resultados, datos_del_usuario, juego_trivia, resultado_de_respuesta, generar_grafica_lineal, generar_grafica_circular, generar_graficas_pdf

aciertos = 0
app = Flask("server")
archivo_vacio = False # Se inicializa en false porque el archivo tiene que mostrarse.
contador_repeticiones = 0 # Contador de cuantas preguntas lleva jugando.

lista = [] # Donde se guardan los datos de la función trivia [frase, peli ganadora, opciones de peli].
numero_de_opciones = 3 # Lo inicializamos en 3 para que no nos muestre el mensaje.
respuesta = None  # Es la respuesta que se muestra para cada opción.
valores = [] # Guarda una línea con los resultados de la trivia.

RUTA = "./data/"
DIRECCION = RUTA + "frases_de_peliculas.txt"
DIRECCION2 = RUTA + "resultados_historicos.txt"

@app.route("/", methods=["GET", "POST"]) 
def home():
    global aciertos, contador_repeticiones, usuario, archivo_vacio, mensaje, metodo, numero_de_opciones
    mensaje = "El número de opciones debe estar entre 3 y 10."
    metodo = "POST"
    if numero_de_opciones >= 3 and numero_de_opciones <= 10:
        usuario = datos_del_usuario (metodo) 
        redirect(url_for('jugar_trivia'))
        return render_template("home.html", mensaje=mensaje, numero_de_opciones=usuario[0])
    else:
        numero_de_opciones = 0 
        return render_template("home.html", mensaje=mensaje, numero_de_opciones=usuario[0])
        
aciertos = 0
archivo_vacio = False # Se establece que el archivo no está vacío.
contador_repeticiones = 0

@app.route("/trivia", methods=["GET", "POST"])
def jugar_trivia():
    global contador_repeticiones, lista, usuario
    if contador_repeticiones <= usuario[0]:
        lista = juego_trivia(DIRECCION)
        contador_repeticiones += 1
        return render_template("trivia.html", lista=lista)
    else:
        return render_template("home.html", numero_de_opciones=usuario[0])
    
@app.route("/respuestas", methods=["GET", "POST"])
def respuestas():
    global aciertos, respuesta
    resultado = resultado_de_respuesta(metodo, lista, usuario, contador_repeticiones)
    return render_template("respuestas.html", respuesta=resultado[0], calificacion=resultado[1], contador_repeticiones=contador_repeticiones, numero_de_opciones=usuario[0])

@app.route("/resultados", methods=["GET", "POST"])
def ver_resultados():
    global advertencia, archivo_vacio, resultados_partidas
    resultados_partidas = []
    advertencia = "No hay resultados para mostrar ya que todavía no empezó la trivia"
    # Manejo de excepciones en el caso de que el archivo no se encuentre creado.
    try: 
        resultados_partidas1 = mostrar_resultados (DIRECCION2, resultados_partidas)
        if not resultados_partidas: # Si la lista de info de la partida está vacía.
            archivo_vacio = True    # Cambia a True y se muestra la advertencia.
            advertencia = "No hay resultados para mostrar ya que todavía no empezó la trivia"
    except FileNotFoundError: # Si el archivo no fue creado todavía, se cambia a True.
        archivo_vacio = True
    return render_template("resultados.html", resultados_partidas1=resultados_partidas1, advertencia=advertencia, archivo_vacio=archivo_vacio)  

@app.route("/graficas", methods=["GET", "POST"])
def ver_resultados_graficos():
    global grafica, grafica_circular
    if lista_para_graficar1: # Si la lista no se encuentra vacía se van a utilizar las funciones para graficar.
        grafica = generar_grafica_lineal(lista_para_graficar1)
        grafica_circular = generar_grafica_circular(lista_para_graficar1)
        return render_template("graficas.html", grafica=grafica, grafica_circular=grafica_circular)
    else: # Si no hay lista aún se muestra el siguiente mensaje.
        mensaje_error = "No hay datos disponibles para generar gráficas."
        return render_template("graficas.html", mensaje_error=mensaje_error)

@app.route("/lista_peliculas", methods=["GET", "POST"])
def listar_peliculas():
    lista_peliculas = mostrar_lista_peliculas(DIRECCION)
    return render_template("listar_peliculas.html", lista_peliculas=lista_peliculas)

@app.route('/mostrar_graficas_pdf')
def mostrar_graficas_pdf():
    global lista_para_graficar1
    try:
        with open("./data/resultados_historicos.txt", "r", encoding="utf-8") as a: # Leemos el archivo otra vez para actualizar con los nuevos resultados
            lista_para_graficar = a.readlines()
            lista_para_graficar1 = [(linea.strip().split(',')[0], linea.strip().split(',')[1], datetime.datetime.strptime(linea.strip().split(',')[2], '%d-%m-%y %H:%M:%S')) for linea in lista_para_graficar]
    except FileNotFoundError:
        with open("./data/resultados_historicos.txt", "w", encoding="utf-8") as a: 
            pass
    generar_graficas_pdf(lista_para_graficar1)  # Genera las gráficas y luego las guarda en un archivo PDF.
    return send_file("graficas.pdf", as_attachment=True) # Se envía el archivo cuando el usuario seleccione el botón

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')
