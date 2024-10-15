import sqlite3
from reclamo import Reclamo
from usuario import Usuario, UsuarioFinal

class BaseDatos:
    def _init_(self, db_name="crm_reclamos.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def guardar_usuario(self, usuario: Usuario):
        self.cursor.execute('INSERT INTO usuarios (nombre, apellido, email, nombre_usuario, contraseña, claustro) VALUES (?, ?, ?, ?, ?, ?)', 
                            (usuario.nombre, usuario.apellido, usuario.email, usuario.nombre_usuario, usuario.contraseña, usuario.claustro))
        self.conn.commit()

    def filtrar_reclamo_departamento(self):
        pass

    def guardar_reclamo(self, reclamo: Reclamo):
        self.cursor.execute('INSERT INTO reclamos (id_usuario, contenido, estado, departamento, fecha) VALUES (?, ?, ?, ?, ?)', 
                            (reclamo.usuario, reclamo.contenido, reclamo.estado, reclamo.departamento, reclamo.fecha))
        self.conn.commit()

    def listar_reclamos(self):
        pass
