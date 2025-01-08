<template>
  <div id="app">
    <div class="casino-background">
      <h1 class="title">Blackjack Prediction</h1>
      <form @submit.prevent="makePrediction" class="prediction-form">
        <div class="form-group">
          <label for="total_joueur">Your hand :</label>
          <input v-model="totalJoueur" type="number" id="total_joueur" required class="input-field"/>
          <div v-if="totalJoueurError" class="error-message">{{ totalJoueurError }}</div>
        </div>

        <div class="form-group">
          <label for="carte_croupier">Dealer's hand :</label>
          <input v-model="carteCroupier" type="number" id="carte_croupier" required class="input-field"/>
          <div v-if="carteCroupierError" class="error-message">{{ carteCroupierError }}</div>
        </div>

        <button type="submit" class="submit-btn">Win some money</button>
      </form>

      <div v-if="prediction" class="prediction-result">
        <h2>Your call ! :</h2>
        <p class="action">Action : {{ prediction }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      totalJoueur: null,
    carteCroupier: null,
    prediction: null,
    totalJoueurError: '',  // Erreur pour Total_Joueur
    carteCroupierError: ''  // Erreur pour Carte_Croupier
    };
  },

  methods: {
  validateInput() {
    // Validation pour le total du joueur
    if (this.totalJoueur < 4 || this.totalJoueur > 21) {
      this.totalJoueurError = 'The number must be between 4 and 21';
      return false;
    }
    
    // Validation pour la carte du croupier
    if (this.carteCroupier < 2 || this.carteCroupier > 11) {
      this.carteCroupierError = 'The number must be between 2 and 11';
      return false;
    }
    
    // Si les entrées sont valides
    return true;
  },

  async makePrediction() {
    // Réinitialiser les erreurs
    this.totalJoueurError = '';
    this.carteCroupierError = '';

    // Vérifier les entrées avant d'envoyer la requête
    if (!this.validateInput()) {
      return; // Ne pas envoyer la requête si les données sont invalides
    }

    try {
      const response = await axios.post('/predict', {
        Total_Joueur: this.totalJoueur,
        Carte_Croupier: this.carteCroupier,
      });

      this.prediction = response.data.Action; // Afficher la prédiction
    } catch (error) {
      console.error('Erreur lors de la requête:', error);
    }
  },
},
};
</script>

<style scoped>

/* Définir une palette de couleurs et un fond de casino */
.casino-background {
  background-color: #2e3b4e; /* Couleur sombre de fond */
  background-image: url('@/assets/images/background.jpg'); /* Utilise @ pour faire référence au dossier src */
  background-size: cover;
  text-align: center;
  color: white;
  padding: 50px 20px;
  min-height: 100vh;
  font-family: 'Arial', sans-serif;
}

.title {
  font-size: 3rem;
  font-weight: bold;
  text-transform: uppercase;
  color: #f1c40f; /* Or pour un aspect casino élégant */
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5);
  margin-bottom: 30px;
}

.prediction-form {
  background-color: rgba(0, 0, 0, 0.6); /* Fond semi-transparent */
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.7);
  display: inline-block;
}

.form-group {
  margin: 20px 0;
}

label {
  font-size: 1.2rem;
  font-weight: bold;
}

.input-field {
  padding: 10px;
  font-size: 1rem;
  width: 100%;
  border: 2px solid #e74c3c; /* Rouge, pour rappeler les couleurs de casino */
  border-radius: 5px;
  background-color: #34495e;
  color: white;
  margin-top: 5px;
}

.input-field:focus {
  border-color: #f1c40f;
  outline: none;
}

.submit-btn {
  background-color: #f1c40f; /* Or */
  color: #2e3b4e;
  font-size: 1.2rem;
  padding: 12px 30px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.5);
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.submit-btn:hover {
  background-color: #e67e22; /* Rouge-orange pour hover */
  transform: scale(1.05);
}

.submit-btn:active {
  background-color: #d35400;
}

.prediction-result {
  margin-top: 30px;
  font-size: 1.5rem;
}

.action {
  font-weight: bold;
  color: #e74c3c;
}
</style>