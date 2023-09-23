class Persona_Facultativa:
    def __init__(self,p_nombre, p_apellido,p_dni):
        self._nombre=p_nombre
        self._apellido=p_apellido
        self._dni=p_dni

    @property
    def nombre(self):
        return(self._nombre)
    @property
    def apellido(self):
        return(self._apellido)
    @property
    def dni (self):
        return(self._nombre)
    
    @nombre.setter
    def nombre(self,nombre_nuevo):
        self._nombre=nombre_nuevo

class Estudiante (Persona_Facultativa):
    def agregar_cursos_del_estudiante (self):
        pass
        

class Profesor (Persona_Facultativa):
    def agregarse_a_cursos(self):
        pass





