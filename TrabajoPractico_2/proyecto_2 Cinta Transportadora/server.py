import webbrowser
from modules.alimentos import Kiwi,Manzana, Papa, Zanahoria, Fruta, Verdura, Alimentos
from modules.cajon import Cajon
from modules.cinta_transportadora import Cinta_Transportadora
from modules.calculador import calcular_aw_promedio, calcular_peso
from flask import render_template,request
from modules.config import app

@app.route("/", methods=["GET", "POST"])
def home():
    # Instanciamos una cinta transportadora:
    cinta_transportadora = Cinta_Transportadora()

    # Mediante un método GET, el usuario ingresa la cantidad de alimentos: 
    n_alimentos = int(request.form.get("usuario", 0))

    # Obtenemos una lista de alimentos instanciados, y la utilizamos como parámetro para instanciar un cajón:
    cajon=Cajon()
    while len(cajon) < n_alimentos:
        alimento = cinta_transportadora.clasificar_alimento()
        if alimento != None:
            cajon.agregar_alimento(alimento)

    # Calculamos el aw promedio de cada clase: 
    diccionario_de_aw_promedio={"aw_kiwi": round(calcular_aw_promedio(Kiwi,cajon),2),
    "aw_manzana": round(calcular_aw_promedio(Manzana,cajon),2),
    "aw_papa": round(calcular_aw_promedio(Papa,cajon),2),
    "aw_zanahoria": round(calcular_aw_promedio(Zanahoria,cajon),2),
    "aw_frutas": round(calcular_aw_promedio(Fruta,cajon),2),
    "aw_verduras": round(calcular_aw_promedio(Verdura,cajon),2),
    "aw_total": round(calcular_aw_promedio(Alimentos,cajon),2),
    }
    
    peso_total = round(calcular_peso(cajon),2)

    return render_template("home.html",awk=diccionario_de_aw_promedio["aw_kiwi"], 
                        awm=diccionario_de_aw_promedio["aw_manzana"],
                        awp=diccionario_de_aw_promedio["aw_papa"], 
                        awz=diccionario_de_aw_promedio["aw_zanahoria"], 
                        awf=diccionario_de_aw_promedio["aw_frutas"], 
                        awv=diccionario_de_aw_promedio["aw_verduras"], 
                        awt=diccionario_de_aw_promedio["aw_total"],
                        peso_total=peso_total)


if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=True)
