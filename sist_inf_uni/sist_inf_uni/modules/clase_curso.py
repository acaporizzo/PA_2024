from modules.clase_persona import Alumno
class Curso:

    def __init__(self, nombre, profesor_a_cargo):
        self.__nombre=nombre
        self.__profesor_a_cargo=profesor_a_cargo
        profesor_a_cargo.agregar_cursos_dictados(self)
        self.__estudiantes=[]
        self.__dpto=[]
    
    @property
    def nombre(self):
        return(self.__nombre)

    @property
    def profesor_a_cargo(self):
        return(self.__profesor_a_cargo)
    
    @property
    def estudiantes(self):
        return(self.__estudiantes)

    @property
    def dpto(self):
        return(self.__dpto)
    
    def agregar_alumno(self, p_alumno):
        if isinstance(p_alumno, Alumno):
            self.__estudiantes.append(p_alumno)
            p_alumno.agregar_cursos_inscriptos(self)
    

    def agregar_dpto_perteneciente(self, p_dpto):
        self.__dpto.append(p_dpto)
    
    
    def __str__(self):
        salida=self.__nombre
        return (salida)
    
    def __repr__(self):
        salida=self.__nombre
        return (salida) #sirve para mostrar objetos dentro de una lista