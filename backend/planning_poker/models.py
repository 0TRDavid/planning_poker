from django.db import models

from random import randint

class Session(models.Model):
    def generate_six_digit_code():
        return f"{randint(0, 999999):06d}"
    id_session = models.CharField(max_length=6, unique=True, editable=False, default=generate_six_digit_code, primary_key=True)
    titre = models.CharField(max_length=255)
    stories = models.JSONField()
    mode_de_jeu = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='open') # open, in_progress, closed
    def __str__(self):
        return f"{self.titre} ({self.id_session} - {self.mode_de_jeu})"
    


class Partie(models.Model):
    # user_id = models.CharField(max_length=100, unique=True, editable=False)  a ajouter si le temps (envoyer un cookie unique par joueur depuis le front)
    username = models.CharField(max_length=100)
    carte_choisie = models.CharField(max_length=10, blank=True, null=True)
    a_vote = models.BooleanField(default=False)
    id_session = models.ForeignKey(Session, on_delete=models.CASCADE) # id de la table session = code de la session (6 chiffres) pour rejoindre la partie
    # est_admin = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.username} in session {self.id_session.id_session}"
    
    class Meta:
        unique_together = ('username', 'id_session') # Empeche 2 joueurs avec le même nom dans une même session

