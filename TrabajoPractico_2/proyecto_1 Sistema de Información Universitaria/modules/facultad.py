from modules.curso import Curso
from modules.departamento import Departamento 
from modules.persona_facultativa import Estudiante, Profesor

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
    
    @classmethod
    def inicializar_desde_archivo(cls, ruta_archivo):
        """Clase método para inicializar una instancia de Facultad desde un archivo"""
        try:
            with open(ruta_archivo, 'r') as archivo:
                nombre_facu = archivo.readline().strip()
                nombre_dpto_inicial = archivo.readline().strip()
                nombre_profesor_inicial = archivo.readline().strip()
                # Crea la facultad con los datos iniciales
                facultad = cls(nombre_facu, nombre_dpto_inicial, Profesor(nombre_profesor_inicial))
                return facultad
        except FileNotFoundError:
            print(f"Error: El archivo '{ruta_archivo}' no fue encontrado.")
        except Exception as e:
            print(f"Error: {e}")

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
    
    
                    
    def contratar_profesor(self, nombre, apellido, dni):
        """método para agregar un nuevo profesor a la facultad
        """
        profesor = Profesor(nombre, apellido, dni)
        self._profesores.append(profesor)
        return profesor

    def crear_curso(self, p_nombre_curso, p_profesor):
        """método para crear un nuevo curso y agregarlo a la lista
        """
        curso = Curso(p_nombre_curso, p_profesor)
        self._cursos.append(Curso(p_nombre_curso, p_profesor))
        return curso

    def crear_departamento (self, p_nombre_dpto, p_profesor):
        """método para crear un nuevo dpto y agregarlo a la lista
        """
        departamento = Departamento(p_nombre_dpto, p_profesor)
        self._departamentos.append(Departamento(p_nombre_dpto, p_profesor))
        return departamento

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

    def inscribir_estudiante(self, nombre, apellido, dni):
        """método para agregar un nuevo estudiante a la facultad
        """
        estudiante = Estudiante(nombre, apellido, dni)
        self._estudiantes.append(estudiante)
        return estudiante

    def __repr__(self):
        """método para definir la representación de cadena de una instancia de una clase
        """
        return self._nombre_facu
    
    def __str__(self):
        """para definir una representación legible de una instancia de una clase o 
        cuando se intenta imprimir la instancia
        """
        return self._nombre_facu
    


                
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
