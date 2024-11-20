from modules.config import app, db
from modules.dominio import Usuario
from modules.gestores import GestorBaseDeDatos

Jefe1=Usuario(0, "Juan", "Perez", "j_perez", "jperez@gmail.com", "blabla", "PAyS", "Jefe de Departamento", "Secretaría técnica")
Jefe2=Usuario(0, "Maria", "Gomez", "m_gomez", "mgomez@gmail.com", "blabla", "PAyS", "Jefe de Departamento", "Maestranza")
Jefe3=Usuario(0, "Pedro", "Martinez", "p_martinez", "pmartinez@gmail.com", "blabla", "PAyS", "Jefe de Departamento", "Soporte informático")

datos_jefe1=[Jefe1.nombre, Jefe1.apellido, Jefe1.nombre_usuario, Jefe1.email, Jefe1.contraseña, Jefe1.claustro, Jefe1.rol, Jefe1.departamento]
datos_jefe2=[Jefe2.nombre, Jefe2.apellido, Jefe2.nombre_usuario, Jefe2.email, Jefe2.contraseña, Jefe2.claustro, Jefe2.rol, Jefe2.departamento]
datos_jefe3=[Jefe3.nombre, Jefe3.apellido, Jefe3.nombre_usuario, Jefe3.email, Jefe3.contraseña, Jefe3.claustro, Jefe3.rol, Jefe3.departamento]

with app.app_context():
    db.create_all()
    GestorDB=GestorBaseDeDatos()
    GestorDB.guardar_nuevo_objeto("jefe", datos_jefe1)
    GestorDB.guardar_nuevo_objeto("jefe", datos_jefe2)
    GestorDB.guardar_nuevo_objeto("jefe", datos_jefe3)