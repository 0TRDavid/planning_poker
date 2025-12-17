from rest_framework import serializers
from .models import Session, Partie

class SessionSerializer(serializers.ModelSerializer):
    """!
    @brief Sérialiseur pour le modèle Session.
    
    Transforme les objets Session en format JSON et valide les données 
    entrantes pour la création ou la modification de sessions.
    Utilisé par SessionViewSet.
    """
    class Meta:
        """!
        @brief Métadonnées du sérialiseur Session.
        """
        model = Session
        ## @brief Champs exposés dans l'API.
        fields = ['id_session', 'titre', 'stories', 'mode_de_jeu', 'status']


class PartieSerializer(serializers.ModelSerializer):
    """!
    @brief Sérialiseur pour le modèle Partie.
    
    Gère la représentation JSON des joueurs (participants) d'une session.
    Permet notamment de valider les votes et les inscriptions.
    """
    class Meta:
        """!
        @brief Métadonnées du sérialiseur Partie.
        """
        model = Partie
        ## @brief Tous les champs du modèle sont inclus ('username', 'carte_choisie', etc.).
        fields = '__all__'