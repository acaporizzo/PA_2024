from modules.curso import Curso
from modules.persona_facultativa import Profesor

class Departamento:
    def __init__(self, p_nombre_dpto, p_primer_profesor):
        """método constructor de la clase Departamento, determina un nuevo departamento perteneciente a una 
        única facultad, con uno o más cursos y uno o más profesores, siendo uno de ellos el director.

        Args:
            p_nombre_dpto (str): nombre del departamento
            p_primer_profesor (str): nombre del primer profesor, ya que no puede haber un departamento sin profesores
        """
        self._cursos = [] #lista de cursos de ese departamento
        self._director_de_dpto = None #se inicia vacía hasta ser definida
        self._nombre_dpto = p_nombre_dpto
        self._profesores = [p_primer_profesor] #lista de profesores,se incluye al primero que se pasa como parámetro

    @property
    def cursos (self):
        return (self._cursos)
    
    @property
    def director_de_dpto (self):
        return (self._director_de_dpto)
    
    @property
    def profesores (self):
        return (self._profesores) 
    
    @property
    def nombre_dpto (self):
        return (self._nombre_dpto)

    def agregar_profesor_a_dpto(self, p_nuevo_profesor):
        """método para agregar un profesor a la lista de profesores de un departamento
        """
        if isinstance(p_nuevo_profesor,Profesor):
            self._profesores.append(p_nuevo_profesor)
            p_nuevo_profesor.agregar_dpto_a_profesor(self) #en persona_facultativa.py , clase Profesor

    def atribuir_curso(self, p_nombre_del_curso):
        """método para agregar un curso a la lista cursos de un departamento en específico
        """
        if isinstance(p_nombre_del_curso, Curso):
            self._cursos.append(p_nombre_del_curso)
            p_nombre_del_curso.atribuir_dpto_al_curso(self) #en curso.py

    def atribuir_director(self, p_profesor):
        """método para definir el profesor pasado como parámetro como director
        """
        if isinstance(p_profesor, Profesor):
            if p_profesor in self._profesores and not p_profesor._es_director:
                self._director_de_dpto = p_profesor
                p_profesor.es_director = True #se define en la clase Profesor
    
    def __str__(self):
        """para definir una representación legible de una instancia de una clase o 
        cuando se intenta imprimir la instancia
        """
        salida = self._nombre_dpto
        return(salida)