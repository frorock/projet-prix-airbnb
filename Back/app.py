from flask import Flask, request, jsonify
from flask_cors import CORS
import predict

# 🚀 Flask
app = Flask(__name__)
CORS(app)  # ⚠️ Active CORS pour toutes les routes et origines

@app.route("/predict", methods=["POST"])
def predict_route():
    try:
        data = request.get_json()  # Récupérer les données JSON envoyées

        # Appeler la fonction de prédiction depuis predict.py
        result = predict.predict_price(data)

        # Retourner la réponse en format JSON avec le prix prédit
        return jsonify({"prix": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
