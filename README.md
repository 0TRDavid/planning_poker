# Rapport de Projet : Planning Poker

![CI Status](https://github.com/0TRDavid/planning_poker/actions/workflows/ci_pipeline.yml/badge.svg) ![Python](https://img.shields.io/badge/Python-3.12-blue) ![React](https://img.shields.io/badge/React-18-blue) ![Docker](https://img.shields.io/badge/Docker-Available-blue)

**Auteurs :** Nicolas MENY & David TRUONG

**Dépôt GitHub :** [https://github.com/0TRDavid/planning_poker](https://github.com/0TRDavid/planning_poker)

**Doc technique :** [https://0trdavid.github.io/planning_poker/](https://0trdavid.github.io/planning_poker/)

**Application collaborative d'estimation de tâches pour les équipes Scrum.**

## Présentation

Le projet **Planning Poker** est une application web collaborative destinée aux équipes agiles pour estimer la complexité des tâches (User Stories).

L'application permet de :

* **Créer** une session
* **Définir** des tâches.
* **Rejoindre** la session via un code unique.
* **Voter** en temps réel pour chaque tâche selon différents modes (Suite de Fibonacci, T-shirt sizing, etc.).
* **Calculer** automatiquement le résultat final (Moyenne, Médiane, Majorité) une fois les votes révélés.

L'objectif est de **fournir une solution robuste, testée et documentée**, reposant sur une architecture moderne séparant clairement l'interface utilisateur de la logique métier.

## Stack Technique

### Backend (API)

* **Langage :** Python 3.12
* **Framework :** Django 5 + Django REST Framework (DRF)
* **Base de données :** SQLite (Dev) / Extensible vers PostgreSQL
* **Tests :** Pytest, FactoryBoy
* **Doc :** Doxygen

### Frontend (Client)

* **Langage :** JavaScript (ES6+)
* **Framework :** React 19 (via Vite)
* **UI :** Material UI (MUI)
* **HTTP :** Axios / Fetch API

### DevOps

* **Conteneurisation :** Docker & Docker Compose
* **CI/CD :** GitHub Actions (Tests auto + Déploiement Doc)

## Pré-requis

Avant de commencer, assurez-vous d'avoir installé :

* **Python :** Version 3.12 ou supérieure.
* **Node.js :** Version 22 ou supérieure.
* **Docker Desktop :** Installé et lancé (pour le déploiement conteneurisé).

## Méthode 1 : Développement local

### Lancement du backend

```bash
cd backend

# Création de l'environnement virtuel
python -m venv env

# Activation du venv (Windows)
env/Scripts/activate

# Activation du venv (Linux)
# source env/bin/activate

# Installation des dépendences
pip install -r requirements.txt

# Migration BDD + lancement du serveur
python manage.py migrate
python manage.py runserver
```

Le backend sera accessible sur : http://localhost:8000

### Lancement du frontend

```bash
cd frontend

# Installation des dépendances
npm install

# Lancement du serveur
npm run dev
```

Le frontend sera accessible sur : http://localhost:5173

## Méthode 2 : Docker (recommandé)

Utilisez cette méthode pour lancer l'application en une seule commande.

```bash
docker compose build
docker compose up -d
```

L'application est alors accessible sur http://localhost:5173
