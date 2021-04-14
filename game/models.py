from django.db import models
from api_clan.models.clan_abc import ClanABC
from api_clan.models.clan_chat_abc import ClanChatABC
from api_clan.models.clan_chat_message_abc import ChatMessageABC
from api_clan.models.clan_member_abc import ClanMemberABC
from myuser.models import User


class Game(models.Model):
    game = models.CharField(max_length=30, default='Game')
    slug = models.CharField(max_length=30, default='game')

    def __str__(self):
        return self.game


class GameClan(ClanABC):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class GameClanMember(ClanMemberABC):
    clan = models.ForeignKey(GameClan, on_delete=models.CASCADE, related_name='members')


class GameClanChat(ClanChatABC):
    clan = models.ForeignKey(GameClan, on_delete=models.CASCADE, related_name='chats',
                             unique=False)


class GameChatTextMessage(ChatMessageABC):
    clan_chat = models.ForeignKey(GameClanChat, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_messages')
    type = models.CharField(max_length=30, default='message')
    text = models.TextField()


class GameChatRequestResource(ChatMessageABC):
    clan_chat = models.ForeignKey(GameClanChat, on_delete=models.CASCADE, related_name='requests_resource')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_requests_resources')
    type = models.CharField(max_length=30, default='resource_request')
    text = models.CharField(default='This is a resource request', max_length=20)


class GameChatRequestItem(ChatMessageABC):
    clan_chat = models.ForeignKey(GameClanChat, on_delete=models.CASCADE, related_name='requests_item')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_requests_item')
    type = models.CharField(max_length=30, default='request_item')
    text = models.CharField(default='This is a item request', max_length=20)


class GameChatNotification(ChatMessageABC):
    clan_chat = models.ForeignKey(GameClanChat, on_delete=models.CASCADE, related_name='notifications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_notifications')
    type = models.CharField(max_length=30, default='notification')
    text = models.CharField(default='Notification', max_length=20)

