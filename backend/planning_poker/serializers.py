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