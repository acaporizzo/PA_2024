from modules.cajon import Cajon
from modules.cinta_transportadora import Cinta_Transportadora
from modules.calculador_aw import calcular_aw_promedio
from flask import Flask, render_template,request
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    # Instanciamos una cinta transportadora:
    cinta_transportadora = Cinta_Transportadora()

    # Mediante un método GET, el usuario ingresa la cantidad de alimentos: 
    n_alimentos = int(request.form.get("usuario", 0))

    # Obtenemos una lista de alimentos instanciados, y la utilizamos como parámetro para instanciar un cajón:
    lista_de_n_alimentos = cinta_transportadora.clasificar_alimentos(n_alimentos)
    cajon_de_n_alimentos = Cajon(lista_de_n_alimentos)

    # Calculamos el aw promedio de cada clase: 
    aw_promedios = cajon_de_n_alimentos.calcular_aw_promedios()

    

    lista_de_alimentos= []
    while len(lista_de_alimentos) < p_n_alimentos:

    #return render_template("home.html",awk=aw_promedios[0], awm=aw_promedios[1], awp=aw_promedios[2], awz=aw_promedios[3], awf=aw_promedios[4], awv=aw_promedios[5], awt=aw_promedios[6])
        return()
    
if __name__ == "__main__":
    app.run(debug=True)
