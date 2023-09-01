from flask import Flask, render_template, request, redirect, url_for
from modules.modulo1 import trivia, guardar_opciones
import datetime
app = Flask("server")
aciertos=0
contador_repeticiones=0
lista=[]
numero_de_opciones = 3
nombre_de_usuario = ""
respuesta=None

RUTA="./data/"
DIRECCION=RUTA + "frases_de_peliculas.txt"

with open (DIRECCION, "r",encoding="utf-8") as f:
    lista1=f.readlines()
    frases_y_pelis=[(linea.strip().split(';')[0], linea.strip().split(';')[1]) for linea in lista1]

@app.route("/",methods=["GET", "POST"])
def home():
    global aciertos
    global contador_repeticiones
    global mensaje
    global nombre_de_usuario 
    global numero_de_opciones
    mensaje = "El número de opciones debe estar entre 3 y 10."

    if request.method == 'POST':
        numero_de_opciones=int(request.form['input_numero'])
        nombre_de_usuario=request.form['input_nombre']
        if numero_de_opciones >= 3 and numero_de_opciones <= 10:
            return redirect(url_for('jugar_trivia'))
        else:
            numero_de_opciones = 0
            return render_template("home.html", mensaje=mensaje, numero_de_opciones=numero_de_opciones)
    aciertos = 0
    contador_repeticiones = 0
    return render_template("home.html", mensaje=mensaje, numero_de_opciones=numero_de_opciones)

@app.route("/trivia", methods=["GET", "POST"])
def jugar_trivia():
    global frases_y_pelis
    global lista
    global numero_de_opciones

    if contador_repeticiones <= numero_de_opciones:
        lista = trivia(frases_y_pelis)
        return render_template("trivia.html",lista=lista)
    
    else:
        return render_template("home.html",numero_de_opciones=numero_de_opciones,nombre_de_usuario=nombre_de_usuario)
    
@app.route("/respuestas", methods=["GET", "POST"])
def respuestas():
    global aciertos
    global calificacion
    global contador_repeticiones
    global numero_de_opciones
    global opcion_elegida
    global respuesta
    contador_repeticiones+=1

    if request.method == 'POST':
        opcion_elegida = request.form['opcion_elegida']
    if opcion_elegida == lista[1]:
        aciertos+=1
        calificacion=(f"{aciertos}/{numero_de_opciones}")
        respuesta="correcta"  
    else:
        calificacion=(f"{aciertos}/{numero_de_opciones}")
        respuesta=(f"incorrecta, la correcta es: {lista[1]}")
    return render_template("respuestas.html", respuesta=respuesta,calificacion=calificacion, contador_repeticiones=contador_repeticiones, numero_de_opciones=numero_de_opciones)


#@app.route("/resultados", methods=["GET", "POST"])
#def ver_resultados():
#    resultados_partidas=[]
#    try:
#        fecha_hora = datetime.datetime.now().strftime('%d/%m/%y %H:%M')
#        calificacion=aciertos/numero_de_opciones
#        resultados_partidas.append(f"{opcion_elegida} - {calificacion} - {fecha_hora}")
#        return render_template("resultados.html", resultados_partidas=resultados_partidas)
#    except KeyError:

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')
    
