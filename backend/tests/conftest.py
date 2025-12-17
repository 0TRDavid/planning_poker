# tests/conftest.py
import os
import django
import pytest
from django.conf import settings

# Ce fichier configure l'environnement de test Django et définit des fixtures globales. 
# Les fixtures sont utilisées pour fournir des clients de test réutilisables dans plusieurs fichiers de test.

# Configure Django AVANT les imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.test import Client
from rest_framework.test import APIClient


# ==================== FIXTURES GLOBALES ====================

@pytest.fixture
def api_client():
    """Client API REST pour les tests"""
    return APIClient()


@pytest.fixture
def client():
    """Client Django standard"""
    return Client()
