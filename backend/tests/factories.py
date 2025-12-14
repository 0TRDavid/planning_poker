# tests/factories.py
import factory
from planning_poker.models import Session, Partie


# Ce fichier permet de créer des usines (factories) pour générer des instances de modèles pour les tests.

class SessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Session
    
    # id_session sera généré automatiquement par la fonction generate_six_digit_code
    titre = factory.Faker('word')
    stories = factory.LazyFunction(lambda: {"story1": "Implémenter login", "story2": "Créer dashboard"})
          # 'median'
        # 'average'
        # 'majority_abs'
        # 'majority_rel'
    mode_de_jeu = factory.Faker('random_element', elements=['strict', 'average', 'majority_abs', 'majority_rel', 'median'])
    status = 'open'


class PartieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Partie
        django_get_or_create = ('username', 'id_session')  # Pour éviter les violations de contrainte unique

    username = factory.Faker('user_name')
    carte_choisie = factory.Faker('random_element', elements=['1', '2', '3', '5', '8', '13', '20', None])
    a_vote = False
    id_session = factory.SubFactory(SessionFactory)
    

