import datetime
import matplotlib
matplotlib.use('Agg') #se usa cuando se guardan gráficas en un archivo (matplot no interactivo)
from flask import Flask, render_template, redirect, url_for, send_file, request
from modules.modulo1 import trivia, guardar_datos_del_juego, mostrar_lista_peliculas, generar_grafica, generar_grafica_circular, generar_graficas_pdf

aciertos = 0
app = Flask("server")
archivo_vacio = False #Se inicializa en false porque el archivo tiene que mostrarse.
contador_repeticiones = 0 #Contador de cuantas preguntas lleva jugando.
frases_utilizadas = [] #Lista donde se guardan las frases que se utilizaron en una trivia.
lista = [] #Donde se guardan los datos de la función trivia [frase, peli ganadora, opciones de peli].
nombre_de_usuario = "" 
numero_de_opciones = 3 #Lo inicializamos en 3 para que no nos muestre el mensaje.
respuesta = None  #Es la respuesta que se muestra para cada opcion.
 #Guarda una línea con los resultados de la trivia.
valores=[]

RUTA ="./data/"
DIRECCION = RUTA + "frases_de_peliculas.txt"

with open (DIRECCION, "r",encoding="utf-8") as f: # lee el archivo con frases y peliculas que luego se 
                                                  # va a pasar como parametro de la función trivia.
    lista1=f.readlines()
    frases_y_pelis=[(linea.strip().split(';')[0], linea.strip().split(';')[1]) for linea in lista1]

try:
    with open ("./data/resultados_historicos.txt", "r",encoding="utf-8") as a: 
        lista_para_graficar=a.readlines()
        lista_para_graficar1=[(linea.strip().split(',')[0], linea.strip().split(',')[1],linea.strip().split(',')[2]) for linea in lista_para_graficar]
except FileNotFoundError:
    with open ("./data/resultados_historicos.txt", "w",encoding="utf-8") as a: 
        pass

@app.route("/",methods=["GET", "POST"]) 
def home():
    global aciertos, contador_repeticiones, fecha_hora, fecha_hora_dt, archivo_vacio, mensaje, nombre_de_usuario, numero_de_opciones
    mensaje = "El número de opciones debe estar entre 3 y 10."

    if request.method == 'POST':
        numero_de_opciones=int(request.form['input_numero'])
        nombre_de_usuario=request.form['input_nombre']

        if numero_de_opciones >= 3 and numero_de_opciones <= 10:
            fecha_hora=datetime.datetime.now().strftime('%d/%m/%y %H:%M')  #Se establece cuando comienza la partida.
            fecha_hora = datetime.datetime.strptime(fecha_hora, '%d/%m/%y %H:%M')
            return redirect(url_for('jugar_trivia'))
        else:
            numero_de_opciones = 0 
            return render_template("home.html", mensaje=mensaje, numero_de_opciones=numero_de_opciones)
        
    aciertos = 0
    archivo_vacio=False #Se dstablece que el archivo no está vacío.
    contador_repeticiones = 0
    frases_utilizadas.clear() #Se eliminan los elementos de la lista.
    return render_template("home.html", mensaje=mensaje, numero_de_opciones=numero_de_opciones)

@app.route("/trivia", methods=["GET", "POST"])
def jugar_trivia():
    global contador_repeticiones, frases_y_pelis,frases_utilizadas, lista, numero_de_opciones
    if contador_repeticiones <= numero_de_opciones:
        lista = trivia(frases_y_pelis,frases_utilizadas)
        contador_repeticiones+=1
        return render_template("trivia.html",lista=lista)
    else:
        return render_template("home.html",numero_de_opciones=numero_de_opciones,nombre_de_usuario=nombre_de_usuario)
    
@app.route("/respuestas", methods=["GET", "POST"])
def respuestas():
    global aciertos, calificacion,fecha_hora_dt, numero_de_opciones, opcion_elegida, respuesta,valores
    if request.method == 'POST':
        opcion_elegida = request.form['opcion_elegida']
    
    #Se compara la opción elegida con la correcta.
    if opcion_elegida == lista[1]:
        aciertos+=1
        calificacion=(f"{aciertos}/{numero_de_opciones}")
        respuesta="¡Correcta!"  
    else:
        calificacion=(f"{aciertos}/{numero_de_opciones}")
        respuesta=(f"¡Incorrecta!, la respuesta correcta es: {lista[1]}.")

    if contador_repeticiones == numero_de_opciones: #Cuando se termina la trivia se guardan los datos en un archivo .txt
        #valores=[aciertos,numero_de_opciones-aciertos,fecha_hora]
        #Se guardan los datos necesarios para graficar.
        guardar_datos_del_juego(nombre_de_usuario, calificacion, fecha_hora)#, valores)
    return render_template("respuestas.html", respuesta=respuesta,calificacion=calificacion, contador_repeticiones=contador_repeticiones, numero_de_opciones=numero_de_opciones)

@app.route("/resultados", methods=["GET", "POST"])
def ver_resultados():
    global advertencia, archivo_vacio, resultados_partidas
    resultados_partidas = []
    advertencia = "No hay resultados para mostrar ya que todavía no empezó la trivia"
    #Manejo de excepciones en el caso de que el archivo no se encuentre creado.
    try: 
        with open ("./data/resultados_historicos.txt", "r") as f:
            for linea in f:
                resultados_partidas.append(linea.split(","))
            if not resultados_partidas: #Si la lista de info de la partida esta vacía  
                archivo_vacio = True    #cambia a True y se muestra la advertiencia.
                advertencia = "No hay resultados para mostrar ya que todavía no empezó la trivia"
    except FileNotFoundError: #Si el archivo no fue creado todavía, se cambia a True.
        archivo_vacio = True
    return render_template("resultados.html", resultados_partidas=resultados_partidas, advertencia=advertencia, archivo_vacio=archivo_vacio)  

@app.route("/graficas", methods=["GET", "POST"])
def ver_resultados_graficos():
    global grafica, grafica_circular, lista_para_graficar1
    if lista_para_graficar: #Si la lista no se encuentra vacía se van a utilizar las funciones para graficar.
        grafica = generar_grafica(lista_para_graficar1)
        grafica_circular = generar_grafica_circular(lista_para_graficar1)
        return render_template("graficas.html", grafica=grafica, grafica_circular=grafica_circular)
    else: #Si no se muestra el siguiente mensaje.
        mensaje_error = "No hay datos disponibles para generar gráficas."
        return render_template("graficas.html", mensaje_error=mensaje_error)

@app.route("/lista_peliculas", methods=["GET", "POST"])
def listar_peliculas():
    lista_peliculas = mostrar_lista_peliculas(lista1)
    return render_template("listar_peliculas.html", lista_peliculas=lista_peliculas)

@app.route('/mostrar_graficas_pdf')
def mostrar_graficas_pdf():
    generar_graficas_pdf(lista_para_graficar)  # Genera las gráficas y luego las guarda en un archivo PDF.
    return send_file("graficas.pdf", as_attachment=True) #Se envia el archivo cuando el usuario seleccione el botón

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')