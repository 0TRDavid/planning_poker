from rest_framework import serializers
from .models import Session
from .models import Partie


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id_session', 'titre', 'stories', 'mode_de_jeu']


class PartieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partie
        fields = '__all__'


class JoinPartieSerializer(serializers.ModelSerializer):
    id_session = serializers.PrimaryKeyRelatedField(
        source='session',
        queryset=Session.objects.all(),
        write_only=True
    )

    class Meta:
        model = Partie
        fields = ['username', 'id_session']  # Inclure id_session ici



# class VoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Partie
#         fields = ['username', 'carte_choisie']
#         if fields[1].value is not None:
#             fields.append('a_vote')