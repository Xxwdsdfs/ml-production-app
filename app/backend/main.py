from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
import joblib
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Autorise toutes les origines par défaut

# Obtenir le chemin du répertoire courant du fichier (main.py)
current_dir = os.path.dirname(__file__)

# Construire un chemin relatif pour le modèle
model_path = os.path.join(current_dir, "../../ml/model_registry/model.joblib")

# Charger le modèle
model, encoder = joblib.load(model_path)
print(f"Modèle chargé depuis : {model_path}")

# Route d'accueil (pour éviter l'erreur 404)
@app.route('/', methods=['GET'])
def home():
    return "Bienvenue sur l'API de prédiction Blackjack !"

# Route pour les prédictions
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    total_joueur = data.get('Total_Joueur')
    carte_croupier = data.get('Carte_Croupier')

    if total_joueur is None or carte_croupier is None:
        return jsonify({"error": "Veuillez fournir Total_Joueur et Carte_Croupier"}), 400

    exemple = pd.DataFrame([[total_joueur, carte_croupier]], columns=['Total_Joueur', 'Carte_Croupier'])
    prediction = model.predict(exemple)
    action = encoder.inverse_transform(prediction)

    return jsonify({"Total_Joueur": total_joueur, "Carte_Croupier": carte_croupier, "Action": action[0]})

if __name__ == '__main__':
    app.run(debug=True, port=5000)