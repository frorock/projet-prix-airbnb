import pytest
import sys
import os

# Ajouter le chemin du dossier Back où se trouve app.py et predict.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Back')))


from predict import predict_price

def test_predict_price():
    """
    Test de la fonction predict_price
    """

    # Cas normal
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

    result = predict_price(data)
    assert isinstance(result, float), "La prédiction doit être un nombre à virgule flottante"
    assert result > 0, "Le prix prédit doit être positif"

    # Cas d'entrée manquante ou incorrecte
    with pytest.raises(ValueError):
        bad_data = {
            "latitude": "invalid",  # Mauvaise valeur
            "longitude": "invalid",  # Mauvaise valeur
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
        predict_price(bad_data)
