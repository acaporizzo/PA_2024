from modules.reclamo import Reclamo
from modules.base_datos import bd   #bd es una instancia de la clase basededatos
from modules.generador_reporte import GeneradorReporte
from modules.analizador_estadisticas import AnalizadorEstadisticas

class Usuario:
    def _init_(self, nombre, apellido, email, nombre_usuario, contraseña, claustro):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.nombre_usuario = nombre_usuario
        self.contraseña = contraseña
        self.claustro = claustro
    
    def registrar(self):
        pass
    
    def iniciar_sesion(self, email, contraseña):
        pass

# UsuarioFinal, JefeDepartamento y SecretarioTecnico heredan de la clase base Usuario: --------------------------

class UsuarioFinal(Usuario):
    def crear_reclamo(self, contenido, departamento, bd):
        reclamo = Reclamo(None, self.nombre_usuario, contenido, departamento)
        bd.guardar_reclamo(reclamo)

    def listar_reclamos(self, bd):
        pass

    def adherirse_a_reclamo(self, bd):
        pass


class JefeDepartamento(Usuario):
    def _init_(self, nombre, apellido, email, nombre_usuario, contraseña, claustro, departamento):
        super()._init_(nombre, apellido, email, nombre_usuario, contraseña, claustro)
        self.departamento = departamento
        self.reporte = GeneradorReporte()
        self.analizador = AnalizadorEstadisticas()
    
    def ver_panel(self):
        pass
    
    def manejar_reclamo(self, bd):
        return bd.listar_reclamos_por_departamento(self.departamento)

    def generar_reporte(self, formato="PDF"):
        reclamos = self.manejar_reclamos(bd)
        estadisticas = self.analizador.calcular_estadisticas(reclamos)
        return self.reporte.generar_reporte(reclamos, estadisticas, formato)


class SecretarioTecnico(Usuario):
    def ver_panel(self):
        pass

    def derivar_reclamo(self, reclamo_id, nuevo_departamento, bd):
        bd.actualizar_departamento_reclamo(reclamo_id, nuevo_departamento)