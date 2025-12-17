# tests/test_models.py
import pytest
from planning_poker.models import Session, Partie
from tests.factories import SessionFactory, PartieFactory


@pytest.mark.django_db
class TestSession:
    """!
    @brief Suite de tests pour le modèle `Session`.
    
    Vérifie l'intégrité des données, la génération automatique des ID,
    les valeurs par défaut et le stockage du JSON.
    """
    
    def test_session_creation(self):
        """!
        @brief Vérifie la création basique d'une session.
        
        S'assure que les champs principaux (titre, mode de jeu) sont bien
        enregistrés et que les valeurs par défaut (status) sont appliquées.
        """
        session = SessionFactory(titre='Mon Planning', mode_de_jeu='strict')
        assert session.titre == 'Mon Planning'
        assert session.mode_de_jeu == 'strict'
        assert session.status == 'open'
        assert session.id_session is not None
    
    def test_session_id_is_six_digits(self):
        """!
        @brief Vérifie le format de l'ID de session.
        
        L'ID doit être une chaîne numérique de exactement 6 caractères.
        """
        session = SessionFactory()
        assert len(session.id_session) == 6
        assert session.id_session.isdigit()
    
    def test_session_id_is_unique(self):
        """!
        @brief Vérifie l'unicité des IDs de session.
        
        Bien que théoriquement improbable, factory_boy doit générer
        des sessions distinctes.
        """
        session1 = SessionFactory()
        # Créer une autre session avec un id_session différent
        session2 = SessionFactory()
        assert session1.id_session != session2.id_session
    
    def test_session_str(self):
        """!
        @brief Vérifie la méthode `__str__` du modèle Session.
        
        Le format attendu est "Titre (ID - Mode)".
        """
        session = SessionFactory(titre='Sprint 1', mode_de_jeu='strict')
        expected = f"Sprint 1 ({session.id_session} - strict)"
        assert str(session) == expected
    
    def test_session_default_status(self):
        """!
        @brief Vérifie que le statut par défaut est bien 'open'.
        """
        session = SessionFactory()
        assert session.status == 'open'
    
    def test_session_status_values(self):
        """!
        @brief Vérifie que le champ status accepte les valeurs attendues.
        
        Valeurs testées : 'open', 'in_progress', 'closed'.
        """
        statuses = ['open', 'in_progress', 'closed']
        for status in statuses:
            session = SessionFactory(status=status)
            assert session.status == status
    
    def test_session_stories_json(self):
        """!
        @brief Vérifie la persistance du champ JSONField `stories`.
        
        S'assure que les dictionnaires Python sont correctement sérialisés
        et récupérés depuis la base de données.
        """
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
    """!
    @brief Suite de tests pour le modèle `Partie` (Joueur).
    
    Vérifie les liens avec la Session, les contraintes d'unicité (unique_together)
    et le comportement lors de la suppression.
    """
    
    def test_partie_creation(self):
        """!
        @brief Vérifie la création d'un joueur rattaché à une session.
        """
        session = SessionFactory()
        partie = PartieFactory(username='Alice', id_session=session, carte_choisie=None)
        assert partie.username == 'Alice'
        assert partie.id_session == session
        assert partie.a_vote is False
        assert partie.carte_choisie is None
    
    def test_partie_str(self):
        """!
        @brief Vérifie la représentation textuelle d'une Partie.
        """
        session = SessionFactory()
        partie = PartieFactory(username='Bob', id_session=session)
        expected = f"Bob in session {session.id_session}"
        assert str(partie) == expected
    
    def test_partie_carte_choisie(self):
        """!
        @brief Vérifie que le choix de carte et l'état de vote sont bien persistés.
        """
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
        """!
        @brief Vérifie qu'une session peut contenir plusieurs joueurs différents.
        """
        session = SessionFactory()
        partie1 = PartieFactory(username='Alice', id_session=session)
        partie2 = PartieFactory(username='Bob', id_session=session)
        partie3 = PartieFactory(username='Charlie', id_session=session)
        
        parties = Partie.objects.filter(id_session=session)
        assert parties.count() == 3
    
    def test_unique_together_constraint(self):
        """!
        @brief Vérifie la contrainte d'unicité `(username, id_session)`.
        
        Il doit être impossible de créer deux fois le même joueur dans la même session.
        """
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
        """!
        @brief Vérifie la suppression en cascade (`on_delete=models.CASCADE`).
        
        Si une session est supprimée, tous les joueurs associés doivent l'être aussi.
        """
        session = SessionFactory()
        partie1 = PartieFactory(id_session=session)
        partie2 = PartieFactory(id_session=session)
        
        assert Partie.objects.filter(id_session=session).count() == 2
        
        # Supprimer la session
        session.delete()
        
        # Les parties doivent aussi être supprimées
        assert Partie.objects.filter(id_session_id=session.id_session).count() == 0
    
    def test_partie_possible_cartes(self):
        """!
        @brief Vérifie que le champ `carte_choisie` accepte différentes valeurs.
        """
        session = SessionFactory()
        cartes = ['1', '2', '3', '5', '8', '13', '20']
        
        for carte in cartes:
            partie = PartieFactory(id_session=session, username=f'player_{carte}', carte_choisie=carte)
            assert partie.carte_choisie == carte