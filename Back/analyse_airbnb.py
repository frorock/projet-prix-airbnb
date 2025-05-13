import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# --- 📁 Chemins ---
BASE_DIR = r"D:\Projet_Ia_Indus"
RAW_CSV = os.path.join(BASE_DIR, "Data", "AB_NYC_2019.csv")
CLEAN_CSV = os.path.join(BASE_DIR, "Data", "AB_NYC_2019_model_ready.csv")
csv_path = RAW_CSV  # ✅ Change ici pour analyser le fichier voulu
logs_folder = os.path.join(BASE_DIR, "Analyses")
viz_folder = os.path.join(logs_folder, "visualisations")
os.makedirs(logs_folder, exist_ok=True)
os.makedirs(viz_folder, exist_ok=True)
report_file = os.path.join(logs_folder, f"rapport_analyse_{os.path.basename(csv_path)}.txt")

# --- 📥 Chargement des données ---
df = pd.read_csv(csv_path)

# --- 📊 Analyse texte ---
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
content = []
content.append(f"\n📊 Analyse de {os.path.basename(csv_path)} - {timestamp}")
content.append("-" * 80)
content.append(f"🔢 Dimensions : {df.shape[0]} lignes, {df.shape[1]} colonnes")
content.append(f"📛 Colonnes : {list(df.columns)}")
content.append(f"🔠 Types :\n{df.dtypes}")
content.append(f"❓ Valeurs manquantes :\n{df.isnull().sum()}")
content.append(f"🧮 Total NaN : {df.isnull().sum().sum()}")

if 'price' in df.columns:
    content.append(f"\n📊 Statistiques descriptives des prix :\n{df['price'].describe()}")

if 'minimum_nights' in df.columns:
    content.append(f"⚠️ Séjours > 365 nuits : {(df['minimum_nights'] > 365).sum()}")

if 'calculated_host_listings_count' in df.columns:
    content.append(f"👥 Hôtes avec > 50 annonces : {(df['calculated_host_listings_count'] > 50).sum()}")

if 'latitude' in df.columns and 'longitude' in df.columns:
    bad_geo = df[~df['latitude'].between(40.5, 40.95) | ~df['longitude'].between(-74.25, -73.7)]
    content.append(f"🗺️ Coordonnées hors NYC : {bad_geo.shape[0]} lignes")

if 'neighbourhood_group' in df.columns:
    group_price = df.groupby("neighbourhood_group")["price"].mean().sort_values(ascending=False)
    content.append(f"\n💰 Prix moyen par quartier :\n{group_price}")

# --- 📝 Rapport écrit ---
with open(report_file, "w", encoding="utf-8") as f:
    for line in content:
        f.write(str(line) + "\n")
print(f"✅ Rapport généré : {report_file}")

# --- 📊 Distribution des prix ---
if 'price' in df.columns:
    plt.figure(figsize=(10, 6))
    sns.histplot(df['price'], bins=100, kde=True)
    plt.title("Distribution des prix (≤ 1000$)")
    plt.xlabel("Prix ($)")
    plt.ylabel("Nombre de logements")
    hist_path = os.path.join(viz_folder, "distribution_prix.png")
    plt.savefig(hist_path, dpi=300)
    plt.close()

# --- 📈 Prix vs Nuits ---
if 'minimum_nights' in df.columns and 'price' in df.columns:
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df[df['minimum_nights'] <= 100], x="minimum_nights", y="price", alpha=0.4)
    plt.title("Prix vs Nuits minimum")
    plt.xlabel("Nuits minimum")
    plt.ylabel("Prix ($)")
    scatter_path = os.path.join(viz_folder, "prix_vs_nuits.png")
    plt.savefig(scatter_path, dpi=300)
    plt.close()

# --- 📊 Prix moyen par type de logement ---
room_type_col = [col for col in df.columns if "type_logement_" in col or col == "room_type"]
if room_type_col and 'price' in df.columns:
    if 'room_type' in df.columns:
        room_prices = df.groupby("room_type")["price"].mean().sort_values()
    else:
        melted = df[room_type_col + ['price']].copy()
        melted = melted.melt(id_vars='price', var_name='type', value_name='valeur')
        melted = melted[melted['valeur'] == 1]
        room_prices = melted.groupby("type")["price"].mean().sort_values()

    plt.figure(figsize=(8, 6))
    sns.barplot(x=room_prices.values, y=room_prices.index, color="skyblue")
    plt.title("Prix moyen par type de logement")
    plt.xlabel("Prix moyen ($)")
    plt.ylabel("Type de logement")
    barplot_path = os.path.join(viz_folder, "prix_par_type.png")
    plt.savefig(barplot_path, dpi=300)
    plt.close()
