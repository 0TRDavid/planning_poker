# tests/test_serializers.py
import pytest
from planning_poker.serializers import SessionSerializer, PartieSerializer
from tests.factories import SessionFactory, PartieFactory


class TestSessionSerializer:
    """Tests pour SessionSerializer"""
    @pytest.mark.django_db
    def test_serialize_session(self):
        """Test la sérialisation d'une session"""
        session = SessionFactory()
        serializer = SessionSerializer(session)
        assert 'id_session' in serializer.data
        assert 'titre' in serializer.data
        assert 'stories' in serializer.data
        assert 'mode_de_jeu' in serializer.data
        assert 'status' in serializer.data
    
    @pytest.mark.django_db
    def test_deserialize_session_valid(self):
        """Test la désérialisation valide"""
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
        """Test la désérialisation invalide"""
        data = {
            'titre': 'Nouvelle session'
            # Manque mode_de_jeu, stories, etc.
        }
        serializer = SessionSerializer(data=data)
        assert not serializer.is_valid()


class TestPartieSerializer:
    """Tests pour PartieSerializer"""
    @pytest.mark.django_db
    
    def test_serialize_partie(self):
        """Test la sérialisation d'une partie"""
        partie = PartieFactory()
        serializer = PartieSerializer(partie)
        assert 'username' in serializer.data
        assert 'carte_choisie' in serializer.data
        assert 'a_vote' in serializer.data
        assert 'id_session' in serializer.data

    @pytest.mark.django_db
    def test_deserialize_partie_valid(self):
        """Test la désérialisation valide"""
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
        """Test la désérialisation invalide"""
        data = {
            'username': 'Alice'
            # Manque id_session, etc.
        }
        serializer = PartieSerializer(data=data)
        assert not serializer.is_valid()
