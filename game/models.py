from django.contrib.auth.models import User
from django.db import models
from api_clan.models import (
    ClanABS,
    ClanUserABS,
    ClanChatABS,
    ChatMessages
)


class Game(models.Model):
    game = models.CharField(max_length=30, default='Game')
    slug = models.CharField(max_length=30, default='game')

    def __str__(self):
        return self.game


class GameClan(ClanABS):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class GameClanUser(ClanUserABS):
    clan = models.ForeignKey(GameClan, on_delete=models.CASCADE, related_name='clan_users')


class GameClanChat(ClanChatABS):
    chat_id = models.AutoField(primary_key=True)
    clan = models.ForeignKey(GameClan, on_delete=models.CASCADE, related_name='chats', unique=False)
    name = models.CharField(max_length=30, null=True, unique=True)



class GameChatMessage(ChatMessages):
    clan_chat = models.ForeignKey(GameClanChat, on_delete=models.CASCADE, related_name='msgs')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_msgs')
