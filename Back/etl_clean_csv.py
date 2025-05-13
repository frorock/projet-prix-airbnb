# etl_model_ready.py

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# --- 📁 Chemins ---
BASE_DIR = r"D:\Projet_Ia_Indus"
INPUT_PATH = os.path.join(BASE_DIR, "Data", "AB_NYC_2019.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "Data", "AB_NYC_2019_model_ready.csv")

# --- 📥 EXTRACT ---
def extract(path):
    print("📥 Chargement du fichier source...")
    return pd.read_csv(path)

# --- 🛠️ TRANSFORM ---
def transform(df):
    print("🔧 Nettoyage et transformation des données...")

    # Nettoyage initial
    df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')
    df['reviews_per_month'] = df['reviews_per_month'].fillna(0)

    # Filtrage des valeurs aberrantes
    df = df[
        (df['price'] <= 1000) &
        (df['minimum_nights'] <= 365) &
        (df['latitude'].between(40.55, 40.91)) &
        (df['longitude'].between(-74.05, -73.75))
    ].copy()

    # Feature engineering
    df['is_high_demand'] = (df['number_of_reviews'] > 20).astype(int)

    # Colonnes utiles
    features = [
        'latitude', 'longitude', 'minimum_nights', 'number_of_reviews',
        'reviews_per_month', 'availability_365', 'room_type',
        'neighbourhood_group', 'is_high_demand', 'price'
    ]
    df = df[features]

    # Encodage des variables catégorielles
    df = pd.get_dummies(df, columns=['room_type', 'neighbourhood_group'], drop_first=True)

    # Ajout de la colonne manquante "logement_entier"
    if "room_type_Private room" in df.columns and "room_type_Shared room" in df.columns:
        df["room_type_Entire home/apt"] = 1 - (
            df["room_type_Private room"].astype(int) + df["room_type_Shared room"].astype(int)
        )

    # Clustering géographique
    kmeans = KMeans(n_clusters=10, random_state=42)
    df["zone_geo"] = kmeans.fit_predict(df[['latitude', 'longitude']])

    # Transformation logarithmique du prix
    df["prix_log"] = np.log1p(df["price"])

    # Normalisation des colonnes numériques
    scaler = StandardScaler()
    numeric_cols = ['minimum_nights', 'number_of_reviews', 'reviews_per_month', 'availability_365']
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    # 🏷️ Renommage en français
    rename_map = {
        'minimum_nights': 'nuits_min',
        'number_of_reviews': 'nombre_avis',
        'reviews_per_month': 'avis_par_mois',
        'availability_365': 'disponibilite_annuelle',
        'is_high_demand': 'forte_demande',
        'price': 'prix',
        'prix_log': 'prix_log'
    }

    for col in df.columns:
        if col.startswith("room_type_"):
            rename_map[col] = col.replace("room_type_", "type_logement_").replace(" ", "_").lower()
        if col.startswith("neighbourhood_group_"):
            rename_map[col] = col.replace("neighbourhood_group_", "quartier_").replace(" ", "_").lower()

    df.rename(columns=rename_map, inplace=True)

    return df

# --- 💾 LOAD ---
def load(df, path):
    print("💾 Sauvegarde dans :", path)
    df.to_csv(path, index=False, encoding="utf-8")
    print("✅ Données enregistrées avec succès.")

# --- 🚀 PIPELINE ---
def main():
    df_raw = extract(INPUT_PATH)
    df_ready = transform(df_raw)
    load(df_ready, OUTPUT_PATH)

if __name__ == "__main__":
    main()
