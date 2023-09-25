from modules.curso import Curso
from modules.persona_facultativa import Profesor

class Departamento:
    def __init__(self, p_nombre_dpto, p_primer_profesor):
        self._cursos = []
        self._director_de_dpto = None
        self._nombre_dpto = p_nombre_dpto
        self._profesores = [p_primer_profesor] 

    @property #atributo
    def cursos (self):
        return (self._cursos)
    
    @property #atributo
    def director_de_dpto (self):
        return (self._director_de_dpto)
    
    @property #atributo
    def profesores (self):
        return (self._profesores) 
    
    @property #atributo
    def nombre_dpto (self):
        return (self._nombre_dpto)

    def agregar_profesor_a_dpto(self, p_nuevo_profesor):
        if isinstance(p_nuevo_profesor,Profesor):
            self._profesores.append(p_nuevo_profesor)
            p_nuevo_profesor.agregar_dpto_a_profesor(self)

    def atribuir_curso(self, p_nombre_del_curso):
        if isinstance(p_nombre_del_curso, Curso):
            self._cursos.append(p_nombre_del_curso)
            p_nombre_del_curso.atribuir_dpto_al_curso(self)

    def atribuir_director(self, p_profesor):
        if isinstance(p_profesor, Profesor):
            if p_profesor in self._profesores and not p_profesor._es_director:
                self._director_de_dpto = p_profesor
                p_profesor._es_director = True
        
    def __str__(self):
        salida = self._nombre_dpto
        return(salida)