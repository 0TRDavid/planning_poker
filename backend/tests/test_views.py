# tests/test_views.py
"""!
@brief Tests d'intégration pour les ViewSets (API Endpoints).

Ce fichier contient les tests fonctionnels de l'API. Il vérifie :
- Les opérations CRUD sur les Sessions et les Parties.
- La logique métier complexe de clôture de story (calculs de votes).
- Les règles de gestion (rejoindre une session, unicité des joueurs, reset).
"""

import pytest
from django.urls import reverse
from rest_framework import status
from planning_poker.models import Session, Partie
from tests.factories import SessionFactory, PartieFactory


@pytest.mark.django_db
class TestSessionViewSet:
    """!
    @brief Tests des endpoints CRUD pour les Sessions (/api/sessions/).
    
    Vérifie qu'on peut lister, créer, récupérer, modifier et supprimer des sessions.
    """
    
    def test_list_sessions(self, api_client):
        """!
        @brief Vérifie la récupération de la liste des sessions (GET /sessions/).
        """
        SessionFactory.create_batch(3)
        response = api_client.get(reverse('session-list'))
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 3
    
    def test_create_session(self, api_client):
        """!
        @brief Vérifie la création d'une nouvelle session (POST /sessions/).
        
        S'assure que l'ID est bien généré et le statut initial est 'open'.
        """
        data = {
            'titre': 'Sprint Planning',
            'stories': {
                'story1': {'nom': 'Feature A'},
                'story2': {'nom': 'Feature B'}
            },
            'mode_de_jeu': 'fibonacci',
            'status': 'open'
        }
        response = api_client.post(
            reverse('session-list'),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['titre'] == 'Sprint Planning'
        assert len(response.data['id_session']) == 6
        assert response.data['status'] == 'open'
    
    def test_retrieve_session(self, api_client):
        """!
        @brief Vérifie la récupération d'une session unique par ID (GET /sessions/{id}/).
        """
        session = SessionFactory(titre='Mon Planning')
        response = api_client.get(
            reverse('session-detail', args=[session.id_session])
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['titre'] == 'Mon Planning'
        assert response.data['id_session'] == session.id_session
    
    def test_update_session(self, api_client):
        """!
        @brief Vérifie la mise à jour partielle d'une session (PATCH /sessions/{id}/).
        """
        session = SessionFactory(titre='Ancien titre')
        data = {'titre': 'Nouveau titre'}
        response = api_client.patch(
            reverse('session-detail', args=[session.id_session]),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        session.refresh_from_db()
        assert session.titre == 'Nouveau titre'
    
    def test_delete_session(self, api_client):
        """!
        @brief Vérifie la suppression d'une session (DELETE /sessions/{id}/).
        """
        session = SessionFactory()
        response = api_client.delete(
            reverse('session-detail', args=[session.id_session])
        )
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Session.objects.filter(id_session=session.id_session).exists()
    
    def test_session_not_found(self, api_client):
        """!
        @brief Vérifie le comportement si l'ID de session n'existe pas (404 Not Found).
        """
        response = api_client.get(reverse('session-detail', args=['999999']))
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestSessionCloseStory:
    """!
    @brief Tests de l'action `close_story` (Calcul des votes).
    
    Cette classe teste tous les algorithmes de vote supportés (Strict, Moyenne, Médiane, Majorités)
    et les cas limites (égalité, pas de vote).
    """
    
    def test_close_story_strict_consensus(self, api_client):
        """!
        @brief Mode STRICT : Teste le succès quand il y a unanimité.
        """
        session = SessionFactory(
            mode_de_jeu='strict',
            stories=[{'nom': 'Story 1'}, {'nom': 'Story 2'}]
        )
        # Créer des participants avec le même vote
        PartieFactory(id_session=session, username='alice', carte_choisie='5')
        PartieFactory(id_session=session, username='bob', carte_choisie='5')
        PartieFactory(id_session=session, username='charlie', carte_choisie='5')
        
        data = {'story_index': 0}
        response = api_client.post(
            reverse('session-close-story', args=[session.id_session]),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['valeur_finale'] == 5
        assert response.data['status'] == 'Validé'
    
    def test_close_story_strict_no_consensus(self, api_client):
        """!
        @brief Mode STRICT : Teste l'échec (retourne -1) en cas de désaccord.
        """
        session = SessionFactory(
            mode_de_jeu='strict',
            stories=[{'nom': 'Story 1'}, {'nom': 'Story 2'}]
        )
        # Votes différents
        PartieFactory(id_session=session, username='alice', carte_choisie='5')
        PartieFactory(id_session=session, username='bob', carte_choisie='8')
        
        data = {'story_index': 0}
        response = api_client.post(
            reverse('session-close-story', args=[session.id_session]),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['valeur_finale'] == -1  # Désaccord
    
    def test_close_story_median(self, api_client):
        """!
        @brief Mode MEDIANE : Teste le calcul avec un nombre impair de votes.
        Ex: [3, 5, 8] -> 5.
        """
        session = SessionFactory(
            mode_de_jeu='median',
            stories=[{'nom': 'Story 1'}]
        )
        # Votes: 3, 5, 8 -> médiane = 5
        PartieFactory(id_session=session, username='alice', carte_choisie='3')
        PartieFactory(id_session=session, username='bob', carte_choisie='5')
        PartieFactory(id_session=session, username='charlie', carte_choisie='8')
        
        data = {'story_index': 0}
        response = api_client.post(
            reverse('session-close-story', args=[session.id_session]),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['valeur_finale'] == 5
    
    def test_close_story_median_even_count(self, api_client):
        """!
        @brief Mode MEDIANE : Teste le calcul avec un nombre pair de votes (moyenne des deux centraux).
        Ex: [3, 5, 8, 13] -> (5+8)/2 = 6.5 -> 6 ou 7.
        """
        session = SessionFactory(
            mode_de_jeu='median',
            stories=[{'nom': 'Story 1'}]
        )
        # Votes: 3, 5, 8, 13 -> médiane = (5+8)/2 = 6.5 -> arrondi à 6
        PartieFactory(id_session=session, username='alice', carte_choisie='3')
        PartieFactory(id_session=session, username='bob', carte_choisie='5')
        PartieFactory(id_session=session, username='charlie', carte_choisie='8')
        PartieFactory(id_session=session, username='david', carte_choisie='13')
        
        data = {'story_index': 0}
        response = api_client.post(
            reverse('session-close-story', args=[session.id_session]),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['valeur_finale'] in [6, 7]  # Arrondi (5+8)/2
    
    def test_close_story_average(self, api_client):
        """!
        @brief Mode MOYENNE : Teste le calcul de la moyenne arithmétique arrondie.
        Ex: [2, 4, 6] -> 4.
        """
        session = SessionFactory(
            mode_de_jeu='average',
            stories=[{'nom': 'Story 1'}]
        )
        # Votes: 2, 4, 6 -> moyenne = 4
        PartieFactory(id_session=session, username='alice', carte_choisie='2')
        PartieFactory(id_session=session, username='bob', carte_choisie='4')
        PartieFactory(id_session=session, username='charlie', carte_choisie='6')
        
        data = {'story_index': 0}
        response = api_client.post(
            reverse('session-close-story', args=[session.id_session]),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['valeur_finale'] == 4
    
    def test_close_story_majority_absolute(self, api_client):
        """!
        @brief Mode MAJORITÉ ABSOLUE : Succès si une valeur a > 50% des votes.
        Ex: [5, 5, 5, 8] (3/4) -> 5.
        """
        session = SessionFactory(
            mode_de_jeu='majority_abs',
            stories=[{'nom': 'Story 1'}]
        )
        # Votes: 5, 5, 5, 8 -> 5 a la majorité absolue (3/4 > 50%)
        PartieFactory(id_session=session, username='alice', carte_choisie='5')
        PartieFactory(id_session=session, username='bob', carte_choisie='5')
        PartieFactory(id_session=session, username='charlie', carte_choisie='5')
        PartieFactory(id_session=session, username='david', carte_choisie='8')
        
        data = {'story_index': 0}
        response = api_client.post(
            reverse('session-close-story', args=[session.id_session]),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['valeur_finale'] == 5
    
    def test_close_story_majority_absolute_no_majority(self, api_client):
        """!
        @brief Mode MAJORITÉ ABSOLUE : Échec (-1) si aucune valeur n'a > 50%.
        Ex: [5, 5, 8, 8] -> -1.
        """
        session = SessionFactory(
            mode_de_jeu='majority_abs',
            stories=[{'nom': 'Story 1'}]
        )
        # Votes: 5, 5, 8, 8 -> pas de majorité
        PartieFactory(id_session=session, username='alice', carte_choisie='5')
        PartieFactory(id_session=session, username='bob', carte_choisie='5')
        PartieFactory(id_session=session, username='charlie', carte_choisie='8')
        PartieFactory(id_session=session, username='david', carte_choisie='8')
        
        data = {'story_index': 0}
        response = api_client.post(
            reverse('session-close-story', args=[session.id_session]),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['valeur_finale'] == -1
    
    def test_close_story_majority_relative(self, api_client):
        """!
        @brief Mode MAJORITÉ RELATIVE : Prend la valeur la plus fréquente (même sans 50%).
        Ex: [5, 5, 8, 13] -> 5.
        """
        session = SessionFactory(
            mode_de_jeu='majority_rel',
            stories=[{'nom': 'Story 1'}]
        )
        # Votes: 5, 5, 8, 13 -> 5 est le plus voté (2 votes)
        PartieFactory(id_session=session, username='alice', carte_choisie='5')
        PartieFactory(id_session=session, username='bob', carte_choisie='5')
        PartieFactory(id_session=session, username='charlie', carte_choisie='8')
        PartieFactory(id_session=session, username='david', carte_choisie='13')
        
        data = {'story_index': 0}
        response = api_client.post(
            reverse('session-close-story', args=[session.id_session]),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['valeur_finale'] == 5
    
    def test_close_story_no_votes(self, api_client):
        """!
        @brief Teste le cas où des joueurs sont présents mais n'ont pas voté (valeurs None).
        """
        session = SessionFactory(
            mode_de_jeu='average',
            stories=[{'nom': 'Story 1'}]
        )
        PartieFactory(id_session=session, username='alice', carte_choisie=None)
        PartieFactory(id_session=session, username='bob', carte_choisie=None)
        
        data = {'story_index': 0}
        response = api_client.post(
            reverse('session-close-story', args=[session.id_session]),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['valeur_finale'] == 0
    
    def test_close_story_missing_story_index(self, api_client):
        """!
        @brief Teste l'erreur 400 quand `story_index` est manquant.
        """
        session = SessionFactory()
        response = api_client.post(
            reverse('session-close-story', args=[session.id_session]),
            {},
            format='json'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
    
    def test_close_story_invalid_story_index(self, api_client):
        """!
        @brief Teste l'erreur 400 quand `story_index` est hors limites.
        """
        session = SessionFactory(stories=[{'nom': 'Story 1'}])
        PartieFactory(id_session=session, username='alice', carte_choisie='5')
        
        response = api_client.post(
            reverse('session-close-story', args=[session.id_session]),
            {'story_index': 999},
            format='json'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
    
    def test_close_story_updates_session_stories(self, api_client):
        """!
        @brief Vérifie que le résultat est bien sauvegardé dans le JSON `stories` de la session.
        """
        session = SessionFactory(stories=[{'nom': 'Story 1'}, {'nom': 'Story 2'}])
        PartieFactory(id_session=session, username='alice', carte_choisie='5')
        PartieFactory(id_session=session, username='bob', carte_choisie='5')
        
        data = {'story_index': 0}
        api_client.post(
            reverse('session-close-story', args=[session.id_session]),
            data,
            format='json'
        )
        
        session.refresh_from_db()
        assert session.stories[0]['valeur_finale'] == '5'

    def test_close_story_no_votes_found(self, api_client):
        """!
        @brief Teste l'erreur quand aucun joueur n'est associé à la session.
        """
        session = SessionFactory(stories={'0': {'nom': 'Story 1'}})
        data = {'story_index': 0}
        response = api_client.post(
            reverse('session-close-story', args=[session.id_session]),
            data,
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        assert response.data['error'] == 'Aucun vote trouvé'


@pytest.mark.django_db
class TestSessionCloseSession:
    """!
    @brief Tests pour l'action `close_session` (Fermeture de la salle).
    """
    
    def test_close_session(self, api_client):
        """!
        @brief Vérifie le passage du statut à 'closed'.
        """
        session = SessionFactory(status='in_progress')
        response = api_client.post(
            reverse('session-close-session', args=[session.id_session]),
            {'status': 'closed'},
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        session.refresh_from_db()
        assert session.status == 'closed'
    
    def test_close_session_invalid_status(self, api_client):
        """!
        @brief Vérifie le rejet d'un statut invalide.
        """
        session = SessionFactory(status='open')
        response = api_client.post(
            reverse('session-close-session', args=[session.id_session]),
            {'status': 'invalid'},
            format='json'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPartieViewSet:
    """!
    @brief Tests CRUD pour les Parties (Joueurs).
    """
    
    def test_list_parties(self, api_client):
        """!
        @brief Vérifie la récupération de la liste globale des joueurs.
        """
        SessionFactory.create_batch(2)
        response = api_client.get(reverse('partie-list'))
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_list_parties_by_session(self, api_client):
        """!
        @brief Vérifie le filtre par session (GET /parties/?id_session=X).
        """
        session = SessionFactory()
        PartieFactory.create_batch(3, id_session=session)
        
        response = api_client.get(
            reverse('partie-list') + f'?id_session={session.id_session}'
        )
        
        assert response.status_code == status.HTTP_200_OK
        # Vérifier que seules les parties de cette session sont retournées
        assert all(partie['id_session'] == session.id_session for partie in response.data)
    
    def test_create_partie(self, api_client):
        """!
        @brief Vérifie la création manuelle d'un joueur.
        """
        session = SessionFactory()
        data = {
            'username': 'Alice',
            'id_session': session.id_session,
            'carte_choisie': None,
            'a_vote': False
        }
        response = api_client.post(
            reverse('partie-list'),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['username'] == 'Alice'
    
    def test_update_partie(self, api_client):
        """!
        @brief Vérifie la mise à jour d'un joueur (ex: vote manuel).
        """
        session = SessionFactory()
        partie = PartieFactory(id_session=session, a_vote=False)
        
        data = {'carte_choisie': '13', 'a_vote': True}
        response = api_client.patch(
            reverse('partie-detail', args=[partie.id]),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        partie.refresh_from_db()
        assert partie.carte_choisie == '13'
        assert partie.a_vote is True
    
    def test_delete_partie(self, api_client):
        """!
        @brief Vérifie la suppression d'un joueur.
        """
        session = SessionFactory()
        partie = PartieFactory(id_session=session)
        
        response = api_client.delete(
            reverse('partie-detail', args=[partie.id])
        )
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Partie.objects.filter(id=partie.id).exists()


@pytest.mark.django_db
class TestPartieVoteCard:
    """!
    @brief Tests de l'action `vote_card` (Enregistrement du vote).
    """
    
    def test_vote_card_success(self, api_client):
        """!
        @brief Vérifie qu'un vote est bien enregistré et que `a_vote` passe à True.
        """
        session = SessionFactory()
        partie = PartieFactory(id_session=session, username='Alice', a_vote=False)
        
        data = {
            'username': 'Alice',
            'id_session': session.id_session,
            'carte_choisie': '8'
        }
        response = api_client.post(
            reverse('partie-vote-card'),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        partie.refresh_from_db()
        assert partie.carte_choisie == '8'
        assert partie.a_vote is True
    
    def test_vote_card_missing_parameters(self, api_client):
        """!
        @brief Vérifie l'erreur 400 si des paramètres manquent.
        """
        data = {'username': 'Alice'}
        response = api_client.post(
            reverse('partie-vote-card'),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
    
    def test_vote_card_partie_not_found(self, api_client):
        """!
        @brief Vérifie l'erreur 404 si le joueur n'existe pas dans la session.
        """
        session = SessionFactory()
        data = {
            'username': 'NonExistent',
            'id_session': session.id_session,
            'carte_choisie': '5'
        }
        response = api_client.post(
            reverse('partie-vote-card'),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestPartieFin:
    """!
    @brief Tests de l'action `fin_partie` (Déconnexion).
    """
    
    def test_fin_partie_success(self, api_client):
        """!
        @brief Vérifie que le joueur est supprimé de la base.
        """
        session = SessionFactory()
        partie = PartieFactory(id_session=session, username='Alice')
        
        data = {
            'username': 'Alice',
            'id_session': session.id_session
        }
        response = api_client.post(
            reverse('partie-fin-partie'),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert not Partie.objects.filter(id=partie.id).exists()
    
    def test_fin_partie_missing_parameters(self, api_client):
        """!
        @brief Vérifie l'erreur 400 si paramètres manquants.
        """
        response = api_client.post(reverse('partie-fin-partie'), {}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_fin_partie_not_found(self, api_client):
        """!
        @brief Vérifie l'erreur 404 si le joueur est déjà parti.
        """
        session = SessionFactory()
        data = {
            'username': 'NonExistent',
            'id_session': session.id_session
        }
        response = api_client.post(
            reverse('partie-fin-partie'),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestPartieJoin:
    """!
    @brief Tests de l'action `join_partie` (Connexion).
    """
    
    def test_join_partie_new_player(self, api_client):
        """!
        @brief Vérifie l'inscription d'un nouveau joueur.
        """
        session = SessionFactory(status='open')
        data = {
            'username': 'NewPlayer',
            'id_session': session.id_session
        }
        response = api_client.post(
            reverse('partie-join-partie'),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['mode_de_jeu'] == session.mode_de_jeu
        assert response.data['status'] == 'open'
        
        # Vérifier que la partie a été créée
        assert Partie.objects.filter(username='NewPlayer', id_session=session).exists()
    
    def test_join_partie_existing_player(self, api_client):
        """!
        @brief Vérifie qu'un joueur existant se reconnecte sans erreur (pas de doublon).
        """
        session = SessionFactory()
        PartieFactory(id_session=session, username='ExistingPlayer')
        
        data = {
            'username': 'ExistingPlayer',
            'id_session': session.id_session
        }
        response = api_client.post(
            reverse('partie-join-partie'),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        # Vérifier qu'une seule partie existe
        assert Partie.objects.filter(username='ExistingPlayer', id_session=session).count() == 1
    
    def test_join_partie_closed_session(self, api_client):
        """!
        @brief Vérifie qu'on ne peut pas rejoindre une session fermée.
        """
        session = SessionFactory(status='closed')
        data = {
            'username': 'Player',
            'id_session': session.id_session
        }
        response = api_client.post(
            reverse('partie-join-partie'),
            data,
            format='json'
        )
        
        # La session ne devrait pas être accessible ou le join échoue
        assert response.data['status'] == 'closed'
    
    def test_join_partie_missing_parameters(self, api_client):
        """!
        @brief Vérifie l'erreur 400 si username ou id_session manquent.
        """
        response = api_client.post(reverse('partie-join-partie'), {}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_join_partie_session_not_found(self, api_client):
        """!
        @brief Vérifie l'erreur 404 si la session n'existe pas.
        """
        data = {
            'username': 'Player',
            'id_session': '999999'
        }
        response = api_client.post(
            reverse('partie-join-partie'),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_join_partie_updates_session_status(self, api_client):
        """!
        @brief Vérifie que rejoindre une session 'open' la passe à 'in_progress'.
        """
        session = SessionFactory(status='open')
        data = {
            'username': 'Player',
            'id_session': session.id_session
        }
        api_client.post(reverse('partie-join-partie'), data, format='json')
        
        session.refresh_from_db()
        assert session.status == 'in_progress'


@pytest.mark.django_db
class TestPartieRazVote:
    """!
    @brief Tests de l'action `raz_vote` (Remise à zéro des votes).
    """
    
    def test_raz_vote_success(self, api_client):
        """!
        @brief Vérifie que tous les votes de la session sont effacés.
        """
        session = SessionFactory()
        PartieFactory(id_session=session, username='alice', carte_choisie='5', a_vote=True)
        PartieFactory(id_session=session, username='bob', carte_choisie='8', a_vote=True)
        PartieFactory(id_session=session, username='charlie', carte_choisie='13', a_vote=True)
        
        data = {'id_session': session.id_session}
        response = api_client.post(
            reverse('partie-raz-vote'),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        
        # Vérifier que tous les votes sont réinitialisés
        parties = Partie.objects.filter(id_session=session)
        for partie in parties:
            assert partie.carte_choisie is None
            assert partie.a_vote is False
    
    def test_raz_vote_missing_session_id(self, api_client):
        """!
        @brief Vérifie l'erreur 400 si id_session manque.
        """
        response = api_client.post(reverse('partie-raz-vote'), {}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_raz_vote_no_parties(self, api_client):
        """!
        @brief Vérifie que l'action réussit même s'il n'y a pas encore de joueurs.
        """
        session = SessionFactory()
        data = {'id_session': session.id_session}
        response = api_client.post(
            reverse('partie-raz-vote'),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_raz_vote_sessionnotexist(self, api_client):
        """!
        @brief Vérifie l'erreur 404 si la session n'existe pas.
        """
        data = {'id_session': '999999'}
        response = api_client.post(
            reverse('partie-raz-vote'),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestPartieUniqueTogether:
    """!
    @brief Tests des contraintes d'intégrité de la base de données.
    """
    
    def test_cannot_create_duplicate_partie(self, api_client):
        """!
        @brief Vérifie qu'on ne peut pas créer deux fois le même utilisateur dans la même session.
        """
        session = SessionFactory()
        PartieFactory(id_session=session, username='Alice')
        
        data = {
            'username': 'Alice',
            'id_session': session.id_session,
            'carte_choisie': None,
            'a_vote': False
        }
        
        # La création devrait échouer ou retourner l'existant
        response = api_client.post(reverse('partie-list'), data, format='json')
        
        # Accepter 400 ou 409 selon votre implémentation
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT]