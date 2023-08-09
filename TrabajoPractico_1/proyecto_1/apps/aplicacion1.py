# Aplicación secundaria

from modules.modulo1 import mostrar_lista_peliculas

print("""
#######################################
 Películas: Preguntas y respuestas
#######################################

Elige una opción
1 - Mostrar lista de películas.
2 - ¡Trivia de película!
3 - Mostrar secuencia de opciones seleccionadas previamente.
4 - Borrar historial de opciones.
5 - Salir
      """
)
RUTA="./data/"
DIRECCION=RUTA + "frases_de_peliculas.txt"
opcion=int(input("Ingrese su opción: "))

if opcion == 1:
    for i in mostrar_lista_peliculas(DIRECCION):
        print(str(i[0])+")",i[1])