# Open Thread CategorIA

_Tableau de bord d'annotation des discussions autour des jeux de données du Ministère de l'économie et des
finances (data.gouv.fr)_

## Description du projet

Ce projet s'inscrit dans le cadre de la mission OpenData du ministère.
Il s'agit d'un tableau de bord qui permettra aux agents du ministère de comprendre quels sont les problèmes que
rencontrent les utilisateurs de la plateforme data.gouv.fr avec leurs jeux de données.
Chaque discussion autour des jeux de données sera annotée en une catégorie parmi 6 et une sous catégorie parmi 26
possibles.

L'annotation est automatisée grâce à un modèle d'IA de catégorisation basé sur CamemBERT, un modèle largement utilisé
dans le domaine du Traitement Automatique du Langage Naturel (NLP).
Le dashboard quant à lui est développé avec Dash plotly.

## Fonctionnalités Principales

- Annotation Automatisée : Le modèle d'IA prend en entrée un texte, composé du titre et de la discussion, et retourne sa
  classification en catégorie et sous-catégorie.
- Modèle de Catégorisation Imbriqué : Deux modèles CamemBERT sont utilisés. Le premier prédit la catégorie, et le
  deuxième prédit la sous-catégorie en prenant en entrée la prédiction du premier modèle (catégorie prédite), concaténée
  avec la discussion et le titre de la discussion pour en prédire la sous catégorie.
- Entraînement Supervisé : Le modèle est entraîné de manière supervisée en s'appuyant sur un échantillon de données
  préalablement catégorisées manuellement. Nous avons capitalisé pour cela sur les travaux qui ont été réalisés en 2019
  par Datactivist pour le compte d'Etalab.

## Architecture du Projet

### Entrypoints

- API pilotée par Flask
- Système de gestion en lignes de commande (CLI)

### Applications :

Les applications suivent la même arborescence :

- `exceptions` : les exceptions métier levées par les différents cas d'usage.
- `gateways` : les contrats (sous forme d'Abstract Base Class en Python) passés avec les dépendances.
- `infrastructure` : les repositories, qui héritent des contrats définis dans `gateways`
- `models` : les objets de base (écrits en Python) qui circulent entre les couches.
- `usecases` : fonctions utilisées par les `entrypoints` qui permettent de traiter les cas d'usage

## Installation

1. Modifiez le contenu des variables d'environnement selon vos usages :

   ```bash
   cp .env.sample .env
   ```

2. Installez les dépendances :

   ```bash
   make install
   ```

## Instructions d'Utilisation

- **Installation des Dépendances** : Exécutez `pip install -r requirements.txt` pour installer les bibliothèques nécessaires.
- **Exécution des Scripts** : Utilisez les scripts et notebooks dans le dossier `src/` pour exécuter différentes parties du projet.
- **Configuration** : Modifiez le fichier `config.json` pour ajuster les variables d'environnement si nécessaire.

**Remarques** :

- Assurez-vous d'avoir les autorisations nécessaires pour accéder aux données et effectuer des requêtes API.
- Les modèles entraînés sont stockés dans le dossier `trained_models/`.
- Les résultats des requêtes API sont disponibles dans le dossier `data/raw/data_acquisition/`.

## Usage

### Lancer le Tableau de Bord

Pour lancer le front-end (tableau de bord) depuis un environnement virtuel, exécutez :

```bash
python app.py
```

### Lignes de Commande

Pour interagir via la ligne de commande, utilisez :

```bash
python commands.py
```

### Développement

**Pré-requis** : Avoir installé Docker et `docker-compose`. Les commandes associées sont dans le fichier `Makefile`.

1. Créez un dossier `data` dans `app/static/`.
2. Créez un fichier `.env` avec `KEY=api_key`.
3. Créez un environnement virtuel avec `virtualenv -p python3.11 venv`.
4. Installez `pip` avec :

   ```bash
   curl -sS https://bootstrap.pypa.io/get-pip.py | python3
   ```

5. Récupérez les fichiers zip contenant les poids des modèles depuis le dépôt Hugging Face :

   [BercyHub/CamemBERT_classification_discussions](https://huggingface.co/BercyHub/CamemBERT_classification_discussions/tree/main)

6. Exécutez les tests pour vérifier le bon fonctionnement des fetchers avec :

   ```bash
   pytest -k test_fetch_discussions_from_data_gouv_api
   ```

## Lancer les Tests

### Tests des Use Cases

Les tests pour les use cases se trouvent dans `tests/test_usecases.py`. Pour les exécuter, utilisez :

```bash
pytest tests/test_usecases.py
```

### Tests des Fetchers

Les tests pour les fetchers se trouvent dans `tests/test_fetchers.py`. Pour les exécuter, utilisez :

```bash
pytest tests/test_fetchers.py
```

### Ce que Produisent les Tests

Les tests génèrent des fichiers JSON dans les répertoires suivants :

- `tests/fixtures/unformatted_data/` : Contient les données brutes récupérées depuis les APIs.
- `tests/fixtures/formatted_data/` : Contient les données formatées prêtes à être utilisées par l'application.

## Script de Mise à Jour des Données

### Ce que Fait `update_data.py`

Le script `update_data.py` récupère les dernières données depuis les APIs, les formate et les stocke dans la base de données locale.

### Lancer `update_data.py`

Pour exécuter le script :

```bash
python update_data.py
```

## Structure du Projet

```
├── .gitignore             # Fichier pour spécifier les fichiers/dossiers à ignorer par Git
├── README.md              # Documentation du projet
├── requirements.txt       # Liste des dépendances Python requises pour le projet
├── core/
│   └── config.py          # Configuration de l'application (API Keys, URLs, etc.)
├── domain/
│   ├── gateways.py        # Contient les classes abstraites pour les repositories
│   ├── models.py          # Contient les modèles de données utilisés dans l'application
│   └── usecases/          # Contient les cas d'utilisation (logique métier) de l'application (orchestre l'interaction entre les différentes couches du système)
├── api/
│   └── fetch_data.py      # Script pour récupérer et formater les données à partir des APIs
├── scripts/
│   └── update_data.py     # Script pour récupérer et mettre à jour les données dans la base
├── inference/
│   └── model.py           # Contient les scripts pour l'inférence et le traitement avec le modèle CamemBERT
├── infrastructure/
│   ├── repositories/      # Contient les implémentations des repositories (accès aux données)
│   └── services/          # Contient les services (logique métier supplémentaire ou intégrations externes)
├── src/
│   ├── app.py             # Point d'entrée pour le lancement de l'application (Dash Plotly)
│   ├── commands.py        # Script pour les interactions en ligne de commande
│   └── config.json        # Fichier de configuration pour les variables d'environnement
├── tests/
│   ├── test_usecases.py   # Tests pour valider les différents cas d'utilisation
│   ├── test_fetchers.py   # Tests pour valider les fetchers (récupérateurs de données via les APIs data.gouv.fr et data.economie.gouv.fr)
│   └── fixtures/          # Données de test et données de sortie des fetchers
├── app/
│   ├── static/            # Fichiers statiques utilisés par l'application front-end, tels que les images, les fichiers CSS, JavaScript, etc.
│   └── templates/         # Fichiers HTML utilisés pour le rendu du front-end côté serveur, notamment pour les pages du tableau de bord
├── data/
│   └── raw/               # Contient les données brutes récupérées via les APIs
└── trained_models/        # Contient les poids des modèles pré-entraînés pour l'inférence (CamemBERT). Ces modèles sont utilisés pour prédire les catégories et sous-catégories des discussions.

```

## License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus d'informations.