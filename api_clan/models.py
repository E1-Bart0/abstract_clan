from django.contrib.auth.models import User
from django.db import models


class ClanUserRole(models.IntegerChoices):
    """Role Choices"""
    admin = 0, 'admin'
    player = 1, 'player'


class ClanUserABS(models.Model):
    """
    Abstract model for Clan User.
    !!! When inherit: clan -> Ref to your Clan model needed with related_name 'clan_user'

        Example:
        clan = models.ForeignKey(GameClan, on_delete=models.CASCADE, related_name='clan_users')
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    role = models.PositiveSmallIntegerField(choices=ClanUserRole.choices, default=1)
    entry = models.DateTimeField(auto_now_add=True)
    clan = None

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        """Deleting Clan Model if no users """
        if self.clan.members_count == 1:
            self.clan.delete()
        return super().delete(*args, **kwargs)


class ClanInfoABS(models.Model):
    """
    Abstract model for Clan Info
    """
    description = models.TextField(default='Clan description')
    rating = models.IntegerField(default=0)

    class Meta:
        abstract = True


class ClanSettingsABS(models.Model):
    """
    Abstract model for Clan Settings
    """
    open_close = models.BooleanField(default=True)
    min_rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ClanChatABS(models.Model):
    """
    Abstract model for Clan Chat.
    !!! When inherit: clan -> Ref to your Clan model needed with related_name 'chat'
                      user -> Ref to your Clan User model needed with related_name 'user_msgs'

        Example:
        clan = models.ForeignKey(GameClan, on_delete=models.CASCADE, related_name='chat')
        clan_user = models.ForeignKey(GameClanUser, on_delete=models.CASCADE, related_name='clan_user_msgs')
    """
    type = models.CharField(max_length=30, default='message')
    text = models.TextField(null=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    clan = None
    user = None

    class Meta:
        abstract = True


class ClanManager(models.Manager):
    """
    Clan Manager. Needed for Clan.objects.create
    !!! When inherit: info -> Ref to GameClanInfo
                      settings -> Ref to Game clanSettings

        Example:
        info = GameClanInfo
        settings = GameClanSettings
    """
    info = None
    settings = None

    def create(self, host, name, **kwargs):
        """
        Creating ClanInfo, ClanSettings, ClanUser(admin) with Clan creation

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
        clan.clan_users.create(user=host, clan=clan, role=0)
        return clan

    def init_info__settings(self, kwargs):
        """Creating ClanInfo and ClanSettings with your params

        :param kwargs: {'info' : {'description': str, ...}, {'settings' : {'min_rating' : int, ...}}
        :return ClanInfo, ClanSettings
        """
        if 'info' in kwargs:
            info = self.info.objects.create(**kwargs['info'])
        else:
            info = self.info.objects.create()
        if 'settings' in kwargs:
            settings = self.settings.objects.create(**kwargs['settings'])
        else:
            settings = self.settings.objects.create()
        return info, settings


class ClanABS(models.Model):
    """
    Abstract model for Clan.
    !!! When inherit: info -> Ref to your ClanInfo model needed.
                      settings -> Ref to your ClanSettings model needed.
                      objects -> Ref to your ClanManager model needed.

        Example:
        info = models.OneToOneField(GameClanInfo, on_delete=models.CASCADE)
        settings = models.OneToOneField(GameClanSettings, on_delete=models.CASCADE)
        objects = GameClanManager()
    """
    name = models.CharField(max_length=60, unique=True)
    info = None
    settings = None
    objects = None

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

    @property
    def get_users(self):
        """Getting all users by related name in ClanUser on Clan (clan_users)"""
        return self.clan_users.all()

    @property
    def members_count(self):
        """Getting users count in clan"""
        return self.get_users.count()

    @property
    def get_messages(self):
        """Getting all messages by related_name on Clan in ClanChat (chat)"""
        return self.chat.all()

    @property
    def oldest_user(self):
        """Getting oldest user by related_name on Clan in ClanUser (clan_users)"""
        return self.clan_users.order_by('entry').first()

    @property
    def get_all_admins(self):
        """Getting all users if they admin"""
        return self.get_users.filter(role=ClanUserRole.admin).all()

    @staticmethod
    def _update(model, new_values, model_name):
        """Updating model by new_values"""
        model_dict = model.__dict__
        for key, value in new_values.items():
            if key not in model_dict:
                raise ModuleNotFoundError(f'Not field "{key}" in {model_name}')
            model_dict[key] = value
        model.save()

    def update_info(self, **kwargs):
        """Changing ClanInfo model"""
        self._update(self.info, kwargs, 'Clan Info')

    def update_settings(self, **kwargs):
        """Changing ClanInfo model"""
        self._update(self.settings, kwargs, 'Clan Settings')

    def send_msg(self, user, **kwargs):
        """
        Creating new ClanMessage with type message
        :param user: User
        :param kwargs: {'text': str}
        :return: ClanMessage
        """
        return self._create_msg_with_type(user=user, type='message', kwargs=kwargs)

    def send_request(self, user, **kwargs):
        """
        Creating new ClanMessage with type request
        :param user: User
        :param kwargs: {'text': str}
        :return: ClanMessage
        """
        return self._create_msg_with_type(user=user, type='request', kwargs=kwargs)

    def _create_msg_with_type(self, user, type, kwargs):
        """Creating new ClanMessage by related_name on Clan in ClanChat (chat) and on Clan in ClanUser (clan_users)"""
        clan_user = self.clan_users.filter(user=user).first()
        msg = self.chat.create(clan=self, clan_user=clan_user, type=type, **kwargs)
        return msg

    def get_all_user_msgs(self, user):
        """Get all user ClanMessage by related_name on ClanUser in ClanChat (clan_user_msgs)
             and on Clan in ClanUser (clan_users)"""
        clan_user = self.clan_users.filter(user=user).first()
        return clan_user.clan_user_msgs.all()

    def join(self, user, **kwargs):
        """Create new ClanUser"""
        clan_user = self.clan_users.create(clan=self, user=user, **kwargs)
        return clan_user

    def exit(self, user):
        """Deleting ClanUser. If user is admin checking others users and if no more admins in clan,
            making oldest user admin"""
        clan_user = self.clan_users.filter(user=user)
        if clan_user.exists():
            clan_user = clan_user.first()
            clan_user_role = clan_user.role
            clan_user.delete()

            if not self.members_count:
                return
            self.change_admin(clan_user_role)

    def change_admin(self, clan_user_role):
        """Give admin to oldest user if no more admins in clan"""
        if clan_user_role == ClanUserRole.admin and not \
                len(list(filter(lambda u: u.role == ClanUserRole.admin, self.get_users))):
            self.give_role_to(self.oldest_user)

    def give_role_to(self, user, role=ClanUserRole.admin):
        """Giving admin to user. Needed related_name in ClanUsers on Clan (clan_users)"""
        clan_user = self.clan_users.filter(user=user)
        if clan_user.exists():
            clan_user = clan_user.first()
            clan_user.role = role
            clan_user.save()

    def delete(self, *args, **kwargs):
        """Deleting ClanInfo and ClanSettings while ClanDelete
            ClanUsers and ClanChats will be deleted automatically"""
        self.info.delete()
        self.settings.delete()
        return super().delete(*args, **kwargs)
