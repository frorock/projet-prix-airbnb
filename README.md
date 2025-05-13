# README - Prédiction de prix Airbnb à NYC

## 🎓 Objectif

Ce projet vise à prédire le **prix moyen par nuit d'un logement Airbnb à New York** en fonction de ses caractéristiques :

* localisation (latitude/longitude)
* type de logement
* nombre d'avis
* disponibilité annuelle, etc.

## ⚖️ Stack technique

* Python 3.9+
* Scikit-learn
* Pandas
* Flask (API REST)
* Streamlit (interface utilisateur)
* Selenium (tests UI)
* GitHub Actions (CI)

## 🔧 Installation

```bash
git clone https://github.com/<ton-user>/projet-prix-airbnb.git
cd projet-prix-airbnb
pip install -r requirements.txt
```

## 🚀 Lancer le projet

```bash
# 1. Nettoyage et préparation du dataset
python Back/etl_clean_csv.py

# 2. Entraînement du modèle
python Back/train_model.py

# 3. Lancer l'API Flask
python Back/app.py

# 4. (Optionnel) Interface Streamlit
streamlit run Front/streamlit_app.py
```

## 🌐 Interface utilisateur (Streamlit)

Une interface simple permet de prédire le prix en sélectionnant :

* le type de logement
* les paramètres du logement
* une position sur la carte (latitude/longitude)

## ✅ Lancer les tests

```bash
pytest
```

Les tests couvrent l'API et la fonction `predict_price()` (cas normaux, cas limites).

## 📅 Intégration continue

Le projet utilise GitHub Actions :

* Le fichier `.github/workflows/test.yml` permet de lancer les tests à chaque `push`.

## 🎨 Démo Selenium

### Script `test_ui_selenium.py`

Utilise Selenium pour tester l'interface Streamlit :

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

url = "http://localhost:8501"
driver = webdriver.Chrome()
driver.get(url)

time.sleep(5)
textarea = driver.find_element(By.TAG_NAME, "textarea")
textarea.send_keys("I love this service")

button = driver.find_element(By.XPATH, "//button[contains(., 'Prédire')]" )
button.click()

time.sleep(3)
result = driver.find_element(By.ID, "prediction")
assert "Prix estimé" in result.text

print("✅ Test Selenium passé")
driver.quit()
```


