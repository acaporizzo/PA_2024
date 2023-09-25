class Persona_Facultativa:
    def __init__(self,p_nombre, p_apellido,p_dni):
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
        super().__init__(p_nombre, p_apellido,p_dni)
        self._cursos_del_estudiante = []
    
    @property #atributo
    def cursos_del_estudiante (self):
        return (self._cursos_del_estudiante)
    
    def agregar_cursos_del_estudiante (self, p_nombre_del_curso):
        self._cursos_del_estudiante.append(p_nombre_del_curso)

    def __repr__(self):
        salida = self._nombre + " " + self._apellido
        return(salida)
    
    def __str__(self):
        salida = self._nombre + " " + self._apellido
        return(salida)


class Profesor (Persona_Facultativa):
    def __init__(self,p_nombre, p_apellido,p_dni):
        super().__init__(p_nombre, p_apellido,p_dni)
        self._cursos_del_profesor = []
        self._dptos_del_profesor = []
        self._es_director = False

    @property #atributo
    def cursos_del_profesor (self):
        return (self._cursos_del_profesor)
    
    @property #atributo
    def deptos_del_profesor (self):
        return (self._dptos_del_profesor)
    
    @property #atributo
    def es_director (self):
        return (self._es_director)
    
    @es_director.setter #para modificar el atributo es_director
    def es_director (self, cambio_de_director):
        self._es_director = cambio_de_director

    def agregar_dpto_a_profesor(self, p_nombre_dpto):
        self._dptos_del_profesor.append(p_nombre_dpto)

    def atribuir_curso_al_profesor (self, p_nombre_del_curso):
        self._cursos_del_profesor.append(p_nombre_del_curso)

    def __repr__(self):
        salida = self._nombre + " " + self._apellido
        return(salida)
    
    def __str__(self):
        salida = self._nombre + " " + self._apellido
        return(salida)