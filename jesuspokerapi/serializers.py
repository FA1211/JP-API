from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import StringRelatedField, SlugRelatedField

from .models import Player, Session, SessionResult


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name')


class SessionResultSerializer(serializers.ModelSerializer):
    player = StringRelatedField(many=False)

    class Meta:
        model = SessionResult
        fields = ('id', 'player', 'result')


class SessionSerializer(serializers.ModelSerializer):
    results = SessionResultSerializer(many=True, required=False)
    creator = SlugRelatedField(many=False, read_only=True, slug_field='first_name')
    class Meta:
        model = Session
        fields = ('id', 'date', 'creator', 'balance', 'results')


class PlayerScoreSerializer(serializers.ModelSerializer):
    def get_total_score(self, obj):
        return obj.get_total_score()

    total_score = SerializerMethodField()

    class Meta:
        model = Player
        fields = ('id', 'name', 'total_score')


class PlayerSessionSerializer(serializers.ModelSerializer):
    sessions = SessionResultSerializer(many=True)

    class Meta:
        model = Player
        fields = ('id', 'name', 'sessions')


class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token and provider.
    """
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)