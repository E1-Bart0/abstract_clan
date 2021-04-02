from rest_framework.serializers import Serializer

from game.models import GameClan


class ClanListSerializer(Serializer):
    class Meta:
        model = GameClan
        fields = ['name', 'id']