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

        profesor_director = facultad.crear_departamento()
        facultad.mostrar_departamentos()


    if opcion == 4:  # Crear curso nuevo
        nombre_curso = input("Ingrese el nombre del curso: ")
        facultad.mostrar_profesores()

        # Solicita el número de profesor una vez, sin bucle
        try:
            num_profesor_elegido = int(input("Selecciona el número de profesor: "))
            profesor_asignado = facultad.obtener_profesor(num_profesor_elegido)

            if profesor_asignado:
                # Crear el curso solo si se seleccionó un profesor válido
                nuevo_curso = facultad.crear_curso(nombre_curso, profesor_asignado)

                # Mostrar departamentos para asignar el curso
                facultad.mostrar_departamentos()

                # Solicita el número del departamento una vez, sin bucle
                try:
                    num_dpto_elegido = int(input("Ingrese el número que corresponde al departamento que pertenece el curso: "))
                    dpto_del_curso = facultad.obtener_departamento(num_dpto_elegido)

                    if dpto_del_curso:
                        # Asignar el curso al departamento solo si es válido
                        facultad.atribuir_curso_al_dpto(nuevo_curso, dpto_del_curso.nombre_dpto)
                        print(f"Curso '{nombre_curso}' asignado al departamento '{dpto_del_curso.nombre_dpto}'.")
                    else:
                        print("Número de departamento no válido.")

                except ValueError:
                    print("Por favor, ingresa un número válido.")
            else:
                print("Número de profesor no válido.")
                
        except ValueError:
            print("Por favor, ingresa un número válido.")


    if opcion == 5: #inscribir estudiante a un curso
        facultad.mostrar_estudiantes()
        num_estudiante_elegido = int(input("Ingrese el número que corresponde al estudiante que se inscribirá: "))
        estudiante_elegido = facultad.obtener_estudiante(num_estudiante_elegido)
        facultad.mostrar_cursos()
        num_curso_elegido = int(input("Ingrese el número que corresponde al curso donde se va a inscribir: "))
        curso_elegido = facultad.obtener_curso(num_curso_elegido)
        curso_elegido.inscribir_estudiante_a_curso(estudiante_elegido)
        curso_elegido.mostrar_estudiantes()

    opcion = int(input("Elige otra opción entre 1 y 6: "))

print("Gracias :)")