from django.db import models
from api_clan.models import (
    ClanABS,
    ClanMemberABS,
    ClanChatABS,
    ChatMessageABS
)
from myuser.models import User


class Game(models.Model):
    game = models.CharField(max_length=30, default='Game')
    slug = models.CharField(max_length=30, default='game')

    def __str__(self):
        return self.game


class GameClan(ClanABS):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class GameClanMember(ClanMemberABS):
    clan = models.ForeignKey(GameClan, on_delete=models.CASCADE, related_name='members')


class GameClanChat(ClanChatABS):
    clan = models.ForeignKey(GameClan, on_delete=models.CASCADE, related_name='chats',
                             unique=False)


class GameChatTextMessage(ChatMessageABS):
    clan_chat = models.ForeignKey(GameClanChat, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_messages')
    type = models.CharField(max_length=30, default='message')
    text = models.TextField()


class GameChatRequestResource(ChatMessageABS):
    clan_chat = models.ForeignKey(GameClanChat, on_delete=models.CASCADE, related_name='resource_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_resource_requests')
    type = models.CharField(max_length=30, default='resource_request')
    text = models.CharField(default='This is a resource request', max_length=20)


class GameChatRequestItem(ChatMessageABS):
    clan_chat = models.ForeignKey(GameClanChat, on_delete=models.CASCADE, related_name='items_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_items_requests')
    type = models.CharField(max_length=30, default='request_item')
    text = models.CharField(default='This is a item request', max_length=20)
