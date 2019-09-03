from django.db.models import Sum
from rest_framework import viewsets, status, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from jesuspokerapi.models import Player, Session, SessionResult
from jesuspokerapi.serializers import PlayerSerializer, SessionSerializer, SessionResultSerializer, \
    PlayerScoreSerializer, \
    PlayerSessionSerializer


# Create your views here.

class PlayerView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def create(self, request, pk=None, company_pk=None, project_pk=None):
        is_many = True if isinstance(request.data, list) else False

        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FormView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    def create(self, request, *args, **kwargs):
        try:
            date = {"date": request.data.pop('date')}
        except KeyError as err:
            return Response({
                "error": "date not supplied",
                "details": str(err)
            })

        players = request.data
        serializer = self.get_serializer(data=date)
        serializer.is_valid(raise_exception=True)
        sess = serializer.save()
        sess.creator = request.user
        for player_name, scr in players.items():
            plyr, created = Player.objects.get_or_create(name=player_name)
            result = SessionResult.objects.create(player=plyr, result=int(scr), session=sess)
            result.save()
            plyr.save()
            sess.players.add(plyr)
            sess.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SessionResultView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    queryset = SessionResult.objects.all()
    serializer_class = SessionResultSerializer

    def create(self, request, pk=None, company_pk=None, project_pk=None):
        is_many = True if isinstance(request.data, list) else False

        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PlayerScoreView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    queryset = Player.objects.all()
    serializer_class = PlayerScoreSerializer
    filter_backends = [filters.OrderingFilter]

    @action(detail=False)
    def get_max(self, request):
        sessions = SessionResultSerializer
        try:
            max_player = Player.objects.all().annotate(total_score=Sum('sessions__result')).order_by('-total_score')[0]
        except IndexError:
            return Response({"error":"No players in database"}, status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)
        serialized = PlayerSessionSerializer(max_player)
        return Response(serialized.data, status=status.HTTP_200_OK)


class SessionView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date']
