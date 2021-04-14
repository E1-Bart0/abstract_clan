from rest_framework import serializers

from game.models import GameClan, GameClanMember
from game.serializers.clan_serializer import UserSerializer, ClanSerializer


class ClanMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = GameClanMember
        fields = ['user_id', 'user', 'joined_at']


class ClanMembersListSerializer(ClanSerializer):
    id = serializers.PrimaryKeyRelatedField(required=True, queryset=GameClan.objects.all())
    all_members = ClanMemberSerializer(source='members', many=True, read_only=True)

    class Meta:
        model = GameClan
        fields = ['id', 'name', 'created_at', 'members_count', 'all_members']
