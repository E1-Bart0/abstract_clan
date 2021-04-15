from rest_framework import serializers

from game.models import GameClan, GameClanMember
from game.serializers.clan_serializers import UserSerializer, ClanSerializer
from myuser.models import User


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


class ClanMemberJoinSerializer(ClanSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)

    class Meta:
        model = GameClan
        fields = ['id', 'user']

    @staticmethod
    def validate_user(user):
        if hasattr(user, 'clan_member') or hasattr(user, 'my_clan'):
            raise serializers.ValidationError(f'"{user}" already in clan "{user.clan_member.clan.name}"')
        return user

    def add_member(self):
        clan = self.validated_data.get('id')
        user = self.validated_data.get('user')
        clan.add(user)
