from rest_framework import serializers

from api_clan.models import ClanABC


class ClanSerializer(serializers.Serializer):
    class Meta:
        model = ClanABC
