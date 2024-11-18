import sqlite3

conexion = sqlite3.connect('mi_base_de_datos.db')  # Cambia al nombre de tu base de datos si es necesario
cursor = conexion.cursor()

try:
    cursor.execute("""
        INSERT INTO reclamos (id, id_usuario, contenido, clasificacion, estado, imagen, fecha)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ('f7902fad-619c-4d37-930a-526e68a0d92b', '9c02d37f-3f8c-41e0-b132-a8c9372f9cf4', 
          'No hay papel en el baño de mujeres', 'maestranza', 'pendiente', None, '2024-11-18 16:02:33'))
    conexion.commit()
    print("Inserción exitosa.")
except sqlite3.Error as e:
    print(f"Error al insertar: {e}")
finally:
    conexion.close()
