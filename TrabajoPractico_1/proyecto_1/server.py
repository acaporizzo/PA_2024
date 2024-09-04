from flask import render_template, redirect, url_for, send_file, request
from modules.servicio import mostrar_lista_peliculas, obtener_datos_graficas, mostrar_resultados, jugar_juego_trivia, generar_grafica_lineal, generar_grafica_circular, generar_graficas_pdf
from modules.auxiliar import obtener_datos_del_usuario, devolver_resultado_de_respuesta
from modules.config import app
aciertos = 0
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
    aciertos = 0
    contador_repeticiones = 0

    if request.method == "POST":
        usuario = obtener_datos_del_usuario(metodo)
        
        # Verificar si el usuario ha ingresado un número válido de repeticiones
        if usuario and 3 <= usuario[0] <= 10:
            numero_de_opciones = usuario[0]
            return redirect(url_for('jugar_trivia'))  # Redirige a la ruta de jugar trivia
        else:
            # Muestra un mensaje de error si el número de repeticiones está fuera del rango permitido
            mensaje = "Error: El número de opciones debe estar entre 3 y 10."
            return render_template("home.html", mensaje=mensaje, numero_de_opciones=0)

    # Mostrar la página inicial sin errores para solicitudes GET
    return render_template("home.html", mensaje="", numero_de_opciones=numero_de_opciones)


@app.route("/trivia", methods=["GET", "POST"])
def jugar_trivia():
    global contador_repeticiones, lista, usuario
    if contador_repeticiones <= usuario[0]:
        lista = jugar_juego_trivia(DIRECCION)
        contador_repeticiones += 1
        return render_template("trivia.html", lista=lista)
    else:
        return render_template("home.html", numero_de_opciones=usuario[0])
    
@app.route("/respuestas", methods=["GET", "POST"])
def respuestas():
    global aciertos, respuesta
    resultado, aciertos = devolver_resultado_de_respuesta (metodo, lista, usuario, contador_repeticiones, aciertos)
    return render_template("respuestas.html", respuesta=resultado[0], calificacion=resultado[1], contador_repeticiones=contador_repeticiones, numero_de_opciones=usuario[0])

@app.route("/resultados", methods=["GET", "POST"])
def ver_resultados():
    global advertencia, archivo_vacio, resultados_partidas
    resultados_partidas = []
    advertencia = "No hay resultados para mostrar ya que todavía no empezó la trivia"
    
    try: 
        resultados_partidas = mostrar_resultados(DIRECCION2, resultados_partidas)
        if not resultados_partidas:  # Si la lista de info de la partida está vacía.
            archivo_vacio = True    # Cambia a True y se muestra la advertencia.
            advertencia = "No hay resultados para mostrar ya que todavía no empezó la trivia"
    except FileNotFoundError:  # Si el archivo no fue creado todavía, se cambia a True.
        archivo_vacio = True
    
    return render_template("resultados.html", resultados_partidas1=resultados_partidas, advertencia=advertencia, archivo_vacio=archivo_vacio)

@app.route("/graficas", methods=["GET", "POST"])
def ver_resultados_graficos():
    global grafica, grafica_circular, lista_para_graficar1
    
    lista_para_graficar1 = obtener_datos_graficas(DIRECCION2)

    if lista_para_graficar1:  # Si la lista no se encuentra vacía, generar las gráficas
        grafica = generar_grafica_lineal(DIRECCION2)
        grafica_circular = generar_grafica_circular(DIRECCION2)
        return render_template("graficas.html", grafica=grafica, grafica_circular=grafica_circular)
    else:  # Si no hay lista aún, muestra el siguiente mensaje
        mensaje_error = "No hay datos disponibles para generar gráficas."
        return render_template("graficas.html", mensaje_error=mensaje_error)

@app.route("/lista_peliculas", methods=["GET", "POST"])
def listar_peliculas():
    lista_peliculas = mostrar_lista_peliculas(DIRECCION)
    return render_template("listar_peliculas.html", lista_peliculas=lista_peliculas)

@app.route('/mostrar_graficas_pdf')
def mostrar_graficas_pdf():
    global lista_para_graficar1

    # Verificar y generar el PDF utilizando la función en servicio
    graficas_pdf = generar_graficas_pdf(lista_para_graficar1)

    if graficas_pdf:
        try:
            # Asegúrate de que la ruta es correcta y envía el archivo
            return send_file(graficas_pdf, as_attachment=True, download_name="graficas.pdf")
        except FileNotFoundError:
            # Manejo de error si el archivo no se encuentra
            return "El archivo PDF no se pudo encontrar o generar.", 404
    else:
        return "No hay datos disponibles para generar el PDF.", 400


if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')
