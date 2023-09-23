from modules.clase_persona import Profesor
from modules.clase_curso import Curso
class Departamento:
    def __init__(self, nombre):
        self.__nombre=nombre
        self.__lista_integrantes=[]
        self.__director= None
        self.__lista_cursos=[]
    
    @property
    def nombre(self):
        return(self.__nombre)
    
    @property
    def lista_integrantes(self):
        return(self.__lista_integrantes)
    
    @property
    def director(self):
        return(self.__director)
    
    @property
    def lista_cursos(self):
        return(self.__lista_cursos)

    def agregar_profe(self, p_profesor):
        if isinstance(p_profesor, Profesor):
            self.__lista_integrantes.append(p_profesor)
            p_profesor.agregar_dpto_perteneciente(self)

                 
    def asignar_director(self, p_profesor):
        if isinstance(p_profesor, Profesor):
            if p_profesor in self.__lista_integrantes:
                if not p_profesor.es_jefe:
                    self.__director=p_profesor
                    p_profesor.es_jefe=True

    
    
    def asignar_profesor_curso(self, p_profesor, p_curso):
            if isinstance(p_profesor,Profesor):
                for curso in self.__lista_cursos:
                    if p_curso == curso.nombre:
                        curso.agregar_profesor(p_profesor)
                        
    def agregar_curso(self, p_curso):
        if isinstance(p_curso,Curso):
            if p_curso not in self.__lista_cursos:
                self.__lista_cursos.append(p_curso)
                p_curso.agregar_dpto_perteneciente(self)
    
    def __str__(self):
        salida=self.__nombre
        return (salida)
    def __repr__(self):
        salida=self.__nombre
        return (salida) #sirve para mostrar objetos dentro de una lista