from flask import Flask, render_template, request, redirect, url_for
from modules.modulo1 import trivia, guardar_datos_del_juego
import datetime
aciertos=0
app = Flask("server")
contador_repeticiones=0
info = False 
guardado = False 
lista=[]
nombre_de_usuario = "" 
numero_de_opciones = 3 
respuesta=None 
resultados_partidas=[]

RUTA="./data/"
DIRECCION=RUTA + "frases_de_peliculas.txt"

with open (DIRECCION, "r",encoding="utf-8") as f:
    lista1=f.readlines()
    frases_y_pelis=[(linea.strip().split(';')[0], linea.strip().split(';')[1]) for linea in lista1]
with open("./data/resultados_historicos.txt", "w"):
        pass

@app.route("/",methods=["GET", "POST"]) 
def home():
    global aciertos, contador_repeticiones, fecha_hora, guardado, info, mensaje, nombre_de_usuario, numero_de_opciones
    mensaje = "El número de opciones debe estar entre 3 y 10."
    if request.method == 'POST':
        numero_de_opciones=int(request.form['input_numero'])
        nombre_de_usuario=request.form['input_nombre']

        if numero_de_opciones >= 3 and numero_de_opciones <= 10: 
            guardado = False
            fecha_hora = datetime.datetime.now().strftime('%d/%m/%y %H:%M')
            return redirect(url_for('jugar_trivia'))
        else:
            numero_de_opciones = 0
            return render_template("home.html", mensaje=mensaje, numero_de_opciones=numero_de_opciones)
    
    aciertos = 0
    contador_repeticiones = 0
    info=False
    return render_template("home.html", mensaje=mensaje, numero_de_opciones=numero_de_opciones)

@app.route("/trivia", methods=["GET", "POST"])
def jugar_trivia():
    global contador_repeticiones, frases_y_pelis, guardado, lista, numero_de_opciones

    if contador_repeticiones <= numero_de_opciones:
        lista = trivia(frases_y_pelis)
        contador_repeticiones+=1
        return render_template("trivia.html",lista=lista)
    else:
        guardar_datos_del_juego(nombre_de_usuario, calificacion, fecha_hora)
        guardado = True
        return render_template("home.html",numero_de_opciones=numero_de_opciones,nombre_de_usuario=nombre_de_usuario)
@app.route("/respuestas", methods=["GET", "POST"])
def respuestas():
    global aciertos, calificacion, guardado, numero_de_opciones, opcion_elegida, respuesta
    

    if request.method == 'POST':
        opcion_elegida = request.form['opcion_elegida']

    if opcion_elegida == lista[1]:
        aciertos+=1
        calificacion=(f"Su calificación es: {aciertos}/{numero_de_opciones}")
        respuesta="¡Correcta!"  

    else:
        calificacion=(f"Su calificación es: {aciertos}/{numero_de_opciones}")
        respuesta=(f"¡Incorrecta!, la respuesta correcta es: {lista[1]}.")

    if contador_repeticiones==numero_de_opciones:
        guardar_datos_del_juego(nombre_de_usuario, calificacion, fecha_hora)
    return render_template("respuestas.html", respuesta=respuesta,calificacion=calificacion, contador_repeticiones=contador_repeticiones, numero_de_opciones=numero_de_opciones)

@app.route("/resultados", methods=["GET", "POST"])
def ver_resultados():
    global advertencia, guardado, info, resultados_partidas
    advertencia = "No hay resultados para mostrar ya que todavía no empezó la trivia"

    try: 
        with open ("./data/resultados_historicos.txt", "r") as f:
            resultados_partidas=f.readlines()
            if not resultados_partidas:
                info = True
                advertencia = "No hay resultados para mostrar ya que todavía no empezó la trivia"
    except FileNotFoundError: 
        info = True
        
    return render_template("resultados.html", resultados_partidas=resultados_partidas, advertencia=advertencia, info=info)  

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')