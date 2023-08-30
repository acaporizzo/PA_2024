from flask import Flask, render_template, request, redirect, url_for
app = Flask("server")
from modules.modulo1 import trivia, guardar_opciones, trivia2
import datetime
lista=[]
numero_de_opciones=0
RUTA="./data/"
DIRECCION=RUTA + "frases_de_peliculas.txt"

with open (DIRECCION, "r",encoding="utf-8") as f:
    lista1=f.readlines()
    frases_y_pelis=[(linea.strip().split(';')[0], linea.strip().split(';')[1]) for linea in lista1]

@app.route("/",methods=["GET", "POST"])
def home():
    global numero_de_opciones
    global nombre_de_usuario 
    if request.method == 'POST':
        numero_de_opciones=int(request.form['input_numero'])
        nombre_de_usuario=request.form['input_nombre']
        if numero_de_opciones>=3 and numero_de_opciones<=10:
            return redirect( url_for('jugar_trivia') )
        else:
            mensaje = "El número de opciones debe estar entre 3 y 10."
            return render_template("home.html", mensaje=mensaje)
    return render_template("home.html")

#@app.route("/borrar", methods=["GET", "POST"])
#def borrar():
    #global opcion_elegida
    
    #for i in range(1,numero_de_opciones+1):
        #lista = trivia(frases_y_pelis)
    #if request.method == 'POST':
        #opcion_elegida = request.form['opcion_elegida']
    #return render_template("borrar.html", lista=lista)

@app.route("/trivia", methods=["GET", "POST"])
def jugar_trivia():
    global frases_y_pelis
    global opcion_elegida
    for i in range(1,numero_de_opciones+1):
        lista = trivia(frases_y_pelis)
        return render_template("trivia.html",lista=lista)
    return redirect( url_for('home') )
    
@app.route("/respuestas", methods=["GET", "POST"])
def respuestas():
    global aciertos
    global numero_de_opciones
    global opcion_elegida
    global lista
    aciertos=0
    
    lista = trivia(frases_y_pelis)
    if request.method == 'POST':
        opcion_elegida = request.form['opcion_elegida']
    if opcion_elegida == lista[1]:
        aciertos+=1
        calificacion=(f"{aciertos}/{numero_de_opciones}")
        respuesta="correcta"  
    else:
        calificacion=(f"{aciertos}/{numero_de_opciones}")
        respuesta=(f"incorrecta, la correcta es: {lista[1]}")
    return render_template("respuestas.html", respuesta=respuesta,calificacion=calificacion)


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
    
