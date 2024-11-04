from modules.dominio import Reclamo
from datetime import datetime
import uuid

class GestorReclamo:
    def __init__(self, repositorio_reclamos):
        self.repositorio = repositorio_reclamos

    def mostrar_reclamos(self):
        return self.repositorio.obtener_todos_los_registros()

    def mostrar_reclamos_de_usuario(self, usuario):
        return self.repositorio.obtener_registros_seguidas_por_usuario(usuario)

    def crear_reclamo(self, usuario, contenido, departamento):
        nuevo_reclamo = Reclamo(
            id_reclamo=uuid.uuid4(),
            usuario=usuario,
            contenido=contenido,
            departamento=departamento,
            fecha_hora=datetime.now(),
            estado="pendiente",
            usuarios_adheridos=[usuario]
        )
        self.repositorio.guardar_registro(nuevo_reclamo)
        return nuevo_reclamo

    def adherir_a_reclamo(self, id_reclamo, usuario):
        reclamo = self.repositorio.obtener_registro_por_filtro("id_reclamo", id_reclamo)
        if reclamo and usuario not in reclamo.usuarios_adheridos:
            reclamo.usuarios_adheridos.append(usuario)
            self.repositorio.modificar_registro(reclamo)
            return True
        return False

    def derivar_reclamo(self, id_reclamo, nuevo_departamento):
        reclamo = self.repositorio.obtener_registro_por_filtro("id_reclamo", id_reclamo)
        if reclamo:
            reclamo.departamento = nuevo_departamento
            self.repositorio.modificar_registro(reclamo)
            return reclamo
        return None

    def modificar_estado_reclamo(self, id_reclamo, nuevo_estado):
        reclamo = self.repositorio.obtener_registro_por_filtro("id_reclamo", id_reclamo)
        if reclamo:
            reclamo.estado = nuevo_estado
            self.repositorio.modificar_registro(reclamo)
            return reclamo
        return None
