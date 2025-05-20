# Projet Got : Classification des maisons dans l'univers de Game of Thrones

## Introduction
Ce projet utilise des **Graph Neural Networks (GNN)** pour prédire la maison d'un personnage dans l'univers de **Game of Thrones**, en se basant sur des relations entre les personnages (graphes) et des caractéristiques associés à chaque nœud. L'IA permet de déduire la maison des personnages "Unknown" en fonction de ceux déjà étiquetés et de leurs interactions dans le réseau.

Les personnages sont représentés par des nœuds dans un graphe, et leurs relations avec les autres personnages sont des arêtes. Le modèle GNN va apprendre à partir des personnages ayant déjà une maison assignée et prédire les maisons pour les personnages "Unknown".

## Prérequis

Avant de lancer ce projet, vous devez préparer votre environnement avec les éléments suivants :

1. **Création d'un environnement virtuel** (venv) :
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. **Installation des dépendances** :
    Vous devez installer les bibliothèques requises dans votre environnement virtuel. Exécutez la commande suivante dans le dossier du projet :
    ```bash
    pip install -r requirements.txt
    ```

   Voici les principales dépendances nécessaires :

   - **PyTorch** et **PyTorch Geometric** pour le traitement des graphes et l'apprentissage automatique.
   - **Streamlit** pour l'interface utilisateur.
   - **Pandas** pour la gestion des données en CSV.
   - **NetworkX** pour la manipulation des graphes.

## Lancement du projet

### Commandes à exécuter

1. **Entraîner le modèle** GCN:
    ```bash
    python3 -m model.train
    ```

2. **Lancer l'application Streamlit** pour visualiser les résultats :
    ```bash
    streamlit run app/main.py
    ```

## Annexe

### Script de nettoyage : `clean.sh`

Le script `clean.sh` permet de nettoyer les anciens fichiers générés par les prédictions ou d'autres traitements de données, afin de repartir avec un environnement propre. Exécutez-le avant de commencer un nouveau cycle de traitement.

### Utilisation :

```bash
./clean.sh
```

Cela supprimera tous les fichiers inutiles et les poids du modèle, vous permettant de recommencer avec des données fraîches.

### Fichier init_house

Le fichier init_house est utilisée pour initialiser les maisons des personnages dans le graphe.

---

## Conclusion

Ce projet permet de prédire la maison des personnages "Unknown" dans l'univers de **Game of Thrones** en utilisant un **Graph Neural Network (GNN)**. L'IA apprend à partir des relations entre les personnages pour faire ces prédictions et affiche les résultats sous forme de graphes interactifs avec **Streamlit**.
