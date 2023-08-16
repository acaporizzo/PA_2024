# Aplicación secundaria

from modules.modulo1 import mostrar_lista_peliculas, trivia, guardar_opciones, mostrar_opciones_seleccionadas, borrar_opciones

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
      """)

RUTA="./data/"
DIRECCION=RUTA + "frases_de_peliculas.txt"
DIRECCION1=RUTA+"registro de opciones selecionadas.txt"
lista_opciones=[]
opcion=int(input("Ingrese una opción: "))
guardar_opciones(opcion)
while opcion!=5:
      if opcion == 1:
            for i in mostrar_lista_peliculas(DIRECCION):
                  print(str(i[0])+")",i[1])
      elif opcion==2:
            print(trivia(DIRECCION))
      elif opcion==3:
            print(mostrar_opciones_seleccionadas(DIRECCION1))
      elif opcion==4:
            borrar_opciones(DIRECCION1)
      elif opcion>5:
            print("La opción elegida no es correcta, vuelva a intentarlo.")
      opcion=int(input("Ingrese otra opción: "))
      guardar_opciones(opcion)
if opcion==5:
      print("Gracias por utilizar el programa.")