from modules.cajon import Cajon
from modules.cinta_transportadora import Cinta_Transportadora
from flask import Flask, render_template,request
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    cinta_transportadora = Cinta_Transportadora()
    n_alimentos= int(request.form.get("usuario", 0))
    lista_alimentos= cinta_transportadora.clasificar_alimentos(n_alimentos)
    cajon_de_n_alimentos = Cajon(lista_alimentos)

    #Calculamos el aw de cada alimento de la lista. El valor de aw se agrega a una lista correspondiente al 
    #tipo de alimento del que se trata. Las listas se ubican en el diccionario, en la posición del tipo de alimento.
    diccionario_con_listas_aw = cajon_de_n_alimentos.agregar_y_calcular_aw(lista_alimentos)

    #Creamos las listas con los valores de aw de frutas, verduras y total
    lista_aw_frutas = (diccionario_con_listas_aw["Kiwi"] + diccionario_con_listas_aw["Manzana"])
    lista_aw_verduras = (diccionario_con_listas_aw["Papa"] + diccionario_con_listas_aw["Zanahoria"])
    lista_total = lista_aw_frutas + lista_aw_verduras

    #Obtenemos un diccionario con los promedios de aw para cada tipo de alimento, y separamos los valores en variables
    promedios = cajon_de_n_alimentos.calcular_aw_prom_diccionario(diccionario_con_listas_aw)

    awk = promedios["Kiwi"]
    awm = promedios["Manzana"]
    awp = promedios["Papa"]
    awz = promedios["Zanahoria"]

    #Obtenemos los promedios de aw para las listas creadas anteriormente
    awf = cajon_de_n_alimentos.calcular_aw_prom(lista_aw_frutas)
    awv = cajon_de_n_alimentos.calcular_aw_prom(lista_aw_verduras)
    awt = cajon_de_n_alimentos.calcular_aw_prom(lista_total)

    return render_template("home.html",awk=awk, awm=awm, awp=awp, awz=awz, awf=awf, awv=awv, awt=awt)

if __name__ == "__main__":
    app.run(debug=True)
