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

    if opcion == 3:  # Crear un departamento nuevo
        while True:
            nombre_dpto = input("Ingrese el nombre del nuevo departamento: ")

            # Verificar si el nombre del departamento ya existe

            if not facultad.verificar_nombre_departamento(nombre_dpto):
                print(f"El departamento '{nombre_dpto}' ya existe. Por favor, ingresa un nombre diferente.")
                continue  # Volver a pedir un nuevo nombre de departamento

            # Mostrar profesores antes de la selección
            print("Los profesores son: ")
            facultad.mostrar_profesores()

            # Asignar director
            num_profesor_elegido = int(input("Selecciona el número de profesor para asignar como director: "))
            
            profesor_director = facultad.asignar_director(num_profesor_elegido)

            if profesor_director:
                facultad.crear_departamento(nombre_dpto, profesor_director)
                print(f"El departamento '{nombre_dpto}' ha sido creado y {profesor_director.nombre} ha sido asignado como director.")
                break  # Salir del bucle cuando se complete la creación
            else:
                print("No se pudo asignar el director. Selecciona un profesor válido.")

    if opcion == 4:  # Crear un curso nuevo
        while True:
            nombre_curso = input("Ingrese el nombre del curso: ")

            # Verificar si el nombre del curso ya existe
            if facultad.verificar_nombre_curso(nombre_curso):
                print(f"El curso '{nombre_curso}' ya existe. Por favor, ingresa un nombre diferente.")
                continue  # Volver a pedir si el curso ya existe

            # Mostrar profesores antes de la selección
            facultad.mostrar_profesores()

            # Seleccionar profesor
            profesor_asignado = facultad.seleccionar_profesor()
            if not profesor_asignado:
                print("Selecciona un profesor válido.")
                continue  # Vuelve al inicio si no se seleccionó un profesor válido

            # Mostrar departamentos antes de la selección
            facultad.mostrar_departamentos()

            # Seleccionar departamento
            departamento_asignado = facultad.seleccionar_departamento()
            if not departamento_asignado:
                print("Selecciona un departamento válido.")
                continue  # Vuelve al inicio si no se seleccionó un departamento válido

            # Crear el curso
            nuevo_curso = facultad.crear_curso(nombre_curso, profesor_asignado)
            if nuevo_curso:
                facultad.atribuir_curso_al_dpto(nuevo_curso, departamento_asignado.nombre_dpto)
                print(f"Curso '{nombre_curso}' asignado al departamento '{departamento_asignado.nombre_dpto}'.")
                break  # Salir del bucle si todo se creó correctamente
            else:
                print(f"El curso '{nombre_curso}' ya existe. Intenta con otro nombre.")


    if opcion == 5:  # Inscribir estudiante en un curso
        # Mostrar estudiantes antes de la selección
        facultad.mostrar_estudiantes()

        # Seleccionar estudiante
        estudiante = facultad.seleccionar_estudiante()
        if not estudiante:
            print("Selecciona un estudiante válido.")
            continue  # Vuelve al inicio si no se seleccionó un estudiante válido

        # Mostrar cursos antes de la selección
        facultad.mostrar_cursos()

        # Seleccionar curso
        curso = facultad.seleccionar_curso()
        if not curso:
            print("Selecciona un curso válido.")
            continue  # Vuelve al inicio si no se seleccionó un curso válido

        # Inscribir estudiante al curso
        facultad.inscribir_estudiante_a_curso(estudiante, curso)
        print(f"El estudiante {estudiante.nombre} {estudiante.apellido} ha sido inscrito en el curso {curso.nombre_curso}.")

    opcion = int(input("Elige otra opción entre 1 y 6: "))

print("Gracias :)")