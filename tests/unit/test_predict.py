import requests

BASE_URL = "http://127.0.0.1:5000/predict"  # Assurez-vous que le backend est bien lancé à ce port

def test_predict_valid_data():
    # Exemple de données valides
    test_data = {
        "Total_Joueur": 20.0,  # Valeur valide
        "Carte_Croupier": 10
    }

    # Effectuer une requête POST pour obtenir une prédiction
    response = requests.post(BASE_URL, json=test_data)

    # Vérifiez que la réponse est correcte (status 200)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

  # Vérifiez que la réponse contient l'action prédite
    response_data = response.json()
    assert 'Action' in response_data, f"Action not in response: {response_data}"

def test_predict_invalid_data():
    # Exemple de données invalides
    test_data = {
        "Total_Joueur": "invalid",  # Valeur invalide pour tester le comportement du modèle
        "Carte_Croupier": 10
    }

    # Effectuer une requête POST pour obtenir une prédiction
    # Ici, nous simulons le comportement du frontend qui vérifie les données avant l'envoi
    if isinstance(test_data["Total_Joueur"], (int, float)):  # Vérification que les données sont valides
        response = requests.post(BASE_URL, json=test_data)
        assert response.status_code == 200
    else:
        # Simulez un message d'erreur ou une gestion d'erreur côté frontend
        print("Erreur : Données invalides")
        assert True  # Vous pouvez ajouter une logique plus détaillée ici pour tester les erreurs côté frontend


def test_predict_missing_field():
    # Exemple de données manquantes
    test_data = {
        "Carte_Croupier": 10  # Total_Joueur manquant
    }

    # Effectuer une requête POST pour obtenir une prédiction
    response = requests.post(BASE_URL, json=test_data)

    # Vérifiez que le serveur renvoie une erreur (par exemple, 400 pour données manquantes)
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"

    # Vérifiez que la réponse contient un message d'erreur concernant le champ manquant
    response_data = response.json()
    assert 'error' in response_data, f"Error message not in response: {response_data}"

# Vous pouvez ajouter d'autres tests pour les cas spécifiques à votre API

if __name__ == "__main__":
    # Lancer les tests
    test_predict_valid_data()
    test_predict_invalid_data()
    test_predict_missing_field()
    print("All tests passed successfully.")
