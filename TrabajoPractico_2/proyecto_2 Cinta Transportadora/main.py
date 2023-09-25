from modules.cinta_transportadora import Cinta_Transportadora
from modules.cajon import Cajon_Alimentos

n=5
cinta = Cinta_Transportadora()
lista_alimentos= cinta.transportar(n)
cajon = Cajon_Alimentos(lista_alimentos)

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
    
print("listakiwis",aw_kiwis)
print("awkiwis",awk)
print("listamanzanas",aw_manzanas)
print("awmanzana",awm)
print("awzanahorias", awz)
print("awpapas: ",awp)
print("aw frutas lista", aw_frutas)
print("aw frutas: ",aw_promedio_frutas)
print("aw verduras lista", aw_verduras)
print("aw verduras: ",aw_promedio_verduras)
print("aw total: ",aw_total_promedio)