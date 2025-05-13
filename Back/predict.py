import joblib
import pandas as pd
import os

# 📁 Chemins relatifs à ce fichier, compatibles Linux/GitHub Actions
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "Data", "modele_prix_airbnb.joblib")
FEATURES_PATH = os.path.join(BASE_DIR, "..", "Data", "features_model.txt")

def predict_price(data):
    """
    Fonction de prédiction du prix d'Airbnb à partir des données fournies.

    Arguments:
    - data: Dictionnaire contenant les paramètres d'entrée (latitude, longitude, etc.)

    Retour:
    - Prix prédit (float)
    """
    try:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError("Le fichier du modèle est introuvable.")

        if not os.path.exists(FEATURES_PATH):
            raise FileNotFoundError("Le fichier des colonnes est introuvable.")

        # Charger dynamiquement le modèle et les colonnes
        model = joblib.load(MODEL_PATH)

        with open(FEATURES_PATH, "r") as f:
            ordered_columns = f.read().splitlines()

        # Créer le DataFrame pour l'entrée utilisateur
        df_input = pd.DataFrame([data])
        df_input = df_input.reindex(columns=ordered_columns, fill_value=0)

        # Prédire
        prediction = model.predict(df_input)[0]
        return round(prediction, 2)

    except Exception as e:
        raise ValueError(f"Erreur dans la prédiction : {str(e)}")
