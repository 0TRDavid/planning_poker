from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Session, Partie
from .serializers import SessionSerializer, PartieSerializer #, JoinPartieSerializer

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    @action(detail=True, methods=['post'])
    def close_story(self, request, pk=None): # lA fonction est appelé une fois par chaque joueur... 
        # On peut vérifier si la valeur est déja set et n'est pas cafe ou ? remvoyer comme deja set ?

        # 'strict'
        # 'median'
        # 'average'
        # 'majority_abs'
        # 'majority_rel'
        modes_de_calcul = ['strict', 'median', 'average', 'majority_abs', 'majority_rel']
        session = self.get_object()
        story_index = request.data.get('story_index')

        if story_index is None or not isinstance(story_index, int):
            return Response({'error': 'Index manquant'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            mode_de_calcul = session.mode_de_jeu if session.mode_de_jeu in modes_de_calcul else 'average' # On recupere le mode de calcul de la session
            resultat_final = 0
            votes = Partie.objects.filter(id_session=session)
            if votes.count() == 0:
                return Response({'error': 'Aucun vote trouvé'}, status=status.HTTP_400_BAD_REQUEST)
                    # Mise à jour du JSON
        stories = list(session.stories)
        if 0 <= story_index < len(stories):
        
            if mode_de_calcul == 'strict':
                cartes_choisies = [v.carte_choisie for v in votes if v.carte_choisie]
                if len(set(cartes_choisies)) == 1 and cartes_choisies:
                    resultat_final = int(cartes_choisies[0])
                else:
                    resultat_final = -1  # Indique un désaccord entre les joueurs, on ne peut pas close la story, a gerer dans le front
            

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

            stories[story_index]['valeur_finale'] = str(resultat_final) # On stocke en string pour gérer les cafés, -1 et ?
            session.stories = stories
            session.save()
            
            # Reset des votes
           # Partie.objects.filter(id_session=session).update(carte_choisie=None, a_vote=False)
            
            return Response({'status': 'Validé', 'valeur_finale': resultat_final})
        else:
            return Response({'error': 'Index invalide'}, status=status.HTTP_400_BAD_REQUEST)




    @action(detail=True, methods=['post'])
    def close_session(self, request, pk=None):
        session = self.get_object()
        if request.data.get('status') == 'closed':
            session.status = 'closed' # Evite la saisie directe depuis le frontend
            session.save()
            return Response({'status': 'Session fermée'})
        return Response({'error': 'Statut invalide'}, status=status.HTTP_400_BAD_REQUEST)


class PartieViewSet(viewsets.ModelViewSet):
    queryset = Partie.objects.all()
    serializer_class = PartieSerializer

    def get_queryset(self):
        """Filtre les joueurs par session si l'ID est fourni dans l'URL"""
        qs = super().get_queryset()
        session_id = self.request.query_params.get('id_session')
        return qs.filter(id_session=session_id) if session_id else qs
    
    @action(detail=False, methods=['post'])
    def vote_card(self, request):
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
        username = request.data.get('username')
        id_session = request.data.get('id_session')
        created = False
        if not username or not id_session:
            return Response({'error': 'Paramètres manquants'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            session = Session.objects.get(pk=id_session)
            statut = session.status
            mode_de_jeu = session.mode_de_jeu
            if statut != 'closed': # And nombre de participants pas atteint
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
        
        # Si le temps on peut ajouter dans la creation de la session un nb de participant max 
        # et ici vérifier le nombre de participants avant d'autoriser l'ajout sinon message dans le foront

    @action(detail=False, methods=['post'])
    def raz_vote(self, request):
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

    # checkallvote