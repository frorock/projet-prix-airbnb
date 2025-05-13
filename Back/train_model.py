# train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# 📁 Chemins
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "Data", "AB_NYC_2019_model_ready.csv")
MODEL_PATH = os.path.join(BASE_DIR, "Data", "modele_prix_airbnb.joblib")
FEATURES_PATH = os.path.join(BASE_DIR, "Data", "features_model.txt")

# 📥 Chargement des données
df = pd.read_csv(DATA_PATH)

# 🎯 Cible
y = df["prix"]

# 🧠 Features
X = df.drop(columns=["prix", "prix_log"])

# 🔀 Séparation train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 🤖 Entraînement
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 💾 Sauvegarde du modèle
joblib.dump(model, MODEL_PATH)
print(f"✅ Modèle entraîné et sauvegardé dans : {MODEL_PATH}")

# 💾 Sauvegarde de l'ordre des colonnes
with open(FEATURES_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(X.columns))
print(f"📄 Colonnes sauvegardées dans : {FEATURES_PATH}")
