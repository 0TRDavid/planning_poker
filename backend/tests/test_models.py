# tests/test_models.py
import pytest
from planning_poker.models import Session, Partie
from tests.factories import SessionFactory, PartieFactory


@pytest.mark.django_db
class TestSession:
    """Tests pour le modèle Session"""
    
    def test_session_creation(self):
        """Test la création d'une session"""
        session = SessionFactory(titre='Mon Planning', mode_de_jeu='strict')
        assert session.titre == 'Mon Planning'
        assert session.mode_de_jeu == 'strict'
        assert session.status == 'open'
        assert session.id_session is not None
    
    def test_session_id_is_six_digits(self):
        """Test que l'id_session est un code à 6 chiffres"""
        session = SessionFactory()
        assert len(session.id_session) == 6
        assert session.id_session.isdigit()
    
    def test_session_id_is_unique(self):
        """Test que l'id_session est unique"""
        session1 = SessionFactory()
        # Créer une autre session avec un id_session différent
        session2 = SessionFactory()
        assert session1.id_session != session2.id_session
    
    def test_session_str(self):
        """Test la représentation string de Session"""
        session = SessionFactory(titre='Sprint 1', mode_de_jeu='strict')
        expected = f"Sprint 1 ({session.id_session} - strict)"
        assert str(session) == expected
    
    def test_session_default_status(self):
        """Test le statut par défaut"""
        session = SessionFactory()
        assert session.status == 'open'
    
    def test_session_status_values(self):
        """Test les différentes valeurs de statut"""
        statuses = ['open', 'in_progress', 'closed']
        for status in statuses:
            session = SessionFactory(status=status)
            assert session.status == status
    
    def test_session_stories_json(self):
        """Test le champ stories JSON"""
        stories = {
            "story1": "Développer API",
            "story2": "Faire tests",
            "story3": "Déployer"
        }
        session = SessionFactory(stories=stories)
        assert session.stories == stories
        assert "story1" in session.stories


@pytest.mark.django_db
class TestPartie:
    """Tests pour le modèle Partie"""
    
    def test_partie_creation(self):
        """Test la création d'une partie"""
        session = SessionFactory()
        partie = PartieFactory(username='Alice', id_session=session, carte_choisie=None)
        assert partie.username == 'Alice'
        assert partie.id_session == session
        assert partie.a_vote is False
        assert partie.carte_choisie is None
    
    def test_partie_str(self):
        """Test la représentation string de Partie"""
        session = SessionFactory()
        partie = PartieFactory(username='Bob', id_session=session)
        expected = f"Bob in session {session.id_session}"
        assert str(partie) == expected
    
    def test_partie_carte_choisie(self):
        """Test le choix de carte"""
        session = SessionFactory()
        partie = PartieFactory(id_session=session, carte_choisie='8')
        assert partie.carte_choisie == '8'
        
        # Voter
        partie.a_vote = True
        partie.save()
        partie.refresh_from_db()
        assert partie.a_vote is True
        assert partie.carte_choisie == '8'
    
    def test_multiple_parties_same_session(self):
        """Test plusieurs joueurs dans une même session"""
        session = SessionFactory()
        partie1 = PartieFactory(username='Alice', id_session=session)
        partie2 = PartieFactory(username='Bob', id_session=session)
        partie3 = PartieFactory(username='Charlie', id_session=session)
        
        parties = Partie.objects.filter(id_session=session)
        assert parties.count() == 3
    
    def test_unique_together_constraint(self):
        """Test la contrainte unique (username, id_session)"""
        session = SessionFactory()
        partie1 = PartieFactory(username='Alice', id_session=session)
        
        # Essayer de créer la même partie (même username, même session)
        with pytest.raises(Exception):  # IntegrityError
            partie2 = Partie.objects.create(
                username='Alice',
                id_session=session,
                carte_choisie=None,
                a_vote=False
            )
    
    def test_partie_cascade_delete(self):
        """Test la suppression en cascade quand la session est supprimée"""
        session = SessionFactory()
        partie1 = PartieFactory(id_session=session)
        partie2 = PartieFactory(id_session=session)
        
        assert Partie.objects.filter(id_session=session).count() == 2
        
        # Supprimer la session
        session.delete()
        
        # Les parties doivent aussi être supprimées
        assert Partie.objects.filter(id_session_id=session.id_session).count() == 0
    
    def test_partie_possible_cartes(self):
        """Test les différentes valeurs de cartes possibles"""
        session = SessionFactory()
        cartes = ['1', '2', '3', '5', '8', '13', '20']
        
        for carte in cartes:
            partie = PartieFactory(id_session=session, username=f'player_{carte}', carte_choisie=carte)
            assert partie.carte_choisie == carte
