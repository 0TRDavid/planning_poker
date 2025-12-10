from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Session, Partie
from .serializers import SessionSerializer, PartieSerializer, JoinPartieSerializer, VoteSerializer

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    @action(detail=True, methods=['post'])
    def close_story(self, request, pk=None):
        session = self.get_object()
        
        # Récupération et validation de l'index
        story_index = request.data.get('story_index')
        if story_index is None:
            return Response({'error': 'Index manquant'}, status=status.HTTP_400_BAD_REQUEST)

        # Calcul de la moyenne des votes (exclut les cartes spéciales)
        votes = Partie.objects.filter(id_session=session)
        valeurs = [int(v.carte_choisie) for v in votes if v.carte_choisie and v.carte_choisie.isdigit()]
        
        resultat_final = round(sum(valeurs) / len(valeurs)) if valeurs else 0

        # Mise à jour du JSON de la session
        stories = list(session.stories) # Copie pour mutabilité
        if 0 <= story_index < len(stories):
            stories[story_index]['valeur_finale'] = str(resultat_final)
            session.stories = stories
            session.save()
            
            # Reset des votes pour le round suivant
            votes.update(carte_choisie=None, a_vote=False)
            
            return Response({
                'status': 'Story validée', 
                'valeur_finale': resultat_final,
                'stories': session.stories
            })
        
        return Response({'error': 'Index invalide'}, status=status.HTTP_400_BAD_REQUEST)

class JoinPartieViewSet(viewsets.ModelViewSet):
    queryset = Partie.objects.all()
    serializer_class = JoinPartieSerializer

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Partie.objects.all()
    serializer_class = VoteSerializer

class PartieViewSet(viewsets.ModelViewSet):
    queryset = Partie.objects.all()
    serializer_class = PartieSerializer

    def get_queryset(self):
        """Filtre les joueurs par session si l'ID est fourni dans l'URL"""
        qs = super().get_queryset()
        session_id = self.request.query_params.get('id_session')
        return qs.filter(id_session=session_id) if session_id else qs