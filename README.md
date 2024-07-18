# Application Météo avec CustomTkinter

![Screenshot](OIG3.jpg)

Cette application météo utilise les bibliothèques `customtkinter` et `matplotlib` pour fournir des informations météorologiques et afficher un graphique des températures prévues.

## Fonctionnalités

- Affichage des informations météorologiques actuelles pour une ville donnée.
- Affichage des prévisions météorologiques pour les prochains jours.
- Affichage de la population de la ville (si disponible).
- Affichage d'une image de la ville (si disponible).
- Graphique des températures prévues pour les prochains jours.

## Prérequis

- Python 3.x
- `requests` library
- `customtkinter` library
- `Pillow` library
- `matplotlib` library

## Installation

1. Clonez le dépôt GitHub :

    ```sh
    git clone https://github.com/votre-utilisateur/votre-repo.git
    cd votre-repo
    ```

2. Créez un environnement virtuel et activez-le :

    ```sh
    python -m venv venv
    source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
    ```

3. Installez les dépendances nécessaires :

    ```sh
    pip install requests customtkinter Pillow matplotlib
    ```

## Configuration

1. Remplacez les clés API dans le fichier `app.py` par vos propres clés API :
    - `OWM_API_KEY` : Clé API de [OpenWeatherMap](https://openweathermap.org/api).
    - `GEODB_API_KEY` : Clé API de [GeoDB Cities](https://rapidapi.com/wirefreethought/api/geodb-cities).

    ```python
    OWM_API_KEY = "votre_cle_api_openweathermap"
    GEODB_API_KEY = "votre_cle_api_geodb"
    ```

## Utilisation

1. Exécutez l'application :

    ```sh
    python RainRadar.py
    ```

2. Entrez le nom de la ville dans le champ de saisie et cliquez sur "Obtenir les informations" pour afficher les informations météorologiques et les prévisions.

## Exemple de sortie

- Informations météo actuelles (température, description, humidité, vitesse du vent).
- Population de la ville (si disponible).
- Image de la ville (si disponible).
- Graphique des températures prévues pour les prochains jours.

![Screenshot](OIG3.jpg)

## Contribution

Les contributions sont les bienvenues. Veuillez créer une issue pour discuter de ce que vous souhaitez changer avant de soumettre une pull request.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

