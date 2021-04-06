from django.contrib.auth.models import User
from django.db import models
from api_clan.models import (
    ClanABS,
    ClanUserABS,
    ClanChatABS,
    ChatMessages
)


class GameClan(ClanABS):
    pass


class GameClanUser(ClanUserABS):
    clan = models.ForeignKey(GameClan, on_delete=models.CASCADE, related_name='clan_users')


class GameClanChat(ClanChatABS):
    clan = models.ForeignKey(GameClan, on_delete=models.CASCADE, related_name='chats')


class GameChatMessage(ChatMessages):
    clan_chat = models.ForeignKey(GameClanChat, on_delete=models.CASCADE, related_name='msgs')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_msgs')
