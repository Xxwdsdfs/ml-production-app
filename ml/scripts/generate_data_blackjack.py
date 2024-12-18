import random
import csv
import os

# Fonction pour obtenir la valeur d'une carte
def valeur_carte(carte):
    if carte in ['J', 'Q', 'K']:
        return 10
    elif carte == 'A':
        return 11  # Par défaut, on compte l'As comme 11 pour commencer
    return int(carte)

# Fonction pour calculer le total d'une main
def total_main(main):
    total = sum(valeur_carte(carte) for carte in main)
    as_count = main.count('A')
    while total > 21 and as_count > 0:  # Ajuste les As à 1 si nécessaire
        total -= 10
        as_count -= 1
    return total

# Fonction pour déterminer si l'on doit tirer ou rester (stratégie de base simplifiée)
def determiner_action(total_joueur, carte_croupier):
    if total_joueur <= 11:
        return "tirer"
    elif 12 <= total_joueur <= 16:
        if carte_croupier in [2, 3, 4, 5, 6]:
            return "rester" if random.random() > 0.1 else "tirer"  # 10% de bruit
        else:
            return "tirer"
    else:
        return "rester" if random.random() > 0.05 else "tirer"  # 5% de bruit

# Fonction pour simuler une main et une carte visible du croupier
def simuler_main():
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] * 4
    random.shuffle(deck)
    main_joueur = [deck.pop(), deck.pop()]
    carte_croupier = deck.pop()
    return main_joueur, carte_croupier

# Fonction principale pour générer les données et sauvegarder dans un fichier CSV
def generer_donnees_blackjack(nombre_mains, fichier_sortie):
    with open(fichier_sortie, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Total_Joueur", "Carte_Croupier", "Action"])  # En-tête du fichier

        for i in range(nombre_mains):
            main_joueur, carte_croupier = simuler_main()
            total_joueur = total_main(main_joueur)
            valeur_croupier = valeur_carte(carte_croupier)

            action = determiner_action(total_joueur, valeur_croupier)

            # DEBUG : Afficher chaque main simulée
            print(f"Main {i+1}: Main du joueur={main_joueur}, Carte croupier={carte_croupier}, "
                  f"Total joueur={total_joueur}, Action={action}")
            
            writer.writerow([total_joueur, valeur_croupier, action])

    print(f"{nombre_mains} mains simulées et sauvegardées dans {fichier_sortie}")

# TEST DES FONCTIONS INDIVIDUELLES
if __name__ == "__main__":
    # Test de simuler_main
    print("\nTest de simuler_main:")
    main_joueur, carte_croupier = simuler_main()
    print(f"Main du joueur : {main_joueur}, Carte du croupier : {carte_croupier}")

    # Générer les données et sauvegarder dans un fichier CSV
    print("\n### Génération des données Blackjack ###")
    nombre_mains = 10000  # Nombre de mains à simuler
    fichier_sortie = os.path.abspath("C:\\Users\\user\\Documents\\Axel\\EFREI\\Cours Visio\\M2\\ML FOR PROD\\Final Project\\ml-production-app\\data\\blackjack_data.csv")  
    print(f"Enregistrement dans : {fichier_sortie}")
    generer_donnees_blackjack(nombre_mains, fichier_sortie)