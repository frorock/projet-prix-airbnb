import sys
import os
import pytest


# Ajouter le chemin du dossier Back où se trouve app.py et predict.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Back')))

from app import app  # Assurez-vous que le fichier app.py est dans le dossier Back

# Tester le comportement de l'API
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_predict(client):
    """
    Test de l'API /predict
    """
    # Données d'entrée pour la prédiction
    data = {
        "latitude": 40.73,
        "longitude": -73.99,
        "nuits_min": 2,
        "nombre_avis": 30,
        "avis_par_mois": 1.2,
        "disponibilite_annuelle": 150,
        "forte_demande": 1,
        "type_logement_entire_home/apt": 1,
        "type_logement_private_room": 0,
        "type_logement_shared_room": 0,
        "quartier_brooklyn": 0,
        "quartier_manhattan": 1,
        "quartier_queens": 0,
        "zone_geo": 3
    }

    # Requête POST à l'API
    response = client.post('/predict', json=data)

    # Vérifier que la réponse est valide et que le prix est retourné
    assert response.status_code == 200
    response_json = response.get_json()
    assert 'prix' in response_json, "La clé 'prix' est absente dans la réponse"
    assert isinstance(response_json['prix'], float), "Le prix prédit doit être un nombre à virgule flottante"

def test_invalid_data(client):
    """
    Test d'une entrée invalide dans l'API
    """
    invalid_data = {
        "latitude": "invalid",
        "longitude": "invalid",
        "nuits_min": 2,
        "nombre_avis": 30,
        "avis_par_mois": 1.2,
        "disponibilite_annuelle": 150,
        "forte_demande": 1,
        "type_logement_entire_home/apt": 1,
        "type_logement_private_room": 0,
        "type_logement_shared_room": 0,
        "quartier_brooklyn": 0,
        "quartier_manhattan": 1,
        "quartier_queens": 0,
        "zone_geo": 3
    }

    response = client.post('/predict', json=invalid_data)
    assert response.status_code == 400
    response_json = response.get_json()
    assert 'error' in response_json, "Erreur attendue mais non reçue"
