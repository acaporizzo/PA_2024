from modules.curso import Curso
from modules.departamento import Departamento 
from modules.persona_facultativa import Profesor, Estudiante

class Facultad:
    def __init__(self, p_nombre_facu, p_nombre_dpto_inicial, nombre_profesor, apellido_profesor, dni_profesor): 
        """ Método constructor en el cual al crear una facultad se crea SI O SI un departamento
        """
        self._cursos = []
        primer_profesor = Profesor(nombre_profesor, apellido_profesor, dni_profesor)
        self._departamentos = [Departamento(p_nombre_dpto_inicial, primer_profesor)]
        self._estudiantes = []
        self._nombre_facu = p_nombre_facu
        self._profesores = [primer_profesor]

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
    
    def inscribir_estudiante(self, nombre, apellido, dni):
        """Método para agregar un nuevo estudiante a la facultad
        """
        estudiante = Estudiante(nombre, apellido, dni)
        self._estudiantes.append(estudiante)
        return estudiante
    
    def mostrar_estudiantes(self):
        """ Método para mostrar todos los estudiantes inscriptos en la facultad """
        if not self._estudiantes:
            print("No hay estudiantes inscriptos.")
        else:
            for idx, estudiante in enumerate(self._estudiantes, start=1):
                print(f"{idx}: {estudiante.nombre} {estudiante.apellido}")

    
    
    def contratar_profesor(self,  nombre, apellido, dni):
        """método para agregar un nuevo profesor a la facultad
        """
        profesor = Profesor(nombre, apellido, dni)
        self._profesores.append(profesor)
        return profesor
    
    def mostrar_profesores(self):
        """ Método para mostrar todos los profesores contratados en la facultad """
        if not self._profesores:  # Verifica si la lista de profesores está vacía
            print("No hay profesores contratados.")
        else:
            for idx, profesor in enumerate(self._profesores, start=1):
                print(f"{idx}: {profesor.nombre} {profesor.apellido}")



    def verificar_nombre_departamento(self, nombre_dpto):
        """Verifica si el nombre del departamento ya existe."""
        return not any(departamento.nombre_dpto == nombre_dpto for departamento in self._departamentos)

    def asignar_director(self,num_profesor_elegido):
        """Selecciona y retorna un profesor para ser asignado como director."""
        try:
            if num_profesor_elegido < 1 or num_profesor_elegido > len(self._profesores):
                print(f"Error: El número de profesor debe estar entre 1 y {len(self._profesores)}.")
                return None 
            profesor_director = self.obtener_profesor(num_profesor_elegido - 1)
            if profesor_director and not profesor_director.es_director:
                return profesor_director  # Si el profesor no es ya director, lo retorna
            return None  # Si el profesor ya es director, devuelve None
        except (ValueError, IndexError):
            return None  # Devuelve None si el índice es inválido o si se ingresa un valor no numérico

    def crear_departamento(self, nombre_dpto, profesor_director):
        """Crea un nuevo departamento con el profesor seleccionado como director."""
        nuevo_departamento = Departamento(nombre_dpto, profesor_director)
        self._departamentos.append(nuevo_departamento)
        profesor_director.es_director = True  # Actualiza el estado del profesor
        return nuevo_departamento  # Retorna el departamento creado
    
    def mostrar_departamentos(self):
        if not self.departamentos:
            print("No hay departamentos disponibles.")
        else:
            print("Departamentos disponibles:")
            for idx, departamento in enumerate(self.departamentos, start=1):
                print(f"{idx}: {departamento.nombre_dpto}")



    def verificar_nombre_curso(self, nombre_curso):
        """Verifica si un curso con el mismo nombre ya existe."""
        return any(curso.nombre_curso == nombre_curso for curso in self._cursos)

    def crear_curso(self, p_nombre_curso, p_profesor):
        """Crea un curso si el nombre no está duplicado."""
        if self.verificar_nombre_curso(p_nombre_curso):
            return None  # Retorna None si el curso ya existe
        curso = Curso(p_nombre_curso, p_profesor)
        self._cursos.append(curso)
        return curso

    def atribuir_curso_al_dpto(self, curso, p_nombre_dpto):
        """Método para agregar un curso a un departamento."""
        if isinstance(curso, Curso):
            for dpto in self._departamentos:
                if p_nombre_dpto == dpto.nombre_dpto:
                    dpto.atribuir_curso(curso)

    def seleccionar_profesor(self):
        """Selecciona un profesor por su número, validando el rango."""
        try:
            num_profesor_elegido = int(input("Selecciona el número de profesor: "))
            if num_profesor_elegido < 1 or num_profesor_elegido > len(self._profesores):
                return None  # Retorna None si el número está fuera de rango
            return self.obtener_profesor(num_profesor_elegido - 1)
        except (ValueError, IndexError):
            return None  # Retorna None si hay un error en la entrada

    def seleccionar_departamento(self):
        """Selecciona un departamento por su número, validando el rango."""
        try:
            num_dpto_elegido = int(input("Selecciona el número de departamento: "))
            if num_dpto_elegido < 1 or num_dpto_elegido > len(self._departamentos):
                return None  # Retorna None si el número está fuera de rango
            return self.obtener_departamento(num_dpto_elegido - 1)
        except (ValueError, IndexError):
            return None  # Retorna None si hay un error en la entrada





    def agregar_departamento(self, departamento):
        """Método para agregar un departamento a la facultad."""
        self._departamentos.append(departamento)

    def obtener_departamento(self, indice):
        """Método para obtener un departamento por su índice."""
        try:
            return self._departamentos[indice]  # Retorna el departamento correspondiente al índice
        except IndexError:
            print("Índice de departamento no válido. Por favor, elige uno de la lista.")
            return None  # Devuelve None si el índice es inválido
            
    
                    
    def guardar_profesor(self, profesor):
        """Este método guarda al profesor en la lista de profesores."""
        self.profesores.append(profesor)
        print(f"Profesor {profesor['nombre']} {profesor['apellido']} guardado con éxito.")
      
    def atribuir_dpto_a_profesor (self, p_nuevo_profesor, p_nombre_dpto):
        """método para inscribir a un profesor en un dpto
        """
        if isinstance(p_nuevo_profesor, Profesor):
            for dpto in self._departamentos:
                if p_nombre_dpto == dpto.nombre_dpto:
                    dpto.agregar_profesor_a_dpto(p_nuevo_profesor) #en departamento.py
    
    def listar_profesores(self):
        """Este método lista todos los profesores contratados."""
        for profesor in self.profesores:
            print(f"{profesor['nombre']} {profesor['apellido']} - DNI: {profesor['dni']}")


  
            
    def devolver_estudiantes_de_curso(self, p_nombre_curso):
        """método para mostrar los estudiantes de un curso en específico
        """
        for curso in self._cursos:
            if p_nombre_curso == curso.nombre_curso:
                return curso.estudiantes_del_curso


    
    def obtener_profesor(self, num_profesor):
        """ Método para obtener un profesor según su índice en la lista de profesores """
        try:
            return self._profesores[num_profesor]
        except IndexError:
            print(f"Error: El número de profesor proporcionado ({num_profesor}) no es válido. Debes elegir un número entre 0 y {len(self._profesores) - 1}.")
            return None  # O puedes decidir lanzar nuevamente la excepción si prefieres

    
    def obtener_estudiante(self, num_estudiante):
        """ Método para obtener un estudiante según su índice """
        try:
            return self._estudiantes[num_estudiante - 1]  # Restamos 1 porque la enumeración inicia en 1
        except IndexError:
            print(f"Error: El número de estudiante proporcionado ({num_estudiante}) no es válido.")
            return None
        
    def mostrar_cursos(self):
        """ Método para mostrar todos los cursos disponibles """
        if not self._cursos:
            print("No hay cursos disponibles.")
        else:
            print("Cursos disponibles:")
            for idx, curso in enumerate(self._cursos, start=1):
                print(f"{idx}: {curso.nombre_curso}")



    def __repr__(self):
        """método para definir la representación de cadena de una instancia de una clase
        """
        return self._nombre_facu
        
    
    def __str__(self):
        """para definir una representación legible de una instancia de una clase o 
        cuando se intenta imprimir la instancia
        """
        return self._nombre_facu
        
    


    #def crear_departamento (self, p_nombre_dpto, p_profesor):
        #"""método para crear un nuevo dpto y agregarlo a la lista
        #"""
        #departamento = Departamento(p_nombre_dpto, p_profesor)
        #self._departamentos.append(Departamento(p_nombre_dpto, p_profesor))
        #return departamento

                
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