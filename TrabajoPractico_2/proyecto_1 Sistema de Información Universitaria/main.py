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
            if primer_profesor is None:
                facultad = Facultad("FI UNER", "Dpto Programación", nombre, apellido, dni)  # Crear facultad con el primer profesor
                primer_profesor = True
            else:
                facultad.contratar_profesor(nombre, apellido, dni)
        elif tipo == 'Estudiante':
            facultad.inscribir_estudiante(nombre, apellido, dni)

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
        
        facultad.inscribir_estudiante(nombre_estudiante, apellido_estudiante, dni_estudiante)

        with open("data/datos.txt", 'a') as archi:
            archi.write(f"Estudiante,{nombre_estudiante},{apellido_estudiante},{dni_estudiante}\n")  # Añade el nuevo estudiante al archivo
        
        print("Los estudiantes de la facultad son: ")
        facultad.mostrar_estudiantes()


    if opcion == 2: #contratar un profesor
        nombre_profesor = input("Ingrese el nombre del profesor: ")
        apellido_profesor = input("Ingrese el apellido del profesor: ")
        dni_profesor = input("Ingrese el dni del profesor: ")

        facultad.contratar_profesor(nombre_profesor, apellido_profesor, dni_profesor)

        with open("data/datos.txt", 'a') as archi:
            archi.write(f"Profesor,{nombre_profesor},{apellido_profesor},{dni_profesor}\n")  # Añade el nuevo profesor al archivo
        
        print("Los profesores de la facultad son: ")
        facultad.mostrar_profesores()


    if opcion == 3:  #crear un departamento nuevo
        while True:
            nombre_dpto = input("Ingrese el nombre del nuevo departamento: ")

            if facultad.verificar_nombre_departamento(nombre_dpto): #verifica si el nombre del departamento ya existe
                break
            print(f"El departamento '{nombre_dpto}' ya existe. Por favor, ingresa un nombre diferente.")

        print("Los profesores son: ")
        facultad.mostrar_profesores()

        while True:
            num_profesor_elegido = int(input("Selecciona el número de profesor para asignar como director: "))
            profesor_director = facultad.asignar_director(num_profesor_elegido)

            if profesor_director:
                facultad.crear_departamento(nombre_dpto, profesor_director)
                print(f"El departamento '{nombre_dpto}' ha sido creado y {profesor_director.nombre} ha sido asignado como director.")
                print("Los departamentos de la facultad son: ")
                facultad.mostrar_departamentos()
                break
            print("El profesor ya es director de otro departamento. Selecciona un profesor válido.")


    if opcion == 4:  # Crear un curso nuevo
        while True:
            nombre_curso = input("Ingrese el nombre del curso: ")

            if facultad.verificar_nombre_curso(nombre_curso): # verifica si el nombre del curso ya existe
                print(f"El curso '{nombre_curso}' ya existe. Por favor, ingresa un nombre diferente.")
                continue  #volver a pedir si el curso ya existe

            facultad.mostrar_profesores()
            profesor_asignado = facultad.seleccionar_profesor()
            if not profesor_asignado:
                print("Selecciona un profesor válido.")
                continue  #vuelve al inicio si no se seleccionó un profesor válido

            facultad.mostrar_departamentos()
            departamento_asignado = facultad.seleccionar_departamento()
            if not departamento_asignado:
                print("Selecciona un departamento válido.")
                continue  #vuelve al inicio si no se seleccionó un departamento válido

            nuevo_curso = facultad.crear_curso(nombre_curso, profesor_asignado)

            if nuevo_curso:
                facultad.atribuir_curso_al_dpto(nuevo_curso, departamento_asignado.nombre_dpto)
                print(f"Curso '{nombre_curso}' asignado al departamento '{departamento_asignado.nombre_dpto}'.")
                cursos = facultad.devolver_cursos_de_dpto(departamento_asignado.nombre_dpto)
                if cursos:
                    print(f"Los cursos del departamento '{departamento_asignado.nombre_dpto}' son:")
                    for curso in cursos:
                        print(f"- {curso.nombre_curso}")
                else:
                    print(f"No hay cursos registrados en el departamento '{departamento_asignado.nombre_dpto}'.")
                break
            else: print(f"El curso '{nombre_curso}' ya existe. Intenta con otro nombre.")


    if opcion == 5:  # Inscribir estudiante en un curso

        while True: #para seleccionar un estudiante válido
            facultad.mostrar_estudiantes()
            estudiante = facultad.seleccionar_estudiante()
            if estudiante:
                break  # Sale del bucle si se seleccionó un estudiante válido
            print("Selecciona un estudiante válido.")

        while True: #para seleccionar un curso válido
            facultad.mostrar_cursos()
            curso = facultad.seleccionar_curso()

            if curso:
                break  # Sale del bucle si se seleccionó un curso válido
            print("Selecciona un curso válido.")

        facultad.inscribir_estudiante_a_curso(estudiante, curso)
        print(f"El estudiante {estudiante.nombre} {estudiante.apellido} ha sido inscripto en el curso {curso.nombre_curso}.")


    opcion = int(input("Elige otra opción entre 1 y 6: "))

print("Gracias :)")