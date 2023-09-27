from modules.curso import Curso
from modules.facultad import Facultad
from modules.persona_facultativa import Estudiante, Profesor

#instanciamos objetos para probar las relaciones:
primer_profesor = Profesor("Diana","Vertiz","31287332") 
facultad = Facultad("FIUNER","Dpto Programación",primer_profesor)
segundo_profesor = Profesor("Jordán","Insfrán","45387332")
tercer_profesor = Profesor("Leandro","Escher","45387555")
cuarto_profesor = Profesor("Liliana","Taborda","45387777")
primer_estudiante = Estudiante("Agustina","Wiesner","45387444")
segundo_estudiante = Estudiante("Ana Clara","Polari","45387333")
primer_curso = Curso("Álgebra")
segundo_curso = Curso("Programación Avanzada")
tercer_curso = Curso("Ecuaciones Diferenciales")

#creamos otro departamento y mostramos todos los departamentos de la facultad:
facultad.crear_departamento("Dpto Matemática",cuarto_profesor)
print("Los departamentos de la facultad son: ")
for i,depto in enumerate(facultad.departamentos):
    print(i+1,depto)

#la facultad asigna un departamento a cada profesor:
facultad.atribuir_dpto_a_profesor(segundo_profesor, "Dpto Programación")
facultad.atribuir_dpto_a_profesor(tercer_profesor, "Dpto Matemática")
facultad.atribuir_dpto_a_profesor(cuarto_profesor, "Dpto Matemática")

#mostramos LOS departamentos a los que pertenece UN profesor:
print(f"El profesor {segundo_profesor} pertenece a el/los siguiente/s departamento/s: ")
for i,depto in enumerate(segundo_profesor._dptos_del_profesor):
    print(i+1,depto)

#mostramos LOS profesores que pertenecen a UN departamento:
print("Los profesores del departamento son: ")
for i,profesor in enumerate(facultad.devolver_profesores_de_dpto("Dpto Programación")):
    print(i+1,profesor)

#definimos UN profesor del departamento como director SOLO DE ESE departamento y lo mostramos:
facultad.atribuir_director_a_dpto(primer_profesor, "Dpto Programación")
facultad.atribuir_director_a_dpto(segundo_profesor, "Dpto Programación")   #prueba para cambiar el director y que se muestre solo uno
director=facultad.devolver_director_de_dpto("Dpto Programación")
print(f"El director es: {director}")

#inscribimos estudiantes desde la facultad y los mostramos:
facultad.inscribir_estudiante(primer_estudiante)
facultad.inscribir_estudiante(segundo_estudiante)
print("Los estudiantes de la facultad son: ")
for i,estudiante in enumerate(facultad._estudiantes):
    print(i+1,estudiante)

#desde facultad agregamos UNO O MÁS cursos a UN departamento y mostramos los cursos de un dpto:
facultad.atribuir_curso_al_dpto(primer_curso,"Dpto Matemática")
facultad.atribuir_curso_al_dpto(tercer_curso,"Dpto Matemática")
print ("Los cursos del departamento son: ")
for i,cursos in enumerate(facultad.devolver_cursos_de_dpto("Dpto Matemática")):
    print(i+1,cursos)

#mostramos el departamento al que pertenece un curso:
print(f"{primer_curso} pertenece a {primer_curso._dpto_del_curso}")

#agregamos UNO O MÁS estudiantes a UNO O MÁS cursos:
primer_curso.agregar_estudiante_al_curso(primer_estudiante)
primer_curso.agregar_estudiante_al_curso(segundo_estudiante)
segundo_curso.agregar_estudiante_al_curso(primer_estudiante)

#mostramos LOS cursos a los que asiste UN estudiante:
print(f"Los cursos a los que asiste {primer_estudiante} son: ")
for i,cursos in enumerate(primer_estudiante._cursos_del_estudiante):
    print(i+1,cursos)

#mostramos LOS estudiantes de UN curso:
print(f"Los estudiantes que asisten a {primer_curso} son: ")
for i,estudiantes in enumerate(primer_curso._estudiantes_del_curso):
    print(i+1,estudiantes)

#agregamos UNO O MÁS profesores a UNO O MÁS cursos que enseñan:
primer_curso.agregar_profesor_al_curso(tercer_profesor)
primer_curso.agregar_profesor_al_curso(cuarto_profesor)
tercer_curso.agregar_profesor_al_curso(tercer_profesor)

#mostramos LOS cursos en los que enseña UN profesor:
print(f"Los cursos en los que enseña {tercer_profesor} son: ")
for i,cursos in enumerate(tercer_profesor._cursos_del_profesor):
    print(i+1,cursos)

#mostramos LOS profesores que enseñan en UN curso:
print(f"Los profesores que enseñan en {primer_curso} son: ")
for i,profesores in enumerate(primer_curso._profesores_del_curso):
    print(i+1,profesores)