# train_dummy.py
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import joblib

# 1) jeu de données jouet
X, y = load_iris(return_X_y=True)

# 2) petit modèle très simple
clf = LogisticRegression(max_iter=200)
clf.fit(X, y)

# 3) on le sauvegarde
joblib.dump(clf, "model.pkl")
print("✅ model.pkl enregistré")
