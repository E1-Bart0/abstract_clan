from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from game.models import GameClan, GameClanMember, GameClanChat


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class ClanListSerializer(serializers.ModelSerializer):
    creator = UserSerializer('creator', read_only=True, required=False)
    required = ('name', 'description', 'game', 'creator')

    def is_valid(self, raise_exception=False):
        try:
            request = self.context.get('request')
            add_data = {}
            add_data['creator'] = request.user
            add_data['game'] = request.user.game
            self.to_internal_value(data=add_data)
        except AttributeError:
            raise_exception = True
        return super().is_valid(raise_exception)


    class Meta:
        model = GameClan
        depth = 1
        fields = ['name', 'game', 'description', 'creator', 'chats']


def save(self):
    print('aaa', self.initial_data)
    print(self.validated_data)
    # return GameClan.create(**self.validated_data)


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
