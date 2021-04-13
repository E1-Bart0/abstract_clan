from rest_framework import serializers

from game.models import GameClan, GameClanMember, GameClanChat
from myuser.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class ClanListSerializer(serializers.ModelSerializer):
    creator = UserSerializer('creator', read_only=True)
    game = serializers.SlugRelatedField(many=False, read_only=True, slug_field='game')

    class Meta:
        model = GameClan
        fields = ['id', 'name', 'description', 'max_members', 'game', 'creator', 'created_at']


class ClanDetailUpdateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(required=True, queryset=GameClan.objects.all())
    creator = UserSerializer(many=False, required=False, read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = GameClan
        depth = 1
        fields = ['name', 'description', 'max_members', 'game', 'creator', 'created_at', 'chats', 'id']

    def to_internal_value(self, data):
        user = self.context.user
        clan_id = self.context.GET.get('id')
        if not clan_id and hasattr(user, 'my_clan'):
            clan_id = user.my_clan.id
        resource_data = {
            'id': clan_id,
        }
        for key in data:
            resource_data[key] = data[key][0] if len(data[key]) == 1 else data[key]
        return super().to_internal_value(resource_data)

    def save(self, **kwargs):
        clan = self.validated_data['id']
        for attr, value in self.validated_data.items():
            if attr != 'id':
                setattr(clan, attr, value)
        clan.save()
        return clan

    def delete_model(self):
        clan = self.validated_data['id']
        return clan.delete()

class ClanCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameClan
        fields = ['name', 'description', 'creator', 'game', 'max_members']

    def to_internal_value(self, data):
        user = self.context.user
        resource_data = {
            'creator': user.id,
            'game': user.game.id if hasattr(user, 'game') else None,
        }
        for key in data:
            resource_data[key] = data[key][0] if len(data[key]) == 1 else data[key]
        return super().to_internal_value(resource_data)








class ClanUsersListSerializer(serializers.ModelSerializer):
    user = UserSerializer('user')

    class Meta:
        model = GameClanMember
        depth = 2
        fields = ['user', 'joined_at', 'clan']


class ClanChatSerializer(serializers.ModelSerializer):
    user_serializer = ClanUsersListSerializer
    user_serializer.Meta.fields = ['user', ]

    class Meta:
        model = GameClanChat
        depth = 1
        fields = ['clan', 'name']
