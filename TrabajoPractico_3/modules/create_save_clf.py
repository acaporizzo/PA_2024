from modules.classifier import Classifier
from modules.create_csv import crear_csv
import pickle

datos = crear_csv("./data/frases.json")
X = datos['reclamo']
y = datos['etiqueta']

clf = Classifier()
clf.fit(X, y)

with open('./data/claims_clf.pkl', 'wb') as archivo:
    pickle.dump(clf, archivo)