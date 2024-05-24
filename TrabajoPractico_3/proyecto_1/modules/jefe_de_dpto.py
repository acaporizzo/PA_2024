from modules import Usuario

class JefeDepartamento(Usuario):
    def __init__(self, nombre, apellido, email, nombre_usuario, contraseña, departamento):
        super().__init__(nombre, apellido, email, nombre_usuario, 'jefe', contraseña)
        self.departamento = departamento

    def ver_reclamos_dpto (self):
        pass

    def manejar_reclamo (self):
        pass
    
    def derivar_reclamo (self):
        pass
    