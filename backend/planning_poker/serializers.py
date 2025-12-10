from rest_framework import serializers
from .models import Session
from .models import Partie


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id_session', 'titre', 'stories', 'mode_de_jeu', 'status']


class PartieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partie
        fields = '__all__'


class JoinPartieSerializer(serializers.ModelSerializer):
    id_session = serializers.PrimaryKeyRelatedField(
        queryset=Session.objects.all())
    status = serializers.SerializerMethodField() # Champ en lecture seule pour le status de la session
    class Meta:
        model = Partie
        fields = ['username', 'id_session', 'status']  # Inclure id_session ici
    def get_status(self, obj):
        return obj.id_session.status # Récupère le status de la session associée et le retourne

# MAJ de la table Partie pour gérer le vote
class VoteSerializer(serializers.ModelSerializer):
    id_session = serializers.PrimaryKeyRelatedField(
        queryset=Session.objects.all(),
        write_only=True
    )

    class Meta:
        model = Partie
        fields = ['id_session', 'username', 'carte_choisie']

    def create(self, validated_data):
        session = validated_data.pop('id_session')
        username = validated_data.get('username')
        carte_choisie = validated_data.get('carte_choisie')

        try:
            partie = Partie.objects.get(id_session=session, username=username)
        except Partie.DoesNotExist:
            partie = Partie(id_session=session, username=username)

        partie.carte_choisie = carte_choisie
        partie.a_vote = carte_choisie is not None
        partie.save()
        return partie

# class VoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Partie
#         fields = ['username', 'carte_choisie']
#         if fields[1].value is not None:
#             fields.append('a_vote')