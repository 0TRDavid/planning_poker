from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Session, Partie
from .serializers import SessionSerializer, PartieSerializer

class SessionViewSet(viewsets.ModelViewSet):
    """!
    @brief VueSet pour la gestion des Sessions de Planning Poker.
    
    Permet de créer, voir et modifier les sessions. Contient la logique principale 
    pour la gestion du cycle de vie d'une session (fermeture de story, clôture de session).
    """
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    @action(detail=True, methods=['post'])
    def close_story(self, request, pk=None):
        """!
        @brief Clôture le vote pour une user story spécifique et calcule le résultat.
        
        Cette méthode récupère tous les votes des participants pour la session en cours,
        applique l'algorithme de calcul défini par `mode_de_jeu` (strict, median, average, etc.),
        et met à jour le JSON de la session avec la valeur finale.

        @param request Objet HttpRequest contenant les données POST :
            - `story_index` (int): L'index de la story dans le tableau JSON 'stories' de la session.
        @param pk Clé primaire de la session (id_session).

        @return Response :
            - 200 OK : Contient `{'status': 'Validé', 'valeur_finale': <valeur>}`.
            - 400 Bad Request : Si l'index est invalide, manquant ou si aucun vote n'est trouvé.
        
        @note En mode 'strict', si les votes ne sont pas unanimes, `valeur_finale` sera -1.
        """
        # Modes de calcul supportés
        modes_de_calcul = ['strict', 'median', 'average', 'majority_abs', 'majority_rel']
        session = self.get_object()
        story_index = request.data.get('story_index')

        if story_index is None or not isinstance(story_index, int):
            return Response({'error': 'Index manquant'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            # Détermination du mode de calcul (défaut: average)
            mode_de_calcul = session.mode_de_jeu if session.mode_de_jeu in modes_de_calcul else 'average'
            resultat_final = 0
            votes = Partie.objects.filter(id_session=session)
            
            if votes.count() == 0:
                return Response({'error': 'Aucun vote trouvé'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Mise à jour du JSON
            stories = list(session.stories)
            if 0 <= story_index < len(stories):
                
                # --- Logique des modes de jeu ---
                if mode_de_calcul == 'strict':
                    cartes_choisies = [v.carte_choisie for v in votes if v.carte_choisie]
                    if len(set(cartes_choisies)) == 1 and cartes_choisies:
                        resultat_final = int(cartes_choisies[0])
                    else:
                        resultat_final = -1  # Désaccord

                elif mode_de_calcul == 'median':
                    valeurs = sorted([int(v.carte_choisie) for v in votes if v.carte_choisie and v.carte_choisie.isdigit()])
                    n = len(valeurs)
                    if n % 2 == 1:
                        resultat_final = valeurs[n // 2]
                    else:
                        resultat_final = round((valeurs[n // 2 - 1] + valeurs[n // 2]) / 2)
                
                elif mode_de_calcul == 'average':
                    valeurs = [int(v.carte_choisie) for v in votes if v.carte_choisie and v.carte_choisie.isdigit()]
                    resultat_final = round(sum(valeurs) / len(valeurs)) if valeurs else 0
                
                elif mode_de_calcul == 'majority_abs':
                    from collections import Counter
                    cartes = [v.carte_choisie for v in votes if v.carte_choisie]
                    if cartes:
                        most_common = Counter(cartes).most_common(1)[0]
                        resultat_final = int(most_common[0]) if most_common[1] > len(cartes) / 2 else -1

                elif mode_de_calcul == 'majority_rel':
                    from collections import Counter
                    cartes = [v.carte_choisie for v in votes if v.carte_choisie]
                    if cartes:
                        most_common = Counter(cartes).most_common(1)[0]
                        resultat_final = int(most_common[0])

                # Sauvegarde du résultat dans le JSON stories
                stories[story_index]['valeur_finale'] = str(resultat_final) 
                session.stories = stories
                session.save()
                
                return Response({'status': 'Validé', 'valeur_finale': resultat_final})
            else:
                return Response({'error': 'Index invalide'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def close_session(self, request, pk=None):
        """!
        @brief Ferme définitivement une session.
        
        Passe le statut de la session à 'closed'. Empêche de nouveaux joueurs de rejoindre.

        @param request Objet HttpRequest contenant `status='closed'`.
        @param pk Clé primaire de la session.
        @return Response JSON confirmant la fermeture.
        """
        session = self.get_object()
        if request.data.get('status') == 'closed':
            session.status = 'closed' # Evite la saisie directe depuis le frontend
            session.save()
            return Response({'status': 'Session fermée'})
        return Response({'error': 'Statut invalide'}, status=status.HTTP_400_BAD_REQUEST)


class PartieViewSet(viewsets.ModelViewSet):
    """!
    @brief VueSet pour la gestion des participants (joueurs).
    
    Gère les actions liées aux joueurs : rejoindre une partie, voter, 
    quitter la partie, et réinitialiser les votes.
    """
    queryset = Partie.objects.all()
    serializer_class = PartieSerializer

    def get_queryset(self):
        """!
        @brief Filtre les participants par session.
        
        Si un paramètre `id_session` est fourni dans l'URL, ne renvoie que les joueurs
        de cette session. Sinon, renvoie tous les joueurs.
        """
        qs = super().get_queryset()
        session_id = self.request.query_params.get('id_session')
        return qs.filter(id_session=session_id) if session_id else qs
    
    @action(detail=False, methods=['post'])
    def vote_card(self, request):
        """!
        @brief Enregistre le vote d'un joueur.
        
        Met à jour le champ `carte_choisie` et passe `a_vote` à True pour le joueur donné.

        @param request Objet HttpRequest contenant :
            - `username` (str): Nom du joueur.
            - `id_session` (str): ID de la session.
            - `carte_choisie` (str): La valeur de la carte votée (ex: "5", "?", "cafe").
        
        @return Response 200 OK si le vote est enregistré, ou erreur 400/404.
        """
        username = request.data.get('username')
        id_session = request.data.get('id_session')
        carte_choisie = request.data.get('carte_choisie')

        if not username or not id_session or carte_choisie is None:
            return Response({'error': 'Paramètres manquants'}, status=status.HTTP_400_BAD_REQUEST)

        partie = Partie.objects.filter(username=username, id_session=id_session).first()
        if not partie:
            return Response({'error': 'Partie introuvable'}, status=status.HTTP_404_NOT_FOUND)

        partie.carte_choisie = carte_choisie
        partie.a_vote = True
        partie.save()
        return Response({'status': 'Vote enregistré'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def fin_partie(self, request):
        """!
        @brief Supprime un joueur d'une session (Déconnexion).
        
        Utilisé lorsqu'un joueur quitte l'écran de jeu ou que la session se termine.

        @param request Objet HttpRequest contenant `username` et `id_session`.
        @return Response confirmant la suppression du joueur.
        """
        username = request.data.get('username')
        id_session = request.data.get('id_session')
        partie = Partie.objects.filter(username=username, id_session=id_session).first()
        if not username or not id_session:
            return Response({'error': 'Paramètres manquants'}, status=status.HTTP_400_BAD_REQUEST)

        if not partie:
            return Response({'error': 'Partie introuvable'}, status=status.HTTP_404_NOT_FOUND)

        partie.delete()
        return Response({'status': 'Joueur supprimé de la session'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def join_partie(self, request):
        """!
        @brief Inscrit un joueur dans une session.
        
        Si la session existe et n'est pas fermée, crée une entrée Partie pour ce joueur.
        Passe automatiquement le statut de la session à 'in_progress'.

        @param request Objet HttpRequest contenant `username` et `id_session`.
        
        @return Response contenant :
            - `mode_de_jeu`: Le mode de jeu de la session rejointe.
            - `status`: Le statut de la session.
        """
        username = request.data.get('username')
        id_session = request.data.get('id_session')
        created = False
        if not username or not id_session:
            return Response({'error': 'Paramètres manquants'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            session = Session.objects.get(pk=id_session)
            statut = session.status
            mode_de_jeu = session.mode_de_jeu
            if statut != 'closed': 
                created = Partie.objects.get_or_create(username=username, id_session=session)
                session.status = 'in_progress'  # Mettre à jour le statut de la session
                session.save()

            return_data = {
                'mode_de_jeu': mode_de_jeu,
                'status': statut,
            }
            
            return Response(return_data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

        except Session.DoesNotExist:
            return Response({'error': 'Session introuvable'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['post'])
    def raz_vote(self, request):
        """!
        @brief Réinitialise les votes pour une nouvelle manche.
        
        Remet à zéro (null/False) les champs `carte_choisie` et `a_vote` 
        pour tous les joueurs de la session donnée.

        @param request Objet HttpRequest contenant `id_session`.
        @return Response confirmant la réinitialisation.
        """
        id_session = request.data.get('id_session')
        if not id_session:
            return Response({'error': 'Paramètres manquants'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # On vérifie que la session existe
            Session.objects.get(pk=id_session)
            Partie.objects.filter(id_session=id_session).update(carte_choisie=None, a_vote=False)
            return Response({'status': 'Vote réinitialisé'}, status=status.HTTP_200_OK)
        except Session.DoesNotExist:
            return Response({'error': 'Session introuvable'}, status=status.HTTP_404_NOT_FOUND)