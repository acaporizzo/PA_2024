from modules.curso import Curso
from modules.departamento import Departamento
from modules.facultad import Facultad
from modules.persona_facultativa import Estudiante, Profesor

facultad = Facultad("FIUNER","Dpto Matemática","Lili Sanchez")

facultad.crear_departamento("Dpto Biología","Agus y Ana")
for depto in facultad._departamentos:
    print(depto)

primer_profesor = Profesor("Juan","Perez","45387332")
segundo_profesor = Profesor("Agustina","Wiesner","45387555")

facultad.atribuir_dpto_a_profesor(primer_profesor, "Dpto Matemática")
facultad.atribuir_dpto_a_profesor(segundo_profesor, "Dpto Matemática")

for depto in primer_profesor._deptos_del_profesor:
    print(depto)

for profesor in facultad.devolver_profesores_de_dpto("Dpto Biología"):
    print(profesor)

facultad.atribuir_director_a_dpto(primer_profesor, "Dpto Matemática")
director=facultad.devolver_director_de_dpto("Dpto Matemática")
print(f"el director es: {director}")