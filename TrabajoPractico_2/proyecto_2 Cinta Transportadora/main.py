from modules.cajon import Cajon
from modules.cinta_transportadora import Cinta_Transportadora

cinta_transportadora = Cinta_Transportadora()
n_alimentos = 8
lista2= ["papa","kiwi","zanahoria","papa"]
cajon_de_n_alimentos= cinta_transportadora.clasificar_alimentos(n_alimentos)

aw_promedios = cajon_de_n_alimentos.calcular_aw_promedios()
for i in aw_promedios:
    print(i)
awk=aw_promedios[0]
print(awk)