from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import StringRelatedField, SlugRelatedField

from .models import Player, Session, SessionResult, Payment


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name')


class SessionResultSerializer(serializers.ModelSerializer):
    player = StringRelatedField(many=False)
    session = SlugRelatedField(many=False, read_only=True, slug_field='date')

    class Meta:
        model = SessionResult
        fields = ('id', 'player', 'result', 'session')


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


class PlayerCurrentScoreSerializer(serializers.ModelSerializer):
    def get_current_score(self, obj):
        return obj.get_current_score()

    current_score = SerializerMethodField()

    class Meta:
        model = Player
        fields = ('id', 'name', 'current_score')


class PlayerSessionSerializer(serializers.ModelSerializer):
    sessions = SessionResultSerializer(many=True)

    class Meta:
        model = Player
        fields = ('id', 'name', 'sessions')


class PaymentSerializer(serializers.ModelSerializer):
    payer = SlugRelatedField(many=False, queryset=Player.objects, read_only=False, slug_field='name')
    payee = SlugRelatedField(many=False, queryset=Player.objects, read_only=False, slug_field='name')
    class Meta:
        model = Payment
        fields = ('payer', 'payee', 'amount')


class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token and provider.
    """
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)
