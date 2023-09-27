from flask import Flask, render_template,request
app= Flask(__name__)
from modules.cajon import Cajon
from modules.cinta_transportadora import Cinta_Transportadora

@app.route("/", methods=['GET', 'POST'])
def home():
    n_alimentos= int(request.form.get('usuario', 0))
    cinta_transportadora = Cinta_Transportadora()
    lista_alimentos= cinta_transportadora.clasificar_alimentos(n_alimentos)
    cajon_de_n_alimentos = Cajon(lista_alimentos)

    diccionario_con_listas_aw = cajon_de_n_alimentos.agregar_y_calcular_aw(lista_alimentos)
    lista_aw_frutas = (diccionario_con_listas_aw["Kiwi"] + diccionario_con_listas_aw["Manzana"])
    lista_aw_verduras = (diccionario_con_listas_aw["Papa"] + diccionario_con_listas_aw["Zanahoria"])
    lista_total = lista_aw_frutas + lista_aw_verduras

    promedios = cajon_de_n_alimentos.calcular_aw_prom_diccionario(diccionario_con_listas_aw)
    awk = promedios["Kiwi"]
    awm = promedios["Manzana"]
    awp = promedios["Papa"]
    awz=promedios["Zanahoria"]
    promedio_fruta = cajon_de_n_alimentos.calcular_aw_prom(lista_aw_frutas)
    promedio_verdura = cajon_de_n_alimentos.calcular_aw_prom(lista_aw_verduras)
    promedio_total = cajon_de_n_alimentos.calcular_aw_prom(lista_total)

    return render_template("home.html",awk= awk, awp= awp, awz= awz,awm= awm, promedio_verdura= promedio_verdura,promedio_fruta= promedio_fruta, promedio_total= promedio_total)
    
if __name__ == "__main__":
    app.run(debug=True)
