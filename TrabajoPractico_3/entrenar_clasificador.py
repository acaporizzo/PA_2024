from modules.classifier import ClaimsClassifier
import pickle
import os

# Define los datos de entrenamiento en X e y (debes reemplazarlos con datos reales)
X = ["Ejemplo de texto para clasificar", "Otro ejemplo de reclamo"]  # Lista de textos de reclamos
y = [0, 1]  # Etiquetas correspondientes (por ejemplo, 0 para 'secretaría técnica', 1 para 'soporte informático')

# Crea una instancia de Classifier y entrena el modelo
classifier = ClaimsClassifier(X, y, escalado=True)

# Verifica que la carpeta `data` exista, y si no, créala
if not os.path.exists('./data'):
    os.makedirs('./data')

# Guarda el modelo entrenado en `claims_clf.pkl`
with open('./data/claims_clf.pkl', 'wb') as f:
    pickle.dump(classifier, f)
print("Modelo guardado exitosamente en './data/claims_clf.pkl'")
