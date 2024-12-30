from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
import joblib
import pandas as pd
import os
import mlflow
import mlflow.pyfunc
from sklearn.preprocessing import LabelEncoder
import dagshub

app = Flask(__name__)
CORS(app)  # Autorise toutes les origines par défaut

# Obtenir le chemin du répertoire courant du fichier (main.py)
# Configuration de MLFlow avec l'URI de suivi
dagshub.init(repo_owner='Xxwdsdfs', repo_name='ml-production-app', mlflow=True)

# Charger le modèle depuis MLFlow
model_uri = "models:/DecisionTree/1"  # Assure-toi de mettre la bonne version du modèle ici
model = mlflow.pyfunc.load_model(model_uri)
print(f"Modèle chargé depuis : {model_uri}")

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
    
    # Convertir les colonnes en float64
    exemple['Total_Joueur'] = exemple['Total_Joueur'].astype('float64')
    exemple['Carte_Croupier'] = exemple['Carte_Croupier'].astype('float64')

    prediction = model.predict(exemple)
    # Encodage des résultats de l'action (tirer/rester) avec LabelEncoder
    encoder = LabelEncoder()
    actions = ['tirer', 'rester']  # Possible actions (tirer/rester)
    encoder.fit(actions)  # On entraîne l'encoder sur ces valeurs
    action = encoder.inverse_transform(prediction)

    return jsonify({"Total_Joueur": total_joueur, "Carte_Croupier": carte_croupier, "Action": action[0]})

if __name__ == '__main__':
    app.run(debug=True, port=5000)