from flask import render_template, request, redirect, url_for
from modules.config import app
from modules.modulo1 import trivia

@app.route("/")
def home():
    esta_vacia = False
    # opción 1
    # if request.method == 'POST':
    #     nombre = request.form['input_nombre']
    #     autor = request.form['input_autor']
    #     puntaje = request.form['input_puntaje']
    #     agregar_libro_a_lista(lista_libros, nombre, autor, puntaje)
    #     guardar_libro_en_archivo(ARCHIVO, nombre, autor, puntaje)

    if len(lista_libros) == 0:
        esta_vacia = True

    return render_template('home.html', esta_vacia=esta_vacia, lista_libros=lista_libros)

@app.route("/trivia", methods=["GET", "POST"])
def agregar():
    # opción 2
    if request.method == 'POST':
        nombre = request.form['input_nombre']
        autor = request.form['input_autor']
        puntaje = request.form['input_puntaje']
        agregar_libro_a_lista(lista_libros, nombre, autor, puntaje)
        guardar_libro_en_archivo(ARCHIVO, nombre, autor, puntaje)

        return redirect( url_for('home') )

    return render_template('agregar.html')


if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')
