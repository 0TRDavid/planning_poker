from rest_framework import viewsets
from .models import Session, Partie
from .serializers import SessionSerializer
from .serializers import PartieSerializer
from .serializers import JoinPartieSerializer
from .serializers import VoteSerializer

# Apparemment mauvaise methode ! il faut utiliser des @action dans les ViewSet existants
class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

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
        queryset = Partie.objects.all()
        id_session = self.request.query_params.get('id_session')
        
        if id_session is not None:
            queryset = queryset.filter(id_session=id_session)
        return queryset