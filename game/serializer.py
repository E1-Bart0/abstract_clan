from django.contrib.auth.models import User
from rest_framework import serializers
from game.models import GameClan, GameClanUser, GameClanChat


class ClanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameClan
        depth = 1
        fields = ['name', 'info', 'settings', 'clan_users']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class ClanUsersListSerializer(serializers.ModelSerializer):
    user = UserSerializer('user')

    class Meta:
        model = GameClanUser
        depth = 2
        fields = ['user', 'role', 'entry', 'clan']


class ClanChatSerializer(serializers.ModelSerializer):
    user_serializer = ClanUsersListSerializer
    user_serializer.Meta.fields = ['user', 'role']
    clan_user = user_serializer('clan_user')

    class Meta:
        model = GameClanChat
        depth = 1
        fields = ['text', 'pub_date', 'clan', 'type', 'clan_user']