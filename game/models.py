from django.db import models
from api_clan.models import (
    ClanABS,
    ClanUserABS,
    ClanChatABS,
    ClanSettingsABS,
    ClanInfoABS,
    ClanManager
)


class GameClanInfo(ClanInfoABS):
    pass


class GameClanSettings(ClanSettingsABS):
    pass


class GameClanManager(ClanManager):
    info = GameClanInfo
    settings = GameClanSettings


class GameClan(ClanABS):
    info = models.OneToOneField(GameClanInfo, on_delete=models.CASCADE)
    settings = models.OneToOneField(GameClanSettings, on_delete=models.CASCADE)

    objects = GameClanManager()


class GameClanUser(ClanUserABS):
    clan = models.ForeignKey(GameClan, on_delete=models.CASCADE, related_name='clan_users')


class GameClanChat(ClanChatABS):
    clan = models.ForeignKey(GameClan, on_delete=models.CASCADE, related_name='chat')
    clan_user = models.ForeignKey(GameClanUser, on_delete=models.CASCADE, related_name='clan_user_msgs')
