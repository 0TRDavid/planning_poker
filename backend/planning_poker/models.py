from django.db import models
from random import randint

class Session(models.Model):
    """!
    @brief Représente une session de jeu de Planning Poker.
    
    Cette classe agit comme le conteneur principal d'une partie. Elle stocke
    la configuration du jeu (titre, mode) et l'état des user stories.
    """

    def generate_six_digit_code():
        """!
        @brief Génère un code aléatoire unique à 6 chiffres.
        
        Utilisé comme valeur par défaut pour l'identifiant de session.
        
        @return Une chaîne de caractères de 6 chiffres (ex: "048239").
        """
        return f"{randint(0, 999999):06d}"

    ## @brief Identifiant unique (Code pin) pour rejoindre la session.
    id_session = models.CharField(
        max_length=6, 
        unique=True, 
        editable=False, 
        default=generate_six_digit_code, 
        primary_key=True
    )

    ## @brief Titre ou nom de la séance de poker.
    titre = models.CharField(max_length=255)

    """!
    @brief Liste des user stories à voter.
    
    Stocké au format JSON. Structure attendue :
    @code
    [
      {
        "titre": "Story 1",
        "contenu": "Description...",
        "valeur_finale": "5" // ou null si pas encore voté
      },
      ...
    ]
    @endcode
    """
    stories = models.JSONField()

    ## @brief Mode de calcul des résultats (ex: 'strict', 'average', 'median', 'majority_abs', 'majority_rel').
    mode_de_jeu = models.CharField(max_length=50)

    ## @brief État de la session ('open', 'in_progress', 'closed').
    status = models.CharField(max_length=50, default='open') 

    def __str__(self):
        """!
        @brief Représentation textuelle de la session.
        """
        return f"{self.titre} ({self.id_session} - {self.mode_de_jeu})"
    

class Partie(models.Model):
    """!
    @brief Représente la participation d'un joueur à une session.
    
    Cette table de liaison stocke l'état individuel de chaque joueur 
    (son vote actuel, s'il a voté, etc.) pour une session donnée.
    """

    # Note: user_id pourrait être ajouté ici plus tard via cookie/uuid.

    ## @brief Nom d'affichage du joueur.
    username = models.CharField(max_length=100)

    ## @brief Valeur de la carte sélectionnée (ex: "5", "8", "cafe", "?").
    ## Null si le joueur n'a pas encore choisi de carte.
    carte_choisie = models.CharField(max_length=10, blank=True, null=True)

    ## @brief Indique si le joueur a validé son vote pour le tour actuel.
    a_vote = models.BooleanField(default=False)

    ## @brief Lien vers la Session active (Clé étrangère).
    id_session = models.ForeignKey(Session, on_delete=models.CASCADE) 

    def __str__(self):
        return f"{self.username} in session {self.id_session.id_session}"
    
    class Meta:
        """!
        @brief Métadonnées du modèle Partie.
        """
        # Empêche d'avoir deux fois le même username dans la même session
        unique_together = ('username', 'id_session')