from modules.facultad import Facultad

# Inicialización de la facultad con un primer profesor
facultad = Facultad.inicializar_desde_archivo("data/datos.txt")
if facultad is None:
    print("Error al inicializar la facultad desde el archivo")
else:
    facultad.inscribir_alumno()
    
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
    if opcion == 1:  # Inscribir un alumno
        facultad.inscribir_alumno()

    elif opcion == 2:  # Contratar un profesor
        facultad.contratar_profesor()

    elif opcion == 3:  # Crear un departamento nuevo
        facultad.crear_departamento()

    elif opcion == 4:  # Crear un curso nuevo
        facultad.crear_curso()

    elif opcion == 5:  # Inscribir estudiante a un curso
        facultad.inscribir_estudiante_a_curso()

    opcion = int(input("Elige otra opción entre 1 y 6: "))

print("Gracias :)")