from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Session, Partie
from .serializers import SessionSerializer, PartieSerializer #, JoinPartieSerializer

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    @action(detail=True, methods=['post'])
    def close_story(self, request, pk=None):
        session = self.get_object()
        
        story_index = request.data.get('story_index')
        custom_value = request.data.get('final_value') # <--- ON RÉCUPÈRE LA VALEUR FORCÉE

        if story_index is None:
            return Response({'error': 'Index manquant'}, status=status.HTTP_400_BAD_REQUEST)

        # SI une valeur est envoyée (ex: "5", "8", "?"), on l'utilise directement
        if custom_value:
            resultat_final = custom_value
        else:
            # SINON : Calcul automatique de la moyenne (fallback)
            votes = Partie.objects.filter(id_session=session)
            valeurs = [int(v.carte_choisie) for v in votes if v.carte_choisie and v.carte_choisie.isdigit()]
            resultat_final = round(sum(valeurs) / len(valeurs)) if valeurs else 0

        # Mise à jour du JSON
        stories = list(session.stories)
        if 0 <= story_index < len(stories):
            stories[story_index]['valeur_finale'] = str(resultat_final)
            session.stories = stories
            session.save()
            
            # Reset des votes
            Partie.objects.filter(id_session=session).update(carte_choisie=None, a_vote=False)
            
            return Response({'status': 'Validé', 'valeur_finale': resultat_final})
        
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

        if not username or not id_session:
            return Response({'error': 'Paramètres manquants'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = Session.objects.get(pk=id_session)
            if session.status == 'closed':
                return Response({'status': 'closed'}, status=status.HTTP_200_OK)

            partie, created = Partie.objects.get_or_create(username=username, id_session=session)
            serializer = PartieSerializer(partie)
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

        except Session.DoesNotExist:
            return Response({'error': 'Session introuvable'}, status=status.HTTP_404_NOT_FOUND)
        
        
        # Si le temps on peut ajouter dans la creation de la session un nb de participant max 
        # et ici vérifier le nombre de participants avant d'autoriser l'ajout sinon message dans le foront
