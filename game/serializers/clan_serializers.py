from django.http import QueryDict
from rest_framework import serializers

from game.models import GameClan, Game
from myuser.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class ClanSerializer(serializers.ModelSerializer):
    creator = UserSerializer(many=False, required=False, read_only=True)
    members_count = serializers.SerializerMethodField('get_members_count')
    id = serializers.PrimaryKeyRelatedField(required=True, queryset=GameClan.objects.all())

    @staticmethod
    def get_members_count(clan) -> int:
        clan = clan if isinstance(clan, GameClan) else clan.get('id')
        return clan.members.count()

    @staticmethod
    def add_to_resource_data(data: QueryDict, resource_data: dict) -> dict:
        for key in data:
            resource_data[key] = data[key][0] if len(data[key]) == 1 else data[key]
        return resource_data


class ClanListSerializer(ClanSerializer):
    class Meta:
        model = GameClan
        fields = ['id', 'name', 'description', 'max_members', 'creator', 'created_at', 'members_count']


class ClanDetailView(ClanSerializer):
    class Meta:
        model = GameClan
        depth = 1
        fields = ['id', 'name', 'description', 'max_members', 'creator', 'created_at', 'chats', 'members_count']


class ClanUpdateSerializer(ClanSerializer):

    def to_internal_value(self, data):
        user = self.context.user
        clan_id = user.my_clan.id if hasattr(user, 'my_clan') else None
        resource_data = {
            'id': clan_id,
        }
        self.add_to_resource_data(data, resource_data)
        return super().to_internal_value(resource_data)

    def validate_id(self, clan):
        if clan.creator == self.context.user:
            return clan
        raise serializers.ValidationError(f'Only creator "{clan.creator}" could made change')

    def save(self, **kwargs):
        try:
            clan = self.validated_data['id']
            for attr, value in self.validated_data.items():
                if attr != 'id':
                    setattr(clan, attr, value)
            clan.save()
            return clan
        except Exception as err:
            raise serializers.ValidationError(err)

    class Meta:
        model = GameClan
        depth = 1
        fields = ['id', 'name', 'description', 'max_members', 'creator', 'created_at', 'chats']


class ClanDeleteSerializer(ClanUpdateSerializer):

    def delete_model(self):
        clan = self.validated_data['id']
        return clan.delete()

    class Meta:
        model = GameClan
        depth = 1
        fields = ['id']


class ClanCreateSerializer(ClanSerializer):
    creator = None
    game = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all(), required=True)

    def to_internal_value(self, data):
        user = self.context.user
        resource_data = {
            'creator': user.id,
            'game': user.game.id if hasattr(user, 'game') else None,
        }
        self.add_to_resource_data(data, resource_data)
        return super().to_internal_value(resource_data)

    @staticmethod
    def validate_creator(creator):
        if hasattr(creator, 'clan_member'):
            raise serializers.ValidationError(f'{creator} already in clan {creator.clan_member.clan}')
        return creator

    def save(self, **kwargs):
        return self.Meta.model.create(**self.validated_data)

    class Meta:
        model = GameClan
        fields = ['name', 'description', 'creator', 'game', 'max_members']
