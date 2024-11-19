
from modules.config import db, app
from modules.modelos import ModeloReclamo

def eliminar_reclamos_repetidos(id_reclamo_1, id_reclamo_2):
    with app.app_context():  # Usar el contexto de la aplicación
        try:
            reclamo_1 = db.session.query(ModeloReclamo).filter_by(id=id_reclamo_1).first()
            if reclamo_1:
                db.session.delete(reclamo_1)

            reclamo_2 = db.session.query(ModeloReclamo).filter_by(id=id_reclamo_2).first()
            if reclamo_2:
                db.session.delete(reclamo_2)

            db.session.commit()
            print("Los reclamos duplicados fueron eliminados exitosamente.")
        except Exception as e:
            db.session.rollback()
            print(f"Error al eliminar los reclamos: {e}")

# Llamar a la función
eliminar_reclamos_repetidos('b73b146f-87ed-4b74-a698-6e1aa894bd42', 'd27b1d41-9057-41bb-bd12-f2f53d124f7b')
