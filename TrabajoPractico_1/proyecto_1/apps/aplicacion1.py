from modules.modulo1 import mostrar_lista_peliculas, trivia, guardar_opciones, mostrar_opciones_seleccionadas, borrar_opciones
import random
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
with open (DIRECCION, "r",encoding="utf-8") as f:
      lista1=f.readlines()
      frases_y_pelis=[(linea.strip().split(';')[0], linea.strip().split(';')[1]) for linea in lista1]

while opcion!=5: #si la opción es 5, sale del bucle y finaliza el código

      if opcion == 1:
            for i in mostrar_lista_peliculas(lista1): 
                  print(str(i[0])+")",i[1])

      elif opcion == 2:
            repeticiones=int(input("Ingrese la cantidad de frases en la que consistirá la trivia (mínimo 3, máximo 10): "))
            while repeticiones<3 or repeticiones>10:
                  repeticiones=int(input("Ingrese nuevamente la cantidad. Debe ser un número entre 3 y 10: \n"))
            for i in range(1,repeticiones+1):
                  lista=trivia(frases_y_pelis)  #va a ser una lista con los tres datos: la frase, la opción ganadora y una tupla con las 3 opciones a mostrar
                  print("\nAdivine a que película pertenece la siguiente frase: \n","\n"+str(i)+")",lista[0])
                  print("\nLas opciones para elegir son: ")
                  for i,j in zip(lista[2],range(1,4)): #agrega numero a las opciones de peliculas
                        print(str(j)+")",i)        
                  opcion=int(input("\nElija la opción correcta, ingresando 1, 2 o 3 : "))
                  if opcion-1==lista[2].index(lista[1]):
                        print("\n¡¡¡Felicitaciones, la opción elegida es la correcta!!!\n")   #compara resultados
                  elif opcion-1!=lista[2].index(lista[1]):
                        print("\nLa opción es incorrecta, la opción correcta es:",lista[1])
                  else:
                        print("El número ingresado no es una opción posible")
            
      elif opcion == 3:
            print("El historial es: ")
            for i in mostrar_opciones_seleccionadas(DIRECCION1): #ruta de archivo txt con los datos solicitados
                  print(i)

      elif opcion == 4:
            borrar_opciones(DIRECCION1)
            print("Se eliminó correctamente el historial.")

      elif opcion > 5:
            print("La opción elegida no es correcta, vuelva a intentarlo.")
            
      opcion=int(input("\nIngrese otra opción: "))
      guardar_opciones(opcion)

if opcion==5:
      print("Gracias por utilizar el programa.")