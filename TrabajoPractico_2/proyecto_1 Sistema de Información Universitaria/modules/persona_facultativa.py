class Persona_Facultativa:
    def __init__(self,p_nombre, p_apellido,p_dni):
        """método constructor de la clase abstracta Persona_Facultativa, que heredará 3 
        atributos a sus clases hijas, Estudiante y Profesor.

        Args:
            p_nombre (str): nombre de la persona, ya sea estudiante o profesor.
            p_apellido (str): apellido de la persona.
            p_dni (str): dni de la persona.
        """
        self._apellido = p_apellido
        self._dni = p_dni
        self._nombre = p_nombre

    @property
    def apellido(self):
        return(self._apellido)
    
    @property
    def dni (self):
        return(self._nombre)
    
    @property
    def nombre(self):
        return(self._nombre)


class Estudiante (Persona_Facultativa):
    def __init__(self,p_nombre, p_apellido,p_dni):
        """los atributos serán heredados de la clase Persona_Facultativa
        """
        super().__init__(p_nombre, p_apellido,p_dni)
        self._cursos_del_estudiante = []
    
    @property
    def cursos_del_estudiante (self):
        return (self._cursos_del_estudiante)
    
    def agregar_cursos_del_estudiante (self, p_nombre_del_curso):
        """método para agregar al estudiante a un nuevo curso
        """
        self._cursos_del_estudiante.append(p_nombre_del_curso)

    def __repr__(self):
        """método para definir la representación de cadena de una instancia de una clase
        """
        salida = self._nombre + " " + self._apellido
        return(salida)


class Profesor (Persona_Facultativa):
    def __init__(self,p_nombre, p_apellido,p_dni):
        """los atributos serán heredados de la clase Persona_Facultativa
        """
        super().__init__(p_nombre, p_apellido,p_dni)
        self._cursos_del_profesor = []
        self._dptos_del_profesor = []
        self._es_director = False #booleano que cambia en la clase Departamento
        self._es_titular = False #booleano que cambia en la clase Curso

    @property
    def cursos_del_profesor (self):
        return (self._cursos_del_profesor)
    
    @property
    def deptos_del_profesor (self):
        return (self._dptos_del_profesor)
    
    @property
    def es_director (self):
        return (self._es_director)
    
    @es_director.setter
    def es_director (self, cambio_de_director):
        self._es_director = cambio_de_director

    @property
    def es_titular (self):
        return (self._es_titular)

    def agregar_dpto_a_profesor(self, p_nombre_dpto):
        """método para agregar un dpto a la lista de dptos de un profesor en específico
        """
        self._dptos_del_profesor.append(p_nombre_dpto)

    def atribuir_curso_al_profesor (self, p_nombre_del_curso):
        """método para que el profesor enseñe en un nuevo curso, se agrega a la lista
        """
        self._cursos_del_profesor.append(p_nombre_del_curso)

    def __repr__(self):
        """método para definir la representación de cadena de una instancia de una clase
        """
        salida = self._nombre + " " + self._apellido
        return(salida)
    
    def __str__(self):
        """para definir una representación legible de una instancia de una clase o 
        cuando se intenta imprimir la instancia
        """
        salida = self._nombre + " " + self._apellido
        return(salida)