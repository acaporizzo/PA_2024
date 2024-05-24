from modules import Usuario

class SecretarioTecnico(Usuario):
    def __init__(self, nombre, apellido, email, nombre_usuario, contraseña):
        super().__init__(nombre, apellido, email, nombre_usuario, 'secretario', contraseña)

    def ver_reclamos_dpto (self):
        pass

    def manejar_reclamo (self):
        pass
    
    def derivar_reclamo (self):
        pass
    