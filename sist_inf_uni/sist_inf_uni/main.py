from modules.clase_curso import Curso
from modules.clase_facultad import Facultad
from modules.clase_persona import Alumno, Profesor


facultad=Facultad("Facultad de Ingenieria","Alumnado")
profesor1=Profesor('20338023', 'Isidora Zibecchi', 'abo_zibecchi@hotmail.com')
profesor2=Profesor('21129054', 'Mario Erni', 'mario.erni2gmail.com')
curso=Curso('Programación Avanzada', profesor1)
alumno1=Alumno('44981249','Sofía Mendez','sofiamendez847@gmail.com')

 


facultad.agregar_alumno(alumno1)

print(facultad.lista_alumnos)


facultad.asignar_profesor_departamento(profesor1,"Alumnado")



facultad.crear_departamentos('Departamento de Programación')
facultad.asignar_profesor_departamento(profesor2,"Departamento de Programación")
print(facultad.lista_departamentos)


print(facultad.devolver_equipo())

print(alumno1.nombre_y_apellido)
print(alumno1.DNI)
print(alumno1.correo)
print(alumno1.cursos_inscriptos)

curso.agregar_alumno(alumno1)
print(alumno1.cursos_inscriptos)

print(curso.estudiantes)


print(curso.profesor_a_cargo) 


facultad.asignar_director_departamento(profesor1,"Alumnado")

print(facultad.devolver_director_dpto("Alumnado"))

facultad.agregar_curso_departamento(curso,'Alumnado')
print(facultad.devolver_lista_cursos_departamento('Alumnado'))