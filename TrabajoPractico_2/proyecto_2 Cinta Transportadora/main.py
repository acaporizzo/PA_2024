from modules.cajon import Cajon
from modules.cinta_transportadora import Cinta_Transportadora

cinta_transportadora = Cinta_Transportadora()
n_alimentos = 8
lista_alimentos = cinta_transportadora.clasificar_alimentos(n_alimentos)
cajon_de_n_alimentos = Cajon(lista_alimentos)

diccionario_con_listas_aw = cajon_de_n_alimentos.agregar_y_calcular_aw(lista_alimentos)

lista_aw_frutas = (diccionario_con_listas_aw["Kiwi"] + diccionario_con_listas_aw["Manzana"])
lista_aw_verduras = (diccionario_con_listas_aw["Papa"] + diccionario_con_listas_aw["Zanahoria"])
lista_total = lista_aw_frutas + lista_aw_verduras

promedios = cajon_de_n_alimentos.calcular_aw_prom_diccionario(diccionario_con_listas_aw)
promedio_fruta = cajon_de_n_alimentos.calcular_aw_prom(lista_aw_frutas)
promedio_verdura = cajon_de_n_alimentos.calcular_aw_prom(lista_aw_verduras)
promedio_total = cajon_de_n_alimentos.calcular_aw_prom(lista_total)

print("lista de aw de kiwis: ",diccionario_con_listas_aw["Kiwi"])
print("lista de aw de manzanas: ",diccionario_con_listas_aw["Manzana"])
print("lista de aw de papas: ",diccionario_con_listas_aw["Papa"])
print("lista de aw de zanahorias: ",diccionario_con_listas_aw["Zanahoria"])

print("lista de aw de frutas: ", lista_aw_frutas)
print("lista de aw de verduras: ", lista_aw_verduras)
print("lista de aw totales: ", lista_total)

print("aw promedio de kiwi: ",promedios["Kiwi"])
print("aw promedio de manzana: ",promedios["Manzana"])
print("aw promedio de papa: ",promedios["Papa"])
print("aw promedio de zanahoria: ",promedios["Zanahoria"])

print("aw promedio de frutas: ", promedio_fruta)
print("aw promedio de verduras: ", promedio_verdura)
print("aw promedio total: ", promedio_total)