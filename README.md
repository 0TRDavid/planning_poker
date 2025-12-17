# Rapport de Projet : Planning Poker

**Auteurs :** Nicolas MENY & David TRUONG
**Dépôt GitHub :** https://github.com/0TRDavid/planning_poker

---

## 1 - Présentation

Le projet **Planning Poker** est une application web collaborative destinée aux équipes agiles pour estimer la complexité des tâches (User Stories).

L'application permet de :

* Créer une session
* Définir des tâches.
* Rejoindre la session via un code unique.
* Voter en temps réel pour chaque tâche selon différents modes (Suite de Fibonacci, T-shirt sizing, etc.).
* Calculer automatiquement le résultat final (Moyenne, Médiane, Majorité) une fois les votes révélés.

L'objectif est de fournir une solution robuste, testée et documentée, reposant sur une architecture moderne séparant clairement l'interface utilisateur de la logique métier.

---

## 2 - Pré-requis

Python :

Node.js :

Docker desktop :

## 3 - Lancement

### Lancement du backend

```bash
cd backend
python -m venv env
env/Scripts/activate
pip install requirements.txt
python manage.py migrate
python manage.py runserver
```

### Lancement du frontend

```bash
cd frontend
npm install
npm run dev
```

### Docker

```bash
docker compose build
docker compose up -d
```
