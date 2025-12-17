"""!
@brief Définition des URL racines du projet.

Ce fichier orchestre le routage des requêtes HTTP vers les applications correspondantes.
Il utilise un routeur REST Framework pour l'API.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from planning_poker import views

## @brief Routeur principal pour l'API REST.
## Gère automatiquement les URLs pour les ViewSets enregistrés.
router = DefaultRouter()

# Enregistrement des routes de l'application Planning Poker
router.register(r'sessions', views.SessionViewSet, basename='session')
router.register(r'parties', views.PartieViewSet, basename='partie')

## @brief Liste des points d'entrée URL du projet.
urlpatterns = [
    path("admin/", admin.site.urls), #< Interface d'administration Django
    path('api/', include(router.urls)), #< Préfixe '/api/' pour toutes les routes de l'application
]