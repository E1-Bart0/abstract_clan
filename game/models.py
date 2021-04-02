from django.db import models
from api_clan.models import (
    ClanABS,
    ClanUserABS,
    ClanChatABS,
    ClanSettingsABS,
    ClanInfoABS,
    ClanUserRole,
)


class GameClanInfo(ClanInfoABS):
    pass


class GameClanSettings(ClanSettingsABS):
    pass


class ClanManager(models.Manager):

    def create(self, host, name, **kwargs):
        """
        :param host: User
        :param name: str
        :param kwargs: {'info': kwargs, 'settings': kwargs}
        :return: GameClan
        """
        params = {}
        info, settings = self.init_info__settings(kwargs)

        params['name'] = name
        params['info'] = info
        params['settings'] = settings

        clan = super().create(**params)
        clan_user = clan.clan_users.create(user=host, clan=clan, role=0)
        return clan

    def init_info__settings(self, kwargs):
        if 'info' in kwargs:
            info = GameClanInfo.objects.create(**kwargs['info'])
        else:
            info = GameClanInfo.objects.create()
        if 'settings' in kwargs:
            settings = GameClanSettings.objects.create(**kwargs['settings'])
        else:
            settings = GameClanSettings.objects.create()
        return info, settings


class GameClan(ClanABS):
    info = models.OneToOneField(GameClanInfo, on_delete=models.CASCADE)
    settings = models.OneToOneField(GameClanSettings, on_delete=models.CASCADE)

    objects = ClanManager()


class GameClanUser(ClanUserABS):
    clan = models.ForeignKey(GameClan, on_delete=models.CASCADE, related_name='clan_users')


class GameClanChat(ClanChatABS):
    clan = models.ForeignKey(GameClan, on_delete=models.CASCADE, related_name='chat')
    clan_user = models.ForeignKey(GameClanUser, on_delete=models.CASCADE, related_name='clan_user_msgs')
