from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
import joblib
import pandas as pd
import os
import mlflow
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
CORS(app)  # Autorise toutes les origines par défaut

# Définir l'URI pour MLFlow
mlflow.set_tracking_uri("http://localhost:5000")  # URI pour accéder à MLFlow UI
model_uri = "models:/Model_Finalv2/1"  # Remplace 'model_final' par ton modèle enregistré

# Charger le modèle depuis MLFlow
model = mlflow.sklearn.load_model(model_uri)
print(f"Modèle chargé depuis MLFlow : {model_uri}")

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
    encoder = LabelEncoder()
    actions = ['tirer', 'rester']  # Possible actions (tirer/rester)
    encoder.fit(actions)  # On entraîne l'encoder sur ces valeurs
    action = encoder.inverse_transform(prediction)

    return jsonify({"Total_Joueur": total_joueur, "Carte_Croupier": carte_croupier, "Action": action[0]})

if __name__ == '__main__':
    app.run(debug=True, port=5000)