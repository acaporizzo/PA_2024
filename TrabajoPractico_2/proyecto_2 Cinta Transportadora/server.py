from flask import Flask, render_template,request
app= Flask(__name__)
from modules.cajon import Cajon
from modules.cinta_transportadora import Cinta_Transportadora

@app.route("/", methods=['GET', 'POST'])
def raiz():
    n= int(request.form.get('usuario', 0))
    cinta = Cinta_Transportadora()
    lista_alimentos= cinta.transportar(n)
    cajon = Cajon(lista_alimentos)

    aw_kiwis, aw_manzanas, aw_papas, aw_zanahorias = cajon.agregar_y_calcular_aw(lista_alimentos)

    aw_frutas= aw_kiwis + aw_manzanas
    aw_verduras= aw_papas + aw_zanahorias
    aw_total= aw_frutas + aw_verduras

    awk= cajon.calcular_aw_prom(aw_kiwis)
    awm= cajon.calcular_aw_prom(aw_manzanas)
    awz= cajon.calcular_aw_prom(aw_zanahorias)
    awp= cajon.calcular_aw_prom(aw_papas)
    aw_promedio_frutas= cajon.calcular_aw_prom(aw_frutas)
    aw_promedio_verduras= cajon.calcular_aw_prom(aw_verduras)
    aw_total_promedio= cajon.calcular_aw_prom(aw_total)
    
    return render_template("home.html",awk= awk, awp= awp, awz= awz,awm= awm, aw_promedio_verduras= aw_promedio_verduras,aw_promedio_frutas= aw_promedio_frutas, aw_total_promedio= aw_total_promedio)
    
if __name__ == "__main__":
    app.run(debug=True)
