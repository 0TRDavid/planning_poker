from django.db import models

from random import randint

class Session(models.Model):
    def generate_six_digit_code():
        return f"{randint(0, 999999):06d}"

    id_session = models.CharField(max_length=6, unique=True, editable=False, default=generate_six_digit_code)
    titre = models.CharField(max_length=255)
    stories = models.JSONField()  # Utilisez ici django.db.models.JSONField

    def __str__(self):
        return f"{self.titre} ({self.id_session})"
