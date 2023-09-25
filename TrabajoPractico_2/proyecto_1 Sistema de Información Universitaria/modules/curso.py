from modules.persona_facultativa import Estudiante, Profesor

class Curso: 
    def __init__(self, p_nombre_curso):
        self._dpto_del_curso = None #departamento al que pertenece el curso, es un str porque un curso puede pertenecer a un solo dpto
        self._estudiantes_del_curso = [] #lista de estudiantes de ese curso
        self._nombre_curso = p_nombre_curso #nombre del curso
        self._profesores_del_curso = [] #lista de profesores que dan clases en ese curso

    @property
    def dpto_del_curso (self):
        return (self._dpto_del_curso)
    
    @property
    def estudiantes_del_curso (self):
        return (self._estudiantes_del_curso)
    
    @property
    def nombre_curso (self):
        return (self._nombre_curso)
    
    @property
    def profesores_del_curso (self):
        return (self._profesores_del_curso)
    
    def agregar_estudiante_al_curso (self, p_nombre_de_estudiante): #método para que un nuevo estudiante asista al curso
        if isinstance(p_nombre_de_estudiante, Estudiante):
            self._estudiantes_del_curso.append(p_nombre_de_estudiante)
            p_nombre_de_estudiante.agregar_cursos_del_estudiante(self) #en persona_facultativa.py, clase Estudiante

    def agregar_profesor_al_curso (self, p_nombre_de_profesor): #método para que un nuevo profesor enseñe en el curso
        if isinstance(p_nombre_de_profesor, Profesor):
            self._profesores_del_curso.append(p_nombre_de_profesor)
            p_nombre_de_profesor.atribuir_curso_al_profesor(self) #en persona_facultativa.py, clase Profesor

    def atribuir_dpto_al_curso (self,p_nombre_dpto):  #se asigna un único dpto al que pertenece el curso en un str
        self._dpto_del_curso = p_nombre_dpto

    def __repr__(self): #método para definir la representación de cadena de una instancia de una clase
        salida = self._nombre_curso
        return(salida)