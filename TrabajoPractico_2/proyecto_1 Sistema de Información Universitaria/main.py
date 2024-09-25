from modules.curso import Curso
from modules.departamento import Departamento 
from modules.persona_facultativa import Estudiante, Profesor
from modules.facultad import Facultad

primer_profesor=None
facultad=None

with open("data/datos.txt", 'r') as archi:
    for linea in archi:
        datos = linea.strip().split(",")
        tipo = datos[0]
        nombre = datos[1]
        apellido = datos[2]
        dni = datos[3]
        if tipo == "Profesor":
            profesor = Profesor(nombre, apellido, dni)
            if primer_profesor is None:
                primer_profesor = profesor
                facultad = Facultad("FI UNER", "Dpto Programación", primer_profesor) #la facultad debe tener al menos uno o  mas deptos
                facultad.contratar_profesor(profesor)
            else:
                facultad.contratar_profesor(profesor)
        elif tipo == 'Estudiante':
            estudiante = Estudiante(nombre, apellido, dni)
            facultad.inscribir_estudiante(estudiante)

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

    if opcion == 1: #inscribir un alumno
        nombre_estudiante = input("Ingrese el nombre del estudiante: ")
        apellido_estudiante = input("Ingrese el apellido del estudiante: ")
        dni_estudiante = input("Ingrese el dni del estudiante: ")
        estudiante = Estudiante(nombre_estudiante, apellido_estudiante, dni_estudiante)
        facultad.inscribir_estudiante(estudiante)
        with open("data/datos.txt", 'a') as archi:  # Abre el archivo en modo 'append'
            archi.write(f"Estudiante,{nombre_estudiante},{apellido_estudiante},{dni_estudiante}\n")  # Añade el nuevo estudiante al archivo
        print("Los estudiantes de la facultad son: ")
        for i, estudiante in enumerate(facultad.estudiantes):
            print(i+1, estudiante)

    if opcion == 2: #contratar un profesor
        nombre_profesor = input("Ingrese el nombre del profesor: ")
        apellido_profesor = input("Ingrese el apellido del profesor: ")
        dni_profesor = input("Ingrese el dni del profesor: ")
        profesor = Profesor(nombre_profesor, apellido_profesor, dni_profesor)
        facultad.contratar_profesor(profesor)
        print("Los departamentos de la facultad son: ")
        for i, dpto in enumerate(facultad.departamentos):
            print(i+1, dpto)
        num_dpto_elegido = int(input("Ingrese el número que corresponde al departamento que pertenece el profesor: "))
        dpto_del_profesor = facultad.departamentos[num_dpto_elegido-1]
        facultad.atribuir_dpto_a_profesor(profesor,dpto_del_profesor)
        with open("data/datos.txt", 'a') as archi:  # Abre el archivo en modo 'append'
            archi.write(f"Profesor,{nombre_profesor},{apellido_profesor},{dni_profesor}\n")  # Añade el nuevo profesor al archivo
        print("Los profesores de la facultad son: ")
        for i, profesor in enumerate(facultad.profesores):
            print(i+1, profesor)

    if opcion == 3: #crear un dpto nuevo
        nombre_dpto = input("Ingrese el nombre del nuevo departamento: ")
        print("Los profesores de la facultad son: ")
        for i, profesor in enumerate(facultad.profesores):
            print(i+1, profesor)
        num_profesor_elegido = int(input("Ingrese el número que corresponde al director del nuevo departamento: "))
        profesor_director = facultad.profesores[num_profesor_elegido-1]
        while profesor_director.es_director:
            print("Este profesor ya es director de otro departamento")
            num_profesor_elegido = int(input("Ingrese el número que corresponde al director del nuevo departamento: "))
            profesor_director = facultad.profesores[num_profesor_elegido-1]
        facultad.crear_departamento(nombre_dpto,profesor_director)
        facultad.atribuir_dpto_a_profesor(profesor_director,nombre_dpto)
        facultad.atribuir_director_a_dpto(profesor_director,nombre_dpto)
        print("Los departamentos de la facultad son: ")
        for i, dpto in enumerate(facultad.departamentos):
            print(i+1, dpto)

    if opcion == 4: #crear curso nuevo
        nombre_curso = input("Ingrese el nombre del curso: ")
        print("Los profesores de la facultad son: ")
        for i, profesor in enumerate(facultad.profesores):
            print(i+1, profesor)
        num_profesor_elegido = int(input("Ingrese el número que corresponde al titular del nuevo curso: "))
        profesor_titular = facultad.profesores[num_profesor_elegido-1]
        facultad.crear_curso(nombre_curso,profesor_titular)
        print("Los departamentos de la facultad son: ")
        for i, dpto in enumerate(facultad.departamentos):
            print(i+1, dpto)
        num_dpto_elegido = int(input("Ingrese el número que corresponde al departamento que pertenece el curso: "))
        dpto_del_curso = facultad.departamentos[num_dpto_elegido-1]
        facultad.atribuir_curso_al_dpto(Curso(nombre_curso,profesor_titular),dpto_del_curso.nombre_dpto)
        print("Los cursos en el departamento:",dpto_del_curso,"son: ")
        for i,curso in enumerate(facultad.devolver_cursos_de_dpto(dpto_del_curso.nombre_dpto)):
            print(i+1,curso)
    
    if opcion == 5: #inscribir estudiante a un curso
        print("Los estudiantes de la facultad son: ")
        for i, estudiante in enumerate(facultad.estudiantes):
            print(i+1, estudiante)
        num_estudiante_elegido = int(input("Ingrese el número que corresponde al estudiante que se inscribirá: "))
        estudiante_elegido = facultad.estudiantes[num_estudiante_elegido-1]
        print("Los cursos a los que se puede inscribir son: ")
        for i,curso in enumerate(facultad.cursos):
            print(i+1,curso)
        num_curso_elegido = int(input("Ingrese el número que corresponde al curso donde se va a inscribir: "))
        curso_elegido = facultad.cursos[num_curso_elegido-1]
        curso_elegido.agregar_estudiante_al_curso(estudiante_elegido)
        print("Los estudiantes de ",curso_elegido,"son: ")
        for i,estudiante in enumerate(curso_elegido.estudiantes_del_curso):
            print(i+1,estudiante)

    opcion = int(input("Elige otra opción entre 1 y 6: "))

print("Gracias :)")