from modules.curso import Curso
from modules.departamento import Departamento 
from modules.persona_facultativa import Profesor

class Facultad:
    def __init__(self, p_nombre_facu, p_nombre_dpto_inicial, p_primer_profesor): 
        """ Método constructor en el cual al crear una facultad se crea SI O SI un departamento
        """
        self._cursos = []
        self._departamentos = [Departamento(p_nombre_dpto_inicial, p_primer_profesor)]
        self._estudiantes = [] 
        self._nombre_facu = p_nombre_facu
        self._profesores = []

    @property
    def cursos(self):
        return self._cursos
    
    @property
    def departamentos(self):
        return self._departamentos
    
    @property
    def estudiantes(self):
        return self._estudiantes
    
    @property
    def profesores(self):
        return self._profesores
    
    @property
    def nombre_facu(self):
        return self._nombre_facu
   
    def crear_departamento_y_asignar_director(self, nombre_dpto, profesor_director):
        """ Método que crea un departamento nuevo y asigna un director """
        if isinstance(profesor_director, Profesor):
            self.crear_departamento(nombre_dpto, profesor_director)
            self.atribuir_dpto_a_profesor(profesor_director, nombre_dpto)
            self.atribuir_director_a_dpto(profesor_director, nombre_dpto)

    def atribuir_curso_al_dpto(self, p_nombre_del_curso, p_nombre_dpto):
        """método para agregar un curso a un departamento
        """
        if isinstance(p_nombre_del_curso, Curso):
            for dpto in self._departamentos:
                if p_nombre_dpto == dpto.nombre_dpto:
                    dpto.atribuir_curso(p_nombre_del_curso) #en departamento.py

    def atribuir_director_a_dpto (self, p_profesor, p_nombre_dpto):
        """método para asignar a un profesor como director de un dpto
        """
        for depto in self._departamentos:
            if p_nombre_dpto == depto.nombre_dpto:
                depto.atribuir_director(p_profesor) #en departamento.py

    def atribuir_dpto_a_profesor (self, p_nuevo_profesor, p_nombre_dpto):
        """método para inscribir a un profesor en un dpto
        """
        if isinstance(p_nuevo_profesor, Profesor):
            for dpto in self._departamentos:
                if p_nombre_dpto == dpto.nombre_dpto:
                    dpto.agregar_profesor_a_dpto(p_nuevo_profesor) #en departamento.py
                    
    def contratar_profesor(self, profesor):
        """método para agregar un nuevo profesor a la facultad
        """
        self._profesores.append(profesor)

    def crear_curso(self, p_nombre_curso, p_profesor):
        """método para crear un nuevo curso y agregarlo a la lista
        """
        self._cursos.append(Curso(p_nombre_curso, p_profesor))

    def crear_departamento (self, p_nombre_dpto, p_profesor):
        """método para crear un nuevo dpto y agregarlo a la lista
        """
        self._departamentos.append(Departamento (p_nombre_dpto, p_profesor))

    def devolver_cursos_de_dpto(self, p_nombre_dpto):
        """método para mostrar los cursos de un departamento en específico
        """
        for dpto in self._departamentos:
            if p_nombre_dpto == dpto.nombre_dpto:
                return(dpto.cursos)
            
    def devolver_estudiantes_de_curso(self, p_nombre_curso):
        """método para mostrar los estudiantes de un curso en específico
        """
        for curso in self._cursos:
            if p_nombre_curso == curso.nombre_curso:
                return(curso.estudiantes_del_curso)
            
#    def devolver_director_de_dpto (self, p_nombre_dpto):
#        """método para mostrar el director de un dpto (se define en departamento.py)
#        """
#        for dpto in self._departamentos:
#            if p_nombre_dpto == dpto.nombre_dpto:
#                return(dpto.director_de_dpto)
            
#    def devolver_profesores_de_dpto(self, p_nombre_dpto):
#        """método para mostrar los profesores de un dpto (la lista de profesores 
#        está definida en departamento.py)
#        """
#        profesores_de_dpto = []
#        for dpto in self._departamentos:
#            if dpto.nombre_dpto == p_nombre_dpto:
#                profesores_de_dpto = dpto.profesores
#                break
#        return(profesores_de_dpto)

    def inscribir_estudiante(self, estudiante):
        """método para agregar un nuevo estudiante a la facultad
        """
        self._estudiantes.append(estudiante)

    def __repr__(self):
        """método para definir la representación de cadena de una instancia de una clase
        """
        salida = self._nombre_facu
        return(salida)
    
    def __str__(self):
        """para definir una representación legible de una instancia de una clase o 
        cuando se intenta imprimir la instancia
        """
        salida = self._nombre_facu
        return(salida)