from modules.curso import Curso
from modules.departamento import Departamento 
from modules.persona_facultativa import Estudiante, Profesor
from modules.facultad import Facultad

primer_profesor = None
facultad = None
profesores=[]
alumnos=[]
with open("data/datos.txt", 'r') as archi:
    for linea in archi:
        datos = linea.strip().split(",")
        tipo = datos[0]
        nombre = datos[1]
        apellido = datos[2]
        dni = datos[3]
        if tipo == 'Profesor':
            profesor = Profesor(nombre, apellido, dni)
            if primer_profesor is None:
                primer_profesor = profesor
                facultad = Facultad("FI UNER", "Dpto Programación", primer_profesor) #preguntar si podemos crear la facu asi
                facultad.contratar_profesor(profesor)
                profesores.append(primer_profesor)
            else:
                facultad.contratar_profesor(profesor)
                profesores.append(profesor)
        elif tipo == 'Estudiante':
            estudiante = Estudiante(nombre, apellido, dni)
            facultad.inscribir_estudiante(estudiante)
            alumnos.append(estudiante)

texto = """
########################################
# Sistema de información universitaria #
########################################
Las opciones son:
1 - Inscribir alumno.
2 - Contratar profesor.
3 - Crear departamento nuevo.
4 - Crear curso nuevo.
5 - Inscribir estudiante a un curso.
6 - Salir.
"""

print(texto)
opcion = int(input("Elige una opción: "))
while opcion != 6:

    if opcion == 1:
        nombre_estudiante = input("Ingrese el nombre del estudiante: ")
        apellido_estudiante = input("Ingrese el apellido del estudiante: ")
        dni_estudiante = input("Ingrese el dni del estudiante: ")
        estudiante = Estudiante(nombre_estudiante, apellido_estudiante, dni_estudiante)
        facultad.inscribir_estudiante(estudiante)
        alumnos.append(estudiante)
        with open("data/datos.txt", 'a') as archi:  # Abre el archivo en modo 'append'
            archi.write(f"Estudiante,{nombre_estudiante},{apellido_estudiante},{dni_estudiante}\n")  # Añade el nuevo estudiante al archivo
        print("Los estudiantes de la facultad son: ")
        for i, estudiante in enumerate(facultad.estudiantes):
            print(i+1, estudiante)

    if opcion == 2:
        nombre_profesor = input("Ingrese el nombre del profesor: ")
        apellido_profesor = input("Ingrese el apellido del profesor: ")
        dni_profesor = input("Ingrese el dni del profesor: ")
        profesor = Profesor(nombre_profesor, apellido_profesor, dni_profesor)
        facultad.contratar_profesor(profesor)
        profesores.append(profesor)
        with open("data/datos.txt", 'a') as archi:  # Abre el archivo en modo 'append'
            archi.write(f"Profesor,{nombre_profesor},{apellido_profesor},{dni_profesor}\n")  # Añade el nuevo profesor al archivo
        print("Los profesores de la facultad son: ")
        for i, profesor in enumerate(facultad.profesores):
            print(i+1, profesor)


    if opcion == 3:
        nombre_dpto = input("Ingrese el nombre del nuevo departamento: ")
        print("Los profesores de la facultad son: ")
        for i, profesor in enumerate(facultad.profesores):
            print(i+1, profesor)
        num_profesor_elegido = int(input("Ingrese el número que corresponde al director del nuevo departamento: "))
        profesor_director = facultad.profesores[num_profesor_elegido-1]
        facultad.crear_departamento(nombre_dpto,profesor_director)
        facultad.atribuir_director_a_dpto(profesor_director,nombre_dpto) #ver esto
        print("Los departamentos de la facultad son: ")
        for i, dpto in enumerate(facultad.departamentos):
            print(i+1, dpto)

    #if opcion == 4:

    opcion = int(input("Elige otra opción entre 1 y 6: "))
print("Gracias :)")