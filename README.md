# Open Thread CategorIA

_Tableau de bord d'annotation des discussions autour des jeux de données du Ministère de l'économie et des
finances ([data.gouv.fr](https://www.data.gouv.fr/fr/) et [data.economie.gouv.fr](https://data.economie.gouv.fr/pages/accueil/))_

## Description du projet

Ce projet s'inscrit dans le cadre de la mission OpenData du ministère. Il s'agit d'un tableau de bord qui permet aux agents du ministère de comprendre les problèmes que rencontrent les utilisateurs des plateformes [data.gouv.fr](https://www.data.gouv.fr/fr/) et [data.economie.gouv.fr](https://data.economie.gouv.fr/pages/accueil/) avec leurs jeux de données. Chaque discussion est automatiquement annotée dans une des 6 catégories principales et l'une des 26 sous-catégories possibles.

L'annotation est réalisée grâce à des modèles de traitement automatique du langage naturel (TALN), en particulier les modèles CamemBERT, adaptés à la langue française. Le tableau de bord est développé avec D3.js et Plotly.js.

## Fonctionnalités Principales

- **Annotation automatisée** : Le modèle d'IA analyse le texte (titre et message) des discussions et renvoie une classification dans une catégorie et sous-catégorie.
- **Modèle de catégorisation imbriqué** : Deux modèles CamemBERT sont utilisés : le premier prédit la catégorie principale, tandis que le second prédit la sous-catégorie en utilisant les prédictions du premier modèle ainsi que les informations textuelles (titre et message).
- **Entraînement supervisé** : Les modèles sont entraînés avec des données annotées manuellement, issues de travaux réalisés par Datactivist pour le compte d'Etalab en 2019.

## Architecture du projet

<!-- Le projet suit une architecture claire avec plusieurs couches. Chaque application est organisée selon cette structure :
- `exceptions` : Gère les exceptions spécifiques aux cas d'utilisation.
- `gateways` : Définit les contrats (interfaces) avec les dépendances via des classes abstraites (Abstract Base Class en Python).
- `infrastructure` : Gère les implémentations des contrats et l'accès aux données.
- `models` : Définit les objets de données utilisés dans les différentes couches de l'application.
- `usecases` : Implémente la logique métier et orchestre les interactions entre les différentes couches. -->

Le projet est organisé selon une architecture modulaire (Clean archi et architecture hexagonale) et est organisé en plusieurs dossiers clés :

- `app/` : Contient les fichiers statiques et les templates de l'application (CSS, JS, HTML).
- `core/` : Fichiers de configuration (comme les clés API, URLs, etc.).
- `domain/` : Gère les modèles de données et les cas d'utilisation.
- `inference/` : Scripts pour l'inférence avec les modèles CamemBERT.
- `infrastructure/` : Implémentation des repositories et services externes.
- `scripts/` : Scripts divers pour l'application, tels que update_data.py.
- `tests/` : Contient les tests unitaires et les fixtures pour tester les fonctionnalités.

## Installation

### 1. Cloner le dépôt

Clonez le dépôt sur votre machine :

```bash
git clone https://github.com/139bercy/open-data-discussions.git
cd open-data-discussions
```

### 2. Configuration des variables d'environnement

Copiez le fichier .env.sample et modifiez-le selon vos besoins (renseigner votre clé API data.economie.gouv.fr):

```bash
cp .env.sample .env
```

### 3. Créer un environnement virtuel

Avant d'installer les dépendances, créez un environnement virtuel pour isoler vos paquets Python. Vous avez deux options : utiliser venv ou virtualenv.

**Option 1 :** Utiliser `venv` (recommandé pour Python 3.3+)

```bash
python3 -m venv venv
```

Activez l'environnement virtuel :

- Sur **Linux/MacOS** :

```bash
source venv/bin/activate
```

- Sur **Windows** :

```bash
.\venv\Scripts\activate
```

**Option 2 :** Utiliser `virtualenv` (compatible avec Python 2 et 3)

1. Installez pip si ce n'est pas déjà fait :

```bash
sudo apt-get install python3-pip
```

2. Installez `virtualenv` :

```bash
pip install virtualenv
```

3. Créez un environnement virtuel :

```bash
virtualenv venv
```

4. Activez l'environnement virtuel :

- Sur **Linux/MacOS** :

```bash
source venv/bin/activate
```

- Sur **Windows** :

```bash
.\venv\Scripts\activate
```

### 4. Installer les dépendances

Installez les dépendances nécessaires en fonction de l'environnement souhaité :

- Environnement de `Développement`:

```bash
pip install -r requirements.dev.txt
```

- Environnement de `Production` :

```bash
pip install -r requirements.prod.txt
```

- Environnement `Data Science` :

```bash
pip install -r requirements.ds.txt
```

### 5. Télécharger les modèles d'IA pré-entraînés

Créez un dossier `trained_models` à la racine du projet et téléchargez les poids des modèles pré-entraînés **CamemBERT** :

```bash
mkdir trained_models
```

```bash
cd trained_models
```

- Zip Modèle 1 (Catégories) :

```bash
wget https://huggingface.co/BercyHub/CamemBERT_classification_discussions/resolve/main/bert-finetuned-my-data-final_archive.zip
```

- Zip Modèle 2 (Sous-Catégories) :

```bash
wget https://huggingface.co/BercyHub/CamemBERT_classification_discussions/resolve/main/bert-finetuned-my-data-final2_archive2.zip
```

## Récupérer ou Mettre à jour les données

Pour récupérer ou mettre à jour les données à partir des sources API, depuis la racine du projet, exécutez :

```bash
make update_data
```

### Ce que Fait `update_data.py`

Le script `update_data.py` récupère les dernières données depuis les APIs ([data.gouv.fr](https://www.data.gouv.fr/fr/) et [data.economie.gouv.fr](https://data.economie.gouv.fr/pages/accueil/)), les formate et les stocke dans la base de données locale.

## Utilisation

### Lancer l'Application

Pour lancer l'application front-end (tableau de bord), depuis la racine du projet, exécutez :

```bash
python app.py
```

## Exécuter les Tests

### Tests des Fetchers

Exécutez les tests des fetchers avec la commande :

```bash
make test_fetchers
```

### Test des Usecases

Exécutez les tests des différents cas d'usages :

```bash
make test_usecases
```

### Lancer tous les tests

Pour lancer tous les tests :

```bash
make test_all
```

### Structure des tests

Les tests génèrent des fichiers JSON dans le répertoire tests/fixtures/. Ces fichiers contiennent :

- Données brutes dans `unformatted_data/`
- Données formatées dans `formatted_data/`
- Échantillons de tests dans `samples_data/`

## Structure du Projet

```
├── app/                    # Contient les fichiers statiques et les templates
│   ├── static/             # Fichiers statiques (images, CSS, JS) pour l'application front-end
│   └── templates/          # Fichiers HTML pour le front-end
|
├── core/                   # Configuration (API, URLs, etc.)
│   └── config.py           # Configuration de l'application (API Keys, URLs, etc.)
|
├── domain/                 # Logique métier, modèles de données
│   ├── gateways.py         # Contient les classes abstraites pour les repositories
│   ├── models.py           # Contient les modèles de données utilisés dans l'application
│   └── usecases.py         # Contient la logique métier
|
├── inference/              # Inférence des modèles CamemBERT
│   ├── categories.py       # Catégorisation des discussions
│   ├── classe_inference.py # Classes pour l'inférence
│   ├── inference_script.py # Script d'inférence avec le modèle CamemBERT
│   └── preprocess.py       # Pré-traitement des données avant inférence
|
├── infrastructure/         # Implémentation des repositories et services
│   ├── repositories/       # Implémentation des repositories (accès aux données)
│   └── services/           # Services et intégrations externes
|
├── scripts/                # Scripts divers, ex : update_data.py
│   ├── json_to_csv         # Script de conversion JSON vers CSV
│   └── update_data.py      # Script pour récupérer et mettre à jour les données dans la base
|
├── src/                    # Application principale (ex : app.py)
│   └── format/             # Scripts de formatage des données
|
├── tests/                  # Tests unitaires et fixtures
│   ├── test_fetchers.py    # Tests pour les fetchers (récupération des données)
│   └── test_usecases.py    # Tests pour les cas d'usage
|
├── trained_models/         # Contient les poids des modèles CamemBERT pré-entraînés pour l'inférence
│   ├── trained_models/bert-finetuned-my-data-final_archive.zip           # Poids du modèle 1 (Catégories)
    ├── trained_models/bert-finetuned-my-data-final_archive2.zip           # Poids du modèle 2 (Sous-catégories)
|
├── .env.sample             # Fichier d'exemple pour les variables d'environnement (à copier sous le nom .env et redéfinir l'API key)
├── .gitignore              # Fichiers/dossiers ignorés par Git
├── .pre-commit-config.yaml # Configuration pre-commit hooks
├── Makefile                # Commandes make (update_data, tests, etc.)
├── README.md               # Documentation du projet
├── app.py                  # Point d'entrée de l'application
├── fetch_samples_data.py   # Script de génération d'échantillons de données
├── pyproject.toml          # Configuration pour gestion des dépendances
├── requirements.dev.txt    # Dépendances pour le développement
├── requirements.ds.txt     # Dépendances pour data science
├── requirements.prod.txt   # Dépendances pour la production
├── requirements.readme.txt # Dépendances supplémentaires pour le README
├── setup.py                # Installation du package Python
├── tox.ini                 # Configuration pour tox (environnement de test)
```

## License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus d'informations.
