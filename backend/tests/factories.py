"""!
@brief Définition des usines (factories) pour la génération de données de test.

Ce fichier utilise la bibliothèque `factory_boy` pour créer facilement des instances
de modèles (`Session`, `Partie`) avec des données réalistes mais aléatoires.
Cela évite de devoir remplir manuellement chaque champ dans les tests unitaires.
"""

import factory
from planning_poker.models import Session, Partie

class SessionFactory(factory.django.DjangoModelFactory):
    """!
    @brief Usine pour générer des objets `Session` de test.
    
    Par défaut, crée une session avec un titre aléatoire, un jeu de stories
    par défaut et un mode de jeu choisi au hasard.
    """
    class Meta:
        model = Session
    
    ## @brief Titre généré aléatoirement (un mot).
    titre = factory.Faker('word')

    ## @brief Données JSON par défaut pour les stories (2 stories d'exemple).
    stories = factory.LazyFunction(lambda: {"story1": "Implémenter login", "story2": "Créer dashboard"})

    ## @brief Mode de jeu choisi aléatoirement parmi les options valides.
    mode_de_jeu = factory.Faker('random_element', elements=['strict', 'average', 'majority_abs', 'majority_rel', 'median'])

    ## @brief Statut par défaut à la création ('open').
    status = 'open'


class PartieFactory(factory.django.DjangoModelFactory):
    """!
    @brief Usine pour générer des objets `Partie` (Joueurs) de test.
    
    Crée un joueur virtuel rattaché à une session (créée automatiquement si non fournie).
    """
    class Meta:
        model = Partie
        # Pour éviter les erreurs si on tente de créer deux fois le même utilisateur dans la même session
        django_get_or_create = ('username', 'id_session')

    ## @brief Nom d'utilisateur aléatoire.
    username = factory.Faker('user_name')

    ## @brief Carte choisie aléatoirement (Fibonacci ou None).
    carte_choisie = factory.Faker('random_element', elements=['1', '2', '3', '5', '8', '13', '20', None])

    ## @brief État du vote (False par défaut).
    a_vote = False

    ## @brief Session associée. Si non fournie, une nouvelle SessionFactory est appelée.
    id_session = factory.SubFactory(SessionFactory)