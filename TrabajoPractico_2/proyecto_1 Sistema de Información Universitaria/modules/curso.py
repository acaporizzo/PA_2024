from modules.persona_facultativa import Estudiante, Profesor

class Curso: 
    def __init__(self, p_nombre_curso, p_primer_profesor):
        """método constructor de la clase Curso, determina un nuevo curso perteneciente a un departamento, 
        con uno o más estudiantes y uno o más profesores.

        Args:
            p_nombre_curso (str): nombre del curso
        """
        self._dpto_del_curso = None #departamento al que pertenece el curso
        self._estudiantes_del_curso = []
        self._nombre_curso = p_nombre_curso
        self._profesores_del_curso = [p_primer_profesor]
        self._titular_del_curso = None #se inicia vacía hasta ser definida

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
    
    @property
    def titular_del_curso (self):
        return (self._titular_del_curso)
    
    def agregar_estudiante_al_curso (self, p_nombre_de_estudiante):
        """método para que un nuevo estudiante asista al curso
        """
        if isinstance(p_nombre_de_estudiante, Estudiante):
            self._estudiantes_del_curso.append(p_nombre_de_estudiante)
            p_nombre_de_estudiante.agregar_cursos_del_estudiante(self) #en persona_facultativa.py, clase Estudiante

    def atribuir_dpto_al_curso (self,p_nombre_dpto):
        """método que asigna un único dpto al que pertenece el curso en un str
        """
        self._dpto_del_curso = p_nombre_dpto

    def atribuir_titular(self, p_profesor):
        """método para definir el profesor pasado como parámetro como titular del curso
        """
        if isinstance(p_profesor, Profesor):
            if p_profesor in self._profesores_del_curso and not p_profesor.es_titular:
                self._titular_del_curso = p_profesor
                p_profesor.es_titular = True #se define en la clase Profesor

    def __repr__(self):
        """método para definir la representación de cadena de una instancia de una clase
        """
        salida = self._nombre_curso
        return(salida)