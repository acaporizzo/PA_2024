from modules.classifier import ClaimsClassifier
from modules.create_csv import crear_csv
import pickle

# Cargar los datos de entrenamiento
datos = crear_csv("./data/frases.json")
X = datos['reclamo']  # Textos de los reclamos
y = datos['etiqueta']  # Etiquetas de clasificación (departamentos)

# Entrenar el clasificador
clasificador = ClaimsClassifier(X=X, y=y, escalado=True)

# Guardar el modelo entrenado
with open('./data/claims_clf.pkl', 'wb') as archivo:
    pickle.dump(clasificador, archivo)

print("Clasificador entrenado y guardado en './data/claims_clf.pkl'")
