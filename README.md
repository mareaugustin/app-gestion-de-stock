# App Gestion de Stock

Ce projet est une application de gestion de stock développée avec Django. Elle permet de gérer les produits, les catégories, les fournisseurs, et les mouvements de stock.

## Fonctionnalités

- **Gestion des ventes** :
  - Création, modification et suppression des ventes.
  - Calcul automatique des sous-totaux, taxes et montants totaux.
  - Génération de reçus détaillés pour chaque vente.
  - Exportation des ventes au format CSV.

- **Gestion des achats** :
  - Création, modification et suppression des achats.
  - Suivi des fournisseurs et des articles achetés.
  - Exportation des achats au format CSV.

- **Gestion des articles** :
  - Ajout, modification et suppression des articles.
  - Recherche et filtrage des articles.

- **Gestion des clients et fournisseurs** :
  - Ajout, modification et suppression des clients et fournisseurs.
  - Recherche et filtrage des clients et fournisseurs.

- **Interface utilisateur** :
  - Interface responsive et intuitive.
  - Utilisation de bibliothèques comme DataTables, Select2, Bootstrap et SweetAlert pour une meilleure expérience utilisateur.

## Prérequis

- Python 3.x
- Django 4.x
- SQLite (par défaut) ou tout autre SGBD compatible avec Django.

## Technologies utilisées

- **Backend** :
  - Django (Python)
  - Django ORM pour la gestion de la base de données
  - OpenPyXL pour l'exportation des données au format Excel

- **Frontend** :
  - HTML, CSS, JavaScript
  - Bootstrap pour le design
  - DataTables pour les tableaux interactifs
  - Select2 pour les champs de recherche
  - SweetAlert pour les alertes et confirmations

- **Base de données** :
  - SQLite (par défaut, peut être remplacée par PostgreSQL, MySQL, etc.)


## Installation

1. Clonez ce dépôt :
    ```bash
    git clone https://github.com/mareaugustin/app-gestion-de-stock.git
    cd app-gestion-de-stock
    ```

2. Créez un environnement virtuel et activez-le :
    ```bash
    python -m venv env
    source env/bin/activate  # Sur Windows : env\Scripts\activate
    ```

3. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

4. Appliquez les migrations :
    ```bash
    python manage.py migrate
    ```

5. Lancez le serveur de développement :
    ```bash
    python manage.py runserver
    ```

6. Accédez à l'application via [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Utilisation

- Connectez-vous à l'interface d'administration pour gérer les données : [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin).
- Ajoutez des produits, des catégories et des fournisseurs.
- Suivez les mouvements de stock via l'interface utilisateur.

## Contribution

Les contributions sont les bienvenues ! Veuillez soumettre une pull request ou ouvrir une issue pour discuter des améliorations.

## Licence

Ce projet est sous licence libre.

## Auteur

- **Augustin Maré MILLOGO** - [Votre Profil GitHub](https://github.com/mareaugustin)