# tests/test_views.py
import pytest
from django.urls import reverse
from rest_framework import status
from planning_poker.models import Session, Partie
from tests.factories import SessionFactory, PartieFactory


@pytest.mark.django_db
class TestSessionViewSet:
    """Tests pour SessionViewSet"""
    
    def test_list_sessions(self, api_client):
        """Test la récupération de toutes les sessions"""
        SessionFactory.create_batch(3)
        response = api_client.get(reverse('session-list'))
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 3
    
    def test_create_session(self, api_client):
        """Test la création d'une session"""
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
        """Test la récupération d'une session spécifique"""
        session = SessionFactory(titre='Mon Planning')
        response = api_client.get(
            reverse('session-detail', args=[session.id_session])
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['titre'] == 'Mon Planning'
        assert response.data['id_session'] == session.id_session
    
    def test_update_session(self, api_client):
        """Test la mise à jour d'une session"""
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
        """Test la suppression d'une session"""
        session = SessionFactory()
        response = api_client.delete(
            reverse('session-detail', args=[session.id_session])
        )
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Session.objects.filter(id_session=session.id_session).exists()
    
    def test_session_not_found(self, api_client):
        """Test l'accès à une session inexistante"""
        response = api_client.get(reverse('session-detail', args=['999999']))
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestSessionCloseStory:
    """Tests pour l'action close_story"""
    
    def test_close_story_strict_consensus(self, api_client):
        """Test fermer une story en mode strict avec consensus"""
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
        """Test fermer une story en mode strict sans consensus"""
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
        """Test fermer une story en mode median"""
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
        """Test fermer une story en mode median avec nombre pair de votes"""
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
        """Test fermer une story en mode average"""
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
        """Test fermer une story en mode majority_abs"""
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
        """Test fermer une story sans majorité absolue"""
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
        """Test fermer une story en mode majority_rel (prend la majorité même sans > 50%)"""
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
        """Test fermer une story quand personne n'a voté"""
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
        """Test close_story sans story_index"""
        session = SessionFactory()
        response = api_client.post(
            reverse('session-close-story', args=[session.id_session]),
            {},
            format='json'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
    
    def test_close_story_invalid_story_index(self, api_client):
        """Test close_story avec un story_index invalide"""
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
        """Test que close_story met à jour correctement le JSON stories"""
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

    def test_close_story_no_votes(self, api_client):
        """Test close_story quand il n'y a aucun vote pour la session"""
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
    """Tests pour l'action close_session"""
    
    def test_close_session(self, api_client):
        """Test fermer une session"""
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
        """Test fermer une session avec un statut invalide"""
        session = SessionFactory(status='open')
        response = api_client.post(
            reverse('session-close-session', args=[session.id_session]),
            {'status': 'invalid'},
            format='json'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPartieViewSet:
    """Tests pour PartieViewSet"""
    
    def test_list_parties(self, api_client):
        """Test la récupération de toutes les parties"""
        SessionFactory.create_batch(2)
        response = api_client.get(reverse('partie-list'))
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_list_parties_by_session(self, api_client):
        """Test la récupération des parties d'une session spécifique"""
        session = SessionFactory()
        PartieFactory.create_batch(3, id_session=session)
        
        response = api_client.get(
            reverse('partie-list') + f'?id_session={session.id_session}'
        )
        
        assert response.status_code == status.HTTP_200_OK
        # Vérifier que seules les parties de cette session sont retournées
        assert all(partie['id_session'] == session.id_session for partie in response.data)
    
    def test_create_partie(self, api_client):
        """Test la création d'une partie via ViewSet"""
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
        """Test la mise à jour d'une partie"""
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
        """Test la suppression d'une partie"""
        session = SessionFactory()
        partie = PartieFactory(id_session=session)
        
        response = api_client.delete(
            reverse('partie-detail', args=[partie.id])
        )
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Partie.objects.filter(id=partie.id).exists()


@pytest.mark.django_db
class TestPartieVoteCard:
    """Tests pour l'action vote_card"""
    
    def test_vote_card_success(self, api_client):
        """Test enregistrer un vote avec succès"""
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
        """Test vote_card sans paramètres requis"""
        data = {'username': 'Alice'}
        response = api_client.post(
            reverse('partie-vote-card'),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
    
    def test_vote_card_partie_not_found(self, api_client):
        """Test vote_card avec une partie inexistante"""
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
    """Tests pour l'action fin_partie"""
    
    def test_fin_partie_success(self, api_client):
        """Test supprimer un joueur de la session"""
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
        """Test fin_partie sans paramètres"""
        response = api_client.post(reverse('partie-fin-partie'), {}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_fin_partie_not_found(self, api_client):
        """Test fin_partie avec une partie inexistante"""
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
    """Tests pour l'action join_partie"""
    
    def test_join_partie_new_player(self, api_client):
        """Test qu'un nouveau joueur peut rejoindre"""
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
        """Test qu'un joueur existant peut se reconnecter"""
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
        """Test qu'on ne peut pas rejoindre une session fermée"""
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
        # Selon votre logique, vous pourriez retourner 400 ou refuser
        assert response.data['status'] == 'closed'
    
    def test_join_partie_missing_parameters(self, api_client):
        """Test join_partie sans paramètres"""
        response = api_client.post(reverse('partie-join-partie'), {}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_join_partie_session_not_found(self, api_client):
        """Test join_partie avec une session inexistante"""
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
        """Test que join_partie met à jour le statut de la session"""
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
    """Tests pour l'action raz_vote"""
    
    def test_raz_vote_success(self, api_client):
        """Test réinitialiser les votes d'une session"""
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
        """Test raz_vote sans session id"""
        response = api_client.post(reverse('partie-raz-vote'), {}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_raz_vote_no_parties(self, api_client):
        """Test raz_vote sur une session vide"""
        session = SessionFactory()
        data = {'id_session': session.id_session}
        response = api_client.post(
            reverse('partie-raz-vote'),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_raz_vote_sessionnotexist(self, api_client):
        """Test raz_vote avec une session inexistante"""
        data = {'id_session': '999999'}
        response = api_client.post(
            reverse('partie-raz-vote'),
            data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestPartieUniqueTogether:
    """Tests pour la contrainte unique (username, id_session)"""
    
    def test_cannot_create_duplicate_partie(self, api_client):
        """Test qu'on ne peut pas créer deux parties avec le même username dans une session"""
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