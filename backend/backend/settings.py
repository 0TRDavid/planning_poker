"""!
@brief Configuration principale du projet Django 'Planning Poker'.

Ce fichier contient toutes les configurations globales : base de données, 
applications installées, middleware, sécurité, etc.

@note Ce projet utilise la bibliothèque `python-dotenv` pour charger les 
variables sensibles depuis un fichier `.env`.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# SÉCURITÉ ET ENVIRONNEMENT
# ==============================================================================

## @brief Clé secrète de Django. Doit rester confidentielle en production.
SECRET_KEY = os.environ.get('SECRET_KEY')

## @brief Mode debug. Si True, affiche les erreurs détaillées. (Jamais True en prod !)
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

## @brief Liste des domaines/IP autorisés à accéder au site.
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

## @brief Liste des origines autorisées pour les requêtes CORS (Cross-Origin).
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')

# ==============================================================================
# APPLICATIONS
# ==============================================================================

## @brief Applications activées dans ce projet.
INSTALLED_APPS = [
    # Applications Django de base
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Applications tierces
    'rest_framework', #< Pour l'API REST
    'corsheaders',    #< Pour gérer les requêtes du Front React

    # Applications locales
    'planning_poker', #< Notre application principale
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# ==============================================================================
# BASE DE DONNÉES
# ==============================================================================

## @brief Configuration de la base de données.
## Par défaut utilise SQLite, configurable via variables d'environnement.
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': BASE_DIR / os.environ.get('DB_NAME', 'db.sqlite3'),
    }
}


# ==============================================================================
# VALIDATION DES MOTS DE PASSE
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ==============================================================================
# INTERNATIONALISATION
# ==============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==============================================================================
# FICHIERS STATIQUES
# ==============================================================================

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'