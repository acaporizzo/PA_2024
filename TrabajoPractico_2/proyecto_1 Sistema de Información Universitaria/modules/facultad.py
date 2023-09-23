class Facultad:
    def __init__(self,p_nombre_de_facu,p_dpto,primer_profesor):
        self._nombre_facu=p_nombre_de_facu

        self._departamentos=[Departamento(p_dpto,primer_profesor)]

        

    @property
    def nombre_dpto(self):
        return (self._nombre_dpto)  
    @property
    def nombre_facu (self):
        return (self._nombre_facu)
 
    def crear_departamentos(self,p_dpto,primer_profesor):

        self._departamentos.append(Departamento(p_dpto,primer_profesor))
    


