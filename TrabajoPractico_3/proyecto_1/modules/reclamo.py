import datetime
import uuid
class Reclamo:
    def __init__(self, usuario, contenido, departamento):
        self.id_reclamo = uuid.uuid4()
        self.usuario = usuario
        self.contenido = contenido
        self.departamento = departamento
        self.fecha_hora = datetime.datetime.now()
        self.estado = 'pendiente'
        self.usuarios_adheridos = [usuario]

    def clasificar_reclamo(self):
        pass

    def mostrar_similares(self):
        pass

    def cambiar_estado(self):
        pass

    def devolver_reclamos(self):
        pass