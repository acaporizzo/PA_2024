import pickle
from modules.classifier import ClaimsClassifier
from modules.create_csv import crear_csv

# Cargar los datos desde el archivo JSON
datos = crear_csv("./data/frases.json")
X = datos['reclamo']
y = datos['etiqueta']

# Crear una instancia del clasificador y entrenarlo
clf = ClaimsClassifier()
clf.fit(X, y)

# Guardar el modelo entrenado en un archivo pickle
with open('./data/claims_clf.pkl', 'wb') as archivo:
    pickle.dump(clf, archivo)

print("Modelo entrenado y guardado como 'claims_clf.pkl'")
