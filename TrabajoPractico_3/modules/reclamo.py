from datetime import datetime

class Reclamo:
    def _init_(self, id_reclamo, usuario, contenido, departamento, estado="pendiente"):
        self.id_reclamo = id_reclamo
        self.usuario = usuario
        self.contenido = contenido
        self.departamento = departamento
        self.fecha_hora = datetime.now()
        self.estado = estado
        self.usuarios_adheridos = []

    def clasificar_reclamo(self):
        pass

    def mostrar_reclamos_similares(self):
        pass