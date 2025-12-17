"""!
@brief Configuration globale des tests pytest pour le projet.

Ce fichier est automatiquement détecté par pytest. Il est responsable de :
- Configurer l'environnement Django avant le lancement des tests.
- Définir des "fixtures" globales (objets réutilisables) accessibles par tous les fichiers de test.
"""

import os
import django
import pytest
from django.conf import settings

# Configure Django AVANT les imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.test import Client
from rest_framework.test import APIClient


# ==================== FIXTURES GLOBALES ====================

@pytest.fixture
def api_client():
    """!
    @brief Fournit un client API REST Framework pour les tests.
    
    Cette fixture permet de simuler des requêtes HTTP (GET, POST, etc.) vers l'API
    sans avoir besoin de lancer un serveur réel. Elle gère nativement le format JSON.
    
    @return Une instance de `rest_framework.test.APIClient`.
    """
    return APIClient()


@pytest.fixture
def client():
    """!
    @brief Fournit un client Django standard pour les tests.
    
    Utilisé pour tester les vues Django classiques (non-API) ou pour des besoins
    spécifiques ne nécessitant pas les fonctionnalités de DRF.
    
    @return Une instance de `django.test.Client`.
    """
    return Client()