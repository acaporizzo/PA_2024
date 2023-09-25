from modules.curso import Curso
from modules.departamento import Departamento 
from modules.persona_facultativa import Estudiante,Profesor

class Facultad:
    def __init__(self, p_nombre_facu, p_nombre_dpto_inicial, p_primer_profesor):    #facultad = Facultad (3 parámetros) para crear una nueva facultad
        self._departamentos = [Departamento (p_nombre_dpto_inicial, p_primer_profesor)]    #al crear una facultad se crea SI O SI un departamento
        self._estudiantes = []
        self._nombre_facu = p_nombre_facu
        
    @property #atributo
    def departamentos (self):
        return (self._departamentos)
    
    @property #atributo
    def estudiantes (self):
        return (self._estudiantes)
    
    @property #atributo
    def nombre_facu (self):
        return (self._nombre_facu)
    
    def atribuir_curso_al_dpto(self, p_nombre_del_curso, p_nombre_dpto):
        if isinstance(p_nombre_del_curso,Curso):
            for dpto in self._departamentos:
                if p_nombre_dpto == dpto._nombre_dpto:
                    dpto.atribuir_curso(p_nombre_del_curso)

    def atribuir_director_a_dpto (self, p_profesor, p_nombre_dpto):
        for depto in self._departamentos:
            if p_nombre_dpto == depto._nombre_dpto:
                depto.atribuir_director(p_profesor)

    def atribuir_dpto_a_profesor (self, p_nuevo_profesor, p_nombre_dpto):
        if isinstance(p_nuevo_profesor, Profesor):
            for dpto in self._departamentos:
                if p_nombre_dpto == dpto._nombre_dpto:
                    dpto.agregar_profesor_a_dpto(p_nuevo_profesor)

    def crear_departamento (self, p_nombre_dpto, p_profesor): #método
        self._departamentos.append(Departamento (p_nombre_dpto, p_profesor))

    def devolver_director_de_dpto (self, p_nombre_dpto):
        for dpto in self._departamentos:
            if p_nombre_dpto == dpto._nombre_dpto:
                return(dpto._director_de_dpto)
            
    def devolver_profesores_de_dpto(self, p_nombre_dpto):
        profesores_de_dpto = []
        for dpto in self._departamentos:
            if dpto._nombre_dpto == p_nombre_dpto:
                profesores_de_dpto = dpto._profesores
                break
        return(profesores_de_dpto)

    def inscribir_estudiante (self, p_nombre_de_estudiante):
        self._estudiantes.append(p_nombre_de_estudiante)

    def __repr__(self):
        salida = self._nombre_facu
        return(salida)
    
    def __str__(self):
        salida = self._nombre_facu
        return(salida)