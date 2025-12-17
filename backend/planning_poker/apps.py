from django.apps import AppConfig


class PlanningPokerConfig(AppConfig):
    """!
    @brief Configuration de l'application Django 'planning_poker'.
    
    Cette classe est le point d'entrée pour la configuration de l'application 
    au sein du projet Django. Elle définit les paramètres par défaut 
    pour tous les modèles de cette app.
    """

    ## @brief Type de champ par défaut pour les clés primaires (BigInt).
    default_auto_field = 'django.db.models.BigAutoField'

    ## @brief Nom technique de l'application (utilisé dans INSTALLED_APPS).
    name = 'planning_poker'