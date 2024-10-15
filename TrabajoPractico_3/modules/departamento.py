class Departamento:
    def _init_(self, nombre):
        self.id_departamento = int
        self.nombre = nombre
        self.reclamos = []  # Reclamos asociados al departamento

    def asignar_tiempo_resolucion(self, reclamo):
        pass

    def modificar_estado_reclamo(self):
        pass