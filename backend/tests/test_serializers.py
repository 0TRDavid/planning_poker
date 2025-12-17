# tests/test_serializers.py
import pytest
from planning_poker.serializers import SessionSerializer, PartieSerializer
from tests.factories import SessionFactory, PartieFactory


class TestSessionSerializer:
    """!
    @brief Tests unitaires pour le sérialiseur `SessionSerializer`.
    
    Vérifie que les objets Session sont correctement convertis en JSON et que
    les données entrantes (pour créer une session) sont bien validées.
    """

    @pytest.mark.django_db
    def test_serialize_session(self):
        """!
        @brief Vérifie la sérialisation (Objet -> JSON).
        
        S'assure que le JSON généré contient bien tous les champs attendus
        ('id_session', 'titre', 'stories', etc.).
        """
        session = SessionFactory()
        serializer = SessionSerializer(session)
        assert 'id_session' in serializer.data
        assert 'titre' in serializer.data
        assert 'stories' in serializer.data
        assert 'mode_de_jeu' in serializer.data
        assert 'status' in serializer.data
    
    @pytest.mark.django_db
    def test_deserialize_session_valid(self):
        """!
        @brief Vérifie la désérialisation valide (JSON -> Objet).
        
        Le sérialiseur doit accepter un dictionnaire complet et valide.
        """
        data = {
            'titre': 'Nouvelle session',
            'stories': {'story1': 'Feature A'},
            'mode_de_jeu': 'fibonacci',
            'status': 'open'
        }
        serializer = SessionSerializer(data=data)
        assert serializer.is_valid()

    @pytest.mark.django_db
    def test_deserialize_session_invalid(self):
        """!
        @brief Vérifie le rejet de données invalides.
        
        Le sérialiseur doit refuser les données s'il manque des champs obligatoires
        (comme 'stories' ou 'mode_de_jeu').
        """
        data = {
            'titre': 'Nouvelle session'
            # Manque mode_de_jeu, stories, etc.
        }
        serializer = SessionSerializer(data=data)
        assert not serializer.is_valid()


class TestPartieSerializer:
    """!
    @brief Tests unitaires pour le sérialiseur `PartieSerializer`.
    
    Vérifie la gestion des données des joueurs (sérialisation et validation).
    """

    @pytest.mark.django_db
    def test_serialize_partie(self):
        """!
        @brief Vérifie la sérialisation d'un joueur (Objet -> JSON).
        """
        partie = PartieFactory()
        serializer = PartieSerializer(partie)
        assert 'username' in serializer.data
        assert 'carte_choisie' in serializer.data
        assert 'a_vote' in serializer.data
        assert 'id_session' in serializer.data

    @pytest.mark.django_db
    def test_deserialize_partie_valid(self):
        """!
        @brief Vérifie la désérialisation valide pour un joueur.
        
        Doit réussir si tous les champs requis (dont la clé étrangère id_session) sont présents.
        """
        session = SessionFactory()
        data = {
            'username': 'Alice',
            'id_session': session.id_session,
            'carte_choisie': '5',
            'a_vote': True
        }
        serializer = PartieSerializer(data=data)
        assert serializer.is_valid()

    @pytest.mark.django_db
    def test_deserialize_partie_invalid(self):
        """!
        @brief Vérifie le rejet d'un joueur mal formé.
        
        Doit échouer si l'ID de session est manquant.
        """
        data = {
            'username': 'Alice'
            # Manque id_session, etc.
        }
        serializer = PartieSerializer(data=data)
        assert not serializer.is_valid()