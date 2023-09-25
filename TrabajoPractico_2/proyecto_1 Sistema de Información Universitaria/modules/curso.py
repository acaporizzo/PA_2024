from modules.persona_facultativa import Estudiante, Profesor

class Curso: 
    def __init__(self, p_nombre_curso):
        self._dpto_del_curso = None
        self._estudiantes_del_curso = []
        self._nombre_curso = p_nombre_curso

    @property #atributo
    def dpto_del_curso (self):
        return (self._dpto_del_curso)
    
    @property #atributo
    def estudiantes_del_curso (self):
        return (self._estudiantes_del_curso)
    
    @property #atributo
    def nombre_curso (self):
        return (self._nombre_curso)
    
    def agregar_estudiante_al_curso (self, p_nombre_de_estudiante):
        if isinstance(p_nombre_de_estudiante, Estudiante):
            self._estudiantes_del_curso.append(p_nombre_de_estudiante)
            p_nombre_de_estudiante.agregar_cursos_del_estudiante(self)

    def agregar_profesor_al_curso (self, p_nombre_de_profesor):
        if isinstance(p_nombre_de_profesor, Profesor):
            self._estudiantes_del_curso.append(p_nombre_de_profesor)
            p_nombre_de_profesor.atribuir_curso_al_profesor(self)

    def atribuir_dpto_al_curso (self,p_nombre_dpto):
        self._dpto_del_curso = p_nombre_dpto

