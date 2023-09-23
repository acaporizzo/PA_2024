class Persona:
    def __init__(self, DNI, nombre_y_apellido, correo):
        self.__DNI= DNI
        self.__nombre_y_apellido= nombre_y_apellido
        self.__correo= correo

    @property
    def nombre_y_apellido(self):
        return(self.__nombre_y_apellido)
    
    @property
    def DNI(self):
        return(self.__DNI)

    @property
    def correo(self):
        return(self.__correo)


    def __str__(self):
        salida=self.__nombre_y_apellido
        return (salida) #muestra solo objeto con sus atributos
    
    def __repr__(self):
        salida=self.__nombre_y_apellido
        return (salida) #sirve para mostrar objetos dentro de una lista
    

class Alumno(Persona):
    def __init__(self, DNI, nombre, correo):
        super().__init__(DNI, nombre, correo)
        self.__cursos_inscriptos=[]

    @property
    def cursos_inscriptos(self):
        return(self.__cursos_inscriptos)
    
    def agregar_cursos_inscriptos(self,p_curso):
        self.__cursos_inscriptos.append(p_curso)

    def __str__(self):
        salida=self.nombre_y_apellido
        return (salida) #muestra solo objeto con sus atributos
    
    def __repr__(self):
        salida=self.nombre_y_apellido
        return (salida) #sirve para mostrar objetos dentro de una lista

class Profesor(Persona):
    
    def __init__(self, DNI, nombre, correo):
        super().__init__(DNI, nombre, correo)
        self.__es_jefe = False
        self.__dptos=[]
        self.__cursos_dictados=[]
    
    @property
    def es_jefe(self):
        return(self.__es_jefe)
   
    @es_jefe.setter
    def es_jefe(self,p_valor):
        self.__es_jefe=p_valor

    @property
    def dptos(self):
        return(self.__dptos)   

    @property
    def cursos_dictados(self):
        return(self.__cursos_dictados) 
    
    def agregar_cursos_dictados(self,p_curso):
        self.__cursos_dictados.append(p_curso)

    def agregar_dpto_perteneciente(self, p_dpto):
        self.__dptos.append(p_dpto)


