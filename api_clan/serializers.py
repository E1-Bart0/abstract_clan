from rest_framework import serializers

from api_clan.models import ClanABS


class ClanSerializer(serializers.Serializer):
    class Meta:
        model = ClanABS
