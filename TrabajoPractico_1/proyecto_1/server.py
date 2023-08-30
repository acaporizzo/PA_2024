from flask import Flask, render_template, request, redirect, url_for
app = Flask("server")
from modules.modulo1 import trivia, guardar_opciones

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

@app.route("/trivia", methods=["GET", "POST"])
def jugar_trivia():
    global frases_y_pelis
    global opcion_elegida
    resultado=None
    opcion_elegida = request.form.get('opcion_elegida')
    if opcion_elegida is None:
        return "Opción no seleccionada", 400
    for i in range(1,numero_de_opciones+1):
        lista = trivia(frases_y_pelis)
    if opcion_elegida == lista[1]:
        resultado = "¡Correcto!"
    else:
        resultado = "Incorrecto"
    
    return render_template("trivia.html", lista=lista, resultado=resultado)

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')
    
